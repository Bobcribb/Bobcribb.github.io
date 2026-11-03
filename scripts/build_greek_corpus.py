#!/usr/bin/env python3
"""MYTHOS : entrée unique regroupant les publications grecques vérifiées par chemin."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from html import escape
import re

ARCHIVES = [
 ("Hésiode : cosmogonie et Théogonie","livre-hesiode.html"),
 ("Dictionnaire des dieux","livre-dieux.html"),
 ("Monographies et personnages","monographies.html"),
 ("Héraclès","livre-heracles.html"),
 ("Le cycle de Thèbes","livre-thebes.html"),
 ("Les Argonautiques","livre-argonautiques.html"),
 ("Le cycle de Troie","livre-troie.html"),
 ("L'Odyssée","livre-odyssee.html"),
 ("Atlas mythologique","atlas-mythologique.html"),
 ("Cultes et cités","cultes-cites.html"),
 ("Sources et méthodes","sources-methodes.html"),
 ("Historiographie","historiographie-v6.html"),
 ("Bibliothèque grecque","bibliotheque.html"),
 ("Bibliothèque historique générale, transversale","MYTHOS_bibliotheque_navigable.html"),
]
RELATED = [
 ("Homère, l'Iliade : analyse philosophique","/philosophie-iliade.html"),
 ("Homère, l'Odyssée : analyse philosophique","/philosophie-odyssee.html"),
 ("Hésiode, Théogonie : analyse philosophique","/philosophie-theogonie.html"),
 ("Études d'histoire et de géographie grecque","/grece/"),
 ("Théâtre grec, corpus associé mais distinct","/theatre/"),
 ("Grande Encyclopédie, collection distincte","/grande-encyclopedie/"),
]
def present(out, url):
    p = out / url.lstrip("/")
    return p.is_file() if url.endswith(".html") else (p/"index.html").is_file()

def scholarly_title(path):
    heads = []
    for line in path.read_text(encoding="utf-8").splitlines()[:65]:
        m = re.match(r"^#{1,3}\s+(.+)", line)
        if m:
            heads.append(re.sub(r"[*_\x60]", "", m.group(1)).strip())
    if len(heads)>1 and not heads[1].lower().startswith("mythos"):
        return heads[1]
    if heads and ":" in heads[0]:
        return heads[0].split(":",1)[1].strip()
    return heads[0] if heads else path.stem.replace("-", " ")

def page_title(path):
    d = BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    e = d.find("h1") or d.title
    return e.get_text(" ",strip=True) if e else path.parent.name.replace("-"," ").title()

def main(out, root):
    path = out/"mythologie-grecque"/"index.html"
    if not path.is_file():
        raise RuntimeError("Le portail grec principal est absent")
    doc = BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    article=doc.select_one("main article.content")
    if article is None: raise RuntimeError("Portail grec : article introuvable")
    old=doc.select_one("#greek-unified-corpus")
    if old: old.decompose()
    style=doc.select_one("#greek-unified-corpus-style")
    if style: style.decompose()
    chapters=[]; numbers=Counter()
    for src in sorted((root/"chapitres"/"encyclopedie").glob("chapitre-*.md")):
        m=re.match(r"chapitre-(\d+)-",src.stem)
        if not m: continue
        no=int(m.group(1))
        link="/chapitres/encyclopedie/"+src.stem+"/"
        if not present(out,link):
            raise RuntimeError("Chapitre universitaire non rendu : "+link)
        chapters.append((no,src.stem,link,"Chapitre "+str(no)+" — "+scholarly_title(src)))
        numbers[no]+=1
    chapters.sort(key=lambda x:(x[0],x[1]))
    if len(chapters)<50: raise RuntimeError("Corpus grec incomplet dans le dépôt")
    archives=[]
    for title,name in ARCHIVES:
        link="/corpus/mythologie-grecque/archives/"+name
        if not present(out,link): raise RuntimeError("Archive grecque absente : "+link)
        archives.append((link,title))
    monographs=[]
    for p in sorted((out/"corpus"/"mythologie-grecque").rglob("*.html")):
        if "archives" in p.parts: continue
        link="/"+p.relative_to(out).as_posix()
        monographs.append((link, "Aphrodite : étude universitaire complète" if "aphrodite" in p.stem else p.stem.replace("-"," ")))
    def individual(glob):
        return [("/"+p.relative_to(out).parent.as_posix()+"/", page_title(p))
                for p in sorted(out.glob(glob))]
    gods=individual("dieu-*/index.html")
    heroes=individual("heros-*/index.html")
    groups=[
      ("Archives et volumes complets","grec-archives",archives),
      ("Encyclopédie universitaire numérotée","grec-universitaire",[(u,t) for _,_,u,t in chapters]),
      ("Monographies propres au corpus MG","grec-monographies",monographs),
      ("Dieux et puissances divines","grec-dieux",gods),
      ("Héros et héroïnes","grec-heros",heroes),
      ("Philosophie, histoire et collections reliées","grec-liens",[(u,t) for t,u in RELATED if present(out,u)]),
    ]
    seen=set(); dedup=[]
    for label,key,items in groups:
        selected=[]
        for url,title in items:
            if url not in seen: seen.add(url); selected.append((url,title))
        dedup.append((label,key,selected))
    def link(url,title):
        return '<li><a href="'+escape(url,quote=True)+'">'+escape(title)+'</a></li>'
    menu=''.join('<a href="#'+key+'">'+escape(label)+' ('+str(len(items))+')</a>'
                 for label,key,items in dedup if items)
    blocks=''.join('<section class="greek-corpus-group" id="'+key+'"><h3>'+escape(label)+
                   ' <small>('+str(len(items))+')</small></h3><ol class="greek-corpus-links">'+
                   ''.join(link(u,t) for u,t in items)+'</ol></section>'
                   for label,key,items in dedup if items)
    colliding=", ".join(str(k) for k,v in sorted(numbers.items()) if v>1) or "aucune"
    html='''<section class="portal-section greek-corpus-full" id="greek-unified-corpus">
    <div class="greek-corpus-banner"><span class="greek-corpus-kicker">COLLECTION AUTONOME MG</span>
    <h2>Encyclopédie mythologique grecque : accès à tout le corpus disponible</h2>
    <p>Un sommaire unique vers les textes intégraux existants, les volumes historiques,
    les études universitaires, les dieux, les héros, les cycles, la philologie et les atlas.
    Les manuscrits restent à leur emplacement d'origine, sans duplication ni résumé.</p></div>
    <p class="greek-corpus-status">''' + str(len(chapters)) + ''' chapitres universitaires numérotés ;
    '''+str(len(archives))+''' archives intégrales ; '''+str(len(gods))+''' notices de dieux ;
    '''+str(len(heroes))+''' notices de héros. Inventaire vérifié des fichiers disponibles,
    non de tous les manuscrits mentionnés dans les anciens échanges.</p>
    <nav class="greek-corpus-toc" aria-label="Sommaire de toute la mythologie grecque">'''+menu+'''</nav>
    '''+blocks+'''
    <section class="greek-corpus-group greek-corpus-pending" id="grec-en-attente">
    <h3>Chapitres dont le manuscrit complet reste à récupérer</h3>
    <p>Chiron et les chapitres 118–133 ainsi que la série historique 218–224
    figurent au registre de récupération ; ils ne sont pas déclarés publiés
    sans contrôle de leurs textes complets. Les numéros historiques homonymes
    ('''+escape(colliding)+''') restent distingués par leurs titres et leurs chemins.</p>
    <p><a href="https://github.com/Bobcribb/Bobcribb.github.io/blob/main/corpus/mythologie-grecque/REGISTRE-RECUPERATION.md">Consulter le registre des manuscrits manquants</a></p>
    </section></section>'''
    intro=article.select_one("p.section-intro") or article.find("h1")
    if intro is None: raise RuntimeError("Absence d'introduction pour le portail grec")
    intro.insert_after(BeautifulSoup(html,"html.parser"))
    css=doc.new_tag("style",id="greek-unified-corpus-style")
    css.string=""" .greek-corpus-full{margin:2.5rem 0 3.5rem}
    .greek-corpus-banner{background:linear-gradient(90deg,#091013ee,#101617d7 48%,#081012ad),url('/assets/mythos-hero.svg') center/cover;padding:clamp(1.5rem,5vw,3.2rem);border:1px solid #b18e53;border-radius:6px}
    .greek-corpus-banner h2{color:#f0d6a1;font:clamp(1.8rem,3.6vw,3rem)/1.15 Georgia,serif;max-width:780px}
    .greek-corpus-banner p{color:#f1e7d7;line-height:1.65;max-width:750px}
    .greek-corpus-kicker{color:#d8b778;font:600 .8rem system-ui;letter-spacing:.15em}
    .greek-corpus-status{background:#151c1c;color:#e3d6bc;border-left:3px solid #b39158;padding:1rem}
    .greek-corpus-toc{display:flex;gap:.6rem;flex-wrap:wrap;margin:1rem 0 2rem}
    .greek-corpus-toc a{flex:1 1 205px;display:block;padding:.6rem;border:1px solid #8b724d;background:#151b1b;color:#e8cc98;text-align:center;text-decoration:none;border-radius:5px}
    .greek-corpus-toc a:focus-visible{outline:3px solid #ffe1a9}
    .greek-corpus-group{margin:1.2rem 0;padding:1.2rem;background:#111819;border:1px solid #6f5938;border-radius:6px}
    .greek-corpus-group h3{color:#e5c58d;font:clamp(1.3rem,2.3vw,1.85rem) Georgia,serif}
    .greek-corpus-group small{font:.8rem system-ui;color:#c9b186}
    .greek-corpus-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.35rem 1.3rem;margin:0;padding:0;list-style:none}
    .greek-corpus-links li{border-bottom:1px solid #443627;padding:.25rem 0;min-width:0}
    .greek-corpus-links a{display:block;color:#eadbc1;overflow-wrap:anywhere;padding:.35rem 0}
    .greek-corpus-links a:hover{color:#ffe2a3}
    .greek-corpus-pending{border-style:dashed}
    @media(max-width:760px){.greek-corpus-links{grid-template-columns:1fr}
    .greek-corpus-group{padding:.85rem}.greek-corpus-toc a{flex:1 1 100%}}
    """
    doc.head.append(css)
    path.write_text(str(doc),encoding="utf-8")
    return {"chapitres":len(chapters),"archives":len(archives),"dieux":len(gods),
            "heros":len(heroes),"monographies":len(monographs),"liens_uniques":len(seen)}

if __name__=="__main__":
    print(main(Path("_site").resolve(),Path(".").resolve()))
