"""Garde-fous de l'alternance du chantier iconographique MYTHOS.

Ne modifie ni le registre de numérotation ni les planifications horaires.
"""
import json
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "MYTHOS_ICONOGRAPHIE_ALTERNANCE.json"
MONOGRAPHS = {
    "philosophie-iliade.html": ("icono-iliade-mycene-panorama-philosophie-20261104", "/assets/reconstitutions-3d/mycenes-citadelle-porte-lionnes-panorama.webp"),
    "philosophie-odyssee.html": ("icono-odyssee-tirynthe-palais-20261104", "/assets/reconstitutions-3d/tirynthe-citadelle-mycenienne-panorama.webp"),
    "philosophie-theogonie.html": ("icono-theogonie-zeus-olympie-altis-20261104", "/assets/reconstitutions-3d/olympie-altis-panorama.webp"),
}


class IconographyAlternationTests(unittest.TestCase):
    def test_last_logged_session_and_next_kind_are_consistent(self):
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        history = data["history"]
        self.assertGreaterEqual(len(history), 2)
        self.assertEqual(data["latest_session"], history[-1])
        self.assertEqual(history[-1]["previous_kind"], history[-2]["kind"])
        self.assertNotEqual(history[-1]["next_kind"], history[-1]["kind"])
        allowed = {"AUDIT ET CORRECTION", "ENRICHISSEMENT ICONOGRAPHIQUE"}
        self.assertTrue(all(event["kind"] in allowed for event in history))
        for previous, current in zip(history, history[1:]):
            self.assertNotEqual(previous["kind"], current["kind"])
        encoded = [json.dumps(event, sort_keys=True, ensure_ascii=False) for event in history]
        self.assertEqual(len(encoded), len(set(encoded)), "Le même audit figure deux fois dans l'historique")

    def test_recent_illustrations_are_present_and_documented(self):
        for path, (figure_id, image_src) in MONOGRAPHS.items():
            with self.subTest(page=path):
                doc = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                figures = doc.find_all("figure", id=figure_id)
                self.assertEqual(len(figures), 1)
                figure = figures[0]
                image = figure.find("img")
                self.assertIsNotNone(image)
                self.assertEqual(image.get("src"), image_src)
                self.assertTrue(image.get("alt", "").strip())
                self.assertTrue((ROOT / image_src.lstrip("/")).is_file())
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn("IA", caption.get_text(" ", strip=True))
                self.assertTrue(any(a.get("href", "").startswith("https://") for a in caption.find_all("a")))

                ids = [element["id"] for element in doc.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for link in doc.find_all("a", href=True):
                    target = link["href"]
                    if target.startswith("#") and len(target) > 1:
                        self.assertIn(target[1:], ids)


if __name__ == "__main__":
    unittest.main()
