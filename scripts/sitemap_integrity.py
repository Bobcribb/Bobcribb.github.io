"""Recognize intentional canonical aliases without weakening sitemap checks.

Only internal HTTPS aliases to the canonical MYTHOS domain can be exempted.
The historical page must continue to exist in the generated site.
"""
from pathlib import Path
from urllib.parse import urlsplit
import re

from bs4 import BeautifulSoup

DOMAIN = "bobmythos.fr"


def canonical_target(root, url):
    """Return a valid internal canonical URL for an existing public HTML page."""
    if not url.startswith("/") or url.startswith("//"):
        return None
    file = Path(root) / url.lstrip("/")
    if url.endswith("/") or file.is_dir() or (not file.suffix and not file.is_file()):
        file = file / "index.html"
    if not file.is_file() or file.suffix.lower() != ".html":
        return None
    head = re.split(r"</head\s*>", file.read_text(encoding="utf-8"), maxsplit=1, flags=re.I)[0]
    canonical = BeautifulSoup(head, "html.parser").select_one('link[rel~="canonical"]')
    if not canonical:
        return None
    parsed = urlsplit(canonical.get("href", "").strip())
    if (parsed.scheme.lower() != "https" or parsed.netloc.lower() != DOMAIN
            or parsed.query or parsed.fragment or not parsed.path.startswith("/")
            or parsed.path.startswith("//")):
        return None
    return f"https://{DOMAIN}{parsed.path}"
