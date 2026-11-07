"""MYTHOS : conservation du corpus et accès documentaire à Gonur Depe."""
import sys
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

SLUG = "civilisations-margiane-gonur-depe-oasis-age-du-bronze"
STUDY_URL = "/bibliotheque-mythologies-du-monde/" + SLUG + "/"
STUDY = ROOT / STUDY_URL.strip("/") / "index.html"
INDUS = ROOT / "bibliotheque-mythologies-du-monde/civilisations-histoire-indus-harappa/index.html"


class GonurMargianaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = STUDY.read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")
        cls.indus = BeautifulSoup(INDUS.read_text(encoding="utf-8"), "html.parser")

    def test_study_is_full_and_original(self):
        self.assertGreater(len(self.doc.get_text(" ", strip=True).split()), 2600)
        self.assertEqual(len(self.doc.select("section.mythos-study-section")), 21)
        self.assertEqual(len(self.doc.select("#sources-gonur ol > li")), 11)
        self.assertIn("Murghab", self.raw)
        self.assertIn("Sarianidi", self.raw)
        self.assertIn("Berdysyčran", self.raw)
        self.assertTrue(self.doc.select_one('link[rel="canonical"][href$="/civilisations-margiane-gonur-depe-oasis-age-du-bronze/"]'))

    def test_toc_and_bibliography_anchors_are_unique(self):
        toc = self.doc.select_one("nav#sommaire-gonur")
        links = [a["href"] for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(links), 21)
        self.assertEqual(len(set(links)), len(links))
        ids = [x["id"] for x in self.doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(link[1:] in ids for link in links))

    def test_asian_classification_remains_automatic(self):
        groups = get_civilisations([{"url": STUDY_URL, "title": "Gonur Depe"}])
        self.assertEqual(len(groups["asie"]), 1)
        for area in ("afrique", "europe", "ameriques", "oceanie"):
            self.assertFalse(groups[area])

    def test_reciprocal_historic_navigation_preserved(self):
        self.assertIn("Dholavira", self.indus.get_text(" ", strip=True))
        block = self.indus.select_one("#gonur-margiane-liens")
        self.assertIsNotNone(block)
        self.assertEqual(len(block.select('a[href="' + STUDY_URL + '"]')), 1)
        self.assertEqual(len(block.select('.portal-card')), 2)
        self.assertTrue(self.doc.select_one('a[href="/bibliotheque-mythologies-du-monde/civilisations-histoire-indus-harappa/"]'))

    def test_real_photo_has_provenance_and_correct_license(self):
        figure = self.doc.select_one("figure.museum-object")
        image = figure.select_one("img")
        self.assertEqual(image["src"], "https://upload.wikimedia.org/wikipedia/commons/6/65/Gonur_ruins.jpg")
        self.assertGreater(len(image.get("alt", "")), 45)
        self.assertIn("David Stanley", figure.get_text(" ", strip=True))
        self.assertTrue(figure.select_one('a[href="https://creativecommons.org/licenses/by/2.0/"]'))
        self.assertFalse(self.doc.select_one('img[src$=".svg"]'))


if __name__ == "__main__":
    unittest.main()
