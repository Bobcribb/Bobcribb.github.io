#!/usr/bin/env python3
"""Fail GitHub Pages if Holkades loses source text, sections, or navigation.
Pure Python 3 standard library; source remains the immutable manuscript.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus/theatre-grec/comedies"
EXPECTED_BLOB = "775999ca4ba7bbeb668802eb8b7dfc7f56643a93"
SCENES = {15, 16, 17}
NUMBERS = set(range(1, 20))
HEADING = re.compile(r"^### (\d+)\. (.+)$", re.M)


def normal(s: str) -> str:
    return " ".join(s.split())


def visible_md(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"^#{1,6} +", "", s, flags=re.M)
    s = re.sub(r"^- +", "", s, flags=re.M)
    s = re.sub(r"^---[ \t]*$", "", s, flags=re.M)
    return normal(s.replace("*", ""))


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.prose: dict[str, list[str]] = {}
        self.heads: dict[str, list[str]] = {}
        self.current: str | None = None
        self.capture = False
        self.capture_heading = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, "Duplicate HTML ID: " + a["id"]
            self.ids.add(a["id"])
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "section":
            n = a.get("data-source-section")
            if n is not None:
                self.current = n
            elif a.get("data-source-intro") == "true":
                self.current = "intro"
        if tag == "h2" and self.current not in {None, "intro"}:
            self.heads[self.current] = []
            self.capture_heading = True
        if tag == "div" and self.current and "dai-prose" in a.get("class", "").split():
            assert self.current not in self.prose, "Repeated source block " + self.current
            self.capture = True
            self.prose[self.current] = []
        if tag == "hr" and self.capture:
            self.prose[self.current].append("\n")

    def handle_data(self, data):
        if self.capture and self.current:
            self.prose[self.current].append(data)
        if self.capture_heading and self.current:
            self.heads[self.current].append(data)

    def handle_endtag(self, tag):
        if self.capture and tag in {"p", "li", "h2", "h3", "h4", "ul"}:
            self.prose[self.current].append("\n")
        if tag == "h2":
            self.capture_heading = False
        if tag == "div" and self.capture:
            self.capture = False
        if tag == "section":
            self.current = None


def main():
    data = (BASE / "holkades-source.md").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert blob == EXPECTED_BLOB, "Source changed; cannot certify exact copy"
    manuscript = data.decode("utf-8")
    front = re.match(r"\A---\n.*?\n---\n", manuscript, re.S)
    assert front, "Source metadata missing"
    matches = list(HEADING.finditer(manuscript))
    assert [int(m.group(1)) for m in matches] == list(range(1, 20))
    assert all(("[C]" in m.group(2)) == (int(m.group(1)) in SCENES) for m in matches)
    assert "Bibliographie et contrôle des sources" in matches[-1].group(2)
    preamble = manuscript[front.end():matches[0].start()]
    parts = {
        m.group(1): manuscript[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(manuscript)]
        for i, m in enumerate(matches)
    }
    pages = {}
    all_sections = []
    for kind in ("etude", "scenes-modernes"):
        page = BASE / ("holkades-" + kind + ".html")
        assert page.is_file(), "Missing reader: " + str(page)
        raw = page.read_text("utf-8")
        assert "775999ca4ba7bbeb668802eb8b7dfc7f56643a93" in raw
        assert "/assets/mythos-theatre.css" in raw and 'class="dai-hero"' in raw
        parser = Collector()
        parser.feed(raw)
        pages[kind] = parser
        required = NUMBERS - SCENES if kind == "etude" else SCENES
        assert {int(x) for x in parser.prose if x != "intro"} == required, "Section partition"
        assert set(parser.heads) == {str(n) for n in required}, "Section headings missing"
        for num in required:
            k = str(num)
            expected = visible_md(parts[k])
            actual = normal("".join(parser.prose[k]))
            assert actual == expected, "Text loss/change in " + kind + " section " + k
            expected_heading = visible_md(k + ". " + matches[num - 1].group(2))
            assert normal("".join(parser.heads[k])) == expected_heading
            all_sections.append(num)
        if kind == "etude":
            assert normal("".join(parser.prose["intro"])) == visible_md(preamble), "Preamble altered"
            assert "bibliographie" in parser.ids, "Bibliography anchor missing"
        else:
            assert "intro" not in parser.prose, "Duplicate preamble"
        for href in parser.links:
            u = urlsplit(href)
            if href.startswith("#"):
                assert u.fragment in parser.ids, "Missing anchor: " + href
            if href.startswith("/"):
                dest = ROOT / unquote(u.path).lstrip("/") if u.path != "/" else ROOT / "index.html"
                assert dest.is_file(), "Broken local file link: " + href
    assert sorted(all_sections) == list(range(1, 20)), "Missing/duplicated source section"
    for kind in ("etude", "scenes-modernes"):
        other = "scenes-modernes" if kind == "etude" else "etude"
        hrefs = pages[kind].links
        assert any("holkades-" + other + ".html" in h for h in hrefs), "Missing counterpart"
        assert any("holkades-source.md" in h for h in hrefs), "Missing source link"
        assert any("aiolosikon-etude.html" in h for h in hrefs), "Missing previous volume link"
    for page in ("theatre-grec.html", "philosophie.html", "sommaire-general.html", "index.html"):
        assert "holkades-etude.html" in (ROOT / page).read_text("utf-8"), "Missing index: " + page
    assert "holkades-etude.html" in (BASE / "aiolosikon-etude.html").read_text("utf-8"), "Broken reverse cycle link"
    report = {
        "source_repository": "Bobcribb/Bobcribb.github.io",
        "source_path": "chapitres/comedies/volume-029-aristophane-holkades.md",
        "source_git_blob": blob,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_bytes": len(data),
        "source_characters": len(manuscript),
        "source_lines": len(manuscript.splitlines()),
        "critical_sections": 16,
        "modern_scenes": 3,
        "sections_verified_identical_in_readable_text": 19,
        "preamble_verified_identical_in_readable_text": True,
        "local_links_verified": True,
        "scientific_collation": "Not exhaustive; check Kassel-Austin before claiming new fragment attributions."
    }
    (BASE / "holkades-controle.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print("Holkades: 19/19 source sections preserved, HTML and navigation valid.")


if __name__ == "__main__":
    main()
