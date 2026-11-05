"""Études publiques de Civilisations : classement grec, intégralité et renvois."""
from pathlib import Path
import sys
import unittest
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_corpus import RELATED
from build_greek_folders import (
    ANATOLIA_THRACE_STUDIES, build, classify, verify,
)


class GreekAnatoliaThraceReferencesTests(unittest.TestCase):
    def test_verified_public_sources_are_integral_and_newly_referenced(self):
        urls = [url for url, _, _ in ANATOLIA_THRACE_STUDIES]
        self.assertEqual(len(urls), 4)
        self.assertEqual(len(urls), len(set(urls)))
        catalogue = [url for _, url in RELATED]
        for url in urls:
            self.assertEqual(catalogue.count(url), 1, url)
            source = ROOT / url.lstrip('/') / 'index.html'
            self.assertTrue(source.is_file(), url)
            html = source.read_text(encoding='utf-8')
            doc = BeautifulSoup(html, 'html.parser')
            article = doc.select_one('article.content')
            self.assertIsNotNone(article, url)
            self.assertGreater(len(html), 12000, url)
            self.assertGreater(len(article.get_text(' ', strip=True)), 2000, url)
            self.assertRegex(html.lower(), 'sources|bibliograph|références')
        expected = {
            'civilisations-lydie-sardes-cresus': 'sources-anciennes',
            'civilisations-phrygie-midas-gordion': 'cultes-sanctuaires',
            'civilisations-thraces-odryses-kazanlak': 'cultes-sanctuaires',
            'civilisations-empire-seleucide-antiochos': 'sources-anciennes',
        }
        for url, title, _ in ANATOLIA_THRACE_STUDIES:
            family, subsection = classify(url, title, 'Lecture associée')
            self.assertEqual(family, expected[url.strip('/').split('/')[-1]])
            self.assertTrue(subsection.strip())

    def test_crosslinks_are_bidirectional_idempotent_and_outside_articles(self):
        urls = {url for url, _, _ in ANATOLIA_THRACE_STUDIES}
        with TemporaryDirectory() as temporary:
            out = Path(temporary)
            originals = {}
            for url, title, _ in ANATOLIA_THRACE_STUDIES:
                page = out / url.lstrip('/') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<!doctype html><html lang="fr"><head><title>Étude</title></head>'
                    '<body><main><article class="content"><h1>' + title + '</h1>'
                    '<p>Le manuscrit complet reste ici : Hérodote, histoire et chronologie.</p>'
                    '<section id="sources"><h2>Sources et bibliographie</h2>'
                    '<p>Références conservées sans troncature.</p></section>'
                    '</article></main></body></html>', encoding='utf-8'
                )
                originals[url] = str(BeautifulSoup(
                    page.read_text(encoding='utf-8'), 'html.parser').article)
            groups = [('Études accessibles', 'grec-liens',
                       [(url, title) for url, title, _ in ANATOLIA_THRACE_STUDIES])]
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({r['url'] for r in rows}, urls)
                verify(out, urls)
                for url in urls:
                    page = out / url.lstrip('/') / 'index.html'
                    doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), originals[url], url)
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    panels = doc.select('aside[data-greek-cross-readings="frontieres"]')
                    self.assertEqual(len(panels), 1, url)
                    links = [a['href'] for a in panels[0].select('a[href]')]
                    self.assertEqual(set(links), urls - {url})
                    self.assertEqual(len(links), 3)
                    self.assertEqual(len(set(links)), 3)
                    self.assertFalse(doc.article.select('[data-greek-cross-readings]'))
                    self.assertTrue(doc.select_one('nav a.greek-folder-return-topic'))
        css = (ROOT / 'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('data-greek-cross-readings="frontieres"', css)
        self.assertIn('@media(max-width:480px)', css)


if __name__ == '__main__':
    unittest.main()
