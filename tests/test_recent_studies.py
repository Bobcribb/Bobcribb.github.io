"""Tests du panneau de lecteurs universitaires : reçus, intégralité et idempotence."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from recent_studies import install, latest_verified, roman


class RecentStudyTests(unittest.TestCase):
    def make_fixture(self, root):
        root = Path(root)
        output = root / 'output'
        (root / 'editorial').mkdir()
        (output / 'media/2026/10').mkdir(parents=True)
        (output / 'media/2026/10/epidaure-theatre-antique-zde.jpg').write_bytes(b'photo')
        (output / 'index.html').write_text(
            '<html lang="fr"><head><title>MYTHOS</title></head><body>'
            '<nav class="mythos-home-toc"><ul><li><a href="#home-oeuvres">Œuvres</a></li></ul></nav>'
            '<main><article class="content">'
            '<section id="home-parcours"><h2>Parcours</h2></section>'
            '<section id="home-oeuvres"><h2>Œuvres</h2></section>'
            '<p id="original">Bibliographie historique intacte.</p></article></main>'
            '</body></html>', encoding='utf-8')
        self.write_study(root, output, 'tragedies', 230, 'volume-ccxxx-triptoleme',
                         'Sophocle, *Triptolème*')
        registry = {'version': 1, 'collections': {
            'tragedies': {'allocations': {'uuid-valide': {
                'number': 230, 'path': 'chapitres/tragedies/volume-ccxxx-triptoleme.md'}}},
            'comedies': {'allocations': {'uuid-manquant': {
                'number': 999, 'path': 'chapitres/comedies/volume-999-inexistant.md'}}},
        }}
        (root / 'editorial/numbering.json').write_text(
            json.dumps(registry), encoding='utf-8')
        return root, output

    def write_study(self, root, output, collection, number, slug, title):
        path = root / 'chapitres' / collection / (slug + '.md')
        path.parent.mkdir(parents=True, exist_ok=True)
        content = '# Étude universitaire\n## ' + title + '\n' + ('Texte intégral et sources. ' * 140)
        path.write_text(content, encoding='utf-8')
        reader = output / 'chapitres' / collection / slug / 'index.html'
        reader.parent.mkdir(parents=True, exist_ok=True)
        reader.write_text('<html><body><article>Texte intégral avec bibliographie</article></body></html>',
                          encoding='utf-8')
        return path

    def test_receipt_and_full_text_are_required(self):
        with TemporaryDirectory() as temp:
            root, output = self.make_fixture(temp)
            records = latest_verified(root, output)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['cote'], 'Volume CCXXX (230)')
            self.assertEqual(records[0]['url'], '/chapitres/tragedies/volume-ccxxx-triptoleme/')
            # Un brouillon complet dans inbox, sans attribution et sans lecteur,
            # ne doit pas être exposé comme une nouvelle publication.
            (root / 'editorial/inbox').mkdir()
            (root / 'editorial/inbox/unassigned.json').write_text(
                json.dumps({'markdown': '# Inédit\n' + 'x' * 5000}), encoding='utf-8')
            self.assertEqual(len(latest_verified(root, output)), 1)

    def test_illustrated_cards_toc_repeated_build_and_no_overwriting(self):
        with TemporaryDirectory() as temp:
            root, output = self.make_fixture(temp)
            source = root / 'chapitres/tragedies/volume-ccxxx-triptoleme.md'
            before = source.read_bytes()
            original_reader = (output / 'chapitres/tragedies/volume-ccxxx-triptoleme/index.html').read_bytes()
            self.assertEqual(install(root, output), 1)
            self.assertEqual(install(root, output), 1)
            doc = BeautifulSoup((output / 'index.html').read_text(encoding='utf-8'), 'html.parser')
            self.assertEqual(len(doc.select('#home-etudes-recentes .portal-card')), 1)
            self.assertEqual(len(doc.select('a[href="#home-etudes-recentes"]')), 1)
            self.assertEqual(doc.select_one('#home-etudes-recentes img')['src'],
                             '/media/2026/10/epidaure-theatre-antique-zde.jpg')
            self.assertIn('Triptolème', doc.select_one('#home-etudes-recentes strong').get_text())
            self.assertIsNotNone(doc.select_one('#original'))
            self.assertEqual(before, source.read_bytes())
            self.assertEqual(original_reader, (output / 'chapitres/tragedies/volume-ccxxx-triptoleme/index.html').read_bytes())

    def test_incomplete_study_or_missing_reader_not_promoted(self):
        with TemporaryDirectory() as temp:
            root, output = self.make_fixture(temp)
            source = root / 'chapitres/tragedies/volume-ccxxx-triptoleme.md'
            source.write_text('# Notice sommaire\n', encoding='utf-8')
            self.assertEqual(latest_verified(root, output), [])
            self.assertEqual(install(root, output), 0)
            self.assertFalse('home-etudes-recentes' in (output / 'index.html').read_text(encoding='utf-8'))
            self.assertEqual(roman(86), 'LXXXVI')


if __name__ == '__main__':
    unittest.main()
