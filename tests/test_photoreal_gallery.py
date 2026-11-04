"""Pure, offline tests of the MYTHOS image verification guard."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.verify_photoreal_gallery import ImagesInGallery, inventory, is_webp


class TestPhotorealGalleryVerification(unittest.TestCase):
    def test_webp_signature(self):
        self.assertTrue(is_webp(b"RIFF" + b"\x04\x00\x00\x00" + b"WEBP" + b"abc"))
        self.assertFalse(is_webp(b"<html>404 not found</html>"))
        self.assertFalse(is_webp(b"RIFF" + b"\x04\x00\x00\x00" + b"PNG "))

    def test_image_src_is_a_real_img_tag(self):
        parser = ImagesInGallery()
        parser.feed('<a href="/x.webp">image</a><img loading="lazy" src="/assets/reconstitutions-3d/x.webp">')
        self.assertEqual(parser.sources, {"/assets/reconstitutions-3d/x.webp"})

    def test_duplicate_slug_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "assets/reconstitutions-3d/catalogue-photorealiste.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"count": 2, "entries": [
                {"slug": "duplicate", "src": "/assets/reconstitutions-3d/a.webp"},
                {"slug": "duplicate", "src": "/assets/reconstitutions-3d/b.webp"}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dupliqués"):
                inventory(root)


if __name__ == "__main__":
    unittest.main()
