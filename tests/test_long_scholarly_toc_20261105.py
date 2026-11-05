"""Un sommaire complet pour les longues monographies, sans toucher au texte universitaire."""
from html import escape
from pathlib import Path
import re
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import add_scholarly_toc


class LongScholarlyTocTests(unittest.TestCase):
    @staticmethod
    def sample(level="h2", count=36):
        items = ''.join(
            f'<{level}>Partie {n} — Sources et bibliographie</{level}>'
            f'<p>Texte scientifique conservé, passage {n}.</p>'
            for n in range(1, count + 1)
        )
        if level == "h3":
            items = "<h2>Présentation générale de l'étude</h2>" + items
        return BeautifulSoup(
            '<!doctype html><html lang="fr"><head><title>Étude</title></head>'
            '<body><main id="mythos-content"><article class="content">'
            '<h1>Monographie intégrale</h1>' + items +
            '</article></main></body></html>', "html.parser")

    def check_toc(self, level, count):
        doc = self.sample(level, count)
        original_text = doc.article.get_text(' ', strip=True)
        original_paragraphs = [p.get_text(' ', strip=True) for p in doc.article.find_all('p')]
        rel = 'chapitres/encyclopedie/chapitre-444-test/index.html'
        add_scholarly_toc(doc, doc.main, rel)
        nav = doc.select_one('nav.mythos-scholarly-toc')
        self.assertIsNotNone(nav)
        self.assertIs(nav.parent, doc.main)
        self.assertIsNone(nav.find_parent('article'))
        self.assertEqual(doc.article.get_text(' ', strip=True), original_text)
        self.assertEqual([p.get_text(' ', strip=True) for p in doc.article.find_all('p')],
                         original_paragraphs)
        links = nav.select('ol a[href^="#"]')
        self.assertEqual(len(links), count)
        self.assertEqual(len({a["href"] for a in links}), count)
        for link in links:
            self.assertEqual(len(doc.find_all(id=link["href"][1:])), 1)
        if count > 32:
            disclosure = nav.select_one('details.mythos-scholarly-toc-disclosure')
            self.assertIsNotNone(disclosure)
            self.assertIn(str(count), disclosure.summary.get_text())
        else:
            self.assertIsNone(nav.select_one('details'))
        snapshot = str(doc)
        add_scholarly_toc(doc, doc.main, rel)
        self.assertEqual(str(doc), snapshot, "Un deuxième habillage doit être idempotent")
        self.assertEqual(len(doc.select('nav.mythos-scholarly-toc')), 1)

    def test_36_sections_integres_eros_thespies(self):
        source = (ROOT / 'chapitres/encyclopedie/'
                  'chapitre-444-eros-thespies-pierre-aniconique-praxiteles-erotideia-phryne.md')
        self.assertGreater(len(re.findall(r'^##\s+', source.read_text(encoding='utf-8'), re.M)), 32)
        self.check_toc('h2', 36)

    def test_39_sous_sections_artemis_orthia(self):
        source = (ROOT / 'chapitres/encyclopedie/'
                  'chapitre-443-artemis-orthia-sparte-lygos-masques-fouet-sanctuaire.md')
        self.assertGreater(len(re.findall(r'^###\s+', source.read_text(encoding='utf-8'), re.M)), 32)
        self.check_toc('h3', 39)

    def test_petits_sommaires_restent_deplies(self):
        self.check_toc('h2', 4)

    def test_sommaire_redige_par_auteur_reste_prioritaire(self):
        doc = self.sample('h2', 36)
        doc.article.insert(0, BeautifulSoup(
            '<nav aria-label="Sommaire de l’auteur"><a href="#source">Sources</a></nav>',
            'html.parser'))
        add_scholarly_toc(doc, doc.main, 'chapitres/encyclopedie/test/index.html')
        self.assertIsNone(doc.select_one('nav.mythos-scholarly-toc'))
        self.assertIsNotNone(doc.article.select_one('nav[aria-label]'))

    def test_sommaire_de_lecture_existant_n_est_pas_double(self):
        doc = self.sample('h2', 36)
        # Les outils de lecture servent déjà un sommaire natif sur Éros.
        # Même sans ses liens, ce conteneur doit bloquer tout doublon.
        authored = BeautifulSoup(
            '<details class="mythos-reading-toc" data-reading-owned="true">'
            '<summary>Sommaire de lecture · 36 sections</summary>'
            '<p>Navigation déjà disponible dans le lecteur</p></details>',
            'html.parser'
        )
        doc.article.insert(0, authored)
        before = str(doc.article)
        add_scholarly_toc(doc, doc.main, 'chapitres/encyclopedie/test/index.html')
        self.assertEqual(len(doc.select('.mythos-reading-toc')), 1)
        self.assertIsNone(doc.select_one('nav.mythos-scholarly-toc'))
        self.assertEqual(str(doc.article), before)

    def test_habillage_accessible_mobile(self):
        css = (ROOT / 'assets/mythos-museum.css').read_text(encoding='utf-8')
        self.assertIn('.mythos-scholarly-toc-disclosure>summary', css)
        self.assertIn('min-height:48px', css)
        self.assertIn('@media(max-width:700px)', css)


if __name__ == '__main__':
    unittest.main()
