"""F11F original evidence gate: no R08 promotion without two real source F2."""
from pathlib import Path
import importlib.util,json,unittest
ROOT=Path(__file__).resolve().parents[2]
code=ROOT/"scripts/integration/build_int4_f11f_r08_two_original_f2_audit.py"
spec=importlib.util.spec_from_file_location("int4f11f_original",code)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
class F11FIndependentAudit(unittest.TestCase):
    def test_original_f11e_and_study_sha_locked(self):
        for p in (f.PRIOR,f.STUDY):
            self.assertEqual(f.gitblob(f.frozen(p)),f.PINS[str(p)])
    def test_original_f70_69_conditional_one_hold(self):
        records=f.crows(f.frozen(f.PRIOR))
        self.assertEqual(len(records),70)
        self.assertEqual(sum(r["final_disposition"].startswith("CONDITIONAL") for r in records),69)
        self.assertEqual([r["target_id"] for r in records if r["final_disposition"].startswith("HOLD")],["R08"])
    def test_study_vs_official_version_not_equated(self):
        self.assertEqual(f.GIT,"57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertNotEqual(f.OLD_STATE_BLOB,f.NEW_STATE_BLOB)
        self.assertEqual(len(f.NEW_MODEL_BLOB),40)
    def test_representative_state_not_88_option_equivalence(self):
        self.assertEqual(f.STATE,"another_furniture:acacia_chair[facing=north,tucked=false,variant=1]")
        self.assertEqual(f.MODEL,"another_furniture:block/chair/acacia_1")
        self.assertEqual(f.OUT70.name,"INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv")
    def test_pinned_source_image_and_actions_run(self):
        self.assertEqual(f.RUN,45108332421)
        self.assertEqual(f.ARTIFACT,14788254210)
        self.assertEqual(len(f.PNG_SHA),64)
        self.assertEqual(len(f.ZIP_SHA),64)
    def test_closed_fail_if_source_digest_modified(self):
        original=f.PINS[str(f.PRIOR)]
        try:
            f.PINS[str(f.PRIOR)]="0"*40
            with self.assertRaises(AssertionError):f.frozen(f.PRIOR)
        finally:f.PINS[str(f.PRIOR)]=original
    def test_no_original_game_source_committed_to_github(self):
        self.assertTrue(str(f.OUT70).startswith("project/integration/"))
        self.assertFalse(str(f.OUT70).endswith(".png"))
        self.assertEqual(f.OUTZERO.name,"INT4_F11F_0_PENDING_EXACT_F2_TARGETS_V1.csv")
    def test_robust_existing_frozen_70_count(self):
        old=f.crows(f.frozen(f.PRIOR))
        self.assertTrue(all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in old))
        self.assertEqual(len({r["target_id"] for r in old}),70)
if __name__=="__main__":unittest.main()
