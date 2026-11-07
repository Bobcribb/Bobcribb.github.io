"""Kuk : navigation océanienne, intégrité du dossier et absence de faux classement khmer."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

KUK = "/bibliotheque-mythologies-du-monde/civilisations-kuk-papouasie-nouvelle-guinee/"
KHMER = "/bibliotheque-mythologies-du-monde/civilisations-sambor-prei-kuk-chenla/"
PATH = ROOT / KUK.strip("/") / "index.html"


class KukOceaniaNavigationTests(unittest.TestCase):
    def test_kuk_is_in_oceania_but_sambor_prei_kuk_remains_in_asia(self):
        kuk = {"url": KUK, "title": "Kuk — Nouvelle-Guinée"}
        khmer = {"url": KHMER, "title": "Sambor Prei Kuk — Cambodge"}
        self.assertEqual(group_continent(kuk), "oceanie")
        self.assertEqual(group_continent(khmer), "asie")
        groups = get_civilisations([kuk, khmer])
        self.assertEqual([x["url"] for x in groups["oceanie"]], [KUK])
        self.assertEqual([x["url"] for x in groups["asie"]], [KHMER])
        self.assertEqual(sum(len(x) for x in groups.values()), 2)

    def test_full_text_canonical_breadcrumb_toc_and_references(self):
        text = PATH.read_text(encoding="utf-8")
        doc = BeautifulSoup(text, "html.parser")
        self.assertEqual(doc.select_one('link[rel="canonical"]')["href"], "https://bobmythos.fr" + KUK)
        self.assertEqual(doc.select_one('html')["lang"], "fr")
        self.assertEqual(len(doc.select("section.mythos-study-section")), 16)
        breadcrumb = doc.select_one('nav[aria-label="Fil d’Ariane"]')
        self.assertIsNotNone(breadcrumb)
        self.assertTrue(breadcrumb.select_one('a[href="/civilisations/oceanie/"]'))
        self.assertTrue(doc.select_one('a.mythos-skip[href="#contenu"]'))
        ids = [x["id"] for x in doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        for a in doc.select('nav.origins-toc a[href^="#"]'):
            self.assertIn(a["href"][1:], ids)
        for a in doc.select('a[href^="#kuk-source-"]'):
            self.assertIn(a["href"][1:], ids)
        self.assertEqual(len(doc.select('#kuk-bibliographie li[id^="kuk-source-"]')), 7)
        self.assertIn("6 950", doc.get_text(" ", strip=True))
        self.assertIn("Kawelka", text)
        self.assertGreater(len(doc.select_one("article.content").get_text(" ", strip=True).split()), 2800)

    def test_study_has_reciprocal_links_without_invented_ancient_texts(self):
        doc = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")
        links = {a.get("href", "") for a in doc.select("a[href]")}
        for href in ("/mythologie-grecque/", "/mythologie-comparee/",
                     "/origines-du-sacre/", "/civilisations/oceanie/",
                     "/bibliotheque-mythologies-du-monde/civilisations-histoire-oceanie/"):
            self.assertIn(href, links)
            self.assertTrue((ROOT / href.strip("/") / "index.html").is_file(), href)
        self.assertIn("aucun texte écrit", doc.get_text(" ", strip=True).lower())
        self.assertIn("aucune photographie sous licence indéterminée", doc.get_text(" ", strip=True).lower())

if __name__ == "__main__":
    unittest.main()
