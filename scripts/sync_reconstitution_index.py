#!/usr/bin/env python3
"""Synchroniser le sommaire illustré avec les notices 3D photoréalistes.

La galerie conserve ses notices, sources, légendes et images d'origine.
La synchronisation ajoute uniquement les vignettes absentes du sommaire.
Elle est déterministe et idempotente pour les deux modes de publication.
"""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import sys

GRID = '<div class="r3d-index-grid">'
CARD = re.compile(r'<div class="r3d-index-card">.*?</div>', re.DOTALL)
LINK = re.compile(r'class="r3d-index-image" href="#([^"]+)"')
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def sync_index(root: str | Path) -> int:
    root = Path(root)
    gallery_path = root / 'reconstitutions-photorealistes.html'
    catalog_path = root / 'assets/reconstitutions-3d/catalogue-photorealiste.json'
    markup = gallery_path.read_text(encoding='utf-8')
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    entries = catalog['entries']
    if catalog.get('count') != len(entries):
        raise ValueError('Catalogue 3D : compteur incohérent')
    if markup.count(GRID) != 1:
        raise ValueError('Sommaire illustré absent ou dupliqué')
    start = markup.index(GRID) + len(GRID)
    nav_end = markup.index('</nav>', start)
    end = markup.rfind('</div>', start, nav_end)
    if end < start:
        raise ValueError('Grille 3D non fermée')
    inner = markup[start:end]
    links = LINK.findall(inner)
    if len(set(links)) != len(links):
        raise ValueError('Ancres du sommaire 3D dupliquées')
    existing = set(links)
    added = 0
    for item in entries:
        slug = item['slug']
        src = item['src']
        title = item['title']
        source = item.get('source_url', '')
        if not SLUG.fullmatch(slug):
            raise ValueError('Identifiant 3D invalide : ' + slug)
        if not src.startswith('/assets/reconstitutions-3d/') or not src.endswith('.webp'):
            raise ValueError('Image 3D invalide : ' + src)
        if 'id="' + slug + '"' not in markup:
            raise ValueError('Notice 3D sans ancre : ' + slug)
        if slug in existing:
            continue
        label = escape(title)
        card = (
            '<div class="r3d-index-card"><a class="r3d-index-image" href="#'
            + escape(slug, quote=True) + '"><img alt="" decoding="async" loading="lazy" src="'
            + escape(src, quote=True) + '"/><strong>' + label
            + '</strong><span>Voir la reconstitution ↓</span></a>'
        )
        if source.startswith('https://'):
            card += ('<a class="r3d-index-dossier" href="'
                     + escape(source, quote=True)
                     + '" rel="noopener noreferrer" target="_blank">'
                     'Source archéologique ↗</a>')
        card += '</div>'
        # Regrouper les vues appartenant à une même localité.
        prefix = slug.split('-', 1)[0] + '-'
        same_place = [match for match in CARD.finditer(inner)
                      if any(anchor.startswith(prefix)
                             for anchor in LINK.findall(match.group()))]
        if same_place:
            offset = same_place[-1].end()
            inner = inner[:offset] + '\n' + card + inner[offset:]
        else:
            inner = '\n' + card + inner
        existing.add(slug)
        added += 1
    # The source gallery can lag behind concurrent additions: the published
    # count must reflect the inventory, never a manually maintained number.
    updated = markup[:start] + inner + markup[end:] if added else markup
    count = len(entries)
    updated = re.sub(
        r'(?<=<strong>État du corpus : )\d+ reconstitutions?(?=\.</strong>)',
        f'{count} reconstitution' + ('s' if count != 1 else ''),
        updated, count=1,
    )
    if updated != markup:
        gallery_path.write_text(updated, encoding='utf-8')
    return added


if __name__ == '__main__':
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('_site')
    print('Vignettes 3D ajoutées au sommaire :', sync_index(base))
