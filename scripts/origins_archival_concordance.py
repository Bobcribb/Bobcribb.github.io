"""Concordance documentaire des tomes historiques des Origines du sacré.

Aucune attribution de numéro ; aucun changement des manuscrits. Les images sont
des exemples attestés, non des reconstitutions des rites de chaque tradition.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import html
import json
import re

# Une image n'illustre qu'un exemple précisément identifié du thème du tome.
ILLUSTRATIONS = {
    "ODS-CONV-XXV": ("delphes-temple-apollon-bernard-gagnon",
                     "Exemple grec : ruines du sanctuaire de Delphes, non modèle universel."),
    "ODS-CONV-XXVI": ("delos-plan-aire-sacree-tomisti",
                      "Exemple grec : le lac sacré de Délos sur un plan scientifique moderne."),
    "ODS-CONV-XXXI": ("mythos-artemis-ephesienne-statue-musee-selcuk-furkan-akkurt",
                      "Exemple : image cultuelle d’Artémis à Éphèse, interprétations discutées."),
    "ODS-CONV-XXXII": ("mythos-masques-theatre-rondelles-hellenistiques-met-2001-767",
                       "Exemple théâtral hellénistique ; ne documente pas la possession rituelle."),
    "ODS-CONV-XXXIII": ("mythos-enheduanna-disque-penn-museum-mefman00",
                        "Exemple mésopotamien : disque d’une prêtresse, non manuscrit de ses hymnes."),
}

# Numéros déjà attribués et vérifiés sur main. Ce sont des liens vers les
# études intégrales, pas de nouvelles notices ni de nouvelles attributions.
READINGS = (
    ("499", "Grèce — consacrer l’espace et instituer un sanctuaire",
     "499-grece-consecration-dedicace-sanctuaires"),
    ("500", "Mésopotamie — Gudéa et la fondation de l’E-ninnu",
     "500-mesopotamie-fondation-temples-gudea"),
    ("501", "Égypte — Séchat et l’étirement du cordeau",
     "501-egypte-fondation-cordeau-seshat"),
    ("502", "Inde — pratiṣṭhā et installation des images",
     "502-inde-pratistha-images-temples"),
)


def enrich(fragment: str, output: Path, root: Path) -> str:
    """Ajoute illustrations sourcées et lecture croisée à un sommaire existant.

    Les lecteurs et les sources universitaires ne sont jamais modifiés. Pour les
    tests d'archives isolés, les dossiers optionnels absents sont ignorés ; dès
    que le catalogue ou les sources canoniques existent, leur validité est
    obligatoire afin de ne pas publier de liens ou de médias cassés.
    """
    output, root = Path(output), Path(root)
    doc = BeautifulSoup(fragment, "html.parser")
    shelf = doc.select_one("#origines-archives-documentaires")
    grid = doc.select_one(".origins-archival-grid")
    if shelf is None or grid is None:
        raise RuntimeError("Sommaire ODS : structure documentaire absente")

    catalogue = root / "scripts" / "editorial_media.json"
    if catalogue.is_file():
        data = json.loads(catalogue.read_text(encoding="utf-8"))
        records = data.get("media", [])
        indexed = {item["id"]: item for item in records}
        if len(indexed) != len(records):
            raise RuntimeError("ODS : doublon dans le catalogue iconographique")
        for anchor in grid.select("a.origins-archival-card[href]"):
            # Préserver le lien de lecture de chaque manuscrit comme seule action
            # principale : crédits dans un <details> frère, jamais un lien imbriqué.
            code = anchor.select_one(".origins-archival-code")
            if code is None:
                raise RuntimeError("ODS : cote de carte introuvable")
            key = code.get_text(" ", strip=True).split(" · ", 1)[0]
            tile = doc.new_tag("article", attrs={"class": "origins-archival-tile"})
            anchor.wrap(tile)
            if key not in ILLUSTRATIONS:
                continue
            media_id, contextual_note = ILLUSTRATIONS[key]
            record = indexed.get(media_id)
            if not record:
                raise RuntimeError("ODS : notice iconographique absente : " + media_id)
            path = record.get("path", "")
            if (not path.startswith("media/2026/10/")
                or not path.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
                or not (output / path).is_file()
                or not record.get("alt") or not record.get("caption_html")):
                raise RuntimeError("ODS : média, provenance ou légende absents : " + media_id)
            pic = doc.new_tag("img", attrs={
                "class": "origins-archival-image", "src": "/" + path,
                "alt": record["alt"], "loading": "lazy", "decoding": "async",
            })
            anchor.insert(0, pic)
            credit = doc.new_tag("details", attrs={"class": "origins-archival-credit"})
            summary = doc.new_tag("summary")
            summary.string = "Document, datation et crédit"
            credit.append(summary)
            note = doc.new_tag("p")
            note.string = contextual_note
            credit.append(note)
            credit.append(BeautifulSoup(
                "<div>" + record["caption_html"] + "</div>", "html.parser"
            ).div)
            tile.append(credit)

    canonical = root / "chapitres" / "origines-du-sacre"
    if canonical.is_dir():
        cards = []
        for number, label, slug in READINGS:
            source = canonical / (slug + ".md")
            reader = output / "chapitres" / "origines-du-sacre" / slug / "index.html"
            if not source.is_file() or not reader.is_file():
                raise RuntimeError("ODS : lecture canonique intégrale absente : " + slug)
            manuscript = source.read_text(encoding="utf-8")
            markup = reader.read_text(encoding="utf-8")
            if (len(manuscript) < 9000 or len(markup) < 9000
                or not re.search(r"bibliograph|références|sources", manuscript, re.I)
                or not re.search(r"<main\b|<article\b", markup, re.I)):
                raise RuntimeError("ODS : étude canonique non vérifiée : " + slug)
            href = "/chapitres/origines-du-sacre/" + slug + "/"
            cards.append(
                '<li><a href="' + html.escape(href, quote=True) + '">'
                '<span>Chapitre canonique ' + number + '</span><strong>'
                + html.escape(label) + '</strong><small>Texte intégral et références'
                ' · cote distincte des archives XXV–XXXIII</small></a></li>'
            )
        block = BeautifulSoup(
            '<section class="origins-archival-concordance" id="origines-etudes-fondations" '
            'aria-labelledby="origines-etudes-fondations-titre">'
            '<h3 id="origines-etudes-fondations-titre">Quatre études canoniques à lire en regard</h3>'
            '<p>Confrontation de quatre traditions de consécration et de fondation. '
            'Ces manuscrits sont déjà publiés et conservent leurs numéros, leurs sources et '
            'leurs bibliographies ; les liens ci-dessous conduisent aux éditions complètes.</p>'
            '<ul>' + "".join(cards) + '</ul></section>',
            "html.parser",
        ).section
        shelf.append(block)
    return str(doc)
