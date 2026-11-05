"""Mettre en avant les derniers manuscrits attribués, sans rééditer les sources.

Ce panneau est purement navigant. Seuls les reçus de `editorial/numbering.json`
avec un Markdown complet et un lecteur effectivement construit sont sélectionnés.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Images déjà publiées et sourcées dans les bibliothèques MYTHOS.
COLLECTIONS = (
    ('origines-du-sacre', 'Origines du sacré', 'mythos-ounas-chambre-funeraire-vincent-brown.jpg', False),
    ('encyclopedie', 'Encyclopédie grecque', 'delphes-temple-apollon-bernard-gagnon.jpg', False),
    ('comedies', 'Comédies grecques', 'mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg', True),
    ('tragedies', 'Tragédies grecques', 'epidaure-theatre-antique-zde.jpg', True),
    ('comparatif', 'Études comparatives', 'mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg', True),
)

# Images de collection : ces documents ne représentent pas nécessairement
# le sujet précis du dernier chapitre. Ne pas les légender comme tels.
IMAGE_CONTEXT = {
    'origines-du-sacre': "Chambre funéraire d’Ounas, Saqqara",
    'encyclopedie': "Vestiges du temple d’Apollon à Delphes",
    'comedies': "Masques de théâtre hellénistiques, Metropolitan Museum of Art",
    'tragedies': "Théâtre antique d’Épidaure",
    'comparatif': "Tablette de l’Enūma eliš, musée britannique",
}
COLLECTION_HOME = {
    'origines-du-sacre': '/origines-du-sacre/',
    'encyclopedie': '/mythologie-grecque/',
    'comedies': '/theatre/',
    'tragedies': '/theatre/',
    'comparatif': '/mythologie-comparee/',
}


def roman(number):
    parts = ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
             (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
             (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'))
    result = ''
    for value, symbol in parts:
        count, number = divmod(number, value)
        result += symbol * count
    return result


def latest_verified(root, output):
    """Receipts only; no guesses based on older summaries or unassigned inbox."""
    root, output = Path(root), Path(output)
    registry = json.loads((root / 'editorial/numbering.json').read_text(encoding='utf-8'))
    found = []
    for collection, label, image, roman_numbering in COLLECTIONS:
        receipts = registry.get('collections', {}).get(collection, {}).get('allocations', {})
        for item in sorted(receipts.values(), key=lambda x: int(x.get('number', 0)), reverse=True):
            number = item.get('number')
            rel = Path(item.get('path', ''))
            if (not isinstance(number, int) or number <= 0 or len(rel.parts) != 3
                    or rel.parts[:2] != ('chapitres', collection) or rel.suffix != '.md'):
                continue
            source = root / rel
            reader = output / rel.with_suffix('') / 'index.html'
            if not source.is_file() or not reader.is_file():
                continue
            markdown = source.read_text(encoding='utf-8')
            # Une notice, un ancien sommaire ou une demande conservée en attente
            # ne doit jamais apparaître comme une nouvelle étude intégrale.
            if len(markdown) < 2000:
                continue
            # L'encyclopédie place le titre scientifique en H1 (par exemple,
            # « Chapitre 409 — Agathos Daimôn ») et les sections en H2.
            # Dans les quatre autres collections, le titre est généralement
            # le premier H2, après un H1 décrivant le cycle et son numéro.
            first_h1 = re.search(r'(?m)^#\s+(.+)$', markdown)
            first_h2 = re.search(r'(?m)^##\s+(.+)$', markdown)
            h1_text = re.sub(r'[`*_]', '', first_h1.group(1)).strip() if first_h1 else ''
            # Les Origines et l'encyclopédie utilisent toutes deux un H1
            # scientifique « Chapitre N — titre ». Un H2 « Résumé
            # scientifique » ne doit jamais remplacer ce titre sur l'accueil.
            titled_chapter = bool(re.match(
                r'(?i)^chapitre\s+\d+\s+[—:-]\s+\S+', h1_text))
            heading = first_h1 if titled_chapter else (first_h2 or first_h1)
            if not heading:
                continue
            title = re.sub(r'[`*_]', '', heading.group(1)).strip()
            if not title:
                continue
            src = '/media/2026/10/' + image
            if not (output / src.lstrip('/')).is_file():
                src = ''
            cote = 'Volume ' + roman(number) + f' ({number})' if roman_numbering else f'Chapitre {number}'
            found.append({'collection': label, 'cote': cote, 'title': title,
                          'url': '/' + rel.with_suffix('').as_posix() + '/', 'image': src,
                          'illustration': IMAGE_CONTEXT[collection] if src else '',
                          'collection_url': COLLECTION_HOME[collection],
                          'anchor': 'etude-recente-' + collection})
            break
    return found


def install(root, output):
    """Ajoute des cartes responsive et un renvoi au sommaire, sans toucher aux études."""
    root, output = Path(root), Path(output)
    records = latest_verified(root, output)
    if not records:
        return 0
    home = output / 'index.html'
    if not home.is_file():
        return 0
    doc = BeautifulSoup(home.read_text(encoding='utf-8'), 'html.parser')
    main = doc.select_one('main article.content')
    if not main:
        return 0
    for previous in main.select('section#home-etudes-recentes'):
        previous.decompose()
    cards = []
    for item in records:
        img = (
            '<span class="mythos-recent-illustration">'
            f'<img class="mythos-card-image" loading="lazy" decoding="async" '
            f'alt="{html.escape(item["illustration"], quote=True)}" '
            f'src="{html.escape(item["image"], quote=True)}"/>'
            '<span class="mythos-recent-caption">Repère iconographique de la collection : '
            f'{html.escape(item["illustration"])}. '
            'Cette image ne représente pas nécessairement l’étude.</span></span>'
            if item['image'] else '')
        cards.append(
            f'<a class="portal-card" id="{html.escape(item["anchor"], quote=True)}" '
            f'href="{html.escape(item["url"], quote=True)}">{img}'
            f'<span class="portal-card-kicker">{html.escape(item["collection"])} · '
            f'{html.escape(item["cote"])}</span>'
            f'<strong>{html.escape(item["title"])}</strong>'
            '<span>Consulter la monographie universitaire et ses références.</span>'
            '<span class="card-indicator" aria-hidden="true">↗</span></a>')
    # Sous-sommaire accessible sur mobile : cibles stables par collection,
    # sans ajouter de copie du manuscrit ni de lien non attribué.
    quick_nav = (
        '<nav class="mythos-recent-jump" '
        'aria-label="Accès rapide aux études récentes par collection"><ul>'
        + ''.join(
            f'<li><a href="#{html.escape(item["anchor"], quote=True)}">'
            f'{html.escape(item["collection"])}</a></li>'
            for item in records
        )
        + '</ul></nav>'
    )
    markup = ('<section class="portal-section" id="home-etudes-recentes">'
              '<h2>Dernières études par collection</h2>'
              '<p class="section-intro">Un accès direct au dernier numéro attribué '
              'et construit dans chacune des cinq collections universitaires. '
              'Les textes, notes et bibliographies restent à leur emplacement d’origine.</p>'
              quick_nav + '<div class="portal-grid">' + ''.join(cards) + '</div></section>')
    section = BeautifulSoup(markup, 'html.parser').section
    anchor = main.select_one('#home-parcours')
    if anchor:
        anchor.insert_after(section)
    else:
        main.insert(0, section)
    toc = doc.select_one('nav.mythos-home-toc ul')
    if toc:
        for old in toc.select('a[href="#home-etudes-recentes"]'):
            old.parent.decompose()
        li = doc.new_tag('li')
        link = doc.new_tag('a', href='#home-etudes-recentes')
        link.string = 'Dernières études par collection'
        li.append(link)
        reference = toc.select_one('a[href="#home-oeuvres"]')
        if reference:
            reference.parent.insert_before(li)
        else:
            toc.append(li)
    home.write_text(str(doc), encoding='utf-8')

    # Renvoi réciproque ajouté seulement aux copies HTML générées :
    # les Markdown scientifiques et leurs bibliographies restent intacts.
    # data-reading-owned l'exclut des empreintes et des index de textes.
    for item in records:
        reader = output / item['url'].lstrip('/') / 'index.html'
        reader_doc = BeautifulSoup(reader.read_text(encoding='utf-8'), 'html.parser')
        article = (reader_doc.select_one('main article.content')
                   or reader_doc.select_one('main')
                   or reader_doc.select_one('article'))
        if article is None:
            continue
        for existing in article.select('nav[data-mythos-recent-backlinks]'):
            existing.decompose()
        back = (
            '<nav class="mythos-recent-backlinks" data-mythos-recent-backlinks="true" '
            'data-reading-owned="true" aria-label="Poursuivre la lecture">'
            '<span>Parcours MYTHOS</span>'
            '<a href="/#home-etudes-recentes">Dernières études universitaires</a>'
            f'<a href="{html.escape(item["collection_url"], quote=True)}">'
            'Explorer la collection</a></nav>'
        )
        article.append(BeautifulSoup(back, 'html.parser').nav)
        reader.write_text(str(reader_doc), encoding='utf-8')
    return len(records)
