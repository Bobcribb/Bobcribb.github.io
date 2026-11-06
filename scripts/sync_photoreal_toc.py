#!/usr/bin/env python3
"""Synchroniser le sommaire généré de la galerie, sans toucher aux notices.

Les ajouts concurrents de cartes photoréalistes peuvent laisser un ancien
sommaire figé dans le HTML source. Ce script ne reconstruit que le <details>
de navigation, à partir des  titres et ancres réellement présents. Les IDs
historiques, photographies et notices archéologiques restent strictement intacts.

Utilisation : python scripts/sync_photoreal_toc.py --check
              python scripts/sync_photoreal_toc.py --write
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "reconstitutions-photorealistes.html"
TOC = re.compile(
    r'(<details(?=[^>]*\bmythos-gallery-toc\b)[^>]*>)(.*?)(</details>)',
    re.DOTALL,
)
SECTION = re.compile(r"lecture-section-[1-9][0-9]*")


def sections_and_labels(markup: str) -> list[tuple[str, str]]:
    doc = BeautifulSoup(markup, "html.parser")
    articles = doc.select("article.r3d-card")
    if not articles:
        raise ValueError("Aucune carte archéologique dans la galerie")
    output = []
    for article in articles:
        headings = article.select('h2[data-reading-section="true"][id]')
        if len(headings) != 1:
            raise ValueError("Chaque carte doit conserver une section scientifique unique")
        heading = headings[0]
        anchor = heading.get("id", "")
        if not SECTION.fullmatch(anchor):
            raise ValueError("Ancre scientifique absente ou non canonique : " + anchor)
        caption = article.select_one("figcaption strong")
        if caption is None or not caption.get_text(" ", strip=True):
            raise ValueError("Légende archéologique absente pour " + anchor)
        label = caption.get_text(" ", strip=True) + " — " + heading.get_text(" ", strip=True)
        output.append((anchor, label))
    ids = [anchor for anchor, _ in output]
    if len(ids) != len(set(ids)):
        raise ValueError("Ancres scientifiques dupliquées")
    return output


def synchronized_markup(markup: str) -> str:
    """Réécrire uniquement la navigation générée, jamais les cartes ni images."""
    entries = sections_and_labels(markup)
    toc = TOC.search(markup)
    if toc is None or TOC.search(markup, toc.end()) is not None:
        raise ValueError("La galerie requiert exactement un sommaire généré")
    inner = (
        "<summary>Sommaire de lecture · " + str(len(entries)) + " sections</summary><ol>"
        + "".join(
            '<li><a href="#' + escape(anchor, quote=True) + '">'
            + escape(label) + '</a></li>'
            for anchor, label in entries
        ) + "</ol>"
    )
    return markup[:toc.start(2)] + inner + markup[toc.end(2):]


def synchronize(path: Path = GALLERY, *, write: bool = False) -> dict:
    original = path.read_text(encoding="utf-8")
    updated = synchronized_markup(original)
    changed = original != updated
    count = len(sections_and_labels(original))
    if changed and write:
        path.write_text(updated, encoding="utf-8")
    return {"sections": count, "changed": changed, "saved": changed and write}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Vérifier sans modifier")
    mode.add_argument("--write", action="store_true", help="Mettre à jour le seul sommaire généré")
    parser.add_argument("--path", type=Path, default=GALLERY)
    args = parser.parse_args()
    result = synchronize(args.path, write=args.write)
    if result["changed"] and not args.write:
        parser.exit(1, "Sommaire périmé : "
                    + str(result["sections"])
                    + " sections réelles. Exécuter --write puis valider le diff.\n")
    print("Sommaire galerie : "
          + str(result["sections"]) + " sections ; "
          + ("corrigé" if result["saved"] else "synchronisé"))


if __name__ == "__main__":
    main()
