"""Inventaire documentaire des neuf tomes ODS-S28/ODS-CONV déjà conservés.

Ces cotes historiques ne sont PAS les numéros canoniques de chapitres.
La routine ajoute de la navigation au rendu, sans modifier les manuscrits sources.
"""
from pathlib import Path
import html
import re
from bs4 import BeautifulSoup

ARCHIVES = (
    ("ODS-CONV-XXV", "XXV", "339–346", "Sanctuaires et espaces sacrés", "conv-tome-XXV-chapitres-339-346"),
    ("ODS-CONV-XXVI", "XXVI", "347–354", "Les eaux sacrées", "conv-tome-XXVI-chapitres-347-354"),
    ("ODS-CONV-XXVII", "XXVII", "355–362", "Le feu sacré", "conv-tome-XXVII-chapitres-355-362"),
    ("ODS-S28", "XXVIII", "363–370", "Montagnes, grottes et profondeurs", "tome-XXVIII-chapitres-363-370"),
    ("ODS-CONV-XXIX", "XXIX", "371–378", "Arbres sacrés", "conv-tome-XXIX-chapitres-371-378"),
    ("ODS-CONV-XXX", "XXX", "379–386", "Pierres sacrées, bétyles et images aniconiques", "conv-tome-XXX-chapitres-379-386"),
    ("ODS-CONV-XXXI", "XXXI", "387–394", "Images divines", "conv-tome-XXXI-chapitres-387-394"),
    ("ODS-CONV-XXXII", "XXXII", "395–402", "Corps, possession et masques", "conv-tome-XXXII-chapitres-395-402"),
    ("ODS-CONV-XXXIII", "XXXIII", "403–410", "Voix, hymnes et musique sacrée", "conv-tome-XXXIII-chapitres-403-410"),
)
ROOT_URL = "/corpus/origines-du-sacre/"
PORTAL = "/origines-du-sacre/#origines-archives-documentaires"


def archive_shelf(out: Path, root: Path) -> str:
    """Build nine verified links and reciprocal, idempotent reader navigation.

    The HTML and Markdown files must both exist and be long-form manuscripts.
    Existing canonical chapters, the editorial queue and its numbering are untouched.
    """
    cards = []
    for code, volume, chapters, title, slug in ARCHIVES:
        relative = Path("corpus/origines-du-sacre") / (slug + ".html")
        page = out / relative
        source = root / relative.with_suffix(".md")
        if not page.is_file() or not source.is_file():
            raise RuntimeError(f"ODS : archive intégrale absente : {code}")
        manuscript = source.read_text(encoding="utf-8")
        markup = page.read_text(encoding="utf-8")
        if len(manuscript) < 30000 or len(markup) < 30000:
            raise RuntimeError(f"ODS : archive anormalement courte : {code}")
        if not re.search(r"bibliograph|sources primaires|références", manuscript, re.I):
            raise RuntimeError(f"ODS : appareil documentaire introuvable : {code}")
        if "<html" not in markup.lower() or not re.search(r"bibliograph|sources|références", markup, re.I):
            raise RuntimeError(f"ODS : lecteur incomplet : {code}")
        url = ROOT_URL + slug + ".html"
        esc = lambda value: html.escape(value, quote=True)
        caveat = (" · édition de travail, vérification scientifique à poursuivre"
                  if code == "ODS-S28" else "")
        cards.append(
            '<a class="origins-archival-card" href="' + esc(url) + '">'
            '<span class="origins-archival-code">' + esc(code) + " · tome " + esc(volume) + '</span>'
            '<strong>' + esc(title) + '</strong>'
            '<span>Chapitres ' + esc(chapters) + " · texte intégral et bibliographie" + esc(caveat) + '</span>'
            '<span class="origins-archival-cta">Lire le manuscrit complet →</span></a>'
        )
        document = BeautifulSoup(markup, "html.parser")
        if not document.body:
            raise RuntimeError(f"ODS : structure HTML absente : {code}")
        main = document.select_one("main")
        masthead = document.select_one("header.mythos-masthead")
        if not main or not masthead:
            raise RuntimeError(f"ODS : navigation ou texte intégral absent : {code}")
        original_text = main.get_text(" ", strip=True)
        for old in document.select("nav[data-mythos-archival-return]"):
            old.decompose()
        back = BeautifulSoup(
            '<nav class="origins-archival-return" data-mythos-archival-return="1" '
            'aria-label="Retour au sommaire des archives des Origines du sacré">'
            '<a href="' + PORTAL + '">← Sommaire des neuf tomes historiques (XXV–XXXIII)</a>'
            '</nav>', "html.parser"
        ).nav
        masthead.insert_after(back)
        if main.get_text(" ", strip=True) != original_text:
            raise RuntimeError(f"ODS : contenu scientifique modifié : {code}")
        page.write_text(str(document), encoding="utf-8")
    fragment = (
        '<section class="origins-archival-shelf portal-section" '
        'id="origines-archives-documentaires" aria-labelledby="origines-archives-titre">'
        '<h2 id="origines-archives-titre">Archives universitaires historiques : tomes XXV à XXXIII</h2>'
        '<p class="section-intro">Neuf manuscrits complets, déjà conservés dans le corpus public, '
        'retrouvent ici leur sommaire et leurs liens de retour. Les cotes ODS-CONV et ODS-S28 '
        'désignent des séries historiques distinctes des numéros canoniques attribués par '
        'GitHub Actions. Sources et bibliographies demeurent dans chaque lecteur.</p>'
        '<div class="origins-archival-grid">' + "".join(cards) + '</div>'
        '</section>'
    )
    from origins_archival_concordance import enrich
    return enrich(fragment, out, root)
