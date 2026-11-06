"""Régression MYTHOS : menu et recherche tactiles, sans modifier les articles.

Les cibles de l'en-tête atteignent au moins 44 × 44 px, y compris en vue
mobile compacte. Le contrôle navigateur complémentaire mesure le rendu réel.
"""
from pathlib import Path
import re
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MARKER = "/* MYTHOS — en-tête tactile accessible, 6 novembre 2026."


class MuseumHeaderTouchTargetsTests(unittest.TestCase):
    def css_patch(self):
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertEqual(css.count(MARKER), 1)
        return css.split(MARKER, 1)[1]

    def test_search_and_menu_have_44px_clickable_surfaces(self):
        css = self.css_patch()
        for selector in (
            "body.mythos-design .mythos-search-link",
            "body.mythos-design .mythos-menu>summary",
        ):
            matches = re.findall(re.escape(selector) + r"\s*\{([^{}]+)\}", css)
            self.assertEqual(len(matches), 1, selector)
            block = matches[0]
            for rule in ("width:44px", "height:44px",
                         "min-width:44px", "min-height:44px"):
                self.assertIn(rule, block, (selector, rule))
        # Le symbole de recherche reste petit à l'intérieur de sa grande cible.
        icon_rule = re.search(
            r"body\.mythos-design \.mythos-search-link>svg\s*\{([^{}]+)\}",
            css,
        )
        self.assertIsNotNone(icon_rule)
        self.assertIn("width:23px", icon_rule.group(1))
        self.assertIn("height:23px", icon_rule.group(1))

    def test_compact_mobile_header_avoids_large_gaps(self):
        css = self.css_patch()
        self.assertIn("@media(max-width:420px)", css)
        self.assertIn(".mythos-masthead{gap:8px!important}", css)
        self.assertIn(".mythos-header-tools{gap:6px!important}", css)
        self.assertIn("font-size:clamp(22px,6vw,26px)!important", css)
        self.assertIn(".mythos-menu[open]>summary", css)
        self.assertIn(".mythos-menu>summary:focus-visible", css)

    def test_controls_keep_semantic_labels_on_existing_public_pages(self):
        paths = [
            ROOT / "index.html",
            ROOT / "mythologie-grecque/index.html",
            ROOT / "theatre/index.html",
            ROOT / "origines-du-sacre/index.html",
        ]
        for path in paths:
            with self.subTest(page=path.relative_to(ROOT)):
                doc = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
                search = doc.select_one(".mythos-masthead a.mythos-search-link")
                menu = doc.select_one(".mythos-masthead details.mythos-menu")
                summary = doc.select_one(".mythos-masthead details.mythos-menu > summary")
                self.assertIsNotNone(search)
                self.assertEqual(search.get("href"), "/recherche/")
                self.assertTrue(search.get("aria-label"))
                self.assertIsNotNone(menu)
                self.assertIsNotNone(summary)
                self.assertTrue(summary.get("aria-label"))
                self.assertIsNotNone(menu.select_one("nav[aria-label]"))
                self.assertFalse(summary.select("a,button"))
                self.assertEqual(
                    len(menu.select('nav a[href="/mythologie-grecque/"]')), 1
                )


if __name__ == "__main__":
    unittest.main()
