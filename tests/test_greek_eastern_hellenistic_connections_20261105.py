"""Two verified unabridged studies enter the Greek catalogue without copying."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_corpus import RELATED
from build_greek_folders import EASTERN_CONTACT_STUDIES, BASE, classify, build, verify


class EasternContactStudiesTests(unittest.TestCase):
    def test_sources_remain_integral_and_have_one_thematic_home(self):
        urls = [url for url, _, _ in EASTERN_CONTACT_STUDIES]
        self.assertEqual(len(urls), 3)
        self.assertEqual(len(set(urls)), 3)
        existing = [url for _, url in RELATED]
        prefixes = {
            'civilisations-royaumes-greco-bactriens-indo-grecs': 'Royaumes gréco-bactriens',
            'civilisations-empire-kouchan-gandhara': 'Bactriane et Gandhara',
            'civilisations-palmyre-zenobie': 'Palmyre',
        }
        for url, title, note in EASTERN_CONTACT_STUDIES:
            self.assertEqual(existing.count(url), 1, url)
            html = (ROOT / url.strip('/') / 'index.html').read_text(encoding='utf-8')
            self.assertGreater(len(html), 13000, url)
            doc = BeautifulSoup(html, 'html.parser')
            article = doc.select_one('article.content')
            self.assertIsNotNone(article, url)
            self.assertGreater(len(article.get_text(' ', strip=True)), 4500, url)
            self.assertRegex(article.get_text(' ', strip=True).lower(), 'sources|bibliograph|références', url)
            family, subsection = classify(url, 'Athéna citée incidemment', 'Lecture associée')
            self.assertEqual(family, 'sources-anciennes', url)
            self.assertTrue(subsection.startswith(prefixes[url.strip('/').split('/')[-1]]), url)
            self.assertTrue(title and note)

    def test_reciprocal_six_links_and_no_manuscript_mutation_after_two_builds(self):
        urls = {url for url, _, _ in EASTERN_CONTACT_STUDIES}
        with TemporaryDirectory() as t:
            out = Path(t)
            initial = {}
            for url, title, _ in EASTERN_CONTACT_STUDIES:
                page = out / url.lstrip('/') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<!doctype html><html lang="fr"><head><title>Étude complète</title></head>'
                    '<body><main><article class="content"><h1>' + title + '</h1>'
                    '<h2 id="bibliographie">Sources et bibliographie</h2>'
                    '<p>Manuscrit universitaire complet, conservé sans troncature.</p>'
                    '</article></main></body></html>', encoding='utf-8')
                initial[url] = str(BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser').article)
            groups = [('Études vérifiées', 'grec-liens', [(u, title)
                       for u, title, _ in EASTERN_CONTACT_STUDIES])]
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({r['url'] for r in rows}, urls)
                verify(out, urls)
                for url in urls:
                    doc = BeautifulSoup((out / url.lstrip('/') / 'index.html')
                                        .read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), initial[url], url)
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    panel = doc.select('aside[data-greek-cross-readings="orient-hellenistique"]')
                    self.assertEqual(len(panel), 1, url)
                    self.assertFalse(doc.article.select('[data-greek-cross-readings]'))
                    links = [a['href'] for a in panel[0].select('a[href]')]
                    self.assertEqual(set(links), urls - {url})
                    self.assertEqual(len(links), 2)
                    back = doc.select_one('a.greek-folder-return-topic')
                    base, anchor = back['href'].split('#', 1)
                    folder = BeautifulSoup((out / base.lstrip('/') / 'index.html')
                                           .read_text(encoding='utf-8'), 'html.parser')
                    section = folder.find(id=anchor)
                    self.assertIsNotNone(section)
                    self.assertIsNotNone(section.find('a', href=url))
        css = (ROOT / 'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('data-greek-cross-readings="orient-hellenistique"', css)
        self.assertIn('border-inline-start:3px solid #d8b67a', css)


if __name__ == '__main__':
    unittest.main()
