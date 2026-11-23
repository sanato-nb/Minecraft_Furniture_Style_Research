"""F11E R06 Macaw original ZIP and fixed 70 targets independent audit regression."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
file=ROOT/"scripts/integration/build_int4_f11e_r06_temporal_f2_audit.py"
spec=importlib.util.spec_from_file_location("int4_f11e_r06_auditor",file)
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class IndependentR06TemporalAudit(unittest.TestCase):
    def test_three_original_git_blob_source_pins(self):
        for key in (a.PREV,a.NEW,a.STUDY):
            self.assertEqual(a.blob(a.locked(key)),a.PINS[str(key)])

    def test_previous_70_targets_conditional68_HOLD2(self):
        rows=a.rows(a.locked(a.PREV))
        self.assertEqual(len(rows),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in rows),68)
        self.assertEqual({x["target_id"] for x in rows if x["final_disposition"].startswith("HOLD")},
                         {"R06","R08"})

    def test_original_S42_and_S43_same_mod_model_family(self):
        rows=a.rows(a.locked(a.STUDY))
        originals={r["case"]:r for r in rows if r["case"] in ("S42","S43")}
        self.assertEqual(len(originals),2)
        self.assertEqual(originals["S42"]["block"],originals["S43"]["block"])
        self.assertEqual(originals["S42"]["state"],"facing=north;water=false")
        self.assertEqual(originals["S43"]["state"],"facing=north;water=true")
        self.assertEqual(int(originals["S42"]["faces"]),55)
        self.assertEqual(int(originals["S43"]["faces"]),56)

    def test_original_capture_reports_minimum_three_states_and_frames(self):
        j=json.loads(a.locked(a.NEW))
        self.assertEqual(j["risk_id"],"R06")
        self.assertEqual(j["historical_source_case"],"S43")
        self.assertEqual(j["real_exact_server_state_checks"],3)
        self.assertEqual(j["original_native_F2_count"],3)
        self.assertEqual(set(j["native_F2_sha256"]),set(a.KEYS))

    def test_monotonic_real_time_intervals(self):
        j=json.loads(a.locked(a.NEW))
        self.assertEqual(len(j["time_intervals_seconds"]),2)
        self.assertGreaterEqual(min(j["time_intervals_seconds"]),8.)

    def test_water_blue_visible_and_static_stone_control(self):
        j=json.loads(a.locked(a.NEW))
        p=j["pixel_observation"]
        self.assertGreaterEqual(min(p["foreground_blue_water_pixels_each_frame"].values()),200)
        self.assertLessEqual(p["max_background_stone_control_delta"],40)
        self.assertEqual(p["water_roi"],list(a.WATER_ROI))

    def test_original_temporal_observation_not_code_causality(self):
        j=json.loads(a.locked(a.NEW))
        self.assertFalse(j["water_animation_causally_proven"])
        self.assertIn("NOT_",j["pixel_observation"]["temporal_interpretation"])

    def test_final_F_INT5_INT6_all_unapproved(self):
        j=json.loads(a.locked(a.NEW))
        self.assertEqual((j["full_F_approved"],j["INT5_semantics_approved"],
                          j["INT6_training_or_redistribution_rights_approved"]),(0,0,0))

    def test_source_mod_jar_sha_locked(self):
        j=json.loads(a.locked(a.NEW))
        self.assertEqual(j["source_mod_jar_sha256"],a.MACAW_SHA256)
        self.assertEqual(j["historical_source_case"],"S43")

    def test_fail_closed_when_70_row_ledger_is_modified(self):
        key=str(a.PREV);orig=a.PINS[key]
        try:
            a.PINS[key]="0"*40
            with self.assertRaises(AssertionError):
                a.locked(a.PREV)
        finally:
            a.PINS[key]=orig

if __name__=="__main__":
    unittest.main()
