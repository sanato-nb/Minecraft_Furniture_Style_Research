"""INT-4-F prohibitions: never promote archival images to universal render acceptance."""
from pathlib import Path
import importlib.util
import unittest

def source_module():
    script=Path(__file__).resolve().parents[2]/"scripts/integration/build_int4_f_real_f2_archive_audit.py"
    spec=importlib.util.spec_from_file_location("int4f_review",script)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

f=source_module()

class OriginalImageReviewContract(unittest.TestCase):
    def test_exact_target_divisions(self):
        self.assertEqual(len(f.EXACT_CASE_ARCHIVE),15)
        self.assertEqual(len(f.RISKS),8)

    def test_direct_case_ids_are_unique_and_observed(self):
        self.assertEqual(set(f.EXACT_CASE_ARCHIVE),set(f.OBS))

    def test_risk_hold_exemptions(self):
        self.assertTrue(f.RISKS["R01"]["status"].startswith("HOLD"))
        self.assertTrue(f.RISKS["R06"]["status"].startswith("HOLD"))
        self.assertTrue(f.RISKS["R08"]["status"].startswith("HOLD"))

    def test_no_historic_unmapped_case_false_pass(self):
        self.assertEqual(f.classify_original_target(True,False,"S10"),"HOLD_NO_EXACT_CASE_F2_LINKED")

    def test_historic_visual_case_is_conditional_not_accepted(self):
        self.assertTrue(f.classify_original_target(True,True,"S14").startswith("CONDITIONAL"))

    def test_risk_reused_evidence_still_conditional(self):
        for id_ in ("R02","R03","R04","R05","R07"):
            self.assertTrue(f.classify_original_target(False,False,id_).startswith("CONDITIONAL"))

    def test_unknown_scenario_rejected(self):
        with self.assertRaises(AssertionError):
            f.classify_original_target(False,False,"R09")

    def test_original_archive_pin_sha256(self):
        self.assertEqual(len(f.ARCHIVES),11)
        self.assertEqual(len({x[2] for x in f.ARCHIVES}),11)
        self.assertTrue(all(len(x[3])==64 for x in f.ARCHIVES))

    def test_duplicate_source_case_rejected(self):
        with self.assertRaises(AssertionError):
            f.unique([{"case":"S37"},{"case":"S37"}],lambda r:r["case"],"TEST")

    def test_original_git_blob_pin_drift(self):
        path="project/integration/INT4_F_RENDER_TARGETS_V1.csv"
        saved=f.PINS[path]
        try:
            f.PINS[path]="0"*40
            with self.assertRaises(AssertionError):
                f.pinned(path)
        finally:
            f.PINS[path]=saved

if __name__=="__main__":unittest.main()
