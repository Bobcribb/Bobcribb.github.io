#!/usr/bin/env python3
"""Publie MYTHOS depuis le dépôt GitHub, sans accès à WordPress.

Source de vérité : fichiers HTML existants dans main, médias dans media/,
et nouvelles études Markdown dans chapitres/. Ne publie aucun brouillon.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape as xml_escape
import html
import json
import os
import re
import shutil
import sys

import mistune
from bs4 import BeautifulSoup

ROOT = Path(".").resolve()
OUT = Path("_site").resolve()
SITE_URL = "https://bobmythos.fr"
MIN_HTML_PAGES = 450
MIN_MEDIA_FILES = 110
markdown = mistune.create_markdown(escape=True, plugins=["table", "strikethrough", "url"])
EXCLUDED = {".git", ".github", "scripts", "chapitres", "_site", ".venv", "node_modules", "__pycache__", ".pytest_cache"}

def text(s):
    return re.sub(r"\s+", " ", BeautifulSoup(s or "", "html.parser").get_text(" ", strip=True)).strip()

def render(title, body, description=""):
    label = html.escape(title, quote=True)
    desc = html.escape(description[:230] or "Encyclopédie MYTHOS — Mythes, civilisations et philosophie", quote=True)
    return f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}"><title>{label} | MYTHOS</title>
<link rel="stylesheet" href="/assets/style.css"></head><body>
<header class="masthead"><div class="masthead-inner"><a href="/" class="brand">MYTHOS <span>✦</span></a>
<nav><a href="/">Accueil</a><a href="/rubriques/">Dossiers</a><a href="/recherche/">Recherche</a></nav></div></header>
<main class="layout"><article class="content"><div class="eyebrow">BIBLIOTHÈQUE · MYTHOS</div>
{body}</article></main>
<footer class="footer"><span>MYTHOS — Encyclopédie universitaire comparative</span><a href="/rubriques/">Tous les dossiers</a></footer>
<script defer src="/assets/search.js"></script></body></html>'''

def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.resolve().is_relative_to(OUT):
        raise ValueError("Chemin interdit " + str(path))
    p.write_text(content, encoding="utf-8")

def copy_repository():
    # Prendre uniquement les fichiers utiles au site ; ne pas rendre publics
    # les scripts, workflows, brouillons ou futures sources Markdown.
    count=0
    for current, directories, files in os.walk(ROOT):
        base = Path(current)
        directories[:] = [d for d in directories if d not in EXCLUDED and not d.startswith(".")]
        rel = base.relative_to(ROOT)
        for file in files:
            source = base / file
            if not source.is_file():
                continue
            if rel.parts and rel.parts[0] in ("media", "assets"):
                if file.startswith(".") and file != ".nojekyll":
                    continue
                target=OUT / rel / file
            elif file.lower().endswith(".html") and (not rel.parts or (rel.parts[0] not in EXCLUDED)):
                # Conserver aussi les pages HTML historiques dont le nom n'est
                # pas index.html (anciens portails, corpus et dossiers migrés).
                target=OUT / rel / file
                count += 1
            elif not rel.parts and file in ("404.html", "CNAME", ".nojekyll", "robots.txt", "sitemap.xml", "search.json"):
                target=OUT / file
            else:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source,target)
    # Copier les sources et ressources du corpus déjà liées depuis les pages
    # publiques (manuscrits, CSS, scripts, catalogues et médias existants).
    # Les fichiers non référencés ne sont pas ajoutés à la publication.
    linked_sources = set()
    for page in OUT.rglob("*.html"):
        page_html = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for anchor in page_html.select("[href], [src], [poster]"):
            link = str(anchor.get("href") or anchor.get("src") or anchor.get("poster") or "")
            href = link.split("#", 1)[0].split("?", 1)[0]
            if Path(href).suffix.lower() not in {".md", ".css", ".js", ".json", ".svg", ".webp", ".jpg", ".png", ".pdf"} or href.startswith(("http:", "https:", "//")):
                continue
            try:
                rel_source = (Path(href.lstrip("/")) if href.startswith("/")
                              else (page.parent / href).resolve().relative_to(OUT))
            except ValueError:
                continue
            if not rel_source.parts or rel_source.parts[0] != "corpus":
                continue
            source = ROOT / rel_source
            if source.is_file():
                target = OUT / rel_source
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                linked_sources.add(rel_source.as_posix())
    # Les livres archivés proviennent d'un ancien export à fichiers plats.
    # Raccorder les liens absents à leur page migrée, seulement si elle existe.
    # Les archives sources restent inchangées : ces réparations concernent
    # exclusivement leurs copies dans _site.
    archive = OUT / "corpus" / "mythologie-grecque" / "archives"
    legacy_media_url = re.compile(
        r"https?://bobmythos\.wordpress\.com/wp-content/uploads/2026/10/"
        r"([A-Za-z0-9_.%-]+\.(?:jpg|jpeg|png|webp))", re.IGNORECASE)
    for page in archive.glob("*.html"):
        original_html = page.read_text(encoding="utf-8")
        # Les URL sont parfois dans du JavaScript intégré : une substitution
        # HTML via les seuls <img> les manquerait. Toute photo doit exister
        # localement, sous le même nom, avant le changement d'adresse.
        def local_image(match):
            filename = match.group(1)
            target = OUT / "media" / "2026" / "10" / filename
            return "/media/2026/10/" + filename if target.is_file() else match.group(0)
        local_html = legacy_media_url.sub(local_image, original_html)
        doc = BeautifulSoup(local_html, "html.parser")
        changed = local_html != original_html
        for anchor in doc.find_all("a", href=True):
            link = urlsplit(str(anchor["href"]))
            if link.scheme or link.netloc or "/" in link.path or not link.path.endswith(".html"):
                continue
            if (page.parent / link.path).exists():
                continue
            migrated = OUT / Path(link.path).stem / "index.html"
            if migrated.is_file():
                anchor["href"] = urlunsplit(("", "", "/" + Path(link.path).stem + "/", link.query, link.fragment))
                changed = True
        # Treize livres appellent assets/app.js, absent jusque dans le dépôt
        # historique. Éviter une requête 404 ; ne jamais retirer un script
        # existant, ni les outils de lecture actuels déjà chargés ailleurs.
        for script in list(doc.select('script[src="assets/app.js"]')):
            if not (page.parent / "assets" / "app.js").is_file():
                script.decompose()
                changed = True
        if changed:
            page.write_text(str(doc), encoding="utf-8")
    print(f"Ressources du corpus liées et publiées : {len(linked_sources)}")
    if count < MIN_HTML_PAGES:
        raise RuntimeError(f"Protection : seulement {count} pages HTML dans GitHub, minimum {MIN_HTML_PAGES}")
    medias = [p for p in (OUT/"media").rglob("*") if p.is_file() and p.name != "manifest.json"]
    if len(medias) < MIN_MEDIA_FILES:
        raise RuntimeError(f"Protection : {len(medias)} médias, minimum {MIN_MEDIA_FILES}")
    return count, len(medias)

def frontmatter(raw):
    # Optionnel : title: et description: dans un front matter YAML simple.
    meta={}
    if raw.startswith("---\n"):
        head, sep, rest=raw[4:].partition("\n---\n")
        # Ne reconnaître un front matter que si le bloc initial contient
        # de véritables clés YAML ; les séparateurs éditoriaux ne sont pas du YAML.
        if sep and head.strip() and all(re.match(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:", line) for line in head.splitlines() if line.strip()):
            for line in head.splitlines():
                if ":" in line:
                    k, v=line.split(":",1)
                    k=k.strip()
                    if k in ("title","description"):
                        meta[k]=v.strip().strip("'\"")
            raw=rest
    return meta,raw

def resolve_chapter_links(html_body, source, chapters):
    """Raccorder les liens relatifs .md aux lecteurs HTML publiés."""
    # Mistune échappe le HTML des manuscrits. Rétablir uniquement les ancres
    # vides documentaires, jamais du HTML arbitraire ou des attributs actifs.
    html_body = re.sub(
        r'&lt;a id=&quot;([A-Za-z][A-Za-z0-9_-]*)&quot;&gt;&lt;/a&gt;',
        r'<span id="\1"></span>', html_body,
    )
    soup = BeautifulSoup(html_body, "html.parser")
    ids = {node["id"] for node in soup.select("[id]")}
    requested = {a["href"][1:] for a in soup.select('a[href^="#"]')}
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        match = re.match(r"(?:Chapitre\s+)?(\d+)(?:\b|\.)", heading.get_text(" ", strip=True), re.I)
        if match and not heading.get("id"):
            anchor = ("chap-" if "chap-" + match.group(1) in requested else "chapitre-") + match.group(1)
            if anchor not in ids:
                heading["id"] = anchor
                ids.add(anchor)
    root = chapters.resolve()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if href == "/catalogue/":
            anchor["href"] = "/rubriques/"
            continue
        plain, sep, fragment = href.partition("#")
        if not plain.endswith(".md") or plain.startswith(("/", "http:", "https:", "//")):
            continue
        target = (source.parent / plain).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            continue
        rel = target.relative_to(root)
        if rel.name.lower() == "readme.md":
            anchor["href"] = ("https://github.com/Bobcribb/Bobcribb.github.io/blob/main/chapitres/"
                              + rel.as_posix() + ("#" + fragment if sep else ""))
        else:
            anchor["href"] = "/chapitres/" + rel.with_suffix("").as_posix() + "/" + ("#" + fragment if sep else "")
    return str(soup)

def publish_chapters():
    chapters=Path("chapitres")
    published=[]
    if not chapters.is_dir():
        return published
    for source in sorted(chapters.rglob("*.md")):
        if source.name.lower()=="readme.md":
            continue
        rel=source.relative_to(chapters)
        if any(part.startswith(".") or part in (".","..") for part in rel.parts):
            continue
        slugpath=rel.with_suffix("")
        if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*",part) for part in slugpath.parts):
            raise ValueError("Nom de chapitre invalide : "+str(rel))
        url="/chapitres/"+"/".join(slugpath.parts)+"/"
        meta,body=frontmatter(source.read_text(encoding="utf-8"))
        title=meta.get("title","")
        if not title:
            heading=re.search(r"(?m)^#\s+(.+)$",body)
            title=heading.group(1).strip() if heading else slugpath.name.replace("-"," ").title()
        if not body.strip() or len(text(markdown(body)))<60:
            raise ValueError("Chapitre trop court : "+str(source))
        desc=meta.get("description") or text(markdown(body))[:190]
        page=OUT / url.lstrip("/") / "index.html"
        # Les pages HTML générées lors du précédent déploiement sont
        # conservées dans main : les reconstruire depuis leur Markdown,
        # sans les traiter comme des doublons éditoriaux.
        write(url.lstrip("/")+"index.html",render(title,resolve_chapter_links(markdown(body),source,chapters),desc))
        published.append({"title":text(title),"url":url,"excerpt":text(desc)[:190]})
    return published

def reindex(chapters):
    index_path=OUT/"search.json"
    if not index_path.exists():
        raise RuntimeError("L'index source MYTHOS est absent")
    existing=json.loads(index_path.read_text(encoding="utf-8"))
    from editorial_numbering import redirects
    historical_aliases = redirects(ROOT)
    by_url={}
    for entry in existing:
        path=entry.get("url","")
        if path not in historical_aliases and path.startswith("/") and not path.startswith("//") and (OUT/path.lstrip("/")/"index.html").is_file():
            by_url[path]={"title":str(entry.get("title","")).strip(),
                          "url":path,"excerpt":str(entry.get("excerpt",""))[:190]}
    for entry in chapters:
        if entry["url"] not in historical_aliases:
            by_url[entry["url"]]=entry
    # Inclure également les pages HTML ajoutées directement dans GitHub.
    for p in OUT.rglob("index.html"):
        rel=p.relative_to(OUT).parent
        if not rel.parts or rel.parts[0] in ("rubriques","recherche"):
            continue
        url="/"+"/".join(rel.parts)+"/"
        if url in by_url or url in historical_aliases:
            continue
        doc=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
        for owned in doc.select("[data-reading-owned], [data-epic-owned], [data-discovery-footer]"):
            owned.decompose()
        title=text(str(doc.h1 or doc.title or url))
        para=doc.select_one(".content p") or doc.select_one("p")
        excerpt=text(str(para))[:190] if para else ""
        by_url[url]={"title":title,"url":url,"excerpt":excerpt}
    # Tous les lecteurs autonomes : corpus, études philosophiques et sites.
    # Les redirections et la page d'erreur ne sont pas des résultats de recherche.
    for p in OUT.rglob("*.html"):
        if p.name in ("index.html", "404.html"):
            continue
        url = "/" + p.relative_to(OUT).as_posix()
        if url in by_url or url in historical_aliases:
            continue
        doc = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
        if any(str(meta.get("http-equiv", "")).lower() == "refresh"
               for meta in doc.find_all("meta")):
            continue
        for owned in doc.select("[data-reading-owned], [data-epic-owned], [data-discovery-footer]"):
            owned.decompose()
        title = text(str(doc.h1 or doc.title or url))
        para = doc.select_one("main p") or doc.select_one("p")
        excerpt = text(str(para))[:190] if para else ""
        by_url[url] = {"title": title, "url": url, "excerpt": excerpt}
    # Portail encyclopédique autonome (HTML racine, sans réécriture des sources).
    greek_portal = OUT / "mythologie-grecque.html"
    if greek_portal.is_file():
        by_url["/mythologie-grecque.html"] = {
            "title": "Encyclopédie mythologique grecque — corpus et sommaire général",
            "url": "/mythologie-grecque.html",
            "excerpt": "Entrée unique : chapitres universitaires grecs, dieux, héros, cosmogonies, cycles mythologiques, archives et analyses philosophiques."
        }
    # Les anciens index peuvent déjà contenir des alias de dossiers. Filtrer
    # toutes les entrées, pas seulement les nouvelles pages HTML autonomes.
    # Les fichiers de redirection eux-mêmes restent intacts et accessibles.
    for url in list(by_url):
        page = OUT / url.lstrip('/')
        if page.is_dir():
            page = page / 'index.html'
        if not page.is_file():
            continue
        head = re.split(r'</head\s*>', page.read_text(encoding='utf-8'),
                        maxsplit=1, flags=re.I)[0]
        doc = BeautifulSoup(head, 'html.parser')
        if any(str(meta.get('http-equiv', '')).strip().lower() == 'refresh'
               for meta in doc.find_all('meta')):
            del by_url[url]
    if len(by_url)<450:
        raise RuntimeError("Protection : moins de 450 pages indexées")
    entries=sorted(by_url.values(),key=lambda e:e["title"].casefold())
    write("search.json",json.dumps(entries,ensure_ascii=False,separators=(",",":")))
    listing='<ul class="listing">'+''.join('<li><a href="'+html.escape(e["url"],quote=True)+'">'+html.escape(e["title"])+'</a></li>' for e in entries)+'</ul>'
    write("rubriques/index.html",render("Tous les dossiers","<h1>Tous les dossiers</h1><p>"+str(len(entries))+" dossiers publics indexés.</p>"+listing))
    urls=["/"]+[e["url"] for e in entries]+["/recherche/","/rubriques/"]
    # Des adresses historiques restent disponibles dans le catalogue sans
    # concurrencer leur page canonique dans le sitemap des moteurs de recherche.
    # Ne jamais supprimer la page ni son texte lors de cette déduplication.
    sitemap_urls=[]
    for url in sorted(set(urls)):
        # Les doublons historiques sont principalement des fichiers .html ;
        # la Grande Encyclopédie est la seule ancienne entrée en répertoire.
        if url.endswith(".html") or url == "/grande-encyclopedie/":
            page=OUT/url.lstrip("/")
            if page.is_dir():
                page=page/"index.html"
            if page.is_file():
                head=re.split(r"</head\s*>",page.read_text(encoding="utf-8"),
                              maxsplit=1,flags=re.I)[0]
                doc=BeautifulSoup(head,"html.parser")
                canonical=doc.select_one('link[rel~="canonical"]')
                if canonical and canonical.get("href"):
                    parsed=urlsplit(canonical["href"])
                    if (parsed.netloc.lower() in ("bobmythos.fr","www.bobmythos.fr")
                            and (parsed.path.rstrip("/") or "/") != (url.rstrip("/") or "/")):
                        continue
        sitemap_urls.append(url)
    write("sitemap.xml",'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
          "\n".join("<url><loc>"+xml_escape(SITE_URL+u)+"</loc></url>" for u in sitemap_urls)+"\n</urlset>\n")
    write("robots.txt","User-agent: *\nAllow: /\nSitemap: "+SITE_URL+"/sitemap.xml\n")
    return len(entries)


def decorate_editorial_pages():
    """Distribute documented figures within studies and retain complementary galleries."""
    from editorial_illustrations import decorate_pages
    return decorate_pages(OUT)

def main():
    # Validate source numbering before touching the publishable directory.
    from editorial_queue import validate
    validate(ROOT)
    from editorial_numbering import scan, finish
    numbered_collections = scan(ROOT)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    n_pages,n_media=copy_repository()
    from sync_reconstitution_index import sync_index
    print('Sommaire 3D :', sync_index(OUT), 'vignettes ajoutées')
    chapters=publish_chapters()
    numbered_titles = {e['url']: e['title'] for items in numbered_collections.values() for e in items}
    for entry in chapters:
        if entry['url'] in numbered_titles:
            entry['title'] = numbered_titles[entry['url']]
    from comparative_history import annotate as annotate_history
    annotate_history(ROOT, numbered_collections, chapters)
    # Réconciliation explicite de deux collisions documentées, sans réécrire les sources.
    import build_navigation as navigation
    from origines_reconciliation import install, verify_sources
    protected_sources=install(navigation, chapters)
    n_indexed=reindex(chapters)
    # Construire les portails géographiques et thématiques avant la seconde indexation.
    navigation.build_portals()
    n_indexed=reindex(chapters)
    # Sommaire unique MG : reconstruit à chaque publication depuis les manuscrits présents.
    from build_greek_corpus import main as build_greek_corpus
    greek_stats = build_greek_corpus(OUT, ROOT)
    print("MYTHOS — Corpus mythologique grec réuni :", greek_stats)
    # Raccorder durablement la galerie photoréaliste du dépôt projet au portail principal.
    atlas_page = OUT / "reconstitutions-antiquite" / "index.html"
    if atlas_page.is_file():
        atlas_doc = BeautifulSoup(atlas_page.read_text(encoding="utf-8"), "html.parser")
        intro = atlas_doc.select_one("p.portal-lead")
        href = "/reconstitutions-photorealistes.html"
        changed = False
        for old_link in atlas_doc.select('a[href="/Mythos/reconstitutions-photorealistes.html"]'):
            old_link["href"] = href
            changed = True
        if intro and not atlas_doc.select_one('a[href="' + href + '"]'):
            link_block = atlas_doc.new_tag("p", attrs={"class": "mythos-photorealistic-link"})
            link = atlas_doc.new_tag("a", href=href)
            link.string = "Reconstitutions 3D photoréalistes publiées — consulter les images, sources et degrés de certitude"
            link_block.append(link)
            intro.insert_after(link_block)
            changed = True
        if changed:
            atlas_page.write_text(str(atlas_doc), encoding="utf-8")
    # Ancienne adresse de catalogue encore utilisée par des archives conservées.
    write("catalogue/index.html", '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/rubriques/"><link rel="canonical" href="https://bobmythos.fr/rubriques/"><title>Catalogue MYTHOS</title></head><body><p><a href="/rubriques/">Accéder au catalogue MYTHOS</a></p></body></html>')
    numbering = finish(OUT, ROOT, numbered_collections)
    from improve_reading import prepare, enhance, audit
    prepare(OUT, ROOT)
    from comparative_history import install as install_history
    install_history(ROOT, OUT)
    n_indexed = reindex(chapters)
    navigation.finalize_navigation(n_indexed)
    print("Numérotation vérifiée :", numbering["renumbered_studies"], "études réconciliées ;", numbering["corrected_links"], "liens harmonisés")
    n_illustrated = decorate_editorial_pages()
    from apply_museum_design import apply as apply_museum_design
    n_styled = apply_museum_design(OUT)
    print(f"Identité muséale commune : {n_styled} pages HTML.")
    enhance(OUT, ROOT)
    from improve_reading import install_civilisation_reciprocal_navigation
    install_civilisation_reciprocal_navigation(OUT, ROOT)
    # Raccorder neuf dossiers critiques déjà intégraux, sans copier ni attribuer
    # de volumes et sans confondre scènes contemporaines et témoins antiques.
    from theatre_fragment_index import install as install_theatre_fragment_index
    print('Théâtre — éditions fragmentaires documentées :',
          install_theatre_fragment_index(ROOT, OUT))
    # Ce panneau est bâti uniquement sur les allocations reçues et les pages
    # intégrales du rendu ; aucune nouvelle cote ni copie d'étude n'est créée.
    from recent_studies import install as install_recent_studies
    print('Accueil — dernières études attribuées :', install_recent_studies(ROOT, OUT))
    from build_reading_pdfs import build as build_reading_pdfs
    build_reading_pdfs(OUT)
    verify_sources(protected_sources)
    from verify_publication import verify as verify_publication
    verify_publication(ROOT, OUT)
    audit(OUT)
    print(f"Images documentées et reconstitutions sourcées réparties dans ou après {n_illustrated} articles.")
    write(".nojekyll","")
    write("CNAME","bobmythos.fr\n")
    print(f"MYTHOS SANS WORDPRESS : {n_pages} HTML de GitHub, {n_media} médias locaux, {len(chapters)} nouveaux chapitres Markdown, {n_indexed} dossiers indexés.")
    print("Pas de réseau, pas d'API WordPress, pas de publication de brouillons.")

if __name__=="__main__":
    main()
