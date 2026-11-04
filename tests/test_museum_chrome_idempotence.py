"""MYTHOS — prevent repeated editorial class names during successive museum builds.

The same public HTML can be read, restyled, and written many times. It must
retain source prose and links while keeping presentation classes unique.
"""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply


class MuseumChromeIdempotenceTests(unittest.TestCase):
    def test_eyebrow_classes_are_unique_after_three_builds(self):
        with TemporaryDirectory() as workdir:
            page = Path(workdir) / "religion" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<!DOCTYPE html><html lang="fr"><head><title>Religion | MYTHOS</title></head>'
                '<body><main class="layout"><article class="content">'
                '<h1>Polythéisme grec</h1>'
                '<div class="eyebrow mythos-chrome-label mythos-chrome-label mythos-chrome-label">'
                'BIBLIOTHÈQUE · MYTHOS</div>'
                '<p id="source">Texte original : ἱερόν, ἔθος et bibliographie.</p>'
                '<p><a href="https://example.org/edition">Édition scientifique</a></p>'
                '</article></main></body></html>',
                encoding="utf-8",
            )
            for _ in range(3):
                self.assertEqual(apply(workdir), 1)
                document = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                eyebrow = document.select_one("article.content > .eyebrow")
                self.assertIsNotNone(eyebrow)
                classes = eyebrow.get("class", [])
                self.assertEqual(len(classes), len(set(classes)))
                self.assertEqual(classes.count("mythos-chrome-label"), 1)
                self.assertEqual(eyebrow.get_text(" ", strip=True), "BIBLIOTHÈQUE · MYTHOS")
                self.assertEqual(document.select_one("#source").get_text(" ", strip=True),
                                 "Texte original : ἱερόν, ἔθος et bibliographie.")
                self.assertIsNotNone(document.select_one(
                    'a[href="https://example.org/edition"]'))
                self.assertEqual(len(document.select("header.mythos-masthead")), 1)


if __name__ == "__main__":
    unittest.main()
