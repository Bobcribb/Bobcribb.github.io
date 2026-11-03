#!/usr/bin/env python3
"""Publish the existing Polyidos manuscript without abridgement or network access.

Run after build-daidalos.py. The immutable source and all 19 sections are checked
before rendering. Three explicitly modern scenes remain separate from the study.
Navigation inserts are idempotent and preserve the surrounding pages verbatim.
"""
from __future__ import annotations
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'corpus/theatre-grec/comedies/'
BLOB = '46c2cd20c5d797aee436bd83b429a8ffeef0e76b'
REV = 'fafe12416fc918d2576116cd0a4e0a9a2836ee11'
ORIGIN = f'https://github.com/Bobcribb/Bobcribb.github.io/blob/{REV}/'
STUDY = '/' + BASE + 'polyidos-etude.html'
SCENES = '/' + BASE + 'polyidos-scenes-modernes.html'
DAIDALOS = '/' + BASE + 'daidalos-etude.html'
ROMANS = 'I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX'.split()
CREATIVE = {'XIV', 'XV', 'XVI'}
TOKEN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*([^*\n]+)\*')
MARKER = 'MYTHOS-POLYIDOS'


def target_url(target: str) -> str:
    known = {'/theatre/': '/theatre-grec.html', '/philosophie/': '/philosophie.html',
             'volume-026-aristophane-daidalos.md': DAIDALOS,
             'volume-024-aristophane-babylonioi.md': ORIGIN + 'chapitres/comedies/volume-024-aristophane-babylonioi.md'}
    if target in known:
        return known[target]
    if target.startswith('/comedie-grecque-aristophane-menandre-etudes/') and target.endswith('/'):
        return ORIGIN + target.lstrip('/') + 'index.html'
    if target.startswith(('https://', '#')):
        return target
    raise ValueError('Unreviewed source link: ' + target)


def inline(text: str) -> str:
    result, cursor = [], 0
    for match in TOKEN.finditer(text):
        result.append(html.escape(text[cursor:match.start()], quote=False))
        if match.group(1) is not None:
            result.append('<a href="' + html.escape(target_url(match.group(2)), quote=True) + '">' + inline(match.group(1)) + '</a>')
        elif match.group(3) is not None:
            result.append('<strong>' + inline(match.group(3)) + '</strong>')
        else:
            result.append('<em>' + inline(match.group(4)) + '</em>')
        cursor = match.end()
    result.append(html.escape(text[cursor:], quote=False))
    return ''.join(result)


def prose(text: str) -> str:
    parts = []
    for block in re.split(r'\n\s*\n', text.strip()):
        heading = re.fullmatch(r'(#{1,2}) (.+)', block)
        if block == '---':
            parts.append('<hr>')
        elif heading:
            level = len(heading.group(1)) + 1
            parts.append(f'<h{level}>' + inline(heading.group(2)) + f'</h{level}>')
        else:
            parts.append('<p>' + inline(block) + '</p>')
    return '\n'.join(parts)


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.text = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in {'a', 'link'}:
            self.links.append(attrs.get('href', ''))
    def handle_endtag(self, tag):
        if tag in {'p', 'h1', 'h2', 'h3', 'h4', 'li', 'section', 'div'}:
            self.text.append('\n')
    def handle_data(self, data):
        self.text.append(data)


def normal(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def visible_markdown(text: str) -> str:
    text = re.sub(r'^#{1,6} ', '', text, flags=re.M)
    text = re.sub(r'^---\s*$', '', text, flags=re.M)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return normal(text.replace('*', ''))


def assert_prose_equal(raw: str, markup: str) -> None:
    parser = Inspector()
    parser.feed(markup)
    if normal(''.join(parser.text)) != visible_markdown(raw):
        raise ValueError('Readable source text was altered during rendering')


def section_id(roman: str) -> str:
    return 'bibliographie' if roman == 'XVIII' else 'section-' + roman.lower()


def render(kind: str, intro: str, sections: list[tuple[str, str, str]]) -> str:
    scholarly = kind == 'etude'
    selected = [s for s in sections if (s[0] not in CREATIVE) == scholarly]
    title = 'Polyidos — Étude critique' if scholarly else 'Polyidos — Scènes modernes'
    cote = 'TH-03-POL' if scholarly else 'TH-02-POL'
    counterpart = SCENES if scholarly else STUDY
    label = 'Lire les trois scènes modernes' if scholarly else 'Lire l’étude et sa bibliographie'
    notice = ('Le manuscrit est conservé intégralement dans deux lectures complémentaires. Les seize sections critiques restent ici ; '
              'les trois scènes modernes sont séparées, sans suppression. Les repères historiques du volume XXV sont conservés.' if scholarly else
              'Les trois scènes ci-dessous sont des créations contemporaines déjà présentes dans le manuscrit. '
              'Elles ne sont ni des fragments antiques ni une traduction de la comédie perdue. L’analyse et la bibliographie sont dans la lecture liée.')
    toc = ''.join(f'<li><a href="#{section_id(r)}">{inline(t)}</a></li>' for r, t, _ in selected)
    article = ''
    if scholarly:
        intro_html = prose(intro)
        assert_prose_equal(intro, intro_html)
        article = '<div data-source-intro="true">' + intro_html + '</div>'
    for roman, heading, block in selected:
        _, body = block.split('\n', 1)
        markup = f'<h2>{inline(heading)}</h2>' + prose(body)
        assert_prose_equal(block, markup)
        article += f'<section id="{section_id(roman)}" data-source-section="{roman}">{markup}</section>\n'
        if roman == 'XIII':
            article += f'<p class="dai-editorial-link">Les sections XIV–XVI sont conservées dans la <a href="{SCENES}">lecture des scènes modernes</a>.</p>'
    bibliography = '#bibliographie' if scholarly else STUDY + '#bibliographie'
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0c1012"><meta name="mythos-source-blob" content="{BLOB}"><title>{title} — MYTHOS</title>
<meta name="description" content="Polyidos : manuscrit universitaire intégral, analyses et trois scènes modernes séparées, sources et bibliographie conservées.">
<link rel="stylesheet" href="/assets/mythos-theatre.css"><link rel="stylesheet" href="/assets/mythos-reading-tools.css"></head>
<body class="dai-reader"><a class="dai-skip" href="#lecture">Aller au texte</a><header class="dai-header"><a class="dai-brand" href="/">MYTHOS<small>ENCYCLOPÉDIE DES MYTHOLOGIES</small></a><nav aria-label="Navigation principale"><a href="/theatre-grec.html">Théâtre grec</a><a href="/philosophie.html">Philosophie</a><a href="/sommaire-general.html">Sommaire général</a></nav></header>
<section class="dai-hero"><div><p class="dai-overline">COMÉDIES GRECQUES · {cote}</p><h1>Polyidos</h1><p class="dai-subtitle">{'Voir l’invisible, rendre la vie ?' if scholarly else 'Trois scènes contemporaines, non antiques'}</p><p>Aristophane · Comédie perdue · Volume source XXV</p></div></section>
<div class="dai-shell"><nav class="dai-breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a> / <a href="/theatre-grec.html">Théâtre grec</a> / {title}</nav>
<nav class="dai-paths" aria-label="Parcours de lecture"><a href="{STUDY}" {'aria-current="page"' if scholarly else ''}>01 · Étude critique</a><a href="{SCENES}" {'' if scholarly else 'aria-current="page"'}>02 · Scènes modernes</a></nav>
<p class="dai-notice">{notice}</p><nav class="mythos-reading-tools" aria-label="Accès rapides"><a href="#lecture">Lire le texte</a><a href="{bibliography}">Sources et bibliographie</a><a href="/{BASE}polyidos-source.md">Manuscrit intégral</a></nav>
<div class="dai-layout"><aside class="dai-sidebar"><details open><summary>Sommaire · {len(selected)} sections</summary><nav aria-label="Sommaire de la lecture"><ol>{toc}</ol></nav></details><p><a href="{counterpart}">{label}</a></p><p><a href="{DAIDALOS}">Dossier suivant : Daidalos</a></p></aside>
<main id="lecture" class="dai-article" tabindex="-1">{article}<nav class="dai-reading-end" aria-label="Poursuivre la lecture"><a href="{counterpart}">{label} →</a><a href="{DAIDALOS}">Daidalos →</a><a href="/theatre-grec.html#polyidos">Retour à la collection</a></nav>
<aside class="dai-provenance"><h2>Provenance et contrôle éditorial</h2><p>Manuscrit repris du <a href="{ORIGIN}chapitres/comedies/volume-025-aristophane-polyidos.md">dépôt historique</a>, version <code>{REV[:7]}</code>. La source Markdown est conservée à l’octet près. Les 19 sections et le préambule sont répartis sans abrègement et sans doublon entre les deux lectures.</p><p>Les liens vers les anciens dossiers ouvrent les archives historiques ; ils ne désignent pas d’autres études nouvellement importées. Le contrôle d’intégrité ne remplace pas la collation des fragments réclamée par le manuscrit. <a href="/{BASE}polyidos-controle.json">Rapport technique</a>.</p></aside></main></div></div>
<footer class="dai-footer">MYTHOS · {cote} · <a href="/sommaire-general.html">Sommaire général</a></footer></body></html>'''


def insert_before_main_end(path: Path, content: str) -> None:
    original = path.read_text(encoding='utf-8')
    start, end = '<!-- ' + MARKER + ':START -->', '<!-- ' + MARKER + ':END -->'
    if start in original:
        if original.count(start) != 1 or original.count(end) != 1:
            raise ValueError('Duplicate navigation marker: ' + str(path))
        clean = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', original, flags=re.S)
    else:
        clean = original
    if clean.count('</main>') != 1:
        raise ValueError('Expected one main closing tag: ' + str(path))
    block = start + content + end
    updated = clean.replace('</main>', block + '</main>')
    if updated.replace(block, '', 1) != clean:
        raise ValueError('Surrounding page was changed')
    path.write_text(updated, encoding='utf-8')


def navigation() -> list[str]:
    card = lambda href, cote, title, text, scene='': f'<a class="dai-card" href="{href}"><span class="dai-card-art {scene}" aria-hidden="true"></span><span class="dai-card-copy"><small>{cote}</small><h3>{title}</h3><p>{text}</p><b>Lire →</b></span></a>'
    study = card(STUDY, 'TH-03-POL · ÉTUDE CRITIQUE', 'Polyidos — Savoir et pouvoir', 'Seize sections critiques, bibliographie et conclusion conservées. Analyses liées à une pièce, distinctes des dialogues modernes.')
    scenes = card(SCENES, 'TH-02-POL · CRÉATIONS CONTEMPORAINES', 'Polyidos — Trois scènes modernes', 'Le prix de la certitude, la leçon du serpent, l’épreuve du retour. Aucun de ces dialogues n’est attribué au texte antique.', 'dai-card-art--scene')
    entries = {
        'theatre-grec.html': '<section class="container dai-collection" id="polyidos"><h2>Polyidos — Deux parcours distincts</h2><div class="dai-cards">' + study + scenes + '</div><p class="notice">Motifs décoratifs du site, non restitutions archéologiques. <a href="/corpus/theatre-grec/REGISTRE-INTEGRATIONS.md">Provenance et contrôles</a>.</p></section>',
        'philosophie.html': '<section class="container dai-collection" id="polyidos-philosophie"><h2>Analyses liées aux pièces — Polyidos</h2><div class="dai-cards">' + study + '</div></section>',
        'sommaire-general.html': f'<section class="rules" id="polyidos-sommaire"><h2>Théâtre grec — Polyidos</h2><p><a href="{STUDY}">TH-03-POL · Étude critique intégrale</a> · <a href="{SCENES}">TH-02-POL · Trois scènes modernes</a></p></section>'}
    for name, content in entries.items():
        insert_before_main_end(ROOT / name, content)
    for filename in ('daidalos-etude.html', 'daidalos-scenes-modernes.html'):
        insert_before_main_end(ROOT / BASE / filename, f'<nav class="dai-reading-end" aria-label="Dossier précédent"><a href="{STUDY}">← Polyidos : étude critique et bibliographie</a></nav>')
    return list(entries)


def validate_links(markup: str, page: Path) -> None:
    parsed = Inspector()
    parsed.feed(markup)
    if len(parsed.ids) != len(set(parsed.ids)):
        raise ValueError('Duplicate IDs: ' + str(page))
    for link in parsed.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / url.path.lstrip('/')) if url.path.startswith('/') else page.parent / url.path
        if not url.path:
            target = page
        if target.is_dir():
            target = target / 'index.html'
        if not target.is_file():
            raise ValueError('Missing internal target: ' + link)
        if url.fragment:
            other = Inspector()
            other.feed(target.read_text(encoding='utf-8'))
            if unquote(url.fragment) not in other.ids:
                raise ValueError('Missing cross-page anchor: ' + link)


def main() -> None:
    source_path = ROOT / BASE / 'polyidos-source.md'
    data = source_path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if actual != BLOB:
        raise ValueError('Source changed: ' + actual)
    source = data.decode('utf-8')
    front = re.match(r'\A---\n.*?\n---\n\n', source, re.S)
    if not front:
        raise ValueError('Missing front matter')
    body = source[front.end():]
    headings = list(re.finditer(r'^### ([IVX]+)\. (.+)$', body, re.M))
    if [h.group(1) for h in headings] != ROMANS:
        raise ValueError('Missing or reordered section')
    intro = body[:headings[0].start()]
    sections = [(m.group(1), m.group(1) + '. ' + m.group(2), body[m.start():headings[i+1].start() if i+1 < len(headings) else len(body)]) for i, m in enumerate(headings)]
    if front.group() + intro + ''.join(s[2] for s in sections) != source:
        raise ValueError('Non-exact source partition')
    if any(('[C]' in title) != (roman in CREATIVE) for roman, title, _ in sections):
        raise ValueError('Creative/scholarly classification changed')
    outputs = {}
    for kind, filename in [('etude', 'polyidos-etude.html'), ('scenes', 'polyidos-scenes-modernes.html')]:
        page = ROOT / BASE / filename
        if page.exists() and f'content="{BLOB}"' not in page.read_text(encoding='utf-8'):
            raise ValueError('Refusing to overwrite an unrelated page: ' + str(page))
        markup = render(kind, intro, sections)
        found = re.findall(r'data-source-section="([IVX]+)"', markup)
        expected = [s[0] for s in sections if (s[0] not in CREATIVE) == (kind == 'etude')]
        if found != expected:
            raise ValueError('Section coverage failed')
        page.write_text(markup, encoding='utf-8')
        outputs[filename] = {'sections': found, 'bytes': len(markup.encode()), 'visible_text_equal': True}
    linked_pages = navigation()
    report = {'source_repository': 'Bobcribb/Bobcribb.github.io', 'source_ref': REV, 'source_path': 'chapitres/comedies/volume-025-aristophane-polyidos.md', 'source_git_blob': actual, 'source_sha256': hashlib.sha256(data).hexdigest(), 'source_bytes': len(data), 'source_characters': len(source), 'source_lines': len(source.splitlines()), 'section_count': len(sections), 'partition_exact': True, 'no_duplicate_section': True, 'outputs': outputs, 'navigation_pages': linked_pages, 'reciprocal_daidalos_links': True, 'scientific_review': 'Textual integrity checked; exhaustive philological collation not performed.'}
    report_path = ROOT / BASE / 'polyidos-controle.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for filename in outputs:
        page = ROOT / BASE / filename
        validate_links(page.read_text(encoding='utf-8'), page)
    report['internal_links_and_anchors_valid'] = True
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
