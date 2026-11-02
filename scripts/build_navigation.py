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
      ("/grande-encyclopedie/","Grande encyclopédie","Volumes universitaires, études et chapitres classés.","COLLECTION AUTONOME"),
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
    # Index documentaire transversal : toutes les entrées grecques déjà publiées,
    # sans copier ni modifier leurs manuscrits et sans doublonner les liens.
    greek_groups=[
      ("Dieux, héros et mythes",("/dieu-","/heros-","/dieux-et-deesses/","/heros-et-heroines/","/recits-mythologiques/","/mythologies/grece")),
      ("Épopées et auteurs",("/iliade/","/odyssee/","/livre-hesiode/","/chapitres/iliade/","/chapitres/odyssee/","/chapitres/hesiode/","/chapitres/homere/","/chapitres/theogonie/")),
      ("Tragédies et comédies",("/tragedies/","/chapitres/tragedies/","/chapitres/comedies/","/comedie-grecque-aristophane-menandre-etudes/","/theatre-grec-conserve-etudes-philosophiques/")),
      ("Histoire, sanctuaires et civilisation",("/grece/","/grece-antique/","/delphes","/atlas-mythologique/","/civilisations/grece")),
    ]
    # Certains dossiers grecs sont classés dans des collections transversales.
    greek_terms=("grec","athen","spart","delphes","eleus","olympie","mycene","corinthe","epidaure","pnyx","agora","socrate","platon","aristote","zeus","apollon","athena","artemis","dionysos","demeter","persephone","heracles","achille","ulysse","odysse","iliade","hesiode","homere","theogon","aristophane","eschyle","sophocle","euripide","menandre","promethee","troie","mythologie-hellen")
    assigned=set()
    collections=[]
    for group_name,prefixes in greek_groups:
        selected=[]
        for e in entries:
            url=e["url"]
            if url in assigned or url=="/grece/" or not url.startswith("/"):
                continue
            if any(url.startswith(p) for p in prefixes):
                selected.append(e)
                assigned.add(url)
        collections.append((group_name,selected))
    additional=[]
    for e in entries:
        url=e["url"]
        if url in assigned or url=="/grece/" or not url.startswith("/"):
            continue
        key=(url+" "+e.get("title","")).casefold()
        if any(term in key for term in greek_terms):
            additional.append(e)
            assigned.add(url)
    collections.append(("Autres études grecques et dossiers comparatifs",additional))
    total=sum(len(items) for _,items in collections)
    if total<60:
        raise RuntimeError("Corpus grec : index anormalement restreint ("+str(total)+")")
    body+='<section class="portal-section greek-complete-index" id="corpus-grec-complet"><h2>Catalogue des contenus grecs publiés</h2><p class="section-intro">'+str(total)+' pages et dossiers repérés dans la bibliothèque MYTHOS, classés par domaine. Les études restent à leur emplacement d’origine, sans suppression ni duplication des textes.</p><nav class="greek-index-toc" aria-label="Collections du corpus grec">'+''.join('<a href="#grec-corpus-'+str(i)+'">'+esc(name)+' ('+str(len(items))+')</a>' for i,(name,items) in enumerate(collections,1) if items)+'</nav>'
    for i,(name,items) in enumerate(collections,1):
        if not items:
            continue
        ordered=sorted(items,key=lambda e:(e.get("title") or e["url"]).casefold())
        body+='<section class="greek-index-group" id="grec-corpus-'+str(i)+'"><h3>'+esc(name)+' — '+str(len(items))+' dossiers</h3><ol class="greek-index-list">'+''.join('<li><a href="'+esc(e["url"])+'">'+esc(e.get("title") or e["url"])+'</a></li>' for e in ordered)+'</ol></section>'
    body+='</section>'
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
    """Catalogue exhaustif des 48 chapitres présents (443 à 490), sans doubler les textes."""
    corpus=[e for e in entries if e["url"].startswith("/chapitres/origines-du-sacre/")]
    by_number={}
    omnibus="/chapitres/origines-du-sacre/tome-xxxviii-chapitres-443-450/"
    for e in corpus:
        m=re.match(r"/chapitres/origines-du-sacre/(\d+)-",e["url"])
        if m:
            number=int(m.group(1))
            if number in by_number:
                raise RuntimeError("Origines du sacré : doublon du chapitre "+str(number))
            by_number[number]=e
    expected=set(range(451,491))
    if not expected.issubset(by_number):
        raise RuntimeError("Origines du sacré : chapitres historiques manquants : "+str(sorted(expected-set(by_number))))
    # Les chapitres ultérieurs (491 et suivants) sont légitimes : ne pas bloquer la publication.
    if not any(e["url"]==omnibus for e in corpus):
        raise RuntimeError("Origines du sacré : tome 443–450 absent")
    titles={
      443:"Éleusis : Déméter, Perséphone et les Mystères",
      444:"Dionysos, Orphée et les savoirs de l’au-delà",
      445:"Mithras romain : grades, repas et cosmos",
      446:"Égypte et Mésopotamie : savoirs sacerdotaux",
      447:"Inde et Iran : initiation, ordination et récitation",
      448:"Chine, Afrique et Amériques : rites de passage",
      449:"Van Gennep et Turner : théorie des rites",
      450:"Philosophie du secret et de la transmission",
      451:"Platon : inspiration et mania divine",
      452:"Delphes : Pythie et parole oraculaire",
      453:"Dionysos, ménades et tragédie",
      454:"Mari : prophétie en Mésopotamie",
      455:"Égypte : oracles et médiation divine",
      456:"Inde et Chine : possession et médiumnité",
      457:"Afrique et Amériques : corps et puissances divines",
      458:"Anthropologie et neurosciences des expériences religieuses",
      459:"Grèce : mousikē et musique rituelle",
      460:"Grèce : chœurs et choréia",
      461:"Mésopotamie : lamentations et langue emesal",
      462:"Égypte : sistre et culte d’Hathor",
      463:"Iran et Inde : chant liturgique",
      464:"Chine : rites et musique",
      465:"Afrique et Amériques : rythmes et cérémonies",
      466:"Philosophie de la musique sacrée",
      467:"Grèce : calendriers et temps sacré",
      468:"Mésopotamie : fête de l’Akītu",
      469:"Égypte : calendrier et cycle sothiaque",
      470:"Iran : zoroastrisme et temps",
      471:"Inde : yuga et calendriers",
      472:"Chine : calendrier et mandat",
      473:"Afrique et Amériques : calendriers rituels",
      474:"Philosophie du temps sacré",
      475:"Grèce : téménos et frontières du sacré",
      476:"Grèce : sanctuaires et territoires",
      477:"Mésopotamie : temples et ziggurats",
      478:"Égypte : temple et paysage cosmique",
      479:"Iran et Inde : feu, mandala et temple",
      480:"Chine : autels, montagnes et espaces sacrés",
      481:"Afrique et Amériques : paysages sacrés",
      482:"Philosophie de la géographie sacrée",
      483:"Grèce : serment et Horkos",
      484:"Grèce : malédictions et katadesmoi",
      485:"Traités hittites et assyriens : obligations sacrées",
      486:"Égypte : parole rituelle et exécration",
      487:"Iran et Inde : Mithra, ṛta et satya",
      488:"Chine : serments et alliances",
      489:"Afrique et Amériques : parole rituelle",
      490:"Philosophie du serment et performativité"
    }
    def row(n):
        url=(omnibus+"#chapitre-"+str(n)) if n<=450 else by_number[n]["url"]
        code="ODS-"+str(n-442).zfill(3)
        return '<li data-public-id="'+esc(code)+'"><span class="origin-id">'+esc(code)+'</span><a href="'+esc(url)+'">'+esc(titles[n])+'</a></li>'
    sections=[
      ("I · Initiation, secret et transmission",range(443,451),"Tome XXXVIII — huit chapitres réunis dans un document intégral."),
      ("II · Oracles, inspiration et médiations",range(451,459),"Tome XXXIX — huit dossiers individuels."),
      ("III · Musique, chants et rythmes sacrés",range(459,467),"Huit dossiers individuels."),
      ("IV · Calendriers et temps sacré",range(467,475),"Huit dossiers individuels."),
      ("V · Sanctuaires et géographies sacrées",range(475,483),"Huit dossiers individuels."),
      ("VI · Serments, malédictions et puissance de la parole",range(483,491),"Huit dossiers individuels.")
    ]
    body='<h1>Origines du sacré</h1><p class="portal-lead">Quarante-huit chapitres accessibles dans leur intégralité : des Mystères grecs aux rites, musiques, calendriers et sanctuaires des sociétés anciennes. La collection possède ses propres numéros ODS-001 à ODS-048 ; les anciennes références techniques sont conservées dans les adresses des sources, mais ne figurent plus dans le sommaire public.</p>'
    body+=museum_figures([
      ("mythos-ounas-chambre-funeraire-vincent-brown.jpg","Textes funéraires dans la pyramide d’Ounas","Égypte — écriture et pratiques funéraires."),
      ("mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg","Fragments du papyrus de Derveni","Grèce — interprétation d’une tradition poétique religieuse."),
      ("mythos-enheduanna-disque-penn-museum-mefman00.jpg","Disque d’Enheduanna","Mésopotamie — poésie et fonction cultuelle."),
      ("mythos-yazilikaya-chambre-b-douze-dieux-ywpark.jpg","Reliefs du sanctuaire de Yazılıkaya","Anatolie — espace et iconographie sacrés.")
    ],"Sources et objets de l’histoire religieuse")
    # Le parcours en six étapes est retiré du portail public.
    # Les 48 dossiers historiques restent accessibles dans une liste documentaire unique.
    body+='<section class="portal-section" id="dossiers-historiques"><h2>Dossiers thématiques historiques</h2><p class="section-intro">48 dossiers conservés, sans parcours imposé ni suppression de contenu.</p><ol class="chapter-list origins-index">'+''.join(row(n) for n in range(443,491))+'</ol></section>'
    # Manuscrit historique récupéré depuis la bibliothèque MYTHOS, conservé intégralement en neuf parties.
    integral_parts=[e for e in corpus if re.fullmatch(r"/chapitres/origines-du-sacre/manuscrit-integral-partie-0[1-9]/",e["url"])]
    if len(integral_parts)!=9:
        raise RuntimeError("Manuscrit historique des Origines du sacré incomplet : "+str(len(integral_parts))+"/9")
    integral_parts.sort(key=lambda e:e["url"])
    body+='<section class="portal-section" id="manuscrit-integral"><h2>Manuscrit historique intégral — tomes I à XX</h2><p class="section-intro">Texte original conservé en neuf parties continues, sans abrègement. Édition de recherche, non évaluée par les pairs. Le manuscrit est distinct des chapitres 443 à 490 publiés ci-dessous.</p><ol class="chapter-list">'+''.join('<li><a href="'+esc(e["url"])+'">'+esc("Lire le manuscrit — partie "+str(i)+" sur 9")+'</a></li>' for i,e in enumerate(integral_parts,1))+'</ol></section>'
    # Publication complète des 27 tomes : les dossiers historiques restent accessibles.
    # Bibliothèque intégrale : 27 tomes de la sauvegarde, sans supprimer les 48 dossiers historiques.
    roman_volumes = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv","xxvi","xxvii"]
    roman_labels = [x.upper() for x in roman_volumes]
    special_slugs = {"i":"tome-i-hohle-fels","ii":"tome-ii-prehistoire-du-sacre","iii":"tome-iii-corps-caverne-mondes-invisibles"}
    # Intitulés fidèles aux titres des manuscrits, illustrations issues des médias MYTHOS existants.
    volume_titles = ["Hohle Fels et les premières images","Préhistoire du sacré","Le corps, la caverne et les mondes invisibles","Des maisons des ancêtres aux premiers dieux écrits","La naissance du cosmos et la souveraineté des dieux","Le Déluge, la mort et la renaissance","Les mystères de l’immortalité","La naissance du mal et de la justice divine","Le destin, les oracles et la liberté humaine","Le temps sacré et les cycles cosmiques","Le sacrifice, le sang et les dieux","Prêtres, sanctuaires et pouvoir religieux","La loi sacrée et la conscience morale","Violence politique, tyrannie et pouvoir sacré","Révolte, impiété, athéisme et critique de la religion","Nature, hasard et naissance des sciences","L’âme, la conscience et l’identité personnelle","Rêves, visions et prophéties","Magie, théurgie et puissances invisibles","La naissance de la sagesse","Justice universelle et cosmopolitisme","La naissance du beau","Monstres, dragons, chaos et altérité","Métamorphoses et transformations du vivant","Amour, désir et puissance divine","Familles divines, filiation et pouvoir","La mort, le deuil et la mémoire des ancêtres"]
    volume_images = ["mythos-e28094-ceramique-grecque-a-figures-rouges.png","mythos-mycene-porte-lionnes-zde-2020.jpg","mythos-ounas-chambre-funeraire-vincent-brown.jpg","mythos-enheduanna-disque-penn-museum-mefman00.jpg","mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg","gilgamesh-tablette-deluge-british-museum-babelstone.jpg","eleusis-grand-relief-demeter-trip-toleme-persephone-zde.jpg","mythos-papyrus-ani-pesee-coeur-british-museum.jpg","delphes-temple-apollon-bernard-gagnon.jpg","mythos-gathas-bodleian-j2-fol175-yasna28.jpg","mythos-demeter-porcelet-terre-cuite-athenes-cma-1926-521.jpg","mythos-samothrace-sanctuaire-grands-dieux-ggia-2002.jpg","mythos-behistun-inscription-darius-mahdimanavimvi-2018.jpg","mythos-persepolis-apadana-delegations-pentocelo-2006.jpg","jacques-louis-david-mort-de-socrate-1787.jpg","raphael-ecole-athenes-1511.jpg","mythos-papyrus-ani-pesee-coeur-british-museum.jpg","mythos-dodone-theatre-koen-2006.jpg","mythos-hecate-triple-graces-met-1987-11-2.jpg","mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg","mythos-relief-hero-banquet-attique-met-57-42.jpg","mythos-samothrace-nike-louvre-dada-photo.jpg","moreau-oedipe-sphinx-1864-met.jpg","mythos-medee-fuite-char-serpents-hydrie-policoro-35296.jpg","mythos-aphrodite-cygne-kylix-british-museum.jpg","amarna-akhenaton-nefertiti-filles-relief.jpg","mythos-ounas-chambre-funeraire-vincent-brown.jpg"]
    integral_volumes = []
    for index, (roman, label) in enumerate(zip(roman_volumes, roman_labels)):
        slug = special_slugs.get(roman, "tome-"+roman)
        url = "/chapitres/origines-du-sacre/archives-integrales/"+slug+"/"
        page = OUT / url.lstrip("/") / "index.html"
        if not page.is_file():
            raise RuntimeError("Origines du sacré : tome manquant : "+label)
        image_url = "/media/2026/10/"+volume_images[index]
        if not (OUT / image_url.lstrip("/")).is_file():
            raise RuntimeError("Origines du sacré : illustration manquante : "+image_url)
        integral_volumes.append((url, "Tome "+label, volume_titles[index], image_url))
    hero = '<section class="origins-hero"><div class="origins-hero-inner"><h1>ORIGINES DU SACRÉ</h1><span class="origins-hero-rule" aria-hidden="true">◇</span><p class="origins-hero-subtitle">Bibliothèque intégrale de recherche</p><p>Des premiers rituels aux grandes religions, une exploration approfondie des origines du sacré à travers les civilisations, les mythes et les cultures.</p></div></section>'
    volumes_html = '<section class="origins-volumes"><h2>Les 27 tomes — édition intégrale</h2><p>Vingt-sept volumes pour explorer les origines du sacré, de la préhistoire aux grandes civilisations, à travers les mythes, les rites, les dieux et les sociétés.</p><div class="origins-volume-grid">'+''.join('<a class="origins-volume" href="'+esc(url)+'"><img class="origins-volume-image" src="'+esc(image_url)+'" alt="Illustration thématique du '+esc(label)+'" loading="lazy"><span class="origins-volume-copy"><strong>'+esc(label)+'</strong><span class="origins-volume-title">'+esc(title)+'</span><span class="origins-volume-read" aria-label="Lire '+esc(label)+'">→</span></span></a>' for url,label,title,image_url in integral_volumes)+'</div></section>'
    dossier_images = [("mythos-demeter-porcelet-terre-cuite-athenes-cma-1926-521.jpg","Rites et sacrifices"),("mythos-bronze-artemision-zeus-ou-poseidon.jpg","Les grandes divinités"),("delphes-temple-apollon-bernard-gagnon.jpg","Lieux sacrés"),("mythos-dionysos-kylix-brygos-bnf-576.jpg","Sociétés et cultures"),("mythos-ounas-chambre-funeraire-vincent-brown.jpg","Pratiques funéraires")]
    dossier_preview = '<section class="origins-dossier-preview"><div class="origins-dossier-summary"><h2>Dossiers thématiques historiques</h2><p>48 dossiers conservés</p><p>Une sélection de dossiers pour approfondir les grandes thématiques : rites, divinités, sociétés, lieux sacrés, pratiques funéraires, et bien plus encore.</p><a class="origins-dossier-button" href="#dossiers-historiques">Accéder aux 48 dossiers →</a></div><div class="origins-dossier-gallery">'+''.join('<figure><img src="/media/2026/10/'+esc(img)+'" alt="'+esc(caption)+'" loading="lazy"><figcaption>'+esc(caption)+'</figcaption></figure>' for img,caption in dossier_images)+'</div></section>'
    body = hero+volumes_html+dossier_preview+'<div class="origins-archives">'+body+'</div>'
    write("origines-du-sacre",shell("Origines du sacré — 27 tomes intégraux et dossiers thématiques MYTHOS",body).replace("<body>", '<body class="origins-landing">'))

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
      ("#analyses","03 · Analyses philosophiques","Interprétations distinctes des intrigues et des textes de théâtre.","PHILOSOPHIE"),
      ("#commentaires-vers","04 · Commentaires par vers","Lectures suivies des pièces, avec passages et vers numérotés.","COMMENTAIRE")
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
    body+='<section class="portal-section theatre-catalog" id="commentaires-vers"><h2>04 · Commentaires suivis et analyses par vers</h2>'
    body+='<p class="section-intro">Les commentaires déjà rédigés sont consultables ici : passages numérotés, scènes et ensembles de vers. Une étude par plages de vers n’est pas une édition philologique mot à mot. Les analyses sont conservées dans leurs dossiers d’origine, sans mélange avec les reconstitutions.</p>'
    # Répertorier toutes les études des œuvres identifiées, sans créer de doublons.
    # Contrôle automatisé de la présence de références de vers : syntaxe seulement,
    # sans prétendre vérifier une édition grecque critique.
    all_specs=list(tragic_specs.items())+list(comedy_specs.items())
    used=set()
    catalog_rows=[]
    audit_missing=[]
    audit_ranges=[]
    for author,spec in all_specs:
        author_rows=[]
        for local_num,(title,prefix) in enumerate(spec,1):
            entry=resolve(prefix)
            if entry["url"] in used:
                raise RuntimeError("Doublon dans les commentaires : "+entry["url"])
            used.add(entry["url"])
            file=OUT/entry["url"].lstrip("/")/"index.html"
            if not file.is_file():
                raise RuntimeError("Commentaire absent du site généré : "+str(file))
            source=BeautifulSoup(file.read_text(encoding="utf-8"),"html.parser")
            main=source.find("article") or source
            text_content=main.get_text(" ",strip=True)
            references=[]
            for m in re.finditer(r"\bvers\s+(\d{1,4})(?:\s*[–—-]\s*(\d{1,4}))?",text_content,re.I):
                first=int(m.group(1))
                last=int(m.group(2)) if m.group(2) else first
                if first<=last:
                    references.append((first,last))
            unique_refs=sorted(set(references))
            explicit=len(unique_refs)
            has_commentary=bool(re.search(r"commentaire (?:suivi|intégral|des |de |philologique)|étude suivie des scènes|grand commentaire|lecture suivie",text_content,re.I))
            if explicit:
                status=str(explicit)+" repère(s) de vers dans le texte — à confronter à l’édition critique"
                audit_ranges.append((author,title,explicit))
            elif has_commentary:
                status="Commentaire de scènes : plages de vers non repérées automatiquement"
                audit_missing.append((author,title))
            else:
                status="Étude critique : repérage vers par vers à compléter"
                audit_missing.append((author,title))
            code=({"Eschyle":"ES-TR","Sophocle":"SO-TR","Euripide":"EU-TR","Aristophane":"AR-CO","Ménandre":"ME-CO"}[author]
                  +"-"+str(local_num).zfill(3))
            author_rows.append('<li><a href="'+esc(entry["url"])+'">'+esc(code+" · "+title)+'</a><small>'+esc(status)+'</small></li>')
        catalog_rows.append('<div class="theatre-author"><h3>'+esc(author)+' — '+str(len(author_rows))+' dossiers</h3><ol class="work-list linked-works">'+''.join(author_rows)+'</ol></div>')
    if len(used)!=51:
        raise RuntimeError("Le catalogue de commentaires doit couvrir exactement 51 dossiers distincts")
    body+='<p class="small-note">Inventaire intégral : '+str(len(used))+' dossiers de pièces conservées ou partiellement conservées, dont '+str(len(audit_ranges))+' avec au moins un repère de vers détecté et '+str(len(audit_missing))+' sans repère exploitable automatiquement. La présence d’un repère ne certifie pas son exactitude philologique ; les commentaires par scènes ne sont pas présentés comme du mot à mot.</p>'
    body+=''.join(catalog_rows)
    body+='<details class="library-details"><summary>Contrôle éditorial : lacunes de référencement ('+str(len(audit_missing))+') <span aria-hidden="true">＋</span></summary><p>Ces études existent, mais les références de vers demandent une vérification ou une indexation supplémentaire :</p><ul class="portal-list">'+''.join('<li>'+esc(author+" — "+title)+'</li>' for author,title in audit_missing)+'</ul></details>'
    body+='<p class="small-note">Audit effectué sur les 51 pages HTML du dépôt pendant la génération. Les variantes textuelles, les interpolations, les numérotations divergentes et les traductions doivent être vérifiées sur des éditions critiques. Les 33 reconstitutions et analyses des comédies perdues restent accessibles séparément dans la rubrique 02.</p></section>'
    body+=section("Archives intégrales","Aucun ancien dossier n’est supprimé ; les archives restent accessibles depuis l’index général.",
      details(tragedies,f"Tous les {len(tragedies)} dossiers de tragédie")+details(comedies,f"Tous les {len(comedies)} dossiers de comédie"))
    write("theatre",shell("Théâtre grec — catalogue par auteur et par œuvre",body))

def classify_encyclopedia(entry):
    """Une seule collection primaire par URL ; catégories éditoriales, non mots-clés flous."""
    url=entry["url"]
    if url.startswith("/chapitres/origines-du-sacre/"): return "ODS"
    if url.startswith(("/tragedies/","/comedie-grecque-aristophane-menandre-etudes/","/chapitres/tragedies/","/chapitres/comedies/")): return "TH"
    if url.startswith(("/philosophie-et-interpretations/","/chapitres/comparatif/","/historiographie-")): return "PH"
    if url.startswith(("/chapitres/encyclopedie/","/livre-dieux/","/dieux-et-deesses/","/heros-et-heroines/","/recits-mythologiques/")): return "GE"
    if url.startswith(("/bibliotheque-mythologies-du-monde/","/bibliotheque-egypte-ancienne/","/bibliotheque-mesopotamie/","/bibliotheque-perse-iran-ancien/")): return "CM"
    return "REF"

def create_encyclopedia(entries):
    """Registre public stable par collection, sans toucher aux archives ni réécrire les études."""
    canonical={}
    for e in entries:
        url=e["url"]
        if url in canonical:
            raise RuntimeError("MYTHOS : URL dupliquée dans l'index : "+url)
        canonical[url]=e
    collections=[
      ("GE","Grande encyclopédie","Dieux, héros, récits et chapitres universitaires"),
      ("ODS","Origines du sacré","Préhistoire, cultes, rites et anthropologie religieuse"),
      ("TH","Théâtre grec","Pièces conservées, fragments, reconstitutions et commentaires"),
      ("PH","Philosophie et interprétations","Études générales indépendantes des pièces"),
      ("CM","Civilisations et mythologies comparées","Bibliothèques et traditions du monde"),
      ("REF","Autres ressources","Documents transversaux, index et ressources complémentaires")
    ]
    groups={code:[] for code,_,_ in collections}
    for e in canonical.values():
        groups[classify_encyclopedia(e)].append(e)
    # Les cotes de registre sont recalculées lors des ajouts ; les URL restent pérennes.
    # L'identifiant canonique est l'URL : les numéros sont des cotes de catalogue,
    # jamais des remplacements des références scientifiques d'une édition.
    assigned={}
    for code,_,_ in collections:
        for i,e in enumerate(sorted(groups[code],key=lambda x:x["url"]),1):
            assigned[e["url"]]="RG-"+code+"-"+str(i).zfill(4)
    if len(assigned)!=len(canonical) or len(set(assigned.values()))!=len(assigned):
        raise RuntimeError("MYTHOS : registre incomplet ou cotes en double")
    body='<h1>Grande encyclopédie MYTHOS</h1><p class="portal-lead">Catalogue général de tous les dossiers publics, organisé en collections distinctes. Chaque entrée a une cote de registre RG distincte des numéros éditoriaux ODS et AR-CO, sans effacement des textes, des sources ni des anciennes références scientifiques. Les manuscrits non encore importés ne sont pas présentés comme publiés.</p>'
    body+='<nav class="origins-toc" aria-label="Collections encyclopédiques"><h2>Collections</h2><ol>'+''.join(
        '<li><a href="#collection-'+code.lower()+'">'+esc(code+" · "+name)+" ("+str(len(groups[code]))+')</a></li>'
        for code,name,_ in collections)+'</ol></nav>'
    for code,name,description in collections:
        rows=sorted(groups[code],key=lambda e:e["url"])
        body+='<section class="portal-section" id="collection-'+code.lower()+'"><h2>'+esc(name)+'</h2><p class="section-intro">'+esc(description)+'</p>'
        body+='<details class="library-details"><summary>Consulter les '+str(len(rows))+' entrées <span aria-hidden="true">＋</span></summary><ol class="chapter-list origins-index">'+''.join(
          '<li data-public-id="'+esc(assigned[e["url"]])+'"><span class="origin-id">'+esc(assigned[e["url"]])+'</span><a href="'+esc(e["url"])+'">'+esc(e["title"])+'</a></li>'
          for e in rows)+'</ol></details></section>'
    body+=section("Règles de classement","Une URL ne figure qu'une fois dans le registre. Les cotes des collections sont indépendantes ; la numérotation scientifique historique est conservée dans les documents sources.",
      '<p>Le registre présente les pages effectivement indexées. La grande édition manuscrite des Origines du sacré, distincte des chapitres déjà publiés, sera intégrée seulement après comparaison de ses versions pour éviter les doublons.</p>')
    write("grande-encyclopedie",shell("Grande encyclopédie — catalogue général MYTHOS",body))

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
      ("#analyses","03 · Analyses philosophiques","Interprétations distinctes des intrigues et des textes de théâtre.","PHILOSOPHIE"),
      ("#commentaires-vers","04 · Commentaires par vers","Lectures suivies des pièces, avec passages et vers numérotés.","COMMENTAIRE")
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
    body+='<section class="portal-section theatre-catalog" id="commentaires-vers"><h2>04 · Commentaires suivis et analyses par vers</h2>'
    body+='<p class="section-intro">Les commentaires déjà rédigés sont consultables ici : passages numérotés, scènes et ensembles de vers. Une étude par plages de vers n’est pas une édition philologique mot à mot. Les analyses sont conservées dans leurs dossiers d’origine, sans mélange avec les reconstitutions.</p>'
    # Répertorier toutes les études des œuvres identifiées, sans créer de doublons.
    # Contrôle automatisé de la présence de références de vers : syntaxe seulement,
    # sans prétendre vérifier une édition grecque critique.
    all_specs=list(tragic_specs.items())+list(comedy_specs.items())
    used=set()
    catalog_rows=[]
    audit_missing=[]
    audit_ranges=[]
    for author,spec in all_specs:
        author_rows=[]
        for local_num,(title,prefix) in enumerate(spec,1):
            entry=resolve(prefix)
            if entry["url"] in used:
                raise RuntimeError("Doublon dans les commentaires : "+entry["url"])
            used.add(entry["url"])
            file=OUT/entry["url"].lstrip("/")/"index.html"
            if not file.is_file():
                raise RuntimeError("Commentaire absent du site généré : "+str(file))
            source=BeautifulSoup(file.read_text(encoding="utf-8"),"html.parser")
            main=source.find("article") or source
            text_content=main.get_text(" ",strip=True)
            references=[]
            for m in re.finditer(r"\bvers\s+(\d{1,4})(?:\s*[–—-]\s*(\d{1,4}))?",text_content,re.I):
                first=int(m.group(1))
                last=int(m.group(2)) if m.group(2) else first
                if first<=last:
                    references.append((first,last))
            unique_refs=sorted(set(references))
            explicit=len(unique_refs)
            has_commentary=bool(re.search(r"commentaire (?:suivi|intégral|des |de |philologique)|étude suivie des scènes|grand commentaire|lecture suivie",text_content,re.I))
            if explicit:
                status=str(explicit)+" repère(s) de vers dans le texte — à confronter à l’édition critique"
                audit_ranges.append((author,title,explicit))
            elif has_commentary:
                status="Commentaire de scènes : plages de vers non repérées automatiquement"
                audit_missing.append((author,title))
            else:
                status="Étude critique : repérage vers par vers à compléter"
                audit_missing.append((author,title))
            code=({"Eschyle":"ES-TR","Sophocle":"SO-TR","Euripide":"EU-TR","Aristophane":"AR-CO","Ménandre":"ME-CO"}[author]
                  +"-"+str(local_num).zfill(3))
            author_rows.append('<li><a href="'+esc(entry["url"])+'">'+esc(code+" · "+title)+'</a><small>'+esc(status)+'</small></li>')
        catalog_rows.append('<div class="theatre-author"><h3>'+esc(author)+' — '+str(len(author_rows))+' dossiers</h3><ol class="work-list linked-works">'+''.join(author_rows)+'</ol></div>')
    if len(used)!=51:
        raise RuntimeError("Le catalogue de commentaires doit couvrir exactement 51 dossiers distincts")
    body+='<p class="small-note">Inventaire intégral : '+str(len(used))+' dossiers de pièces conservées ou partiellement conservées, dont '+str(len(audit_ranges))+' avec au moins un repère de vers détecté et '+str(len(audit_missing))+' sans repère exploitable automatiquement. La présence d’un repère ne certifie pas son exactitude philologique ; les commentaires par scènes ne sont pas présentés comme du mot à mot.</p>'
    body+=''.join(catalog_rows)
    body+='<details class="library-details"><summary>Contrôle éditorial : lacunes de référencement ('+str(len(audit_missing))+') <span aria-hidden="true">＋</span></summary><p>Ces études existent, mais les références de vers demandent une vérification ou une indexation supplémentaire :</p><ul class="portal-list">'+''.join('<li>'+esc(author+" — "+title)+'</li>' for author,title in audit_missing)+'</ul></details>'
    body+='<p class="small-note">Audit effectué sur les 51 pages HTML du dépôt pendant la génération. Les variantes textuelles, les interpolations, les numérotations divergentes et les traductions doivent être vérifiées sur des éditions critiques. Les 33 reconstitutions et analyses des comédies perdues restent accessibles séparément dans la rubrique 02.</p></section>'
    body+=section("Archives intégrales","Aucun ancien dossier n’est supprimé ; les archives restent accessibles depuis l’index général.",
      details(tragedies,f"Tous les {len(tragedies)} dossiers de tragédie")+details(comedies,f"Tous les {len(comedies)} dossiers de comédie"))
    write("theatre",shell("Théâtre grec — catalogue par auteur et par œuvre",body))

def create_encyclopedia(entries):
    """Portail indépendant de la grande encyclopédie : aucun article source supprimé."""
    corpus=[e for e in entries if e["url"].startswith("/chapitres/encyclopedie/")]
    # La grande encyclopédie couvre aussi les volumes conservés hors du dossier /chapitres/.
    roots=[
      ("/bibliotheque-mythologies-du-monde/mythos-grande-encyclopedie-dieux-heros-recits/","Grande encyclopédie — sommaire historique","Accès au cycle complet de volumes, dieux, héros et récits.","SOMMAIRE"),
      ("/bibliotheque-mythologies-du-monde/","Bibliothèque des mythologies du monde","Volumes, traditions et études comparées.","BIBLIOTHÈQUE"),
      ("/bibliotheque-mythologies-du-monde/dictionnaire-dieux-monde/","Dictionnaire des dieux du monde","Entrées thématiques et noms divins.","DICTIONNAIRE")
    ]
    available={e["url"] for e in entries}
    body='<h1>Grande encyclopédie MYTHOS</h1><p class="portal-lead">La grande encyclopédie dispose de sa propre entrée, distincte des pièces de théâtre, des études philosophiques générales et des Origines du sacré. Les anciens volumes restent intacts et consultables par leur sommaire.</p>'
    body+=section("Accès aux collections","Les numéros de volumes appartiennent aux séries universitaires ; les références de navigation ne les remplacent pas.",cards([x for x in roots if x[0] in available]))
    body+=section("Chapitres individuels repérés","Chapitres déjà présents dans le dépôt, sans reproduire ni renuméroter leurs textes.",list_entries(sorted(corpus,key=lambda e:e["url"])))
    body+=section("Autres collections de MYTHOS","Des bibliothèques distinctes, sans confusion de numéros.",cards([
      ("/origines-du-sacre/","Origines du sacré","Collection ODS et parcours thématiques.","ODS"),
      ("/theatre/","Théâtre grec","Pièces, fragments et commentaires.","THÉÂTRE"),
      ("/philosophie/","Études philosophiques","Philosophie générale et comparée.","PHILOSOPHIE")
    ]))
    write("grande-encyclopedie",shell("Grande encyclopédie — MYTHOS",body))

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
    independent=[e for e in studies if not re.search(r"/(tragedies|comedie-grecque-aristophane-menandre-etudes|theatre-grec|chapitres/tragedies|chapitres/comedies)/",e["url"]) and not re.search(r"(aristophane|eschyle|sophocle|euripide|menandre).*(analyse|étude|etude)",e["title"].casefold())]
    theatre_philosophy=[e for e in studies if e not in independent]
    body+=section("Philosophie générale et comparée","Études indépendantes des pièces de théâtre : auteurs, concepts, mythes, religion et historiographie.",details(independent,f"Afficher les {len(independent)} études philosophiques générales"))
    body+=section("Philosophie appliquée aux pièces de théâtre","Collection distincte : ces analyses interprètent une œuvre dramatique et ne doivent pas être confondues avec les études générales.",cards([("/theatre/#analyses","Revenir au théâtre","Études philosophiques liées à une pièce déterminée.","THÉÂTRE")])+details(theatre_philosophy,f"Afficher les {len(theatre_philosophy)} dossiers philosophiques théâtraux"))
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
  ("/grande-encyclopedie/","Grande encyclopédie","Volumes et dossiers universitaires"),
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


# Collections iconographiques documentées : photographies, plans, peintures et
# restitutions historiques. Ne jamais qualifier une photographie de modèle 3D.
VISUAL_COLLECTIONS = {
 "grece": [
  ("mythos-epidaure-tholos-reconstitution-defrasse-lechat-1895.jpg","Tholos d’Épidaure — restitution historique de 1895","Restitution historique"),
  ("mythos-nemee-temple-zeus-ophelia2-2010.jpg","Temple de Zeus à Némée — photographie","Photographie"),
  ("mythos-bronze-artemision-zeus-ou-poseidon.jpg","Bronze de l’Artémision — Zeus ou Poséidon, attribution discutée","Statue"),
  ("mythos-samothrace-nike-louvre-dada-photo.jpg","Victoire de Samothrace — sculpture antique","Statue"),
  ("mythos-e28094-illustration-du-sanctuaire-de-delphes.png","Sanctuaire de Delphes — illustration","Illustration"),
  ("mythos-mycene-porte-lionnes-zde-2020.jpg","Porte des Lionnes à Mycènes — photographie","Site antique"),
  ("raphael-ecole-athenes-1511.jpg","Raphaël, L’École d’Athènes — peinture","Peinture"),
  ("mythos-olympie-nike-paionios-jarvis-2005.jpg","Nikè de Paionios à Olympie — sculpture","Statue")],
 "theatre": [
  ("epidaure-theatre-antique-zde.jpg","Théâtre antique d’Épidaure","Architecture"),
  ("mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg","Masques théâtraux hellénistiques","Objet antique"),
  ("antigone-libation-rinehart-1870.jpg","Antigone — représentation artistique du XIXe siècle","Peinture"),
  ("moreau-oedipe-sphinx-1864-met.jpg","Gustave Moreau, Œdipe et le Sphinx","Peinture"),
  ("mythos-dionysos-kylix-brygos-bnf-576.jpg","Dionysos sur une coupe grecque","Céramique"),
  ("oreste-apollon-cratere-eumenides-louvre-cp-710.jpg","Oreste et Apollon — cratère antique","Céramique")],
 "sacre": [
  ("mythos-epidaure-tholos-reconstitution-defrasse-lechat-1895.jpg","Épidaure — restitution historique","Restitution historique"),
  ("mythos-ounas-chambre-funeraire-vincent-brown.jpg","Chambre funéraire d’Ounas","Site antique"),
  ("mythos-papyrus-ani-pesee-coeur-british-museum.jpg","Pesée du cœur — papyrus d’Ani","Papyrus"),
  ("eleusis-grand-relief-demeter-trip-toleme-persephone-zde.jpg","Grand relief d’Éleusis","Relief"),
  ("mythos-derveni-cratere-dionysos-menade-carole-raddato.jpg","Cratère de Dervéni","Objet antique")],
 "mesopotamie": [
  ("gilgamesh-tablette-deluge-british-museum-babelstone.jpg","Tablette du Déluge de Gilgamesh","Tablette"),
  ("mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg","Tablette de l’Enūma eliš","Tablette"),
  ("mythos-e28094-gilgamesh-devant-uruk-evocation-artistique-generee-par-ia.png","Gilgamesh devant Uruk — évocation générée par IA","Évocation artistique")],
 "egypte": [
  ("amarna-akhenaton-nefertiti-filles-relief.jpg","Akhenaton, Néfertiti et leurs filles — relief","Relief"),
  ("mythos-ounas-plan-complexe-funeraire-monnier-gdk.png","Complexe funéraire d’Ounas — plan","Plan"),
  ("mythos-ounas-chambre-funeraire-vincent-brown.jpg","Chambre funéraire d’Ounas","Photographie")],
 "perse": [
  ("mythos-persepolis-apadana-delegations-pentocelo-2006.jpg","Persépolis — relief des délégations","Relief"),
  ("mythos-persepolis-plan-historique-britannica-1911.png","Persépolis — plan historique","Plan"),
  ("mythos-behistun-inscription-darius-mahdimanavimvi-2018.jpg","Behistun — inscription de Darius","Inscription")]
}

def add_visual_rails(path):
    """Illustrations latérales sur pages de lecture, sans altérer les manuscrits."""
    source=path.read_text(encoding="utf-8")
    if 'class="mythos-visual-rail"' in source or 'class="visual-rails-active"' in source:
        return source
    slug=str(path.parent).casefold()
    if slug in ("_site", "_site/recherche"):
        return source
    if any(t in slug for t in ("traged","theatre","comedie","aristophane","eschyle","sophocle","euripide","menandre")):
        collection=VISUAL_COLLECTIONS["theatre"]
    elif any(t in slug for t in ("origine","sacre","religion","culte","rituel","prehistoire")):
        collection=VISUAL_COLLECTIONS["sacre"]
    elif any(t in slug for t in ("egypte","amarna","akhenaton","pharaon")):
        collection=VISUAL_COLLECTIONS["egypte"]
    elif any(t in slug for t in ("mesopotam","sumer","babylon","gilgamesh","assyr")):
        collection=VISUAL_COLLECTIONS["mesopotamie"]
    elif any(t in slug for t in ("perse","iran","zoroastr","achemen")):
        collection=VISUAL_COLLECTIONS["perse"]
    else:
        collection=VISUAL_COLLECTIONS["grece"]
    # Rotation stable par chemin, pour varier les œuvres sans répétition uniforme.
    offset=sum(ord(c) for c in slug)%len(collection)
    chosen=[collection[(offset+i)%len(collection)] for i in range(min(4,len(collection)))]
    figures=''.join('<figure><img loading="lazy" decoding="async" src="/media/2026/10/'+esc(filename)+'" alt="'+esc(alt)+'"><figcaption><span>'+esc(kind)+'</span> — '+esc(alt)+'</figcaption></figure>' for filename,alt,kind in chosen)
    rail='<aside class="mythos-visual-rail" aria-label="Galerie iconographique"><h2>Galerie iconographique</h2>'+figures+'</aside>'
    soup=BeautifulSoup(source,"html.parser")
    main=soup.find("main")
    article=main.find("article") if main else None
    if article is None:
        return source
    article.insert_after(BeautifulSoup(rail,"html.parser"))
    main["class"]=list(dict.fromkeys(main.get("class",[])+["visual-rails-active"]))
    return str(soup)


def apply_navigation():
    changed=0
    for path in OUT.rglob("index.html"):
        raw=path.read_text(encoding="utf-8")
        result,n=re.subn(r'<nav(?:\s[^>]*)?>[\s\S]*?</nav>',NAV,raw,count=1,flags=re.IGNORECASE)
        if n!=1:
            raise RuntimeError("Aucun menu de navigation dans "+str(path))
        result=add_visual_rails(path) if result==raw else result
        result=result.replace("MYTHOS — Encyclopédie universitaire comparative","MYTHOS — Encyclopédie des mythologies du monde")
        # SUPPRIMER « EXPLORER MYTHOS » À DROITE SUR TOUTES LES PAGES, Y COMPRIS ARCHIVES.
        result=re.sub(r'<aside class="sidebar">[\s\S]*?</aside>', "", result, flags=re.IGNORECASE)
        result=add_visual_rails(path) if "mythos-visual-rail" not in result else result
        if result!=raw:
            path.write_text(result,encoding="utf-8")
            changed+=1
    return changed


def reorganize_preserved_plays_analyses(entries):
    """Créer un index ordonné des 51 œuvres sans effacer les études anciennes."""
    path=OUT/"theatre-grec-conserve-etudes-philosophiques"/"index.html"
    if not path.is_file():
        raise RuntimeError("Catalogue des pièces conservées absent")
    page=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    article=page.find("article",class_="content")
    if article is None:
        raise RuntimeError("Contenu des études conservées introuvable")
    old=article.find(id="index-analyses-conservees")
    if old:
        old.decompose()
    catalog={e["url"].rstrip("/").split("/")[-1]:e for e in entries}
    groups=[
      ("Tragédies d’Eschyle",[("Les Perses","eschyle-perses-analyse"),("Les Sept contre Thèbes","eschyle-sept-contre-thebes-analyse"),("Les Suppliantes","eschyle-suppliantes-danaides-analyse"),("Agamemnon","eschyle-agamemnon-analyse"),("Les Choéphores","eschyle-choephores-analyse"),("Les Euménides","eschyle-eumenides-analyse"),("Prométhée enchaîné — attribution discutée","eschyle-promethee-enchaine-analyse")]),
      ("Tragédies de Sophocle",[("Ajax","sophocle-ajax-analyse"),("Antigone","sophocle-antigone-lecture-critique"),("Les Trachiniennes","sophocle-trachiniennes-analyse"),("Œdipe roi","sophocle-oedipe-roi-analyse"),("Électre","sophocle-electre-analyse"),("Philoctète","sophocle-philoctete-analyse"),("Œdipe à Colone","sophocle-oedipe-a-colone-analyse")]),
      ("Tragédies et drame satyrique d’Euripide",[("Alceste","euripide-alceste-analyse"),("Médée","euripide-medee-analyse"),("Les Héraclides","euripide-heraclides-analyse"),("Hippolyte","euripide-hippolyte-analyse"),("Andromaque","euripide-andromaque-analyse"),("Hécube","euripide-hecube-analyse"),("Les Suppliantes","euripide-suppliantes-analyse"),("Héraclès","euripide-heracles-analyse"),("Ion","euripide-ion-analyse"),("Les Troyennes","euripide-troyennes-analyse"),("Électre","euripide-electre-analyse"),("Iphigénie en Tauride","euripide-iphigenie-en-tauride-analyse"),("Hélène","euripide-helene-analyse"),("Les Phéniciennes","euripide-pheniciennes-analyse"),("Oreste","euripide-oreste-analyse"),("Iphigénie à Aulis","euripide-iphigenie-a-aulis-analyse"),("Les Bacchantes","euripide-bacchantes-dionysos-tragedie"),("Rhésos — attribution discutée","euripide-rhesos-analyse"),("Le Cyclope — drame satyrique","euripide-cyclope-analyse")]),
      ("Comédies d’Aristophane",[("Les Acharniens","aristophane-acharniens-etude"),("Les Cavaliers","aristophane-cavaliers-etude"),("Les Nuées","aristophane-nuees-etude"),("Les Guêpes","aristophane-guepes-etude"),("La Paix","aristophane-paix-etude"),("Les Oiseaux","aristophane-oiseaux-etude"),("Lysistrata","aristophane-lysistrata-etude"),("Les Thesmophories","aristophane-thesmophories-etude"),("Les Grenouilles","aristophane-grenouilles-etude"),("L’Assemblée des femmes","aristophane-assemblee-des-femmes-etude"),("Ploutos","aristophane-ploutos-etude")]),
      ("Comédies de Ménandre — conservation partielle pour plusieurs pièces",[("Le Dyscolos","menandre-dyscolos-analyse"),("La Samienne","menandre-samia-analyse"),("L’Arbitrage","menandre-epitrepontes-analyse"),("La Femme tondue","menandre-perikeiromene-analyse"),("Le Bouclier","menandre-aspis-analyse"),("Le Sicyonien","menandre-sikyonios-analyse"),("L’Homme haï","menandre-misoumenos-analyse")])
    ]
    if sum(len(items) for _,items in groups)!=51:
        raise RuntimeError("Index des analyses : 51 œuvres attendues")
    blocks=['<section id="index-analyses-conservees" class="preserved-analysis-index"><h2>Explorer les analyses des pièces conservées</h2><p>51 dossiers classés par genre, auteur et œuvre. Les études critiques sont distinctes des résumés et des reconstitutions. Les textes antérieurs restent intégralement disponibles plus bas.</p><nav class="analysis-index-nav" aria-label="Auteurs et genres">'+''.join('<a href="#analyse-auteur-'+str(i)+'">'+esc(name.split(" — ")[0])+'</a>' for i,(name,_) in enumerate(groups,1))+'</nav>']
    seen=set()
    for i,(name,items) in enumerate(groups,1):
        blocks.append('<section id="analyse-auteur-'+str(i)+'" class="analysis-author-group"><h3>'+esc(name)+'</h3><ol class="analysis-work-grid">')
        for title,prefix in items:
            matches=[e for e in entries if e["url"].rstrip("/").split("/")[-1].startswith(prefix)]
            if len(matches)!=1 or matches[0]["url"] in seen:
                raise RuntimeError("Analyse absente, ambiguë ou doublonnée : "+prefix)
            seen.add(matches[0]["url"])
            blocks.append('<li><a href="'+esc(matches[0]["url"])+'">'+esc(title)+'</a></li>')
        blocks.append('</ol></section>')
    blocks.append('<p><a href="#archives-analyses-conservees">Consulter les cycles universitaires et les analyses historiques conservés ↓</a></p></section><div id="archives-analyses-conservees"></div>')
    fragment=BeautifulSoup(''.join(blocks),"html.parser")
    first_h1=article.find("h1")
    if first_h1:
        first_h1.insert_after(fragment)
    else:
        article.insert(0,fragment)
    path.write_text(str(page),encoding="utf-8")



def reorganize_aristophanes_33(entries):
    """Index canonique des 33 monographies, avec les archives originales intactes."""
    path=OUT/"comedie-grecque-aristophane-menandre-etudes"/"aristophane-bibliotheque-etudes-philosophiques"/"index.html"
    if not path.is_file():
        raise RuntimeError("Bibliothèque des 33 études d'Aristophane absente")
    page=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    article=page.find("article",class_="content")
    if article is None:
        raise RuntimeError("Article des 33 études d'Aristophane absent")
    for old in article.select("#index-aristophane-33, #archives-aristophane-33"):
        old.decompose()
    groups=[
      ("Cité, démocratie, guerre et économie",[
        ("Les Babyloniens","babyloniens-analyse-philosophique"),("Les Paysans","paysans-analyse-philosophique"),("Les Navires marchands","navires-marchands-analyse-philosophique"),("La Paix — deuxième version","paix-deuxieme-version-analyse-philosophique"),("Les Îles — attribution discutée","iles-analyse-philosophique"),("Ploutos — première version","ploutos-premiere-version-analyse-philosophique")]),
      ("Éducation, savoirs, poésie et théâtre",[
        ("Les Banqueteurs","banqueteurs-analyse-philosophique"),("Polyidos","polyidos-analyse-philosophique"),("Les Nuées — première version","nuees-premiere-version-analyse-philosophique"),("Le Proagôn","proagon-analyse-philosophique"),("Gérytadès","gerytades-analyse-philosophique"),("La Poésie — attribution discutée","poesie-analyse-philosophique"),("Aiolosicon — première version","aiolosicon-premiere-version-analyse-philosophique"),("Aiolosicon — deuxième version","aiolosicon-deuxieme-version-analyse-philosophique")]),
      ("Famille, femmes, corps et générations",[
        ("Les Danaïdes","danaides-analyse-philosophique"),("Les Lemniennes","lemniennes-analyse-philosophique"),("La Vieillesse","vieillesse-analyse-philosophique"),("Les Cigognes","cigognes-analyse-philosophique"),("Triphâlès","triphales-analyse-philosophique"),("Les Thesmophories — deuxième version","thesmophories-deuxieme-version-analyse-philosophique"),("Les Femmes occupant les tentes","femmes-occupant-tentes-analyse-philosophique")]),
      ("Religion, divination, justice et mort",[
        ("Amphiaraos","amphiaraos-analyse-philosophique"),("Cocalos","cocalos-analyse-philosophique"),("Les Héros","heros-analyse-philosophique"),("Anagyros","anagyros-analyse-philosophique"),("Les Saisons","saisons-analyse-philosophique"),("Les Hommes à la poêle","hommes-poele-analyse-philosophique"),("Les Telmessiens","telmessiens-analyse-philosophique"),("Dionysos naufragé — attribution discutée","dionysos-naufrage-analyse-philosophique"),("Niobos — attribution discutée","niobos-analyse-philosophique")]),
      ("Mythe, technique et parodie tragique",[
        ("Dédale","dedale-analyse-philosophique"),("Le Centaure — attribution discutée","centaure-analyse-philosophique"),("Les Phéniciennes","pheniciennes-analyse-philosophique")])
    ]
    if sum(len(works) for _,works in groups)!=33:
        raise RuntimeError("Aristophane : 33 études attendues")
    all_urls=set()
    html=['<section id="index-aristophane-33" class="aristophanes-index"><h2>Les 33 études d’Aristophane — catalogue réorganisé</h2><p>Accès par grands thèmes aux 33 analyses philosophiques des œuvres perdues, versions anciennes ou attributions discutées. Les fragments attestés doivent être distingués des reconstructions modernes. Les onze comédies conservées disposent de leur propre catalogue.</p><nav class="aristophanes-theme-nav" aria-label="Thèmes des 33 études">'+''.join('<a href="#aristophane-theme-'+str(i)+'">'+esc(name)+'</a>' for i,(name,_) in enumerate(groups,1))+'</nav>']
    for i,(name,works) in enumerate(groups,1):
        html.append('<section id="aristophane-theme-'+str(i)+'" class="aristophanes-theme"><h3>'+esc(name)+'</h3><ol class="aristophanes-study-list">')
        for title,prefix in works:
            found=[e for e in entries if e["url"].rstrip("/").split("/")[-1].startswith(prefix)]
            if len(found)!=1 or found[0]["url"] in all_urls:
                raise RuntimeError("Aristophane : étude absente, ambiguë ou doublonnée : "+prefix)
            all_urls.add(found[0]["url"])
            html.append('<li><a href="'+esc(found[0]["url"])+'">'+esc(title)+'</a></li>')
        html.append('</ol></section>')
    html.append('<p class="small-note">Classement thématique de consultation ; les numéros de la collection historique restent inchangés dans les manuscrits.</p><a href="#archives-aristophane-33">Lire les cycles universitaires et les analyses historiques conservés ↓</a></section><div id="archives-aristophane-33"></div>')
    fragment=BeautifulSoup(''.join(html),"html.parser")
    h1=article.find("h1")
    if h1:
        h1.insert_after(fragment)
    else:
        article.insert(0,fragment)
    path.write_text(str(page),encoding="utf-8")


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
    reorganize_preserved_plays_analyses(entries)
    reorganize_aristophanes_33(entries)
    create_origins(entries)
    create_encyclopedia(entries)
    create_philosophy(entries)
    create_civilisations(entries,groups)
    print("MYTHOS NAVIGATION :",sum(len(v) for v in groups.values()),"dossiers de civilisation répartis en",len(groups),"continents", {k:len(v) for k,v in groups.items()},flush=True)

def finalize_navigation(index_count):
    renovate_catalog(index_count)
    renovate_search()
    total=apply_navigation()
    print("MYTHOS NAVIGATION :",total,"pages avec menu commun, index thématique créé",flush=True)
