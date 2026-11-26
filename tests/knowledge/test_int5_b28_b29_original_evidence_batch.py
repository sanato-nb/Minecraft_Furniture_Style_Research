"""INT5 B28/B29 bounded evidence provenance and strict non-approval tests."""
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from mcfr.int5_b28_aggregate_original_artifact_reaudit import ARTIFACTS, diff, audit_one
from mcfr.int5_b29_full45_crossledger_audit import FILES, audit


ROOT = Path(__file__).resolve().parents[2] / "project" / "integration"


class B28B29OriginalEvidenceTests(unittest.TestCase):
    def test_all_eight_artifacts_pinned_with_distinct_sha(self):
        self.assertEqual(len(ARTIFACTS), 8)
        self.assertEqual(len({key for key in ARTIFACTS}), 8)
        self.assertEqual(len({v[0] for v in ARTIFACTS.values()}), 8)
        self.assertEqual(len({v[1] for v in ARTIFACTS.values()}), 8)
        for _, sha in ARTIFACTS.values():
            self.assertEqual(len(sha), 64)
            self.assertTrue(all(x in "0123456789abcdef" for x in sha))

    def test_original_rgb_threshold_24_rejects_stray_small_delta(self):
        a = np.zeros((2, 2, 3), dtype=np.int16)
        b = a.copy()
        b[0, 0] = [24, 0, 0]
        b[1, 0] = [25, 0, 0]
        result = diff(a, b)
        self.assertFalse(result[0, 0])
        self.assertTrue(result[1, 0])
        self.assertEqual(int(result.sum()), 1)

    def test_missing_original_artifact_cannot_be_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises((FileNotFoundError, ValueError)):
                audit_one(Path(tmp), "AF121_without_leg0")

    def test_b29_full_45_source_ledger_reconciles(self):
        outcome = audit(ROOT)
        self.assertEqual(outcome["source_faces"], 229)
        self.assertEqual(outcome["source_rows"], {"B24": 45, "B26": 24, "B27": 45})
        self.assertEqual(outcome["original_native_F2_SHA256_verified_record_sum"], 560)
        self.assertEqual(outcome["bounded_original_element_removal_visual_response"], 43)
        self.assertEqual(outcome["role_function_material_style_approved"], 0)

    def _modified_copy(self, target, modify):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            for f in FILES.values():
                shutil.copyfile(ROOT / f, path / f)
            source = path / FILES[target]
            with source.open(encoding="utf-8-sig", newline="") as fh:
                reader = csv.DictReader(fh)
                names = reader.fieldnames
                records = list(reader)
            modify(records)
            with source.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, names)
                writer.writeheader()
                writer.writerows(records)
            with self.assertRaisesRegex(ValueError, "INT5_B29_CROSSLEDGER_REJECT"):
                audit(path)

    def test_mutated_B27_role_approval_fails_closed(self):
        self._modified_copy("b27", lambda rows: rows[0].__setitem__("physical_role_material_style_approved", "true"))

    def test_mutated_B26_pixel_breaks_join(self):
        self._modified_copy("b26", lambda rows: rows[0].__setitem__("B26_south_original_F2_removed_pixel_count", "9999"))

    def test_duplicated_B24_source_key_rejected(self):
        self._modified_copy("b24", lambda rows: rows[1].__setitem__("source_element_index", rows[0]["source_element_index"]))


if __name__ == "__main__":
    unittest.main()
