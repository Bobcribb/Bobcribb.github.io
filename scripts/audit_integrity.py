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

out=Path("_site")
manifest=json.loads((out/"media/manifest.json").read_text(encoding="utf-8"))
catalogue=json.loads((out/"search.json").read_text(encoding="utf-8"))
pages=list(out.rglob("index.html"))
styles=[out/"assets/style.css",out/"assets/search.js",out/"CNAME",out/"index.html",out/"rubriques/index.html",out/"recherche/index.html"]
issues=[];warnings=[];stats=Counter()
for f in styles:
    if not f.is_file():
        issues.append("File missing: "+str(f))
expected=set(entry["url"] for entry in catalogue)
if len(expected)!=len(catalogue): issues.append("Duplicate URLs in search catalogue")
for entry in catalogue:
    url=entry["url"]
    f=out / url.lstrip("/") / "index.html"
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
for path in expected:
    if "https://bobmythos.fr"+path not in sitemap: issues.append("Sitemap missing: "+path)
stats["indexed"]=len(catalogue)
stats["html_files"]=len(pages)
for file in pages:
    html=file.read_text(encoding="utf-8")
    soup=BeautifulSoup(html,"html.parser")
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
        if not url or url.startswith(("mailto:","tel:","data:","javascript:","#")): continue
        full=urlparse(url)
        if full.hostname and full.hostname not in ("bobmythos.fr","www.bobmythos.fr","bobmythos.wordpress.com"):
            stats["external_url"]+=1;continue
        if full.hostname=="bobmythos.wordpress.com":
            if "/wp-content/uploads/" in full.path:
                warnings.append("WordPress-dependent media URL in "+str(file)+": "+url[:120])
            continue
        if not full.path.startswith("/"):
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
    stats["pages_scanned"]+=1

print("=== MYTHOS AUTOMATED INTEGRITY AUDIT ===")
print(json.dumps(dict(stats),ensure_ascii=False,indent=2))
print("HARD ERRORS: ",len(issues))
for i in issues[:45]:print("ERROR:",i)
print("WARNINGS:",len(warnings))
print("WARNINGS_BY_TYPE:",dict(Counter(w.split(":")[0] for w in warnings)))
for i in warnings[:65]:print("WARNING:",i)
if len(issues):
    sys.exit(1)
print("Core integrity: PASS. Broken links are reported as warnings for editorial follow-up.")
