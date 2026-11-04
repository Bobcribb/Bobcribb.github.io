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

    def test_no_false_author_from_article_prose(self):
        doc=self.document();doc.p.string='Nietzsche et Hegel commentent des mythes.'
        entry=metadata({'url':'/sources/','title':'Sources anciennes','excerpt':''},doc)
        self.assertEqual(entry['authors'],[])
        self.assertEqual(norm('Œdipe et Hésiode'),'oedipe et hesiode')


if __name__=='__main__':unittest.main()
