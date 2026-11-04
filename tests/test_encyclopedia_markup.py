"""Regression: the six encyclopedia collection lists are valid ordered lists."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as navigation


ENTRIES = [
    {"title": "Phèmè — étude intégrale", "url": "/chapitres/encyclopedie/chapitre-388-pheme/"},
    {"title": "Origines du sacré — rites", "url": "/chapitres/origines-du-sacre/614-terres-sacrees/"},
    {"title": "Comédie grecque", "url": "/chapitres/comedies/volume-067-sterrhoi/"},
    {"title": "Comparatisme", "url": "/chapitres/comparatif/volume-clxxxix-maat-isfet/"},
    {"title": "Égypte ancienne", "url": "/bibliotheque-egypte-ancienne/osiris/"},
    {"title": "Bibliothèque", "url": "/bibliotheque/"},
]


class EncyclopediaMarkupTests(unittest.TestCase):
    def test_six_collections_and_all_urls_survive_valid_ordered_lists(self):
        with TemporaryDirectory() as temporary, patch.object(navigation, "OUT", Path(temporary)):
            navigation.create_encyclopedia(ENTRIES)
            page = Path(temporary) / "grande-encyclopedie/index.html"
            raw = page.read_text(encoding="utf-8")
            # The raw markup must be paired before any HTML parser repairs it.
            self.assertEqual(raw.count("<ol"), raw.count("</ol>"))
            self.assertNotIn("</ul>", raw)
            self.assertEqual(raw.count("<ol"), 7)
            doc = BeautifulSoup(raw, "html.parser")
            toc = doc.select_one('nav[aria-label="Collections encyclopédiques"] ol')
            self.assertEqual(len(toc.select(":scope > li")), 6)
            self.assertEqual(len(doc.select("section.portal-section[id^=collection-]")), 6)
            self.assertEqual(len(doc.select(".chapter-list > li[data-public-id]")), len(ENTRIES))
            for entry in ENTRIES:
                self.assertEqual(len(doc.select('a[href="' + entry["url"] + '"]')), 1)
            ids = [x["data-public-id"] for x in doc.select(".chapter-list > li")]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(identifier.startswith("RG-") for identifier in ids))

    def test_duplicate_urls_remain_rejected(self):
        with TemporaryDirectory() as temporary, patch.object(navigation, "OUT", Path(temporary)):
            with self.assertRaisesRegex(RuntimeError, "URL dupliquée"):
                navigation.create_encyclopedia(ENTRIES + [ENTRIES[0]])


if __name__ == "__main__":
    unittest.main()
