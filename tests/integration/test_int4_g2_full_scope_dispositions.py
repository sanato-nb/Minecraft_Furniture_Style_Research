"""INT-4-G2 source-scope protections. No full GUI/asset reuse approvals."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"scripts/integration/build_int4_g2_full_scope_dispositions.py"
spec=importlib.util.spec_from_file_location("g2_original_source",FILE)
g2=importlib.util.module_from_spec(spec);spec.loader.exec_module(g2)

class G2ResearchScopeAudit(unittest.TestCase):
    def test_git_blob_sources_pinned(self):
        for name in g2.PINS:
            self.assertEqual(g2.gitblob(g2.pinned(name)),g2.PINS[name],name)

    def test_full_four_gzip_population_denominators(self):
        self.assertEqual({k:v[1] for k,v in g2.COMP.items()},{
            "INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":16572,
            "INT4_B_592312_FACE_PROVENANCE_V1.csv.gz":592312,
            "INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":6343,
            "INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":78456,
        })

    def test_a_model_dispositions_are_scoped(self):
        mapping={
            "VERIFIED_REUSED_STATIC_SCOPE":"VERIFIED_STATIC_SOURCE_ONLY",
            "CONDITIONAL_STATIC_SOURCE_EXCEPTION":"CONDITIONAL_MISSING_PARENT_STATIC_UNREACHABLE_DYNAMIC_UNKNOWN",
            "HOLD_MODEL_USAGE_AND_RENDER_PATH":"HOLD_BASE_MODEL_USAGE_UNKNOWN",
            "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":"NOT_APPLICABLE_GENERATED_ITEM_CUBOID"
        }
        for old,new in mapping.items():
            self.assertEqual(g2.disposition_for_A(old),new)
        with self.assertRaises(KeyError):
            g2.disposition_for_A("UNAUTHORIZED_FINAL_APPROVAL")

    def test_face_key_separates_slot_uv(self):
        a={"model_key":"A","element_index":"1","face_direction":"up",
           "source_slot":"#texture","uv":"0|0|16|16"}
        b={"model_key":"A","element_index":"1","face_direction":"up",
           "source_texture_slot":"#texture","source_uv":"0|0|16|16"}
        self.assertEqual(g2.face_key(a),g2.face_key(b))
        self.assertEqual(g2.exact_key(a,True),g2.exact_key(b,False))
        b["source_uv"]="0|0|8|8"
        self.assertNotEqual(g2.exact_key(a,True),g2.exact_key(b,False))

    def test_prior_claims_unlicensed(self):
        x=g2.csvrows(g2.pinned("INT4_E_21_FINDING_DISPOSITIONS_V1.csv"))
        self.assertEqual(len(x),21)
        self.assertEqual(sum(r["original_INT2_disposition"]=="SCOPE_LIMIT_ONLY" for r in x),7)
        self.assertEqual(sum(r["original_INT2_disposition"]=="CANDIDATE_REQUIRES_REVIEW" for r in x),14)
        self.assertTrue(all(r["int6_rights_approved"]=="false" for r in x))

    def test_f70_is_all_conditional_and_no_final_acceptance(self):
        x=g2.csvrows(g2.pinned("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
        self.assertEqual(len(x),70)
        self.assertEqual(sum(r["target_kind"]=="HISTORICAL_1_5_CASE" for r in x),62)
        self.assertTrue(all(r["final_disposition"].startswith("CONDITIONAL") for r in x))
        self.assertTrue(all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in x))

    def test_modified_pin_fails_closed(self):
        key="INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json"
        original=g2.PINS[key]
        try:
            g2.PINS[key]="0"*40
            with self.assertRaises(AssertionError):
                g2.pinned(key)
        finally:
            g2.PINS[key]=original

if __name__=="__main__":
    unittest.main()
