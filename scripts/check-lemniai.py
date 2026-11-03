#!/usr/bin/env python3
"""Audit de fidélité du transfert Lemniai : volume historique XXX."""
from pathlib import Path
import hashlib
import html
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus/theatre-grec/comedies"
SRC = BASE / "lemniai-source.md"
STUDY = BASE / "lemniai-etude.html"
SCENES = BASE / "lemniai-scenes-modernes.html"
SOURCE_BLOB = "92ea495425566b16125151268f07729478b9d0ec"

raw = SRC.read_bytes()
git_sha = hashlib.sha1(f"blob {len(raw)}\0".encode().replace(b"\0", b"\0") + raw).hexdigest()
assert git_sha == SOURCE_BLOB, f"Manuscrit modifié : {git_sha} != {SOURCE_BLOB}"
source = raw.decode("utf-8")
study = STUDY.read_text(encoding="utf-8")
scenes = SCENES.read_text(encoding="utf-8")
headings = list(re.finditer(r"^### (\d+)\. (.+)$", source, re.M))
assert len(headings) == 22, f"22 sections attendues, trouvé {len(headings)}"
assert [int(m.group(1)) for m in headings] == list(range(1, 23))
assert [int(m.group(1)) for m in headings if "[C]" in m.group(2)] == [17, 18, 19]

def normalize(s):
    return " ".join(s.split())

def markdown_plain(s):
    s = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "")
    s = re.sub(r"(?<!\w)\*(?=\S)|(?<=\S)\*(?!\w)", "", s)
    s = re.sub(r"^---+$", "", s, flags=re.M)
    s = re.sub(r"^-\s", "", s, flags=re.M)
    return normalize(s.replace("`", ""))

def html_plain(s):
    s = re.sub(r"</(?:p|li|ul|h2|h3)>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return normalize(html.unescape(s))

for i, heading in enumerate(headings):
    n = i + 1
    original = source[heading.end():headings[i+1].start() if i+1 < 22 else len(source)].strip()
    target = scenes if 17 <= n <= 19 else study
    match = re.search(r'<section id="section-' + str(n) +
                      r'"[^>]*>\s*<h2[^>]*>[\s\S]*?</h2><div class="dai-prose">([\s\S]*?)</div></section>', target)
    assert match, f"Section {n} absente du bon lecteur"
    assert markdown_plain(original) == html_plain(match.group(1)), f"Texte altéré à la section {n}"

assert study.count('class="lem-section"') == 19
assert scenes.count('class="lem-section"') == 3
assert 'id="bibliographie"' in study
assert 'id="bibliographie"' not in scenes
for filename, page in (("lemniai-etude.html", study), ("lemniai-scenes-modernes.html", scenes)):
    assert SOURCE_BLOB in page
    for dest in ("lemniai-source.md", "lemniai-etude.html", "lemniai-scenes-modernes.html", "/theatre-grec.html", "/sommaire-general.html"):
        assert dest in page, f"Manque lien {dest} dans {filename}"
    for anchor in re.findall(r'href="#(section-\d+)"', page):
        assert f'id="{anchor}"' in page, f"Ancre sans cible {anchor}"
for index in ("theatre-grec.html", "philosophie.html", "sommaire-general.html", "index.html"):
    assert "lemniai-etude.html" in (ROOT / index).read_text(encoding="utf-8"), index
assert "lemniai-scenes-modernes.html" in (ROOT / "theatre-grec.html").read_text(encoding="utf-8")
print("OK : manuscrit original intact ; 22/22 sections identiques en texte lisible ; 19/3 ; bibliographie ; sommaires et liens vérifiés.")
