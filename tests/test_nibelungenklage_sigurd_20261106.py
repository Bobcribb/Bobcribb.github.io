"""Vérifie le dossier Nibelungenklage sans altérer les sources historiques."""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CYCLE = Path("bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/cycle-sigurd-brynhildr-fafnir-nibelungen")
KLAGE = CYCLE / "nibelungenklage-memoire-deuil" / "index.html"
PAGES = [
    CYCLE / "index.html",
    CYCLE / "brynhildr-gudrun" / "index.html",
    CYCLE / "nibelungenlied-kriemhild-hagen" / "index.html",
    CYCLE / "atli-gunnar-hogni-atlakvida-atlamal" / "index.html",
]
PORTAL = CYCLE.parent / "index.html"
URL = "/" + KLAGE.parent.as_posix() + "/"

class NibelungenklagePublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / KLAGE).read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")

    def test_document_is_complete_not_a_numbered_manuscript(self):
        self.assertGreater(len(self.raw), 35000)
        self.assertIn("La Nibelungenklage", self.doc.title.get_text())
        for phrase in ["Die Klage", "Cod. Sang. 857", "Cod. Donaueschingen 64",
                       "Swemmelin", "Pilgrim", "Bumke", "Buschinger",
                       "deuil", "versions", "Etzel", "Rüdiger"]:
            self.assertIn(phrase, self.raw)
        self.assertNotIn("{{numero}}", self.raw)
        self.assertNotIn("{{volume}}", self.raw)

    def test_hierarchy_and_resolvable_reading_toc(self):
        headings = self.doc.select('h2[id^="klage-"]')
        self.assertEqual(len(headings), 24)
        self.assertIsNotNone(self.doc.find(id="klage-22"))
        self.assertIsNotNone(self.doc.find(id="klage-sources"))
        self.assertIsNotNone(self.doc.find(id="klage-iconographie"))
        ids = [x["id"] for x in self.doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        toc = self.doc.select("details.mythos-reading-toc a[href^='#']")
        self.assertEqual(len(toc), 24)
        for a in toc:
            self.assertIn(a["href"][1:], ids)

    def test_museum_style_preserved_and_image_sources_explicit(self):
        self.assertIn("mythos-design", self.doc.body.get("class", []))
        self.assertIn("mythos-reading", self.doc.body.get("class", []))
        self.assertIsNotNone(self.doc.select_one('link[href="/assets/mythos-museum.css?v=20261104"]'))
        self.assertIsNotNone(self.doc.select_one('script[src="/assets/mythos-reading.js?v=20261104-lecture-2"]'))
        self.assertEqual(len(self.doc.select(".mythos-masthead")), 1)
        self.assertNotIn("mythos-hero.svg", self.raw)
        self.assertNotIn("Grande encyclopédie", self.raw)
        images = self.doc.select(".mythos-klage-document")
        self.assertEqual(len(images), 2)
        for fig in images:
            self.assertIsNotNone(fig.img)
            self.assertTrue(fig.img.get("alt"))
            self.assertEqual(fig.img.get("loading"), "lazy")
            caption = fig.get_text(" ", strip=True)
            self.assertIn("Wikimedia Commons", caption)

    def test_bidirectional_links_and_single_catalog_entry(self):
        for path in PAGES:
            raw = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn(URL, raw, str(path))
        soup = BeautifulSoup((ROOT / PORTAL).read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(len(soup.select('a[href="' + URL + '"]')), 1)
        self.assertIn("/nibelungenlied-kriemhild-hagen/", self.raw)
        self.assertIn("/atli-gunnar-hogni-atlakvida-atlamal/", self.raw)
        canonical = self.doc.select_one('link[rel="canonical"]')
        self.assertIsNotNone(canonical)
        self.assertEqual(canonical["href"], "https://bobmythos.fr" + URL)

if __name__ == "__main__":
    unittest.main()
