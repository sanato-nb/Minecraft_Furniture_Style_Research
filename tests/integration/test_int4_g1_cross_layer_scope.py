"""G1 source census and final non-approval boundary tests (offline)."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/"scripts/integration/build_int4_g1_cross_layer_scope.py"
sp=importlib.util.spec_from_file_location("int4_g1_scope",p)
g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)

class G1IndependentSourceScope(unittest.TestCase):
    def test_pinned_source_git_blobs_unchanged(self):
        for path in g.PINS:
            self.assertEqual(g.gitblob(g.blob(path)),g.PINS[path])
    def test_separate_fixed_static_denominators(self):
        self.assertEqual(g.GZIP["INT4_A_MODEL_DISPOSITIONS_V2.csv.gz"][1],16572)
        self.assertEqual(g.GZIP["INT4_B_592312_FACE_PROVENANCE_V1.csv.gz"][1],592312)
        self.assertEqual(g.GZIP["INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz"][1],6343)
        self.assertEqual(g.GZIP["INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz"][1],78456)
    def test_a_union_non_disjoint_parent_and_no_static(self):
        A=g.jsonin("INT4_A_ADJUDICATION_SUMMARY_V2.json")
        self.assertEqual(A["exception_rows"],112)
        self.assertEqual(A["source_parent_missing_remains"],48)
        self.assertEqual(A["static_geometry_na_generated_items"],58)
        self.assertEqual(A["review_results"]["HOLD_MODEL_USAGE_AND_RENDER_PATH"],6)
    def test_e_claim_candidates_not_automatic_rules(self):
        E=g.jsonin("INT4_E_CROSS_AUDIT_SUMMARY_V1.json")
        self.assertEqual(E["counts"]["finding_source_rows"],21)
        self.assertEqual(E["counts"]["historical_handoff_disposition_counts"],{
            "CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7})
    def test_f70_conditional_not_final_exit(self):
        F=g.jsonin("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
        self.assertEqual(F["counts"]["F_conditional_after"],70)
        self.assertEqual(F["counts"]["F_HOLD_after"],0)
        self.assertEqual(F["counts"]["F_unconditional_final_approvals"],0)
        self.assertEqual(F["counts"]["G_approvals"],0)
        self.assertEqual(F["counts"]["H_exit_approvals"],0)
    def test_original_sha_tamper_fails_closed(self):
        old=g.PINS["INT4_A_ADJUDICATION_SUMMARY_V2.json"]
        try:
            g.PINS["INT4_A_ADJUDICATION_SUMMARY_V2.json"]="0"*40
            with self.assertRaises(AssertionError):
                g.jsonin("INT4_A_ADJUDICATION_SUMMARY_V2.json")
        finally:
            g.PINS["INT4_A_ADJUDICATION_SUMMARY_V2.json"]=old

if __name__=="__main__":unittest.main()
