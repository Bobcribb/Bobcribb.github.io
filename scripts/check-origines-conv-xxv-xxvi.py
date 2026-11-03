#!/usr/bin/env python3
"""Validation du texte intégral ODS-CONV-XXV/XXVI, sans dépendance externe."""
from __future__ import annotations
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus/origines-du-sacre"
ITEMS = (("XXV", 339, 346, 45000), ("XXVI", 347, 354, 34000))
CHAPTER = re.compile(r"^#\s+CHAPITRE\s+(3\d{2})\s+—\s+(.+)$", re.I | re.M)

class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_pre = False
        self.pre: list[str] = []
        self.current: list[str] = []
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(attr["id"])
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag == "pre" and "reader-transcription" in attr.get("class", "").split():
            assert not self.in_pre, "Unclosed <pre>"
            self.in_pre = True
            self.current = []

    def handle_endtag(self, tag):
        if tag == "pre" and self.in_pre:
            self.pre.append("".join(self.current))
            self.in_pre = False

    def handle_data(self, data):
        if self.in_pre:
            self.current.append(data)


def run():
    for volume, first, last, min_bytes in ITEMS:
        basename = f"conv-tome-{volume}-chapitres-{first}-{last}"
        source_path, reader_path = BASE / (basename + ".md"), BASE / (basename + ".html")
        raw = source_path.read_bytes()
        assert len(raw) > min_bytes, f"Manuscrit trop court : {source_path}"
        src = raw.decode("utf-8")
        parsed = Reader()
        parsed.feed(reader_path.read_text(encoding="utf-8"))
        assert not parsed.in_pre
        ch = list(CHAPTER.finditer(src))
        assert [int(m.group(1)) for m in ch] == list(range(first, last + 1)), f"Chapitres incomplets : {volume}"
        expected_transcription = src[:ch[0].start()]
        for idx, m in enumerate(ch):
            end = ch[idx + 1].start() if idx + 1 < len(ch) else len(src)
            block = src[m.start():end]
            assert "\n" in block
            expected_transcription += block.split("\n", 1)[1]
            assert f"chapitre-{m.group(1)}" in parsed.ids, f"Ancre absente : {m.group(1)}"
            assert f"#chapitre-{m.group(1)}" in parsed.links, f"Lien de sommaire absent : {m.group(1)}"
        actual = "".join(parsed.pre)
        assert actual == expected_transcription, (
            f"Troncature, substitution ou écart de transcription : {volume}, "
            f"{len(actual)} caractères lus contre {len(expected_transcription)} attendus"
        )
        assert "bibliographie" in src.lower() and "bibliographie" in parsed.ids
        assert "conclusion" in parsed.ids
        for link in parsed.links:
            if link.startswith("#"):
                assert link[1:] in parsed.ids, f"Ancre morte {volume}: {link}"
                continue
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path.endswith((".md", ".html")):
                continue
            target = ROOT / unquote(url.path.lstrip("/")) if link.startswith("/") else reader_path.parent / unquote(url.path)
            assert target.is_file(), f"Lien local cassé : {volume} / {link}"
        print(f"ODS-CONV-{volume}: {len(raw)} octets, {len(ch)} chapitres, "
              f"transcription intégrale confirmée, SHA-256 {sha256(raw).hexdigest()}")
    for section in ("origines-du-sacre.html", "sommaire-general.html", "corpus/sommaire-general.md"):
        s = (ROOT / section).read_text(encoding="utf-8")
        for volume, first, last, _ in ITEMS:
            assert f"conv-tome-{volume}-chapitres-{first}-{last}.html" in s, (
                f"Lien du tome {volume} manquant dans {section}"
            )
    previous = (BASE / "conv-tome-XXVII-chapitres-355-362.html").read_text(encoding="utf-8")
    assert "conv-tome-XXVI-chapitres-347-354.html" in previous
    print("Sommaires, collection et navigation XXVI ↔ XXVII contrôlés.")


if __name__ == "__main__":
    run()
