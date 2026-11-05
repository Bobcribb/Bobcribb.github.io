"""Régressions de l'enrichissement documentaire MYTHOS, séance 54."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("osiris-abydos-cultes-textes-funeraires/index.html",
     "icono-osiris-anubis-met-570675-20261105", 570675, "5. Anubis"),
    ("bibliotheque-egypte-ancienne/index.html",
     "icono-egypte-maat-met-551794-20261105", 551794, "7. Maat"),
    ("bibliotheque-egypte-ancienne/index.html",
     "icono-egypte-thot-maat-met-544093-20261105", 544093, "7. Maat"),
    ("gilgamesh-epopee-mort-deluge/index.html",
     "icono-gilgamesh-shamash-humbaba-sceau-met-327455-20261105",
     327455, "3. Amitié"),
)


class DocumentaryIconographyTests(unittest.TestCase):
    def test_museum_sources_media_and_context(self):
        catalogue = json.loads(
            (ROOT / "assets/illustrations-articles/sources-met.json").read_text(
                encoding="utf-8"))
        objects = {entry["object_id"]: entry for entry in catalogue["images"]}
        for path, figure_id, object_id, heading in CASES:
            with self.subTest(page=path, object_id=object_id):
                page = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"),
                                     "html.parser")
                figures = page.select("figure#" + figure_id)
                self.assertEqual(len(figures), 1)
                fig = figures[0]
                img = fig.find("img")
                self.assertIsNotNone(img)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertEqual(img["src"], "/" + objects[object_id]["path"])
                self.assertTrue((ROOT / objects[object_id]["path"]).is_file())
                self.assertIn("CC0-1.0", objects[object_id]["license"])
                self.assertIn("non générée par IA", fig.get_text(" ", strip=True))
                self.assertIn("CC0", fig.get_text(" ", strip=True))
                self.assertIn(objects[object_id]["source_url"],
                              [a.get("href") for a in fig.select("figcaption a")])
                prev = fig.find_previous(["h2", "h3"])
                self.assertIsNotNone(prev)
                self.assertIn(heading, prev.get_text(" ", strip=True))
                self.assertEqual(len(page.select('img[src="' + img["src"] + '"]')), 1)

    def test_unique_html_ids_on_modified_pages(self):
        for path in dict.fromkeys(case[0] for case in CASES):
            with self.subTest(page=path):
                page = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"),
                                     "html.parser")
                ids = [node["id"] for node in page.select("[id]")]
                self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
