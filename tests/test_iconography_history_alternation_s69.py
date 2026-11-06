"""MYTHOS : garde contre deux séances horaires successives du même type."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "MYTHOS_ICONOGRAPHIE_ALTERNANCE.json"
AUDIT = "AUDIT ET CORRECTION"
ICONO = "ENRICHISSEMENT ICONOGRAPHIQUE"


class HistoryAlternationTests(unittest.TestCase):
    def test_all_recorded_transitions_are_strict(self):
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        history = report["history"]
        self.assertGreaterEqual(len(history), 69)
        self.assertEqual(report["latest_session"], history[-1])
        for i, session in enumerate(history):
            self.assertIn(session["kind"], (AUDIT, ICONO))
            expected_opposite = ICONO if session["kind"] == AUDIT else AUDIT
            self.assertEqual(expected_opposite, session["next_kind"])
            self.assertEqual(expected_opposite, session["previous_kind"])
            if i:
                self.assertNotEqual(history[i - 1]["kind"], session["kind"])
            if i + 1 < len(history):
                self.assertEqual(history[i + 1]["kind"], session["next_kind"])

    def test_session69_is_single_audit_following_68(self):
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        history = report["history"]
        matching = [i for i, session in enumerate(history)
                    if session.get("scope", "").startswith("Séance 69 :")]
        self.assertEqual([68], matching)
        session = history[matching[0]]
        self.assertEqual(AUDIT, session["kind"])
        self.assertEqual(ICONO, history[matching[0] - 1]["kind"])
        self.assertEqual(ICONO, session["next_kind"])
        self.assertEqual("Séance 70 — ENRICHISSEMENT ICONOGRAPHIQUE",
                         session["next_session"])


if __name__ == "__main__":
    unittest.main()
