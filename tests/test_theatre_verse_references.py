"""Contrôle philologique minimal des repères réellement présents dans les textes."""
import sys
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_navigation import detect_verse_references


class VerseReferenceTests(unittest.TestCase):
    def doc(self, content):
        return BeautifulSoup("<article>" + content + "</article>", "html.parser").article

    def test_headings_in_aristophanes_peace_are_detected_without_invention(self):
        spans = [(1,81),(82,176),(177,235),(236,295),(296,360),
                 (361,458),(459,519),(520,602),(603,728),(729,816),
                 (819,921),(922,1042),(1043,1126),(1127,1190),
                 (1191,1264),(1265,1315),(1316,1357)]
        article = self.doc("".join(
            f"<h3>{first}–{last} — Commentaire de scène</h3>"
            for first, last in spans
        ))
        self.assertEqual(detect_verse_references(article), spans)

    def test_bibliographic_pagination_is_not_a_verse_range(self):
        article = self.doc(
            "<h2>Bibliographie</h2><p>Greece and Rome (1982), p. 42–52 ; "
            "Classical Quarterly (1983), p. 412–420.</p>"
        )
        self.assertEqual(detect_verse_references(article), [])

    def test_existing_explicit_vers_references_are_preserved(self):
        article = self.doc("<p>Comparer vers 25–38, vers 50 et vers 25–38.</p>")
        self.assertEqual(detect_verse_references(article), [(25,38),(50,50)])

    def test_two_unrelated_numbered_titles_are_not_a_false_positive(self):
        article = self.doc(
            "<h2>1–5 — Section</h2><h2>6–12 — Section</h2>"
            "<p>Ouvrage, p. 120–155.</p>"
        )
        self.assertEqual(detect_verse_references(article), [])


if __name__ == "__main__":
    unittest.main()
