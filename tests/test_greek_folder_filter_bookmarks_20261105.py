"""Liens de filtres partageables : contrôle JS sur un DOM simulé.

Le corpus et la numérotation ne sont pas écrits par ce test.
"""
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GreekFolderBookmarksTests(unittest.TestCase):
    def test_js_browser_url_and_accessible_filter(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js absent ; contrôle JS disponible séparément")
        process = subprocess.run(
            [node, str(ROOT / "tests/greek_folder_filter_bookmarks_20261105.cjs")],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn("URL partageable", process.stdout)


if __name__ == "__main__":
    unittest.main()
