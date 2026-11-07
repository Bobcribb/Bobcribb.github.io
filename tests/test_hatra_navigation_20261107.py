"""Hatra : étude intégrale et parcours asie sans liens non publiés."""
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
import sys

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as nav

SLUG = "civilisations-hatra-royaume-arsacide"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
PAGE = ROOT / "bibliotheque-mythologies-du-monde" / SLUG / "index.html"
PALMYRA = "/bibliotheque-mythologies-du-monde/civilisations-palmyre-zenobie/"


class HatraCivilisationsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = PAGE.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.raw, "html.parser")

    def test_integral_study_and_scholarly_notes(self):
        self.assertGreater(len(self.raw), 30000)
        headings = self.soup.select("section.mythos-study-section h2")
        self.assertEqual(len(headings), 19)
        ids = [element.get("id") for element in headings]
        self.assertEqual(len(set(ids)), len(ids))
        self.assertTrue(all(self.soup.select_one(f'nav[aria-label="Sommaire scientifique"] a[href="#{id}"]')
                            for id in ids))
        bib = self.soup.select_one("#sources-et-bibliographie")
        self.assertIsNotNone(bib)
        self.assertGreaterEqual(len(bib.find_parent("section").select("li")), 12)
        text = self.soup.get_text(" ", strip=True).casefold()
        for term in ("araméen", "šamaš", "rome", "sassanide",
                     "fortification", "patrimoine", "palmyre", "méthode"):
            self.assertIn(term, text)

    def test_attribution_accessibility_and_canonical_route(self):
        self.assertEqual(self.soup.html.get("lang"), "fr")
        self.assertEqual(len(self.soup.select("h1")), 1)
        self.assertEqual(self.soup.select_one('link[rel="canonical"]')["href"],
                         "https://bobmythos.fr" + URL)
        self.assertTrue(self.soup.select_one('a.mythos-skip[href="#contenu"]'))
        self.assertEqual(len(self.soup.select('nav[aria-label="Fil d’Ariane"]')), 1)
        self.assertTrue(self.soup.select_one('img[alt][loading="lazy"]'))
        self.assertIn("creativecommons.org/licenses/by-sa/4.0", self.raw)
        self.assertIn("commons.wikimedia.org/wiki/File:Hatra_ruins_2022.jpg", self.raw)
        self.assertNotIn("Grande encyclopédie", self.raw)
        self.assertNotIn("2,5D.svg", self.raw)

    def test_continent_and_conditional_frontier_navigation(self):
        entries = [
            {"url": URL, "title": "Hatra — royaume arsacide"},
            {"url": PALMYRA, "title": "Palmyre"},
        ]
        groups = nav.get_civilisations(entries)
        self.assertEqual([e["url"] for e in groups["asie"]], [URL, PALMYRA])
        built = {}
        with patch.object(nav, "write", side_effect=lambda slug, html: built.__setitem__(slug, html)):
            nav.create_civilisations(entries, groups)
        asian = BeautifulSoup(built["civilisations/asie"], "html.parser")
        self.assertIsNotNone(asian.find(string=lambda s: s and "Hatra : les frontières parthe et romaine" in s))
        self.assertEqual(len(asian.select(f'a[href="{URL}"]')), 2)  # catalogue et parcours
        self.assertTrue(asian.select_one(f'a[href="{PALMYRA}"]'))

        # Un brouillon sans URL dans search.json ne crée aucun parcours fantôme.
        reduced = [entries[1]]
        built.clear()
        with patch.object(nav, "write", side_effect=lambda slug, html: built.__setitem__(slug, html)):
            nav.create_civilisations(reduced, nav.get_civilisations(reduced))
        self.assertNotIn("Hatra : les frontières parthe et romaine", built["civilisations/asie"])
        self.assertNotIn(f'href="{URL}"', built["civilisations/asie"])

    def test_reference_links_are_specific(self):
        hrefs = [node["href"] for node in self.soup.select("#sources-et-bibliographie a[href]")]
        self.assertGreaterEqual(len(hrefs), 12)
        self.assertTrue(any("persee.fr" in x for x in hrefs))
        self.assertTrue(any("whc.unesco.org" in x for x in hrefs))
        self.assertTrue(any("doi.org/10.1017/irq.2025.10038" in x for x in hrefs))
