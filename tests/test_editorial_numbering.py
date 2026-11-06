"""Regression cases for publication identity and permanent incoming links."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from editorial_numbering import scan, canonical_link, relabel


class NumberingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'EDITORIAL_NUMBERING.json').write_text(json.dumps({'version':1,'renumbered':[]}))
        (self.root/'EDITORIAL_REDIRECTS.json').write_text('{"redirects":{}}')
        self.source('comedies/volume-003-eupolis-heilotes.md','# Volume III\n## Heilôtes')

    def source(self,name,content):
        path=self.root/'chapitres'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)

    def test_different_titles_cannot_share_a_number(self):
        self.source('encyclopedie/chapitre-353-daphne.md','# Chapitre 353\n## Daphné')
        self.source('encyclopedie/chapitre-353-pindare.md','# Chapitre 353\n## Pindare')
        with self.assertRaisesRegex(ValueError,'Doublon éditorial'):scan(self.root)

    def test_collections_have_independent_sequences(self):
        self.source('tragedies/volume-clxviii-hypsipyle.md','# Volume CLXVIII (168)\n## Hypsipyle')
        self.source('comparatif/volume-clxviii-auteur.md','# Volume CLXVIII (168)\n## Auteur')
        self.assertEqual(len(scan(self.root)),3)

    def test_chapter_titles_do_not_repeat_their_canonical_number(self):
        # The title belongs to the manuscript, but the index is numbered once.
        self.source('encyclopedie/chapitre-433-athena-lindia.md',
                    '# Chapitre 433 — Athéna Lindia : la Chronique de Lindos\n## Résumé')
        self.source('encyclopedie/chapitre-438-athena-lindia.md',
                    '# MYTHOS — Encyclopédie de la mythologie grecque — Chapitre 438\n'
                    '## Athéna Lindia et la Chronique de Lindos')
        self.source('origines-du-sacre/500-objets-sacres.md',
                    '# Chapitre 500 : Objets sacrés et offrandes')
        self.source('encyclopedie/chapitre-359-chiron.md',
                    '# Chapitre 359\n## Chiron et l’éducation des héros')
        records = scan(self.root)
        titles = {e['number']: e['title'] for e in records['encyclopedie']}
        self.assertEqual(titles[433],
                         'Chapitre 433 — Athéna Lindia : la Chronique de Lindos')
        self.assertEqual(titles[359], 'Chapitre 359 — Chiron et l’éducation des héros')
        self.assertEqual(titles[438],
                         'Chapitre 438 — Athéna Lindia et la Chronique de Lindos')
        self.assertEqual(records['origines-du-sacre'][0]['title'],
                         'Chapitre 500 — Objets sacrés et offrandes')

    def test_mismatched_title_is_rejected(self):
        self.source('tragedies/volume-clxviii-hypsipyle.md','# Volume CLXVII (167)\n## Hypsipyle')
        with self.assertRaisesRegex(ValueError,'titre'):scan(self.root)

    def test_only_named_historical_alias_is_exempt(self):
        self.source('comedies/volume-002-eupolis-chrysoun-genos.md','# Volume II\n## Chrysoun genos')
        self.source('comedies/volume-002-eupolis-heilotes.md','# Ancienne adresse\nNotice de redirection')
        self.assertEqual(len(scan(self.root)['comedies']),2)
        self.source('comedies/volume-002-autre.md','# Volume II\n## Autre')
        with self.assertRaisesRegex(ValueError,'Doublon'):scan(self.root)

    def test_relative_and_absolute_links_preserve_query_and_fragment(self):
        old='/chapitres/tragedies/volume-clxviii-euripide-archelaos/'
        new='/chapitres/tragedies/volume-cxcix-euripide-archelaos/'
        for href in ['../volume-clxviii-euripide-archelaos/?x=1#sources',old+'index.html?x=1#sources','https://bobmythos.fr'+old+'?x=1#sources','../volume-clxviii-euripide-archelaos.md?x=1#sources']:
            self.assertEqual(canonical_link(href,'/chapitres/tragedies/autre/index.html',{old:new}),(new+'?x=1#sources',old))
        external='https://example.org'+old
        self.assertEqual(canonical_link(external,'/',{old:new}),(external,None))

    def test_link_label_does_not_change_verse_numbers(self):
        m={'collection':'tragedies','old_number':168,'number':199,'old_roman':'CLXVIII','roman':'CXCIX'}
        self.assertEqual(relabel('Volume CLXVIII (168) — vers 168–199',m),'Volume CXCIX (199) — vers 168–199')


if __name__=='__main__':unittest.main()
