#!/usr/bin/env python3
"""Non-mutating MYTHOS full-site snapshot for urgent photorealistic-gallery deployments."""
from pathlib import Path
import hashlib, json, os, shutil, sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"_site"
EXCLUDE={".git",".github","_site","scripts","tests","editorial","docs",".venv","node_modules","__pycache__",".pytest_cache"}
EXTS={".html",".css",".js",".json",".svg",".webp",".jpeg",".jpg",".png",".gif",".ico",".xml",".pdf",".woff",".woff2",".webm",".mp4",".mp3",".ogg",".wav",".webmanifest"}
SPECIAL={".nojekyll","CNAME","robots.txt","sitemap.xml","search.json"}

def included(rel):
    if rel.parts[0] in EXCLUDE or any(p.startswith(".") for p in rel.parts[:-1]):
        return False
    if len(rel.parts)==1 and rel.name in SPECIAL:
        return True
    if rel.parts[0]=="corpus" and rel.suffix.lower()==".md":
        return True
    return rel.suffix.lower() in EXTS

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    copies=0
    for directory,subdirs,files in os.walk(ROOT):
        base=Path(directory)
        subdirs[:]=[d for d in subdirs if d not in EXCLUDE and not d.startswith(".")]
        for name in files:
            rel=base.relative_to(ROOT)/name
            if not included(rel): continue
            source=ROOT/rel
            if not source.is_file() or source.is_symlink(): continue
            dest=OUT/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,dest)
            copies+=1
    gallery=(OUT/"reconstitutions-photorealistes.html").read_text(encoding="utf-8")
    catalogue=json.loads((OUT/"assets/reconstitutions-3d/catalogue-photorealiste.json").read_text(encoding="utf-8"))
    items=catalogue["entries"]
    if len(items)!=catalogue.get("count") or len({i["slug"] for i in items})!=len(items):
        raise RuntimeError("Numérotation de galerie ou nombre d'images incohérent")
    for image in items:
        src=image["src"]
        if not src.startswith("/assets/reconstitutions-3d/") or not src.endswith(".webp"):
            raise RuntimeError("Chemin invalide : "+src)
        dest=OUT/src.lstrip("/")
        if not dest.is_file() or dest.stat().st_size<10000: raise RuntimeError("WebP manquant : "+src)
        content=dest.read_bytes()
        if not (content[:4]==b"RIFF" and content[8:12]==b"WEBP"):
            raise RuntimeError("Image non WebP : "+src)
        if image.get("sha256") and hashlib.sha256(content).hexdigest()!=image["sha256"]:
            raise RuntimeError("Image modifiée : "+src)
        if src not in gallery or ('id="'+image["slug"]+'"') not in gallery:
            raise RuntimeError("Fiche de galerie manquante : "+src)
        if not image.get("source_url","").startswith("https://"):
            raise RuntimeError("Source archéologique absente : "+src)
    if (OUT/"CNAME").read_text().strip()!="bobmythos.fr":
        raise RuntimeError("Domaine MYTHOS manquant")
    pages=list(OUT.rglob("index.html"))
    if len(pages)<1000: raise RuntimeError("Site tronqué : trop peu de pages")
    pdfs=json.loads((OUT/"catalog/reading-pdfs.json").read_text(encoding="utf-8"))
    for item in pdfs:
        f=OUT/item["url"].lstrip("/")
        if not f.is_file() or f.stat().st_size<10000: raise RuntimeError("PDF manquant : "+item["url"])
        if item.get("sha256") and hashlib.sha256(f.read_bytes()).hexdigest()!=item["sha256"]:
            raise RuntimeError("PDF modifié : "+item["url"])
    entries=json.loads((OUT/"catalog/entries.json").read_text(encoding="utf-8"))["entries"]
    for row in entries:
        uri=row["url"]
        target=OUT/uri.lstrip("/")
        if uri.endswith("/"): target=target/"index.html"
        if not target.is_file(): raise RuntimeError("Article public absent : "+uri)
    print(f"MYTHOS : {copies} ressources, {len(pages)} pages, {len(pdfs)} PDF, {len(items)} WebP vérifiés.",flush=True)

if __name__=="__main__":
    try: build()
    except Exception as exc:
        print(f"::error::{exc}",file=sys.stderr)
        raise
