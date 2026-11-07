"""Purépechas : conservation du texte, preuves, navigation et classement géographique."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

BASE = ROOT / "bibliotheque-mythologies-du-monde"
STUDY_SLUG = "civilisations-purepecha-mexicas-tzintzuntzan"
STUDY_URL = f"/bibliotheque-mythologies-du-monde/{STUDY_SLUG}/"
STUDY = BASE / STUDY_SLUG / "index.html"
MEXICA = BASE / "civilisations-histoire-mexicas-tenochtitlan" / "index.html"


class PurepechaNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = STUDY.read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")
        cls.mexica = BeautifulSoup(MEXICA.read_text(encoding="utf-8"), "html.parser")

    def test_original_scholarly_text_and_citations_are_complete(self):
        self.assertGreater(len(self.doc.get_text(" ", strip=True).split()), 3500)
        sections = self.doc.select("section.civilisation-monograph")
        self.assertEqual(len(sections), 19)  # 18 analyses + 1 bibliographie
        self.assertEqual(sum(x.get("id") != "bibliographie" for x in sections), 18)
        self.assertEqual(len(self.doc.select("#bibliographie ol > li")), 12)
        for essential in ("INAH", "Pollard", "El Escorial", "CEMCA", "Curicaueri"):
            self.assertIn(essential, self.raw)
        for i in range(1, 13):
            self.assertIsNotNone(self.doc.select_one(f"#source-{i}"))

    def test_toc_has_valid_distinct_anchors(self):
        toc = self.doc.select_one('nav[aria-label="Sommaire scientifique de Tzintzuntzan"]')
        self.assertIsNotNone(toc)
        links = [a.get("href") for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(links), 19)
        self.assertEqual(len(links), len(set(links)))
        ids = {tag["id"] for tag in self.doc.select("[id]")}
        self.assertTrue(all(anchor[1:] in ids for anchor in links))

    def test_crosslinks_and_archive_conservation(self):
        cards = self.mexica.select("#parcours-mexicas-purepecha a.portal-card")
        self.assertEqual(len(cards), 2)
        self.assertEqual(sum(c.get("href") == STUDY_URL for c in cards), 1)
        self.assertEqual(len(self.mexica.select("#parcours-mexicas-purepecha")), 1)
        self.assertIn("Tenochtitlan et la Triple Alliance", self.mexica.get_text(" ", strip=True))
        for route in ("/civilisations/ameriques/", "/mythologie-comparee/"):
            self.assertIn(route, self.raw)

    def test_new_study_classifies_in_americas_and_not_asia(self):
        groups = get_civilisations([{
            "url": STUDY_URL,
            "title": "Purépechas et Tzintzuntzan",
            "excerpt": "Michoacán et rivalités mexicas",
        }])
        self.assertEqual(len(groups["ameriques"]), 1)
        for other in ("afrique", "asie", "oceanie", "europe"):
            self.assertFalse(groups[other])

    def test_documentary_photograph_attribution_and_original_historical_texts(self):
        image = self.doc.select_one("figure.museum-object img")
        self.assertIsNotNone(image)
        self.assertIn("wikimedia.org", image.get("src", ""))
        self.assertGreater(len(image.get("alt", "")), 50)
        caption = self.doc.select_one("figure.museum-object figcaption")
        self.assertIn("Arian Zwegers", caption.get_text(" ", strip=True))
        self.assertTrue(caption.select_one(
            'a[href="https://creativecommons.org/licenses/by/2.0/"]'
        ))
        self.assertNotIn("2,5D générée", self.raw)
        self.assertNotIn("Grande encyclopédie</a>", self.raw)


if __name__ == "__main__":
    unittest.main()
