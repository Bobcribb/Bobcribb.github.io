"""Protection de la monographie Nabatéens : études, liens, droits et texte intégral."""
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations
from improve_reading import add_reading, authored_blocks

COLLECTION = ROOT / "bibliotheque-mythologies-du-monde"
SLUG = "civilisations-nabateens-petra-hegra-epigraphie-eau"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
SOURCE = COLLECTION / SLUG / "index.html"
OVERVIEW = COLLECTION / "civilisations-histoire-arabie-antique" / "index.html"


class NabateensPetraHegraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = SOURCE.read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")
        cls.overview_raw = OVERVIEW.read_text(encoding="utf-8")
        cls.overview = BeautifulSoup(cls.overview_raw, "html.parser")

    def test_substantial_unnumbered_source_and_bibliography(self):
        self.assertGreater(len(self.doc.get_text(" ", strip=True).split()), 3700)
        self.assertEqual(len(self.doc.select("section.mythos-critical-chapter")), 20)
        refs = self.doc.select("#bibliographie ol > li")
        self.assertEqual(len(refs), 14)
        self.assertEqual([x.get("id") for x in refs],
                         [f"ref-{i}" for i in range(1, 15)])
        self.assertIn("Diodore", self.raw)
        self.assertIn("Strabon", self.raw)
        self.assertIn("Nehmé", self.raw)
        self.assertIn("archeologie.culture.gouv.fr/fr/hegra", self.raw)
        self.assertIn("whc.unesco.org", self.raw)
        self.assertNotIn("{{numero}}", self.raw)

    def test_breadcrumbs_chapter_anchors_and_canonical(self):
        crumbs = self.doc.select_one('nav[aria-label="Fil d\'Ariane"]')
        self.assertIsNotNone(crumbs)
        for url in ("/civilisations/", "/civilisations/asie/",
                    "/bibliotheque-mythologies-du-monde/civilisations-histoire-arabie-antique/"):
            self.assertTrue(crumbs.select_one('a[href="' + url + '"]'))
        anchors = [s.get("id") for s in self.doc.select("section.mythos-critical-chapter")]
        self.assertEqual(len(set(anchors)), 20)
        self.assertTrue(all(anchors))
        canonical = self.doc.select_one('link[rel="canonical"]')
        self.assertEqual(canonical.get("href"), "https://bobmythos.fr" + URL)

    def test_overview_is_unchanged_except_unique_approved_link(self):
        self.assertIn("DOSSIER UNIVERSITAIRE APPROFONDI", self.overview_raw)
        self.assertIn("Pétra et les Nabatéens : pierre et techniques hydrauliques", self.overview_raw)
        self.assertEqual(len(self.overview.select("#arabies-nabateens-parcours")), 1)
        links = self.overview.select("#arabies-nabateens-parcours a")
        self.assertEqual(sum(a.get("href") == URL for a in links), 1)
        self.assertTrue(any("civilisations-palmyre-zenobie" in a.get("href", "")
                            for a in links))
        self.assertEqual(len(self.overview.select(
            'nav.reader-bottom[data-reading-owned="true"]')), 1)

    def test_image_is_provenanced_without_25d_or_embedded_menu(self):
        figure = self.doc.select_one("figure.museum-object")
        self.assertIsNotNone(figure)
        img = figure.select_one("img")
        self.assertIn("Al_Khazneh.jpg", img.get("src", ""))
        self.assertIn("Photographie", img.get("alt", ""))
        self.assertIn("Bernard Gagnon", figure.get_text(" ", strip=True))
        self.assertIsNotNone(figure.select_one(
            'a[href="https://creativecommons.org/licenses/by-sa/3.0/"]'))
        self.assertFalse(figure.select_one("nav, button, form"))
        self.assertFalse(self.doc.select_one("img[src$='.svg']"))
        self.assertNotIn("Grande encyclopédie</a>", self.raw)

    def test_asian_grouping_without_generator_edits(self):
        groups = get_civilisations([{"url": URL, "title": "Nabatéens et Pétra"}])
        self.assertEqual(len(groups["asie"]), 1)
        self.assertTrue(all(not groups[k] for k in
                            ("afrique", "europe", "ameriques", "oceanie")))

    def test_all_critical_citations_link_to_existing_bibliography(self):
        calls = self.doc.select("a.citation-inline")
        self.assertGreaterEqual(len(calls), 40)
        known = {x.get("id") for x in self.doc.select("#bibliographie li[id]")}
        targets = {a.get("href", "")[1:] for a in calls}
        self.assertTrue(targets.issubset(known))
        self.assertEqual(targets, {f"ref-{i}" for i in range(1, 15)})
        self.assertTrue(all(a.get("aria-label", "").startswith("Voir la référence ")
                            for a in calls))

    def test_generated_reader_preserves_every_authored_block(self):
        # Les éléments du manuscrit ne doivent jamais être supprimés par le lecteur.
        document = BeautifulSoup(self.raw, "html.parser")
        before = authored_blocks(document)
        add_reading(document, URL, {"words": 4400, "minutes": 20})
        self.assertFalse(before - authored_blocks(document))
        self.assertEqual(len(document.select("details.mythos-reading-toc")), 1)
        toc = document.select_one("details.mythos-reading-toc")
        hrefs = [a.get("href") for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(hrefs), len(set(hrefs)))
        self.assertTrue(all(document.find(id=href[1:]) for href in hrefs))


if __name__ == "__main__":
    unittest.main()
