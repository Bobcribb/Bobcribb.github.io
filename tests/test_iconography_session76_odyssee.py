"""MYTHOS séance 76 : figure 2D originale et alternance conservée."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "philosophie-odyssee.html"
ASSET = ROOT / "assets/philosophie/odyssee-arc-preuve-autorite-s76-20261106.svg"
FIGURE = "icono-odyssee-arc-preuve-autorite-s76-20261106"

class IconographySession76(unittest.TestCase):
    def test_odyssee_arc_figure_is_accessible_and_does_not_duplicate_content(self):
        soup = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        figures = soup.find_all("figure", id=FIGURE)
        self.assertEqual(len(figures), 1)
        figure = figures[0]
        self.assertEqual(figure.find_previous("h2").get("id"), "lecture-section-38")
        self.assertIn("assistance IA", figure.get("data-image-status", ""))
        image = figure.find("img")
        self.assertEqual(image.get("src"), "/assets/philosophie/odyssee-arc-preuve-autorite-s76-20261106.svg")
        self.assertEqual(image.get("loading"), "lazy")
        self.assertTrue(image.get("alt", "").strip())
        self.assertEqual(len(soup.find_all("img", src="/assets/philosophie/odyssee-arc-preuve-autorite-s76-20261106.svg")), 1)
        self.assertTrue(ASSET.is_file())
        caption = figure.find("figcaption").get_text(" ", strip=True)
        for required in ("Odyssée", "Pénélope", "douze haches", "assistance IA", "ni artefact"):
            self.assertIn(required.lower(), caption.lower())
        self.assertIsNotNone(figure.find("a", href="https://homer.johnhboyer.com/odyssey/book/21/"))
        ids = [tag["id"] for tag in soup.find_all(id=True)]
        self.assertEqual(len(ids), len(set(ids)))
        for link in soup.select('a[href^="#"]'):
            if len(link["href"]) > 1:
                self.assertIn(link["href"][1:], ids)

    def test_svg_is_explicable_two_dimensional_not_an_antique_object(self):
        content = ASSET.read_text(encoding="utf-8")
        self.assertIn("<title", content)
        self.assertIn("<desc", content)
        self.assertIn("Schéma éditorial 2D", content)
        self.assertIn("assistance IA", content)
        self.assertIn("non artefact grec", content)
        self.assertIn("Odyssée XXI", content)

    def test_session_alternation_has_no_duplicate_adjacent_types(self):
        journal = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        sessions = [e for e in journal["history"] if e.get("session_number") in (74, 75, 76)]
        self.assertEqual([e["session_number"] for e in sessions], [74, 75, 76])
        self.assertEqual([e["kind"] for e in sessions], [
            "ENRICHISSEMENT ICONOGRAPHIQUE",
            "AUDIT ET CORRECTION",
            "ENRICHISSEMENT ICONOGRAPHIQUE",
        ])
        self.assertEqual(sessions[-1]["next_kind"], "AUDIT ET CORRECTION")
        # The latest session naturally advances on the next hourly run;
        # this test must not freeze the journal at session 76 forever.
        self.assertEqual(journal["latest_session"], journal["history"][-1])
        later = [event for event in journal["history"]
                 if event.get("session_number", 0) >= 74]
        for previous, current in zip(later, later[1:]):
            self.assertEqual(current["session_number"], previous["session_number"] + 1)
            self.assertEqual(current["previous_kind"], previous["kind"])
            self.assertEqual(previous["next_kind"], current["kind"])
            self.assertNotEqual(previous["kind"], current["kind"])

if __name__ == "__main__":
    unittest.main()
