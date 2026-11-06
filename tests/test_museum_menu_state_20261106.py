"""Régression du menu MYTHOS : libellé dynamique, clavier et clic extérieur.

Ne touche ni aux textes universitaires ni aux réglages des automations.
"""
from pathlib import Path
import shutil
import subprocess
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


class MuseumMenuStateTests(unittest.TestCase):
    def test_real_javascript_menu_behaviour(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js absent ; vérification dans GitHub Actions")
        result = subprocess.run(
            [node, str(ROOT / "tests/museum_menu_state_20261106.cjs")],
            cwd=ROOT, capture_output=True, text=True,
            check=False, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("MYTHOS menu state", result.stdout)

    def test_native_menu_remains_readable_without_javascript(self):
        # Le <details> natif reste ouvert au clavier et sans JavaScript.
        for rel in ("index.html", "mythologie-grecque/index.html",
                    "theatre/index.html", "origines-du-sacre/index.html"):
            with self.subTest(page=rel):
                doc = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"),
                                   "html.parser")
                menu = doc.select_one("details.mythos-menu")
                self.assertIsNotNone(menu)
                trigger = menu.select_one("summary")
                self.assertIsNotNone(trigger)
                self.assertEqual(trigger.get("aria-label"), "Ouvrir le menu")
                nav = menu.select_one("nav[aria-label]")
                self.assertIsNotNone(nav)
                self.assertEqual(len(nav.select('a[href="/mythologie-grecque/"]')), 1)
                self.assertFalse(nav.select('a[href="/grande-encyclopedie/"]'))


if __name__ == "__main__":
    unittest.main()
