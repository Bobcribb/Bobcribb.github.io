"""One ancient work per concordance: Sophocles 233–234, Achaeus 270–272."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from bs4 import BeautifulSoup
from build_native import markdown, render
from tragedy_work_identity import (annotate, annotate_search, git_blob_sha,
                                   install, load, url, validate, verify, work_key)

ROOT = Path(__file__).resolve().parents[1]
SOPHOCLES = "sophocle:helenes-apaitesis"
ACHAEUS = "acheos-eretrie:iris-satyrique"


class TragedyIdentityTests(unittest.TestCase):
    def setUp(self):
        self.data = load(ROOT)
        self.sophocles = self.data["groups"][SOPHOCLES]
        self.achaeus = self.data["groups"][ACHAEUS]
        self.members = [m for group in self.data["groups"].values() for m in group["members"]]

    def test_registry_preserves_five_issued_volumes_and_bytes(self):
        validate(ROOT)
        self.assertEqual(set(self.data["groups"]), {SOPHOCLES, ACHAEUS})
        self.assertEqual([(m["number"], m["role"]) for m in self.sophocles["members"]],
                         [(233, "primary"), (234, "complement")])
        self.assertEqual([(m["number"], m["role"]) for m in self.achaeus["members"]],
                         [(270, "primary"), (271, "complement"), (272, "complement")])
        state = json.loads((ROOT / "editorial/numbering.json").read_text())["collections"]["tragedies"]["allocations"]
        self.assertEqual(len({m["uuid"] for m in self.members}), 5)
        self.assertEqual(len({url(m) for m in self.members}), 5)
        for member in self.members:
            with self.subTest(number=member["number"]):
                receipt = state[member["uuid"]]
                self.assertEqual(receipt["number"], member["number"])
                self.assertEqual(receipt["path"], member["source"])
                self.assertEqual(git_blob_sha((ROOT / member["source"]).read_bytes()),
                                 member["git_blob_sha"])

    def test_greek_transliteration_french_and_diacritics(self):
        cases = {
            SOPHOCLES: ("Sophocle — La Revendication d’Hélène",
                        "Sophocle — La Réclamation d'Hélène",
                        "SOPHOCLE — LA RECLAMATION D HELENE",
                        "Sophocle — Helenes Apaitesis",
                        "Sophocle — Ἑλένης ἀπαίτησις",
                        "Sophocle — Demande de restitution d'Hélène"),
            ACHAEUS: ("Achéos d’Érétrie — Iris satyrique",
                      "ACHÉOS D'ERETRIE — IRIS SATYRIQUE",
                      "Achéos d’Érétrie — Ἴρις Σατυρική",
                      "Achéos d’Érétrie — Ἶρις Σατυρική",
                      "Achéos d’Érétrie — Iris et les satyres"),
        }
        for key, titles in cases.items():
            for title in titles:
                with self.subTest(title=title):
                    self.assertEqual(work_key("## " + title, self.data["groups"]), key)

    def test_unrelated_authors_and_works_are_not_conflated(self):
        for title in ("Sophocle — L'Enlèvement d'Hélène",
                      "Sophocle — Le Mariage d'Hélène",
                      "Euripide — La Réclamation d'Hélène",
                      "Sophocle — Hermione et les Phthiotides",
                      "Achéos d’Érétrie — Héphaïstos satyrique",
                      "Achéos d’Érétrie — Thésée",
                      "Eschyle — Iris satyrique"):
            with self.subTest(title=title):
                self.assertIsNone(work_key("## " + title, self.data["groups"]))

    def test_third_sophocles_and_fourth_achaeus_blocked_before_allocation(self):
        cases = [("Sophocle - La Reclamation d'Helene",
                  "chapitres/tragedies/volume-cccl-sophocle-other.md"),
                 ("Achéos d'Érétrie - Iris satyrique",
                  "chapitres/tragedies/volume-cccl-acheos-iris-other.md")]
        for title, path in cases:
            with self.subTest(title=title):
                with self.assertRaisesRegex(ValueError, "Collision d'identit"):
                    validate(ROOT, [(Path(path), ("# Volume CCCL\n\n## " + title).encode())])

    def test_distinct_future_tragedies_do_not_block_allocation(self):
        for title in ("Sophocle - L'Enlevement d'Helene",
                      "Achéos d'Érétrie - Katápeira",
                      "Achéos d'Érétrie - Kyknos"):
            with self.subTest(title=title):
                path = Path("chapitres/tragedies/volume-cccl-new-study.md")
                self.assertEqual(validate(ROOT, [(path, ("# Volume CCCL\n\n## " + title).encode())]),
                                 self.data)

    def test_annotation_counts_two_works_five_monographs(self):
        entries = [{"url": url(m), "title": "historique"} for m in self.members]
        numbered = {"tragedies": [dict(e) for e in entries]}
        chapters = [dict(e) for e in entries]
        annotate(ROOT, numbered, chapters)
        annotate_search(ROOT, entries)
        for rows in (numbered["tragedies"], chapters, entries):
            self.assertEqual([e["work_role"] for e in rows],
                             ["primary", "complement", "primary", "complement", "complement"])
            self.assertEqual(sum(e["ancient_work_count_contribution"] for e in rows), 2)
            self.assertEqual(len({e["work_id"] for e in rows}), 2)
            self.assertEqual(len({e["url"] for e in rows}), 5)
            self.assertIn("Achéos", rows[3]["title"])
            self.assertNotIn("Sophocle", rows[3]["title"])
            self.assertIn("volume 270", rows[4]["excerpt"])

    def test_historical_administrative_status_is_corrected_in_metadata(self):
        self.assertIn("désormais", self.achaeus["administrative_notice"])
        self.assertEqual(self.achaeus["primary_url"], url(self.achaeus["members"][0]))


class RenderedConcordanceTests(unittest.TestCase):
    def test_generated_html_reciprocal_links_indices_source_integrity_and_idempotence(self):
        groups = load(ROOT)["groups"]
        members = [m for group in groups.values() for m in group["members"]]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            rows = []
            for member in members:
                page = out / url(member).strip("/") / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(render("Monographie intégrale",
                                       markdown((ROOT / member["source"]).read_text(encoding="utf-8"))),
                                encoding="utf-8")
                rows.append({"url": url(member), "title": "Monographie",
                             "excerpt": "Source", "number": member["number"]})
            for portal in ("theatre", "collections-numerotees"):
                page = out / portal / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(render("Sommaire",
                                       "<h1>Catalogue</h1><section id='numerotation-tragedies'></section>"),
                                encoding="utf-8")
            (out / "catalog").mkdir()
            (out / "catalog/numbering.json").write_text(
                json.dumps({"collections": {"tragedies": rows}}), encoding="utf-8")
            (out / "catalog/entries.json").write_text(
                json.dumps({"entries": rows}), encoding="utf-8")
            guide_rows = [{"url": group["guide_url"], "title": "Concordance",
                           "excerpt": "Guide"} for group in groups.values()]
            (out / "search.json").write_text(json.dumps(rows + guide_rows), encoding="utf-8")
            addresses = [url(m) for m in members] + [g["guide_url"] for g in groups.values()]
            (out / "sitemap.xml").write_text(
                "\n".join("https://bobmythos.fr" + address for address in addresses),
                encoding="utf-8")
            for attempt in range(2):
                install(ROOT, out)
                self.assertEqual(verify(ROOT, out), {"works": 2, "monographs": 5})
            for member in members:
                page = BeautifulSoup(
                    (out / url(member).strip("/") / "index.html").read_text(encoding="utf-8"),
                    "html.parser")
                self.assertEqual(len(page.select("aside[data-tragedy-work]")), 1)
                self.assertTrue(page.select_one('meta[name="mythos:work-id"]'))
                self.assertFalse(page.select('meta[http-equiv="refresh"]'))
                self.assertEqual(len(page.select('link[rel="canonical"]')), 0)
            for key, group in groups.items():
                self.assertTrue((out / group["guide_url"].strip("/") / "index.html").is_file())
                for portal in ("theatre", "collections-numerotees"):
                    page = BeautifulSoup((out / portal / "index.html").read_text(encoding="utf-8"),
                                         "html.parser")
                    section = page.find(id="tragedy-work-" + key.replace(":", "-"))
                    self.assertIsNotNone(section)
                    self.assertTrue(all(section.find("a", href=url(m))
                                        for m in group["members"]))
                if key == ACHAEUS:
                    page = BeautifulSoup((out / url(group["members"][2]).strip("/") /
                                          "index.html").read_text(encoding="utf-8"), "html.parser")
                    self.assertIn("Rectification administrative", page.get_text(" ", strip=True))
            report = json.loads((out / "catalog/tragedy-works.json").read_text())
            self.assertEqual(report["registered_ancient_works"], 2)
            self.assertEqual(report["registered_monographs"], 5)


if __name__ == "__main__":
    unittest.main()
