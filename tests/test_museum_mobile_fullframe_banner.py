"""MYTHOS: keep both ends of the statue/temple banner visible on phones.

The artwork is a very wide 2172 x 724 WebP. A fixed 160 px background height
cropped both lateral ends on narrow viewports; fit it to the viewport width.
This verifies source design only; a browser screenshot is still needed for QA.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MuseumMobileBannerTests(unittest.TestCase):
    def test_mobile_banner_shows_both_lateral_ends(self):
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        blocks = re.findall(
            r"@media\(max-width:700px\)\{\s*body\.mythos-design "
            r"\.mythos-banner\{([^{}]+)\}", css
        )
        self.assertTrue(blocks, "Expected the narrow-screen banner override")
        # Last matching rule takes priority over older mobile defaults.
        self.assertIn("background-size:100% auto!important", blocks[-1])
        self.assertIn("background-position:center top!important", blocks[-1])
        self.assertIn("background-color:#090e10!important", blocks[-1])

    def test_original_museum_image_and_home_layout_are_preserved(self):
        banner = ROOT / "assets/mythos-museum-banner.webp"
        self.assertTrue(banner.is_file())
        self.assertEqual(banner.read_bytes()[:4], b"RIFF")
        css = (ROOT / "assets/mythos-museum.css").read_text(encoding="utf-8")
        self.assertIn("/assets/mythos-museum-banner.webp", css)
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="mythos-banner"', home)
        self.assertIn('class="mythos-home-toc"', home)
        self.assertIn('href="/mythologie-grecque/"', home)


if __name__ == "__main__":
    unittest.main()
