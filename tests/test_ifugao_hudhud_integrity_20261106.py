"""Restauration du volume historique XV sur les chants Hudhud des Ifugao."""
from pathlib import Path
import re
import sys
import shutil
import tempfile
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REL = "bibliotheque-mythologies-du-monde/mythos-volume-15-philippines-ifugao-hudhud/index.html"
PAGE = ROOT / REL
NAV = ROOT / "scripts/build_navigation.py"
CSS = ROOT / "assets/mythos-museum.css"
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply as apply_museum_design


class HudhudHistoricalVolumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = PAGE.read_text(encoding="utf-8")
        start = '<div class="mythos-original-study" id="texte-integral-hudhud-ifugao">\n'
        # La charte muséale ajoute des attributs de navigation au <nav> sans
        # modifier la limite du manuscrit historique.
        end = re.search(r'\n</div>\n<nav\b[^>]*class="mythos-world-study-crosslinks"[^>]*>', cls.full)
        if start not in cls.full or not end:
            raise AssertionError("Bornes du manuscrit universitaire absentes")
        cls.marked = cls.full.split(start, 1)[1].split(end.group(0), 1)[0]
        # Les 62 ancres décoratives ont un ordre d'attributs variable selon
        # les moteurs de rendu. Restituer le texte original à cote constante.
        cls.original = re.sub(
            r'<span\b[^>]*\bid="ifugao-lecture-[0-9]+"[^>]*></span>',
            "", cls.marked,
        )

    def test_scientific_text_not_abridged(self):
        self.assertEqual(len(self.original), 46646)
        self.assertEqual(len(re.findall(r"<h2[ >]", self.original)), 20)
        self.assertEqual(len(re.findall(r"<h[23][ >]", self.original)), 62)
        for token in ("Aliguyon", "Pumbakhayon", "Sources institutionnelles et méthodologie", "ich.unesco.org"):
            self.assertIn(token, self.original)
        self.assertIn("data-original-html-length=\"46646\"", self.full)

    def test_exact_reader_anchors_and_toc(self):
        doc = BeautifulSoup(self.full, "html.parser")
        links = doc.select('details.mythos-world-study-toc a[href^="#ifugao-lecture-"]')
        self.assertEqual(len(links), 20)
        for item in links:
            self.assertIsNotNone(doc.find(id=item["href"][1:]))
        self.assertEqual(len(doc.select("span.mythos-text-anchor")), 62)
        all_ids = [el["id"] for el in doc.find_all(id=True)]
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_historical_number_not_canonical_numbering(self):
        self.assertIn('data-source-archive="wordpress-1139"', self.full)
        self.assertTrue(REL.startswith("bibliotheque-mythologies-du-monde/"))
        self.assertNotIn("editorial/inbox/", REL)
        nav = NAV.read_text(encoding="utf-8")
        self.assertIn('"/bibliotheque-mythologies-du-monde/mythos-volume-15-philippines-ifugao-hudhud/"', nav)
        self.assertIn('if key == "asie"', nav)
        self.assertIn('ifugao-rizieres-2022', nav)
        self.assertIn('href="/civilisations/asie/"', self.full)
        self.assertIn('href="/mythologies/"', self.full)

    def test_photo_context_and_rights(self):
        doc = BeautifulSoup(self.full, "html.parser")
        figure = doc.select_one("figure.mythos-ifugao-figure")
        self.assertIsNotNone(figure)
        self.assertIn("Ifugao", figure.get_text(" ", strip=True))
        self.assertIn("Pogidawako1234", figure.get_text(" ", strip=True))
        self.assertIn("creativecommons.org/licenses/by-sa/4.0/", self.full)
        self.assertIn("non représentation directe", figure.img["alt"])
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("mythos-ifugao-figure", css)
        self.assertIn("@media(max-width:720px)", css)

    def test_museum_theme_preserves_original_prose(self):
        expected = BeautifulSoup(self.original, "html.parser").get_text(" ", strip=True)
        with tempfile.TemporaryDirectory() as directory:
            dst = Path(directory) / REL
            dst.parent.mkdir(parents=True)
            shutil.copyfile(PAGE, dst)
            self.assertEqual(apply_museum_design(directory), 1)
            doc = BeautifulSoup(dst.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(doc.body.get("data-mythos-design"), "20261104")
            self.assertIsNotNone(doc.select_one(".mythos-banner"))
            self.assertIsNotNone(doc.select_one(".mythos-masthead"))
            self.assertIsNotNone(doc.select_one('link[href*="mythos-museum.css"]'))
            self.assertEqual(doc.select_one(".mythos-original-study").get_text(" ", strip=True), expected)
            self.assertEqual(len(doc.select("span.mythos-text-anchor")), 62)


if __name__ == "__main__":
    unittest.main()
