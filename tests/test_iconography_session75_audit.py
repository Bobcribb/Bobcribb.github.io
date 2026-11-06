"""Séance 75 — garde-fous de structure pour les trois études et le lecteur."""
from pathlib import Path
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

class Session75StructureAudit(unittest.TestCase):
    def test_local_anchors_figure_alts_and_css_js_exist(self):
        for page in PAGES:
            with self.subTest(page=page):
                soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
                ids = [tag.get("id") for tag in soup.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)), "Identifiants HTML dupliqués")
                for link in soup.find_all("a", href=True):
                    target = link["href"]
                    if target.startswith("#") and len(target) > 1:
                        self.assertIn(target[1:], ids, f"Ancre absente dans {page}: {target}")
                for img in soup.find_all("img"):
                    self.assertTrue(img.has_attr("alt") and img.get("alt", "").strip(),
                                    f"Image sans texte alternatif dans {page}")
                for node in soup.select('link[rel="stylesheet"][href], script[src]'):
                    resource = node.get("href") or node.get("src")
                    if resource.startswith("/"):
                        file = ROOT / resource.split("?", 1)[0].lstrip("/")
                        self.assertTrue(file.is_file(), f"CSS/JS absent : {file}")

    def test_nibelungen_navigation_is_unique_and_crosslink_retained(self):
        page = PAGES[-1]
        markup = (ROOT / page).read_text(encoding="utf-8")
        self.assertNotIn('class="reader-bottom data-reading-owned="', markup)
        soup = BeautifulSoup(markup, "html.parser")
        bottom = soup.find_all("nav", attrs={"aria-label": "Poursuivre la lecture"})
        self.assertEqual(len(bottom), 1)
        self.assertEqual(bottom[0].get("data-reading-owned"), "true")
        self.assertIn("Nouvelle étude du cycle", soup.get_text(" ", strip=True))

if __name__ == "__main__":
    unittest.main()
