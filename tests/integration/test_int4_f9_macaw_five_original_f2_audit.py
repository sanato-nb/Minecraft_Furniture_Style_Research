"""INT-4-F9 independent no-network source/provenance audit guard tests."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"scripts/integration/build_int4_f9_five_macaw_original_f2_audit.py"
spec=importlib.util.spec_from_file_location("int4f9_audit",FILE)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)

class MacawFiveIndependentGate(unittest.TestCase):
    def test_original_inputs_git_blobs_pinned(self):
        for p in (f.PREVIOUS,f.F8,f.F9,f.SOURCE):
            self.assertEqual(f.blob(f.locked(p)),f.PINS[str(p)])

    def test_real_native_F2_report_five_original_case_ids(self):
        data=json.loads(f.locked(f.F9))
        self.assertEqual(data["case_ids"],list(f.CASES))
        self.assertEqual((data["server_exact_states"],data["actual_native_F2"]),(5,5))
        self.assertEqual((data["historical_elements"],data["historical_faces"]),(39,179))
        self.assertEqual(data["actual_mod_jar_SHA256"],f.MACAW_JAR)

    def test_f8_70_target_denominator_and_holds_remain_fixed_at_input(self):
        data=f.rows(f.locked(f.PREVIOUS))
        self.assertEqual(len(data),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in data),43)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in data),27)

    def test_only_original_exact_five_are_hold_in_prior(self):
        data=f.rows(f.locked(f.PREVIOUS))
        self.assertEqual(f.CASES,("S08","S09","S11","S12","S23"))
        self.assertTrue(all(r["final_disposition"].startswith("HOLD")
                            for r in data if r["target_id"] in f.CASES))

    def test_macaw_fixed_element_face_denominator(self):
        self.assertEqual(sum(f.EXPECTED_ELEMENTS.values()),39)
        self.assertEqual(sum(f.EXPECTED_FACES.values()),179)
        self.assertEqual(list(f.OBS),list(f.CASES))

    def test_original_zip_artifact_run_is_pinned(self):
        self.assertEqual(f.RUN,45035905411)
        self.assertEqual(f.ARTIFACT,14759742774)
        self.assertEqual(len(f.ZIP_SHA256),64)

    def test_no_advanced_acceptance_in_original_source_report(self):
        x=json.loads(f.locked(f.F9))
        self.assertEqual(x["f_full_approval"],0)
        self.assertEqual(x["int5_semantic_approval"],0)
        self.assertEqual(x["int6_rights_approval"],0)
        self.assertEqual(x["human_visual_review"],"PENDING_ORIGINAL_NATIVE_F2_INDEPENDENT_REOPEN")

    def test_input_git_blob_drift_is_a_hard_error(self):
        saved=f.PINS[str(f.F9)]
        try:
            f.PINS[str(f.F9)]="0"*40
            with self.assertRaises(AssertionError):
                f.locked(f.F9)
        finally:
            f.PINS[str(f.F9)]=saved

if __name__=="__main__":
    unittest.main()
