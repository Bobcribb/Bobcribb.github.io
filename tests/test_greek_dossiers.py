"""Regroupements du corpus grec : couverture intégrale et cotes inchangées."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_corpus import CHAPTER_CYCLES, chapter_dossiers


class GreekDossierTests(unittest.TestCase):
    def test_canonical_manuscripts_are_each_in_one_dossier(self):
        paths = sorted((ROOT / "chapitres/encyclopedie").glob("chapitre-*.md"))
        self.assertGreaterEqual(len(paths), 86)
        chapters = []
        for path in paths:
            match = re.match(r"chapitre-(\d+)-", path.name)
            if match:
                chapters.append((int(match.group(1)), path.stem,
                                 "/chapitres/encyclopedie/" + path.stem + "/",
                                 path.stem))
        dossiers = chapter_dossiers(chapters)
        links = [url for _, _, _, items in dossiers for url, _ in items]
        self.assertEqual(len(links), len(chapters))
        self.assertEqual(len(set(links)), len(chapters))
        self.assertEqual(set(links), {x[2] for x in chapters})
        self.assertGreaterEqual(len(dossiers), 8)
        self.assertEqual({key for key, _, _, _ in dossiers
                          if key != "autres-etudes"},
                         {key for key, _, _, _, _ in CHAPTER_CYCLES})

    def test_future_chapters_stay_accessible_without_invented_classification(self):
        rows = [(259, "helios", "/chapitres/encyclopedie/chapitre-259-helios/", "Hélios"),
                (389, "future", "/chapitres/encyclopedie/chapitre-389-future/", "Étude ajoutée")]
        dossiers = chapter_dossiers(rows)
        self.assertEqual(dossiers[-1][0], "autres-etudes")
        self.assertEqual(dossiers[-1][-1], [(rows[1][2], rows[1][3])])

    def test_duplicate_source_links_are_rejected(self):
        row = (305, "pandion", "/chapitres/encyclopedie/chapitre-305-pandion/", "Pandion")
        with self.assertRaisesRegex(RuntimeError, "même URL deux fois"):
            chapter_dossiers([row, row])


if __name__ == "__main__":
    unittest.main()
