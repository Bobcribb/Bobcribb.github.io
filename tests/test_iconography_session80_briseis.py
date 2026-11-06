"""MYTHOS séance 80 : Briséis, statut d'une figure contemporaine et alternance."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import unittest

from bs4 import BeautifulSoup
from scripts import verify_live_site as live

ROOT = Path(__file__).resolve().parents[1]
PAGE = "philosophie-iliade.html"
FIGURE = "icono-iliade-briseis-deuil-parole-s80-20261106"
ASSET = "/assets/philosophie/iliade-briseis-deuil-parole-s80-20261106.svg"

class IconographySession80Briseis(unittest.TestCase):
    def test_dedicated_section_and_status(self):
        markup = (ROOT / PAGE).read_text(encoding="utf-8")
        soup = BeautifulSoup(markup, "html.parser")
        figures = soup.find_all("figure", id=FIGURE)
        self.assertEqual(len(figures), 1)
        figure = figures[0]
        self.assertEqual(figure.find_previous("h2")["id"], "lecture-section-16")
        self.assertIn("assistance IA", figure.get("data-image-status", ""))
        self.assertIn("non artefact antique", figure.get("data-image-status", ""))
        image = figure.find("img")
        self.assertEqual(image["src"], ASSET)
        self.assertEqual(image["loading"], "lazy")
        self.assertTrue(image["alt"].strip())
        self.assertEqual(len(soup.find_all("img", src=ASSET)), 1)
        caption = figure.figcaption.get_text(" ", strip=True)
        for key in ("Briséis", "282–302", "géras", "assistance IA", "non artefact antique"):
            self.assertIn(key, caption)
        metadata = live.figure_metadata(markup, FIGURE, ASSET)
        self.assertIn("https://beta.perseus.tufts.edu/urn%3Acts%3AgreekLit%3Atlg0012.tlg001.perseus-grc2%3A19.276/", metadata["source_urls"])
        ids = [el["id"] for el in soup.find_all(id=True)]
        self.assertEqual(len(ids), len(set(ids)))
        for a in soup.select('a[href^="#"]'):
            if len(a["href"]) > 1:
                self.assertIn(a["href"][1:], ids)

    def test_original_svg_and_https_publication_guard(self):
        body = (ROOT / ASSET.lstrip("/")).read_bytes()
        self.assertTrue(live.valid_local_illustration(ASSET, body))
        root = ET.fromstring(body)
        ns = "{http://www.w3.org/2000/svg}"
        self.assertEqual(root.tag, ns+"svg")
        self.assertEqual(len(root.findall(ns+"title")), 1)
        self.assertEqual(len(root.findall(ns+"desc")), 1)
        self.assertIn("assistance IA", body.decode("utf-8"))
        self.assertIn("non artefact historique", body.decode("utf-8"))
        self.assertEqual(live.RECENT_FIGURES.count((PAGE, FIGURE, ASSET)), 1)

    def test_session_80_follows_audit_79(self):
        journal = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        events = [e for e in journal["history"] if e.get("session_number", 0) >= 74]
        self.assertEqual(events[-1]["session_number"], 80)
        self.assertEqual(events[-1]["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(events[-1]["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(journal["latest_session"], events[-1])
        for previous, current in zip(events, events[1:]):
            self.assertEqual(previous["session_number"]+1, current["session_number"])
            self.assertEqual(previous["next_kind"], current["kind"])
            self.assertEqual(current["previous_kind"], previous["kind"])
            self.assertNotEqual(previous["kind"], current["kind"])

if __name__ == "__main__":
    unittest.main()
