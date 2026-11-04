#!/usr/bin/env python3
"""MYTHOS : entrée unique regroupant les publications grecques vérifiées par chemin."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from html import escape
import re
import hashlib
import json


REWRITES = Path('corpus/mythologie-grecque/recritures-2026-11-04.json')


def rewritten_studies(root):
    """Resolve new studies through their allocation receipts, never guessed numbers."""
    manifest = root / REWRITES
    if not manifest.is_file():
        return []
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('version') != 1:
        raise RuntimeError('Version du parcours de réécriture inconnue')
    registry = json.loads((root / 'editorial/numbering.json').read_text(encoding='utf-8'))
    allocations = registry['collections']['encyclopedie']['allocations']
    rows = []
    seen = set()
    for study in data['studies']:
        key = study['request_id']
        if key in seen:
            raise RuntimeError('Réécriture répétée : ' + key)
        seen.add(key)
        receipt = allocations.get(key)
        if not receipt:
            raise RuntimeError('Réécriture non attribuée : ' + key)
        expected = f"chapitres/encyclopedie/chapitre-{receipt['number']}-{study['slug']}.md"
        if receipt['path'] != expected or not (root / expected).is_file():
            raise RuntimeError('Manuscrit de réécriture incohérent : ' + key)
        if study['kind'] not in ('identified', 'reconstructed'):
            raise RuntimeError('Statut de réécriture inconnu : ' + key)
        if study['kind'] == 'reconstructed' and study['historical_number'] is not None:
            raise RuntimeError('Numéro historique inventé pour une reconstruction : ' + key)
        rows.append({**study, 'number': receipt['number'], 'url': '/' + expected[:-3] + '/'})
    return rows

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
# Volumes déjà publiés, auparavant absents du sommaire de la Grande Encyclopédie.
BOOKS = [
 ("Hésiode : Théogonie et Travaux", "livre-hesiode"),
 ("Encyclopédie des dieux grecs", "livre-dieux"),
 ("Trente monographies de dieux et de héros", "monographies"),
 ("Héraclès : travaux et traditions", "livre-heracles"),
 ("Thèbes : de Cadmos à Antigone", "livre-thebes"),
 ("Jason, Médée et les Argonautiques", "livre-argonautiques"),
 ("Le cycle de Troie", "livre-troie"),
 ("Les Atrides : de Tantale à Oreste", "livre-atrides"),
 ("L’Iliade : lecture chant par chant", "iliade"),
 ("L’Iliade : lecture scène par scène", "livre-iliade-scenes"),
 ("L’Odyssée : les vingt-quatre chants", "livre-odyssee"),
 ("L’Odyssée : dossiers et analyses", "odyssee"),
 ("Atlas mythologique", "atlas-mythologique"),
 ("Cultes et cités", "cultes-cites"),
 ("Sources et méthodes", "sources-methodes"),
 ("L’école de Paris", "ecole-paris"),
 ("Historiographie des mythes", "historiographie-v6"),
 ("Bibliothèque grecque", "bibliotheque"),
]
DOSSIERS = [
 "papyrus-derveni-orphee-cosmogonie-philosophie-presocratique",
 "artemis-ephese-artemision-temple-culte-anatolie",
 "brauron-artemis-arkteia-ourses-rites-attique",
 "delphes-oracle-apollon-etude", "delos-apollon-sanctuaire-histoire-archeologie",
 "dodone-zeus-oracle-chene-lamelles", "eleusis-demeter-persephone-mysteres",
 "epidaure-asclepios-incubation-iamata-guerisons",
 "amphiaraion-oropos-amphiaraos-oracle-guerison-incubation",
 "hecate-hesiode-demeter-carrefours-lagina-culte",
 "isthmia-poseidon-jeux-isthmiques-palemon", "nemee-zeus-jeux-nemeens-opheltes",
 "olympie-zeus-jeux-sanctuaire-etude", "samothrace-grands-dieux-mysteres-victoire",
 "sappho-aphrodite-poesie-lyrique-fragments-papyrus", "orphee-lamelles-or-initiation-au-dela",
 "aristophane-grenouilles-theatre-cite", "euripide-bacchantes-dionysos-tragedie",
 "2026/10/28/dionysos-thebes-prologue-bacchantes",
 "2026/10/27/demeter-demophon-immortalite-eleusis", "2026/10/27/demodocos-pilote-mythos",
 "bestiaire", "recits", "religion", "textes", "glossaire", "bibliographie", "chronologie",
]


def number_ranges(numbers):
    ranges = []
    for number in sorted(set(numbers)):
        if ranges and number == ranges[-1][1] + 1:
            ranges[-1][1] = number
        else:
            ranges.append([number, number])
    return ", ".join(str(a) if a == b else f"{a}–{b}" for a, b in ranges)


def book_sections(out, slug):
    """Liens vers les sections existantes, sans inventer de chapitres numérotés."""
    path = out / slug / "index.html"
    if not path.is_file():
        raise RuntimeError("Livre grec absent : " + slug)
    doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = doc.select_one("article.content")
    if article is None:
        raise RuntimeError("Livre grec sans article : " + slug)
    before = article.get_text()
    used = {tag['id'] for tag in doc.select('[id]')}
    rows = []
    for heading in article.select("h2, h3"):
        if heading.find_parent(["nav", "aside"]) or heading.find_parent(class_="toc"):
            continue
        title = heading.get_text(" ", strip=True)
        if not title:
            continue
        if not heading.get('id'):
            base = "lecture-" + hashlib.sha256(title.encode()).hexdigest()[:12]
            anchor = base
            suffix = 2
            while anchor in used:
                anchor = base + "-" + str(suffix)
                suffix += 1
            heading['id'] = anchor
            used.add(anchor)
        rows.append(("/" + slug + "/#" + heading['id'], title))
    if article.get_text() != before:
        raise RuntimeError("Texte modifié pendant l’indexation : " + slug)
    path.write_text(str(doc), encoding="utf-8")
    return rows


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
    if heads and re.search(r"chapitre\s+\d+\s*:", heads[0], re.I):
        return heads[0].split(":", 1)[1].strip()
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
    rewrites = rewritten_studies(root)
    path = out/"mythologie-grecque"/"index.html"
    if not path.is_file():
        raise RuntimeError("Le portail grec principal est absent")
    doc = BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    article=doc.select_one("main article.content")
    if article is None: raise RuntimeError("Portail grec : article introuvable")
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
    books = [("/"+slug+"/", title) for title, slug in BOOKS]
    sections = [(title, book_sections(out, slug)) for title, slug in BOOKS]
    dossiers = [("/"+slug+"/", page_title(out/slug/"index.html")) for slug in DOSSIERS if present(out, "/"+slug+"/")]
    groups=[
      ("Livres, cycles et lectures des épopées", "grec-livres", books),
      ("Archives historiques conservées","grec-archives",archives),
      ("Encyclopédie universitaire numérotée","grec-universitaire",[(u,t) for _,_,u,t in chapters]),
      ("Monographies propres au corpus MG","grec-monographies",monographs),
      ("Dieux et puissances divines","grec-dieux",gods),
      ("Héros et héroïnes","grec-heros",heroes),
      ("Sanctuaires, récits et dossiers documentaires", "grec-dossiers", dossiers),
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
    if any(v > 1 for v in numbers.values()):
        raise RuntimeError("Doublon dans le sommaire grec : " + str(dict(numbers)))
    missing = number_ranges(set(range(1, max(numbers)+1)) - set(numbers))
    section_count = sum(len(rows) for _, rows in sections)
    section_html = '<section class="greek-corpus-group" id="grec-sections"><h3>Sommaires détaillés des livres</h3><p>Accès direct aux '+str(section_count)+' sections existantes. Ces subdivisions des livres ne sont pas les numéros de la série universitaire.</p>'
    for title, rows in sections:
        section_html += '<details class="greek-book"><summary>'+escape(title)+' — '+str(len(rows))+' sections</summary><ul class="greek-corpus-links">'+''.join(link(u,t) for u,t in rows)+'</ul></details>'
    section_html += '</section>'
    menu += '<a href="#grec-sections">Sommaires détaillés ('+str(section_count)+')</a><a href="#grec-en-attente">État des lacunes</a>'
    rewrite_html = ''
    recovery_status = '''<p>Chiron et les chapitres 118–133 ainsi que la série historique 218–224
    figurent au registre de récupération ; ils ne sont pas déclarés publiés
    sans contrôle de leurs textes complets. La numérotation des études présentes est unique ;
    les anciennes références sont conservées dans le registre de correspondance.</p>'''
    if rewrites:
        identified = sum(s['kind'] == 'identified' for s in rewrites)
        reconstructed = len(rewrites) - identified
        menu = '<a href="#grec-recritures">Nouvelles rédactions ('+str(len(rewrites))+')</a>' + menu
        rewrite_html = '<section class="greek-corpus-group" id="grec-recritures"><h3>'+str(len(rewrites))+' nouvelles études pour les lacunes du corpus</h3>'
        rewrite_html += '<p>Rédaction du 4 novembre 2026 : '+str(identified)+' sujets historiquement identifiés (Chiron, ancien 118 ; série 218–224) et '+str(reconstructed)+' études d’un parcours reconstitué du Pélion aux Hespérides. Chaque texte développe le récit, les variantes et une analyse accompagnée de références antiques.</p>'
        rewrite_html += '<p><strong>Les anciens manuscrits n’ont pas été retrouvés.</strong> Les nouveaux textes sont signalés comme tels. Pour 119–133, les titres exacts restent inconnus : les sujets du parcours ne leur sont pas attribués arbitrairement. Les numéros actuels ci-dessous sont ceux de la collection publiée.</p>'
        for series, title in [('pelion-hesperides', 'Du Pélion aux Hespérides'), ('cosmogonie', 'Origines divines, souveraineté et condition humaine')]:
            rewrite_html += '<h4>'+title+'</h4><ol class="greek-corpus-links">'
            for study in rewrites:
                if study['series'] != series:
                    continue
                historical = ('Sujet de l’ancien chapitre '+str(study['historical_number'])) if study['kind'] == 'identified' else 'Parcours reconstitué ; numéro historique non établi'
                rewrite_html += '<li id="recriture-'+escape(study['slug'], quote=True)+'"><a href="'+escape(study['url'], quote=True)+'">Chapitre '+str(study['number'])+' — '+escape(study['title'])+'</a><small>'+escape(historical)+' · Nouvelle rédaction</small></li>'
            rewrite_html += '</ol>'
        rewrite_html += '</section>'
        recovery_status = '<p>Les sujets de Chiron (ancien 118) et de la série 218–224 disposent désormais de <a href="#grec-recritures">nouvelles rédactions intégrales</a>. Un parcours de quinze études complète la continuation jusqu’aux Hespérides ; ses sujets ne sont pas présentés comme les titres retrouvés de 119–133. La récupération des anciens manuscrits reste distincte de ces nouvelles publications.</p>'
    html='''<section class="portal-section greek-corpus-full" id="greek-unified-corpus">
    <div class="greek-corpus-banner"><span class="greek-corpus-kicker">CORPUS GREC · MYTHOS</span>
    <h2>Mythologie grecque : livres, chapitres et dossiers disponibles</h2>
    <p>Un sommaire unique vers les textes intégraux existants, les volumes historiques,
    les études universitaires, les dieux, les héros, les cycles, la philologie et les atlas.
    Les études intégrales sont conservées ; les anciennes adresses suivent les références corrigées.</p></div>
    <p class="greek-corpus-status">''' + str(len(books)) + ''' livres et parcours ; '''+str(section_count)+''' sections accessibles directement ; '''+ str(len(chapters)) + ''' chapitres universitaires numérotés ;
    '''+str(len(archives))+''' accès aux archives ; '''+str(len(gods))+''' notices de dieux ;
    '''+str(len(heroes))+''' notices de héros. Inventaire vérifié des fichiers disponibles,
    non de tous les manuscrits mentionnés dans les anciens échanges.</p>
    <nav class="greek-corpus-toc" aria-label="Sommaire de toute la mythologie grecque">'''+menu+'''</nav>
    '''+rewrite_html+blocks+section_html+'''
    <section class="greek-corpus-group greek-corpus-pending" id="grec-en-attente">
    <h3>Chapitres dont le manuscrit complet reste à récupérer</h3>
    <p><strong>Série universitaire : numéros sans manuscrit individuel dans le dépôt — '''+escape(missing)+'''.</strong>
    Ces trous ne prouvent pas la perte d’autant de textes : les anciennes séries et les livres ont leurs propres divisions.
    Les notices courtes ou les sections d’un livre ne remplacent pas une étude approfondie manquante.</p>
    '''+recovery_status+'''
    <p><a href="https://github.com/Bobcribb/Bobcribb.github.io/blob/main/corpus/mythologie-grecque/REGISTRE-RECUPERATION.md">Consulter le registre des manuscrits manquants</a></p>
    </section></section>'''
    css=doc.new_tag("style",id="greek-unified-corpus-style")
    css.string=""" .greek-corpus-full{margin:2.5rem 0 3.5rem}
    .greek-corpus-banner{background:linear-gradient(90deg,#091013ee,#101617d7 48%,#081012ad),url('/assets/mythos-museum-banner.webp') center/cover;padding:clamp(1.5rem,5vw,3.2rem);border:1px solid #b18e53;border-radius:6px}
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
    css.string += " .greek-book{margin:.7rem 0;border-top:1px solid #6f5938;padding:.7rem 0}.greek-book summary{cursor:pointer;color:#e5c58d;padding:.5rem;font-size:1.1rem}.greek-book summary:focus-visible{outline:3px solid #ffe1a9}.greek-corpus-toc{justify-content:center} "
    from build_navigation import shell
    portals = [
        ("mythologie-grecque", "Encyclopédie mythologique grecque"),
        ("grande-encyclopedie", "Grande Encyclopédie mythologique grecque"),
    ]
    for slug, title in portals:
        intro = '<h1>'+escape(title)+'</h1><p class="portal-lead">Retrouvez les livres anciens, les études numérotées et les dossiers déjà publiés. Le catalogue distingue les textes disponibles des manuscrits encore à retrouver.</p>'
        extra = '<p><a href="/bibliotheque-mythologies-du-monde/">Bibliothèque des mythologies du monde</a> · <a href="/mythologie-comparee/">Mythologie comparée</a> · <a href="/origines-du-sacre/">Origines du sacré</a> · <a href="/theatre/">Théâtre grec</a></p>'
        rendered = BeautifulSoup(shell(title, intro+html+extra), "html.parser")
        rendered.head.append(BeautifulSoup(str(css), "html.parser"))
        canonical = rendered.new_tag('link', rel='canonical', href='https://bobmythos.fr/'+slug+'/')
        rendered.head.append(canonical)
        for target in [out/slug/"index.html", out/(slug+".html")]:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(rendered), encoding="utf-8")
    return {"chapitres":len(chapters),"archives":len(archives),"dieux":len(gods),
            "heros":len(heroes),"monographies":len(monographs),"liens_uniques":len(seen),
            "livres":len(books),"sections":section_count,"dossiers":len(dossiers),"lacunes_numeriques":missing,
            "nouvelles_redactions":len(rewrites)}



def verify(out, root):
    """Refuse un sommaire incomplet ou des liens de section introuvables."""
    from urllib.parse import urlsplit, unquote
    pages = [out / name for name in (
        'mythologie-grecque/index.html', 'mythologie-grecque.html',
        'grande-encyclopedie/index.html', 'grande-encyclopedie.html')]
    expected = {'/chapitres/encyclopedie/'+p.stem+'/'
                for p in (root/'chapitres/encyclopedie').glob('chapitre-*.md')}
    expected.update('/'+slug+'/' for _, slug in BOOKS)
    rewrites = rewritten_studies(root)
    reference = None
    cache = {}
    for page in pages:
        doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        catalog = doc.select_one('#greek-unified-corpus')
        assert catalog, f'Sommaire grec absent : {page}'
        links = {a['href'] for a in catalog.select('a[href]')}
        assert expected <= links, f'Textes absents de {page} : {expected - links}'
        if rewrites:
            section = catalog.select_one('#grec-recritures')
            assert section, f'Parcours de réécriture absent : {page}'
            rewritten_links = {a['href'] for a in section.select('a[href]')}
            assert rewritten_links == {s['url'] for s in rewrites}, f'Parcours de réécriture incomplet : {page}'
        assert "'+escape(" not in catalog.get_text(), 'Interpolation non résolue'
        if reference is None:
            reference = links
        assert links == reference, f'Ancienne entrée restée incomplète : {page}'
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (out / unquote(parsed.path).lstrip('/')) if parsed.path else page
            if parsed.path.endswith('/'):
                target = target / 'index.html'
            assert target.is_file(), f'Page liée absente : {page} → {link}'
            if parsed.fragment:
                if target not in cache:
                    cache[target] = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                assert cache[target].find(id=unquote(parsed.fragment)), f'Section absente : {link}'
    print(f'OK : quatre sommaires grecs cohérents, {len(expected)} manuscrits/livres attendus et toutes les ancres accessibles')


if __name__=="__main__":
    print(main(Path("_site").resolve(),Path(".").resolve()))
