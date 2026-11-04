"""Check semantic heading hierarchy without losing scholarly content.

The museum banner owns the unique page H1. Full scholarly articles sometimes
contain an additional H1 from their Markdown source. Preserve its text, links,
id and place in the document while normalizing it to H2.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply


class MuseumHeadingHierarchyTests(unittest.TestCase):
    def test_scholarly_title_preserves_anchor_sources_and_text_after_two_builds(self):
        source = (
            '<html lang="fr"><head><title>MYTHOS — Phèmè</title></head><body>'
            '<main><article class="content">'
            '<h1 id="volume">Grande Encyclopédie — Étude 388</h1>'
            '<h1 id="pheme" class="manuscript-title"><em>PHÈMÈ</em> — parole publique</h1>'
            '<p id="introduction">Argument philologique intégral, non résumé.</p>'
            '<a href="#pheme">Revenir à l’étude</a>'
            '<h2 id="sources">Sources primaires</h2>'
            '<p>Hésiode, <em>Les Travaux et les Jours</em>, 763–764.</p>'
            '<h2 id="bibliographie">Bibliographie</h2>'
            '<p>Références critiques et éditions vérifiables.</p>'
            '</article></main></body></html>'
        )
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "chapitres/encyclopedie/chapitre-388-pheme/index.html"
            page.parent.mkdir(parents=True)
            page.write_text(source, encoding="utf-8")
            originals = BeautifulSoup(source, "html.parser")
            original_article_text = originals.select_one("article").get_text(" ", strip=True)
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                result = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(len(result.select("h1")), 1)
                self.assertEqual(len(result.select(".mythos-banner h1")), 1)
                self.assertEqual(len(result.select('article h2#pheme')), 1)
                self.assertEqual(result.select_one('article h2#pheme').get("class"), ["manuscript-title"])
                self.assertIsNotNone(result.select_one('article h2#pheme em'))
                self.assertEqual(result.select_one('article').get_text(" ", strip=True),
                                 original_article_text.replace("Grande Encyclopédie — Étude 388", "").strip())
                self.assertEqual(result.select_one('a[href="#pheme"]').get_text(strip=True),
                                 "Revenir à l’étude")
                self.assertEqual(len(result.select("article #sources")), 1)
                self.assertEqual(len(result.select("article #bibliographie")), 1)
                self.assertIn("Références critiques et éditions vérifiables.",
                              result.get_text(" ", strip=True))

    def test_preserves_portal_headings_and_skips_redirects(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "index.html"
            home.write_text(
                '<html><head><title>MYTHOS</title></head><body>'
                '<main><h1>MYTHOS</h1><section><h2>Collections</h2>'
                '<p>Accès aux volumes intégraux.</p></section></main>'
                '</body></html>', encoding="utf-8")
            redirect = root / "ancien/index.html"
            redirect.parent.mkdir()
            original = ('<html><head><meta http-equiv="refresh" content="0;url=/">'
                        '</head><body><h1>Ancien accès</h1></body></html>')
            redirect.write_text(original, encoding="utf-8")
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                result = BeautifulSoup(home.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(len(result.select("h1")), 1)
                self.assertEqual(len(result.select("main h2")), 1)
                self.assertEqual(redirect.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
