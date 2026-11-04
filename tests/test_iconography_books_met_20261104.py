"""Figures documentaires dans les trois livres grecs : unicité et distinction des sources."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FIGURES = (
    ("livre-iliade-scenes/index.html", "temps", "guerre",
     "icono-iliade-enee-virgile-distinction-20261104", 199612,
     "œuvre de réception renaissante authentique, non générée par IA"),
    ("livre-odyssee/index.html", "chant-5", "chant-6",
     "icono-odyssee-hermes-bronze-met-246679-20261104", 246679,
     "artefact antique authentique, non généré par IA"),
    ("livre-hesiode/index.html", "promethee", "feu",
     "icono-hesiode-promethee-bartolozzi-1795-20261104", 680363,
     "œuvre de réception moderne authentique, non générée par IA"),
)

class MetBookIconographyTests(unittest.TestCase):
    def test_three_distinct_documentary_figures_are_located_and_sourced(self):
        manifest = json.loads((ROOT / "assets/illustrations-articles/sources-met.json").read_text(encoding="utf-8"))
        objects = {item["object_id"]: item for item in manifest["images"]}
        for page, start_id, end_id, fig_id, met_id, status in FIGURES:
            with self.subTest(page=page):
                doc = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                figures = doc.find_all("figure", id=fig_id)
                self.assertEqual(len(figures), 1)
                fig = figures[0]
                self.assertEqual(fig.get("data-image-status"), status)
                anchor = doc.find("h2", id=start_id)
                self.assertIsNotNone(anchor)
                following = list(anchor.next_siblings)
                boundary = next(i for i, node in enumerate(following)
                                if getattr(node, "name", None) == "h2" and node.get("id") == end_id)
                self.assertIn(fig, following[:boundary])
                data = objects[met_id]
                img = fig.find("img")
                self.assertIsNotNone(img)
                self.assertEqual(img.get("src"), "/" + data["path"])
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertEqual(int(img.get("width")), data["width"])
                self.assertEqual(int(img.get("height")), data["height"])
                self.assertTrue((ROOT / data["path"]).is_file())
                self.assertEqual(len(doc.find_all("img", src="/" + data["path"])), 1)
                caption = fig.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn("non généré", caption.get_text(" ", strip=True))
                self.assertIn("CC0", caption.get_text(" ", strip=True))
                self.assertIsNotNone(caption.find("a", href=data["source_url"]))
                ids = [element.get("id") for element in doc.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))

    def test_editorial_distinction_between_epic_and_reception(self):
        cases = (
            ("livre-iliade-scenes/index.html", "icono-iliade-enee-virgile-distinction-20261104",
             ["hors du récit", "Virgile"]),
            ("livre-odyssee/index.html", "icono-odyssee-hermes-bronze-met-246679-20261104",
             ["postérieur", "Calypso"]),
            ("livre-hesiode/index.html", "icono-hesiode-promethee-bartolozzi-1795-20261104",
             ["non du partage", "521–534"]),
        )
        for page, fig_id, terms in cases:
            with self.subTest(page=page):
                doc = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                fig = doc.find("figure", id=fig_id)
                legend = fig.find("figcaption").get_text(" ", strip=True)
                for term in terms:
                    self.assertIn(term, legend)

if __name__ == "__main__":
    unittest.main()
