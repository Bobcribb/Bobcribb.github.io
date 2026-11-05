#!/usr/bin/env python3
"""Read-only integrity audit for the autonomous MYTHOS website.

Run after scripts/build_native.py to inspect the publishable _site/
and compare it to versioned public source content.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from collections import Counter
from hashlib import sha256
import json, re, sys
from sitemap_integrity import canonical_target
from audit_policy import publication_audit_fails

out=Path("_site")
manifest=json.loads((out/"media/manifest.json").read_text(encoding="utf-8"))
catalogue=json.loads((out/"search.json").read_text(encoding="utf-8"))
pages=list(out.rglob("*.html"))
styles=[out/"assets/style.css",out/"assets/search.js",out/"CNAME",out/"index.html",out/"rubriques/index.html",out/"recherche/index.html"]
issues=[];warnings=[];stats=Counter()
for f in styles:
    if not f.is_file():
        issues.append("File missing: "+str(f))
expected=set(entry["url"] for entry in catalogue)
if len(expected)!=len(catalogue): issues.append("Duplicate URLs in search catalogue")
for entry in catalogue:
    url=entry["url"]
    candidate=out / url.lstrip("/")
    # Une URL peut viser un fichier .html autonome ou un dossier /index.html.
    f=candidate if candidate.is_file() else candidate / "index.html"
    if not f.is_file(): issues.append("Indexed page missing: "+url)
if len(catalogue)<500: issues.append("Fewer than 500 indexed dossiers")
if manifest["count"]!=110 or len(manifest["files"])!=110: issues.append("Media manifest not 110")
for entry in manifest["files"]:
    target=out/entry["path"]
    if not target.is_file():
        issues.append("Media missing: "+entry["path"]);continue
    body=target.read_bytes()
    if len(body)!=entry["size"] or sha256(body).hexdigest()!=entry["sha256"]:
        issues.append("Media size/hash differs: "+entry["path"])
    stats["media_checked"]+=1
    stats["media_bytes"]+=len(body)
if (out/"CNAME").read_text().strip()!="bobmythos.fr": issues.append("Wrong CNAME")
sitemap=(out/"sitemap.xml").read_text()
sitemap_urls=set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
for path in expected:
    public_url="https://bobmythos.fr"+path
    if public_url in sitemap_urls:
        continue
    # Conserver les lecteurs historiques dans la recherche, tout en excluant
    # du sitemap les URL non canoniques. La destination DOIT être indexée et
    # l'archive HTML source DOIT toujours exister sur le disque.
    canonical=canonical_target(out, path)
    if canonical and canonical != public_url and canonical in sitemap_urls:
        stats["historical_canonical_aliases"] += 1
        continue
    issues.append("Sitemap missing: "+path)
stats["indexed"]=len(catalogue)
stats["html_files"]=len(pages)
page_ids = {}
fragment_links = []
for file in pages:
    html=file.read_text(encoding="utf-8")
    soup=BeautifulSoup(html,"html.parser")
    ids = [str(node["id"]) for node in soup.select("[id]")]
    page_ids[file.resolve()] = set(ids) | {str(node["name"]) for node in soup.select("a[name]")}
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        warnings.append("Duplicate HTML IDs: " + str(file) + " => " + ", ".join(duplicates))
    if not soup.find("title"):warnings.append("Missing title: "+str(file))
    stats["html_kb"]+=len(html)//1024
    attr_urls=[]
    for e in soup.select("[href],[src],[poster],[data-src],[srcset]"):
        for a in ("href","src","poster","data-src"):
            if e.has_attr(a):attr_urls.append((a,str(e[a])))
        if e.has_attr("srcset"):
            attr_urls.extend(("srcset", z.strip().split(" ")[0]) for z in str(e["srcset"]).split(","))
    stats["html_urls"]+=len(attr_urls)
    for attr,url in attr_urls:
        if not url or url.startswith(("mailto:","tel:","data:","javascript:")): continue
        full=urlparse(url)
        if full.hostname and full.hostname not in ("bobmythos.fr","www.bobmythos.fr","bobmythos.wordpress.com"):
            stats["external_url"]+=1;continue
        if full.hostname=="bobmythos.wordpress.com":
            if "/wp-content/uploads/" in full.path:
                warnings.append("WordPress-dependent media URL in "+str(file)+": "+url[:120])
            continue
        if not full.path:
            target=file
        elif not full.path.startswith("/"):
            # relative URLs resolved relative to current page
            target=(file.parent / unquote(full.path))
        else:
            target=(out / unquote(full.path.lstrip("/")))
        if target.is_dir(): target=target/"index.html"
        elif target.suffix=="" and not target.exists(): target=target/"index.html"
        try:
            relative=target.resolve().relative_to(out.resolve())
        except ValueError:
            warnings.append("Unsafe or malformed relative URL: "+str(file)+" => "+url[:100])
            continue
        if not target.is_file():
            # Report internal missing links without halting the existing public site.
            warnings.append("Broken internal "+attr+" from "+str(file)+": "+url[:180])
        else:
            stats["local_links_checked"]+=1
            if full.fragment and target.suffix.lower() == ".html":
                # This particular archived JavaScript library uses #/accueil
                # and similar hash-router states, not HTML element anchors.
                # Check ordinary fragments normally, including missing ones.
                spa_route = (target.name == "MYTHOS_bibliotheque_navigable.html"
                             and full.fragment.startswith("/"))
                if spa_route:
                    stats["spa_routes_checked"] += 1
                else:
                    fragment_links.append((file, target.resolve(), unquote(full.fragment), url))
    stats["pages_scanned"]+=1

for source, target, fragment, url in fragment_links:
    if fragment not in page_ids.get(target, set()):
        warnings.append("Broken internal fragment: " + str(source) + " => " + url)
    else:
        stats["fragment_links_checked"] += 1

print("=== MYTHOS AUTOMATED INTEGRITY AUDIT ===")
print(json.dumps(dict(stats),ensure_ascii=False,indent=2))
print("HARD ERRORS: ",len(issues))
for i in issues[:45]:print("ERROR:",i)
print("WARNINGS:",len(warnings))
print("WARNINGS_BY_TYPE:",dict(Counter(w.split(":")[0] for w in warnings)))
for i in warnings[:65]:print("WARNING:",i)
# Un lien interne, une ancre, un média, un CSS/JS, un doublon d'identifiant,
# un titre manquant ou une dépendance WordPress ne doivent jamais laisser la CI verte.
# Chaque avertissement correspond déjà à un constat contrôlé par cet auditeur.
if publication_audit_fails(issues, warnings):
    print("Publication blocked by integrity errors/warnings.", file=sys.stderr)
    sys.exit(1)
print("Core integrity: PASS. No broken links, fragments or resources detected.")
