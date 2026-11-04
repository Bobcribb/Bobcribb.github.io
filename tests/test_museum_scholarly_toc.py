"""Non-régression des sommaires automatiques des études MYTHOS."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from apply_museum_design import apply


class ScholarlyTocTests(unittest.TestCase):
    def test_reader_toc_preserves_all_sources_and_rebuilds_once(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'chapitres/grece/mycenes/index.html'
            path.parent.mkdir(parents=True)
            original = (
                '<html lang="fr"><head><title>Mycènes | MYTHOS</title></head><body>'
                '<main class="layout"><article class="content">'
                '<h1>Mycènes — les Atrides</h1>'
                '<p id="prose">Texte intégral : Ἀγαμέμνων et mémoire historique.</p>'
                '<h2 id="geographie">Géographie et chronologie</h2>'
                '<p>Contexte archéologique et stratigraphie.</p>'
                '<h2>Sources textuelles</h2>'
                '<p><a href="https://example.org/source">Pausanias, II</a>.</p>'
                '<h2>Analyse philosophique et comparaisons</h2>'
                '<p>Analyse de la tradition grecque.</p>'
                '<h2>Bibliographie critique</h2>'
                '<p id="bibliographie">Travaux et éditions scientifiques.</p>'
                '</article></main></body></html>'
            )
            path.write_text(original, encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(temp), 1)
                doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
                navs = doc.select('main nav.mythos-scholarly-toc')
                self.assertEqual(len(navs), 1)
                links = navs[0].select('ol a[href^="#"]')
                self.assertEqual(len(links), 4)
                self.assertEqual(links[0]['href'], '#geographie')
                self.assertEqual(len({a['href'] for a in links}), 4)
                for a in links:
                    self.assertEqual(len(doc.find_all(id=a['href'][1:])), 1)
                self.assertEqual(len(doc.select('h1')), 1)
                self.assertEqual(doc.find(id='prose').get_text(strip=True),
                                 'Texte intégral : Ἀγαμέμνων et mémoire historique.')
                self.assertEqual(doc.find(id='bibliographie').get_text(strip=True),
                                 'Travaux et éditions scientifiques.')
                self.assertIsNotNone(doc.select_one('a[href="https://example.org/source"]'))

    def test_authored_toc_is_never_duplicated(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'chapitres/comparatif/volume-1/index.html'
            path.parent.mkdir(parents=True)
            path.write_text(
                '<html><head><title>Étude</title></head><body><main>'
                '<article class="content"><h1>Titre</h1><h2>Sommaire</h2>'
                '<ul class="toc"><li><a href="#source">Source</a></li></ul>'
                '<h2 id="source">Source</h2><p>Source primaire.</p>'
                '<h2>Analyse</h2><p>Commentaire.</p>'
                '<h2>Bibliographie</h2><p>Ouvrages.</p>'
                '</article></main></body></html>', encoding='utf-8')
            for _ in range(2):
                self.assertEqual(apply(temp), 1)
                doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
                self.assertFalse(doc.select('nav.mythos-scholarly-toc'))
                self.assertEqual(len(doc.select('ul.toc')), 1)
                self.assertEqual(doc.find(id='source').get_text(strip=True), 'Source')

    def test_portal_never_receives_study_toc(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'index.html'
            path.write_text(
                '<html><head><title>Accueil</title></head><body><main><h1>Accueil</h1>'
                '<h2>A</h2><h2>B</h2><h2>C</h2></main></body></html>',
                encoding='utf-8')
            self.assertEqual(apply(temp), 1)
            doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            self.assertFalse(doc.select('nav.mythos-scholarly-toc'))


if __name__ == '__main__':
    unittest.main()
