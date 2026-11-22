"""Independent F7 70-target provenance audit gate, source hash and S22 hold."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_f7_four_native_f2_provenance.py"
sp=importlib.util.spec_from_file_location("int4f7auditor",path)
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)

class F7IndependentEvidenceGate(unittest.TestCase):
    def test_fixed_original_git_blob_inputs_are_unchanged(self):
        for p in (f.BASE,f.CAPTURE,f.STUDY):
            self.assertEqual(f.blob(f.locked(p)),f.PIN[str(p)])

    def test_original_70_denominator_and_prior_counts(self):
        old=f.rows(f.locked(f.BASE))
        self.assertEqual(len(old),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in old),39)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in old),31)
        self.assertTrue(all(x["final_disposition"].startswith("HOLD")
            for x in old if x["target_id"] in f.CASES))

    def test_original_F7_4_real_game_states_and_models(self):
        doc=json.loads(f.locked(f.CAPTURE))
        self.assertEqual(doc["historical_case_ids"],list(f.CASES))
        self.assertEqual(doc["counts"]["real_game_exact_state"],4)
        self.assertEqual(doc["counts"]["original_model_selection_matched_release"],4)
        self.assertEqual(doc["original_source_applications"],5)
        self.assertEqual(doc["original_effective_elements"],31)
        self.assertEqual(doc["original_effective_faces"],144)

    def test_s30_is_two_source_models_one_case(self):
        doc=json.loads(f.locked(f.CAPTURE))
        self.assertEqual(doc["source_cases"]["S30"]["original_model_application_count"],2)
        self.assertEqual(doc["source_cases"]["S30"]["original_geometry_faces"],46)

    def test_s22_vanilla_parent_exception_stays_hold(self):
        doc=json.loads(f.locked(f.CAPTURE))
        item=doc["source_cases"]["S22"]
        self.assertIs(item["external_vanilla_parent_independent_runtime_sha_approved"],False)
        self.assertEqual(f.VANILLA_PARENT,"assets/minecraft/models/block/cube.json")
        self.assertEqual(f.VANILLA_PARENT_SHA,
                         "3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e")
        self.assertNotIn("S22",f.CONDITIONAL)

    def test_native_images_and_captured_original_game_action_pinned(self):
        self.assertEqual(len(set(f.NOTES)),4)
        self.assertEqual(f.RUN,45031468054)
        self.assertEqual(f.ARTIFACT_ID,14758360785)
        self.assertEqual(len(f.ZIP_SHA),64)

    def test_unknown_original_blob_must_fail_closed(self):
        saved=f.PIN[str(f.CAPTURE)]
        try:
            f.PIN[str(f.CAPTURE)]="0"*40
            with self.assertRaises(AssertionError):
                f.locked(f.CAPTURE)
        finally:
            f.PIN[str(f.CAPTURE)]=saved

    def test_never_full_approve_F_or_infer_asset_rights(self):
        doc=json.loads(f.locked(f.CAPTURE))
        self.assertEqual(doc["counts"]["newly_approved_1_5_cases"],0)
        self.assertEqual(doc["counts"]["unconditionally_completed_F_cases"],0)
        self.assertEqual(doc["counts"]["newly_approved_INT5_parts_or_INT6_training_rights"],0)

if __name__=="__main__":
    unittest.main()
