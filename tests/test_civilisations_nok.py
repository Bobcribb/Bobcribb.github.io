"""Tests de publication et de classement pour le dossier historique Nok."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations, group_continent


NOK_URL = "/bibliotheque-mythologies-du-monde/civilisations-nok-nigeria/"
NOK_PATH = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-nok-nigeria" / "index.html"


class NokStudyHTMLParser(HTMLParser):
    """Contrôle les attributs HTML sans dépendre de leur ordre de sérialisation."""

    def __init__(self):
        super().__init__()
        self.canonical = None
        self.numbered_sections = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href")
        if (tag == "section"
                and "mythos-study-section" in data.get("class", "").split()
                and data.get("aria-labelledby", "").startswith("nok-")):
            self.numbered_sections += 1


class NokCivilisationsTests(unittest.TestCase):
    def test_nok_is_classified_under_africa(self):
        item = {"url": NOK_URL, "title": "Culture Nok, Nigeria"}
        self.assertEqual(group_continent(item), "afrique")
        groups = get_civilisations([item])
        self.assertEqual([record["url"] for record in groups["afrique"]], [NOK_URL])
        self.assertEqual(sum(map(len, groups.values())), 1)

    def test_nok_study_is_complete_and_crosslinked(self):
        article = NOK_PATH.read_text(encoding="utf-8")
        parsed = NokStudyHTMLParser()
        parsed.feed(article)
        self.assertEqual(parsed.canonical, "https://bobmythos.fr" + NOK_URL)
        self.assertEqual(parsed.numbered_sections, 12)
        self.assertIn('id="nok-sources"', article)
        self.assertIn("/civilisations/afrique/", article)
        self.assertIn("/chapitres/origines-du-sacre/736-nok-nigeria-", article)
        self.assertIn("Gabriele Franke", article)
        self.assertIn("10.1093/acrefore", article)
        self.assertIn("commons.wikimedia.org/wiki/File:Nok_sculpture", article)


    def test_nok_canonical_accepts_both_attribute_orders(self):
        expected = "https://bobmythos.fr" + NOK_URL
        for markup in (
            f'<link rel="canonical" href="{expected}">',
            f'<link href="{expected}" rel="canonical">',
        ):
            with self.subTest(markup=markup):
                parsed = NokStudyHTMLParser()
                parsed.feed(markup)
                self.assertEqual(parsed.canonical, expected)

    def test_nok_canonical_rejects_invalid_links(self):
        expected = "https://bobmythos.fr" + NOK_URL
        for markup in (
            f'<link rel="stylesheet" href="{expected}">',
            f'<link href="{expected}">',
            '<link rel="canonical" href="https://example.org/wrong/">',
        ):
            with self.subTest(markup=markup):
                parsed = NokStudyHTMLParser()
                parsed.feed(markup)
                self.assertNotEqual(parsed.canonical, expected)

    def test_nok_section_count_is_attribute_order_independent(self):
        markup = (
            '<section class="mythos-study-section" aria-labelledby="nok-1"></section>'
            '<section aria-labelledby="nok-2" class="other mythos-study-section"></section>'
            '<section class="mythos-study-section" aria-labelledby="other-1"></section>'
            '<section aria-labelledby="nok-3" class="other"></section>'
        )
        parsed = NokStudyHTMLParser()
        parsed.feed(markup)
        self.assertEqual(parsed.numbered_sections, 2)

if __name__ == "__main__":
    unittest.main()
