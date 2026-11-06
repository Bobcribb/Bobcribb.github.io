"""Accès direct aux textes intégraux historiques : intégrité et idempotence."""
import sys
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import add_home_integral_archive_shelf


class TestHomeIntegralArchiveShelf(unittest.TestCase):
    SOURCES = (
        'corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html',
        'corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html',
    )
    IMAGES = (
        'media/2026/10/mythos-aphrodite-cygne-kylix-british-museum.jpg',
        'media/2026/10/mythos-ounas-chambre-funeraire-vincent-brown.jpg',
    )

    def test_originals_retained_and_cards_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            originals = {}
            for idx, filename in enumerate(self.SOURCES):
                path = root / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                originals[filename] = ('<article><h1>Édition intégrale</h1>'
                                       '<p>Sources antiques ; bibliographie, tome %d.</p>'
                                       '<a href="/">Retour accueil</a></article>' % idx).encode('utf-8')
                path.write_bytes(originals[filename])
            for filename in self.IMAGES:
                path = root / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'original media')
            doc = BeautifulSoup('<html><body><section id="corpus-status">'
                                '<h2>Une bibliothèque documentée</h2>'
                                '<p>Corpus inchangé.</p></section></body></html>', 'html.parser')
            self.assertEqual(add_home_integral_archive_shelf(doc, root), 2)
            self.assertEqual(add_home_integral_archive_shelf(doc, root), 2)
            self.assertEqual(len(doc.select('[data-mythos-integral-archives]')), 1)
            cards = doc.select('#corpus-status .mythos-home-archive-link')
            self.assertEqual(len(cards), 2)
            self.assertEqual(
                {c['href'].lstrip('/') for c in cards},
                set(self.SOURCES))
            self.assertEqual(len(doc.select('.mythos-home-archive-credit')), 2)
            self.assertTrue(all(c.select_one('img[src^="/media/"]') for c in cards))
            self.assertEqual(len(doc.select('.mythos-home-archive-link a')), 0)
            self.assertIn('Corpus inchangé.', doc.get_text())
            for filename, before in originals.items():
                self.assertEqual((root / filename).read_bytes(), before)

    def test_missing_readers_do_not_generate_false_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = BeautifulSoup('<section id="corpus-status"><h2>État du fonds</h2></section>', 'html.parser')
            self.assertEqual(add_home_integral_archive_shelf(doc, root), 0)
            self.assertIsNone(doc.select_one('.mythos-home-archive-shelf'))


if __name__ == '__main__':
    unittest.main()
