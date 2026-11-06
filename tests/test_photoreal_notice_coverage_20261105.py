"""Coverage of the gallery's standalone notices and their different historical schemas.

Existing notices were authored at different stages of MYTHOS, sometimes with
src rather than image, and with different source metadata. Do not rewrite
historical notices merely to satisfy a new JSON schema.
"""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
NOTICE_DIR = ROOT / 'assets/reconstitutions-3d/notices'

# These 15 notices were missing entirely before this non-destructive audit fix.
AUDIT_NOTICES = {
    'delphes-apollon-panorama', 'athenes-acropole',
    'delphes-sanctuaire-vue-ensemble', 'nemee-temple-zeus-vue',
    'corinthe-temple-apollon-vue', 'messene-asklepieion-vue',
    'sounion-poseidon-vue', 'brauron-artemis-vue', 'dodone-theatre-vue',
    'bassae-apollon-exterieur-vue', 'nemee-stade-vue', 'corinthe-pirene-vue',
    'messene-stade-vue', 'sounion-athena-vue', 'brauron-stoa-vue',
}


class PhotorealNoticeCoverageTests(unittest.TestCase):
    def test_every_gallery_entry_has_a_notice_and_original_image(self):
        catalogue = json.loads(MANIFEST.read_text(encoding='utf-8'))
        entries = catalogue['entries']
        self.assertEqual(catalogue['count'], len(entries))
        self.assertEqual(len({entry['slug'] for entry in entries}), len(entries))
        slugs = {entry['slug'] for entry in entries}
        self.assertTrue(AUDIT_NOTICES <= slugs)
        for entry in entries:
            with self.subTest(slug=entry['slug']):
                file = NOTICE_DIR / (entry['slug'] + '.json')
                self.assertTrue(file.is_file(), 'Notice manquante : ' + str(file))
                notice = json.loads(file.read_text(encoding='utf-8'))
                self.assertIsInstance(notice, dict)
                # A notice filename is also a stable locator, even when its
                # historical JSON did not yet contain a 'slug' member.
                if 'slug' in notice:
                    self.assertEqual(notice['slug'], entry['slug'])
                if 'id' in notice:
                    self.assertEqual(notice['id'], entry['id'])
                if 'image' in notice:
                    self.assertEqual(notice['image'], entry['src'])
                if 'src' in notice:
                    self.assertEqual(notice['src'], entry['src'])
                self.assertTrue((ROOT / entry['src'].lstrip('/')).is_file())
                # The central catalogue is the shared source of complete
                # scholarly metadata for legacy and newer notices alike.
                for field in ('title', 'period', 'caption', 'commentary',
                              'certainty', 'source_url', 'sha256'):
                    self.assertTrue(entry.get(field), field + ': ' + entry['slug'])
                # Newly created notices are consistently complete, but do
                # not impose that schema retroactively on archival documents.
                if entry['slug'] in AUDIT_NOTICES:
                    self.assertEqual(notice['slug'], entry['slug'])
                    self.assertEqual(notice['id'], entry['id'])
                    self.assertEqual(notice['image'], entry['src'])
                    for field in ('period', 'caption', 'commentary',
                                  'certainty', 'sources', 'rights_and_method'):
                        self.assertTrue(notice.get(field), field)


if __name__ == '__main__':
    unittest.main()
