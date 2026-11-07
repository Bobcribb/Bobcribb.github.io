"""Contrôle documentaire et de navigation de l'étude Wari (MYTHOS #164)."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

SLUG = "civilisations-wari-huari-ayacucho"
URL = "/bibliotheque-mythologies-du-monde/" + SLUG + "/"
FILE = ROOT / "bibliotheque-mythologies-du-monde" / SLUG / "index.html"


class WariCivilisationsTests(unittest.TestCase):
    def test_wari_is_american_but_unrelated_regions_remain_unchanged(self):
        entries = [
            {"url": URL, "title": "Wari (Huari), Ayacucho"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-sambor-prei-kuk-chenla/", "title": "Sambor Prei Kuk"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-tiwanaku-altiplano/", "title": "Tiwanaku"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-nok-nigeria/", "title": "Nok"},
        ]
        self.assertEqual(group_continent(entries[0]), "ameriques")
        self.assertEqual(group_continent(entries[1]), "asie")
        self.assertEqual(group_continent(entries[2]), "ameriques")
        self.assertEqual(group_continent(entries[3]), "afrique")
        groups = get_civilisations(entries)
        self.assertEqual(set(x["url"] for x in groups["ameriques"]), {URL, entries[2]["url"]})
        self.assertEqual(sum(map(len, groups.values())), len(entries))

    def test_integral_study_bibliography_breadcrumb_toc_and_rights(self):
        self.assertTrue(FILE.exists())
        html = FILE.read_text(encoding="utf-8")
        doc = BeautifulSoup(html, "html.parser")
        self.assertEqual(doc.select_one('link[rel="canonical"]')["href"], "https://bobmythos.fr" + URL)
        self.assertGreaterEqual(len(doc.get_text(" ", strip=True).split()), 3200)
        sections = doc.select("section.mythos-study-section")
        self.assertEqual(len(sections), 20)  # 18 study sections plus bibliography and cartography
        for i in range(1, 19):
            self.assertEqual(len(doc.select(f'h2[id="wari-{i}"]')), 1)
            self.assertIsNotNone(doc.select_one(f'nav[aria-label="Sommaire scientifique de l’étude"] a[href="#wari-{i}"]'))
        bibliography = doc.select_one("#wari-bibliographie")
        self.assertIsNotNone(bibliography)
        self.assertGreaterEqual(len(doc.select('li[id^="wari-ref-"] a[href^="https://"]')), 16)
        self.assertIsNotNone(doc.select_one('nav[aria-label="Fil d’Ariane"] a[href="/civilisations/ameriques/"]'))
        self.assertIsNotNone(doc.select_one('a[href="#contenu"]'))
        self.assertIsNotNone(doc.select_one('a[href="/mythologie-grecque/"]'))
        self.assertIsNotNone(doc.select_one('a[href="/mythologie-comparee/"]'))
        self.assertIsNotNone(doc.select_one('a[href="/origines-du-sacre/"]'))
        self.assertIsNotNone(doc.select_one('img[alt][loading="lazy"]'))
        self.assertIn("creativecommons.org/publicdomain/zero", html)
        self.assertIn("Cleveland Museum of Art", html)
        self.assertIn("doi.org/10.3998/mpub.11396257", html)
        self.assertIn("museos.cultura.pe", html)
        self.assertNotIn("Cités pyu", html)

    def test_internal_study_references_and_existing_collection_links(self):
        doc = BeautifulSoup(FILE.read_text(encoding="utf-8"), "html.parser")
        ids = {node["id"] for node in doc.select("[id]")}
        for link in doc.select('a[href^="#"]'):
            self.assertIn(link["href"][1:], ids)
        for url in (
            "/bibliotheque-mythologies-du-monde/civilisations-tiwanaku-altiplano/",
            "/bibliotheque-mythologies-du-monde/civilisations-mochicas-huacas-sol-luna/",
            "/bibliotheque-mythologies-du-monde/civilisations-chimu-chan-chan/",
            "/bibliotheque-mythologies-du-monde/civilisations-chavin-huantar-andes/",
        ):
            self.assertTrue((ROOT / url.strip("/") / "index.html").exists(), url)


if __name__ == "__main__":
    unittest.main()
