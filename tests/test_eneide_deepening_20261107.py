"""Vérifier la conservation et la visibilité des compléments Énéide du 7 novembre 2026."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "philosophie-eneide.html"
CORPUS = ROOT / "corpus/philosophie/eneide"
SAMPLES = {
    "04-chant-iv.md": "Microlecture philologique : « coniugium » et « culpa »",
    "06-chant-vi.md": "Les impératifs d’Anchise",
    "08-chant-viii.md": "L’ekphrasis et la fabrication d’une mémoire politique",
    "12-chant-xii.md": "Une supplication exactement formulée",
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

if __name__ == "__main__":
    unittest.main()
