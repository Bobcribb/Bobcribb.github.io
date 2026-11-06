"""Séance 77 : ressources locales et accessibilité de la figure s76."""
from pathlib import Path
from xml.etree import ElementTree as ET
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "philosophie-iliade.html",
    "philosophie-odyssee.html",
    "philosophie-theogonie.html",
    "bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/"
    "cycle-sigurd-brynhildr-fafnir-nibelungen/nibelungenlied-kriemhild-hagen/index.html",
)
ASSET = ROOT / "assets/philosophie/odyssee-arc-preuve-autorite-s76-20261106.svg"

class IconographySession77Audit(unittest.TestCase):
    def test_every_local_image_css_and_script_is_a_file(self):
        for page in PAGES:
            with self.subTest(page=page):
                soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                for node in soup.select("img[src], link[rel='stylesheet'][href], script[src]"):
                    url = node.get("src") or node.get("href")
                    if url and url.startswith("/"):
                        path = ROOT / url.split("?", 1)[0].split("#", 1)[0].lstrip("/")
                        self.assertTrue(path.is_file(), f"Ressource locale manquante : {page} → {url}")
                self.assertIsNotNone(soup.find("html", lang="fr"))
                self.assertIsNotNone(soup.find("meta", attrs={"name": "viewport"}))
                headings = soup.find_all("h1")
                self.assertEqual(len(headings), 1, f"Hiérarchie H1 irrégulière : {page}")

    def test_session76_svg_is_well_formed_and_declared_as_interpretation(self):
        root = ET.fromstring(ASSET.read_bytes())
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        titles = root.findall("{http://www.w3.org/2000/svg}title")
        descriptions = root.findall("{http://www.w3.org/2000/svg}desc")
        self.assertEqual(len(titles), 1)
        self.assertEqual(len(descriptions), 1)
        self.assertTrue(titles[0].text and descriptions[0].text)
        self.assertIn("non artefact", ASSET.read_text(encoding="utf-8"))
        self.assertIn("assistance IA", ASSET.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
