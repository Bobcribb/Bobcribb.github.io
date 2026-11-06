"""Régression : neuf éditions critiques et leurs liens réciproques, sans altérer les textes."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from theatre_fragment_index import SLUGS, verified_editions, install


class TheatreArchivesNavigationTests(unittest.TestCase):
    def test_nine_real_sources_are_long_form_and_documented(self):
        self.assertEqual(len(SLUGS), 9)
        self.assertEqual(len(set(SLUGS)), 9)
        base = ROOT / "corpus/theatre-grec/comedies"
        for slug in SLUGS:
            source = (base / (slug + "-source.md")).read_text(encoding="utf-8")
            study = (base / (slug + "-etude.html")).read_text(encoding="utf-8")
            scenes = (base / (slug + "-scenes-modernes.html")).read_text(encoding="utf-8")
            self.assertGreater(len(source), 8000, slug)
            self.assertGreater(len(study), 10000, slug)
            self.assertGreater(len(scenes), 5000, slug)
            self.assertIn("bibliograph", source.lower(), slug)
            self.assertIn("bibliograph", study.lower(), slug)
        css = ROOT / "assets/mythos-theatre-archive.css"
        self.assertTrue(css.is_file())
        self.assertIn("@media (max-width:620px)", css.read_text(encoding="utf-8"))

    def test_portal_and_eighteen_readers_are_reciprocal_and_idempotent(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "source"
            out = Path(tmp) / "_site"
            base = Path("corpus/theatre-grec/comedies")
            (root / base).mkdir(parents=True)
            (out / base).mkdir(parents=True)
            (out / "theatre").mkdir(parents=True)
            portal = (
                "<!doctype html><html><head><title>Théâtre</title></head><body>"
                '<main><article class="content"><section class="portal-section">'
                "<h2>Choisir sa lecture</h2><div class=\"portal-grid\"></div></section>"
                '<section class="portal-section" id="pieces-perdues">'
                "<h2>Pièces perdues</h2></section></article></main></body></html>"
            )
            (out / "theatre/index.html").write_text(portal, encoding="utf-8")
            original = {}
            for slug in SLUGS:
                (root / base / (slug + "-source.md")).write_text(
                    "# MYTHOS — volume XXV\n\n## Aristophane : " + slug +
                    "\n\nSources et bibliographie.\n" + "Analyse universitaire. " * 500,
                    encoding="utf-8",
                )
                for kind, suffix in (("critique", "-etude.html"), ("scenes", "-scenes-modernes.html")):
                    # Lemniai a historiquement un article sans balise main.
                    container = 'article class="dai-article"' if slug == "lemniai" else "main"
                    endtag = "article" if slug == "lemniai" else "main"
                    paragraph = ("Sources et bibliographie. " if kind == "critique" else
                                 "Scènes modernes non attestées. ")
                    body = "<p>" + paragraph * 480 + "</p>"
                    html = (
                        '<!doctype html><html><head><title>MYTHOS</title></head><body>'
                        '<header class="mythos-masthead">Navigation</header>'
                        "<" + container + ">" + body + "</" + endtag + ">"
                        "</body></html>"
                    )
                    page = out / base / (slug + suffix)
                    page.write_text(html, encoding="utf-8")
                    original[(slug, kind)] = BeautifulSoup(
                        html, "html.parser"
                    ).select_one("main,article.dai-article").get_text(" ", strip=True)
            self.assertEqual(len(verified_editions(root, out)), 9)
            for _ in range(2):
                self.assertEqual(install(root, out), 9)
                page = BeautifulSoup(
                    (out / "theatre/index.html").read_text(encoding="utf-8"),
                    "html.parser",
                )
                self.assertEqual(len(page.select("#theatre-comedies-editions")), 1)
                self.assertEqual(len(page.select(".mythos-theatre-edition")), 9)
                self.assertEqual(len(page.select(".mythos-theatre-archive-figure img")), 1)
                self.assertEqual(len(page.select(".mythos-theatre-edition-source a[href$='-source.md']")), 9)
                for slug in SLUGS:
                    for kind, suffix in (("critique", "-etude.html"), ("scenes", "-scenes-modernes.html")):
                        reader = BeautifulSoup(
                            (out / base / (slug + suffix)).read_text(encoding="utf-8"),
                            "html.parser",
                        )
                        self.assertEqual(
                            reader.select_one("main,article.dai-article").get_text(" ", strip=True),
                            original[(slug, kind)],
                        )
                        self.assertEqual(
                            len(reader.select("[data-mythos-theatre-archive-nav]")), 1
                        )
                        links = [a["href"] for a in reader.select(
                            "[data-mythos-theatre-archive-nav] a")]
                        self.assertIn("/theatre/#theatre-source-" + slug, links)
                        self.assertIn("/corpus/theatre-grec/comedies/" + slug + "-source.md", links)
                        self.assertEqual(len(links), 3)
                        self.assertEqual(len(reader.select(
                            'link[href="/assets/mythos-theatre-archive.css"]')), 1)


if __name__ == "__main__":
    unittest.main()
