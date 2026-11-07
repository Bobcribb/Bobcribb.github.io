"""Régression MYTHOS : Moundville, classement américain, images et lectures préservées."""
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

BASE = ROOT / "bibliotheque-mythologies-du-monde"
SLUG = "civilisations-moundville-cahokia-comparaison-mississippienne"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
STUDY = BASE / SLUG / "index.html"
CAHOKIA = BASE / "civilisations-cahokia-mississippienne" / "index.html"


class MoundvilleNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = STUDY.read_text(encoding="utf-8")
        cls.study = BeautifulSoup(cls.raw, "html.parser")
        cls.cahokia_raw = CAHOKIA.read_text(encoding="utf-8")
        cls.cahokia = BeautifulSoup(cls.cahokia_raw, "html.parser")

    def test_monograph_is_full_length_and_critically_sourced(self):
        self.assertGreater(len(self.study.get_text(" ", strip=True).split()), 3700)
        self.assertEqual(len(self.study.select("section.civilisation-monograph")), 19)
        self.assertEqual(len(self.study.select("#bibliographie ol > li")), 15)
        self.assertEqual(
            len(self.study.select("section.civilisation-monograph[id]:not(#bibliographie)")), 18
        )
        for marker in ("Black Warrior", "Blitz", "Steponaitis",
                       "NAGPRA", "Cahokia", "Knight", "Moundville"):
            self.assertIn(marker, self.raw)
        for i in range(1, 16):
            self.assertIsNotNone(self.study.select_one(f"#source-{i}"))

    def test_accessible_toc_and_breadcrumbs_resolve(self):
        toc = self.study.select_one('nav[aria-label="Sommaire scientifique de Moundville"]')
        self.assertIsNotNone(toc)
        hrefs = [a.get("href") for a in toc.select("a[href^='#']")]
        self.assertEqual(len(hrefs), 19)
        self.assertEqual(len(hrefs), len(set(hrefs)))
        ids = {e.get("id") for e in self.study.select("[id]")}
        self.assertTrue(all(h[1:] in ids for h in hrefs))
        for target in ("/civilisations/", "/civilisations/ameriques/",
                       "/bibliotheque-mythologies-du-monde/civilisations-cahokia-mississippienne/"):
            self.assertTrue(self.study.select_one(
                'nav[aria-label="Fil d’Ariane"] a[href="' + target + '"]'
            ))

    def test_backlinks_are_unique_and_cahokia_archive_is_intact(self):
        self.assertEqual(len(self.cahokia.select("#parcours-cahokia-moundville")), 1)
        cards = self.cahokia.select("#parcours-cahokia-moundville a.portal-card")
        self.assertEqual(len(cards), 2)
        self.assertEqual(sum(card.get("href") == URL for card in cards), 1)
        self.assertTrue(self.cahokia.select_one('a[href="/civilisations/ameriques/"]'))
        self.assertIn("Monks Mound", self.cahokia_raw)
        self.assertIn("Méthode et limites", self.cahokia.get_text(" ", strip=True))

    def test_classified_in_americas_without_shared_generator_edit(self):
        groups = get_civilisations([{
            "url": URL, "title": "Moundville et Cahokia",
            "excerpt": "Black Warrior, Alabama",
        }])
        self.assertEqual(len(groups["ameriques"]), 1)
        for other in ("asie", "afrique", "europe", "oceanie"):
            self.assertFalse(groups[other])

    def test_documentary_photo_attribution_is_complete(self):
        figure = self.study.select_one("figure.museum-object")
        self.assertIsNotNone(figure)
        photo = figure.select_one("img")
        self.assertIn("Moundville_Archaeological_Park_03.JPG", photo.get("src", ""))
        self.assertGreater(len(photo.get("alt", "")), 70)
        caption = figure.select_one("figcaption")
        self.assertIn("Jeffrey Reed", caption.get_text(" ", strip=True))
        self.assertTrue(caption.select_one(
            'a[href="https://creativecommons.org/licenses/by-sa/3.0/"]'
        ))
        self.assertFalse(self.study.select_one('img[src$=".svg"]'))
        self.assertNotIn('Grande encyclopédie</a>', self.raw)


if __name__ == "__main__":
    unittest.main()
