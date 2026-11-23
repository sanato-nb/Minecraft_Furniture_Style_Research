"""H6 source-provenance fail-closed log / case / F2 bridge regression."""
import importlib.util,unittest,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"scripts/integration/build_int4_h6_original_f70_log_state_bridge.py"
spec=importlib.util.spec_from_file_location("int4_h6",PATH)
h6=importlib.util.module_from_spec(spec);spec.loader.exec_module(h6)

class H6CaseLogSourceAudit(unittest.TestCase):
    def test_all_original_hash_sources_are_unchanged(self):
        self.assertEqual(len(h6.PINS),7)
        for n in h6.PINS:self.assertEqual(h6.gitblob(h6.original(n)),h6.PINS[n])

    def test_20_origins_91_png_70_cases_and_eight_H_gates(self):
        self.assertEqual(len(h6.csvin(h6.original("INT4_H3_20_ORIGINAL_ARTIFACT_ZIP_SHA_AUDIT_V1.csv"))),20)
        self.assertEqual(len(h6.csvin(h6.original("INT4_H3_91_NATIVE_F2_ORIGINAL_PNG_SHA_AUDIT_V1.csv"))),91)
        self.assertEqual(len(h6.csvin(h6.original("INT4_H3_70_CASE_ORIGINAL_F2_REOPEN_V1.csv"))),70)
        self.assertEqual(len(h6.csvin(h6.original("INT4_H5_EIGHT_REASSESSED_SCOPED_EXIT_GATES_V1.csv"))),8)

    def test_whole_log_hash_only_not_partial_log_region_hash(self):
        q="a"*64
        x={"original_game_client_log_sha256":q,
           "state_check_evidence":[{"log_region_sha256":"b"*64}]}
        self.assertEqual(h6.log_pins(x),{q})

    def test_nested_full_log_pin_accepted(self):
        value="1"*64
        self.assertEqual(h6.log_pins({"version":[{"capture":{"client_log_sha256":value}}]}),{value})

    def test_server_exact_needs_specific_case_not_summary_count(self):
        d={"real_game_server_exact_states":5,"states":[{"case_id":"V03","server_state_verified":True}]}
        self.assertEqual(h6.structured_exact(d,"V01"),[])
        self.assertTrue(h6.structured_exact(d,"V03"))

    def test_server_states_subject_exact_boolean_is_per_case(self):
        x={"server_states":{"S03":{"subject":{"exact":True}},"S04":{"subject":{"exact":False}}}}
        self.assertTrue(h6.structured_exact(x,"S03"))
        self.assertFalse(h6.structured_exact(x,"S04"))

    def test_no_risk_inherits_normal_historic_state(self):
        d={"server_states":{"S43":{"subject":{"exact":True}}},
           "states":[{"case_id":"AFV3_north","server_blockstate_verified":True}]}
        for case in ("R06","R07","R08"):self.assertEqual(h6.structured_exact(d,case),[])

    def test_risk_requires_id_and_all_exact_evidence(self):
        good={"risk_id":"R06","state_check_evidence":[{"PASS":True},{"PASS":True}]}
        bad={"risk_id":"R06","state_check_evidence":[{"PASS":True},{"PASS":False}]}
        self.assertTrue(h6.structured_exact(good,"R06"))
        self.assertEqual(h6.structured_exact(bad,"R06"),[])
        self.assertEqual(h6.structured_exact(good,"S43"),[])

    def test_exact_photo_requires_both_png_name_and_sha(self):
        digest="c"*64
        d={"states":[{"case_id":"V01","screenshot_file":"V01.png",
                      "screenshot_sha256":digest,"server_state_verified":True}]}
        self.assertTrue(h6.png_filename_sha_in_capture(d,"V01.png",digest))
        self.assertFalse(h6.png_filename_sha_in_capture(d,"V02.png",digest))
        self.assertFalse(h6.png_filename_sha_in_capture(d,"V01.png","b"*64))

    def test_photo_map_png_name_and_hash_for_case(self):
        digest="d"*64
        d={"native_f2_sha256":{"S30":digest,"S31":"a"*64}}
        self.assertTrue(h6.png_filename_sha_in_capture(d,"S30.png",digest))
        self.assertFalse(h6.png_filename_sha_in_capture(d,"S31.png",digest))

    def test_log_line_word_boundaries(self):
        log="[CHAT] S03 subject exact\n[CHAT] S030 subject exact\nS03 screenshot saved\nS03_same key\n"
        self.assertEqual(h6.log_line_mentions(log,"S03"),(2,1))

    def test_source_review_never_implies_full_f_contract(self):
        j=json.loads(h6.original("INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json"))
        self.assertEqual(j["F_unconditional_full_exit_approved"],0)
        self.assertEqual(j["H_gate_hold"],1)
        self.assertEqual(j["H_gate_conditional"],1)
        self.assertFalse(j["H_all_eight_gates_fully_satisfied"])

if __name__=="__main__":unittest.main()
