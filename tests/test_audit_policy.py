"""Fail-closed regressions for the autonomous MYTHOS integrity audit."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_policy import publication_audit_fails


class PublicationAuditPolicyTests(unittest.TestCase):
    def test_clean_site_passes(self):
        self.assertFalse(publication_audit_fails([], []))

    def test_hard_errors_still_block(self):
        self.assertTrue(publication_audit_fails(["Media size/hash differs: foo.webp"], []))

    def test_broken_internal_links_and_resources_block(self):
        for item in (
            "Broken internal href from _site/index.html: /page-absente/",
            "Broken internal src from _site/chapitre/index.html: /images/manquante.webp",
            "Broken internal src from _site/chapitre/index.html: /assets/search.js",
            "Broken internal srcset from _site/chapitre/index.html: /assets/manquante-2x.webp",
            "Broken internal fragment: _site/index.html => /glossaire/#absent",
        ):
            with self.subTest(item=item):
                self.assertTrue(publication_audit_fails([], [item]))

    def test_html_and_external_dependency_warnings_block(self):
        for item in (
            "Duplicate HTML IDs: _site/etude/index.html => duplicate",
            "Missing title: _site/sans-titre/index.html",
            "Unsafe or malformed relative URL: _site/a.html => ../../../escape",
            "WordPress-dependent media URL in _site/a.html: https://bobmythos.wordpress.com/wp-content/uploads/image.jpg",
        ):
            with self.subTest(item=item):
                self.assertTrue(publication_audit_fails([], [item]))

    def test_no_warning_can_be_hidden_by_another_one(self):
        self.assertTrue(publication_audit_fails([], ["informational warning", "Broken internal href: /404/"]))


if __name__ == "__main__":
    unittest.main()
