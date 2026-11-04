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
from bs4 import BeautifulSoup


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



# Figures from two iconography sessions. Require both the published notices
# and exact local image bytes, not just a successful gallery response.
TARGET_FIGURES = {
    "philosophie-iliade.html": ("icono-iliade-mycene-panorama-philosophie-20261104",
        "/assets/reconstitutions-3d/mycenes-citadelle-porte-lionnes-panorama.webp"),
    "philosophie-odyssee.html": ("icono-odyssee-tirynthe-palais-20261104",
        "/assets/reconstitutions-3d/tirynthe-citadelle-mycenienne-panorama.webp"),
    "philosophie-theogonie.html": ("icono-theogonie-zeus-olympie-altis-20261104",
        "/assets/reconstitutions-3d/olympie-altis-panorama.webp"),
    "livre-hesiode/index.html": ("mythos-fig-hesiode-succession-pouvoir-20261104",
        "/assets/philosophie/theogonie-succession-pouvoir.svg"),
    "epidaure-asclepios-incubation-iamata-guerisons/index.html":
        ("mythos-fig-epidaure-panorama-20261104",
         "/assets/reconstitutions-3d/epidaure-asclepieion-sanctuaire-panorama.webp"),
    "eleusis-demeter-persephone-mysteres/index.html":
        ("mythos-fig-eleusis-telesterion-20261104",
         "/assets/reconstitutions-3d/eleusis-telesterion-sanctuaire-panorama.webp"),
}


def figure_metadata(markup, figure_id, src):
    soup = BeautifulSoup(markup, "html.parser")
    nodes = soup.find_all("figure", id=figure_id)
    if len(nodes) != 1:
        raise ValueError("Figure absente ou dupliquée : " + figure_id)
    figure = nodes[0]
    img, caption = figure.find("img"), figure.find("figcaption")
    if img is None or caption is None:
        raise ValueError("Image ou légende absente : " + figure_id)
    if img.get("src", "").split("?", 1)[0].split("#", 1)[0] != src:
        raise ValueError("Image inattendue : " + figure_id)
    if not img.get("alt", "").strip() or figure.has_attr("hidden") or figure.get("aria-hidden") == "true":
        raise ValueError("Alt absent ou figure masquée : " + figure_id)
    sources = sorted({a["href"] for a in caption.find_all("a", href=True)
                      if a["href"].startswith("https://")})
    data = {"alt": img["alt"].strip(),
            "caption": " ".join(caption.get_text(" ", strip=True).split()),
            "status": figure.get("data-image-status", "").strip(),
            "source_urls": sources}
    if not data["caption"] or not data["status"] or not sources:
        raise ValueError("Notice, statut IA ou provenance absente : " + figure_id)
    return data


def figure_inventory(root):
    pages, assets = {}, {}
    for page, (fid, src) in TARGET_FIGURES.items():
        html = (root / page).read_text(encoding="utf-8")
        pages[page] = figure_metadata(html, fid, src)
        path = root / src.lstrip("/")
        body = path.read_bytes()
        valid = (len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WEBP"
                 if src.endswith(".webp") else b"<svg" in body[:2048])
        if not valid:
            raise ValueError("Image absente ou invalide : " + src)
        assets[src] = hashlib.sha256(body).hexdigest()
    return pages, assets


def verify_public_figures(base, root):
    pages, images = figure_inventory(root)
    base = base.rstrip("/")

    def check_page(entry):
        page, expected = entry
        fid, src = TARGET_FIGURES[page]
        try:
            status, _, body = fetch(base + "/" + page)
            actual = figure_metadata(body.decode("utf-8"), fid, src)
            valid = status == 200 and actual == expected
            return {"url": "/" + page, "valid": valid,
                    "figure_id": fid, "notice_matches_build": valid}
        except Exception as error:
            return {"url": "/" + page, "valid": False, "error": str(error)}

    def check_image(entry):
        src, digest = entry
        try:
            status, _, body = fetch(base + src)
            magic = (len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WEBP"
                     if src.endswith(".webp") else b"<svg" in body[:2048])
            valid = status == 200 and magic and hashlib.sha256(body).hexdigest() == digest
            return {"url": src, "valid": valid, "sha256_matches_build": valid}
        except Exception as error:
            return {"url": src, "valid": False, "error": str(error)}

    with ThreadPoolExecutor(max_workers=6) as executor:
        return (list(executor.map(check_page, pages.items()))
                + list(executor.map(check_image, images.items())))


# Documented photographs, historical artworks and modern photography:
# validate JPEG and WebP by their distinct binary signatures.
RECENT_FIGURES = (
    ("livre-iliade-scenes/index.html", "mythos-iliade-troie-vi-remparts-20261104",
     "/media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg"),
    ("livre-odyssee/index.html", "mythos-odyssee-penelope-telemaque-skyphos-20261104",
     "/media/2026/10/penelope-telemaque-metier-coupe-chiusi-1831.jpg"),
    ("livre-odyssee/index.html", "mythos-odyssee-pylos-palais-nestor-20261104",
     "/assets/philosophie/documents/odyssee-04.jpg"),
    # Five documented illustrations added to the philosophy monographs
    # and the Hesiod reading book on 4 November 2026.
    ("philosophie-iliade.html", "icono-iliade-achille-ajax-jeu-hydrie-20261104",
     "/media/2026/10/mythos-iliade-achille-ajax-athena-hydrie-met-56-171-29.jpg"),
    ("philosophie-odyssee.html", "icono-odyssee-papyrus-met-xx-20261104",
     "/media/2026/10/mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg"),
    ("livre-hesiode/index.html", "icono-hesiode-livre-hippocrene-20261104",
     "/assets/philosophie/documents/theogonie-04.jpg"),
    ("livre-hesiode/index.html", "icono-hesiode-livre-rhea-cronos-20261104",
     "/assets/philosophie/documents/theogonie-01.jpg"),
    ("livre-hesiode/index.html", "icono-hesiode-livre-zeus-typhon-hydrie-20261104",
     "/assets/philosophie/documents/theogonie-02.jpg"),
    # Genuine nineteenth-century artworks documented by The Metropolitan Museum
    # of Art. Check them separately on their respective pages and verify their
    # local WebP bytes, rather than assuming that a successful HTML response
    # means the newly inserted figures were deployed.
    ("philosophie-iliade.html", "icono-iliade-flaxman-ombre-patrocle-reception-20261104",
     "/assets/illustrations-articles/met-341681-achille-ombre-patrocle-flaxman.webp"),
    ("philosophie-odyssee.html", "icono-odyssee-flaxman-parker-circe-1805-20261104",
     "/assets/illustrations-articles/met-705224-ulysse-circe-flaxman.webp"),
    ("philosophie-theogonie.html", "icono-theogonie-ottley-nuit-enfants-attribution-20261104",
     "/assets/illustrations-articles/met-649972-ottley-nuit-enfants.webp"),
    # Museum documents inserted during the immediately preceding iconography
    # session. Compare every figure, caption and exact WebP file on HTTPS.
    ("philosophie-iliade.html", "icono-iliade-rembrandt-aristote-homere-met-437394-20261104",
     "/assets/illustrations-articles/met-437394-aristote-homere-rembrandt.webp"),
    ("philosophie-odyssee.html", "icono-odyssee-persephone-enfers-met-252973-20261104",
     "/assets/illustrations-articles/met-252973-persephone-retour-enfers.webp"),
    ("philosophie-theogonie.html", "icono-theogonie-nike-styx-met-247903-20261104",
     "/assets/illustrations-articles/met-247903-nike-terre-cuite.webp"),
    # Latest documented museum images on the Iliad, Odyssey and Hesiod
    # reading pages. Verify both public notices and identical WebP bytes.
    ("livre-iliade-scenes/index.html", "icono-iliade-enee-virgile-distinction-20261104",
     "/assets/illustrations-articles/met-199612-enee-fuite-troie-email.webp"),
    ("livre-odyssee/index.html", "icono-odyssee-hermes-bronze-met-246679-20261104",
     "/assets/illustrations-articles/met-246679-hermes-bronze-aile.webp"),
    ("livre-hesiode/index.html", "icono-hesiode-promethee-bartolozzi-1795-20261104",
     "/assets/illustrations-articles/met-680363-promethee-bartolozzi.webp"),
)


def valid_local_illustration(src, body):
    """Check actual file signatures before verifying SHA-256 equality."""
    if src.lower().endswith((".jpg", ".jpeg")):
        return len(body) >= 3 and body[:3] == bytes.fromhex("ffd8ff")
    if src.lower().endswith(".webp"):
        return len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WEBP"
    if src.lower().endswith(".svg"):
        return b"<svg" in body[:2048]
    return False


def recent_figure_inventory(root):
    """Group multiple authored figures on a page without losing either one."""
    pages, digests = {}, {}
    for page, fid, src in RECENT_FIGURES:
        markup = (root / page).read_text(encoding="utf-8")
        meta = figure_metadata(markup, fid, src)
        figures = pages.setdefault(page, {})
        if fid in figures or src in digests:
            raise ValueError("Illustration historique dupliquée : " + fid)
        figures[fid] = (src, meta)
        image = (root / src.lstrip("/")).read_bytes()
        if not valid_local_illustration(src, image):
            raise ValueError("Photographie locale absente ou invalide : " + src)
        digests[src] = hashlib.sha256(image).hexdigest()
    return pages, digests


def verify_recent_public_figures(base, root):
    """Require all recent figures on public pages and exact JPEG/WebP bytes."""
    page_inventory, digests = recent_figure_inventory(root)
    base = base.rstrip("/")

    def check_page(entry):
        page, expected_figures = entry
        try:
            status, _, body = fetch(base + "/" + page)
            markup = body.decode("utf-8")
            mismatches = []
            for fid, (src, expected) in expected_figures.items():
                try:
                    if figure_metadata(markup, fid, src) != expected:
                        mismatches.append(fid)
                except ValueError:
                    mismatches.append(fid)
            return {"url": "/" + page, "valid": status == 200 and not mismatches,
                    "figures_verified": len(expected_figures) - len(mismatches),
                    "missing_or_changed_figures": mismatches}
        except Exception as error:
            return {"url": "/" + page, "valid": False, "error": str(error)}

    def check_asset(entry):
        src, digest = entry
        try:
            status, _, body = fetch(base + src)
            valid = (status == 200 and valid_local_illustration(src, body)
                     and hashlib.sha256(body).hexdigest() == digest)
            return {"url": src, "valid": valid, "sha256_matches_build": valid}
        except Exception as error:
            return {"url": src, "valid": False, "error": str(error)}

    with ThreadPoolExecutor(max_workers=5) as pool:
        page_results = list(pool.map(check_page, page_inventory.items()))
        image_results = list(pool.map(check_asset, digests.items()))
    return page_results + image_results



def verify_public_receipt(base, root):
    """Identical catalogue URLs alone do not prove a new Pages deployment."""
    path = root / "catalog/publication-verification.json"
    expected = json.loads(path.read_text(encoding="utf-8"))
    status, _, body = fetch(base.rstrip("/") + "/catalog/publication-verification.json?verify="
                            + str(int(time.time())))
    return status == 200 and json.loads(body) == expected



def verify_public_history(base, root):
    """Verify the deployed MC notices, complete texts and catalogue statuses."""
    from comparative_history import REPORT, url
    expected = json.loads((root/REPORT).read_text())
    pages = {'/mythologie-comparee/', '/philosophie/', '/collections-numerotees/'}
    members = set()
    for group in expected['groups'].values():
        pages.add(group['guide_url'])
        members.add(group['guide_url'])
        for member in group['members']:
            pages.add(url(member))
            members.add(url(member))
    results = []
    for path in ['/'+REPORT.as_posix(), '/search.json', '/catalog/entries.json', '/sitemap.xml']+sorted(pages):
        try:
            status, _, body = fetch(base.rstrip('/')+path)
            local = root/path.lstrip('/')
            if path.endswith('/'): local /= 'index.html'
            if path in ('/search.json', '/catalog/entries.json'):
                def selected(value):
                    data = json.loads(value)
                    entries = data['entries'] if isinstance(data,dict) else data
                    return {e['url']:e for e in entries if e['url'] in members}
                valid = selected(body) == selected(local.read_bytes()) and len(selected(body)) == len(members)
            elif path == '/sitemap.xml':
                valid = all(('https://bobmythos.fr'+address).encode() in body for address in members)
            else:
                valid = body == local.read_bytes()
            results.append({'url':path, 'valid':status==200 and valid,
                            'status':status, 'historical_content_matches_build':valid})
        except Exception as error:
            results.append({'url':path,'valid':False,'error':str(error)})
    return results


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',default='https://bobmythos.fr')
    parser.add_argument('--output',default='/tmp/mythos-live-verification.json')
    args=parser.parse_args()
    expected=json.loads(Path('_site/catalog/entries.json').read_text())
    # Wait for propagation, but fail visibly if the newly deployed inventory
    # cannot be identified. A 200 from an older site is not publication proof.
    remote=None
    receipt_ok=False
    for attempt in range(6):
        try:
            _,_,body=fetch(args.base+'/catalog/entries.json?verify='+str(int(time.time())))
            remote=json.loads(body)
            if remote==expected:
                receipt_ok=verify_public_receipt(args.base, Path('_site'))
            if remote==expected and receipt_ok:break
        except Exception:pass
        if attempt<5:time.sleep(10)
    if remote!=expected:raise RuntimeError('Le catalogue public ne correspond pas à cette publication')
    if not receipt_ok:raise RuntimeError('Le reçu public diffère du build : déploiement non confirmé')
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
    try:
        figure_results=verify_public_figures(args.base, Path('_site'))
    except Exception as error:
        figure_results=[{'url':'/figures-scientifiques/', 'valid':False,
                         'error':'Inventaire de figures : '+str(error)}]
    try:
        recent_results=verify_recent_public_figures(args.base, Path('_site'))
    except Exception as error:
        recent_results=[{'url':'/figures-epiques/', 'valid':False,
                         'error':'Photographies patrimoniales : '+str(error)}]
    history_results=verify_public_history(args.base, Path('_site'))
    failures=[r for r in results+svg_results+figure_results+recent_results+history_results if not r['valid']]
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'base_url':args.base,
            'checked':len(results)+len(svg_results)+len(figure_results)+len(recent_results)+len(history_results),
            'historical_checks':history_results, 'epic_figure_checks':recent_results, 'patrimonial_figure_checks':recent_results,
            'receipt_matches_build':receipt_ok,'svg_checks':svg_results,
            'figure_checks':figure_results,'failures':failures,'results':results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Pages publiques vérifiées :',len(results),' ; erreurs :',len(failures))
    if failures:raise RuntimeError(json.dumps(failures[:10],ensure_ascii=False))


if __name__=='__main__':main()
