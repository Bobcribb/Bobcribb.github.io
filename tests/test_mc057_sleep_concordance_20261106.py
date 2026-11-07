"""Non-régression : sommeil divin, retenues intactes, numérotation immuable (issue #55)."""

from hashlib import sha256
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "editorial" / "inbox"
HOLD_VALUES = {
    "b8500850-0bad-4085-8085-202611050085": (
        "1126ce5bbb6cbda8ae180895317bdb8bb303aa1e3c1b8cc738e122a5bc371e0f",
        50222,
    ),
    "b8600860-0bad-4086-8086-202611050086": (
        "3682ec0fe4728e28c6328c4743eb15222a63d8cb49b923bcb5f65e225c742045",
        51435,
    ),
}
SLEEP_UUID = "6d7fd89c-2d44-4ef5-95a7-5d574d6d0057"
FOOTPRINTS_UUID = "cd6f6086-213a-4b2a-98c7-1d62c3006086"
SLEEP_PATH = (
    "chapitres/comparatif/"
    "volume-ccxxxvii-mc-057-quand-les-dieux-dorment-"
    "sommeil-veille-cosmique-pouvoir-de-l-eveil.md"
)
FOOTPRINTS_PATH = (
    "chapitres/comparatif/"
    "volume-cclxxviii-mc-086-empreinte-des-dieux-"
    "pas-traces-lieux-presence-heracles-vishnu-buddha-isis.md"
)
NOTE_PATH = ROOT / "docs" / "CONCORDANCE_MC057_SOMMEIL_ISSUE55_20261106.md"
ANNEX_MARKER = "## Annexe critique non numérotée — Formes de sommeil"


class SleepConcordanceTests(unittest.TestCase):
    def test_both_submissions_remain_held_unchanged_and_without_receipts(self):
        holds = json.loads((ROOT / "editorial/holds.json").read_text(encoding="utf-8"))["requests"]
        allocations = json.loads((ROOT / "editorial/numbering.json").read_text(
            encoding="utf-8"))["collections"]["comparatif"]["allocations"]
        for uid, (expected_sha, expected_length) in HOLD_VALUES.items():
            with self.subTest(uid=uid):
                original_bytes = (INBOX / (uid + ".json")).read_bytes()
                manuscript = json.loads(original_bytes.decode("utf-8"))
                self.assertEqual(sha256(original_bytes).hexdigest(), expected_sha)
                self.assertEqual(holds[uid]["request_sha256"], expected_sha)
                self.assertTrue(holds[uid]["reason"])
                self.assertNotIn(uid, allocations)
                self.assertEqual(manuscript["collection"], "comparatif")
                self.assertEqual(len(manuscript["markdown"]), expected_length)
                self.assertIn("Les dieux dorment-ils ?", manuscript["markdown"])

    def test_mc057_and_mc086_existing_canonical_receipts_are_preserved(self):
        allocations = json.loads((ROOT / "editorial/numbering.json").read_text(
            encoding="utf-8"))["collections"]["comparatif"]["allocations"]
        for uid, number, path in (
            (SLEEP_UUID, 237, SLEEP_PATH),
            (FOOTPRINTS_UUID, 278, FOOTPRINTS_PATH),
        ):
            with self.subTest(uuid=uid):
                receipt = allocations[uid]
                self.assertEqual(receipt["number"], number)
                self.assertEqual(receipt["path"], path)
                self.assertEqual(
                    sha256((INBOX / (uid + ".json")).read_bytes()).hexdigest(),
                    receipt["request_sha256"],
                )
                self.assertTrue((ROOT / path).is_file())
        footprints = (ROOT / FOOTPRINTS_PATH).read_text(encoding="utf-8")
        self.assertIn("L'empreinte des dieux", footprints)
        self.assertNotIn(FOOTPRINTS_UUID, HOLD_VALUES)
        self.assertEqual(len({receipt["number"] for receipt in (
            allocations[SLEEP_UUID], allocations[FOOTPRINTS_UUID],
        )}), 2)

    def test_canonical_study_contains_one_unnumbered_annex_and_full_bibliography(self):
        source = (ROOT / SLEEP_PATH).read_text(encoding="utf-8")
        self.assertGreater(len(source), 85000)
        self.assertEqual(source.count(ANNEX_MARKER), 1)
        self.assertIn("Volume CCXXXVII (237)", source)
        self.assertIn("## XIV. Bibliographie analytique", source)
        self.assertIn("## XV. Iconographie documentée", source)
        self.assertIn("## XVI. Synthèse et programme critique", source)
        self.assertIn("**FIN DU MANUSCRIT INTÉGRAL MYTHOS — MC-057.**", source)
        self.assertIn("nidrāvaśaṃ nītaḥ", source)
        self.assertIn("prasuptaṃ ca janārdanam", source)
        self.assertIn("Met 16.140", source)
        self.assertIn("CONCORDANCE_MC057_SOMMEIL_ISSUE55_20261106.md", source)
        self.assertNotIn("## MC-086 — Les dieux dorment-ils ?", source)

    def test_documentary_concordance_links_both_held_uuids_and_real_mc086(self):
        text = NOTE_PATH.read_text(encoding="utf-8")
        self.assertGreater(len(text), 12000)
        for uuid in (*HOLD_VALUES, SLEEP_UUID, FOOTPRINTS_UUID):
            self.assertIn(uuid, text)
        self.assertIn("MC-057", text)
        self.assertIn("MC-086", text)
        self.assertIn("n'a", text)
        self.assertIn("Bibliographies", text)
        self.assertIn("Sarpédon", text)
        self.assertIn("https://github.com/Bobcribb/Bobcribb.github.io/issues/55", text)


if __name__ == "__main__":
    unittest.main()
