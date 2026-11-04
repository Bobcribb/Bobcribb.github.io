"""Regression cases for the reported mismatches and regenerated HTML."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup
import mistune

import editorial_illustrations as illustrations

ROOT = Path(__file__).resolve().parents[1]
HATHOR_IMAGES = ['mythos-met-550893-hathor-sistre-arque', 'mythos-met-543897-hathor-sistre-teti']


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
                expected = HATHOR_IMAGES if 'hathor' in slug else []
                self.assertEqual(selected, expected)
                illustrations_found = after.select('main > aside figure, article figure[data-editorial-inline="subject-v3"]')
                self.assertEqual(len(illustrations_found), len(expected))
                # Compare authored content only: the checked-in HTML may
                # already include a previously generated subject-v3 figure.
                # A rebuild must replace that figure, not preserve it as prose.
                for doc in (before, after):
                    for figure in doc.select('article figure[data-editorial-inline="subject-v3"]'):
                        figure.decompose()
                self.assertEqual(str(before.article), str(after.article))
                self.assertNotIn('visual-rails-active', after.main.get('class', []))

    def test_fresh_markdown_chapter_gets_same_selection(self):
        for slug in ('471-inde-yuga-calendriers', '462-egypte-sistre-hathor'):
            manuscript = ROOT / 'chapitres/origines-du-sacre' / (slug + '.md')
            source = '<html><head></head><body><main><article>' + mistune.html(manuscript.read_text()) + '</article></main></body></html>'
            _, selected = illustrations.decorate_document(source, Path(slug) / 'index.html', ROOT, self.records)
            self.assertEqual(HATHOR_IMAGES if 'hathor' in slug else [], selected)

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
                if title == 'Maât':
                    allowed_extras.add('mythos-met-544093-thot-ibis-plume-maat')
                    allowed_extras.update({'mythos-met-551794-maat-faience-bleue', 'mythos-met-570207-maat-buste-offrande'})
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
        self.assertEqual(6, len(selected))
        self.assertTrue({'mythos-medee-fuite-char-serpents-hydrie-policoro-35296', 'mythos-van-loo-medee-jason', 'mythos-euripide-portrait-antique-szilas'} <= set(selected))
        self.assertTrue(all('medee' in key or 'euripide-portrait' in key for key in selected))

    def test_enriched_iliad_keeps_ancient_documents_and_adds_modern_reception(self):
        doc, selected = self.render_page('iliade', 'Iliade')
        self.assertEqual(5, len(selected))
        self.assertEqual(5, len(set(selected)))
        self.assertIn('mythos-papyrus-oxyrhynchus-20-iliade-ii', selected)
        self.assertIn('mythos-met-341681-achille-ombre-patrocle-flaxman', selected)
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

    def test_museum_documents_match_named_subjects(self):
        for title, object_id in [('Anubis', 570675), ('Sekhmet', 544486), ('Gudéa', 329072), ('Nimrud', 322608), ('Niké', 247903), ('Aristophane, Les Cavaliers', 844483)]:
            with self.subTest(title=title):
                doc, selected = self.render_page('nouveau-chapitre', title)
                self.assertTrue(any(f'met-{object_id}-' in key for key in selected))
                for img in doc.select('aside img[src^="/assets/illustrations-articles/"]'):
                    self.assertGreater(int(img['width']), 0)
                    self.assertGreater(int(img['height']), 0)

    def test_museum_original_url_is_not_repeated(self):
        record = next(r for r in self.records if 'met-570675-' in r['id'])
        _, selected = self.render_page('anubis', 'Anubis', f'<img src="{record["equivalents"][0]}">')
        self.assertEqual([], selected)

    def test_museum_assets_have_matching_provenance_and_hashes(self):
        import hashlib, json
        manifest = json.loads((ROOT / 'assets/illustrations-articles/sources-met.json').read_text())
        self.assertEqual(manifest['count'], len(manifest['images']))
        for item in manifest['images']:
            record = next(r for r in self.records if r['id'] == item['id'])
            self.assertEqual(record['path'], item['path'])
            self.assertTrue(item['is_public_domain'])
            self.assertEqual('CC0-1.0', item['license'])
            self.assertIn(item['source_url'], record['caption_html'])
            self.assertEqual(item['sha256'], hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest())

    def test_euripides_portrait_has_photographer_rights_and_integrity(self):
        import hashlib
        record = next(r for r in self.records if r['id'] == 'mythos-euripide-portrait-antique-szilas')
        self.assertEqual('Szilas', record['provenance']['photographer'])
        self.assertEqual('PD-self', record['provenance']['license'])
        self.assertIn(record['source_url'], record['caption_html'])
        self.assertEqual(record['provenance']['sha256'], hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest())
        _, selected = self.render_page('une-piece-perdue', 'Euripide — Alcméon à Corinthe')
        self.assertIn(record['id'], selected)
        _, selected = self.render_page('calendriers', 'Calendriers', '<p>Un parallèle chez Euripide.</p>')
        self.assertNotIn(record['id'], selected)

    def test_large_gallery_remains_bounded_and_idempotent(self):
        doc, selected = self.render_page('etude-comparee', 'Euripide, Médée, Iphigénie et Oreste', '<p>Étude conservée.</p>')
        self.assertEqual(12, len(selected))
        self.assertEqual(12, len(set(selected)))
        again, other = illustrations.decorate_document(str(doc), Path('etude-comparee/index.html'), ROOT, self.records)
        self.assertEqual(str(doc), again)
        self.assertEqual(selected, other)
        self.assertEqual('Étude conservée.', doc.article.p.get_text())

    def test_long_article_distributes_documented_images_in_reading_flow(self):
        prose = "Une étude universitaire conserve ses sources antiques et ses variantes philologiques. " * 6
        body = "".join(f"<h2>Partie {i}</h2><p>{prose}</p>" for i in range(14))
        doc, selected = self.render_page('dossier-heracles', 'Héraclès', body)
        inline = doc.select('article figure[data-editorial-inline="subject-v3"]')
        supplementary = doc.select('main > aside figure')
        self.assertGreaterEqual(len(selected), 2)
        self.assertEqual(min(4, len(selected)), len(inline))
        self.assertEqual(len(selected), len(inline) + len(supplementary))
        self.assertEqual(14, len(doc.article.select('h2')))
        self.assertEqual(14, len(doc.article.select('p')))
        for figure in inline + supplementary:
            self.assertTrue(figure.img.get('alt'))
            self.assertTrue(figure.select('figcaption a[href^="https://"]'))
            self.assertNotIn('.svg', figure.img['src'])
        again, other = illustrations.decorate_document(str(doc), Path('dossier-heracles/index.html'), ROOT, self.records)
        self.assertEqual(selected, other)
        self.assertEqual(str(doc), again)

    def test_inline_does_not_replace_authored_figure(self):
        prose = "<p>" + ("Texte original documenté. " * 12) + "</p>"
        existing = '<figure><img src="/media/2026/10/photo-auteur.jpg" alt="Document original"><figcaption>Notice de l’auteur</figcaption></figure>'
        doc, selected = self.render_page('dossier-athena', 'Athéna', existing + prose * 8)
        self.assertTrue(selected)
        self.assertEqual(1, len(doc.select('article figure:not([data-editorial-inline])')))
        self.assertEqual('Notice de l’auteur', doc.select_one('article figure:not([data-editorial-inline]) figcaption').get_text())
        self.assertGreaterEqual(len(doc.select('article figure[data-editorial-inline]')), 1)

    def test_photorealistic_panorama_has_explicit_provenance_and_warning(self):
        reconstructions = [r for r in self.records if r['id'].startswith('mythos-reconstitution-')]
        self.assertEqual(23, len(reconstructions))
        self.assertEqual(23, len({r['path'] for r in reconstructions}))
        for r in reconstructions:
            self.assertTrue(r['path'].endswith('.webp'))
            self.assertTrue((ROOT / r['path']).is_file())
            self.assertIn('hypothèse', r['caption_html'])
            self.assertIn('Degré de certitude', r['caption_html'])
            self.assertIn('Référence archéologique', r['caption_html'])
            self.assertNotIn('2,5D', r['caption_html'])
        page, selected = self.render_page('delphes', 'Delphes')
        self.assertTrue(any('mythos-reconstitution-delphes-' in key for key in selected))
        self.assertTrue(page.select('figure figcaption a[href^="https://"]'))
        _, other = self.render_page('héra', 'Héra')
        self.assertFalse(any('mythos-reconstitution-samos-' in key for key in other))

    def test_long_article_receives_eight_inline_figures_not_just_a_bottom_rail(self):
        prose = '<p>' + ('Un document archéologique est distinct de ses interprétations et des hypothèses. ' * 6) + '</p>'
        body = ''.join(f'<h2>Partie {i}</h2>{prose}' for i in range(24))
        doc, selected = self.render_page('cycle-dramatique', 'Euripide, Médée, Iphigénie et Oreste', body)
        self.assertEqual(12, len(selected))
        self.assertEqual(8, len(doc.select('article figure[data-editorial-inline="subject-v3"]')))
        self.assertEqual(4, len(doc.select('main > aside figure')))
        self.assertEqual(24, len(doc.article.select('p')))
        self.assertEqual(24, len(doc.article.select('h2')))
        again, selected_again = illustrations.decorate_document(str(doc), Path('cycle-dramatique/index.html'), ROOT, self.records)
        self.assertEqual(selected, selected_again)
        self.assertEqual(str(doc), again)

    def test_named_scholarly_section_can_be_illustrated_without_unrelated_article_fallback(self):
        prose = '<p>' + ('Les fragments matériels attestés doivent être distingués des rapprochements interprétatifs. ' * 5) + '</p>'
        body = '<h2>Les images d’Isis et d’Horus</h2>' + prose + '<h2>Étude philologique</h2>' + prose
        doc, selected = self.render_page('chapitres/comparatif/volume-experimentation', 'Étude des pratiques rituelles', body)
        self.assertTrue(any('isis' in key for key in selected))
        self.assertEqual(1, len(doc.select('article figure[data-editorial-inline="subject-v3"]')))
        self.assertLess(str(doc).index('Les images d’Isis'), str(doc).index('mythos-editorial-inline'))
        unrelated, selected_unrelated = self.render_page('chapitres/comparatif/volume-chronologies', 'Calendriers de l’Inde',
                                                        '<h2>Comparaison avec Derveni</h2>' + prose)
        self.assertEqual([], selected_unrelated)
        self.assertFalse(unrelated.select('figure[data-editorial-inline]'))

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
