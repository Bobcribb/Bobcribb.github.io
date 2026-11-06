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
NAV = [('/mythologie-grecque/','Encyclopédie grecque'),('/dieux-et-deesses/','Dieux'),('/heros-et-heroines/','Héros'),('/recits-mythologiques/','Récits'),('/theatre/','Théâtre'),('/origines-du-sacre/','Origines du sacré'),('/philosophie/','Philosophie'),('/reconstitutions-photorealistes.html','Reconstitutions 3D')]
MORE = [('/','Accueil'),*NAV,('/parcours/','Parcours de lecture'),('/catalogue-integral/','Catalogue intégral'),('/methode-editoriale/','Sources et méthode'),('/mythologie-comparee/','Mythologie comparée'),('/mythologies/','Mythologies du monde'),('/civilisations/','Civilisations'),('/reconstitutions-antiquite/','Atlas des sites antiques'),('/rubriques/','Tous les dossiers'),('/recherche/','Recherche')]
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
 # Énéide : vestiges de la Troie historique, repère contextuel non narratif.
 '/philosophie-eneide.html': 'mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg',
 '/parcours/decouvrir-les-mythes-grecs/': 'mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg',
 '/parcours/comprendre-la-tragedie/': 'mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg',
 '/parcours/comparer-les-creations-du-monde/': 'mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg',
 '/mythologie-comparee/': 'mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg',
 '/bibliotheque-egypte-ancienne/': 'mythos-papyrus-ani-pesee-coeur-british-museum.jpg',
 '/bibliotheque-mesopotamie/': 'gilgamesh-tablette-deluge-british-museum-babelstone.jpg',
 '/bibliotheque-perse-iran-ancien/': 'mythos-persepolis-apadana-delegations-pentocelo-2006.jpg',
 '/reconstitutions-antiquite/': '/assets/reconstitutions-3d/delphes-apollon-panorama.webp',
 '/reconstitutions-photorealistes.html': '/assets/reconstitutions-3d/delphes-apollon-panorama.webp',
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
    '/mythologie-comparee/': 'Mythologie comparée : Grèce, Égypte, Mésopotamie, Iran, méthodes critiques et études universitaires.',
    '/recherche/': 'Rechercher une étude MYTHOS par nom, auteur, civilisation, œuvre ou thème dans le catalogue intégral.',
    '/catalogue-integral/': 'Catalogue intégral de MYTHOS : retrouver les chapitres, les collections, les archives et les sources disponibles.',
    '/etat-du-corpus/': 'État vérifiable des collections MYTHOS, des pages publiées, des archives et des contrôles éditoriaux.',
    '/civilisations/': 'Explorer les civilisations antiques dans MYTHOS : textes, religions, sanctuaires et bibliothèques thématiques.',
    '/mythologies/': 'Parcourir les mythologies du monde : traditions documentées, sources, comparaisons et dossiers historiques.',
    '/reconstitutions-antiquite/': 'Reconstitutions documentées de cités et sanctuaires antiques : images, contexte et degré de certitude.',
    '/rubriques/': 'Index des dossiers MYTHOS : accès alphabétique aux mythologies, textes, personnages et analyses.',
}


def add_scholarly_toc(doc, main, rel):
    """Sommaire de lecture pour les études publiées, sans modifier leur source."""
    if not main or not (rel.startswith('chapitres/') and rel.endswith('/index.html')):
        return
    article = main.select_one('article.content') or main
    # Placer le sommaire hors de l'article : la prose, les notes et les
    # comparaisons textuelles des sources universitaires restent identiques.
    if main.name == 'article':
        return
    for old in main.select('nav.mythos-scholarly-toc'):
        old.decompose()
    # Les sommaires d'auteur et de lecture (amélioration progressive)
    # prévalent sur la navigation générée. Un long chapitre tel qu'Éros
    # à Thespies possède déjà un details.mythos-reading-toc complet.
    if article.select_one(
        '.toc, .article-toc, .table-of-contents, .mythos-reading-toc, '
        'nav[aria-label*="ommaire"]'
    ):
        return
    # Les renvois internes rédigés à la main doivent rester les premiers
    # liens vers leurs cibles, sans interposition d'une navigation générée.
    if article.select_one('a[href^="#"]'):
        return
    def eligible_headings(level):
        return [node for node in article.find_all(level)
                if not node.find_parent(['nav', 'aside', 'footer'])
                and node.get_text(' ', strip=True)]
    headings = eligible_headings('h2')
    # Certaines éditions ont un titre H2 suivi d'un plan scientifique H3.
    # Ne pas leur refuser un sommaire complet au seul motif de ce balisage.
    if len(headings) < 3:
        subheadings = eligible_headings('h3')
        if len(subheadings) >= 3:
            headings = subheadings
    if any(re.match(r"^(sommaire|table des mati[eè]res|plan de .{0,5}étude)\b",
                    node.get_text(' ', strip=True), re.I) for node in headings):
        return
    # Les très longues études reçoivent un sommaire repliable, jamais tronqué.
    # Les sommaires d'auteur restent prioritaires (voir contrôle ci-dessus).
    if len(headings) < 3:
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
    if len(targets) > 32:
        disclosure = doc.new_tag('details', attrs={
            'class': 'mythos-scholarly-toc-disclosure',
        })
        summary = doc.new_tag('summary')
        summary.string = f'Afficher les {len(targets)} sections de l’étude'
        disclosure.append(summary)
        disclosure.append(ordered)
        toc.append(disclosure)
    else:
        toc.append(ordered)
    main.insert(0, toc)



# Les lecteurs historiques 1138/1139 possèdent leur propre sommaire et leurs
# blocs d'origine immuables. BeautifulSoup reformate sinon les octets du texte
# universitaire, malgré une prose visuellement identique.
ARCHIVE_SOURCE_BLOCKS = {
    'bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/index.html': 'texte-integral-khmer-angkor',
    'bibliotheque-mythologies-du-monde/mythos-volume-15-philippines-ifugao-hudhud/index.html': 'texte-integral-hudhud-ifugao',
}


def _shield_original_archive(rel, raw):
    archive_id = ARCHIVE_SOURCE_BLOCKS.get(rel)
    if not archive_id:
        return raw, None, None
    opener = re.search(
        r'<div\b(?=[^>]*\bclass="mythos-original-study")(?=[^>]*\bid="'
        + re.escape(archive_id) + r'")[^>]*>', raw)
    if not opener:
        raise ValueError('Bloc scientifique historique absent : ' + rel)
    if archive_id == 'texte-integral-khmer-angkor':
        end_marker = raw.find('<!--MYTHOS-KHMER-SOURCE-END-->', opener.end())
        close = raw.find('</div>', end_marker) if end_marker >= 0 else -1
        if close < 0:
            raise ValueError('Bornes historiques Khmer absentes : ' + rel)
        stop = close + len('</div>')
    else:
        crosslinks = re.search(
            r'</div>\s*<nav\b[^>]*\bclass="mythos-world-study-crosslinks"',
            raw[opener.end():])
        if crosslinks is None:
            raise ValueError('Bornes historiques Hudhud absentes : ' + rel)
        stop = opener.end() + crosslinks.start() + len('</div>')
    original = raw[opener.start():stop]
    guard = '<!--MYTHOS-PRESERVED-' + archive_id.upper().replace('-', '_') + '-->'
    return raw[:opener.start()] + guard + raw[stop:], guard, original


def add_home_integral_archive_shelf(doc, root):
    """Relier deux éditions historiques déjà publiques sans recopier leurs textes.

    Les fichiers intégraux sont la source de vérité ; une carte n'est créée
    que si son lecteur et sa photographie documentée existent dans le build.
    Cette opération ne touche ni aux manuscrits ni aux séries numérotées.
    """
    section = doc.select_one('#corpus-status')
    if section is None:
        return 0
    for old in section.select('[data-mythos-integral-archives]'):
        old.decompose()
    # Les légendes reprennent les crédits du catalogue scripts/editorial_media.json.
    entries = (
        (
            '/corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html',
            '/media/2026/10/mythos-aphrodite-cygne-kylix-british-museum.jpg',
            'Aphrodite — étude universitaire intégrale',
            'Traditions, cultes, sources anciennes et philosophie du désir.',
            'Aphrodite sur un cygne, coupe attique du peintre de Pistoxénos, vers 460 av. n. è.',
            'Peintre de Pistoxénos, kylix, British Museum GR 1869.10-7.77 ; photo Marie-Lan Nguyen (2007), CC BY 2.5.',
            'https://commons.wikimedia.org/wiki/File:Aphrodite_swan_BM_D2.jpg',
            'https://creativecommons.org/licenses/by/2.5/',
        ),
        (
            '/corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html',
            '/media/2026/10/mythos-ounas-chambre-funeraire-vincent-brown.jpg',
            'Origines du sacré — édition historique I à XXVII',
            'Les vingt-sept tomes complets, sans extraction ni résumé.',
            'Photographie de la chambre funéraire d’Ounas, témoin égyptien contextuel (et non illustration de tous les chapitres).',
            'Pyramide d’Ounas, Saqqarah, Ve dynastie ; photo Vincent Brown (2011), CC BY 2.0.',
            'https://commons.wikimedia.org/wiki/File:Burial_chamber_in_Unas%27_pyramid.jpg',
            'https://creativecommons.org/licenses/by/2.0/',
        ),
    )
    cards = []
    for link, picture_url, title, description, alt, credit, source, license_url in entries:
        if not (root / link.lstrip('/')).is_file():
            continue
        if not (root / picture_url.lstrip('/')).is_file():
            continue
        cards.append(
            '<article class="mythos-home-archive-card">'
            '<a class="mythos-home-archive-link" href="' + html.escape(link, quote=True) + '">'
            '<img src="' + html.escape(picture_url, quote=True) + '" alt="'
            + html.escape(alt, quote=True) + '" loading="lazy" decoding="async"/>'
            '<strong>' + html.escape(title) + '</strong>'
            '<span>' + html.escape(description) + '</span></a>'
            '<p class="mythos-home-archive-credit">' + html.escape(credit)
            + ' <a href="' + html.escape(source, quote=True)
            + '">Source de l’image</a> · <a href="'
            + html.escape(license_url, quote=True)
            + '">Licence</a>.</p></article>'
        )
    if not cards:
        return 0
    panel = fragment(
        '<div class="mythos-home-archive-shelf" data-mythos-integral-archives="v1">'
        '<h3>Accès aux éditions historiques intégrales</h3>'
        '<p>Textes originaux déjà conservés sur MYTHOS : '
        'lecture directe, sommaires et bibliographies de leurs éditions conservés.</p>'
        '<div class="mythos-home-archive-grid">' + ''.join(cards) + '</div></div>'
    ).div
    section.append(panel)
    return len(cards)



def decorate_greek_archive_cards(doc, root):
    """Illustrer trois liens existants vers les archives grecques, sans copie.

    Chaque image et chaque lecteur doivent exister dans le site construit.
    Les légendes reprennent le catalogue éditorial des objets du Met (CC0).
    Le texte scientifique original et les quatorze liens restent intacts.
    """
    shelf = doc.select_one('#grec-archives ol.greek-corpus-links')
    if shelf is None:
        return 0
    entries = (
        (
            '/corpus/mythologie-grecque/archives/livre-heracles.html',
            '/media/2026/10/mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg',
            'Oinochoé attique : Héraclès affronte le lion de Némée.',
            'Héraclès et le lion de Némée, oinochoé attique du début du Ve siècle av. n. è., Met 06.1021.66.',
            'https://www.metmuseum.org/art/collection/search/247235',
        ),
        (
            '/corpus/mythologie-grecque/archives/livre-troie.html',
            '/media/2026/10/mythos-iliade-achille-ajax-athena-hydrie-met-56-171-29.jpg',
            'Hydrie attique : Achille et Ajax jouent en présence d’Athéna.',
            'Hydrie du Groupe de Léagros, vers 510 av. n. è., Met 56.171.29. Scène absente du poème homérique conservé.',
            'https://www.metmuseum.org/art/collection/search/254887',
        ),
        (
            '/corpus/mythologie-grecque/archives/livre-odyssee.html',
            '/media/2026/10/mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg',
            'Papyrus grec de l’Odyssée, chant XX, époque ptolémaïque.',
            'Fragment de l’Odyssée XX, vers 285–250 av. n. è., Met 09.182.50. Témoin postérieur à la composition du poème.',
            'https://www.metmuseum.org/art/collection/search/248134',
        ),
    )
    illustrated = 0
    for href, image_url, alt, caption, source_url in entries:
        if not (root / href.lstrip('/')).is_file():
            continue
        if not (root / image_url.lstrip('/')).is_file():
            continue
        anchor = shelf.select_one('a[href="' + href + '"]')
        if anchor is None or anchor.parent.name != 'li':
            continue
        item = anchor.parent
        # Rebuild only our illustration, never duplicate or rewrite the link.
        for old in item.select('.mythos-greek-archive-credit'):
            old.decompose()
        label = anchor.get_text(' ', strip=True)
        if not label:
            continue
        anchor.clear()
        anchor['class'] = list(dict.fromkeys(
            anchor.get('class', []) + ['mythos-greek-archive-illustrated-link']))
        item['class'] = list(dict.fromkeys(
            item.get('class', []) + ['mythos-greek-archive-illustrated']))
        image = doc.new_tag('img', src=image_url, alt=alt,
                            loading='lazy', decoding='async')
        image['class'] = ['mythos-greek-archive-image']
        anchor.append(image)
        title = doc.new_tag('span', attrs={'class': 'mythos-greek-archive-title'})
        title.string = label
        anchor.append(title)
        credit = doc.new_tag('p', attrs={'class': 'mythos-greek-archive-credit'})
        credit.append(caption + ' Reproduction Open Access (CC0). ')
        source = doc.new_tag('a', href=source_url)
        source.string = 'Notice du Met'
        credit.append(source)
        credit.append(' · ')
        licence = doc.new_tag(
            'a', href='https://creativecommons.org/publicdomain/zero/1.0/')
        licence.string = 'CC0'
        credit.append(licence)
        item.append(credit)
        illustrated += 1
    return illustrated


def add_greek_archive_return(doc, root):
    """Renvoi depuis l'édition HTML historique vers le sommaire grec."""
    banner = doc.select_one('.mythos-banner')
    portal = root / 'mythologie-grecque/index.html'
    if banner is None or not portal.is_file():
        return 0
    for old in doc.select('nav.mythos-greek-archive-return'):
        old.decompose()
    nav = doc.new_tag('nav', attrs={
        'class': 'mythos-greek-archive-return',
        'aria-label': 'Retour au catalogue des archives grecques',
    })
    link = doc.new_tag('a', href='/mythologie-grecque/#grec-archives')
    link.string = 'Retour aux archives historiques de la mythologie grecque'
    nav.append(link)
    banner.insert_after(nav)
    return 1


def apply(root):
    root = Path(root)
    count = 0
    for path in sorted(root.rglob('*.html')):
        # Les pièces jointes restent des sources immuables, même en HTML.
        if path.relative_to(root).parts[0] in {'assets', 'media'}:
            continue
        rel = path.relative_to(root).as_posix()
        protected_raw, protected_guard, protected_original = _shield_original_archive(
            rel, path.read_text(encoding='utf-8'))
        doc = BeautifulSoup(protected_raw, 'html.parser')
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
            # Décodage non bloquant des figures, sans changer la taille ou
            # l'origine des documents scientifiques et de leurs légendes.
            if not img.has_attr('decoding'):
                img['decoding'] = 'async'
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
        # Les galeries autonomes conservent leur extension .html pour l'état actif.
        nav_url = ('/mythologie-grecque/' if portal_url == '/grande-encyclopedie/'
                   else url if url == '/reconstitutions-photorealistes.html'
                   else portal_url)
        top = header(nav_url)
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
        if url == '/mythologie-grecque/':
            decorate_greek_archive_cards(doc, root)
        if rel.startswith('corpus/mythologie-grecque/archives/') and rel.endswith('.html'):
            add_greek_archive_return(doc, root)
        # Keep all iconography; display it below the text as a horizontal gallery.
        for rail in doc.select('.mythos-visual-rail, .mythos-home-illustrations, .article-aside'):
            rail['class'] = list(dict.fromkeys(rail.get('class',[]) + ['mythos-bottom-gallery']))
        # Remove presentation-only empty wrappers and redundant decorative eyebrow.
        for eyebrow in doc.select('article.content > .eyebrow'):
            eyebrow['class'] = list(dict.fromkeys(eyebrow.get('class', []) + ['mythos-chrome-label']))
        # Six-column illustrated directory reproduces the reference card rhythm.
        if url == '/' and not doc.select_one('.mythos-directory'):
            items = [*NAV,('/mythologie-comparee/','Mythologie comparée'),('/bibliotheque-egypte-ancienne/','Égypte ancienne'),('/bibliotheque-mesopotamie/','Mésopotamie')]
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
        # La galerie photoréaliste doit être visible parmi les collections de
        # l'accueil, lorsque ce portail présente déjà le groupe dédié. Garder
        # une seule carte et qualifier le caractère interprétatif des images.
        if url == '/':
            add_home_integral_archive_shelf(doc, root)
            collection_grid = doc.select_one('#home-collections .portal-grid')
            gallery_url = '/reconstitutions-photorealistes.html'
            if (collection_grid and not collection_grid.select_one(
                    'a.portal-card[href="' + gallery_url + '"]')):
                gallery_card = fragment(
                    '<a class="portal-card" href="' + gallery_url + '">'
                    '<img class="mythos-card-image" loading="lazy" decoding="async" '
                    'src="/assets/reconstitutions-3d/delphes-apollon-panorama.webp" '
                    'alt="Vue interprétative du sanctuaire de Delphes ; reconstitution numérique."/>'
                    '<span class="portal-card-kicker">GALERIE DOCUMENTÉE</span>'
                    '<strong>Reconstitutions 3D</strong>'
                    '<span>Vues des sanctuaires, sources archéologiques et degrés de certitude.</span>'
                    '<span class="card-indicator" aria-hidden="true">↗</span></a>'
                ).a
                collection_grid.append(gallery_card)
        # Sommaire de l'accueil : navigation interne vers les rubriques existantes,
        # sans reproduire les textes, changer les cartes ni créer d'entrées de corpus.
        # Cette passe est idempotente, y compris après deux reconstructions.
        if url == '/':
            for old in doc.select('nav.mythos-home-toc'):
                old.decompose()
            home_targets = (
                ('Les collections', 'home-collections'),
                ('Commencer une lecture', 'home-parcours'),
                ('Dernières études par collection', 'home-etudes-recentes'),
                ('Quatre œuvres à approfondir', 'home-oeuvres'),
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
                # Le parcours de l'Énéide possède une photographie précise
                # des vestiges de Troie VI, explicitement NON assimilés aux
                # scènes du poème. Conserver son ALT scientifique à chaque passe.
                if (card.get('href') == '/philosophie-eneide.html'
                        and authored.get('src') ==
                        '/media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg'):
                    if not (root / authored['src'].lstrip('/')).is_file():
                        raise RuntimeError('Photographie de Troie manquante : parcours Énéide')
                    # Une reconstruction du portail peut recréer la carte
                    # avec alt="" : restituer la description attestée.
                    authored['alt'] = ('Vestiges de Troie VI à Hisarlik : contexte '
                                      'archéologique, non illustration du récit virgilien.')
                    continue
                # Les cartes des dernières études proviennent des reçus
                # d'attribution et de recent_studies.py. Leurs photographies
                # documentaires sont déjà archivées dans media/ et accompagnées
                # d'une légende prudente ; une seconde passe musée ne doit pas
                # les effacer et laisser une légende sans illustration.
                # Ne jamais conserver un SVG 2,5D ou un fichier inexistant.
                if (card.find_parent(id='home-etudes-recentes') is not None
                        and authored.find_parent(class_='mythos-recent-illustration') is not None
                        and image_path.startswith('/media/')
                        and '/../' not in image_path
                        and image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
                        and (root / image_path.lstrip('/')).is_file()):
                    continue
                # CIV-01 : la carte de Behistun porte une vraie photographie
                # archéologique locale, avec crédit et licence dans la carte.
                # Un habillage ultérieur ne doit pas la supprimer silencieusement.
                if (card.get('href') ==
                        '/corpus/civilisations/perse-iran-ancien-behistun.html'
                        and image_path ==
                        '/media/2026/10/mythos-behistun-inscription-darius-mahdimanavimvi-2018.jpg'):
                    if not (root / image_path.lstrip('/')).is_file():
                        raise RuntimeError('Photographie de Behistun manquante : CIV-01')
                    authored['alt'] = ('Relief de Darius Ier et inscription trilingue '
                                      'gravés sur la falaise de Behistun.')
                    continue
                # Photographies patrimoniales documentées des volumes historiques
                # XII–XIV : sources et licences créditées sur chaque carte.
                verified_world_figures = {
                    "/bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/":
                        ("koush-naqa-lassihu", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Naqa_Apedamak_temple.jpg/960px-Naqa_Apedamak_temple.jpg"),
                    "/bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/":
                        ("sassoun-kochar-2014", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/2014_Erywa%C5%84%2C_Pomnik_Dawida_Sasu%C5%84skiego_%2801%29.jpg/960px-2014_Erywa%C5%84%2C_Pomnik_Dawida_Sasu%C5%84skiego_%2801%29.jpg"),
                    "/bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/":
                        ("khmer-angkor-jadamta-2012", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Angkor_Wat_-_Churning_of_the_Sea_of_Milk.JPG/640px-Angkor_Wat_-_Churning_of_the_Sea_of_Milk.JPG"),
                }
                verified = verified_world_figures.get(card.get('href'))
                if (verified and authored.get('data-mythos-card-source') == verified[0]
                        and image_path == verified[1]):
                    continue
                # La Galigo: archive photographique de Leyde, conservée avec
                # crédit et licence dans la carte de la bibliothèque.
                # Ne conserver aucun SVG 2,5D ni image externe arbitraire.
                if (card.get('href') ==
                        '/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/'
                        and authored.get('data-mythos-card-source') == 'la-galigo-leiden'
                        and image_path ==
                        'https://upload.wikimedia.org/wikipedia/commons/1/10/La_Galigo_item_29355-0009_%28cropped2%29.jpg'):
                    continue
            for old in card.select('img.mythos-card-image'):
                old.decompose()
            src = picture(card.get('href', ''), root)
            if src and not card.find('img'):
                # Un nouveau portail ne doit pas réintroduire alt="" pour Troie.
                image_alt = ''
                if card.get('href') == '/philosophie-eneide.html' and src == '/media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg':
                    image_alt = 'Vestiges de Troie VI à Hisarlik : contexte archéologique, non illustration du récit virgilien.'
                card.insert(0, doc.new_tag('img', src=src, alt=image_alt, loading='lazy', attrs={'class':'mythos-card-image'}))
        # MYTHOS safeguard: gallery-thumbnail retention on repeated passes.
        # This gallery card must keep its locally stored original WebP, never
        # a generated SVG or a missing image. No scholarly article is changed.
        if url == '/':
            gallery_card = doc.select_one(
                '#home-collections a.portal-card'
                '[href="/reconstitutions-photorealistes.html"]')
            thumbnail = '/assets/reconstitutions-3d/delphes-apollon-panorama.webp'
            if gallery_card and (root / thumbnail.lstrip('/')).is_file():
                images = gallery_card.find_all('img')
                for duplicate in images[1:]:
                    duplicate.decompose()
                image = images[0] if images else None
                if image is None:
                    image = doc.new_tag('img', attrs={
                        'class': 'mythos-card-image',
                        'src': thumbnail,
                        'alt': 'Reconstitution photoréaliste interprétative du sanctuaire de Delphes.',
                        'loading': 'lazy',
                        'decoding': 'async',
                    })
                    gallery_card.insert(0, image)
                else:
                    image['src'] = thumbnail
                    image['class'] = list(dict.fromkeys(
                        image.get('class', []) + ['mythos-card-image']))
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
        # Navigation de fin d'étude : l'article, ses sources et sa bibliographie
        # restent immuables. Les renvois pointent vers les rubriques du site.
        for previous in doc.select('nav.mythos-study-endnav'):
            previous.decompose()
        if (len(parts) >= 4 and parts[0] == 'chapitres'
                and parts[1] in collection_trails and main):
            study_article = main.select_one('article.content') or main.select_one('article')
            if study_article:
                parent_url, parent_label = collection_trails[parts[1]]
                endnav = doc.new_tag('nav', attrs={
                    'class': 'mythos-study-endnav',
                    'aria-label': 'Navigation de fin de lecture',
                })
                for href, label in (
                    (parent_url, 'Retour : ' + parent_label),
                    ('/catalogue-integral/', 'Catalogue intégral'),
                    ('#' + heading['id'], 'Retour au titre'),
                ):
                    link = doc.new_tag('a', href=href)
                    link.string = label
                    endnav.append(link)
                study_article.insert_after(endnav)
        # Shared keyboard behaviour for the native menu; no client-side theming.
        if not doc.select_one('script[src*="mythos-museum.js"]'):
            doc.body.append(doc.new_tag('script', src='/assets/mythos-museum.js?v='+VERSION, defer=''))
        rendered = str(doc)
        if protected_guard:
            if rendered.count(protected_guard) != 1:
                raise ValueError('Marqueur de préservation perdu : ' + rel)
            rendered = rendered.replace(protected_guard, protected_original)
        path.write_text(rendered, encoding='utf-8')
        count += 1
    return count

if __name__ == '__main__':
    import sys
    print('Habillage muséal :', apply(sys.argv[1] if len(sys.argv)>1 else '_site'), 'pages')
