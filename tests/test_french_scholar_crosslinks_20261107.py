"""Contrôle des liens thématiques vers la bibliographie scientifique française MYTHOS.

Contrôle les 50 ancres scientifiques et les renvois thématiques ; aucun manuscrit canonique
ni aux anciennes références.
"""
from pathlib import Path
from urllib.parse import urlsplit
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BIBLIOGRAPHY = ROOT / "bibliographie" / "index.html"
SOURCES = {
    "hellenistes/index.html": 20,
    "bibliotheque-mesopotamie/index.html": 8,
    "bibliotheque-egypte-ancienne/index.html": 12,
    "bibliotheque-perse-iran-ancien/index.html": 11,
}


def read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


class FrenchScholarCrosslinksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bibliography = read_html(BIBLIOGRAPHY)
        cls.index = cls.bibliography.find(id="chercheurs-francais-parcours")

    def test_index_lists_unique_targeted_studies(self):
        self.assertIsNotNone(self.index)
        links = self.index.select('a[href^="#"]')
        self.assertEqual(len(links), 50)
        targets = [link["href"][1:] for link in links]
        self.assertEqual(len(targets), len(set(targets)))
        for target in targets:
            with self.subTest(target=target):
                matches = self.bibliography.find_all(id=target)
                self.assertEqual(len(matches), 1, f"Ancre absente ou doublée : {target}")

    def test_subject_libraries_point_to_existing_studies(self):
        for relative_path, expected_min in SOURCES.items():
            with self.subTest(source=relative_path):
                doc = read_html(ROOT / relative_path)
                panels = doc.select("section.mythos-crossreferences")
                self.assertEqual(len(panels), 1)
                links = [
                    link["href"]
                    for link in panels[0].select('a[href^="/bibliographie/#"]')
                ]
                targets = [urlsplit(link).fragment for link in links]
                self.assertGreaterEqual(len(targets), expected_min)
                self.assertEqual(len(targets), len(set(targets)))
                for target in targets:
                    self.assertIsNotNone(
                        self.bibliography.find(id=target),
                        f"{relative_path}: destination manquante : {target}",
                    )


if __name__ == "__main__":
    unittest.main()
