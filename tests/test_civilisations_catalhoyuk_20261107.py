"""Çatalhöyük : sources, classement, navigation réciproque et photographie autorisée."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_navigation import get_civilisations, group_continent
URL = "/bibliotheque-mythologies-du-monde/civilisations-catalhoyuk-neolithique-anatolie/"
ARTICLE = ROOT / "bibliotheque-mythologies-du-monde/civilisations-catalhoyuk-neolithique-anatolie/index.html"
PREVIOUS = ROOT / "bibliotheque-mythologies-du-monde/civilisations-histoire-hittites-anatolie/index.html"
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set(); self.links=[]; self.sections=0; self.canonical=None; self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="a" and a.get("href","").startswith("#"): self.links.append(a["href"][1:])
        if tag=="link" and a.get("rel")=="canonical": self.canonical=a.get("href")
        if tag=="section" and "mythos-critical-chapter" in a.get("class","").split(): self.sections+=1
        if tag=="img": self.images.append(a)
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=ARTICLE.read_text(encoding="utf-8")
        cls.prev=PREVIOUS.read_text(encoding="utf-8")
        cls.p=Inspector(); cls.p.feed(cls.html)
    def test_asian_index(self):
        a={"url":URL,"title":"Çatalhöyük"}
        b={"url":"/bibliotheque-mythologies-du-monde/civilisations-histoire-hittites-anatolie/","title":"Hittites"}
        self.assertEqual(group_continent(a),"asie")
        self.assertEqual(len(get_civilisations([a,b])["asie"]),2)
    def test_complete_and_canonical(self):
        self.assertEqual(self.p.canonical,"https://bobmythos.fr"+URL)
        self.assertEqual(self.p.sections,20)
        self.assertIn("10.1126/science.adr2915",self.html)
        self.assertIn("131 paléogénomes",self.html)
    def test_anchors_and_rights(self):
        self.assertTrue(set(self.p.links).issubset(self.p.ids))
        self.assertTrue(all("cat-ref-"+str(i) in self.p.ids for i in range(1,10)))
        self.assertEqual(len(self.p.images),1)
        self.assertIn("CatalHoyukSouthArea.JPG",self.p.images[0]["src"])
        self.assertIn("CC BY-SA 3.0",self.html)
    def test_reciprocal_link_without_filiation(self):
        self.assertIn('href="'+URL+'"',self.prev)
        self.assertEqual(self.prev.count('id="catalhoyuk-parcours-anatolie"'),1)
        self.assertIn("plusieurs millénaires",self.prev)
        self.assertIn("/civilisations/asie/",self.html)
        self.assertNotIn("Grande Encyclopédie",self.html)
if __name__=="__main__": unittest.main()
