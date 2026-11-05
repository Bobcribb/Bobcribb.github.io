"""Contrôles statiques des documents patrimoniaux MYTHOS — séance 58.

Ne requiert pas de connexion aux CDN dans la CI ; la disponibilité
du média sur le site déployé est un contrôle HTTPS distinct.
"""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "philosophie-iliade.html": (
        "icono-iliade-sophilos-jeux-patrocle-s58-20261105",
        "lecture-section-39",
        "olympicgames.culture.gov.gr",
        "Athènes, Musée archéologique national",
    ),
    "philosophie-odyssee.html": (
        "icono-odyssee-berlin-cithare-demodocos-s58-20261105",
        "lecture-section-25",
        "metmuseum.org/art/collection/search/254896",
        "56.171.38",
    ),
    "philosophie-theogonie.html": (
        "icono-theogonie-athena-naissance-metis-s58-20261105",
        "lecture-section-39",
        "metmuseum.org/art/collection/search/247515",
        "06.1097",
    ),
}


class MuseumDocumentsSession58Tests(unittest.TestCase):
    def test_three_documentary_figures_are_unique_contextual_and_provenanced(self):
        for page, (figure_id, section_id, source, provenance) in FIGURES.items():
            with self.subTest(page=page):
                doc = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                figures = doc.find_all("figure", id=figure_id)
                self.assertEqual(len(figures), 1)
                figure = figures[0]
                self.assertIn("non générée par IA", figure.get("data-image-status", ""))
                heading = doc.find("h2", id=section_id)
                self.assertIsNotNone(heading)
                self.assertIsNotNone(heading.find_parent("section").find("figure", id=figure_id))
                img = figure.find("img")
                self.assertIsNotNone(img)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertTrue(img.get("src", "").startswith("https://"))
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn(source, str(caption))
                self.assertIn(provenance, caption.get_text(" ", strip=True))
                self.assertIn("aucune création IA", caption.get_text(" ", strip=True))
                self.assertIn("av. J.-C.", caption.get_text(" ", strip=True))
                self.assertEqual(len(doc.find_all("img", src=img["src"])), 1)

    def test_history_58_is_preserved_when_later_sessions_are_appended(self):
        report = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        matches = [x for x in report["history"] if x.get("scope", "").startswith("Séance 58 :")]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(matches[0]["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(matches[0]["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(len(matches[0]["new_figures"]), 3)
        self.assertEqual(len({x["id"] for x in matches[0]["new_figures"]}), 3)


if __name__ == "__main__":
    unittest.main()
