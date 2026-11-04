"""MYTHOS : provenance de Nikè et seuil d'illustration des trois livres grecs."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ("livre-iliade-scenes/index.html", "livre-odyssee/index.html", "livre-hesiode/index.html")
ID = "icono-hesiode-styx-nike-met-247903-20261104"
IMAGE = "/assets/illustrations-articles/met-247903-nike-terre-cuite.webp"

class HesiodeNikeTests(unittest.TestCase):
    def test_nike_documentary_figure_and_provenance(self):
        doc = BeautifulSoup((ROOT / BOOKS[2]).read_text(encoding="utf-8"), "html.parser")
        anchor = doc.find("h2", id="titanides")
        figure = doc.find("figure", id=ID)
        self.assertIsNotNone(anchor)
        self.assertIsNotNone(figure)
        self.assertIs(anchor.find_next_sibling(), figure)
        self.assertEqual(len(doc.find_all("figure", id=ID)), 1)
        self.assertEqual(figure.get("data-image-status"), "artefact antique authentique, non généré par IA")
        asset = next(x for x in json.loads((ROOT / "assets/illustrations-articles/sources-met.json").read_text(encoding="utf-8"))["images"] if x["object_id"] == 247903)
        self.assertEqual(IMAGE, "/" + asset["path"])
        self.assertTrue((ROOT / asset["path"]).is_file())
        self.assertTrue(asset["is_public_domain"])
        self.assertEqual(asset["license"], "CC0-1.0")
        img = figure.find("img")
        self.assertEqual(img["src"], IMAGE)
        self.assertTrue(img["alt"])
        self.assertEqual(int(img["width"]), asset["width"])
        self.assertEqual(int(img["height"]), asset["height"])
        self.assertEqual(len(doc.find_all("img", src=IMAGE)), 1)
        caption = figure.find("figcaption")
        s = caption.get_text(" ", strip=True)
        for expected in ("383–403", "Metropolitan Museum of Art", "07.286.23", "CC0", "non générée par IA", "postérieur"):
            self.assertIn(expected, s)
        self.assertIsNotNone(caption.find("a", href=asset["source_url"]))
        ids = [x["id"] for x in doc.find_all(id=True)]
        self.assertEqual(len(ids), len(set(ids)))
        for x in doc.find_all("a", href=True):
            if x["href"].startswith("#") and len(x["href"]) > 1:
                self.assertIn(x["href"][1:], ids)

    def test_all_three_books_ten_accessible_images(self):
        for book in BOOKS:
            with self.subTest(book=book):
                doc = BeautifulSoup((ROOT / book).read_text(encoding="utf-8"), "html.parser")
                images = doc.find_all("img")
                self.assertGreaterEqual(len(images), 10)
                self.assertTrue(all(image.get("alt", "").strip() for image in images))

if __name__ == "__main__":
    unittest.main()
