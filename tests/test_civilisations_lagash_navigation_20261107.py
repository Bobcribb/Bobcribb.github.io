"""Non-régression : édition Lagash et navigation mésopotamienne de MYTHOS.

Vérifie les sources (jamais le HTML généré, protégé de tout écrasement).
"""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

SLUG = "civilisations-lagash-girsu-umma-frontieres"
URL = "/bibliotheque-mythologies-du-monde/" + SLUG + "/"
STUDY = ROOT / URL.strip("/") / "index.html"
HUB = ROOT / "bibliotheque-mythologies-du-monde/civilisations-histoire-mesopotamie/index.html"


class LagashStudyNavigationTests(unittest.TestCase):
    def test_source_is_integral_and_structured(self):
        page = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(page.html.get("lang"), "fr")
        self.assertEqual(page.select_one('link[rel="canonical"]')["href"],
                         "https://bobmythos.fr" + URL)
        self.assertEqual(len(page.select("h1")), 1)
        sections = page.select("article h2[id]")
        self.assertGreaterEqual(len(sections), 16)
        ids = [h["id"] for h in sections]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(page.get_text(" ", strip=True).split()), 2500)
        for toc_link in page.select(".mythos-reading-toc a[href^='#']"):
            self.assertIn(toc_link["href"][1:], ids)
        self.assertGreaterEqual(len(page.select("#references li")), 10)
        self.assertIn("degrés de certitude", page.get_text(" ", strip=True))
        for a in page.select("a[href]"):
            self.assertFalse(a["href"].startswith("http://"))

    def test_documentary_image_is_present_and_provenanced(self):
        page = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        figures = page.select("figure")
        self.assertEqual(len(figures), 1)
        figure = figures[0]
        src = figure.select_one("img")["src"]
        self.assertEqual(src, "/assets/illustrations-articles/met-329072-gudea-statue-assise.webp")
        self.assertTrue((ROOT / src.lstrip("/")).is_file())
        self.assertIn("CC0", figure.get_text(" ", strip=True))
        self.assertTrue(figure.select_one('a[href="https://www.metmuseum.org/art/collection/search/329072"]'))
        self.assertTrue(figure.select_one("img").get("alt"))
        self.assertNotIn(".svg", STUDY.read_text(encoding="utf-8").lower())

    def test_reciprocal_navigation_and_auto_index(self):
        study = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        hub = BeautifulSoup(HUB.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(len(hub.select('a[href="' + URL + '"]')), 1)
        self.assertTrue(study.select_one(
            'a[href="/bibliotheque-mythologies-du-monde/civilisations-histoire-mesopotamie/"]'))
        self.assertTrue(study.select_one('a[href="/civilisations/asie/"]'))
        self.assertTrue(study.select_one('a[href="/mythologie-grecque/"]'))
        entries = [{"url": URL, "title": "Civilisations — Lagash et Girsu"}]
        continents = get_civilisations(entries)
        self.assertEqual([entry["url"] for entry in continents["asie"]], [URL])
        self.assertEqual(sum(map(len, continents.values())), 1)

    def test_existing_meso_corpus_kept(self):
        source = HUB.read_text(encoding="utf-8")
        self.assertIn("La transformation d’Uruk", source)
        self.assertIn("DOSSIER APPROFONDI — Mésopotamie", source)
        self.assertIn("APPAREIL CRITIQUE MYTHOS", source)
        self.assertNotIn("Grande encyclopédie", source)


if __name__ == "__main__":
    unittest.main()
