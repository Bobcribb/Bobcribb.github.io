#!/usr/bin/env python3
"""Mirror MYTHOS media to GitHub Pages, so the published site does not hotlink WordPress.

Run after scripts/build.py. For any image/PDF already saved under media/, reuse the
checked local copy. On new or changed WP pages, download newly referenced media.
All assets are public WordPress attachments; no WordPress drafts are published.
The three unreferenced media are included for a complete original-library snapshot.
"""
import hashlib
import json
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("media")
SITE = Path("_site")
EXTRA = {
    "2026/10/mythos-monogramme-or-noir-512.png",
    "2026/10/mythos-demeter-porcelet-terre-cuite-athenes-cma-1926-521.jpg",
    "2026/10/mythos-e28094-illustration-du-sanctuaire-de-delphes.png",
}
PATTERN = re.compile(r"/media/((?:20\d{2})/(?:0[1-9]|1[0-2])/[A-Za-z0-9._~%+\-]+)",re.I)
SIGNATURES = {".png":b"\x89PNG\r\n\x1a\n", ".jpg":b"\xff\xd8",
              ".jpeg":b"\xff\xd8", ".pdf":b"%PDF"}
MAX_FILE_BYTES = 40_000_000

def valid(blob, ext):
    return len(blob) > 40 and len(blob) <= MAX_FILE_BYTES and (
        ext not in SIGNATURES or blob.startswith(SIGNATURES[ext]))

def download_one(rel):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    extension = p.suffix.lower()
    if p.is_file():
        blob = p.read_bytes()
        if valid(blob,extension):
            return {"file":str(p), "bytes":len(blob),
                    "sha256":hashlib.sha256(blob).hexdigest(),
                    "source":"local-cache","status":"saved"}
    remote = urllib.parse.quote(rel,safe="/._-~")
    base = "bobmythos.wordpress.com/wp-content/uploads/" + remote
    hosts = ["https://"+base, "https://i0.wp.com/"+base]
    error = ""
    for u in hosts:
        try:
            req = urllib.request.Request(u,headers={
                "User-Agent":"Mozilla/5.0 (MYTHOS independent media archive)",
                "Accept":"image/jpeg,image/png,image/*,application/pdf,*/*;q=0.8"})
            with urllib.request.urlopen(req,timeout=60) as response:
                blob = response.read(MAX_FILE_BYTES+1)
                ctype = response.headers.get("Content-Type","").lower()
            if ctype.startswith("text/html") or not valid(blob,extension):
                raise ValueError("Invalid image/PDF response: "+ctype)
            p.write_bytes(blob)
            return {"file":str(p),"bytes":len(blob),
                    "sha256":hashlib.sha256(blob).hexdigest(),
                    "source":"wordpress-original","status":"saved"}
        except (urllib.error.URLError,OSError,ValueError,TimeoutError) as e:
            error=str(e)[:250]
    return {"file":str(p),"status":"failed","error":error}

def main():
    if not (SITE/"index.html").is_file():
        raise RuntimeError("MYTHOS site must be built first")
    refs=set(EXTRA)
    for path in SITE.rglob("*.html"):
        content=path.read_text(encoding="utf-8")
        for m in PATTERN.finditer(content):
            rel=urllib.parse.unquote(m.group(1))
            parts=Path(rel).parts
            if len(parts)==3 and ".." not in parts:
                refs.add(rel)
    if len(refs)<100:
        raise RuntimeError(f"Media source mismatch: {len(refs)} references; expected at least 100")
    print(f"MYTHOS: checking {len(refs)} local media",flush=True)
    results=[]
    with ThreadPoolExecutor(max_workers=6) as executor:
        requests={executor.submit(download_one,rel):rel for rel in sorted(refs)}
        for idx,fut in enumerate(as_completed(requests),1):
            result=fut.result()
            results.append(result)
            if idx%20==0:print(f"Media {idx}/{len(refs)} checked",flush=True)
    failed=[r for r in results if r["status"]!="saved"]
    if failed:
        print("Missing media:",json.dumps(failed,ensure_ascii=False),file=sys.stderr)
        raise RuntimeError(f"{len(failed)} media could not be saved, refusing site deployment")
    target=SITE/"media"
    for rec in results:
        src=Path(rec["file"])
        dst=target/src.relative_to(ROOT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src,dst)
    results.sort(key=lambda x:x["file"])
    inventory={"count":len(results),"total_bytes":sum(r["bytes"] for r in results),
               "files":[{"path":r["file"],"size":r["bytes"],"sha256":r["sha256"]} for r in results]}
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/"manifest.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (target/"manifest.json").write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"MYTHOS: self-hosted {len(results)} media, {inventory['total_bytes']} bytes",flush=True)

if __name__=="__main__":
    main()
