"""Vérifier la conservation et la visibilité des compléments Énéide du 7 novembre 2026."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "philosophie-eneide.html"
CORPUS = ROOT / "corpus/philosophie/eneide"
SAMPLES = {
    "00-introduction.md": "La fondation romaine comme récit de plusieurs temps historiques",
    "01-chant-i.md": "Le proème et la question du jugement porté sur les dieux",
    "02-chant-ii.md": "Lecture rapprochée : Priam, Pyrrhus et les droits du suppliant",
    "03-chant-iii.md": "Polydore : quand le sol révèle le crime",
    "04-chant-iv.md": "Microlecture philologique : « coniugium » et « culpa »",
    "05-chant-v.md": "Les jeux d’Anchise : l’honneur comme distribution contestable",
    "06-chant-vi.md": "Les impératifs d’Anchise",
    "07-chant-vii.md": "« Acheronta movebo »",
    "08-chant-viii.md": "L’ekphrasis et la fabrication d’une mémoire politique",
    "09-chant-ix.md": "« Dine hunc ardorem »",
    "10-chant-x.md": "Lausus, miroir de la pietas du vainqueur",
    "11-chant-xi.md": "La trêve des morts : un minimum commun entre ennemis",
    "12-chant-xii.md": "Une supplication exactement formulée",
    "13-pietas-destin.md": "La pietas entre fidélité familiale et responsabilité publique",
    "14-empire-memoire.md": "L’augustéisme de l’épopée",
    "15-philosophies-comparaisons.md": "Hegel, téléologie et résistance des existences singulières",
    "16-poetique-conclusion.md": "Récits enchâssés, récits de survivants et autorité de la voix",
    "17-reperes-et-sources.md": "Appareil critique complémentaire",
}

class EneideDeepeningTest(unittest.TestCase):
    def test_sources_et_lecteur_contiennent_chaque_ajout(self):
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(18, len(doc.select("section.philo-chapter")))
        txt = doc.get_text(" ", strip=True)
        for name, signature in SAMPLES.items():
            raw = (CORPUS / name).read_text(encoding="utf-8")
            self.assertIn(signature, raw)
            self.assertIn(signature, txt)
        self.assertIn("Le PDF de 84 pages", txt)

    def test_references_et_titles_sont_uniques(self):
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        ids = [node["id"] for node in doc.select("[id]")]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("10.1017/S000983881600077X",
                      (CORPUS / "17-reperes-et-sources.md").read_text(encoding="utf-8"))
        self.assertIn("vitaque cum gemitu fugit indignata sub umbras",
                      (CORPUS / "12-chant-xii.md").read_text(encoding="utf-8"))


    def test_all_eighteen_sources_match_the_html_chapter_map(self):
        """Ne jamais perdre une section ni casser les ancres lors d'un enrichissement."""
        import re
        doc = BeautifulSoup(STUDY.read_text(encoding="utf-8"), "html.parser")
        names = [
            "00-introduction.md", "01-chant-i.md", "02-chant-ii.md",
            "03-chant-iii.md", "04-chant-iv.md", "05-chant-v.md",
            "06-chant-vi.md", "07-chant-vii.md", "08-chant-viii.md",
            "09-chant-ix.md", "10-chant-x.md", "11-chant-xi.md",
            "12-chant-xii.md", "13-pietas-destin.md",
            "14-empire-memoire.md", "15-philosophies-comparaisons.md",
            "16-poetique-conclusion.md", "17-reperes-et-sources.md",
        ]
        chapters = doc.select("section.philo-chapter")
        self.assertEqual(len(chapters), len(names))
        for i, name in enumerate(names):
            text = (CORPUS / name).read_text(encoding="utf-8")
            title = re.search(r"^# (.+)$", text, flags=re.M).group(1)
            headings = re.findall(r"^## (.+)$", text, flags=re.M)
            chapter = chapters[i]
            heading = chapter.select_one(f'h2[id="eneide-{i:02}"]')
            self.assertIsNotNone(heading, name)
            self.assertEqual(heading.get_text(" ", strip=True), title, name)
            anchors = chapter.select("h3[id]")
            self.assertEqual(len(anchors), len(headings), name)
            for j, expected in enumerate(headings):
                subheading = chapter.select_one(f'h3[id="eneide-{i:02}-{j:02}"]')
                self.assertIsNotNone(subheading, name + ": " + expected)
                self.assertEqual(subheading.get_text(" ", strip=True), expected)
        shelf = doc.select("#eneide-manuscrits-originaux")
        self.assertLessEqual(len(shelf), 1)
        if shelf:
            self.assertEqual(
                len(shelf[0].select(".mythos-eneide-source-grid li a")), 18
            )

if __name__ == "__main__":
    unittest.main()
