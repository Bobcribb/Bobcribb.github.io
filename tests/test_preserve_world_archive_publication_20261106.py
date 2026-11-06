"""Préserver les archives XIV/XV pendant la reconstruction et le déploiement."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import sys
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from improve_reading import add_reading
from publish_site import CANONICAL_WORLD_ARCHIVES, overlay_render_preserving_archives

EXPECTED_GIT_BLOBS = {
    "bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/index.html":
        "7ff155c4bc4eea7fb01560af3cbb61cd5519deb9",
    "bibliotheque-mythologies-du-monde/mythos-volume-15-philippines-ifugao-hudhud/index.html":
        "58ef11d17522225187e6f1437e70277c3c23d154",
}


class WorldArchivePreservationTests(unittest.TestCase):
    def test_source_archives_equal_human_verified_originals(self):
        self.assertEqual(set(CANONICAL_WORLD_ARCHIVES), set(EXPECTED_GIT_BLOBS))
        for relative, expected_blob in EXPECTED_GIT_BLOBS.items():
            with self.subTest(relative=relative):
                raw = (ROOT / relative).read_bytes()
                blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
                self.assertEqual(blob, expected_blob)

    def test_reader_preserves_authored_figures_and_navigation_twice(self):
        for relative, css in (
            (CANONICAL_WORLD_ARCHIVES[0], "figure.mythos-khmer-figure"),
            (CANONICAL_WORLD_ARCHIVES[1], "figure.mythos-ifugao-figure"),
        ):
            with self.subTest(relative=relative):
                doc = BeautifulSoup((ROOT / relative).read_text(encoding="utf-8"), "html.parser")
                authored = doc.select_one(css)
                self.assertIsNotNone(authored)
                before = str(authored)
                for _ in range(2):
                    add_reading(doc, "/" + relative.replace("index.html", ""), {"words": 1200, "minutes": 7})
                    self.assertEqual(str(doc.select_one(css)), before)
                    self.assertEqual(len(doc.select(".mythos-reader")), 1)
                    self.assertEqual(len(doc.select(".mythos-reading-toc")), 1)
                    self.assertEqual(len(doc.select("nav.reader-bottom")), 1)

    def test_public_render_does_not_overwrite_source_archive_bytes(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in CANONICAL_WORLD_ARCHIVES:
                source = root / relative
                built = root / "_site" / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                built.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(b"author-preserved-archive\\n")
                built.write_bytes(b"responsive-public-render\\n")
            other = root / "_site" / "philosophie-iliade.html"
            other.write_text("updated public reading", encoding="utf-8")
            overlay_render_preserving_archives(root)
            for relative in CANONICAL_WORLD_ARCHIVES:
                self.assertEqual((root / relative).read_bytes(), b"author-preserved-archive\\n")
                self.assertEqual((root / "_site" / relative).read_bytes(), b"responsive-public-render\\n")
            self.assertEqual((root / "philosophie-iliade.html").read_text(), "updated public reading")

    def test_minimal_repositories_without_historical_archives_still_publish(self):
        # Les tests de course Git construisent des dépôts restreints.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_site").mkdir()
            (root / "_site" / "index.html").write_text("latest render", encoding="utf-8")
            overlay_render_preserving_archives(root)
            self.assertEqual((root / "index.html").read_text(), "latest render")

    def test_missing_rendered_archive_blocks_publication(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in CANONICAL_WORLD_ARCHIVES:
                source = root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text("source", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "archive historique absente"):
                overlay_render_preserving_archives(root)


if __name__ == "__main__":
    unittest.main()
