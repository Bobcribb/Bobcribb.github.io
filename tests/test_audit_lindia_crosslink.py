"""Audit MYTHOS : garde de concordance 433 ↔ 438 d'Athéna Lindia.

Vérifie les chemins du manuscrit et du lecteur HTML ; n'attribue aucun numéro.
"""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_native as build

PART433 = "chapitre-433-athena-lindia-rhodes-chronique-lindos-anathemes-epiphanies-danaides"
PART438 = "chapitre-438-athena-lindia-chronique-lindos-danaides-offrandes-epiphanies-memoire"
CHAPTERS = ROOT / "chapitres"
SOURCE433 = CHAPTERS / "encyclopedie" / (PART433 + ".md")
SOURCE438 = CHAPTERS / "encyclopedie" / (PART438 + ".md")
HTML433 = CHAPTERS / "encyclopedie" / PART433 / "index.html"
HTML438 = CHAPTERS / "encyclopedie" / PART438 / "index.html"
URL433 = "/chapitres/encyclopedie/" + PART433 + "/"
URL438 = "/chapitres/encyclopedie/" + PART438 + "/"

class AthenaLindiaCrosslinkAudit(unittest.TestCase):
    def test_sources_exist_and_numbers_remain_distinct(self):
        self.assertTrue(SOURCE433.is_file())
        self.assertTrue(SOURCE438.is_file())
        self.assertTrue(HTML433.is_file())
        self.assertTrue(HTML438.is_file())
        self.assertIn("# Chapitre 433", SOURCE433.read_text(encoding="utf-8"))
        self.assertIn("chapitre 438", SOURCE438.read_text(encoding="utf-8").lower())

    def test_markdown_relative_link_resolves_to_published_html(self):
        raw = SOURCE438.read_text(encoding="utf-8")
        self.assertIn("](" + PART433 + ".md)", raw)
        self.assertNotIn("](../" + PART433 + ".md)", raw)
        rendered = build.resolve_chapter_links(build.markdown(raw), SOURCE438, CHAPTERS)
        doc = BeautifulSoup(rendered, "html.parser")
        links = [anchor.get("href") for anchor in doc.find_all("a", href=True)
                 if PART433 in anchor["href"]]
        self.assertEqual(links, [URL433])
        self.assertTrue((ROOT / URL433.lstrip("/") / "index.html").is_file())

    def test_versioned_public_pages_have_bidirectional_valid_links(self):
        page438 = BeautifulSoup(HTML438.read_text(encoding="utf-8"), "html.parser")
        page433 = BeautifulSoup(HTML433.read_text(encoding="utf-8"), "html.parser")
        links438 = [a["href"] for a in page438.select("a[href]")
                    if PART433 in a["href"]]
        links433 = [a["href"] for a in page433.select("a[href]")
                    if PART438 in a["href"]]
        self.assertEqual(links438, [URL433])
        self.assertIn(URL438, links433)
        self.assertTrue((ROOT / URL438.lstrip("/") / "index.html").is_file())

if __name__ == "__main__":
    unittest.main()
