"""Contrôles non destructifs du parcours Liangzhu (MYTHOS, 7 novembre 2026)."""
import sys
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as navigation

LIANGZHU = "/bibliotheque-mythologies-du-monde/civilisations-liangzhu-yangzi-neolithique/"
CHINA = "/bibliotheque-mythologies-du-monde/civilisations-histoire-chine-ancienne/"
SHU = "/bibliotheque-mythologies-du-monde/civilisations-shu-sanxingdui-jinsha/"


class TestLiangzhuNavigation(unittest.TestCase):
    def test_study_integrity_and_evidence(self):
        path = ROOT / LIANGZHU.lstrip("/") / "index.html"
        source = path.read_text(encoding="utf-8")
        page = BeautifulSoup(source, "html.parser")
        self.assertEqual(len(page.select('section > h2[id^="section-"]')), 18)
        self.assertEqual(len(page.select('.mythos-reading-toc a[href^="#section-"]')), 18)
        self.assertEqual(len(page.select('ol li[id^="ref-"]')), 11)
        self.assertTrue(page.select_one('nav[aria-label="Fil d’Ariane"] a[href="/civilisations/asie/"]'))
        self.assertTrue(page.select_one('a.mythos-skip[href="#contenu"]'))
        self.assertTrue(page.select_one('img[alt][loading="lazy"]'))
        self.assertIn("xiquinhosilva", source)
        self.assertIn("creativecommons.org/licenses/by/2.0/", source)
        self.assertIn("whc.unesco.org/fr/list/1592/", source)
        self.assertIn("10.1073/pnas.1710516114", source)
        self.assertIn("10.1126/sciadv.abi9275", source)
        self.assertIn(CHINA, source)
        self.assertIn(SHU, source)
        self.assertNotIn("Grande encyclopédie", source)

    def _render_asia(self, entries):
        with tempfile.TemporaryDirectory() as temporary:
            original = navigation.OUT
            navigation.OUT = Path(temporary)
            try:
                navigation.create_civilisations(
                    entries, navigation.get_civilisations(entries))
                return (navigation.OUT / "civilisations/asie/index.html").read_text(
                    encoding="utf-8")
            finally:
                navigation.OUT = original

    def test_no_link_to_an_unindexed_liangzhu(self):
        asia = self._render_asia([{"url": CHINA, "title": "Chine ancienne"}])
        self.assertNotIn(LIANGZHU, asia)
        self.assertNotIn("Bas Yangzi — urbanisme néolithique", asia)

    def test_conditional_asia_route_and_related_studies(self):
        entries = [
            {"url": LIANGZHU, "title": "Liangzhu — Bas Yangzi"},
            {"url": CHINA, "title": "Chine ancienne"},
            {"url": SHU, "title": "Shu, Sanxingdui et Jinsha"},
        ]
        grouped = navigation.get_civilisations(entries)
        self.assertEqual(len(grouped["asie"]), 3)
        self.assertEqual(sum(len(group) for name, group in grouped.items()
                             if name != "asie"), 0)
        asia = self._render_asia(entries)
        self.assertIn("Bas Yangzi — urbanisme néolithique", asia)
        self.assertIn(LIANGZHU, asia)
        self.assertIn(CHINA, asia)
        self.assertIn(SHU, asia)

    def test_no_nonexistent_crosslink(self):
        asia = self._render_asia([{"url": LIANGZHU, "title": "Liangzhu"}])
        self.assertIn(LIANGZHU, asia)
        # La carte transversale est conditionnelle : l'étude de Shu ne doit pas
        # être affichée dans cette sous-section si elle manque de l'index.
        start = asia.index("Bas Yangzi — urbanisme néolithique")
        end = asia.index("Poursuivre l’exploration", start)
        self.assertNotIn(SHU, asia[start:end])
        self.assertNotIn(CHINA, asia[start:end])


if __name__ == "__main__":
    unittest.main()
