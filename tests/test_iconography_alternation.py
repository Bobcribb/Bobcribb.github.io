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
    "livre-iliade-scenes/index.html": ("icono-iliade-louvre-g153-corps-hector-20261104", "/assets/philosophie/documents/iliade-02.jpg"),
    "livre-odyssee/index.html": ("icono-odyssee-sirenes-stamnos-bm-e440-20261104", "/assets/philosophie/documents/odyssee-02.jpg"),
    "livre-hesiode/index.html": ("icono-hesiode-enuma-elish-comparaison-tablette-k3473-20261104", "/assets/philosophie/documents/theogonie-03.jpg"),
    "philosophie-iliade.html": ("icono-iliade-mycene-panorama-philosophie-20261104", "/assets/reconstitutions-3d/mycenes-citadelle-porte-lionnes-panorama.webp"),
    "philosophie-odyssee.html": ("icono-odyssee-tirynthe-palais-20261104", "/assets/reconstitutions-3d/tirynthe-citadelle-mycenienne-panorama.webp"),
    "philosophie-theogonie.html": ("icono-theogonie-zeus-olympie-altis-20261104", "/assets/reconstitutions-3d/olympie-altis-panorama.webp"),
}



RECEPTION_FIGURES = {
    "philosophie-iliade.html": ("icono-iliade-flaxman-ombre-patrocle-reception-20261104", "/assets/illustrations-articles/met-341681-achille-ombre-patrocle-flaxman.webp", "lecture-section-9"),
    "philosophie-odyssee.html": ("icono-odyssee-flaxman-parker-circe-1805-20261104", "/assets/illustrations-articles/met-705224-ulysse-circe-flaxman.webp", "lecture-section-8"),
    "philosophie-theogonie.html": ("icono-theogonie-ottley-nuit-enfants-attribution-20261104", "/assets/illustrations-articles/met-649972-ottley-nuit-enfants.webp", "lecture-section-8"),
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

    def test_reception_images_are_unique_sourced_accessible_and_in_context(self):
        for path, (figure_id, image_src, section_id) in RECEPTION_FIGURES.items():
            with self.subTest(page=path):
                doc = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                figs = doc.find_all("figure", id=figure_id)
                self.assertEqual(len(figs), 1)
                figure = figs[0]
                self.assertEqual(figure.get("data-image-status"), "œuvre de réception moderne authentique, non générée par IA")
                heading = doc.find(id=section_id)
                self.assertIsNotNone(heading)
                self.assertIsNotNone(heading.find_parent("section"))
                self.assertIn(figure, heading.find_parent("section").descendants)
                img = figure.find("img")
                self.assertIsNotNone(img)
                self.assertEqual(img.get("src"), image_src)
                self.assertTrue(img.get("alt", "").strip())
                self.assertGreater(int(img.get("width", "0")), 0)
                self.assertGreater(int(img.get("height", "0")), 0)
                self.assertEqual(len(doc.find_all("img", src=image_src)), 1)
                self.assertTrue((ROOT / image_src.lstrip("/")).is_file())
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                text = caption.get_text(" ", strip=True)
                self.assertIn("non générée par IA", text)
                self.assertIn("Metropolitan Museum of Art", text)
                self.assertIn("CC0", text)
                self.assertTrue(any(a.get("href", "").startswith("https://www.metmuseum.org/art/collection/search/")
                                    for a in caption.find_all("a", href=True)))
                ids = [e.get("id") for e in doc.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for a in doc.find_all("a", href=True):
                    if a["href"].startswith("#") and len(a["href"]) > 1:
                        self.assertIn(a["href"][1:], ids)

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
