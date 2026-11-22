"""INT-4-F8 official parent SHA reconciliation, isolated tests without internet."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"scripts/integration/audit_int4_f8_s22_parent_sha_and_70_cases.py"
spec=importlib.util.spec_from_file_location("mcfr_f8_audit",SCRIPT)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)


class F8OriginalParent70Cases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=f.build()
        cls.summary=json.loads(cls.files[f.SUMMARY])
        cls.correction=json.loads(cls.files[f.CORRECTION])
        cls.target=f.rows(cls.files[f.OUT70])
        cls.old=f.rows(f.pin(f.PREV))

    def test_study_source_and_official_metadata_sha_locked(self):
        for path in (f.PREV,f.F7,f.EX,f.OFFICIAL,f.SOURCE):
            self.assertEqual(f.blob(f.pin(path)),f.PINS[str(path)])

    def test_only_s22_row_changes_from_previous_f7(self):
        previous={r["target_id"]:r for r in self.old}
        current={r["target_id"]:r for r in self.target}
        self.assertEqual(len(previous),len(current))
        self.assertEqual(len(previous),70)
        self.assertEqual({k for k in previous if previous[k]!=current[k]},{"S22"})

    def test_frozen_historical_source_is_not_modified(self):
        self.assertEqual(f.sha(f.pin(f.SOURCE)),f.ORIGINAL_SOURCE_SHA256)
        self.assertEqual(self.summary["counts"]["historic_1_5_research_source_files_changed"],0)
        self.assertIs(self.correction["original_research_csv_modified"],False)

    def test_hash_kind_declared_wrong_but_actual_official_file_sha256_equal(self):
        self.assertEqual(self.correction["original_label"],"GIT_BLOB_SHA1")
        self.assertEqual(self.correction["actual_recorded_hash_algorithm"],"SHA256")
        self.assertEqual(self.correction["recorded_original_parent_SHA"],f.ORIGINAL_HASH)
        self.assertEqual(self.correction["official_parent_git_blob_SHA1"],f.CORRECT_GIT_BLOB)
        self.assertNotEqual(f.ORIGINAL_HASH,f.CORRECT_GIT_BLOB)

    def test_parent_difference_only_in_item_display(self):
        self.assertEqual(self.correction["inherited_parent_changed_paths"],["display.on_shelf"])
        self.assertIs(self.correction["inherited_parent_world_fields_stable"],True)

    def test_F7_actual_image_reused_no_new_F2_claim(self):
        self.assertEqual(self.summary["counts"]["new_F2_images"],0)
        f7=json.loads(f.pin(f.F7))
        self.assertEqual(self.summary["f7_original_F2_SHA256"],
                         f7["cases"]["S22"]["original_native_F2_sha256"])

    def test_70_cases_43_conditional_and_27_hold(self):
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in self.target),43)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in self.target),27)
        self.assertEqual(self.summary["remaining_HOLD_by_cohort"],{"MACAW":10,"RISK":2,"VANILLA":15})

    def test_f_stage_unconditional_approval_and_AI_rights_remain_zero(self):
        self.assertTrue(all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false"
                            for x in self.target))
        self.assertEqual(self.summary["counts"]["F_full_unconditional_approval"],0)
        self.assertEqual(self.summary["counts"]["new_INT5_part_semantic_approval"],0)
        self.assertEqual(self.summary["counts"]["new_INT6_AI_training_and_redistribution_rights"],0)

    def test_results_are_deterministic(self):
        self.assertEqual(self.files,f.build())

    def test_pinned_original_drift_rejected(self):
        old=f.PINS[str(f.OFFICIAL)]
        try:
            f.PINS[str(f.OFFICIAL)]="0"*40
            with self.assertRaises(AssertionError):
                f.build()
        finally:
            f.PINS[str(f.OFFICIAL)]=old

if __name__=="__main__":
    unittest.main()
