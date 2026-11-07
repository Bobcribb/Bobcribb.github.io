"""Tests de couverture Dvāravatī — lot ciblé MYTHOS #164, sans I/O réseau."""
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation  # noqa: E402

STUDY = ROOT / "bibliotheque-mythologies-du-monde" / "civilisations-dvaravati-si-thep" / "index.html"
URL = "/bibliotheque-mythologies-du-monde/civilisations-dvaravati-si-thep/"


class DvaravatiIntegrityTests(unittest.TestCase):
    def test_study_complete_and_accessible(self):
        soup = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(soup.html.get("lang"), "fr")
        self.assertEqual(soup.select_one('link[rel="canonical"]').get("href"),
                         "https://bobmythos.fr" + URL)
        self.assertTrue(soup.select_one('a[href="#mythos-content"]'))
        self.assertTrue(soup.select_one('nav[aria-label="Fil d\'Ariane"]'))
        sections = soup.select("section.mythos-study-section h2[id]")
        self.assertEqual(len(sections), 18)
        toc = soup.select('nav[aria-label="Sommaire de la monographie"] li a')
        self.assertEqual(len(toc), len(sections))
        self.assertEqual({a["href"] for a in toc},
                         {"#" + s["id"] for s in sections})
        self.assertTrue(soup.select_one('a[href="/civilisations/asie/"]'))
        self.assertTrue(soup.select_one('a[href="/mythologie-grecque/"]'))
        self.assertFalse(soup.find(string=re.compile(r"Grande encyclopédie")))

    def test_archaeological_image_license_and_sourcing(self):
        soup = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        photo = soup.select_one("figure img")
        self.assertTrue(photo and "Khao_Khlang_Nai-004.jpg" in photo["src"])
        self.assertTrue(photo.get("alt"))
        self.assertTrue(soup.select_one('a[href="https://creativecommons.org/licenses/by-sa/3.0/"]'))
        self.assertTrue(soup.select_one('a[href="https://commons.wikimedia.org/wiki/File:Khao_Khlang_Nai-004.jpg"]'))
        refs = soup.select(".study-biblio li")
        self.assertGreaterEqual(len(refs), 10)
        self.assertTrue(all(ref.a and ref.a.get("href", "").startswith("https://") for ref in refs))

    def test_asia_routes_are_conditioned_on_index_entries(self):
        def item(url, title):
            return {"url": url, "title": title}
        dvaravati = item(URL, "Dvāravatī")
        khmer = item("/bibliotheque-mythologies-du-monde/civilisations-histoire-khmers-angkor/", "Khmers")
        srivijaya = item("/bibliotheque-mythologies-du-monde/civilisations-srivijaya-sumatra/", "Śrīvijaya")
        entries = [dvaravati, khmer, srivijaya]
        groups = build_navigation.get_civilisations(entries)
        self.assertEqual([e["url"] for e in groups["asie"]], [e["url"] for e in entries])
        output = {}
        with patch.object(build_navigation, "write", side_effect=lambda slug, html: output.setdefault(slug, html)):
            build_navigation.create_civilisations(entries, groups)
        page = output["civilisations/asie"]
        self.assertIn("Asie du Sud-Est — villes, sanctuaires et réseaux", page)
        for e in entries:
            self.assertIn(e["url"], page)
        missing_groups = build_navigation.get_civilisations(entries[1:])
        missing_output = {}
        with patch.object(build_navigation, "write", side_effect=lambda slug, html: missing_output.setdefault(slug, html)):
            build_navigation.create_civilisations(entries[1:], missing_groups)
        self.assertNotIn("Asie du Sud-Est — villes, sanctuaires et réseaux", missing_output["civilisations/asie"])


if __name__ == "__main__":
    unittest.main()
