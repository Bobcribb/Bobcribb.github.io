"""Hésiode / Kumarbi : conservation, classement, liens réciproques et mobile."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_corpus import RELATED
from build_greek_folders import BASE, COSMIC_STUDIES, build, classify, verify


class GreekCosmicGenealogyTests(unittest.TestCase):
    def test_public_integral_sources_and_one_primary_folder(self):
        urls = [url for url, _, _ in COSMIC_STUDIES]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(len(urls), 3)
        related_urls = [url for _, url in RELATED]
        self.assertNotIn('/livre-hesiode/', related_urls)  # Déjà dans BOOKS.
        expected = ('cosmogonies', 'sources-anciennes', 'interpretations-philosophiques')
        for i, (url, title, context) in enumerate(COSMIC_STUDIES):
            source = ROOT / url.lstrip('/') / 'index.html'
            self.assertTrue(source.is_file(), url)
            html = source.read_text(encoding='utf-8')
            self.assertGreater(len(html), 17000, url)
            article = BeautifulSoup(html, 'html.parser').select_one('article.content')
            self.assertIsNotNone(article, url)
            self.assertGreater(len(article.get_text(' ', strip=True)), 2000, url)
            self.assertRegex(html.lower(), 'sources|bibliograph|références', url)
            self.assertEqual(classify(url, title, 'Lecture associée')[0], expected[i])
            self.assertTrue(title and context)
            if i:
                self.assertEqual(related_urls.count(url), 1, url)

    def test_reciprocal_links_and_integrity_after_two_builds(self):
        urls = {url for url, _, _ in COSMIC_STUDIES}
        with TemporaryDirectory() as temp:
            out = Path(temp)
            originals = {}
            for url, title, _ in COSMIC_STUDIES:
                page = out / url.lstrip('/') / 'index.html'
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text(
                    '<!doctype html><html lang="fr"><head><title>Étude</title></head>'
                    '<body><main><article class="content"><h1>' + title +
                    '</h1><p>Le texte intégral, sources et bibliographie.</p>'
                    '</article></main></body></html>', encoding='utf-8')
                originals[url] = str(BeautifulSoup(
                    page.read_text(encoding='utf-8'), 'html.parser').article)
            groups = [('Études intégrales', 'grec-liens',
                       [(url, title) for url, title, _ in COSMIC_STUDIES])]
            for _ in range(2):
                rows = build(out, groups, [], [])
                self.assertEqual({row['url'] for row in rows}, urls)
                verify(out, urls)
                for url in urls:
                    doc = BeautifulSoup(
                        (out / url.lstrip('/') / 'index.html')
                        .read_text(encoding='utf-8'), 'html.parser')
                    self.assertEqual(str(doc.article), originals[url], url)
                    self.assertEqual(len(doc.select('nav[data-greek-folder-nav]')), 1)
                    panels = doc.select('aside[data-greek-cross-readings="souverainete-cosmique"]')
                    self.assertEqual(len(panels), 1, url)
                    self.assertFalse(doc.article.select('[data-greek-cross-readings]'))
                    links = [a['href'] for a in panels[0].select('a[href]')]
                    self.assertEqual(set(links), urls - {url})
                    self.assertEqual(len(links), 2)
                    href = doc.select_one('a.greek-folder-return-topic')['href']
                    path, anchor = href.split('#', 1)
                    folder = BeautifulSoup(
                        (out / path.lstrip('/') / 'index.html').read_text(encoding='utf-8'),
                        'html.parser')
                    self.assertIsNotNone(folder.find(id=anchor))
        css = (ROOT / 'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('data-greek-cross-readings="souverainete-cosmique"', css)
        self.assertIn('border-inline-start:3px solid #d8b67a', css)
        self.assertIn('@media(max-width:480px)', css)


if __name__ == '__main__':
    unittest.main()
