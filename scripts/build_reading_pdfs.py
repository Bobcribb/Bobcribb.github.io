#!/usr/bin/env python3
"""Verify and expose the six reference PDFs without creating duplicate editions."""
from html import escape
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader
from improve_reading import EPICS, fragment


def build(out):
    out = Path(out).resolve()
    edition = json.loads((out/'assets/philosophie/pagination-2026-11-04.json').read_text())
    report = []
    for key, (title, *_) in EPICS.items():
        reference = edition['studies'][key]
        for kind in ('etude', 'analyse-seule'):
            url = '/assets/philosophie/pdf/'+key+'-'+kind+'-a4.pdf'
            target = out/url.lstrip('/')
            digest = sha256(target.read_bytes()).hexdigest()
            if digest != reference[kind+'_sha256']:
                raise ValueError('Empreinte PDF différente de l’édition vérifiée : '+url)
            reader = PdfReader(target)
            pages = len(reader.pages)
            if pages != reference[kind+'_pages']:
                raise ValueError('Pagination PDF différente de l’audit : '+url)
            for page in reader.pages:
                if abs(float(page.mediabox.width)-595.276)>1 or abs(float(page.mediabox.height)-841.89)>1:
                    raise ValueError('Format A4 attendu : '+url)
            if kind == 'analyse-seule' and pages < edition['minimum_analysis_pages']:
                raise ValueError('Seuil de 100 pages d’analyse non atteint : '+url)
            report.append({'work': title, 'edition': edition['date'], 'kind': kind,
                           'url': url, 'pages': pages, 'analysis_words': reference['analysis_words'],
                           'analysis_pages': reference['analyse-seule_pages'],
                           'target_pages': edition['minimum_analysis_pages'],
                           'target_reached': reference['analyse-seule_pages'] >= edition['minimum_analysis_pages'],
                           'bytes': target.stat().st_size, 'sha256': digest})
    (out/'catalog/reading-pdfs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    status = out/'etat-du-corpus/index.html'
    doc = BeautifulSoup(status.read_text(),'html.parser')
    container = doc.select_one('#epic-pdf-status')
    if container:
        container.clear()
        rows = []
        for full, analysis in zip(report[::2], report[1::2]):
            rows.append('<li>'+escape(full['work'])+' : <a href="'+full['url']+'">étude illustrée, '+str(full['pages'])+' pages</a> ; <a href="'+analysis['url']+'">analyse seule, '+str(analysis['pages'])+' pages</a>.</li>')
        container.append(fragment('<ul>'+''.join(rows)+'</ul><p>Édition du 4 novembre 2026. Le seuil de 100 pages est contrôlé sur l’analyse seule, sans illustrations, légendes, bibliographies, notes de référence ou navigation. <a href="/philosophie-audit-pagination-2026-11-04.html">Consulter la méthode de pagination</a>.</p>'))
        status.write_text(str(doc),encoding='utf-8')
    print('PDF vérifiés :',[(r['work'],r['kind'],r['pages']) for r in report])
    return report


if __name__=='__main__':
    build(Path('_site'))
