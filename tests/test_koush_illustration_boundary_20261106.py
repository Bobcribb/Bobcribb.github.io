"""Contrôle de l'image documentaire sans altération de l'archive universitaire de Koush."""
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from editorial_illustrations import eligible_paragraph, section_heading_ok
from archival_prose_integrity import verify

PAGE = ROOT / "bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/index.html"


class KoushIllustrationBoundaryTests(unittest.TestCase):
    def test_original_scholarly_prose_and_illustration_are_both_preserved(self):
        # Historical reference is the WordPress original, not the caption text.
        verify(PAGE, "texte-integral-koush-meroe", 36371,
               "fc817178632b87b3d413afdb28794bb13d4659d4")
        doc = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        archive = doc.select_one("#texte-integral-koush-meroe.mythos-original-study")
        self.assertIsNotNone(archive)
        self.assertFalse(archive.select("figure[data-media-id]"))
        figure = doc.select_one(
            'figure[data-archival-figure="outside-protected-prose"]'
            '[data-media-id="mythos-met-544874-amon-statuette-or"]'
        )
        self.assertIsNotNone(figure)
        self.assertIsNone(figure.find_parent(class_="mythos-original-study"))
        self.assertIn("Amon et la victoire", figure.get_text(" ", strip=True))
        self.assertIsNotNone(figure.select_one('a[href^="https://www.metmuseum.org/"]'))

    def test_decorative_placement_cannot_target_protected_wordpress_blocks(self):
        doc = BeautifulSoup(
            '<article><div class="mythos-original-study">'
            '<h2>Amon et souveraineté</h2>'
            '<p>' + ("Prose universitaire à conserver intacte. " * 6) + '</p>'
            '</div><p>' + ("Contexte éditorial extérieur. " * 7) + '</p></article>',
            "html.parser",
        )
        self.assertFalse(eligible_paragraph(doc.select_one(".mythos-original-study p")))
        self.assertFalse(section_heading_ok(doc.select_one(".mythos-original-study h2")))
        self.assertTrue(eligible_paragraph(doc.select_one("article > p")))


if __name__ == "__main__":
    unittest.main()
