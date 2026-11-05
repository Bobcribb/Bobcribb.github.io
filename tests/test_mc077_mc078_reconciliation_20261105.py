"""Réconciliation de deux sujets MC-077 : conservation intégrale et allocation atomique.

Ne publie aucun numéro et ne modifie aucun manuscrit historique.
"""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from comparative_history import historical_id

FIRST = "9e762fc3-2e15-4d58-832a-7b01cb9bd077"
ORIGINAL = "1d8b9a77-c1e5-4b55-9d77-202611050077"
RECONCILED = "c8de648c-1dc3-4de3-8ac6-202611050078"

OLD_CONTINUITY = (
    "Les recherches dans le dépôt n’ont révélé aucune soumission ni monographie "
    "MC-077 antérieure au présent manuscrit. Une détection d’éventuelle arrivée "
    "concurrente reste de la compétence de la procédure transactionnelle."
)
NEW_CONTINUITY = (
    "Le contrôle chronologique postérieur a établi qu’une demande distincte, "
    "« Le parfum du sacré », fut soumise antérieurement sous MC-077 "
    "(UUID 9e762fc3-2e15-4d58-832a-7b01cb9bd077, commit "
    "678068cd4a6b656bdb756c47cc213c5920b01790, 12:07:37 UTC) et conserve "
    "cette identité historique. La soumission originale de la présente étude "
    "(UUID 1d8b9a77-c1e5-4b55-9d77-202611050077, 12:09:19 UTC) reste "
    "intégralement préservée et retenue sous empreinte SHA-256 ; seule cette "
    "nouvelle demande scientifique distincte porte MC-078. Le numéro canonique "
    "du volume sera attribué exclusivement par GitHub Actions."
)


class ReconciliationMC077078(unittest.TestCase):
    def read(self, identity):
        return json.loads((ROOT / "editorial/inbox" / (identity + ".json")).read_text(
            encoding="utf-8"))

    def test_original_is_preserved_under_hash_locked_hold(self):
        holds = json.loads((ROOT / "editorial/holds.json").read_text(encoding="utf-8"))
        self.assertEqual(holds["version"], 1)
        holding = holds["requests"][ORIGINAL]
        raw = (ROOT / "editorial/inbox" / (ORIGINAL + ".json")).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), holding["request_sha256"])
        self.assertEqual(
            holding["request_sha256"],
            "b677888768c94847d77840756f8c222384814adc26c78a3d2434e1dde90aa2a6")
        self.assertNotIn(FIRST, holds["requests"])
        self.assertNotIn(RECONCILED, holds["requests"])

    def test_histories_are_distinct_without_reserving_canonical_number(self):
        first = self.read(FIRST)
        previous = self.read(ORIGINAL)
        next_study = self.read(RECONCILED)
        for manuscript in (first, previous, next_study):
            self.assertEqual(manuscript["version"], 1)
            self.assertEqual(manuscript["collection"], "comparatif")
            self.assertEqual(set(manuscript), {"version", "collection", "slug", "markdown"})
            self.assertIn("{{volume}}", manuscript["markdown"])
            self.assertIn("{{numero}}", manuscript["markdown"])
        self.assertEqual(historical_id(first["markdown"]), "MC-077")
        self.assertEqual(historical_id(previous["markdown"]), "MC-077")
        self.assertEqual(historical_id(next_study["markdown"]), "MC-078")
        self.assertNotEqual(first["slug"], next_study["slug"])
        self.assertNotEqual(previous["slug"], next_study["slug"])

    def test_reissued_monograph_is_integral_except_identification_and_proof(self):
        original = self.read(ORIGINAL)["markdown"]
        adjusted = self.read(RECONCILED)["markdown"]
        expected = original
        for before, after in (
            ("## MC-077 — Entraver les immortels",
             "## MC-078 — Entraver les immortels"),
            ("la cote historique MC-077 est distincte",
             "la cote historique MC-078 est distincte"),
            (OLD_CONTINUITY, NEW_CONTINUITY),
        ):
            self.assertEqual(expected.count(before), 1)
            expected = expected.replace(before, after)
        self.assertEqual(adjusted, expected)
        self.assertGreater(len(adjusted), 60000)
        self.assertIn("Bibliographie", adjusted)
        self.assertIn("### 88. Synthèse épistémique finale", adjusted)


if __name__ == "__main__":
    unittest.main()
