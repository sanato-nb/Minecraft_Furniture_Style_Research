"""F11A original five vanilla native F2 and fixed seventy-row fail-closed checks."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location(
    "f11a_auditor",ROOT/"scripts/integration/build_int4_f11a_vanilla_five_original_f2_audit.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class F11AFrozenStudyAndRealGameEvidence(unittest.TestCase):
    def test_all_three_original_Git_blobs_are_fixed(self):
        for path in (audit.PREV,audit.NEW,audit.STUDY):
            self.assertEqual(audit.blob(audit.locked(path)),audit.PINS[str(path)])

    def test_f10_study_scope_and_original_count(self):
        old=audit.rows(audit.locked(audit.PREV))
        self.assertEqual(len(old),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in old),53)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in old),17)

    def test_five_cases_were_HOLD_not_mixed_with_other_ranges(self):
        old={r["target_id"]:r for r in audit.rows(audit.locked(audit.PREV))}
        self.assertEqual(audit.CASES,("V01","V02","V05","V07","V10"))
        for case in audit.CASES:
            self.assertTrue(old[case]["final_disposition"].startswith("HOLD"))
            self.assertEqual(old[case]["cohort"],"VANILLA")

    def test_real_client_evidence_before_independent_recheck(self):
        j=json.loads(audit.locked(audit.NEW))
        self.assertEqual(j["status"],"PASS_FIVE_OFFICIAL_VANILLA_12111_EXACT_STATE_F2_NOT_FINAL_APPROVAL")
        self.assertEqual(j["official_client_sha1"],audit.CLIENT_SHA1)
        self.assertEqual(j["official_client_sha256"],audit.CLIENT_SHA256)
        self.assertEqual(j["real_game_server_exact_states"],5)
        self.assertEqual(j["real_game_native_original_F2_PNG"],5)
        self.assertEqual(j["source_elements"],6)
        self.assertEqual(j["source_faces"],35)

    def test_original_study_provider_not_always_direct_parent(self):
        j=json.loads(audit.locked(audit.NEW))
        for case in ("V05","V07","V10"):
            self.assertEqual(len(j["source_cases"][case]["official_parent_chain_git_blob_sha1"]),2)
        for case in ("V01","V02"):
            self.assertEqual(len(j["source_cases"][case]["official_parent_chain_git_blob_sha1"]),1)

    def test_original_S2_hypotheses_not_promoted_to_finished_cases(self):
        self.assertEqual((sum(audit.ELEMENT.values()),sum(audit.FACE.values())),(6,35))
        self.assertNotIn("V03",audit.CASES)
        self.assertNotIn("V08",audit.CASES)
        self.assertNotIn("V11",audit.CASES)
        self.assertNotIn("R06",audit.CASES)
        self.assertNotIn("R08",audit.CASES)

    def test_invalid_upstream_SHA_must_fail_closed(self):
        key=str(audit.NEW);original=audit.PINS[key]
        try:
            audit.PINS[key]="0"*40
            with self.assertRaises(AssertionError):
                audit.locked(audit.NEW)
        finally:
            audit.PINS[key]=original

    def test_f11_source_report_not_F_exit_or_AI_rights_approval(self):
        j=json.loads(audit.locked(audit.NEW))
        self.assertEqual(j["full_INT4_F_approved"],0)
        self.assertEqual(j["INT5_part_semantics_approved"],0)
        self.assertEqual(j["INT6_training_or_distribution_rights_approved"],0)

if __name__=="__main__":
    unittest.main()
