"""Régression de l'audit de la navigation MYTHOS : pas d'attente réseau indéfinie."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class BrowserNavigationReadinessTests(unittest.TestCase):
    def test_dom_content_loaded_then_real_masthead_and_status_checks(self):
        script = (ROOT / "scripts" / "verify_greek_navigation.cjs").read_text(encoding="utf-8")
        self.assertIn("waitUntil:'domcontentloaded',timeout:60000", script)
        self.assertNotIn("waitUntil:'networkidle'", script)
        self.assertIn("page.locator('.mythos-masthead').waitFor()", script)
        self.assertIn("assert.equal(response.status(),200,route)", script)
