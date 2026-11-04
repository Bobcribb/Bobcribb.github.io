#!/usr/bin/env python3
"""Fail before committing/deploying if the numbered corpus loses content or links."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import os

from bs4 import BeautifulSoup
from build_native import markdown, frontmatter
from editorial_queue import validate
from origines_reconciliation import BASE, CANONICAL, COMPLEMENTS


def normalized(value):
    return re.sub(r"\s+", " ", value).strip()


def verify(root=Path("."), out=Path("_site")):
    registry = validate(root)
    from editorial_numbering import redirects
    historical_redirects = redirects(root)
    report = json.loads((out / "catalog/origines-continuity.json").read_text())
    catalogue = json.loads((out / "search.json").read_text())
    indexed = {item["url"]: item for item in catalogue}
    assert len(indexed) == len(catalogue) and len(indexed) >= 500, "Catalogue incomplet ou en doublon"
    sitemap = (out / "sitemap.xml").read_text()
    portal = BeautifulSoup((out / "origines-du-sacre/index.html").read_text(), "html.parser")
    items = portal.select("#chapitres-recents li[data-chapter]")
    numbers = [int(item["data-chapter"]) for item in items]
    assert len(numbers) == len(set(numbers)), "Doublon dans le sommaire"
    expected = {int(n): url for n, url in report["canonical"].items() if int(n) >= 491}
    actual = {int(item["data-chapter"]): item.find("a")["href"] for item in items}
    assert actual == expected, "Sommaire différent du registre canonique"
    assert expected[583] == CANONICAL[583], "Identité du chapitre 583 altérée"
    for url, spec in COMPLEMENTS.items():
        if not spec.get("inline"):
            continue
        assert portal.find("a", href=url), "Complément absent du sommaire : " + url
        assert indexed[url]["title"] == spec["title"], "Complément mal identifié dans la recherche"
        page = BeautifulSoup((out / url.strip("/") / "index.html").read_text(), "html.parser")
        assert not page.select('meta[http-equiv="refresh"]'), "Redirection d'une étude distincte"
        assert page.find("a", href=spec["canonical"]), "Renvoi canonique manquant"
        canonical = BeautifulSoup((out / spec["canonical"].strip("/") / "index.html").read_text(), "html.parser")
        assert canonical.find("a", href=url), "Renvoi réciproque manquant"
    # Check all scholarly blocks, not just byte counts. Only the displayed H1
    # of historical complements is relabelled; their prose remains complete.
    for path, source_hash in report["preserved_source_sha256"].items():
        source = root / path
        assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, path
        url = "/" + Path(path).with_suffix("").as_posix() + "/"
        if url in historical_redirects:
            # Source bytes remain archived; the complete destination is checked
            # separately. Historical redirect pages are intentionally unindexed.
            target = historical_redirects[url]
            assert url not in indexed and target in indexed, url
            redirect = BeautifulSoup((out / url.strip("/") / "index.html").read_text(), "html.parser")
            assert redirect.select_one('meta[http-equiv="refresh"]'), url
            assert redirect.find("a", href=target), url
            continue
        assert url in indexed and "https://bobmythos.fr" + url in sitemap, url
        _, body = frontmatter(source.read_text(encoding="utf-8"))
        original = BeautifulSoup(markdown(body), "html.parser")
        page = BeautifulSoup((out / url.strip("/") / "index.html").read_text(), "html.parser")
        article = page.select_one("article.content")
        assert article, url
        rendered = normalized(article.get_text(" ", strip=True))
        for block in original.select("p, li, h2, h3, h4, h5, h6, table, pre"):
            assert normalized(block.get_text(" ", strip=True)) in rendered, "Texte perdu : " + path
    for collection, state in registry["collections"].items():
        for allocation in state["allocations"].values():
            path = allocation["path"]
            url = "/" + str(Path(path).with_suffix("")) + "/"
            assert url in indexed and "https://bobmythos.fr" + url in sitemap, url
            assert (out / url.strip("/") / "index.html").is_file(), url
    romans = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv","xxv","xxvi","xxvii"]
    special = {"i":"tome-i-hohle-fels", "ii":"tome-ii-prehistoire-du-sacre", "iii":"tome-iii-corps-caverne-mondes-invisibles"}
    for roman in romans:
        slug = special.get(roman, "tome-" + roman)
        path = Path("chapitres/origines-du-sacre/archives-integrales") / slug
        assert (root / path.with_suffix(".md")).stat().st_size > 10000, slug
        assert (out / path / "index.html").stat().st_size > 10000, slug
        assert portal.find("a", href="/" + path.as_posix() + "/"), slug
    media = json.loads((out / "media/manifest.json").read_text())
    assert media["count"] == len(media["files"]) == 110
    for item in media["files"]:
        body = (out / item["path"]).read_bytes()
        assert len(body) == item["size"] and hashlib.sha256(body).hexdigest() == item["sha256"], item["path"]
    assert (out / "CNAME").read_text().strip() == "bobmythos.fr"
    assert "/media/2026/10/" in (out / "akhetaton-horizon-aton-etude/index.html").read_text()
    evidence = {
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "indexed_documents": len(indexed), "verified_archives": 27, "verified_media": 110,
        "preserved_source_sha256": report["preserved_source_sha256"],
        "last_numbered_chapter": report["last_numbered_chapter"],
        "numbering_registry_sha256": hashlib.sha256((root / "editorial/numbering.json").read_bytes()).hexdigest(),
    }
    (out / "catalog/publication-verification.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print("Publication vérifiée :", len(indexed), "documents ; 27 tomes ; 110 médias ;", len(report["preserved_source_sha256"]), "manuscrits réconciliés intégraux")


if __name__ == "__main__":
    verify()
