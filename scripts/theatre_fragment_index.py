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
    return len(records)


if __name__ == '__main__':
    print('Dossiers critiques accessibles :', install(Path('.'), Path('_site')))
