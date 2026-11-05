"""Non-régression de la photographie Behistun sur le site HTTPS MYTHOS."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_live_site as live


class BehistunPublicPublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.photo = bytes.fromhex("ffd8ff") + b"documentary-jpeg-fixture"
        image_path = self.root / live.BEHISTUN_IMAGE.lstrip("/")
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image_path.write_bytes(self.photo)
        self.page = (
            '<html><body><main><section id="etude-behistun"><div>'
            '<a class="portal-card" href="' + live.BEHISTUN_STUDY + '">'
            '<img class="mythos-card-image" src="' + live.BEHISTUN_IMAGE + '" '
            'alt="Relief de Darius Ier et inscription trilingue à Behistun.">'
            '<strong>Behistun : Darius et les inscriptions</strong>'
            '<span>Photo : Mahdimanavimvi (2018), CC BY-SA 4.0, '
            'sources et bibliographie.</span></a></div></section></main></body></html>'
        ).encode("utf-8")
        p = self.root / "civilisations/index.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(self.page)

    def site_fetch(self, url):
        if url.endswith(live.BEHISTUN_IMAGE):
            return 200, "image/jpeg", self.photo
        if url.endswith(live.BEHISTUN_PAGE):
            return 200, "text/html", self.page
        raise AssertionError("Unexpected URL: " + url)

    def test_public_card_and_jpeg_match_local_build(self):
        with patch.object(live, "fetch", side_effect=self.site_fetch):
            checks = live.verify_public_behistun("https://example.test", self.root)
        self.assertEqual([c["url"] for c in checks],
                         [live.BEHISTUN_PAGE, live.BEHISTUN_IMAGE])
        self.assertTrue(all(c["valid"] for c in checks))
        self.assertTrue(checks[1]["sha256_matches_build"])

    def test_outdated_portal_missing_image_must_fail(self):
        old_html = self.page.replace(
            ('<img class="mythos-card-image" src="' + live.BEHISTUN_IMAGE + '" '
             'alt="Relief de Darius Ier et inscription trilingue à Behistun.">').encode(),
            b"",
        )

        def stale_page_fetch(url):
            if url.endswith(live.BEHISTUN_PAGE):
                return 200, "text/html", old_html
            return self.site_fetch(url)

        with patch.object(live, "fetch", side_effect=stale_page_fetch):
            checks = live.verify_public_behistun("https://example.test", self.root)
        self.assertFalse(checks[0]["valid"])
        self.assertTrue(checks[1]["valid"])

    def test_altered_public_jpeg_must_fail_sha256(self):
        def altered_photo_fetch(url):
            if url.endswith(live.BEHISTUN_IMAGE):
                return 200, "image/jpeg", self.photo + b"tampered"
            return self.site_fetch(url)

        with patch.object(live, "fetch", side_effect=altered_photo_fetch):
            checks = live.verify_public_behistun("https://example.test", self.root)
        self.assertTrue(checks[0]["valid"])
        self.assertFalse(checks[1]["valid"])

    def test_source_image_missing_is_not_silently_ignored(self):
        (self.root / live.BEHISTUN_IMAGE.lstrip("/")).unlink()
        with self.assertRaises(FileNotFoundError):
            live.verify_public_behistun("https://example.test", self.root)


if __name__ == "__main__":
    unittest.main()
