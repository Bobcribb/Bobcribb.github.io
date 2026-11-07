"""Contrôles non destructifs : étude Kanem-Bornou et index africain."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

PATH = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-kanem-bornou-lac-tchad" / "index.html"
URL = "/bibliotheque-mythologies-du-monde/civilisations-kanem-bornou-lac-tchad/"

class KanemBornouTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PATH.read_text(encoding="utf-8")
        cls.page = BeautifulSoup(cls.html, "html.parser")

    def test_continental_classification(self):
        record = {"url": URL, "title": "Civilisations — Kanem-Bornou et le lac Tchad"}
        self.assertEqual(group_continent(record), "afrique")
        groups = get_civilisations([record])
        self.assertEqual([e["url"] for e in groups["afrique"]], [URL])
        self.assertFalse(groups["asie"])

    def test_scholarly_sections_and_bibliography(self):
        headers = self.page.select("section.mythos-study-section > h2")
        self.assertEqual(len(headers), 16)
        for i, header in enumerate(headers, start=1):
            self.assertEqual(header.get("id"), f"section-{i}")
            self.assertIsNotNone(self.page.select_one(f'nav[aria-label="Sommaire de l’étude"] a[href="#section-{i}"]'))
        self.assertGreaterEqual(len(self.page.select(".study-biblio ol li")), 13)
        self.assertIn("Girgam", self.html)
        self.assertIn("Dīwān", self.html)
        self.assertIn("archéologie", self.html)
        self.assertIn("hypothèses", self.html)

    def test_accessibility_and_canonical(self):
        self.assertEqual(self.page.html.get("lang"), "fr")
        self.assertEqual(self.page.find("link", rel="canonical").get("href"), "https://bobmythos.fr" + URL)
        self.assertIsNotNone(self.page.select_one('a.mythos-skip[href="#mythos-content"]'))
        self.assertIsNotNone(self.page.select_one('nav[aria-label="Fil d\'Ariane"]'))
        self.assertTrue(all(img.get("alt") for img in self.page.select("figure img")))

    def test_links_and_visual_integrity(self):
        hrefs = {a.get("href") for a in self.page.select("a[href]")}
        for required in ("/", "/mythologie-grecque/", "/civilisations/afrique/", "/mythologie-comparee/", "/origines-du-sacre/", "/methode-editoriale/"):
            self.assertIn(required, hrefs)
        self.assertNotIn("/grande-encyclopedie/", hrefs)
        self.assertIn("https://commons.wikimedia.org/wiki/File:Kanem-Bornu.svg", hrefs)
        self.assertIn("CC0 1.0", self.html)
        self.assertNotIn("2,5D", self.html)

if __name__ == "__main__":
    unittest.main()
