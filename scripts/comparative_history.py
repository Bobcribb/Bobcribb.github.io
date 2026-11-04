#!/usr/bin/env python3
"""Historical MC identities are distinct from canonical volume numbers.

Only explicitly reviewed complements share an identity. All original source
bytes are protected; editorial notices and display labels are derived separately.
"""
from collections import defaultdict, Counter
import hashlib
from html import escape
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup

REGISTRY = Path('editorial/comparative-history.json')
REPORT = Path('catalog/comparative-history.json')


def normalized(value):
    return ' '.join(value.split())


def folded(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value.casefold())
                   if unicodedata.category(c) != 'Mn')


def heading_text(raw):
    # Identity belongs to the title, never to body citations or reading links.
    titles = re.findall(r'^#{1,2}\s+(.+)$', raw, re.M)[:2]
    front_title = re.match(r'---\n[\s\S]*?\ntitle:\s*([^\n]+)', raw)
    return ' '.join(titles + ([front_title[1]] if front_title else []))


def historical_id(raw):
    ids = {f'MC-{int(n):03d}' for n in re.findall(
        r'\bMC[-\u2011\u2013 ]0*(\d+)\b', heading_text(raw), re.I)}
    if len(ids) > 1:
        raise ValueError('Plusieurs identifiants historiques dans un titre : '+str(sorted(ids)))
    return next(iter(ids), None)


def load(root):
    path = root / REGISTRY
    if not path.exists():
        return {'version': 1, 'groups': {}}
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('version') != 1 or not isinstance(data.get('groups'), dict):
        raise ValueError('Registre des identifiants historiques invalide')
    return data


def url(member):
    return '/' + Path(member['source']).with_suffix('').as_posix() + '/'


def display_title(key, member):
    from editorial_numbering import roman
    return (f"Volume {roman(member['number'])} ({member['number']}) — "
            f"{key} · {member['label']} — Maât et Isfet : {member['focus']}")


def validate(root, pending=()):
    """Validate existing and pending identities before any allocation or render."""
    root = Path(root)
    data = load(root)
    sources = {p.relative_to(root).as_posix(): p.read_bytes()
               for p in (root/'chapitres/comparatif').glob('*.md')}
    sources.update({p.as_posix(): content for p, content in pending
                    if p.parent == Path('chapitres/comparatif')})
    identities = defaultdict(set)
    for path, content in sources.items():
        key = historical_id(content.decode('utf-8'))
        if key:
            identities[key].add(path)
    numbering_file = root/'editorial/numbering.json'
    numbers = {}
    if numbering_file.exists():
        state = json.loads(numbering_file.read_text())['collections']['comparatif']
        numbers = dict(state['legacy'])
        numbers.update({e['path']:e['number'] for e in state['allocations'].values()})
    registered = set()
    for key, group in data['groups'].items():
        if not re.fullmatch(r'MC-\d{3,}', key):
            raise ValueError('Identifiant historique invalide : '+key)
        members = group['members']
        expected = {m['source'] for m in members}
        if len(expected) != len(members) or registered & expected:
            raise ValueError('Manuscrit enregistré plusieurs fois : '+key)
        registered.update(expected)
        if sum(m['role']=='primary' for m in members) != 1 or any(
                m['role'] not in ('primary','complement') for m in members):
            raise ValueError('Une référence historique principale requise : '+key)
        if identities[key] != expected:
            raise ValueError('Collision ou source historique manquante : '+key)
        if not (root/group['notice_source']).is_file():
            raise ValueError('Notice historique absente : '+key)
        tokens = group.get('subject_tokens', [])
        for path, content in sources.items():
            if tokens and all(token in folded(heading_text(content.decode('utf-8'))) for token in tokens) and path not in expected:
                raise ValueError('Sujet historique déjà traité ; réconciliation explicite requise : '+key+' ; '+path)
        for member in members:
            path = member['source']
            if numbers.get(path) != member['number']:
                raise ValueError('Numéro canonique historique altéré : '+path)
            if hashlib.sha256(sources[path]).hexdigest() != member['sha256']:
                raise ValueError('Manuscrit historique protégé altéré : '+path)
    for key, paths in identities.items():
        if len(paths)>1 and key not in data['groups']:
            raise ValueError('Collision d’identifiant historique non réconciliée : '+key)
    return data


def annotate(root, collections, chapters):
    """Use the same explicit status in every generated list and search index."""
    for key, group in load(root)['groups'].items():
        primary = next(m for m in group['members'] if m['role']=='primary')
        for member in group['members']:
            fields = dict(title=display_title(key, member), excerpt=member['summary'],
                          historical_id=key, historical_role=member['role'],
                          historical_primary_url=url(primary), historical_guide_url=group['guide_url'])
            for entry in collections.get('comparatif', []) + chapters:
                if entry['url'] == url(member):
                    entry.update(fields)


def install(root, out):
    """Add notices, stable passage anchors and one historical dossier landing page."""
    from build_native import render, markdown
    data = validate(root)
    for key, group in data['groups'].items():
        primary = next(m for m in group['members'] if m['role']=='primary')
        links = '<ul>'+''.join('<li><a href="'+url(m)+'">'+escape(
            f"{m['label'].capitalize()} — volume {m['number']} : {m['focus']}")+'</a></li>'
            for m in group['members'])+'</ul>'
        for member in group['members']:
            page = out/url(member).strip('/')/'index.html'
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            article = doc.select_one('article.content')
            for old in doc.select('[data-mc-history]'):
                old.decompose()
            # Add separate anchors: existing lecture-section-* bookmarks survive.
            for anchor, prefix in member['anchors'].items():
                headings = [h for h in article.select('h2,h3') if h.get_text(' ',strip=True).startswith(prefix)]
                if len(headings) != 1:
                    raise ValueError('Passage absent ou ambigu : '+member['source']+' ; '+prefix)
                marker = doc.new_tag('span', id='mc025-'+anchor)
                marker['data-mc-history'] = key
                headings[0].insert_before(marker)
            note = ('<aside class="editorial-note" data-mc-history="'+key+'" aria-label="Statut historique de cette étude">'
                    '<p><strong>'+escape(key+' — '+member['label'].capitalize())+'</strong></p>'
                    '<p>'+escape(member['summary'])+'</p>'
                    '<p>Une entrée historique, trois manuscrits intégraux. CLXXXIII (183) est la référence principale ; '
                    'CLXXXVII (187) et CLXXXIX (189) sont ses études complémentaires. '
                    'Leurs numéros canoniques et leurs textes sont conservés. Les mentions originales « inédite », '
                    '« autonome » ou de publication à venir témoignent de la rédaction initiale et ne définissent pas le statut actuel.</p>'
                    +links+'<p><a href="'+group['guide_url']+'">Comparer les apports, répétitions, sources et différences scientifiques</a></p></aside>')
            article.insert(0, BeautifulSoup(note, 'html.parser'))
            doc.title.string = display_title(key, member)+' | MYTHOS'
            doc.head.find('meta',attrs={'name':'description'})['content'] = member['summary']
            page.write_text(str(doc),encoding='utf-8')
        body = markdown((root/group['notice_source']).read_text(encoding='utf-8'))
        target = out/group['guide_url'].strip('/')/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(render(key+' — Maât et Isfet : guide des trois études', body),encoding='utf-8')
        for portal in ('mythologie-comparee','philosophie','collections-numerotees'):
            page = out/portal/'index.html'
            doc = BeautifulSoup(page.read_text(), 'html.parser')
            marker = 'historique-'+key.lower()
            for old in doc.select('#'+marker): old.decompose()
            block = ('<section class="portal-section" id="'+marker+'"><h2>'+escape(key+' — '+group['subject'])+'</h2>'
                     '<p>Un dossier historique : une étude principale et deux compléments intégraux. '
                     'Les trois numéros de volume restent distincts ; ils ne représentent pas trois livraisons historiques.</p>'
                     +links+'<p><a href="'+group['guide_url']+'">Lire la notice comparée et les renvois thématiques</a></p></section>')
            doc.select_one('article.content').insert(1, BeautifulSoup(block,'html.parser'))
            page.write_text(str(doc),encoding='utf-8')
    (out/REPORT).parent.mkdir(parents=True, exist_ok=True)
    (out/REPORT).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def blocks(doc):
    return Counter(normalized(node.get_text(' ',strip=True)) for node in doc.select(
        'h1,h2,h3,h4,h5,h6,p,li,table,pre,blockquote') if node.get_text(' ',strip=True))


def verify(root, out):
    """Check source bytes, all prose blocks, reciprocal links, indexes and fragments."""
    from build_native import markdown, frontmatter
    data = validate(root)
    search = {e['url']:e for e in json.loads((out/'search.json').read_text())}
    catalogue = {e['url']:e for e in json.loads((out/'catalog/entries.json').read_text())['entries']}
    numbers = json.loads((out/'catalog/numbering.json').read_text())['collections']['comparatif']
    numbers = {e['url']:e for e in numbers}
    sitemap = (out/'sitemap.xml').read_text()
    for key, group in data['groups'].items():
        pages = [group['guide_url']] + [url(m) for m in group['members']]
        for member in group['members']:
            address = url(member)
            for index in (search, catalogue, numbers):
                item = index[address]
                assert item['title'] == display_title(key, member), address
                assert item['historical_role'] == member['role'], address
            assert numbers[address]['number'] == member['number'], address
            doc = BeautifulSoup((out/address.strip('/')/'index.html').read_text(), 'html.parser')
            assert not doc.select('meta[http-equiv="refresh"]'), address
            original = BeautifulSoup(markdown(frontmatter((root/member['source']).read_text())[1]), 'html.parser')
            assert not (blocks(original)-blocks(doc)), 'Texte perdu : '+address
            note = doc.select_one('aside[data-mc-history]')
            assert note and member['label'].casefold() in note.get_text().casefold(), address
            for target in pages:
                assert note.find('a',href=target), 'Renvoi manquant : '+target
        for portal in ('mythologie-comparee','philosophie','collections-numerotees'):
            doc = BeautifulSoup((out/portal/'index.html').read_text(),'html.parser')
            assert len(doc.select('#historique-'+key.lower()))==1, portal
            for address in pages:
                assert doc.find('a',href=address), portal+' : '+address
        for address in pages:
            assert address in search and address in catalogue, address
            assert 'https://bobmythos.fr'+address in sitemap, address
            doc = BeautifulSoup((out/address.strip('/')/'index.html').read_text(),'html.parser')
            for a in doc.select('[data-mc-history] a[href]') if address != group['guide_url'] else doc.select('article.content a[href]'):
                link = urlsplit(urljoin('https://bobmythos.fr'+address,a['href']))
                if link.netloc != 'bobmythos.fr': continue
                target = out/link.path.lstrip('/')
                if link.path.endswith('/'): target /= 'index.html'
                assert target.is_file(), a['href']
                if link.fragment:
                    assert BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(link.fragment)), a['href']
    assert json.loads((out/REPORT).read_text()) == data
    return {'groups':len(data['groups']), 'protected_manuscripts':sum(len(g['members']) for g in data['groups'].values())}
