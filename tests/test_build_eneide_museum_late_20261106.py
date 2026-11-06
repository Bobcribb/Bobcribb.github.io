"""Régression de publication : les 18 lecteurs Énéide naissent après la passe muséale.

Seuls leurs fichiers HTML sont retraités ; les Markdown et les autres pages
restent octet pour octet identiques. Aucun numéro canonique n'est créé.
"""
import sys
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply
from eneide_readers import build_readers
from eneide_source_access import NAMES, SOURCE_DIR


class LateEneideMuseumTests(unittest.TestCase):
    def test_all_eighteen_late_readers_get_museum_chrome_without_source_loss(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            other = out / "temoin" / "index.html"
            other.parent.mkdir(parents=True)
            other.write_text(
                '<!doctype html><html lang="fr"><head><title>Autre page</title></head>'
                '<body><main><h1>Intouchable</h1></main></body></html>',
                encoding="utf-8",
            )
            original_other = other.read_bytes()
            sources = []
            titles = []
            for i, name in enumerate(NAMES):
                title = f"Énéide : source {i:02}"
                source = f"# {title}\n\nParagraphes documentaires pour le manuscrit {i}.\n\nBibliographie : Virgile.\n"
                target = out / SOURCE_DIR / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source, encoding="utf-8")
                sources.append((name, source))
                titles.append(title)
            self.assertEqual(build_readers(out, sources, titles, SOURCE_DIR), 18)
            paths = [SOURCE_DIR / (n.removesuffix(".md") + ".html") for n in NAMES]
            originals = {n: (out / SOURCE_DIR / n).read_bytes() for n in NAMES}
            self.assertEqual(apply(out, relative_paths=paths), 18)
            self.assertEqual(other.read_bytes(), original_other)
            for i, (name, _) in enumerate(sources):
                page = out / paths[i]
                doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(doc.body.get("data-mythos-design"), "20261104")
                self.assertEqual(len(doc.select("header.mythos-masthead")), 1)
                self.assertEqual(len(doc.select("section.mythos-banner")), 1)
                self.assertEqual(len(doc.select('link[href*="mythos-museum.css"]')), 1)
                self.assertEqual(len(doc.select(".mythos-primary-nav")), 1)
                self.assertIsNotNone(doc.select_one("#texte-integral"))
                self.assertIn(
                    f"Paragraphes documentaires pour le manuscrit {i}.",
                    doc.select_one("article.eneide-reader-text").get_text(" ", strip=True),
                )
                self.assertEqual((out / SOURCE_DIR / name).read_bytes(), originals[name])
                self.assertEqual(len(doc.select("a[href*='/mythologie-grecque/']")) >= 1, True)


if __name__ == "__main__":
    unittest.main()
