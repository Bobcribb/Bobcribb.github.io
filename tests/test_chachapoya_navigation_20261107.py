"""MYTHOS : étude Chachapoya et navigation continentale, sans mutation de manuscrits."""
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations, group_continent
from improve_reading import add_reading, authored_blocks

SLUG = "civilisations-chachapoyas-kuelap-utcubamba"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
ARTICLE = ROOT / "bibliotheque-mythologies-du-monde" / SLUG / "index.html"
ANDES = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-histoire-andes" / "index.html"


class ChachapoyaNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = ARTICLE.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.raw, "html.parser")
        cls.legacy = ANDES.read_text(encoding="utf-8")
        cls.legacy_soup = BeautifulSoup(cls.legacy, "html.parser")

    def test_substantial_integral_study_and_sections(self):
        self.assertGreater(len(self.soup.get_text(" ", strip=True).split()), 3800)
        chapters = self.soup.select("section.mythos-critical-chapter")
        self.assertEqual(len(chapters), 20)
        self.assertEqual(len({s["id"] for s in chapters}), len(chapters))
        self.assertTrue(all(section.select_one("h2") for section in chapters))
        for term in ("Kuélap", "Schjellerup", "Koschmieder", "Laguna de los Cóndores", "PRIAK"):
            self.assertIn(term, self.raw)
        self.assertNotIn("{{numero}}", self.raw)
        self.assertNotIn("{{volume}}", self.raw)

    def test_sources_citations_and_primary_chronicles(self):
        notes = self.soup.select("a.citation-inline")
        items = self.soup.select("#bibliographie ol > li[id]")
        self.assertGreaterEqual(len(notes), 90)
        self.assertEqual(len(items), 15)
        targets = {item["id"] for item in items}
        self.assertEqual(targets, {f"ref-{i}" for i in range(1, 16)})
        self.assertEqual({note["href"][1:] for note in notes}, targets)
        self.assertTrue(all(item.select_one('a[href^="https://"]') for item in items))
        self.assertIn("Cieza de León", self.raw)
        self.assertIn("Garcilaso de la Vega", self.raw)

    def test_legal_photo_map_breadcrumb_and_canonical(self):
        self.assertEqual(
            self.soup.select_one('link[rel="canonical"]')["href"],
            "https://bobmythos.fr" + URL)
        crumbs = self.soup.select_one('nav[aria-label="Fil d\'Ariane"]')
        self.assertIsNotNone(crumbs)
        self.assertIsNotNone(crumbs.select_one('a[href="/civilisations/"]'))
        self.assertIsNotNone(crumbs.select_one('a[href="/civilisations/ameriques/"]'))
        fig = self.soup.select_one("figure.museum-object")
        self.assertIsNotNone(fig.select_one("img[alt]"))
        self.assertIn("Elisolidum", fig.get_text(" ", strip=True))
        self.assertIsNotNone(fig.select_one('a[href="https://creativecommons.org/licenses/by-sa/4.0/"]'))
        self.assertIn("openstreetmap.org", self.raw)
        self.assertFalse(self.soup.select("figure nav, figure button, img[src$='.svg']"))
        self.assertNotIn('Grande encyclopédie</a>', self.raw)

    def test_america_classification_is_explicit(self):
        item = {"url": URL, "title": "Chachapoya : Kuélap et Utcubamba"}
        self.assertEqual(group_continent(item), "ameriques")
        groups = get_civilisations([item])
        self.assertEqual(groups["ameriques"], [item])
        self.assertTrue(all(not groups[k] for k in ("afrique", "asie", "europe", "oceanie")))

    def test_reciprocal_link_and_preservation_of_andes_text(self):
        panel = self.legacy_soup.select_one("#parcours-andes-chachapoyas")
        self.assertIsNotNone(panel)
        self.assertEqual(len(self.legacy_soup.select(f'a[href="{URL}"]')), 1)
        for original in ("Chavín", "Caral", "Wari", "Tiwanaku", "Incas",
                         "APPAREIL CRITIQUE MYTHOS"):
            self.assertIn(original, self.legacy)
        self.assertIsNotNone(self.legacy_soup.select_one(
            'nav.reader-bottom[data-reading-owned="true"]'))

    def test_reader_toc_preserves_authored_sections(self):
        doc = BeautifulSoup(self.raw, "html.parser")
        before = authored_blocks(doc)
        add_reading(doc, URL, {"words": 4400, "minutes": 21})
        self.assertFalse(before - authored_blocks(doc))
        toc = doc.select_one("details.mythos-reading-toc")
        self.assertIsNotNone(toc)
        anchors = [a.get("href", "")[1:] for a in toc.select('a[href^="#"]')]
        self.assertGreaterEqual(len(anchors), 20)
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertTrue(all(doc.find(id=anchor) is not None for anchor in anchors))


if __name__ == "__main__":
    unittest.main()
