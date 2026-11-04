"""Regression cases for the reported mismatches and regenerated HTML."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup
import mistune

import editorial_illustrations as illustrations

ROOT = Path(__file__).resolve().parents[1]


class EditorialIllustrationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = illustrations.load_catalog()

    def render_page(self, slug, title, body="", legacy="", out=ROOT):
        source = f'<html><head></head><body><main class="layout visual-rails-active"><article class="content"><h1>{title}</h1>{body}</article>{legacy}</main></body></html>'
        result, selected = illustrations.decorate_document(source, Path(slug) / 'index.html', out, self.records)
        return BeautifulSoup(result, 'html.parser'), selected

    def test_reported_chapters_have_no_unrelated_fallback(self):
        for slug in ('471-inde-yuga-calendriers', '462-egypte-sistre-hathor'):
            with self.subTest(slug=slug):
                page = ROOT / 'chapitres/origines-du-sacre' / slug / 'index.html'
                before = BeautifulSoup(page.read_text(), 'html.parser')
                result, selected = illustrations.decorate_document(str(before), page, ROOT, self.records)
                after = BeautifulSoup(result, 'html.parser')
                self.assertEqual(selected, [])
                self.assertFalse(after.select('main > aside'))
                self.assertEqual(str(before.article), str(after.article))
                self.assertNotIn('visual-rails-active', after.main.get('class', []))

    def test_fresh_markdown_chapter_gets_same_selection(self):
        for slug in ('471-inde-yuga-calendriers', '462-egypte-sistre-hathor'):
            manuscript = ROOT / 'chapitres/origines-du-sacre' / (slug + '.md')
            source = '<html><head></head><body><main><article>' + mistune.html(manuscript.read_text()) + '</article></main></body></html>'
            _, selected = illustrations.decorate_document(source, Path(slug) / 'index.html', ROOT, self.records)
            self.assertEqual([], selected)

    def test_exact_subject_not_collection_or_body(self):
        doc, selected = self.render_page('chapitres/origines-du-sacre/900-inde-temps', 'Calendriers de l’Inde', '<p>Comparaison avec Derveni, Socrate et Maât.</p>')
        self.assertEqual([], selected)
        self.assertFalse(doc.select('aside'))

    def test_collections_have_no_generic_default(self):
        for path in ('theatre/une-piece-perdue', 'philosophie/epicure', 'civilisations/chine', 'grece/un-nouveau-sujet', 'mesopotamie/calendriers', 'perse/commerce', 'egypte/sistre'):
            with self.subTest(path=path):
                _, selected = self.render_page(path, 'Une étude universitaire')
                self.assertEqual([], selected)

    def test_relevant_selections_across_collections(self):
        for title, fragment in (('Enūma eliš', 'enuma-elish'), ('Maât', 'papyrus-ani'), ('Behistun', 'behistun'), ('Antigone', 'antigone'), ('Socrate', 'socrate'), ('Delphes', 'delphes')):
            with self.subTest(title=title):
                doc, selected = self.render_page('nouveau-chapitre', title)
                self.assertTrue(selected)
                allowed_extras = {'mythos-apollon-heracles-tripode-andokides-met-63-11-6'} if title == 'Delphes' else set()
                self.assertTrue(all(fragment in key or key in allowed_extras for key in selected))
                for figure in doc.select('aside figure'):
                    self.assertTrue(figure.img['alt'])
                    self.assertTrue(figure.select('figcaption a[href^="https://"]'))

    def test_word_boundaries_and_mithra_not_mithras(self):
        for title in ('Mithra dans l’Iran ancien', 'Antigonos', 'Les athénées'):
            _, selected = self.render_page('nouveau-chapitre', title)
            self.assertEqual([], selected)

    def test_snapshot_uses_the_page_title_moved_to_the_museum_banner(self):
        for banner, heading in [('Chapitre 260 : Astéria et la naissance de Délos', 'Introduction'), ('MYTHOS — Volume XCVII — Chapitre 315', 'Égée et l’oracle de Delphes'), ('MYTHOS — Volume CL (150)', 'Euripide, Médée')]:
            source = f'<html><body><header class="mythos-banner"><h1>{banner}</h1></header><main><article><h2>{heading}</h2><p>Texte conservé.</p></article></main></body></html>'
            result, selected = illustrations.decorate_document(source, Path('chapitre/index.html'), ROOT, self.records)
            self.assertGreaterEqual(len(selected), 2)
            self.assertIn('mythos-bottom-gallery', result)
            self.assertIn('Texte conservé.', result)

    def test_snapshot_does_not_select_from_a_comparative_subsection(self):
        source = '<html><body><header class="mythos-banner"><h1>Calendriers de l’Inde</h1></header><main><article><h2>Comparaison avec Derveni</h2><p>Étude.</p></article></main></body></html>'
        _, selected = illustrations.decorate_document(source, Path('calendriers/index.html'), ROOT, self.records)
        self.assertEqual([], selected)

    def test_work_heading_after_collection_heading(self):
        _, selected = self.render_page('volume-150', 'MYTHOS — Tragédies grecques', '<h1>Euripide, Médée</h1><p>Étude intégrale.</p>')
        self.assertEqual(['mythos-medee-fuite-char-serpents-hydrie-policoro-35296', 'mythos-van-loo-medee-jason'], selected)

    def test_enriched_iliad_has_four_distinct_sourced_documents(self):
        doc, selected = self.render_page('iliade', 'Iliade')
        self.assertEqual(4, len(selected))
        self.assertEqual(4, len(set(selected)))
        self.assertIn('mythos-papyrus-oxyrhynchus-20-iliade-ii', selected)
        for figure in doc.select('aside figure'):
            self.assertEqual(figure.img['src'], figure.select_one('a')['href'])
            self.assertEqual('lazy', figure.img['loading'])
            self.assertTrue(figure.select('figcaption a[href^="https://"]'))

    def test_alternate_local_hydria_is_not_repeated(self):
        body = '<figure><img src="/media/2026/10/mythos-persephone-enlevement-hydrie-apulie-met-07-128-1.jpg"><figcaption>Notice existante</figcaption></figure>'
        doc, selected = self.render_page('hades', 'Hadès', body)
        self.assertEqual([], selected)
        self.assertEqual(1, len(doc.select('img')))

    def test_new_subjects_do_not_use_civilization_fallbacks(self):
        for title in ('Calendriers de l’Inde', 'Mithra dans l’Iran ancien', 'Thèbes dans l’Égypte ancienne'):
            _, selected = self.render_page('nouveau-chapitre', title)
            self.assertEqual([], selected)

    def test_missing_local_media_never_triggers_fallback(self):
        with TemporaryDirectory() as tmp:
            doc, selected = self.render_page('derveni', 'Derveni', out=Path(tmp))
            self.assertEqual([], selected)
            self.assertFalse(doc.select('aside'))

    def test_existing_image_with_query_is_not_duplicated(self):
        record = next(r for r in self.records if 'antigone' in r['id'])
        body = f'<figure><img src="/{record["path"]}?w=900"><figcaption>Notice originale</figcaption></figure>'
        doc, selected = self.render_page('antigone', 'Antigone', body)
        self.assertEqual([], selected)
        self.assertEqual(1, len(doc.select('img')))
        self.assertEqual('Notice originale', doc.figcaption.get_text())

    def test_legacy_wordpress_and_commons_images_not_duplicated(self):
        record = next(r for r in self.records if 'derveni-papyrus' in r['id'])
        urls = ['https://bobmythos.wordpress.com/wp-content/uploads/' + record['path'].removeprefix('media/') + '?w=400', record['equivalents'][0].replace('/wiki/File:', '/wiki/Special:FilePath/')]
        for url in urls:
            _, selected = self.render_page('derveni', 'Derveni', f'<img src="{url}">')
            self.assertNotIn(record['id'], selected)

    def test_migration_idempotent_preserves_manuscript_and_notes(self):
        legacy = '<aside class="mythos-home-illustrations">Derveni</aside><aside class="mythos-visual-rail">Ounas</aside>'
        body = '<p>Texte intégral avec <em>philologie</em>.</p><table><tr><td>42</td></tr></table><aside>Note universitaire</aside>'
        doc, selected = self.render_page('antigone', 'Antigone', body, legacy)
        self.assertEqual(1, len(doc.select('main > aside')))
        self.assertEqual('Note universitaire', doc.article.aside.get_text())
        self.assertEqual('42', doc.article.td.get_text())
        again, other_selected = illustrations.decorate_document(str(doc), Path('antigone/index.html'), ROOT, self.records)
        self.assertEqual(str(doc), again)
        self.assertEqual(selected, other_selected)

    def test_navigation_changes_not_overwritten_by_stale_html(self):
        import build_navigation
        from unittest.mock import patch
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<html><nav>Ancien menu</nav><main><article><h1>Inde</h1><p>Texte intact</p></article></main></html>')
            with patch.object(build_navigation, 'OUT', root):
                build_navigation.apply_navigation()
            result = (root / 'index.html').read_text()
            self.assertIn('Encyclopédie grecque', result)
            self.assertNotIn('Ancien menu', result)
            self.assertIn('Texte intact', result)

    def test_navigation_covers_do_not_inherit_collection_or_default(self):
        from apply_museum_design import picture, cover
        for url in ('/chapitres/origines-du-sacre/471-inde-yuga-calendriers/', '/chapitres/origines-du-sacre/462-egypte-sistre-hathor/', '/civilisations/asie/', '/inconnu/'):
            self.assertIsNone(picture(url, ROOT))
            self.assertEqual('', cover(url, ROOT))
        self.assertIn('epidaure', picture('/theatre/', ROOT))
        with TemporaryDirectory() as tmp:
            self.assertIsNone(picture('/theatre/', Path(tmp)))


if __name__ == '__main__':
    unittest.main()
