"""Régression du lien documentaire corrigé dans la comédie 91 de MYTHOS."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STEM = "volume-091-nikochares-galateia-polypheme-dithyrambe-philonides-cumin-nereides"
TARGET = "/comedies-grecques-aristophane-menandre/"


class ComedyReferenceLinkTests(unittest.TestCase):
    def test_target_exists_and_both_versions_use_it(self):
        self.assertTrue((ROOT / TARGET.lstrip("/") / "index.html").is_file())
        for filename in (
            ROOT / "chapitres/comedies" / (STEM + ".md"),
            ROOT / "chapitres/comedies" / STEM / "index.html",
        ):
            with self.subTest(path=str(filename)):
                text = filename.read_text(encoding="utf-8")
                self.assertIn(TARGET, text)
                self.assertNotIn("/comedies-grecques/", text)


if __name__ == "__main__":
    unittest.main()
