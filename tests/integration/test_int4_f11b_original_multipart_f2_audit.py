"""F11B independent original five vanilla state, multipart and 70-row locks."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_f11b_original_multipart_f2_audit.py"
spec=importlib.util.spec_from_file_location("int4_f11b_multipart_auditor",path)
auditor=importlib.util.module_from_spec(spec)
spec.loader.exec_module(auditor)

class IndependentF11BOriginalSource(unittest.TestCase):
    def test_original_git_blobs_unchanged(self):
        for p in (auditor.PREV,auditor.NEW,auditor.STUDY):
            self.assertEqual(auditor.blob(auditor.locked(p)),auditor.PINS[str(p)])

    def test_previous_70_scope_is_frozen(self):
        records=auditor.rows(auditor.locked(auditor.PREV))
        self.assertEqual(len(records),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in records),58)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in records),12)

    def test_five_new_historical_vanilla_holds_before_audit(self):
        records={x["target_id"]:x for x in auditor.rows(auditor.locked(auditor.PREV))}
        self.assertEqual(auditor.CASES,("V03","V04","V06","V08","V09"))
        for cid in auditor.CASES:
            self.assertEqual(records[cid]["cohort"],"VANILLA")
            self.assertTrue(records[cid]["final_disposition"].startswith("HOLD"))

    def test_exact_five_states_and_twelve_selected_models(self):
        j=json.loads(auditor.locked(auditor.NEW))
        self.assertEqual(j["original_historical_case_ids"],list(auditor.CASES))
        self.assertEqual(j["original_model_applications"],12)
        self.assertEqual(j["original_source_elements"],13)
        self.assertEqual(j["original_source_faces"],45)
        self.assertEqual(j["real_game_server_exact_states"],5)
        self.assertEqual(j["real_game_native_F2_count"],5)

    def test_multipart_rule_indices_from_actual_study(self):
        j=json.loads(auditor.locked(auditor.NEW))
        self.assertEqual([x["original_rule_index"] for x in
                          j["source_cases"]["V03"]["original_applications"]],[0,1])
        self.assertEqual([x["original_rule_index"] for x in
                          j["source_cases"]["V08"]["original_applications"]],[0,1,4,6,8,10,12])

    def test_fence_connected_and_open_barrel_exact_state(self):
        j=json.loads(auditor.locked(auditor.NEW))
        self.assertEqual(j["source_cases"]["V03"]["original_state"],
                         "minecraft:oak_fence[east=false,north=true,south=false,west=false]")
        self.assertEqual(j["source_cases"]["V06"]["original_state"],
                         "minecraft:barrel[facing=north,open=true]")

    def test_white_wool_has_independent_visible_white_pixels(self):
        j=json.loads(auditor.locked(auditor.NEW))
        self.assertGreaterEqual(j["native_F2_visible_pixel_counts"]["V09"]["neutral_white"],300)

    def test_actual_original_game_sha_and_artifact_id(self):
        self.assertEqual(auditor.RUN,45098021558)
        self.assertEqual(auditor.ARTIFACT,14784297231)
        self.assertEqual(len(auditor.ZIP_SHA),64)

    def test_fail_closed_when_historic_git_blob_changes(self):
        key=str(auditor.NEW);was=auditor.PINS[key]
        try:
            auditor.PINS[key]="0"*40
            with self.assertRaises(AssertionError):auditor.locked(auditor.NEW)
        finally:
            auditor.PINS[key]=was

    def test_no_unconditional_semantic_or_redistribution_acceptance(self):
        j=json.loads(auditor.locked(auditor.NEW))
        self.assertEqual(j["full_F_approved"],0)
        self.assertEqual(j["INT5_part_semantics_approved"],0)
        self.assertEqual(j["INT6_AI_training_or_redistribution_rights_approved"],0)

if __name__=="__main__":
    unittest.main()
