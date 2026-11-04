"""Pure, offline tests of the MYTHOS image verification guard."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.verify_photoreal_gallery import ImagesInGallery, gallery_markup_failures, inventory, is_webp


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
                '<html><body><nav class="r3d-index"><div class="r3d-index-grid">'
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
            doc = BeautifulSoup(html_once, 'html.parser')
            card = doc.select_one('nav.r3d-index a[href="#delphes-temple"]')
            self.assertIsNotNone(card)
            self.assertEqual(card.img.get('src'),
                             '/assets/reconstitutions-3d/delphes-temple.webp')


if __name__ == "__main__":
    unittest.main()
