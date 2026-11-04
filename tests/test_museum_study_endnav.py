"""Navigation réciproque des études : intégrité, ancres et génération répétée."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_museum_design import apply


class EndOfStudyNavigationTests(unittest.TestCase):
    def test_all_collections_get_accessible_end_navigation_without_touching_text(self):
        routes = {
            'origines-du-sacre': '/origines-du-sacre/',
            'encyclopedie': '/mythologie-grecque/',
            'comedies': '/theatre/',
            'tragedies': '/theatre/',
            'comparatif': '/mythologie-comparee/',
            'philosophie': '/philosophie/',
            'grece': '/mythologie-grecque/',
        }
        markup = (
            '<html lang="fr"><head><title>Étude critique</title></head><body>'
            '<main class="layout"><article class="content">'
            '<h1 id="titre-scientifique">Rites et interprétations</h1>'
            '<p id="argument">Argument universitaire intégral : Ἀπόλλων et Ἄρτεμις.</p>'
            '<h2 id="sources">Sources primaires</h2>'
            '<p><a href="https://example.org/source">Texte antique attesté</a></p>'
            '<h2 id="biblio">Bibliographie critique</h2>'
            '<p id="reference">Bibliographie préservée et pagination.</p>'
            '</article></main></body></html>'
        )
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for collection in routes:
                page = root / 'chapitres' / collection / 'un-volume' / 'index.html'
                page.parent.mkdir(parents=True)
                page.write_text(markup, encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), len(routes))
                for collection, expected in routes.items():
                    page = root / 'chapitres' / collection / 'un-volume' / 'index.html'
                    doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                    article = doc.select_one('main article.content')
                    nav = doc.select('nav.mythos-study-endnav')
                    self.assertEqual(len(nav), 1, collection)
                    self.assertIs(nav[0].previous_sibling, article)
                    self.assertEqual([a['href'] for a in nav[0].select('a[href]')],
                        [expected, '/catalogue-integral/', '#titre-scientifique'])
                    self.assertEqual(len(doc.select('#titre-scientifique')), 1)
                    self.assertEqual(article.select_one('#argument').get_text(strip=True),
                        'Argument universitaire intégral : Ἀπόλλων et Ἄρτεμις.')
                    self.assertEqual(article.select_one('#reference').get_text(strip=True),
                        'Bibliographie préservée et pagination.')
                    self.assertEqual(len(article.select('a[href="https://example.org/source"]')), 1)
                    self.assertFalse(article.select('nav.mythos-study-endnav'))

    def test_portal_and_redirect_keep_their_original_navigation(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            portal = root / 'index.html'
            portal.write_text('<html><head><title>MYTHOS</title></head><body>'
                '<main><h1>MYTHOS</h1><p>Portail.</p></main></body></html>', encoding='utf-8')
            redirect = root / 'chapitres/tragedies/ancienne/index.html'
            redirect.parent.mkdir(parents=True)
            text = ('<html><head><meta http-equiv="refresh" content="0;url=/theatre/">'
                '</head><body>Redirection</body></html>')
            redirect.write_text(text, encoding='utf-8')
            self.assertEqual(apply(root), 1)
            self.assertFalse(BeautifulSoup(portal.read_text(encoding='utf-8'),
                'html.parser').select('nav.mythos-study-endnav'))
            self.assertEqual(redirect.read_text(encoding='utf-8'), text)


if __name__ == '__main__':
    unittest.main()
