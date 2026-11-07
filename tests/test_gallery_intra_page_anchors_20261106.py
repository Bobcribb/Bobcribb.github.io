"""Régression MYTHOS : les ancres 3D doivent viser une section réellement présente.

Le contrôle couvre toutes les vignettes et les liens de lecture d'une galerie
publiée ; il ne touche ni aux images, ni aux notices, ni aux manuscrits.
"""
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
import unittest

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


class GalleryIntraPageAnchorTests(unittest.TestCase):
    def test_all_internal_gallery_links_resolve_to_unique_ids(self):
        gallery = ROOT / "reconstitutions-photorealistes.html"
        source = gallery.read_text(encoding="utf-8")
        doc = BeautifulSoup(source, "html.parser")
        identifiers = [item["id"] for item in doc.select("[id]")]
        counts = Counter(identifiers)
        duplicate = [key for key, count in counts.items() if count != 1]
        self.assertFalse(duplicate, f"Identifiants HTML dupliqués : {duplicate}")
        links = [
            (link.get("href"), unquote(link["href"][1:]))
            for link in doc.select('a[href^="#"]')
            if link["href"] != "#"
        ]
        self.assertGreater(len(links), 50, "Sommaire de la galerie manquant")
        for href, target in links:
            with self.subTest(href=href):
                self.assertNotIn("{", target, "Gabarit de navigation non résolu")
                self.assertIn(target, counts, "Cible de lecture absente")
        self.assertIn("lecture-section-76", counts, "Repère Métaponte disparu")
        self.assertIsNotNone(doc.find(id="metaponte-tavole-palatine-heraion-vers-515-av-jc"))


if __name__ == "__main__":
    unittest.main()
