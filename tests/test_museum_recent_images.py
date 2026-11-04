"""Cartes récentes : une seconde passe muséale ne perd pas les documents sourcés.

Ce test ne touche ni aux manuscrits, ni aux numéros ni aux registres.
"""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import apply


class MuseumRecentImagesTests(unittest.TestCase):
    def write_home(self, root, image_url):
        home = root / 'index.html'
        home.write_text(
            '<!doctype html><html lang="fr"><head><title>MYTHOS</title></head>'
            '<body><main><article class="content"><h1>MYTHOS</h1>'
            '<section class="portal-section" id="home-etudes-recentes">'
            '<h2>Dernières études par collection</h2>'
            '<div class="portal-grid"><a class="portal-card" '
            'href="/chapitres/comparatif/volume-201-fixture/">'
            '<span class="mythos-recent-illustration">'
            '<img class="mythos-card-image" alt="Tablette antique documentée" '
            'src="' + image_url + '" loading="lazy"/>'
            '<span class="mythos-recent-caption">Photographie de collection, '
            'sans attribution au sujet précis.</span></span>'
            '<span class="portal-card-kicker">Comparatif · Volume CCI</span>'
            '<strong>Étude universitaire intégrale</strong></a></div></section>'
            '<p id="archive">Texte source intact, références et bibliographie.</p>'
            '</article></main></body></html>', encoding='utf-8')
        return home

    def test_verified_local_media_survives_three_passes(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / 'media/2026/10/tablette-sourcee.jpg'
            media.parent.mkdir(parents=True)
            media.write_bytes(b'archived-documentary-image')
            page = self.write_home(root, '/media/2026/10/tablette-sourcee.jpg')
            for _ in range(3):
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding='utf-8'),
                                   'html.parser')
                card = doc.select_one('#home-etudes-recentes a.portal-card')
                photos = card.select('img.mythos-card-image')
                self.assertEqual(len(photos), 1)
                self.assertEqual(photos[0]['src'], '/media/2026/10/tablette-sourcee.jpg')
                self.assertEqual(photos[0]['alt'], 'Tablette antique documentée')
                self.assertEqual(
                    len(card.select('.mythos-recent-caption')), 1)
                self.assertIn('sans attribution au sujet précis',
                              card.get_text(' ', strip=True))
                self.assertIn('bibliographie', doc.select_one('#archive').get_text())

    def test_unpublished_or_legacy_image_is_not_whitelisted(self):
        for source in ('/media/2026/10/non-archivee.jpg',
                       '/assets/reconstitutions-3d/ancien-dessin-2-5d.svg'):
            with self.subTest(source=source), TemporaryDirectory() as temporary:
                root = Path(temporary)
                page = self.write_home(root, source)
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding='utf-8'),
                                   'html.parser')
                self.assertFalse(doc.select('img[src="' + source + '"]'))
                self.assertEqual(
                    doc.select_one('#archive').get_text(' ', strip=True),
                    'Texte source intact, références et bibliographie.')


if __name__ == '__main__':
    unittest.main()
