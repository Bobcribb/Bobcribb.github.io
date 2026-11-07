"""Pure, offline tests of the MYTHOS image verification guard."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from scripts.verify_photoreal_gallery import ImagesInGallery, gallery_markup_failures, inventory, is_webp, verify_once


class TestPhotorealGalleryVerification(unittest.TestCase):
    def test_public_image_does_not_replace_missing_scientific_notice(self):
        entry = {"slug": "temple", "src": "/assets/reconstitutions-3d/temple.webp",
                 "source_url": "https://museum.example/temple"}
        valid = '''<article id="temple"><figure>
        <img src="/assets/reconstitutions-3d/temple.webp" alt="Temple interprétatif">
        <figcaption>Temple, IVe siècle</figcaption></figure>
        <div class="r3d-science"><p>Les vestiges attestent le plan.</p>
        <p>Degré de certitude : élevé pour le plan.</p>
        <a href="https://museum.example/temple">Source institutionnelle</a></div></article>'''
        self.assertEqual(gallery_markup_failures(valid, [entry]), [])
        for broken in (
            valid.replace('<figcaption>Temple, IVe siècle</figcaption>', ''),
            valid.replace('class="r3d-science"', 'class="removed"'),
            valid.replace('https://museum.example/temple', 'https://museum.example/other'),
            valid.replace('id="temple"', 'id="removed"'),
            valid.replace('<article ', '<article hidden '),
            valid + '<img src="/assets/reconstitutions/temple.svg">',
        ):
            with self.subTest(markup=broken):
                self.assertTrue(gallery_markup_failures(broken, [entry]))

    def test_scientific_notice_json_must_be_served_and_match_build(self):
        base = "https://bobmythos.fr"
        image = "/assets/reconstitutions-3d/kassope-test.webp"
        notice = "/assets/reconstitutions-3d/notices/kassope-test.json"
        entry = {"slug": "kassope-test", "src": image, "source_url": "https://example.org/kassope",
                 "scientific_notice": notice}
        catalog = {"count": 1, "entries": [entry]}
        markup = (f'<article id="kassope-test"><figure><img src="{image}" alt="Agora de Kassopè">'
                  '<figcaption>Restitution hypothétique</figcaption></figure>'
                  '<div class="r3d-science"><p>Degré de certitude faible pour les élévations.</p>'
                  '<a href="https://example.org/kassope">Source</a></div></article>')
        webp = b"RIFF" + b"\x04\x00\x00\x00" + b"WEBP" + b"test"
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for resource, contents in ((image, webp), (notice, b'{"id":"KAS-AGO-001"}')):
                target = root / resource.lstrip("/")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(contents)
            responses = {
                "/assets/reconstitutions-3d/catalogue-photorealiste.json":
                    (200, json.dumps(catalog).encode("utf-8")),
                "/reconstitutions-photorealistes.html": (200, markup.encode("utf-8")),
                image: (200, webp),
                notice: (200, b'{"id":"KAS-AGO-001"}'),
            }

            def fake_request(url):
                return responses[url.removeprefix(base)]

            with patch("scripts.verify_photoreal_gallery.request_bytes", side_effect=fake_request):
                good = verify_once(base, root, catalog, [entry])
                self.assertEqual(good["verified_images"], 1)
                self.assertEqual(good["verified_notices"], 1)
                self.assertEqual(good["failures"], [])
                responses[notice] = (404, b"missing")
                missing = verify_once(base, root, catalog, [entry])
                self.assertEqual(missing["verified_notices"], 0)
                self.assertTrue(any("HTTP 404" in v["error"] for v in missing["failures"]))
                responses[notice] = (200, b'{"id":"WRONG"}')
                stale = verify_once(base, root, catalog, [entry])
                self.assertTrue(any("différente" in v["error"] for v in stale["failures"]))

    def test_legacy_notice_without_declared_url_is_verified_on_https(self):
        """Les notices historiques sans champ scientific_notice ne sont pas ignorées."""
        base = "https://bobmythos.fr"
        slug = "delphes-legacy"
        image = "/assets/reconstitutions-3d/" + slug + ".webp"
        notice = "/assets/reconstitutions-3d/notices/" + slug + ".json"
        entry = {"slug": slug, "src": image,
                 "source_url": "https://museum.example/delphes"}
        catalog = {"count": 1, "entries": [entry]}
        markup = (
            '<article id="' + slug + '"><figure><img src="' + image
            + '" alt="Restitution hypothétique de Delphes">'
            '<figcaption>Delphes, vue archéologique</figcaption></figure>'
            '<div class="r3d-science"><p>Degré de certitude : faible pour les élévations.</p>'
            '<a href="https://museum.example/delphes">Source archéologique</a>'
            '</div></article>'
        )
        webp = b"RIFF\x04\x00\x00\x00WEBPtest"
        original_notice = b'{"id":"DEL-OLD-001","title":"Delphes"}'
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for path, payload in ((image, webp), (notice, original_notice)):
                local = root / path.lstrip("/")
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_bytes(payload)
            responses = {
                "/assets/reconstitutions-3d/catalogue-photorealiste.json":
                    (200, json.dumps(catalog).encode("utf-8")),
                "/reconstitutions-photorealistes.html":
                    (200, markup.encode("utf-8")),
                image: (200, webp),
                notice: (200, original_notice),
            }
            with patch("scripts.verify_photoreal_gallery.request_bytes",
                       side_effect=lambda url: responses[url.removeprefix(base)]):
                valid = verify_once(base, root, catalog, [entry])
                self.assertEqual(valid["expected_notices"], 1)
                self.assertEqual(valid["verified_notices"], 1)
                self.assertEqual(valid["failures"], [])
                self.assertNotIn("scientific_notice", entry)

                responses[notice] = (404, b"missing")
                missing = verify_once(base, root, catalog, [entry])
                self.assertEqual(missing["expected_notices"], 1)
                self.assertEqual(missing["verified_notices"], 0)
                self.assertTrue(any("HTTP 404" in failure["error"]
                                    for failure in missing["failures"]))

                responses[notice] = (200, b'{"id":"WRONG"}')
                changed = verify_once(base, root, catalog, [entry])
                self.assertTrue(any("différente" in failure["error"]
                                    for failure in changed["failures"]))

    def test_webp_signature(self):
        self.assertTrue(is_webp(b"RIFF" + b"\x04\x00\x00\x00" + b"WEBP" + b"abc"))
        self.assertFalse(is_webp(b"<html>404 not found</html>"))
        self.assertFalse(is_webp(b"RIFF" + b"\x04\x00\x00\x00" + b"PNG "))

    def test_image_src_is_a_real_img_tag(self):
        parser = ImagesInGallery()
        parser.feed('<a href="/x.webp">image</a><img loading="lazy" src="/assets/reconstitutions-3d/x.webp">')
        self.assertEqual(parser.sources, {"/assets/reconstitutions-3d/x.webp"})

    def test_duplicate_slug_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "assets/reconstitutions-3d/catalogue-photorealiste.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"count": 2, "entries": [
                {"slug": "duplicate", "src": "/assets/reconstitutions-3d/a.webp"},
                {"slug": "duplicate", "src": "/assets/reconstitutions-3d/b.webp"}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dupliqués"):
                inventory(root)


    def test_index_references_all_published_3d_notices(self):
        from bs4 import BeautifulSoup
        from shutil import copy2
        from scripts.sync_reconstitution_index import sync_index

        repo = Path(__file__).resolve().parents[1]
        gallery = repo / 'reconstitutions-photorealistes.html'
        manifest = repo / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / 'reconstitutions-photorealistes.html'
            catalog = root / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
            catalog.parent.mkdir(parents=True, exist_ok=True)
            copy2(gallery, target)
            copy2(manifest, catalog)
            sync_index(root)
            self.assertEqual(sync_index(root), 0, 'Sommaire 3D non idempotent')
            entries = json.loads(catalog.read_text(encoding='utf-8'))['entries']
            doc = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
            cards = doc.select('nav.r3d-index a.r3d-index-image[href^="#"]')
            self.assertEqual(len(cards), len(entries))
            links = {card['href'][1:]: card for card in cards}
            self.assertEqual(len(links), len(entries), 'Sommaire 3D dupliqué')
            for item in entries:
                with self.subTest(slug=item['slug']):
                    card = links[item['slug']]
                    self.assertEqual(card.img.get('src'), item['src'])
                    self.assertIsNotNone(doc.find('article', id=item['slug']))

    def test_index_sync_repairs_missing_thumbnail(self):
        from bs4 import BeautifulSoup
        from scripts.sync_reconstitution_index import sync_index

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / 'reconstitutions-photorealistes.html'
            page.write_text(
                '<html><body><p><strong>État du corpus : 0 reconstitutions.</strong></p>'
                '<nav class="r3d-index"><div class="r3d-index-grid">'
                '</div></nav><article class="r3d-card" id="delphes-temple">'
                '<h2>Delphes</h2></article></body></html>', encoding='utf-8')
            catalog = root / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps({'count': 1, 'entries': [{
                'slug': 'delphes-temple',
                'title': 'Delphes — temple',
                'src': '/assets/reconstitutions-3d/delphes-temple.webp',
                'source_url': 'https://example.org/delphes',
            }]}), encoding='utf-8')
            self.assertEqual(sync_index(root), 1)
            html_once = page.read_text(encoding='utf-8')
            self.assertEqual(sync_index(root), 0)
            self.assertEqual(page.read_text(encoding='utf-8'), html_once)
            self.assertIn('État du corpus : 1 reconstitution.', html_once)
            # Corriger également une valeur obsolète sans modifier les cartes.
            page.write_text(html_once.replace('État du corpus : 1 reconstitution.',
                                              'État du corpus : 99 reconstitutions.'),
                            encoding='utf-8')
            self.assertEqual(sync_index(root), 0)
            self.assertEqual(page.read_text(encoding='utf-8'), html_once)
            doc = BeautifulSoup(html_once, 'html.parser')
            card = doc.select_one('nav.r3d-index a[href="#delphes-temple"]')
            self.assertIsNotNone(card)
            self.assertEqual(card.img.get('src'),
                             '/assets/reconstitutions-3d/delphes-temple.webp')


if __name__ == "__main__":
    unittest.main()
