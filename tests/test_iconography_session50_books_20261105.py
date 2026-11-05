"""Séance 50 : provenance, pertinence, accessibilité et unicité des figures des trois lecteurs MYTHOS."""
import unittest
import json
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "assets/illustrations-articles/sources-met.json"
FIGURES = (
    ("livre-iliade-scenes/index.html", "crise", "icono-iliade-apollon-peste-bronze-met-246408-20261105", "/assets/illustrations-articles/met-246408-apollon-bronze-romain.webp", 246408, "96.9.401"),
    ("livre-odyssee/index.html", "chant-11", "icono-odyssee-persephone-nekuia-met-252973-20261105", "/assets/illustrations-articles/met-252973-persephone-retour-enfers.webp", 252973, "28.57.23"),
    ("livre-hesiode/index.html", "mariages-zeus", "icono-hesiode-dionysos-genealogie-met-256902-20261105", "/assets/illustrations-articles/met-256902-dionysos-medaillon-bois.webp", 256902, "1998.43"),
)


class Session50GreekBooksTests(unittest.TestCase):
    def test_documentary_figures_are_in_the_right_sections_without_duplication(self):
        catalog = json.loads(SOURCES.read_text(encoding="utf-8"))
        records = {entry["object_id"]: entry for entry in catalog["images"]}
        for path, section, fid, source, object_id, accession in FIGURES:
            with self.subTest(page=path):
                page = ROOT / path
                doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                ids = [el["id"] for el in doc.find_all(id=True)]
                self.assertEqual(len(ids), len(set(ids)))
                for link in doc.find_all("a", href=True):
                    if link["href"].startswith("#") and len(link["href"]) > 1:
                        self.assertIn(link["href"][1:], ids)
                figures = doc.find_all("figure", id=fid)
                self.assertEqual(len(figures), 1)
                figure = figures[0]
                self.assertIn("non générée par IA", figure.get("data-image-status", ""))
                img = figure.find("img")
                self.assertIsNotNone(img)
                self.assertEqual(img.get("src"), source)
                self.assertTrue(img.get("alt", "").strip())
                self.assertEqual(img.get("loading"), "lazy")
                self.assertEqual(len(doc.find_all("img", src=source)), 1)
                self.assertTrue((ROOT / source.lstrip("/")).is_file())
                caption = figure.find("figcaption")
                self.assertIsNotNone(caption)
                self.assertIn(accession, caption.get_text(" ", strip=True))
                self.assertIn("non générée par IA", caption.get_text(" ", strip=True))
                self.assertIn("non", caption.get_text(" ", strip=True).lower())
                record = records[object_id]
                self.assertEqual(source, "/" + record["path"])
                self.assertTrue(record["is_public_domain"])
                self.assertEqual(record["license"], "CC0-1.0")
                self.assertIsNotNone(caption.find("a", href=record["source_url"]))
                heading = doc.find("h2", id=section)
                self.assertIsNotNone(heading)
                in_section = False
                for sibling in heading.next_siblings:
                    if getattr(sibling, "name", None) == "h2":
                        break
                    if sibling is figure:
                        in_section = True
                self.assertTrue(in_section, "La figure doit rester dans son passage antique")


if __name__ == "__main__":
    unittest.main()
