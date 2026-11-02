#!/usr/bin/env python3
"""Archive les fichiers publics de la médiathèque WordPress MYTHOS.
Les fichiers sont copiés en lecture seule, avec somme SHA256 et manifeste.
N'exporte pas les brouillons ni les pages privées.
"""
import hashlib
import json
import os
import pathlib
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

API="https://public-api.wordpress.com/wp/v2/sites/bobmythos.wordpress.com/media"
ROOT=pathlib.Path("archive")
MEDIA=ROOT/"medias"
ROOT.mkdir(parents=True,exist_ok=True)
MEDIA.mkdir(parents=True,exist_ok=True)

def grab(url,tries=5):
    for k in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"MYTHOS-private-backup/1.0", "Accept":"*/*"})
            with urllib.request.urlopen(req,timeout=100) as r:
                return r.read(),r.headers.get("content-type","")
        except (urllib.error.URLError,TimeoutError) as exc:
            if k==tries-1:
                raise RuntimeError("Échec de récupération: "+url) from exc
            time.sleep(min(3*(k+1),16))

items=[]
for page in range(1,20):
    query=urllib.parse.urlencode({"per_page":100,"page":page})
    raw,ctype=grab(API+"?"+query)
    batch=json.loads(raw)
    if not isinstance(batch,list):
        raise RuntimeError("Réponse media API non valide")
    items.extend(batch)
    print("Médiathèque page",page,"nombre:",len(batch),flush=True)
    if len(batch)<100:
        break
if len(items)<100:
    raise RuntimeError(f"Médiathèque incomplète : {len(items)} éléments (minimum 100)")
seen=set()
manifest=[]
for index,item in enumerate(items,1):
    url=item.get("source_url","")
    if not url.startswith("https://bobmythos.wordpress.com/wp-content/uploads/") and not url.startswith("https://bobmythos.fr/wp-content/uploads/"):
        raise RuntimeError("URL de média inattendue : "+str(url))
    id_=int(item["id"])
    if id_ in seen:
        raise RuntimeError("ID média en double")
    seen.add(id_)
    name=pathlib.PurePosixPath(urllib.parse.urlparse(url).path).name
    name=re.sub(r"[^A-Za-z0-9._-]","_",name) or str(id_)
    name=f"{id_:05d}_{name}"
    file_content,ctype=grab(url)
    if not file_content:
        raise RuntimeError("Fichier média vide : "+url)
    mime=item.get("mime_type","")
    if mime.startswith("image/") and not (ctype.startswith("image/") or ctype.startswith("application/octet-stream")):
        raise RuntimeError(f"Réponse inattendue {ctype} pour image {url}")
    if mime=="application/pdf" and not file_content.startswith(b"%PDF"):
        raise RuntimeError("PDF non reconnu : "+url)
    if mime=="image/png" and not file_content.startswith(b"\x89PNG"):
        raise RuntimeError("PNG non reconnu : "+url)
    if mime=="image/jpeg" and not file_content.startswith(b"\xff\xd8"):
        raise RuntimeError("JPEG non reconnu : "+url)
    p=MEDIA/name
    p.write_bytes(file_content)
    manifest.append({
        "id":id_,"original_url":url,"saved_as":str(p.relative_to(ROOT)),
        "mime_type":mime,"bytes":len(file_content),
        "sha256":hashlib.sha256(file_content).hexdigest(),
        "title":item.get("title",{}).get("rendered",""),
        "alt_text":item.get("alt_text",""),
        "wp_expected_filesize":item.get("media_details",{}).get("filesize"),
    })
    if index%10==0:
        print("Copiés:",index,"/",len(items),flush=True)
manifest.sort(key=lambda x:x["id"])
(ROOT/"manifest.json").write_text(json.dumps({
    "origin":"MYTHOS WordPress public media API",
    "captured_at_utc":datetime.now(timezone.utc).isoformat(),
    "count":len(manifest),
    "total_bytes":sum(m["bytes"] for m in manifest),
    "items":manifest,
},ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"README.txt").write_text(
    "MYTHOS - Archive des médias publics de WordPress.com\n"
    "Cette archive ne comprend pas les brouillons privés ni les contenus WordPress.\n"
    "Pour vérifier les fichiers, comparer leurs sommes SHA256 à manifest.json.\n"
    "Ne pas supprimer le site WordPress avant d'avoir vérifié les liens de la version GitHub.\n", encoding="utf-8")
print("SAUVEGARDE TERMINEE",len(manifest),"fichiers,",sum(m["bytes"] for m in manifest),"octets",flush=True)
