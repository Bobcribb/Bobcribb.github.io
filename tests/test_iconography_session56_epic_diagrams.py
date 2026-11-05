"""Séance MYTHOS 56 : images 2D sourcées et alternance horaire."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CASES=[["philosophie-iliade.html","assets/philosophie/iliade-scamandre-limite-s56-20261105.svg","icono-iliade-scamandre-limite-s56-20261105"],["philosophie-odyssee.html","assets/philosophie/odyssee-outis-metis-s56-20261105.svg","icono-odyssee-outis-metis-s56-20261105"],["philosophie-theogonie.html","assets/philosophie/theogonie-deesses-mortels-s56-20261105.svg","icono-theogonie-deesses-mortels-s56-20261105"]]
class Iconography56(unittest.TestCase):
    def test_media_and_documentation(self):
        for page,asset,ident in CASES:
            with self.subTest(page=page):
                html=BeautifulSoup((ROOT/page).read_text(encoding="utf-8"),"html.parser")
                figures=html.find_all("figure",id=ident)
                self.assertEqual(len(figures),1)
                fig=figures[0]
                img=fig.find("img")
                self.assertEqual(img.get("src"),"/"+asset)
                self.assertTrue(img.get("alt"))
                self.assertEqual(img.get("width"),"1200")
                self.assertEqual(img.get("height"),"650")
                self.assertIn("assistance IA",fig.get_text(" ",strip=True))
                self.assertTrue(fig.select_one('a[href^="https://"]'))
                self.assertTrue((ROOT/asset).is_file())
                svg=ET.parse(ROOT/asset).getroot()
                self.assertEqual(svg.tag,"{http://www.w3.org/2000/svg}svg")
                for tag in ("title","desc","metadata"):
                    self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}"+tag))
                ids=[e["id"] for e in html.find_all(id=True)]
                self.assertEqual(len(ids),len(set(ids)))
    def test_alternation_and_minimum_a4(self):
        d=json.loads((ROOT/"docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(d["latest_session"],d["history"][-1])
        # Vérifier la séance 56 à sa position historique : latest_session
        # doit évoluer à chaque nouvelle heure sans invalider ce test.
        matches = [(i, entry) for i, entry in enumerate(d["history"])
                   if entry.get("scope", "").startswith("Séance 56 :")]
        self.assertEqual(len(matches), 1, "Une seule séance 56 doit être consignée")
        position, session56 = matches[0]
        self.assertGreater(position, 0)
        self.assertEqual(d["history"][position - 1]["kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session56["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(session56["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session56["next_kind"], "AUDIT ET CORRECTION")
        if position + 1 < len(d["history"]):
            self.assertEqual(d["history"][position + 1]["kind"], "AUDIT ET CORRECTION")
        p=json.loads((ROOT/"assets/philosophie/pagination-2026-11-04.json").read_text(encoding="utf-8"))
        for k in ("iliade","odyssee","theogonie"):
            self.assertGreaterEqual(p["studies"][k]["analyse-seule_pages"],10)
if __name__=="__main__":unittest.main()
