"""Rendre consultables les dix-huit sources intégrales de l’Énéide sur bobmythos.fr.

Le texte existe déjà dans le lecteur HTML et dans le dépôt, mais ses 18
manuscrits Markdown ne sont pas nécessairement distribués par GitHub Pages.
Hors collections numérotées : aucun numéro ni reçu d'attribution n'est créé.
"""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

SOURCE_DIR = Path("corpus/philosophie/eneide")
NAMES = (
    "00-introduction.md",
    "01-chant-i.md", "02-chant-ii.md", "03-chant-iii.md",
    "04-chant-iv.md", "05-chant-v.md", "06-chant-vi.md",
    "07-chant-vii.md", "08-chant-viii.md", "09-chant-ix.md",
    "10-chant-x.md", "11-chant-xi.md", "12-chant-xii.md",
    "13-pietas-destin.md", "14-empire-memoire.md",
    "15-philosophies-comparaisons.md", "16-poetique-conclusion.md",
    "17-reperes-et-sources.md",
)
STUDY = Path("philosophie-eneide.html")
NARRATIVE = Path(
    "bibliotheque-mythologies-du-monde/"
    "heros-mythologies-monde-cycles-epiques/"
    "cycle-enee-didon-eneide-romaine/index.html"
)
NARRATIVE_URL = "/" + NARRATIVE.parent.as_posix() + "/"


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _stylesheet(doc: BeautifulSoup) -> None:
    if doc.head is None:
        raise RuntimeError("MYTHOS : document Énéide dépourvu d'élément head")
    if not doc.head.select_one('link[href="/assets/mythos-eneide-sources.css"]'):
        doc.head.append(doc.new_tag(
            "link", rel="stylesheet", href="/assets/mythos-eneide-sources.css"
        ))


def _remove_owned(doc: BeautifulSoup) -> None:
    for node in doc.select('[data-mythos-eneide-sources]'):
        node.decompose()


def install(root: Path, out: Path) -> int:
    """Vérifier l'édition, copier octet pour octet les sources, relier les deux lecteurs."""
    root, out = Path(root), Path(out)
    study_path, narrative_path = out / STUDY, out / NARRATIVE
    if not study_path.is_file() or not narrative_path.is_file():
        raise RuntimeError("MYTHOS : lecteurs Énéide et récit d'Énée requis")

    doc = BeautifulSoup(study_path.read_text(encoding="utf-8"), "html.parser")
    narrative = BeautifulSoup(narrative_path.read_text(encoding="utf-8"), "html.parser")
    main = doc.select_one("main.philo-work")
    narrative_main = narrative.select_one("main article.content") or narrative.select_one("main")
    if main is None or narrative_main is None:
        raise RuntimeError("MYTHOS : structures de lecture de l'Énéide absentes")
    if not main.select_one(".philo-toc"):
        raise RuntimeError("MYTHOS : sommaire universitaire de l'Énéide absent")

    original_text = _clean(main.get_text(" ", strip=True))
    source_texts = []
    title_labels = []
    for i, name in enumerate(NAMES):
        source_path = root / SOURCE_DIR / name
        if not source_path.is_file():
            raise RuntimeError(f"Source Énéide absente : {source_path}")
        raw = source_path.read_text(encoding="utf-8")
        match = re.match(r"^#\s+([^\r\n]+)", raw)
        if len(raw) < 8000 or not match:
            raise RuntimeError(f"Source Énéide manifestement incomplète : {name}")
        title = _clean(match.group(1))
        heading = main.select_one(f"#eneide-{i:02}")
        if heading is None or _clean(heading.get_text(" ", strip=True)) != title:
            raise RuntimeError(f"Énéide : source et lecteur HTML divergents pour {name}")
        source_texts.append((name, raw))
        title_labels.append(title)
    if not re.search(r"bibliograph|sources|références", source_texts[-1][1], re.I):
        raise RuntimeError("Énéide : appareil documentaire de référence absent")

    _remove_owned(doc)
    _remove_owned(narrative)
    # Le sommaire ne reprend pas le texte : il le relie à son source intact.
    items = "".join(
        '<li><a href="/corpus/philosophie/eneide/'
        + html.escape(name, quote=True) + '">'
        + html.escape(title) + '</a></li>'
        for (name, _), title in zip(source_texts, title_labels)
    )
    shelf = BeautifulSoup(
        '<section class="mythos-eneide-sources" id="eneide-manuscrits-originaux" '
        'data-mythos-eneide-sources="shelf" aria-labelledby="sources-eneide-heading">'
        '<h2 id="sources-eneide-heading">Manuscrits originaux de l’étude de l’Énéide</h2>'
        '<p>Les dix-huit sources Markdown intégrales de cette première livraison '
        'sont proposées sans coupure ni réécriture, y compris le lexique, les '
        'références et la bibliographie. Leur présence n’équivaut pas à '
        'l’achèvement du projet de 300 pages.</p>'
        '<details><summary>Afficher les 18 sources intégrales</summary>'
        '<ol class="mythos-eneide-source-grid">' + items + '</ol></details>'
        '<p class="mythos-eneide-source-note">Lire aussi '
        '<a href="' + NARRATIVE_URL + '">le cycle d’Énée et Didon dans '
        'la bibliothèque des grands récits</a> (présentation narrative distincte).</p>'
        '</section>', "html.parser"
    ).section
    bottom = main.select_one("nav.reader-bottom")
    if bottom:
        bottom.insert_before(shelf)
    else:
        main.append(shelf)

    nav = BeautifulSoup(
        '<nav class="mythos-eneide-pair-nav" data-mythos-eneide-sources="study" '
        'aria-label="Parcours croisés entre récit et étude critique">'
        '<a href="' + NARRATIVE_URL + '">Lire le récit d’Énée et de Didon</a>'
        '<a href="#eneide-manuscrits-originaux">Consulter les 18 manuscrits '
        'de cette étude</a></nav>', "html.parser"
    ).nav
    main.select_one(".philo-toc").insert_after(nav)
    # Le titre principal h1 figure dans la bannière muséale, hors du main.
    # Le récit commence normalement par un paragraphe, puis son premier h2.
    intro = narrative_main.find(["h1", "h2"])
    if intro is None:
        raise RuntimeError("MYTHOS : sections du récit d'Énée absentes")
    sister = BeautifulSoup(
        '<aside class="mythos-eneide-pair-nav" data-mythos-eneide-sources="narrative" '
        'aria-label="Étude universitaire associée">'
        '<p><strong>Prolongement philosophique :</strong> '
        'l’Énéide de Virgile, étude critique intégrale de la première livraison '
        '(douze chants, fondation, <i>pietas</i>, empire et mémoire).</p>'
        '<a href="/philosophie-eneide.html">Lire l’étude universitaire intégrale</a>'
        '<a href="/philosophie-eneide.html#eneide-manuscrits-originaux">'
        'Consulter les 18 manuscrits originaux</a></aside>', "html.parser"
    ).aside
    if intro.name == "h1":
        intro.insert_after(sister)
    else:
        intro.insert_before(sister)
    _stylesheet(doc)
    _stylesheet(narrative)

    # Vérification avant copie : aucun texte déjà présent n'est remplacé.
    for (name, raw) in source_texts:
        target = out / SOURCE_DIR / name
        if target.is_file() and target.read_text(encoding="utf-8") != raw:
            raise RuntimeError(f"Énéide : source publique différente : {name}")
    # Copier intégralement les sources de travail publiques, jamais les brouillons Drive.
    for (name, _) in source_texts:
        target = out / SOURCE_DIR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / SOURCE_DIR / name, target)
    # BeautifulSoup ajoute parfois un saut de ligne au DOCTYPE à chaque
    # aller-retour. Normaliser uniquement cet espace, sans toucher aux textes.
    def serialize(page: BeautifulSoup) -> str:
        return re.sub(r"(?i)^(<!doctype\\s+html>)\\s*(?=<html\\b)",
                      r"\\1\\n", str(page))

    study_path.write_text(serialize(doc), encoding="utf-8")
    narrative_path.write_text(serialize(narrative), encoding="utf-8")
    return len(source_texts)


if __name__ == "__main__":
    print("Sources Énéide reliées :", install(Path("."), Path("_site")))
