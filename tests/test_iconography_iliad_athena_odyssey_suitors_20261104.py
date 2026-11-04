"""MYTHOS : figures sourcées des chants V de l'Iliade et XXII de l'Odyssée."""
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "livre-iliade-scenes/index.html": {
        "section": "diomede",
        "id": "icono-iliade-athena-diomede-met-254648-20261104",
        "src": "/assets/illustrations-articles/met-254648-athena-chouette-bronze.webp",
        "source": "https://www.metmuseum.org/art/collection/search/254648",
        "identifier": "50.11.1",
    },
    "livre-odyssee/index.html": {
        "section": "chant-22",
        "id": "icono-odyssee-pretendants-skyphos-tarquinia-20261104",
        "src": "/assets/philosophie/documents/odyssee-03.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Odysseus_slays_the_suitors_of_his_wife_Penelope_(Skyphos_pot).jpg",
        "identifier": "F 2588",
    },
}


class GreekBooksDocumentaryFiguresTests(unittest.TestCase):
    def test_each_figure_is_unique_local_accessible_sourced_and_inside_chapter(self):
        for path, entry in FIGURES.items():
            with self.subTest(path=path):
                doc = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                figure = doc.find_all("figure", id=entry["id"])
                self.assertEqual(len(figure), 1)
                figure = figure[0]
                self.assertIn("non générée par IA", figure.get("data-image-status", ""))
                img = figure.find("img")
                self.assertIsNotNone(img)
                self.assertEqual(img.get("src"), entry["src"])
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertTrue((ROOT / entry["src"].lstrip("/")).is_file())
                self.assertEqual(len(doc.find_all("img", src=entry["src"])), 1)
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn(entry["identifier"], caption.get_text(" ", strip=True))
                self.assertIn("non générée par IA", caption.get_text(" ", strip=True))
                self.assertIsNotNone(caption.find("a", href=entry["source"]))
                heading = doc.find("h2", id=entry["section"])
                self.assertIsNotNone(heading)
                within = False
                for sibling in heading.next_siblings:
                    if getattr(sibling, "name", None) == "h2":
                        break
                    if sibling is figure:
                        within = True
                self.assertTrue(within, "La figure doit se trouver dans le bon chant")
                ids = [node.get("id") for node in doc.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for anchor in doc.find_all("a", href=True):
                    href = anchor["href"]
                    if href.startswith("#") and len(href) > 1:
                        self.assertIn(href[1:], ids)


if __name__ == "__main__":
    unittest.main()
