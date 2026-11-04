#!/usr/bin/env python3
"""Check the deployed inventory and every listed page; no content mutations."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'User-Agent':'MYTHOS-publication-check/1.0','Cache-Control':'no-cache'}),timeout=25) as response:
                return response.status,response.headers.get('Content-Type',''),response.read()
        except Exception:
            if attempt==2:raise
            time.sleep(2)


class PhilosophySVGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = set()

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        source = dict(attrs).get("src", "").split("?", 1)[0].split("#", 1)[0]
        if source.startswith("/assets/philosophie/") and source.lower().endswith(".svg"):
            self.sources.add(source)


def svg_inventory(root):
    """Inventory every local SVG shown in the three philosophical monographs."""
    page_sources = {}
    digests = {}
    for page in ("philosophie-iliade.html", "philosophie-odyssee.html",
                 "philosophie-theogonie.html"):
        parser = PhilosophySVGParser()
        parser.feed((root / page).read_text(encoding="utf-8"))
        if not parser.sources:
            raise RuntimeError(f"Aucune illustration SVG interne dans {page}")
        page_sources[page] = sorted(parser.sources)
        for source in parser.sources:
            path = root / source.lstrip("/")
            if not path.is_file():
                raise RuntimeError(f"Illustration SVG absente du build : {source}")
            contents = path.read_bytes()
            if b"<svg" not in contents[:1024]:
                raise RuntimeError(f"Illustration SVG invalide : {source}")
            digests[source] = hashlib.sha256(contents).hexdigest()
    return page_sources, digests


def verify_public_svgs(base, root):
    """Check the public HTML references and exact SVG bytes, not just HTTP 200."""
    page_sources, digests = svg_inventory(root)
    base = base.rstrip("/")

    def check_page(entry):
        page, sources = entry
        try:
            status, _, body = fetch(base + "/" + page)
            missing = [source for source in sources if source.encode("utf-8") not in body]
            return {"url": "/" + page, "valid": status == 200 and not missing,
                    "missing_assets_in_public_html": missing}
        except Exception as error:
            return {"url": "/" + page, "valid": False, "error": str(error)}

    def check_asset(entry):
        source, digest = entry
        try:
            status, _, body = fetch(base + source)
            valid = (status == 200 and b"<svg" in body[:1024]
                     and hashlib.sha256(body).hexdigest() == digest)
            return {"url": source, "valid": valid, "status": status,
                    "sha256_matches_build": valid}
        except Exception as error:
            return {"url": source, "valid": False, "error": str(error)}

    with ThreadPoolExecutor(max_workers=6) as pool:
        page_results = list(pool.map(check_page, page_sources.items()))
        asset_results = list(pool.map(check_asset, digests.items()))
    return page_results + asset_results


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',default='https://bobmythos.fr')
    parser.add_argument('--output',default='/tmp/mythos-live-verification.json')
    args=parser.parse_args()
    expected=json.loads(Path('_site/catalog/entries.json').read_text())
    # Wait for propagation, but fail visibly if the newly deployed inventory
    # cannot be identified. A 200 from an older site is not publication proof.
    remote=None
    for attempt in range(6):
        try:
            _,_,body=fetch(args.base+'/catalog/entries.json?verify='+str(int(time.time())))
            remote=json.loads(body)
            if remote==expected:break
        except Exception:pass
        time.sleep(10)
    if remote!=expected:raise RuntimeError('Le catalogue public ne correspond pas à cette publication')
    urls=['/']+[entry['url'] for entry in expected['entries']]
    urls += [item['url'] for item in json.loads(Path('_site/catalog/reading-pdfs.json').read_text())]
    def check(path):
        try:
            status,kind,body=fetch(args.base+path)
            pdf=path.endswith('.pdf')
            valid=status==200 and (body.startswith(b'%PDF') if pdf else b'<html' in body.lower())
            return {'url':path,'status':status,'valid':valid,'bytes':len(body)}
        except Exception as error:return {'url':path,'valid':False,'error':str(error)}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,urls))
    try:
        svg_results = verify_public_svgs(args.base, Path('_site'))
    except Exception as error:
        svg_results = [{'url': '/assets/philosophie/', 'valid': False,
                        'error': f'Inventaire SVG : {error}'}]
    failures=[r for r in results+svg_results if not r['valid']]
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'base_url':args.base,
            'checked':len(results)+len(svg_results),'svg_checks':svg_results,
            'failures':failures,'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Pages publiques vérifiées :',len(results),' ; erreurs :',len(failures))
    if failures:raise RuntimeError(json.dumps(failures[:10],ensure_ascii=False))


if __name__=='__main__':main()
