"""Independent V11 special bed F2 SHA evidence and exact F70 scope lock."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"scripts/integration/build_int4_f11d_v11_white_bed_original_f2_audit.py"
spec=importlib.util.spec_from_file_location("f11d_real_bed_independent_audit",path)
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class V11IndependentEvidenceTests(unittest.TestCase):
    def test_frozen_original_sources(self):
        for filename in (a.PREV,a.NEW,a.STUDY):
            self.assertEqual(a.blob(a.locked(filename)),a.PINS[str(filename)])

    def test_previous_70_denominator(self):
        original=a.rows(a.locked(a.PREV))
        self.assertEqual(len(original),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in original),67)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in original),3)
        self.assertEqual([x["final_disposition"] for x in original if x["target_id"]=="V11"],
                         ["HOLD_NO_EXACT_CASE_F2_LINKED"])

    def test_historic_original_bed_no_ordinary_geometry(self):
        original=[r for r in a.rows(a.locked(a.STUDY)) if r["case"]=="V11"]
        self.assertEqual(len(original),1)
        row=original[0]
        self.assertEqual(row["geometry_status"],"NO_ORDINARY_ELEMENTS")
        self.assertEqual((int(row["elements"]),int(row["faces"])),(0,0))
        self.assertEqual(row["model_sha"],a.MODEL_SHA1)
        self.assertEqual(row["state_sha"],a.STATE_SHA1)
        self.assertFalse(row["provider_path"])

    def test_actual_bed_foot_head_and_paired_control_four_png(self):
        evidence=json.loads(a.locked(a.NEW))
        self.assertEqual(evidence["historical_case_id"],"V11")
        self.assertEqual(evidence["real_game_two_exact_server_blockstates"],2)
        self.assertEqual(evidence["actual_original_native_F2_PNG_count"],4)
        self.assertEqual(set(evidence["native_F2_png_sha256"]),set(a.IMAGES))

    def test_real_bed_contrast_is_above_original_baseline(self):
        metrics=json.loads(a.locked(a.NEW))["same_camera_air_vs_bed_pixel_contrast"]
        self.assertLessEqual(metrics["air_control_changed_pixels"],250)
        self.assertGreaterEqual(metrics["bed_vs_air_changed_pixels"],700)
        self.assertGreater(metrics["bed_vs_air_changed_pixels"],
                           metrics["air_control_changed_pixels"]*5)
        self.assertEqual(metrics["roi"],list(a.ROI))

    def test_official_mojang_client_and_source_SHA(self):
        evidence=json.loads(a.locked(a.NEW))
        self.assertEqual(evidence["official_client_sha256"],a.CLIENT_SHA256)
        self.assertEqual(evidence["original_study_sha256"],a.STUDY_SHA)
        self.assertEqual(evidence["source_model_git_blob_sha1"],a.MODEL_SHA1)
        self.assertEqual(evidence["source_blockstate_git_blob_sha1"],a.STATE_SHA1)

    def test_special_renderer_java_call_not_claimed(self):
        evidence=json.loads(a.locked(a.NEW))
        self.assertFalse(evidence["direct_special_renderer_java_call_verified"])
        self.assertTrue(evidence["original_no_ordinary_elements_or_faces"])

    def test_full_F_INT5_INT6_not_approved(self):
        evidence=json.loads(a.locked(a.NEW))
        self.assertEqual((evidence["full_F_approved"],evidence["INT5_part_semantics_approved"],
                          evidence["INT6_AI_training_or_redistribution_rights_approved"]),(0,0,0))

    def test_conditional_target_not_other_pending_R_cases(self):
        self.assertNotIn("R06",a.IMAGES)
        self.assertNotIn("R08",a.IMAGES)
        self.assertEqual(a.IMAGES,("V11_AIR_A","V11_AIR_B","V11_BED","V11_BED_SIDE"))

    def test_fail_closed_original_SHA_change(self):
        key=str(a.PREV);value=a.PINS[key]
        try:
            a.PINS[key]="0"*40
            with self.assertRaises(AssertionError):
                a.locked(a.PREV)
        finally:
            a.PINS[key]=value

if __name__=="__main__":
    unittest.main()
