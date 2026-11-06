"""Tests éditoriaux MYTHOS — séance 78, Tartare et alternance."""
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from scripts import verify_live_site as live

ROOT = Path(__file__).resolve().parents[1]
PAGE = "philosophie-theogonie.html"
ID = "icono-theogonie-tartare-limites-s78-20261106"
SRC = "/assets/philosophie/theogonie-tartare-limites-s78-20261106.svg"

class Session78Iconography(unittest.TestCase):
    def test_source_figure_is_documented_accessible_and_in_right_section(self):
        soup = BeautifulSoup((ROOT/PAGE).read_text(encoding="utf-8"), "html.parser")
        figs = soup.find_all("figure", id=ID)
        self.assertEqual(len(figs), 1)
        fig = figs[0]
        self.assertEqual(fig.find_previous("h2")["id"], "lecture-section-35")
        img = fig.find("img")
        self.assertEqual(img["src"], SRC)
        self.assertEqual(img["loading"], "lazy")
        self.assertTrue(img["alt"].strip())
        self.assertEqual(len(soup.find_all("img", src=SRC)), 1)
        txt = fig.find("figcaption").get_text(" ", strip=True)
        for phrase in ("Hésiode", "720–735", "744–757", "assistance IA", "non artefact antique"):
            self.assertIn(phrase, txt)
        self.assertIsNotNone(fig.find("figcaption").find("a", href="https://chs.harvard.edu/primary-source/hesiod-theogony-sb/"))
        ids = [tag["id"] for tag in soup.find_all(id=True)]
        self.assertEqual(len(ids), len(set(ids)))
        for a in soup.select('a[href^="#"]'):
            if len(a["href"]) > 1:
                self.assertIn(a["href"][1:], ids)

    def test_svg_is_well_formed_and_non_archaeological(self):
        content = (ROOT/SRC.lstrip("/")).read_text(encoding="utf-8")
        root = ET.fromstring(content)
        ns = "{http://www.w3.org/2000/svg}"
        self.assertEqual(root.tag, ns+"svg")
        self.assertEqual(len(root.findall(ns+"title")), 1)
        self.assertEqual(len(root.findall(ns+"desc")), 1)
        self.assertIn("assistance IA", content)
        self.assertIn("non artefact historique", content)
        self.assertIn("sans perspective 2,5D", content)

    def test_https_guard_and_session_alternation(self):
        self.assertEqual(live.RECENT_FIGURES.count((PAGE,ID,SRC)), 1)
        metadata = live.figure_metadata((ROOT/PAGE).read_text(encoding="utf-8"), ID, SRC)
        self.assertIn("assistance IA", metadata["status"])
        self.assertIn("https://chs.harvard.edu/primary-source/hesiod-theogony-sb/", metadata["source_urls"])
        doc = json.loads((ROOT/"docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        evs = [e for e in doc["history"] if e.get("session_number",0)>=74]
        s78 = [e for e in evs if e["session_number"]==78]
        self.assertEqual(len(s78),1)
        self.assertEqual(s78[0]["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(s78[0]["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(s78[0]["next_kind"], "AUDIT ET CORRECTION")
        for x,y in zip(evs,evs[1:]):
            self.assertEqual(x["session_number"]+1,y["session_number"])
            self.assertEqual(x["next_kind"],y["kind"])
            self.assertNotEqual(x["kind"],y["kind"])
        self.assertEqual(doc["latest_session"], doc["history"][-1])

if __name__ == "__main__":
    unittest.main()
