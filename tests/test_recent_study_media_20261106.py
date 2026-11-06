"""Accueil MYTHOS : pertinence documentaire des images des dernières études.

Tests sans retoucher les manuscrits ni faire d'attribution canonique.
"""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from recent_study_media import documented_image
from recent_studies import install, latest_verified


class RelevantRecentMediaTests(unittest.TestCase):
    @staticmethod
    def known_catalog():
        rows = json.loads((ROOT / "scripts/editorial_media.json").read_text(encoding="utf-8"))["media"]
        return {row["id"]: row for row in rows}

    def test_existing_source_images_only_for_a_relevant_topic(self):
        studies = (
            ("encyclopedie", "Athéna Chalkioikos et Poliouchos à Sparte",
             "chapitre-454-athena-chalkioikos", "mythos-athena-lecythe-brygos-aplaste-met-25-189-1"),
            ("tragedies", "Alcméon satyrique : purification delphique et Delphes",
             "volume-cclxiii-alcmeon-delphes", "delphes-temple-apollon-bernard-gagnon"),
            ("comparatif", "Les Oiseaux d’Aristophane : Prométhée et souveraineté",
             "volume-ccxci-oiseaux-aristophane", "mythos-met-844483-acteurs-comiques-grecs"),
            ("comedies", "Ménècrate, Hermioneus et le jeu des osselets",
             "volume-123-menekrates", "mythos-met-844483-acteurs-comiques-grecs"),
        )
        catalog = self.known_catalog()
        for collection, title, slug, expected in studies:
            with self.subTest(collection=collection):
                result = documented_image(ROOT, ROOT, collection, title, slug)
                self.assertEqual(result["media_id"], expected)
                self.assertEqual(result["image"], "/" + catalog[expected]["path"])
                self.assertEqual(result["alt"], catalog[expected]["alt"])
                self.assertIn("https://", result["credit_html"])
                self.assertTrue(result["illustration"])

    def test_absent_image_better_than_misleading_generic_picture(self):
        tests = (
            ("origines-du-sacre", "Tadrart Acacus : art rupestre du Sahara",
             "721-tadrart-acacus"),
            ("encyclopedie", "Athéna n'est pas ici : héros et généalogies",
             "chapitre-455-heros-genealogies"),  # Texte sur Athéna : iconographie comparative permise
            ("comparatif", "Les ombres du divin : Égypte, Grèce et Inde",
             "volume-mc-096-ombres-divin"),
        )
        # Les deux dossiers sans sujet iconographique sûr ne prennent aucune image.
        for collection, title, slug in (tests[0], tests[2]):
            self.assertEqual(documented_image(ROOT, ROOT, collection, title, slug), {})
        # Le sélecteur, en revanche, ne doit pas avoir de rapport avec les chiffres.
        self.assertNotIn("tadrart", str(documented_image(ROOT, ROOT, tests[0][0], tests[0][1], tests[0][2])))

    def test_media_file_missing_causes_graceful_abstention(self):
        with TemporaryDirectory() as folder:
            root, out = Path(folder) / "repo", Path(folder) / "public"
            row = self.known_catalog()["delphes-temple-apollon-bernard-gagnon"]
            p = root / "scripts/editorial_media.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"media": [row]}), encoding="utf-8")
            self.assertEqual(documented_image(root, out, "tragedies", "Delphes",
                                              "volume-delphes"), {})

    def test_full_readers_navigation_and_credits_without_text_copy(self):
        with TemporaryDirectory() as folder:
            root, out = Path(folder) / "repo", Path(folder) / "public"
            media = self.known_catalog()["delphes-temple-apollon-bernard-gagnon"]
            manifest = root / "scripts/editorial_media.json"
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text(json.dumps({"media": [media]}, ensure_ascii=False), encoding="utf-8")
            picture = out / media["path"]
            picture.parent.mkdir(parents=True, exist_ok=True)
            picture.write_bytes(b"photo-source-attestee")
            records = (
                ("origines-du-sacre", 721, "721-tadrart-acacus",
                 "# Chapitre 721 — Tadrart Acacus : art rupestre saharien"),
                ("tragedies", 263, "volume-cclxiii-delphes",
                 "# MYTHOS — Tragédies grecques, Volume CCLXIII\n## Delphes : Achéos d’Érétrie"),
            )
            allocations = {}
            originals = {}
            for collection, number, slug, heading in records:
                path = Path("chapitres") / collection / (slug + ".md")
                source = root / path
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(heading + "\n\n" + ("Analyse universitaire et références. " * 110),
                                  encoding="utf-8")
                originals[str(path)] = source.read_bytes()
                reader = out / path.with_suffix("") / "index.html"
                reader.parent.mkdir(parents=True, exist_ok=True)
                reader.write_text('<html><body><main><article class="content"><p>'
                                  'Texte intégral et bibliographie.</p></article></main></body></html>',
                                  encoding="utf-8")
                allocations[collection] = {"allocations": {
                    "uuid-" + collection: {"path": path.as_posix(), "number": number}}}
            registry = root / "editorial/numbering.json"
            registry.parent.mkdir(parents=True, exist_ok=True)
            registry.write_text(json.dumps({"version": 1, "collections": allocations}), encoding="utf-8")
            (out / "index.html").write_text(
                '<html><body class="mythos-design"><nav class="mythos-home-toc"><ul>'
                '<li><a href="#home-oeuvres">Œuvres</a></li></ul></nav>'
                '<main><article class="content"><section id="home-parcours"></section>'
                '<p id="permanent">Texte de navigation préservé.</p></article></main></body></html>',
                encoding="utf-8"
            )
            self.assertEqual(len(latest_verified(root, out)), 2)
            for _ in range(2):
                self.assertEqual(install(root, out), 2)
                page = BeautifulSoup((out / "index.html").read_text(encoding="utf-8"),
                                     "html.parser")
                self.assertEqual(len(page.select("#home-etudes-recentes a.portal-card")), 2)
                self.assertIsNone(page.select_one("#etude-recente-origines-du-sacre img"))
                self.assertIn("mythos-recent-unillustrated",
                              page.select_one("#etude-recente-origines-du-sacre")["class"])
                image = page.select_one("#etude-recente-tragedies img")
                self.assertEqual(image["src"], "/" + media["path"])
                self.assertEqual(image["alt"], media["alt"])
                self.assertEqual(len(page.select(".mythos-recent-credits li")), 1)
                self.assertIn("Source", page.select_one(".mythos-recent-credits").get_text())
                self.assertEqual(len(page.select('a[href="#home-etudes-recentes"]')), 1)
                self.assertIn("navigation préservé", page.get_text(" ", strip=True))
                for collection, number, slug, title in records:
                    path = Path("chapitres") / collection / (slug + ".md")
                    self.assertEqual((root / path).read_bytes(), originals[str(path)])
                    reader = BeautifulSoup((out / path.with_suffix("") / "index.html")
                                           .read_text(encoding="utf-8"), "html.parser")
                    self.assertEqual(len(reader.select("nav[data-mythos-recent-backlinks]")), 1)
                    self.assertIn("Texte intégral et bibliographie", reader.get_text())


if __name__ == "__main__":
    unittest.main()
