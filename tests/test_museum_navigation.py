"""The Greek encyclopedia has one entrance; historical texts stay available."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from apply_museum_design import apply, NAV, MORE
from build_navigation import NAV as BASE_NAV

GREEK = '/mythologie-grecque/'
LEGACY = '/grande-encyclopedie/'


class MuseumNavigationTests(unittest.TestCase):
    def test_one_encyclopedia_entrance_in_all_generated_menus(self):
        for menu in (NAV, MORE):
            self.assertEqual(sum(path == GREEK for path, _ in menu), 1)
            self.assertFalse(any('grande-encyclopedie' in path for path, _ in menu))
        doc = BeautifulSoup(BASE_NAV, 'html.parser')
        self.assertEqual(len(doc.select('a[href="'+GREEK+'"]')), 1)
        self.assertFalse(doc.select('a[href*="grande-encyclopedie"]'))

    def test_repeated_build_removes_stale_navigation_without_losing_articles(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixtures = {
                'index.html': False,
                'mythologie-grecque/index.html': True,
                'mythologie-grecque/dossiers/cosmogonies/index.html': True,
                'grande-encyclopedie/index.html': True,
                'grande-encyclopedie.html': True,
                'chapitres/encyclopedie/chapitre-375-nyx/index.html': True,
                'theatre/index.html': False,
            }
            prose = '<p id="source">Texte intégral, αἰδώς et bibliographie.</p><a href="/grande-encyclopedie/registre-integral/">Registre historique</a>'
            for rel in fixtures:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('<html lang="fr"><head><title>MYTHOS</title></head><body>'
                                '<header class="mythos-masthead"><nav><a href="'+LEGACY+'">Grande encyclopédie</a></nav></header>'
                                '<main><article class="content"><h1>Étude</h1>'+prose+'</article></main></body></html>', encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), len(fixtures))
                for rel, active in fixtures.items():
                    doc = BeautifulSoup((root / rel).read_text(), 'html.parser')
                    for selector in ('.mythos-primary-nav', '.mythos-menu nav'):
                        nav = doc.select_one(selector)
                        self.assertFalse(nav.select('a[href*="grande-encyclopedie"]'), rel)
                        links = nav.select('a[href="'+GREEK+'"]')
                        self.assertEqual(len(links), 1, rel)
                        self.assertEqual(links[0].get('aria-current') == 'page', active, rel)
                    self.assertEqual(len(doc.select('.mythos-masthead')), 1)
                    self.assertEqual(doc.find(id='source').get_text(), 'Texte intégral, αἰδώς et bibliographie.')
                    self.assertTrue(doc.article.select_one('a[href="/grande-encyclopedie/registre-integral/"]'))


if __name__ == '__main__':
    unittest.main()
