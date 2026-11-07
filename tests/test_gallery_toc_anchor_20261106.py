"""Contrôle du sommaire de la galerie photoréaliste après ajouts concurrents."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / 'reconstitutions-photorealistes.html'


class GalleryTOCAnchorTests(unittest.TestCase):
    def test_all_gallery_section_links_target_existing_numbered_sections(self):
        text = GALLERY.read_text(encoding='utf-8')
        self.assertNotIn('{LECTURE_INDEX}', text)
        doc = BeautifulSoup(text, 'html.parser')
        ids = {node['id'] for node in doc.select('[id]')}
        # Ne pas compter le lien de fin de page « Revenir au début ».
        targets = [a['href'][1:] for a in doc.select(
            'details.mythos-gallery-toc ol a[href^="#lecture-section-"]')]
        self.assertGreaterEqual(len(targets), 82)
        self.assertEqual(len(targets), len(set(targets)))
        section_ids = {name for name in ids
                       if name.startswith('lecture-section-')
                       and name[len('lecture-section-'):].isdigit()}
        # Une nouvelle section peut preceder le sommaire HTML source :
        # le lecteur final sera reconstruit et controlé plus bas.
        self.assertLessEqual(len(targets), len(section_ids))
        for anchor in targets:
            with self.subTest(target=anchor):
                self.assertIn(anchor, ids)

    def test_final_reader_rebuilds_complete_toc_for_new_3d_notice(self):
        """Une section ajoutée pendant une publication reste atteignable après build."""
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from improve_reading import add_reading

        doc = BeautifulSoup(GALLERY.read_text(encoding='utf-8'), 'html.parser')
        before_sources = [
            p.get_text(' ', strip=True)
            for p in doc.select('article.r3d-card .r3d-science p')
        ]
        holder = doc.main.select_one('article.content') or doc.main
        self.assertIsNotNone(holder)
        probe = BeautifulSoup(
            '<article class="r3d-card" id="test-nouvelle-notice">'
            '<figure><figcaption><strong>Site-test — ajout concurrent</strong>'
            '</figcaption></figure>'
            '<div class="r3d-science"><h2 id="lecture-section-9999">'
            'Commentaire scientifique</h2>'
            '<p>Texte scientifique témoin, conservé sans résumé.</p></div>'
            '</article>', 'html.parser').article
        holder.append(probe)
        # Le sommaire préexistant ne contient délibérément pas la 9999.
        self.assertNotIn('#lecture-section-9999', [
            a['href'] for a in doc.select('details.mythos-gallery-toc a[href]')])
        source_sections = [h['id'] for h in holder.select('h2')
                           if not h.find_parent(['nav', 'aside'])
                           and not h.find_parent(class_='toc')]
        entry = {'words': 10000, 'minutes': 150}
        add_reading(doc, '/reconstitutions-photorealistes.html', entry)
        toc = doc.select_one('details.mythos-gallery-toc')
        self.assertIsNotNone(toc)
        targets = [a['href'][1:] for a in toc.select('ol > li > a')]
        self.assertEqual(targets, source_sections)
        self.assertEqual(len(targets), len(set(targets)))
        self.assertEqual(len(doc.select('details.mythos-gallery-toc')), 1)
        self.assertTrue(all(doc.find(id=anchor) for anchor in targets))
        self.assertIn('Site-test — ajout concurrent', toc.get_text(' ', strip=True))
        self.assertEqual(before_sources, [
            p.get_text(' ', strip=True)
            for p in doc.select('article.r3d-card .r3d-science p')[:-1]
        ])
        # Une seconde génération n'ajoute ni copie de la notice ni liens doubles.
        add_reading(doc, '/reconstitutions-photorealistes.html', entry)
        self.assertEqual(len(doc.select('details.mythos-gallery-toc')), 1)
        self.assertEqual(len(doc.select('details.mythos-gallery-toc ol > li')), len(source_sections))


    def test_reciprocal_gallery_links_are_accessible_and_idempotent(self):
        """Un retour au sommaire par notice sans modifier les sources."""
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from improve_reading import add_reading

        doc = BeautifulSoup(GALLERY.read_text(encoding='utf-8'), 'html.parser')
        paragraphs_before = [
            p.get_text(' ', strip=True)
            for p in doc.select('article.r3d-card .r3d-science p')
        ]
        images_before = [
            (im.get('src'), im.get('alt'))
            for im in doc.select('article.r3d-card img')
        ]
        entry = {'words': 10000, 'minutes': 150}
        add_reading(doc, '/reconstitutions-photorealistes.html', entry)
        toc = doc.select_one('details#sommaire-reconstitutions.mythos-gallery-toc')
        self.assertIsNotNone(toc)
        eligible = [
            card for card in doc.select('article.r3d-card')
            if card.select_one('.r3d-science h2') is not None
        ]
        self.assertGreaterEqual(len(eligible), 82)
        for card in eligible:
            with self.subTest(card=card.get('id')):
                links = card.select(
                    '.mythos-gallery-backtoc[data-reading-owned="true"]'
                    ' a[href="#sommaire-reconstitutions"]')
                self.assertEqual(len(links), 1)
                self.assertIn('Revenir au sommaire', links[0].get_text())
        self.assertEqual(len(doc.select('.mythos-gallery-backtoc')), len(eligible))
        self.assertEqual(
            paragraphs_before,
            [p.get_text(' ', strip=True)
             for p in doc.select('article.r3d-card .r3d-science p')])
        self.assertEqual(
            images_before,
            [(im.get('src'), im.get('alt'))
             for im in doc.select('article.r3d-card img')])

        # Même résultat après une deuxième passe : ni section ni renvoi doublés.
        add_reading(doc, '/reconstitutions-photorealistes.html', entry)
        self.assertEqual(len(doc.select('details#sommaire-reconstitutions')), 1)
        self.assertEqual(len(doc.select('.mythos-gallery-backtoc')), len(eligible))
        self.assertEqual(
            [p.get_text(' ', strip=True)
             for p in doc.select('article.r3d-card .r3d-science p')],
            paragraphs_before)

    def test_non_gallery_reader_has_no_reconstruction_backlinks(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from improve_reading import add_reading

        doc = BeautifulSoup(
            '<html><body><main><article class="content">'
            '<h2>Section A</h2><p>Texte intégral.</p>'
            '<h2>Section B</h2><p>Notes philologiques.</p>'
            '<h2>Section C</h2><p>Bibliographie.</p>'
            '</article></main></body></html>', 'html.parser')
        add_reading(doc, '/philosophie/etude-test/',
                    {'words': 10000, 'minutes': 150})
        self.assertFalse(doc.select('.mythos-gallery-backtoc'))
        self.assertFalse(doc.select('#sommaire-reconstitutions'))
        self.assertEqual(len(doc.select('.mythos-reading-toc')), 1)

    def test_final_reader_refuses_duplicate_scientific_anchors(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from improve_reading import add_reading
        doc = BeautifulSoup(GALLERY.read_text(encoding='utf-8'), 'html.parser')
        headings = doc.select('article.r3d-card h2[id]')
        self.assertGreaterEqual(len(headings), 82)
        headings[-1]['id'] = headings[0]['id']
        with self.assertRaisesRegex(RuntimeError, 'Sommaire 3D'):
            add_reading(doc, '/reconstitutions-photorealistes.html',
                        {'words': 10000, 'minutes': 150})

    def test_metaponte_toc_and_actual_76_section_stay_connected(self):
        doc = BeautifulSoup(GALLERY.read_text(encoding='utf-8'), 'html.parser')
        section = doc.find(id='lecture-section-76')
        self.assertIsNotNone(section)
        matching = [link for link in doc.select('a[href="#lecture-section-76"]')
                    if 'Métaponte' in link.get_text(' ', strip=True)]
        self.assertEqual(len(matching), 1)
        akragas = [link for link in doc.select('a[href="#lecture-section-75"]')
                   if 'Akragas' in link.get_text(' ', strip=True)]
        self.assertEqual(len(akragas), 1)
        # Aucune entrée Akragas répétée dans le sommaire historique.
        toc = doc.select('details.mythos-gallery-toc ol li')
        sections = [node for node in doc.select('[id]')
                    if node['id'].startswith('lecture-section-')
                    and node['id'][len('lecture-section-'):].isdigit()]
        self.assertLessEqual(len(toc), len(sections))
        self.assertIsNotNone(doc.find(id='lecture-section-75'))


if __name__ == '__main__':
    unittest.main()
