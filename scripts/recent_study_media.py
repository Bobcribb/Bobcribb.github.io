"""Associer aux études récentes une image documentaire réellement pertinente.

Les images de collection génériques (Saqqarah pour le Sahara, Ninive pour
Aristophane, Delphes pour un culte spartiate) ne constituent pas des preuves du
sujet traité. Ce sélecteur préfère l'absence d'image à une association trompeuse.
Aucune image nouvelle ni reconstitution synthétique n'est créée.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

# Un motif nécessite un sujet explicite dans le titre OU dans le slug.
# L'image est documentaire / comparative, jamais une illustration de la pièce
# perdue elle-même. Son statut figure aussi dans la notice source du catalogue.
RULES = {
    "origines-du-sacre": (
        (r"\bounas\b", "mythos-ounas-chambre-funeraire-vincent-brown",
         "Pyramide d’Ounas : exemple égyptien documenté, non modèle général du sacré."),
        (r"\bdelphes\b", "delphes-temple-apollon-bernard-gagnon",
         "Delphes : vestiges du sanctuaire, non restitution d’une cérémonie."),
        (r"\bderveni\b", "mythos-derveni-papyrus-fragments-thessalonique-gts-tg",
         "Papyrus de Derveni : témoin matériel de transmission textuelle."),
    ),
    "encyclopedie": (
        (r"\bathena\b", "mythos-athena-lecythe-brygos-aplaste-met-25-189-1",
         "Athéna sur un vase attique ; ne documente pas un sanctuaire particulier."),
        (r"\bartemis\b", "mythos-artemis-faon-lecythe-peintre-providence-met-41-162-18",
         "Artémis sur un vase grec ; représentation distincte du culte étudié."),
        (r"\bdelphes\b", "delphes-temple-apollon-bernard-gagnon",
         "Delphes : vestiges archéologiques du sanctuaire d’Apollon."),
        (r"\bdionysos\b", "mythos-dionysos-kylix-brygos-bnf-576",
         "Dionysos sur une coupe attique ; image de mythe, non rituel photographié."),
    ),
    "comedies": (
        (r"\b(?:aristophane|menekrates)\b", "mythos-met-844483-acteurs-comiques-grecs",
         "Figurines antiques d’acteurs comiques : contexte du genre, non représentation de cette pièce."),
    ),
    "tragedies": (
        (r"\bdelphes\b", "delphes-temple-apollon-bernard-gagnon",
         "Delphes : vestiges d’un sanctuaire lié au dossier, non décor théâtral."),
        (r"\bepidaure\b", "epidaure-theatre-antique-zde",
         "Théâtre d’Épidaure : monument archéologique, non scène de la tragédie."),
    ),
    "comparatif": (
        (r"\baristophane\b", "mythos-met-844483-acteurs-comiques-grecs",
         "Figurines d’acteurs comiques : contexte d’Aristophane, non scène des Oiseaux."),
        (r"\benuma\b", "mythos-enuma-elish-tablette-k3473-ninive-zunkir",
         "Tablette d’Enūma eliš : témoin matériel du texte mésopotamien."),
        (r"\bderveni\b", "mythos-derveni-papyrus-fragments-thessalonique-gts-tg",
         "Papyrus de Derveni : témoin grec conservé, non illustration de la comparaison."),
    ),
}


def _normalized(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", value.casefold())
                   if not unicodedata.combining(c))


def documented_image(root: Path, output: Path, collection: str,
                     title: str, slug: str) -> dict:
    """Retourne média, alt, crédit et limite d'interprétation ou dict vide.

    Le catalogue et le fichier de média doivent tous deux exister. L'image
    reste optionnelle : son absence ne peut bloquer la publication des textes.
    """
    root, output = Path(root), Path(output)
    catalog_path = root / "scripts/editorial_media.json"
    if not catalog_path.is_file():
        return {}
    haystack = _normalized(title + " " + slug.replace("-", " "))
    match = next(((media_id, caption)
                  for regex, media_id, caption in RULES.get(collection, ())
                  if re.search(regex, haystack)), None)
    if not match:
        return {}
    media_id, caveat = match
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    records = catalog.get("media", [])
    ids = {record.get("id"): record for record in records}
    if len(ids) != len(records):
        raise RuntimeError("MYTHOS : catalogue iconographique aux identifiants dupliqués")
    record = ids.get(media_id)
    if not record:
        return {}
    path = record.get("path", "")
    allowed = path.startswith(("media/2026/10/", "assets/illustrations-articles/"))
    safe = path.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    if (not allowed or not safe or not record.get("alt")
            or not record.get("caption_html") or not (output / path).is_file()):
        return {}
    return {
        "image": "/" + path, "alt": record["alt"], "illustration": caveat,
        "credit_html": record["caption_html"], "media_id": media_id,
    }
