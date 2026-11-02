#!/usr/bin/env python3
"""Navigation éditoriale de MYTHOS — encyclopédie des mythologies du monde.

Exécuté seulement dans _site/ après la première indexation GitHub.
Crée des portails pérennes, sans modifier les articles originaux ni utiliser WordPress.
"""
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
import html
import json
import re

OUT = Path("_site")
GOLD="BIBLIOTHÈQUE UNIVERSITAIRE · MYTHOS"
NAV = '''<nav class="site-nav" aria-label="Navigation principale">
<a href="/grece/" class="nav-greece">Grèce</a>
<a href="/dieux-et-deesses/">Dieux</a>
<a href="/heros-et-heroines/">Héros</a>
<a href="/recits-mythologiques/">Récits</a>
<a href="/mythologies/">Mythologies</a>
<a href="/theatre/">Théâtre</a>
<a href="/origines-du-sacre/">Origines du sacré</a>
<a href="/philosophie/">Philosophie</a>
<a href="/civilisations/">Civilisations</a>
<a href="/recherche/">Recherche</a>
</nav>'''

CONTINENTS = {
 "afrique": ("Afrique","Égypte ancienne, Afrique du Nord, royaumes du Nil et traditions subsahariennes"),
 "europe": ("Europe","Grèce, Rome, Méditerranée européenne, Celtes et sociétés anciennes"),
 "asie": ("Asie","Mésopotamie, Proche-Orient, Iran, Inde, Chine, Japon et routes de l'Asie"),
 "ameriques": ("Amériques","Amérique du Nord, Mésoamérique, monde andin et civilisations précolombiennes"),
 "oceanie": ("Océanie","Rapa Nui, cultures insulaires et navigations du Pacifique"),
}
AFRICAN = ("afrique","aksoum","carthage","zagwe","garamantes","grand-zimbabwe","ife-yoruba","swahili","mali-songhai","mapungubwe","koush","numidie","benin","makouria","kongo","egypte")
EUROPEAN = ("daces","romain-orient","grece-antique","celtes-gaules","rome-antique","sardaigne","tartessos","thraces","etrusques","egee-bronze")
AMERICAN = ("sonora","andes","cahokia","caral","chavin","chimu","el-tajin","mexicas","mixteques","mochicas","mayas","olmeques","pueblos","muisca","teotihuacan","tiwanaku","tolteques","uxmal","zapoteques")
OCEANIAN = ("oceanie","rapa-nui")

def esc(x): return html.escape(str(x),quote=True)
def write(slug,content):
    p=OUT/slug/"index.html"
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content,encoding="utf-8")

def shell(title,body,desc=""):
    description=desc or "MYTHOS — Encyclopédie des mythologies du monde : sources, peuples, récits, théâtre et philosophie."
    return f'''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="description" content="{esc(description)}">
<title>{esc(title)} | MYTHOS</title><link rel="stylesheet" href="/assets/style.css"></head>
<body><header class="masthead"><div class="masthead-inner"><a class="brand" href="/" aria-label="MYTHOS — Accueil">MYTHOS <span>✦</span></a>{NAV}</div></header>
<main class="layout portal-layout"><article class="content" id="contenu"><div class="eyebrow">{GOLD}</div>{body}</article></main>
<footer class="footer"><span>MYTHOS — Encyclopédie des mythologies du monde</span>
<a href="/rubriques/">Index complet des dossiers</a></footer>
<script defer src="/assets/search.js"></script></body></html>'''

def section(title,lead="",body=""):
    return f'<section class="portal-section"><h2>{esc(title)}</h2>'+ (f'<p class="section-intro">{esc(lead)}</p>' if lead else "")+body+"</section>"

def card(url,title,description="",label="COLLECTION"):
    return f'<a class="portal-card" href="{esc(url)}"><span class="portal-card-kicker">{esc(label)}</span><strong>{esc(title)}</strong><span>{esc(description)}</span><span class="card-indicator" aria-hidden="true">↗</span></a>'

def cards(items,cols=""):
    return '<div class="portal-grid '+esc(cols)+'">'+''.join(card(*x) for x in items)+"</div>"

def link(url,label):
    return f'<a href="{esc(url)}">{esc(label)}</a>'

def list_entries(entries,limit=None):
    rows=entries if limit is None else entries[:limit]
    return '<ul class="portal-list">'+''.join('<li><a href="'+esc(e["url"])+'">'+esc(e["title"])+'</a></li>' for e in rows)+'</ul>'

def details(items,label):
    return '<details class="library-details"><summary>'+esc(label)+' <span aria-hidden="true">＋</span></summary>'+list_entries(items)+'</details>'

def starts(entry,*prefixes):
    return any(entry["url"].startswith(x) for x in prefixes)

def group_continent(entry):
    slug=entry["url"].split("/")[-2]
    if any(token in slug for token in OCEANIAN): return "oceanie"
    if any(token in slug for token in AMERICAN): return "ameriques"
    if any(token in slug for token in AFRICAN): return "afrique"
    if any(token in slug for token in EUROPEAN): return "europe"
    return "asie"

def get_civilisations(entries):
    selected=[e for e in entries
        if re.search(r"/civilisations?-[^/]+/$",e["url"])
        and e["url"]!="/bibliotheque-mythologies-du-monde/civilisations-histoire-encyclopedie-sommaire/"]
    groups={key:[] for key in CONTINENTS}
    for e in selected:
        groups[group_continent(e)].append(e)
    return groups

def create_home(entries,groups):
    introductory='''<section class="hero hero-editorial">
<div class="eyebrow">LE MONDE DES MYTHES, DES DIEUX ET DES CIVILISATIONS</div>
<h1>MYTHOS<span class="hero-dot">.</span></h1>
<div class="gold-line"></div>
<p class="hero-deck">Une encyclopédie des mythologies du monde.</p>
<p class="hero-secondary">Des récits de la Grèce antique aux cosmologies de l’Égypte, de la Mésopotamie, des Amériques, de l’Asie et de l’Océanie — sources, comparaisons, histoire et interprétations.</p>
<div class="hero-links"><a class="primary-link" href="/mythologies/">Explorer les mythologies</a><a class="secondary-link" href="/rubriques/">Index alphabétique intégral</a></div>
</section>'''
    major=cards([
      ("/grece/","Grèce antique","Dieux, héros, Homère, Hésiode, cultes, sanctuaires et récits.","DOSSIER À LA UNE"),
      ("/mythologies/","Mythologies du monde","Cosmogonies, panthéons, récits fondateurs et traditions comparées.","LE CŒUR DE MYTHOS"),
      ("/theatre/","Théâtre grec","Eschyle, Sophocle, Euripide, Aristophane, Ménandre, œuvres perdues.","ŒUVRES ET FRAGMENTS"),
      ("/origines-du-sacre/","Origines du sacré","Préhistoire, rituels, chants, temps sacré et religions comparées.","GRAND DOSSIER"),
      ("/philosophie/","Études philosophiques","Hegel, Nietzsche, philosophie antique et interprétation des mythes.","ANALYSE CRITIQUE"),
    ])
    continent_cards=cards([(f"/civilisations/{k}/",label,f"{len(groups[k])} dossiers — {subtitle}","PAR CONTINENT") for k,(label,subtitle) in CONTINENTS.items()])
    world=cards([
        ("/bibliotheque-egypte-ancienne/","Égypte ancienne","Osiris, Rê, Maât, Akhetaton et l’au-delà.","AFRIQUE"),
        ("/bibliotheque-mesopotamie/","Mésopotamie","Gilgameš, Inanna, Marduk et les mythes de la création.","ASIE"),
        ("/bibliotheque-perse-iran-ancien/","Perse et Iran ancien","Ahura Mazdā, royauté et traditions iraniennes.","ASIE"),
        ("/bibliotheque-mythologies-du-monde/","Traditions du monde","Dictionnaire des dieux, héros et récits comparés.","COLLECTION"),
    ])
    essentials=cards([
      ("/dieux-et-deesses/","Dieux et déesses","Panthéons, cultes et puissances de toutes les traditions.","GRANDES ENTRÉES"),
      ("/heros-et-heroines/","Héros et héroïnes","Exploits, voyages, fondations et destins.","GRANDES ENTRÉES"),
      ("/recits-mythologiques/","Grands récits","Créations, guerres, déluges, épopées et Enfers.","GRANDES ENTRÉES")
    ],"portal-grid-compact")
    museum='''<section class="portal-section museum-gallery-section" aria-labelledby="museum-gallery-title">
<div class="museum-gallery-heading"><span class="eyebrow">GALERIE ANTIQUE · MYTHOS</span>
<h2 id="museum-gallery-title">Les œuvres et leurs mondes</h2>
<p class="section-intro">Six œuvres et documents pour entrer dans les récits, les cultes et les sanctuaires. Des images conservées dans la médiathèque GitHub, sans dépendance à WordPress.</p></div>
<div class="museum-gallery">
<figure><img loading="lazy" src="/media/2026/10/mythos-bronze-artemision-zeus-ou-poseidon.jpg" alt="Statue de bronze du cap Artémision, représentant Zeus ou Poséidon, attribution discutée."><figcaption><strong>Zeus ou Poséidon</strong><span>Bronze du cap Artémision · identification discutée</span></figcaption></figure>
<figure><img loading="lazy" src="/media/2026/10/mythos-olympie-nike-paionios-jarvis-2005.jpg" alt="Niké sculptée par Paionios, au musée archéologique d’Olympie."><figcaption><strong>Niké de Paionios</strong><span>Olympie · offrande et célébration de la victoire</span></figcaption></figure>
<figure><img loading="lazy" src="/media/2026/10/mythos-artemis-ephesienne-statue-musee-selcuk-furkan-akkurt.jpg" alt="Statue cultuelle dite Artémis Éphésienne, conservée à Selçuk."><figcaption><strong>Artémis Éphésienne</strong><span>Asie Mineure · iconographie cultuelle</span></figcaption></figure>
<figure><img loading="lazy" src="/media/2026/10/mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg" alt="Fragments anciens du papyrus de Derveni, en Grèce."><figcaption><strong>Papyrus de Derveni</strong><span>Texte ancien · traditions et interprétation</span></figcaption></figure>
<figure><img loading="lazy" src="/media/2026/10/mythos-papyrus-ani-pesee-coeur-british-museum.jpg" alt="Scène de la pesée du cœur du papyrus funéraire d’Ani en Égypte."><figcaption><strong>Papyrus d’Ani</strong><span>Égypte · représentation funéraire</span></figcaption></figure>
<figure><img loading="lazy" src="/media/2026/10/mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg" alt="Tablette cunéiforme de l’épopée de création babylonienne Enūma eliš."><figcaption><strong>Tablette d’Enūma eliš</strong><span>Mésopotamie · écriture et cosmogonie</span></figcaption></figure>
</div></section>'''
    body=introductory+museum+section("Dieux, héros et récits — les trois grandes entrées","Accédez directement aux personnages et aux histoires des mythologies grecque et mondiale.",essentials)
    body+=section("Les grands parcours de recherche","Choisissez un monde, un genre littéraire ou une méthode d’étude.",major)
    body+=section("Aux origines des religions","Des témoignages matériels aux traditions écrites, sans confondre indices et certitudes.",cards([("/origines-du-sacre/","Origines du sacré","Un parcours critique sur les rites, les sanctuaires, les images et la mémoire.","NOUVELLE ENTRÉE"),("/chapitres/origines-du-sacre/459-musique-grecque-mousike/","Musique et rites grecs","Mousikē, voix et performance rituelle.","GRÈCE"),("/chapitres/origines-du-sacre/452-delphes-pythie-parole-oraculaire/","La parole oraculaire","Delphes, Pythie et médiation religieuse.","SOURCES")]))
    body+=section("Civilisations du monde, par continent","Une géographie de consultation moderne : les échanges et les appartenances historiques débordent les frontières continentales.",continent_cards)
    body+=section("Bibliothèques et traditions à découvrir","Des portes d’entrée vers les principaux corpus.",world)
    body+='''<section class="portal-section search-zone"><h2>Rechercher dans l’encyclopédie</h2>
<p class="section-intro">Un dieu, un héros, une œuvre, une civilisation, un auteur ou un concept.</p>
<input class="search" data-search placeholder="Ex. Athéna, Gilgameš, Sophocle, Maat, Nietzsche…" aria-label="Rechercher dans MYTHOS">
<div class="results" data-results></div>
<p class="small-note">Pour parcourir l’ensemble des dossiers classés par ordre alphabétique, consultez l’<a href="/rubriques/">index intégral</a>.</p></section>'''
    write("",shell("Encyclopédie des mythologies du monde",body))

def create_greece(entries):
    gods=[("/dieu-zeus/","Zeus"),("/dieu-athena/","Athéna"),("/dieu-apollon/","Apollon"),("/dieu-artemis/","Artémis"),("/dieu-dionysos/","Dionysos"),("/dieu-demeter/","Déméter")]
    heroes=[("/heros-achille/","Achille"),("/heros-ulysse/","Ulysse"),("/heros-heracles/","Héraclès"),("/heros-antigone/","Antigone"),("/heros-thesee/","Thésée"),("/heros-medee/","Médée")]
    body='<h1>Grèce antique</h1><p class="portal-lead">Le grand corpus grec est mis au premier plan : des généalogies divines aux héros, des épopées homériques aux pratiques cultuelles des cités.</p>'
    body+=section("Parcourir les dieux, les héros et les mythes","Trois bibliothèques dédiées, la Grèce en premier et une ouverture sur le monde.",cards([
      ("/dieux-et-deesses/","Dieux et déesses","15 monographies grecques et divinités des autres traditions."),
      ("/heros-et-heroines/","Héros et héroïnes","Achille, Médée, Ulysse et les cycles héroïques du monde."),
      ("/recits-mythologiques/","Grands récits","Théogonie, guerre de Troie, épopées et cosmologies comparées.")
    ],"portal-grid-compact"))
    body+=section("Dieux et puissances divines","Entrer par les grandes figures du panthéon.",'<div class="tag-links">'+''.join(link(u,n) for u,n in gods)+'</div>')
    body+=section("Héros, héroïnes et cycles","Une encyclopédie des récits, des variantes et des destins.",'<div class="tag-links">'+''.join(link(u,n) for u,n in heroes)+'</div>')
    body+=section("Épopées, auteurs et sanctuaires","Sources antiques et lieux du culte.",cards([
     ("/iliade/","L’Iliade","Guerre de Troie, colère d’Achille et monde héroïque."),
     ("/odyssee/","L’Odyssée","Voyages d’Ulysse, hospitalité et retour."),
     ("/livre-hesiode/","Hésiode","Théogonie, travail et ordre cosmique."),
     ("/atlas-mythologique/","Atlas grec","Une entrée par les lieux et les sanctuaires."),
     ("/delphes-oracle-apollon-etude/","Delphes","Oracle d’Apollon et pratiques religieuses."),
     ("/theatre/","Théâtre grec","Tragédies, comédies et analyses des pièces.")
    ]))
    write("grece",shell("Mythologie grecque et Grèce antique",body))

def create_mythologies(entries):
    body='<h1>Mythologies du monde</h1><p class="portal-lead">Une encyclopédie comparée des dieux, des cosmogonies, des héros et des pratiques religieuses, fondée sur les textes et sur les témoignages matériels. La Grèce demeure notre point d’entrée privilégié, mais non notre seule perspective.</p>'
    body+=section("Commencer par les figures et les histoires","Trois entrées fondamentales pour parcourir les traditions.",cards([
      ("/dieux-et-deesses/","Dieux et déesses","Panthéons grecs et divinités du monde."),
      ("/heros-et-heroines/","Héros et héroïnes","Destins, lignées et cycles épiques."),
      ("/recits-mythologiques/","Grands récits","Cosmogonies, voyages, déluges et épopées.")
    ],"portal-grid-compact"))
    body+=section("Les grandes traditions","Panthéons, cosmologies et traditions documentées.",cards([
     ("/grece/","Grèce antique","Olympiens, Titans, héros et sanctuaires.","À LA UNE"),
     ("/bibliotheque-egypte-ancienne/mythologie-egypte-cosmogonies-osiris-maat-au-dela/","Égypte","Cosmogonies, Osiris, Maât et textes funéraires."),
     ("/bibliotheque-mesopotamie/mythologie-mesopotamie-enuma-elish-gilgamesh-inanna/","Mésopotamie","Enūma eliš, Gilgameš, Inanna et Marduk."),
     ("/bibliotheque-perse-iran-ancien/","Perse et Iran","Mazdéisme, figures divines et royauté."),
     ("/bibliotheque-mythologies-du-monde/mythologie-inde-vedas-puranas-vishnu-shiva-devi/","Inde","Veda, épopées, Purāṇa et divinités."),
     ("/bibliotheque-mythologies-du-monde/mythologie-chinoise-nuwa-pangu-shanhaijing/","Chine","Nüwa, Pangu et traditions des immortels."),
     ("/bibliotheque-mythologies-du-monde/mythologie-japonaise-kojiki-nihon-shoki-kami/","Japon","Kami, Kojiki et cosmogonies."),
     ("/civilisations/ameriques/","Amériques","Mondes mayas, mexicas et andins."),
    ]))
    body+=section("Figures, récits et méthodes","Parcours transversaux au-delà d’un seul panthéon.",cards([
      ("/bibliotheque-mythologies-du-monde/dictionnaire-dieux-monde/","Dictionnaire des dieux","Monographies des puissances et de leurs cultes."),
      ("/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/","Héros du monde","Cycles épiques, voyages et récits."),
      ("/civilisations/","Civilisations par continent","Contexte historique et culturel des traditions."),
      ("/philosophie/","Interpréter les mythes","Lectures philosophiques et comparaisons.")
    ]))
    write("mythologies",shell("Mythologies du monde",body))


# Trois entrées centrales distinctes et indexées : dieux, héros et récits.
# Les études grecques /dieux/, /heros/, /recits/ ne sont ni supprimées
# ni remplacées ; elles restent accessibles dans chaque nouveau portail.
def create_figures_and_stories(entries):
    known={e["url"]:e for e in entries}

    def references(urls):
        # Ne pas fabriquer des titres ou des adresses : n'afficher que
        # les dossiers dont le chemin figure effectivement dans l'index.
        return [known[url] for url in urls if url in known]

    def curated_section(title,description,urls):
        items=references(urls)
        return section(title,description,list_entries(items)) if items else ""

    greek_deities=[e for e in entries if re.fullmatch(r"/dieu-[a-z0-9-]+/",e["url"])]
    global_deities=[e for e in entries if e["url"].startswith("/bibliotheque-mythologies-du-monde/dictionnaire-dieux-monde/")
                    and e["url"]!="/bibliotheque-mythologies-du-monde/dictionnaire-dieux-monde/"]
    greek_heroes=[e for e in entries if re.fullmatch(r"/heros-[a-z0-9-]+/",e["url"])]
    global_heroes=[e for e in entries if e["url"].startswith("/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/")
                   and e["url"]!="/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/"]

    body='<h1>Dieux et déesses</h1><p class="portal-lead">Un atlas des puissances divines, de la Grèce antique aux autres traditions du monde : domaines, généalogies, mythes, cultes, épiclèses et interprétations. Chaque religion est étudiée dans son contexte, sans supposer que tous les dieux ont les mêmes fonctions.</p>'
    body+=section("Entrer dans les panthéons","La Grèce antique est notre première collection ; les autres mythologies ont leurs propres sources.",cards([
        ("/dieux/","Panthéon grec — étude intégrale","Olympiens, puissances divines et transformations des cultes.","GRÈCE À LA UNE"),
        ("/bibliotheque-mythologies-du-monde/dictionnaire-dieux-monde/","Dictionnaire mondial des dieux","Monographies documentées des divinités et puissances."),
        ("/bibliotheque-egypte-ancienne/","Dieux d’Égypte","Rê, Isis, Osiris, Horus, Seth, Thot et les traditions du Nil."),
        ("/bibliotheque-mesopotamie/","Dieux de Mésopotamie","Enki, Enlil, Inanna, Marduk et les cités-temples."),
        ("/bibliotheque-perse-iran-ancien/","Iran et Perse","Traditions religieuses de l’Iran ancien."),
        ("/mythologies/","Tous les mondes mythologiques","Inde, Chine, Japon, traditions nordiques et autres corpus.")
    ]))
    body+=section("Tous les dieux grecs documentés",f"{len(greek_deities)} notices individuelles accessibles par nom.",list_entries(greek_deities))
    body+=section("Divinités et puissances des autres traditions",f"{len(global_deities)} monographies actuellement indexées, avec leurs propres cadres historiques.",list_entries(global_deities))
    body+=section("Comparer les mythes sans confondre les cultes","Croiser figures, épopées et cosmologies.",cards([
        ("/heros-et-heroines/","Héros et héroïnes","Les humains, demi-dieux et personnages des traditions épiques."),
        ("/recits-mythologiques/","Grands récits","Les mythes dans leur enchaînement narratif et leurs variantes."),
        ("/civilisations/","Civilisations","Les sociétés et lieux de transmission des traditions.")
    ]))
    write("dieux-et-deesses",shell("Dieux et déesses du monde",body))

    body='<h1>Héros et héroïnes</h1><p class="portal-lead">Les parcours héroïques ne sont pas interchangeables : exploits, épreuves, fondations, exils, transgressions, destins tragiques et mémoire des communautés. MYTHOS relie chaque personnage à ses sources et à ses traditions.</p>'
    body+=section("Les grands univers héroïques","Un accès direct aux études grecques et aux cycles épiques du monde.",cards([
        ("/heros/","Héros de la Grèce antique","Étude intégrale des héros, héroïnes et destins.","GRÈCE À LA UNE"),
        ("/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/","Héros des mythologies du monde","Épopées et cycles de différentes traditions."),
        ("/livre-troie/","Guerre de Troie","Achille, Hector, Hélène et les mémoires troyennes."),
        ("/livre-argonautiques/","Argonautes","Jason, Médée et les récits de la Toison d’or."),
        ("/livre-thebes/","Cycle thébain","Cadmos, Œdipe, Antigone et les Labdacides."),
        ("/recits-mythologiques/","Voyages et récits","Replacer les aventures dans leurs grandes histoires.")
    ]))
    body+=section("Héros et héroïnes grecs",f"{len(greek_heroes)} monographies individuelles disponibles.",list_entries(greek_heroes))
    body+=section("Figures héroïques d’autres traditions",f"{len(global_heroes)} dossiers et cycles épiques, de Gilgameš à Sunjata et Māui.",list_entries(global_heroes))
    body+=section("Lire et interpréter les parcours","Le héros comme figure sociale, religieuse et littéraire.",cards([
        ("/theatre/","Tragédie et comédie","Mises en scène des héros et leurs conflits."),
        ("/philosophie/","Interprétations philosophiques","Justice, destin, liberté, violence et reconnaissance."),
        ("/dieux-et-deesses/","Dieux et déesses","Les puissances auxquelles les héros sont confrontés.")
    ]))
    write("heros-et-heroines",shell("Héros et héroïnes des mythologies du monde",body))

    greek_cycles=references([
        "/livre-hesiode/","/livre-heracles/","/livre-argonautiques/","/livre-thebes/",
        "/livre-atrides/","/livre-troie/","/livre-iliade-scenes/","/livre-odyssee/",
        "/iliade/","/odyssee/"
    ])
    ancient_world=references([
        "/enuma-elish-marduk-tiamat-creation-babylone/",
        "/atrahasis-creation-humanite-deluge-mesopotamie/",
        "/gilgamesh-epopee-mort-deluge/",
        "/inanna-ishtar-descente-enfers-sumer-akkad/",
        "/bibliotheque-egypte-ancienne/mythologie-egypte-cosmogonies-osiris-maat-au-dela/",
        "/livre-des-morts-papyrus-ani-pesee-coeur-osiris/",
        "/bibliotheque-mythologies-du-monde/mythologie-inde-vedas-puranas-vishnu-shiva-devi/",
        "/bibliotheque-mythologies-du-monde/mythologie-chinoise-nuwa-pangu-shanhaijing/",
        "/bibliotheque-mythologies-du-monde/mythologie-japonaise-kojiki-nihon-shoki-kami/"
    ])
    body='<h1>Grands récits mythologiques</h1><p class="portal-lead">Cosmogonies, origines des dieux et des humains, fondations, aventures héroïques, guerres, descentes aux Enfers, déluges et fins du monde. Les récits sont présentés comme des traditions multiples, et non comme une chronologie universelle unique.</p>'
    body+=section("La grande bibliothèque des récits","Les cycles grecs d’abord, puis les traditions textuelles et orales d’autres régions.",cards([
        ("/recits/","Récits grecs — étude intégrale","Des origines cosmiques aux retours après Troie.","GRÈCE À LA UNE"),
        ("/livre-hesiode/","Théogonie et premiers âges","Les générations divines et l’établissement de l’ordre cosmique."),
        ("/livre-troie/","La guerre de Troie","Généalogies, guerre et mémoire des héros."),
        ("/livre-odyssee/","Le retour d’Ulysse","Épreuves, reconnaissance et hospitalité."),
        ("/bibliotheque-mesopotamie/mythologie-mesopotamie-enuma-elish-gilgamesh-inanna/","Récits mésopotamiens","Création, déluge, royauté et immortalité."),
        ("/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/","Épopées du monde","Des récits d’Inde aux Amériques et à l’Océanie.")
    ]))
    body+=section("Les cycles grecs",f"{len(greek_cycles)} dossiers narratifs et guides de lecture.",list_entries(greek_cycles))
    body+=section("Cosmogonies et récits du monde","Des corpus et des textes à aborder dans leur langue et leur contexte.",list_entries(ancient_world))
    body+=section("Épopées des autres cultures","Les épisodes héroïques dans les traditions celtiques, iraniennes, indiennes, africaines, américaines et océaniennes.",list_entries(global_heroes))
    body+=section("Approfondir les sources","Relier chaque récit aux personnages et aux problèmes interprétatifs.",cards([
        ("/dieux-et-deesses/","Dieux et déesses","Les puissances actives dans les mythes."),
        ("/heros-et-heroines/","Héros et héroïnes","Les figures et les lignées des récits."),
        ("/philosophie/","Études philosophiques","Analyser les fonctions et lectures des mythes."),
        ("/civilisations/","Civilisations du monde","Situer les récits dans le temps et l’espace.")
    ]))
    write("recits-mythologiques",shell("Grands récits mythologiques du monde",body))
    print("MYTHOS FIGURES :",len(greek_deities),"dieux grecs,",len(global_deities),"divinités du monde,",len(greek_heroes),"héros grecs,",len(global_heroes),"cycles du monde,",len(greek_cycles),"récits grecs.",flush=True)


def museum_figures(figures, heading="Images et objets à observer"):
    """Images déjà conservées dans le dépôt, avec légendes explicites."""
    figs=[]
    for file,alt,caption in figures:
        figs.append('<figure class="museum-object"><img loading="lazy" decoding="async" src="/media/2026/10/'+esc(file)+'" alt="'+esc(alt)+'"><figcaption>'+esc(caption)+'</figcaption></figure>')
    return '<section class="portal-section museum-feature"><h2>'+esc(heading)+'</h2><div class="museum-objects">'+''.join(figs)+'</div></section>'

def numbered_works(items, kind):
    """Numéros locaux à l'auteur : ne pas les confondre avec les volumes universitaires."""
    if not items:
        return '<p class="small-note">Aucun dossier vérifié dans cette catégorie.</p>'
    return '<ol class="work-list">'+''.join(
        '<li><a href="'+esc(e["url"])+'">'+esc(e["title"].split(" — ",1)[-1].split(" : ",1)[0].split(" | ",1)[0])+'</a><small>'+esc(kind)+'</small></li>'
        for e in items
    )+'</ol>'

def create_origins(entries):
    corpus=[e for e in entries if e["url"].startswith("/chapitres/origines-du-sacre/")]
    numbered=[]
    for e in corpus:
        match=re.search(r"/(\d+)-",e["url"])
        if match:
            numbered.append((int(match.group(1)),e))
    numbered.sort(key=lambda x:x[0])
    body='<h1>Origines du sacré</h1><p class="portal-lead">Une enquête historique et comparée sur les premières manifestations matérielles des rites, la formation des sanctuaires, les images, la parole religieuse et les grandes traditions anciennes. Ni origine unique, ni continuité universelle présumée.</p>'
    body+=museum_figures([
      ("mythos-ounas-chambre-funeraire-vincent-brown.jpg","Textes funéraires dans la pyramide d’Ounas","Égypte ancienne — textes funéraires de la pyramide d’Ounas."),
      ("mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg","Fragments du papyrus de Derveni","Grèce ancienne — papyrus de Derveni, interprétation des traditions orphiques."),
      ("mythos-enheduanna-disque-penn-museum-mefman00.jpg","Disque d’Enheduanna","Mésopotamie — disque associé à Enheduanna et à l’univers cultuel mésopotamien."),
      ("mythos-yazilikaya-chambre-b-douze-dieux-ywpark.jpg","Reliefs de divinités à Yazılıkaya","Anatolie hittite — cortège de divinités du sanctuaire de Yazılıkaya.")
    ],"Documents et sanctuaires : regarder les sources")
    body+=section("Les grandes questions","Un classement thématique avant la succession des volumes.",cards([
      ("/chapitres/origines-du-sacre/452-delphes-pythie-parole-oraculaire/","Oracles et médiations","La parole divine dans les cités grecques.","RITES"),
      ("/chapitres/origines-du-sacre/459-musique-grecque-mousike/","Musique et performance","La mousikē grecque, les chœurs et la fête.","GRÈCE"),
      ("/chapitres/origines-du-sacre/468-mesopotamie-akitu-annee/","Temps sacré","Le calendrier rituel et l’Akītu mésopotamien.","MÉSOPOTAMIE"),
      ("/chapitres/origines-du-sacre/462-egypte-sistre-hathor/","Gestes et objets cultuels","Le sistre, Hathor et la musique rituelle.","ÉGYPTE")
    ]))
    body+=section("Chapitres de la collection","Numérotation d'origine conservée : elle désigne les chapitres de la série, et non les œuvres du théâtre grec.",
      '<ol class="chapter-list">'+''.join('<li value="'+str(n)+'"><a href="'+esc(e["url"])+'">'+esc(e["title"])+'</a><span class="chapter-topic">'+esc(e["url"].split("/")[-2].split("-",1)[-1].replace("-"," "))+'</span></li>' for n,e in numbered)+'</ol>'
      +details([e for e in corpus if not re.search(r"/\d+-",e["url"])],"Tomes et dossiers complémentaires"))
    body+=section("Méthode et limites","Une image ou une sépulture ne suffit pas à démontrer une croyance déterminée.",
      '<p>Les datations, les contextes archéologiques, les textes anciens et les interprétations modernes sont présentés comme des niveaux de preuve distincts. Les analogies entre civilisations sont discutées, et non posées comme des filiations certaines.</p>')
    write("origines-du-sacre",shell("Origines du sacré — MYTHOS",body))

def create_theatre(entries):
    """Théâtre grec : corpus méthodique vérifié dans search.json, sans renuméroter les volumes."""
    catalog={e["url"]:e for e in entries}
    tragic_specs={"Eschyle":[["Les Perses","eschyle-perses-analyse"],["Les Sept contre Thèbes","eschyle-sept-contre-thebes-analyse"],["Les Suppliantes","eschyle-suppliantes-danaides-analyse"],["Agamemnon","eschyle-agamemnon-analyse"],["Les Choéphores","eschyle-choephores-analyse"],["Les Euménides","eschyle-eumenides-analyse"],["Prométhée enchaîné (attribution discutée)","eschyle-promethee-enchaine-analyse"]],"Sophocle":[["Ajax","sophocle-ajax-analyse"],["Antigone","sophocle-antigone-lecture-critique"],["Les Trachiniennes","sophocle-trachiniennes-analyse"],["Œdipe roi","sophocle-oedipe-roi-analyse"],["Électre","sophocle-electre-analyse"],["Philoctète","sophocle-philoctete-analyse"],["Œdipe à Colone","sophocle-oedipe-a-colone-analyse"]],"Euripide":[["Alceste","euripide-alceste-analyse"],["Médée","euripide-medee-analyse"],["Les Héraclides","euripide-heraclides-analyse"],["Hippolyte","euripide-hippolyte-analyse"],["Andromaque","euripide-andromaque-analyse"],["Hécube","euripide-hecube-analyse"],["Les Suppliantes","euripide-suppliantes-analyse"],["Héraclès","euripide-heracles-analyse"],["Ion","euripide-ion-analyse"],["Les Troyennes","euripide-troyennes-analyse"],["Électre","euripide-electre-analyse"],["Iphigénie en Tauride","euripide-iphigenie-en-tauride-analyse"],["Hélène","euripide-helene-analyse"],["Les Phéniciennes","euripide-pheniciennes-analyse"],["Oreste","euripide-oreste-analyse"],["Iphigénie à Aulis","euripide-iphigenie-a-aulis-analyse"],["Les Bacchantes","euripide-bacchantes-dionysos-tragedie"],["Rhésos (attribution discutée)","euripide-rhesos-analyse"],["Le Cyclope (drame satyrique)","euripide-cyclope-analyse"]]}
    comedy_specs={"Aristophane":[["Les Acharniens","aristophane-acharniens-etude"],["Les Cavaliers","aristophane-cavaliers-etude"],["Les Nuées","aristophane-nuees-etude"],["Les Guêpes","aristophane-guepes-etude"],["La Paix","aristophane-paix-etude"],["Les Oiseaux","aristophane-oiseaux-etude"],["Lysistrata","aristophane-lysistrata-etude"],["Les Thesmophories","aristophane-thesmophories-etude"],["Les Grenouilles","aristophane-grenouilles-etude"],["L’Assemblée des femmes","aristophane-assemblee-des-femmes-etude"],["Ploutos","aristophane-ploutos-etude"]],"Ménandre":[["Le Dyscolos","menandre-dyscolos-analyse"],["La Samienne","menandre-samia-analyse"],["L’Arbitrage","menandre-epitrepontes-analyse"],["La Femme tondue","menandre-perikeiromene-analyse"],["Le Bouclier","menandre-aspis-analyse"],["Le Sicyonien","menandre-sikyonios-analyse"],["L’Homme haï","menandre-misoumenos-analyse"]]}
    lost_specs=[["Les Banqueteurs","aristophane-banqueteurs-reconstitution","banqueteurs-analyse-philosophique"],["Les Babyloniens","aristophane-babyloniens-reconstitution","babyloniens-analyse-philosophique"],["Les Paysans","aristophane-paysans-reconstitution","paysans-analyse-philosophique"],["Amphiaraos","aristophane-amphiaraos-reconstitution","amphiaraos-analyse-philosophique"],["Polyidos","aristophane-polyidos-reconstitution","polyidos-analyse-philosophique"],["Cocalos","aristophane-cocalos-reconstitution","cocalos-analyse-philosophique"],["Les Danaïdes","aristophane-danaides-reconstitution","danaides-analyse-philosophique"],["Les Lemniennes","aristophane-lemniennes-reconstitution","lemniennes-analyse-philosophique"],["Dédale","aristophane-dedale-reconstitution","dedale-analyse-philosophique"],["Les Héros","aristophane-heros-reconstitution","heros-analyse-philosophique"],["La Vieillesse","aristophane-vieillesse-reconstitution","vieillesse-analyse-philosophique"],["Gérytadès","aristophane-gerytades-reconstitution","gerytades-analyse-philosophique"],["Anagyros","aristophane-anagyros-reconstitution","anagyros-analyse-philosophique"],["Les Saisons","aristophane-saisons-reconstitution","saisons-analyse-philosophique"],["Les Cigognes","aristophane-cigognes-reconstitution","cigognes-analyse-philosophique"],["Les Navires marchands","aristophane-navires-marchands-reconstitution","navires-marchands-analyse-philosophique"],["Les Nuées (première version)","aristophane-nuees-premiere-version-reconstitution","nuees-premiere-version-analyse-philosophique"],["Le Proagôn","aristophane-proagon-reconstitution","proagon-analyse-philosophique"],["Ploutos (première version)","aristophane-ploutos-premiere-version-reconstitution","ploutos-premiere-version-analyse-philosophique"],["Les Hommes à la poêle","aristophane-hommes-poele-reconstitution","hommes-poele-analyse-philosophique"],["Le Centaure (attribution discutée)","aristophane-centaure-reconstitution","centaure-analyse-philosophique"],["La Paix (deuxième version)","aristophane-paix-deuxieme-version-reconstitution","paix-deuxieme-version-analyse-philosophique"],["Les Phéniciennes","aristophane-pheniciennes-reconstitution","pheniciennes-analyse-philosophique"],["Les Telmessiens","aristophane-telmessiens-reconstitution","telmessiens-analyse-philosophique"],["Triphâlès","aristophane-triphales-reconstitution","triphales-analyse-philosophique"],["Les Thesmophories (deuxième version)","aristophane-thesmophories-deuxieme-version-reconstitution","thesmophories-deuxieme-version-analyse-philosophique"],["Aiolosicon (première version)","aristophane-aiolosicon-reconstitution","aiolosicon-premiere-version-analyse-philosophique"],["Les Femmes occupant les tentes","aristophane-femmes-occupant-tentes-reconstitution","femmes-occupant-tentes-analyse-philosophique"],["Aiolosicon (deuxième version)","aristophane-aiolosicon-deuxieme-version-reconstitution","aiolosicon-deuxieme-version-analyse-philosophique"],["Dionysos naufragé (attribution discutée)","dionysos-naufrage-reconstitution","dionysos-naufrage-analyse-philosophique"],["Les Îles (attribution discutée)","les-iles-reconstitution","iles-analyse-philosophique"],["Niobos (attribution discutée)","niobos-reconstitution","niobos-analyse-philosophique"],["La Poésie (attribution discutée)","la-poesie-reconstitution","poesie-analyse-philosophique"]]
    def resolve(prefix):
        matched=[e for e in entries if e["url"].rstrip("/").split("/")[-1].startswith(prefix)]
        if len(matched)!=1:
            raise RuntimeError("Catalogue du théâtre : titre absent ou ambigu : "+prefix+" ("+str(len(matched))+")")
        return matched[0]
    def works(author, specs):
        return [{"url":resolve(key)["url"],"title":author+" — "+title} for title,key in specs]
    tragedies=[e for e in entries if starts(e,"/tragedies/","/chapitres/tragedies/")]
    comedies=[e for e in entries if starts(e,"/comedie-grecque-aristophane-menandre-etudes/","/chapitres/comedies/")]
    lost_t=[e for e in tragedies if "/mythos-theatre-perdu-volume-" in e["url"] and re.search(r"mythos-(eschyle|sophocle|euripide)-",e["url"])]
    lost_t=sorted(lost_t,key=lambda e:e["title"].casefold())
    pairs=[]
    for title,recon_prefix,analysis_prefix in lost_specs:
        reconstruction=resolve(recon_prefix)
        analysis=resolve(analysis_prefix)
        pairs.append((title,reconstruction,analysis))
    if sum(len(v) for v in tragic_specs.values())!=33 or sum(len(v) for v in comedy_specs.values())!=18 or len(pairs)!=33:
        raise RuntimeError("Nombre de pièces du catalogue théâtral incorrect")
    body='<h1>Théâtre grec</h1><p class="portal-lead">Une bibliothèque organisée par genre, auteur et œuvre. Les résumés et les reconstitutions sont consultables séparément des analyses philosophiques. Chaque auteur dispose de sa propre numérotation de lecture ; les volumes universitaires conservent leurs numéros historiques.</p>'
    body+=museum_figures([
      ("epidaure-theatre-antique-zde.jpg","Théâtre antique d’Épidaure","Épidaure — espace de représentation du théâtre grec."),
      ("mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg","Représentations hellénistiques de masques de théâtre","Masques — iconographie antique."),
      ("antigone-libation-rinehart-1870.jpg","Représentation artistique d’Antigone","Antigone — représentation artistique du XIXe siècle."),
      ("mythos-dionysos-kylix-brygos-bnf-576.jpg","Dionysos sur une céramique grecque","Dionysos — contexte cultuel et iconographie.")
    ],"Le théâtre : lieux, masques et figures")
    body+=section("Choisir sa lecture","Trois parcours indépendants, reliés œuvre par œuvre.",cards([
      ("#pieces-conservees","01 · Pièces conservées","33 dossiers tragiques, 11 pièces d’Aristophane et 7 dossiers de Ménandre.","ŒUVRES"),
      ("#pieces-perdues","02 · Pièces perdues","Fragments, catalogues critiques et reconstitutions modernes.","FRAGMENTS"),
      ("#analyses","03 · Analyses philosophiques","Interprétations distinctes des intrigues et des textes de théâtre.","PHILOSOPHIE")
    ]))
    body+='<section class="portal-section theatre-catalog" id="pieces-conservees"><h2>01 · Pièces conservées et dossiers de lecture</h2>'
    body+='<p class="section-intro">Numéros 01, 02, 03… propres à chaque auteur. Ordre éditorial des pièces : ni chronologie certaine ni volumes universitaires.</p>'
    body+='<h3>Tragédies</h3>'
    for author,spec in tragic_specs.items():
        body+='<div class="theatre-author"><h3>'+esc(author)+' — '+str(len(spec))+' œuvres</h3>'+numbered_works(works(author,spec),"Œuvre et dossier de lecture")+'</div>'
    body+='<p class="small-note">Prométhée enchaîné et Rhésos sont accompagnés de mentions d’attribution discutée ; Le Cyclope est un drame satyrique. Les différentes pièces de Ménandre ne sont pas toutes intégralement conservées.</p>'
    body+='<h3>Comédies</h3>'
    for author,spec in comedy_specs.items():
        body+='<div class="theatre-author"><h3>'+esc(author)+' — '+str(len(spec))+' dossiers</h3>'+numbered_works(works(author,spec),"Œuvre et dossier de lecture")+'</div>'
    body+='</section>'
    body+='<section class="portal-section theatre-catalog" id="pieces-perdues"><h2>02 · Pièces perdues, fragments et reconstitutions modernes</h2>'
    body+='<p class="section-intro">La reconstitution est une création moderne : la page distingue les témoignages transmis, les hypothèses et les scènes imaginées. Les numéros ci-dessous servent uniquement au repérage des dossiers.</p>'
    body+='<h3>Tragédies perdues — dossiers individuels disponibles</h3>'
    for author in ("Eschyle","Sophocle","Euripide"):
        selected=[e for e in lost_t if e["title"].startswith(author+" —")]
        body+='<div class="theatre-author"><h3>'+esc(author)+'</h3>'+numbered_works(selected,"Fragments et restitution")+'</div>'
    body+=cards([("/tragedies/mythos-bibliotheque-89-tragedies-perdues-edition-vii/","Répertoire général des 89 tragédies perdues","Volumes et sources, même lorsque toutes les œuvres ne disposent pas d’une page individuelle.","CATALOGUE")])
    body+='<h3>Aristophane — 33 comédies perdues et versions</h3><p class="section-intro">Une œuvre porte un numéro constant dans cette liste. Sous chaque titre, deux accès : reconstitution et analyse philosophique. Pour les attributions contestées, la mention est conservée.</p>'
    body+='<ol class="work-list linked-works">'+''.join(
      '<li><strong>'+esc(title)+'</strong><div class="work-links"><a href="'+esc(recon["url"])+'">Fragments et reconstitution</a><a href="'+esc(analysis["url"])+'">Analyse philosophique</a></div></li>'
      for title,recon,analysis in pairs
    )+'</ol>'
    body+=cards([
     ("/comedie-grecque-aristophane-menandre-etudes/aristophane-catalogue-critiques-33-comedies-perdues/","Catalogue critique des 33 œuvres et versions","Répertoire, attribution et bibliographies.","SOURCES"),
     ("/comedie-grecque-aristophane-menandre-etudes/comedies-perdues-cratinos-eupolis-philemon-fragments/","Autres auteurs comiques","Cratinos, Eupolis, Ménandre et les œuvres fragmentaires.","SOURCES")
    ])+'</section>'
    body+='<section class="portal-section theatre-catalog" id="analyses"><h2>03 · Analyses philosophiques : une bibliothèque distincte</h2>'
    body+='<p class="section-intro">L’interprétation philosophique et historique ne se substitue pas au résumé ou au témoignage antique. Les analyses de chaque comédie perdue sont accessibles à partir du même numéro ci-dessus.</p>'
    body+=cards([
      ("/philosophie/","Études philosophiques","Interprétations par thème, auteur et œuvre.","INTERPRÉTATIONS"),
      ("/theatre-grec-conserve-etudes-philosophiques/","Analyse des pièces conservées","Tragique, politique, justice, langage et religion.","INTERPRÉTATIONS"),
      ("/comedie-grecque-aristophane-menandre-etudes/aristophane-bibliotheque-etudes-philosophiques/","33 études d’Aristophane","Une analyse associée à chaque œuvre du catalogue.","INTERPRÉTATIONS")
    ])+'</section>'
    body+=section("Archives intégrales","Aucun ancien dossier n’est supprimé ; les archives restent accessibles depuis l’index général.",
      details(tragedies,f"Tous les {len(tragedies)} dossiers de tragédie")+details(comedies,f"Tous les {len(comedies)} dossiers de comédie"))
    write("theatre",shell("Théâtre grec — catalogue par auteur et par œuvre",body))

def create_philosophy(entries):
    studies=[e for e in entries if
        re.search(r"philosoph|nietzsche|hegel|socrate|platon|aristote|epicure|feuerbach|marx|auguste-comte|dumezil|vernant|detienne|historiograph|exegese", (e["title"]+" "+e["url"]).casefold())]
    body='<h1>Études philosophiques</h1><p class="portal-lead">Une porte d’entrée distincte pour la lecture philosophique des récits, de la religion et du théâtre. Les sources anciennes, les interprétations modernes et les reconstructions sont distinguées.</p>'
    body+=section("Philosophie des mythes et du tragique","La mythologie comme problème de connaissance, de pouvoir et de sens.",cards([
     ("/philosophie-et-interpretations/","Philosophie et interprétations","Concepts, écoles et lecture des mythes."),
     ("/tragedies/philosophie-theatre-grec-tragique-comique-hegel-nietzsche/","Hegel et Nietzsche","Tragique, justice, liberté et connaissance."),
     ("/papyrus-derveni-orphee-cosmogonie-philosophie-presocratique/","Papyrus de Derveni","Cosmogonie, interprétation et pensée grecque."),
     ("/historiographie-v6/","Historiographie","Vernant, Détienne, Loraux et les études du mythe."),
     ("/theatre-grec-conserve-etudes-philosophiques/","Philosophie des pièces","Études philosophiques des œuvres conservées."),
     ("/chapitres/comparatif/volume-lv-feuerbach-marx/","Feuerbach et Marx","Critique de la religion et société.")
    ]))
    body+=section("Dossiers philosophiques indexés","Une sélection par titres, auteurs et thèmes explicitement philosophiques.",details(studies,f"Afficher les {len(studies)} études et parcours apparentés"))
    write("philosophie",shell("Études philosophiques et mythologie comparée",body))

def create_civilisations(entries, groups):
    body='<h1>Civilisations du monde</h1><p class="portal-lead">Explorer les contextes historiques dans lesquels prennent forme les mythes : sociétés, langues, cultes, archéologie et transmissions. Le classement par continent est un outil de navigation contemporain, pas une frontière culturelle antique.</p>'
    body+=section("Choisir un continent","Les dossiers géographiques sont classés sans effacer les circulations entre les mondes.",cards([(f"/civilisations/{k}/",name,f"{len(groups[k])} études. {description}","CONTINENT") for k,(name,description) in CONTINENTS.items()]))
    body+=section("Études transversales","Comparer les sources et les espaces.",cards([
      ("/bibliotheque-mythologies-du-monde/civilisations-histoire-encyclopedie-sommaire/","Sommaire historique","Panorama et méthode comparative."),
      ("/atlas-comparatif-mythes-cultes-pouvoirs-antiquite/","Atlas comparatif","Récits, territoires, cultes et pouvoir."),
      ("/mythologies/","Panthéons et mythes","Retrouver les récits de ces civilisations."),
      ("/grece/","Grèce et Méditerranée","Le monde grec dans son environnement.")
    ]))
    write("civilisations",shell("Civilisations du monde, par continent",body))
    for key,(name,desc) in CONTINENTS.items():
        docs=groups[key]
        text_intro=f"<h1>{esc(name)}</h1><p class='portal-lead'>{esc(desc)}. {len(docs)} études historiques disponibles. Les catégories géographiques servent à chercher, non à isoler les cultures.</p>"
        hub_cards=cards([
          ("/civilisations/","Tous les continents","Retour à la carte des civilisations."),
          ("/mythologies/","Mythes et traditions","Textes, dieux, récits et cultes."),
          ("/recherche/","Recherche transversale","Trouver un mot ou un personnage.")
        ],"portal-grid-compact")
        section_body=list_entries(docs)
        write("civilisations/"+key,shell(f"Civilisations — {name}",text_intro+section("Dossiers de ce continent",f"{len(docs)} études, classées par titre.",section_body)+section("Poursuivre l’exploration","",hub_cards)))

def renovate_catalog(total):
    path=OUT/"rubriques/index.html"
    raw=path.read_text(encoding="utf-8")
    if '<ul class="listing">' not in raw: raise RuntimeError("Catalogue original sans index alphabétique")
    top='''<h1>Bibliothèque et index intégral</h1>
<p class="portal-lead">Commencez par une grande collection ou ouvrez l'index alphabétique de tous les dossiers.</p>
<div class="portal-grid portal-grid-compact">'''+''.join(
 card(url,title,desc,"PARCOURS")
 for url,title,desc in [
  ("/mythologies/","Mythologies","Panthéons et récits du monde"),
  ("/dieux-et-deesses/","Dieux et déesses","Panthéons et divinités"),
  ("/heros-et-heroines/","Héros et héroïnes","Personnages et cycles épiques"),
  ("/recits-mythologiques/","Grands récits","Cosmogonies, voyages et épopées"),
  ("/grece/","Grèce antique","Dieux, héros, cultes et épopées"),
  ("/theatre/","Théâtre","Tragédies, comédies et fragments"),
  ("/origines-du-sacre/","Origines du sacré","Rites, images, textes et traditions religieuses"),
  ("/philosophie/","Philosophie","Études critiques et interprétations"),
  ("/civilisations/","Civilisations","Cinq continents et leurs traditions"),
 ])+'''</div><h2>Index alphabétique intégral</h2>
<p class="section-intro">'''+str(total)+''' dossiers classés par titre. L'index est conservé sans suppressions.</p>'''
    raw=raw.replace('<h1>Tous les dossiers</h1><p>'+str(total)+' dossiers publics indexés.</p>',top,1)
    raw=raw.replace('<ul class="listing">','<details class="library-details full-index"><summary>Déplier les '+str(total)+' entrées alphabétiques <span aria-hidden="true">＋</span></summary><ul class="listing">',1)
    raw=raw.replace('</ul></article>','</ul></details></article>',1)
    path.write_text(raw,encoding="utf-8")

def renovate_search():
    path=OUT/"recherche/index.html"
    body=path.read_text(encoding="utf-8")
    a=body.index('<article class="content">')
    b=body.index('</article>',a)+len('</article>')
    replacement='''<article class="content"><div class="eyebrow">INDEX · RECHERCHE</div>
<h1>Rechercher dans MYTHOS</h1><p class="portal-lead">Un moteur unique pour les mythologies, les œuvres dramatiques, les analyses philosophiques et les civilisations du monde.</p>
<input class="search" data-search placeholder="Ex. Chiron, Osiris, Aristophane, Chine, Nietzsche…" aria-label="Rechercher dans l'encyclopédie">
<div class="results" data-results></div><h2>Parcourir plutôt que rechercher</h2>'''+cards([
  ("/mythologies/","Mythologies","Les dieux et les récits du monde."),
  ("/dieux-et-deesses/","Dieux et déesses","Panthéons et monographies."),
  ("/heros-et-heroines/","Héros et héroïnes","Personnages des épopées."),
  ("/recits-mythologiques/","Grands récits","Cosmogonies et cycles narratifs."),
  ("/grece/","Grèce","Dieux, héros et sanctuaires grecs."),
  ("/theatre/","Théâtre","Œuvres et analyses."),
  ("/origines-du-sacre/","Origines du sacré","Sources et histoire comparée des religions."),
  ("/philosophie/","Philosophie","Les grands problèmes et les penseurs."),
  ("/civilisations/","Civilisations","Les cultures par continent.")
 ],"portal-grid-compact")+'</article>'
    body=body[:a]+replacement+body[b:]
    body=re.sub(r'<aside class="sidebar">[\s\S]*?</aside>','',body,count=1)
    path.write_text(body,encoding="utf-8")

def apply_navigation():
    changed=0
    for path in OUT.rglob("index.html"):
        raw=path.read_text(encoding="utf-8")
        result,n=re.subn(r'<nav(?:\s[^>]*)?>[\s\S]*?</nav>',NAV,raw,count=1,flags=re.IGNORECASE)
        if n!=1:
            raise RuntimeError("Aucun menu de navigation dans "+str(path))
        result=result.replace("MYTHOS — Encyclopédie universitaire comparative","MYTHOS — Encyclopédie des mythologies du monde")
        # SUPPRIMER « EXPLORER MYTHOS » À DROITE SUR TOUTES LES PAGES, Y COMPRIS ARCHIVES.
        result=re.sub(r'<aside class="sidebar">[\s\S]*?</aside>', "", result, flags=re.IGNORECASE)
        if result!=raw:
            path.write_text(result,encoding="utf-8")
            changed+=1
    return changed

def build_portals():
    entries=json.loads((OUT/"search.json").read_text(encoding="utf-8"))
    groups=get_civilisations(entries)
    if sum(len(x) for x in groups.values())<80:
        raise RuntimeError("Nombre de dossiers sur les civilisations anormalement faible")
    create_home(entries,groups)
    create_greece(entries)
    create_mythologies(entries)
    create_figures_and_stories(entries)
    create_theatre(entries)
    create_origins(entries)
    create_philosophy(entries)
    create_civilisations(entries,groups)
    print("MYTHOS NAVIGATION :",sum(len(v) for v in groups.values()),"dossiers de civilisation répartis en",len(groups),"continents", {k:len(v) for k,v in groups.items()},flush=True)

def finalize_navigation(index_count):
    renovate_catalog(index_count)
    renovate_search()
    total=apply_navigation()
    print("MYTHOS NAVIGATION :",total,"pages avec menu commun, index thématique créé",flush=True)
