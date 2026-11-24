"""Independent positive and fail-closed checks for INT-4 scoped H03/H05 exit."""
import csv
import io
import json
import unittest

from mcfr import int4_modeling_scope_exit as scope


class ModelingScopedExitTests(unittest.TestCase):
    def setUp(self):
        self.inputs = scope.pinned_inputs()

    def test_all_seventy_exact_source_cases_and_separated_gates(self):
        report = scope.adjudicate(self.inputs)
        self.assertEqual(report["modeling_case_count"], 70)
        self.assertEqual(report["modeling_historical_pass"], 62)
        self.assertEqual(report["modeling_risk_question_pass"], 8)
        self.assertEqual(report["modeling_H03"], "PASS_SCOPED_MODEL_RENDER_EVIDENCE")
        self.assertEqual(report["modeling_H05"], "PASS_SCOPED_HISTORICAL_PROVENANCE")
        self.assertEqual(report["original_strict_H03"], "HOLD")
        self.assertEqual(report["original_strict_H05"], "CONDITIONAL")
        self.assertEqual(report["original_strict_F_unconditional"], 0)
        self.assertFalse(report["full_INT4_unconditional_exit"])
        self.assertEqual(report["INT6_asset_training_redistribution_rights_approved"], 0)

    def test_committed_result_identical_to_recomputed_result(self):
        with (scope.ROOT / scope.OUT).open(encoding="utf-8") as f:
            saved = json.load(f)
        self.assertEqual(saved, scope.adjudicate(self.inputs))

    @staticmethod
    def changed_row(inputs, field, value):
        out = dict(inputs)
        name = "INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv"
        text = inputs[name].decode("utf-8")
        rows = list(csv.DictReader(io.StringIO(text)))
        rows[0][field] = value
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        out[name] = buf.getvalue().encode("utf-8")
        return out

    def test_missing_one_modeling_pass_cannot_be_approved(self):
        tampered = self.changed_row(self.inputs, "modeling_status", "CONDITIONAL_MODELING")
        with self.assertRaisesRegex(ValueError, "modeling source does not approve"):
            scope.adjudicate(tampered)

    def test_one_wrong_frame_sha_blocks_scoped_approval(self):
        tampered = self.changed_row(self.inputs, "original_f2_sha256s", "bad_sha")
        with self.assertRaisesRegex(ValueError, "PNG SHA mismatch"):
            scope.adjudicate(tampered)

    def test_one_unproven_legacy_gpu_flag_cannot_be_promoted(self):
        tampered = self.changed_row(self.inputs, "runtime_GPU_per_face_approved", "true")
        with self.assertRaisesRegex(ValueError, "unauthorized approval flag"):
            scope.adjudicate(tampered)

    def test_historical_original_strict_gate_cannot_be_rewritten(self):
        tampered = dict(self.inputs)
        name = "INT4_DF_ORIGINAL_EXIT_CONTRACT_REAUDIT_V1.json"
        doc = json.loads(tampered[name])
        doc["original_H_gates"]["H03"] = "PASS"
        tampered[name] = json.dumps(doc).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "strict F/H original result changed"):
            scope.adjudicate(tampered)

    def test_missing_archive_sha_evidence_blocks_scope(self):
        tampered = dict(self.inputs)
        name = "INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"
        doc = json.loads(tampered[name])
        doc["all_91_native_F2_PNG_sha256_verified"] = False
        tampered[name] = json.dumps(doc).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "archive verification missing"):
            scope.adjudicate(tampered)

    def test_exact_git_blob_source_pins_match(self):
        for name, blob in self.inputs.items():
            self.assertEqual(scope.git_blob_sha(blob), scope.PINS[name])


if __name__ == "__main__":
    unittest.main()
