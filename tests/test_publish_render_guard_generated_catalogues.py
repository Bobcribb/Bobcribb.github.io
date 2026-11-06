"""Regression checks for GitHub Pages generated-catalogue publication.

These tests use an isolated Git index. They must not change any public
chapter, media file, numbering receipt, or Pages workflow.
"""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from publish_site import guard_render_commit


def command(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


class RenderCommitGuardTests(unittest.TestCase):
    def test_known_comparative_history_catalogue_is_allowed(self):
        """Repro: this generated report previously blocked a valid rebuild."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            command(root, "init", "-q")
            report = root / "catalog" / "comparative-history.json"
            report.parent.mkdir(parents=True)
            report.write_text('{"version":1,"studies":[]}', encoding="utf-8")
            command(root, "add", "-A")
            guard_render_commit(root)

    def test_compact_search_catalogue_is_generated_and_allowed(self):
        """The lightweight search projection may be committed by the renderer."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            command(root, "init", "-q")
            report = root / "catalog" / "search-light.json"
            report.parent.mkdir(parents=True)
            report.write_text('[{"id":"MYT-1","url":"/","title":"MYTHOS"}]',
                              encoding="utf-8")
            command(root, "add", "-A")
            guard_render_commit(root)

    def test_arbitrary_catalogue_is_not_treated_as_generated(self):
        """Allowing one report must not allow unapproved catalogue sources."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            command(root, "init", "-q")
            report = root / "catalog" / "manually-injected.json"
            report.parent.mkdir(parents=True)
            report.write_text('{"unverified":"source"}', encoding="utf-8")
            command(root, "add", "-A")
            with self.assertRaisesRegex(RuntimeError, "source ou média modifié"):
                guard_render_commit(root)

    def test_media_changes_remain_protected(self):
        """The publication allowlist cannot silently permit media mutation."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            command(root, "init", "-q")
            media = root / "media" / "raw-image.jpg"
            media.parent.mkdir(parents=True)
            media.write_bytes(b"unapproved media")
            command(root, "add", "-A")
            with self.assertRaisesRegex(RuntimeError, "source ou média modifié"):
                guard_render_commit(root)


if __name__ == "__main__":
    unittest.main()
