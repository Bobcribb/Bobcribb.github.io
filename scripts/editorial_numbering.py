#!/usr/bin/env python3
"""Canonical numbering, historical addresses and collection navigation for MYTHOS.

Manuscripts are never rewritten by this module. Unknown duplicate numbers fail
before rendering. Only explicitly documented historical aliases are exempted.
"""
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
import html
import json
import re
from bs4 import BeautifulSoup

COLLECTIONS = {
    'encyclopedie': ('Grande Encyclopédie', 'Chapitre', '/grande-encyclopedie/'),
    'tragedies': ('Encyclopédie des tragédies', 'Volume', '/theatre/'),
    'comparatif': ('Cycle philosophique comparatif', 'Volume', '/philosophie/'),
    'comedies': ('Encyclopédie des comédies', 'Volume', '/theatre/'),
    'origines-du-sacre': ('Origines du sacré', 'Chapitre', '/origines-du-sacre/'),
}
COMEDY_ALIAS = '/chapitres/comedies/volume-002-eupolis-heilotes/'
COMEDY_TARGET = '/chapitres/comedies/volume-003-eupolis-heilotes/'


def roman(number):
    result = ''
    for value, symbol in [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        count, number = divmod(number, value)
        result += symbol * count
    return result


def integer(token):
    if token.isdigit():
        return int(token)
    values = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    token = token.upper()
    result = sum(-values[c] if i+1<len(token) and values[c]<values[token[i+1]] else values[c] for i,c in enumerate(token))
    if roman(result) != token:
        raise ValueError('Nombre romain invalide : ' + token)
    return result


def identity(path):
    match = re.match(r'(?:(?:chapitre|volume|mc)-)?(\d+|[ivxlcdm]+)-', path.stem, re.I)
    return integer(match[1]) if match else None


def registry(root):
    data = json.loads((root / 'EDITORIAL_NUMBERING.json').read_text(encoding='utf-8'))
    if data['version'] != 1:
        raise ValueError('Version du registre de numérotation inconnue')
    return data


def redirects(root):
    result = {m['old_url']: m['url'] for m in registry(root)['renumbered']}
    result[COMEDY_ALIAS] = COMEDY_TARGET
    result.update(json.loads((root / 'EDITORIAL_REDIRECTS.json').read_text())['redirects'])
    for old, new in result.items():
        if old == new or new in result or not new.startswith('/chapitres/'):
            raise ValueError('Redirection invalide ou en chaîne : ' + old)
    return result


def scan(root):
    """Audit all numbered active manuscript collections; aliases are explicit."""
    from origines_reconciliation import COMPLEMENTS
    aliases = set(COMPLEMENTS) | {COMEDY_ALIAS}
    result = defaultdict(list)
    seen = {}
    for collection in COLLECTIONS:
        for path in sorted((root / 'chapitres' / collection).glob('*.md')):
            number = identity(path)
            if number is None:
                continue
            url = '/' + path.relative_to(root).with_suffix('').as_posix() + '/'
            if url in aliases:
                continue
            key = collection, number
            if key in seen:
                raise ValueError(f'Doublon éditorial {collection} {number} : {seen[key]} ; {path}')
            seen[key] = str(path)
            raw = path.read_text(encoding='utf-8')
            headings = re.findall(r'^#{1,2}\s+(.+)$', raw, re.M)[:3]
            kind = COLLECTIONS[collection][1]
            title_number = re.search(r'\b'+kind+r'\s+(\d+|[IVXLCDM]+)\b', ' '.join(headings), re.I)
            if title_number and integer(title_number[1]) != number:
                raise ValueError(f'Numéro du titre différent du chemin : {path}')
            subject = next((h for h in headings if not re.search(r'MYTHOS|^Volume\s+[IVXLCDM]',h,re.I)), headings[-1] if headings else path.stem)
            subject = re.sub(r'^Volume\s+[IVXLCDM]+(?:\s*\(\d+\))?\s*[—:–-]\s*', '', subject, flags=re.I)
            subject = re.sub(r'[*_`]', '', subject).strip()
            if kind == 'Chapitre':
                # The manuscript may already title its first heading
                # "Chapitre 433 — Athéna Lindia". The canonical index adds
                # that same number: strip only a matching source prefix.
                source_heading = subject
                subject = re.sub(
                    r'^Chapitre\s+' + str(number) + r'\b(?:\s*[—:–-]\s*|\s*$)',
                    '', subject, count=1, flags=re.I).strip()
                if not subject:
                    # A number-only h1 can be followed by a scientific h2.
                    subject = next((re.sub(r'[*_`]', '', h).strip()
                                    for h in headings if h != source_heading
                                    and not re.match(
                                        r'^(?:Chapitre\s+\d+\b|Résumé\b|Abstract\b|MYTHOS\b)', h, re.I)),
                                   source_heading)
            label = f'{kind} {number}' if kind == 'Chapitre' else f'{kind} {roman(number)} ({number})'
            result[collection].append({'number':number,'url':url,'title':label+' — '+subject,'source':path.relative_to(root).as_posix()})
    for items in result.values():
        items.sort(key=lambda e:e['number'])
    # Old source files must not reappear as second active manuscripts.
    for move in registry(root)['renumbered']:
        if (root / move['old_path']).exists():
            raise ValueError('Ancienne source réintroduite : '+move['old_path'])
        path = root / move['path']
        if not path.is_file() or identity(path) != move['number']:
            raise ValueError('Source renumérotée manquante ou incohérente : '+move['path'])
    for old, target in redirects(root).items():
        if not (root / (target.strip('/')+'.md')).is_file():
            raise ValueError('Cible de redirection sans manuscrit : '+target)
    return dict(result)


def relabel(value, move):
    """Change only the editorial reference in a link to a moved manuscript."""
    if move['collection'] == 'encyclopedie':
        value = re.sub(r'(?i)(chapitre\s+)'+str(move['old_number'])+r'\b',lambda m:m[1]+str(move['number']),value)
        value = re.sub(r'(?i)(volume\s+)'+roman(move['old_number']-218)+r'\b',lambda m:m[1]+roman(move['number']-218),value)
    else:
        value = re.sub(r'(?i)(volume\s+)'+move['old_roman']+r'\b(?:\s*\('+str(move['old_number'])+r'\))?',lambda m:m[1]+move['roman']+' ('+str(move['number'])+')',value)
    return value


def canonical_link(href, page_url, mapping):
    parsed = urlsplit(urljoin('https://bobmythos.fr'+page_url, href))
    if parsed.hostname not in ('bobmythos.fr','www.bobmythos.fr','bobcribb.github.io'):
        return href, None
    path = unquote(parsed.path)
    if path.endswith('/index.html'):
        path = path[:-10]
    if path.endswith('.md'):
        path = path[:-3]+'/'
    if path in mapping:
        return urlunsplit(('', '', mapping[path], parsed.query, parsed.fragment)), path
    return href, None


def finish(out, root, collections):
    from build_native import render
    mapping = redirects(root)
    moves = {m['old_url']:m for m in registry(root)['renumbered']}
    # Rewrite links and their visible numbers together, including old root HTML
    # portals, relative links, .md links, fragments and absolute domain links.
    corrected = 0
    for page in out.rglob('*.html'):
        raw = page.read_text(encoding='utf-8')
        if not any(old.strip('/').split('/')[-1] in raw for old in mapping):
            continue
        doc = BeautifulSoup(raw, 'html.parser')
        page_url = '/'+page.relative_to(out).as_posix()
        changed = False
        for a in doc.select('a[href]'):
            target, old = canonical_link(a['href'],page_url,mapping)
            if old:
                a['href'] = target
                if old in moves:
                    for node in list(a.find_all(string=True)):
                        node.replace_with(relabel(str(node),moves[old]))
                corrected += 1
                changed = True
        if changed:
            page.write_text(str(doc),encoding='utf-8')
    index_body = '<h1>Collections numérotées de MYTHOS</h1><p>Chaque collection possède sa numérotation. Les études et versions parallèles sont conservées intégralement ; les anciennes adresses renvoient aux références corrigées.</p>'
    by_url = {m['url']:m for m in moves.values()}
    for collection, items in collections.items():
        name, kind, portal = COLLECTIONS[collection]
        rows = ''.join('<li value="'+str(e['number'])+'"><a href="'+html.escape(e['url'],quote=True)+'">'+html.escape(e['title'])+'</a></li>' for e in items)
        section = '<section class="portal-section" id="numerotation-'+collection+'"><h2>'+html.escape(name)+'</h2><p>'+str(len(items))+' études numérotées présentes dans cette série. <a href="'+portal+'">Ouvrir la collection</a></p><ol class="portal-list">'+rows+'</ol></section>'
        index_body += section
        # Keep the existing portals and their thematic organisation intact.
        p = out / portal.strip('/') / 'index.html'
        doc = BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        article = doc.select_one('article.content')
        if article is None:
            raise ValueError('Portail sans contenu : '+str(p))
        old = doc.find(id='numerotation-'+collection)
        if old:old.decompose()
        if collection != 'encyclopedie' or not doc.find(id='grec-universitaire'):
            article.append(BeautifulSoup(section,'html.parser'))
        p.write_text(str(doc),encoding='utf-8')
        for i,entry in enumerate(items):
            path = out / entry['url'].strip('/') / 'index.html'
            doc = BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
            article = doc.select_one('article.content')
            old = doc.find(id='collection-number-navigation')
            if old:old.decompose()
            links = []
            if i:
                e=items[i-1];links.append('<a rel="prev" href="'+e['url']+'">← '+html.escape(e['title'])+'</a>')
            links.append('<a href="/collections-numerotees/#numerotation-'+collection+'">Sommaire de la collection</a>')
            if i+1<len(items):
                e=items[i+1];links.append('<a rel="next" href="'+e['url']+'">'+html.escape(e['title'])+' →</a>')
            article.append(BeautifulSoup('<nav id="collection-number-navigation" aria-label="Parcours dans la collection">'+' · '.join(links)+'</nav>','html.parser'))
            if entry['url'] in by_url:
                m=by_url[entry['url']]
                note = '<p class="editorial-note">Référence corrigée : '+kind.lower()+' '+str(m['number'])+' (ancienne référence '+str(m['old_number'])+'). Texte intégral conservé.</p>'
                article.append(BeautifulSoup(note,'html.parser'))
            if doc.head:
                for node in doc.head.select('link[rel="canonical"]'):node.decompose()
                doc.head.append(doc.new_tag('link',rel='canonical',href='https://bobmythos.fr'+entry['url']))
            path.write_text(str(doc),encoding='utf-8')
    p=out/'collections-numerotees/index.html';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(render('Collections numérotées — MYTHOS',index_body),encoding='utf-8')
    for old,new in mapping.items():
        path=out/old.strip('/')/'index.html';path.parent.mkdir(parents=True,exist_ok=True)
        # Preserve fragment identifiers when an old URL has been bookmarked.
        content=render('Référence corrigée — MYTHOS', '<h1>Référence corrigée</h1><p>Cette étude intégrale possède une nouvelle référence. <a href="'+new+'">Lire le texte intégral</a>.</p><script>location.replace('+json.dumps(new)+'+location.search+location.hash)</script>')
        content=content.replace('</head>', '<meta name="robots" content="noindex,follow"><link rel="canonical" href="https://bobmythos.fr'+new+'"><meta http-equiv="refresh" content="0;url='+new+'"></head>')
        path.write_text(content,encoding='utf-8')
    report={'collections':collections,'redirects':mapping,'renumbered_studies':len(moves),'unresolved_collisions':0,'corrected_links':corrected}
    path=out/'catalog/numbering.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


if __name__ == '__main__':
    data=scan(Path('.').resolve())
    print(json.dumps({k:{'studies':len(v),'last_number':max(e['number'] for e in v)} for k,v in data.items()},ensure_ascii=False,indent=2))
    print('Numérotation : aucun doublon actif ; adresses historiques contrôlées.')
