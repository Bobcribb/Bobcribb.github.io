"""Contrôle de conservation de MC-078, sans attribuer de numéro de volume.

Les deux textes sources sont lus depuis la file publique existante ; les
manuscrits, reçus, archives et planifications restent inchangés.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from comparative_history import historical_id

FIRST = "9e762fc3-2e15-4d58-832a-7b01cb9bd077"
HELD = "1d8b9a77-c1e5-4b55-9d77-202611050077"
RECONCILED = "1e78cdda-fd79-4dd8-8ff6-202611050078"


def request(identity):
    file = ROOT / "editorial" / "inbox" / (identity + ".json")
    return json.loads(file.read_text(encoding="utf-8"))


def paragraphs(markdown):
    return [item.strip() for item in re.split(r"\n{2,}", markdown)
            if item.strip()]


class MC078PreservationTests(unittest.TestCase):
    def test_original_held_by_exact_sha256(self):
        holds = json.loads((ROOT / "editorial/holds.json").read_text(encoding="utf-8"))
        assert holds["version"] == 1
        hold = holds["requests"][HELD]
        old_bytes = (ROOT / "editorial/inbox" / (HELD + ".json")).read_bytes()
        self.assertEqual(hashlib.sha256(old_bytes).hexdigest(), hold["request_sha256"])
        self.assertEqual(
            hold["request_sha256"],
            "b677888768c94847d77840756f8c222384814adc26c78a3d2434e1dde90aa2a6")
        self.assertNotIn(FIRST, holds["requests"])
        self.assertNotIn(RECONCILED, holds["requests"])

    def test_distinct_historical_identities_and_atomic_numbering(self):
        first = request(FIRST)
        original = request(HELD)
        revised = request(RECONCILED)
        for study in (first, original, revised):
            self.assertEqual(set(study), {"version", "collection", "slug", "markdown"})
            self.assertEqual(study["version"], 1)
            self.assertEqual(study["collection"], "comparatif")
            self.assertIn("{{numero}}", study["markdown"])
            self.assertIn("{{volume}}", study["markdown"])
        self.assertEqual(historical_id(first["markdown"]), "MC-077")
        self.assertEqual(historical_id(original["markdown"]), "MC-077")
        self.assertEqual(historical_id(revised["markdown"]), "MC-078")
        self.assertNotEqual(first["slug"], revised["slug"])
        self.assertNotEqual(original["slug"], revised["slug"])

    def test_all_eighty_eight_sections_and_non_editorial_prose_survive(self):
        before = request(HELD)["markdown"]
        after = request(RECONCILED)["markdown"]
        numbered = lambda text: re.findall(r"^###\s+\d+\.\s+.+$", text, flags=re.M)
        self.assertEqual(len(numbered(before)), 88)
        self.assertEqual(numbered(before), numbered(after))
        self.assertIn("Bibliographie", after)
        self.assertIn("### 88. Synthèse épistémique finale", after)

        # Seules quatre unités du manuscrit historique ont été modifiées :
        # le titre, la cote dans la notice, la continuité réconciliée et le
        # cartel archéologique corrigé. Toutes les autres restent identiques.
        editorial_prefixes = (
            "## MC-077 — Entraver les immortels",
            "**Monographie universitaire originale — 5 novembre 2026.",
            "La branche principale de",
            "**Type :** photographie d’un artefact conservé",
        )
        original_parts = paragraphs(before)
        stable = Counter(part for part in original_parts
                         if not part.startswith(editorial_prefixes))
        updated = Counter(paragraphs(after))
        self.assertGreaterEqual(sum(stable.values()), 200)
        self.assertFalse(stable - updated, "Un paragraphe non éditorial a disparu")
        self.assertGreater(len(after), 62000)

    def test_a_single_pending_mc078_identity(self):
        files = (ROOT / "editorial/inbox").glob("*.json")
        claimants = []
        for path in files:
            # Les autres collections ne partagent pas la série MC.
            if path.name == "20261105-mc-069-souffle-vent-vie-philologie.json":
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("collection") == "comparatif" and (
                    historical_id(data["markdown"]) == "MC-078"):
                claimants.append(path.stem)
        self.assertEqual(claimants, [RECONCILED])


if __name__ == "__main__":
    unittest.main()
