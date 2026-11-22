"""INT-4-F10 frozen 70-case provenance and five original native F2 guards."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"scripts/integration/build_int4_f10_macaw_five_original_f2_audit.py"
spec=importlib.util.spec_from_file_location("f10_auditor",SOURCE)
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)

class F10OriginalGameIndependentAudit(unittest.TestCase):
    def test_four_source_git_blobs_are_immutable(self):
        for p in (f.PREV,f.F9_AUDIT,f.F10_CAPTURE,f.HISTORICAL):
            self.assertEqual(f.blob(f.locked(p)),f.LOCKS[str(p)])

    def test_previous_seventy_cases_remain_48_conditional_and_22_hold(self):
        items=f.csvrows(f.locked(f.PREV))
        self.assertEqual(len(items),70)
        self.assertEqual(len({x["target_id"] for x in items}),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in items),48)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in items),22)

    def test_original_f10_five_are_previous_hold(self):
        items=f.csvrows(f.locked(f.PREV))
        self.assertEqual(f.CASES,("S13","S24","S25","S35","S36"))
        for k in f.CASES:
            case=next(x for x in items if x["target_id"]==k)
            self.assertTrue(case["final_disposition"].startswith("HOLD"))

    def test_frozen_original_applications_five_geometry(self):
        entries=f.csvrows(f.locked(f.HISTORICAL))
        self.assertEqual(f.sha256(f.locked(f.HISTORICAL)),f.HIST_SHA256)
        self.assertEqual(sum(f.ELEMENTS.values()),30)
        self.assertEqual(sum(f.FACES.values()),171)
        for case in f.CASES:
            originals=[r for r in entries if r["case"]==case]
            self.assertEqual(len(originals),1)
            r=originals[0]
            self.assertEqual(r["block"],f.EXPECTED[case][0])
            self.assertEqual(r["state"],f.EXPECTED[case][1])
            self.assertEqual((int(r["elements"]),int(r["faces"])),(f.ELEMENTS[case],f.FACES[case]))

    def test_real_game_report_five_states_and_sha(self):
        m=json.loads(f.locked(f.F10_CAPTURE))
        self.assertEqual(m["status"],"PASS_EXACT_FIVE_ORIGINAL_1_21_11_MACAW_SOURCE_STATES_ACTUAL_F2")
        self.assertEqual((m["server_exact_blockstates"],m["native_F2_original_images"]),(5,5))
        self.assertEqual(m["original_model_faces"],171)
        self.assertEqual(m["macaw_mod_jar_sha256"],f.MACAW_JAR_SHA256)
        self.assertEqual(set(m["native_F2_SHA256"]),set(f.CASES))

    def test_F10_still_does_not_certify_any_semantic_or_rights(self):
        m=json.loads(f.locked(f.F10_CAPTURE))
        self.assertEqual(m["full_F_accepted"],0)
        self.assertEqual(m["INT5_part_semantics_approved"],0)
        self.assertEqual(m["INT6_rights_approved"],0)
        self.assertFalse(m["boundaries"]["natural_connected_block_update_rules_tested"])
        self.assertFalse(m["boundaries"]["face_uv_render_pixel_causality_proven"])

    def test_original_zip_artifact_pin_not_guessing_images(self):
        self.assertEqual(f.RUN,45039429134)
        self.assertEqual(f.ARTIFACT,14761291650)
        self.assertEqual(len(f.ZIP_SHA256),64)
        self.assertNotEqual(f.ZIP_SHA256,"0"*64)

    def test_blob_pin_drift_rejected(self):
        saved=f.LOCKS[str(f.F10_CAPTURE)]
        try:
            f.LOCKS[str(f.F10_CAPTURE)]="0"*40
            with self.assertRaises(AssertionError):
                f.locked(f.F10_CAPTURE)
        finally:
            f.LOCKS[str(f.F10_CAPTURE)]=saved

if __name__=="__main__":
    unittest.main()
