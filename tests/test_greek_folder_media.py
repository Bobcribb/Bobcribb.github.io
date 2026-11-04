"""Provenance et préservation des huit cartes thématiques MYTHOS."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_folders import FOLDER_ARTWORK, folder_artworks, overview


class GreekFolderMediaTests(unittest.TestCase):
    def test_all_eight_families_use_distinct_verified_artworks(self):
        self.assertEqual(len(FOLDER_ARTWORK), 8)
        self.assertIn("cosmogonies", FOLDER_ARTWORK)
        self.assertEqual(FOLDER_ARTWORK["cosmogonies"][1], "Derveni")
        self.assertEqual(FOLDER_ARTWORK["sources-anciennes"][1], "Iliade")
        self.assertEqual(len(FOLDER_ARTWORK), len({item[0] for item in FOLDER_ARTWORK.values()}))
        self.assertFalse(any(".svg" in item[0] or "2.5" in item[0] for item in FOLDER_ARTWORK.values()))
        artwork = folder_artworks(ROOT, ROOT, set(FOLDER_ARTWORK))
        self.assertEqual(len(artwork), 8)
        self.assertIn("Derveni", artwork["cosmogonies"]["caption_html"])
        self.assertIn("commons.wikimedia.org", artwork["cosmogonies"]["caption_html"])
        self.assertIn("P.Oxy.", artwork["sources-anciennes"]["caption_html"])

    def test_picture_credits_and_longform_links_survive_repeated_renders(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            out = Path(temporary) / "site"
            art_id, subject = FOLDER_ARTWORK["heros"]
            path = "media/2026/10/" + art_id + ".jpg"
            image = out / path
            image.parent.mkdir(parents=True)
            image.write_bytes(b"source JPG not modified")
            reg = root / "scripts/editorial_media.json"
            reg.parent.mkdir(parents=True)
            reg.write_text(json.dumps({"media": [{
                "id": art_id, "subjects": [subject], "path": path,
                "alt": "Thésée et le Minotaure sur une amphore.",
                "caption_html": '<strong>Objet antique.</strong> <a href="https://www.metmuseum.org/">Source</a>'
            }]}), encoding="utf-8")
            rows = [
                {"url": "/chapitres/encyclopedie/chapitre-359-chiron/",
                 "title": "Chiron — étude intégrale", "kind": "Chapitre universitaire",
                 "folder": "heros", "section": "Héros", "book": None},
                {"url": "/chapitres/encyclopedie/chapitre-375-nyx/",
                 "title": "Nyx — cosmogonie", "kind": "Chapitre universitaire",
                 "folder": "cosmogonies", "section": "Nuit", "book": None},
            ]
            artwork = folder_artworks(root, out, {"heros"})
            for _ in range(2):
                doc = BeautifulSoup(overview(rows, artwork), "html.parser")
                self.assertEqual(len(doc.select(".greek-folder-link")), 2)
                self.assertEqual(len(doc.select(".greek-folder-illustration")), 1)
                self.assertIn("Thésée et le Minotaure", doc.select_one("img")["alt"])
                self.assertEqual(doc.select_one(".greek-folder-credit a")["href"],
                                 "https://www.metmuseum.org/")
                self.assertEqual(doc.select_one('a[href="/mythologie-grecque/dossiers/heros/"]').get_text(" ", strip=True).count("Héros et héroïnes"), 1)
                self.assertEqual(len(doc.select(".greek-folder-credit")), 1)
                self.assertEqual(image.read_bytes(), b"source JPG not modified")

    def test_missing_source_blocks_publishing_instead_of_substitution(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            reg = root / "scripts/editorial_media.json"
            reg.parent.mkdir(parents=True)
            art_id, subject = FOLDER_ARTWORK["heros"]
            reg.write_text(json.dumps({"media": [{
                "id": art_id, "subjects": [subject], "path": "media/2026/10/absent.jpg",
                "alt": "Thésée", "caption_html": '<a href="https://example.org">Source</a>'
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "image/source absente"):
                folder_artworks(root, Path(temporary) / "site", {"heros"})


if __name__ == "__main__":
    unittest.main()
