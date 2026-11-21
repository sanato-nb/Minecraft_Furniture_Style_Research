"""INT-0/INT-1 pinned source inventory and evidence-reference regression tests."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION = ROOT / "project/integration"
API = runpy.run_path(str(ROOT / "scripts/integration/inventory.py"))


class IntegrationInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = API["inventory"](ROOT, API["BASELINE"])

    def test_manifest_reproducible_from_pinned_git_tree(self):
        expected = API["render"](self.rows)
        self.assertEqual((INTEGRATION / "SOURCE_MANIFEST.csv").read_text(encoding="utf-8"), expected)
        self.assertEqual(len(self.rows), len({r["path"] for r in self.rows}))
        self.assertFalse(any(r["path"].startswith("1.21.11/") for r in self.rows))

    def test_manifest_stats_match_precise_scope(self):
        actual = API["overview"](self.rows)
        stored = json.loads((INTEGRATION / "INVENTORY_STATS.json").read_text(encoding="utf-8"))
        self.assertEqual(actual, stored)
        self.assertEqual(sum(stored["by_stage"].values()), stored["file_count"])
        self.assertEqual(sum(stored["by_role"].values()), stored["file_count"])

    def test_evidence_and_dependency_paths_are_pinned(self):
        checks = API["validate_references"](self.rows, INTEGRATION)
        self.assertEqual(set(checks), {"evidence_map", "dependencies"})
        with (INTEGRATION / "DEPENDENCY_MAP.csv").open(newline="", encoding="utf-8") as f:
            edges = list(csv.DictReader(f))
        self.assertEqual(len(edges), len({(e["source"], e["relation"], e["target"]) for e in edges}))

    def test_evidence_anchor_bytes_match_actual_git_blob(self):
        catalog = {r["path"]: r for r in self.rows}
        with (INTEGRATION / "EVIDENCE_MAP.csv").open(newline="", encoding="utf-8") as f:
            anchors = list(csv.DictReader(f))
        self.assertGreater(len(anchors), 20)
        for anchor in anchors:
            path = anchor["path"]
            row = catalog[path]
            body = (ROOT / path).read_bytes()
            blob_hash = hashlib.sha1(f"blob {len(body)}\\0".encode() + body).hexdigest()
            with self.subTest(path=path):
                self.assertEqual(len(body), int(row["bytes"]))
                self.assertEqual(row["git_blob_sha1"], anchor["git_blob_sha1"])
                self.assertEqual(blob_hash, row["git_blob_sha1"])

    def test_baseline_contract_and_no_false_reaudit(self):
        baseline = json.loads((INTEGRATION / "INT0_BASELINE.json").read_text(encoding="utf-8"))
        self.assertEqual(baseline["baseline_commit"], API["BASELINE"])
        with (INTEGRATION / "AUDIT_FINDINGS.csv").open(newline="", encoding="utf-8") as f:
            findings = list(csv.DictReader(f))
        self.assertTrue(findings)
        self.assertTrue(all(item["int1_verdict"] == "NOT_REVALIDATED" for item in findings))


if __name__ == "__main__":
    unittest.main()
