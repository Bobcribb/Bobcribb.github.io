"""Navigation du corpus fragmentaire : intégrité, deux lectures, aucun doublon."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from theatre_fragment_index import install, verified_editions


class TheatreFragmentIndexTests(unittest.TestCase):
    def fixture(self, temporary):
        root = Path(temporary) / 'sources'
        output = Path(temporary) / 'site'
        source_dir = root / 'corpus/theatre-grec/comedies'
        reader_dir = output / 'corpus/theatre-grec/comedies'
        reader_dir.mkdir(parents=True)
        source_dir.mkdir(parents=True)
        (output / 'theatre').mkdir()
        page = output / 'theatre/index.html'
        page.write_text(
            '<!doctype html><html lang="fr"><head><title>Théâtre</title></head>'
            '<body><main><article class="content">'
            '<section class="portal-section"><h2>Choisir sa lecture</h2>'
            '<div class="portal-grid"><a class="portal-card" href="#pieces-perdues">'
            'Pièces perdues</a></div></section>'
            '<section class="portal-section" id="pieces-perdues">'
            '<h2>Pièces perdues</h2></section>'
            '<p id="historique">Bibliographie et texte originaux.</p>'
            '</article></main></body></html>', encoding='utf-8')
        source = source_dir / 'polyidos-source.md'
        source.write_text(
            '# MYTHOS — Comédies grecques — Volume XXV\n'
            '## Aristophane, *Polyidos* — voir l’invisible\n'
            '## Bibliographie critique\n'
            + ('Paragraphe philologique documenté et conservé. ' * 250),
            encoding='utf-8')
        critical = reader_dir / 'polyidos-etude.html'
        critical.write_text(
            '<html><body><main><h1>Polyidos</h1><h2>Bibliographie</h2><p>'
            + ('Étude critique intégrale. ' * 550)
            + '</p></main></body></html>', encoding='utf-8')
        modern = reader_dir / 'polyidos-scenes-modernes.html'
        modern.write_text(
            '<html><body><main><h1>Scènes modernes : créations contemporaines</h1>'
            + ('<p>Interprétation moderne, non attribuable à Aristophane.</p>' * 105)
            + '</main></body></html>', encoding='utf-8')
        return root, output, page, source, critical, modern

    def test_nine_parts_are_not_duplicated_and_originals_are_unchanged(self):
        with TemporaryDirectory() as temporary:
            root, output, page, source, critical, modern = self.fixture(temporary)
            originals = [f.read_bytes() for f in (source, critical, modern)]
            self.assertEqual(install(root, output, slugs=('polyidos',)), 1)
            first = page.read_bytes()
            self.assertEqual(install(root, output, slugs=('polyidos',)), 1)
            self.assertEqual(page.read_bytes(), first)
            doc = BeautifulSoup(first, 'html.parser')
            self.assertEqual(len(doc.select('#theatre-comedies-editions')), 1)
            self.assertEqual(len(doc.select('#theatre-comedies-editions .mythos-theatre-edition')), 1)
            self.assertEqual(len(doc.select('a[href="#theatre-comedies-editions"]')), 1)
            self.assertEqual(doc.select_one('.mythos-theatre-edition-cote').get_text(),
                             'Volume historique XXV')
            self.assertIn('Polyidos', doc.select_one('.mythos-theatre-edition h3').get_text())
            self.assertEqual(
                {a['href'] for a in doc.select('#theatre-comedies-editions article nav a')},
                {'/corpus/theatre-grec/comedies/polyidos-etude.html',
                 '/corpus/theatre-grec/comedies/polyidos-scenes-modernes.html'})
            self.assertLess(
                str(doc).index('id="theatre-comedies-editions"'),
                str(doc).index('id="pieces-perdues"'))
            self.assertEqual(doc.select_one('#historique').get_text(),
                             'Bibliographie et texte originaux.')
            self.assertEqual([f.read_bytes() for f in (source, critical, modern)], originals)

    def test_missing_reader_stops_publication(self):
        with TemporaryDirectory() as temporary:
            root, output, *_rest = self.fixture(temporary)
            (output / 'corpus/theatre-grec/comedies/polyidos-etude.html').unlink()
            with self.assertRaisesRegex(RuntimeError, 'incomplète'):
                verified_editions(root, output, slugs=('polyidos',))

    def test_short_source_stops_publication(self):
        with TemporaryDirectory() as temporary:
            root, output, _, source, *_rest = self.fixture(temporary)
            source.write_text('# Volume XXV\n## Polyidos\nBibliographie', encoding='utf-8')
            with self.assertRaisesRegex(RuntimeError, 'insuffisamment'):
                install(root, output, slugs=('polyidos',))


if __name__ == '__main__':
    unittest.main()
