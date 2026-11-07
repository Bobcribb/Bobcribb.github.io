"""Conservation intégrale du volume historique XIV Khmer et Angkor."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import re
import shutil
import sys
import unittest
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/index.html"
NAV = ROOT / "scripts/build_navigation.py"
CSS = ROOT / "assets/mythos-museum.css"
OLDER = ROOT / "bibliotheque-mythologies-du-monde/civilisations-histoire-khmers-angkor/index.html"
SOURCE_BLOB = "b04f7fdecb1ef6c76fb394797b6a58b477e8462d"
SOURCE_LEN = 47507
URL = "/bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/"
PHOTO = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Angkor_Wat_-_Churning_of_the_Sea_of_Milk.JPG/640px-Angkor_Wat_-_Churning_of_the_Sea_of_Milk.JPG"
sys.path.insert(0, str(ROOT / "scripts"))
from apply_museum_design import apply as apply_museum_design

def original_html():
    raw = PAGE.read_text(encoding="utf-8")
    match = re.search(r"<!--MYTHOS-KHMER-SOURCE-BEGIN-->\n(.*?)\n<!--MYTHOS-KHMER-SOURCE-END-->", raw, re.S)
    if not match:
        raise AssertionError("Bornes du contenu source manquantes")
    marked = match.group(1)
    # Les illustrations documentaires additionnelles sont insérées dans le
    # lecteur, mais restent hors du blob source universitaire protégé.
    marked = re.sub(
        r'<figure class="mythos-editorial-inline"[^>]*>.*?</figure>',
        "", marked, flags=re.S,
    )
    # Les identifiants de lecture sont ajoutés après les classes h2/h3.
    # Les retirer uniquement pour vérifier le SHA du manuscrit conservé.
    return re.sub(r'\s+id="khmer-lecture-\d+"', "", marked)

class KhmerHistoricalVolumeTests(unittest.TestCase):
    def test_original_html_entire_and_sha(self):
        source = original_html()
        binary = source.encode("utf-8")
        blob_sha = hashlib.sha1(b"blob " + str(len(binary)).encode() + b"\0" + binary).hexdigest()
        self.assertEqual(len(source), SOURCE_LEN)
        self.assertEqual(blob_sha, SOURCE_BLOB)
        self.assertEqual(len(re.findall(r"<h2\b", source)), 20)
        self.assertEqual(len(re.findall(r"<h3\b", source)), 43)
        for token in ("Angkor Wat", "Viṣṇu", "Śiva", "Sources institutionnelles", "Smarthistory"):
            self.assertIn(token, source)
    def test_toc_anchors_and_historical_not_canonical_cote(self):
        doc = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(doc.select_one(".mythos-original-study")["data-source-archive"], "wordpress-1138")
        self.assertEqual(doc.select_one(".mythos-original-study")["data-original-git-blob"], SOURCE_BLOB)
        self.assertEqual(len(doc.select("#texte-integral-khmer-angkor h2[id^='khmer-lecture-']")), 20)
        self.assertEqual(len(doc.select("#texte-integral-khmer-angkor h3[id^='khmer-lecture-']")), 43)
        links = doc.select("details.mythos-khmer-toc a[href^='#khmer-lecture-']")
        self.assertEqual(len(links), 63)
        self.assertEqual(len(set(a["href"] for a in links)), 63)
        for a in links:
            self.assertIsNotNone(doc.find(id=a["href"][1:]))
        all_ids = [node["id"] for node in doc.select("[id]")]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertIn("Volume XIV", doc.title.text)
        self.assertNotIn("Chapitre {{numero}}", str(doc))
    def test_photo_license_and_bidirectional_links(self):
        doc = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        photo = doc.select_one("figure.mythos-khmer-figure img")
        self.assertEqual(photo["src"], PHOTO)
        self.assertIn("barattage", photo["alt"])
        credit = doc.select_one("figure.mythos-khmer-figure figcaption").get_text(" ", strip=True)
        self.assertIn("Jadamta", credit)
        self.assertIn("2012", credit)
        self.assertIn("CC BY-SA 3.0", credit)
        self.assertIn(URL, NAV.read_text(encoding="utf-8"))
        old = BeautifulSoup(OLDER.read_text(encoding="utf-8"), "html.parser")
        self.assertIsNotNone(old.select_one('nav[data-mythos-khmer-reciprocal] a[href="' + URL + '"]'))
        self.assertIsNotNone(doc.select_one('a[href="/bibliotheque-mythologies-du-monde/civilisations-histoire-khmers-angkor/"]'))
    def test_museum_rebuild_preserves_original_prose(self):
        before = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
        expected = before.select_one(".mythos-original-study").get_text(" ", strip=True)
        with TemporaryDirectory() as temp:
            path = Path(temp) / "bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/index.html"
            path.parent.mkdir(parents=True)
            shutil.copyfile(PAGE, path)
            for _ in range(2):
                self.assertEqual(apply_museum_design(temp), 1)
                after = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual(after.select_one(".mythos-original-study").get_text(" ", strip=True), expected)
                self.assertEqual(after.body["data-mythos-design"], "20261104")
                self.assertIsNotNone(after.select_one(".mythos-masthead"))
                self.assertIsNotNone(after.select_one(".mythos-banner"))
    def test_card_images_survive_two_museum_passes(self):
        with TemporaryDirectory() as temp:
            p = Path(temp) / "mythologies/index.html"
            p.parent.mkdir(parents=True)
            p.write_text('<html><head><title>MYTHOS</title></head><body><main><h1>MYTHOS</h1><div class="portal-grid"><a class="portal-card" href="' + URL + '"><img class="mythos-card-image" data-mythos-card-source="khmer-angkor-jadamta-2012" src="' + PHOTO + '" alt="Relief d’Angkor"><strong>Khmer et Angkor</strong></a></div></main></body></html>', encoding="utf-8")
            for _ in range(2):
                self.assertEqual(apply_museum_design(temp), 1)
                doc = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                self.assertEqual([x["src"] for x in doc.select("a.portal-card img.mythos-card-image")], [PHOTO])
    def test_responsive_and_no_legacy_vector(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn(".mythos-khmer-figure", css)
        self.assertIn("@media(max-width:720px)", css)
        self.assertIn("min-height:48px", css)
        self.assertNotIn("mythos-hero.svg", PAGE.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
