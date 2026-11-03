#!/usr/bin/env python3
"""Vérification éditoriale de Triphalēs XXXIII : copie, 22 sections et navigation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,re
root=Path(__file__).resolve().parents[1]
folder=root/"corpus/theatre-grec/comedies"
blob="d59cac3b1838b36b3879e9bcfd4f12c9e4bc7ad4"
data=(folder/"triphales-source.md").read_bytes()
assert hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()==blob,"Blob source différent"
source=data.decode("utf-8")
front=re.match(r"\A---\n.*?\n---\n\n",source,re.S)
assert front,"Métadonnées absentes"
body=source[front.end():]
headings=list(re.finditer(r"^### (\d+)\. (.+)$",body,re.M))
assert [int(h.group(1)) for h in headings]==list(range(1,23)),"22 sections attendues"
assert [int(h.group(1)) for h in headings if "[C]" in h.group(2)]==[18,19,20]
study=(folder/"triphales-etude.html").read_text(encoding="utf-8")
scenes=(folder/"triphales-scenes-modernes.html").read_text(encoding="utf-8")
def norm(s):return " ".join(s.split())
def mdtext(s):
    s=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",s)
    s=re.sub(r"^#{1,3} ","",s,flags=re.M)
    s=re.sub(r"^-\s","",s,flags=re.M)
    s=re.sub(r"^---\s*$","",s,flags=re.M)
    return norm(s.replace("**","").replace("*",""))
class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.words=[];self.ids=[];self.links=[]
    def handle_data(self,d):self.words.append(d)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d:self.ids.append(d["id"])
        if tag=="a":self.links.append(d.get("href",""))
    def handle_endtag(self,tag):
        if tag in ("p","li","h1","h2","h3","ul","hr"):self.words.append(" ")
def visible(s):
    p=Reader();p.feed(s);return norm("".join(p.words))
pre=body[:headings[0].start()]
intro=re.search(r'<div data-source-intro="true">([\s\S]*?)</div>',study)
assert intro and mdtext(pre)==visible(intro.group(1)),"Préambule tronqué"
for i,m in enumerate(headings):
    n=i+1
    end=headings[i+1].start() if i<21 else len(body)
    raw=body[m.end():end].strip()
    page=scenes if 18<=n<=20 else study
    part=re.search(r'<section id="sec-'+str(n)+r'" data-source-section="'+str(n)+r'"><h2>[\s\S]*?</h2>([\s\S]*?)</section>',page)
    assert part and mdtext(raw)==visible(part.group(1)),f"Section {n} différente"
assert study.count("data-source-section=")==19 and scenes.count("data-source-section=")==3
assert 'id="sec-22"' in study and 'id="sec-22"' not in scenes
assert "Poetae Comici Graeci" in study and "Sources et bibliographie" in study
for page in (study,scenes):
    r=Reader();r.feed(page)
    assert len(r.ids)==len(set(r.ids)),"Ancres dupliquées"
    assert blob in page
    for target in ("triphales-source.md","triphales-etude.html","triphales-scenes-modernes.html","theatre-grec.html","sommaire-general.html"):
        assert target in page,target
    for href in r.links:
        if href.startswith("#"):assert href[1:] in r.ids,href
for f in ("index.html","theatre-grec.html","philosophie.html","sommaire-general.html"):
    assert "triphales-etude.html" in (root/f).read_text(encoding="utf-8"),f
assert "triphales-scenes-modernes.html" in (root/"theatre-grec.html").read_text(encoding="utf-8")
assert "triphales-etude.html" in (folder/"ploutos-protos-etude.html").read_text(encoding="utf-8")
print("OK Triphalēs : source SHA, préambule, 22 sections intactes, 19/3, bibliographie et liens.")
