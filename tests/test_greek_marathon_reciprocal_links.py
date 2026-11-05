"""Marathon: four intact, already-published studies and reciprocal dossier navigation.

No numbered manuscript, editorial receipt, bibliography or archive is edited.
"""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_folders import MARATHON_STUDIES, BASE, build, classify, verify


class MarathonCrossReadingTests(unittest.TestCase):
    def test_four_existing_complete_studies_and_receipt(self):
        self.assertEqual(len(MARATHON_STUDIES), 4)
        expected = {
            425: ('heros', 'Marathon — Échétlos, araire et mémoire civique'),
            326: ('heros', None),
            371: ('divinites', None),
            393: ('cultes-sanctuaires', None),
        }
        for url, heading, context in MARATHON_STUDIES:
            with self.subTest(heading=heading):
                path = ROOT / url.lstrip('/')
                source = path.with_suffix('.md')
                self.assertTrue(source.is_file(), 'Manuscrit introuvable : ' + str(source))
                self.assertTrue((path / 'index.html').is_file(), 'HTML absent : ' + url)
                manuscript = source.read_text(encoding='utf-8')
                number = int(source.name.split('-')[1])
                self.assertIn('Chapitre ' + str(number), manuscript[:300])
                self.assertGreater(len(manuscript), 5000)
                self.assertTrue(
                    ('bibliograph' in manuscript.lower() or 'sources et pistes de lecture' in manuscript.lower()),
                    'Sources ou bibliographie absentes : ' + url)
                self.assertTrue(context.strip())
                family, section = classify(url, 'Un titre mentionnant Zeus et Athéna par hasard',
                                           'Chapitre universitaire')
                self.assertEqual(family, expected[number][0])
                if expected[number][1]:
                    self.assertEqual(section, expected[number][1])
                self.assertNotEqual(section, 'Nouvelles études à classer')
        registry = json.loads((ROOT / 'editorial/numbering.json').read_text(encoding='utf-8'))
        records = list(registry['collections']['encyclopedie']['allocations'].values())
        url425 = MARATHON_STUDIES[0][0]
        self.assertEqual(sum(rec['path'].replace('.md', '/') == url425.lstrip('/')
                             and rec['number'] == 425 for rec in records), 1)

    def test_rebuild_preserves_manuscripts_and_makes_bidirectional_usable_links(self):
        with TemporaryDirectory() as temp:
            out = Path(temp)
            links = []
            originals = {}
            for url, title, _ in MARATHON_STUDIES:
                path = out / url.lstrip('/') / 'index.html'
                path.parent.mkdir(parents=True, exist_ok=True)
                page = ('<!doctype html><html lang="fr"><head><title>Étude</title></head>'
                        '<body><main><article class="content"><h1>' + title + '</h1>'
                        '<h2 id="notes">Sources, bibliographie et notes</h2>'
                        '<p>Texte original intégral à préserver · Ἐχετλαῖος.</p>'
                        '</article></main></body></html>')
                path.write_text(page, encoding='utf-8')
                originals[url] = str(BeautifulSoup(page, 'html.parser').article)
                links.append((url, title))
            group = [('Études universitaires', 'grec-universitaire', links)]
            for _ in range(2):
                rows = build(out, group, [], [])
                verify(out, {url for url, _, _ in MARATHON_STUDIES})
                self.assertEqual(len(rows), 4)
                for url, title, _ in MARATHON_STUDIES:
                    doc = BeautifulSoup((out / url.lstrip('/') / 'index.html').read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), originals[url])
                    self.assertEqual(len(doc.select('[data-greek-folder-nav]')), 1)
                    panels = doc.select('aside[data-greek-cross-readings="marathon"]')
                    self.assertEqual(len(panels), 1)
                    cited = {a['href'] for a in panels[0].select('a[href]')}
                    self.assertEqual(cited, {u for u, _, _ in MARATHON_STUDIES if u != url})
                    self.assertEqual(len(panels[0].select('a[href]')), 3)
                    self.assertTrue(all(a.get_text(' ', strip=True) for a in panels[0].select('a')))
                echetlos = BeautifulSoup(
                    (out / MARATHON_STUDIES[0][0].lstrip('/') / 'index.html').read_text(encoding='utf-8'), 'html.parser')
                chapter_425_folder = echetlos.select_one('nav[data-greek-folder-nav] .greek-folder-return-topic')
                self.assertTrue(chapter_425_folder['href'].startswith(BASE + 'heros/#theme-'))
                heroes = BeautifulSoup((out / BASE.lstrip('/') / 'heros/index.html').read_text(encoding='utf-8'), 'html.parser')
                self.assertIsNotNone(heroes.select_one('a[data-greek-entry][href="' + MARATHON_STUDIES[0][0] + '"]'))

    def test_mobile_style_has_legible_cards_and_keyboard_focus(self):
        css = (ROOT / 'assets/mythos-discovery.css').read_text(encoding='utf-8')
        self.assertIn('.greek-cross-readings', css)
        self.assertIn('.greek-cross-readings li a:focus-visible', css)
        self.assertIn('min-height:44px', css)
        self.assertIn('@media(max-width:700px){.mythos-design .greek-cross-readings', css)
        self.assertIn('grid-template-columns:1fr', css)


if __name__ == '__main__':
    unittest.main()
