"""Contrôles éditoriaux non destructifs : étude Baekje et parcours coréen."""
import sys
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations  # noqa: E402

BASE = "/bibliotheque-mythologies-du-monde/"
BAEKJE = BASE + "civilisations-baekje-ungjin-sabi-coree/"
REGIONAL = BASE + "civilisations-histoire-japon-coree/"
SILLA = BASE + "civilisations-silla-gyeongju/"
GAYA = BASE + "civilisations-confederation-gaya-coree/"


def page(relative_path):
    return BeautifulSoup((ROOT / relative_path).read_text(encoding="utf-8"), "html.parser")


class BaekjeNavigationTests(unittest.TestCase):
    def setUp(self):
        self.doc = page("bibliotheque-mythologies-du-monde/civilisations-baekje-ungjin-sabi-coree/index.html")

    def test_complete_monograph_and_source_apparatus(self):
        self.assertEqual(len(self.doc.select("section.mythos-study-section > h2")), 17)
        self.assertEqual(len(self.doc.select("#bibliographie li[id^='ref-']")), 13)
        article = self.doc.select_one("article")
        self.assertGreater(len(article.get_text(" ", strip=True).split()), 2200)
        self.assertIn("Muryeong", article.get_text(" ", strip=True))
        self.assertIn("Mireuksa", article.get_text(" ", strip=True))
        self.assertIn("Baekje", article.get_text(" ", strip=True))
        self.assertIsNotNone(self.doc.select_one("link[rel='canonical'][href$='/civilisations-baekje-ungjin-sabi-coree/']"))

    def test_accessibility_and_documented_image(self):
        self.assertIsNotNone(self.doc.select_one("a[href='#contenu'].mythos-skip"))
        self.assertIsNotNone(self.doc.select_one("nav[aria-label='Fil d’Ariane']"))
        self.assertIsNotNone(self.doc.select_one("nav[aria-label='Sommaire de la monographie']"))
        ids = [x["id"] for x in self.doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(ref["href"][1:] in ids for ref in self.doc.select("a[href^='#']")))
        self.assertIsNotNone(self.doc.select_one("img[alt][loading='lazy']"))
        self.assertIsNotNone(self.doc.select_one("figcaption a[href*='creativecommons.org/licenses/by-sa/3.0/']"))
        self.assertIsNotNone(self.doc.select_one("a[href='https://whc.unesco.org/en/list/1477/maps/']"))

    def test_crosslinks_and_navigation_classification(self):
        urls = {a.get("href") for a in self.doc.select("article a[href]")}
        self.assertTrue({REGIONAL, GAYA, SILLA, "/civilisations/asie/", "/mythologie-grecque/"}.issubset(urls))
        groups = get_civilisations([
            {"url": BAEKJE, "title": "Baekje — Ungjin et Sabi"}
        ])
        self.assertEqual([e["url"] for e in groups["asie"]], [BAEKJE])
        self.assertFalse(any(groups[k] for k in ("afrique", "oceanie", "ameriques", "europe")))

    def test_regional_reader_remains_intact_with_baekje_path(self):
        region = page("bibliotheque-mythologies-du-monde/civilisations-histoire-japon-coree/index.html")
        self.assertEqual(len(region.select("#parcours-coree-baekje")), 1)
        self.assertEqual(len(region.select("h2[id^='lecture-section-']")), 9)
        crosslinks = region.select("aside[data-mythos-crosslinks='coree-trois-royaumes'] a[href]")
        urls = [a["href"] for a in crosslinks]
        for url in (BAEKJE, GAYA, SILLA, "/civilisations/asie/"):
            self.assertEqual(urls.count(url), 1)
        self.assertEqual(len(region.select('a[href="' + BAEKJE + '"]')), 1)


if __name__ == "__main__":
    unittest.main()
