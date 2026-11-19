"""Safety and configuration tests for the non-destructive H1 foundation."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from mcfr.foundation import preview_plan, validate


class FoundationTests(unittest.TestCase):
    def test_profiles_and_modes(self):
        result = validate(ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(set(result["profiles"]), {"vanilla", "mods"})
        self.assertIn("FRESH", result["modes"])

    def test_fresh_is_independent(self):
        result = preview_plan(ROOT, "mods", "FRESH", "example_mod", "1.0.0")
        self.assertEqual(result["prior_result_policy"], "do_not_use_prior_conclusions")
        self.assertFalse(result["writes_repository"])
        self.assertFalse(result["execution_enabled"])

    def test_incremental_needs_baseline(self):
        with self.assertRaises(ValueError):
            preview_plan(ROOT, "vanilla", "INCREMENTAL", "minecraft", "1.21.12")
        result = preview_plan(ROOT, "vanilla", "INCREMENTAL", "minecraft", "1.21.12", "1.21.11")
        self.assertEqual(result["baseline_release"], "1.21.11")

    def test_requires_nonempty_target(self):
        with self.assertRaises(ValueError):
            preview_plan(ROOT, "mods", "NEW", "", "1.0.0")

    def test_no_automatic_main_or_inbox_deletion(self):
        shared = json.loads((ROOT / "harness/shared/config.json").read_text(encoding="utf-8"))
        self.assertEqual(shared["default_write_policy"], "branch_pr_only")
        self.assertIs(shared["automatic_main_merge"], False)
        self.assertIs(shared["automatic_inbox_delete"], False)


if __name__ == "__main__":
    unittest.main()
