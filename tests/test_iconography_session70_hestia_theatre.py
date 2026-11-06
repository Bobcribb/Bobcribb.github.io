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
        history = state["history"]
        self.assertEqual(state["latest_session"], history[-1])
        matches70 = [row for row in history if row.get("session_number") == 70]
        matches69 = [row for row in history if row.get("session_number") == 69]
        self.assertEqual(len(matches70), 1)
        self.assertEqual(len(matches69), 1)
        session70 = matches70[0]
        self.assertEqual(session70["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session70["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(session70["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session70["new_figures"], 5)
        figures = session70["supplemental_documentary_figures"]["figures"]
        self.assertEqual({row["id"] for row in figures}, {row[1] for row in FIGURES})
        self.assertIn("parallel_audit_pr75", matches69[0])
        for prev, current in zip(history, history[1:]):
            self.assertNotEqual(prev["kind"], current["kind"])
            self.assertEqual(prev["next_kind"], current["kind"])

if __name__ == "__main__":
    unittest.main()
