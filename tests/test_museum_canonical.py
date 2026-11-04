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


if __name__ == '__main__':
    unittest.main()
