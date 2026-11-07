"""Vijayanagara/Hampi : dossier intégral, liens documentés, classement pérenne."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations

COLLECTION = ROOT / "bibliotheque-mythologies-du-monde"
NEW_SLUG = "civilisations-vijayanagara-hampi-societe-architecture-echanges"
NEW_URL = f"/bibliotheque-mythologies-du-monde/{NEW_SLUG}/"
STUDY = COLLECTION / NEW_SLUG / "index.html"
INDIA = COLLECTION / "civilisations-histoire-inde-ancienne" / "index.html"


class VijayanagaraNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = STUDY.read_text(encoding="utf-8")
        cls.doc = BeautifulSoup(cls.raw, "html.parser")
        cls.india = BeautifulSoup(INDIA.read_text(encoding="utf-8"), "html.parser")

    def test_study_keeps_full_text_and_critical_sources(self):
        self.assertGreater(len(self.doc.get_text(" ", strip=True).split()), 2800)
        headings = self.doc.select(".mythos-study-section > h2")
        self.assertEqual(len(headings), 18)
        bibliography = self.doc.select("#bibliographie > ol > li")
        self.assertEqual(len(bibliography), 11)
        self.assertTrue(all(row.get("id") == f"ref-{i}" for i, row in enumerate(bibliography, 1)))
        for institution in ("whc.unesco.org", "cambridge.org", "persee.fr"):
            self.assertIn(institution, self.raw)
        self.assertIn("Talikota", self.raw)
        self.assertIn("Tungabhadra", self.raw)

    def test_toc_anchors_and_breadcrumbs_remain_accessible(self):
        toc = self.doc.select_one('nav[aria-label="Sommaire de l\'étude"]')
        self.assertIsNotNone(toc)
        hrefs = [x.get("href") for x in toc.select("a[href^='#']")]
        self.assertEqual(len(hrefs), 19)
        self.assertEqual(len(hrefs), len(set(hrefs)))
        anchors = {x.get("id") for x in self.doc.select("[id]")}
        self.assertTrue(all(href[1:] in anchors for href in hrefs))
        for route in ("/civilisations/", "/civilisations/asie/",
                      "/bibliotheque-mythologies-du-monde/civilisations-histoire-inde-ancienne/"):
            self.assertTrue(self.doc.select_one('nav[aria-label="Fil d\'Ariane"] a[href="' + route + '"]'))

    def test_living_indian_corpus_is_preserved_and_backlinked(self):
        self.assertIn("Les mondes harappéens ne sont pas une simple préface aux Veda", self.india.get_text(" ", strip=True))
        cards = self.india.select("#inde-sud-vijayanagara-parcours a.portal-card")
        self.assertEqual(len(cards), 2)
        self.assertEqual(len([c for c in cards if c.get("href") == NEW_URL]), 1)
        self.assertTrue(any("civilisations-chola-tamil-nadu" in c.get("href", "") for c in cards))
        self.assertEqual(len(self.india.select("#inde-sud-vijayanagara-parcours")), 1)

    def test_is_classified_as_asia_without_modifying_generator(self):
        groups = get_civilisations([{
            "url": NEW_URL,
            "title": "Vijayanagara et Hampi",
            "excerpt": "Inde du Sud, inscriptions et temples",
        }])
        self.assertEqual(len(groups["asie"]), 1)
        self.assertFalse(any(groups[key] for key in ("afrique", "europe", "ameriques", "oceanie")))

    def test_image_is_real_and_attributed_not_25d(self):
        image = self.doc.select_one("figure.museum-object img")
        self.assertIsNotNone(image)
        self.assertGreater(len(image.get("alt", "")), 50)
        self.assertIn("wikimedia.org", image.get("src", ""))
        caption = image.parent.select_one("figcaption")
        self.assertIn("Ankit.k9", caption.get_text(" ", strip=True))
        self.assertTrue(caption.select_one('a[href="https://creativecommons.org/licenses/by-sa/4.0/"]'))
        self.assertFalse(self.doc.select_one('img[src$=".svg"]'))
        self.assertNotIn("Grande encyclopédie</a>", self.raw)


if __name__ == "__main__":
    unittest.main()
