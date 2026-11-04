"""Conservative, offline illustration selection shared by every collection.

Only an explicit subject in a page's own title/slug can select a documented
local object. Collection names, article prose, menus and existing galleries
are deliberately not evidence. An empty selection is a valid result.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import unicodedata

from bs4 import BeautifulSoup

CATALOG = Path(__file__).with_name("editorial_media.json")
GENERATED_CLASSES = {"mythos-home-illustrations", "mythos-visual-rail"}
MAX_ADDED_IMAGES = 6


def normalized(value):
    value = unicodedata.normalize("NFKD", value.casefold().replace("œ", "oe").replace("æ", "ae"))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", value))


def image_key(url):
    """Deduplicate local, legacy WordPress and Commons versions of one image."""
    path = unquote(urlsplit(url).path)
    name = path.rsplit("/", 1)[-1]
    name = re.sub(r"^(?:File:|\d+px-)", "", name, flags=re.I)
    return name.casefold().replace("_", " ")


def load_catalog():
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["media"]
    ids = set()
    for record in records:
        if record["id"] in ids:
            raise ValueError("Illustration dupliquée : " + record["id"])
        ids.add(record["id"])
        rel = Path(record["path"])
        allowed_root = rel.parts[:1] == ("media",) or rel.parts[:2] == ("assets", "illustrations-articles")
        if rel.is_absolute() or ".." in rel.parts or not allowed_root:
            raise ValueError("Média non local : " + str(rel))
        caption = BeautifulSoup(record["caption_html"], "html.parser")
        if not record["alt"].strip() or not record["subjects"] or not caption.get_text(strip=True):
            raise ValueError("Notice iconographique incomplète : " + record["id"])
        if not any(a.get("href", "").startswith("https://") for a in caption.find_all("a")):
            raise ValueError("Provenance absente : " + record["id"])
    return records


def page_subject(path, article):
    # The parent collections must never turn a chapter into a Greek/Egyptian
    # topic. For index.html only its immediate parent is the page's slug.
    leaf = path.parent.name if path.name == "index.html" else path.stem
    parts = [leaf]
    # Some manuscripts put the collection and the actual work in two H1s.
    for heading in article.find_all("h1", limit=2):
        parts.append(heading.get_text(" ", strip=True))
    # The museum renderer moves the page H1 into its banner. Its title is
    # still page-specific evidence when a snapshot reuses rendered HTML.
    body = article.find_parent("body")
    banner = body.select_one(".mythos-banner h1") if body else None
    banner_title = banner.get_text(" ", strip=True) if banner else ""
    if banner_title:
        parts.append(banner_title)
    # Older Markdown manuscripts use a collection-wide H1 and a chapter H2.
    chapter_heading = article.find("h2")
    if chapter_heading and re.match(r"^(?:Tome|Volume|Chapitre|Dossier|MC[- ])\b", chapter_heading.get_text(strip=True), re.I):
        parts.append(chapter_heading.get_text(" ", strip=True))
    elif chapter_heading and not article.find("h1") and re.search(r"\b(?:Chapitre|Volume)\s+(?:\d+|[IVXLCDM]+)(?:\s*\(\d+\))?\s*$", banner_title, re.I):
        # A collection/number-only banner leaves the actual work title as
        # the first H2. Do not use arbitrary subsection headings otherwise.
        parts.append(chapter_heading.get_text(" ", strip=True))
    return normalized(" ".join(parts))


def select_media(path, article, out, records):
    subject = " " + page_subject(path, article) + " "
    present = {image_key(img.get("src", "")) for img in article.find_all("img")}
    chosen = []
    for record in records:
        if not any(" " + normalized(term) + " " in subject for term in record["subjects"]):
            continue
        if not (out / record["path"]).is_file():
            continue  # Never fill the gap with a different, unrelated object.
        keys = {image_key(record["path"])} | {image_key(u) for u in record.get("equivalents", [])}
        if keys & present:
            continue
        chosen.append(record)
        present.update(keys)
        if len(chosen) == MAX_ADDED_IMAGES:
            break
    return chosen


def decorate_document(source, path, out, records):
    doc = BeautifulSoup(source, "html.parser")
    main = doc.find("main")
    article = main.find("article") if main else None
    if not article:
        return source, []
    # Migrate previously generated HTML as well as newly rendered Markdown.
    # Only generator-owned sibling asides are replaced; authored figures,
    # notes, quotations, tables and studies inside the article are preserved.
    removed = False
    for aside in main.find_all("aside", recursive=False):
        if GENERATED_CLASSES.intersection(aside.get("class", [])):
            aside.decompose()
            removed = True
    if removed or "visual-rails-active" in main.get("class", []):
        classes = [c for c in main.get("class", []) if c not in ("visual-rails-active", "portal-layout")]
        # Portals already have their own full-width layout, independent of rails.
        if article.select_one(".portal-section, .hero-editorial"):
            classes.append("portal-layout")
        main["class"] = classes
    if doc.head and not doc.select_one('link[href="/assets/mythos-refonte.css"]'):
        doc.head.append(doc.new_tag("link", rel="stylesheet", href="/assets/mythos-refonte.css"))
    chosen = select_media(path, article, out, records)
    if chosen:
        aside = doc.new_tag("aside", attrs={"class": "mythos-home-illustrations mythos-bottom-gallery", "data-editorial-gallery": "subject-v2", "aria-label": "Documents en rapport avec le sujet"})
        heading = doc.new_tag("h2")
        heading.string = "Documents iconographiques"
        aside.append(heading)
        for record in chosen:
            figure = doc.new_tag("figure", attrs={"data-media-id": record["id"]})
            full_size = doc.new_tag("a", href="/" + record["path"], attrs={"aria-label": "Agrandir : " + record["alt"]})
            img = doc.new_tag("img", src="/" + record["path"], alt=record["alt"], loading="lazy", decoding="async")
            if record.get("width") and record.get("height"):
                img["width"], img["height"] = record["width"], record["height"]
            full_size.append(img)
            figure.append(full_size)
            caption = doc.new_tag("figcaption")
            for node in list(BeautifulSoup(record["caption_html"], "html.parser").contents):
                caption.append(node)
            figure.append(caption)
            aside.append(figure)
        article.insert_after(aside)
        main["class"] = list(dict.fromkeys(main.get("class", []) + ["portal-layout"]))
    return str(doc), [r["id"] for r in chosen]


def decorate_pages(out):
    records = load_catalog()
    illustrated = 0
    for path in sorted(out.rglob("*.html")):
        if path.relative_to(out).parts[0] in ("rubriques", "recherche"):
            continue
        source = path.read_text(encoding="utf-8")
        result, selected = decorate_document(source, path, out, records)
        if result != source:
            path.write_text(result, encoding="utf-8")
        illustrated += bool(selected)
    return illustrated
