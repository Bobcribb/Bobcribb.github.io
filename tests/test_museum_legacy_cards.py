"""La navigation MYTHOS comporte une seule entrée encyclopédique grecque.

L'accès historique /grande-encyclopedie/ et le registre intégral restent
intacts et indexables ; seuls les doublons du menu et de l'accueil disparaissent.
Le correctif doit être stable après deux reconstructions.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply, NAV, MORE

GREEK = "/mythologie-grecque/"
GRANDE = "/grande-encyclopedie/"


class MuseumNavigationTests(unittest.TestCase):
    def test_one_greek_encyclopedia_in_both_menus(self):
        for items in (NAV, MORE):
            urls = [path for path, _ in items]
            self.assertNotIn(GRANDE, urls)
            self.assertEqual(urls.count(GREEK), 1)
            self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(dict(NAV)[GREEK], "Encyclopédie grecque")

    def test_rebuild_removes_only_duplicate_cards_and_preserves_scholarly_pages(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixtures = {
                "index.html": (
                    '<h1>Accueil MYTHOS</h1><p>Corpus et bibliographies conservés.</p>'
                    '<section class="portal-section"><h2>Collections</h2>'
                    '<div class="portal-grid">'
                    '<a class="portal-card" href="/mythologie-grecque/">Encyclopédie grecque</a>'
                    '<a class="portal-card" href="/grande-encyclopedie/">Ancien doublon</a>'
                    '<a class="portal-card" href="/theatre/">Théâtre grec</a>'
                    '</div></section>'
                    '<section class="mythos-directory"><div class="mythos-collection-grid">'
                    '<a class="mythos-collection-card" href="/grande-encyclopedie/">Ancienne carte</a>'
                    '<a class="mythos-collection-card" href="/mythologie-grecque/">Corpus grec</a>'
                    '</div></section>'
                ),
                "grande-encyclopedie/index.html": (
                    '<h1>Grande Encyclopédie</h1>'
                    '<p>Manuscrit historique et bibliographie intégraux.</p>'
                    '<a href="/mythologie-grecque/">Accès au corpus grec</a>'
                ),
                "theatre/index.html": (
                    '<h1>Théâtre grec</h1><p>Fragments antiques et éditions critiques.</p>'
                ),
            }
            for rel, content in fixtures.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<html lang="fr"><head><title>MYTHOS</title></head>'
                    '<body><main><article class="content">' + content
                    + '</article></main></body></html>', encoding="utf-8"
                )
            for _ in range(2):
                self.assertEqual(apply(root), len(fixtures))
                for rel, source in fixtures.items():
                    document = BeautifulSoup(
                        (root / rel).read_text(encoding="utf-8"), "html.parser")
                    for menu in (".mythos-primary-nav", ".mythos-menu nav"):
                        self.assertEqual(len(document.select(
                            menu + ' a[href="' + GREEK + '"]')), 1, rel)
                        self.assertFalse(document.select(
                            menu + ' a[href="' + GRANDE + '"]'), rel)
                        greek_link = document.select_one(menu + ' a[href="' + GREEK + '"]')
                        self.assertEqual(greek_link.get("aria-current") == "page",
                                         rel.startswith("grande-encyclopedie/"), rel)
                    self.assertEqual(len(document.select(".mythos-banner h1")), 1)
                    expected_text = ("Manuscrit historique et bibliographie intégraux."
                                     if "grande-" in rel else
                                     "Fragments antiques et éditions critiques."
                                     if rel.startswith("theatre/") else
                                     "Corpus et bibliographies conservés.")
                    self.assertIn(expected_text, document.get_text(" ", strip=True))
                home = BeautifulSoup(
                    (root / "index.html").read_text(encoding="utf-8"), "html.parser")
                self.assertFalse(home.select(
                    'a.portal-card[href="' + GRANDE + '"], '
                    'a.mythos-collection-card[href="' + GRANDE + '"]'))
                self.assertEqual(len(home.select(
                    'a.portal-card[href="' + GREEK + '"]')), 1)
                self.assertEqual(len(home.select(
                    'a.portal-card[href="/theatre/"]')), 1)
                self.assertTrue(home.select(
                    'a.mythos-collection-card[href="' + GREEK + '"]'))
                historic = BeautifulSoup(
                    (root / "grande-encyclopedie/index.html").read_text(
                        encoding="utf-8"), "html.parser")
                self.assertIn("Manuscrit historique et bibliographie intégraux.",
                              historic.get_text(" ", strip=True))
                self.assertIsNotNone(historic.select_one(
                    'a[href="/mythologie-grecque/"]'))


if __name__ == "__main__":
    unittest.main()
