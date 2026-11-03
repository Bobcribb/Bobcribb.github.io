#!/usr/bin/env python3
"""Render the preserved Daidalos manuscript; no network or third-party dependency.

The source blob is immutable. All 22 original sections are assigned exactly once:
19 to the critical study, 3 to the explicitly modern scenes. Source prose is never
summarised. Run from any directory before publishing the Pages artifact.
"""
from __future__ import annotations
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'corpus/theatre-grec/comedies/'
SOURCE = ROOT / BASE / 'daidalos-source.md'
BLOB = '7e700ab6e72f26208e47d6e3eb600e41f95af78c'
REV = 'f865cd391413301f9f2788c2caf4026c257a28c4'
ORIGIN = f'https://github.com/Bobcribb/Bobcribb.github.io/blob/{REV}/chapitres/comedies/'
STUDY = '/' + BASE + 'daidalos-etude.html'
SCENES = '/' + BASE + 'daidalos-scenes-modernes.html'
CREATIVE = {'XVIII', 'XIX', 'XX'}
ROMANS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII']
TOKEN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*([^*\n]+)\*')


def inline(text: str) -> str:
    """Escape all raw HTML; interpret only the source's three inline constructs."""
    result, cursor = [], 0
    for match in TOKEN.finditer(text):
        result.append(html.escape(text[cursor:match.start()], quote=False))
        if match.group(1) is not None:
            target = match.group(2)
            # The two historical navigation links remain external, not fake local pages.
            if target in {'volume-025-aristophane-polyidos.md', 'volume-027-aristophane-kokalos.md'}:
                target = ORIGIN + target
            elif not target.startswith(('https://', '/', '#')):
                raise ValueError(f'Unreviewed link: {target}')
            result.append(f'<a href="{html.escape(target, quote=True)}">{inline(match.group(1))}</a>')
        elif match.group(3) is not None:
            result.append('<strong>' + inline(match.group(3)) + '</strong>')
        else:
            result.append('<em>' + html.escape(match.group(4), quote=False) + '</em>')
        cursor = match.end()
    result.append(html.escape(text[cursor:], quote=False))
    return ''.join(result)


def prose(text: str) -> str:
    output = []
    for paragraph in re.split(r'\n\s*\n', text.strip()):
        heading = re.fullmatch(r'(#{1,2}) (.+)', paragraph)
        if heading:
            level = len(heading.group(1)) + 1
            output.append(f'<h{level}>' + inline(heading.group(2)) + f'</h{level}>')
        else:
            output.append('<p>' + inline(paragraph) + '</p>')
    return '\n'.join(output)


class Inspection(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.text = [], [], []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if 'id' in data:
            self.ids.append(data['id'])
        if tag == 'a':
            self.links.append(data.get('href', ''))
    def handle_data(self, data):
        self.text.append(data)


def section_id(roman: str) -> str:
    return 'bibliographie' if roman == 'XXII' else 'section-' + roman.lower()


def render_page(kind: str, intro: str, sections: list[tuple[str, str, str]]) -> str:
    scholarly = kind == 'etude'
    selected = [s for s in sections if (s[0] not in CREATIVE) == scholarly]
    title = 'Daidalos — Étude critique' if scholarly else 'Daidalos — Scènes modernes'
    cote = 'TH-03-DAI' if scholarly else 'TH-02-DAI'
    target, target_label = (SCENES, 'Lire les trois scènes modernes') if scholarly else (STUDY, 'Lire l’étude critique et la bibliographie')
    notice = ('Le texte source est repris sans abrègement. Les trois scènes modernes sont placées dans une lecture distincte, reliée ci-dessous. '
              'Les anciens numéros de sections restent des repères documentaires ; la cote du site est TH-03-DAI.' if scholarly else
              'Ces trois dialogues sont des créations contemporaines du manuscrit MYTHOS. Ce ne sont ni des fragments antiques ni une restitution du texte perdu d’Aristophane. '
              'Les analyses et la bibliographie sont accessibles dans l’étude liée.')
    toc = ''.join(f'<li><a href="#{section_id(r)}">{inline(t)}</a></li>' for r, t, _ in selected)
    article = prose(intro) if scholarly else ''
    for roman, title_text, block in selected:
        heading_line, content = block.split('\n', 1)
        article += f'\n<section id="{section_id(roman)}" data-source-section="{roman}"><h2>{inline(title_text)}</h2>{prose(content)}</section>'
        if roman == 'XVII':
            article += f'<p class="dai-editorial-link"><a href="{SCENES}">Les scènes XVIII–XX sont conservées intégralement dans la lecture séparée →</a></p>'
    bibliography = '#bibliographie' if scholarly else STUDY + '#bibliographie'
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0c1012"><title>{title} — MYTHOS</title>
<meta name="description" content="Daidalos : étude critique conservée intégralement, scènes modernes séparées, sources et bibliographie.">
<link rel="stylesheet" href="/assets/mythos-theatre.css"></head>
<body class="dai-reader"><a class="dai-skip" href="#lecture">Aller au texte</a>
<header class="dai-header"><a class="dai-brand" href="/">MYTHOS<small>ENCYCLOPÉDIE DES MYTHOLOGIES</small></a>
<nav aria-label="Navigation principale"><a href="/theatre-grec.html">Théâtre grec</a><a href="/philosophie.html">Philosophie</a><a href="/sommaire-general.html">Sommaire général</a></nav></header>
<section class="dai-hero"><div><p class="dai-overline">COMÉDIES GRECQUES · {cote}</p><h1>Daidalos</h1><p class="dai-subtitle">{'L’artisan, l’image et la puissance de fabriquer' if scholarly else 'Trois scènes contemporaines, distinctes du dossier antique'}</p><p>Aristophane · Œuvre perdue · Volume source XXVI</p></div></section>
<div class="dai-shell"><nav class="dai-breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span> / </span><a href="/theatre-grec.html">Théâtre grec</a><span> / {title}</span></nav>
<div class="dai-paths" aria-label="Deux parcours de lecture"><a href="{STUDY}" {'aria-current="page"' if scholarly else ''}>01 · Étude critique</a><a href="{SCENES}" {'' if scholarly else 'aria-current="page"'}>02 · Scènes modernes</a></div>
<p class="dai-notice">{notice}</p><div class="dai-layout"><aside class="dai-sidebar"><details open><summary>Sommaire · {len(selected)} sections</summary><nav aria-label="Sommaire de la lecture"><ol>{toc}</ol></nav></details><p><a href="{bibliography}">Sources et bibliographie</a></p><p><a href="/{BASE}daidalos-source.md">Manuscrit source intégral</a></p></aside>
<main class="dai-article" id="lecture" tabindex="-1">{article}<nav class="dai-reading-end" aria-label="Poursuivre la lecture"><a href="{target}">{target_label} →</a><a href="/theatre-grec.html">← Retour au théâtre grec</a></nav>
<aside class="dai-provenance"><h2>Provenance et contrôle éditorial</h2><p>Transfert depuis le dépôt historique <a href="{ORIGIN}volume-026-aristophane-daidalos.md">Bobcribb/Bobcribb.github.io</a>, version <code>{REV[:7]}</code>. Source conservée à l’octet près ; les 22 sections sont réparties une seule fois entre les deux lectures. Les liens de voisinage du manuscrit ouvrent les archives historiques, pas des volumes nouvellement intégrés ici.</p><p>Contrôle de copie et de navigation. Les réserves du manuscrit sont conservées : cette édition n’est pas une collation exhaustive des fragments. <a href="/{BASE}daidalos-controle.json">Rapport technique</a>.</p></aside></main></div></div>
<footer class="dai-footer">MYTHOS · Théâtre grec · {cote} · <a href="/sommaire-general.html">Sommaire général</a></footer></body></html>'''


def main() -> None:
    data = SOURCE.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if actual != BLOB:
        raise ValueError(f'Source changed: expected {BLOB}, received {actual}; review before publishing')
    source = data.decode('utf-8')
    front = re.match(r'\A---\n.*?\n---\n\n', source, re.S)
    if not front:
        raise ValueError('Missing front matter')
    body = source[front.end():]
    headings = list(re.finditer(r'^### ([IVX]+)\. (.+)$', body, re.M))
    if [m.group(1) for m in headings] != ROMANS:
        raise ValueError('Incomplete or reordered source sections')
    intro = body[:headings[0].start()]
    sections = [(m.group(1), m.group(1) + '. ' + m.group(2), body[m.start():headings[i + 1].start() if i + 1 < len(headings) else len(body)]) for i, m in enumerate(headings)]
    if front.group() + intro + ''.join(s[2] for s in sections) != source:
        raise ValueError('Source coverage is not exact')
    if any(('[C]' in title) != (roman in CREATIVE) for roman, title, _ in sections):
        raise ValueError('Creative/scholarly classification changed')
    outputs = {}
    for kind, filename in [('etude', 'daidalos-etude.html'), ('scenes', 'daidalos-scenes-modernes.html')]:
        text = render_page(kind, intro, sections)
        parsed = Inspection()
        parsed.feed(text)
        if len(parsed.ids) != len(set(parsed.ids)):
            raise ValueError('Duplicate anchors')
        for link in parsed.links:
            if link.startswith('#') and link[1:] not in parsed.ids:
                raise ValueError('Missing anchor: ' + link)
        expected = [s[0] for s in sections if (s[0] not in CREATIVE) == (kind == 'etude')]
        found = re.findall(r'data-source-section="([IVX]+)"', text)
        if found != expected:
            raise ValueError('HTML section coverage failed')
        (ROOT / BASE / filename).write_text(text, encoding='utf-8')
        outputs[filename] = {'sections': found, 'bytes': len(text.encode()), 'unique_ids': len(parsed.ids), 'internal_anchors_valid': True}
    report = {'source_repository': 'Bobcribb/Bobcribb.github.io', 'source_ref': REV, 'source_path': 'chapitres/comedies/volume-026-aristophane-daidalos.md', 'source_git_blob': actual, 'source_sha256': hashlib.sha256(data).hexdigest(), 'source_bytes': len(data), 'source_characters': len(source), 'source_lines': len(source.splitlines()), 'section_count': len(sections), 'partition_exact': True, 'no_duplicate_section': True, 'outputs': outputs, 'scientific_review': 'Textual integrity checked; critical collation of all fragments not performed.'}
    (ROOT / BASE / 'daidalos-controle.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
