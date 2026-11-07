"""Tests de publication et de classement pour le dossier historique Nok."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_navigation import get_civilisations, group_continent


NOK_URL = "/bibliotheque-mythologies-du-monde/civilisations-nok-nigeria/"
NOK_PATH = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-nok-nigeria" / "index.html"


class NokCivilisationsTests(unittest.TestCase):
    def test_nok_is_classified_under_africa(self):
        item = {"url": NOK_URL, "title": "Culture Nok, Nigeria"}
        self.assertEqual(group_continent(item), "afrique")
        groups = get_civilisations([item])
        self.assertEqual([record["url"] for record in groups["afrique"]], [NOK_URL])
        self.assertEqual(sum(map(len, groups.values())), 1)

    def test_nok_study_is_complete_and_crosslinked(self):
        article = NOK_PATH.read_text(encoding="utf-8")
        self.assertIn('rel="canonical" href="https://bobmythos.fr' + NOK_URL + '"', article)
        self.assertEqual(article.count('class="mythos-study-section" aria-labelledby="nok-'), 12)
        self.assertIn('id="nok-sources"', article)
        self.assertIn("/civilisations/afrique/", article)
        self.assertIn("/chapitres/origines-du-sacre/736-nok-nigeria-", article)
        self.assertIn("Gabriele Franke", article)
        self.assertIn("10.1093/acrefore", article)
        self.assertIn("commons.wikimedia.org/wiki/File:Nok_sculpture", article)


if __name__ == "__main__":
    unittest.main()
