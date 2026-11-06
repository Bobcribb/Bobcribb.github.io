"""Concordances : deux corpus conservés, cinq cultes laconiens, aucune perte."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from editorial_concordances import PAIRS, LACONIA, install, validate_sources


class EditorialConcordancesTests(unittest.TestCase):
    def test_receipts_sources_bibliographies_and_six_identifiers(self):
        registry = json.loads((ROOT / "editorial/numbering.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(set(PAIRS), {"chalkioikos", "menekrates", "iacchos"})
        self.assertEqual(
            {m[2] for m in PAIRS["chalkioikos"]["members"]}, {449, 454})
        self.assertEqual(
            {m[2] for m in PAIRS["menekrates"]["members"]}, {122, 123})
        self.assertEqual({m[2] for m in PAIRS["iacchos"]["members"]}, {269, 273})
        for group in PAIRS.values():
            for collection, uid, number, title, context in group["members"]:
                with self.subTest(uid=uid):
                    receipt = registry["collections"][collection]["allocations"][uid]
                    self.assertEqual(receipt["number"], number)
                    request = (ROOT / "editorial/inbox" / (uid + ".json")).read_bytes()
                    self.assertEqual(sha256(request).hexdigest(),
                                     receipt["request_sha256"])
                    source = (ROOT / receipt["path"]).read_text(encoding="utf-8")
                    self.assertGreater(len(source), 30000)
                    self.assertIn("bibliograph", source.casefold())

    def test_repeated_insertion_is_reciprocal_and_preserves_article(self):
        registry = json.loads((ROOT / "editorial/numbering.json")
                              .read_text(encoding="utf-8"))
        urls = {u for u, _, _ in LACONIA}
        for group in PAIRS.values():
            for collection, uid, _, _, _ in group["members"]:
                rel = registry["collections"][collection]["allocations"][uid]["path"]
                urls.add("/" + Path(rel).with_suffix("").as_posix() + "/")
        self.assertEqual(len(urls), 10)
        with TemporaryDirectory() as folder:
            out = Path(folder)
            snapshots = {}
            for url in urls:
                path = out / url.strip("/") / "index.html"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<html lang="fr"><head><title>Étude</title></head><body>'
                    '<main><article class="content"><h1>Monographie intégrale</h1>'
                    '<p>Texte original.</p><h2>Sources</h2><p>Éditions.</p>'
                    '<h2>Bibliographie</h2><p>Références critiques.</p>'
                    '</article></main></body></html>', encoding="utf-8")
                snapshots[url] = str(BeautifulSoup(
                    path.read_text(encoding="utf-8"), "html.parser").article)
            for rel in ("theatre/index.html",
                        "mythologie-comparee/index.html",
                        "mythologie-grecque/dossiers/cultes-sanctuaires/index.html"):
                path = out / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('<html><body><main><article class="content">'
                                '<h1>Sommaire</h1></article></main></body></html>',
                                encoding="utf-8")
            for _ in range(2):
                stats = install(ROOT, out)
                self.assertEqual(stats, {"readers": 10, "panels": 11, "portals": 3})
                validate_sources(ROOT, out)
                for url in urls:
                    path = out / url.strip("/") / "index.html"
                    doc = BeautifulSoup(path.read_text(encoding="utf-8"),
                                        "html.parser")
                    self.assertEqual(str(doc.article), snapshots[url])
                    panels = doc.select("aside[data-mythos-concordance]")
                    self.assertEqual(len(panels), 2 if
                                     url == LACONIA[2][0] else 1)
                    for link in doc.select("aside[data-mythos-concordance] a[href]"):
                        target = out / urlsplit(link["href"]).path.strip("/") / "index.html"
                        self.assertTrue(target.is_file(), target)
            greek = BeautifulSoup(
                (out / "mythologie-grecque/dossiers/cultes-sanctuaires/index.html")
                .read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(len(greek.select("section[data-mythos-concordance]")), 2)
            theatre = BeautifulSoup((out / "theatre/index.html").read_text(),
                                    "html.parser")
            self.assertEqual(len(theatre.select("section[data-mythos-concordance]")), 1)
            comparison = BeautifulSoup(
                (out / "mythologie-comparee/index.html").read_text(encoding="utf-8"),
                "html.parser")
            notice = comparison.select_one(
                'section#concordance-iacchos[data-mythos-concordance="iacchos"]')
            self.assertIsNotNone(notice)
            self.assertEqual(len(notice.select("tbody tr")), 8)
            self.assertEqual(
                {a["href"] for a in notice.select("ul a[href]")},
                {"/" + Path(registry["collections"]["comparatif"]["allocations"][uid]["path"])
                           .with_suffix("").as_posix() + "/"
                 for uid in ("8d9ce5f4-d076-4f00-9dbf-209d8476b3bf",
                             "d73f9a62-1e48-45f8-9d0a-5bcd730e9a24")})


    def test_accessible_css(self):
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertIn("body.mythos-design .mythos-concordance", css)
        self.assertIn("@media(max-width:700px)", css)
        self.assertIn("grid-template-columns:1fr", css)
        self.assertIn(".mythos-concordance-table", css)


if __name__ == "__main__":
    unittest.main()
