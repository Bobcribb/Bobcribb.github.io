#!/usr/bin/env python3
"""Garde de conservation de la prose des volumes MYTHOS historiques.

La sérialisation des éléments HTML peut changer pendant la publication.
L'empreinte porte donc sur chaque mot et sa position, indépendamment des balises.
Les empreintes de référence viennent des corps WordPress originaux récupérés.
"""
from __future__ import annotations
from hashlib import sha1
from pathlib import Path
import re

ENTITIES = {"amp":"&", "lt":"<", "gt":">", "quot":'"', "apos":"'",
            "nbsp":" ", "ndash":"–", "mdash":"—", "hellip":"…"}
ENTITY = re.compile(r"&(#x[0-9a-f]+|#[0-9]+|amp|lt|gt|quot|apos|nbsp|ndash|mdash|hellip);", re.I)


def extract_original_body(html: str, element_id: str) -> str:
    opening = re.search(
        r'<div\b[^>]*\bid\s*=\s*["\']' + re.escape(element_id) + r'["\'][^>]*>',
        html, re.I,
    )
    if opening is None:
        raise AssertionError("Corps universitaire introuvable : " + element_id)
    footer = html.find("mythos-world-study-crosslinks", opening.end())
    if footer < 0:
        raise AssertionError("Renvois de fin absents : " + element_id)
    close = html.rfind("</div>", opening.end(), footer)
    if close <= opening.end():
        raise AssertionError("Corps universitaire sans fermeture : " + element_id)
    return html[opening.end():close].strip()


def normalize_prose(fragment: str) -> str:
    # Les figures documentaires ajoutées après la reprise WordPress sont des
    # notices iconographiques, non de la prose du manuscrit patrimonial.
    # Ignorer uniquement les figures étiquetées par le générateur éditorial.
    fragment = re.sub(
        r'<figure\b[^>]*\bclass="mythos-editorial-inline"[^>]*'
        r'\bdata-editorial-inline="subject-v3"[^>]*>[\s\S]*?</figure>',
        " ", fragment, flags=re.I)
    plain = re.sub(r"<!--[\s\S]*?-->", " ", fragment)
    plain = re.sub(r"<[^>]*>", " ", plain)

    def decode(match):
        name = match.group(1).lower()
        if name.startswith("#x"):
            return chr(int(name[2:], 16))
        if name.startswith("#"):
            return chr(int(name[1:]))
        return ENTITIES.get(name, match.group())

    plain = ENTITY.sub(decode, plain)
    return " ".join(plain.split())


def git_sha(text: str) -> str:
    data = text.encode("utf-8")
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def verify(path: Path, node_id: str, length: int, git_digest: str) -> str:
    markup = extract_original_body(Path(path).read_text(encoding="utf-8"), node_id)
    prose = normalize_prose(markup)
    if len(prose) != length:
        raise AssertionError(f"Longueur scientifique altérée : {path}: {len(prose)}")
    result = git_sha(prose)
    if result != git_digest:
        raise AssertionError(f"Prose scientifique altérée : {path}: {result}")
    return prose
