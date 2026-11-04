"""Quatre œuvres en accueil : édition de l'Énéide vérifiée et images fidèles."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import PICTURES, apply

IMAGE = '/media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg'
URL = '/philosophie-eneide.html'


class HomeEneideCardsTests(unittest.TestCase):
    def test_four_cards_point_to_existing_readers_without_replacing_eneide(self):
        page = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
        section = page.select_one('#home-oeuvres')
        self.assertIsNotNone(section)
        self.assertEqual(section.select_one('h2').get_text(' ', strip=True),
                         'Quatre œuvres à approfondir')
        links = [a['href'] for a in section.select('.portal-card')]
        self.assertEqual(links, [
            '/philosophie-iliade.html', '/philosophie-odyssee.html',
            '/philosophie-theogonie.html', URL,
        ])
        for url in links:
            self.assertTrue((ROOT / url.lstrip('/')).is_file(), url)
        ena = section.select_one('a[href="' + URL + '"]')
        img = ena.select_one('img')
        self.assertEqual(img['src'], IMAGE)
        self.assertTrue((ROOT / IMAGE.lstrip('/')).is_file())
        self.assertIn('non illustration du récit', img['alt'])
        self.assertEqual(PICTURES[URL], Path(IMAGE).name)
        report = json.loads((ROOT / 'assets/philosophie/eneide-pagination.json').read_text(encoding='utf-8'))
        self.assertEqual(report['status'], 'partial')
        self.assertEqual(report['actual_analysis_pages'], 76)
        self.assertEqual(report['target_analysis_pages'], 300)
        self.assertEqual(len(report['sources_sha256']), 18)
        self.assertIn('76 pages', ena.get_text(' ', strip=True))
        self.assertIn('300 pages', section.get_text(' ', strip=True))
        self.assertEqual(len(page.select('nav.mythos-home-toc a[href="#home-oeuvres"]')), 1)

    def test_museum_rebuild_preserves_contextual_alt_and_is_idempotent(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'index.html').write_bytes((ROOT / 'index.html').read_bytes())
            picture = root / IMAGE.lstrip('/')
            picture.parent.mkdir(parents=True)
            picture.write_bytes(b'archaeological-document-fixture')
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                page = BeautifulSoup((root / 'index.html').read_text(encoding='utf-8'), 'html.parser')
                cards = page.select('#home-oeuvres a.portal-card[href="' + URL + '"]')
                self.assertEqual(len(cards), 1)
                self.assertEqual(cards[0].select_one('img')['src'], IMAGE)
                self.assertIn('non illustration du récit', cards[0].select_one('img')['alt'])
                self.assertEqual(len(page.select('nav.mythos-home-toc a[href="#home-oeuvres"]')), 1)
                self.assertEqual(page.select_one('#home-oeuvres h2').get_text(),
                                 'Quatre œuvres à approfondir')

    def test_missing_documentary_image_is_not_hidden(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'index.html').write_bytes((ROOT / 'index.html').read_bytes())
            with self.assertRaisesRegex(RuntimeError, 'Troie manquante'):
                apply(root)


if __name__ == '__main__':
    unittest.main()
