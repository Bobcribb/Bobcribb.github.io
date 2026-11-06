"""Non-régression des cartes documentaires des mythologies du monde."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_museum_design import apply


WORLD = '/mythologies/'
CIVILISATIONS = '/civilisations/'
GALIGO = ('/bibliotheque-mythologies-du-monde/'
          'mythos-volume-19-la-galigo-bugis-sawerigading/')
COVERS = (
    'shiva-nataraja-chola-met-1987-80-1.jpg',
    'mythos-behistun-inscription-darius-mahdimanavimvi-2018.jpg',
)


def source_home():
    return ('<!doctype html><html lang="fr"><head><title>MYTHOS</title></head>'
            '<body><main><section class="portal-section" id="home-collections">'
            '<h2>Les collections</h2><div class="portal-grid">'
            '<a class="portal-card" href="/mythologie-grecque/">'
            '<strong>Encyclopédie grecque</strong>'
            '<span>Corpus grec vérifié et intact.</span></a></div></section>'
            '</main></body></html>')


class WorldCollectionsTests(unittest.TestCase):
    def test_adds_documented_cards_and_integral_reader_link_only_once(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / 'index.html'
            home.write_text(source_home(), encoding='utf-8')
            media = root / 'media/2026/10'
            media.mkdir(parents=True)
            for name in COVERS:
                (media / name).write_bytes(b'fixture image')
            reader = root / GALIGO.lstrip('/') / 'index.html'
            reader.parent.mkdir(parents=True)
            reader.write_text(
                '<!doctype html><html lang="fr"><head><title>La Galigo</title>'
                '</head><body><main><section id="etude-integrale">'
                '<h2>Manuscrit</h2><p>Texte original conservé.</p></section>'
                '<h2 id="bibliographie">Bibliographie</h2></main></body></html>',
                encoding='utf-8',
            )
            for _ in range(2):
                apply(root)
            doc = BeautifulSoup(home.read_text(encoding='utf-8'), 'html.parser')
            self.assertEqual(len(doc.select('a.portal-card[href="' + WORLD + '"]')), 1)
            self.assertEqual(
                len(doc.select('a.portal-card[href="' + CIVILISATIONS + '"]')), 1)
            self.assertEqual(len(doc.select('p[data-mythos-world-reading]')), 1)
            self.assertEqual(len(doc.select('a[href="' + GALIGO + '"]')), 1)
            for url in (WORLD, CIVILISATIONS):
                card = doc.select_one('a.portal-card[href="' + url + '"]')
                image = card.select_one('img.mythos-card-image')
                self.assertTrue(image)
                self.assertTrue(image['src'].startswith('/media/2026/10/'))
                self.assertGreater(len(image['alt']), 30)
                self.assertTrue(card.select_one('.mythos-home-cover-credit'))
            self.assertEqual(
                len(doc.select('a.portal-card[href="/mythologie-grecque/"]')), 1)
            self.assertIn('Corpus grec vérifié et intact.', doc.get_text(' '))
            preserved = BeautifulSoup(reader.read_text(encoding='utf-8'), 'html.parser')
            self.assertIn('Texte original conservé.',
                          preserved.select_one('#etude-integrale').get_text(' '))
            self.assertIsNotNone(preserved.select_one('#bibliographie'))

    def test_refuses_missing_local_illustrations_and_reader(self):
        with TemporaryDirectory() as directory:
            home = Path(directory) / 'index.html'
            home.write_text(source_home(), encoding='utf-8')
            apply(directory)
            doc = BeautifulSoup(home.read_text(encoding='utf-8'), 'html.parser')
            self.assertFalse(doc.select('[data-mythos-home-collection]'))
            self.assertFalse(doc.select('[data-mythos-world-reading]'))


if __name__ == '__main__':
    unittest.main()
