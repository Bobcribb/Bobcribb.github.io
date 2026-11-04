"""Regression tests for navigation on historical dossier redirects.

The Greek thematic library preserves former URLs as lightweight redirects.
They intentionally have no main editorial nav; rebuild must not reject or
rewrite them, while substantive pages remain required to have a nav.
"""
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_navigation as navigation
from build_greek_folders import BASE, LEGACY_FOLDERS


class LegacyRedirectNavigationTests(unittest.TestCase):
    def test_greek_aliases_are_preserved_and_normal_pages_get_navigation(self):
        with TemporaryDirectory() as temp:
            out = Path(temp)
            original = {}
            for legacy, current in LEGACY_FOLDERS.items():
                target = out / BASE.strip("/") / legacy / "index.html"
                target.parent.mkdir(parents=True, exist_ok=True)
                raw = (
                    '<!doctype html><html lang="fr"><head>'
                    '<meta http-equiv="refresh" content="0;url='
                    + BASE + current + '/"></head><body><p>'
                    '<a href="' + BASE + current + '/">Ouvrir le dossier</a>'
                    '</p></body></html>'
                )
                target.write_text(raw, encoding="utf-8")
                original[target] = raw

            article = out / "philosophie" / "index.html"
            article.parent.mkdir(parents=True, exist_ok=True)
            article.write_text(
                '<!doctype html><html lang="fr"><body>'
                '<nav class="old-nav"><a href="/">Ancien menu</a></nav>'
                '<article><h1>Analyse conservée</h1><p>Texte intégral.</p></article>'
                '</body></html>', encoding="utf-8"
            )
            with patch.object(navigation, "OUT", out):
                changed = navigation.apply_navigation()
            self.assertEqual(changed, 1)
            for path, raw in original.items():
                self.assertEqual(path.read_text(encoding="utf-8"), raw)
            updated = article.read_text(encoding="utf-8")
            self.assertIn('class="site-nav"', updated)
            self.assertIn("Analyse conservée", updated)
            self.assertIn("Texte intégral.", updated)

    def test_redirects_outside_greek_dossiers_remain_unchanged(self):
        with TemporaryDirectory() as temp:
            out = Path(temp)
            path = out / "ancienne-adresse" / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = (
                '<html><head><meta content="0;url=/rubriques/" '
                'http-equiv="refresh"/></head><body>'
                '<a href="/rubriques/">Redirection</a></body></html>'
            )
            path.write_text(raw, encoding="utf-8")
            with patch.object(navigation, "OUT", out):
                changed = navigation.apply_navigation()
            self.assertEqual(changed, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), raw)

    def test_unexpected_page_without_menu_still_fails(self):
        with TemporaryDirectory() as temp:
            out = Path(temp)
            path = out / "philosophie" / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("<html><body><h1>Texte sans menu</h1></body></html>", encoding="utf-8")
            with patch.object(navigation, "OUT", out):
                with self.assertRaisesRegex(RuntimeError, "Aucun menu de navigation"):
                    navigation.apply_navigation()


if __name__ == "__main__":
    unittest.main()
