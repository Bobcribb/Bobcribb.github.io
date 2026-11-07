"""Régression : nouvelle étude Saba, navigation contrôlée, source et accès intégral.

N'édite aucun manuscrit et ne modifie aucun numéro canonique.
"""
import sys
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

SLUG = "civilisations-saba-marib-hydraulique-epigraphie"
URL = "/bibliotheque-mythologies-du-monde/" + SLUG + "/"
FILE = ROOT / "bibliotheque-mythologies-du-monde" / SLUG / "index.html"


class SabaArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(FILE.is_file(), FILE)
        self.text = FILE.read_text(encoding="utf-8")
        self.soup = BeautifulSoup(self.text, "html.parser")

    def test_saba_is_in_asia_without_reclassifying_existing_civilisations(self):
        studies = [
            {"url": URL, "title": "Saba et Maʾrib"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-sambor-prei-kuk-chenla/", "title": "Sambor Prei Kuk"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-histoire-aksoum/", "title": "Aksoum"},
            {"url": "/bibliotheque-mythologies-du-monde/civilisations-tiwanaku-altiplano/", "title": "Tiwanaku"},
        ]
        self.assertEqual([group_continent(x) for x in studies], ["asie", "asie", "afrique", "ameriques"])
        groups = get_civilisations(studies)
        self.assertIn(URL, {x["url"] for x in groups["asie"]})
        self.assertEqual(sum(map(len, groups.values())), len(studies))

    def test_canonical_heritage_styles_mobile_and_reader_navigation(self):
        self.assertEqual(
            self.soup.select_one('link[rel="canonical"]')["href"],
            "https://bobmythos.fr" + URL,
        )
        self.assertEqual(self.soup.html.get("lang"), "fr")
        self.assertIsNotNone(self.soup.select_one('meta[name="viewport"]'))
        self.assertIsNotNone(self.soup.select_one('a[href="#contenu"]'))
        self.assertIsNotNone(self.soup.select_one('nav[aria-label="Fil d’Ariane"] a[href="/civilisations/asie/"]'))
        self.assertIsNotNone(self.soup.select_one('nav.mythos-primary-nav a[href="/mythologie-grecque/"]'))
        self.assertIsNone(self.soup.select_one('nav.mythos-primary-nav a[href*="grande-encyclopedie"]'))
        self.assertIsNotNone(self.soup.select_one('details.mythos-menu nav[aria-label="Toutes les rubriques"]'))
        self.assertIsNotNone(self.soup.select_one('link[href="/assets/mythos-museum.css?v=20261104"]'))
        self.assertIsNotNone(self.soup.select_one('script[src^="/assets/mythos-reading.js"]'))

    def test_integral_scientific_content_and_source_links(self):
        content = self.soup.select_one("main article")
        self.assertIsNotNone(content)
        self.assertGreaterEqual(len(content.get_text(" ", strip=True).split()), 3000)
        sections = self.soup.select("section.mythos-study-section")
        self.assertEqual(len(sections), 22)  # vingt chapitres, carte et bibliographie
        toc = self.soup.select_one('nav[aria-label="Sommaire scientifique de l’étude"]')
        self.assertIsNotNone(toc)
        for i in range(1, 21):
            self.assertIsNotNone(self.soup.select_one(f'section[id="saba-{i}"] h2'))
            self.assertIsNotNone(toc.select_one(f'a[href="#saba-{i}"]'))
        for i in range(1, 15):
            self.assertIsNotNone(self.soup.select_one(f'li[id="saba-ref-{i}"] a[href^="https://"]'))
            self.assertIsNotNone(self.soup.select_one(f'a[href="#saba-ref-{i}"]'))
        self.assertIn("Sirwāḥ", content.get_text())
        self.assertIn("DASI", content.get_text())
        self.assertIn("Périple", content.get_text())
        self.assertIn("UNESCO", content.get_text())

    def test_illustration_cartography_crosslinks_and_no_broken_anchors(self):
        ids = {x["id"] for x in self.soup.select("[id]")}
        for a in self.soup.select('a[href^="#"]'):
            self.assertIn(a["href"][1:], ids, a["href"])
        self.assertIsNotNone(self.soup.select_one('a[href*="openstreetmap.org"]'))
        self.assertIsNotNone(self.soup.select_one('a[href*="whc.unesco.org/en/list/1700/maps"]'))
        image = self.soup.select_one("figure.mythos-study-figure img")
        self.assertIsNotNone(image)
        self.assertIn("commons.wikimedia.org", image["src"])
        self.assertTrue(image.get("alt"))
        self.assertIn("creativecommons.org/licenses/by-sa/3.0", self.text)
        self.assertIn("Bernard Gagnon", self.text)
        for url in (
            "/chapitres/origines-du-sacre/707-marib-awwam-almaqah-pelerinage-inscriptions-pouvoir-memoire/",
            "/bibliotheque-mythologies-du-monde/civilisations-histoire-arabie-antique/",
            "/bibliotheque-mythologies-du-monde/mythos-comparatif-nil-mer-rouge-koush-aksoum-saba/",
            "/mythologie-grecque/",
            "/mythologie-comparee/",
        ):
            self.assertIsNotNone(self.soup.select_one(f'a[href="{url}"]'))
            if url != "/mythologie-comparee/":
                self.assertTrue((ROOT / url.lstrip("/") / "index.html").exists(), url)


    def test_reader_keeps_authored_scientific_toc_and_all_prose(self):
        # La navigation rédigée par l'auteur n'est pas une aide de lecture
        # automatique. Le lecteur ne doit ni effacer ses titres ni ses liens.
        from improve_reading import add_reading, authored_blocks
        doc = BeautifulSoup(self.text, "html.parser")
        toc_selector = 'article.content nav.mythos-reading-toc[aria-label="Sommaire scientifique de l’étude"]'
        toc = doc.select_one(toc_selector)
        self.assertIsNotNone(toc)
        before = authored_blocks(doc)
        toc_before = str(toc)
        add_reading(doc, URL, {"words": 3500, "minutes": 16})
        self.assertEqual(before, authored_blocks(doc))
        self.assertEqual(str(doc.select_one(toc_selector)), toc_before)
        for n in range(1, 21):
            self.assertIsNotNone(doc.select_one(f'a[href="#saba-{n}"]'))



if __name__ == "__main__":
    unittest.main()
