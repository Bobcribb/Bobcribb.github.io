"""Neuf manuscrits sources grecs : lecteurs HTML intégraux et sources inchangées."""
import hashlib
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from theatre_fragment_index import SLUGS, verified_editions
from theatre_source_readers import BASE, build_readers


class TheatreSourceReadersTests(unittest.TestCase):
    def test_all_nine_original_sources_have_idempotent_integral_html_readers(self):
        records = verified_editions(ROOT, ROOT)
        self.assertEqual(len(records), len(SLUGS))
        with TemporaryDirectory() as tmp:
            output = Path(tmp) / "_site"
            for _ in range(2):
                self.assertEqual(build_readers(ROOT, output, records), 9)
                for item in records:
                    slug = item["slug"]
                    raw = ROOT / BASE / (slug + "-source.md")
                    copy = output / BASE / (slug + "-source.md")
                    rendered = output / BASE / (slug + "-source.html")
                    self.assertEqual(raw.read_bytes(), copy.read_bytes(), slug)
                    self.assertTrue(rendered.is_file(), slug)
                    doc = BeautifulSoup(rendered.read_text(encoding="utf-8"), "html.parser")
                    self.assertEqual(doc.html.get("lang"), "fr")
                    self.assertIsNotNone(doc.select_one("meta[name='viewport']"))
                    self.assertEqual(len(doc.select("article#texte-source")), 1)
                    self.assertEqual(len(doc.select(".theatre-original-toc")), 1)
                    self.assertGreaterEqual(len(doc.select(".theatre-original-toc li a")), 2)
                    self.assertTrue(all(
                        doc.select_one(anchor["href"]) if False else
                        doc.find(id=anchor["href"][1:]) is not None
                        for anchor in doc.select(".theatre-original-toc a[href^='#']")
                    ))
                    self.assertIn("bibliograph", doc.select_one("article").get_text(" ", strip=True).lower())
                    self.assertGreater(len(doc.select_one("article").get_text(" ", strip=True)), 6500)
                    self.assertIn(hashlib.sha256(raw.read_bytes()).hexdigest(), doc.get_text())
                    links = {a.get("href") for a in doc.select(".theatre-original-nav a")}
                    self.assertIn(item["critique"], links)
                    self.assertIn(item["scenes"], links)
                    self.assertIn("/corpus/theatre-grec/comedies/" + slug + "-source.md", links)
                    self.assertIn("/theatre/#theatre-source-" + slug, links)
                    self.assertIsNotNone(doc.select_one('link[href="/assets/mythos-theatre-archive.css"]'))
                    self.assertIsNotNone(doc.select_one('link[rel="canonical"]'))
                before = {
                    item["slug"]: (output / BASE / (item["slug"] + "-source.html")).read_bytes()
                    for item in records
                }
                # A repeated rebuild should not accumulate HTML, notes or links.
                self.assertEqual(build_readers(ROOT, output, records), 9)
                self.assertEqual(before, {
                    item["slug"]: (output / BASE / (item["slug"] + "-source.html")).read_bytes()
                    for item in records
                })

    def test_existing_public_source_is_not_overwritten(self):
        records = verified_editions(ROOT, ROOT)
        with TemporaryDirectory() as tmp:
            output = Path(tmp) / "_site"
            original = output / BASE / (records[0]["slug"] + "-source.md")
            original.parent.mkdir(parents=True, exist_ok=True)
            original.write_text("# Document différent, potentiellement plus récent", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "manuscrit public divergent"):
                build_readers(ROOT, output, records)
            self.assertEqual(original.read_text(), "# Document différent, potentiellement plus récent")
            self.assertFalse((output / BASE / (records[0]["slug"] + "-source.html")).exists())

    def test_missing_source_fails_without_creating_partial_html(self):
        records = verified_editions(ROOT, ROOT)
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            output = Path(tmp) / "_site"
            for item in records[:1]:
                path = root / BASE / (item["slug"] + "-source.md")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / BASE / (item["slug"] + "-source.md")).read_bytes())
            with self.assertRaises(FileNotFoundError):
                build_readers(root, output, records)
            self.assertFalse(list(output.rglob("*-source.html")))


if __name__ == "__main__":
    unittest.main()
