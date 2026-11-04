#!/usr/bin/env python3
"""Apply the approved MYTHOS museum identity to every public HTML page.

Presentation only: manuscript paragraphs, source links, IDs and media stay intact.
The final build pass also covers standalone .html files and future chapters.
"""
from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup
import html
import re

VERSION = '20261104'
MEDIA = '/media/2026/10/'
NAV = [('/mythologie-grecque/','Grèce'),('/dieux-et-deesses/','Dieux'),('/heros-et-heroines/','Héros'),('/recits-mythologiques/','Récits'),('/grande-encyclopedie/','Grande encyclopédie'),('/theatre/','Théâtre'),('/origines-du-sacre/','Origines du sacré'),('/philosophie/','Philosophie')]
MORE = [('/','Accueil'),*NAV,('/parcours/','Parcours de lecture'),('/catalogue-integral/','Catalogue intégral'),('/methode-editoriale/','Sources et méthode'),('/mythologie-comparee/','Mythologie comparée'),('/mythologies/','Mythologies du monde'),('/civilisations/','Civilisations'),('/reconstitutions-antiquite/','Reconstitutions'),('/rubriques/','Tous les dossiers'),('/recherche/','Recherche')]
PILLAR = '<svg viewBox="0 0 36 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 5h28M5 10h26M8 14h20M9 40h18M5 44h26M12 16v22M18 16v22M24 16v22M7 10C0 10 1 1 7 2h22c6-1 7 8 0 8M7 5c-3 0-3 3 0 3m22-3c3 0 3 3 0 3"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg>'
# Decorative collection covers are approved for these exact portals only.
# A chapter linked from a card must never inherit a civilisation-wide cover.
PICTURES = {
 '/mythologie-grecque/': 'delphes-temple-apollon-bernard-gagnon.jpg',
 '/grece/': 'delphes-temple-apollon-bernard-gagnon.jpg',
 '/dieux-et-deesses/': 'mythos-bronze-artemision-zeus-ou-poseidon.jpg',
 '/heros-et-heroines/': 'antigone-libation-rinehart-1870.jpg',
 '/recits-mythologiques/': 'mythos-hector-priam-rancon-briseis-peintre-british-museum-e75.jpg',
 '/grande-encyclopedie/': 'mythos-e28094-ceramique-grecque-a-figures-rouges.png',
 '/theatre/': 'epidaure-theatre-antique-zde.jpg',
 '/origines-du-sacre/': 'mythos-ounas-chambre-funeraire-vincent-brown.jpg',
 '/philosophie/': 'raphael-ecole-athenes-1511.jpg',
 # Six exact reading links: locally archived object photography, not 2.5D reconstructions.
 '/philosophie-iliade.html': 'mythos-iliade-achille-ajax-athena-hydrie-met-56-171-29.jpg',
 '/philosophie-odyssee.html': 'mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg',
 '/philosophie-theogonie.html': 'mythos-bronze-artemision-zeus-ou-poseidon.jpg',
 '/parcours/decouvrir-les-mythes-grecs/': 'mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg',
 '/parcours/comprendre-la-tragedie/': 'mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg',
 '/parcours/comparer-les-creations-du-monde/': 'mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg',
 '/mythologie-comparee/': 'mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg',
 '/bibliotheque-egypte-ancienne/': 'mythos-papyrus-ani-pesee-coeur-british-museum.jpg',
 '/bibliotheque-mesopotamie/': 'gilgamesh-tablette-deluge-british-museum-babelstone.jpg',
 '/bibliotheque-perse-iran-ancien/': 'mythos-persepolis-apadana-delegations-pentocelo-2006.jpg',
 '/reconstitutions-antiquite/': '/assets/reconstitutions-3d/delphes-apollon-panorama.webp',
}

def picture(url, root):
    name = PICTURES.get(url)
    if name and name.startswith('/assets/reconstitutions-3d/') and name.endswith('.webp'):
        return name if (root / name.lstrip('/')).is_file() else None
    if name and (root / 'media/2026/10' / name).is_file():
        return MEDIA + name
    return None

def cover(url, root):
    src = picture(url, root)
    return '<img src="'+src+'" alt="" loading="lazy">' if src else ''

def fragment(markup):
    return BeautifulSoup(markup, 'html.parser')

def header(url):
    def links(items, active=False):
        return ''.join('<a href="'+html.escape(href)+'"'+(' aria-current="page"' if active and (url == href or url.startswith(href) and href != '/') else '')+'>'+html.escape(label)+'</a>' for href,label in items)
    return fragment('<header class="mythos-masthead"><a class="mythos-brand" href="/" aria-label="MYTHOS — Accueil">'+PILLAR+'<span>MYTHOS<small>ENCYCLOPÉDIE DES MYTHOLOGIES</small></span></a><nav class="mythos-primary-nav" aria-label="Navigation principale">'+links(NAV,True)+'</nav><div class="mythos-header-tools"><a class="mythos-search-link" href="/recherche/" aria-label="Rechercher dans MYTHOS">'+SEARCH+'</a><details class="mythos-menu"><summary aria-label="Ouvrir le menu"><span></span><span></span><span></span></summary><nav aria-label="Toutes les rubriques">'+links(MORE,True)+'</nav></details></div></header>').header

PORTALS = {'/','/origines-du-sacre/','/mythologie-grecque/','/grece/','/grande-encyclopedie/','/theatre/','/philosophie/','/mythologie-comparee/','/dieux-et-deesses/','/heros-et-heroines/','/recits-mythologiques/','/civilisations/','/mythologies/','/reconstitutions-antiquite/','/rubriques/','/recherche/'}
# Unique SEO descriptions for the six principal public portals.
# Do not override article metadata or authored descriptions.
GENERIC_DESCRIPTION = 'MYTHOS — Encyclopédie des mythologies du monde : sources, peuples, récits, théâtre et philosophie.'
PORTAL_DESCRIPTIONS = {
    '/': 'MYTHOS : encyclopédie des mythologies, théâtre grec, philosophie, sources et parcours de lecture.',
    '/mythologie-grecque/': 'Mythologie grecque : dieux, héros, cycles, manuscrits universitaires et archives de MYTHOS.',
    '/grande-encyclopedie/': 'Grande Encyclopédie mythologique grecque : chapitres, livres, sources, bibliographies et archives.',
    '/origines-du-sacre/': 'Origines du sacré : 27 tomes, rites, archéologie et textes des religions anciennes.',
    '/theatre/': 'Théâtre grec : tragédies, comédies, fragments, études philosophiques et bibliographies.',
    '/philosophie/': 'Philosophie MYTHOS : études de l’Iliade, de l’Odyssée, de la Théogonie et des pensées antiques.',
}


def apply(root):
    root = Path(root)
    count = 0
    for path in sorted(root.rglob('*.html')):
        # Les pièces jointes restent des sources immuables, même en HTML.
        if path.relative_to(root).parts[0] in {'assets', 'media'}:
            continue
        doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        if not doc.body or not doc.head or doc.select_one('meta[http-equiv="refresh" i]'):
            continue
        rel = path.relative_to(root).as_posix()
        url = '/' + (rel[:-10] if rel.endswith('index.html') else rel)
        portal_url = '/' if url == '/' else url.removesuffix('.html').rstrip('/') + '/'
        portal = portal_url in PORTALS or portal_url.startswith(('/parcours/', '/catalogue-integral/', '/etat-du-corpus/', '/methode-editoriale/'))
        description = doc.head.select_one('meta[name="description"]')
        if (description and description.get('content') == GENERIC_DESCRIPTION
                and portal_url in PORTAL_DESCRIPTIONS):
            description['content'] = PORTAL_DESCRIPTIONS[portal_url]
        # Idempotent: an already transformed static page keeps its hero and title.
        old_hero = doc.select_one('.mythos-banner')
        heading = old_hero.h1 if old_hero else doc.h1
        if not heading:
            heading = doc.new_tag('h1')
            heading.string = doc.title.get_text(' ', strip=True).split('|')[0].strip() if doc.title else 'MYTHOS'
        # Only old chrome is replaced, never article headers or article navigation.
        for old in doc.select('.masthead, .mythos-masthead, .mythos-skip'):
            old.decompose()
        for legacy_header in list(doc.find_all('header')):
            if legacy_header.select_one('.brand') and not legacy_header.find('h1'):
                legacy_header.decompose()
        old_parent = heading.parent
        heading.extract()
        if old_hero:
            old_hero.decompose()
        else:
            hero = old_parent
            while hero and hero.name not in ('body', 'main', 'article'):
                if any(c in hero.get('class',[]) for c in ('hero-editorial','origins-hero','hero-archive','hero','page-title','article-head')) or hero.name == 'header':
                    hero['class'] = list(dict.fromkeys(hero.get('class',[]) + ['mythos-original-intro']))
                    break
                hero = hero.parent
        for old in doc.select('link[href*="mythos-museum.css"]'):
            old.decompose()
        doc.head.append(doc.new_tag('link', rel='stylesheet', href='/assets/mythos-museum.css?v='+VERSION))
        # Preserve authored canonical links, and skip redirects and the 404 page.
        # Alias portals that also have a /directory/ edition use that single URL.
        if rel != '404.html' and not doc.head.select_one('link[rel~="canonical"]'):
            canonical_path = url
            if (rel.endswith('.html') and portal_url in PORTALS
                    and (root / portal_url.lstrip('/') / 'index.html').is_file()):
                canonical_path = portal_url
            doc.head.append(doc.new_tag('link', rel='canonical',
                href='https://bobmythos.fr' + quote(canonical_path, safe='/-._~')))
        doc.body['class'] = list(dict.fromkeys(doc.body.get('class',[]) + ['mythos-design', 'mythos-portal' if portal else 'mythos-reading']))
        doc.body['data-mythos-design'] = VERSION
        # Les anciens dossiers emploient parfois « Revenir en haut » via #top
        # sans cible réelle. L'ancre sur body reste stable après reconstruction
        # et n'ajoute aucun élément visible au texte universitaire.
        if doc.select_one('a[href="#top"]') and not doc.find(id='top'):
            if not doc.body.get('id'):
                doc.body['id'] = 'top'
            else:
                doc.body.insert(0, doc.new_tag('span', id='top'))
        # Les trois éditions philosophiques possèdent un vrai H1 dans la
        # bannière ET un titre dédié à l'impression. Réserver H1 au bandeau,
        # conserver l'intitulé imprimé en H2 sans changer les paragraphes.
        if rel in {'philosophie-iliade.html', 'philosophie-odyssee.html',
                   'philosophie-theogonie.html'}:
            for print_heading in doc.select('main h1.print-title'):
                print_heading.name = 'h2'
        main = doc.main or doc.select_one('article, .container, .article-wrapper')
        if main and not main.get('id'):
            main['id'] = 'mythos-content' if doc.find(id='contenu') else 'contenu'
        if main and len(doc.find_all(id=main.get('id'))) > 1:
            main['id'] = 'mythos-content'
        target = main.get('id') if main else 'mythos-page-title'
        skip = doc.new_tag('a', href='#'+target, attrs={'class':'mythos-skip'})
        skip.string = 'Aller au contenu'
        top = header(portal_url)
        doc.body.insert(0, top)
        doc.body.insert(0, skip)
        banner = doc.new_tag('section', attrs={'class':'mythos-banner', 'aria-label':'Présentation de la page'})
        inner = doc.new_tag('div', attrs={'class':'mythos-banner-inner'})
        if not heading.get('id'):
            heading['id'] = 'mythos-page-title'
        heading['class'] = list(dict.fromkeys(heading.get('class',[]) + ['mythos-banner-title']))
        if url == '/':
            heading.clear()
            heading.string = 'MYTHOS'
        if len(heading.get_text(' ',strip=True)) > 65:
            banner['class'].append('mythos-banner-long')
        inner.append(heading)
        rule = doc.new_tag('span', attrs={'class':'mythos-banner-rule','aria-hidden':'true'})
        rule.string = '◇'
        inner.append(rule)
        subtitle = doc.new_tag('p', attrs={'class':'mythos-banner-subtitle'})
        subtitle.string = ('Encyclopédie des mythologies' if url == '/' else 'Bibliothèque intégrale de recherche' if 'origines-du-sacre' in portal_url and portal else 'Mythes, textes et civilisations' if portal else 'MYTHOS · Textes, sources et interprétations')
        inner.append(subtitle)
        if url == '/' or portal_url == '/origines-du-sacre/':
            intro = doc.new_tag('p', attrs={'class':'mythos-banner-deck'})
            intro.string = ('Des dieux et des héros aux grandes civilisations, une exploration des mythes, du théâtre et de la philosophie.' if url == '/' else 'Des premiers rituels aux grandes religions, une exploration approfondie des origines du sacré à travers les civilisations, les mythes et les cultures.')
            inner.append(intro)
        banner.append(inner)
        top.insert_after(banner)
        # Respecter un seul titre H1 par page : les titres internes des études
        # conservent leur texte, ancres et renvois bibliographiques. Seul le
        # niveau sémantique change, jamais le contenu universitaire.
        if main:
            for inner_heading in main.select('h1'):
                inner_heading.name = 'h2'
        # Keep all iconography; display it below the text as a horizontal gallery.
        for rail in doc.select('.mythos-visual-rail, .mythos-home-illustrations, .article-aside'):
            rail['class'] = list(dict.fromkeys(rail.get('class',[]) + ['mythos-bottom-gallery']))
        # Remove presentation-only empty wrappers and redundant decorative eyebrow.
        for eyebrow in doc.select('article.content > .eyebrow'):
            eyebrow['class'].append('mythos-chrome-label')
        # Six-column illustrated directory reproduces the reference card rhythm.
        if url == '/' and not doc.select_one('.mythos-directory'):
            items = [*NAV,('/mythologie-comparee/','Mythologie comparée'),('/bibliotheque-egypte-ancienne/','Égypte ancienne'),('/bibliotheque-mesopotamie/','Mésopotamie'),('/reconstitutions-antiquite/','Reconstitutions')]
            section = fragment('<section class="mythos-directory"><h2>Les collections de MYTHOS</h2><p>Une bibliothèque pour explorer les mythes, les rites, les œuvres et les sociétés.</p><div class="mythos-collection-grid">'+''.join('<a class="mythos-collection-card" href="'+u+'">'+cover(u,root)+'<span><strong>'+t+'</strong><span aria-hidden="true">→</span></span></a>' for u,t in items)+'</div></section>').section
            banner.insert_after(section)
        for card in doc.select('.portal-card'):
            # A gallery card can point to a verified photorealistic WebP outside
            # the collection-cover map. Preserve that authored photograph: an
            # earlier pass discarded it and silently left the card without art.
            # Do not retain legacy 2.5D/vector thumbnails from older pages.
            authored = card.select_one('img.mythos-card-image')
            if authored:
                image_path = authored.get('src', '').split('?', 1)[0]
                if (image_path.startswith('/assets/reconstitutions-3d/')
                        and image_path.endswith('.webp')
                        and (root / image_path.lstrip('/')).is_file()):
                    continue
            for old in card.select('img.mythos-card-image'):
                old.decompose()
            src = picture(card.get('href', ''), root)
            if src and not card.find('img'):
                card.insert(0, doc.new_tag('img', src=src, alt='', loading='lazy', attrs={'class':'mythos-card-image'}))
        grid = doc.select_one('.origins-volume-grid')
        if grid and len(grid.select(':scope > .origins-volume')) > 12:
            more = fragment('<details class="mythos-more-volumes"><summary>… jusqu’au tome XXVII <span aria-hidden="true">→</span></summary><div class="origins-volume-grid"></div></details>').details
            more_grid = more.div
            for volume in list(grid.select(':scope > .origins-volume'))[12:]:
                more_grid.append(volume.extract())
            grid.insert_after(more)
        # Shared keyboard behaviour for the native menu; no client-side theming.
        if not doc.select_one('script[src*="mythos-museum.js"]'):
            doc.body.append(doc.new_tag('script', src='/assets/mythos-museum.js?v='+VERSION, defer=''))
        path.write_text(str(doc), encoding='utf-8')
        count += 1
    return count

if __name__ == '__main__':
    import sys
    print('Habillage muséal :', apply(sys.argv[1] if len(sys.argv)>1 else '_site'), 'pages')
