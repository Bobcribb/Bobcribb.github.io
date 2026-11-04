#!/usr/bin/env python3
"""Pin three public-domain museum images used by the Eneid study.

Source of truth: Metropolitan Museum of Art Open Access API.
No generated image is claimed to be an ancient witness to Virgil's text.
Requires Pillow. Run before scripts/render_eneide.py.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from PIL import Image, ImageOps, UnidentifiedImageError
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets/philosophie/eneide"
MANIFEST = ROOT / "assets/philosophie/eneide-art-sources.json"
API = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
ITEMS = [
    (195297, "didon-carthage-met.jpg", "Aeneas Departs from Carthage (Aeneid, Book IV)"),
    (435813, "sibylle-enfers-met.jpg", "Aeneas and the Sibyl in the Underworld"),
    (420445, "venus-vulcain-met.jpg", "Venus at the Forge of Vulcan"),
]
USER_AGENT = "MYTHOS-academic-edition/1.0 (Open Access museum illustration; https://bobmythos.fr/)"

def read_url(url: str, max_bytes=35_000_000) -> bytes:
    last = None
    for attempt in range(4):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,image/*"})
            with urlopen(req, timeout=35) as r:
                data = r.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError("image exceeds limit")
                return data
        except (OSError, ValueError, URLError) as exc:
            last = exc
            if attempt < 3:
                time.sleep(1 + attempt * 2)
    raise RuntimeError(f"Unable to retrieve {url}: {last}")

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for object_id, filename, expected in ITEMS:
        obj = json.loads(read_url(API + str(object_id), 2_000_000).decode("utf-8"))
        if obj.get("objectID") != object_id or not obj.get("isPublicDomain"):
            raise ValueError(f"Public-domain status not verified for {object_id}")
        if expected.lower() not in obj.get("title", "").lower():
            raise ValueError(f"Unexpected museum object {object_id}: {obj.get('title')}")
        source = obj.get("primaryImage") or obj.get("primaryImageSmall")
        if not source:
            raise ValueError(f"No official open-access image for {object_id}")
        original = read_url(source)
        with Image.open(BytesIO(original)) as src:
            image = ImageOps.exif_transpose(src)
            image.thumbnail((1850, 1850), Image.Resampling.LANCZOS)
            if image.mode != "RGB":
                image = image.convert("RGB")
            out = DEST / filename
            image.save(out, format="JPEG", quality=85, optimize=True, progressive=True)
            width, height = image.size
        if out.stat().st_size < 8000:
            raise ValueError(f"Suspiciously small museum image: {out}")
        records.append({
            "path": str(out.relative_to(ROOT)),
            "museum": "The Metropolitan Museum of Art, New York",
            "object_id": object_id,
            "title": obj["title"],
            "artist": obj.get("artistDisplayName", ""),
            "date": obj.get("objectDate", ""),
            "object_number": obj.get("accessionNumber", ""),
            "object_url": obj.get("objectURL", f"https://www.metmuseum.org/art/collection/search/{object_id}"),
            "source_image_url": source,
            "rights": "Public Domain — Met Open Access / CC0",
            "width_px": width, "height_px": height,
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest()
        })
        print(f"Pinned {filename}: {width}x{height} / {out.stat().st_size} bytes")
    MANIFEST.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
