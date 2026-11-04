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
            heading = (re.search(r'(?m)^##\s+(.+)$', markdown)
                       or re.search(r'(?m)^#\s+(.+)$', markdown))
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
                          'url': '/' + rel.with_suffix('').as_posix() + '/', 'image': src})
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
        img = (f'<img class="mythos-card-image" loading="lazy" decoding="async" alt="" '
               f'src="{html.escape(item["image"], quote=True)}"/>' if item['image'] else '')
        cards.append(
            f'<a class="portal-card" href="{html.escape(item["url"], quote=True)}">{img}'
            f'<span class="portal-card-kicker">{html.escape(item["collection"])} · '
            f'{html.escape(item["cote"])}</span>'
            f'<strong>{html.escape(item["title"])}</strong>'
            '<span>Consulter la monographie universitaire et ses références.</span>'
            '<span class="card-indicator" aria-hidden="true">↗</span></a>')
    markup = ('<section class="portal-section" id="home-etudes-recentes">'
              '<h2>Dernières études par collection</h2>'
              '<p class="section-intro">Un accès direct au dernier numéro attribué '
              'et construit dans chacune des cinq collections universitaires. '
              'Les textes, notes et bibliographies restent à leur emplacement d’origine.</p>'
              '<div class="portal-grid">' + ''.join(cards) + '</div></section>')
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
    return len(records)
