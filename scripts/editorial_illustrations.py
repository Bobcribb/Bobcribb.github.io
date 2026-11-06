"""Documented local images from titles and explicitly named scholarly sections.

No content-wide keyword fallback, unverified external media, old 2.5D assets
or indiscriminate image placement. An empty selection is a valid result.
"""
from html import escape
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import unicodedata

from bs4 import BeautifulSoup

CATALOG = Path(__file__).with_name("editorial_media.json")
DIAGRAM_CATALOG = Path(__file__).with_name("editorial_diagrams.json")
PLACEMENT_CATALOG = Path(__file__).with_name("editorial_placements.json")
RECON_SELECTIONS = Path(__file__).with_name("editorial_reconstitutions.json")
RECON_CATALOG = Path(__file__).resolve().parents[1] / "assets/reconstitutions-3d/catalogue-photorealiste.json"
GENERATED_CLASSES = {"mythos-home-illustrations", "mythos-visual-rail"}
MAX_ADDED_IMAGES = 12
MAX_INLINE_IMAGES = 8


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


def documented_reconstructions():
    """Use existing MYTHOS panoramas only, with their individual scientific notices."""
    curated = json.loads(RECON_SELECTIONS.read_text(encoding="utf-8"))["subjects"]
    inventory = json.loads(RECON_CATALOG.read_text(encoding="utf-8"))["entries"]
    by_slug = {item["slug"]: item for item in inventory}
    if len(by_slug) != len(inventory):
        raise ValueError("Identifiants 3D dupliqués dans le catalogue")
    result = []
    for slug, subjects in curated.items():
        item = by_slug.get(slug)
        if not item or not subjects:
            raise ValueError("Notice photoréaliste manquante : " + slug)
        kind = item["type"].casefold()
        if any(old in kind for old in ("planche ancienne", "antérieure conservée", "2,5d")):
            raise ValueError("Ancienne image 2,5D interdite : " + slug)
        src = item["src"]
        if src != "/assets/reconstitutions-3d/" + slug + ".webp":
            raise ValueError("Chemin 3D imprévu : " + slug)
        if not item["source_url"].startswith("https://"):
            raise ValueError("Source archéologique 3D manquante : " + slug)
        for field in ("title", "caption", "period", "certainty", "commentary"):
            if not str(item.get(field, "")).strip():
                raise ValueError("Notice 3D incomplète : " + slug)
        caption = (
            "<strong>Reconstitution numérique photoréaliste MYTHOS : hypothèse, "
            "ni photographie ni relevé métrique.</strong> "
            + escape(item["caption"]) + " "
            + "<strong>Période évoquée :</strong> " + escape(item["period"]) + ". "
            + "<strong>Degré de certitude :</strong> " + escape(item["certainty"]) + ". "
            + '<a href="' + escape(item["source_url"], quote=True) + '">Référence archéologique ou scientifique</a> ; '
            + '<a href="/reconstitutions-photorealistes.html#' + escape(slug, quote=True)
            + '">notice détaillée et limites de la restitution</a>.'
        )
        result.append({
            "id": "mythos-reconstitution-" + slug,
            "path": src.lstrip("/"),
            "subjects": subjects,
            "alt": "Reconstitution 3D interprétative et non métrique : " + item["title"],
            "caption_html": caption,
            "width": item["width"],
            "height": item["height"],
        })
    return result


def load_catalog():
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["media"]
    records.extend(documented_reconstructions())
    records.extend(json.loads(DIAGRAM_CATALOG.read_text(encoding="utf-8"))["media"])
    ids = set()
    for record in records:
        if record["id"] in ids:
            raise ValueError("Illustration dupliquée : " + record["id"])
        ids.add(record["id"])
        rel = Path(record["path"])
        allowed_root = (
            rel.parts[:1] == ("media",)
            or rel.parts[:2] in (("assets", "illustrations-articles"), ("assets", "reconstitutions-3d"), ("assets", "iconographie"))
        )
        if rel.is_absolute() or ".." in rel.parts or not allowed_root:
            raise ValueError("Média non local : " + str(rel))
        if rel.parts[:2] == ("assets", "iconographie"):
            allowed = {Path(item["path"]).name for item in
                       json.loads(DIAGRAM_CATALOG.read_text(encoding="utf-8"))["media"]}
            if rel.suffix != ".svg" or rel.name not in allowed or "2.5d" in rel.name.lower():
                raise ValueError("Schéma non documentaire interdit : " + str(rel))
        if rel.parts[:2] == ("assets", "reconstitutions-3d") and rel.suffix != ".webp":
            raise ValueError("Reconstitution SVG ou fichier non WebP interdit : " + str(rel))
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


def make_figure(doc, record, inline=False):
    """A documented object, preserving its existing caption and provenance."""
    attrs = {"data-media-id": record["id"]}
    if inline:
        attrs.update({"class": "mythos-editorial-inline", "data-editorial-inline": "subject-v3"})
    figure = doc.new_tag("figure", attrs=attrs)
    link = doc.new_tag("a", href="/" + record["path"], attrs={"aria-label": "Agrandir : " + record["alt"]})
    img = doc.new_tag("img", src="/" + record["path"], alt=record["alt"], loading="lazy", decoding="async")
    if record.get("width") and record.get("height"):
        img["width"], img["height"] = record["width"], record["height"]
    link.append(img)
    figure.append(link)
    caption = doc.new_tag("figcaption")
    for node in list(BeautifulSoup(record["caption_html"], "html.parser").contents):
        caption.append(node)
    figure.append(caption)
    return figure


def eligible_paragraph(p):
    # Archived WordPress prose is immutable: add images outside its protected block.
    if p.find_parent(class_="mythos-original-study"):
        return False
    if len(p.get_text(" ", strip=True)) < 100:
        return False
    if p.find_parent(("figure", "aside", "blockquote", "li", "nav", "footer")):
        return False
    return not any(
        getattr(parent, "name", None) and parent.has_attr("data-reading-owned")
        for parent in p.parents
    )


def editorial_paragraphs(article):
    """Only substantive authored paragraphs, never toolbar, quotations or captions."""
    return [p for p in article.find_all("p") if eligible_paragraph(p)]


def matching_subject(source, record):
    subject = " " + normalized(source) + " "
    return any(" " + normalized(term) + " " in subject for term in record["subjects"])


def section_anchor(heading):
    """First substantial paragraph before the next chapter or section heading."""
    for node in heading.next_elements:
        if getattr(node, "name", None) in ("h1", "h2", "h3"):
            break
        if getattr(node, "name", None) == "p" and eligible_paragraph(node):
            return node
    return None


def section_heading_ok(heading):
    if heading.find_parent(class_="mythos-original-study"):
        return False
    if heading.find_parent(("nav", "aside", "figure", "blockquote", "footer")):
        return False
    words = normalized(heading.get_text(" ", strip=True)).split()
    words = [w for w in words if not w.isdigit()]
    # A cross-reference is not evidence that its entire article depicts that
    # object. Named primary subsections are eligible; comparative detours aren't.
    excluded = {"comparaison", "comparer", "comparative", "comparatif",
                "parallele", "paralleles", "bibliographie", "sources",
                "conclusion", "notes", "references", "annexe", "annexes",
                "rapprochement", "rapprochements"}
    return bool(words) and not any(w in excluded for w in words[:3])


def select_section_media(path, article, out, records, primary):
    """One relevant source-backed object per explicitly named subsection."""
    if "chapitres" not in path.parts or len(primary) >= MAX_ADDED_IMAGES:
        return [], {}
    present = {image_key(img.get("src", "")) for img in article.find_all("img")}
    for record in primary:
        present.add(image_key(record["path"]))
        present.update(image_key(url) for url in record.get("equivalents", []))
    selected, anchors = [], {}
    for heading in article.find_all(("h2", "h3")):
        if not section_heading_ok(heading):
            continue
        anchor = section_anchor(heading)
        if anchor is None:
            continue
        heading_title = heading.get_text(" ", strip=True)
        for record in records:
            if not matching_subject(heading_title, record):
                continue
            keys = {image_key(record["path"])}
            keys.update(image_key(url) for url in record.get("equivalents", []))
            if present.intersection(keys) or not (out / record["path"]).is_file():
                continue
            selected.append(record)
            anchors[record["id"]] = anchor
            present.update(keys)
            break
        if len(primary) + len(selected) >= MAX_ADDED_IMAGES:
            break
    return selected, anchors


def positioned_illustrations(path, article, records):
    """Use only explicit page-specific subject-to-section placements."""
    if not PLACEMENT_CATALOG.is_file():
        return {}
    rules = json.loads(PLACEMENT_CATALOG.read_text(encoding="utf-8")).get("pages", {}).get(path.name, {})
    if not rules:
        return {}
    selected = {record["id"] for record in records}
    anchors = {}
    for media_id, heading_excerpt in rules.items():
        if media_id not in selected:
            continue
        excerpt = normalized(heading_excerpt)
        for heading in article.find_all(("h2", "h3")):
            if section_heading_ok(heading) and excerpt in normalized(heading.get_text(" ", strip=True)):
                anchor = section_anchor(heading)
                if anchor is not None:
                    anchors[media_id] = anchor
                break
    return anchors


def decorate_document(source, path, out, records):
    doc = BeautifulSoup(source, "html.parser")
    main = doc.find("main")
    article = (main.find("article") or (main if "philo-work" in main.get("class", []) else None)) if main else None
    if not article:
        return source, []

    removed = False
    for figure in article.select('figure[data-editorial-inline="subject-v3"]'):
        if "mythos-editorial-inline" in figure.get("class", []):
            figure.decompose()
            removed = True
    for aside in main.find_all("aside", recursive=False):
        if GENERATED_CLASSES.intersection(aside.get("class", [])):
            aside.decompose()
            removed = True
    if removed or "visual-rails-active" in main.get("class", []):
        classes = [c for c in main.get("class", []) if c not in ("visual-rails-active", "portal-layout")]
        if article.select_one(".portal-section, .hero-editorial"):
            classes.append("portal-layout")
        main["class"] = classes
    if doc.head and not doc.select_one('link[href="/assets/mythos-refonte.css"]'):
        doc.head.append(doc.new_tag("link", rel="stylesheet", href="/assets/mythos-refonte.css"))

    primary = select_media(path, article, out, records)
    scoped, anchors = select_section_media(path, article, out, records, primary)
    chosen = (primary + scoped)[:MAX_ADDED_IMAGES]
    paragraphs = editorial_paragraphs(article)
    inline_count = min(len(chosen), MAX_INLINE_IMAGES, len(paragraphs),
                       max(1, len(paragraphs) // 2)) if paragraphs else 0

    # First place section-specific documentary figures alongside their actual
    # subsection; distribute title-backed images across remaining paragraphs.
    inline_records = (scoped + primary)[:inline_count]
    anchors.update(positioned_illustrations(path, article, inline_records))
    used_paragraphs = set()
    for record in inline_records:
        anchor = anchors.get(record["id"])
        if anchor is not None and id(anchor) not in used_paragraphs:
            used_paragraphs.add(id(anchor))
            anchor.insert_after(make_figure(doc, record, inline=True))

    global_records = [record for record in inline_records if record["id"] not in anchors
                      or id(anchors[record["id"]]) not in used_paragraphs]
    for i, record in enumerate(global_records):
        index = ((2 * i + 1) * len(paragraphs)) // (2 * len(global_records))
        target = None
        for offset in range(len(paragraphs)):
            for j in (index + offset, index - offset):
                if 0 <= j < len(paragraphs) and id(paragraphs[j]) not in used_paragraphs:
                    target = paragraphs[j]
                    break
            if target is not None:
                break
        if target is not None:
            used_paragraphs.add(id(target))
            target.insert_after(make_figure(doc, record, inline=True))

    inline_ids = {record["id"] for record in inline_records}
    remaining = [record for record in chosen if record["id"] not in inline_ids]
    if remaining:
        aside = doc.new_tag("aside", attrs={
            "class": "mythos-home-illustrations mythos-bottom-gallery",
            "data-editorial-gallery": "subject-v4",
            "aria-label": "Documents en rapport avec le sujet"
        })
        heading = doc.new_tag("h2")
        heading.string = "Documents iconographiques complémentaires" if inline_count else "Documents iconographiques"
        aside.append(heading)
        for record in remaining:
            aside.append(make_figure(doc, record))
        if article is main:
            main.append(aside)
        else:
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
