"""Régression documentaire — trois figures de la séance iconographique après audit."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("livre-iliade-scenes/index.html", "atelier-narratologie-iliade",
     "icono-iliade-rembrandt-reception-homere-livre-20261104", 437394,
     "œuvre de réception moderne authentique, non générée par IA"),
    ("livre-odyssee/index.html", "chant-1",
     "icono-odyssee-athena-chouette-met-254648-20261104", 254648,
     "artefact antique authentique, non généré par IA"),
    ("livre-hesiode/index.html", "aphrodite",
     "icono-hesiode-aphrodite-hellenistique-met-253504-20261104", 253504,
     "artefact antique authentique, non généré par IA"),
)

class SecondMuseumBookFigures(unittest.TestCase):
    def test_figures_are_unique_sourced_and_within_their_subject_sections(self):
        manifest = json.loads((ROOT / "assets/illustrations-articles/sources-met.json").read_text(encoding="utf-8"))
        catalog = {item["object_id"]: item for item in manifest["images"]}
        for path, section_id, figure_id, object_id, status in CASES:
            with self.subTest(path=path):
                page = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                headings = page.find_all("h2", id=section_id)
                self.assertEqual(len(headings), 1)
                figures = page.find_all("figure", id=figure_id)
                self.assertEqual(len(figures), 1)
                figure = figures[0]
                self.assertEqual(figure.get("data-image-status"), status)
                node = headings[0].find_next_sibling()
                while node is not None and node.name != "h2" and node != figure:
                    node = node.find_next_sibling()
                self.assertIs(node, figure, "Figure déplacée hors de sa section")
                item = catalog[object_id]
                image = figure.find("img")
                self.assertIsNotNone(image)
                self.assertEqual(image.get("src"), "/" + item["path"])
                self.assertEqual(image.get("loading"), "lazy")
                self.assertEqual(int(image.get("width")), item["width"])
                self.assertEqual(int(image.get("height")), item["height"])
                self.assertTrue(image.get("alt", "").strip())
                self.assertTrue((ROOT / item["path"]).is_file())
                self.assertEqual(len(page.find_all("img", src="/" + item["path"])), 1)
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn("non générée par IA", caption.get_text(" ", strip=True))
                self.assertIn("Metropolitan Museum of Art", caption.get_text(" ", strip=True))
                self.assertIn("CC0", caption.get_text(" ", strip=True))
                self.assertIsNotNone(caption.find("a", href=item["source_url"]))
                ids = [x["id"] for x in page.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for link in page.find_all("a", href=True):
                    if link["href"].startswith("#") and len(link["href"]) > 1:
                        self.assertIn(link["href"][1:], ids)

if __name__ == "__main__":
    unittest.main()
