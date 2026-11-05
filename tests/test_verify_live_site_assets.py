"""Régression : les SVG, JPEG et WebP des monographies doivent être publiés à l'identique."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify_live_site as live


PAGES = ("philosophie-iliade.html", "philosophie-odyssee.html",
         "philosophie-theogonie.html")
ASSET = "/assets/philosophie/test-regression.svg"
SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><title>Test</title></svg>'


class PhilosophySVGPublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        asset = self.root / ASSET.lstrip("/")
        asset.parent.mkdir(parents=True)
        asset.write_bytes(SVG)
        for page in PAGES:
            (self.root / page).write_text(
                '<!doctype html><html><body><img src="' + ASSET
                + '" alt="Schéma documentaire"></body></html>', encoding="utf-8")

    def test_inventory_finds_pages_and_checks_original_bytes(self):
        pages, digests = live.svg_inventory(self.root)
        self.assertEqual(set(pages), set(PAGES))
        self.assertEqual(set(digests), {ASSET})
        self.assertEqual(digests[ASSET], hashlib.sha256(SVG).hexdigest())

    def test_public_svg_must_match_source_and_be_referenced_in_html(self):
        def good_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == ASSET:
                return (200, "image/svg+xml", SVG)
            return (200, "text/html", (self.root / path.lstrip("/")).read_bytes())

        with patch.object(live, "fetch", side_effect=good_fetch):
            self.assertTrue(all(x["valid"] for x in
                                live.verify_public_svgs("https://example.test", self.root)))

        def outdated_fetch(url):
            if url.endswith(".svg"):
                return (200, "image/svg+xml", SVG + b"<!-- altered -->")
            return good_fetch(url)

        with patch.object(live, "fetch", side_effect=outdated_fetch):
            report = live.verify_public_svgs("https://example.test", self.root)
        self.assertEqual(len([x for x in report if not x["valid"]]), 1)
        self.assertEqual([x["url"] for x in report if not x["valid"]], [ASSET])


class FigureAndReceiptGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.files = {}
        for page, (fid, src) in live.TARGET_FIGURES.items():
            data = (b'<svg xmlns="http://www.w3.org/2000/svg"></svg>' if src.endswith(".svg")
                    else b"RIFF" + b"\x08\x00\x00\x00" + b"WEBP" + b"VP8 ")
            image = self.root / src.lstrip("/")
            image.parent.mkdir(parents=True, exist_ok=True)
            image.write_bytes(data)
            self.files[src] = data
            markup = ('<html><figure id="' + fid + '" data-image-status="création 2026">'
                      '<img src="' + src + '" alt="Vue documentée">'
                      '<figcaption>Légende historique et statut. '
                      '<a href="https://example.org/source">Source institutionnelle</a>'
                      '</figcaption></figure></html>').encode("utf-8")
            path = self.root / page
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(markup)
            self.files["/" + page] = markup

    def live_fetch(self, url):
        return (200, "data", self.files[url.split("https://example.test", 1)[-1]])

    def test_local_inventory_and_matching_public_figures(self):
        pages, assets = live.figure_inventory(self.root)
        self.assertEqual(len(pages), 6)
        self.assertEqual(len(assets), 6)
        with patch.object(live, "fetch", side_effect=self.live_fetch):
            report = live.verify_public_figures("https://example.test", self.root)
        self.assertEqual(len(report), 12)
        self.assertTrue(all(x["valid"] for x in report))

    def test_outdated_figure_and_changed_webp_are_detected(self):
        def broken(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/livre-hesiode/index.html":
                return (200, "text/html", b"<html>Ancien document</html>")
            if path.endswith("eleusis-telesterion-sanctuaire-panorama.webp"):
                return (200, "image/webp", self.files[path] + b"changed")
            return self.live_fetch(url)
        with patch.object(live, "fetch", side_effect=broken):
            bad = [r["url"] for r in live.verify_public_figures(
                "https://example.test", self.root) if not r["valid"]]
        self.assertIn("/livre-hesiode/index.html", bad)
        self.assertIn("/assets/reconstitutions-3d/eleusis-telesterion-sanctuaire-panorama.webp", bad)

    def test_missing_caption_status_is_not_accepted(self):
        page = self.root / "livre-hesiode/index.html"
        page.write_text(page.read_text(encoding="utf-8").replace(
            'data-image-status="création 2026"', ''), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Notice"):
            live.figure_inventory(self.root)

    def test_stale_public_receipt_fails_even_if_catalogue_is_unchanged(self):
        receipt = self.root / "catalog/publication-verification.json"
        receipt.parent.mkdir(parents=True)
        receipt.write_text(json.dumps({"source_commit": "nouveau", "github_run_id": 1}))
        with patch.object(live, "fetch", return_value=(
            200, "json", b'{"source_commit":"nouveau","github_run_id":1}')):
            self.assertTrue(live.verify_public_receipt("https://example.test", self.root))
        with patch.object(live, "fetch", return_value=(
            200, "json", b'{"source_commit":"ancien","github_run_id":1}')):
            self.assertFalse(live.verify_public_receipt("https://example.test", self.root))


class RecentFigurePublicationTests(unittest.TestCase):
    """Recent documented figures must be independently verified, even on a shared page."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.assets = {}
        per_page = {}
        for page, fid, src in live.RECENT_FIGURES:
            content = (b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"mock-webp"
                       if src.lower().endswith(".webp")
                       else bytes.fromhex("ffd8ff") + b"mock-jpeg-binary")
            asset = self.root / src.lstrip("/")
            asset.parent.mkdir(parents=True, exist_ok=True)
            asset.write_bytes(content)
            self.assets[src] = content
            figure = ('<figure id="' + fid + '" data-image-status="photographie antique">'
                      '<img src="' + src + '" alt="Document photographique">'
                      '<figcaption>Image historique, datée, avec licence et '
                      '<a href="https://example.org/notice">source institutionnelle</a>.'
                      '</figcaption></figure>')
            per_page.setdefault(page, []).append(figure)
        self.pages = {}
        for page, figures in per_page.items():
            raw = ('<!doctype html><html><body>' + "".join(figures) +
                   '</body></html>').encode("utf-8")
            file = self.root / page
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(raw)
            self.pages["/" + page] = raw

    def fetch(self, url):
        path = url.split("https://example.test", 1)[-1]
        if path in self.assets:
            kind = "image/webp" if path.lower().endswith(".webp") else "image/jpeg"
            return (200, kind, self.assets[path])
        return (200, "text/html", self.pages[path])

    def test_all_forty_documentary_figures_and_six_pages_verified(self):
        pages, assets = live.recent_figure_inventory(self.root)
        self.assertEqual(len(pages), 6)
        self.assertEqual(len(pages["livre-iliade-scenes/index.html"]), 4)
        self.assertEqual(len(pages["livre-odyssee/index.html"]), 5)
        self.assertEqual(len(pages["livre-hesiode/index.html"]), 5)
        self.assertEqual(len(pages["philosophie-iliade.html"]), 9)
        self.assertEqual(len(pages["philosophie-odyssee.html"]), 9)
        self.assertEqual(len(pages["philosophie-theogonie.html"]), 8)
        self.assertEqual(len(assets), 32)
        self.assertEqual(sum(len(items) for items in pages.values()), 40)
        # Rembrandt est réutilisé entre l’étude philosophique et le livre.
        shared = "/assets/illustrations-articles/met-437394-aristote-homere-rembrandt.webp"
        self.assertIn(shared, assets)
        self.assertEqual(sum(src == shared for _, _, src in live.RECENT_FIGURES), 2)
        with patch.object(live, "fetch", side_effect=self.fetch):
            report = live.verify_recent_public_figures("https://example.test", self.root)
        # The verifier reports one result per HTML page and one per unique
        # binary asset, not one result for every figure. Cross-page reuse
        # therefore produces fewer network checks than figure occurrences.
        self.assertEqual(len(report), len(pages) + len(assets))
        self.assertTrue(all(item["valid"] for item in report))
        self.assertEqual(sum(item.get("figures_verified", 0) for item in report), 40)

    def test_session_42_scientific_figures_fail_on_stale_page_or_tampered_webp(self):
        """Three Met notices and binary assets must appear unchanged on HTTPS."""
        additions = (
            ("philosophie-iliade.html", "icono-iliade-enee-limoges-reception-met-199612-20261105",
             "/assets/illustrations-articles/met-199612-enee-fuite-troie-email.webp"),
            ("philosophie-odyssee.html", "icono-odyssee-ariane-thesee-met-245585-20261105",
             "/assets/illustrations-articles/met-245585-thesee-ariane-sarcophage.webp"),
            ("philosophie-theogonie.html", "icono-theogonie-tyche-oceanide-met-246414-20261105",
             "/assets/illustrations-articles/met-246414-tyche-fortuna-bronze.webp"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def stale_fetch(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"old-page-without-met-notice"))
                    if path == src:
                        return (200, "image/webp", self.assets[path] + b"tampered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=stale_fetch):
                    report = live.verify_recent_public_figures(
                        "https://example.test", self.root)
                failures = {item["url"] for item in report if not item["valid"]}
                self.assertEqual(failures, {"/" + page, src})

    def test_session_44_met_museum_figures_and_media_are_required(self):
        """Both old public pages and altered JPEG/WebP binaries must fail."""
        additions = (
            ("philosophie-iliade.html", "icono-iliade-apollon-patrocle-tete-chypre-20261105",
             "/assets/illustrations-articles/met-242366-apollon-tete-chypre.webp"),
            ("philosophie-odyssee.html", "icono-odyssee-athena-navale-lecythe-brygos-20261105",
             "/media/2026/10/mythos-athena-lecythe-brygos-aplaste-met-25-189-1.jpg"),
            ("philosophie-theogonie.html", "icono-theogonie-hecate-hekatation-romain-20261105",
             "/media/2026/10/mythos-hecate-triple-graces-met-1987-11-2.jpg"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def stale_fetch(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"old-page-without-figure"))
                    if path == src:
                        return (200, "image/webp" if src.endswith(".webp") else "image/jpeg",
                                self.assets[path] + b"tampered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=stale_fetch):
                    report = live.verify_recent_public_figures("https://example.test", self.root)
                self.assertEqual({r["url"] for r in report if not r["valid"]},
                                 {"/" + page, src})

    def test_session_46_three_archaeological_figures_are_required_on_public_site(self):
        """A stale notice and altered JPEG bytes are rejected for each of three figures."""
        additions = (
            ("philosophie-iliade.html", "icono-iliade-thetis-armure-deepdene-met-254187-20261105",
             "/media/2026/10/mythos-helene-menelas-stamnos-deepdene-met-41-162-20.jpg"),
            ("philosophie-odyssee.html", "icono-odyssee-artemision-zeus-poseidon-attribution-20261105",
             "/media/2026/10/mythos-bronze-artemision-zeus-ou-poseidon.jpg"),
            ("philosophie-theogonie.html", "icono-theogonie-poseidon-berlin-met-254184-20261105",
             "/media/2026/10/met-poseidon-berlin-painter-41-162-17.jpg"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def stale_fetch(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"missing-session-46-figure"))
                    if path == src:
                        return (200, "image/jpeg", self.assets[path] + b"tampered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=stale_fetch):
                    report = live.verify_recent_public_figures(
                        "https://example.test", self.root)
                self.assertEqual(
                    {item["url"] for item in report if not item["valid"]},
                    {"/" + page, src})

    def test_stale_odyssey_figure_and_tampered_jpeg_are_detected(self):
        def stale_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/livre-odyssee/index.html":
                return (200, "text/html", self.pages[path].replace(
                    b"mythos-odyssee-pylos-palais-nestor-20261104",
                    b"missing-pylos-figure"))
            if path.endswith("odyssee-04.jpg"):
                return (200, "image/jpeg", self.assets[path] + b"altered")
            return self.fetch(url)
        with patch.object(live, "fetch", side_effect=stale_fetch):
            report = live.verify_recent_public_figures("https://example.test", self.root)
        broken = [r for r in report if not r["valid"]]
        self.assertEqual({r["url"] for r in broken}, {
            "/livre-odyssee/index.html",
            "/assets/philosophie/documents/odyssee-04.jpg"})

    def test_five_latest_notices_and_images_are_required(self):
        """Detect a stale Hesiod page and corrupted museum photograph."""
        def stale_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/livre-hesiode/index.html":
                return (200, "text/html", self.pages[path].replace(
                    b"icono-hesiode-livre-rhea-cronos-20261104",
                    b"absent-hesiode-rhea"))
            if path.endswith("mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg"):
                return (200, "image/jpeg", self.assets[path] + b"tampered")
            return self.fetch(url)
        with patch.object(live, "fetch", side_effect=stale_fetch):
            report = live.verify_recent_public_figures("https://example.test", self.root)
        failures = {item["url"] for item in report if not item["valid"]}
        self.assertEqual(failures, {
            "/livre-hesiode/index.html",
            "/media/2026/10/mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg",
        })

    def test_recent_webp_and_stale_reception_figure_detected(self):
        """A stale Ottley notice and altered Parker/Flaxman WebP must fail."""
        altered = ("/assets/illustrations-articles/"
                   "met-705224-ulysse-circe-flaxman.webp")

        def stale_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/philosophie-theogonie.html":
                return (200, "text/html", self.pages[path].replace(
                    b"icono-theogonie-ottley-nuit-enfants-attribution-20261104",
                    b"missing-ottley-figure"))
            if path == altered:
                return (200, "image/webp", self.assets[path] + b"tampered")
            return self.fetch(url)

        with patch.object(live, "fetch", side_effect=stale_fetch):
            results = live.verify_recent_public_figures("https://example.test", self.root)
        self.assertEqual({item["url"] for item in results if not item["valid"]}, {
            "/philosophie-theogonie.html", altered,
        })

    def test_latest_museum_stale_nike_caption_and_tampered_rembrandt_detected(self):
        """A stale Nyx-family icon and altered Rembrandt image must fail."""
        source = ("/assets/illustrations-articles/"
                  "met-437394-aristote-homere-rembrandt.webp")

        def wrong_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/philosophie-theogonie.html":
                return (200, "text/html", self.pages[path].replace(
                    b"icono-theogonie-nike-styx-met-247903-20261104",
                    b"old-theogonie-without-nike"))
            if path == source:
                return (200, "image/webp", self.assets[path] + b"changed")
            return self.fetch(url)

        with patch.object(live, "fetch", side_effect=wrong_fetch):
            results = live.verify_recent_public_figures("https://example.test", self.root)
        self.assertEqual({item["url"] for item in results if not item["valid"]}, {
            "/philosophie-theogonie.html", source,
        })


    def test_last_three_book_figures_are_required_in_publication(self):
        """Missing Prometheus and modified Hermes WebP must stop live verification."""
        hermes = ("/assets/illustrations-articles/"
                  "met-246679-hermes-bronze-aile.webp")

        def stale_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/livre-hesiode/index.html":
                return (200, "text/html", self.pages[path].replace(
                    b"icono-hesiode-promethee-bartolozzi-1795-20261104",
                    b"missing-prometheus-illustration"))
            if path == hermes:
                return (200, "image/webp", self.assets[path] + b"modified")
            return self.fetch(url)

        with patch.object(live, "fetch", side_effect=stale_fetch):
            checked = live.verify_recent_public_figures("https://example.test", self.root)
        self.assertEqual({entry["url"] for entry in checked if not entry["valid"]}, {
            "/livre-hesiode/index.html", hermes,
        })
        self.assertEqual(len(live.RECENT_FIGURES), 37)

    def test_newest_met_book_figures_are_required_and_image_bytes_must_match(self):
        """Audit each new book figure against stale HTML and altered WebP."""
        additions = (
            ("livre-iliade-scenes/index.html",
             "icono-iliade-rembrandt-reception-homere-livre-20261104",
             "/assets/illustrations-articles/met-437394-aristote-homere-rembrandt.webp"),
            ("livre-odyssee/index.html",
             "icono-odyssee-athena-chouette-met-254648-20261104",
             "/assets/illustrations-articles/met-254648-athena-chouette-bronze.webp"),
            ("livre-hesiode/index.html",
             "icono-hesiode-aphrodite-hellenistique-met-253504-20261104",
             "/assets/illustrations-articles/met-253504-aphrodite-bronze.webp"),
        )
        for page, figure_id, image_path in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count(
                    (page, figure_id, image_path)), 1)

                def outdated(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            figure_id.encode("utf-8"), b"old-figure-without-new-museum-notice"))
                    if path == image_path:
                        return (200, "image/webp", self.assets[path] + b"altered")
                    return self.fetch(url)

                with patch.object(live, "fetch", side_effect=outdated):
                    checked = live.verify_recent_public_figures(
                        "https://example.test", self.root)
                broken = {row["url"] for row in checked if not row["valid"]}
                self.assertEqual(broken, {"/" + page, image_path})

    def test_new_apollo_hermes_perseus_figures_and_exact_webp_bytes(self):
        """The three new museum figures must exist online with unmodified bytes."""
        additions = (
            ("philosophie-iliade.html", "icono-iliade-apollon-bronze-met-246408-20261104",
             "/assets/illustrations-articles/met-246408-apollon-bronze-romain.webp"),
            ("philosophie-odyssee.html", "icono-odyssee-hermes-calypso-met-246679-20261104",
             "/assets/illustrations-articles/met-246679-hermes-bronze-aile.webp"),
            ("philosophie-theogonie.html", "icono-theogonie-meduse-pegase-lecythe-met-247488-20261104",
             "/assets/illustrations-articles/met-247488-persee-meduse-pegase.webp"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def outdated(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"stale-museum-figure"))
                    if path == src:
                        return (200, "image/webp", self.assets[path] + b"altered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=outdated):
                    report = live.verify_recent_public_figures("https://example.test", self.root)
                self.assertEqual({r["url"] for r in report if not r["valid"]},
                                 {"/" + page, src})


    def test_20261105_museum_figures_and_exact_assets(self):
        """Each newly added figure must survive publication with untampered WebP."""
        additions = (
            ("philosophie-iliade.html", "icono-iliade-aphrodite-hera-met-253504-20261105",
             "/assets/illustrations-articles/met-253504-aphrodite-bronze.webp"),
            ("philosophie-odyssee.html", "icono-odyssee-oreste-egisthe-met-252960-20261105",
             "/assets/illustrations-articles/met-252960-oreste-sarcophage-orestie.webp"),
            ("philosophie-theogonie.html", "icono-theogonie-eros-psyche-met-247480-20261105",
             "/assets/illustrations-articles/met-247480-eros-psyche-terre-cuite.webp"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def stale(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"figure-obsolete"))
                    if path == src:
                        return (200, "image/webp", self.assets[path] + b"tampered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=stale):
                    report = live.verify_recent_public_figures("https://example.test", self.root)
                self.assertEqual({entry["url"] for entry in report if not entry["valid"]},
                                 {"/" + page, src})

    def test_three_reused_artifact_images_in_philosophical_monographs(self):
        """Stale public notices and altered JPEG/WebP bytes must be rejected."""
        additions = (
            ("philosophie-iliade.html",
             "icono-iliade-athena-diomede-bronze-philosophie-20261104",
             "/assets/illustrations-articles/met-254648-athena-chouette-bronze.webp"),
            ("philosophie-odyssee.html",
             "icono-odyssee-penelope-telemaque-chiusi-philosophie-20261104",
             "/media/2026/10/penelope-telemaque-metier-coupe-chiusi-1831.jpg"),
            ("philosophie-theogonie.html",
             "icono-theogonie-aphrodite-anadyomene-philosophie-20261104",
             "/assets/illustrations-articles/met-253504-aphrodite-bronze.webp"),
        )
        for page, fid, src in additions:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, src)), 1)
                def bad_fetch(url):
                    path = url.split("https://example.test", 1)[-1]
                    if path == "/" + page:
                        return (200, "text/html", self.pages[path].replace(
                            fid.encode("utf-8"), b"old-page-without-notice"))
                    if path == src:
                        return (200, "image", self.assets[path] + b"altered")
                    return self.fetch(url)
                with patch.object(live, "fetch", side_effect=bad_fetch):
                    report = live.verify_recent_public_figures(
                        "https://example.test", self.root)
                self.assertEqual({r["url"] for r in report if not r["valid"]},
                                 {"/" + page, src})

    def test_athena_and_suitors_are_required_on_https_with_exact_bytes(self):
        """A stale Athena figure or altered suitors JPEG must stop publication."""
        iliad = ("livre-iliade-scenes/index.html",
                 "icono-iliade-athena-diomede-met-254648-20261104",
                 "/assets/illustrations-articles/met-254648-athena-chouette-bronze.webp")
        odyssey = ("livre-odyssee/index.html",
                   "icono-odyssee-pretendants-skyphos-tarquinia-20261104",
                   "/assets/philosophie/documents/odyssee-03.jpg")
        self.assertEqual(live.RECENT_FIGURES.count(iliad), 1)
        self.assertEqual(live.RECENT_FIGURES.count(odyssey), 1)

        def stale_fetch(url):
            path = url.split("https://example.test", 1)[-1]
            if path == "/" + iliad[0]:
                return (200, "text/html", self.pages[path].replace(
                    iliad[1].encode("utf-8"), b"old-iliad-without-athena"))
            if path == odyssey[2]:
                return (200, "image/jpeg", self.assets[path] + b"changed")
            return self.fetch(url)

        with patch.object(live, "fetch", side_effect=stale_fetch):
            report = live.verify_recent_public_figures(
                "https://example.test", self.root)
        self.assertEqual({row["url"] for row in report if not row["valid"]},
                         {"/" + iliad[0], odyssey[2]})

    def test_same_page_duplicate_media_is_rejected_but_cross_page_reuse_is_allowed(self):
        """Un fichier partagé est contrôlé une fois, une répétition sur la page est interdite."""
        page = "livre-iliade-scenes/index.html"
        image = "/assets/illustrations-articles/met-437394-aristote-homere-rembrandt.webp"
        duplicate_id = "test-duplicate-media-on-same-page"
        source = self.root / page
        extra = ('<figure id="' + duplicate_id + '" data-image-status="œuvre historique">'
                 '<img src="' + image + '" alt="Œuvre authentique">'
                 '<figcaption>Notice documentée, non générée par IA '
                 '<a href="https://www.metmuseum.org/art/collection/search/437394">'
                 'Metropolitan Museum of Art</a></figcaption></figure>')
        source.write_text(source.read_text(encoding="utf-8") + extra,
                          encoding="utf-8")
        new_rows = live.RECENT_FIGURES + ((page, duplicate_id, image),)
        with patch.object(live, "RECENT_FIGURES", new_rows):
            with self.assertRaisesRegex(ValueError, "dupliquée sur une page"):
                live.recent_figure_inventory(self.root)

    def test_bogus_webp_file_rejected_at_inventory(self):
        src = next(src for _, _, src in live.RECENT_FIGURES
                   if src.endswith("met-341681-achille-ombre-patrocle-flaxman.webp"))
        (self.root / src.lstrip("/")).write_bytes(b"<html>404</html>")
        with self.assertRaisesRegex(ValueError, "invalide"):
            live.recent_figure_inventory(self.root)

    def test_non_jpeg_rejected(self):
        src = live.RECENT_FIGURES[0][2]
        (self.root / src.lstrip("/")).write_bytes(b"<html>404</html>")
        with self.assertRaisesRegex(ValueError, "invalide"):
            live.recent_figure_inventory(self.root)


if __name__ == "__main__":
    unittest.main()
