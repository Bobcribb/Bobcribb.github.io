"""Prevent silent integrity-audit CI skips after policy or CNAME changes."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github" / "workflows" / "audit-integrity.yml").read_text(encoding="utf-8")


class AuditWorkflowCoverageTests(unittest.TestCase):
    def test_push_filters_cover_policy_tests_and_domain(self):
        push = WORKFLOW.split("\n  pull_request:", 1)[0]
        for path in (
            "scripts/audit_integrity.py",
            "scripts/audit_policy.py",
            "tests/test_audit_*.py",
            "CNAME",
        ):
            with self.subTest(path=path):
                self.assertIn(f"      - '{path}'", push)

    def test_pull_request_filters_cover_policy_tests_and_domain(self):
        pr = WORKFLOW.split("\n  pull_request:", 1)[1].split("\n  workflow_dispatch:", 1)[0]
        self.assertIn("      - 'scripts/**'", pr)
        self.assertIn("      - 'tests/test_audit_*.py'", pr)
        self.assertIn("      - 'CNAME'", pr)

    def test_policy_regressions_run_before_full_audit(self):
        self.assertIn("python -m unittest discover -s tests -p 'test_audit_*.py' -v", WORKFLOW)
        self.assertIn("python scripts/audit_integrity.py", WORKFLOW)
        self.assertLess(
            WORKFLOW.index("python -m unittest discover -s tests -p 'test_audit_*.py' -v"),
            WORKFLOW.index("python scripts/audit_integrity.py"),
        )


if __name__ == "__main__":
    unittest.main()
