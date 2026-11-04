"""Protect one documented La Galigo folio while refusing unapproved card images.

The museum-design pass must be idempotent, preserve the original article
paragraphs and credits, and must never restore legacy SVG 2.5D illustrations.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply

CARD_URL = "/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/"
FOLIO_URL = ("https://upload.wikimedia.org/wikipedia/commons/1/10/"
             "La_Galigo_item_29355-0009_%28cropped2%29.jpg")


class VerifiedCardTests(unittest.TestCase):
    def test_approved_folio_survives_three_museum_passes(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "mythologies" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<!doctype html><html lang="fr"><head><title>Mythologies</title></head>'
                '<body><main><article class="content"><h1>Mythologies du monde</h1>'
                '<a class="portal-card" href="' + CARD_URL + '">'
                '<img class="mythos-card-image" data-mythos-card-source="la-galigo-leiden" '
                'src="' + FOLIO_URL + '" alt="Folio de Leyde" loading="lazy"/>'
                '<span>Sulawesi — La Galigo · Leiden University Libraries · CC BY-SA 4.0</span>'
                '</a><p id="manuscrit">Document intégral préservé, sources et bibliographie.</p>'
                '</article></main></body></html>', encoding="utf-8"
            )
            for _ in range(3):
                self.assertEqual(apply(root), 1)
                soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                image = soup.select_one('a.portal-card[href="' + CARD_URL + '"] '
                                        'img[data-mythos-card-source="la-galigo-leiden"]')
                self.assertIsNotNone(image)
                self.assertEqual(image.get("src"), FOLIO_URL)
                self.assertEqual(len(soup.select('a.portal-card[href="' + CARD_URL + '"] img')), 1)
                self.assertIn("Leiden University Libraries", soup.select_one("a.portal-card").get_text(" ", strip=True))
                self.assertIn("CC BY-SA 4.0", soup.select_one("a.portal-card").get_text(" ", strip=True))
                self.assertEqual(soup.select_one("#manuscrit").get_text(" ", strip=True),
                                 "Document intégral préservé, sources et bibliographie.")

    def test_unapproved_svg_card_does_not_survive(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "mythologies" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<html><head><title>Mythologies</title></head><body>'
                '<main><article><h1>Mythologies</h1>'
                '<a class="portal-card" href="/mythes-inconnus/">'
                '<img class="mythos-card-image" src="/assets/reconstitutions-3d/ancien-2-5d.svg" alt=""/>'
                '<span>Texte scientifique conservé.</span></a>'
                '</article></main></body></html>', encoding="utf-8"
            )
            self.assertEqual(apply(root), 1)
            html = page.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            self.assertIsNone(soup.select_one('img[src*="ancien-2-5d.svg"]'))
            self.assertIn("Texte scientifique conservé.", soup.get_text(" ", strip=True))


if __name__ == "__main__":
    unittest.main()
