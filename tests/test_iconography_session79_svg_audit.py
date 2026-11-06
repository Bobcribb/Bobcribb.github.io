"""MYTHOS séance 79 : refuser les faux SVG dans les contrôles de publication."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts import verify_live_site as live

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("philosophie-iliade.html", "philosophie-odyssee.html",
         "philosophie-theogonie.html")
NEW_FIGURES = (
    ("philosophie-odyssee.html", "icono-odyssee-arc-preuve-autorite-s76-20261106",
     "/assets/philosophie/odyssee-arc-preuve-autorite-s76-20261106.svg"),
    ("philosophie-theogonie.html", "icono-theogonie-tartare-limites-s78-20261106",
     "/assets/philosophie/theogonie-tartare-limites-s78-20261106.svg"),
)


class IconographySession79SvgAudit(unittest.TestCase):
    def test_rejects_svg_marker_inside_html_and_malformed_xml(self):
        asset = "/assets/philosophie/exemple.svg"
        invalid = (
            b"<html><body><!-- <svg -->Page d'erreur</body></html>",
            b"<svg xmlns='http://www.w3.org/2000/svg'><g>",
            b"<html><svg xmlns='http://www.w3.org/2000/svg'></svg></html>",
        )
        for payload in invalid:
            with self.subTest(payload=payload[:35]):
                self.assertFalse(live.valid_local_illustration(asset, payload))
        self.assertTrue(live.valid_local_illustration(
            asset, b'<svg xmlns="http://www.w3.org/2000/svg"><title>Test</title></svg>'))

    def test_svg_inventory_rejects_html_that_contains_svg_literal(self):
        """Previously the test b'<svg' in body accepted this fake SVG."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "assets/philosophie"
            assets.mkdir(parents=True)
            asset = assets / "faux.svg"
            asset.write_bytes(b"<html><body><!-- <svg fake -->Not found</body></html>")
            for page in PAGES:
                (root / page).write_text(
                    '<html lang="fr"><img src="/assets/philosophie/faux.svg" alt="test"/></html>',
                    encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "SVG invalide"):
                live.svg_inventory(root)

    def test_newest_philosophy_diagrams_are_real_local_svg_documents(self):
        for page, figure_id, src in NEW_FIGURES:
            with self.subTest(figure=figure_id):
                self.assertEqual(live.RECENT_FIGURES.count((page, figure_id, src)), 1)
                svg = ROOT / src.lstrip("/")
                self.assertTrue(svg.is_file(), src)
                self.assertTrue(live.valid_local_illustration(src, svg.read_bytes()))
                metadata = live.figure_metadata(
                    (ROOT / page).read_text(encoding="utf-8"), figure_id, src)
                self.assertIn("assistance IA", metadata["status"])
                self.assertGreater(len(metadata["source_urls"]), 0)


if __name__ == "__main__":
    unittest.main()
