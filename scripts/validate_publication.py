#!/usr/bin/env python3
"""Contrôles de publication, exécutés sur chaque reconstruction de main."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def validate():
    romans = ['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx','xxi','xxii','xxiii','xxiv','xxv','xxvi','xxvii']
    special = {'i': 'tome-i-hohle-fels', 'ii': 'tome-ii-prehistoire-du-sacre', 'iii': 'tome-iii-corps-caverne-mondes-invisibles'}
    portal = Path('_site/origines-du-sacre/index.html').read_text(encoding='utf-8')
    for i, roman in enumerate(romans, 1):
        slug = special.get(roman, f'tome-{roman}')
        source = Path(f'chapitres/origines-du-sacre/archives-integrales/{slug}.md')
        rendered = Path(f'_site/chapitres/origines-du-sacre/archives-integrales/{slug}/index.html')
        assert source.is_file() and source.stat().st_size > 10000, f'Tome {i} : source manquante ou incomplète'
        assert rendered.is_file() and rendered.stat().st_size > 10000, f'Tome {i} : page non générée'
        assert f'/chapitres/origines-du-sacre/archives-integrales/{slug}/' in portal, f'Lien absent : {roman}'
    print('OK : 27 tomes complets, 27 pages générées, 27 liens dans le sommaire')

    docs = json.loads(Path('_site/search.json').read_text(encoding='utf-8'))
    media = json.loads(Path('_site/media/manifest.json').read_text(encoding='utf-8'))
    assert len(docs) >= 500, f'Catalogue incomplet : {len(docs)}'
    assert media['count'] == 110, f"Médiathèque incomplète : {media['count']}"
    assert len(list(Path('_site/media/2026/10').glob('*'))) >= 110
    assert Path('_site/CNAME').read_text().strip() == 'bobmythos.fr'
    aton = Path('_site/akhetaton-horizon-aton-etude/index.html')
    assert aton.is_file() and '/media/2026/10/' in aton.read_text(encoding='utf-8')
    print('OK :', len(docs), 'dossiers, 110 médias, aucun appel WordPress')

    # Vérifier l'inclusion de chaque manuscrit, pas seulement un seuil global.
    indexed = {doc['url'] for doc in docs}
    sitemap = {node.text for node in ET.parse('_site/sitemap.xml').findall('.//{*}loc')}
    from editorial_numbering import scan, redirects
    scan(Path.cwd())
    aliases = redirects(Path.cwd())
    assert not (set(aliases) & indexed), "Adresses historiques dans la recherche"
    for old, target in aliases.items():
        assert target in indexed, f"Cible canonique non indexée : {target}"
        assert 'https://bobmythos.fr' + old not in sitemap, f"Ancienne adresse dans le sitemap : {old}"
    chapters = 0
    for source in Path('chapitres').rglob('*.md'):
        if source.name.lower() == 'readme.md':
            continue
        url = '/' + source.with_suffix('').as_posix() + '/'
        assert (Path('_site') / url.lstrip('/') / 'index.html').is_file(), f'Chapitre non généré : {source}'
        if url in aliases:
            chapters += 1
            continue
        assert url in indexed, f'Chapitre absent de la recherche : {source}'
        assert 'https://bobmythos.fr' + url in sitemap, f'Chapitre absent du sitemap : {source}'
        chapters += 1
    print(f'OK : {chapters} manuscrits conservés ; références canoniques dans la recherche et le sitemap')
    from verify_publication import verify
    verify()


if __name__ == '__main__':
    validate()
