"""Régression : les SVG des grandes monographies doivent être publiquement servis."""
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


if __name__ == "__main__":
    unittest.main()
