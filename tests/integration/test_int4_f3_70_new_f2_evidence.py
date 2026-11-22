"""Independent confidence guards for seven real-game F2 and 70 original cases."""
from pathlib import Path
import importlib.util
import csv
import io
import json
import unittest

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"scripts/integration/build_int4_f3_70_new_f2_evidence.py"
sp=importlib.util.spec_from_file_location("int4f3_evidence",SCRIPT)
f=importlib.util.module_from_spec(sp)
sp.loader.exec_module(f)


def table(blob):
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8"))))


class SevenOriginalF2CrossAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items=f.run_audit()
        cls.summary=json.loads(cls.items[f.I/"INT4_F3_7_DIRECT_IMAGE_VISUAL_AUDIT_V1.json"])
        cls.target=table(cls.items[f.I/"INT4_F3_70_TARGET_EVIDENCE_DISPOSITIONS_V3.csv"])
        cls.queue=table(cls.items[f.I/"INT4_F3_38_PENDING_EXACT_F2_CASES_V1.csv"])
        cls.exc=table(cls.items[f.I/"INT4_F3_3_RENDER_SOURCE_EXCEPTIONS_V1.csv"])

    def test_cannot_approve_historical_source_if_sha_changed(self):
        name=f.BASE
        saved=f.PINS[name]
        try:
            f.PINS[name]="0"*40
            with self.assertRaises(AssertionError):
                f.run_audit()
        finally:
            f.PINS[name]=saved

    def test_7_server_state_evidence_registered(self):
        self.assertEqual(tuple(self.summary["cases"]),tuple(sorted(f.CASE_IDS)))
        for v in self.summary["cases"].values():
            self.assertEqual(v["server_readback_exact"],"PASS")
            self.assertEqual(v["model_selection_matches_release"],"PASS")

    def test_old_cases_unchanged_except_seven(self):
        old={x["target_id"]:x for x in f.orig_rows()}
        new={x["target_id"]:x for x in self.target}
        self.assertEqual(len(old),len(new))
        self.assertEqual(len(old),70)
        self.assertEqual({k for k in old if old[k]!=new[k]},set(f.CASE_IDS))

    def test_pixelwise_identical_drawer_state_is_not_falsely_approved(self):
        first=self.summary["cases"]["S20"]
        second=self.summary["cases"]["S21"]
        self.assertEqual(first["original_game_native_f2_png_sha256"],
                         second["original_game_native_f2_png_sha256"])
        self.assertNotEqual(first["original_exact_block_state"],
                            second["original_exact_block_state"])
        self.assertNotEqual(first["original_model_key"],second["original_model_key"])
        self.assertTrue(any("DRAWER" in x["exception_id"] for x in self.exc))
        self.assertEqual(len(self.exc),3)

    def test_original_model_source_release_byte_equality_is_not_upcast(self):
        r=self.summary["cases"]
        for k in ("S20","S21","S26","S44","S45","S46"):
            self.assertEqual(set(r[k]["research_model_state_provider_bytes_equal_release"].values()),{False})
        self.assertEqual(set(r["S27"]["research_model_state_provider_bytes_equal_release"].values()),{True})

    def test_case_types_and_counts(self):
        self.assertEqual(len(self.target),70)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in self.target),32)
        self.assertEqual(sum(x["final_disposition"].startswith("HOLD") for x in self.target),38)
        hist=[x for x in self.target if x["target_kind"]=="HISTORICAL_1_5_CASE"]
        self.assertEqual(len(hist),62)
        self.assertEqual(sum(x["final_disposition"].startswith("CONDITIONAL") for x in hist),26)

    def test_both_critical_risks_remain_hold(self):
        hold={x["target_id"] for x in self.queue}
        self.assertEqual(len(hold),38)
        self.assertIn("R06",hold)
        self.assertIn("R08",hold)
        self.assertNotIn("R01",hold)
        self.assertNotIn("S20",hold)
        self.assertNotIn("S21",hold)

    def test_not_actual_full_exit_or_AI_rights(self):
        self.assertEqual(self.summary["counts"]["F_targets_unconditionally_accepted"],0)
        self.assertEqual(self.summary["counts"]["new_AI_part_semantics_approved"],0)
        self.assertEqual(self.summary["counts"]["new_original_asset_AI_training_or_redistribution_rights_approved"],0)
        self.assertTrue(all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in self.target))

    def test_7_original_shots_only_six_unique(self):
        self.assertEqual(self.summary["counts"]["new_case_png_occurrences"],7)
        self.assertEqual(self.summary["counts"]["new_case_distinct_png_sha"],6)
        self.assertEqual(self.summary["counts"]["different_source_state_same_F2_png_case_pairs"],1)
        self.assertEqual(self.summary["source_Github_Actions_artifact_zip_sha256"],f.ZIP_SHA256)

    def test_artifacts_have_deterministic_bytes(self):
        another=f.run_audit()
        self.assertEqual(self.items,another)

    def test_does_not_invent_game_rights_and_complete_model_roles(self):
        for item in self.summary["cases"].values():
            self.assertEqual(item["baked_uv_or_semantic_approved"],"false")
            self.assertEqual(item["licensing_approved"],"false")
        self.assertEqual(self.summary["progress"]["G_and_H_independent_final_audit"],"NOT_STARTED")


if __name__=="__main__":unittest.main()
