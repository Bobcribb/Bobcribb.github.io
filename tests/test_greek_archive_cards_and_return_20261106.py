"""Archives grecques : iconographie documentée, retours et conservation."""
import sys
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import decorate_greek_archive_cards, add_greek_archive_return


class TestGreekArchiveCardsAndNavigation(unittest.TestCase):
    urls = (
        '/corpus/mythologie-grecque/archives/livre-heracles.html',
        '/corpus/mythologie-grecque/archives/livre-troie.html',
        '/corpus/mythologie-grecque/archives/livre-odyssee.html',
    )
    media = (
        'mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg',
        'mythos-iliade-achille-ajax-athena-hydrie-met-56-171-29.jpg',
        'mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg',
    )

    def setup_site(self, root):
        originals = {}
        for idx, url in enumerate(self.urls):
            path = root / url.lstrip('/')
            path.parent.mkdir(parents=True, exist_ok=True)
            data = ('<html><head><title>Archive</title></head><body>'
                    '<h1>Texte scientifique intégral</h1>'
                    '<p>Analyse et apparat des sources antiques %d</p>'
                    '<h2>Bibliographie critique</h2></body></html>' % idx).encode('utf-8')
            path.write_bytes(data)
            originals[url] = data
        for media in self.media:
            path = root / 'media/2026/10' / media
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'original photographic archive')
        return originals

    def page(self):
        anchors = ''.join(
            '<li><a href="%s">%s</a></li>' % (url, name)
            for url, name in zip(self.urls, ('Héraclès', 'Troie', "L'Odyssée")))
        anchors += '<li><a href="/autre-archive/">Autre archive</a></li>'
        return BeautifulSoup(
            '<html><body><section id="grec-archives">'
            '<h3>Archives historiques conservées</h3>'
            '<ol class="greek-corpus-links">' + anchors +
            '</ol></section></body></html>', 'html.parser')

    def test_three_illustrated_cards_keep_original_links_and_scholarly_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            originals = self.setup_site(root)
            doc = self.page()
            before = [a['href'] for a in doc.select('#grec-archives ol > li > a')]
            self.assertEqual(decorate_greek_archive_cards(doc, root), 3)
            self.assertEqual(decorate_greek_archive_cards(doc, root), 3)
            after = [a['href'] for a in doc.select('#grec-archives ol > li > a')]
            self.assertEqual(before, after)
            self.assertEqual(len(after), 4)
            self.assertEqual(len(doc.select('#grec-archives img.mythos-greek-archive-image')), 3)
            self.assertEqual(len(doc.select('#grec-archives p.mythos-greek-archive-credit')), 3)
            self.assertEqual(len(doc.select('#grec-archives p.mythos-greek-archive-credit a')), 6)
            self.assertEqual(len(doc.select('#grec-archives li > a a')), 0)
            self.assertEqual(doc.select('#grec-archives ol > li > a')[-1].get_text(strip=True),
                             'Autre archive')
            for url, original in originals.items():
                self.assertEqual((root / url.lstrip('/')).read_bytes(), original)

    def test_all_four_greek_entry_points_keep_identical_archive_credits(self):
        """La passe muséale n'ajoute pas six liens au seul portail canonique."""
        from apply_museum_design import apply as apply_museum_design

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.setup_site(root)
            names = (
                'mythologie-grecque/index.html',
                'mythologie-grecque.html',
                'grande-encyclopedie/index.html',
                'grande-encyclopedie.html',
            )
            links = ''.join(
                '<li><a href="' + url + '">Archive grecque</a></li>'
                for url in self.urls
            )
            fixture = (
                '<html lang="fr"><head><title>Corpus grec | MYTHOS</title></head>'
                '<body><main><article class="content"><h1>Corpus grec</h1>'
                '<section id="greek-unified-corpus"><h2>Catalogue intégral</h2>'
                '<section id="grec-archives"><h3>Archives</h3>'
                '<ol class="greek-corpus-links">' + links + '</ol></section>'
                '</section><p id="original">Texte universitaire inchangé.</p>'
                '</article></main></body></html>'
            )
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(fixture, encoding='utf-8')

            for _ in range(2):
                apply_museum_design(root)
                all_links = []
                for name in names:
                    doc = BeautifulSoup(
                        (root / name).read_text(encoding='utf-8'),
                        'html.parser',
                    )
                    block = doc.select_one('#greek-unified-corpus')
                    self.assertIsNotNone(block, name)
                    all_links.append([
                        a['href'] for a in block.select('a[href]')
                    ])
                    self.assertEqual(len(block.select('img.mythos-greek-archive-image')), 3, name)
                    self.assertEqual(len(block.select('p.mythos-greek-archive-credit a')), 6, name)
                    self.assertEqual(
                        doc.select_one('#original').get_text(' ', strip=True),
                        'Texte universitaire inchangé.',
                    )
                self.assertTrue(
                    all(urls == all_links[0] for urls in all_links),
                    'Les quatre sommaires grecs ont des liens différents',
                )

    def test_without_assets_no_false_illustration_or_backlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = self.page()
            self.assertEqual(decorate_greek_archive_cards(doc, root), 0)
            self.assertEqual(len(doc.select('#grec-archives ol > li > a')), 4)
            reader = BeautifulSoup('<html><body><section class="mythos-banner"></section>'
                                   '<article><p>Source inchangée.</p></article></body></html>',
                                   'html.parser')
            self.assertEqual(add_greek_archive_return(reader, root), 0)
            self.assertEqual(len(reader.select('nav.mythos-greek-archive-return')), 0)

    def test_reader_has_a_single_accessible_reciprocal_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'mythologie-grecque/index.html'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('<section id="grec-archives"></section>', encoding='utf-8')
            reader = BeautifulSoup(
                '<html><body><section class="mythos-banner"></section>'
                '<main><article><p>Texte universitaire inchangé.</p>'
                '<h2>Sources et bibliographie</h2></article></main></body></html>',
                'html.parser')
            original_text = reader.article.get_text(' ', strip=True)
            self.assertEqual(add_greek_archive_return(reader, root), 1)
            self.assertEqual(add_greek_archive_return(reader, root), 1)
            links = reader.select('nav.mythos-greek-archive-return a')
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0]['href'], '/mythologie-grecque/#grec-archives')
            self.assertEqual(reader.article.get_text(' ', strip=True), original_text)


if __name__ == '__main__':
    unittest.main()
