"""Issues #29 and #108: two ancient works, five protected monographs."""
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
SOPHOCLE = "sophocle:helenes-apaitesis"
IRIS = "acheos:iris-satyrique"


class TragedyIdentityTests(unittest.TestCase):
    def setUp(self):
        self.data = load(ROOT)
        self.groups = self.data["groups"]

    def test_registry_preserves_two_works_five_volumes_receipts_and_bytes(self):
        self.assertEqual(validate(ROOT), self.data)
        self.assertEqual(set(self.groups), {SOPHOCLE, IRIS})
        self.assertEqual(
            [(m["number"], m["role"]) for m in self.groups[SOPHOCLE]["members"]],
            [(233, "primary"), (234, "complement")])
        self.assertEqual(
            [(m["number"], m["role"]) for m in self.groups[IRIS]["members"]],
            [(270, "primary"), (271, "complement"), (272, "complement")])
        state = json.loads((ROOT / "editorial/numbering.json").read_text(
            encoding="utf-8"))["collections"]["tragedies"]["allocations"]
        seen_uuids, seen_paths = set(), set()
        for group in self.groups.values():
            for member in group["members"]:
                self.assertNotIn(member["uuid"], seen_uuids)
                self.assertNotIn(member["source"], seen_paths)
                seen_uuids.add(member["uuid"])
                seen_paths.add(member["source"])
                self.assertEqual(state[member["uuid"]]["number"], member["number"])
                self.assertEqual(state[member["uuid"]]["path"], member["source"])
                self.assertEqual(git_blob_sha((ROOT / member["source"]).read_bytes()),
                                 member["git_blob_sha"])

    def test_variants_match_author_and_ancient_work(self):
        samples = {
            SOPHOCLE: (
                "Sophocle — La Revendication d’Hélène",
                "Sophocle — La Réclamation d'Hélène",
                "SOPHOCLE — LA RECLAMATION D HELENE",
                "Sophocle — Helenes Apaitesis",
                "Sophocle — Ἑλένης ἀπαίτησις",
                "Sophocle — Demande de restitution d'Hélène",
            ),
            IRIS: (
                "Achéos d’Érétrie — Iris satyrique",
                "ACHEOS D ERÉTRIE — IRIS SATYRIQUE",
                "Achéos d’Érétrie — Ἴρις Σατυρική",
                "Achéos d’Érétrie — Ἶρις Σατυρική",
                "Achéos d’Érétrie — Iris Satyrikē",
                "Achéos d’Érétrie — Iris Saturoi",
            ),
        }
        for key, titles in samples.items():
            for title in titles:
                with self.subTest(key=key, title=title):
                    self.assertEqual(work_key("## " + title, self.groups), key)

    def test_other_tragedies_and_other_authors_remain_distinct(self):
        for title in (
            "Sophocle — L'Enlèvement d'Hélène",
            "Sophocle — Le Mariage d'Hélène",
            "Euripide — La Réclamation d'Hélène",
            "Sophocle — Hermione et les Phthiotides",
            "Achéos d’Érétrie — Héphaïstos satyrique",
            "Achéos d’Érétrie — Katápeira",
            "Achéos d’Érétrie — Kyknos",
            "Sophocle — Iris satyrique",
        ):
            with self.subTest(title=title):
                self.assertIsNone(work_key("## " + title, self.groups))

    def test_new_unregistered_monograph_refused_for_both_authors(self):
        for title in ("Sophocle — La Réclamation d'Hélène",
                      "Achéos d’Érétrie — Iris satyrique"):
            pending = Path("chapitres/tragedies/volume-ccccl-new-duplicate.md")
            payload = ("# Volume CCCCL\n\n## " + title
                       + "\n\nNouveau texte non enregistré.").encode("utf-8")
            with self.subTest(title=title):
                with self.assertRaisesRegex(ValueError, "Collision d'identit"):
                    validate(ROOT, [(pending, payload)])

    def test_other_achean_title_does_not_block_pending_work(self):
        pending = Path("chapitres/tragedies/volume-ccccl-acheos-katapeira.md")
        payload = "# Volume CCCCL\n\n## Achéos d’Érétrie — Katápeira\n\nAutre œuvre.".encode("utf-8")
        self.assertEqual(validate(ROOT, [(pending, payload)]), self.data)

    def test_index_contributes_one_work_per_primary_not_per_monograph(self):
        entries = [{"url": url(m), "title": "ancien titre"}
                   for group in self.groups.values() for m in group["members"]]
        collection = {"tragedies": [dict(e) for e in entries]}
        chapters = [dict(e) for e in entries]
        annotate(ROOT, collection, chapters)
        annotate_search(ROOT, entries)
        for rows in (collection["tragedies"], chapters, entries):
            self.assertEqual(len(rows), 5)
            self.assertEqual(len({e["url"] for e in rows}), 5)
            self.assertEqual(len({e["work_id"] for e in rows}), 2)
            self.assertEqual(sum(e["ancient_work_count_contribution"] for e in rows), 2)
            self.assertEqual([e["work_role"] for e in rows],
                             ["primary", "complement", "primary", "complement", "complement"])
            for entry in rows:
                self.assertEqual(entry["work_primary_url"],
                                 self.groups[entry["work_id"]]["primary_url"])


class RenderedConcordanceTests(unittest.TestCase):
    def test_html_notes_crosslinks_indices_source_passages_and_idempotency(self):
        data = load(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            rows = []
            numbering = []
            for group in data["groups"].values():
                for member in group["members"]:
                    page = out / url(member).strip("/") / "index.html"
                    page.parent.mkdir(parents=True, exist_ok=True)
                    page.write_text(render("Monographie intégrale",
                                           markdown((ROOT / member["source"]).read_text(
                                               encoding="utf-8"))),
                                    encoding="utf-8")
                    rows.append({"url": url(member), "title": "Monographie", "excerpt": "Source"})
                    numbering.append(dict(rows[-1], number=member["number"]))
            for portal in ("theatre", "collections-numerotees"):
                page = out / portal / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(render("Sommaire",
                                       "<h1>Catalogue</h1><section id='numerotation-tragedies'></section>"),
                                encoding="utf-8")
            (out / "catalog").mkdir()
            (out / "catalog/numbering.json").write_text(
                json.dumps({"collections": {"tragedies": numbering}}),
                encoding="utf-8")
            (out / "catalog/entries.json").write_text(
                json.dumps({"entries": rows}), encoding="utf-8")
            extra = [{"url": group["guide_url"], "title": "Concordance", "excerpt": "Guide"}
                     for group in data["groups"].values()]
            (out / "search.json").write_text(json.dumps(rows + extra), encoding="utf-8")
            (out / "sitemap.xml").write_text(
                "\n".join("https://bobmythos.fr" + addr
                          for addr in [e["url"] for e in rows + extra]),
                encoding="utf-8")
            result = install(ROOT, out)
            self.assertEqual(result["registered_ancient_works"], 2)
            self.assertEqual(result["registered_monographs"], 5)
            self.assertEqual(verify(ROOT, out), {"works": 2, "monographs": 5})
            for key, group in data["groups"].items():
                for member in group["members"]:
                    page = out / url(member).strip("/") / "index.html"
                    doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                    note = doc.select_one("aside[data-tragedy-work]")
                    self.assertEqual(note["data-tragedy-work"], key)
                    self.assertEqual(len(note.select("li")), len(group["members"]))
                    self.assertEqual(doc.select_one('meta[name="mythos:work-primary"]')[
                        "content"], group["primary_url"])
                    self.assertNotIn("Sophocle", doc.title.string) if key == IRIS else None
                    self.assertFalse(doc.select('meta[http-equiv="refresh"]'))
                guide = BeautifulSoup(
                    (out / group["guide_url"].strip("/") / "index.html").read_text(
                        encoding="utf-8"), "html.parser")
                self.assertTrue(all(guide.find("a", href=url(m)) for m in group["members"]))
            # The historical pending status remains in the protected source,
            # while the reader's administrative erratum gives the current receipt.
            iris = data["groups"][IRIS]
            third = iris["members"][2]
            self.assertIn("demande en attente d’attribution",
                          (ROOT / third["source"]).read_text(encoding="utf-8"))
            doc = BeautifulSoup(
                (out / url(third).strip("/") / "index.html").read_text(encoding="utf-8"),
                "html.parser")
            self.assertIn("Erratum administratif", doc.select_one(
                "aside[data-tragedy-work]").get_text())
            install(ROOT, out)
            self.assertEqual(verify(ROOT, out), {"works": 2, "monographs": 5})
            for group in data["groups"].values():
                for member in group["members"]:
                    doc = BeautifulSoup(
                        (out / url(member).strip("/") / "index.html").read_text(
                            encoding="utf-8"), "html.parser")
                    self.assertEqual(len(doc.select("aside[data-tragedy-work]")), 1)


if __name__ == "__main__":
    unittest.main()
