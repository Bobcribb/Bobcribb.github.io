"""Reconstruction checks for the six illustrated reading cards on MYTHOS."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply, picture

READING_IMAGES = {
    "/philosophie-iliade.html": "mythos-iliade-achille-ajax-athena-hydrie-met-56-171-29.jpg",
    "/philosophie-odyssee.html": "mythos-papyrus-odyssee-ptolemaique-met-09-182-50.jpg",
    "/philosophie-theogonie.html": "mythos-bronze-artemision-zeus-ou-poseidon.jpg",
    "/parcours/decouvrir-les-mythes-grecs/": "mythos-heracles-lion-nemee-oinochoe-met-06-1021-66.jpg",
    "/parcours/comprendre-la-tragedie/": "mythos-masques-theatre-rondelles-hellenistiques-met-2001-767.jpg",
    "/parcours/comparer-les-creations-du-monde/": "mythos-enuma-elish-tablette-k3473-ninive-zunkir.jpg",
}


class PortalIllustrationTests(unittest.TestCase):
    def test_six_reading_cards_keep_exact_images_on_repeated_builds(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "media" / "2026" / "10"
            media.mkdir(parents=True)
            for filename in READING_IMAGES.values():
                (media / filename).write_bytes(b"media fixture")
            cards = "".join(
                '<a class="portal-card" href="' + url + '"><strong>Lecture</strong>'
                '<span>Sources et bibliographie</span></a>' for url in READING_IMAGES
            )
            cards += '<a class="portal-card" href="/not-an-editorial-cover/"><strong>Sans image</strong></a>'
            page = root / "index.html"
            page.write_text(
                '<html lang="fr"><head><title>MYTHOS</title></head><body><main>'
                '<h1>Accueil</h1><p>Texte universitaire préservé.</p>'
                + cards + '</main></body></html>', encoding="utf-8"
            )
            for _ in range(2):
                self.assertEqual(apply(root), 1)
                doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
                for url, filename in READING_IMAGES.items():
                    expected = "/media/2026/10/" + filename
                    card = doc.select_one('a.portal-card[href="' + url + '"]')
                    self.assertIsNotNone(card)
                    self.assertEqual([img.get("src") for img in card.select("img")], [expected])
                    self.assertEqual(picture(url, root), expected)
                other = doc.select_one('a.portal-card[href="/not-an-editorial-cover/"]')
                self.assertEqual(len(other.select("img")), 0)
                self.assertIn("Texte universitaire préservé.", doc.get_text(" ", strip=True))
                self.assertIn("Sources et bibliographie", doc.get_text(" ", strip=True))

    def test_does_not_invent_missing_media(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            for url in READING_IMAGES:
                self.assertIsNone(picture(url, root))


if __name__ == "__main__":
    unittest.main()
