"""Non-régression documentaire : Sigurd et prolongement Brynhildr/Guðrún.

Les sources HTML restent publiables par build_native.py sans attribution de numéro.
"""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques")
SIGURD = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen" / "index.html"
BRYNHILDR = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen" / "brynhildr-gudrun" / "index.html"
NIBELUNGEN = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen" / "nibelungenlied-kriemhild-hagen" / "index.html"
ATLI = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen" / "atli-gunnar-hogni-atlakvida-atlamal" / "index.html"
KLAGE = BASE / "cycle-sigurd-brynhildr-fafnir-nibelungen" / "nibelungenklage-memoire-deuil" / "index.html"
PORTAL = BASE / "index.html"


class SigurdBrynhildrPublicationTests(unittest.TestCase):
    def test_original_not_deleted_and_monograph_complete(self):
        html = (ROOT / SIGURD).read_text(encoding="utf-8")
        self.assertIn("1. Des témoins qui ne racontent pas la même histoire", html)
        self.assertIn('id="lecture-section-7"', html)
        self.assertIn("XXII. Histoire, réception moderne et conclusion critique", html)
        self.assertIn("sigurd-monographie-sources", html)
        self.assertGreater(len(html), 35000)
        self.assertIn("Hugr mik hvatti", html)
        self.assertIn("Ramsund", html)
        self.assertIn("Hylestad", html)

    def test_anchors_are_unique_and_toc_links_resolve(self):
        for path in (SIGURD, BRYNHILDR, NIBELUNGEN, ATLI, KLAGE):
            soup = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
            ids = [tag["id"] for tag in soup.select("[id]")]
            self.assertEqual(len(ids), len(set(ids)), str(path))
            for link in soup.select("details.mythos-reading-toc a[href^='#']"):
                self.assertIn(link["href"][1:], ids, str(path))

    def test_brynhildr_study_is_distinct_and_reciprocal(self):
        main = (ROOT / SIGURD).read_text(encoding="utf-8")
        follow = (ROOT / BRYNHILDR).read_text(encoding="utf-8")
        self.assertIn("/brynhildr-gudrun/", main)
        self.assertIn("/cycle-sigurd-brynhildr-fafnir-nibelungen/", follow)
        self.assertIn("La lamentation de Guðrún", follow)
        self.assertIn("Atli", follow)
        self.assertIn("/nibelungenlied-kriemhild-hagen/", main)
        self.assertIn("/nibelungenlied-kriemhild-hagen/", follow)
        self.assertGreater(len(follow), 15000)

    def test_portal_references_five_studies_without_draft_label(self):
        soup = BeautifulSoup((ROOT / PORTAL).read_text(encoding="utf-8"), "html.parser")
        items = [a for a in soup.select("a[href]") if "cycle-sigurd-brynhildr-fafnir-nibelungen/" in a.get("href", "")]
        self.assertEqual(len(items), 5)
        for a in items:
            self.assertNotIn("brouillon", a.parent.get_text(" ", strip=True).lower())
        self.assertIn("monographie universitaire approfondie", items[0].parent.get_text(" ", strip=True).lower())

    def test_traditional_page_shell_retained(self):
        for path in (SIGURD, BRYNHILDR):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn('href="/assets/mythos-museum.css?v=20261104"', text)
            self.assertIn('class="mythos-design mythos-reading"', text)
            self.assertIn('src="/assets/mythos-reading.js?v=20261104-lecture-2"', text)
            self.assertIn("bobmythos.fr", text)


if __name__ == "__main__":
    unittest.main()
