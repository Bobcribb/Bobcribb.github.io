"""Regression tests for the canonical-vs-historical sitemap policy."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sitemap_integrity import canonical_target


class CanonicalSitemapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def page(self, filename, canonical=None):
        target = self.root / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        link = f'<link rel="canonical" href="{canonical}">' if canonical else ""
        target.write_text(f'<html><head>{link}</head><body><h1>Archive préservée</h1></body></html>', encoding="utf-8")
        return target

    def test_historical_html_alias_to_existing_primary_address(self):
        self.page("mythologie-grecque.html", "https://bobmythos.fr/mythologie-grecque/")
        self.assertEqual(canonical_target(self.root, "/mythologie-grecque.html"),
                         "https://bobmythos.fr/mythologie-grecque/")

    def test_historical_directory_alias_is_recognized(self):
        self.page("grande-encyclopedie/index.html", "https://bobmythos.fr/mythologie-grecque/")
        self.assertEqual(canonical_target(self.root, "/grande-encyclopedie/"),
                         "https://bobmythos.fr/mythologie-grecque/")

    def test_missing_or_unrecognized_canonical_remains_a_failure(self):
        self.page("without/index.html")
        self.assertIsNone(canonical_target(self.root, "/without/"))
        self.assertIsNone(canonical_target(self.root, "/missing/"))

    def test_external_http_query_and_fragment_cannot_waive_sitemap(self):
        for value in ["http://bobmythos.fr/portail/", "https://example.org/portail/",
                      "https://bobmythos.fr/portail/?q=1",
                      "https://bobmythos.fr/portail/#chapitre"]:
            self.page("bad/index.html", value)
            with self.subTest(value=value):
                self.assertIsNone(canonical_target(self.root, "/bad/"))


if __name__ == "__main__":
    unittest.main()
