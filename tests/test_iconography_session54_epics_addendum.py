"""Contrôles de provenance et non-régression, complément de la séance 54 MYTHOS."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_live_site as live

CASES = (
    ("iliade/index.html", "lecture-3d9ef4210377", "icono-iliade-apollon-peste-met-246408-s54-20261105", 246408),
    ("odyssee/index.html", "lecture-c65dcea7cf34", "icono-odyssee-hermes-calypso-met-246679-s54-20261105", 246679),
    ("livre-hesiode/index.html", "metis", "icono-hesiode-athena-metis-met-254648-s54-20261105", 254648),
)

class EpicIconographySession54Tests(unittest.TestCase):
    def test_documented_figures_and_file_hashes(self):
        data = json.loads((ROOT / "assets/illustrations-articles/sources-met.json").read_text(encoding="utf-8"))
        catalogue = {entry["object_id"]: entry for entry in data["images"]}
        for page, anchor, figure_id, object_id in CASES:
            with self.subTest(page=page):
                document = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                figures = document.find_all("figure", id=figure_id)
                self.assertEqual(len(figures), 1)
                figure = figures[0]
                self.assertIn("authentique", figure.get("data-image-status", ""))
                heading = document.find(id=anchor)
                self.assertIsNotNone(heading)
                self.assertIs(figure.find_previous(["h2", "h3"]), heading)
                item = catalogue[object_id]
                self.assertTrue(item["is_public_domain"])
                self.assertEqual(item["license"], "CC0-1.0")
                image = figure.find("img")
                self.assertIsNotNone(image)
                source = "/" + item["path"]
                self.assertEqual(image.get("src"), source)
                self.assertEqual(image.get("loading"), "lazy")
                self.assertEqual(int(image.get("width")), item["width"])
                self.assertEqual(int(image.get("height")), item["height"])
                self.assertTrue(image.get("alt", "").strip())
                self.assertEqual(len(document.find_all("img", src=source)), 1)
                self.assertIn("non générée par IA", figure.get_text(" ", strip=True))
                self.assertIn("Metropolitan Museum of Art", figure.get_text(" ", strip=True))
                self.assertIn("CC0", figure.get_text(" ", strip=True))
                self.assertIsNotNone(figure.find("a", href=item["source_url"]))
                self.assertEqual(len(document.find_all(id=True)), len(set(x["id"] for x in document.find_all(id=True))))
                for link in document.find_all("a", href=True):
                    if link["href"].startswith("#") and len(link["href"]) > 1:
                        self.assertIsNotNone(document.find(id=link["href"][1:]))
                path = ROOT / item["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
                self.assertEqual(live.RECENT_FIGURES.count((page, figure_id, source)), 1)

    def test_session_log_preserves_strict_alternation(self):
        data = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        history = data["history"]
        self.assertEqual(data["latest_session"], history[-1])
        matches = [(i, session) for i, session in enumerate(history)
                   if session.get("scope", "").startswith("Séance 54 :")]
        self.assertEqual(len(matches), 1, "La séance historique 54 doit être unique")
        position, session54 = matches[0]
        self.assertEqual(session54["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(session54["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session54["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(len(session54["figures"]), 7)
        if position + 1 < len(history):
            self.assertEqual(history[position + 1]["kind"], "AUDIT ET CORRECTION")

if __name__ == "__main__":
    unittest.main()
