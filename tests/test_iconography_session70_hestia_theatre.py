"""Contrôle documentaire et alternance MYTHOS — séance 70."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = (
    ("dieu-hestia/index.html", "icono-hestia-laraire-vettii-comparaison-s70-20261106", "/media/2026/10/mythos-lararium-maison-vettii-pompei-lorente-waterborough.jpg", "Casa_dei_Vettii_-_Larario.jpg", "Ier siècle"),
    ("theatre-grec.html", "icono-theatre-masques-met-2001-767-s70-20261106", "/media/2026/10/mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg", "metmuseum.org/art/collection/search/257595", "Ier siècle"),
)

class TestSession70Iconography(unittest.TestCase):
    def test_figures_artifacts_and_credit(self):
        for page, identifier, asset, source, date in FIGURES:
            with self.subTest(page=page):
                original = (ROOT / page).read_text(encoding="utf-8")
                figure = re.findall(r'<figure\b[^>]*\bid="' + re.escape(identifier) + r'"[^>]*>[\s\S]*?</figure>', original, flags=re.I)
                self.assertEqual(len(figure), 1)
                markup = figure[0]
                self.assertIn('src="' + asset + '"', markup)
                self.assertTrue((ROOT / asset.lstrip("/")).is_file())
                for marker in ('<figcaption>', 'alt="', source, date, "Statut", "non générée par IA"):
                    self.assertIn(marker, markup)

    def test_alternance_et_navigation(self):
        hestia = (ROOT / FIGURES[0][0]).read_text(encoding="utf-8")
        theatre = (ROOT / FIGURES[1][0]).read_text(encoding="utf-8")
        self.assertIn('id="lecture-section-4"', hestia)
        self.assertIn('id="lecture-section-1"', theatre)
        state = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        latest = state["latest_session"]
        self.assertEqual(latest["session_number"], 70)
        self.assertEqual(latest["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(latest["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(latest["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(sum(row.get("session_number") == 70 for row in state["history"]), 1)

if __name__ == "__main__":
    unittest.main()
