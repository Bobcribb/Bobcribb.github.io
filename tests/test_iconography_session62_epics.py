"""MYTHOS séance 62 : conservation, sourçage et alternance iconographiques."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("philosophie-iliade.html", "iliade-long-b08", "icono-iliade-patrocle-corps-devoir-s62-20261106", "/assets/philosophie/iliade-patrocle-corps-devoir-s62-20261106.svg", "https://www.theoi.com/Text/HomerIliad17.html", True),
    ("philosophie-odyssee.html", "odyssee-long-b02", "icono-odyssee-sirenes-engagement-s62-20261106", "/assets/philosophie/odyssee-sirenes-engagement-s62-20261106.svg", "https://www.theoi.com/Text/HomerOdyssey12.html", True),
    ("philosophie-theogonie.html", "partie-6", "icono-theogonie-aphrodite-cygne-pistoxenos-s62-20261106", "/media/2026/10/mythos-aphrodite-cygne-kylix-british-museum.jpg", "https://commons.wikimedia.org/wiki/File:Aphrodite_swan_BM_D2.jpg", False),
)

class EpicsIconography62Tests(unittest.TestCase):
    def test_figures_unique_sourced_accessible_and_local(self):
        for page, section, ident, src, source, is_schema in CASES:
            with self.subTest(page=page):
                doc=BeautifulSoup((ROOT/page).read_text(encoding="utf-8"),"html.parser")
                figures=doc.find_all("figure",id=ident)
                self.assertEqual(len(figures),1)
                fig=figures[0]
                self.assertIsNotNone(doc.find("section",id=section).find("figure",id=ident))
                img=fig.find("img")
                self.assertEqual(img.get("src"),src)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"),"lazy")
                self.assertGreater(int(img.get("width",0)),0)
                self.assertGreater(int(img.get("height",0)),0)
                self.assertEqual(len(doc.find_all("img",src=src)),1)
                self.assertTrue((ROOT/src.lstrip("/")).is_file())
                cap=fig.find("figcaption")
                self.assertIsNotNone(cap.find("a",href=source))
                self.assertIn("IA",cap.get_text(" ",strip=True))
                self.assertIn("non historique" if is_schema else "artefact grec antique",cap.get_text(" ",strip=True))
                if is_schema:
                    svg=ET.parse(ROOT/src.lstrip("/")).getroot()
                    ns="{http://www.w3.org/2000/svg}"
                    self.assertEqual(svg.tag,ns+"svg")
                    for tag in ("title","desc","metadata"):
                        self.assertIsNotNone(svg.find(ns+tag))
                ids=[x["id"] for x in doc.find_all(id=True)]
                self.assertEqual(len(ids),len(set(ids)))
                for a in doc.find_all("a",href=True):
                    if a["href"].startswith("#") and len(a["href"])>1:
                        self.assertIn(a["href"][1:],ids)
    def test_alternation_and_historic_minimum_a4(self):
        d=json.loads((ROOT/"docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(d["latest_session"],d["history"][-1])
        # La séance 62 demeure dans l'historique lorsque les séances suivantes arrivent.
        # Ne pas exiger qu'elle reste indéfiniment latest_session.
        matches = [(i, event) for i, event in enumerate(d["history"])
                   if event.get("scope", "").startswith("Séance 62 :")]
        self.assertEqual(len(matches), 1)
        position, session62 = matches[0]
        self.assertGreater(position, 0)
        self.assertEqual(session62["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(session62["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session62["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(d["history"][position - 1]["kind"], "AUDIT ET CORRECTION")
        if position + 1 < len(d["history"]):
            self.assertEqual(d["history"][position + 1]["kind"], "AUDIT ET CORRECTION")
        p=json.loads((ROOT/"assets/philosophie/pagination-2026-11-04.json").read_text(encoding="utf-8"))
        for work in ("iliade","odyssee","theogonie"):
            self.assertGreaterEqual(p["studies"][work]["analyse-seule_pages"],10)

if __name__ == "__main__":
    unittest.main()
