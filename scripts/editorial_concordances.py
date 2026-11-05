"""Concordances MYTHOS : préserver les volumes distincts et leurs sources."""
from collections import defaultdict
from hashlib import sha256
from html import escape
import json
from pathlib import Path
from bs4 import BeautifulSoup

PAIRS = {
    "chalkioikos": {
        "title": "Athéna Chalkioikos — deux lectures du même sanctuaire",
        "description": "Les chapitres 449 et 454 étudient l’acropole de Sparte, Gitiadas, les bronzes, Athéna Poliouchos et l’asile. Leurs numéros et leurs textes restent distincts ; il ne s’agit pas de deux sanctuaires indépendants.",
        "portal": "mythologie-grecque/dossiers/cultes-sanctuaires/index.html",
        "members": [
            ("encyclopedie", "341e66ee-4e95-4c9f-8530-ef19edbc2b88", 449,
             "449 — étude du sanctuaire et du droit d’asile",
             "Bronzes, magistrats, Thucydide et pratiques civiques"),
            ("encyclopedie", "30fdb5ad-ff4b-4f0b-8bf2-819c0a97874b", 454,
             "454 — lecture parallèle de Chalkioikos et Poliouchos",
             "Épiclèses, répertoire figuré, Gitiadas et mémoire politique"),
        ],
    },
    "menekrates": {
        "title": "Ménécrate — Hermioneus et Manektōr, deux études critiques",
        "description": "Les volumes 122 et 123 utilisent la Souda μ 601 et traitent tous deux Hermioneus. Le volume 123 étudie aussi Manektōr et le vers sur les osselets. Les scènes créées aujourd’hui ne sont pas des fragments antiques retrouvés.",
        "portal": "theatre/index.html",
        "members": [
            ("comedies", "4f6c2f90-21e7-4495-a7dc-7d7f01f32c06", 122,
             "CXXII (122) — Hermioneus",
             "La Souda, l’ethnique et la cité d’Hermione"),
            ("comedies", "b48f16e3-6ac1-40a4-97a7-c70b4d319c5a", 123,
             "CXXIII (123) — Hermioneus, Manektōr et les osselets",
             "Deux titres, lexiques et fragment d’une comédie perdue"),
        ],
    },
}

LACONIA = (
    ("/chapitres/encyclopedie/chapitre-439-apollon-karneios-karneia-sparte-thera-cyrene-messene-rites-musique/",
     "439 — Apollon Karneios", "Karnéia et liens avec Théra et Cyrène"),
    ("/chapitres/encyclopedie/chapitre-443-artemis-orthia-sparte-lygos-masques-fouet-sanctuaire/",
     "443 — Artémis Orthia", "Limnaion, masques votifs et rites"),
    ("/chapitres/encyclopedie/chapitre-449-athena-chalkioikos-sparta-acropole-gitiadas-bronze-asylie/",
     "449 — Athéna Chalkioikos", "Acropole, bronze et droit d’asile"),
    ("/chapitres/encyclopedie/chapitre-452-helene-menelas-menelaion-therapne-epigraphie-cultes-memoire/",
     "452 — Hélène et Ménélas", "Ménélaion de Thérapné"),
    ("/chapitres/encyclopedie/chapitre-453-apollon-amyklaios-hyakinthos-amyklaion-hyakinthies-bathykles/",
     "453 — Apollon Amyklaios", "Amyclées et les Hyakinthies"),
)


def validate_sources(root, out):
    state = json.loads((root / "editorial/numbering.json").read_text(encoding="utf-8"))
    groups = {}
    for key, spec in PAIRS.items():
        items = []
        for collection, uid, number, title, context in spec["members"]:
            receipt = state["collections"][collection]["allocations"].get(uid)
            if not receipt or receipt["number"] != number:
                raise ValueError("Reçu canonique manquant : " + uid)
            source_path = Path(receipt["path"])
            if source_path.parent != Path("chapitres") / collection:
                raise ValueError("Collection incorrecte : " + str(source_path))
            request = root / "editorial/inbox" / (uid + ".json")
            source = root / source_path
            url = "/" + source_path.with_suffix("").as_posix() + "/"
            reader = out / url.strip("/") / "index.html"
            if not source.is_file() or not reader.is_file() or not request.is_file():
                raise ValueError("Étude intégrale inaccessible : " + url)
            if sha256(request.read_bytes()).hexdigest() != receipt["request_sha256"]:
                raise ValueError("Demande historique altérée : " + uid)
            text = source.read_text(encoding="utf-8")
            if len(text) < 30000 or "bibliograph" not in text.casefold():
                raise ValueError("Étude incomplète : " + url)
            items.append((url, title, context))
        groups[key] = items
    for url, title, context in LACONIA:
        source = root / (url.strip("/") + ".md")
        reader = out / url.strip("/") / "index.html"
        if not source.is_file() or not reader.is_file():
            raise ValueError("Parcours Laconie absent : " + url)
        text = source.read_text(encoding="utf-8")
        if len(text) < 30000 or "bibliograph" not in text.casefold():
            raise ValueError("Étude lacédémonienne incomplète : " + url)
    return groups


def panel(key, title, description, studies, own=None, kind="aside"):
    entries = "".join(
        '<li><a href="' + escape(url, quote=True) + '">' + escape(label) +
        '</a><small>' + escape(context) + '</small></li>'
        for url, label, context in studies if url != own
    )
    return (
        '<' + kind + ' class="mythos-concordance" '
        'data-mythos-concordance="' + escape(key, quote=True) + '" '
        'aria-label="' + escape(title, quote=True) + '">'
        '<h2>' + escape(title) + '</h2><p>' + escape(description) + '</p>'
        '<ul>' + entries + '</ul></' + kind + '>'
    )


def install(root, out):
    """Ajouter des panneaux après le lecteur, sans toucher aux articles."""
    root, out = Path(root), Path(out)
    groups = validate_sources(root, out)
    additions = defaultdict(list)
    portals = defaultdict(list)
    for key, spec in PAIRS.items():
        entries = groups[key]
        for url, _, _ in entries:
            additions[url].append(panel(key, spec["title"], spec["description"],
                                        entries, own=url))
        portals[spec["portal"]].append(
            panel(key, spec["title"], spec["description"], entries,
                  kind="section"))
    title = "Laconie — cinq sanctuaires, cinq monographies intégrales"
    lead = ("Karnéia, Orthia, Chalkioikos, Ménélaion et Amyklaion. La proximité "
            "géographique ne prouve pas un rite commun. Le chapitre 454 "
            "est une seconde étude du sanctuaire d’Athéna présenté au 449.")
    for url, _, _ in LACONIA:
        additions[url].append(panel("laconie", title, lead, LACONIA, own=url))
    portals["mythologie-grecque/dossiers/cultes-sanctuaires/index.html"].append(
        panel("laconie", title, lead, LACONIA, kind="section"))
    for url, snippets in additions.items():
        path = out / url.strip("/") / "index.html"
        doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        main = doc.find("main")
        article = main.select_one("article.content") if main else None
        if article is None:
            raise ValueError("Article sans conteneur universitaire : " + url)
        before = str(article)
        for old in main.select("aside[data-mythos-concordance]"):
            old.decompose()
        for html in snippets:
            main.append(BeautifulSoup(html, "html.parser").aside)
        if str(article) != before:
            raise ValueError("Texte source altéré : " + url)
        path.write_text(str(doc), encoding="utf-8")
    for rel, snippets in portals.items():
        path = out / rel
        if not path.is_file():
            raise ValueError("Portail absent : " + rel)
        doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        main = doc.select_one("main article.content") or doc.find("main")
        if main is None:
            raise ValueError("Portail sans article : " + rel)
        for old in main.select("section[data-mythos-concordance]"):
            old.decompose()
        for html in snippets:
            main.append(BeautifulSoup(html, "html.parser").section)
        path.write_text(str(doc), encoding="utf-8")
    return {"readers": len(additions), "panels": sum(map(len, additions.values())),
            "portals": len(portals)}
