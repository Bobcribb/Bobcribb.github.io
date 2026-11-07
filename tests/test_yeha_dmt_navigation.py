"""Étude Yeha-Dʿmt : continuité des sources, classement, lecteur et preuves scientifiques."""
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations
from improve_reading import add_reading, authored_blocks

SLUG = "civilisations-yeha-dmt-pre-aksoum"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
COLLECTION = ROOT / "bibliotheque-mythologies-du-monde"
NEW = COLLECTION / SLUG / "index.html"
AKSUM = COLLECTION / "civilisations-histoire-aksoum" / "index.html"


class YehaPreAksumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = NEW.read_text(encoding="utf-8")
        cls.article = BeautifulSoup(cls.source, "html.parser")
        cls.aksum_source = AKSUM.read_text(encoding="utf-8")
        cls.aksum = BeautifulSoup(cls.aksum_source, "html.parser")

    def test_full_study_is_substantial_and_unumbered(self):
        self.assertGreater(len(self.article.get_text(" ", strip=True).split()), 3700)
        chapters = self.article.select("section.mythos-critical-chapter")
        self.assertEqual(len(chapters), 21)
        self.assertEqual(len({chapter["id"] for chapter in chapters}), 21)
        self.assertFalse(any(not chapter.select_one("h2") for chapter in chapters))
        self.assertNotIn("{{numero}}", self.source)
        self.assertNotIn("{{volume}}", self.source)
        self.assertIn("Gerlach", self.source)
        self.assertIn("Phillipson", self.source)
        self.assertIn("Fattovich", self.source)
        self.assertIn("Dʿmt", self.source)

    def test_references_and_note_targets_are_complete(self):
        bibliography = self.article.select("#bibliographie ol > li")
        self.assertEqual(len(bibliography), 13)
        ids = {x["id"] for x in bibliography}
        self.assertEqual(ids, {f"ref-{i}" for i in range(1, 14)})
        notes = self.article.select("a.citation-inline")
        self.assertGreaterEqual(len(notes), 80)
        self.assertEqual({x["href"][1:] for x in notes}, ids)
        self.assertTrue(all(note.get("aria-label", "").startswith("Voir la référence ")
                            for note in notes))
        self.assertTrue(all(x.select_one("a[href^='https://']") for x in bibliography))

    def test_breadcrumbs_canonical_and_navigation(self):
        canonical = self.article.select_one('link[rel="canonical"]')
        self.assertEqual(canonical.get("href"), "https://bobmythos.fr" + URL)
        crumbs = self.article.select_one('nav[aria-label="Fil d\'Ariane"]')
        self.assertIsNotNone(crumbs)
        for path in ("/civilisations/", "/civilisations/afrique/",
                     "/bibliotheque-mythologies-du-monde/civilisations-histoire-aksoum/"):
            self.assertIsNotNone(crumbs.select_one(f'a[href="{path}"]'))
        self.assertIsNotNone(self.article.select_one('nav.site-nav[aria-label="Navigation principale"]'))
        self.assertFalse(self.article.select(".portal-section"))
        self.assertIn("/mythologie-grecque/", self.source)
        self.assertNotIn('Grande encyclopédie</a>', self.source)

    def test_archaeological_photograph_has_legal_attribution(self):
        figure = self.article.select_one("figure.museum-object")
        self.assertIsNotNone(figure)
        self.assertIsNotNone(figure.select_one('img[alt]'))
        self.assertIn("A. Davey", figure.get_text(" ", strip=True))
        self.assertIsNotNone(figure.select_one(
            'a[href="https://creativecommons.org/licenses/by/2.0/"]'))
        self.assertTrue(figure.select_one("a[href^='https://commons.wikimedia.org/']"))
        self.assertFalse(figure.select_one("nav, button, form"))
        self.assertFalse(self.article.select_one("img[src$='.svg']"))
        self.assertIn("sans modification", figure.get_text(" ", strip=True))

    def test_aksum_reciprocal_link_is_unique_and_additive(self):
        section = self.aksum.select_one("#aksoum-yeha-parcours")
        self.assertIsNotNone(section)
        self.assertEqual(len(self.aksum.select("#aksoum-yeha-parcours")), 1)
        self.assertEqual(len(self.aksum.select(f'a[href="{URL}"]')), 1)
        self.assertIn("DOSSIER UNIVERSITAIRE APPROFONDI", self.aksum_source)
        self.assertIn("Frumentius", self.aksum_source)
        self.assertIn("lecture-section-9", self.aksum_source)
        self.assertIn("civilisations-histoire-arabie-antique", self.aksum_source)
        self.assertEqual(len(self.aksum.select('nav.reader-bottom[data-reading-owned="true"]')), 1)

    def test_african_portal_discovery_needs_no_generator_change(self):
        groups = get_civilisations([{"url": URL, "title": "Yeha et Dʿmt"}])
        self.assertEqual([x["url"] for x in groups["afrique"]], [URL])
        self.assertTrue(all(not groups[k] for k in
                            ("europe", "asie", "ameriques", "oceanie")))

    def test_reader_generates_toc_without_losing_authored_blocks(self):
        document = BeautifulSoup(self.source, "html.parser")
        before = authored_blocks(document)
        add_reading(document, URL, {"words": 4500, "minutes": 21})
        self.assertFalse(before - authored_blocks(document))
        tocs = document.select("details.mythos-reading-toc")
        self.assertEqual(len(tocs), 1)
        urls = [a["href"] for a in tocs[0].select('a[href^="#"]')]
        self.assertGreaterEqual(len(urls), 21)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(document.find(id=target[1:]) is not None for target in urls))


if __name__ == "__main__":
    unittest.main()
