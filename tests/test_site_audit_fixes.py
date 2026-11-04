"""Régressions des anomalies publiques relevées pendant l'audit complet."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_native as build
import build_navigation as navigation
from apply_museum_design import apply as apply_museum_design


class SiteAuditFixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw, encoding='utf-8')
        return path

    def test_bibliography_links_target_actual_anchors_without_unescaping_active_html(self):
        raw = '[R1](#ref-1)\n\n<a id="ref-1"></a>**[R1]** Source\n\n<script>alert(1)</script>\n\n<a id="bad" onclick="alert(1)"></a>'
        result = build.resolve_chapter_links(build.markdown(raw), self.root/'chapter.md', self.root)
        doc = BeautifulSoup(result, 'html.parser')
        self.assertIsNotNone(doc.select_one('#ref-1'))
        self.assertEqual(doc.select_one('a')['href'], '#ref-1')
        self.assertIsNone(doc.find('script'))
        self.assertIsNone(doc.select_one('[onclick]'))
        self.assertIsNone(doc.select_one('#bad'))

    def test_museum_design_preserves_html_attachments_byte_for_byte(self):
        raw = '<!doctype html><html><head><title>Annexe</title></head><body><h1>Annexe</h1><main><p>Source intacte.</p></main></body></html>\n'
        attachments = [self.write(name, raw) for name in
                       ['assets/philosophie/audit.html', 'media/annexe.html']]
        page = self.write('etude/index.html', raw)
        self.assertEqual(apply_museum_design(self.root), 1)
        for attachment in attachments:
            self.assertEqual(attachment.read_bytes(), raw.encode('utf-8'))
        self.assertIn('data-mythos-design', page.read_text())

    def test_chapter_toc_anchors_are_unique_and_existing_ids_are_preserved(self):
        result = build.resolve_chapter_links('<a href="#chap-853">Sommaire</a><h2>853. Monstres</h2><h2>Chapitre 443 — Éleusis</h2><h2>Chapitre 443 — Complément</h2><h2 id="custom">Chapitre 444</h2>', self.root/'chapter.md', self.root)
        doc = BeautifulSoup(result, 'html.parser')
        self.assertIsNotNone(doc.select_one('#chap-853'))
        self.assertEqual(len(doc.select('#chapitre-443')), 1)
        self.assertIsNotNone(doc.select_one('#custom'))

    def test_standalone_philosophy_and_sites_are_searchable_and_in_sitemap(self):
        self.write('search.json', '[]')
        for i in range(450):
            self.write(f'dossier-{i}/index.html', f'<h1>Dossier {i}</h1>')
        paths = ['philosophie-iliade.html', 'philosophie-odyssee.html', 'philosophie-theogonie.html', 'sites/dodone.html']
        for name in paths:
            self.write(name, f'<title>{name}</title><main><h1>{name}</h1><p>Étude</p></main>')
        self.write('404.html', '<h1>Erreur</h1>')
        self.write('redirect.html', '<meta http-equiv="refresh" content="0;url=/"><h1>Ancien lien</h1>')
        with patch.object(build, 'OUT', self.root):
            build.reindex([])
            first = json.loads((self.root/'search.json').read_text())
            build.reindex([])
            self.assertEqual(first, json.loads((self.root/'search.json').read_text()))
        urls = {item['url'] for item in first}
        for name in paths:
            self.assertIn('/'+name, urls)
            self.assertIn('https://bobmythos.fr/'+name, (self.root/'sitemap.xml').read_text())
        self.assertNotIn('/404.html', urls)
        self.assertNotIn('/redirect.html', urls)

    def test_analysis_index_can_rebuild_twice_without_accumulating_ids(self):
        path = self.write('theatre-grec-conserve-etudes-philosophiques/index.html', '<main><article class="content"><h1>Analyses</h1><div id="archives-analyses-conservees"></div><div id="archives-analyses-conservees"></div><p>Texte historique conservé.</p></article></main>')
        entries = json.loads((ROOT/'search.json').read_text())
        with patch.object(navigation, 'OUT', self.root):
            for _ in range(2):
                navigation.reorganize_preserved_plays_analyses(entries)
                doc = BeautifulSoup(path.read_text(), 'html.parser')
                self.assertEqual(len(doc.select('#archives-analyses-conservees')), 1)
                self.assertEqual(len(doc.select('#index-analyses-conservees')), 1)
                self.assertEqual(len(doc.select('.analysis-work-grid li')), 51)
                self.assertIn('Texte historique conservé.', doc.get_text())

    def test_archived_links_migrate_only_to_existing_pages(self):
        source = self.root/'source'
        output = self.root/'output'
        source.mkdir(); output.mkdir()
        def source_file(name, raw):
            p=source/name;p.parent.mkdir(parents=True, exist_ok=True);p.write_text(raw)
        source_file('corpus/mythologie-grecque/archives/book.html', '<link href="assets/style.css" rel="stylesheet"><script src="assets/app.js"></script><a href="dieu-zeus.html#source">Zeus</a><a href="missing.html">Inconnu</a><a href="kept.html">Archive</a><a href="control.json">Contrôle</a>')
        source_file('corpus/mythologie-grecque/archives/assets/style.css', 'body{color:gold}')
        source_file('corpus/mythologie-grecque/archives/assets/app.js', '"use strict";')
        source_file('corpus/mythologie-grecque/archives/control.json', '{"ok":true}')
        source_file('corpus/mythologie-grecque/archives/kept.html', '<h1>Archive existante</h1>')
        source_file('dieu-zeus/index.html', '<h1>Zeus</h1>')
        with patch.object(build, 'ROOT', source), patch.object(build, 'OUT', output), patch.object(build, 'MIN_HTML_PAGES', 0), patch.object(build, 'MIN_MEDIA_FILES', 0):
            build.copy_repository()
        doc=BeautifulSoup((output/'corpus/mythologie-grecque/archives/book.html').read_text(), 'html.parser')
        self.assertEqual([a['href'] for a in doc.find_all('a')], ['/dieu-zeus/#source','missing.html','kept.html','control.json'])
        for name in ['assets/style.css', 'assets/app.js', 'control.json']:
            self.assertEqual((output/'corpus/mythologie-grecque/archives'/name).read_bytes(), (source/'corpus/mythologie-grecque/archives'/name).read_bytes())
        self.assertIn('dieu-zeus.html#source', (source/'corpus/mythologie-grecque/archives/book.html').read_text())


    def test_origines_landing_keeps_single_primary_heading(self):
        """The museum banner is H1; archive subsection is H2 after rebuild."""
        page = BeautifulSoup((ROOT / 'origines-du-sacre/index.html').read_text(
            encoding='utf-8'), 'html.parser')
        self.assertEqual(len(page.select('h1')), 1)
        self.assertIsNotNone(page.select_one('h1.mythos-banner-title'))
        archive_heading = page.select_one('.origins-archives > h2')
        self.assertIsNotNone(archive_heading)
        self.assertEqual(archive_heading.get_text(strip=True), 'Origines du sacré')
        self.assertIsNotNone(page.select_one('#numerotation-origines-du-sacre'))

    def test_archived_spa_hash_is_not_misreported_as_missing_anchor(self):
        from improve_reading import audit
        self.write('catalog/entries.json', '{"entries": []}')
        self.write('corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html',
                   '<html><head><title>Bibliothèque</title></head><body>'
                   '<a href="#/accueil">Accueil (route JS)</a>'
                   '<script>window.addEventListener("hashchange", () => {})</script>'
                   '<a href="#ancre-absente">Lien incorrect à signaler</a></body></html>')
        report = audit(self.root)
        self.assertEqual(report['status'], 'passed')
        self.assertEqual(report['new_navigation_errors'], [])
        self.assertEqual(report['legacy_link_issues'],
                         [{'page': '/corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html',
                           'url': '#ancre-absente', 'problem': 'ancre absente'}])

    def test_integral_origines_archive_ids_are_unique(self):
        """Compilation I–XXVII: each bibliography link must reach its own tome."""
        from urllib.parse import unquote
        source = ROOT / 'corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html'
        doc = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
        ids = [str(tag['id']) for tag in doc.select('[id]')]
        self.assertEqual(len(ids), len(set(ids)), 'Duplicate archive HTML ids')
        available = set(ids)
        links = [unquote(tag['href'][1:]) for tag in doc.select('a[href^="#"]')
                 if len(tag['href']) > 1 and not tag['href'].startswith('#/')]
        self.assertTrue(links)
        self.assertEqual([], sorted(set(link for link in links if link not in available)))
        for anchor in ('chap-1013', 'chap-1052', 'ref-1',
                       'ref-1--tome-xxiv', 'ref-1--tome-xxv',
                       'ref-1--tome-xxvi'):
            self.assertIn(anchor, available)



if __name__ == '__main__':
    unittest.main()
