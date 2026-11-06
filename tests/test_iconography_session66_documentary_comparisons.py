"""MYTHOS séance 66 : illustrations documentaires sans doublon, alt ni dérive de l'alternance."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASES = [
  [
    "philosophie-iliade.html",
    "lecture-section-32",
    "icono-iliade-poseidon-artemision-s66-20261106",
    "/media/2026/10/mythos-bronze-artemision-zeus-ou-poseidon.jpg",
    "https://www.theoi.com/Text/HomerIliad13.html",
    "https://commons.wikimedia.org/wiki/File:Bronze_statue_of_Zeus_or_Poseidon_from_Artemision,_Euboea._ca._460_BC.jpg"
  ],
  [
    "philosophie-odyssee.html",
    "lecture-section-29",
    "icono-odyssee-orphee-eurydice-seuil-s66-20261106",
    "/media/2026/10/mythos-relief-orphee-eurydice-hermes-naples-6727.jpg",
    "https://www.theoi.com/Text/HomerOdyssey11.html",
    "https://commons.wikimedia.org/wiki/File:Orfeo,_euridice_ed_hermes,_da_torre_del_greco,_copia_augustea_da_orig._greco_del_450_ac_ca._6727.JPG"
  ],
  [
    "philosophie-theogonie.html",
    "lecture-section-14",
    "icono-theogonie-yazilikaya-teshub-hebat-s66-20261106",
    "/media/2026/10/mythos-yazilikaya-teshub-hebat-rita1234.jpg",
    "https://whc.unesco.org/en/list/377/",
    "https://commons.wikimedia.org/wiki/File:Yazilikaya_reliefs_42_43.JPG"
  ]
]

class Session66Iconography(unittest.TestCase):
    def test_reused_documentary_artifacts_are_unique_and_sourced(self):
        for page, heading_id, ident, src, primary, credit in CASES:
            with self.subTest(page=page):
                soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                figs = soup.find_all("figure", id=ident)
                self.assertEqual(len(figs), 1)
                fig = figs[0]
                self.assertEqual(fig.find_previous("h2").get("id"), heading_id)
                self.assertEqual(fig.find("img").get("src"), src)
                self.assertTrue(fig.find("img").get("alt", "").strip())
                self.assertEqual(fig.find("img").get("loading"), "lazy")
                self.assertEqual(len(soup.find_all("img", src=src)), 1)
                self.assertTrue((ROOT / src.lstrip("/")).is_file())
                cap = fig.find("figcaption")
                self.assertTrue(cap)
                self.assertIn("non générée par IA", cap.get_text(" ", strip=True))
                self.assertTrue(cap.find("a", href=primary))
                self.assertTrue(cap.find("a", href=credit))
                ids = [element["id"] for element in soup.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for link in soup.find_all("a", href=True):
                    if link["href"].startswith("#") and len(link["href"]) > 1:
                        self.assertIn(link["href"][1:], ids)

    def test_stable_historic_session_and_a4_minimum(self):
        d = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(d["latest_session"], d["history"][-1])
        found = [(i, s) for i, s in enumerate(d["history"]) if s.get("scope", "").startswith("Séance 66 :")]
        self.assertEqual(len(found), 1)
        i, session = found[0]
        self.assertGreater(i, 0)
        self.assertEqual(session["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(session["previous_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(session["next_kind"], "AUDIT ET CORRECTION")
        self.assertEqual(d["history"][i-1]["kind"], "AUDIT ET CORRECTION")
        if i + 1 < len(d["history"]):
            self.assertEqual(d["history"][i+1]["kind"], "AUDIT ET CORRECTION")
        pagination = json.loads((ROOT / "assets/philosophie/pagination-2026-11-04.json").read_text(encoding="utf-8"))
        for work in ("iliade", "odyssee", "theogonie"):
            self.assertGreaterEqual(pagination["studies"][work]["analyse-seule_pages"], 10)

if __name__ == "__main__":
    unittest.main()
