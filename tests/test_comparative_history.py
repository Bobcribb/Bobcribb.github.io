import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import comparative_history as history
from build_native import render, markdown
from bs4 import BeautifulSoup
from test_editorial_queue import initialize, request
from editorial_queue import apply, REGISTRY

ROOT = Path(__file__).resolve().parents[1]


class HistoryTests(unittest.TestCase):
    def test_only_title_identity_not_cross_reference(self):
        self.assertIsNone(history.historical_id('# Étude du destin\n\n## Présentation\n\nVoir MC-025.\n## Dialogue avec MC-025'))
        self.assertEqual(history.historical_id('# Volume I\n## MC‑25 — Maât'), 'MC-025')
        self.assertEqual(history.historical_id('# MC-025 — Maât'), 'MC-025')

    def test_real_sources_and_canonical_numbers(self):
        data = history.validate(ROOT)
        members = data['groups']['MC-025']['members']
        self.assertEqual([m['number'] for m in members], [183,187,189])
        self.assertEqual([m['role'] for m in members], ['primary','complement','complement'])

    def test_unregistered_duplicate_in_batch_is_atomic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            initialize(root)
            for slug in ('texte-a','texte-b'):
                request(root,slug,'comparatif',body='# Volume {{volume}}\n\n## MC-099 — Sujet\n\nContenu différent.')
            before = (root/REGISTRY).read_bytes()
            with self.assertRaisesRegex(ValueError, 'Collision d’identifiant historique'):
                apply(root)
            self.assertEqual((root/REGISTRY).read_bytes(), before)
            self.assertEqual(list((root/'chapitres/comparatif').glob('*.md')), [])
            self.assertEqual(len(list((root/'editorial/inbox').glob('*.json'))), 2)

    def test_duplicate_identity_already_published_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            initialize(root)
            request(root,'premier','comparatif',body='# Volume {{volume}}\n\n## MC-099 — Sujet\n\nTexte.')
            apply(root)
            request(root,'autre','comparatif',body='# Volume {{volume}}\n\n## MC-099 — Autre titre\n\nAutre texte.')
            before = (root/REGISTRY).read_bytes()
            with self.assertRaisesRegex(ValueError, 'Collision d’identifiant historique'):
                apply(root)
            self.assertEqual((root/REGISTRY).read_bytes(), before)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.data = history.load(ROOT)
        for name in ('editorial/numbering.json','editorial/mc-025-notice.md',str(history.REGISTRY)):
            p = self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,p)
        self.members = self.data['groups']['MC-025']['members']
        for m in self.members:
            p=self.root/m['source'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/m['source'],p)
        self.out = self.root/'_site'
        self.collections = {'comparatif':[dict(m, url=history.url(m),title='ancien titre') for m in self.members]}
        self.chapters = [dict(url=history.url(m),title='ancien titre',excerpt='ancien extrait') for m in self.members]

    def tearDown(self):
        self.tmp.cleanup()

    def test_protected_manuscript_mutation_rejected(self):
        p=self.root/self.members[0]['source'];p.write_text(p.read_text()+'\nModification')
        with self.assertRaisesRegex(ValueError,'protégé altéré'): history.validate(self.root)

    def test_canonical_number_mutation_rejected(self):
        self.data['groups']['MC-025']['members'][0]['number']=200
        (self.root/history.REGISTRY).write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError,'canonique historique altéré'): history.validate(self.root)

    def test_two_primary_entries_rejected(self):
        self.data['groups']['MC-025']['members'][1]['role']='primary'
        (self.root/history.REGISTRY).write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError,'Une référence'): history.validate(self.root)

    def test_duplicate_025_with_different_slug_rejected(self):
        pending=[(Path('chapitres/comparatif/volume-cc-different.md'),b'# Volume CC\n\n## MC-025 -- Autre titre\n')]
        with self.assertRaisesRegex(ValueError,'Collision'): history.validate(self.root,pending)

    def test_same_subject_without_historical_id_rejected(self):
        pending=[(Path('chapitres/comparatif/volume-cc-different.md'),'# Volume CC\n\n## Isfet et Maât : études\n'.encode())]
        with self.assertRaisesRegex(ValueError,'Sujet historique déjà traité'): history.validate(self.root,pending)

    def test_body_citation_is_not_subject_collision(self):
        pending=[(Path('chapitres/comparatif/volume-cc-destin.md'),'# Volume CC\n\n## MC-030 — Destin\n\nVoir Maât et Isfet, MC-025.'.encode())]
        history.validate(self.root,pending)

    def render(self):
        for m in self.members:
            p=self.out/history.url(m).strip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(render('Titre',markdown((self.root/m['source']).read_text())))
        for portal in ('mythologie-comparee','philosophie','collections-numerotees'):
            p=self.out/portal/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(render(portal,'<h1>'+portal+'</h1><section id="numerotation-comparatif"></section>'))
        prior=self.out/'chapitres/comparatif/volume-clxxxi-amon-re-aton-akhenaton-unite-divine-pouvoir-royal/index.html'
        prior.parent.mkdir(parents=True,exist_ok=True);prior.write_text(render('MC-024','<h1>Aton</h1>'))
        history.annotate(self.root,self.collections,self.chapters)
        history.install(self.root,self.out)
        guide=self.data['groups']['MC-025']['guide_url']
        entries=self.chapters+[dict(url=guide,title='Notice comparée')]
        (self.out/'search.json').write_text(json.dumps(entries))
        (self.out/'catalog/entries.json').write_text(json.dumps({'entries':entries}))
        (self.out/'catalog/numbering.json').write_text(json.dumps({'collections':self.collections}))
        (self.out/'sitemap.xml').write_text('\n'.join('https://bobmythos.fr'+e['url'] for e in entries))

    def test_full_render_preserves_all_blocks_and_links_idempotently(self):
        self.render()
        history.install(self.root,self.out)
        self.assertEqual(history.verify(self.root,self.out)['protected_manuscripts'],3)
        for m in self.members:
            doc=BeautifulSoup((self.out/history.url(m).strip('/')/'index.html').read_text(),'html.parser')
            self.assertEqual(len(doc.select('aside[data-mc-history]')),1)
            self.assertEqual(hashlib.sha256((self.root/m['source']).read_bytes()).hexdigest(),m['sha256'])

    def test_live_content_check_rejects_stale_complement(self):
        from verify_live_site import verify_public_history
        self.render()
        stale = history.url(self.members[1])
        def fetch(address):
            path = address.removeprefix('https://bobmythos.fr')
            p = self.out/path.lstrip('/')
            if path.endswith('/'): p /= 'index.html'
            content = p.read_bytes()
            if path == stale: content = b'<html>Ancienne livraison MC-025</html>'
            return 200, 'text/html', content
        with patch('verify_live_site.fetch', side_effect=fetch):
            results = verify_public_history('https://bobmythos.fr', self.out)
        self.assertEqual([r['url'] for r in results if not r['valid']], [stale])

    def test_bibliography_loss_in_render_is_detected(self):
        self.render()
        p=self.out/history.url(self.members[0]).strip('/')/'index.html'
        doc=BeautifulSoup(p.read_text(),'html.parser')
        doc.find('span',id='mc025-bibliographie').find_next('ol').decompose()
        p.write_text(str(doc))
        with self.assertRaisesRegex(AssertionError,'Texte perdu'): history.verify(self.root,self.out)

    def test_invalid_deep_link_is_detected(self):
        self.render()
        p=self.out/self.data['groups']['MC-025']['guide_url'].strip('/')/'index.html'
        p.write_text(p.read_text().replace('#mc025-ptahhotep','#absent'))
        with self.assertRaisesRegex(AssertionError,'absent'): history.verify(self.root,self.out)

    def test_search_complement_mislabel_is_detected(self):
        self.render()
        p=self.out/'search.json';data=json.loads(p.read_text());data[1]['historical_role']='primary';p.write_text(json.dumps(data))
        with self.assertRaises(AssertionError): history.verify(self.root,self.out)


if __name__=='__main__': unittest.main()
