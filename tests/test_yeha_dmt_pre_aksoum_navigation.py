"""Yeha-Dʿmt : vérification du corpus, des sources, de la navigation et des archives."""
from pathlib import Path
import re
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations
from improve_reading import add_reading, authored_blocks

COLLECTION = ROOT / "bibliotheque-mythologies-du-monde"
SLUG = "civilisations-yeha-dmt-pre-aksoum"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
STUDY = COLLECTION / SLUG / "index.html"
AKSUM = COLLECTION / "civilisations-histoire-aksoum" / "index.html"


class YehaDmtCivilisationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = STUDY.read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")
        cls.aksum_raw = AKSUM.read_text(encoding="utf-8")
        cls.aksum = BeautifulSoup(cls.aksum_raw, "html.parser")

    def test_substantial_complete_and_unnumbered(self):
        words = len(self.doc.get_text(" ", strip=True).split())
        self.assertGreaterEqual(words, 3400)
        sections = self.doc.select("section.mythos-critical-chapter")
        self.assertEqual(len(sections), 21)
        self.assertEqual(len({x["id"] for x in sections}), 21)
        self.assertIn("Dʿmt", self.raw)
        self.assertIn("Gerlach", self.raw)
        self.assertIn("Japp", self.raw)
        self.assertIn("Fattovich", self.raw)
        self.assertIn("Phillipson", self.raw)
        self.assertNotIn("{{numero}}", self.raw)
        self.assertNotIn("{{volume}}", self.raw)

    def test_primary_navigation_precedes_authored_breadcrumb(self):
        navigations = self.doc.select("nav")
        self.assertGreaterEqual(len(navigations), 2)
        self.assertEqual(navigations[0].get("aria-label"), "Navigation principale")
        breadcrumb = self.doc.select_one("nav.greek-folder-breadcrumb")
        self.assertIsNotNone(breadcrumb)
        for target in ("/civilisations/", "/civilisations/afrique/",
                       "/bibliotheque-mythologies-du-monde/civilisations-histoire-aksoum/"):
            self.assertIsNotNone(breadcrumb.select_one('a[href="' + target + '"]'))
        self.assertEqual(self.doc.select_one('link[rel="canonical"]')["href"],
                         "https://bobmythos.fr" + URL)
        # Le générateur remplace seulement le premier nav. Il ne doit pas
        # détruire le fil d'Ariane rédigé juste après le header.
        simulated = re.sub(r"<nav(?:\s[^>]*)?>[\s\S]*?</nav>",
                           "<nav class='site-nav'>Navigation générée</nav>",
                           self.raw, count=1, flags=re.IGNORECASE)
        self.assertIn("Fil d'Ariane", simulated)
        self.assertIn('class="greek-folder-breadcrumb"', simulated)

    def test_references_and_accessible_note_targets(self):
        bibliography = self.doc.select("#bibliographie ol > li")
        self.assertEqual([entry.get("id") for entry in bibliography],
                         [f"ref-{i}" for i in range(1, 14)])
        calls = self.doc.select("a.citation-inline")
        self.assertGreaterEqual(len(calls), 90)
        targets = {a.get("href", "") for a in calls}
        self.assertEqual(targets, {f"#ref-{i}" for i in range(1, 14)})
        self.assertTrue(all(a.get("aria-label", "").startswith("Voir la référence")
                            for a in calls))
        self.assertIn("10.34780/qva6-b73q", self.raw)
        self.assertIn("10.34780/m6vdgk03", self.raw)
        self.assertIn("whc.unesco.org/en/tentativelists/6477", self.raw)
        self.assertIn("dasi.cnr.it", self.raw)

    def test_image_license_and_legal_map(self):
        figure = self.doc.select_one("figure.museum-object")
        self.assertIsNotNone(figure)
        photo = figure.select_one("img")
        self.assertIn("The_Gates_of_the_Temple_of_the_Moon", photo["src"])
        self.assertIn("Photographie réelle", photo["alt"])
        self.assertIn("A. Davey", figure.get_text(" ", strip=True))
        self.assertIsNotNone(
            figure.select_one('a[href="https://creativecommons.org/licenses/by/2.0/"]'))
        self.assertIsNotNone(
            self.doc.select_one('a[href^="https://www.openstreetmap.org/#map="]'))
        self.assertIsNone(figure.select_one("nav, form, button"))
        self.assertIsNone(self.doc.select_one("img[src$='.svg']"))

    def test_automatic_africa_grouping_without_generator_edit(self):
        groups = get_civilisations([{"url": URL, "title": "Yeha et Dʿmt"}])
        self.assertEqual([entry["url"] for entry in groups["afrique"]], [URL])
        self.assertEqual(sum(len(group) for group in groups.values()), 1)

    def test_aksoum_keeps_old_text_and_one_reciprocal_link(self):
        self.assertGreater(len(self.aksum_raw), 22000)
        self.assertIn("Les inscriptions attribuées à Ezana", self.aksum_raw)
        self.assertIn("Frumentius, l’Église", self.aksum_raw)
        self.assertIn("Le monde d’Aksoum et le royaume de", self.aksum_raw)
        block = self.aksum.select("#aksoum-yeha-parcours")
        self.assertEqual(len(block), 1)
        self.assertEqual(len(block[0].select('a[href="' + URL + '"]')), 1)
        self.assertEqual(self.aksum_raw.count('href="' + URL + '"'), 1)
        self.assertEqual(len(self.aksum.select('nav.reader-bottom[data-reading-owned="true"]')), 1)

    def test_reader_keeps_all_scientific_blocks_and_notes(self):
        doc = BeautifulSoup(self.raw, "html.parser")
        before = authored_blocks(doc)
        add_reading(doc, URL, {"words": 4200, "minutes": 20})
        self.assertFalse(before - authored_blocks(doc))
        toc = doc.select_one("details.mythos-reading-toc")
        self.assertIsNotNone(toc)
        anchors = [a.get("href") for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertGreaterEqual(len(anchors), 22)
        self.assertTrue(all(doc.find(id=href[1:]) for href in anchors))


if __name__ == "__main__":
    unittest.main()
