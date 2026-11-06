"""Séance 71 : contrôle des ajouts s70 et conservation de l'alternance."""
import json
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_live_site as live

CASES = (
    ("philosophie-iliade.html", "icono-iliade-chryses-crise-s70-20261106", "/assets/philosophie/iliade-chryses-crise-20261106-s70.svg"),
    ("philosophie-odyssee.html", "icono-odyssee-ithaque-paix-s70-20261106", "/assets/philosophie/odyssee-ithaque-paix-20261106-s70.svg"),
    ("philosophie-theogonie.html", "icono-theogonie-athena-bronze-met-s70-20261106", "/assets/illustrations-articles/met-254648-athena-chouette-bronze.webp"),
    ("dieu-hestia/index.html", "icono-hestia-laraire-vettii-comparaison-s70-20261106", "/media/2026/10/mythos-lararium-maison-vettii-pompei-lorente-waterborough.jpg"),
    ("theatre-grec.html", "icono-theatre-masques-met-2001-767-s70-20261106", "/media/2026/10/mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg"),
)

class AuditIconography71Tests(unittest.TestCase):
    def test_five_documentary_figures_are_in_live_verification(self):
        for page, fid, asset in CASES:
            with self.subTest(page=page):
                self.assertEqual(live.RECENT_FIGURES.count((page, fid, asset)), 1)
                raw = (ROOT / page).read_text(encoding="utf-8")
                meta = live.figure_metadata(raw, fid, asset)
                self.assertTrue(meta["status"])
                self.assertTrue(meta["source_urls"])
                self.assertTrue(meta["alt"])
                self.assertTrue((ROOT / asset.lstrip("/")).is_file())
                self.assertTrue(live.valid_local_illustration(
                    asset, (ROOT / asset.lstrip("/")).read_bytes()))
                document = BeautifulSoup(raw, "html.parser")
                ids = [tag["id"] for tag in document.select("[id]")]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(all(x.get("alt") is not None for x in document.find_all("img")))

    def test_session_seventy_one_follows_seventy_once(self):
        report = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        history = report["history"]
        self.assertEqual(report["latest_session"], history[-1])
        session_71 = [row for row in history if row.get("session_number") == 71]
        self.assertEqual(len(session_71), 1)
        recorded_71 = session_71[0]
        self.assertEqual(recorded_71["kind"], "AUDIT ET CORRECTION")
        self.assertEqual(recorded_71["previous_kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(recorded_71["next_kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        index_71 = history.index(recorded_71)
        self.assertGreater(index_71, 0)
        self.assertEqual(history[index_71 - 1].get("session_number"), 70)
        if index_71 + 1 < len(history):
            self.assertEqual(history[index_71 + 1].get("session_number"), 72)
            self.assertEqual(history[index_71 + 1]["kind"], "ENRICHISSEMENT ICONOGRAPHIQUE")
        self.assertEqual(sum(e.get("session_number") == 70 for e in history), 1)
        self.assertEqual(sum(e.get("session_number") == 71 for e in history), 1)

if __name__ == "__main__":
    unittest.main()
