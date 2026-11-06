"""Séance 74 : documentation antique sans doublons et correction HTML conservatrice."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("philosophie-iliade.html", "lecture-section-15", "icono-iliade-nike-victoire-met247903-s74-20261106", "/assets/illustrations-articles/met-247903-nike-terre-cuite.webp", 247903),
    ("philosophie-theogonie.html", "lecture-section-40", "icono-theogonie-persephone-retour-met252973-s74-20261106", "/assets/illustrations-articles/met-252973-persephone-retour-enfers.webp", 252973),
]
class IconographySession74(unittest.TestCase):
    def test_new_figures_have_anchored_context_and_scientific_status(self):
        for page, heading_id, figure_id, src, object_id in CASES:
            with self.subTest(page=page):
                soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                figs = soup.find_all("figure", id=figure_id)
                self.assertEqual(len(figs), 1)
                fig = figs[0]
                self.assertEqual(fig.find_previous("h2").get("id"), heading_id)
                self.assertIn("non générée par IA", fig.get("data-image-status", ""))
                img = fig.find("img")
                self.assertEqual(img.get("src"), src)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertGreater(int(img.get("width", 0)), 0)
                self.assertGreater(int(img.get("height", 0)), 0)
                self.assertEqual(len(soup.find_all("img", src=src)), 1)
                self.assertTrue((ROOT / src.lstrip("/")).is_file())
                caption = fig.find("figcaption")
                self.assertIn("Metropolitan Museum of Art", caption.get_text(" ", strip=True))
                self.assertIn("CC0", caption.get_text(" ", strip=True))
                self.assertIn("non générée par IA", caption.get_text(" ", strip=True))
                self.assertTrue(caption.find("a", href=f"https://www.metmuseum.org/art/collection/search/{object_id}"))
                ids = [node.get("id") for node in soup.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(all(a.get("href")[1:] in ids for a in soup.find_all("a", href=True) if a.get("href", "").startswith("#") and len(a["href"]) > 1))
    def test_reader_navigation_attributes_remain_valid(self):
        p = ROOT / "bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/cycle-sigurd-brynhildr-fafnir-nibelungen/nibelungenlied-kriemhild-hagen/index.html"
        html = p.read_text(encoding="utf-8")
        self.assertNotIn('class="reader-bottom data-reading-owned="true"', html)
        soup = BeautifulSoup(html, "html.parser")
        nav = soup.find("nav", class_="reader-bottom")
        self.assertIsNotNone(nav)
        self.assertEqual(nav.get("data-reading-owned"), "true")
        self.assertIsNotNone(soup.find(id="nibelungen-01"))
    def test_alternation_after_session_73(self):
        data = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        events = data["history"]
        sessions74 = [(pos, event) for pos, event in enumerate(events) if event["session_number"] == 74]
        self.assertEqual(len(sessions74), 1)
        pos, event = sessions74[0]
        self.assertGreater(pos, 0)
        self.assertEqual(events[pos - 1]["kind"], "AUDIT ET CORRECTION")
        self.assertEqual(event["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(event["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(event["next_kind"], "AUDIT ET CORRECTION")
        if pos + 1 < len(events):
            self.assertEqual(events[pos + 1]["kind"], "AUDIT ET CORRECTION")
        self.assertEqual(data["latest_session"], events[-1])
if __name__ == "__main__":
    unittest.main()
