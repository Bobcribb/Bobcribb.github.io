"""Tests du sommaire MYTHOS : ancres, intégrité, idempotence."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_museum_design import apply


class HomeTocTests(unittest.TestCase):
    def test_home_toc_links_and_preserves_sections(self):
        titles = ['Les collections', 'Commencer une lecture',
                  'Trois œuvres à approfondir', 'Sanctuaires grecs en images',
                  'Explorer les mondes anciens', 'Une bibliothèque documentée']
        sections = ''.join(
            '<section class="portal-section"><h2>' + t +
            '</h2><p id="source-' + str(i) + '">Source intacte ' +
            str(i) + '</p></section>' for i, t in enumerate(titles))
        markup = ('<html lang="fr"><head><title>MYTHOS</title></head>'
                  '<body><main><h1>MYTHOS</h1>' + sections + '</main></body></html>')
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'index.html'
            path.write_text(markup, encoding='utf-8')
            for _ in range(2):
                apply(temp)
                doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
                nav = doc.select('nav.mythos-home-toc')
                self.assertEqual(len(nav), 1)
                anchors = nav[0].select('a[href^="#"]')
                self.assertEqual([a.get_text(strip=True) for a in anchors], titles)
                self.assertEqual(len(set(a['href'] for a in anchors)), 6)
                for anchor in anchors:
                    self.assertEqual(len(doc.select('section' + anchor['href'])), 1)
                self.assertEqual(len(doc.select('main p[id^="source-"]')), 6)
                self.assertEqual(len(doc.select('section.mythos-directory')), 1)

    def test_non_home_article_does_not_receive_toc(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'chapitres' / 'philosophie' / 'test' / 'index.html'
            path.parent.mkdir(parents=True)
            path.write_text(
                '<html><head><title>Étude</title></head><body>'
                '<main><h1>Étude</h1><p>Texte intégral.</p></main>'
                '</body></html>', encoding='utf-8')
            apply(temp)
            doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            self.assertFalse(doc.select('nav.mythos-home-toc'))
            self.assertIn('Texte intégral.', doc.get_text(' '))


if __name__ == '__main__':
    unittest.main()
