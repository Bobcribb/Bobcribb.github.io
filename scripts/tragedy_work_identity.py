#!/usr/bin/env python3
"""Concordance des œuvres tragiques : une identité antique, plusieurs études.

Suit le protocole éprouvé pour MC-025 : exceptions explicites et empreintes des
manuscrits, rendus enrichis séparément et refus des nouvelles attributions en
collision. Les sources, reçus, numéros et historiques ne sont jamais réécrits.
"""
from collections import Counter
from hashlib import sha1
from html import escape
import json
from pathlib import Path
import re
import unicodedata

from bs4 import BeautifulSoup

REGISTRY = Path("editorial/tragedy-works.json")
REPORT = Path("catalog/tragedy-works.json")


def normalized(value):
    """Comparable across French accents, apostrophes, Greek accents and spaces."""
    raw = unicodedata.normalize("NFD", value.casefold())
    raw = "".join(c for c in raw if unicodedata.category(c) != "Mn")
    return " ".join(re.findall(r"[a-z0-9\u0370-\u03ff]+", raw))


def headings(raw):
    return " ".join(re.findall(r"(?m)^#{1,2}\s+(.+)$", raw)[:3])


def load(root):
    path = Path(root) / REGISTRY
    if not path.is_file():
        return {"version": 1, "groups": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("groups"), dict):
        raise ValueError("Registre d'identités tragiques invalide")
    return data


def work_key(raw, groups):
    """Use manuscript titles, not incidental words in the analysis or its slug."""
    title = " " + normalized(headings(raw)) + " "
    for key, group in groups.items():
        author = " " + normalized(group["author"]) + " "
        if author not in title:
            continue
        for alias in group["aliases"]:
            if " " + normalized(alias) + " " in title:
                return key
    return None


def url(member):
    return "/" + Path(member["source"]).with_suffix("").as_posix() + "/"


def display_title(group, member):
    return (f"Volume {member['roman']} ({member['number']}) — Sophocle, "
            f"{'La Revendication d’Hélène' if member['role'] == 'primary' else 'La Réclamation d’Hélène'}"
            f" · {'monographie de référence' if member['role'] == 'primary' else 'étude complémentaire'}"
            " de Helenēs apaitēsis")


def git_blob_sha(content):
    """Git's SHA-1 content object, verifiable without depending on git commands."""
    return sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()


def validate(root, pending=()):
    """Refuse any unregistered third manuscript of the same ancient tragedy.

    Existing allocated volumes remain protected and unchanged. Pending items
    are checked before a single new number, receipt or file is committed.
    """
    root = Path(root)
    data = load(root)
    groups = data["groups"]
    if not groups:
        return data
    sources = {p.relative_to(root).as_posix(): p.read_bytes()
               for p in (root / "chapitres/tragedies").glob("*.md")}
    for path, raw in pending:
        if path.parent == Path("chapitres/tragedies"):
            sources[path.as_posix()] = raw

    state = json.loads((root / "editorial/numbering.json").read_text(encoding="utf-8"))
    allocations = state["collections"]["tragedies"]["allocations"]
    identified = {key: set() for key in groups}
    for path, raw in sources.items():
        key = work_key(raw.decode("utf-8"), groups)
        if key:
            identified[key].add(path)

    recorded = set()
    for key, group in groups.items():
        members = group["members"]
        expected = {m["source"] for m in members}
        if (not members or len(expected) != len(members) or recorded & expected
                or sum(m["role"] == "primary" for m in members) != 1
                or any(m["role"] not in ("primary", "complement") for m in members)):
            raise ValueError("Membres de concordance invalides : " + key)
        recorded |= expected
        if identified[key] != expected:
            raise ValueError("Collision d'identité d'œuvre antique : " + key
                             + " ; intrus=" + str(sorted(identified[key] - expected))
                             + " ; manquants=" + str(sorted(expected - identified[key])))
        if not (root / group["notice_source"]).is_file():
            raise ValueError("Notice de concordance absente : " + key)
        if group["primary_url"] != url(next(m for m in members if m["role"] == "primary")):
            raise ValueError("Œuvre principale incohérente : " + key)
        uuids = set()
        for member in members:
            path = member["source"]
            if member["uuid"] in uuids:
                raise ValueError("UUID historique répété : " + key)
            uuids.add(member["uuid"])
            receipt = allocations.get(member["uuid"])
            if not receipt or receipt["path"] != path or receipt["number"] != member["number"]:
                raise ValueError("Reçu historique altéré : " + path)
            if git_blob_sha(sources[path]) != member["git_blob_sha"]:
                raise ValueError("Manuscrit universitaire protégé altéré : " + path)
            if member["roman"] != roman(member["number"]):
                raise ValueError("Numérotation romaine incohérente : " + path)
    return data


def roman(number):
    from editorial_queue import roman as render_roman
    return render_roman(number)


def fields(key, group, member):
    return {
        "title": display_title(group, member),
        "excerpt": (f"Sophocle, {group['transliteration']} ({group['greek_title']}) ; "
                    f"{group['reference']}. {member['focus']}. "
                    f"{'Étude de référence.' if member['role'] == 'primary' else 'Étude complémentaire du volume 233.'}"),
        "work_id": key,
        "work_role": member["role"],
        "work_primary_url": group["primary_url"],
        "work_guide_url": group["guide_url"],
        "work_aliases": group["aliases"],
        "work_source_reference": group["reference"],
        "ancient_work_count_contribution": int(member["role"] == "primary"),
    }


def annotate(root, collections, chapters):
    """Status flows to numbered tables, generic portals and reading metadata."""
    for key, group in load(root)["groups"].items():
        for member in group["members"]:
            metadata = fields(key, group, member)
            for entry in collections.get("tragedies", []) + chapters:
                if entry.get("url") == url(member):
                    entry.update(metadata)


def annotate_search(root, entries):
    """Reindexing is run several times; always restore canonical work fields."""
    groups = load(root)["groups"]
    for key, group in groups.items():
        for member in group["members"]:
            for entry in entries:
                if entry.get("url") == url(member):
                    entry.update(fields(key, group, member))


def _apply_json_index(root, path):
    if not path.is_file():
        raise ValueError("Index absent pour les identités tragiques : " + str(path))
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = (data["collections"]["tragedies"] if path.name == "numbering.json"
            else data["entries"] if path.name == "entries.json" else data)
    annotate_search(root, rows)
    # Preserve each generated index's serialization to avoid rewriting every
    # unrelated record in the deployed catalogue on each hourly build.
    if path.name == "numbering.json":
        serialized = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(serialized + "\n", encoding="utf-8")


def _note(key, group, members):
    links = "".join("<li><a href=\"" + escape(url(m), quote=True) + "\">"
                    + escape(m["label"] + f" — volume {m['roman']} ({m['number']})")
                    + "</a> — " + escape(m["focus"]) + "</li>" for m in members)
    return (
        f'<aside class="editorial-note" data-tragedy-work="{escape(key)}" '
        'aria-label="Concordance de cette tragédie perdue">'
        '<p><strong>Sophocle — ' + escape(group["transliteration"]) + ' (' +
        escape(group["greek_title"]) + ') : une œuvre antique, deux monographies.</strong></p>'
        '<p>Les titres « La Revendication d’Hélène » et « La Réclamation d’Hélène » '
        'traduisent une seule tragédie perdue. Référence : ' + escape(group["reference"]) +
        '. Le volume 233 constitue la référence éditoriale ; le volume 234 en est '
        'une étude critique complémentaire. Les deux travaux, leurs numéros et '
        'leurs références scientifiques restent conservés intégralement.</p>'
        '<ul>' + links + '</ul><p><a href="' + escape(group["guide_url"], quote=True) +
        '">Consulter la concordance philologique et les variantes de titre</a></p></aside>'
    )


def install(root, out):
    """Enrich only generated HTML/index files, preserving source bytes and routes."""
    from build_native import render, markdown
    root, out = Path(root), Path(out)
    data = validate(root)
    for key, group in data["groups"].items():
        members = group["members"]
        note = _note(key, group, members)
        for member in members:
            page = out / url(member).strip("/") / "index.html"
            doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            article = doc.select_one("article.content")
            if article is None or doc.head is None:
                raise ValueError("Lecteur universitaire absent : " + str(page))
            for old in doc.select("[data-tragedy-work]"):
                old.decompose()
            article.insert(0, BeautifulSoup(note, "html.parser"))
            doc.title.string = display_title(group, member) + " | MYTHOS"
            description = doc.head.find("meta", attrs={"name": "description"})
            if description:
                description["content"] = fields(key, group, member)["excerpt"]
            for name, value in (("mythos:work-id", key),
                                ("mythos:work-role", member["role"]),
                                ("mythos:work-primary", group["primary_url"])):
                for old in doc.head.find_all("meta", attrs={"name": name}):
                    old.decompose()
                doc.head.append(doc.new_tag("meta", attrs={"name": name, "content": value}))
            page.write_text(str(doc), encoding="utf-8")
        guide = out / group["guide_url"].strip("/") / "index.html"
        guide.parent.mkdir(parents=True, exist_ok=True)
        guide.write_text(render("Sophocle — " + group["transliteration"] +
                                " : concordance des volumes 233 et 234",
                                markdown((root / group["notice_source"]).read_text(encoding="utf-8"))),
                         encoding="utf-8")
        # Only append to existing portals; preserve the black-and-gold design.
        for portal in ("theatre", "collections-numerotees"):
            page = out / portal / "index.html"
            doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            article = doc.select_one("article.content")
            if article is None:
                raise ValueError("Sommaire de tragédies absent : " + portal)
            selector = 'tragedy-work-' + key.replace(":", "-")
            for old in doc.select("#" + selector):
                old.decompose()
            section = BeautifulSoup(
                '<section class="portal-section" id="' + escape(selector) +
                '"><h2>Une œuvre de Sophocle — deux monographies (233 et 234)</h2>'
                '<p><em>Helenēs apaitēsis</em> (Ἑλένης ἀπαίτησις), F 176–180a Radt : '
                'une seule tragédie perdue. Deux études intégrales conservées, '
                'dont une monographie principale et un complément critique.</p>'
                + note + '</section>', "html.parser")
            article.insert(1, section)
            page.write_text(str(doc), encoding="utf-8")
    # The reading catalogue is created later by improve_reading.enhance().
    # Mark indices already available; patch the complete catalogue in the
    # final pass, after it has been generated from the fully decorated pages.
    for suffix in ("catalog/numbering.json", "search.json"):
        _apply_json_index(root, out / suffix)
    if (out / "catalog/entries.json").is_file():
        _apply_json_index(root, out / "catalog/entries.json")
    report = {"version": 1, "registered_ancient_works": len(data["groups"]),
              "registered_monographs": sum(len(g["members"]) for g in data["groups"].values()),
              "groups": data["groups"]}
    target = out / REPORT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return report


def annotate_final_indices(root, out):
    """Apply work identity to the final catalogue after reading metadata exists."""
    root, out = Path(root), Path(out)
    for suffix in ("catalog/numbering.json", "catalog/entries.json", "search.json"):
        _apply_json_index(root, out / suffix)


def blocks(doc):
    return Counter(" ".join(e.get_text(" ", strip=True).split())
                   for e in doc.select("h1,h2,h3,h4,h5,h6,p,li,table,pre,blockquote")
                   if e.get_text(" ", strip=True))


def verify(root, out):
    """Fail on lost passages, wrong counts, broken cross-links or wrong metadata."""
    from build_native import markdown, frontmatter
    root, out = Path(root), Path(out)
    data = validate(root)
    report = json.loads((out / REPORT).read_text(encoding="utf-8"))
    assert report["groups"] == data["groups"], "Registre d'œuvres publié obsolète"
    assert report["registered_ancient_works"] == len(data["groups"])
    assert report["registered_monographs"] == sum(len(g["members"]) for g in data["groups"].values())
    search = {e["url"]: e for e in json.loads((out / "search.json").read_text(encoding="utf-8"))}
    catalogue = {e["url"]: e for e in json.loads((out / "catalog/entries.json").read_text(encoding="utf-8"))["entries"]}
    numbers = {e["url"]: e for e in json.loads((out / "catalog/numbering.json").read_text(encoding="utf-8"))["collections"]["tragedies"]}
    sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
    for key, group in data["groups"].items():
        pages = [url(m) for m in group["members"]]
        for member in group["members"]:
            address = url(member)
            for entries in (search, catalogue, numbers):
                assert entries[address]["work_id"] == key, address
                assert entries[address]["work_role"] == member["role"], address
                assert entries[address]["title"] == display_title(group, member), address
                assert entries[address]["work_primary_url"] == group["primary_url"], address
                assert entries[address]["work_guide_url"] == group["guide_url"], address
            assert numbers[address]["number"] == member["number"], address
            page = BeautifulSoup((out / address.strip("/") / "index.html").read_text(encoding="utf-8"), "html.parser")
            assert not page.select('meta[http-equiv="refresh"]'), "Une étude est devenue une redirection : " + address
            assert page.select_one('meta[name="mythos:work-id"]')['content'] == key, address
            note = page.select_one("aside[data-tragedy-work]")
            assert note, "Concordance absente : " + address
            for linked in pages + [group["guide_url"]]:
                assert note.find("a", href=linked), "Renvoi réciproque absent : " + linked
            _, body = frontmatter((root / member["source"]).read_text(encoding="utf-8"))
            original = BeautifulSoup(markdown(body), "html.parser")
            article = page.select_one("article.content")
            # The museum renderer and reader split inline emphasis into DOM
            # nodes, and numbering of HTML lists is not literal article text.
            # Verify every complete authored block as a normalized word sequence
            # rather than demanding identical BeautifulSoup block serialization.
            rendered_words = normalized(article.get_text(" ", strip=True))
            # The original H1 is the collection header, which the museum
            # layout may lift from article to the page masthead/title.
            source_h1 = original.select_one("h1")
            if source_h1:
                page_words = normalized(page.get_text(" ", strip=True) + " " +
                                        str(page.title.string if page.title else ""))
                assert normalized(source_h1.get_text(" ", strip=True)) in page_words, address
            authored_words = [
                normalized(node.get_text(" ", strip=True))
                for node in original.select("h2,h3,h4,h5,h6,p,li,table,pre,blockquote")
            ]
            missing = [words[:120] for words in authored_words
                       if words and words not in rendered_words]
            assert not missing, "Contenu de la monographie amputé : " + address + " ; " + repr(missing[:3])
        for address in pages + [group["guide_url"]]:
            assert address in search, "Étude ou concordance absente de la recherche : " + address
            assert "https://bobmythos.fr" + address in sitemap, "Sitemap incomplet : " + address
            assert (out / address.strip("/") / "index.html").is_file(), address
        guide = BeautifulSoup((out / group["guide_url"].strip("/") / "index.html").read_text(encoding="utf-8"), "html.parser")
        for address in pages:
            assert guide.find("a", href=address), "Concordance sans étude : " + address
        for portal in ("theatre", "collections-numerotees"):
            doc = BeautifulSoup((out / portal / "index.html").read_text(encoding="utf-8"), "html.parser")
            section = doc.find(id="tragedy-work-" + key.replace(":", "-"))
            assert section and all(section.find("a", href=address) for address in pages), portal
    return {"works": len(data["groups"]),
            "monographs": sum(len(g["members"]) for g in data["groups"].values())}
