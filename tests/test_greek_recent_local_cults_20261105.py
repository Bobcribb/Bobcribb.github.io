"""Dix monographies publiées : classement cultuel et conservation intégrale."""
from hashlib import sha256
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_folders import BASE, build, classify, verify

# Numéros existants : ni fichiers créés, ni nouvelles cotes attribuées.
CASES = (
    ('439-apollon-karneios-karneia-sparte-thera-cyrene-messene-rites-musique',
     'cultes-sanctuaires', 'Sparte, Théra et Cyrène'),
    ('440-zeus-diktaios-palaikastro-hymne-megistos-kouros-ganos-sanctuaire',
     'cultes-sanctuaires', 'Palaikastro (Crète)'),
    ('441-euthymos-locres-temesa-heros-polites-alybas-lycas-heroisation',
     'heros', 'Locres et Témésa'),
    ('442-poseidon-onchestios-onchestos-chars-sans-conducteur-federation-beotie',
     'cultes-sanctuaires', 'Onchestos (Béotie)'),
    ('443-artemis-orthia-sparte-lygos-masques-fouet-sanctuaire',
     'cultes-sanctuaires', 'Sparte — Artémis Orthia'),
    ('444-eros-thespies-pierre-aniconique-praxiteles-erotideia-phryne',
     'cultes-sanctuaires', 'Thespies — Éros'),
    ('445-hermes-kriophoros-tanagra-belier-epidemie-rites-calamis',
     'cultes-sanctuaires', 'Tanagra — Hermès Kriophoros'),
    ('446-artemis-tauropolos-halai-araphenides-oreste-sang-symbolique-tauropolia',
     'cultes-sanctuaires', 'Halai Araphénides'),
    ('447-heracles-thasos-heros-dieu-melqart-rites-sacrificiels-herakleion',
     'cultes-sanctuaires', 'Thasos — Héraclès'),
    ('448-amphiaraos-amphiareion-oropos-devin-incubation-guerison-epigraphie',
     'cultes-sanctuaires', 'Oropos — Amphiaréion'),
)


def study_url(slug):
    n, remainder = slug.split('-', 1)
    return '/chapitres/encyclopedie/chapitre-' + n + '-' + remainder + '/'


class GreekRecentLocalCultsTests(unittest.TestCase):
    def test_authentic_sources_are_complete_and_have_single_primary_home(self):
        for slug, family, section_start in CASES:
            with self.subTest(slug=slug):
                url = study_url(slug)
                source = ROOT / (url.strip('/') + '.md')
                page = ROOT / url.strip('/') / 'index.html'
                self.assertTrue(source.is_file(), source)
                self.assertTrue(page.is_file(), page)
                body = source.read_text(encoding='utf-8')
                self.assertGreater(len(body), 18000, source)
                self.assertIn('bibliograph', body.casefold(), source)
                actual = classify(
                    url, 'Titre parasite mentionnant Athéna et Zeus',
                    'Chapitre universitaire')
                self.assertEqual(actual[0], family)
                self.assertTrue(
                    classify(url, 'Titre parasite', 'Chapitre universitaire')[1]
                    .startswith(section_start))

    def test_navigation_reciproque_is_idempotent_and_manuscripts_untouched(self):
        chosen = [CASES[i] for i in (1, 2, 5, 9)]
        groups = [('Monographies locales', 'grec-universitaire',
                   [(study_url(slug), 'Chapitre ' + slug.split('-', 1)[0])
                    for slug, _, _ in chosen])]
        urls = {study_url(slug) for slug, _, _ in chosen}
        source_hashes = {
            slug: sha256((ROOT / (study_url(slug).strip('/')+'.md')).read_bytes()).hexdigest()
            for slug, _, _ in chosen
        }
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            snapshots = {}
            for slug, _, _ in chosen:
                url = study_url(slug)
                page = out / url.strip('/') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<html lang="fr"><head><title>Étude intégrale</title></head>'
                    '<body><main><article class="content">'
                    '<h1>Chapitre universitaire</h1><p>Texte scientifique complet.</p>'
                    '<h2 id="sources">Sources antiques</h2>'
                    '<p>Références philologiques conservées.</p>'
                    '<h2 id="bibliographie">Bibliographie</h2>'
                    '<p>Éditions et travaux critiques.</p></article></main></body></html>',
                    encoding='utf-8')
                snapshots[url] = str(BeautifulSoup(
                    page.read_text(encoding='utf-8'), 'html.parser').article)
            for _ in range(2):
                records = build(out, groups, [], [])
                self.assertEqual({r['url'] for r in records}, urls)
                verify(out, urls)
                for slug, family, _ in chosen:
                    url = study_url(slug)
                    page = out / url.strip('/') / 'index.html'
                    doc = BeautifulSoup(page.read_text(encoding='utf-8'),
                                        'html.parser')
                    self.assertEqual(str(doc.article), snapshots[url])
                    nav = doc.select('nav[data-greek-folder-nav="true"]')
                    self.assertEqual(len(nav), 1)
                    self.assertTrue(nav[0].find('a', href=BASE+family+'/'))
                    self.assertEqual(
                        sha256((ROOT / (url.strip('/')+'.md')).read_bytes()).hexdigest(),
                        source_hashes[slug])
                for family in {r['folder'] for r in records}:
                    folder = BeautifulSoup(
                        (out/BASE.strip('/')/family/'index.html').read_text(),
                        'html.parser')
                    expected = {r['url'] for r in records if r['folder']==family}
                    self.assertEqual(
                        {a['href'] for a in folder.select('a[data-greek-entry]')},
                        expected)


if __name__ == '__main__':
    unittest.main()
