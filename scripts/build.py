#!/usr/bin/env python3
"""MYTHOS : copie publique statique de WordPress.com pour GitHub Pages.
Les brouillons restent dans l'archive privée. Les médias publics sont auto-hébergés par pin_media.py.
"""
import html
import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from bs4 import BeautifulSoup
import mistune

API = os.environ.get("WP_API", "https://public-api.wordpress.com/wp/v2/sites/bobmythos.wordpress.com").rstrip("/")
SITE_URL = os.environ.get("SITE_URL", "https://bobcribb.github.io").rstrip("/")
OUT = Path(os.environ.get("OUT_DIR", "_site"))
MIN_PAGES = int(os.environ.get("MIN_PAGES", "400"))
SOURCE_HOSTS = {"bobmythos.fr", "www.bobmythos.fr", "bobmythos.wordpress.com"}
markdown = mistune.create_markdown(escape=False, plugins=["table", "strikethrough", "url"])

def fetch_json(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "MYTHOS-public-static-archive/1.0",
                              "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.load(response)
        except (urllib.error.URLError, ValueError, TimeoutError) as exc:
            if attempt == 4:
                raise RuntimeError("WordPress API indisponible: " + url) from exc
            time.sleep(min(2 ** attempt, 15))

def get_items(collection):
    items = []
    for page in range(1, 51):
        query = urllib.parse.urlencode({
            "per_page": 100, "page": page, "status": "publish",
            "_fields": "id,status,link,title,content,parent,modified,excerpt,slug"
        })
        batch = fetch_json(API + "/" + collection + "?" + query)
        if not isinstance(batch, list):
            raise RuntimeError("Réponse API inattendue pour " + collection)
        items += batch
        print(collection, "lot", page, "total", len(items), flush=True)
        if len(batch) < 100:
            return items
    raise RuntimeError("Trop de pages API : pagination interrompue par précaution")

def plain(text):
    return re.sub(r"\s+", " ", BeautifulSoup(text or "", "html.parser").get_text(" ", strip=True)).strip()

def escaped(text):
    return html.escape(str(text), quote=True)

def page_path(item):
    source = urllib.parse.urlparse(item.get("link") or "")
    path = urllib.parse.unquote(source.path or "/")
    path = re.sub(r"/+", "/", path)
    parts = [p for p in path.split("/") if p]
    if any(p in (".", "..") for p in parts):
        raise RuntimeError("Chemin interdit dans l'API")
    return "/" + "/".join(parts) + "/" if parts else "/"

def rewrite_html(raw):
    raw = raw or ""
    if re.search(r"(?m)^\s{0,3}#{1,6}\s+", raw) and raw.count("<p") < 3:
        raw = markdown(raw)
    # Les assets restent sur WordPress.com : le domaine personnalisé va changer de serveur.
    for source in ("https://bobmythos.fr", "https://www.bobmythos.fr",
                   "http://bobmythos.fr", "http://www.bobmythos.fr"):
        raw = raw.replace(source + "/wp-content/uploads/",
                          "https://bobmythos.wordpress.com/wp-content/uploads/")
    # Localiser toutes les images et tous les PDF sur GitHub Pages.
    # Les variantes WordPress ?w=... deviennent la même image originale locale.
    raw = raw.replace(
        "https://i0.wp.com/bobmythos.wordpress.com/wp-content/uploads/",
        "https://bobmythos.wordpress.com/wp-content/uploads/")
    # Convertir uniquement les médias de MYTHOS. Beaucoup de documents
    # universitaires externes utilisent aussi /wp-content/uploads/ :
    # leur domaine et leur URL doivent absolument être préservés.
    media_re = re.compile(
        r"(?:https?:)?//(?:bobmythos\.wordpress\.com|(?:www\.)?bobmythos\.fr)"
        r"/wp-content/uploads/((?:20\d{2})/(?:0[1-9]|1[0-2])/[A-Za-z0-9._~%+\-]+)",
        re.IGNORECASE)
    raw = media_re.sub(lambda m: "/media/" + m.group(1), raw)
    relative_media_re = re.compile(
        r"(?<![A-Za-z0-9._-])/wp-content/uploads/"
        r"((?:20\d{2})/(?:0[1-9]|1[0-2])/[A-Za-z0-9._~%+\-]+)",
        re.IGNORECASE)
    raw = relative_media_re.sub(lambda m: "/media/" + m.group(1), raw)
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup.find_all(["script", "iframe", "form"]):
        tag.decompose()
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.lower().startswith("on"):
                del tag[attr]
        for attr in ("href", "src", "poster", "data-src"):
            if not tag.has_attr(attr):
                continue
            url = str(tag[attr])
            u = urllib.parse.urlparse(url)
            if u.path.startswith("/wp-content/uploads/") and (
                    not u.hostname or u.hostname.lower() in SOURCE_HOSTS):
                tag[attr] = "https://bobmythos.wordpress.com" + u.path + (
                    "?" + u.query if u.query else "") + (
                    "#" + u.fragment if u.fragment else "")
            elif attr == "href" and u.hostname and u.hostname.lower() in SOURCE_HOSTS:
                tag[attr] = (u.path or "/") + (
                    "?" + u.query if u.query else "") + (
                    "#" + u.fragment if u.fragment else "")
        if tag.has_attr("srcset"):
            # Une liste srcset peut contenir des variantes ?w=... ;
            # on ne modifie que le domaine, pas les tailles.
            tag["srcset"] = str(tag["srcset"]).replace(
                "https://bobmythos.fr/wp-content/uploads/",
                "https://bobmythos.wordpress.com/wp-content/uploads/").replace(
                "https://www.bobmythos.fr/wp-content/uploads/",
                "https://bobmythos.wordpress.com/wp-content/uploads/")
    return str(soup)

def layout(title, body, summary="", sidebar="", home=False):
    heading = "" if home else '<div class="eyebrow">BIBLIOTHÈQUE · MYTHOS</div><h1>' + escaped(plain(title)) + "</h1>"
    desc = escaped(summary or "Encyclopédie des mythes, religions, civilisations antiques et philosophie.")
    return '''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark"><meta name="description" content="''' + desc[:240] + '''">
<title>''' + escaped(plain(title)) + ''' | MYTHOS</title>
<link rel="stylesheet" href="/assets/style.css"></head><body>
<header class="masthead"><div class="masthead-inner">
<a class="brand" href="/">MYTHOS <span>✦</span></a>
<nav><a href="/">Accueil</a><a href="/rubriques/">Dossiers</a><a href="/recherche/">Recherche</a></nav>
</div></header><main class="layout"><article class="content">''' + heading + body + '''</article>''' + sidebar + '''</main>
<footer class="footer"><span>MYTHOS — Encyclopédie universitaire comparative</span>
<a href="/rubriques/">Tous les dossiers</a></footer><script defer src="/assets/search.js"></script>
</body></html>'''

def write(path, contents):
    target = OUT / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.resolve().is_relative_to(OUT.resolve()):
        raise RuntimeError("Chemin de sortie interdit: " + path)
    target.write_text(contents, encoding="utf-8")

def main():
    pages = get_items("pages")
    posts = get_items("posts")
    if len(pages) < MIN_PAGES:
        raise RuntimeError("Protection : seulement " + str(len(pages)) + " pages ; " + str(MIN_PAGES) + " attendues. Déploiement bloqué.")
    items, seen = [], set()
    for kind, batch in (("page", pages), ("post", posts)):
        for item in batch:
            if item.get("status") != "publish":
                continue
            path = page_path(item)
            if path in seen:
                print("URL en doublon ignorée:", path, file=sys.stderr)
                continue
            seen.add(path)
            item["_path"], item["_kind"] = path, kind
            items.append(item)
    if not items:
        raise RuntimeError("Aucun dossier public")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    for src in ("style.css", "search.js"):
        write("/assets/" + src, (Path(__file__).parent.parent / "assets" / src).read_text(encoding="utf-8"))
    write("/.nojekyll", "")
    by_id = {p["id"]: p for p in pages}
    roots = [p for p in items if p["_kind"] == "page" and not (p.get("parent") in by_id)]
    roots.sort(key=lambda x: plain(x["title"].get("rendered", "")).casefold())
    side = '<aside class="sidebar"><b>Explorer MYTHOS</b>' + "".join(
        '<a href="' + escaped(p["_path"]) + '">' + escaped(plain(p["title"].get("rendered", ""))) + '</a>'
        for p in roots[:20]) + "</aside>"
    manifest = []
    for item in items:
        path = item["_path"]
        if path == "/":
            continue
        title = item.get("title", {}).get("rendered", "Dossier sans titre")
        excerpt = plain(item.get("excerpt", {}).get("rendered", ""))[:190]
        body = rewrite_html(item.get("content", {}).get("rendered", ""))
        write(path + "index.html", layout(title, body, excerpt, side))
        manifest.append({"title": plain(title), "url": path, "excerpt": excerpt})
    manifest.sort(key=lambda p: p["title"].casefold())
    write("/search.json", json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
    cards = "".join(
        '<div class="card"><small>RUBRIQUE</small><a href="' + escaped(p["_path"]) + '">' +
        escaped(plain(p["title"].get("rendered", ""))) + "</a></div>" for p in roots[:24])
    home = ('<div class="hero"><small>MYTHES · HISTOIRE · RELIGIONS · PHILOSOPHIE</small><h1>MYTHOS</h1>'
            '<div class="gold-line"></div><p>Une encyclopédie des dieux, des héros et des civilisations, '
            'de la Grèce antique aux traditions du monde.</p></div>'
            '<h2>Explorer les civilisations et les œuvres</h2><div class="cards">' + cards + '</div>'
            '<h2>Rechercher parmi ' + str(len(manifest)) + ' dossiers</h2>'
            '<input class="search" data-search placeholder="Rechercher un dieu, une œuvre, un auteur…" aria-label="Rechercher">'
            '<div data-results class="results"></div>')
    write("/index.html", layout("Accueil", home, home=True))
    search = ('<p>Recherche parmi les dossiers publics de MYTHOS.</p>'
              '<input class="search" data-search placeholder="Saisir un mot…" aria-label="Rechercher">'
              '<div data-results class="results"></div>')
    write("/recherche/index.html", layout("Recherche", search, sidebar=side))
    listing = "".join('<li><a href="' + escaped(p["url"]) + '">' + escaped(p["title"]) + '</a></li>' for p in manifest)
    write("/rubriques/index.html", layout("Tous les dossiers",
        '<p>' + str(len(manifest)) + ' dossiers publics indexés.</p><ul class="listing">' + listing + '</ul>', sidebar=side))
    write("/404.html", layout("Page introuvable",
        '<p>Cette page est absente du catalogue.</p><p><a href="/recherche/">Chercher un dossier</a></p>'))
    sm = ['<?xml version="1.0" encoding="utf-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm.append('<url><loc>' + xml_escape(SITE_URL + "/") + '</loc></url>')
    for p in items:
        sm.append('<url><loc>' + xml_escape(SITE_URL + p["_path"]) + '</loc></url>')
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm))
    write("/robots.txt", "User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml\n")
    print("MYTHOS généré :", len(pages), "pages,", len(posts), "articles,", len(manifest), "URL.")
    print("Médias réécrits vers /media (pin_media.py). Brouillons non publiés.")

if __name__ == "__main__":
    main()
