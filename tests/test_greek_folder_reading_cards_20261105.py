"""Direct reading links on the eight illustrated dossier cards."""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_folders import BASE, CSS, build, verify


class ReadingCardsTests(unittest.TestCase):
    def test_shortcuts_keep_canonical_sources_and_original_articles(self):
        book = ("/livre-hesiode/", "Hésiode — Théogonie")
        studies = [
            ("/chapitres/encyclopedie/chapitre-375-nyx-nouvelle-etude/", "Nyx — sources"),
            ("/chapitres/encyclopedie/chapitre-376-gaia-ouranos-cronos-nouvelle-etude/", "Gaia"),
            ("/chapitres/encyclopedie/chapitre-378-typhon-nouvelle-etude/", "Typhon"),
        ]
        groups = [("Livres", "grec-livres", [book]),
                  ("Études", "grec-universitaire", studies)]
        originals = {}
        urls = {u for u, _ in [book, *studies]}
        with TemporaryDirectory() as d:
            out = Path(d)
            for url, title in [book, *studies]:
                p = out / url.lstrip("/") / "index.html"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("<html><head><title>Étude</title></head><body><main>"
                             "<article><h1>" + title + "</h1><h2>Bibliographie</h2>"
                             "<p>Texte universitaire intégral.</p></article></main></body></html>",
                             encoding="utf-8")
                originals[url] = str(BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser").article)
            for _ in range(2):
                rows = build(out, groups, [], [])
                verify(out, urls)
                self.assertEqual({r["url"] for r in rows}, urls)
                index = BeautifulSoup((out / BASE.strip("/") / "index.html").read_text(encoding="utf-8"), "html.parser")
                card = index.select_one(".greek-folder-entry")
                self.assertEqual(card.select_one("a.greek-folder-link")["href"], BASE + "cosmogonies/")
                self.assertIsNone(card.select_one("a.greek-folder-link a"))
                preview = card.select_one("nav.greek-folder-reading-preview")
                self.assertIn("Lectures directes", preview["aria-label"])
                direct = [a["href"] for a in preview.select("a[data-greek-feature]")]
                self.assertEqual(len(direct), 3)
                self.assertEqual(len(set(direct)), 3)
                self.assertIn(book[0], direct)
                self.assertIn(studies[0][0], direct)
                family = BeautifulSoup((out / BASE.strip("/") / "cosmogonies" / "index.html").read_text(encoding="utf-8"), "html.parser")
                self.assertCountEqual([a["href"] for a in family.select("a[data-greek-entry]")], urls)
                for url, _ in [book, *studies]:
                    p = out / url.lstrip("/") / "index.html"
                    self.assertEqual(str(BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser").article), originals[url])

    def test_gold_mobile_keyboard_styles(self):
        self.assertIn(".greek-folder-reading-preview", CSS)
        self.assertIn("min-height:44px", CSS)
        self.assertIn("a:focus-visible", CSS)
        self.assertIn("@media(max-width:400px)", CSS)


if __name__ == "__main__":
    unittest.main()
