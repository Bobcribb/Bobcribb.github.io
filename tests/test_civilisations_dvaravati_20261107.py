"""Contrôles ciblés Dvāravatī : classement, texte intégral et navigation (#164)."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent

SLUG = "civilisations-dvaravati-cites-mon-sithep"
URL = f"/bibliotheque-mythologies-du-monde/{SLUG}/"
FILE = ROOT / "bibliotheque-mythologies-du-monde" / SLUG / "index.html"


class DvaravatiParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.anchors = []
        self.sections = 0
        self.sources = 0
        self.canonical = None
        self.skip = False
        self.image = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            assert attrs["id"] not in self.ids, "duplicate id: " + attrs["id"]
            self.ids.add(attrs["id"])
        if tag == "a":
            href = attrs.get("href", "")
            if href.startswith("#"):
                self.anchors.append(href[1:])
            if "mythos-skip" in attrs.get("class", "").split() and href == "#contenu":
                self.skip = True
        if tag == "section" and attrs.get("aria-labelledby", "").startswith("etude-"):
            self.sections += 1
        if tag == "li" and attrs.get("id", "").startswith("source-"):
            self.sources += 1
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "img" and "Khao_Khlang_Nai-005.jpg" in attrs.get("src", ""):
            self.image = "reconstitution" in attrs.get("alt", "")


class DvaravatiCivilisationsTests(unittest.TestCase):
    def test_navigation_civilisations_asiatiques(self):
        entry = {"url": URL, "title": "Dvāravatī, cités et bouddhismes"}
        self.assertEqual(group_continent(entry), "asie")
        groups = get_civilisations([entry])
        self.assertEqual([item["url"] for item in groups["asie"]], [URL])
        self.assertEqual(sum(map(len, groups.values())), 1)

    def test_integral_scientific_text_and_accessibility(self):
        html = FILE.read_text(encoding="utf-8")
        parsed = DvaravatiParser()
        parsed.feed(html)
        self.assertEqual(parsed.canonical, "https://bobmythos.fr" + URL)
        self.assertEqual(parsed.sections, 20)
        self.assertEqual(parsed.sources, 11)
        self.assertTrue(parsed.skip, "Lien d'évitement absent")
        self.assertTrue(parsed.image, "L'image doit être explicitement décrite comme document, non restitution")
        self.assertEqual(set(parsed.anchors) - parsed.ids, set(), "Ancres internes orphelines")
        self.assertIn('aria-label="Fil d’Ariane"', html)
        self.assertIn('href="/civilisations/asie/"', html)
        self.assertIn('href="/mythologie-grecque/"', html)
        self.assertIn('href="/mythologie-comparee/"', html)
        self.assertIn('href="/methode-editoriale/"', html)
        self.assertIn("publications.efeo.fr", html)
        self.assertIn("www.persee.fr", html)
        self.assertIn("whc.unesco.org", html)
        self.assertIn("creativecommons.org/licenses/by-sa/3.0", html)
        self.assertGreater(len(html.split()), 3200)
        self.assertNotIn("Grande encyclopédie</a>", html)

if __name__ == "__main__":
    unittest.main()
