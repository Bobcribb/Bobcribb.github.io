"""Coverage, preservation and navigation checks for the thematic Greek library."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_greek_folders import BASE, build, classify, inventory, verify, LEGACY_FOLDERS, CSS


class GreekFolderTests(unittest.TestCase):
    def test_thematic_links_are_touch_accessible_without_reflowing_books(self):
        self.assertIn('.greek-folder-links a{display:flex;align-items:center;min-height:44px', CSS)
        self.assertIn('overflow-wrap:anywhere', CSS)
        self.assertIn('@media(max-width:700px)', CSS)
        self.assertIn('.greek-folder-toc a:focus-visible', CSS)
        # Les panneaux sont ajoutés aux monographies, pas seulement aux
        # sommaires : leur présentation doit vivre dans le CSS commun.
        shared_css = (Path(__file__).resolve().parents[1] /
                      'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('body.mythos-design .greek-cross-readings a{display:flex;min-height:44px',
                      shared_css)
        self.assertIn('@media(max-width:700px){body.mythos-design .greek-cross-readings ul',
                      shared_css)
        self.assertIn('data-greek-cross-readings="delphes"', shared_css)
        self.assertIn('border-inline-start:3px solid #d0aa68', shared_css)
        self.assertIn('data-greek-cross-readings="aphrodite"', shared_css)
        self.assertIn('border-inline-start:3px solid #d9af6b', shared_css)
        self.assertIn('@media(max-width:480px)', shared_css)

    def test_single_greek_encyclopedia_entry_in_both_menus(self):
        from apply_museum_design import header
        doc = header('/mythologie-grecque/')
        for nav in doc.select('nav'):
            self.assertEqual(len(nav.select('a[href="/mythologie-grecque/"]')), 1)
            self.assertFalse(nav.select('a[href="/grande-encyclopedie/"]'))

    def test_primary_subject_is_used_instead_of_incidental_names(self):
        cases = [
            ('chapitre-342-medee-athenes-egee-thesee', 'heros'),
            ('chapitre-384-harmonia-cadmos-collier-mariage-thebes-samothrace', 'familles'),
            ('chapitre-380-promethee-pandore-nouvelle-etude', 'cosmogonies'),
            ('chapitre-348-pythie-delphes-parole-inspiree', 'cultes-sanctuaires'),
            ('chapitre-359-chiron-nouvelle-etude', 'heros'),
            ('chapitre-999-zeus-nouvelle-etude', 'divinites'),
            ('chapitre-389-hebe-jeunesse-heracles-phlionte', 'divinites'),
            ('chapitre-390-kairos-occasion-mesure-temps-opportun', 'divinites'),
            ('chapitre-999-sujet-inconnu', 'sources-anciennes'),
        ]
        for slug, folder in cases:
            self.assertEqual(classify('/chapitres/encyclopedie/'+slug+'/',
                                      'Apollon et Zeus cités dans une comparaison', 'Chapitre universitaire')[0], folder)
        self.assertEqual(classify('/monographies/#oedipe', 'Œdipe', 'Section de livre')[0], 'familles')

    def test_recent_published_monographs_have_a_precise_single_home(self):
        # Classement des sujets et non des noms cités dans les développements.
        # Les manuscrits et leurs cotes restent inchangés.
        cases = {
            '420-makaria-heraclides-sacrifice-volontaire-asile-athenes': 'familles',
            '419-agdistis-phrygie-attis-cybele-pessinonte': 'divinites',
            '418-eunostos-tanagra-myrtis-ochna-heroion-bois-sacre-interdit': 'cultes-sanctuaires',
            '417-epimenide-crete-sommeil-purification-athenes-cylon': 'cultes-sanctuaires',
            '416-eiresione-rameau-pyanepsies-apollon-prosperite': 'cultes-sanctuaires',
            '415-alastor-vengeance-sang-atrides-erinyes-tragedie': 'familles',
            '414-bendis-deesse-thrace-piree-bendideia-platon-associations-cultes': 'cultes-sanctuaires',
            '413-couretes-corybantes-zeus-enfant-danse-armee-crete': 'cosmogonies',
            '411-pothos-desir-absent-erotes-scopas-megare': 'divinites',
            '410-telesphoros-pergame-guerison-enfant-capuchon-asclepios': 'cultes-sanctuaires',
            '409-agathos-daimon-serpent-maison-alexandrie-prosperite': 'cultes-sanctuaires',
            '408-asopos-dieu-fleuve-egine-zeus-filles-cites': 'divinites',
            '407-cnossos-palais-minoen-archeologie-et-labyrinthe': 'sources-anciennes',
            '404-zeus-meilichios-diasia-serpent-purification-athenes-selinonte': 'cultes-sanctuaires',
        }
        for slug, expected_folder in cases.items():
            path = 'chapitre-' + slug
            url = '/chapitres/encyclopedie/' + path + '/'
            source = Path(__file__).resolve().parents[1] / 'chapitres/encyclopedie' / (path + '.md')
            self.assertTrue(source.is_file(), 'Manuscrit public absent : ' + path)
            dossier, section = classify(url, 'Chapitre : mythes, sources et bibliographie',
                                        'Chapitre universitaire')
            self.assertEqual(dossier, expected_folder, path)
            self.assertNotEqual(section, 'Nouvelles études à classer', path)
        # Toute autre étude vraiment inconnue demeure dans la file à classer.
        self.assertEqual(classify('/chapitres/encyclopedie/chapitre-999-theme-inconnu/',
                                  'Aucun sujet reconnu', 'Chapitre universitaire'),
                         ('sources-anciennes', 'Nouvelles études à classer'))

    def test_recent_documented_studies_leave_generic_sorting_queue(self):
        # Huit études intègres de 2026 déjà reçues et attribuées sur main ;
        # leur classement ne doit pas se fonder sur des mots fortuits de la prose.
        cases = {
            '401-tritopatores-ancetres-athenes-kerameikos-selinonte-rites-purification':
                ('cultes-sanctuaires', 'Ancêtres, naissance et rites de purification'),
            '402-sosipolis-elide-olympie-enfant-serpent-zeus-magnesie-cultes':
                ('cultes-sanctuaires', 'Olympie, Élide et dieux protecteurs des cités'),
            '403-ennodia-thessalie-pherai-larissa-hecate-artemis-cultes-routes':
                ('cultes-sanctuaires', 'Thessalie — déesses des routes et des seuils'),
            '405-acheloos-dieu-fleuve-heracles-dejanire-corne-abondance':
                ('divinites', 'Dieux-fleuves, paysages et eaux divinisées'),
            '406-poseidon-hippocampes-chevaux-divins-mer':
                ('divinites', 'Poséidon et le cortège marin'),
            '412-aristeas-proconnese-arimaspes-apollon-hyperboreens':
                ('sources-anciennes', 'Poètes, voyages et traditions fragmentaires'),
            '421-praxidikai-praxidike-serments-haliarte-beotie-mnaseas':
                ('cultes-sanctuaires', 'Haliarte — serments, justice et sanction sacrée'),
            '422-salmakis-halicarnasse-hermaphrodite-source-inscription':
                ('cultes-sanctuaires', 'Halicarnasse — fontaines, inscriptions et métamorphoses'),
        }
        for suffix, expected in cases.items():
            slug = 'chapitre-' + suffix
            source = Path(__file__).resolve().parents[1] / 'chapitres' / 'encyclopedie' / (slug + '.md')
            self.assertTrue(source.is_file(), source)
            manuscript = source.read_text(encoding='utf-8')
            self.assertGreater(len(manuscript), 9000, slug)
            self.assertIn('bibliograph', manuscript.lower(), slug)
            actual = classify('/chapitres/encyclopedie/' + slug + '/',
                              'Titre ancien mentionnant Zeus sans rapport avec le sujet',
                              'Chapitre universitaire')
            self.assertEqual(actual, expected, slug)
            self.assertNotEqual(actual[1], 'Nouvelles études à classer')

    def test_artemis_amarysia_has_attribution_and_precise_thematic_home(self):
        import json
        from build_greek_folders import ARTEMIS_STUDIES
        root = Path(__file__).resolve().parents[1]
        register = json.loads((root / 'editorial/numbering.json').read_text(encoding='utf-8'))
        allocations = register['collections']['encyclopedie']['allocations']
        all_paths = {entry['path']: entry['number'] for entry in allocations.values()}
        expected_section = 'Amarynthos et Érétrie — Artémis Amarysia, fêtes et inscriptions'
        for url, title, _ in ARTEMIS_STUDIES:
            manuscript_path = url.strip('/') + '.md'
            source = root / manuscript_path
            self.assertTrue(source.is_file(), manuscript_path)
            manuscript = source.read_text(encoding='utf-8')
            self.assertGreater(len(manuscript), 7000, manuscript_path)
            self.assertIn('bibliograph', manuscript.lower(), manuscript_path)
            self.assertTrue((root / url.strip('/') / 'index.html').is_file(), url)
            self.assertIn(manuscript_path, all_paths)
            self.assertIn('Chapitre ' + str(all_paths[manuscript_path]), title)
        amarysia = ARTEMIS_STUDIES[0][0]
        self.assertEqual(all_paths[amarysia.strip('/') + '.md'], 426)
        self.assertEqual(classify(amarysia, 'Un autre dieu mentionné dans le texte',
                                  'Chapitre universitaire'),
                         ('cultes-sanctuaires', expected_section))

    def test_artemis_cross_readings_are_reciprocal_and_do_not_change_sources(self):
        from build_greek_folders import ARTEMIS_STUDIES
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            articles = {}
            for url, title, _ in ARTEMIS_STUDIES:
                page = out / url.strip('/') / 'index.html'
                page.parent.mkdir(parents=True)
                page.write_text('<html><head><title>Étude</title></head><body>'
                                '<main><article class="content"><h1>' + title + '</h1>'
                                '<section id="sources"><h2>Sources</h2><p>'
                                'Témoignages distincts, bibliographie complète.'
                                '</p></section></article></main></body></html>',
                                encoding='utf-8')
                articles[url] = str(BeautifulSoup(page.read_text(encoding='utf-8'),
                                                  'html.parser').article)
            groups = [('Études vérifiées', 'grec-universitaire',
                       [(url, title) for url, title, _ in ARTEMIS_STUDIES])]
            expected_urls = {url for url, _, _ in ARTEMIS_STUDIES}
            for _ in range(2):
                rows = build(out, groups, [], [])
                verify(out, expected_urls)
                self.assertEqual({r['url'] for r in rows}, expected_urls)
                folder = BeautifulSoup(
                    (out / BASE.strip('/') / 'cultes-sanctuaires/index.html')
                    .read_text(encoding='utf-8'), 'html.parser')
                amarysia_url = ARTEMIS_STUDIES[0][0]
                self.assertIsNotNone(folder.select_one(
                    'a[data-greek-entry][href="' + amarysia_url + '"]'))
                for url in expected_urls:
                    page = out / url.strip('/') / 'index.html'
                    doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), articles[url])
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    panels = doc.select('aside[data-greek-cross-readings="artemis"]')
                    self.assertEqual(len(panels), 1, url)
                    links = [a['href'] for a in panels[0].select('a[href]')]
                    self.assertEqual(set(links), expected_urls - {url})
                    self.assertEqual(len(links), 3)

    def test_delphes_philosophy_study_is_classified_and_linked_reciprocally(self):
        from build_greek_folders import DELPHES_STUDIES
        from build_greek_corpus import RELATED
        root = Path(__file__).resolve().parents[1]
        socrates = DELPHES_STUDIES[0][0]
        self.assertIn(socrates, {url for _, url in RELATED})
        self.assertEqual(
            classify(socrates, 'Socrate et l’oracle de Delphes', 'Lecture associée'),
            ('interpretations-philosophiques', 'Socrate — oracle, enquête et sagesse'))
        self.assertTrue((root / 'assets/philosophie/'
                         'socrate-oracle-delphes-paradoxe-sagesse-2026.pdf').is_file())
        for url, _, _ in DELPHES_STUDIES:
            source = root / (url.strip('/') + '.md')
            manuscript = source.read_text(encoding='utf-8')
            self.assertGreater(len(manuscript), 14000, str(source))
            self.assertIn('bibliograph', manuscript.lower(), str(source))
            self.assertTrue((root / url.strip('/') / 'index.html').is_file(), url)
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            originals = {}
            for url, title, _ in DELPHES_STUDIES:
                page = out / url.strip('/') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<html><head><title>Étude</title></head><body><main>'
                    '<article class="content"><h1>' + title + '</h1>'
                    '<p>Texte intégral conservé, sources, bibliographie et annexes.</p>'
                    '</article></main></body></html>', encoding='utf-8')
                originals[url] = str(BeautifulSoup(page.read_text(encoding='utf-8'),
                                                   'html.parser').article)
            groups = [
                ('Delphes', 'grec-universitaire',
                 [(url, title) for url, title, _ in DELPHES_STUDIES[1:]]),
                ('Philosophie', 'grec-liens',
                 [(DELPHES_STUDIES[0][0], DELPHES_STUDIES[0][1])]),
            ]
            expected = {url for url, _, _ in DELPHES_STUDIES}
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({r['url'] for r in rows}, expected)
                verify(out, expected)
                folder = BeautifulSoup(
                    (out / BASE.strip('/') /
                     'interpretations-philosophiques/index.html').read_text(encoding='utf-8'),
                    'html.parser')
                self.assertIsNotNone(folder.select_one(
                    'a[data-greek-entry][href="' + socrates + '"]'))
                for url in expected:
                    doc = BeautifulSoup((out / url.strip('/') / 'index.html')
                                        .read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), originals[url])
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    panels = doc.select('aside[data-greek-cross-readings="delphes"]')
                    self.assertEqual(len(panels), 1, url)
                    links = [a['href'] for a in panels[0].select('a[href]')]
                    self.assertEqual(set(links), expected - {url})
                    self.assertEqual(len(links), 2)

    def test_paphos_full_study_enters_greek_catalogue_without_copying_any_source(self):
        from build_greek_folders import APHRODITE_STUDIES
        from build_greek_corpus import RELATED
        root = Path(__file__).resolve().parents[1]
        urls = {url for url, _, _ in APHRODITE_STUDIES}
        self.assertEqual(len(urls), 3)
        paphos = APHRODITE_STUDIES[2][0]
        self.assertIn(paphos, {url for _, url in RELATED})
        self.assertEqual(
            classify(paphos, 'Aphrodite citée dans plusieurs sources',
                     'Lecture associée'),
            ('cultes-sanctuaires', 'Palaepaphos — Aphrodite et histoire du sanctuaire'))
        self.assertEqual(classify(APHRODITE_STUDIES[0][0],
                                  'Monographie intégrale', 'Étude')[0], 'divinites')
        self.assertEqual(classify(APHRODITE_STUDIES[1][0],
                                  'Sappho', 'Dossier documentaire')[0], 'sources-anciennes')
        for url in urls:
            path = root / url.lstrip('/')
            if url.endswith('/'):
                path /= 'index.html'
            self.assertTrue(path.is_file(), url)
            html = path.read_text(encoding='utf-8')
            self.assertGreater(len(html), 18000, url)
            self.assertTrue('bibliograph' in html.lower() or
                            'sources académiques' in html.lower(), url)

    def test_aphrodite_paphos_sappho_links_are_reciprocal_and_idempotent(self):
        from build_greek_folders import APHRODITE_STUDIES
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            originals = {}
            for url, title, _ in APHRODITE_STUDIES:
                page = out / url.lstrip('/')
                if url.endswith('/'):
                    page /= 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<html><head><title>Étude intégrale</title></head><body>'
                    '<main><article class="content"><h1>' + title + '</h1>'
                    '<section><p>Source antique, appareil critique et bibliographie '
                    'conservés. Aphrodite ≠ histoire du sanctuaire.</p></section>'
                    '</article></main></body></html>', encoding='utf-8')
                originals[url] = str(BeautifulSoup(page.read_text(encoding='utf-8'),
                                                   'html.parser').article)
            groups = [
                ('Monographie', 'grec-monographies',
                 [(APHRODITE_STUDIES[0][0], APHRODITE_STUDIES[0][1])]),
                ('Dossier de sources', 'grec-dossiers',
                 [(APHRODITE_STUDIES[1][0], APHRODITE_STUDIES[1][1])]),
                ('Civilisation déjà publiée', 'grec-liens',
                 [(APHRODITE_STUDIES[2][0], APHRODITE_STUDIES[2][1])]),
            ]
            urls = {u for u, _, _ in APHRODITE_STUDIES}
            for _ in range(2):
                rows = build(out, groups, [], [])
                verify(out, urls)
                self.assertEqual({r['url'] for r in rows}, urls)
                self.assertEqual(len(rows), 3)
                for url in urls:
                    page = out / url.lstrip('/')
                    if url.endswith('/'):
                        page /= 'index.html'
                    doc = BeautifulSoup(page.read_text(encoding='utf-8'),
                                        'html.parser')
                    self.assertEqual(str(doc.article), originals[url], url)
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    boxes = doc.select('aside[data-greek-cross-readings="aphrodite"]')
                    self.assertEqual(len(boxes), 1, url)
                    links = [a['href'] for a in boxes[0].select('a[href]')]
                    self.assertEqual(set(links), urls - {url})
                    self.assertEqual(len(links), 2)
            folder = BeautifulSoup(
                (out / BASE.strip('/') / 'cultes-sanctuaires/index.html')
                .read_text(encoding='utf-8'), 'html.parser')
            self.assertIsNotNone(folder.select_one(
                'a[data-greek-entry][href="' + APHRODITE_STUDIES[2][0] + '"]'))

    def test_one_home_per_destination_with_separate_book_sections(self):
        groups = [('Livres', 'grec-livres', [('/livre-thebes/', 'Thèbes')]),
                  ('Encore le livre', 'grec-dossiers', [('/livre-thebes/', 'Autre titre')])]
        sections = [('Thèbes', [('/livre-thebes/#cadmos', 'Cadmos'), ('/livre-thebes/#oedipe', 'Œdipe')])]
        rows = inventory(groups, sections, [('Thèbes', 'livre-thebes')])
        self.assertEqual(len(rows), 3)
        self.assertEqual([r['kind'] for r in rows].count('Livre'), 1)
        self.assertEqual([r['kind'] for r in rows].count('Section de livre'), 2)
        self.assertEqual({r['folder'] for r in rows}, {'familles'})

    def test_complete_generation_preserves_article_and_deep_links_after_rebuild(self):
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            url = '/chapitres/encyclopedie/chapitre-347-apollon-python-delphes-oracle/'
            chapter = out / url.strip('/') / 'index.html'
            chapter.parent.mkdir(parents=True)
            chapter.write_text('<html><head><title>Delphes</title></head><body><main><article class="content">'
                               '<h1>Delphes</h1><p id="source">Texte intégral, αἰδώς et bibliographie.</p>'
                               '<a href="https://example.org/source">Source antique</a></article></main></body></html>')
            article = str(BeautifulSoup(chapter.read_text(), 'html.parser').article)
            second_url = '/chapitres/encyclopedie/chapitre-414-bendis-deesse-thrace-piree/'
            second = out / second_url.strip('/') / 'index.html'
            second.parent.mkdir(parents=True)
            second.write_text('<html><body><main><article class="content">'
                              '<h1>Bendis</h1><p>Étude complète et sources.</p>'
                              '</article></main></body></html>')
            second_article = str(BeautifulSoup(second.read_text(), 'html.parser').article)
            book = out / 'livre-thebes/index.html'
            book.parent.mkdir()
            book.write_text('<article><h1>Thèbes</h1><h2 id="oedipe">Œdipe</h2><p>Texte préservé.</p></article>')
            original_book = book.read_bytes()
            groups = [('Études', 'grec-universitaire', [
                          (url, 'Chapitre 347 — Delphes'),
                          (second_url, 'Chapitre 414 — Bendis')]),
                      ('Livres', 'grec-livres', [('/livre-thebes/', 'Thèbes')])]
            sections = [('Thèbes', [('/livre-thebes/#oedipe', 'Œdipe')])]
            for _ in range(2):
                rows = build(out, groups, sections, [('Thèbes', 'livre-thebes')])
                verify(out, {r['url'] for r in rows})
                alias = BeautifulSoup((out / BASE.strip('/') / 'thebes/index.html').read_text(), 'html.parser')
                self.assertIn(BASE+'familles/', alias.select_one('meta[http-equiv="refresh"]')['content'])
                doc = BeautifulSoup(chapter.read_text(), 'html.parser')
                self.assertEqual(str(doc.article), article)
                self.assertEqual(book.read_bytes(), original_book)
                self.assertEqual(len(doc.select('[data-greek-folder-nav]')), 1)
                self.assertIsNotNone(doc.select_one('a[href="'+BASE+'cultes-sanctuaires/"]'))
                # The chapter has a direct backlink to its exact subsection.
                # This anchor is the same one emitted by the dossier TOC.
                topic = doc.select_one('nav[data-greek-folder-nav] a.greek-folder-return-topic')
                self.assertIsNotNone(topic)
                self.assertEqual(topic['href'], BASE+'cultes-sanctuaires/#theme-1')
                self.assertIn('Delphes', topic.get_text(' ', strip=True))
                thematic = BeautifulSoup(
                    (out / BASE.strip('/') / 'cultes-sanctuaires/index.html').read_text(),
                    'html.parser')
                self.assertIsNotNone(thematic.select_one('#theme-1 a[href="'+url+'"]'))
                self.assertIsNotNone(thematic.select_one('nav.greek-folder-toc a[href="#theme-1"]'))
                second_doc = BeautifulSoup(second.read_text(), 'html.parser')
                self.assertEqual(str(second_doc.article), second_article)
                second_topic = second_doc.select_one('a.greek-folder-return-topic')
                self.assertEqual(second_topic['href'], BASE+'cultes-sanctuaires/#theme-2')
                self.assertIn('Cultes thraces', second_topic.get_text(' ', strip=True))
                self.assertIsNotNone(thematic.select_one('#theme-2 a[href="'+second_url+'"]'))
                self.assertIsNotNone(thematic.select_one('nav.greek-folder-toc a[href="#theme-2"]'))
                self.assertIn('scroll-margin-top:115px',
                              (out / BASE.strip('/') / 'cultes-sanctuaires/index.html').read_text())
            folder = out / BASE.strip('/') / 'familles/index.html'
            doc = BeautifulSoup(folder.read_text(), 'html.parser')
            doc.select_one('a[data-greek-entry][href="/livre-thebes/#oedipe"]').decompose()
            folder.write_text(str(doc))
            with self.assertRaisesRegex(AssertionError, 'incomplet'):
                verify(out, {r['url'] for r in rows})
                alias = BeautifulSoup((out / BASE.strip('/') / 'thebes/index.html').read_text(), 'html.parser')
                self.assertIn(BASE+'familles/', alias.select_one('meta[http-equiv="refresh"]')['content'])

    def test_future_unclassified_chapter_stays_visible(self):
        rows = inventory([('Études', 'grec-universitaire', [
            ('/chapitres/encyclopedie/chapitre-1000-nouveau-sujet/', 'Une étude à venir')])], [], [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['section'], 'Nouvelles études à classer')


if __name__ == '__main__':
    unittest.main()
