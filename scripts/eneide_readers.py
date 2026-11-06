"""Lecteurs HTML autonomes des 18 sources publiques de l'Énéide.

Ne crée aucun numéro de collection. Le Markdown source reste copié, octet
pour octet ; l'HTML est une présentation supplémentaire, non une réécriture.
"""
from __future__ import annotations

import html
from pathlib import Path

import mistune
from bs4 import BeautifulSoup



def build_readers(out: Path, source_texts: list[tuple[str, str]], titles: list[str], source_dir: Path) -> int:
    """Rendre chaque texte sans coupure, avec cote, bibliographie et parcours mobile."""
    out = Path(out)
    if len(source_texts) != 18 or len(titles) != 18:
        raise RuntimeError("Énéide : série des manuscrits à publier incomplète")
    names = [name for name, _ in source_texts]
    if len(set(names)) != len(names) or any(Path(n).name != n or not n.endswith(".md") for n in names):
        raise RuntimeError("Énéide : noms de sources invalides ou dupliqués")
    markdown = mistune.create_markdown(escape=True, plugins=["table", "strikethrough", "url"])
    for index, ((name, original), title) in enumerate(zip(source_texts, titles)):
        if not (out / source_dir / name).is_file():
            raise RuntimeError("Énéide : copie du manuscrit source manquante ou désordonnée")
        if (out / source_dir / name).read_text(encoding="utf-8") != original:
            raise RuntimeError("Énéide : texte public divergent du manuscrit original")
        body = markdown(original)
        doc = BeautifulSoup(body, "html.parser")
        heading = doc.find("h1")
        if not heading or heading.get_text(" ", strip=True) != title:
            raise RuntimeError("Énéide : titre altéré lors du rendu HTML : " + name)
        label = html.escape(title)
        source_link = "/corpus/philosophie/eneide/" + html.escape(name, quote=True)
        prev_link = ""
        next_link = ""
        if index:
            previous = names[index - 1].removesuffix(".md") + ".html"
            prev_link = '<a rel="prev" href="/corpus/philosophie/eneide/' + previous + '">← Texte précédent</a>'
        if index + 1 < len(names):
            following = names[index + 1].removesuffix(".md") + ".html"
            next_link = '<a rel="next" href="/corpus/philosophie/eneide/' + following + '">Texte suivant →</a>'
        navigation = (
            '<nav class="eneide-reader-nav" aria-label="Parcours des manuscrits">'
            '<a href="/philosophie-eneide.html#eneide-manuscrits-originaux">Sommaire des 18 manuscrits</a>'
            '<a href="/philosophie-eneide.html#eneide-' + f"{index:02}" + '">Étude réunie</a>'
            '<a href="' + source_link + '">Texte original Markdown</a>'
            + prev_link + next_link + '</nav>'
        )
        page = (
            '<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="Texte universitaire intégral MYTHOS, Énéide de Virgile : '
            + html.escape(title[:150], quote=True) + '">'
            '<link rel="stylesheet" href="/assets/style.css">'
            '<link rel="stylesheet" href="/assets/mythos-eneide-sources.css">'
            '<title>' + label + ' — MYTHOS</title></head>'
            '<body class="mythos-design mythos-eneide-reader-page">'
            '<a class="eneide-skip" href="#texte-integral">Aller au texte intégral</a>'
            '<header class="eneide-reader-banner"><a class="eneide-reader-brand" href="/">MYTHOS</a>'
            '<p>Bibliothèque universitaire · Énéide de Virgile</p>'
            '<strong>Manuscrit ' + str(index + 1) + ' / ' + str(len(names)) + '</strong></header>'
            '<main class="eneide-reader-main"><div class="eneide-reader-inner">'
            + navigation
            + '<article id="texte-integral" class="eneide-reader-text" aria-label="Texte universitaire intégral">'
            + body + '</article>'
            + '<p class="eneide-reader-note">Cette édition HTML présente la source intégrale, '
            'sans retrancher ses notes, références ni bibliographie. '
            'Le fichier Markdown original est conservé à l’identique.</p>'
            + navigation
            + '</div></main><footer class="eneide-reader-footer">'
            '<a href="/philosophie/">Philosophie et interprétations</a> · '
            '<a href="/mythologie-grecque/">Encyclopédie grecque</a></footer>'
            '</body></html>\n'
        )
        target = out / source_dir / (name.removesuffix(".md") + ".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
    return len(source_texts)
