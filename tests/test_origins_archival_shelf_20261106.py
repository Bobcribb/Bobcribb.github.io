"""Neuf manuscrits ODS historiques : visibilité, intégrité, retour et unicité."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from origins_archive_navigation import ARCHIVES, PORTAL, archive_shelf


class OriginsArchivalShelfTests(unittest.TestCase):
    def test_sources_existent_et_sont_documentees(self):
        self.assertEqual(len(ARCHIVES), 9)
        self.assertEqual(len({row[0] for row in ARCHIVES}), 9)
        for code, volume, chapters, title, slug in ARCHIVES:
            source = ROOT / "corpus" / "origines-du-sacre" / (slug + ".md")
            reader = source.with_suffix(".html")
            self.assertTrue(source.is_file(), code)
            self.assertTrue(reader.is_file(), code)
            self.assertGreater(len(source.read_text(encoding="utf-8")), 30000, code)
            self.assertGreater(len(reader.read_text(encoding="utf-8")), 30000, code)
            self.assertTrue(title and chapters and volume)

    def test_cartes_et_renvois_sans_alteration_du_texte(self):
        with TemporaryDirectory() as temp:
            out = Path(temp) / "_site"
            src = Path(temp) / "src"
            originals = {}
            for code, volume, chapters, title, slug in ARCHIVES:
                rel = Path("corpus/origines-du-sacre")
                page = out / rel / (slug + ".html")
                manuscript = src / rel / (slug + ".md")
                page.parent.mkdir(parents=True, exist_ok=True)
                manuscript.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<html><body><header class="mythos-masthead">MYTHOS</header>'
                    '<main><article><h1>' + title + '</h1><p>Texte scientifique conservé.</p>'
                    '<p>Sources primaires et bibliographie.</p></article></main></body></html>'
                    + ("<!-- document intact -->" * 1600), encoding="utf-8")
                manuscript.write_text(
                    "# " + title + "\n\n" + ("Sources primaires et bibliographie. " * 1000),
                    encoding="utf-8"
                )
                originals[slug] = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser").main.get_text(" ", strip=True)
            for _ in range(2):
                fragment = BeautifulSoup(archive_shelf(out, src), "html.parser")
                links = fragment.select(".origins-archival-card[href]")
                self.assertEqual(len(links), 9)
                self.assertEqual(len({link["href"] for link in links}), 9)
                self.assertEqual(len(fragment.select("h2#origines-archives-titre")), 1)
                for _, _, _, _, slug in ARCHIVES:
                    page = BeautifulSoup(
                        (out / "corpus" / "origines-du-sacre" / (slug + ".html"))
                        .read_text(encoding="utf-8"), "html.parser")
                    self.assertEqual(page.main.get_text(" ", strip=True), originals[slug])
                    navs = page.select("nav[data-mythos-archival-return]")
                    self.assertEqual(len(navs), 1)
                    self.assertEqual(navs[0].a["href"], PORTAL)

    def test_archive_absente_refusee(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "archive intégrale absente"):
                archive_shelf(Path(tmp) / "_site", Path(tmp))


if __name__ == "__main__":
    unittest.main()
