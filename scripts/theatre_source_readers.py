"""Lecteurs HTML des neuf manuscrits sources intégraux du théâtre grec.

Les neuf sources Markdown et les deux éditions HTML existantes restent intactes.
Aucun chapitre canonique, numéro, reçu ou brouillon n'est modifié.
"""
from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path
from urllib.parse import urlsplit

import mistune
from bs4 import BeautifulSoup

BASE = Path("corpus/theatre-grec/comedies")
CSS = "/assets/mythos-theatre-archive.css"
ORIGINALS_LABEL = "MYTHOS · Archives universitaires du théâtre"


def _frontmatter(raw: str) -> tuple[str, str]:
    """Expose la métadonnée de l'archive, sans la supprimer ni la réinventer."""
    match = re.match(r"\A(---\r?\n.*?\r?\n---\r?\n)", raw, flags=re.S)
    return (match.group(1), raw[match.end():]) if match else ("", raw)


def _render_text(markdown_source: str) -> tuple[str, str, int]:
    """Rendu exhaustif des sections Markdown et de leur bibliographie."""
    renderer = mistune.create_markdown(escape=True, plugins=["table", "strikethrough", "url"])
    front, body = _frontmatter(markdown_source)
    rendered = BeautifulSoup(renderer(body), "html.parser")
    if not rendered.find("h1"):
        raise RuntimeError("Théâtre : manuscrit sans titre principal")
    headings = rendered.find_all(["h2", "h3"])
    if len(headings) < 2 or not re.search(r"bibliograph", body, re.I):
        raise RuntimeError("Théâtre : sections ou bibliographie manquantes")
    items = []
    for idx, heading in enumerate(headings, 1):
        marker = "source-section-" + str(idx).zfill(2)
        heading["id"] = marker
        label = heading.get_text(" ", strip=True)
        items.append('<li><a href="#' + marker + '">' + html.escape(label) + '</a></li>')
    # Ne pas imprimer les métadonnées YAML comme des paragraphes scientifiques.
    # Elles restent intégralement consultables, tout comme le fichier brut.
    metadata = (
        '<details class="theatre-original-metadata"><summary>Métadonnées originales'
        ' du manuscrit</summary><pre>' + html.escape(front) + '</pre></details>'
        if front else ""
    )
    navigation = '<nav class="theatre-original-toc" aria-label="Sommaire de l’édition source">' + (
        '<h2>Sommaire du texte intégral</h2><ol>' + ''.join(items) + '</ol></nav>'
    )
    return metadata + navigation + str(rendered), body, len(items)


def _fix_relative_links(markup: str, source: Path, root: Path, output: Path,
                        known: dict[str, str]) -> tuple[str, int]:
    """Résoudre les renvois attestés, signaler les anciennes cibles absentes.

    Le texte scientifique lisible reste identique. Les adresses des anciennes
    références Markdown qui n'existent plus ne deviennent pas des liens 404.
    """
    doc = BeautifulSoup(markup, "html.parser")
    unresolved = 0
    for anchor in doc.select("a[href]"):
        href = anchor.get("href", "")
        parsed = urlsplit(href)
        if not parsed.path or href.startswith(("/", "#", "//")) or parsed.scheme or parsed.netloc:
            continue
        target_name = Path(parsed.path).name
        dest = (source.parent / parsed.path).resolve()
        if not dest.is_relative_to(root.resolve()):
            raise RuntimeError("Théâtre : renvoi relatif sortant du dépôt")
        if dest.is_file() and dest.suffix == ".md":
            # Relier aux sources publiques existantes, sans inventer de fichier.
            rel = dest.relative_to(root).as_posix()
            anchor["href"] = "/" + rel + (("#" + parsed.fragment) if parsed.fragment else "")
            continue
        if dest.is_file():
            # Référence d'archive conservée ; sa disponibilité dépend du rendu.
            anchor["href"] = "/" + dest.relative_to(root).as_posix() + (
                ("#" + parsed.fragment) if parsed.fragment else "")
            continue
        matches = [url for slug, url in known.items()
                   if (slug + "-source") in target_name
                   or re.search(r"(?:^|[-_])" + re.escape(slug) + r"(?:\.|[-_])", target_name)]
        if len(matches) == 1:
            anchor["href"] = matches[0]
            continue
        marker = doc.new_tag("span", attrs={
            "class": "theatre-original-unresolved",
            "title": "Renvoi d’archive historique non résolu : " + href,
        })
        marker.string = anchor.get_text(" ", strip=True)
        anchor.replace_with(marker)
        unresolved += 1
    return str(doc), unresolved


def build_readers(root: Path, output: Path, records: list[dict]) -> int:
    """Publie neuf lecteurs autonomes sans perdre une ligne des sources brutes."""
    root, output = Path(root), Path(output)
    if not records:
        return 0
    slugs = [item["slug"] for item in records]
    if len(set(slugs)) != len(records):
        raise RuntimeError("Théâtre : manuscrits sources dupliqués")
    known = {item["slug"]: "/" + (BASE / (item["slug"] + "-source.html")).as_posix()
             for item in records}
    prepared = []
    for i, item in enumerate(records):
        slug = item["slug"]
        src = root / BASE / (slug + "-source.md")
        raw = src.read_bytes()
        original = raw.decode("utf-8")
        if len(original) < 8000 or not re.search(r"bibliograph", original, re.I):
            raise RuntimeError("Théâtre : manuscrit original incomplet : " + slug)
        target_raw = output / BASE / (slug + "-source.md")
        if target_raw.is_file() and target_raw.read_bytes() != raw:
            raise RuntimeError("Théâtre : manuscrit public divergent : " + slug)
        content, body, section_count = _render_text(original)
        content, unresolved = _fix_relative_links(content, src, root, output, known)
        if len(BeautifulSoup(content, "html.parser").get_text(" ", strip=True)) < 6500:
            raise RuntimeError("Théâtre : rendu anormalement court : " + slug)
        previous = known[slugs[i - 1]] if i else ""
        following = known[slugs[i + 1]] if i + 1 < len(slugs) else ""
        prepared.append((item, raw, content, section_count, unresolved, previous, following))
    # Validation des neuf sources terminée avant toute écriture.
    for item, raw, content, section_count, unresolved, previous, following in prepared:
        slug = item["slug"]
        rel_html = BASE / (slug + "-source.html")
        rel_md = BASE / (slug + "-source.md")
        page_url = "/" + rel_html.as_posix()
        raw_url = "/" + rel_md.as_posix()
        title = html.escape(item["title"], quote=True)
        cote = html.escape(item["historical_volume"])
        digest = hashlib.sha256(raw).hexdigest()
        esc = lambda v: html.escape(v, quote=True)
        links = [
            ('/theatre/#theatre-source-' + slug, 'Retour au catalogue Théâtre'),
            (item["critique"], 'Étude critique et bibliographie'),
            (item["scenes"], 'Scènes modernes distinctes'),
            (raw_url, 'Manuscrit Markdown original'),
        ]
        if previous:
            links.append((previous, '← Manuscrit précédent du parcours'))
        if following:
            links.append((following, 'Manuscrit suivant du parcours →'))
        nav = (
            '<nav class="theatre-original-nav" aria-label="Navigation entre les éditions">'
            + ''.join('<a href="' + esc(url) + '">' + esc(label) + '</a>'
                      for url, label in links) + '</nav>'
        )
        page = (
            '<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="dark">'
            '<meta name="description" content="Manuscrit universitaire intégral : '
            + title + '. Édition source sans troncature et avec références bibliographiques.">'
            '<link rel="canonical" href="https://bobmythos.fr' + esc(page_url) + '">'
            '<link rel="stylesheet" href="/assets/mythos-museum.css">'
            '<link rel="stylesheet" href="' + CSS + '">'
            '<title>' + title + ' — Manuscrit source | MYTHOS</title></head>'
            '<body class="mythos-design theatre-original-page">'
            '<a class="theatre-original-skip" href="#texte-source">Aller au texte intégral</a>'
            '<header class="theatre-original-banner"><a href="/" class="theatre-original-brand">MYTHOS</a>'
            '<p>' + ORIGINALS_LABEL + '</p><strong>Volume historique ' + cote
            + ' · manuscrit public original</strong></header>'
            '<main class="theatre-original-layout">' + nav
            + '<p class="theatre-original-context">Édition universitaire complète du dossier '
            + title + '. Les catégories de témoignages antiques, hypothèses et '
            'créations contemporaines restent distinguées dans le texte. '
            'Cette cote historique n’est pas une nouvelle attribution canonique.</p>'
            '<p class="theatre-original-checksum">Source UTF-8 : SHA-256 '
            '<code>' + digest + '</code> · ' + str(section_count)
            + ' sections au sommaire · ' + str(unresolved)
            + ' renvoi(s) historique(s) à vérifier</p>'
            '<article id="texte-source" class="theatre-original-text">'
            + content + '</article>' + nav + '</main>'
            '<footer class="theatre-original-footer"><a href="/theatre/">Théâtre grec</a>'
            ' · <a href="/mythologie-grecque/">Encyclopédie mythologique grecque</a>'
            '</footer></body></html>\n'
        )
        target_raw = output / rel_md
        target_raw.parent.mkdir(parents=True, exist_ok=True)
        if not target_raw.is_file():
            target_raw.write_bytes(raw)
        if target_raw.read_bytes() != raw:
            raise RuntimeError("Théâtre : source original non conservé : " + slug)
        target = output / rel_html
        target.write_text(page, encoding="utf-8")
    return len(prepared)
