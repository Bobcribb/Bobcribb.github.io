"""Issue #29: one Sophoclean tragedy, two protected and searchable monographs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from bs4 import BeautifulSoup
from build_native import markdown, render
from tragedy_work_identity import (annotate, annotate_search, git_blob_sha, install,
                                   load, url, validate, verify, work_key)

ROOT = Path(__file__).resolve().parents[1]


class TragedyIdentityTests(unittest.TestCase):
    def setUp(self):
        self.data = load(ROOT)
        self.key = "sophocle:helenes-apaitesis"
        self.group = self.data["groups"][self.key]

    def test_registry_preserves_two_issued_volumes_and_bytes(self):
        validate(ROOT)
        members = self.group["members"]
        self.assertEqual([(m["number"], m["role"]) for m in members],
                         [(233, "primary"), (234, "complement")])
        state = json.loads((ROOT / "editorial/numbering.json").read_text())["collections"]["tragedies"]["allocations"]
        for member in members:
            self.assertEqual(state[member["uuid"]]["number"], member["number"])
            self.assertEqual(state[member["uuid"]]["path"], member["source"])
            self.assertEqual(git_blob_sha((ROOT / member["source"]).read_bytes()),
                             member["git_blob_sha"])

    def test_french_greek_transliteration_and_diacritic_variants(self):
        for title in (
            "Sophocle — La Revendication d’Hélène",
            "Sophocle — La Réclamation d'Hélène",
            "SOPHOCLE — LA RECLAMATION D HELENE",
            "Sophocle — Helenes Apaitesis",
            "Sophocle — Ἑλένης ἀπαίτησις",
            "Sophocle — Demande de restitution d'Hélène",
        ):
            with self.subTest(title=title):
                self.assertEqual(work_key("## " + title, self.data["groups"]), self.key)

    def test_different_tragedies_or_authors_remain_distinct(self):
        for title in (
            "Sophocle — L'Enlèvement d'Hélène",
            "Sophocle — Le Mariage d'Hélène",
            "Euripide — La Réclamation d'Hélène",
            "Sophocle — Hermione et les Phthiotides",
        ):
            with self.subTest(title=title):
                self.assertIsNone(work_key("## " + title, self.data["groups"]))

    def test_collision_from_a_new_uuid_or_slug_refused_before_allocation(self):
        pending_path = Path("chapitres/tragedies/volume-cccl-sophocle-autre-slug.md")
        payload = b"# Volume CCCL\n\n## Sophocle - La Reclamation d'Helene\n\nUne etude distincte."
        with self.assertRaisesRegex(ValueError, "Collision d'identit"):
            validate(ROOT, [(pending_path, payload)])
        for member in self.group["members"]:
            self.assertTrue((ROOT / member["source"]).is_file())

    def test_distinct_sophoclean_title_does_not_block_pending_work(self):
        pending_path = Path("chapitres/tragedies/volume-cccl-sophocle-enlevement-helene.md")
        payload = b"# Volume CCCL\n\n## Sophocle - L'Enlevement d'Helene\n\nUne autre oeuvre."
        self.assertEqual(validate(ROOT, [(pending_path, payload)]), self.data)

    def test_annotation_never_invents_a_second_ancient_work(self):
        entries = [{"url": url(member), "title": "ancienne entrée"} for member in self.group["members"]]
        numbered = {"tragedies": [dict(e) for e in entries]}
        chapters = [dict(e) for e in entries]
        annotate(ROOT, numbered, chapters)
        annotate_search(ROOT, entries)
        for rows in (numbered["tragedies"], chapters, entries):
            self.assertEqual([e["work_role"] for e in rows], ["primary", "complement"])
            self.assertEqual(sum(e["ancient_work_count_contribution"] for e in rows), 1)
            self.assertEqual(len({e["work_id"] for e in rows}), 1)
            self.assertEqual(len({e["url"] for e in rows}), 2)


class RenderedConcordanceTests(unittest.TestCase):
    def test_html_notes_indexes_and_fragments_preserved(self):
        data = load(ROOT)
        group = data["groups"]["sophocle:helenes-apaitesis"]
        members = group["members"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            rows = []
            for member in members:
                page = out / url(member).strip("/") / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(render("Monographie intégrale",
                                       markdown((ROOT / member["source"]).read_text(encoding="utf-8"))),
                                encoding="utf-8")
                rows.append({"url": url(member), "title": "Monographie", "excerpt": "Source"})
            for portal in ("theatre", "collections-numerotees"):
                page = out / portal / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(render("Sommaire", "<h1>Catalogue</h1><section id='numerotation-tragedies'></section>"),
                                encoding="utf-8")
            (out / "catalog").mkdir()
            (out / "catalog/numbering.json").write_text(json.dumps({
                "collections": {"tragedies": [dict(e, number=m["number"]) for e, m in zip(rows, members)]}
            }), encoding="utf-8")
            (out / "catalog/entries.json").write_text(json.dumps({"entries": rows}), encoding="utf-8")
            (out / "search.json").write_text(json.dumps(rows + [
                {"url": group["guide_url"], "title": "Concordance", "excerpt": "Guide"}
            ]), encoding="utf-8")
            (out / "sitemap.xml").write_text("\n".join(
                "https://bobmythos.fr" + address for address in
                [url(m) for m in members] + [group["guide_url"]]), encoding="utf-8")
            install(ROOT, out)
            results = verify(ROOT, out)
            self.assertEqual(results, {"works": 1, "monographs": 2})
            first = (out / url(members[0]).strip("/") / "index.html")
            html_before = first.read_text(encoding="utf-8")
            # Running again never duplicates editorial notes or loses original passages.
            install(ROOT, out)
            verify(ROOT, out)
            doc = BeautifulSoup(first.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(len(doc.select("aside[data-tragedy-work]")), 1)
            self.assertTrue(doc.select_one('meta[name="mythos:work-id"]'))
            self.assertEqual(len(doc.select('link[rel="canonical"]')), 0)  # fixture has no preexisting canonical
            self.assertGreater(len(html_before), (ROOT / members[0]["source"]).stat().st_size)
            report = json.loads((out / "catalog/tragedy-works.json").read_text())
            self.assertEqual(report["registered_ancient_works"], 1)
            self.assertEqual(report["registered_monographs"], 2)


if __name__ == "__main__":
    unittest.main()
