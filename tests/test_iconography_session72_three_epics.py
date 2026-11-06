"""Séance 72 — figures patrimoniales, sources et garde d'alternance."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FIGURES = (
    ("philosophie-iliade.html", "icono-iliade-ares-parthenon-frise-s72-20261106", "/media/2026/10/mythos-ares-frise-orientale-parthenon-bloc-iv-twospoonfuls.jpg", "447–433", "parthenonfrieze.gr"),
    ("philosophie-odyssee.html", "icono-odyssee-heracles-lion-nemee-met-s72-20261106", "/media/2026/10/mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg", "Ve siècle", "metmuseum.org/art/collection/search/247235"),
    ("philosophie-theogonie.html", "icono-theogonie-demeter-triptoleme-met-s72-20261106", "/media/2026/10/demeter-triptolemos-peintre-niobides-met-41-162-98.jpg", "460–450", "metmuseum.org/art/collection/search/254270"),
)

class Session72SourcesTests(unittest.TestCase):
    def test_real_artifacts_with_documentary_caveats(self):
        for page, ident, src, date, museum in FIGURES:
            with self.subTest(page=page):
                soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                match = soup.find_all("figure", id=ident)
                self.assertEqual(len(match), 1)
                figure = match[0]
                self.assertEqual(len(figure.find_all("img")), 1)
                image = figure.find("img")
                self.assertEqual(image.get("src"), src)
                self.assertTrue(image.get("alt"))
                self.assertTrue((ROOT / src.lstrip("/")).is_file())
                self.assertEqual(len(soup.select(f'img[src="{src}"]')), 1)
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn(date, caption.get_text(" ", strip=True))
                self.assertIn(museum, str(caption))
                self.assertIn("non générée par IA", str(figure))
                self.assertIn("Statut", str(caption))
                self.assertTrue("CC0" in str(caption) or "CC BY-SA" in str(caption))
                self.assertTrue(any(a.get("href", "").startswith("/") for a in caption.find_all("a")))

    def test_session_72_has_unique_sequence(self):
        state = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        entries = [x for x in state["history"] if x.get("session_number") == 72]
        self.assertEqual(len(entries), 1)
        row = entries[0]
        self.assertEqual(row["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(row["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(row["next_kind"], "AUDIT ET CORRECTION")
        latest = state["latest_session"]
        if latest.get("session_number") == 72:
            self.assertEqual(latest["next_kind"], "AUDIT ET CORRECTION")

if __name__ == "__main__":
    unittest.main()
