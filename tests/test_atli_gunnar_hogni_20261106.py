"""Préservation et publication : quatre monographies du cycle de Sigurd.

Vérifie la quatrième étude sur l'Atlakviða et l'Atlamál sans toucher au
système transactionnel de numérotation des autres collections.
"""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques")
CYCLE = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen"
ATLI = CYCLE / "atli-gunnar-hogni-atlakvida-atlamal" / "index.html"
SIGURD = CYCLE / "index.html"
BRYNHILDR = CYCLE / "brynhildr-gudrun" / "index.html"
NIBELUNGEN = CYCLE / "nibelungenlied-kriemhild-hagen" / "index.html"
PORTAL = BASE / "index.html"
URL = "/" + ATLI.parent.as_posix() + "/"


class AtliCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / ATLI).read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")

    def test_full_text_and_source_apparatus(self):
        self.assertGreater(len(self.raw), 40000)
        for token in ("Atlakviða", "Atlamál", "Dráp Niflunga",
                      "Codex Regius", "Kostbera", "Glaumvör", "Högni",
                      "Hjalli", "Guðrún", "Birkett", "Larrington",
                      "Clark", "Guðmundsdóttir", "Speculum"):
            self.assertIn(token, self.raw)
        self.assertIsNotNone(self.doc.find(id="atli-bibliographie"))
        self.assertIn("histoire", self.doc.get_text(" ", strip=True).lower())

    def test_twenty_eight_sections_and_linked_toc(self):
        named = [node for node in self.doc.select("h2[id]") if node["id"].startswith("atli-")]
        self.assertEqual(len(named), 29)  # 28 sections + bibliographie
        self.assertIsNotNone(self.doc.find(id="atli-28"))
        anchors = self.doc.select('details.mythos-reading-toc a[href^="#"]')
        self.assertEqual(len(anchors), 29)
        ids = [node["id"] for node in self.doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        for anchor in anchors:
            self.assertIn(anchor["href"][1:], ids)

    def test_museum_design_and_documentary_image(self):
        self.assertEqual(self.doc.body.get("data-mythos-design"), "20261104")
        self.assertEqual(len(self.doc.select(".mythos-masthead")), 1)
        self.assertIsNotNone(self.doc.select_one('link[href="/assets/mythos-museum.css?v=20261104"]'))
        self.assertIsNotNone(self.doc.select_one('script[src="/assets/mythos-reading.js?v=20261104-lecture-2"]'))
        figure = self.doc.select_one("figure.mythos-documentary-figure")
        self.assertIsNotNone(figure)
        caption = figure.get_text(" ", strip=True)
        self.assertIn("Hylestad", caption)
        self.assertIn("Fabullus", caption)
        self.assertIn("CC BY-SA 3.0", caption)
        self.assertIn("Wikimedia Commons", caption)
        self.assertIn("Gunnar_in_snakepit_Hylestad.jpg", figure.img["src"])
        self.assertTrue(figure.img.get("alt"))
        self.assertNotIn("mythos-hero.svg", self.raw)

    def test_five_reciprocal_links_and_catalogue(self):
        portal = BeautifulSoup((ROOT / PORTAL).read_text(encoding="utf-8"), "html.parser")
        links = portal.select('a[href*="/cycle-sigurd-brynhildr-fafnir-nibelungen/"]')
        self.assertEqual(len(links), 5)
        self.assertEqual(len(portal.select('a[href="' + URL + '"]')), 1)
        for p in (SIGURD, BRYNHILDR, NIBELUNGEN):
            self.assertIn(URL, (ROOT / p).read_text(encoding="utf-8"), str(p))
        for sub in ("brynhildr-gudrun/", "nibelungenlied-kriemhild-hagen/"):
            self.assertIn(sub, self.raw)
        canonical = self.doc.select_one('link[rel="canonical"]')
        self.assertIsNotNone(canonical)
        self.assertTrue(canonical.get("href", "").endswith(URL))

    def test_no_numbering_or_migration_changes(self):
        self.assertTrue(str(ATLI).startswith("bibliotheque-mythologies-du-monde/"))
        self.assertNotIn("{{numero}}", self.raw)
        self.assertNotIn("{{volume}}", self.raw)
        self.assertNotIn("Grande Encyclopédie", self.raw)
        self.assertIn("XXII. Histoire", (ROOT / SIGURD).read_text(encoding="utf-8"))
        self.assertIn("La lamentation de Guðrún", (ROOT / BRYNHILDR).read_text(encoding="utf-8"))
        self.assertIn("nibelungen-22", (ROOT / NIBELUNGEN).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
