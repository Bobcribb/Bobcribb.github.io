import sys
import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_greek_corpus import book_sections, main, verify, BOOKS, ARCHIVES, rewritten_studies, REWRITES, scholarly_title


class GreekCorpusTests(unittest.TestCase):
    def test_subject_title_is_not_replaced_by_abstract_or_repeated_number(self):
        with TemporaryDirectory() as tmp:
            page = Path(tmp) / 'chapter.md'
            for text, expected in [
                ('# Chapitre 384 — Harmonia : Cadmos et Thèbes\n## Résumé scientifique', 'Harmonia : Cadmos et Thèbes'),
                ('# MYTHOS — Encyclopédie\n## Chapitre 385 — ILITHYIE\n### Naissance et vulnérabilité', 'ILITHYIE'),
                ('# Chapitre 12\n## Chiron\n### Introduction', 'Chiron'),
            ]:
                page.write_text(text)
                self.assertEqual(scholarly_title(page), expected)

    def test_rewrite_uses_allocation_receipt_and_keeps_historical_reference(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / REWRITES
            manifest.parent.mkdir(parents=True)
            study = {'request_id': 'request-a', 'slug': 'chiron', 'title': 'Chiron',
                     'historical_number': 118, 'kind': 'identified', 'series': 'pelion-hesperides'}
            manifest.write_text(json.dumps({'version': 1, 'studies': [study]}))
            registry = root / 'editorial/numbering.json'
            registry.parent.mkdir()
            source = root / 'chapitres/encyclopedie/chapitre-981-chiron.md'
            source.parent.mkdir(parents=True)
            source.write_text('# Chapitre 981\n## Chiron\nNouvelle rédaction.')
            allocation = {'number': 981, 'path': source.relative_to(root).as_posix()}
            registry.write_text(json.dumps({'collections': {'encyclopedie': {'allocations': {'request-a': allocation}}}}))
            row = rewritten_studies(root)[0]
            self.assertEqual(row['number'], 981)
            self.assertEqual(row['historical_number'], 118)
            self.assertEqual(row['url'], '/chapitres/encyclopedie/chapitre-981-chiron/')
            registry.write_text(json.dumps({'collections': {'encyclopedie': {'allocations': {}}}}))
            with self.assertRaisesRegex(RuntimeError, 'non attribuée'):
                rewritten_studies(root)

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
            register = out / 'grande-encyclopedie/registre-integral/index.html'
            register.parent.mkdir(parents=True, exist_ok=True)
            register.write_text('<html><body><p>Six collections</p></body></html>')
            main(out, root)
            verify(out, root)
            for slug in ('mythologie-grecque', 'grande-encyclopedie'):
                for path in (out / slug / 'index.html', out / (slug + '.html')):
                    d = BeautifulSoup(path.read_text(), 'html.parser')
                    self.assertEqual(
                        [link['href'] for link in d.select('link[rel~="canonical"]')],
                        ['https://bobmythos.fr/mythologie-grecque/'])
                    self.assertEqual(len(d.select(
                        'a[href="/grande-encyclopedie/registre-integral/"]')), 1)
            page = out / 'grande-encyclopedie.html'
            doc = BeautifulSoup(page.read_text(), 'html.parser')
            doc.find('a', href='/chapitres/encyclopedie/chapitre-12-etude/').decompose()
            page.write_text(str(doc))
            with self.assertRaisesRegex(AssertionError, 'Textes absents'):
                verify(out, root)
