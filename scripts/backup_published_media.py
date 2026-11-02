#!/usr/bin/env python3
"""Back up images and PDF files referenced by public MYTHOS pages.

This script reads only already published static pages from _site/.
No draft or private media paths are disclosed or pulled.
A failed/partial media download is listed honestly in the manifest.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, time, hashlib, re

SOURCE = Path("_site")
DEST = Path("_published_media")
HOSTS = {"bobmythos.fr", "www.bobmythos.fr", "bobmythos.wordpress.com"}
if not (SOURCE / "index.html").exists():
    raise RuntimeError("Run scripts/build.py before backing up media.")

def media_ref(url):
    if not url or url.startswith("data:"):
        return None
    if url.startswith("//"):
        url = "https:" + url
    parts = urlsplit(url)
    if parts.hostname not in HOSTS:
        return None
    match = re.search(r"/wp-content/uploads/([A-Za-z0-9%._~/+-]+)$", parts.path)
    if not match:
        return None
    asset = unquote(match.group(1))
    bits = Path(asset).parts
    if ".." in bits or len(bits) < 2 or len(asset)>250:
        return None
    return asset

references = {}
for fp in SOURCE.rglob("*.html"):
    page_url = "/" + str(fp.relative_to(SOURCE).parent).strip("./") + "/"
    html = BeautifulSoup(fp.read_text(encoding="utf-8"), "html.parser")
    for tag in html.find_all(True):
        vals = []
        for attr in ("src", "href", "poster", "data-src"):
            if tag.has_attr(attr):
                vals.append(str(tag[attr]))
        if tag.has_attr("srcset"):
            vals.extend(part.strip().split(" ")[0] for part in str(tag["srcset"]).split(","))
        for u in vals:
            asset = media_ref(u)
            if asset:
                references.setdefault(asset, set()).add(page_url)

print("Found", len(references), "unique public-page media references", flush=True)
if not references:
    raise RuntimeError("No published media references: aborting")
DEST.mkdir(exist_ok=True)
records = []

def download_one(asset):
    rel = "files/" + asset
    path = DEST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = quote(asset, safe="/.-_~")
    urls = [
        "https://bobmythos.wordpress.com/wp-content/uploads/" + encoded,
        "https://i0.wp.com/bobmythos.wordpress.com/wp-content/uploads/" + encoded
    ]
    last_error = "unknown"
    for u in urls:
        try:
            req = Request(u, headers={"User-Agent":"Mozilla/5.0 (MYTHOS media preservation)", "Accept":"image/avif,image/webp,image/*,application/pdf,*/*;q=0.8"})
            with urlopen(req, timeout=45) as response:
                content = response.read(35_000_000)
                content_type = response.headers.get("Content-Type","").split(";")[0]
                if response.read(1):
                    raise ValueError("Image exceeds 35 MB cap")
            if not content:
                raise ValueError("empty file")
            ext = path.suffix.lower()
            if ext in (".jpg", ".jpeg") and not content.startswith(b"\xff\xd8"):
                raise ValueError("wrong JPEG signature: " + content_type)
            if ext == ".png" and not content.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("wrong PNG signature: " + content_type)
            if ext == ".pdf" and not content.startswith(b"%PDF"):
                raise ValueError("wrong PDF signature: " + content_type)
            if content_type.startswith("text/html") or content_type.startswith("application/json"):
                raise ValueError("unexpected response: " + content_type)
            path.write_bytes(content)
            return {
                "file":rel, "source":u, "bytes":len(content),
                "sha256":hashlib.sha256(content).hexdigest(),
                "referenced_by":sorted(references[asset]),
                "status":"saved"
            }
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as e:
            last_error = type(e).__name__ + ": " + str(e)[:140]
    return {
        "file":rel, "source":urls[0],
        "referenced_by":sorted(references[asset]),
        "status":"failed", "error":last_error
    }

with ThreadPoolExecutor(max_workers=5) as pool:
    fut = {pool.submit(download_one, a): a for a in sorted(references)}
    for idx, f in enumerate(as_completed(fut),1):
        records.append(f.result())
        if idx % 10 == 0:
            print("Handled",idx,"/",len(references),flush=True)
records.sort(key=lambda x:x["file"])
succeeded = sum(r["status"]=="saved" for r in records)
failures = len(records)-succeeded
summary={
    "scope":"Files referenced from published MYTHOS pages only. Unpublished media are not included.",
    "published_media_references":len(records),
    "saved_files":succeeded,
    "failed_files":failures,
    "downloaded_bytes":sum(r.get("bytes",0) for r in records),
    "files":records,
}
(DEST/"manifest.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
(DEST/"README.txt").write_text(
    "MYTHOS — sauvegarde des images et PDF référencés dans les pages publiques.\n"
    "Ce dépôt GitHub ne conserve pas l'archive; elle doit être transférée dans Google Drive.\n"
    "Vérifier manifest.json pour le nombre de fichiers réellement sauvegardés.\n"
    "Les médias non publiés ne sont pas inclus. Ne pas supprimer WordPress avant un audit complet.\n",
    encoding="utf-8"
)
print("BACKUP RESULT:",succeeded,"saved;",failures,"failed;",summary["downloaded_bytes"],"bytes",flush=True)
if not succeeded:
    raise RuntimeError("All media downloads failed. No empty archive should be treated as a backup.")
