"""Unit tests for independent git-object digest calculation."""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/migration"))
from audit_repository import compare_baseline, git_blob_digest


class AuditHashTests(unittest.TestCase):
    def test_empty_blob(self):
        self.assertEqual(git_blob_digest(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_known_blob(self):
        self.assertEqual(git_blob_digest(b"test\n"), "9daeafb9864cf43055ae93beb0afd6c7d144bfa4")

    def test_baseline_tracks_removed_modified_and_added_paths(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            git = ["git", "-C", directory]
            subprocess.run([*git, "init", "--quiet"], check=True)
            names = ("removed", "changed", "mode", "unchanged")
            for name in names:
                (root / name).write_bytes(b"test\n")
            subprocess.run([*git, "add", "--", *names], check=True)
            subprocess.run(
                [*git, "-c", "user.name=Test", "-c", "user.email=test@example.com",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "baseline"],
                check=True,
            )
            same = git_blob_digest(b"test\n")
            current = {
                "changed": ("100644", git_blob_digest(b"changed\n")),
                "mode": ("100755", same),
                "unchanged": ("100644", same),
                "new": ("100644", same),
            }
            result = compare_baseline(root, "HEAD", current)
            self.assertEqual(result["removed"], ["removed"])
            self.assertEqual(result["modified"], ["changed", "mode"])
            self.assertEqual(result["preserved_files"], 1)
            self.assertEqual(result["added_count"], 1)


if __name__ == "__main__":
    unittest.main()
