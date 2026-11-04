#!/usr/bin/env python3
"""Verify each publicly served MYTHOS WebP against the exact GitHub Pages build artifact.

A successful GitHub commit or an HTTP 200 for the gallery is not publication proof:
every listed image must be reachable, be WebP, and match the deployed bytes.
"""
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


MANIFEST = "assets/reconstitutions-3d/catalogue-photorealiste.json"
GALLERY = "reconstitutions-photorealistes.html"


def gallery_markup_failures(markup, entries):
    """A downloaded WebP alone does not prove its notice is publicly visible."""
    doc = BeautifulSoup(markup, "html.parser")
    failures = []
    for entry in entries:
        slug = entry["slug"]
        cards = doc.find_all(id=slug)
        errors = []
        if len(cards) != 1:
            errors.append("Ancre de notice absente ou dupliquée")
        else:
            card = cards[0]
            picture = card.find("img", src=entry["src"])
            caption = card.find("figcaption")
            science = card.select_one(".r3d-science")
            if picture is None or not picture.get("alt", "").strip():
                errors.append("Image de la notice ou texte alternatif absent")
            if caption is None or not caption.get_text(" ", strip=True):
                errors.append("Légende absente")
            science_text = science.get_text(" ", strip=True) if science else ""
            if not science or not science.select_one("p") or "certitude" not in science_text.lower():
                errors.append("Commentaire scientifique ou degré de certitude absent")
            if not card.find("a", href=entry["source_url"]):
                errors.append("Source institutionnelle différente du catalogue ou absente")
            for element in (card, picture, caption, science):
                if element is not None and (element.has_attr("hidden") or element.get("aria-hidden") == "true"):
                    errors.append("Contenu de la notice explicitement masqué")
                    break
        failures.extend({"resource": "/" + GALLERY + "#" + slug, "error": error} for error in errors)
    for node in doc.select("[src], [href]"):
        value = str(node.get("src") or node.get("href") or "")
        if "/assets/reconstitutions/" in value and ".svg" in value.lower():
            failures.append({"resource": value, "error": "Ancienne illustration vectorielle réintroduite"})
    return failures


class ImagesInGallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = set()

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            fields = dict(attrs)
            if fields.get("src"):
                self.sources.add(fields["src"])


def is_webp(data):
    """Recognize RIFF/WEBP bytes, not just a .webp filename or content type."""
    return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"


def request_bytes(url):
    req = Request(url, headers={
        "User-Agent": "MYTHOS-public-photoreal-verification/1.0",
        "Cache-Control": "no-cache",
    })
    with urlopen(req, timeout=25) as response:
        return response.status, response.read()


def inventory(root):
    catalog = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    entries = catalog["entries"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("Le catalogue photoréaliste est vide")
    if catalog.get("count") != len(entries):
        raise ValueError("Le nombre déclaré du catalogue ne correspond pas aux entrées")
    slugs = [e.get("slug") for e in entries]
    if len(set(slugs)) != len(slugs):
        raise ValueError("Identifiants de reconstitution dupliqués")
    image_paths = [e.get("src") for e in entries]
    if len(set(image_paths)) != len(image_paths):
        raise ValueError("La même image est référencée plusieurs fois")
    for e in entries:
        src = e.get("src", "")
        if not isinstance(src, str) or not src.startswith("/assets/reconstitutions-3d/") or not src.endswith(".webp") or ".." in src:
            raise ValueError(f"Chemin de reconstitution invalide : {src}")
        if not isinstance(e.get("source_url"), str) or not e["source_url"].startswith("https://"):
            raise ValueError(f"Source institutionnelle manquante : {src}")
        for field in ("title", "period", "caption", "commentary", "certainty"):
            if not isinstance(e.get(field), str) or not e[field].strip():
                raise ValueError(f"Notice scientifique incomplète ({field}) : {src}")
        local = root / src.lstrip("/")
        if not local.is_file() or local.stat().st_size < 10000 or not is_webp(local.read_bytes()[:12]):
            raise ValueError(f"Fichier source WebP absent ou invalide : {src}")
    return catalog, entries


def verify_once(base, root, catalog, entries):
    failures = []
    gallery_images = set()
    remote_catalog_valid = False
    try:
        status, body = request_bytes(base + "/" + MANIFEST)
        remote_catalog_valid = status == 200 and json.loads(body) == catalog
        if not remote_catalog_valid:
            failures.append({"resource": "/" + MANIFEST, "error": "Catalogue public différent de la source"})
    except Exception as exc:
        failures.append({"resource": "/" + MANIFEST, "error": str(exc)})
    try:
        status, body = request_bytes(base + "/" + GALLERY)
        if status != 200:
            failures.append({"resource": "/" + GALLERY, "error": f"HTTP {status}"})
        else:
            parser = ImagesInGallery()
            markup = body.decode("utf-8")
            parser.feed(markup)
            gallery_images = parser.sources
            failures.extend(gallery_markup_failures(markup, entries))
    except Exception as exc:
        failures.append({"resource": "/" + GALLERY, "error": str(exc)})
    for e in entries:
        if e["src"] not in gallery_images:
            failures.append({"resource": e["src"], "error": "Image non affichée dans le HTML public de la galerie"})

    def check_image(e):
        src = e["src"]
        try:
            status, content = request_bytes(base + src)
            if status != 200:
                return {"src": src, "ok": False, "error": f"HTTP {status}"}
            if not is_webp(content):
                return {"src": src, "ok": False, "error": "Le fichier public ne contient pas d'en-tête WebP"}
            local_digest = hashlib.sha256((root / src.lstrip("/")).read_bytes()).hexdigest()
            live_digest = hashlib.sha256(content).hexdigest()
            if live_digest != local_digest:
                return {"src": src, "ok": False, "error": "Fichier public différent du fichier déployé"}
            return {"src": src, "ok": True, "bytes": len(content), "sha256": live_digest}
        except Exception as exc:
            return {"src": src, "ok": False, "error": str(exc)}

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check_image, entries))
    failures.extend([{"resource": x["src"], "error": x["error"]} for x in results if not x["ok"]])
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "base_url": base,
        "expected_images": len(entries),
        "verified_images": sum(x["ok"] for x in results),
        "catalog_public_matches_build": remote_catalog_valid,
        "gallery_images_found": len(gallery_images),
        "failures": failures,
        "results": results,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="https://bobmythos.fr")
    p.add_argument("--root", default="_site")
    p.add_argument("--output", default="/tmp/mythos-images-verification.json")
    p.add_argument("--attempts", type=int, default=6)
    args = p.parse_args()
    root = Path(args.root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        catalog, entries = inventory(root)
    except Exception as exc:
        report = {"checked_at": datetime.now(timezone.utc).isoformat(), "failures": [{"error": str(exc)}]}
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    report = None
    for attempt in range(max(1, args.attempts)):
        report = verify_once(args.base.rstrip("/"), root, catalog, entries)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Galerie publique : {report['verified_images']}/{len(entries)} WebP identiques au build ; erreurs : {len(report['failures'])}", flush=True)
        if not report["failures"]:
            break
        if attempt + 1 < args.attempts:
            time.sleep(10)
    if report["failures"]:
        raise SystemExit("La publication photoréaliste publique n'est pas intégralement vérifiée")
    print("Publication publique de chaque image et de chaque notice confirmée.", flush=True)


if __name__ == "__main__":
    main()
