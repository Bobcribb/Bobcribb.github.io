"""Régression : les SVG des grandes monographies doivent être publiquement servis."""
import hashlib
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


if __name__ == "__main__":
    unittest.main()
