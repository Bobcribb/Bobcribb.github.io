"""Conservation de l'étude arménienne de 47 776 caractères et de ses lecteurs."""
from pathlib import Path
import re
import sys
import shutil
import tempfile
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REL = "bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/index.html"
PAGE = ROOT / REL
NAV = ROOT / "scripts/build_navigation.py"
CSS = ROOT / "assets/mythos-museum.css"
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


class ArmenianHistoricalVolumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = PAGE.read_text(encoding="utf-8")
        begin = '<div class="mythos-original-study" id="texte-integral-armenie-sassoun">\n'
        end = '\n</div>\n<section'
        if begin not in cls.full or end not in cls.full:
            raise AssertionError("Borniers éditoriaux du manuscrit manquants")
        cls.marked = cls.full.split(begin, 1)[1].split(end, 1)[0]
        cls.original = re.sub(
            r'<span\b(?=[^>]*mythos-text-anchor)[^>]*></span>', '', cls.marked)
        cls.scholarly_text, cls.scholarly_hash = scholarly_fingerprint(cls.marked)

    def test_source_entire_and_documented(self):
        # Le HTML peut être sérialisé par BeautifulSoup lors du catalogue,
        # mais la prose universitaire doit rester strictement identique.
        self.assertIn('data-original-html-length="47776"', self.full)
        self.assertEqual(len(self.scholarly_text), 35162)
        self.assertEqual(self.scholarly_hash, '04082ae0a21b1cd6')
        self.assertEqual(len(re.findall(r"<h[23][ >]", self.original)), 63)
        self.assertEqual(len(re.findall(r"<h2[ >]", self.original)), 20)
        for token in ("Vahagn", "Anahit", "David de Sassoun", "Sources et documentation", "ich.unesco.org"):
            self.assertIn(token, self.original)

    def test_exact_toc_and_no_duplicate_ids(self):
        doc = BeautifulSoup(self.full, "html.parser")
        ids = [el.get("id") for el in doc.find_all(id=True)]
        self.assertEqual(len(ids), len(set(ids)))
        links = doc.select('details.mythos-world-study-toc a[href^="#armenian-lecture-"]')
        self.assertEqual(len(links), 20)
        for link in links:
            self.assertIsNotNone(doc.find(id=link["href"][1:]))
        self.assertEqual(len(doc.select("span.mythos-text-anchor")), 63)

    def test_historical_cote_and_reciprocal_portals(self):
        self.assertIn('data-source-archive="wordpress-1137"', self.full)
        self.assertIn('data-original-html-length="47776"', self.full)
        self.assertTrue(REL.startswith("bibliotheque-mythologies-du-monde/"))
        self.assertIn('href="/mythologies/"', self.full)
        self.assertIn('href="/civilisations/europe/"', self.full)
        nav = NAV.read_text(encoding="utf-8")
        self.assertIn('"/bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/"', nav)
        self.assertIn('if key == "europe"', nav)
        self.assertIn('sassoun-kochar-2014', nav)

    def test_image_license_and_responsive_css(self):
        doc = BeautifulSoup(self.full, "html.parser")
        figure = doc.select_one("figure.mythos-sassoun-figure")
        self.assertIsNotNone(figure)
        self.assertIn("Kochar", figure.get_text(" ", strip=True))
        self.assertIn("2014", figure.get_text(" ", strip=True))
        self.assertIn("creativecommons.org/licenses/by-sa/4.0/", self.full)
        self.assertNotIn("mythos-original-study", figure.get("class", []))
        self.assertIn("mythos-sassoun-figure", CSS.read_text(encoding="utf-8"))
        self.assertIn("@media(max-width:720px)", CSS.read_text(encoding="utf-8"))

    def test_museum_pass_preserves_scholarly_text(self):
        expected = BeautifulSoup(self.original, "html.parser").get_text(" ", strip=True)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / REL
            output.parent.mkdir(parents=True)
            shutil.copyfile(PAGE, output)
            self.assertEqual(apply_museum_design(tmp), 1)
            doc = BeautifulSoup(output.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(doc.body.get("data-mythos-design"), "20261104")
            self.assertIsNotNone(doc.select_one(".mythos-masthead"))
            self.assertIsNotNone(doc.select_one(".mythos-banner"))
            self.assertIsNotNone(doc.select_one('link[href*="mythos-museum.css"]'))
            self.assertEqual(doc.select_one(".mythos-original-study").get_text(" ", strip=True), expected)


if __name__ == "__main__":
    unittest.main()
