"""Monographie Khotan : sources, conservation, classement et renvois sans liens fantômes."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

COL = ROOT / "bibliotheque-mythologies-du-monde"
SLUG = "civilisations-khotan-oasis-bouddhisme-manuscrits"
NEW_URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
KHOTAN = COL / SLUG / "index.html"
TIBET = COL / "civilisations-empire-tibetain-dunhuang" / "index.html"


class KhotanDunhuangNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = KHOTAN.read_text(encoding="utf-8")
        cls.study = BeautifulSoup(cls.raw, "html.parser")
        cls.tibet = BeautifulSoup(TIBET.read_text(encoding="utf-8"), "html.parser")

    def test_complete_scholarly_text_and_documentary_references(self):
        self.assertGreater(len(self.study.get_text(" ", strip=True).split()), 3200)
        self.assertEqual(len(self.study.select(".civilisation-khotan-section")), 16)
        bibliography = self.study.select("#bibliographie > ol > li")
        self.assertEqual(len(bibliography), 13)
        self.assertTrue(all(item.get("id") == f"ref-{i}" for i, item in enumerate(bibliography, 1)))
        for source in ("iranicaonline.org", "idp.bl.uk", "bnf.fr", "ccfr.bnf.fr"):
            self.assertIn(source, self.raw)
        for historical in ("Zambasta", "Dand", "Dunhuang", "Tibet", "saka"):
            self.assertIn(historical, self.raw)

    def test_sommaire_anchors_are_reachable_and_unique(self):
        toc = self.study.select_one('nav[aria-label="Sommaire scientifique de Khotan"]')
        self.assertIsNotNone(toc)
        anchors = [a.get("href", "") for a in toc.select('a[href^="#"]')]
        self.assertEqual(len(anchors), 17)
        self.assertEqual(len(anchors), len(set(anchors)))
        ids = {e.get("id") for e in self.study.select("[id]")}
        self.assertTrue(all(href[1:] in ids for href in anchors))
        self.assertTrue(self.study.select_one('nav[aria-label="Fil d\'Ariane"] a[href="/civilisations/asie/"]'))

    def test_tibetan_archive_is_unmodified_and_linked_once(self):
        doc = self.tibet
        self.assertIn("Dunhuang, laboratoire documentaire", doc.get_text(" ", strip=True))
        self.assertIn("L’écriture tibétaine et les premières archives", doc.get_text(" ", strip=True))
        self.assertEqual(len(doc.select("#dunhuang-khotan-parcours")), 1)
        cards = doc.select("#dunhuang-khotan-parcours a.portal-card")
        self.assertEqual(len(cards), 2)
        self.assertEqual(sum(c.get("href") == NEW_URL for c in cards), 1)
        self.assertTrue(any("civilisations-sogdiane-samarcande" in c.get("href", "") for c in cards))

    def test_khotan_is_classified_in_asia_without_changing_generator(self):
        sample = [{"url": NEW_URL, "title": "Khotan, royaume du Tarim", "excerpt": "Saka et bouddhisme"}]
        groups = get_civilisations(sample)
        self.assertEqual(len(groups["asie"]), 1)
        self.assertFalse(any(groups[k] for k in ("afrique", "ameriques", "europe", "oceanie")))

    def test_archival_photograph_is_licensed_and_attributed(self):
        photo = self.study.select_one("figure.museum-object img")
        self.assertIsNotNone(photo)
        self.assertIn("Ancient_Khotan_BLER2_AKV1_FP246_FIG31.jpg", photo.get("src", ""))
        self.assertGreater(len(photo.get("alt", "")), 60)
        caption = self.study.select_one("figure.museum-object figcaption")
        self.assertIn("Stein", caption.get_text(" ", strip=True))
        self.assertIn("1907", caption.get_text(" ", strip=True))
        self.assertTrue(caption.select_one('a[href*="commons.wikimedia.org/wiki/File:Ancient_Khotan"]'))
        self.assertIn("CC0", caption.get_text(" ", strip=True))
        self.assertFalse(self.study.select_one('img[src$=".svg"]'))


if __name__ == "__main__":
    unittest.main()
