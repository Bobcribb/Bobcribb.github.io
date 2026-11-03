#!/usr/bin/env python3
"""Contrôle d'intégrité des 22 sections de Gēras, sans source extérieure."""
from pathlib import Path
import hashlib
import re
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"corpus/theatre-grec/comedies"
BLOB="cacecbb6b24cfb736e33b4dbd092b7bb9c4b82a3"
raw=(D/"geras-source.md").read_bytes()
assert hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()==BLOB,"Source Git altérée"
source=raw.decode("utf-8")
front=re.match(r"\A---\n.*?\n---\n\n",source,re.S)
assert front,"Métadonnées initiales absentes"
body=source[front.end():]
heads=list(re.finditer(r"^### (\d+)\. (.+)$",body,re.M))
assert [int(m.group(1)) for m in heads]==list(range(1,23))
assert [int(m.group(1)) for m in heads if "[C]" in m.group(2)]==[17,18,19]
study=(D/"geras-etude.html").read_text(encoding="utf-8")
scenes=(D/"geras-scenes-modernes.html").read_text(encoding="utf-8")
def norm(s):return " ".join(s.split())
def markdown_text(s):
    s=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",s)
    s=re.sub(r"^#{1,3} ","",s,flags=re.M)
    s=re.sub(r"^-\s","",s,flags=re.M)
    s=re.sub(r"^---\s*$","",s,flags=re.M)
    return norm(s.replace("**","").replace("*",""))
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.strings=[];self.ids=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        at=dict(attrs)
        if "id" in at:self.ids.append(at["id"])
        if tag=="a":self.links.append(at.get("href",""))
    def handle_data(self,data):self.strings.append(data)
    def handle_endtag(self,tag):
        if tag in ("p","li","h1","h2","h3","ul","hr"):self.strings.append(" ")
def visible(s):
    p=Inspect();p.feed(s);return norm("".join(p.strings))
intro=body[:heads[0].start()]
found=re.search(r'<div class="ger-intro" data-source-intro="true">([\s\S]*?)</div>',study)
assert found and markdown_text(intro)==visible(found.group(1)),"Préambule altéré"
for i,m in enumerate(heads):
    n=i+1
    text=body[m.end():(heads[i+1].start() if i<21 else len(body))].strip()
    page=scenes if 17<=n<=19 else study
    part=re.search(r'<section id="section-'+str(n)+r'" class="ger-section"[\s\S]*?<div class="ger-prose">([\s\S]*?)</div></section>',page)
    assert part,f"Section {n} absente"
    assert markdown_text(text)==visible(part.group(1)),f"Texte {n} altéré"
assert study.count('class="ger-section"')==19 and scenes.count('class="ger-section"')==3
assert 'id="bibliographie"' in study and 'id="bibliographie"' not in scenes
for page in (study,scenes):
    reader=Inspect();reader.feed(page)
    assert len(reader.ids)==len(set(reader.ids)),"Ancres en double"
    assert BLOB in page
    for name in ("geras-source.md","geras-etude.html","geras-scenes-modernes.html","theatre-grec.html","sommaire-general.html"):
        assert name in page,name
    for link in reader.links:
        if link.startswith("#"):assert link[1:] in reader.ids,link
for page in ("index.html","theatre-grec.html","philosophie.html","sommaire-general.html"):
    assert "geras-etude.html" in (ROOT/page).read_text(encoding="utf-8"),page
assert "geras-scenes-modernes.html" in (ROOT/"theatre-grec.html").read_text(encoding="utf-8")
print("OK Gēras : SHA blob, préambule, 22/22 sections intactes, 19/3, bibliographie, liens et sommaires.")
