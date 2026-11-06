"""Vérifie les cotes publiques MC-070/071 après attribution atomique, sans réécriture scientifique."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "editorial" / "numbering.json"
CASES = (
    ("3d64880f-6844-4d2a-b94e-b7ea3a2a0460", "MC-070", 248, "CCXLVIII"),
    ("904ece0d-5591-4e6b-bfea-e39e7143c4c1", "MC-071", 251, "CCLI"),
)


class ComparativeReceiptNoticeTests(unittest.TestCase):
    def test_original_inbox_and_published_status_remain_consistent(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        allocations = registry["collections"]["comparatif"]["allocations"]
        for uid, mc, number, roman in CASES:
            with self.subTest(mc=mc):
                receipt = allocations[uid]
                self.assertEqual(receipt["number"], number)
                original = ROOT / "editorial" / "inbox" / (uid + ".json")
                self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),
                                 receipt["request_sha256"])
                source_path = ROOT / receipt["path"]
                article = source_path.read_text(encoding="utf-8")
                introduction = article.split("\n###", 1)[0]
                self.assertIn(f"Volume {roman} ({number})", introduction)
                self.assertIn(f"Identifiant historique : {mc}", introduction)
                self.assertIn(
                    f"Le circuit transactionnel a attribué le volume {roman} ({number})",
                    introduction,
                )
                self.assertNotIn("emplacements techniques non attribués", introduction)
                self.assertNotIn("conserve les variables", introduction)
                self.assertIn("bibliograph", article.casefold())


if __name__ == "__main__":
    unittest.main()
