"""Cultures aïnoues : étude intégrale, liens, provenance, sommaire et classement."""
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
SLUG = "civilisations-ainou-hokkaido-sakhaline-cultures-vivantes"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
SOURCE = COLLECTION / SLUG / "index.html"
JOMON = COLLECTION / "civilisations-jomon-japon" / "index.html"
JAPAN = COLLECTION / "civilisations-histoire-japon-coree" / "index.html"


class AinouCulturesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.study = BeautifulSoup(cls.source, "html.parser")
        cls.jomon_source = JOMON.read_text(encoding="utf-8")
        cls.jomon = BeautifulSoup(cls.jomon_source, "html.parser")

    def test_integral_unnumbered_study_with_distinct_scholarly_focus(self):
        self.assertGreaterEqual(len(self.study.get_text(" ", strip=True).split()), 3800)
        chapters = self.study.select("section.mythos-critical-chapter")
        self.assertEqual(len(chapters), 22)
        ids = [x.get("id") for x in chapters]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(c.h2 for c in chapters))
        self.assertIn("Chiri Yukie", self.source)
        self.assertIn("Shakushain", self.source)
        self.assertIn("Satsumon", self.source)
        self.assertIn("Okhotsk", self.source)
        self.assertIn("colonisation", self.source)
        self.assertNotIn("{{numero}}", self.source)
        self.assertNotIn("{{volume}}", self.source)

    def test_16_bibliographic_entries_and_anchored_notes(self):
        refs = self.study.select("#bibliographie ol > li")
        self.assertEqual([x.get("id") for x in refs],
                         [f"ref-{i}" for i in range(1, 17)])
        notes = self.study.select("a.citation-inline")
        self.assertGreaterEqual(len(notes), 100)
        self.assertEqual({x.get("href") for x in notes},
                         {f"#ref-{i}" for i in range(1, 17)})
        self.assertTrue(all(x.get("aria-label", "").startswith("Voir la référence")
                            for x in notes))
        self.assertTrue(all(x.select_one('a[href^="https://"]') for x in refs))

    def test_legally_sourced_actual_museum_photo_and_map(self):
        figure = self.study.select_one("figure.museum-object")
        self.assertIsNotNone(figure)
        photo = figure.select_one("img")
        self.assertIn("Inau_in_National_Ainu_Museum.jpg", photo.get("src", ""))
        self.assertIn("Musée", photo.get("alt", ""))
        self.assertIn("掬茶", figure.get_text(" ", strip=True))
        self.assertIsNotNone(figure.select_one(
            'a[href="https://creativecommons.org/licenses/by-sa/4.0/"]'))
        self.assertTrue(self.study.select_one(
            'a[href^="https://www.openstreetmap.org/"]'))
        self.assertFalse(figure.select_one("nav, button, form"))
        self.assertFalse(self.study.select_one("img[src$='.svg']"))

    def test_canonical_and_accessible_trail_survive_nav_generation(self):
        canon = self.study.select_one('link[rel="canonical"]')
        self.assertEqual(canon["href"], "https://bobmythos.fr" + URL)
        nav = self.study.select_one('nav.site-nav[aria-label="Navigation principale"]')
        breadcrumb = self.study.select_one("nav.greek-folder-breadcrumb")
        self.assertIsNotNone(nav)
        self.assertIsNotNone(breadcrumb)
        self.assertEqual(self.study.select("nav").index(nav), 0)
        for x in ("/civilisations/", "/civilisations/asie/",
                  "/bibliotheque-mythologies-du-monde/civilisations-histoire-japon-coree/"):
            self.assertIsNotNone(breadcrumb.select_one('a[href="' + x + '"]'))
        generated = re.sub(r"<nav(?:\s[^>]*)?>[\s\S]*?</nav>",
                           '<nav class="site-nav">Menu reconstruit</nav>',
                           self.source, count=1, flags=re.IGNORECASE)
        self.assertIn("Fil d'Ariane", generated)
        self.assertIn('class="greek-folder-breadcrumb"', generated)
        self.assertNotIn("Grande encyclopédie</a>", self.source)

    def test_existing_jomon_is_complete_and_one_link_is_additive(self):
        original_headers = [h.get_text(" ", strip=True) for h in
                            self.jomon.select("h2.wp-block-heading")]
        self.assertEqual(len(original_headers), 8)
        self.assertIn("Jōmon, Yayoi et religions du Japon ancien",
                      original_headers)
        block = self.jomon.select("#jomon-ainou-distinction")
        self.assertEqual(len(block), 1)
        self.assertEqual(len(block[0].select('a[href="' + URL + '"]')), 1)
        self.assertEqual(self.jomon_source.count('href="' + URL + '"'), 1)
        self.assertEqual(len(self.jomon.select(
            'nav.reader-bottom[data-reading-owned="true"]')), 1)
        self.assertEqual(self.jomon.select_one('link[rel="canonical"]')["href"],
                         "https://bobmythos.fr/bibliotheque-mythologies-du-monde/civilisations-jomon-japon/")

    def test_japan_korea_general_study_links_back_without_rewriting_it(self):
        source = JAPAN.read_text(encoding="utf-8")
        page = BeautifulSoup(source, "html.parser")
        block = page.select_one("#japon-coree-ainou-parcours")
        self.assertIsNotNone(block)
        self.assertEqual(len(block.select('a[href="' + URL + '"]')), 1)
        self.assertEqual(source.count('href="' + URL + '"'), 1)
        self.assertIn("Satsumon", block.get_text(" ", strip=True))
        self.assertIn("Okhotsk", block.get_text(" ", strip=True))
        self.assertIn("Yamato", block.get_text(" ", strip=True))
        self.assertEqual(
            page.select_one('link[rel="canonical"]')["href"],
            "https://bobmythos.fr/bibliotheque-mythologies-du-monde/civilisations-histoire-japon-coree/"
        )
        self.assertEqual(
            len(page.select('nav.reader-bottom[data-reading-owned="true"]')), 1
        )
        self.assertEqual(
            len(page.select("h2.wp-block-heading")), 9
        )

    def test_classification_auto_in_asia_without_shared_generator_edit(self):
        groups = get_civilisations([{"url": URL, "title": "Cultures aïnoues"}])
        self.assertEqual([x["url"] for x in groups["asie"]], [URL])
        self.assertEqual(sum(map(len, groups.values())), 1)

    def test_reading_interface_preserves_100_percent_of_authored_blocks(self):
        document = BeautifulSoup(self.source, "html.parser")
        before = authored_blocks(document)
        add_reading(document, URL, {"words": 4300, "minutes": 20})
        self.assertFalse(before - authored_blocks(document))
        toc = document.select_one("details.mythos-reading-toc")
        self.assertIsNotNone(toc)
        anchors = [a["href"] for a in toc.select('a[href^="#"]')]
        self.assertGreaterEqual(len(anchors), 23)
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertTrue(all(document.find(id=href[1:]) for href in anchors))


if __name__ == "__main__":
    unittest.main()
