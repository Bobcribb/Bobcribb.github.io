"""Contrôle de restauration du Kalevala intégral et de son lecteur muséal.

Le manuscrit WordPress original reste dans la sauvegarde privée. Le test garde
sa longueur d'origine et compare le texte rendu, sans connexion Google Drive.
"""
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = "bibliotheque-mythologies-du-monde/mythos-volume-10-finno-carelien-kalevala/index.html"
PAGE = ROOT / ARTICLE
PORTAL_BUILDER = ROOT / "scripts" / "build_navigation.py"
CSS = ROOT / "assets" / "mythos-museum.css"
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply as apply_museum_design


class TestKalevalaArchiveIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = PAGE.read_text(encoding="utf-8")
        start = '<div class="mythos-original-study" id="texte-integral-kalevala">\n'
        end = '\n</div>\n<section class="mythos-world-study-crosslinks"'
        cls.assert_source_layout = start in cls.page and end in cls.page
        if cls.assert_source_layout:
            cls.marked = cls.page.split(start, 1)[1].split(end, 1)[0]
            cls.unmarked = re.sub(
                r'<span id="lecture-[0-9]+" class="mythos-text-anchor" aria-hidden="true"></span>',
                "", cls.marked,
            )

    def test_entire_source_preserved(self):
        self.assertTrue(self.assert_source_layout)
        self.assertEqual(len(self.unmarked), 48625)
        self.assertEqual(self.unmarked.count("<h2 "), 20)
        self.assertEqual(len(re.findall(r"<h[23][ >]", self.unmarked)), 62)
        self.assertIn("Sources et documentation", self.unmarked)
        self.assertIn("Library of Congress", self.unmarked)
        self.assertIn("finlit.fi", self.unmarked)
        self.assertIn("Lönnrot", self.unmarked)
        self.assertIn("Le Sampo résiste à une classification facile", self.unmarked)

    def test_table_of_contents_resolves_to_real_anchors(self):
        doc = BeautifulSoup(self.page, "html.parser")
        toc = doc.select_one("details.mythos-world-study-toc")
        self.assertIsNotNone(toc)
        links = toc.select('a[href^="#lecture-"]')
        self.assertEqual(len(links), 20)
        for link in links:
            self.assertIsNotNone(doc.find(id=link["href"][1:]))
        anchors = doc.select("span.mythos-text-anchor")
        self.assertEqual(len(anchors), 62)
        self.assertEqual(len({anchor["id"] for anchor in anchors}), 62)
        self.assertEqual(doc.select_one('article[data-source-archive="wordpress-1134"]')["data-original-html-length"], "48625")

    def test_no_parallel_canonical_numbering(self):
        self.assertFalse(ARTICLE.startswith("chapitres/"))
        self.assertIn('href="/mythologies/"', self.page)
        self.assertIn('href="/civilisations/europe/"', self.page)
        builder = PORTAL_BUILDER.read_text(encoding="utf-8")
        # Plusieurs cartes (accueil, Europe, mythologies) peuvent pointer vers\n        # un seul manuscrit ; c'est le fichier source qui doit rester unique.\n        self.assertGreaterEqual(builder.count('"/' + ARTICLE.removesuffix("index.html") + '"'), 1)\n        self.assertTrue(PAGE.is_file())
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("lecteur Kalevala", css)
        self.assertIn("@media(max-width:720px)", css)

    def test_museum_render_does_not_remove_manuscript(self):
        original = BeautifulSoup(self.unmarked, "html.parser").get_text(" ", strip=True)
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / ARTICLE
            destination.parent.mkdir(parents=True)
            shutil.copyfile(PAGE, destination)
            self.assertEqual(apply_museum_design(tmp), 1)
            doc = BeautifulSoup(destination.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(doc.body.get("data-mythos-design"), "20261104")
            self.assertIsNotNone(doc.select_one(".mythos-masthead"))
            self.assertIsNotNone(doc.select_one(".mythos-banner"))
            self.assertIsNotNone(doc.select_one('link[href*="mythos-museum.css"]'))
            restored = doc.select_one(".mythos-original-study").get_text(" ", strip=True)
            self.assertEqual(restored, original)
            self.assertEqual(len(doc.select("span.mythos-text-anchor")), 62)


if __name__ == "__main__":
    unittest.main()
