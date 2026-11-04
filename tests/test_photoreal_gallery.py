"""Pure, offline tests of the MYTHOS image verification guard."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.verify_photoreal_gallery import ImagesInGallery, gallery_markup_failures, inventory, is_webp


class TestPhotorealGalleryVerification(unittest.TestCase):
    def test_public_image_does_not_replace_missing_scientific_notice(self):
        entry = {"slug": "temple", "src": "/assets/reconstitutions-3d/temple.webp",
                 "source_url": "https://museum.example/temple"}
        valid = '''<article id="temple"><figure>
        <img src="/assets/reconstitutions-3d/temple.webp" alt="Temple interprétatif">
        <figcaption>Temple, IVe siècle</figcaption></figure>
        <div class="r3d-science"><p>Les vestiges attestent le plan.</p>
        <p>Degré de certitude : élevé pour le plan.</p>
        <a href="https://museum.example/temple">Source institutionnelle</a></div></article>'''
        self.assertEqual(gallery_markup_failures(valid, [entry]), [])
        for broken in (
            valid.replace('<figcaption>Temple, IVe siècle</figcaption>', ''),
            valid.replace('class="r3d-science"', 'class="removed"'),
            valid.replace('https://museum.example/temple', 'https://museum.example/other'),
            valid.replace('id="temple"', 'id="removed"'),
            valid.replace('<article ', '<article hidden '),
            valid + '<img src="/assets/reconstitutions/temple.svg">',
        ):
            with self.subTest(markup=broken):
                self.assertTrue(gallery_markup_failures(broken, [entry]))

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
