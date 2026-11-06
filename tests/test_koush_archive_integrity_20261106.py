"""Conservation du volume XII Koush et ordre de publication des sources Théâtre."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REL = "bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/index.html"
PAGE = ROOT / REL
sys.path.insert(0, str(ROOT / "scripts"))
from archival_prose_integrity import verify, normalize_prose, extract_original_body
from apply_museum_design import apply as apply_design


class KoushIntegralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = PAGE.read_text(encoding="utf-8")
        cls.prose = verify(PAGE, "texte-integral-koush-meroe", 36371,
                           "fc817178632b87b3d413afdb28794bb13d4659d4")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")

    def test_scholarly_text_and_sources_intact(self):
        for token in ("Apédémak", "Méroé", "Amanitore", "Natakamani", "Sources et documentation"):
            self.assertIn(token, self.prose)
        self.assertEqual(len(self.doc.select(".mythos-original-study h2")), 20)
        self.assertEqual(len(self.doc.select(".mythos-original-study h2, .mythos-original-study h3")), 63)

    def test_toc_and_return_navigation(self):
        toc = self.doc.select('details.mythos-world-study-toc a[href^="#koush-lecture-"]')
        self.assertEqual(len(toc), 20)
        for link in toc:
            self.assertIsNotNone(self.doc.find(id=link["href"][1:]))
        self.assertEqual(len(self.doc.select(".mythos-original-study span.mythos-text-anchor")), 63)
        for link in ('/mythologies/', '/civilisations/afrique/',
                     '/bibliotheque-mythologies-du-monde/civilisations-histoire-koush-meroe/'):
            self.assertIn('href="' + link + '"', self.raw)
        nav = (ROOT / "scripts/build_navigation.py").read_text(encoding="utf-8")
        self.assertIn('"/bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/"', nav)
        self.assertIn('if key == "afrique"', nav)

    def test_photo_provenance_and_mobile(self):
        fig = self.doc.select_one("figure.mythos-koush-figure")
        self.assertIsNotNone(fig)
        self.assertIn("LassiHU", fig.get_text(" ", strip=True))
        self.assertIn("creativecommons.org/licenses/by-sa/4.0/", self.raw)
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertIn("mythos-koush-figure", css)
        self.assertIn("@media(max-width:720px)", css)

    def test_museum_design_preserves_every_word(self):
        with tempfile.TemporaryDirectory() as tmp:
            rendered = Path(tmp) / REL
            rendered.parent.mkdir(parents=True)
            shutil.copyfile(PAGE, rendered)
            self.assertEqual(apply_design(tmp), 1)
            html = rendered.read_text(encoding="utf-8")
            self.assertEqual(normalize_prose(extract_original_body(html, "texte-integral-koush-meroe")), self.prose)

    def test_third_party_theatre_fix_precedes_museum_and_reindex(self):
        s = (ROOT / "scripts/build_native.py").read_text(encoding="utf-8")
        # Les neuf sources des comédies doivent précéder la charte et l'index.
        pos = s.index("build_readers(ROOT, OUT, theatre_source_records)")
        self.assertLess(pos, s.index("n_styled = apply_museum_design(OUT)"))
        self.assertLess(pos, s.index("n_indexed = reindex(chapters)", s.index("install_eneide_source_access(ROOT, OUT)")))


if __name__ == "__main__":
    unittest.main()
