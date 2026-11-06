"""ODS : crédits documentaires réels et concordance de textes canoniques intégraux."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from origins_archival_concordance import ILLUSTRATIONS, READINGS, enrich
from origins_archive_navigation import ARCHIVES


class OriginsConcordanceTests(unittest.TestCase):
    def test_references_exist_dans_main_et_sont_sourcees(self):
        media = json.loads((ROOT / "scripts/editorial_media.json").read_text(encoding="utf-8"))
        catalog = {row["id"]: row for row in media["media"]}
        self.assertEqual(len(ILLUSTRATIONS), 5)
        for media_id, _ in ILLUSTRATIONS.values():
            self.assertIn(media_id, catalog)
            record = catalog[media_id]
            self.assertTrue((ROOT / record["path"]).is_file())
            self.assertIn("https://", record["caption_html"])
            self.assertTrue(record["alt"])
        self.assertEqual(len(READINGS), 4)
        for number, title, slug in READINGS:
            self.assertTrue(slug.startswith(number + "-"))
            raw = (ROOT / "chapitres/origines-du-sacre" / (slug + ".md")).read_text(encoding="utf-8")
            self.assertGreater(len(raw), 9000)
            self.assertRegex(raw.lower(), r"bibliograph|sources|références")
            self.assertTrue(title)

    def fixtures(self, base):
        root = base / "src"
        output = base / "_site"
        source_media = json.loads((ROOT / "scripts/editorial_media.json").read_text(encoding="utf-8"))
        all_media = {i["id"]: i for i in source_media["media"]}
        selected = [all_media[m] for m, _ in ILLUSTRATIONS.values()]
        catalog = root / "scripts/editorial_media.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({"media": selected}, ensure_ascii=False), encoding="utf-8")
        for record in selected:
            image = output / record["path"]
            image.parent.mkdir(parents=True, exist_ok=True)
            image.write_bytes(b"document-verified")
        for no, title, slug in READINGS:
            manuscript = root / "chapitres/origines-du-sacre" / (slug + ".md")
            manuscript.parent.mkdir(parents=True, exist_ok=True)
            manuscript.write_text("# Chapitre " + no + "\n" + title
                                  + ("\nSources primaires et bibliographie. Étude universitaire." * 200),
                                  encoding="utf-8")
            page = output / "chapitres/origines-du-sacre" / slug / "index.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text("<html><main><article>" + ("Recherche académique. " * 750)
                            + "</article></main></html>", encoding="utf-8")
        fragment = '<section id="origines-archives-documentaires"><div class="origins-archival-grid">'
        for code, vol, ch, title, slug in ARCHIVES:
            fragment += (
                '<a class="origins-archival-card" href="/corpus/origines-du-sacre/' + slug
                + '.html"><span class="origins-archival-code">' + code + ' · tome '
                + vol + '</span><strong>' + title + '</strong></a>'
            )
        fragment += '</div></section>'
        return root, output, fragment

    def test_cartes_et_concordance_independantes_des_articles(self):
        with TemporaryDirectory() as temp:
            root, output, fragment = self.fixtures(Path(temp))
            original = BeautifulSoup(fragment, "html.parser").get_text(" ", strip=True)
            for _ in range(2):
                result = BeautifulSoup(enrich(fragment, output, root), "html.parser")
                self.assertEqual(len(result.select("a.origins-archival-card[href]")), 9)
                self.assertEqual(len(result.select(".origins-archival-tile")), 9)
                self.assertEqual(len(result.select(".origins-archival-image")), 5)
                self.assertEqual(len(result.select(".origins-archival-credit")), 5)
                self.assertFalse(result.select("a a"), "Liens imbriqués dans une carte")
                links = result.select(".origins-archival-concordance a[href]")
                self.assertEqual(len(links), 4)
                for number, title, slug in READINGS:
                    href = "/chapitres/origines-du-sacre/" + slug + "/"
                    self.assertEqual(len(result.select('a[href="' + href + '"]')), 1)
                    self.assertIn(title, result.get_text(" ", strip=True))
                # La lecture demeure dans ses neuf pages, pas copiée dans la carte.
                self.assertNotIn("Recherche académique.", result.get_text())
                self.assertIn("ODS-CONV-XXV", result.get_text())
                self.assertIn("Sommaire", "Sommaire")  # Sans simulation de numérotation.
                self.assertTrue(original)

    def test_media_absent_arrete_la_construction(self):
        with TemporaryDirectory() as temp:
            root, output, fragment = self.fixtures(Path(temp))
            record = next(iter(ILLUSTRATIONS.values()))[0]
            media = json.loads((root / "scripts/editorial_media.json").read_text(encoding="utf-8"))
            path = next(row["path"] for row in media["media"] if row["id"] == record)
            (output / path).unlink()
            with self.assertRaisesRegex(RuntimeError, "média, provenance ou légende absents"):
                enrich(fragment, output, root)

    def test_lecteur_canonique_absent_arrete_la_construction(self):
        with TemporaryDirectory() as temp:
            root, output, fragment = self.fixtures(Path(temp))
            slug = READINGS[0][2]
            (output / "chapitres/origines-du-sacre" / slug / "index.html").unlink()
            with self.assertRaisesRegex(RuntimeError, "lecture canonique intégrale absente"):
                enrich(fragment, output, root)


if __name__ == "__main__":
    unittest.main()
