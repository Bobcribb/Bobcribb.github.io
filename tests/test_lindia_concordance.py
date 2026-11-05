"""Garde de réconciliation 433/438 sans renumérotation ni perte documentaire."""
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_greek_folders import classify, LINDIA_433, LINDIA_438, LINDIA_NOTICE
from build_native import annotate_lindia_search
from build_greek_corpus import primary_folder_urls

class LindiaConcordanceTests(unittest.TestCase):
    def test_same_thematic_section_and_unique_urls(self):
        self.assertNotEqual(LINDIA_433, LINDIA_438)
        for url in (LINDIA_433, LINDIA_438):
            folder, section = classify(url, "Athéna Lindia", "Chapitre universitaire")
            self.assertEqual(folder, "cultes-sanctuaires")
            self.assertIn("Lindos", section)
        self.assertEqual(classify(LINDIA_433, "", "Chapitre universitaire"),
                         classify(LINDIA_438, "", "Chapitre universitaire"))

    def test_concordance_is_a_secondary_link_not_a_third_thematic_assignment(self):
        """Two primary monographs; their shared notice remains independently readable."""
        catalogue = {LINDIA_433, LINDIA_438, LINDIA_NOTICE}
        self.assertEqual(primary_folder_urls(catalogue), {LINDIA_433, LINDIA_438})
        self.assertEqual(
            primary_folder_urls(catalogue | {"#concordance-athena-lindia",
                                            "https://example.org/ancient-source"}),
            {LINDIA_433, LINDIA_438},
        )

    def test_search_retains_two_distinct_entries(self):
        entries = [
            {"url": LINDIA_433, "title": "Chapitre 433", "excerpt": ""},
            {"url": LINDIA_438, "title": "Chapitre 438", "excerpt": ""},
        ]
        annotate_lindia_search(entries)
        self.assertEqual(len({x["url"] for x in entries}), 2)
        self.assertIn("Pindare", entries[0]["excerpt"])
        self.assertIn("enquête", entries[1]["excerpt"].lower())
        self.assertLessEqual(max(len(x["excerpt"]) for x in entries), 190)

    def test_notice_is_public_page_with_bidirectional_links(self):
        page = ROOT / LINDIA_NOTICE.strip("/") / "index.html"
        doc = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        links = {a.get("href") for a in doc.select("a[href]")}
        self.assertTrue({LINDIA_433, LINDIA_438}.issubset(links))
        self.assertIn("Lindos II", doc.get_text(" ", strip=True))
        self.assertTrue(doc.select_one("link[rel=canonical]"))

    def test_preserves_both_full_manuscripts_and_reciprocal_links(self):
        srcs = [
            ROOT / "chapitres/encyclopedie" / (LINDIA_433.strip("/").split("/")[-1] + ".md"),
            ROOT / "chapitres/encyclopedie" / (LINDIA_438.strip("/").split("/")[-1] + ".md"),
        ]
        data = [s.read_text(encoding="utf-8") for s in srcs]
        self.assertGreater(len(data[0]), 60000)
        self.assertGreater(len(data[1]), 50000)
        self.assertIn(LINDIA_NOTICE, data[0])
        self.assertIn(LINDIA_NOTICE, data[1])
        self.assertIn("chapitre-438-", data[0])
        self.assertIn("chapitre-433-", data[1])
        self.assertIn("attribuée au chapitre 438", data[1])
        self.assertNotIn("destinée à l’attribution ultérieure", data[1])
        note = (ROOT / "docs/CONCORDANCE_ATHENA_LINDIA_433_438.md").read_text(encoding="utf-8")
        self.assertIn("SIG³ 725", note)
        self.assertIn("Amasis", note)
        self.assertIn("Chaniotis", note)

if __name__ == "__main__":
    unittest.main()
