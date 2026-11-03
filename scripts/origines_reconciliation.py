"""Resolve documented ODS 576/577 aliases without changing manuscripts.

Only named historical URLs are excluded from canonical numbering. All original
sources remain byte-identical; every unknown duplicate still fails the builder.
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
        "id": "ODS-ALIAS-576",
        "title": "Adresse historique — Annexe documentaire du chapitre 576",
        "canonical": CANONICAL[576],
        "target": BASE + "annexe-576-payer-pour-passer-variante/",
        "reason": "Version parallèle conservée intégralement en annexe, sans second chapitre 576.",
    },
    BASE + "577-naufrages-secours-divins-survivants/": {
        "id": "ODS-ALIAS-577",
        "title": "Adresse historique — Naufrages et secours divins, chapitre 580",
        "canonical": CANONICAL[577],
        "target": BASE + "580-naufrages-secours-divins-survivants/",
        "reason": "Étude autonome reprise intégralement au chapitre 580 ; le numéro 577 reste réservé aux monnaies funéraires.",
    },
}


def source_path(url):
    return Path(url.strip("/") + ".md")


def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified_redirects():
    path = Path("EDITORIAL_REDIRECTS.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = {url: spec["target"] for url, spec in COMPLEMENTS.items()}
    if data.get("version") != 1 or data.get("redirects") != expected:
        raise RuntimeError("Le registre des redirections ne correspond pas à la réconciliation explicite.")
    for source, target in expected.items():
        if not re.fullmatch(r"/chapitres/origines-du-sacre/[a-z0-9][a-z0-9-]*/", target):
            raise RuntimeError("Cible de redirection non locale ou invalide : " + target)
        if source == target or target in expected:
            raise RuntimeError("Boucle ou chaîne de redirection interdite : " + source)
    return expected


def preserve_sources():
    snapshots = {}
    urls = [*CANONICAL.values(), *COMPLEMENTS,
            *(spec["target"] for spec in COMPLEMENTS.values())]
    for url in urls:
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


def annotate_page(out, url, title, message, target, identifier, redirect=False):
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
    p.string = message + " Le manuscrit historique reste conservé sans modification. "
    a = doc.new_tag("a", href=target)
    a.string = "Lire la version intégrale à son adresse définitive."
    p.append(a)
    note.append(p)
    article.insert(1, note)
    if redirect:
        if doc.head is None:
            raise RuntimeError("En-tête HTML absent : " + str(path))
        for node in doc.head.select('meta[http-equiv="refresh"], meta[name="robots"], link[rel="canonical"]'):
            node.decompose()
        doc.head.append(doc.new_tag("meta", attrs={"http-equiv": "refresh", "content": "0;url=" + target}))
        doc.head.append(doc.new_tag("meta", attrs={"name": "robots", "content": "noindex,follow"}))
        doc.head.append(doc.new_tag("link", attrs={"rel": "canonical", "href": "https://bobmythos.fr" + target}))
    path.write_text(str(doc), encoding="utf-8")


def install(navigation, chapters):
    """Install explicit aliases while leaving all Markdown source bytes intact."""
    redirects = verified_redirects()
    snapshots = preserve_sources()
    available = {entry["url"] for entry in chapters}
    required = set([*CANONICAL.values(), *COMPLEMENTS, *redirects.values()])
    if not required.issubset(available):
        raise RuntimeError("Sources historiques et cibles intégrales doivent toutes être publiées.")
    out = navigation.OUT
    for url, spec in COMPLEMENTS.items():
        annotate_page(out, url, spec["title"], spec["reason"], spec["target"], spec["id"], redirect=True)
        for entry in chapters:
            if entry["url"] == url:
                entry["title"] = spec["title"]
                entry["excerpt"] = spec["reason"][:190]
    for number, url in CANONICAL.items():
        spec = next(spec for spec in COMPLEMENTS.values() if spec["canonical"] == url)
        annotate_page(out, url, None,
            "Chapitre canonique " + str(number) + ". Le texte issu de la rédaction parallèle possède désormais une adresse distincte.",
            spec["target"], "ods-canonical-" + str(number))
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
        if article is None:
            raise RuntimeError("Portail des origines sans article.")
        previous = article.find(id="chapitres-recents")
        if previous:
            previous.decompose()
        section = doc.new_tag("section", attrs={"class": "portal-section", "id": "chapitres-recents"})
        h2 = doc.new_tag("h2")
        h2.string = "Suite des études — chapitres 491 et suivants"
        section.append(h2)
        intro = doc.new_tag("p")
        intro.string = "Numéros éditoriaux conservés. Les anciennes adresses en conflit renvoient aux textes intégraux réconciliés, sans suppression de manuscrit."
        section.append(intro)
        listing = doc.new_tag("ol", attrs={"class": "chapter-list origins-index"})
        for number, entry in sorted(numbered.items()):
            if number < 491:
                continue
            raw = source_path(entry["url"]).read_text(encoding="utf-8")
            subtitle = re.search(r"(?m)^##\s+(.+)$", raw)
            label = subtitle.group(1) if subtitle else entry["title"]
            li = doc.new_tag("li", attrs={"data-chapter": str(number)})
            a = doc.new_tag("a", href=entry["url"])
            a.string = "Chapitre " + str(number) + " — " + label
            li.append(a)
            listing.append(li)
        section.append(listing)
        h3 = doc.new_tag("h3")
        h3.string = "Annexe documentaire — version parallèle conservée"
        section.append(h3)
        p = doc.new_tag("p")
        a = doc.new_tag("a", href=COMPLEMENTS[BASE + "576-payer-pour-passer-tarifs-bacs-offrandes/"]["target"])
        a.string = "Annexe au chapitre 576 — Tarifs, redevances et offrandes"
        p.append(a)
        section.append(p)
        archives = article.select_one(".origins-archives")
        if archives:
            archives.insert_before(section)
        else:
            article.append(section)
        for p in article.select("p.portal-lead"):
            if p.get_text().startswith("Quarante-huit chapitres"):
                p.string = "Les 48 dossiers historiques restent intégraux. Les études suivantes sont accessibles dans la liste continue ; les tomes et manuscrits archivés conservent leur propre ordre."
        page.write_text(str(doc), encoding="utf-8")
        report = {
            "policy": "first_confirmed_commit_per_number; explicit_historical_aliases; recovered_shipwreck_study_580",
            "canonical": {str(n): e["url"] for n, e in sorted(numbered.items())},
            "historical_aliases": COMPLEMENTS,
            "redirects": redirects,
            "last_numbered_chapter": max(numbered),
            "preserved_source_sha256": snapshots,
        }
        target = out / "catalog/origines-continuity.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        verify_sources(snapshots)
        print("ODS : aliases 576/577 résolus ; six sources intégrales inchangées ; dernier chapitre", max(numbered), flush=True)

    navigation.create_origins = reconciled_origins
    return snapshots
