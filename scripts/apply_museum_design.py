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
# One public entrance for the Greek encyclopedia. Historical readers remain
# available, but must never become a second collection in either shared menu.
NAV = [('/mythologie-grecque/','Encyclopédie grecque'),('/dieux-et-deesses/','Dieux'),('/heros-et-heroines/','Héros'),('/recits-mythologiques/','Récits'),('/theatre/','Théâtre'),('/origines-du-sacre/','Origines du sacré'),('/philosophie/','Philosophie')]
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
    if url.startswith('/grande-encyclopedie/') or url == '/grande-encyclopedie.html' or url.startswith('/chapitres/encyclopedie/'):
        url = '/mythologie-grecque/'
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


def add_scholarly_toc(doc, main, rel):
    """Sommaire de lecture pour les études publiées, sans modifier leur source."""
    if not main or not (rel.startswith('chapitres/') and rel.endswith('/index.html')):
        return
    article = main.select_one('article.content') or main
    # La reconstruction doit produire exactement un sommaire automatique.
    for old in article.select('nav.mythos-scholarly-toc'):
        old.decompose()
    # Ne pas doubler un sommaire d'auteur, ni déplacer ses références.
    if article.select_one('.toc, .article-toc, .table-of-contents, nav[aria-label*="ommaire"]'):
        return
    headings = [node for node in article.find_all('h2')
                if not node.find_parent(['nav', 'aside', 'footer'])
                and node.get_text(' ', strip=True)]
    if any(re.match(r'^(sommaire|table des mati[eè]res|plan de (?:l[’\']|la )étude)\\b',
                    node.get_text(' ', strip=True), re.I) for node in headings):
        return
    # Sommaires compacts : conserver les plans détaillés déjà rédigés au-delà
    # de 32 rubriques, plutôt que les remplacer par une liste tronquée.
    if not 3 <= len(headings) <= 32:
        return
    existing = {node.get('id') for node in doc.find_all(id=True)}
    targets = []
    for position, node in enumerate(headings, 1):
        anchor = node.get('id')
        if not anchor:
            original_anchor = node.find(id=True)
            anchor = original_anchor.get('id') if original_anchor else None
        if anchor and len(doc.find_all(id=anchor)) != 1:
            return  # Ancres déjà ambiguës : ne pas fabriquer de lien incertain.
        if not anchor:
            candidate = f'mythos-section-{position}'
            while candidate in existing:
                candidate += '-bis'
            node['id'] = candidate
            anchor = candidate
            existing.add(anchor)
        targets.append((anchor, node.get_text(' ', strip=True)))
    toc = doc.new_tag('nav', attrs={
        'class': 'mythos-scholarly-toc',
        'aria-label': 'Sommaire de l’étude',
    })
    label = doc.new_tag('p', attrs={'class': 'mythos-scholarly-toc-title'})
    label.string = 'Dans cette étude'
    toc.append(label)
    ordered = doc.new_tag('ol')
    for anchor, title in targets:
        item = doc.new_tag('li')
        link = doc.new_tag('a', href='#' + anchor)
        link.string = title
        item.append(link)
        ordered.append(item)
    toc.append(ordered)
    article.insert(0, toc)


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
        # Normalize the two old 2.5D/vector decorative illustrations on
        # the rendered page only. Linked historical source files and
        # original scholarly text are not modified by this presentation pass.
        legacy_art = ('/assets/mythos-hero.svg', '/assets/mythos-archaeology-tiles.svg')
        museum_banner = '/assets/mythos-museum-banner.webp'
        for img in doc.find_all('img', src=True):
            if img['src'].split('?', 1)[0] in legacy_art:
                img['src'] = museum_banner
        for element in doc.find_all(style=True):
            if any(old in element['style'] for old in legacy_art):
                for old in legacy_art:
                    element['style'] = element['style'].replace(old, museum_banner)
        for style in doc.find_all('style'):
            if style.string and any(old in style.string for old in legacy_art):
                css = str(style.string)
                for old in legacy_art:
                    css = css.replace(old, museum_banner)
                style.string = css
        rel = path.relative_to(root).as_posix()
        url = '/' + (rel[:-10] if rel.endswith('index.html') else rel)
        portal_url = '/' if url == '/' else url.removesuffix('.html').rstrip('/') + '/'
        portal = portal_url in PORTALS or portal_url.startswith(('/mythologie-grecque/dossiers/', '/parcours/', '/catalogue-integral/', '/etat-du-corpus/', '/methode-editoriale/'))
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
        top = header('/mythologie-grecque/' if portal_url == '/grande-encyclopedie/' else portal_url)
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
        add_scholarly_toc(doc, main, rel)
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
        # L'entrée grecque contient déjà le corpus de la Grande Encyclopédie.
        # Retirer uniquement les cartes de navigation redondantes de l'accueil ;
        # le chemin historique et ses manuscrits demeurent intacts et indexables.
        if url == '/':
            for duplicate in doc.select(
                    'a.portal-card[href="/grande-encyclopedie/"], '
                    'a.mythos-collection-card[href="/grande-encyclopedie/"]'):
                duplicate.decompose()
        # Sommaire de l'accueil : navigation interne vers les rubriques existantes,
        # sans reproduire les textes, changer les cartes ni créer d'entrées de corpus.
        # Cette passe est idempotente, y compris après deux reconstructions.
        if url == '/':
            for old in doc.select('nav.mythos-home-toc'):
                old.decompose()
            home_targets = (
                ('Les collections', 'home-collections'),
                ('Commencer une lecture', 'home-parcours'),
                ('Trois œuvres à approfondir', 'home-oeuvres'),
                ('Sanctuaires grecs en images', 'sanctuaires-en-images'),
                ('Explorer les mondes anciens', 'home-civilisations'),
                ('Une bibliothèque documentée', 'corpus-status'),
            )
            available = []
            for title, anchor in home_targets:
                section = next((
                    s for s in doc.select('main section.portal-section')
                    if s.find('h2') and s.find('h2').get_text(' ', strip=True) == title
                ), None)
                if section:
                    if not section.get('id') and not doc.find(id=anchor):
                        section['id'] = anchor
                    if section.get('id'):
                        available.append((title, section['id']))
            if available:
                toc = doc.new_tag('nav', attrs={
                    'class': 'mythos-home-toc',
                    'aria-label': 'Sommaire de la page d’accueil',
                })
                title = doc.new_tag('p', attrs={'class': 'mythos-home-toc-title'})
                title.string = 'Sur cette page'
                toc.append(title)
                links = doc.new_tag('ul')
                for label, anchor in available:
                    li = doc.new_tag('li')
                    link = doc.new_tag('a', href='#' + anchor)
                    link.string = label
                    li.append(link)
                    links.append(li)
                toc.append(links)
                illustrated_directory = doc.select_one('.mythos-directory')
                (illustrated_directory or banner).insert_after(toc)
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
        # Fil d'Ariane scientifique : une seule entrée par collection, sans
        # réécriture des paragraphes, citations, bibliographies ni numéros.
        # Les fiches de chapitre héritent de leur collection et restent
        # accessibles par le sommaire généré de celle-ci.
        collection_trails = {
            'origines-du-sacre': ('/origines-du-sacre/', 'Origines du sacré'),
            'encyclopedie': ('/mythologie-grecque/', 'Encyclopédie grecque'),
            'comedies': ('/theatre/', 'Théâtre grec'),
            'tragedies': ('/theatre/', 'Théâtre grec'),
            'comparatif': ('/mythologie-comparee/', 'Mythologie comparée'),
            'philosophie': ('/philosophie/', 'Philosophie'),
            'grece': ('/mythologie-grecque/', 'Encyclopédie grecque'),
        }
        parts = rel.split('/')
        for previous in doc.select('nav.mythos-breadcrumbs'):
            previous.decompose()
        if (len(parts) >= 4 and parts[0] == 'chapitres'
                and parts[1] in collection_trails):
            parent_url, parent_label = collection_trails[parts[1]]
            trail = doc.new_tag('nav', attrs={
                'class': 'mythos-breadcrumbs', 'aria-label': "Fil d’Ariane"})
            ordered = doc.new_tag('ol')
            for href, label in (('/', 'Accueil'), (parent_url, parent_label)):
                item = doc.new_tag('li')
                link = doc.new_tag('a', href=href)
                link.string = label
                item.append(link)
                ordered.append(item)
            current = doc.new_tag('li', attrs={'aria-current': 'page'})
            current.string = heading.get_text(' ', strip=True)
            ordered.append(current)
            trail.append(ordered)
            banner.insert_after(trail)
        # Shared keyboard behaviour for the native menu; no client-side theming.
        if not doc.select_one('script[src*="mythos-museum.js"]'):
            doc.body.append(doc.new_tag('script', src='/assets/mythos-museum.js?v='+VERSION, defer=''))
        path.write_text(str(doc), encoding='utf-8')
        count += 1
    return count

if __name__ == '__main__':
    import sys
    print('Habillage muséal :', apply(sys.argv[1] if len(sys.argv)>1 else '_site'), 'pages')
