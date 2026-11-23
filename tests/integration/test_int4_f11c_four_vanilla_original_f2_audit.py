"""F11C original vanilla V12–V15 Git/source/F2 independent denominator tests."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
module=ROOT/"scripts/integration/build_int4_f11c_four_vanilla_original_f2_audit.py"
spec=importlib.util.spec_from_file_location("int4_f11c_audit",module)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class F11CIndependentSourceAudit(unittest.TestCase):
    def test_all_three_immutable_inputs_have_correct_git_sha(self):
        for path in (audit.PREV,audit.NEW,audit.STUDY):
            self.assertEqual(audit.blob(audit.locked(path)),audit.PINS[str(path)])

    def test_previous_case_denominator_is_70_conditional63_HOLD7(self):
        ledger=audit.rows(audit.locked(audit.PREV))
        self.assertEqual(len(ledger),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in ledger),63)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in ledger),7)

    def test_four_both_historical_and_current_cases(self):
        self.assertEqual(audit.CASES,("V12","V13","V14","V15"))
        original=audit.rows(audit.locked(audit.STUDY))
        self.assertEqual({k:len([r for r in original if r["case"]==k]) for k in audit.CASES},
                         {k:1 for k in audit.CASES})

    def test_original_36_elements_154_faces(self):
        self.assertEqual(audit.GEOMETRY,
                         {"V12":(13,58),"V13":(14,59),"V14":(4,15),"V15":(5,22)})
        self.assertEqual(tuple(map(sum,zip(*audit.GEOMETRY.values()))),(36,154))

    def test_original_v11_special_bed_not_promoted(self):
        self.assertNotIn("V11",audit.CASES)
        self.assertNotIn("R06",audit.CASES)
        self.assertNotIn("R08",audit.CASES)

    def test_exact_actual_game_four_F2_and_client_source_hash(self):
        j=json.loads(audit.locked(audit.NEW))
        self.assertEqual(j["historical_case_ids"],list(audit.CASES))
        self.assertEqual(j["real_game_exact_server_states"],4)
        self.assertEqual(j["original_native_F2_PNG"],4)
        self.assertEqual(j["official_client_sha1"],audit.CLIENT_SHA1)
        self.assertEqual(j["official_client_sha256"],audit.CLIENT_SHA256)

    def test_dark_cauldron_has_second_visibility_proxy(self):
        j=json.loads(audit.locked(audit.NEW))
        self.assertGreaterEqual(j["native_F2_visibility_pixels"]["V12"]["dark_gray"],200)

    def test_main_F_approval_and_INT5_INT6_are_not_faked(self):
        j=json.loads(audit.locked(audit.NEW))
        self.assertEqual(j["unconditionally_full_F_approved"],0)
        self.assertEqual(j["INT5_part_semantics_approved"],0)
        self.assertEqual(j["INT6_training_or_redistribution_rights_approved"],0)

    def test_bad_input_git_blob_fails_closed(self):
        key=str(audit.STUDY)
        old=audit.PINS[key]
        try:
            audit.PINS[key]="0"*40
            with self.assertRaises(AssertionError):
                audit.locked(audit.STUDY)
        finally:
            audit.PINS[key]=old

    def test_original_native_zip_hex_digest_required(self):
        self.assertEqual(len(audit.ZIP_SHA),64)
        self.assertGreater(audit.RUN,0)
        self.assertGreater(audit.ARTIFACT,0)

if __name__=="__main__":
    unittest.main()
