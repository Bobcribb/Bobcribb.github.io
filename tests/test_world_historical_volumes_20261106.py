"""Bibliothèque du monde : accès aux six intégrales historiques, sans duplication."""
from pathlib import Path
import re
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PORTAL = ROOT / "bibliotheque-mythologies-du-monde" / "index.html"
COLLECTION = ROOT / "bibliotheque-mythologies-du-monde"
CSS = ROOT / "assets" / "mythos-historical-volumes.css"
SLUGS = {
    "X": "mythos-volume-10-finno-carelien-kalevala",
    "XII": "mythos-volume-12-koush-meroe-apedemak",
    "XIII": "mythos-volume-13-armenie-vahagn-david-sassoun",
    "XIV": "mythos-volume-14-khmer-angkor-cosmogonies",
    "XV": "mythos-volume-15-philippines-ifugao-hudhud",
    "XIX": "mythos-volume-19-la-galigo-bugis-sawerigading",
}

class HistoricalWorldVolumesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = BeautifulSoup(PORTAL.read_text(encoding="utf-8"), "html.parser")

    def test_single_illustrated_shelf_and_six_unique_integral_links(self):
        shelves = self.doc.select('nav[data-mythos-historical-volumes]')
        self.assertEqual(len(shelves), 1)
        self.assertEqual(shelves[0].get("id"), "mythos-volumes-historiques")
        self.assertTrue(shelves[0].get("aria-label"))
        cards = shelves[0].select("a.mythos-volume-card")
        self.assertEqual(len(cards), len(SLUGS))
        self.assertEqual(
            {c["href"] for c in cards},
            {"/bibliotheque-mythologies-du-monde/" + slug + "/" for slug in SLUGS.values()})
        self.assertEqual(
            {c["data-mythos-historical-volume"] for c in cards}, set(SLUGS))
        self.assertGreaterEqual(len(shelves[0].select("img.mythos-volume-cover")), 5)
        self.assertTrue(all(c.select_one("strong") for c in cards))
        self.assertEqual(len(self.doc.select('nav[data-mythos-historical-volumes]')), 1)

    def test_original_portal_and_historical_readers_remain_complete(self):
        text = self.doc.get_text(" ", strip=True)
        for marker in ("Bibliothèque comparée des mythologies du monde",
                       "Nouveaux horizons", "Méthode universitaire et éthique",
                       "Dictionnaire des dieux"):
            self.assertIn(marker, text)
        self.assertEqual(len(self.doc.select('h2[id^="lecture-section-"]')), 21)
        for volume, slug in SLUGS.items():
            with self.subTest(volume=volume):
                page = COLLECTION / slug / "index.html"
                self.assertTrue(page.is_file())
                html = page.read_text(encoding="utf-8")
                self.assertGreater(len(html), 45000)
                self.assertRegex(html.lower(), r"sources|bibliograph|références")
                reader = BeautifulSoup(html, "html.parser")
                self.assertIsNotNone(reader.select_one("main"))
                self.assertTrue(reader.select_one('a[href="/bibliotheque-mythologies-du-monde/"]'))
        self.assertFalse(self.doc.select('a[href^="/chapitres/"] [data-mythos-historical-volume]'))

    def test_museum_style_mobile_and_accessible(self):
        self.assertEqual(len(self.doc.select('link[href="/assets/mythos-historical-volumes.css?v=20261106"]')), 1)
        css = CSS.read_text(encoding="utf-8")
        for marker in ("@media(max-width:850px)", "@media(max-width:560px)",
                       "@media(max-width:360px)", "min-height:44px",
                       "prefers-reduced-motion", ".mythos-volume-cover"):
            self.assertIn(marker, css)
        for img in self.doc.select(".mythos-volume-cover"):
            self.assertGreater(len(img.get("alt", "")), 35)
            self.assertEqual(img.get("loading"), "lazy")

if __name__ == "__main__":
    unittest.main()
