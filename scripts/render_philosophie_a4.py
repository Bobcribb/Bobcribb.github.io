"""Reproducible A4 audit. Requires weasyprint==70.0, lxml, pypdf and Nimbus Roman.

Run from the repository root: python scripts/render_philosophie_a4.py
The analysis-only control excludes illustrations, captions, introductory notice,
navigation, reference notes and bibliography. No forced page breaks or min-height.
"""
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, re, hashlib, logging, mimetypes, argparse, subprocess
import weasyprint
from lxml import html, etree
from weasyprint import HTML, CSS
from weasyprint.urls import URLFetcherResponse
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--minimum-pages',type=int,default=100)
parser.add_argument('--only',choices=['iliade','odyssee','theogonie'],default=None)
args=parser.parse_args()
if weasyprint.__version__!='70.0':
    raise RuntimeError('This dated edition requires WeasyPrint 70.0.')
font=subprocess.run(['fc-match','--format=%{family}','Nimbus Roman'],check=True,capture_output=True,text=True).stdout
if 'Nimbus Roman' not in font:
    raise RuntimeError('Install Nimbus Roman before producing the reference pagination.')
OUT=ROOT/'assets/philosophie/pdf'
OUT.mkdir(parents=True,exist_ok=True)
logging.getLogger('weasyprint').setLevel(logging.ERROR)
CSS_TEXT=(ROOT/'assets/philosophie-edition.css').read_text()
failures=[]
def fetch(url):
    u=urlparse(url)
    if u.scheme in ('http','https'):
        raise ValueError('Remote resource forbidden for reproducible rendering: '+url)
    path=Path(unquote(u.path))
    if not path.is_file():
        path=ROOT/unquote(u.path).lstrip('/')
    if not path.is_file():
        failures.append(url);raise FileNotFoundError(url)
    return URLFetcherResponse(path.as_uri(),body=path.read_bytes(),headers={'Content-Type':mimetypes.guess_type(str(path))[0] or 'application/octet-stream'})
fetch._fail_on_errors=True

report={'date':'2026-11-04','edition':'Études longues : seuil de 100 pages d’analyse par œuvre','minimum_analysis_pages':args.minimum_pages,'engine':'WeasyPrint 70.0','format':'A4 210 × 297 mm','margins_mm':25,'font':'Nimbus Roman','body_pt':12,'line_height':1.5,'studies':{}}
report['analysis_excludes']=['illustrations et légendes','bibliographies','notes de référence','navigation','introduction éditoriale','notice de méthode']
report['stylesheet_sha256']=hashlib.sha256(CSS_TEXT.encode()).hexdigest()
baseline={
 'iliade':('8fb25178402d5bca308c7e999e945733349a2bb0',3108),
 'odyssee':('5b35dcbe08e0430ce16742ed77d2d3c2e39868ab',2486),
 'theogonie':('25de01c42edd4ecbe0a3873ef1a0b448bb4ff0a3',2784)}
for slug in ([args.only] if args.only else ['iliade','odyssee','theogonie']):
    path=ROOT/f'philosophie-{slug}.html'
    raw=path.read_text();doc=html.fromstring(raw)
    main=doc.xpath('//main')[0]
    full='<html lang="fr"><head><meta charset="utf-8"><title>'+doc.xpath('//title/text()')[0]+'</title></head><body>'+etree.tostring(main,encoding='unicode',method='html')+'</body></html>'
    chunks=[];words=0
    for sec in main.xpath('.//section[contains(concat(" ",normalize-space(@class)," ")," philo-chapter ")]'):
        for para in sec.xpath('./h2|./h3|./p[not(@class)]'):
            if para.tag in ('h2','h3'):
                chunks.append(etree.tostring(para,encoding='unicode',method='html'))
                continue
            # Original bibliography may share the final analytical paragraph.
            text=para.text_content().split('Bibliographie')[0].strip()
            if text:
                words+=len(re.findall(r"\S+",text))
                clean=etree.Element('p');clean.text=text
                chunks.append(etree.tostring(clean,encoding='unicode',method='html'))
    analysis='<html lang="fr"><head><meta charset="utf-8"><title>'+doc.xpath('//title/text()')[0]+' — analyse seule</title></head><body><main class="philo-work"><section class="philo-chapter">'+''.join(chunks)+'</section></main></body></html>'
    item={'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'analysis_words':words,'figures':len(main.xpath('.//figure'))}
    item.update(initial_git_blob=baseline[slug][0],initial_analysis_words=baseline[slug][1],initial_analysis_pages_same_layout=7)
    for label,data in [('etude',full),('analyse-seule',analysis)]:
        target=OUT/f'{slug}-{label}-a4.pdf'
        HTML(string=data,base_url=ROOT.as_uri()+'/',url_fetcher=fetch).write_pdf(target,stylesheets=[CSS(string=CSS_TEXT)])
        reader=PdfReader(target)
        item[label+'_pages']=len(reader.pages)
        item[label+'_page_words']=[len((p.extract_text() or '').split()) for p in reader.pages]
        item[label+'_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        for page in reader.pages:
            assert abs(float(page.mediabox.width)-595.276)<1
            assert abs(float(page.mediabox.height)-841.89)<1
    report['studies'][slug]=item
    assert item['analyse-seule_pages']>=args.minimum_pages,(slug,'analysis page threshold not reached',item['analyse-seule_pages'],args.minimum_pages)
    print(slug,item['analysis_words'],'words;',item['etude_pages'],'illustrated;',item['analyse-seule_pages'],'analysis only')
assert not failures,failures
report_path=ROOT/('assets/philosophie/pagination-2026-11-04'+('-'+args.only if args.only else '')+'.json')
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
