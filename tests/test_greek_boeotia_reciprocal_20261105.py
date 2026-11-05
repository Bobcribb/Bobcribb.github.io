"""Parcours béotien : réciprocité documentaire, aucune réécriture scientifique."""
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_folders import BASE, BOEOTIA_STUDIES, build, classify, verify

PENDING_HOMES = (
    ('athena-chalkioikos-sparta-acropole-gitiadas-bronze-asylie', 'Sparte'),
    ('apollon-ismenios-thebes-ismenton-melia-trepieds-daphnephorie-oracle', 'Thèbes'),
    ('apollon-amyklaios-hyakinthos-amyklaion-hyakinthies-bathykles', 'Amyclées'),
    ('trophonios-lebadee-descente-oraculaire-lethe-mnemosyne-herkyna', 'Lébadée'),
    ('helene-menelas-menelaion-therapne-epigraphie-cultes-memoire', 'Thérapné'),
)


class BoeotiaCrossReadingsTests(unittest.TestCase):
    def test_four_canonical_sources_are_full_and_distinct(self):
        self.assertEqual(len(BOEOTIA_STUDIES), 4)
        self.assertEqual(len({u for u, _, _ in BOEOTIA_STUDIES}), 4)
        for url, title, context in BOEOTIA_STUDIES:
            with self.subTest(url=url):
                source = ROOT / (url.lstrip('/').rstrip('/')+'.md')
                reader = ROOT / url.lstrip('/') / 'index.html'
                self.assertTrue(source.is_file(), source)
                self.assertTrue(reader.is_file(), reader)
                text = source.read_text(encoding='utf-8')
                self.assertGreater(len(text), 30000)
                self.assertRegex(text.lower(), r'bibliograph')
                self.assertRegex(title, r'^Chapitre (442|444|445|448) — ')
                self.assertGreater(len(context), 25)
                self.assertEqual(classify(url, title, 'Chapitre universitaire')[0],
                                 'cultes-sanctuaires')

    def test_boeotia_reciprocity_and_repeat_build_preserve_articles(self):
        groups = [('Béotie', 'grec-universitaire',
                   [(url, title) for url, title, _ in BOEOTIA_STUDIES])]
        expected = {u for u, _, _ in BOEOTIA_STUDIES}
        source_hashes = {
            u: sha256((ROOT/(u.lstrip('/').rstrip('/')+'.md')).read_bytes()).hexdigest()
            for u in expected}
        with TemporaryDirectory() as tmp:
            out = Path(tmp)
            original = {}
            for url in expected:
                file = out/url.lstrip('/')/'index.html'
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(
                    '<!doctype html><html lang="fr"><head><title>Étude</title></head>'
                    '<body><main><article class="content">'
                    '<h1>Monographie intégrale</h1>'
                    '<p>Corps universitaire préservé, variantes et citations.</p>'
                    '<h2>Sources antiques</h2><p>Strabon, Pausanias, inscriptions.</p>'
                    '<h2>Bibliographie</h2><p>Travaux critiques.</p>'
                    '</article></main></body></html>', encoding='utf-8')
                original[url] = str(BeautifulSoup(
                    file.read_text(encoding='utf-8'),'html.parser').article)
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({r['url'] for r in rows}, expected)
                verify(out, expected)
                for url in expected:
                    file = out/url.lstrip('/')/'index.html'
                    doc = BeautifulSoup(file.read_text(encoding='utf-8'),
                                        'html.parser')
                    self.assertEqual(str(doc.article), original[url])
                    panels = doc.select('aside[data-greek-cross-readings="beotie"]')
                    self.assertEqual(len(panels), 1)
                    self.assertIsNone(panels[0].find_parent('article'))
                    links = panels[0].select('ul a[href]')
                    self.assertEqual({a['href'] for a in links}, expected-{url})
                    self.assertEqual(len(links), 3)
                    self.assertEqual(len(doc.select('[data-greek-folder-nav]')), 1)
                    self.assertEqual(
                        sha256((ROOT/(url.lstrip('/').rstrip('/')+'.md')).read_bytes()).hexdigest(),
                        source_hashes[url])

    def test_future_allocations_are_classified_but_not_inventoried(self):
        # Ces slugs sont dans inbox. Ils n'apparaissent qu'après allocation
        # et création effective d'une page recensée par le générateur.
        for slug, section in PENDING_HOMES:
            with self.subTest(slug=slug):
                url='/chapitres/encyclopedie/chapitre-999-'+slug+'/'
                family, section_label=classify(url, 'Nom de Zeus hors sujet',
                                               'Chapitre universitaire')
                self.assertEqual(family, 'cultes-sanctuaires')
                self.assertTrue(section_label.startswith(section))
        with TemporaryDirectory() as tmp:
            out=Path(tmp)
            only=BOEOTIA_STUDIES[:2]
            for url, _, _ in only:
                path=out/url.lstrip('/')/'index.html'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<html><head><title>Étude</title></head><body>'
                    '<main><article><p>Texte intact</p></article></main></body></html>',
                    encoding='utf-8')
            rows=build(out, [('Béotie', 'grec-universitaire',
                              [(url,title) for url,title,_ in only])], [], [])
            self.assertEqual({r['url'] for r in rows}, {url for url,_,_ in only})
            listings=''.join((out/BASE.strip('/')/folder/'index.html').read_text(
                encoding='utf-8') for folder in {'cultes-sanctuaires'})
            for slug, _ in PENDING_HOMES:
                self.assertNotIn('chapitre-999-'+slug, listings)

    def test_cross_readings_use_accessible_museum_theme(self):
        css=(ROOT/'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('[data-greek-cross-readings="beotie"]', css)
        self.assertIn('grid-template-columns:minmax(0,1fr)', css)
        self.assertIn('min-height:44px', css)


if __name__ == '__main__':
    unittest.main()
