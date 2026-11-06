"""Raccorder les éditions intégrales déjà présentes des comédies perdues.

Les dossiers critiques et les créations modernes sont volontairement séparés.
Ce module n'attribue aucun numéro, ne copie aucun manuscrit et n'altère aucun
lecteur universitaire ; il enrichit seulement le portail Théâtre généré.
"""
from __future__ import annotations
import html
import re
from pathlib import Path
from bs4 import BeautifulSoup

SLUGS = ('polyidos', 'daidalos', 'kokalos', 'aiolosikon', 'holkades',
         'lemniai', 'geras', 'ploutos-protos', 'triphales')
BASE = Path('corpus/theatre-grec/comedies')
TITLE = re.compile(r'(?m)^##\s+(.+)$')
VOLUME = re.compile(r'(?im)^#\s+[^\n]*volume\s+([IVXLCDM]+)')


def verified_editions(root: Path, output: Path, slugs=SLUGS):
    """Refuse les archives partielles et vérifie les trois pièces de chaque édition."""
    root, output = Path(root), Path(output)
    records = []
    for slug in slugs:
        src = root / BASE / f'{slug}-source.md'
        critique = output / BASE / f'{slug}-etude.html'
        scenes = output / BASE / f'{slug}-scenes-modernes.html'
        paths = (src, critique, scenes)
        # Une archive déclarée ne doit jamais disparaître silencieusement du
        # sommaire, même si ses trois fichiers ont été effacés.
        if not any(path.is_file() for path in paths):
            raise RuntimeError(f'Archive déclarée introuvable : {slug}')
        if not all(path.is_file() for path in paths):
            raise RuntimeError(f'Édition incomplète ({slug}) : conserver la source et les deux lecteurs.')
        original = src.read_text(encoding='utf-8')
        study_html = critique.read_text(encoding='utf-8')
        scenes_html = scenes.read_text(encoding='utf-8')
        subject, historical_volume = TITLE.search(original), VOLUME.search(original)
        if (len(original) < 8000 or len(study_html) < 10000
                or len(scenes_html) < 5000 or not subject or not historical_volume
                or 'bibliograph' not in original.lower()
                or 'bibliograph' not in study_html.lower()
                or not re.search(r'moderne|contemporain', scenes_html, flags=re.I)):
            raise RuntimeError(f'Édition insuffisamment documentée : {slug}')
        title = re.sub(r'[*_\x60]', '', subject.group(1)).strip()
        records.append({
            'slug': slug, 'title': title, 'historical_volume': historical_volume.group(1),
            'critique': '/' + (BASE / f'{slug}-etude.html').as_posix(),
            'scenes': '/' + (BASE / f'{slug}-scenes-modernes.html').as_posix(),
        })
    return records


def install(root: Path, output: Path, slugs=SLUGS):
    """Crée le sommaire croisé dans le portail sans toucher aux textes sources."""
    root, output = Path(root), Path(output)
    records = verified_editions(root, output, slugs)
    theatre = output / 'theatre/index.html'
    if not theatre.is_file() or not records:
        return 0
    doc = BeautifulSoup(theatre.read_text(encoding='utf-8'), 'html.parser')
    main = doc.select_one('main article.content') or doc.select_one('main')
    if main is None:
        return 0
    for previous in main.select('#theatre-comedies-editions'):
        previous.decompose()
    cards = []
    for item in records:
        esc = lambda value: html.escape(value, quote=True)
        cards.append(
            f'<article class="mythos-theatre-edition" id="theatre-source-{esc(item["slug"])}">'
            f'<span class="mythos-theatre-edition-cote">Volume historique '
            f'{esc(item["historical_volume"])}</span>'
            f'<h3>{esc(item["title"])}</h3>'
            '<p>Une même archive conservée, deux lectures distinctes.</p>'
            '<nav aria-label="Versions du dossier">'
            f'<a href="{esc(item["critique"])}">Étude critique intégrale et bibliographie</a>'
            f'<a href="{esc(item["scenes"])}">Scènes modernes — créations distinctes</a>'
            f'<a href="/corpus/theatre-grec/comedies/{esc(item["slug"])}-source.md">Source intégrale (Markdown)</a>'
            '</nav></article>'
        )
    markup = (
        '<section id="theatre-comedies-editions" class="portal-section '
        'mythos-theatre-editions" aria-labelledby="theatre-comedies-editions-titre">'
        '<h2 id="theatre-comedies-editions-titre">Comédies perdues d’Aristophane : '
        'éditions critiques et scènes modernes</h2>'
        '<p class="section-intro">Dossiers complets déjà conservés dans MYTHOS. '
        'Les attestations anciennes, les hypothèses savantes et les scènes '
        'contemporaines sont explicitement distinguées ; les titres des '
        'volumes historiques ne sont pas de nouvelles attributions.</p>'
        '<figure class="mythos-theatre-archive-figure">' 
        '<img src="/media/2026/10/mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg" '
        'alt="Rondelles en terre cuite hellénistiques à masques théâtraux, Met 2001.767.1 et 2" '
        'loading="lazy" decoding="async">' 
        '<figcaption>Rondelles de terre cuite, Ier siècle avant notre ère, '
        'Metropolitan Museum of Art 2001.767.1–2. Image de réception hellénistique, '
        'non document d’une représentation d’Aristophane. '
        '<a href="https://www.metmuseum.org/art/collection/search/257595">Notice muséale</a> · '
        '<a href="https://commons.wikimedia.org/wiki/File:Terracotta_roundels_in_the_form_of_theatrical_masks_MET_DP343377.jpg">'
        'Photographie CC0</a>.</figcaption>'
        '</figure>'
        '<div class="mythos-theatre-editions-grid">' + ''.join(cards)
        + '</div></section>'
    )
    section = BeautifulSoup(markup, 'html.parser').section
    target = main.select_one('#pieces-perdues')
    if target:
        target.insert_before(section)
    else:
        main.append(section)
    for group in main.select('section.portal-section'):
        head = group.select_one('h2')
        grid = group.select_one('.portal-grid')
        if not head or not grid or head.get_text(' ', strip=True) != 'Choisir sa lecture':
            continue
        for old in grid.select('a[href="#theatre-comedies-editions"]'):
            old.decompose()
        card = BeautifulSoup(
            '<a class="portal-card" href="#theatre-comedies-editions">'
            '<span class="portal-card-kicker">DOSSIERS COMPLETS</span>'
            '<strong>Comédies perdues : éditions critiques</strong>'
            '<span>Études intégrales et scènes contemporaines classées séparément.</span>'
            '<span aria-hidden="true" class="card-indicator">↗</span></a>',
            'html.parser',
        ).a
        grid.append(card)
        break
    rendered = str(doc)
    # BeautifulSoup peut ajouter un saut de ligne au DOCTYPE à chaque passe.
    # Normaliser seulement cet espace de tête garantit l'idempotence des builds.
    rendered = re.sub(r'(?is)^(\s*<!doctype html>)\s*', r'\1\n', rendered)
    theatre.write_text(rendered, encoding='utf-8')
    # Navigation scientifique réciproque, ajoutée au rendu seulement : les
    # manuscrits sources et les textes des lecteurs demeurent inchangés.
    for item in records:
        for kind in ('critique', 'scenes'):
            page = output / item[kind].lstrip('/')
            document = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            main_reader = document.select_one('main') or document.select_one('article.dai-article')
            header = document.select_one('header.mythos-masthead')
            if main_reader is None or header is None or document.head is None:
                raise RuntimeError(f'Lecteur incomplet pour la navigation : {page}')
            text_before = main_reader.get_text(' ', strip=True)
            for old in document.select('[data-mythos-theatre-archive-nav]'):
                old.decompose()
            other = 'scenes' if kind == 'critique' else 'critique'
            label = 'Lire les créations contemporaines' if other == 'scenes' else 'Lire l’étude critique et sa bibliographie'
            source_url = '/corpus/theatre-grec/comedies/' + item['slug'] + '-source.md'
            nav = BeautifulSoup(
                '<nav class="mythos-theatre-archive-return" data-mythos-theatre-archive-nav="1" '
                'aria-label="Parcours documentaire de cette comédie perdue">'
                '<a href="/theatre/#theatre-source-' + html.escape(item['slug'], quote=True) + '">'
                '← Sommaire du théâtre grec</a>'
                '<a href="' + html.escape(item[other], quote=True) + '">' + label + '</a>'
                '<a href="' + html.escape(source_url, quote=True) + '">Manuscrit source intégral</a>'
                '</nav>', 'html.parser'
            ).nav
            header.insert_after(nav)
            if not document.head.select_one('link[href="/assets/mythos-theatre-archive.css"]'):
                link = document.new_tag('link', rel='stylesheet', href='/assets/mythos-theatre-archive.css')
                document.head.append(link)
            if main_reader.get_text(' ', strip=True) != text_before:
                raise RuntimeError(f'Texte de la comédie modifié : {page}')
            page.write_text(str(document), encoding='utf-8')
    portal = BeautifulSoup(theatre.read_text(encoding='utf-8'), 'html.parser')
    if portal.head is None:
        raise RuntimeError('Portail Théâtre : élément head manquant')
    if not portal.head.select_one('link[href="/assets/mythos-theatre-archive.css"]'):
        portal.head.append(portal.new_tag('link', rel='stylesheet', href='/assets/mythos-theatre-archive.css'))
    theatre.write_text(str(portal), encoding='utf-8')
    return len(records)


if __name__ == '__main__':
    print('Dossiers critiques accessibles :', install(Path('.'), Path('_site')))
