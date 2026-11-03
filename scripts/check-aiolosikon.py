#!/usr/bin/env python3
"""Audit MYTHOS Aiolosikon XXVIII: byte-exact source, readable text, links.
Uses only Python standard library; fails GitHub Pages before deployment on loss.
"""
from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus/theatre-grec/comedies"
BLOB_SHA1 = "e4b75423fe8691c74594b31b4af5a158da64b947"
ROMAN = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII".split()
CREATIVE = {"XIII", "XIV"}
HEADING = re.compile(r"^### ([IVX]+)\.\s+(.+)$", flags=re.M)
SECTION = {v.lower(): v for v in ROMAN}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def readable_markdown(text: str) -> str:
    """Text visible when rendering the small Markdown subset in this source."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("*", "")
    text = re.sub(r"^-\s+", "", text, flags=re.M)
    text = re.sub(r"^---\s*$", "", text, flags=re.M)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    return normalize(text)


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current = None
        self.collect = False
        self.sections = {}
        self.ids = set()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                raise AssertionError("Duplicate HTML id: " + a["id"])
            self.ids.add(a["id"])
        if tag == "section":
            k = a.get("id")
            self.current = k if k in {"preambule"} or k in {
                "section-" + i.lower() for i in ROMAN
            } else None
        if tag == "div" and "dai-prose" in a.get("class", "").split() and self.current:
            self.collect = True
            self.sections[self.current] = []
        if tag in {"a", "link"}:
            if a.get("href"):
                self.hrefs.append(a["href"])

    def handle_data(self, data):
        if self.collect:
            self.sections[self.current].append(data)

    def handle_endtag(self, tag):
        if self.collect and tag in {"p", "h1", "h2", "h3", "li", "br", "hr", "ul"}:
            self.sections[self.current].append(" ")
        elif tag == "div" and self.collect:
            self.collect = False
        if tag == "section":
            self.current = None


source = (BASE / "aiolosikon-source.md").read_bytes()
git_blob = hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + b"\0" + source).hexdigest()
assert git_blob == BLOB_SHA1, f"Manuscript changed: {git_blob}"
text = source.decode("utf-8")
matches = list(HEADING.finditer(text))
assert [m.group(1) for m in matches] == ROMAN, "Section sequence altered"
assert all(("[C]" in m.group(2)) == (m.group(1) in CREATIVE) for m in matches), "Misclassified section"
preface_end = re.match(r"\A---\n.*?\n---\n", text, flags=re.S)
assert preface_end is not None, "Missing YAML preamble"
preface = text[preface_end.end():matches[0].start()]
assert "Navigation" in preface and "Méthode" in preface
parts = {
    match.group(1): text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
    for i, match in enumerate(matches)
}
views = {}
for name in ("etude", "scenes-modernes"):
    path = BASE / f"aiolosikon-{name}.html"
    assert path.is_file() and path.stat().st_size > 4000, path
    parser = Reader()
    parser.feed(path.read_text(encoding="utf-8"))
    views[name] = parser
    expected = set(ROMAN) - CREATIVE if name == "etude" else CREATIVE
    actual = {SECTION[k.removeprefix("section-")] for k in parser.sections if k.startswith("section-")}
    assert actual == expected, (name, "Missing/duplicated section", actual)
    assert set(parser.sections) == {"section-" + i.lower() for i in expected} | (
        {"preambule"} if name == "etude" else set()
    ), "Incorrect number of readable blocks"
    for roman in expected:
        got = normalize("".join(parser.sections["section-" + roman.lower()]))
        want = readable_markdown(parts[roman])
        assert got == want, f"Source prose not fully preserved in {name} section {roman}"
    if name == "etude":
        assert normalize("".join(parser.sections["preambule"])) == readable_markdown(preface), "Preamble changed"
    for href in parser.hrefs:
        if href.startswith("#"):
            assert href[1:] in parser.ids, f"Broken local anchor {href}"
        elif href.startswith("/"):
            u = urlsplit(href)
            target = ROOT / unquote(u.path).lstrip("/")
            if u.path == "/":
                target = ROOT / "index.html"
            assert target.is_file(), f"Dead local file link in {name}: {href}"

combined = {x for p in views.values() for x in p.sections if x.startswith("section-")}
assert combined == {"section-" + i.lower() for i in ROMAN}
for page in ("theatre-grec.html", "philosophie.html", "sommaire-general.html", "index.html"):
    html = (ROOT / page).read_text(encoding="utf-8")
    assert "aiolosikon-etude.html" in html, f"Missing entry in {page}"
for name in ("etude", "scenes-modernes"):
    current = (BASE / f"aiolosikon-{name}.html").read_text(encoding="utf-8")
    other = "scenes-modernes" if name == "etude" else "etude"
    assert f"aiolosikon-{other}.html" in current, "Missing reciprocal link"
    assert "aiolosikon-source.md" in current, "Missing original manuscript link"
    assert "/assets/mythos-theatre.css" in current, "Missing black and gold styling"
    assert "dai-hero" in current and "dai-sidebar" in current, "Missing responsive reading layout"

report = {
    "source_blob_sha1": git_blob,
    "utf8_bytes": len(source),
    "sections_total": len(ROMAN),
    "critical_sections": len(ROMAN) - len(CREATIVE),
    "modern_scenes": len(CREATIVE),
    "rendered_sections_identical_to_source": len(ROMAN),
    "preamble_fidelity": True,
    "local_navigation": True,
    "sources_and_bibliography": "XVII, study",
    "scientific_collation_of_primary_texts": False,
}
(BASE / "aiolosikon-controle.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Aiolosikon XXVIII verified: 17/17 sections, original source and all navigation.")
