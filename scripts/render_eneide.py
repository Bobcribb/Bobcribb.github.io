#!/usr/bin/env python3
"""Render the partial Eneid study; never equate its target with its actual length.

Run from any directory with Python, mistune, beautifulsoup4, WeasyPrint 70,
pypdf, and the Nimbus Roman system font. Sources are preserved as Markdown.
This script is independent of the three existing Homer/Hesiod renderers.
"""
from pathlib import Path
import hashlib, html, json, re
from collections import Counter
import mistune
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'corpus/philosophie/eneide'
PDF=ROOT/'assets/philosophie/pdf/eneide-etude-a4.pdf'
REPORT=ROOT/'assets/philosophie/eneide-pagination.json'
TITLE='L’Énéide de Virgile — Fonder un monde après la catastrophe'
md=mistune.create_markdown(escape=True)
PRINT='''
@page {size:A4;margin:25mm;@bottom-center{content:counter(page);font:10pt "Nimbus Roman";color:#555}}
body {font:12pt/1.5 "Nimbus Roman",serif;color:#151515;margin:0}
p {margin:0 0 8pt;orphans:3;widows:3;text-align:left}
h1{font-size:25pt;line-height:1.2;color:#312515}
h2{font-size:17pt;line-height:1.25;margin:20pt 0 10pt;break-after:avoid}
h3{font-size:13pt;line-height:1.3;margin:14pt 0 8pt;break-after:avoid}
a{color:#4d391b;text-decoration:underline;overflow-wrap:anywhere}
ul{padding-left:18pt}li{margin-bottom:5pt}
.reference{font-size:10pt;line-height:1.35;color:#444;border-top:0.5pt solid #ccc;padding-top:6pt}
.cover{break-after:page;padding-top:30mm}.cover .label{letter-spacing:2pt;font-size:11pt;color:#71552e}
.cover h1{margin:30pt 0}.cover .status{margin:24pt 0 18pt;padding:14pt;border:1pt solid #a48a60}
.contents{break-after:page}.contents ul{list-style:none;padding:0}.contents li{margin-bottom:8pt}
.contents a{text-decoration:none}.contents a::after{content:leader('.') target-counter(attr(href),page)}
'''
WEB='''
html{scroll-behavior:smooth}body{margin:0;background:#090d0f;color:#f0e7d8}
.eneide-nav{padding:22px;display:flex;gap:24px;justify-content:center;flex-wrap:wrap;border-bottom:1px solid #806741}
a{color:#ead0a0;text-underline-offset:.2em}main.philo-work{max-width:1050px;margin:auto;padding:28px 20px 70px;box-sizing:border-box}
.philo-work h1{font:400 clamp(30px,5vw,52px)/1.2 Georgia,serif;color:#ead0a0;text-align:center}
.philo-edition,.philo-toc{background:#151c1e;border:1px solid #806741;padding:22px;line-height:1.7;margin:25px 0}
.philo-toc ol{columns:2;column-gap:36px;padding-left:24px}.philo-toc li{break-inside:avoid;margin:0 0 12px}
.philo-chapter{padding:28px clamp(18px,4vw,42px);background:#12191b;border:1px solid #5f523e;margin:28px 0}
.philo-chapter h2{font:400 31px/1.3 Georgia,serif;color:#edcf99}.philo-chapter h3{font:600 22px/1.4 Georgia,serif;color:#e4c79d;margin-top:30px}
.philo-chapter p,.philo-chapter li{font:18px/1.8 Georgia,serif;color:#e8ddc9;overflow-wrap:anywhere}
.philo-chapter .reference{font:14px/1.6 Arial,sans-serif;border-top:1px solid #62543f;padding-top:14px;color:#d1bfa4}
.philo-work .eyebrow{text-align:center;font:12px/1.5 Arial,sans-serif;letter-spacing:.15em;color:#c7a573}
.philo-edition a{display:inline-block;padding:7px 0}.eneide-foot{padding:25px;text-align:center}
@media(max-width:680px){.philo-toc ol{columns:1}.philo-chapter{padding:20px 16px}.philo-chapter p,.philo-chapter li{font-size:17px}.philo-chapter h2{font-size:27px}}
'''

def build():
    sections=[];chapters=[];analysis=[];words=0;hashes={};paras=[]
    for index,path in enumerate(sorted(SOURCE.glob('*.md'))):
        raw=path.read_text(encoding='utf-8');hashes[path.name]=hashlib.sha256(raw.encode()).hexdigest()
        soup=BeautifulSoup(md(raw),'html.parser')
        title=soup.h1.get_text();soup.h1.name='h2';soup.h2['id']=f'eneide-{index:02}'
        for j,h in enumerate(soup.find_all('h2')[1:]):h.name='h3';h['id']=f'eneide-{index:02}-{j:02}'
        for p in soup.find_all('p'):
            if p.get_text().startswith(('Références','Référence')):p['class']='reference'
        fragment=str(soup);sections.append(f'<section class="philo-chapter">{fragment}</section>')
        chapters.append((f'eneide-{index:02}',title))
        if index<17:
            clean=BeautifulSoup(fragment,'html.parser')
            for p in clean.select('.reference'):p.decompose()
            for p in clean.find_all('p'):
                txt=p.get_text(' ',strip=True);words+=len(txt.split());paras.append(txt)
            analysis.append(str(clean))
    duplicates=[p[:120] for p,n in Counter(paras).items() if n>1]
    if duplicates:raise ValueError(('Duplicate analytical paragraphs',duplicates))
    analysis_doc=HTML(string='<html lang="fr"><body>'+''.join(analysis)+'</body></html>').render(stylesheets=[CSS(string=PRINT)])
    n_analysis=len(analysis_doc.pages)
    notice=f'Première livraison : {n_analysis} pages A4 d’analyse dans le contrôle séparé, pour un objectif de 300 pages. Le volume demandé n’est pas encore achevé.'
    method='Format A4, marges de 25 mm, Nimbus Roman 12 points, interligne 1,5. Analyse en flux continu, sans saut imposé entre chapitres. Le contrôle exclut la couverture, le sommaire, les références de fin de chapitre, le lexique et la bibliographie.'
    links=''.join(f'<li><a href="#{key}">{html.escape(t)}</a></li>' for key,t in chapters)
    contents='<nav class="contents"><h2>Sommaire</h2><ul>'+links+'</ul></nav>'
    cover=f'<section class="cover"><p class="label">MYTHOS · ÉTUDES PHILOSOPHIQUES</p><h1>L’Énéide<br>de Virgile</h1><p style="font-size:17pt">Fonder un monde après la catastrophe</p><p>Lecture des douze chants, éthique, politique et poétique</p><div class="status"><p>{notice}</p><p>{str(words//1000)+' '+str(words%1000).zfill(3)} mots d’analyse, hors titres et références.</p></div><p>Édition du 4 novembre 2026</p><p style="font-size:10pt">{method}</p></section>'
    full='<html lang="fr"><head><meta charset="utf-8"><title>'+TITLE+'</title><meta name="author" content="MYTHOS"></head><body>'+cover+contents+''.join(sections)+'</body></html>'
    PDF.parent.mkdir(parents=True,exist_ok=True)
    HTML(string=full).write_pdf(PDF,stylesheets=[CSS(string=PRINT)])
    reader=PdfReader(PDF);n_full=len(reader.pages)
    report={'edition_date':'2026-11-04','status':'partial','target_analysis_pages':300,'actual_analysis_pages':n_analysis,'actual_total_pdf_pages':n_full,'analysis_words':words,'format':'A4','font':'Nimbus Roman','font_pt':12,'line_height':1.5,'margins_mm':25,'forced_analysis_page_breaks':False,'analysis_excludes':['cover','contents','chapter references','glossary','bibliography'],'sources_sha256':hashes,'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'duplicate_analysis_paragraphs':len(duplicates)}
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    intro=f'<div class="philo-edition"><p><strong>{notice}</strong></p><p>PDF : {n_full} pages au total. Analyse suivie des douze chants ; piété, destin, responsabilité, Empire, mémoire et comparaisons philosophiques.</p><p><a href="/assets/philosophie/pdf/eneide-etude-a4.pdf">Télécharger le PDF A4 — {n_full} pages</a></p><details><summary>Pagination et sources</summary><p>{method}</p><p><a href="/assets/philosophie/eneide-pagination.json">Consulter le contrôle de pagination</a></p></details></div>'
    web=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE} — MYTHOS</title><meta name="description" content="Analyse de l’Énéide : les douze chants, Didon, le destin, la piété, l’Empire et la mort de Turnus. Première livraison du projet de 300 pages, avec PDF et sources."><link rel="canonical" href="https://bobmythos.fr/philosophie-eneide.html"><link rel="stylesheet" href="/assets/mythos-reference.css"><link rel="stylesheet" href="/assets/mythos-museum.css"><link rel="stylesheet" href="/assets/philosophie-edition.css"><style>{WEB}</style></head><body class="mythos-design"><a href="#contenu" class="mythos-skip">Aller au contenu</a><header class="eneide-nav"><a href="/">MYTHOS</a><a href="/philosophie/">Philosophie</a><a href="/recherche/">Recherche</a></header><main id="contenu" class="philo-work"><p class="eyebrow">VIRGILE · ÉPOPÉE ROMAINE · ANALYSE PHILOSOPHIQUE</p><h1>L’Énéide de Virgile</h1>{intro}<nav class="philo-toc" aria-label="Sommaire de l’étude"><h2>Sommaire</h2><ol>{links}</ol></nav>{''.join(sections)}<p><a href="/philosophie/">Retour aux études philosophiques</a></p></main><footer class="eneide-foot">MYTHOS · 4 novembre 2026 · Première livraison</footer></body></html>'''
    page=ROOT/'philosophie-eneide.html';page.write_text(web)
    doc=BeautifulSoup(web,'html.parser');ids=[x['id'] for x in doc.select('[id]')]
    assert len(ids)==len(set(ids))
    assert all(a['href'][1:] in ids for a in doc.select('a[href^="#"]'))
    assert words>30000 and n_analysis<300
    assert len(reader.pages)>n_analysis
    print(json.dumps({k:v for k,v in report.items() if k!='sources_sha256'},ensure_ascii=False))

if __name__=='__main__':build()
