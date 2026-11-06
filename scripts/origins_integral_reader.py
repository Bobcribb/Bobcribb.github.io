"""Rattacher au portail ODS l'édition historique intégrale des tomes I–XXVII.

Ce volume est déjà conservé publiquement : ajouter un accès direct et un retour
dans _site uniquement, sans créer de numéro canonique ni réécrire la source.
"""
from pathlib import Path
import html
import re
from bs4 import BeautifulSoup

RELATIVE = Path("corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html")
URL = "/" + RELATIVE.as_posix()
RETURN = "/origines-du-sacre/#origines-edition-historique-integrale"


def link_integral_edition(fragment: str, out: Path, root: Path) -> str:
    """Valider une source existante, insérer un retour et une carte responsive.

    Les tests isolés des neuf archives ne disposent pas du gros volume :
    ignorer uniquement lorsque ni source ni rendu n'existent.
    """
    out, root = Path(out), Path(root)
    original_file, reader_file = root / RELATIVE, out / RELATIVE
    if not original_file.exists() and not reader_file.exists():
        return fragment
    if not original_file.is_file() or not reader_file.is_file():
        raise RuntimeError("ODS intégrale I–XXVII : fichier source ou lecteur manquant")
    if original_file.stat().st_size < 500_000 or reader_file.stat().st_size < 500_000:
        raise RuntimeError("ODS intégrale I–XXVII : édition anormalement courte")
    original_html = original_file.read_text(encoding="utf-8")
    rendered_html = reader_file.read_text(encoding="utf-8")
    original = BeautifulSoup(original_html, "html.parser")
    reader = BeautifulSoup(rendered_html, "html.parser")
    source_main, main = original.select_one("main"), reader.select_one("main")
    if source_main is None or main is None or reader.body is None:
        raise RuntimeError("ODS intégrale I–XXVII : structure de lecture absente")
    source_text = source_main.get_text(" ", strip=True)
    reader_text = main.get_text(" ", strip=True)
    if (len(source_text) < 50_000 or len(reader_text) < len(source_text) * .95
            or not re.search(r"bibliograph|sources|références", source_text, re.I)
            or source_text[:180] not in reader_text or source_text[-180:] not in reader_text):
        raise RuntimeError("ODS intégrale I–XXVII : intégrité scientifique non vérifiée")

    for previous in reader.select('nav[data-mythos-integral-return]'):
        previous.decompose()
    back = BeautifulSoup(
        '<nav class="origins-archival-return" data-mythos-integral-return="1" '
        'aria-label="Retour au sommaire des Origines du sacré">'
        '<a href="' + RETURN + '">← Retour à l’édition réunie des tomes I–XXVII</a>'
        '</nav>', "html.parser"
    ).nav
    main.insert_before(back)
    if main.get_text(" ", strip=True) != reader_text:
        raise RuntimeError("ODS intégrale I–XXVII : altération du texte lors du rattachement")
    reader_file.write_text(str(reader), encoding="utf-8")

    picture = out / "media/2026/10/mythos-ounas-chambre-funeraire-vincent-brown.jpg"
    illustration = (
        '<img class="origins-integral-picture" src="/media/2026/10/'
        'mythos-ounas-chambre-funeraire-vincent-brown.jpg" loading="lazy" decoding="async" '
        'alt="Chambre funéraire d’Ounas à Saqqara, document égyptien" />'
        if picture.is_file() else ""
    )
    section = (
        '<section class="origins-archival-shelf origins-archival-integral portal-section" '
        'id="origines-edition-historique-integrale" '
        'aria-labelledby="origines-edition-historique-titre">'
        '<h2 id="origines-edition-historique-titre">Édition universitaire historique réunie : tomes I–XXVII</h2>'
        '<p class="section-intro">Retrouver dans un seul lecteur le texte intégral des vingt-sept '
        'premiers tomes historiques, avec son sommaire, ses sources et ses bibliographies. '
        'Cette édition conservée dans le corpus public est distincte des numéros canoniques '
        'attribués aux chapitres contemporains.</p>'
        '<div class="origins-archival-grid origins-integral-grid"><a class="origins-archival-card '
        'origins-integral-link" href="' + html.escape(URL, quote=True) + '">'
        + illustration +
        '<span class="origins-integral-copy">'
        '<span class="origins-archival-code">CORPUS HISTORIQUE · TOMES I–XXVII</span>'
        '<strong>Aux origines du sacré — édition réunie</strong>'
        '<span>Lecture scientifique intégrale, sommaire interne et documentation '
        'historique conservés.</span>'
        '<span class="origins-archival-cta">Ouvrir les 27 tomes en un seul lecteur →</span>'
        '</span></a></div>'
        '<p class="origins-integral-caveat">Illustration documentaire : chambre funéraire '
        'd’Ounas (Égypte). Cet exemple ne représente pas les vingt-sept tomes dans leur ensemble.</p>'
        '</section>'
    )
    return fragment + section
