"""Cross-collection breadcrumb regression tests for long-form MYTHOS studies.

Checks idempotence and preservation of text, citations, sources and article anchors.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import apply


class MuseumBreadcrumbTests(unittest.TestCase):
    def test_approved_collection_routes_and_full_text_are_preserved(self):
        collection_routes = {
            'origines-du-sacre': '/origines-du-sacre/',
            'encyclopedie': '/mythologie-grecque/',
            'comedies': '/theatre/',
            'tragedies': '/theatre/',
            'comparatif': '/mythologie-comparee/',
            'philosophie': '/philosophie/',
            'grece': '/mythologie-grecque/',
        }
        markup = (
            '<!DOCTYPE html><html lang="fr"><head><title>Étude longue</title>'
            '<link rel="canonical" href="https://bobmythos.fr/texte-original/">'
            '</head><body><main><article>'
            '<h1>Étude et critique des sources</h1>'
            '<p id="argument">Argument universitaire intégral, sans résumé.</p>'
            '<h2 id="sources">Sources primaires</h2>'
            '<p><a href="https://example.org/edition">Édition antique</a></p>'
            '<h2 id="bibliographie">Bibliographie</h2>'
            '<p>Bibliographie intégrale, références conservées.</p>'
            '</article></main></body></html>'
        )
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for collection in collection_routes:
                target = root / 'chapitres' / collection / 'etude-test' / 'index.html'
                target.parent.mkdir(parents=True)
                target.write_text(markup, encoding='utf-8')
            landing = root / 'index.html'
            landing.write_text(markup, encoding='utf-8')
            for build in range(2):
                self.assertEqual(apply(root), len(collection_routes) + 1)
                for collection, parent in collection_routes.items():
                    target = root / 'chapitres' / collection / 'etude-test' / 'index.html'
                    doc = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                    crumb = doc.select('nav.mythos-breadcrumbs[aria-label="Fil d’Ariane"]')
                    self.assertEqual(len(crumb), 1, (collection, build))
                    self.assertEqual(
                        [a['href'] for a in crumb[0].select('a[href]')],
                        ['/', parent], (collection, build))
                    self.assertEqual(
                        crumb[0].select_one('li[aria-current="page"]').get_text(strip=True),
                        'Étude et critique des sources')
                    self.assertEqual(len(doc.select('main p#argument')), 1)
                    self.assertEqual(len(doc.select('main #sources')), 1)
                    self.assertEqual(len(doc.select('main #bibliographie')), 1)
                    self.assertEqual(len(doc.select('a[href="https://example.org/edition"]')), 1)
                    self.assertEqual(
                        doc.select_one('link[rel="canonical"]')['href'],
                        'https://bobmythos.fr/texte-original/')
                self.assertFalse(
                    BeautifulSoup(landing.read_text(encoding='utf-8'), 'html.parser')
                    .select('nav.mythos-breadcrumbs'))


if __name__ == '__main__':
    unittest.main()
