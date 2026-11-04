"""MYTHOS: never reactivate historical 2.5D/vector decorations in public readers."""
from pathlib import Path
import sys
import tempfile
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import apply


class NoLegacyVectorDecorationsTests(unittest.TestCase):
    def test_active_styles_and_generators_use_museum_webp(self):
        sources = (
            'scripts/build_greek_corpus.py',
            'scripts/build_navigation.py',
            'assets/mythos-articles.css',
            'assets/mythos-volume-lecture.css',
            'origines-du-sacre.html',
        )
        banned = ('/assets/mythos-hero.svg', '/assets/mythos-archaeology-tiles.svg')
        for name in sources:
            source = (ROOT / name).read_text(encoding='utf-8')
            for asset in banned:
                self.assertNotIn(asset, source, name)
            self.assertIn('/assets/mythos-museum-banner.webp', source, name)
        self.assertGreater((ROOT / 'assets/mythos-museum-banner.webp').stat().st_size, 10000)
        # Historical assets remain in Git history; no archival source deletion.
        self.assertTrue((ROOT / 'assets/mythos-hero.svg').exists())
        self.assertTrue((ROOT / 'assets/mythos-archaeology-tiles.svg').exists())

    def test_render_fixes_only_images_and_styles_not_original_archive_links(self):
        markup = """<html><head><title>Volume universitaire</title>
        <style>.old{background-image:url('/assets/mythos-hero.svg')}</style>
        </head><body><main><h1>Volume universitaire</h1>
        <p>Texte scientifique, sources et bibliographie intégralement conservés.</p>
        <img src="/assets/mythos-hero.svg" alt="Motif éditorial historique">
        <div class="old" style="background:url('/assets/mythos-archaeology-tiles.svg') center/cover">
        <p>Deuxième paragraphe inchangé.</p></div>
        <a href="/assets/mythos-hero.svg">Fichier SVG historique conservé dans les archives</a>
        </main></body></html>"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / 'index.html'
            page.write_text(markup, encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                self.assertEqual(doc.select_one('main img')['src'],
                                 '/assets/mythos-museum-banner.webp')
                self.assertIn('/assets/mythos-museum-banner.webp',
                              doc.select_one('main .old')['style'])
                self.assertIn('/assets/mythos-museum-banner.webp',
                              doc.select_one('style').get_text())
                self.assertNotIn('/assets/mythos-hero.svg',
                                 doc.select_one('style').get_text())
                self.assertEqual(doc.select_one('main a')['href'], '/assets/mythos-hero.svg')
                self.assertIn('Texte scientifique, sources et bibliographie intégralement conservés.',
                              doc.get_text(' ', strip=True))
                self.assertIn('Deuxième paragraphe inchangé.', doc.get_text(' ', strip=True))
                self.assertEqual(len(doc.select('h1')), 1)


if __name__ == '__main__':
    unittest.main()
