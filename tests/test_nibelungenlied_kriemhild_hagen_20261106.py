"""Non-régression scientifique et documentaire : troisième dossier germanique."""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques")
CYCLE = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen"
NEW = CYCLE / "nibelungenlied-kriemhild-hagen" / "index.html"
PORTAL = BASE / "index.html"


class NibelungenliedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / NEW).read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.html, "html.parser")

    def test_corpus_and_bibliography(self):
        self.assertGreater(len(self.html), 35000)
        for token in ("Cod. Sang. 857", "Cod. Donaueschingen 63", "Cgm 34",
                      "Nibelungenklage", "Gondichaire", "Hagen", "Kriemhild",
                      "Serfas", "Buschinger", "UNESCO"):
            self.assertIn(token, self.html)
        self.assertIsNotNone(self.doc.find(id="nibelungen-bibliographie"))

    def test_twenty_two_sections_and_anchors(self):
        headings = self.doc.select('h2[id^="nibelungen-"]')
        self.assertEqual(len(headings), 23)
        self.assertIsNotNone(self.doc.find(id="nibelungen-22"))
        self.assertEqual(len(self.doc.select("details.mythos-reading-toc a[href^='#']")), 23)
        all_ids = [x["id"] for x in self.doc.select("[id]")]
        self.assertEqual(len(set(all_ids)), len(all_ids))
        for link in self.doc.select("details.mythos-reading-toc a[href^='#']"):
            self.assertIn(link["href"][1:], all_ids)

    def test_theme_and_factual_figures(self):
        self.assertEqual(self.doc.body.get("class"), ["mythos-design", "mythos-reading"])
        self.assertIsNotNone(self.doc.select_one('link[href="/assets/mythos-museum.css?v=20261104"]'))
        self.assertIsNotNone(self.doc.select_one('script[src="/assets/mythos-reading.js?v=20261104-lecture-2"]'))
        self.assertEqual(len(self.doc.select(".mythos-masthead")), 1)
        self.assertNotIn("mythos-hero.svg", self.html)
        figs = self.doc.select("figure.mythos-documentary-figure")
        self.assertEqual(len(figs), 2)
        for figure in figs:
            caption = figure.get_text(" ", strip=True)
            self.assertIn("Hundeshagen", caption)
            self.assertIn("Wikimedia Commons", caption)
            self.assertIn("domaine public", caption)
            self.assertTrue(figure.img.get("alt"))
            self.assertEqual(figure.img.get("loading"), "lazy")

    def test_reciprocal_links_and_single_portal_entry(self):
        url = "/" + NEW.parent.as_posix() + "/"
        northern = (ROOT / CYCLE / "brynhildr-gudrun" / "index.html").read_text(encoding="utf-8")
        original = (ROOT / CYCLE / "index.html").read_text(encoding="utf-8")
        portal = BeautifulSoup((ROOT / PORTAL).read_text(encoding="utf-8"), "html.parser")
        self.assertIn(url, northern)
        self.assertIn(url, original)
        self.assertIn("/brynhildr-gudrun/", self.html)
        self.assertEqual(len(portal.select('a[href="' + url + '"]')), 1)
        self.assertIn(url, self.doc.select_one('link[rel="canonical"]')["href"])

    def test_no_numbered_cycle_bypass(self):
        self.assertNotIn("editorial/inbox/", str(NEW))
        self.assertNotIn("{{numero}}", self.html)
        self.assertNotIn("{{volume}}", self.html)


if __name__ == "__main__":
    unittest.main()
