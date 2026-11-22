"""Preserve source locked 70-target denominator and two HOLDs after 12 F5 trials."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/"scripts/integration/build_int4_f5_native_properties_audit.py"
spec=importlib.util.spec_from_file_location("f5audit",source)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)

class F5IndependentGuards(unittest.TestCase):
    def test_original_source_blobs_still_pinned(self):
        for p in (f.FIXED,f.PREVIOUS,f.F4,f.SOURCE):
            self.assertEqual(f.blob(f.pin(p)),f.PINS[str(p)])

    def test_previous_f4_70_final_disposition_does_not_autoupgrade(self):
        rows=f.read_csv(f.pin(f.PREVIOUS))
        self.assertEqual(len(rows),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in rows),37)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in rows),33)
        self.assertTrue(all(x["final_disposition"].startswith("HOLD")
                            for x in rows if x["target_id"] in ("S02","S34")))

    def test_f5_report_explicitly_has_no_historical_exact_pass(self):
        j=json.loads(f.pin(f.FIXED))
        self.assertEqual(j["status"],"PASS_REAL_FABRIC_EXACT_PROPERTY_ENUM_AND_F2_NOT_SEMANTIC_EXIT")
        self.assertEqual(j["trial_count"],12)
        self.assertTrue(all(x["exact_server_state_persisted"] is False for x in j["cases"].values()))

    def test_12_original_png_cases_and_independent_qualitative_notes(self):
        j=json.loads(f.pin(f.FIXED))
        self.assertEqual(set(f.OBS),set(j["cases"]))
        self.assertEqual(sum(k.startswith("S02") for k in f.OBS),3)
        self.assertEqual(sum(k.startswith("S34") for k in f.OBS),9)

    def test_known_pinned_artifact_is_single_source(self):
        self.assertEqual(f.RUN,45026378323)
        self.assertEqual(f.ARTIFACT,14755154139)
        self.assertEqual(len(f.ZIP_SHA),64)

    def test_old_case_original_1_5_source_sha(self):
        self.assertEqual(f.sha(f.pin(f.SOURCE)),
                         "da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e")

    def test_input_drift_causes_failure(self):
        old=f.PINS[str(f.FIXED)]
        try:
            f.PINS[str(f.FIXED)]="0"*40
            with self.assertRaises(AssertionError):
                f.pin(f.FIXED)
        finally:
            f.PINS[str(f.FIXED)]=old

if __name__=="__main__":unittest.main()
