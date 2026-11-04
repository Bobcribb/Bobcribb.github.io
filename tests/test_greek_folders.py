"""Coverage, preservation and navigation checks for the thematic Greek library."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_greek_folders import BASE, build, classify, inventory, verify, LEGACY_FOLDERS


class GreekFolderTests(unittest.TestCase):
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
            book = out / 'livre-thebes/index.html'
            book.parent.mkdir()
            book.write_text('<article><h1>Thèbes</h1><h2 id="oedipe">Œdipe</h2><p>Texte préservé.</p></article>')
            original_book = book.read_bytes()
            groups = [('Études', 'grec-universitaire', [(url, 'Chapitre 347 — Delphes')]),
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
