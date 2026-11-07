"""Goguryeo: intégrité de l'étude, sources et classement de navigation."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

URL = "/bibliotheque-mythologies-du-monde/civilisations-goguryeo-capitales-stele-tombes/"
PAGE = ROOT / URL.strip("/") / "index.html"


class GoguryeoNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")

    def test_canonical_and_unique_entrance(self):
        self.assertEqual(self.soup.select_one('link[rel="canonical"]')["href"],
                         "https://bobmythos.fr" + URL)
        self.assertEqual(len(self.soup.select("h1")), 1)
        self.assertIn("Goguryeo", self.soup.select_one("h1").get_text(" ", strip=True))
        self.assertEqual(len(self.soup.select('nav[aria-label="Fil d’Ariane"]')), 1)

    def test_continent_automatic_index(self):
        entry = {"url": URL, "title": "Civilisations — Goguryeo : capitales, stèle et tombes"}
        self.assertEqual(group_continent(entry), "asie")
        groups = get_civilisations([entry])
        self.assertEqual([e["url"] for e in groups["asie"]], [URL])
        self.assertEqual(sum(len(v) for v in groups.values()), 1)

    def test_study_integrity_and_bibliography(self):
        article = self.soup.select_one("article.content")
        self.assertIsNotNone(article)
        self.assertGreaterEqual(len(article.get_text(" ", strip=True).split()), 3000)
        headings = article.select('h2[id^="lecture-section-"]')
        self.assertGreaterEqual(len(headings), 19)
        self.assertEqual(len(article.select('#bibliographie li[id^="ref-"]')), 12)
        targets = {e.get("id") for e in article.select("[id]")}
        for link in article.select('a[href^="#"]'):
            self.assertIn(link["href"][1:], targets, link)
        for url in ("/civilisations/asie/",
                    "/bibliotheque-mythologies-du-monde/civilisations-silla-gyeongju/",
                    "/bibliotheque-mythologies-du-monde/civilisations-confederation-gaya-coree/",
                    "/mythologie-grecque/", "/methode-editoriale/"):
            self.assertTrue(article.select(f'a[href="{url}"]'), url)

    def test_no_renumbering_or_unsourced_visual(self):
        article = self.soup.select_one("article.content")
        self.assertFalse(article.select("img,svg,canvas"))
        self.assertNotIn("2,5D", article.get_text(" ", strip=True))
        self.assertNotIn("Grande encyclopédie", article.get_text(" ", strip=True))
        self.assertIn("Gwanggaeto", article.get_text(" ", strip=True))
        self.assertIn("https://whc.unesco.org/fr/list/1135/", PAGE.read_text(encoding="utf-8"))
        self.assertIn("https://whc.unesco.org/fr/list/1091/", PAGE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
