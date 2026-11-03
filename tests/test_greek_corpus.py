import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_greek_corpus import book_sections, main, verify, BOOKS, ARCHIVES


class GreekCorpusTests(unittest.TestCase):
    def test_existing_and_duplicate_headings_keep_stable_links_and_prose(self):
        with TemporaryDirectory() as tmp:
            out = Path(tmp)
            page = out / 'livre-atrides' / 'index.html'
            page.parent.mkdir()
            original = '<article class="content"><h1>Atrides</h1><h2 id="ancien">Tantale</h2><p>Texte intégral, α et β.</p><h2>Oreste</h2><p>Premier dossier.</p><h3>Oreste</h3><p>Variante conservée.</p><table><tr><td>Source</td></tr></table></article>'
            page.write_text(original)
            before = BeautifulSoup(original, 'html.parser').get_text()
            first = book_sections(out, 'livre-atrides')
            self.assertEqual(first[0][0], '/livre-atrides/#ancien')
            self.assertEqual(len(set(url for url, _ in first)), 3)
            self.assertEqual(BeautifulSoup(page.read_text(), 'html.parser').get_text(), before)
            self.assertEqual(book_sections(out, 'livre-atrides'), first)

    def test_missing_legacy_book_is_not_silently_dropped(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, 'Livre grec absent'):
                book_sections(Path(tmp), 'livre-atrides')

    def test_all_four_entry_points_receive_the_full_catalogue(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / 'source'
            out = Path(tmp) / 'site'
            for title, slug in BOOKS:
                page = out / slug / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text('<article class="content"><h1>'+title+'</h1><h2>Texte existant</h2><p>Corps conservé.</p></article>')
            for _, name in ARCHIVES:
                page = out / 'corpus/mythologie-grecque/archives' / name
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text('<h1>Archive conservée</h1>')
            for n in range(1, 56):
                source = root / 'chapitres/encyclopedie' / f'chapitre-{n}-etude.md'
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(f'# Chapitre {n} : Sujet {n}\n\nTexte original.')
                page = out / source.relative_to(root).with_suffix('') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(f'<h1>Sujet {n}</h1>')
            portal = out / 'mythologie-grecque/index.html'
            portal.parent.mkdir(parents=True)
            portal.write_text('<html><head></head><body><main><article class="content"><h1>Ancien sommaire</h1></article></main></body></html>')
            main(out, root)
            verify(out, root)
            page = out / 'grande-encyclopedie.html'
            doc = BeautifulSoup(page.read_text(), 'html.parser')
            doc.find('a', href='/chapitres/encyclopedie/chapitre-12-etude/').decompose()
            page.write_text(str(doc))
            with self.assertRaisesRegex(AssertionError, 'Textes absents'):
                verify(out, root)
