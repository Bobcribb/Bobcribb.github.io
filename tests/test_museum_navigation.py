"""Regression: the six MYTHOS collections remain reachable after every museum build.

The user-facing Grande Encyclopédie must be part of the same shared navigation
on the home page and deep scholarly readers. Rebuilds must not duplicate links
or alter source paragraphs and citations.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply, NAV, MORE

GRANDE = "/grande-encyclopedie/"


class MuseumNavigationTests(unittest.TestCase):
    def test_grande_encyclopedie_is_in_both_navigation_menus(self):
        self.assertEqual(sum(path == GRANDE for path, _ in NAV), 1)
        self.assertEqual(sum(path == GRANDE for path, _ in MORE), 1)

    def test_rebuild_preserves_bidirectional_navigation_and_article(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixtures = {
                "index.html": "<h1>Accueil MYTHOS</h1><p>Corpus et bibliographies conservés.</p>",
                "grande-encyclopedie/index.html":
                    "<h1>Grande Encyclopédie</h1><p>Source universitaire complète.</p>",
                "theatre/index.html":
                    "<h1>Théâtre grec</h1><p>Fragments antiques et éditions critiques.</p>",
            }
            for rel, body in fixtures.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<html lang="fr"><head><title>MYTHOS</title></head>'
                    '<body><main><article class="content">' + body
                    + '</article></main></body></html>', encoding="utf-8"
                )
            for _ in range(2):
                self.assertEqual(apply(root), len(fixtures))
                for rel, original in fixtures.items():
                    document = BeautifulSoup((root / rel).read_text(encoding="utf-8"),
                                             "html.parser")
                    primary = document.select('.mythos-primary-nav a[href="' + GRANDE + '"]')
                    complete = document.select('.mythos-menu nav a[href="' + GRANDE + '"]')
                    self.assertEqual(len(primary), 1, rel)
                    self.assertEqual(len(complete), 1, rel)
                    self.assertEqual(len(document.select(".mythos-banner h1")), 1, rel)
                    self.assertIn(
                        BeautifulSoup(original, "html.parser").p.get_text(strip=True),
                        document.get_text(" ", strip=True), rel
                    )
                    self.assertEqual(primary[0].get_text(strip=True),
                                     "Grande encyclopédie")
                    expected_current = rel.startswith("grande-encyclopedie/")
                    self.assertEqual(primary[0].get("aria-current") == "page",
                                     expected_current, rel)


if __name__ == "__main__":
    unittest.main()
