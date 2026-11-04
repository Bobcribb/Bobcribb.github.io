"""Regression checks for the restored full-length La Galigo article and documentary folio.

The visual supplement must never replace scholarly paragraphs with a summary.
"""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "bibliotheque-mythologies-du-monde" / "mythos-volume-19-la-galigo-bugis-sawerigading" / "index.html"
STYLES = ROOT / "assets" / "mythos-museum.css"


class GaligoDocumentaryIllustrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")

    def test_integral_scholarly_study_is_preserved(self):
        study = self.doc.select_one("section#etude-integrale")
        self.assertIsNotNone(study)
        self.assertGreaterEqual(len(study.get_text(" ", strip=True)), 34000)
        self.assertGreaterEqual(len(study.select("p")), 60)
        self.assertIsNotNone(study.select_one("#bibliographie"))
        for anchor in ("sawerigading-voyages", "we-cudaiq-heroines", "manuscrits-lontara"):
            self.assertIsNotNone(study.select_one(f"#{anchor}"))
        self.assertIsNotNone(self.doc.select_one('nav[aria-label="Parcours de lecture"]'))

    def test_single_documentary_image_has_sources_and_license(self):
        figures = self.doc.select('figure[data-mythos-illustration="leiden-galigo-1906"]')
        self.assertEqual(len(figures), 1)
        figure = figures[0]
        img = figure.select_one("img")
        self.assertIsNotNone(img)
        self.assertIn("upload.wikimedia.org/wikipedia/commons/", img["src"])
        self.assertIn("La_Galigo_item_29355-0009", img["src"])
        self.assertGreater(len(img.get("alt", "")), 45)
        self.assertEqual(img.get("loading"), "lazy")
        self.assertIsNotNone(figure.select_one('a[href="https://hdl.handle.net/1887.1/item:29487"]'))
        self.assertIsNotNone(figure.select_one('a[href="https://creativecommons.org/licenses/by-sa/4.0/"]'))
        self.assertIn("non reconstitution", figure.get_text(" ", strip=True))
        self.assertLess(str(figure).find("2.5D"), 0)

    def test_portal_card_uses_the_same_verified_folio(self):
        portal = BeautifulSoup((ROOT / "mythologies" / "index.html").read_text(encoding="utf-8"), "html.parser")
        link = portal.select_one('a.portal-card[href="/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/"]')
        self.assertIsNotNone(link)
        img = link.select_one('img[data-mythos-card-source="la-galigo-leiden"]')
        self.assertIsNotNone(img)
        self.assertEqual(img.get("loading"), "lazy")
        self.assertIn("La_Galigo_item_29355-0009", img["src"])
        self.assertIn("Leiden University Libraries", link.get_text(" ", strip=True))
        self.assertIn("CC BY-SA 4.0", link.get_text(" ", strip=True))

    def test_responsive_layout_has_mobile_and_print_rules(self):
        stylesheet = STYLES.read_text(encoding="utf-8")
        self.assertIn(".mythos-manuscript-figure", stylesheet)
        self.assertIn("@media(max-width:620px)", stylesheet)
        self.assertIn("break-inside:avoid", stylesheet)

    def test_portal_rebuild_preserves_the_documentary_folio(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from build_navigation import card
        rendered = BeautifulSoup(card('/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/', 'Sulawesi — La Galigo'), 'html.parser')
        original = self.doc.select_one('figure[data-mythos-illustration="leiden-galigo-1906"] img')
        self.assertEqual(original['src'], rendered.img['src'])
        self.assertIn('Leiden University Libraries', rendered.get_text())
        self.assertIn('CC BY-SA 4.0', rendered.get_text())


if __name__ == "__main__":
    unittest.main()
