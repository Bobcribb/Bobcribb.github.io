"""Conserver les huit grands domaines MYTHOS dans les menus reconstruits."""
import sys
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_museum_design import NAV, MORE, header
from build_navigation import NAV as FALLBACK_NAV

PILLARS = (
    "/mythologie-grecque/",
    "/theatre/",
    "/mythologie-comparee/",
    "/origines-du-sacre/",
    "/philosophie/",
    "/civilisations/",
    "/reconstitutions-photorealistes.html",
    "/bibliotheque/",
)
SECONDARY = (
    "/dieux-et-deesses/",
    "/heros-et-heroines/",
    "/recits-mythologiques/",
    "/mythologies/",
    "/bibliotheque-sciences-medecine-antiques/",
    "/parcours/",
    "/catalogue-integral/",
    "/methode-editoriale/",
    "/reconstitutions-antiquite/",
    "/rubriques/",
    "/recherche/",
)


class MainCollectionNavigationTests(unittest.TestCase):
    def test_eight_pillars_and_one_entrance_per_collection(self):
        paths = [url for url, _ in NAV]
        self.assertEqual(tuple(paths), PILLARS)
        self.assertEqual(len(paths), len(set(paths)))
        expanded = [url for url, _ in MORE]
        self.assertEqual(expanded[0], "/")
        self.assertEqual(len(expanded), len(set(expanded)))
        for route in (*PILLARS, *SECONDARY):
            self.assertEqual(expanded.count(route), 1)
        self.assertNotIn("/grande-encyclopedie/", expanded)

    def test_legacy_topics_remain_accessible_in_extended_menu(self):
        doc = header("/civilisations/oceanie/")
        primary = doc.select(".mythos-primary-nav a")
        self.assertEqual(
            tuple(a.get("href") for a in primary), PILLARS
        )
        current = doc.select(".mythos-primary-nav a[aria-current='page']")
        self.assertEqual([a.get("href") for a in current], ["/civilisations/"])
        extended = {a.get("href") for a in doc.select(".mythos-menu nav a")}
        for route in SECONDARY:
            self.assertIn(route, extended)

    def test_initial_generator_matches_final_navigation(self):
        doc = BeautifulSoup(FALLBACK_NAV, "html.parser")
        links = doc.select("nav.site-nav a")
        self.assertEqual(tuple(a.get("href") for a in links), PILLARS)
        self.assertNotIn("/grande-encyclopedie/", [a.get("href") for a in links])

    def test_historical_greek_archive_keeps_unique_canonical_menu(self):
        doc = header("/grande-encyclopedie/registre-integral/")
        for selector in (".mythos-primary-nav", ".mythos-menu nav"):
            links = doc.select(selector + " a[href='/mythologie-grecque/']")
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0].get("aria-current"), "page")


if __name__ == "__main__":
    unittest.main()
