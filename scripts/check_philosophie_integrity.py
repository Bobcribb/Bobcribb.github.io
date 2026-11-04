"""Check source preservation and the three long philosophical studies.

Run after render_philosophie_a4.py. Does not claim to automate scholarly review.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
from lxml import html
from pypdf import PdfReader
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
baseline=json.loads((ROOT/'corpus/philosophie/reference-avant-extension.json').read_text())
pagination=json.loads((ROOT/'assets/philosophie/pagination-2026-11-04.json').read_text())
normalize=lambda e:' '.join(e.text_content().split())
digest=lambda value:hashlib.sha256(value.encode()).hexdigest()
seen={}
results={}
for image in json.loads((ROOT/'assets/philosophie/documents/manifest.json').read_text()):
    path=ROOT/image['path'].lstrip('/')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==image['sha256'],('documentary image changed',image['path'])
for slug,source in baseline['sources'].items():
    path=ROOT/f'philosophie-{slug}.html'
    raw=path.read_text()
    doc=html.fromstring(raw)
    ids=doc.xpath('//@id')
    assert len(ids)==len(set(ids)),(slug,'duplicate HTML ids')
    for ident,sha in source['sections'].items():
        matches=doc.xpath('//*[@id=$ident]',ident=ident)
        assert len(matches)==1,(slug,'missing original section',ident)
        assert digest(normalize(matches[0]))==sha,(slug,'original text altered',ident)
    figures=doc.xpath('//main//figure')
    assert len(figures)>=len(source['figures']),(slug,'lost figure')
    for record in source['figures']:
        matches=[]
        for figure in figures:
            im=figure.xpath('.//img')[0]
            if (im.get('data-original-src') or im.get('src'))==record['src']:
                matches.append(figure)
        assert len(matches)==1,(slug,'figure absent or duplicated',record['src'])
        figure=matches[0];im=figure.xpath('.//img')[0]
        assert im.get('alt')==record['alt'],(slug,'original alt text changed')
        assert digest(normalize(figure.xpath('.//figcaption')[0]))==record['caption_sha256'],(slug,'caption changed')
    for image in doc.xpath('//main//img'):
        src=image.get('src')
        assert not urlparse(src).scheme,(slug,'remote image dependency',src)
        assert (ROOT/src.lstrip('/')).is_file(),(slug,'missing image',src)
    for a in doc.xpath('//a[starts-with(@href,"#")]'):
        assert a.get('href')[1:] in ids,(slug,'broken anchor',a.get('href'))
    chapters=doc.xpath('//section[contains(concat(" ",@class," ")," philo-long ")]')
    assert len(chapters)==24,(slug,'expected 24 developed chapters',len(chapters))
    words={}
    for chapter in chapters:
        assert chapter.xpath('./h2'),(slug,'missing chapter title')
        paragraphs=chapter.xpath('./p[not(@class)]')
        words[chapter.get('id')]=sum(len(normalize(p).split()) for p in paragraphs)
        assert words[chapter.get('id')]>=1600,(slug,'underdeveloped chapter',chapter.get('id'))
        assert chapter.xpath('.//*[contains(concat(" ",@class," ")," reference ")]'),(slug,'missing source reference')
        for p in paragraphs:
            text=normalize(p)
            assert not re.search(r'\b(?:TODO|TBD|lorem ipsum)\b',text,re.I),(slug,'placeholder')
            if len(text.split())>35:
                key=digest(text.casefold())
                assert key not in seen,(slug,'duplicated analytical paragraph',chapter.get('id'),seen.get(key))
                seen[key]=(slug,chapter.get('id'))
    item=pagination['studies'][slug]
    assert item['source_sha256']==digest(raw),(slug,'stale PDF evidence')
    assert item['analyse-seule_pages']>=100,(slug,'100-page analysis target not met')
    for label in ['etude','analyse-seule']:
        pdf=ROOT/f'assets/philosophie/pdf/{slug}-{label}-a4.pdf'
        reader=PdfReader(pdf)
        assert len(reader.pages)==item[label+'_pages'],(slug,'incorrect page count')
        assert hashlib.sha256(pdf.read_bytes()).hexdigest()==item[label+'_sha256'],(slug,'PDF digest mismatch')
        for number,page in enumerate(reader.pages,1):
            assert abs(float(page.mediabox.width)-595.276)<1 and abs(float(page.mediabox.height)-841.89)<1,(slug,'not A4',number)
            assert len((page.extract_text() or '').split())>10,(slug,'empty PDF page',label,number)
    results[slug]={'original_sections_preserved':len(source['sections']),'figures_preserved':len(source['figures']),'new_chapters':len(chapters),'new_chapter_words':words,'analysis_pages':item['analyse-seule_pages'],'illustrated_pages':item['etude_pages']}
for portal in ['philosophie.html','philosophie/index.html']:
    doc=html.fromstring((ROOT/portal).read_text())
    links=set(doc.xpath('//a/@href'))
    for slug in baseline['sources']:
        assert '/philosophie-'+slug+'.html' in links,(portal,'missing full study link',slug)
results['scope']='Structural, preservation and pagination checks. Philosophical quality requires editorial reading.'
(ROOT/'assets/philosophie/integrite-2026-11-04.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
