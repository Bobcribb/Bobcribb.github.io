"""Nan Madol — intégrité de la monographie et parcours dynamiques de l'Océanie."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch

from bs4 import BeautifulSoup
from scripts import build_navigation as navigation

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / "bibliotheque-mythologies-du-monde/civilisations-oceanie-nan-madol-pohnpei/index.html"
NAN_MADOL = "/bibliotheque-mythologies-du-monde/civilisations-oceanie-nan-madol-pohnpei/"
RAPA_NUI = "/bibliotheque-mythologies-du-monde/civilisations-rapa-nui-moai/"
OCEANIA = "/bibliotheque-mythologies-du-monde/civilisations-histoire-oceanie/"


class NanMadolTests(TestCase):
    def test_integral_scholarly_work_and_licenced_documentary_photo(self):
        article = BeautifulSoup(DOCUMENT.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(article.html.get("lang"), "fr")
        self.assertEqual(len(article.select("section.mythos-study-section[id^=section-]")), 15)
        self.assertGreater(len(article.select_one("article").get_text(" ", strip=True).split()), 2600)
        self.assertGreaterEqual(len(article.select("ol.source-list > li")), 12)
        self.assertEqual(len(article.select('nav[aria-label="Fil d\'Ariane"]')), 1)
        self.assertTrue(article.select_one('a.mythos-skip[href="#contenu"]'))
        self.assertTrue(article.select_one('link[rel="canonical"]'))
        self.assertTrue(article.select_one('img[alt][loading="lazy"]'))
        credits = article.select_one("figure figcaption").get_text(" ", strip=True)
        self.assertIn("Patrick Nunn", credits)
        self.assertIn("CC BY-SA 4.0", credits)
        for marker in ("Shen", "McCoy", "UNESCO", "Saudeleur", "Nahnmwarki", "2024", "bibliographie"):
            self.assertIn(marker.casefold(), article.get_text(" ", strip=True).casefold())
        for href in ("/civilisations/oceanie/", OCEANIA, RAPA_NUI, "/mythologie-grecque/"):
            self.assertIsNotNone(article.select_one(f'a[href="{href}"]'))
        self.assertIsNone(article.find(string=lambda s: bool(s) and "Grande encyclopédie" in s))

    def test_oceanic_routing_and_conditional_cards(self):
        indexed = [
            {"url": OCEANIA, "title": "Civilisations — Océanie"},
            {"url": RAPA_NUI, "title": "Civilisations — Rapa Nui"},
            {"url": NAN_MADOL, "title": "Civilisations — Nan Madol"},
        ]
        groups = navigation.get_civilisations(indexed)
        self.assertEqual({e["url"] for e in groups["oceanie"]}, {OCEANIA, RAPA_NUI, NAN_MADOL})
        self.assertEqual(sum(len(v) for k, v in groups.items() if k != "oceanie"), 0)
        with TemporaryDirectory() as temp, patch.object(navigation, "OUT", Path(temp)):
            navigation.create_civilisations(indexed, groups)
            portal = BeautifulSoup(
                (Path(temp) / "civilisations/oceanie/index.html").read_text(encoding="utf-8"),
                "html.parser")
            self.assertEqual(len(portal.select(f'a.portal-card[href="{NAN_MADOL}"]')), 1)
            self.assertEqual(len(portal.select(f'a.portal-card[href="{RAPA_NUI}"]')), 1)
            self.assertTrue(portal.select_one('h2').get_text(strip=True).startswith("Dossiers"))
            # Si la page n'est plus indexée, aucun lien fantôme n'est créé.
            remaining = indexed[:2]
            navigation.create_civilisations(remaining, navigation.get_civilisations(remaining))
            absent = BeautifulSoup(
                (Path(temp) / "civilisations/oceanie/index.html").read_text(encoding="utf-8"),
                "html.parser")
            self.assertIsNone(absent.select_one(f'a[href="{NAN_MADOL}"]'))


if __name__ == "__main__":
    main()
