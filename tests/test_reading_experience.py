"""Regression tests for preservation, identifiers and the new reading routes."""
from pathlib import Path
import sys
import tempfile
import unittest

from bs4 import BeautifulSoup
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from improve_reading import add_reading, metadata, epic_links, norm, audit


class ReadingTests(unittest.TestCase):
    def document(self):
        return BeautifulSoup('<html><head><title>Iliade</title></head><body><main><article class="content"><h1>Homère, Iliade</h1><p>'+('Une analyse préservée. '*180)+'</p><h2 id="ancien">Première partie</h2><p>Texte grec : μῆνιν.</p><h2>Deuxième partie</h2><blockquote>Une citation conservée.</blockquote><h2>Troisième partie</h2><a href="#ancien">Renvoi ancien</a></article></main></body></html>','html.parser')

    def test_reading_controls_preserve_prose_and_old_anchors_on_repeated_builds(self):
        doc=self.document();before=[p.get_text() for p in doc.select('article>p,article>blockquote')]
        entry=metadata({'url':'/iliade/','title':'Homère, Iliade','excerpt':'Étude'},doc)
        add_reading(doc,'/iliade/',entry);first=[h['id'] for h in doc.select('h2')]
        add_reading(doc,'/iliade/',entry)
        self.assertEqual(first,[h['id'] for h in doc.select('h2')])
        self.assertEqual(1,len(doc.select('.mythos-reader')))
        self.assertEqual(1,len(doc.select('.mythos-reading-toc')))
        self.assertEqual(before,[p.get_text() for p in doc.select('article>p,article>blockquote')])
        self.assertIsNotNone(doc.find(id='ancien'))
        for link in doc.select('.mythos-reading-toc a'):self.assertIsNotNone(doc.find(id=link['href'][1:]))

    def test_generated_museum_toc_does_not_appear_as_lost_authored_text(self):
        from apply_museum_design import add_scholarly_toc
        from improve_reading import authored_blocks
        doc = self.document()
        add_scholarly_toc(doc, doc.main,
                          'chapitres/encyclopedie/chapitre-259-helios/index.html')
        self.assertIsNotNone(doc.select_one('nav.mythos-scholarly-toc'))
        before = authored_blocks(doc)
        entry = metadata({'url': '/chapitres/encyclopedie/chapitre-259-helios/',
                          'title': 'Hélios', 'excerpt': 'Source'}, doc)
        add_reading(doc, '/chapitres/encyclopedie/chapitre-259-helios/', entry)
        self.assertIsNone(doc.select_one('nav.mythos-scholarly-toc'))
        self.assertEqual(before, authored_blocks(doc))
        self.assertEqual(1, len(doc.select('.mythos-reading-toc')))
        doc.select_one('article.content p').decompose()
        self.assertNotEqual(before, authored_blocks(doc))

    def test_gallery_toc_identifies_each_monument_without_rewriting_scientific_text(self):
        names = ['Delphes — sanctuaire d’Apollon', 'Athènes — l’Acropole',
                 'Olympie — temple de Zeus']
        cards = ''.join(
            '<article class="r3d-card" id="site-'+str(i)+'">'
            '<figure><figcaption><strong>'+name+'</strong></figcaption></figure>'
            '<div class="r3d-science"><h2>Commentaire scientifique</h2>'
            '<p>Sources archéologiques et degré de certitude.</p></div></article>'
            for i, name in enumerate(names, 1)
        )
        doc = BeautifulSoup(
            '<html><body><main><p>'+('Texte introductif. '*500)+'</p>'
            '<section class="r3d-grid">'+cards+'</section></main></body></html>',
            'html.parser'
        )
        original = [p.get_text(' ', strip=True) for p in doc.select('.r3d-science p')]
        for _ in range(2):
            add_reading(doc, '/reconstitutions-photorealistes.html',
                        {'words': 1000, 'minutes': 5})
        self.assertEqual(1, len(doc.select('.mythos-gallery-toc')))
        links = doc.select('.mythos-gallery-toc li a')
        self.assertEqual(len(names), len(links))
        for name, link in zip(names, links):
            self.assertEqual(name+' — Commentaire scientifique', link.get_text(' ', strip=True))
            self.assertIsNotNone(doc.find(id=link['href'][1:]))
        self.assertEqual(['Commentaire scientifique']*3,
                         [h.get_text(' ', strip=True) for h in doc.select('.r3d-science h2')])
        self.assertEqual(original,
                         [p.get_text(' ', strip=True) for p in doc.select('.r3d-science p')])

    def test_catalogue_ids_stable_when_title_changes_and_no_fake_review(self):
        doc=self.document()
        a=metadata({'url':'/iliade/','title':'Iliade','excerpt':''},doc)
        b=metadata({'url':'/iliade/','title':'L’Iliade, version révisée','excerpt':''},doc)
        self.assertEqual(a['id'],b['id'])
        self.assertEqual(a['scholarly_review'],'not_certified')
        self.assertEqual(a['works'],['Iliade'])
        self.assertIn('Grèce',a['civilizations'])

    def test_epic_sources_and_reciprocal_navigation_do_not_accumulate(self):
        doc=self.document()
        for _ in range(2):epic_links(doc,'/philosophie-iliade.html')
        self.assertEqual(len(doc.select('#sources-edition')),1)
        self.assertEqual(len(doc.select('.epic-links')),1)
        self.assertIsNotNone(doc.find('a',href='/iliade/'))
        self.assertIn('μῆνιν',doc.get_text())
        other=self.document();epic_links(other,'/iliade/')
        self.assertIsNotNone(other.find('a',href='/philosophie-iliade.html'))

    def test_inventory_can_link_its_own_audit_without_a_bootstrap_failure(self):
        import json
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            (root/'catalog').mkdir()
            (root/'catalog/entries.json').write_text(json.dumps({'entries':[{'id':'MYT-1','url':'/'}]}))
            (root/'index.html').write_text('<html><body><a href="/catalog/reading-audit.json">Audit</a></body></html>')
            result=audit(root)
            self.assertEqual(result['new_navigation_errors'],[])
            self.assertEqual(result['status'],'passed')

    def test_reindexed_article_keeps_its_excerpt_after_reading_controls_are_published(self):
        import json
        from unittest.mock import patch
        import build_native
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);out=root/'_site';out.mkdir()
            entries=[]
            for i in range(450):
                directory=out/('article-'+str(i));directory.mkdir()
                (directory/'index.html').write_text('<html><h1>Article</h1></html>')
                entries.append({'url':'/article-'+str(i)+'/', 'title':'Article', 'excerpt':'Texte'})
            (out/'search.json').write_text(json.dumps(entries))
            (out/'sanctuaire.html').write_text('<html><head><title>Sanctuaire</title></head><body><main><div data-reading-owned="true"><p>Lecture : environ 3 min</p></div><h1>Sanctuaire</h1><p>Le sanctuaire se trouve dans le Péloponnèse.</p></main></body></html>')
            with patch.object(build_native,'ROOT',root),patch.object(build_native,'OUT',out),patch('editorial_numbering.redirects',return_value={}):
                build_native.reindex([])
            article=next(e for e in json.loads((out/'search.json').read_text()) if e['url']=='/sanctuaire.html')
            self.assertEqual(article['excerpt'],'Le sanctuaire se trouve dans le Péloponnèse.')
            self.assertIn('data-reading-owned', (out/'sanctuaire.html').read_text())

    def test_no_false_author_from_article_prose(self):
        doc=self.document();doc.p.string='Nietzsche et Hegel commentent des mythes.'
        entry=metadata({'url':'/sources/','title':'Sources anciennes','excerpt':''},doc)
        self.assertEqual(entry['authors'],[])
        self.assertEqual(norm('Œdipe et Hésiode'),'oedipe et hesiode')


if __name__=='__main__':unittest.main()
