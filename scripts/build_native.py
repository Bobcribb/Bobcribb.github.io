#!/usr/bin/env python3
"""Publie MYTHOS depuis le dépôt GitHub, sans accès à WordPress.

Source de vérité : fichiers HTML existants dans main, médias dans media/,
et nouvelles études Markdown dans chapitres/. Ne publie aucun brouillon.
"""
from pathlib import Path
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
    # Les manuscrits universitaires déjà liés depuis une page publique doivent
    # être consultables, sans rendre publics les autres brouillons Markdown.
    # Seules les sources existantes dans corpus/ et déjà référencées sont copiées.
    linked_sources = set()
    for page in OUT.rglob("*.html"):
        page_html = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for anchor in page_html.find_all("a", href=True):
            link = str(anchor.get("href", ""))
            href = link.split("#", 1)[0].split("?", 1)[0]
            if not href.endswith(".md") or href.startswith(("http:", "https:", "//")):
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
    print(f"Sources Markdown du corpus liées et publiées : {len(linked_sources)}")
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
    soup = BeautifulSoup(html_body, "html.parser")
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
        title=text(str(doc.h1 or doc.title or url))
        para=doc.select_one(".content p") or doc.select_one("p")
        excerpt=text(str(para))[:190] if para else ""
        by_url[url]={"title":title,"url":url,"excerpt":excerpt}
    # Les lecteurs universitaires HTML du corpus ne s'appellent pas toujours
    # index.html : les rendre trouvables dans la recherche et le sitemap.
    for p in (OUT / "corpus").rglob("*.html"):
        if p.name == "index.html":
            continue
        url = "/" + p.relative_to(OUT).as_posix()
        if url in by_url or url in historical_aliases:
            continue
        doc = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
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
    if len(by_url)<450:
        raise RuntimeError("Protection : moins de 450 pages indexées")
    entries=sorted(by_url.values(),key=lambda e:e["title"].casefold())
    write("search.json",json.dumps(entries,ensure_ascii=False,separators=(",",":")))
    listing='<ul class="listing">'+''.join('<li><a href="'+html.escape(e["url"],quote=True)+'">'+html.escape(e["title"])+'</a></li>' for e in entries)+'</ul>'
    write("rubriques/index.html",render("Tous les dossiers","<h1>Tous les dossiers</h1><p>"+str(len(entries))+" dossiers publics indexés.</p>"+listing))
    urls=["/"]+[e["url"] for e in entries]+["/recherche/","/rubriques/"]
    write("sitemap.xml",'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
          "\n".join("<url><loc>"+xml_escape(SITE_URL+u)+"</loc></url>" for u in sorted(set(urls)))+"\n</urlset>\n")
    write("robots.txt","User-agent: *\nAllow: /\nSitemap: "+SITE_URL+"/sitemap.xml\n")
    return len(entries)


def decorate_editorial_pages():
    """Add contextual illustrated sidebars to existing public pages without changing articles."""
    media_root = OUT / "media" / "2026" / "10"
    groups = {
        "theatre": [("mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg", "Masques de théâtre hellénistiques"), ("antigone-libation-rinehart-1870.jpg", "Antigone, interprétation artistique moderne")],
        "philosophie": [("jacques-louis-david-mort-de-socrate-1787.jpg", "La Mort de Socrate, Jacques-Louis David"), ("mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg", "Papyrus de Derveni")],
        "origines": [("mythos-derveni-papyrus-fragments-thessalonique-gts-tg.jpg", "Papyrus de Derveni"), ("mythos-derveni-cratere-dionysos-menade-carole-raddato.jpg", "Cratère de Derveni")],
        "grece": [("mythos-bronze-artemision-zeus-ou-poseidon.jpg", "Bronze du cap Artémision, attribution discutée"), ("delphes-temple-apollon-bernard-gagnon.jpg", "Temple d’Apollon à Delphes")],
        "monde": [("mythos-papyrus-ani-pesee-coeur-british-museum.jpg", "Égypte, papyrus d’Ani"), ("mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg", "Mésopotamie, Enūma eliš")],
    }
    updated = 0
    for page in OUT.rglob("index.html"):
        if page.relative_to(OUT).parts[0] in ("rubriques", "recherche"):
            continue
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        main = doc.select_one("main.layout")
        article = main.select_one("article.content") if main else None
        if not article:
            continue
        if not doc.select_one('link[href="/assets/mythos-refonte.css"]') and doc.head:
            doc.head.append(doc.new_tag("link", rel="stylesheet", href="/assets/mythos-refonte.css"))
        if main.select_one(".mythos-home-illustrations"):
            page.write_text(str(doc), encoding="utf-8")
            continue
        url = "/" + "/".join(page.relative_to(OUT).parts[:-1]) + "/"
        if "traged" in url or "comed" in url or "/theatre/" in url:
            group = "theatre"
        elif "philosoph" in url or "/comparatif/" in url:
            group = "philosophie"
        elif "origines-du-sacre" in url:
            group = "origines"
        elif any(x in url for x in ("grece", "dieu-", "heros-", "delphes", "athen", "olymp", "chapitres/encyclopedie")):
            group = "grece"
        else:
            group = "monde"
        aside = doc.new_tag("aside", attrs={"class": "mythos-home-illustrations", "aria-label": "Documents iconographiques"})
        heading = doc.new_tag("h2")
        heading.string = "Regards sur les œuvres"
        aside.append(heading)
        for filename, caption in groups[group]:
            if not (media_root / filename).is_file():
                continue
            figure = doc.new_tag("figure")
            figure.append(doc.new_tag("img", src="/media/2026/10/" + filename, alt=caption, loading="lazy"))
            figcaption = doc.new_tag("figcaption")
            figcaption.string = caption
            figure.append(figcaption)
            aside.append(figure)
        if not aside.find("figure"):
            continue
        main["class"] = list(dict.fromkeys(main.get("class", []) + ["portal-layout"]))
        article.insert_after(aside)
        page.write_text(str(doc), encoding="utf-8")
        updated += 1
    return updated

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
    chapters=publish_chapters()
    numbered_titles = {e['url']: e['title'] for items in numbered_collections.values() for e in items}
    for entry in chapters:
        if entry['url'] in numbered_titles:
            entry['title'] = numbered_titles[entry['url']]
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
    n_indexed = reindex(chapters)
    navigation.finalize_navigation(n_indexed)
    print("Numérotation vérifiée :", numbering["renumbered_studies"], "études réconciliées ;", numbering["corrected_links"], "liens harmonisés")
    n_illustrated = decorate_editorial_pages()
    from apply_museum_design import apply as apply_museum_design
    n_styled = apply_museum_design(OUT)
    print(f"Identité muséale commune : {n_styled} pages HTML.")
    verify_sources(protected_sources)
    print(f"Galeries latérales ajoutées sur {n_illustrated} pages.")
    write(".nojekyll","")
    write("CNAME","bobmythos.fr\n")
    print(f"MYTHOS SANS WORDPRESS : {n_pages} HTML de GitHub, {n_media} médias locaux, {len(chapters)} nouveaux chapitres Markdown, {n_indexed} dossiers indexés.")
    print("Pas de réseau, pas d'API WordPress, pas de publication de brouillons.")

if __name__=="__main__":
    main()
