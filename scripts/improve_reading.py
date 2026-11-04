#!/usr/bin/env python3
"""Build discovery, reading aids and a reproducible inventory from real pages.

Never creates scholarly content or certifies an academic review. All additions
are owned, removable navigation blocks; authored text and anchors stay intact.
"""
from collections import Counter
from hashlib import sha256
from html import escape
import json
import math
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit
import unicodedata

from bs4 import BeautifulSoup

VERSION = "20261104-lecture-2"
COLLECTIONS = [
    ("/mythologie-grecque/", "Encyclopédie grecque", "Dossiers thématiques : dieux, héros, cycles, sanctuaires et textes anciens."),
    ("/theatre/", "Théâtre grec", "Intrigues, fragments et analyses philosophiques."),
    ("/origines-du-sacre/", "Origines du sacré", "Rites, témoignages et histoire des religions."),
    ("/philosophie/", "Philosophie", "Œuvres, concepts et interprétations."),
    ("/mythologie-comparee/", "Mythologie comparée", "Comparer les traditions et leurs différences."),
    ("/reconstitutions-photorealistes.html", "Reconstitutions 3D",
     "Monuments antiques en vues photoréalistes, notices sourcées et degrés de certitude.",
     "GALERIE ARCHÉOLOGIQUE"),
]
EPICS = {
    "iliade": ("L’Iliade", "/iliade/", "Homère", "https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg001/", "D. B. Monro et T. W. Allen (éd.), Homeri Opera, vol. 1–2, Oxford, Clarendon Press, 1908–1920. Texte grec et traductions dans Perseus."),
    "odyssee": ("L’Odyssée", "/odyssee/", "Homère", "https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012.tlg002.perseus-grc2/", "A. T. Murray (éd.), The Odyssey, vol. 1–2, 1919. Texte grec dans Perseus ; les traductions se consultent séparément."),
    "theogonie": ("La Théogonie", "/livre-hesiode/", "Hésiode", "https://catalog.perseus.tufts.edu/catalog/urn%3Acts%3AgreekLit%3Atlg0020.tlg001.perseus-grc1", "H. G. Evelyn-White (éd. et trad.), Hesiod, The Homeric Hymns and Homerica, 1914, p. 78–153. Notice du texte grec dans Perseus."),
}
ROUTES = [
    ("decouvrir-les-mythes-grecs", "Découvrir les mythes grecs", "Des premières générations divines à la lecture philosophique d’Homère.", [
        ("/livre-hesiode/", "Naissance du monde et des dieux", "Repérez les générations divines et les successions de pouvoir chez Hésiode."),
        ("/livre-dieux/", "Situer les puissances divines", "Comparez les fonctions, les cultes et les variantes des principaux dieux."),
        ("/iliade/", "Entrer dans l’Iliade", "Suivez le conflit d’Achille et les conséquences de sa colère."),
        ("/philosophie-iliade.html", "Interpréter l’honneur et la mortalité", "Passez du déroulement du récit aux problèmes de valeur, de responsabilité et de compassion."),
        ("/sources-methodes/", "Revenir aux preuves", "Distinguez les traditions littéraires, leurs variantes et les témoignages matériels."),
    ]),
    ("comprendre-la-tragedie", "Comprendre la tragédie grecque", "Lire une intrigue, examiner un conflit, confronter une interprétation au texte.", [
        ("/theatre/", "Choisir une pièce", "Commencez par une œuvre conservée et identifiez son auteur, ses personnages et son intrigue."),
        ("/tragedies/sophocle-antigone-lecture-critique-loi-sepulture/", "Antigone : sépulture et autorité", "Relevez les arguments opposés autour des devoirs envers le mort et la cité."),
        ("/theatre-grec-conserve-etudes-philosophiques/", "Comparer les analyses", "Consultez la bibliothèque distincte d’interprétations philosophiques des pièces."),
        ("/tragedies/philosophie-theatre-grec-tragique-comique-hegel-nietzsche/", "Lire Hegel et Nietzsche", "Distinguez les lectures modernes du sens historique et des mots de la pièce antique."),
        ("/sources-methodes/", "Évaluer une reconstitution", "Pour une œuvre perdue, séparez fragments conservés, témoignages indirects et scènes modernes."),
    ]),
    ("comparer-les-creations-du-monde", "Comparer les récits de création", "Un parcours grec, mésopotamien et égyptien attentif aux différences.", [
        ("/philosophie-theogonie.html", "Hésiode : généalogie et souveraineté", "Observez comment les générations divines organisent le récit du monde."),
        ("/enuma-elish-marduk-tiamat-creation-babylone/", "Babylone : Marduk et Tiamat", "Identifiez la place de la guerre divine, de l’assemblée et de la royauté."),
        ("/bibliotheque-egypte-ancienne/mythologie-egypte-cosmogonies-osiris-maat-au-dela/", "Égypte : plusieurs traditions", "Distinguez les constructions théologiques et leurs lieux de transmission."),
        ("/mythologie-comparee/", "Comparer avec méthode", "Une ressemblance ne suffit pas à démontrer une origine commune ou un emprunt."),
        ("/sources-methodes/", "Documenter la comparaison", "Notez pour chaque texte son contexte, sa date et son mode de conservation."),
    ]),
]


def norm(value):
    value = unicodedata.normalize("NFKD", value.lower().replace("œ", "oe"))
    return re.sub(r"\s+", " ", "".join(c for c in value if not unicodedata.combining(c)))


def page_path(out, url):
    path = out / urlsplit(url).path.lstrip("/")
    return path / "index.html" if url.endswith("/") else path


def fragment(markup):
    return BeautifulSoup(markup, "html.parser")


def write_page(out, slug, title, body):
    from build_navigation import shell
    target = out / slug / "index.html" if slug else out / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(shell(title, body), encoding="utf-8")


def cards(items):
    from build_navigation import cards as render_cards
    return render_cards(items)



# Vitrines documentaires des bibliothèques : images strictement liées à un
# objet attesté, avec la notice complète de provenance du registre existant.
# Ces cartes n'illustrent pas une civilisation entière.
CIVILISATION_DOCUMENTS = [
    ("/bibliotheque-egypte-ancienne/", "Égypte ancienne",
     "Textes funéraires, sanctuaires et histoire religieuse.",
     "mythos-ounas-chambre-funeraire-vincent-brown"),
    ("/bibliotheque-mesopotamie/", "Mésopotamie",
     "Tablettes, cosmogonies et traditions suméro-akkadiennes.",
     "mythos-enuma-elish-tablette-k3473-ninive-zunkir"),
    ("/bibliotheque-perse-iran-ancien/", "Perse et Iran ancien",
     "Reliefs achéménides, inscriptions et sources iraniennes.",
     "persepolis-apadana-delegation-lydienne"),
]


def civilisation_document_cards(out, root):
    """Return three sourced home cards; refuse missing provenance or files."""
    register = json.loads((root / "scripts/editorial_media.json").read_text(encoding="utf-8"))
    media = {item["id"]: item for item in register["media"]}
    cards_html = []
    for url, label, lead, media_id in CIVILISATION_DOCUMENTS:
        if not page_path(out, url).is_file():
            raise RuntimeError("Bibliothèque absente du rendu : " + url)
        item = media.get(media_id)
        if not item or not all(item.get(key) for key in ("path", "alt", "caption_html", "provenance_page")):
            raise RuntimeError("Provenance archéologique manquante : " + media_id)
        relative = Path(item["path"])
        if relative.parts[:3] != ("media", "2026", "10") or not (out / relative).is_file():
            raise RuntimeError("Image archéologique absente du rendu : " + str(relative))
        provenance_page = item["provenance_page"]
        if not (out / provenance_page).is_file():
            raise RuntimeError("Dossier de provenance absent : " + provenance_page)
        cards_html.append(
            '<article class="mythos-civilisation-card" id="mythos-document-' + escape(media_id, quote=True) + '" data-document-id="' + escape(media_id, quote=True) + '">'
            '<a class="mythos-civilisation-link" href="' + escape(url, quote=True) + '">'
            '<img src="/' + escape(relative.as_posix(), quote=True) + '" alt="' + escape(item["alt"], quote=True) + '" loading="lazy" decoding="async">'
            '<span class="mythos-civilisation-kicker">DOCUMENT ARCHÉOLOGIQUE</span>'
            '<strong>' + escape(label) + '</strong>'
            '<span>' + escape(lead) + '</span></a>'
            '<p class="mythos-civilisation-study"><a href="/' + escape(provenance_page, quote=True) + '">'
            'Lire le dossier scientifique et ses sources ↗</a></p>'
            '<details class="mythos-civilisation-credit"><summary>Source et crédits de l’image</summary>'
            '<div>' + item["caption_html"] + ' '
            '<a href="/' + escape(provenance_page, quote=True) + '">Étudier cet objet et ses sources</a></div>'
            '</details></article>'
        )
    return '<div class="mythos-civilisation-grid">' + ''.join(cards_html) + '</div>'



def install_civilisation_reciprocal_navigation(out, root):
    """Relier les trois dossiers attestés à leurs bibliothèques sans réécrire une étude."""
    register = json.loads((root / "scripts/editorial_media.json").read_text(encoding="utf-8"))
    media = {item["id"]: item for item in register["media"]}
    updated = []
    for library, label, _, media_id in CIVILISATION_DOCUMENTS:
        item = media.get(media_id)
        if not item or not item.get("provenance_page"):
            raise RuntimeError("Notice de provenance absente : " + media_id)
        target = out / item["provenance_page"]
        if not target.is_file():
            raise RuntimeError("Étude documentaire absente : " + item["provenance_page"])
        if not page_path(out, library).is_file():
            raise RuntimeError("Bibliothèque absente : " + library)
        doc = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
        article = doc.select_one("main article.content")
        if article is None:
            raise RuntimeError("Contenu scientifique introuvable : " + item["provenance_page"])
        if article.select_one('[data-mythos-document-reciprocal]'):
            continue
        # Bloc strictement navigant : titres, citations, notes et bibliographie intacts.
        nav = (
            '<nav class="mythos-document-reciprocal" data-reading-owned="true" '
            'data-mythos-document-reciprocal="true" aria-label="Renvois documentaires">'
            '<span>Pour poursuivre l’étude : ' + escape(label) + '</span>'
            '<a href="' + escape(library, quote=True) + '">Bibliothèque de la civilisation</a>'
            '<a href="/#mythos-document-' + escape(media_id, quote=True) + '">'
            'Photographie, légende et provenance sur l’accueil</a>'
            '</nav>'
        )
        article.append(fragment(nav))
        target.write_text(str(doc), encoding="utf-8")
        updated.append(item["provenance_page"])
    return updated


def search_form(catalogue=False):
    filters = [("collection", "Collection"), ("civilizations", "Civilisation"),
               ("authors", "Auteur étudié"), ("works", "Œuvre"), ("themes", "Thème")]
    return '<form class="discovery-form" role="search" data-discovery-form><label for="mythos-query">Rechercher un titre, un nom ou un thème</label><input id="mythos-query" name="q" type="search" class="search" data-search placeholder="Ex. Achille, Osiris, Nietzsche…" autocomplete="off"><div class="discovery-filters">' + ''.join(
        '<label>'+label+'<select data-filter="'+key+'" name="'+key+'"><option value="">Tous</option></select></label>' for key,label in filters
    ) + '</div><button type="reset">Effacer les filtres</button></form><p data-search-status role="status" aria-live="polite">Chargement du catalogue…</p><div class="results discovery-results" data-results'+(' data-catalogue="true"' if catalogue else '')+'></div><nav class="result-pagination" aria-label="Pages de résultats" data-pagination></nav><noscript><p>La recherche filtrée nécessite JavaScript. <a href="/rubriques/">Ouvrir l’index alphabétique complet</a>.</p></noscript>'


def home_work_cards():
    """Les quatre études réellement présentées sur la page d'accueil."""
    return [
        ('/philosophie-'+key+'.html', spec[0], desc, 'ÉTUDE PHILOSOPHIQUE')
        for key, spec, desc in [
            ('iliade', EPICS['iliade'], 'Colère, honneur, mortalité et compassion.'),
            ('odyssee', EPICS['odyssee'], 'Identité, hospitalité, retour et reconnaissance.'),
            ('theogonie', EPICS['theogonie'], 'Généalogie divine, savoir poétique et souveraineté.'),
        ]
    ] + [
        ('/philosophie-eneide.html', 'L’Énéide',
         'Exil, pietas, destin et fondation. Première livraison : 76 pages A4 d’analyse ; objectif de 300 pages encore inachevé.',
         'VIRGILE · ÉDITION PARTIELLE'),
    ]


def prepare(out, root):
    """Create portals before the last search/sitemap pass."""
    intro = '<h1>MYTHOS</h1><p class="portal-lead">Mythes, textes et civilisations : une bibliothèque à parcourir, des sources à interroger.</p>'
    intro += '<form class="home-search" action="/recherche/" role="search"><label for="home-q">Que souhaitez-vous explorer ?</label><div><input id="home-q" name="q" type="search" placeholder="Un dieu, une œuvre, un lieu…"><button type="submit">Rechercher</button></div></form>'
    intro += '<section class="portal-section"><h2>Les collections</h2>'+cards(COLLECTIONS)+'</section>'
    intro += '<section class="portal-section"><h2>Commencer une lecture</h2>'+cards([
        ('/parcours/'+slug+'/',title,lead,'PARCOURS GUIDÉ') for slug,title,lead,_ in ROUTES])+'</section>'
    # Les quatre œuvres sont contrôlées contre leurs lecteurs disponibles.
    works = home_work_cards()
    for address, _, _, _ in works:
        if not page_path(out, address).is_file():
            raise RuntimeError('Étude de l’accueil absente du rendu : ' + address)
    intro += ('<section class="portal-section" id="home-oeuvres">'
              '<h2>Quatre œuvres à approfondir</h2>'
              '<p class="section-intro">Trois études grecques d’Homère et d’Hésiode, '
              'prolongées par Virgile et la fondation romaine. L’Énéide est une '
              'première livraison ; l’objectif de 300 pages demeure inachevé.</p>'
              + cards(works) + '</section>')
    # Vitrines de sites antiques : images locales existantes et liens profonds stables.
    # Conserver les notices archéologiques distinctes des vues interprétatives.
    sites = [
        ("Delphes — sanctuaire d’Apollon", "delphes-apollon-panorama", "delphes",
         "Panorama numérique interprétatif du sanctuaire."),
        ("Némée — temple de Zeus", "nemee-temple-zeus-vue", "nemee",
         "Vue interprétative du temple et de son paysage sacré."),
        ("Sounion — temple de Poséidon", "sounion-poseidon-vue", "sounion",
         "Reconstitution interprétative du promontoire attique."),
    ]
    for _, picture, dossier, _ in sites:
        if not (out / "assets/reconstitutions-3d" / (picture + ".webp")).is_file():
            raise RuntimeError("Image du sommaire des sanctuaires absente : " + picture)
        if not (out / "sites" / (dossier + ".html")).is_file():
            raise RuntimeError("Dossier des sanctuaires absent : " + dossier)
    intro += '<section class="portal-section" id="sanctuaires-en-images"><h2>Sanctuaires grecs en images</h2>'
    intro += '<p class="section-intro">Trois vues numériques interprétatives, avec accès aux notices archéologiques et aux sources. Elles ne remplacent pas les vestiges attestés.</p>'
    intro += '<div class="portal-grid">' + ''.join(
        '<a class="portal-card" href="/reconstitutions-photorealistes.html#' + picture + '">'
        '<img class="mythos-card-image" src="/assets/reconstitutions-3d/' + picture + '.webp" alt="" loading="lazy" decoding="async">'
        '<span class="portal-card-kicker">VUE PHOTORÉALISTE</span><strong>' + title + '</strong>'
        '<span>' + description + '</span><span class="card-indicator" aria-hidden="true">↗</span></a>'
        for title, picture, _, description in sites) + '</div>'
    intro += '<p class="discovery-inline">Dossiers et sources : ' + ' · '.join(
        '<a href="/sites/' + dossier + '.html">' + title.split(" — ")[0] + '</a>'
        for title, _, dossier, _ in sites) + ' · <a href="/reconstitutions-photorealistes.html">Galerie complète</a></p></section>'
    intro += '<section class="portal-section" id="home-civilisations"><h2>Explorer les mondes anciens</h2>' + civilisation_document_cards(out, root) + '<p class="discovery-inline">'+ ' · '.join(
        '<a href="'+u+'">'+label+'</a>' for u,label in [('/civilisations/','Toutes les civilisations'),('/reconstitutions-antiquite/','Sites et reconstitutions')])+'</p></section>'
    intro += '<section class="portal-section" id="corpus-status"><h2>Une bibliothèque documentée</h2><p><a href="/catalogue-integral/">Catalogue intégral</a> · <a href="/etat-du-corpus/">État du corpus</a> · <a href="/methode-editoriale/">Sources et méthode</a></p><p data-corpus-count>Le catalogue est reconstruit à partir des textes disponibles.</p></section>'
    write_page(out, '', 'MYTHOS — Mythes, textes et civilisations', intro)
    write_page(out, 'recherche', 'Rechercher dans MYTHOS', '<h1>Rechercher dans MYTHOS</h1><p>Combinez les mots et les filtres pour retrouver une étude.</p>'+search_form())
    write_page(out, 'catalogue-integral', 'Catalogue intégral de MYTHOS', '<h1>Catalogue intégral</h1><p>Chaque adresse correspond à une entrée identifiée. Les filtres décrivent les sujets repérés dans les titres et les collections ; ils ne certifient pas une expertise scientifique.</p>'+search_form(True)+'<p><a href="/rubriques/">Index complet sans filtres</a> · <a href="/etat-du-corpus/">État du corpus et textes à retrouver</a></p>')
    write_page(out, 'parcours', 'Parcours de lecture', '<h1>Parcours de lecture</h1><p>Des itinéraires progressifs pour découvrir les textes puis approfondir leur interprétation.</p>'+cards([('/parcours/'+slug+'/',title,lead) for slug,title,lead,_ in ROUTES]))
    for slug,title,lead,steps in ROUTES:
        for url,_,_ in steps:
            if not page_path(out,url).is_file():
                raise RuntimeError('Étape absente du parcours : '+url)
        body='<h1>'+title+'</h1><p class="portal-lead">'+lead+'</p><ol class="reading-route">'
        for url,label,description in steps:
            body+='<li><h2><a href="'+url+'">'+label+'</a></h2><p>'+description+'</p></li>'
        body+='</ol><p><a href="/parcours/">Tous les parcours</a></p>'
        write_page(out,'parcours/'+slug,title,body)
    method='''<h1>Sources, interprétations et méthode éditoriale</h1>
<p class="portal-lead">MYTHOS réunit récits, analyses et documents. Cette page expose les critères de lecture et les limites des contrôles effectués.</p>
<h2>Trois niveaux à distinguer</h2><dl><dt>Témoignage antique</dt><dd>Un passage d’auteur, une inscription, un papyrus ou un objet documenté. Citer l’œuvre, le livre, les vers ou le numéro d’inventaire permet de retrouver le témoignage.</dd><dt>Hypothèse et débat</dt><dd>Une attribution, une datation ou une interprétation discutée doit être présentée avec ses arguments et ses incertitudes.</dd><dt>Interprétation ou reconstitution moderne</dt><dd>Une lecture philosophique et une scène recomposée ne sont pas des fragments antiques. Leurs choix doivent être annoncés.</dd></dl>
<h2>Lire les références</h2><p>Les références aux œuvres anciennes et les notices bibliographiques restent attachées aux études. Les éditions et traductions doivent être distinguées. La présence d’une bibliographie ne vaut pas validation de toutes les affirmations d’un article.</p>
<h2>Lire les images</h2><p>Les légendes précisent, lorsqu’ils sont documentés, l’objet, la date, le lieu de conservation, l’auteur de l’image, sa provenance et ses droits. Une photographie de vestiges, une œuvre de réception et une reconstitution ne constituent pas le même type de preuve. Une image produite avec assistance IA doit être identifiée comme une création contemporaine.</p>
<h2>Comparer des traditions</h2><p>La comparaison doit partir des textes et de leur contexte. Une ressemblance narrative ne démontre pas à elle seule un contact historique, une filiation ou une origine commune. Les différences et les objections font partie de l’analyse.</p>
<h2>Ce que les contrôles garantissent</h2><p>La construction du site contrôle les adresses du catalogue, les numéros des collections et la conservation des manuscrits protégés. L’état du corpus distingue une page construite et une vérification HTTP après déploiement. Ces contrôles techniques ne remplacent pas une relecture scientifique humaine.</p>
<h2>Signaler une correction</h2><p>Notez le titre, l’adresse, la section, le passage concerné et une référence permettant de vérifier la correction. <a href="https://github.com/Bobcribb/Bobcribb.github.io/issues/new">Transmettre un signalement sur GitHub</a> (compte nécessaire).</p>
<h2>Approfondir la méthode</h2><p><a href="/sources-methodes/">Sources et méthodes de l’étude des mythes</a> · <a href="/bibliotheque-mythologies-du-monde/charte-scientifique-sources-images-reconstitutions-mythos/">Charte scientifique détaillée</a> · <a href="/etat-du-corpus/">État du corpus</a></p>'''
    write_page(out,'methode-editoriale','Sources et méthode éditoriale',method)
    write_page(out,'etat-du-corpus','État du corpus MYTHOS','<h1>État du corpus</h1><div id="corpus-inventory"></div>')


def metadata(entry, doc):
    title = entry['title']
    subject = norm(title+' '+unquote(entry['url']).replace('-',' '))
    title_subject = norm(title)
    collection='Dossiers et archives'
    for token,label in [('origines-du-sacre','Origines du sacré'),('chapitres/encyclopedie','Encyclopédie grecque'),('chapitres/comparatif','Cycle philosophique comparatif'),('philosophie','Philosophie'),('comparee','Mythologie comparée'),('traged','Tragédies'),('comed','Comédies'),('theatre','Théâtre grec')]:
        if token in entry['url']: collection=label; break
    def labels(rules, source=subject):
        return [label for pattern,label in rules if re.search(pattern,source)]
    civilizations=labels([(r'egypte|egypt|osiris|hathor|akhetaton|maat','Égypte'),(r'mesopot|babylon|sumer|gilgame|enuma|akkad|assyr','Mésopotamie'),(r'perse|iran|zoroastre|mazda|behistun','Perse et Iran'),(r'grec|grece|homere|hesiode|iliade|odyssee|theogonie|athenes|delphes|zeus|apollon|sophocle|euripide|eschyle|aristophane|menandre','Grèce'),(r'rome|romain|latin|ciceron|ovide|virgile','Rome'),(r'\binde\b|indien|veda|mahabharata','Inde'),(r'chine|chinois|confucius|xunzi','Chine')])
    if collection in ('Tragédies','Comédies','Théâtre grec') and 'Grèce' not in civilizations: civilizations.append('Grèce')
    authors=labels([(r'\b'+name+r'\b',label) for name,label in [('homere','Homère'),('hesiode','Hésiode'),('eschyle','Eschyle'),('sophocle','Sophocle'),('euripide','Euripide'),('aristophane','Aristophane'),('menandre','Ménandre'),('platon','Platon'),('aristote','Aristote'),('nietzsche','Nietzsche'),('hegel','Hegel'),('dumezil','Dumézil')]])
    works=labels([(r'\biliade\b','Iliade'),(r'\bodyssee\b','Odyssée'),(r'\btheogonie\b','Théogonie'),(r'\bantigone\b','Antigone'),(r'enuma','Enūma eliš'),(r'gilgame','Gilgamesh'),(r'\bfaust\b','Faust')],title_subject)
    if any(work in works for work in ('Iliade','Odyssée')) and 'Homère' not in authors: authors.append('Homère')
    if 'Théogonie' in works and 'Hésiode' not in authors: authors.append('Hésiode')
    themes=labels([(r'mort|funer|sepultur|au dela','Mort et au-delà'),(r'creati|cosmog|theogonie','Création du monde'),(r'rite|rituel|sacrifice|sacre|culte','Rites et cultes'),(r'justice|droit|loi|dik|maat','Justice'),(r'guerre|guerr|iliade','Guerre'),(r'roi|roya|souverain|pouvoir','Pouvoir'),(r'voyage|retour|odyssee','Voyage et retour')],title_subject)
    main=doc.main or doc.select_one('article') or doc.body
    clone=fragment(str(main))
    for tag in clone.select('nav, .mythos-reader, .mythos-reading-toc, [data-reading-owned], script, style'): tag.decompose()
    content=clone.get_text(' ',strip=True)
    words=len(content.split())
    headings=' '.join(h.get_text(' ',strip=True) for h in clone.select('h2,h3'))[:2000]
    return dict(entry, id='MYT-'+sha256(entry['url'].encode()).hexdigest()[:16].upper(),collection=collection,civilizations=civilizations,authors=authors,works=works,themes=themes,words=words,minutes=max(1,math.ceil(words/220)),headings=headings,bibliography_present=bool(re.search(r'bibliograph|references primaires|sources primaires',norm(content))),images=len(clone.select('img')),text_sha256=sha256(content.encode()).hexdigest(),availability='built',scholarly_review='not_certified')


def add_reading(doc, url, entry):
    main=doc.main or doc.select_one('article')
    if not main: return
    for old in doc.select('[data-reading-owned], .mythos-reader, .mythos-reading-toc'): old.decompose()
    article=main.select_one('article.content') or main
    headings=[h for h in article.select('h2') if not h.find_parent(['nav','aside']) and not h.find_parent(class_='toc')]
    is_portal=bool(doc.select_one('.portal-section, #greek-unified-corpus')) or url.startswith(('/parcours/','/etat-du-corpus/','/catalogue-integral/','/methode-editoriale/','/rubriques/','/recherche/'))
    if entry['words'] < 450 or len(headings)<3 or is_portal: return
    article['data-mythos-reader']='true'
    used={x['id'] for x in doc.select('[id]')}
    for i,h in enumerate(headings,1):
        if not h.get('id'):
            candidate='lecture-section-'+str(i)
            while candidate in used: candidate+='-suite'
            h['id']=candidate;used.add(candidate)
        h['data-reading-section']='true'
    toc='<details class="mythos-reading-toc" data-reading-owned="true"><summary>Sommaire de lecture · '+str(len(headings))+' sections</summary><ol>'+''.join('<li><a href="#'+escape(h['id'],quote=True)+'">'+escape(h.get_text(' ',strip=True))+'</a></li>' for h in headings)+'</ol></details>'
    toolbar='''<div class="mythos-reader" data-reading-owned="true"><p>Lecture : environ '''+str(entry['minutes'])+''' min · <a href="/methode-editoriale/">Sources et méthode</a></p><div class="reader-buttons" hidden><button type="button" data-reader="smaller" aria-label="Réduire la taille du texte">A−</button><button type="button" data-reader="larger" aria-label="Agrandir la taille du texte">A+</button><button type="button" data-reader="focus" aria-pressed="false">Lecture épurée</button><button type="button" data-reader="previous">Section précédente</button><button type="button" data-reader="next">Section suivante</button><button type="button" data-reader="print">Imprimer / PDF</button></div><progress class="reader-progress" max="100" value="0" aria-label="Progression dans l’étude" hidden></progress></div>'''
    article.insert(0,fragment(toc));article.insert(0,fragment(toolbar))
    foot='<nav class="reader-bottom" data-reading-owned="true" aria-label="Poursuivre la lecture"><a href="#'+escape(headings[0]['id'],quote=True)+'">Revenir au début de l’étude</a> · <a href="/parcours/">Choisir un parcours</a> · <a href="/catalogue-integral/">Catalogue intégral</a></nav>'
    article.append(fragment(foot))


def epic_links(doc, url):
    for key,(title,narrative,author,source,citation) in EPICS.items():
        study='/philosophie-'+key+'.html'
        if url not in (study,narrative): continue
        main=doc.main
        if not main: continue
        article=main.select_one('article.content') or main
        for old in article.select('[data-epic-owned]'): old.decompose()
        if url==study:
            box='<nav class="epic-links" data-epic-owned="true" aria-label="Les lectures de cette œuvre"><a href="'+narrative+'">Lire le récit et ses épisodes</a> · <a href="#sources-edition">Éditions et références</a> · <a href="/assets/philosophie/pdf/'+key+'-etude-a4.pdf">Télécharger l’étude en PDF</a></nav>'
            bibliography='<section id="sources-edition" data-epic-owned="true" class="editorial-sources"><h2>Éditions et références pour poursuivre</h2><p>'+escape(citation)+' <a href="'+source+'">Consulter la notice et le texte</a>.</p>'
            if key!='theogonie':
                bibliography+='<p>Gregory Nagy, <em>The Best of the Achaeans: Concepts of the Hero in Archaic Greek Poetry</em>, première édition 1979, deuxième édition 1999. <a href="https://chs.harvard.edu/book/nagy-gregory-the-best-of-the-achaeans-concepts-of-the-hero-in-archaic-greek-poetry/">Texte accessible au Center for Hellenic Studies</a>. Il s’agit d’une interprétation moderne de la poésie et de l’héroïsme archaïques.</p>'
            else:
                bibliography+='<p><a href="https://chs.harvard.edu/primary-source/hesiod-theogony-sb/">Traduction anglaise au Center for Hellenic Studies</a> : vers 1–115 par Gregory Nagy, vers 116–1022 par J. Banks, adaptation par Gregory Nagy. Elle ne remplace pas la confrontation au texte grec.</p>'
            bibliography+='<p>Repérage bibliographique mis à jour le 4 novembre 2026. Cette mise à jour porte sur les ressources indiquées ici ; elle ne constitue pas une certification scientifique de toute l’étude.</p></section>'
            article.append(fragment(bibliography))
        else:
            box='<nav class="epic-links" data-epic-owned="true" aria-label="Approfondir cette œuvre"><a href="'+study+'">Lire l’analyse philosophique de '+escape(title)+'</a> · <a href="/philosophie/">Toutes les analyses philosophiques</a></nav>'
        article.insert(0,fragment(box))


def authored_blocks(doc):
    copy=fragment(str(doc.main or doc.body))
    for node in copy.select('[data-reading-owned], [data-epic-owned], [data-discovery-footer]'): node.decompose()
    return Counter(node.get_text(' ',strip=True) for node in copy.select('p,li,h2,h3,blockquote,figcaption,td') if node.get_text(' ',strip=True))


def enhance(out, root):
    """One inventory, derived search metadata and accessible reading controls."""
    entries=json.loads((out/'search.json').read_text())
    numbers=json.loads((out/'catalog/numbering.json').read_text())['collections']
    number_by_url={x['url']:dict(number=x['number'],numbering_collection=key,source=x['source']) for key,items in numbers.items() for x in items}
    complete=[]
    for entry in entries:
        path=page_path(out,entry['url'])
        if not path.is_file(): raise RuntimeError('Page indexée absente : '+entry['url'])
        doc=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        before=authored_blocks(doc)
        epic_links(doc,entry['url'])
        record=metadata(entry,doc)
        record.update(number_by_url.get(entry['url'],{}))
        source=root/(record.get('source') or path.relative_to(out))
        record['source']=source.relative_to(root).as_posix()
        record['source_sha256']=sha256(source.read_bytes()).hexdigest() if source.is_file() else None
        add_reading(doc,entry['url'],record)
        # All pages retain the approved visual identity; this layer adds controls.
        if doc.head:
            for old in doc.select('link[href*="mythos-discovery.css"]'):old.decompose()
            doc.head.append(doc.new_tag('link',rel='stylesheet',href='/assets/mythos-discovery.css?v='+VERSION))
            if not doc.select_one('link[rel="canonical"]'):
                doc.head.append(doc.new_tag('link',rel='canonical',href='https://bobmythos.fr'+entry['url']))
        if doc.body:
            for old in doc.select('script[src*="mythos-reading.js"]'):old.decompose()
            doc.body.append(doc.new_tag('script',src='/assets/mythos-reading.js?v='+VERSION,defer=''))
            footer=doc.find('footer')
            if footer and not footer.select_one('[data-discovery-footer]'):
                footer.append(fragment('<p data-discovery-footer="true"><a href="/parcours/">Parcours</a> · <a href="/catalogue-integral/">Catalogue</a> · <a href="/methode-editoriale/">Méthode</a> · <a href="/etat-du-corpus/">État du corpus</a></p>'))
        if before-authored_blocks(doc):
            raise RuntimeError('Texte altéré par les outils de lecture : '+entry['url'])
        path.write_text(str(doc),encoding='utf-8')
        complete.append(record)
    # Home is deliberately excluded by the older index, so install its CSS here.
    home=out/'index.html'
    doc=BeautifulSoup(home.read_text(),'html.parser')
    for old in doc.select('.mythos-directory'): old.decompose()
    if not doc.select_one('link[href*="mythos-discovery.css"]'):
        doc.head.append(doc.new_tag('link',rel='stylesheet',href='/assets/mythos-discovery.css?v='+VERSION))
    doc.select_one('[data-corpus-count]').string=str(len(complete))+' entrées disponibles dans le catalogue · textes et archives conservés.'
    home.write_text(str(doc),encoding='utf-8')
    search=out/'recherche/index.html'
    search_doc=BeautifulSoup(search.read_text(),'html.parser')
    for old in search_doc.select('link[href*="mythos-discovery.css"]'):old.decompose()
    search_doc.head.append(search_doc.new_tag('link',rel='stylesheet',href='/assets/mythos-discovery.css?v='+VERSION))
    search.write_text(str(search_doc),encoding='utf-8')
    (out/'catalog/entries.json').write_text(json.dumps({'version':1,'entries':complete},ensure_ascii=False,separators=(',',':'))+'\n')
    (out/'search.json').write_text(json.dumps(complete,ensure_ascii=False,separators=(',',':'))+'\n')
    inventory=out/'etat-du-corpus/index.html'
    doc=BeautifulSoup(inventory.read_text(),'html.parser')
    counts=Counter(x['collection'] for x in complete)
    body='<p>Le catalogue compte <strong>'+str(len(complete))+' entrées</strong>. Chaque entrée possède une adresse et un identifiant stable. Les nombres ci-dessous comptent des pages, y compris des portails et des archives, et non autant d’études scientifiques inédites.</p><table><thead><tr><th>Collection</th><th>Entrées</th></tr></thead><tbody>'+''.join('<tr><td>'+escape(k)+'</td><td>'+str(v)+'</td></tr>' for k,v in sorted(counts.items()))+'</tbody></table>'
    body+='<h2>Textes disponibles et lacunes historiques</h2><p>Une page construite est disponible dans le fichier de publication. Sa présence dans le catalogue ne suffit pas à prouver une relecture scientifique ou l’exhaustivité historique de la collection. Les manuscrits anciens non retrouvés sont signalés dans <a href="/mythologie-grecque/#greek-unified-corpus">le sommaire unifié grec</a>.</p><h2>Contrôles de publication</h2><p>Les adresses du catalogue, les fichiers et les numéros sont vérifiés avant déploiement. Un contrôle HTTP est ensuite exécuté sur les pages publiques. <a href="https://github.com/Bobcribb/Bobcribb.github.io/actions/workflows/publish.yml">Consulter le résultat des publications</a>.</p><p><a href="/catalog/entries.json">Catalogue structuré</a> · <a href="/catalog/publication-verification.json">Rapport de conservation</a> · <a href="/catalog/reading-audit.json">Contrôle de navigation</a></p><h2>Grandes études philosophiques</h2><p>Les trois études longues disposent chacune d’un PDF illustré et d’un PDF d’analyse seule. Les empreintes des six fichiers et leur pagination A4 sont contrôlées à chaque publication.</p><div id="epic-pdf-status"></div>'
    doc.select_one('#corpus-inventory').append(fragment(body))
    inventory.write_text(str(doc),encoding='utf-8')
    print('Catalogue enrichi et lecture :',len(complete),'entrées')
    return complete


def audit(out):
    """Block broken new navigation; report legacy faults without hiding them."""
    (out/'catalog/reading-audit.json').write_text('{"status":"running"}\n')
    catalogue=json.loads((out/'catalog/entries.json').read_text())['entries']
    ids=[e['id'] for e in catalogue];urls=[e['url'] for e in catalogue]
    assert len(ids)==len(set(ids)) and len(urls)==len(set(urls)), 'Doublon du catalogue'
    pages={p.resolve():BeautifulSoup(p.read_text(),'html.parser') for p in out.rglob('*.html')}
    page_ids={p:{str(n['id']) for n in d.select('[id]')} | {str(n['name']) for n in d.select('a[name]')} for p,d in pages.items()}
    critical=[];legacy=[];checked=0;readers=0
    new_pages={'index.html','recherche/index.html','catalogue-integral/index.html','etat-du-corpus/index.html','methode-editoriale/index.html'}
    for page,doc in pages.items():
        rel=page.relative_to(out.resolve()).as_posix()
        owned_page=rel in new_pages or rel.startswith('parcours/')
        readers+=bool(doc.select_one('[data-mythos-reader]'))
        for tag in doc.select('a[href],img[src],script[src],link[href]'):
            attr='href' if tag.has_attr('href') else 'src'
            url=str(tag[attr]);parts=urlsplit(url)
            if parts.scheme or parts.netloc or not url:continue
            absolute=urlsplit(urljoin('https://bobmythos.fr/'+rel,url))
            target=(out/ unquote(absolute.path).lstrip('/')).resolve()
            if target.is_dir() or not target.suffix:target=target/'index.html'
            error=None
            if not target.is_file():error='fichier absent'
            elif (parts.fragment and target in pages
                  and unquote(parts.fragment) not in page_ids[target]):
                # This historical library uses #/accueil as a JS router path,
                # not a missing HTML anchor. Keep real missing anchors visible.
                router_hash = (rel == 'corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html'
                               and target == page and parts.fragment.startswith('/'))
                if not router_hash:
                    error = 'ancre absente'
            checked+=1
            if error:
                issue={'page':'/'+rel,'url':url,'problem':error}
                owned=owned_page or tag.find_parent(attrs={'data-reading-owned':'true'}) or tag.find_parent(attrs={'data-epic-owned':'true'}) or tag.find_parent(attrs={'data-discovery-footer':'true'})
                (critical if owned else legacy).append(issue)
    report={'status':'failed' if critical else 'passed','indexed_entries':len(catalogue),'pages_scanned':len(pages),'readers_equipped':readers,'links_checked':checked,'new_navigation_errors':critical,'legacy_link_issues':legacy}
    (out/'catalog/reading-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if critical:raise RuntimeError('Navigation nouvelle invalide : '+json.dumps(critical[:12],ensure_ascii=False))
    print('Navigation vérifiée :',checked,'liens ;',readers,'lecteurs ;',len(legacy),'anomalies historiques signalées')
    return report
