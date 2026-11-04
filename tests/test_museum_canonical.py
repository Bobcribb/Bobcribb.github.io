"""Canonical URL and long-form table-of-contents regression checks."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import apply


class CanonicalURLTests(unittest.TestCase):
    def test_metadata_preserves_authored_canonicals_and_text(self):
        pages = {
            'index.html': '<html><head><title>Accueil</title></head><body><main><h1>Accueil</h1><p>Introduction intégrale.</p></main></body></html>',
            'grande-encyclopedie.html': '<html><head><title>Grande encyclopédie</title></head><body><main><h1>Encyclopédie</h1><p>Archives préservées.</p></main></body></html>',
            'grande-encyclopedie/index.html': '<html><head><title>Grande encyclopédie</title></head><body><main><h1>Encyclopédie</h1><p>Archives préservées.</p></main></body></html>',
            'philosophie-iliade.html': '<html><head><title>Iliade</title></head><body><main><h1>Iliade</h1><p>Étude complète, sources et bibliographie.</p></main></body></html>',
            'archives/étude.html': '<html><head><title>Archive</title></head><body><main><h1>Archive</h1><p>Texte ancien conservé.</p></main></body></html>',
            'dossier/index.html': '<html><head><title>Dossier</title><link rel="canonical" href="https://bobmythos.fr/edition-reference/"></head><body><main><h1>Dossier</h1><p>Source primaire originale.</p></main></body></html>',
            '404.html': '<html><head><title>404</title></head><body><main><h1>Introuvable</h1></main></body></html>',
            'anciennes-pages/index.html': '<html><head><meta http-equiv="refresh" content="0;url=/"><title>Ancienne page</title></head><body><h1>Redirection</h1></body></html>',
        }
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, markup in pages.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(markup, encoding='utf-8')
            expected = {
                'index.html': 'https://bobmythos.fr/',
                'grande-encyclopedie.html': 'https://bobmythos.fr/grande-encyclopedie/',
                'grande-encyclopedie/index.html': 'https://bobmythos.fr/grande-encyclopedie/',
                'philosophie-iliade.html': 'https://bobmythos.fr/philosophie-iliade.html',
                'archives/étude.html': 'https://bobmythos.fr/archives/%C3%A9tude.html',
                'dossier/index.html': 'https://bobmythos.fr/edition-reference/',
            }
            for attempt in range(2):
                self.assertEqual(apply(root), len(pages) - 1)
                for name, href in expected.items():
                    doc = BeautifulSoup((root / name).read_text(encoding='utf-8'), 'html.parser')
                    links = doc.select('link[rel~="canonical"]')
                    self.assertEqual([link['href'] for link in links], [href], name)
                    self.assertEqual(len(doc.select('.mythos-banner')), 1, name)
                    self.assertIn(BeautifulSoup(pages[name], 'html.parser').p.get_text(),
                                  doc.get_text(' ', strip=True), name)
                for name in ('404.html', 'anciennes-pages/index.html'):
                    doc = BeautifulSoup((root / name).read_text(encoding='utf-8'), 'html.parser')
                    self.assertFalse(doc.select('link[rel~="canonical"]'), name)
            self.assertIsNone(BeautifulSoup((root/'anciennes-pages/index.html').read_text(), 'html.parser').select_one('.mythos-banner'))


    def test_photorealistic_home_card_retains_verified_image_after_two_builds(self):
        markup = ('''<html><head><title>MYTHOS</title></head><body><main>
<h1>MYTHOS</h1><p>Texte scientifique et liens conservés.</p>
<section class="portal-section" id="sanctuaires-en-images">
<a class="portal-card" href="/reconstitutions-photorealistes.html#delphes-apollon-panorama">
<img class="mythos-card-image" src="/assets/reconstitutions-3d/delphes-apollon-panorama.webp"
alt="" loading="lazy" decoding="async"><strong>Delphes</strong></a>
<a class="portal-card" href="/theatre/"><img class="mythos-card-image"
src="/assets/legacy-perspective.svg" alt=""><strong>Théâtre grec</strong></a>
</section></main></body></html>''')
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/'assets/reconstitutions-3d').mkdir(parents=True)
            (root/'assets/reconstitutions-3d/delphes-apollon-panorama.webp').write_bytes(
                b'RIFF' + b'\\x04\\x00\\x00\\x00' + b'WEBP')
            (root/'media/2026/10').mkdir(parents=True)
            (root/'media/2026/10/epidaure-theatre-antique-zde.jpg').write_bytes(b'photo')
            page = root/'index.html'
            page.write_text(markup, encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                cards = doc.select('.portal-section .portal-card')
                self.assertEqual(len(cards), 2)
                self.assertEqual([img['src'] for img in cards[0].select('img')],
                                 ['/assets/reconstitutions-3d/delphes-apollon-panorama.webp'])
                self.assertEqual([img['src'] for img in cards[1].select('img')],
                                 ['/media/2026/10/epidaure-theatre-antique-zde.jpg'])
                self.assertIn('Texte scientifique et liens conservés.', doc.get_text(' ', strip=True))
                self.assertEqual(cards[0]['href'],
                                 '/reconstitutions-photorealistes.html#delphes-apollon-panorama')


if __name__ == '__main__':
    unittest.main()
