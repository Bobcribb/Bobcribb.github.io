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


    def test_reconstitutions_3d_entry_is_unique_and_points_to_published_gallery(self):
        gallery = '/reconstitutions-photorealistes.html'
        atlas = '/reconstitutions-antiquite/'
        for menu in (NAV, MORE):
            self.assertEqual([(path, label) for path, label in menu if path == gallery],
                             [(gallery, 'Reconstitutions 3D')])
        self.assertEqual(sum(path == atlas for path, _ in MORE), 1)
        self.assertFalse(any(path == atlas for path, _ in NAV))
        raw_nav = BeautifulSoup(BASE_NAV, 'html.parser')
        self.assertEqual(len(raw_nav.select('a[href="' + gallery + '"]')), 1)
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('index.html', 'reconstitutions-photorealistes.html'):
                (root / name).write_text(
                    '<html lang="fr"><head><title>MYTHOS</title></head>'
                    '<body><main><h1>Étude</h1><p>Sources conservées.</p></main></body></html>',
                    encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), 2)
                for name in ('index.html', 'reconstitutions-photorealistes.html'):
                    doc = BeautifulSoup((root / name).read_text(encoding='utf-8'),
                                        'html.parser')
                    for selector in ('.mythos-primary-nav', '.mythos-menu nav'):
                        links = doc.select(selector + ' a[href="' + gallery + '"]')
                        self.assertEqual(len(links), 1, (name, selector))
                        self.assertEqual(links[0].get('aria-current') == 'page',
                                         name == 'reconstitutions-photorealistes.html')
                    self.assertIn('Sources conservées.', doc.get_text(' ', strip=True))


    def test_gallery_card_survives_repeated_museum_passes(self):
        """Une seule carte illustrée, sans perdre le texte de la page."""
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / 'index.html'
            page.write_text(
                '<html lang="fr"><head><title>MYTHOS</title></head><body>'
                '<main><article class="content"><section class="portal-section" '
                'id="home-collections"><h2>Les collections</h2>'
                '<div class="portal-grid"><a class="portal-card" '
                'href="/mythologie-grecque/"><strong>Grèce</strong></a></div>'
                '</section><p id="archive">Bibliographie et sources conservées.</p>'
                '</article></main></body></html>',
                encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                cards = doc.select(
                    '#home-collections a.portal-card'
                    '[href="/reconstitutions-photorealistes.html"]'
                )
                self.assertEqual(len(cards), 1)
                self.assertEqual(
                    cards[0].select_one('img')['src'],
                    '/assets/reconstitutions-3d/delphes-apollon-panorama.webp')
                self.assertIn('degrés de certitude', cards[0].get_text(' ', strip=True))
                self.assertIn('Bibliographie et sources conservées.',
                              doc.select_one('#archive').get_text())
                self.assertEqual(len(doc.select('a.portal-card[href="/mythologie-grecque/"]')), 1)

    def test_gallery_card_is_present_in_home_collections(self):
        # Verrouiller l'entrée illustrée du portail, et non seulement le menu.
        home = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
        cards = home.select(
            '#home-collections a.portal-card[href="/reconstitutions-photorealistes.html"]'
        )
        self.assertEqual(len(cards), 1, 'Carte de galerie 3D absente ou dupliquée')
        card = cards[0]
        self.assertEqual(card.select_one('strong').get_text(' ', strip=True),
                         'Reconstitutions 3D')
        image = card.select_one('img.mythos-card-image')
        self.assertIsNotNone(image, 'Carte 3D non illustrée')
        self.assertEqual(image.get('src'),
                         '/assets/reconstitutions-3d/delphes-apollon-panorama.webp')
        self.assertTrue((ROOT / image['src'].lstrip('/')).is_file(),
                        'Image 3D référencée mais absente du dépôt')
        self.assertIn('degrés de certitude', card.get_text(' ', strip=True))


if __name__ == '__main__':
    unittest.main()
