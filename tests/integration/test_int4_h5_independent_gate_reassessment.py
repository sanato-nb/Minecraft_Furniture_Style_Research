"""H5 original H1 H3 H4 evidence SHA, 8-gate no-false-exit regression."""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
src=ROOT/"scripts/integration/build_int4_h5_independent_gate_reassessment.py"
spec=importlib.util.spec_from_file_location("h5audit",src)
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class H5IndependentGateReview(unittest.TestCase):
    def test_immutable_H1_H3_H4_G5_original_blobs(self):
        for name,sha in a.FILES.items():
            self.assertEqual(a.gitblob((ROOT/a.I/name).read_bytes()),sha)
    def test_old_eight_gate_statuses_and_H03_mandatory_F70(self):
        d=a.table(a.original("INT4_H1_EIGHT_INDEPENDENT_EXIT_GATES_V1.csv"))
        self.assertEqual(len(d),8)
        by={r["gate_id"]:r for r in d}
        self.assertEqual(by["H03"]["review_status"],"HOLD_FULL_F_EXIT")
        self.assertEqual(by["H05"]["review_status"],"HOLD_FULL_IMAGE_REOPEN")
        self.assertEqual(by["H06"]["review_status"],"CONDITIONAL_PARALLEL_CI_FIX")
    def test_H3_native_real_original_zip_and_png_bytes_only(self):
        j=a.json.loads(a.original("INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"))
        self.assertEqual(j["original_distinct_actions_archive_downloaded"],20)
        self.assertEqual(j["recorded_original_PNG_occurrences"],91)
        self.assertTrue(j["all_91_native_F2_PNG_sha256_verified"])
        self.assertFalse(j["every_original_case_server_state_log_reopened_and_reapproved"])
        self.assertEqual(j["H_full_exit_approved"],0)
    def test_H4_PR73_five_fixes_exact_without_GUI_claim(self):
        j=a.json.loads(a.original("INT4_H4_H06_CI_ENVIRONMENT_INTEGRATED_SOURCE_AUDIT_V1.json"))
        self.assertEqual(len(j["verified_original_PR73_fixed_workflows"]),5)
        self.assertEqual(j["F_unconditional_final_approved"],0)
        self.assertEqual(j["H_full_exit_approved"],0)
    def test_G5_original_scoped_full_F_not_promoted(self):
        j=a.json.loads(a.original("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json"))
        self.assertEqual(j["dispositions"]["real_F_units"],{"CONDITIONAL":70})
        self.assertEqual(j["F_unconditional_exit_approved"],0)
    def test_a_source_tamper_fails_closed(self):
        key="INT4_H4_H06_CI_ENVIRONMENT_INTEGRATED_SOURCE_AUDIT_V1.json"
        original=a.FILES[key]
        try:
            a.FILES[key]="0"*40
            with self.assertRaises(AssertionError):a.original(key)
        finally:a.FILES[key]=original

if __name__=="__main__":unittest.main()
