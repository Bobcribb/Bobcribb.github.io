"""MYTHOS séance 68 : présence, traçabilité et alternance sans figer le dernier numéro."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("philosophie-iliade.html", "icono-iliade-troie-vi-porte-est-s68-20261106",
     "/media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg", "https://commons.wikimedia.org/wiki/File:Walls_of_Troy_(1).jpg"),
    ("philosophie-odyssee.html", "icono-odyssee-achille-patrocle-flaxman-s68-20261106",
     "/assets/illustrations-articles/met-341681-achille-ombre-patrocle-flaxman.webp", "https://www.metmuseum.org/art/collection/search/341681"),
    ("philosophie-theogonie.html", "icono-theogonie-hephaistos-retour-oakeshott-s68-20261106",
     "/media/2026/10/hephaiestos-retour-olympe-coupe-oakeshott-17-230-5.png", "https://www.metmuseum.org/art/collection/search/250543"),
)

class Session68Iconography(unittest.TestCase):
    def test_figure_and_source_preserved(self):
        for path, figure_id, asset, source in CASES:
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                self.assertEqual(1, content.count('id="' + figure_id + '"'))
                self.assertIn('src="' + asset + '"', content)
                self.assertIn(source, content)
                self.assertTrue((ROOT / asset.lstrip("/")).is_file())
                figure = re.search(r'<figure\b[^>]*\bid="' + re.escape(figure_id)
                                   + r'"[^>]*>(.*?)</figure>', content, re.S)
                self.assertIsNotNone(figure)
                self.assertRegex(figure.group(1), r'<img\b[^>]*\balt="[^"]+"')
                self.assertIn('non génér', figure.group(0))
    def test_session68_is_unique_and_alternates(self):
        report = json.loads((ROOT / "docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json").read_text(encoding="utf-8"))
        sessions = [x for x in report["history"] if x.get("scope", "").startswith("Séance 68 :")]
        self.assertEqual(1, len(sessions))
        entry = sessions[0]
        self.assertEqual("ENRICHISSEMENT ICONOGRAPHIQUE", entry["kind"])
        self.assertEqual("AUDIT ET CORRECTION", entry["previous_kind"])
        self.assertEqual("AUDIT ET CORRECTION", entry["next_kind"])
        i = report["history"].index(entry)
        self.assertTrue(i > 0)
        self.assertEqual("AUDIT ET CORRECTION", report["history"][i - 1]["kind"])
        if i + 1 < len(report["history"]):
            self.assertEqual("AUDIT ET CORRECTION", report["history"][i + 1]["kind"])

if __name__ == "__main__":
    unittest.main()
