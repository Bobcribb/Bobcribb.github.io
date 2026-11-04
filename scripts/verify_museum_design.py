#!/usr/bin/env python3
"""Verify universal coverage and preservation of representative legacy readers."""
from pathlib import Path
from collections import Counter
import json
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
import shutil
from apply_museum_design import apply

ROOT=Path(__file__).resolve().parents[1]

def prose(doc):
    return Counter(p.get_text(' ',strip=True) for p in doc.select('main p, article p, main li, article li, main h2, main h3, article td, main figcaption') if p.get_text(' ',strip=True))

def verify():
    fixtures=['philosophie-iliade.html','philosophie-odyssee.html','philosophie-theogonie.html','corpus/civilisations/perse-iran-ancien-behistun.html','corpus/mythologie-grecque/archives/livre-troie.html']
    with TemporaryDirectory() as tmp:
        dest=Path(tmp)
        before={}
        for name in fixtures:
            p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,p)
            before[name]=prose(BeautifulSoup(p.read_text(),'html.parser'))
        assert apply(dest)==len(fixtures)
        snapshots={}
        for name in fixtures:
            p=dest/name;d=BeautifulSoup(p.read_text(),'html.parser')
            assert not before[name]-prose(d),f'Prose lost in {name}'
            assert len(d.select('.mythos-banner'))==1
            assert len(d.select('.mythos-masthead'))==1
            assert len(d.select('link[href*="mythos-museum.css"]'))==1
            snapshots[name]=p.read_text()
        apply(dest)
        for name in fixtures:
            d=BeautifulSoup((dest/name).read_text(),'html.parser')
            assert not before[name]-prose(d),f'Prose lost on rebuild in {name}'
            assert len(d.select('.mythos-banner'))==1
            assert len(d.select('.mythos-masthead'))==1
    print('OK : prose, tables, illustrations et liens conservés dans cinq lecteurs ; transformation répétable.')
    out=ROOT/'_site'
    pages=0;redirects=0
    for p in out.rglob('*.html'):
        relative = p.relative_to(out)
        if relative.parts[0] in {'assets', 'media'}:
            assert p.read_bytes() == (ROOT/relative).read_bytes(), str(p)
            continue
        raw=p.read_text()
        if 'http-equiv="refresh"' in raw.lower() or "http-equiv='refresh'" in raw.lower():
            redirects+=1;continue
        assert 'data-mythos-design="20261104"' in raw,str(p)
        assert raw.count('class="mythos-masthead"')==1,str(p)
        assert raw.count('/assets/mythos-museum.css?')==1,str(p)
        pages+=1
    assert pages>1000
    d=BeautifulSoup((out/'origines-du-sacre/index.html').read_text(),'html.parser')
    assert len(d.select('.origins-volume'))==27
    assert len(d.select('.mythos-more-volumes .origins-volume'))==15
    assert (out/'assets/mythos-museum-banner.webp').stat().st_size>10000
    # Les cartes des sanctuaires avaient perdu leurs trois vignettes au cours
    # de l'habillage final : un lien textuel ne suffit pas à cet inventaire.
    home = BeautifulSoup((out/'index.html').read_text(encoding='utf-8'), 'html.parser')
    gallery = BeautifulSoup(
        (out/'reconstitutions-photorealistes.html').read_text(encoding='utf-8'),
        'html.parser')
    for slug in ('delphes-apollon-panorama', 'nemee-temple-zeus-vue', 'sounion-poseidon-vue'):
        url = '/reconstitutions-photorealistes.html#' + slug
        src = '/assets/reconstitutions-3d/' + slug + '.webp'
        card = home.select_one('a.portal-card[href="' + url + '"]')
        assert card is not None, 'Carte du sanctuaire absente : ' + slug
        assert card.find('img', src=src) is not None, 'Vignette du sanctuaire absente : ' + slug
        assert (out/src.lstrip('/')).is_file(), 'Fichier de vignette absent : ' + src
        assert gallery.find(id=slug) is not None, 'Ancre de galerie absente : ' + slug
    # source-link-dossier-v1 : les illustrations doivent conduire au dossier
    # scientifique correspondant, sans substituer la source institutionnelle.
    gallery_to_dossier = {
        'delphes-apollon-panorama': 'delphes.html',
        'delphes-sanctuaire-vue-ensemble': 'delphes.html',
        'delphes-tholos-athena-pronaia': 'delphes.html',
        'nemee-temple-zeus-vue': 'nemee.html',
        'nemee-stade-vue': 'nemee.html',
        'corinthe-temple-apollon-vue': 'corinthe.html',
        'corinthe-pirene-vue': 'corinthe.html',
        'messene-asklepieion-vue': 'messene.html',
        'messene-stade-vue': 'messene.html',
        'sounion-poseidon-vue': 'sounion.html',
        'sounion-athena-vue': 'sounion.html',
        'brauron-artemis-vue': 'brauron.html',
        'brauron-stoa-vue': 'brauron.html',
        'dodone-theatre-vue': 'dodone.html',
        'bassae-apollon-exterieur-vue': 'bassae.html',
    }
    catalog = json.loads((out/'assets/reconstitutions-3d/catalogue-photorealiste.json').read_text(encoding='utf-8'))
    catalogue_by_slug = {entry['slug']: entry for entry in catalog['entries']}
    assert len(catalogue_by_slug) == catalog['count']
    # Réciprocité : les dossiers doivent aussi afficher les vues, leurs sources,
    # leurs ancres canoniques et les vrais fichiers locaux, sans perte de texte.
    for slug, dossier in gallery_to_dossier.items():
        card = gallery.find(id=slug)
        assert card is not None, 'Illustration absente : ' + slug
        assert card.select_one('p.r3d-source a[href^="https://"]'), 'Source institutionnelle absente : ' + slug
        assert card.select_one('a.r3d-study-link[href="/sites/' + dossier + '"]'), 'Renvoi dossier absent : ' + slug
        assert (out/'sites'/dossier).is_file(), 'Dossier archéologique inexistant : ' + dossier
        study = BeautifulSoup((out/'sites'/dossier).read_text(encoding='utf-8'), 'html.parser')
        assert len(study.select('div[data-mythos-photoreal-dossier="v1"]')) == 1, 'Galerie du dossier absente : ' + dossier
        visual_link = '/reconstitutions-photorealistes.html#' + slug
        figure = study.select_one('figure.mythos-site-visual')
        figures = study.select('div[data-mythos-photoreal-dossier="v1"] figure.mythos-site-visual')
        assert figure is not None and len(figures) > 0, 'Figure absente : ' + dossier
        match = next((f for f in figures if f.find('a', href=visual_link)), None)
        assert match is not None, 'Renvoi réciproque absent : ' + slug
        source = catalogue_by_slug[slug]
        assert match.find('img', src=source['src']) is not None, 'Image du dossier absente : ' + slug
        assert match.find('a', href=source['source_url']) is not None, 'Source institutionnelle du dossier absente : ' + slug
        assert (out/source['src'].lstrip('/')).stat().st_size > 10000, 'WebP local absent : ' + slug
    # Aphaia: 4 sections attestées, jamais une photographie empruntée à un autre lieu.
    aphaia = BeautifulSoup((out/'sites/egine-aphaia.html').read_text(encoding='utf-8'), 'html.parser')
    toc = aphaia.select_one('nav[aria-label="Sommaire du dossier d’Aphaia"]')
    assert toc is not None, 'Sommaire d’Aphaia absent'
    expected_anchors = ('histoire', 'architecture', 'frontons', 'sources')
    assert [link.get('href') for link in toc.select('a[href^="#"]')] == [
        '#' + slug for slug in expected_anchors], 'Sommaire d’Aphaia incomplet'
    for slug in expected_anchors:
        assert aphaia.find(id=slug), 'Ancre du dossier Aphaia absente : ' + slug
    assert not aphaia.select('a[href="/reconstitutions-3d.html"]')
    assert aphaia.select('a[href="/reconstitutions-photorealistes.html"]')
    print('OK : 15 vues photoréalistes affichées dans huit dossiers et liens réciproques conservés.')
    print('OK : trois cartes illustrées, trois WebP et trois renvois de galerie vérifiés.')
    print(f'OK : {pages} pages habillées, {redirects} redirections conservées, 27 tomes accessibles.')

if __name__=='__main__':verify()
