"""Garantir que la refonte conserve le mémoire d’Akhetaton sans doublon.

Le texte universitaire publié comporte seize chapitres, les annexes,
cinq tableaux, trois images institutionnelles et les références originales.
Le portail Égypte doit donner un accès direct à la section intégrale.
"""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "akhetaton-horizon-aton-etude" / "index.html"
PORTAL = ROOT / "bibliotheque-egypte-ancienne" / "index.html"
MEMOIRE = "horizon-aton-memoire-integral"


class HorizonAtonIntegralPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        cls.portal = BeautifulSoup(PORTAL.read_text(encoding="utf-8"), "html.parser")
        cls.studies = cls.page.select(f'section#{MEMOIRE}')

    def test_single_integral_study_and_original_article_survive(self):
        self.assertEqual(len(self.studies), 1, "Aucune seconde insertion du mémoire")
        study = self.studies[0]
        self.assertGreater(len(study.get_text(" ", strip=True)), 65000)
        self.assertIsNotNone(self.page.select_one('h2#lecture-section-13'))
        self.assertIn("12. Questions d’étude", self.page.get_text(" ", strip=True))
        self.assertIn("16 chapitres", study.get_text(" ", strip=True))

    def test_chapters_toc_and_archaeological_references(self):
        study = self.studies[0]
        for i in range(1, 17):
            self.assertTrue(study.select_one(f'[id^="aton-memoire-{i}-"]'), i)
        self.assertIn("Bibliographie et ressources documentaires",
                      study.get_text(" ", strip=True))
        toc = study.select_one('nav[aria-label="Sommaire du mémoire universitaire"]')
        self.assertIsNotNone(toc)
        for link in toc.select('a[href^="#"]'):
            target = link['href'][1:]
            self.assertIsNotNone(self.page.find(id=target),
                                 f"Ancre du mémoire introuvable : {target}")

    def test_five_tables_and_three_documented_museum_figures(self):
        study = self.studies[0]
        self.assertEqual(len(study.select("table")), 5)
        figures = study.select('figure[data-aton-figure]')
        self.assertEqual(len(figures), 3)
        for obj, inventory in zip(figures, ("1985.328.2", "31.114.1", "24.2.11")):
            self.assertIsNotNone(obj.select_one('img[loading="lazy"]'))
            self.assertIn(inventory, obj.get_text(" ", strip=True))
            self.assertIsNotNone(obj.select_one(
                'a[href^="https://www.metmuseum.org/art/collection/search/"]'))

    def test_reciprocal_link_from_egypt_portal(self):
        link = self.portal.select_one(
            'a[href="/akhetaton-horizon-aton-etude/#horizon-aton-memoire-integral"]')
        self.assertIsNotNone(link)
        self.assertIn("16 chapitres", link.get_text())
        self.assertIsNotNone(self.studies[0].select_one(
            'a[href="/bibliotheque-egypte-ancienne/"]'))


if __name__ == "__main__":
    unittest.main()
