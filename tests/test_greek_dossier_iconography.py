"""Cartes des dossiers grecs : provenance, adaptation et conservation des textes."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_corpus import dossier_navigation, DOSSIER_ARTIFACTS


class GreekDossierIconographyTests(unittest.TestCase):
    def test_curated_map_is_unique_and_contains_no_legacy_svg(self):
        ids = [value[0] for value in DOSSIER_ARTIFACTS.values()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all("2.5d" not in name.lower() and ".svg" not in name.lower()
                            for name in ids))
        self.assertNotIn("astres", DOSSIER_ARTIFACTS)
        self.assertNotIn("pelion-heros", DOSSIER_ARTIFACTS)

    def test_captions_and_anchor_survive_while_unillustrated_groups_stay_plain(self):
        with TemporaryDirectory() as temporary:
            tmp = Path(temporary)
            root = tmp / "sources"
            out = tmp / "site"
            mid, subject = DOSSIER_ARTIFACTS["thesee"]
            photo = "media/2026/10/" + mid + ".jpg"
            image = out / photo
            image.parent.mkdir(parents=True)
            image.write_bytes(b"existing JPG")
            manifest = root / "scripts/editorial_media.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"media": [
                {"id": mid, "path": photo, "subjects": [subject],
                 "alt": "Amphore grecque représentant Thésée.",
                 "caption_html": "<strong>Amphore attique.</strong> "
                                 '<a href="https://www.metmuseum.org/">'
                                 "Metropolitan Museum of Art</a>"}
            ]}), encoding="utf-8")
            groups = [
                ("astres", "Hélios et Astéria", "", [("/chap-259/", "Hélios")]),
                ("thesee", "Thésée et Ariane", "", [("/chap-315/", "Thésée"),
                                                   ("/chap-316/", "Ariane")]),
            ]
            for _ in range(2):
                fragment = dossier_navigation(groups, root, out)
                doc = BeautifulSoup(fragment, "html.parser")
                jumps = doc.select(".greek-dossier-jump")
                self.assertEqual([x["href"] for x in jumps],
                                 ["#grec-dossier-astres", "#grec-dossier-thesee"])
                self.assertFalse(jumps[0].find("img"))
                self.assertEqual(jumps[1].img["src"], "/" + photo)
                self.assertEqual(jumps[1].img["alt"],
                                 "Amphore grecque représentant Thésée.")
                self.assertEqual(len(doc.select(".greek-dossier-credit")), 1)
                self.assertEqual(doc.select_one(".greek-dossier-credit a")["href"],
                                 "https://www.metmuseum.org/")
                self.assertEqual(jumps[1].select_one("small").get_text(strip=True),
                                 "2 chapitres")

    def test_registered_source_with_missing_picture_blocks_build(self):
        with TemporaryDirectory() as temporary:
            tmp = Path(temporary)
            root = tmp / "source"
            manifest = root / "scripts/editorial_media.json"
            manifest.parent.mkdir(parents=True)
            image_id, subject = DOSSIER_ARTIFACTS["thesee"]
            manifest.write_text(json.dumps({"media": [
                {"id": image_id, "subjects": [subject],
                 "path": "media/2026/10/missing.jpg", "alt": "Amphore",
                 "caption_html": "Crédit et source"}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Image ou source absente"):
                dossier_navigation([("thesee", "Thésée", "", [("/", "titre")])],
                                   root, tmp / "out")

if __name__ == "__main__":
    unittest.main()
