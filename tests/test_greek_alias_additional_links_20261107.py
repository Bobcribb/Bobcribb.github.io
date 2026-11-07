"""Regression: legacy Greek portal links may include valid secondary links.

The primary inventory remains mandatory. The general verification pass
continues to check each primary or supplementary link for a real target.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_greek_corpus import verify_canonical_links


class GreekPortalAliasLinksTests(unittest.TestCase):

    def test_legacy_portal_accepts_supplementary_navigation(self):
        canonical = {
            '/chapitres/encyclopedie/chapitre-433-athena-lindia/',
            '/mythologie-grecque/dossiers/divinites/',
        }
        alias = canonical | {
            '/reconstitutions-photorealistes.html',
            '/parcours/',
        }
        verify_canonical_links(canonical, alias, 'mythologie-grecque.html')

    def test_legacy_portal_must_not_omit_primary_chapters(self):
        canonical = {
            '/chapitres/encyclopedie/chapitre-433-athena-lindia/',
            '/mythologie-grecque/dossiers/divinites/',
        }
        alias = {'/mythologie-grecque/dossiers/divinites/', '/parcours/'}
        with self.assertRaisesRegex(AssertionError, 'chapitre-433-athena-lindia'):
            verify_canonical_links(canonical, alias, 'grande-encyclopedie.html')

    def test_identical_inventory_is_valid(self):
        canonical = {'/livre-hesiode/', '/mythologie-grecque/dossiers/cosmogonies/'}
        verify_canonical_links(canonical, set(canonical), 'mythologie-grecque/index.html')


if __name__ == '__main__':
    unittest.main()
