"""Garde de conservation exacte : corrections purement éditoriales 449–453."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from editorial_queue import roman

# UUID, numéro canonique et seules lignes de notice éditoriale corrigées.
STUDIES = {
    449: ('341e66ee-4e95-4c9f-8530-ef19edbc2b88', (5, 336)),
    450: ('3c81ed0e-65f9-4b1c-89de-9e401f9d3bf0', (7, 595)),
    451: ('8a93d8bd-1700-4b86-9f2e-d70115f3cc64', (7, 513)),
    452: ('bfe72a9c-6e4b-42a1-8cb8-6f0c287e4f36', (5, 318)),
    453: ('cb680531-6c1f-489e-955e-7a4b4e60ff32', (5,)),
}


class RecentCanonicalNoticesTests(unittest.TestCase):
    def test_receipts_and_provenance_are_unmodified(self):
        register = json.loads((ROOT/'editorial/numbering.json')
                              .read_text(encoding='utf-8'))
        receipts = register['collections']['encyclopedie']['allocations']
        for number, (uid, _) in STUDIES.items():
            with self.subTest(chapter=number):
                self.assertIn(uid, receipts)
                entry = receipts[uid]
                self.assertEqual(entry['number'], number)
                request_path = ROOT/'editorial/inbox'/(uid+'.json')
                raw = request_path.read_bytes()
                self.assertEqual(sha256(raw).hexdigest(),
                                 entry['request_sha256'])
                request = json.loads(raw)
                self.assertEqual(request['collection'], 'encyclopedie')
                original = (request['markdown'].replace('{{numero}}', str(number))
                            .replace('{{volume}}', roman(number)))
                self.assertEqual(sha256(original.encode('utf-8')).hexdigest(),
                                 entry['initial_source_sha256'])
                self.assertTrue((ROOT/entry['path']).is_file())
                self.assertTrue(
                    (ROOT/Path(entry['path']).with_suffix('')/'index.html').is_file())

    def test_all_scholarly_lines_are_exactly_preserved(self):
        register = json.loads((ROOT/'editorial/numbering.json')
                              .read_text(encoding='utf-8'))
        receipts = register['collections']['encyclopedie']['allocations']
        for number, (uid, allowed_lines) in STUDIES.items():
            with self.subTest(chapter=number):
                request = json.loads((ROOT/'editorial/inbox'/(uid+'.json'))
                                     .read_text(encoding='utf-8'))
                original = (request['markdown'].replace('{{numero}}', str(number))
                            .replace('{{volume}}', roman(number)))
                actual = (ROOT/receipts[uid]['path']).read_text(encoding='utf-8')
                before, after = original.splitlines(), actual.splitlines()
                self.assertEqual(len(before), len(after),
                                 'Chapitre tronqué ou lignes ajoutées')
                changed = tuple(index+1 for index, (a, b) in
                                enumerate(zip(before, after)) if a != b)
                self.assertEqual(changed, allowed_lines,
                                 'Une ligne scientifique a été modifiée')
                for line in allowed_lines:
                    self.assertIn('GitHub Actions', after[line-1])
                    self.assertGreater(len(after[line-1]), 60)
                self.assertGreater(len(actual), 30000)
                self.assertIn('bibliograph', actual.casefold())
                self.assertIn('Chapitre '+str(number), actual)
                self.assertNotIn('{{numero}}', actual)

    def test_scope_and_numbering_do_not_change(self):
        self.assertEqual(set(STUDIES), {449, 450, 451, 452, 453})
        self.assertEqual(sum(len(lines) for _, lines in STUDIES.values()), 9)


if __name__ == '__main__':
    unittest.main()
