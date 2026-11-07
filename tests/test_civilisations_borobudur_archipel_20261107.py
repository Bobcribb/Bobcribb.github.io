"""MYTHOS : étude de Borobudur et parcours d'Asie, sans liens inventés."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as navigation

BOROBUDUR = "/bibliotheque-mythologies-du-monde/civilisations-sailendra-borobudur-java/"
SRIVIJAYA = "/bibliotheque-mythologies-du-monde/civilisations-srivijaya-sumatra/"
MAJAPAHIT = "/bibliotheque-mythologies-du-monde/civilisations-majapahit-trowulan-java/"
SOURCE = ROOT / BOROBUDUR.lstrip("/") / "index.html"

class BorobudurArchipelTests(unittest.TestCase):
    def test_integral_scholarly_study_has_scientific_apparatus(self):
        text = SOURCE.read_text(encoding="utf-8")
        doc = BeautifulSoup(text, "html.parser")
        self.assertGreater(len(text), 25000)
        self.assertEqual(doc.find("html").get("lang"), "fr")
        self.assertIsNotNone(doc.select_one('a[href="#contenu"]'))
        self.assertIsNotNone(doc.select_one('nav[aria-label="Fil d\'Ariane"]'))
        self.assertEqual(len(doc.select('section[id]')), 0)  # anchors on headings, not wrapper
        ids = [h.get("id") for h in doc.select("article h2[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        for anchor in doc.select('nav[aria-label="Sommaire de la monographie"] a[href^="#"]'):
            self.assertIn(anchor["href"][1:], ids)
        self.assertGreaterEqual(len(ids), 15)
        for term in ("Kalasan", "Karangtengah", "Tri Tepusan", "Karmavibha",
                     "Gaṇḍavyūha", "Śailendra", "Mendut", "Pawon",
                     "historiograph", "hydraul", "bibliograph"):
            self.assertIn(term.casefold(), text.casefold())
        for href in (SRIVIJAYA, MAJAPAHIT, "/mythologie-grecque/",
                     "https://whc.unesco.org/en/list/592",
                     "https://doi.org/10.26721/spafajournal.bo2frueq93"):
            self.assertIsNotNone(doc.select_one('a[href="' + href + '"]'))
        figure = doc.select_one("figure.mythos-scientific-image")
        self.assertIsNotNone(figure)
        self.assertTrue(figure.select_one("img").get("alt"))
        self.assertIn("CC BY-SA 3.0", figure.get_text(" ", strip=True))
        self.assertNotIn("2,5D", text)
        self.assertNotIn("Grande encyclopédie", doc.find("header").get_text(" ", strip=True))

    def test_archipel_hub_uses_only_indexed_studies(self):
        items = [
            {"url": url, "title": name}
            for url, name in ((SRIVIJAYA, "Śrīvijaya"),
                              (BOROBUDUR, "Borobudur"),
                              (MAJAPAHIT, "Majapahit"))
        ]
        self.assertTrue(all(navigation.group_continent(e) == "asie" for e in items))
        with TemporaryDirectory() as d:
            previous = navigation.OUT
            navigation.OUT = Path(d)
            try:
                navigation.create_civilisations(items, navigation.get_civilisations(items))
                page = BeautifulSoup((Path(d)/"civilisations/asie/index.html").read_text(encoding="utf-8"), "html.parser")
                region = page.select_one('nav[aria-label="Parcours historique de l’archipel indonésien"]')
                self.assertIsNotNone(region)
                self.assertEqual([a["href"] for a in region.select("a.portal-card")],
                                 [SRIVIJAYA, BOROBUDUR, MAJAPAHIT])
                self.assertIn("ne forment pas une succession linéaire", page.get_text(" ", strip=True))
                navigation.create_civilisations(items[:1], navigation.get_civilisations(items[:1]))
                short = BeautifulSoup((Path(d)/"civilisations/asie/index.html").read_text(encoding="utf-8"), "html.parser")
                refs = {a["href"] for a in short.select('nav[aria-label="Parcours historique de l’archipel indonésien"] a')}
                self.assertEqual(refs, {SRIVIJAYA})
            finally:
                navigation.OUT = previous

if __name__ == "__main__":
    unittest.main()
