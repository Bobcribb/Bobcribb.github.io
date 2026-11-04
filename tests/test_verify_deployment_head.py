"""Le site public ne doit jamais recevoir une version périmée du dépôt."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify_deployment_head as guard


class DeploymentHeadTests(unittest.TestCase):
    SHA_A = "a" * 40
    SHA_B = "b" * 40

    @patch.object(guard, "only_pending_requests_or_log")
    @patch.object(guard, "latest_main", return_value=SHA_A)
    def test_exact_head_is_allowed(self, latest, pending):
        self.assertEqual(guard.verify_current_head(Path("."), self.SHA_A), self.SHA_A)
        pending.assert_not_called()

    @patch.object(guard, "only_pending_requests_or_log", return_value=True)
    @patch.object(guard, "latest_main", return_value=SHA_B)
    def test_new_unallocated_requests_cannot_discard_a_valid_render(self, latest, pending):
        self.assertEqual(guard.verify_current_head(Path("."), self.SHA_A), self.SHA_B)
        pending.assert_called_once()

    @patch.object(guard, "only_pending_requests_or_log", return_value=False)
    @patch.object(guard, "latest_main", return_value=SHA_B)
    def test_changed_source_blocks_stale_deployment(self, latest, pending):
        with self.assertRaisesRegex(RuntimeError, "Déploiement annulé"):
            guard.verify_current_head(Path("."), self.SHA_A)

    def test_missing_sha_blocks_deployment(self):
        with self.assertRaisesRegex(RuntimeError, "invalide"):
            guard.verify_current_head(Path("."), "")
