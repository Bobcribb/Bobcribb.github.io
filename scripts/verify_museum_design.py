#!/usr/bin/env python3
"""Verify universal coverage and preservation of representative legacy readers."""
from pathlib import Path
from collections import Counter
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
import shutil
from apply_museum_design import apply

ROOT=Path(__file__).resolve().parents[1]

def prose(doc):
    return Counter(p.get_text(' ',strip=True) for p in doc.select('main p, article p, main li, article li, main h2, main h3, article td, main figcaption') if p.get_text(' ',strip=True))

def verify():
    fixtures=['philosophie-iliade.html','philosophie-odyssee.html','philosophie-theogonie.html','corpus/civilisations/perse-iran-ancien-behistun.html','corpus/mythologie-grecque/archives/livre-troie.html']
    with TemporaryDirectory() as tmp:
        dest=Path(tmp)
        before={}
        for name in fixtures:
            p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,p)
            before[name]=prose(BeautifulSoup(p.read_text(),'html.parser'))
        assert apply(dest)==len(fixtures)
        snapshots={}
        for name in fixtures:
            p=dest/name;d=BeautifulSoup(p.read_text(),'html.parser')
            assert not before[name]-prose(d),f'Prose lost in {name}'
            assert len(d.select('.mythos-banner'))==1
            assert len(d.select('.mythos-masthead'))==1
            assert len(d.select('link[href*="mythos-museum.css"]'))==1
            snapshots[name]=p.read_text()
        apply(dest)
        for name in fixtures:
            d=BeautifulSoup((dest/name).read_text(),'html.parser')
            assert not before[name]-prose(d),f'Prose lost on rebuild in {name}'
            assert len(d.select('.mythos-banner'))==1
            assert len(d.select('.mythos-masthead'))==1
    print('OK : prose, tables, illustrations et liens conservés dans cinq lecteurs ; transformation répétable.')
    out=ROOT/'_site'
    pages=0;redirects=0
    for p in out.rglob('*.html'):
        raw=p.read_text()
        if 'http-equiv="refresh"' in raw.lower() or "http-equiv='refresh'" in raw.lower():
            redirects+=1;continue
        assert 'data-mythos-design="20261104"' in raw,str(p)
        assert raw.count('class="mythos-masthead"')==1,str(p)
        assert raw.count('/assets/mythos-museum.css?')==1,str(p)
        pages+=1
    assert pages>1000
    d=BeautifulSoup((out/'origines-du-sacre/index.html').read_text(),'html.parser')
    assert len(d.select('.origins-volume'))==27
    assert len(d.select('.mythos-more-volumes .origins-volume'))==15
    assert (out/'assets/mythos-museum-banner.webp').stat().st_size>10000
    print(f'OK : {pages} pages habillées, {redirects} redirections conservées, 27 tomes accessibles.')

if __name__=='__main__':verify()
