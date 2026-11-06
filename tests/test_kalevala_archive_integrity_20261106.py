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


def scholarly_fingerprint(html_fragment):
    # Insensible à l'ordre des attributs HTML et aux espaces de sérialisation.
    # Digest FNV-1a 64 bits de la prose + la ponctuation, dérivé des éditions
    # archivées avant le rendu GitHub Actions du 6 novembre 2026.
    html_fragment = re.sub(r'<span\b(?=[^>]*mythos-text-anchor)[^>]*></span>', '', html_fragment)
    html_fragment = re.sub(r'<!--[\s\S]*?-->', '', html_fragment)
    text = re.sub(r'<[^>]*>', ' ', html_fragment).replace('&nbsp;', ' ').replace('&#160;', ' ')
    text = ' '.join(text.split())
    digest = 0xcbf29ce484222325
    for character in text:
        digest = ((digest ^ ord(character)) * 0x100000001b3) & 0xffffffffffffffff
    return text, format(digest, '016x')


class TestKalevalaArchiveIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = PAGE.read_text(encoding="utf-8")
        start = '<div class="mythos-original-study" id="texte-integral-kalevala">\n'
        end = '\n</div>\n<section'
        if start not in cls.page or end not in cls.page:
            raise AssertionError('Borniers documentaires de Kalevala manquants')
        cls.marked = cls.page.split(start, 1)[1].split(end, 1)[0]
        cls.unmarked = re.sub(
            r'<span\b(?=[^>]*mythos-text-anchor)[^>]*></span>', '', cls.marked)
        cls.scholarly_text, cls.scholarly_hash = scholarly_fingerprint(cls.marked)

    def test_entire_source_preserved(self):
        # Longueur historique conservée en provenance ; signature du texte
        # inchangée avant/après la normalisation HTML de la publication.
        self.assertIn('data-original-html-length="48625"', self.page)
        self.assertEqual(len(self.scholarly_text), 36741)
        self.assertEqual(self.scholarly_hash, '7b688d10da810873')
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
        # Plusieurs cartes (accueil, Europe, mythologies) peuvent pointer vers
        # un seul manuscrit ; c'est le fichier source qui doit rester unique.
        self.assertGreaterEqual(builder.count('"/' + ARTICLE.removesuffix("index.html") + '"'), 1)
        self.assertTrue(PAGE.is_file())
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
