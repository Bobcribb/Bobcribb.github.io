"""Le sommaire et les quatre monographies de l'accueil doivent rester cohérents."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from improve_reading import home_work_cards


class HomeWorksTests(unittest.TestCase):
    def test_four_work_cards_cover_greek_epics_and_virgil(self):
        works = home_work_cards()
        self.assertEqual(len(works), 4)
        urls = [work[0] for work in works]
        self.assertEqual(urls, [
            "/philosophie-iliade.html", "/philosophie-odyssee.html",
            "/philosophie-theogonie.html", "/philosophie-eneide.html",
        ])
        self.assertEqual(len(set(urls)), 4)
        self.assertTrue(all((ROOT / url.lstrip("/")).is_file() for url in urls))
        self.assertIn("ÉDITION PARTIELLE", works[-1][3])
        self.assertIn("300 pages", works[-1][2])

    def test_generator_uses_same_four_work_cards_as_public_toc(self):
        generator = (ROOT / "scripts/improve_reading.py").read_text(encoding="utf-8")
        self.assertIn("works = home_work_cards()", generator)
        self.assertIn("<h2>Quatre œuvres à approfondir</h2>", generator)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Quatre œuvres à approfondir", index)
        self.assertIn('href="/philosophie-eneide.html"', index)


if __name__ == "__main__":
    unittest.main()
