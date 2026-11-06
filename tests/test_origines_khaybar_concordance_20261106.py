"""Régression ODS 698/699 : aucune fusion, perte, retenue ou URL dédoublée."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from origines_khaybar_concordance import (DOI, KEY, PORTAL, STUDIES,
                                          install, url_of, validate_sources)


class KhaybarConcordanceTests(unittest.TestCase):
    def test_two_receipts_and_full_sources_are_preserved(self):
        registry = json.loads((ROOT / "editorial/numbering.json").read_text(encoding="utf-8"))
        holds = json.loads((ROOT / "editorial/holds.json").read_text(encoding="utf-8"))
        allocations = registry["collections"]["origines-du-sacre"]["allocations"]
        self.assertEqual({x["number"] for x in STUDIES}, {698, 699})
        self.assertEqual(len({url_of(x) for x in STUDIES}), 2)
        for study in STUDIES:
            with self.subTest(chapter=study["number"]):
                uid = study["uuid"]
                receipt = allocations[uid]
                self.assertEqual(receipt["number"], study["number"])
                self.assertEqual(receipt["path"], study["path"])
                self.assertNotIn(uid, holds.get("requests", {}))
                original = (ROOT / study["path"]).read_bytes()
                request = (ROOT / "editorial/inbox" / (uid + ".json")).read_bytes()
                self.assertEqual(sha256(original).hexdigest(),
                                 receipt["initial_source_sha256"])
                self.assertEqual(sha256(request).hexdigest(),
                                 receipt["request_sha256"])
                self.assertIn(b"10.1177/09596836211060497", original)
                self.assertIn("bibliograph", original.decode("utf-8").casefold())

    def test_rendered_notice_is_reciprocal_and_source_independent(self):
        with TemporaryDirectory() as directory:
            out = Path(directory)
            original = {}
            for study in STUDIES:
                url = url_of(study)
                target = out / url.strip("/") / "index.html"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    '<!doctype html><html lang="fr"><head><title>Chapitre</title>'
                    '</head><body><main><article class="content">'
                    '<h1>Monographie universitaire intégrale</h1>'
                    '<p>Texte original, datations, enquête et interprétations.</p>'
                    '<h2>Bibliographie</h2><p>Références.</p>'
                    '</article></main></body></html>', encoding="utf-8")
                original[url] = str(BeautifulSoup(
                    target.read_text(encoding="utf-8"), "html.parser"
                ).select_one("article.content"))
            portal = out / PORTAL
            portal.parent.mkdir(parents=True, exist_ok=True)
            portal.write_text(
                '<html lang="fr"><body><main><article class="content">'
                '<h1>Origines du sacré</h1><ul id="chapitres-recents">'
                '<li data-chapter="698"><a href="' + url_of(STUDIES[0]) +
                '">Chapitre 698</a></li><li data-chapter="699"><a href="' +
                url_of(STUDIES[1]) +
                '">Chapitre 699</a></li></ul></article></main></body></html>',
                encoding="utf-8")
            sources_before = {x["path"]: sha256((ROOT / x["path"]).read_bytes()).hexdigest()
                              for x in STUDIES}
            for _ in range(2):
                self.assertEqual(install(ROOT, out),
                                 {"readers": 2, "portal": 1, "canonical_numbers": [698, 699]})
                validate_sources(ROOT, out)
                for study in STUDIES:
                    url = url_of(study)
                    reader = BeautifulSoup(
                        (out / url.strip("/") / "index.html").read_text(encoding="utf-8"),
                        "html.parser")
                    self.assertEqual(str(reader.select_one("article.content")),
                                     original[url])
                    notices = reader.select('aside[data-mythos-concordance="' + KEY + '"]')
                    self.assertEqual(len(notices), 1)
                    external = [x for x in STUDIES if x["number"] != study["number"]][0]
                    self.assertEqual([a["href"] for a in notices[0].select("ul a[href]")],
                                     [url_of(external)])
                    self.assertIn(DOI, [a["href"] for a in notices[0].select("a[href]")])
                    self.assertIn("Dalton", notices[0].get_text(" ", strip=True))
                    self.assertIn("hypothèses", notices[0].get_text(" ", strip=True))
                index = BeautifulSoup(portal.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(len(index.select('section[data-mythos-concordance="' +
                                                  KEY + '"]')), 1)
                linkset = {a["href"] for a in index.select('section[data-mythos-concordance="' +
                                                           KEY + '"] li a[href]')}
                self.assertEqual(linkset, {url_of(s) for s in STUDIES})
                self.assertEqual([int(li["data-chapter"]) for li in
                                  index.select("#chapitres-recents li[data-chapter]")],
                                 [698, 699])
                self.assertEqual(sources_before,
                                 {x["path"]: sha256((ROOT / x["path"]).read_bytes()).hexdigest()
                                  for x in STUDIES})


if __name__ == "__main__":
    unittest.main()
