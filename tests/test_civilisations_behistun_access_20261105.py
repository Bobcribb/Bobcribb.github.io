"""Contrôles des renvois réciproques vers la monographie intégrale CIV-01."""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "/corpus/civilisations/perse-iran-ancien-behistun.html"
IMAGE_URL = "/media/2026/10/mythos-behistun-inscription-darius-mahdimanavimvi-2018.jpg"


class BehistunPortalTests(unittest.TestCase):
    def test_illustrated_portal_card_and_scholarly_source(self):
        portal = BeautifulSoup((ROOT / "civilisations/index.html").read_text(encoding="utf-8"), "html.parser")
        section = portal.select_one("#etude-behistun")
        self.assertIsNotNone(section)
        cards = section.select("a.portal-card")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["href"], SOURCE_URL)
        image = cards[0].select_one("img.mythos-card-image")
        self.assertEqual(image["src"], IMAGE_URL)
        self.assertTrue(image.get("alt"))
        self.assertIn("CC BY-SA 4.0", cards[0].get_text(" ", strip=True))
        self.assertIn("bibliographie", cards[0].get_text(" ", strip=True).lower())

    def test_full_text_is_intact_and_has_a_return_link(self):
        source = (ROOT / SOURCE_URL.lstrip("/")).read_text(encoding="utf-8")
        self.assertGreater(len(source), 30000)
        article = BeautifulSoup(source, "html.parser")
        for anchor in ("civ-perse-5", "civ-perse-6", "civ-perse-7"):
            self.assertIsNotNone(article.select_one("#" + anchor))
        self.assertTrue(article.select_one("a[href='/civilisations/#etude-behistun']"))
        self.assertTrue(article.select_one("figure[data-media-id='mythos-behistun-inscription-darius-mahdimanavimvi-2018']"))
        self.assertTrue(article.select_one("aside.article-toc"))

    def test_museum_twice_preserves_local_behistun_photo(self):
        from tempfile import TemporaryDirectory
        from scripts.apply_museum_design import apply

        markup = ('<html><head><title>Bibliothèque des civilisations</title></head>'
                  '<body><main><h1>Civilisations</h1><section id="etude-behistun">'
                  '<a class="portal-card" href="' + SOURCE_URL + '">'
                  '<img class="mythos-card-image" src="' + IMAGE_URL + '" alt="">'
                  '<strong>Behistun</strong><span>Photo : Mahdimanavimvi (2018), '
                  'CC BY-SA 4.0, sources et bibliographie.</span>'
                  '</a></section></main></body></html>')
        with TemporaryDirectory() as temp:
            root = Path(temp)
            local_image = root / IMAGE_URL.lstrip("/")
            local_image.parent.mkdir(parents=True)
            local_image.write_bytes(b"documentary-photograph")
            page = root / "civilisations/index.html"
            page.parent.mkdir(parents=True)
            page.write_text(markup, encoding="utf-8")
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                document = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                card = document.select_one("#etude-behistun .portal-card")
                self.assertEqual([image["src"] for image in card.select("img")], [IMAGE_URL])
                self.assertIn("Relief de Darius", card.img["alt"])
                self.assertIn("CC BY-SA 4.0", card.get_text(" ", strip=True))
                self.assertIn("bibliographie", card.get_text(" ", strip=True))
            local_image.unlink()
            with self.assertRaisesRegex(RuntimeError, "Photographie de Behistun manquante"):
                apply(root)

    def test_generator_keeps_link_and_mobile_layout(self):
        source = (ROOT / "scripts/build_navigation.py").read_text(encoding="utf-8")
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertIn(SOURCE_URL, source)
        self.assertIn('id="etude-behistun"', source)
        self.assertIn(IMAGE_URL, source)
        self.assertIn("#etude-behistun .portal-card:focus-visible", css)
        self.assertIn("@media (max-width: 680px)", css)


if __name__ == "__main__":
    unittest.main()
