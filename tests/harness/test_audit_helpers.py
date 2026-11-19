"""Unit tests for independent git-object digest calculation."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/migration"))
from audit_repository import git_blob_digest


class AuditHashTests(unittest.TestCase):
    def test_empty_blob(self):
        self.assertEqual(git_blob_digest(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_known_blob(self):
        self.assertEqual(git_blob_digest(b"test\n"), "9daeafb9864cf43055ae93beb0afd6c7d144bfa4")


if __name__ == "__main__":
    unittest.main()
