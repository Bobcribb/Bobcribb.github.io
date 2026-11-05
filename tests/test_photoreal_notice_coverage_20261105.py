"""Coverage of photorealistic gallery notices, without changing the images.

Each of the 54 catalogued reconstructions must retain an individual scientific
notice in addition to its central catalogue entry. This test does not pretend
that institutional sources certify the conjectural pixels.
"""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
NOTICE_DIR = ROOT / 'assets/reconstitutions-3d/notices'


class PhotorealNoticeCoverageTests(unittest.TestCase):
    def test_every_gallery_entry_has_a_standalone_notice_and_original_image(self):
        catalogue = json.loads(MANIFEST.read_text(encoding='utf-8'))
        entries = catalogue['entries']
        self.assertEqual(catalogue['count'], len(entries))
        self.assertEqual(len({entry['slug'] for entry in entries}), len(entries))
        for entry in entries:
            with self.subTest(slug=entry['slug']):
                file = NOTICE_DIR / (entry['slug'] + '.json')
                self.assertTrue(file.is_file(), 'Notice manquante : ' + str(file))
                notice = json.loads(file.read_text(encoding='utf-8'))
                self.assertEqual(notice['slug'], entry['slug'])
                self.assertEqual(notice['id'], entry['id'])
                self.assertEqual(notice['image'], entry['src'])
                self.assertTrue(notice.get('period'))
                self.assertTrue(notice.get('caption'))
                self.assertTrue(notice.get('commentary'))
                self.assertTrue(notice.get('certainty'))
                self.assertTrue(notice.get('sources'))
                self.assertTrue((ROOT / entry['src'].lstrip('/')).is_file())


if __name__ == '__main__':
    unittest.main()
