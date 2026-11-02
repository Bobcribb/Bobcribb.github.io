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
<a href="/mythologies/">Mythologies</a>
<a href="/grece/" class="nav-greece">Grèce antique</a>
<a href="/theatre/">Théâtre</a>
<a href="/philosophie/">Philosophie</a>
<a href="/civilisations/">Civilisations</a>
<a href="/rubriques/">Index</a>
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
      ("/philosophie/","Études philosophiques","Hegel, Nietzsche, philosophie antique et interprétation des mythes.","ANALYSE CRITIQUE"),
    ])
    continent_cards=cards([(f"/civilisations/{k}/",label,f"{len(groups[k])} dossiers — {subtitle}","PAR CONTINENT") for k,(label,subtitle) in CONTINENTS.items()])
    world=cards([
        ("/bibliotheque-egypte-ancienne/","Égypte ancienne","Osiris, Rê, Maât, Akhetaton et l’au-delà.","AFRIQUE"),
        ("/bibliotheque-mesopotamie/","Mésopotamie","Gilgameš, Inanna, Marduk et les mythes de la création.","ASIE"),
        ("/bibliotheque-perse-iran-ancien/","Perse et Iran ancien","Ahura Mazdā, royauté et traditions iraniennes.","ASIE"),
        ("/bibliotheque-mythologies-du-monde/","Traditions du monde","Dictionnaire des dieux, héros et récits comparés.","COLLECTION"),
    ])
    body=introductory+section("Quatre parcours pour entrer dans l’encyclopédie","Choisissez un univers, un genre littéraire ou une méthode d’étude.",major)
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

def create_theatre(entries):
    tragedies=[e for e in entries if starts(e,"/tragedies/","/chapitres/tragedies/") or e["url"] in ("/euripide-bacchantes-dionysos-tragedie/","/aristophane-grenouilles-theatre-cite/") and False]
    comedies=[e for e in entries if starts(e,"/comedie-grecque-aristophane-menandre-etudes/","/chapitres/comedies/")]
    body='<h1>Théâtre grec</h1><p class="portal-lead">Le théâtre ancien comme archive des mythes et laboratoire de la cité. Œuvres conservées, fragments de pièces perdues, reconstitutions explicitement modernes et interprétations critiques.</p>'
    body+=section("Les trois grands tragiques","Éditions critiques, tragédies conservées et œuvres perdues.",cards([
      ("/tragedies/","Tragédie grecque","Panorama d’Eschyle, Sophocle et Euripide."),
      ("/tragedies/bibliotheque-tragedies-etudes-individuelles/","Pièces conservées","Analyses individuelles et références."),
      ("/tragedies/mythos-bibliotheque-89-tragedies-perdues-edition-vii/","Tragédies perdues","Fragments, attributions et hypothèses."),
      ("/theatre-grec-conserve-etudes-philosophiques/","51 études philosophiques","Étudier les pièces à travers leurs problèmes.")
    ]))
    body+=section("Comédie ancienne et nouvelle","D’Aristophane à Ménandre : satire, politique et représentations sociales.",cards([
      ("/comedie-grecque-aristophane-menandre-etudes/","Bibliothèque de la comédie","Dossiers et analyses."),
      ("/comedies-grecques-aristophane-menandre/","Aristophane et Ménandre","Œuvres et philosophie du rire."),
      ("/comedie-grecque-aristophane-menandre-etudes/aristophane-catalogue-critiques-33-comedies-perdues/","33 comédies perdues","Catalogue raisonné et variantes."),
      ("/comedie-grecque-aristophane-menandre-etudes/aristophane-bibliotheque-etudes-philosophiques/","Monographies critiques","Analyses historiques et philosophiques.")
    ]))
    body+=section("Parcourir tous les dossiers de théâtre","Toutes les études théâtrales restent accessibles, y compris les pièces perdues.",details(tragedies,f"Voir les {len(tragedies)} dossiers de tragédie")+details(comedies,f"Voir les {len(comedies)} dossiers de comédie"))
    write("theatre",shell("Théâtre grec — tragédies et comédies",body))

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
  ("/grece/","Grèce antique","Dieux, héros, cultes et épopées"),
  ("/theatre/","Théâtre","Tragédies, comédies et fragments"),
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
  ("/grece/","Grèce","Dieux, héros et sanctuaires grecs."),
  ("/theatre/","Théâtre","Œuvres et analyses."),
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
    create_theatre(entries)
    create_philosophy(entries)
    create_civilisations(entries,groups)
    print("MYTHOS NAVIGATION :",sum(len(v) for v in groups.values()),"dossiers de civilisation répartis en",len(groups),"continents", {k:len(v) for k,v in groups.items()},flush=True)

def finalize_navigation(index_count):
    renovate_catalog(index_count)
    renovate_search()
    total=apply_navigation()
    print("MYTHOS NAVIGATION :",total,"pages avec menu commun, index thématique créé",flush=True)
