"""Poverty Point : dossier critique, accès Amériques, protections de navigation et sources."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as navigation

URL = "/bibliotheque-mythologies-du-monde/civilisations-poverty-point-mississippi-archaique/"
CAHOKIA = "/bibliotheque-mythologies-du-monde/civilisations-cahokia-mississippienne/"
FILE = ROOT / "bibliotheque-mythologies-du-monde/civilisations-poverty-point-mississippi-archaique/index.html"

class StudyInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.sections = []
        self.targets = set()
        self.internal = []
        self.images = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.targets.add(a["id"])
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "section" and "mythos-critical-chapter" in a.get("class", "").split():
            self.sections.append(a.get("id"))
        if tag == "a" and a.get("href", "").startswith("#"):
            self.internal.append(a["href"][1:])
        if tag == "img":
            self.images.append(a)

class PovertyPointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = FILE.read_text(encoding="utf-8")
        cls.parsed = StudyInspector()
        cls.parsed.feed(cls.html)
    def test_continent_and_non_regression(self):
        es = [{"url": URL, "title": "Poverty Point"}, {"url": CAHOKIA, "title": "Cahokia"},
              {"url": "/bibliotheque-mythologies-du-monde/civilisations-histoire-mesopotamie/", "title": "Mésopotamie"}]
        groups = navigation.get_civilisations(es)
        self.assertEqual([x["url"] for x in groups["ameriques"]], [URL, CAHOKIA])
        self.assertEqual([x["title"] for x in groups["asie"]], ["Mésopotamie"])
        self.assertEqual(sum(map(len, groups.values())), 3)
    def test_study_complete_and_canonical(self):
        self.assertEqual(self.parsed.canonical, "https://bobmythos.fr" + URL)
        self.assertEqual(len(self.parsed.sections), 22)
        self.assertEqual(len(set(self.parsed.sections)), 22)
        self.assertIn("pp-bibliographie", self.parsed.sections)
        self.assertIn("Grooms", self.html)
        self.assertIn("Kidder", self.html)
        self.assertIn("2024", self.html)
        self.assertIn("2023", self.html)
        self.assertIn("Cahokia", self.html)
        self.assertIn("/civilisations/ameriques/", self.html)
    def test_notes_anchors_and_image_rights(self):
        self.assertTrue(set(self.parsed.internal).issubset(self.parsed.targets))
        self.assertTrue(all(f"pp-ref-{i}" in self.parsed.targets for i in range(1,15)))
        self.assertEqual(len(self.parsed.images), 1)
        self.assertIn("Magnificent_Landformations_", self.parsed.images[0]["src"])
        self.assertIn("Jennifer R. Trotter", self.html)
        self.assertIn("creativecommons.org/licenses/by-sa/4.0", self.html)
        self.assertNotIn("2,5D", self.html)
    def test_mississippi_path_is_conditional(self):
        old = navigation.OUT
        try:
            with tempfile.TemporaryDirectory() as tmp:
                navigation.OUT = Path(tmp)
                a = {"url": URL, "title": "Poverty Point"}
                b = {"url": CAHOKIA, "title": "Cahokia"}
                absent = navigation.get_civilisations([b])
                navigation.create_civilisations([b], absent)
                html = (Path(tmp) / "civilisations/ameriques/index.html").read_text(encoding="utf-8")
                self.assertNotIn("Mississippi : deux âges de la monumentalité", html)
                self.assertNotIn(URL, html)
                present = navigation.get_civilisations([a,b])
                navigation.create_civilisations([a,b], present)
                html = (Path(tmp) / "civilisations/ameriques/index.html").read_text(encoding="utf-8")
                self.assertIn("Mississippi : deux âges de la monumentalité", html)
                self.assertIn(URL, html)
                self.assertIn(CAHOKIA, html)
        finally:
            navigation.OUT = old

if __name__ == "__main__":
    unittest.main()
