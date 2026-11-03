"""Resolve the documented ODS 576/577 collision without changing manuscripts.

Only the four named sources are classified here. Unknown duplicate numbers still
fail the original navigation builder. See EDITORIAL_INCIDENT_ORIGINES_576_577_20261103.md.
"""
from pathlib import Path
import hashlib
import json
import re
from bs4 import BeautifulSoup

BASE = "/chapitres/origines-du-sacre/"
CANONICAL = {
    576: BASE + "576-bacs-peages-offrandes-passage/",
    577: BASE + "577-monnaies-funeraires-charon-preuves-archeologiques/",
}
COMPLEMENTS = {
    BASE + "576-payer-pour-passer-tarifs-bacs-offrandes/": {
        "id": "ODS-C-576-A",
        "title": "Complément documentaire au chapitre 576 — Tarifs, redevances et offrandes",
        "canonical": CANONICAL[576],
        "reason": "Version parallèle conservée intégralement ; le numéro 576 désigne la première version enregistrée sur main.",
    },
    BASE + "577-naufrages-secours-divins-survivants/": {
        "id": "ODS-C-577-A",
        "title": "Complément au cycle des passages — Naufrages et secours divins",
        "canonical": CANONICAL[577],
        "reason": "Étude autonome conservée intégralement, sans nouveau numéro de chapitre ; l'identifiant historique 577 était déjà attribué à l'étude des monnaies funéraires.",
    },
}


def source_path(url):
    return Path(url.strip("/") + ".md")


def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preserve_sources():
    snapshots = {}
    for url in [*CANONICAL.values(), *COMPLEMENTS]:
        path = source_path(url)
        if not path.is_file() or path.stat().st_size < 10000:
            raise RuntimeError("Source intégrale de réconciliation absente ou abrégée : " + str(path))
        snapshots[str(path)] = source_hash(path)
    return snapshots


def verify_sources(snapshots):
    for name, expected in snapshots.items():
        path = Path(name)
        if not path.is_file() or source_hash(path) != expected:
            raise RuntimeError("Un manuscrit protégé a changé pendant la génération : " + name)


def annotate_page(out, url, title, message, target, identifier):
    path = out / url.lstrip("/") / "index.html"
    if not path.is_file():
        raise RuntimeError("Page de réconciliation non générée : " + str(path))
    doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = doc.select_one("article.content")
    if article is None:
        raise RuntimeError("Article introuvable : " + str(path))
    if title:
        heading = article.find("h1")
        if heading is None:
            raise RuntimeError("Titre source absent : " + str(path))
        heading.string = title
        if doc.title:
            doc.title.string = title + " | MYTHOS"
    previous = article.find(id=identifier)
    if previous:
        previous.decompose()
    note = doc.new_tag("aside", attrs={"class": "editorial-note", "id": identifier})
    p = doc.new_tag("p")
    p.string = message + " Les repères internes anciens sont conservés pour permettre les citations ; ils ne créent pas un second chapitre canonique. "
    a = doc.new_tag("a", href=target)
    a.string = "Consulter le dossier associé et sa place dans la série."
    p.append(a)
    note.append(p)
    article.insert(1, note)
    path.write_text(str(doc), encoding="utf-8")


def install(navigation, chapters):
    """Install one explicit catalogue reconciliation; leave all .md bytes intact."""
    snapshots = preserve_sources()
    available = {entry["url"] for entry in chapters}
    if not set([*CANONICAL.values(), *COMPLEMENTS]).issubset(available):
        raise RuntimeError("Les quatre études de l'incident doivent toutes être publiées.")
    out = navigation.OUT
    for url, spec in COMPLEMENTS.items():
        annotate_page(out, url, spec["title"], spec["reason"], spec["canonical"], spec["id"])
        for entry in chapters:
            if entry["url"] == url:
                entry["title"] = spec["title"]
                entry["excerpt"] = spec["reason"][:190]
    for number, url in CANONICAL.items():
        other = next(u for u, spec in COMPLEMENTS.items() if spec["canonical"] == url)
        annotate_page(out, url, None,
            "Chapitre canonique " + str(number) + ". Une étude supplémentaire issue de la rédaction parallèle reste accessible séparément.",
            other, "ods-canonical-" + str(number))
    original = navigation.create_origins

    def reconciled_origins(entries):
        canonical_entries = [entry for entry in entries if entry["url"] not in COMPLEMENTS]
        # The original duplicate, historical-corpus and archive checks stay active.
        original(canonical_entries)
        numbered = {}
        for entry in canonical_entries:
            match = re.fullmatch(re.escape(BASE) + r"(\d+)-[^/]+/", entry["url"])
            if not match:
                continue
            number = int(match.group(1))
            if number in numbered:
                raise RuntimeError("Nouveau doublon non résolu : " + str(number))
            numbered[number] = entry
        for number, url in CANONICAL.items():
            if numbered.get(number, {}).get("url") != url:
                raise RuntimeError("Identité canonique altérée : " + str(number))
        page = out / "origines-du-sacre/index.html"
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        article = doc.select_one("article.content")
        section = doc.new_tag("section", attrs={"class": "portal-section", "id": "chapitres-recents"})
        h2 = doc.new_tag("h2")
        h2.string = "Suite des études — chapitres 491 et suivants"
        section.append(h2)
        intro = doc.new_tag("p")
        intro.string = "Numéros éditoriaux conservés. Les compléments issus de la rédaction parallèle sont classés séparément, sans suppression de texte."
        section.append(intro)
        listing = doc.new_tag("ol", attrs={"class": "chapter-list origins-index"})
        for number, entry in sorted(numbered.items()):
            if number < 491:
                continue
            source = source_path(entry["url"])
            raw = source.read_text(encoding="utf-8")
            subtitle = re.search(r"(?m)^##\s+(.+)$", raw)
            label = subtitle.group(1) if subtitle else entry["title"]
            li = doc.new_tag("li", attrs={"data-chapter": str(number)})
            a = doc.new_tag("a", href=entry["url"])
            a.string = "Chapitre " + str(number) + " — " + label
            li.append(a)
            listing.append(li)
        section.append(listing)
        h3 = doc.new_tag("h3")
        h3.string = "Compléments documentaires — textes intégraux conservés"
        section.append(h3)
        for url, spec in COMPLEMENTS.items():
            p = doc.new_tag("p")
            a = doc.new_tag("a", href=url)
            a.string = spec["id"] + " — " + spec["title"]
            p.append(a)
            section.append(p)
        archives = article.select_one(".origins-archives")
        if archives:
            archives.insert_before(section)
        else:
            article.append(section)
        for p in article.select("p.portal-lead"):
            if p.get_text().startswith("Quarante-huit chapitres"):
                p.string = "Les 48 dossiers historiques restent intégraux. Les études suivantes sont accessibles dans la liste continue ci-dessus ; les tomes et manuscrits archivés conservent leur propre ordre."
        page.write_text(str(doc), encoding="utf-8")
        report = {
            "policy": "first_confirmed_commit_per_number; later_parallel_texts_are_preserved_complements",
            "canonical": {str(n): e["url"] for n, e in sorted(numbered.items())},
            "complements": COMPLEMENTS,
            "last_numbered_chapter": max(numbered),
            "preserved_source_sha256": snapshots,
        }
        target = out / "catalog/origines-continuity.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        verify_sources(snapshots)
        print("ODS : collisions 576/577 résolues ; quatre sources inchangées ; dernier chapitre", max(numbered), flush=True)

    navigation.create_origins = reconciled_origins
    return snapshots
