"""Intégrité des trois enrichissements 2D des profils héroïques — séance 60 MYTHOS.

Conserve le texte source, évite le doublonnage et rend la provenance explicite.
"""
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("heros-achille/index.html", "icono-achille-deux-destins-profil-s60-20261105",
     "/assets/philosophie/iliade-achille-deux-destins.svg", "L’ambassade et les deux destins",
     "https://www.theoi.com/Text/HomerIliad9.html"),
    ("heros-hector/index.html", "icono-hector-andromaque-devoirs-profil-s60-20261105",
     "/assets/philosophie/iliade-hector-andromaque.svg", "Hector dans Troie",
     "https://www.theoi.com/Text/HomerIliad6.html"),
    ("heros-penelope/index.html", "icono-penelope-lit-olivier-profil-s60-20261105",
     "/assets/philosophie/odyssee-lit-olivier-signe-20261104.svg", "Le lit d’olivier",
     "https://www.theoi.com/Text/HomerOdyssey23.html"),
)


class HeroProfileIconographyTests(unittest.TestCase):
    def test_figures_provenance_ia_and_semantic_context(self):
        for path, figure_id, src, heading, source_url in CASES:
            with self.subTest(path=path):
                soup = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                figures = soup.find_all("figure", id=figure_id)
                self.assertEqual(len(figures), 1)
                fig = figures[0]
                self.assertIn("assisté par IA", fig.get("data-image-status", ""))
                self.assertIn("non historique", fig.get("data-image-status", ""))
                img = fig.find("img")
                self.assertEqual(img.get("src"), src)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertGreater(int(img.get("width", 0)), 0)
                self.assertGreater(int(img.get("height", 0)), 0)
                self.assertEqual(len(soup.find_all("img", src=src)), 1)
                asset = ROOT / src.lstrip("/")
                self.assertTrue(asset.is_file())
                svg = BeautifulSoup(asset.read_text(encoding="utf-8"), "html.parser")
                self.assertIsNotNone(svg.find("svg"))
                self.assertIsNotNone(svg.find("title"))
                self.assertIsNotNone(svg.find("desc"))
                caption = fig.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn("assisté par IA", caption.get_text(" ", strip=True))
                self.assertIn("aucun artefact antique", caption.get_text(" ", strip=True))
                self.assertIsNotNone(caption.find("a", href=source_url))
                previous_h3 = fig.find_previous("h3")
                self.assertIsNotNone(previous_h3)
                self.assertEqual(previous_h3.get_text(" ", strip=True), heading)

    def test_no_duplicate_ids_broken_local_fragments_or_missing_assets(self):
        for path, *_ in CASES:
            with self.subTest(path=path):
                soup = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
                ids = [tag["id"] for tag in soup.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for anchor in soup.find_all("a", href=True):
                    href = anchor["href"]
                    if href.startswith("#") and len(href) > 1:
                        self.assertIn(href[1:], ids)
                for tag in soup.find_all(["img", "script", "link"]):
                    src = tag.get("src") or tag.get("href") or ""
                    if src.startswith(("/assets/", "/media/")):
                        self.assertTrue((ROOT / src.split("?", 1)[0].lstrip("/")).is_file(), src)

    def test_three_epics_have_existing_a4_analysis_above_ten_pages(self):
        import json
        pag = json.loads((ROOT / "assets/philosophie/pagination-2026-11-04.json").read_text(encoding="utf-8"))
        for work in ("iliade", "odyssee", "theogonie"):
            with self.subTest(work=work):
                self.assertGreaterEqual(pag["studies"][work]["analyse-seule_pages"], 10)


if __name__ == "__main__":
    unittest.main()
