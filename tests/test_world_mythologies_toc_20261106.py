"""Le sommaire du portail mondial conserve les liens des études intégrales."""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "mythologies/index.html"
GENERATOR = ROOT / "scripts/build_navigation.py"
STYLES = ROOT / "assets/mythos-museum.css"

ANCHORS = {
    "mythologies-figures": "Commencer par les figures et les histoires",
    "mythologies-traditions": "Les grandes traditions",
    "mythologies-methodes": "Figures, récits et méthodes",
}
EXISTING_VOLUME_PATHS = (
    "mythos-volume-10-finno-carelien-kalevala",
    "mythos-volume-12-koush-meroe-apedemak",
    "mythos-volume-13-armenie-vahagn-david-sassoun",
    "mythos-volume-19-la-galigo-bugis-sawerigading",
)


class TestWorldMythologiesToc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.soup = BeautifulSoup(cls.html, "html.parser")

    def test_unique_anchors_and_accessible_navigation(self):
        toc = self.soup.select_one('nav.mythos-world-toc[aria-label]')
        self.assertIsNotNone(toc)
        hrefs = [a.get("href") for a in toc.select("a[href]")]
        self.assertEqual(hrefs, ["#" + anchor for anchor in ANCHORS])
        for anchor, title in ANCHORS.items():
            target = self.soup.find(id=anchor)
            self.assertIsNotNone(target, anchor)
            self.assertEqual(len(self.soup.select('[id="' + anchor + '"]')), 1)
            self.assertEqual(target.name, "section")
            self.assertEqual(target.find("h2").get_text(" ", strip=True), title)

    def test_historical_integral_volumes_remain_linked_and_untruncated(self):
        for slug in EXISTING_VOLUME_PATHS:
            with self.subTest(slug=slug):
                url = "/bibliotheque-mythologies-du-monde/" + slug + "/"
                self.assertEqual(len(self.soup.select('a[href="' + url + '"]')), 1)
                page = ROOT / "bibliotheque-mythologies-du-monde" / slug / "index.html"
                self.assertTrue(page.exists(), slug)
                html = page.read_text(encoding="utf-8")
                self.assertGreater(len(html), 40_000, slug)
                self.assertRegex(html.lower(), r"bibliograph|sources|références")

    def test_restored_image_and_credit_for_two_historical_volumes(self):
        # Les générateurs de navigation conservent les images sourcées.
        for marker in ("koush-naqa-lassihu", "sassoun-kochar-2014"):
            images = self.soup.select('img[data-mythos-card-source="' + marker + '"]')
            self.assertEqual(len(images), 1, marker)
            self.assertTrue(images[0].get("alt"), marker)
            self.assertEqual(images[0].get("loading"), "lazy")
        self.assertIn("LassiHU (2005)", self.html)
        self.assertIn("Marcin Konsek (2014)", self.html)

    def test_build_regenerates_exact_same_three_anchors(self):
        py = GENERATOR.read_text(encoding="utf-8")
        self.assertIn('def create_mythologies(entries):', py)
        self.assertIn('class="mythos-world-toc"', py)
        for anchor, title in ANCHORS.items():
            self.assertIn('("' + title + '", "' + anchor + '")', py)
        self.assertIn('if body.count(old) != 1:', py)

    def test_responsive_museum_skin(self):
        css = STYLES.read_text(encoding="utf-8")
        self.assertIn("body.mythos-design .mythos-world-toc", css)
        self.assertIn("grid-template-columns:repeat(3,minmax(0,1fr))", css)
        self.assertIn("@media(max-width:720px)", css)
        self.assertIn("body.mythos-design .mythos-world-toc a:focus-visible", css)


if __name__ == "__main__":
    unittest.main()
