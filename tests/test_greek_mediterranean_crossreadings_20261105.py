"""Sources de la Méditerranée ancienne : intégralité et navigation réciproque."""
from pathlib import Path
import sys
import unittest
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_corpus import RELATED
from build_greek_folders import BASE, MEDITERRANEAN_STUDIES, build, classify, verify


class MediterraneanCrossReadingTests(unittest.TestCase):
    def test_integral_sources_and_primary_dossiers(self):
        urls = [url for url, _, _ in MEDITERRANEAN_STUDIES]
        self.assertEqual(len(urls), 4)
        self.assertEqual(len(set(urls)), 4)
        catalogue_urls = [url for _, url in RELATED]
        expected = {
            "civilisations-histoire-levant-pheniciens":
                ("sources-anciennes", "Levant"),
            "civilisations-carthage-punique-histoire-religion":
                ("sources-anciennes", "Carthage"),
            "civilisations-tartessos-turunuelo":
                ("sources-anciennes", "Tartessos"),
            "mythos-mediterranee-ecritures-char-bronze-etrusques-tartessos-myceniens":
                ("interpretations-philosophiques", "Méditerranée"),
        }
        for url, title, context in MEDITERRANEAN_STUDIES:
            self.assertEqual(catalogue_urls.count(url), 1, url)
            path = ROOT / url.lstrip("/") / "index.html"
            self.assertTrue(path.is_file(), url)
            html = path.read_text(encoding="utf-8")
            doc = BeautifulSoup(html, "html.parser")
            article = doc.select_one("article.content")
            self.assertIsNotNone(article, url)
            self.assertGreater(len(html), 12500, url)
            self.assertGreater(len(article.get_text(" ", strip=True)), 3500, url)
            self.assertRegex(article.get_text(" ", strip=True).lower(),
                             "bibliograph|sources|références", url)
            slug = url.rstrip("/").split("/")[-1]
            family, subsection = classify(url, "Nom de divinité cité par hasard",
                                         "Lecture associée")
            self.assertEqual(family, expected[slug][0], url)
            self.assertTrue(subsection.startswith(expected[slug][1]), url)
            self.assertTrue(title and context)

    def test_twelve_directed_links_after_two_rebuilds(self):
        urls = {url for url, _, _ in MEDITERRANEAN_STUDIES}
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            original_articles = {}
            for url, title, _ in MEDITERRANEAN_STUDIES:
                path = out / url.lstrip("/") / "index.html"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    '<!doctype html><html lang="fr"><head><title>Source</title></head>'
                    '<body><main><article class="content"><h1>' + title +
                    '</h1><p id="texte">Texte universitaire original complet, '
                    'documentations, références anciennes et bibliographie.</p>'
                    '</article></main></body></html>',
                    encoding="utf-8"
                )
                original_articles[url] = str(BeautifulSoup(
                    path.read_text(encoding="utf-8"), "html.parser").article)
            groups = [("Circulations méditerranéennes", "grec-liens",
                       [(url, title) for url, title, _ in MEDITERRANEAN_STUDIES])]
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({row["url"] for row in rows}, urls)
                verify(out, urls)
                for url in urls:
                    path = out / url.lstrip("/") / "index.html"
                    doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
                    self.assertEqual(str(doc.article), original_articles[url], url)
                    self.assertEqual(len(doc.select("nav[data-greek-folder-nav]")), 1)
                    panels = doc.select('aside[data-greek-cross-readings="mediterranee"]')
                    self.assertEqual(len(panels), 1, url)
                    self.assertFalse(doc.article.select("[data-greek-cross-readings]"))
                    links = [a["href"] for a in panels[0].select("a[href]")]
                    self.assertEqual(set(links), urls - {url})
                    self.assertEqual(len(links), 3)
                    self.assertEqual(len(set(links)), 3)
                    back = doc.select_one("nav.greek-folder-breadcrumb a.greek-folder-return-topic")
                    self.assertIsNotNone(back)
                    folder_url, anchor = back["href"].split("#", 1)
                    folder = BeautifulSoup((out / folder_url.lstrip("/") /
                                            "index.html").read_text(encoding="utf-8"),
                                           "html.parser")
                    section = folder.find(id=anchor)
                    self.assertIsNotNone(section)
                    self.assertIsNotNone(section.find("a", href=url))
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertIn('data-greek-cross-readings="mediterranee"', css)
        self.assertIn("@media(max-width:480px)", css)
        self.assertIn("border-inline-start:3px solid #d8b67a", css)


if __name__ == "__main__":
    unittest.main()
