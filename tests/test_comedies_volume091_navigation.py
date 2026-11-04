"""Régression : renvoi du volume XCI vers la page réelle des comédies grecques."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
VOLUME = "chapitres/comedies/volume-091-nikochares-galateia-polypheme-dithyrambe-philonides-cumin-nereides"
DESTINATION = "/comedies-grecques-aristophane-menandre/"


class Volume91ComedyNavigationTests(unittest.TestCase):
    def test_volume_91_backlink_targets_existing_canonical_page(self):
        markdown = (ROOT / (VOLUME + ".md")).read_text(encoding="utf-8")
        rendered = (ROOT / VOLUME / "index.html").read_text(encoding="utf-8")
        target = ROOT / DESTINATION.lstrip("/") / "index.html"

        self.assertTrue(target.is_file(), "La destination du lien doit exister")
        self.assertIn("[Comédies grecques](" + DESTINATION + ")", markdown)
        self.assertNotIn("[Comédies grecques](/comedies-grecques/)", markdown)
        self.assertIn("Volume XCI (91)", markdown)
        self.assertIn("Volume XCI (91)", rendered)

        soup = BeautifulSoup(rendered, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)
                 if a.get_text(" ", strip=True) == "Comédies grecques"]
        self.assertEqual(links, [DESTINATION])
        self.assertNotIn('href="/comedies-grecques/"', rendered)

        target_soup = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
        canonical = target_soup.find("link", rel="canonical")
        self.assertIsNotNone(canonical)
        self.assertEqual(canonical.get("href"), "https://bobmythos.fr" + DESTINATION)


if __name__ == "__main__":
    unittest.main()
