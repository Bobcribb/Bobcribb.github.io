"""Régression ciblée du dossier Chachapoyas et de son classement géographique.

N'intervient ni dans la file atomique ni dans les anciens lecteurs.
"""
import importlib.util
import re
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-chachapoya-utcubamba-kuelap" / "index.html"
NAV_SCRIPT = ROOT / "scripts" / "build_navigation.py"
NEW_URL = "/bibliotheque-mythologies-du-monde/civilisations-chachapoya-utcubamba-kuelap/"


class ChachapoyaStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")

    def test_integral_scholarly_monograph_is_preserved(self):
        headings = self.doc.select("article.content section[id] > h2")
        self.assertEqual(len(headings), 18, "Les 18 sections, y compris les références, sont conservées")
        self.assertGreater(len(self.doc.select_one("article.content").get_text(" ", strip=True).split()), 2900)
        for marker in ("Kuélap", "Laguna de los Cóndores", "Koschmieder",
                       "Urton", "curacazgos", "liste indicative", "bibliographie"):
            self.assertIn(marker.casefold(), self.doc.get_text(" ", strip=True).casefold())
        self.assertEqual(len(self.doc.select("ol.bibliography > li[id]")), 12)
        self.assertNotIn("Grande encyclopédie", self.doc.get_text(" ", strip=True))
        self.assertNotIn("2,5D", self.doc.get_text(" ", strip=True))

    def test_toc_and_breadcrumbs_are_accessible(self):
        article = self.doc.select_one("main#contenu article.content")
        self.assertIsNotNone(article)
        self.assertIsNotNone(self.doc.select_one('a.mythos-skip[href="#contenu"]'))
        toc = article.select_one('nav[aria-label="Sommaire de l\'étude scientifique"]')
        self.assertIsNotNone(toc)
        anchors = [a.get("href") for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(anchors), 18)
        ids = {tag.get("id") for tag in article.select("[id]") if tag.get("id")}
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertTrue(all(a[1:] in ids for a in anchors))
        breadcrumb = article.select_one('nav[aria-label="Fil d\'Ariane"]')
        self.assertIsNotNone(breadcrumb)
        urls = {a.get("href") for a in breadcrumb.select("a[href]")}
        self.assertIn("/civilisations/ameriques/", urls)
        self.assertIn("/civilisations/", urls)
        canonical = self.doc.select_one('link[rel="canonical"]')
        self.assertEqual(canonical.get("href"), "https://bobmythos.fr" + NEW_URL)

    def test_documentary_image_has_permission_and_correct_alt(self):
        pictures = self.doc.select("article.content figure img")
        self.assertEqual(len(pictures), 1)
        self.assertIn("commons.wikimedia.org/wiki/Special:FilePath/", pictures[0]["src"])
        self.assertIn("Kuélap", pictures[0]["alt"])
        figcaption = pictures[0].find_parent("figure").find("figcaption")
        self.assertIn("Atinker1", figcaption.get_text(" ", strip=True))
        self.assertIn("CC BY-SA 4.0", figcaption.get_text(" ", strip=True))
        self.assertIsNotNone(figcaption.select_one('a[href*="creativecommons.org/licenses/by-sa/4.0/"]'))
        self.assertFalse(self.doc.select("svg[data-2-5d], canvas"))

    def test_world_navigation_auto_routes_to_americas(self):
        spec = importlib.util.spec_from_file_location("mythos_world_nav", NAV_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        entry = {"title": "Civilisations — Chachapoyas : Kuélap",
                 "url": NEW_URL, "excerpt": "Kuélap et l'Utcubamba"}
        self.assertEqual(module.group_continent(entry), "ameriques")
        grouped = module.get_civilisations([entry])
        self.assertEqual(grouped["ameriques"], [entry])
        self.assertFalse(any(entry in values for key, values in grouped.items() if key != "ameriques"))

    def test_internal_references_and_no_numbering(self):
        anchors = [a.get("href") for a in self.doc.select('article.content a[href^="/"]')]
        for expected in ("/mythologie-grecque/", "/origines-du-sacre/",
                         "/civilisations/ameriques/", "/civilisations/",
                         "/bibliotheque-mythologies-du-monde/civilisations-tiwanaku-altiplano/"):
            self.assertIn(expected, anchors)
        self.assertFalse(re.search(r"Chapitre\s+\{\{numero\}\}|Volume\s+\{\{volume\}\}",
                                   SOURCE.read_text(encoding="utf-8"), re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
