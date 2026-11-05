"""Garde de couverture du portail de mythologie comparée, sans modifier les monographies."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_navigation as navigation


class ComparativePortalCoverageTests(unittest.TestCase):
    def test_unclassified_mc_071_remains_visible_and_classified_mc_070_is_not_duplicated(self):
        mc070 = ("/chapitres/comparatif/"
                 "volume-ccxlviii-mc-070-le-nom-des-dieux-isis-re-marduk-zeus-veda-exode-pouvoir-de-nommer/")
        mc071 = ("/chapitres/comparatif/"
                 "volume-ccli-mc-071-qui-ecrit-pour-les-dieux-nisaba-nabu-thot-seshat-ecriture-et-autorite/")
        unrelated = "/chapitres/encyclopedie/notice-sans-rapport/"
        entries = [
            {"url": mc070, "title": "MC-070 — Nommer les dieux : les cinquante noms de Marduk"},
            {"url": mc071, "title": "MC-071 — Qui écrit pour les dieux ? Nisaba, Nabû, Thot et Seshat"},
            {"url": unrelated, "title": "Notice sans rapport"},
        ]
        with patch.object(navigation, "write") as write:
            navigation.create_comparative_mythology(entries)
        write.assert_called_once()
        self.assertEqual(write.call_args.args[0], "mythologie-comparee")
        doc = BeautifulSoup(write.call_args.args[1], "html.parser")
        links = [a["href"] for a in doc.select(".comparison-section .comparison-documents a[href]")]
        self.assertEqual(links.count(mc070), 1)
        self.assertEqual(links.count(mc071), 1)
        self.assertNotIn(unrelated, links)
        additional = doc.select_one("#comparaison-autres")
        self.assertIsNotNone(additional)
        self.assertEqual([a["href"] for a in additional.select("a[href]")], [mc071])
        self.assertEqual(len(doc.select('nav.comparison-toc a[href="#comparaison-autres"]')), 1)

    def test_missing_theme_never_hides_an_attributed_comparative_article(self):
        entries = [
            {"url": "/chapitres/comparatif/volume-cx-unclassified-source/",
             "title": "Écriture et mémoire sans mots-clés thématiques"},
            {"url": "/chapitres/comparatif/volume-cxi-unclassified-source/",
             "title": "Traces du passé et archives humaines"},
        ]
        with patch.object(navigation, "write") as write:
            navigation.create_comparative_mythology(entries)
        doc = BeautifulSoup(write.call_args.args[1], "html.parser")
        targets = [a["href"] for a in doc.select("#comparaison-autres a[href]")]
        self.assertEqual(set(targets), {e["url"] for e in entries})
        self.assertEqual(len(targets), len(entries))


if __name__ == "__main__":
    unittest.main()
