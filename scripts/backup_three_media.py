#!/usr/bin/env python3
"""Complete the MYTHOS WordPress media inventory backup.

These three media files are listed by the authorized WordPress connector but
are not referenced in the generated static pages. Archive them, without
publishing the media files or WordPress drafts in the public repository.
"""
import hashlib, json, zipfile, urllib.request, urllib.error, time
from pathlib import Path
from urllib.parse import quote

FILES=[
    (652,"mythos-monogramme-or-noir-512.png","image/png"),
    (651,"mythos-demeter-porcelet-terre-cuite-athenes-cma-1926-521.jpg","image/jpeg"),
    (24,"mythos-e28094-illustration-du-sanctuaire-de-delphes.png","image/png"),
]
OUT=Path("_three_media")
OUT.mkdir(exist_ok=True)
records=[]
for id_, filename, mime in FILES:
    rel="2026/10/"+filename
    url="https://bobmythos.wordpress.com/wp-content/uploads/"+quote(rel,safe="/.-_")
    last=None
    for candidate in [url,"https://i0.wp.com/bobmythos.wordpress.com/wp-content/uploads/"+quote(rel,safe="/.-_")]:
        try:
            req=urllib.request.Request(candidate,headers={"User-Agent":"Mozilla/5.0 (MYTHOS archive)","Accept":"image/jpeg,image/png,image/*;q=0.8,*/*;q=0.6"})
            with urllib.request.urlopen(req, timeout=50) as response:
                blob=response.read(25000000)
                content_type=response.headers.get("Content-Type","")
                if response.read(1):
                    raise ValueError("file exceeds limit")
            if not blob:
                raise ValueError("empty content")
            if mime=="image/png" and not blob.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("not a PNG: "+content_type)
            if mime=="image/jpeg" and not blob.startswith(b"\xff\xd8"):
                raise ValueError("not a JPEG: "+content_type)
            target=OUT/filename
            target.write_bytes(blob)
            records.append({"wordpress_media_id":id_,"filename":filename,"bytes":len(blob),"sha256":hashlib.sha256(blob).hexdigest(),"source":candidate})
            print("SAVED:",filename,len(blob),flush=True)
            last=None
            break
        except Exception as e:
            last=e
            time.sleep(0.5)
    if last:
        raise RuntimeError(f"Impossible de sauvegarder {filename}: {last}")
assert len(records)==3
with zipfile.ZipFile("MYTHOS_3_images_complementaires.zip","w",compression=zipfile.ZIP_STORED) as out:
    for v in records:
        out.write(OUT/v["filename"],arcname="images/"+v["filename"])
    out.writestr("manifest.json",json.dumps(records,ensure_ascii=False,indent=2))
    out.writestr("README.txt","MYTHOS — trois images complementaires a l'archive des 107 medias publics. Toutes les images sont archivees avec SHA-256. Ne pas supprimer WordPress avant les controles de migration.\n")
print("DONE: 3/3 images.")
