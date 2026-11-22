"""INT-4-F2: independent cross-audit of 70-target disposition after four real F2s."""
from __future__ import annotations
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
I=ROOT/"project/integration"
OLD="INT4_F_70_TARGET_EVIDENCE_DISPOSITIONS_V1.csv"
NEW="INT4_F2_70_TARGET_EVIDENCE_DISPOSITIONS_V2.csv"
PRIOR="INT4_F2_NEW4_ACTUAL_CLIENT_SOURCE_SUMMARY_V1.json"
VISUAL="INT4_F2_4_DIRECT_IMAGE_VISUAL_AUDIT_V1.json"
QUEUE="INT4_F2_45_PENDING_EXACT_F2_CASES_V1.csv"
CHANGED={"S05","S06","S07","S10","R01"}
ZIP_SHA="4f9e738ce5cd0f7d9e0e68c6af47df8975d26ac18395c5b33c802d6c343e0ea7"

def load_csv(name):
    with (I/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def indexed(rows,key):
    result={}
    for r in rows:
        k=r[key]
        assert k not in result,("DUPLICATE",k)
        result[k]=r
    return result

def load_json(name):
    return json.loads((I/name).read_text(encoding="utf-8"))

def git_blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class F2CrossSourceReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before=indexed(load_csv(OLD),"target_id")
        cls.after=indexed(load_csv(NEW),"target_id")
        cls.original=load_json(PRIOR)
        cls.review=load_json(VISUAL)
        cls.queue=indexed(load_csv(QUEUE),"target_id")

    def test_source_locked_originals(self):
        self.assertEqual(git_blob_sha((I/OLD).read_bytes()),
                         "c21cc46630a72647fd744073be823bd68b5738a4")
        self.assertEqual(git_blob_sha((I/PRIOR).read_bytes()),
                         "aded01861ca3b8df8ad608092a416a7ff1ebfbb7")
        self.assertEqual(self.review["source_F70_Git_blob_sha1"],
                         "c21cc46630a72647fd744073be823bd68b5738a4")
        self.assertEqual(self.review["source_runtime_Git_blob_sha1"],
                         "aded01861ca3b8df8ad608092a416a7ff1ebfbb7")

    def test_one_to_one_preservation(self):
        self.assertEqual(len(self.before),len(self.after))
        self.assertEqual(set(self.after),set(self.before))
        self.assertEqual(len(self.after),70)
        self.assertEqual(set(k for k in self.after if self.after[k]!=self.before[k]),CHANGED)
        self.assertEqual(len(self.queue),45)

    def test_four_real_server_exact_images_independent(self):
        self.assertEqual(self.original["cases"],["S05","S06","S07","S10"])
        self.assertEqual(self.original["native_f2_png_count"],4)
        self.assertEqual(self.review["original_artifact_ZIP_sha256"],ZIP_SHA)
        for k in ("S05","S06","S07","S10"):
            orig=self.original["source_files_by_case"][k]
            img=self.review["cases"][k]
            row=self.after[k]
            self.assertTrue(orig["server_exact_state_readback"])
            self.assertTrue(orig["original_source_model_selection_equals_release"])
            self.assertEqual(img["original_F2_png_sha256"],orig["native_f2_sha256"])
            self.assertEqual(row["image_sha256s"],orig["native_f2_sha256"])
            self.assertEqual(row["original_zip_sha256s"],ZIP_SHA)
            self.assertEqual(row["image_run_ids"],"45006039419")
            self.assertEqual(row["image_artifact_ids"],"14747628657")
            self.assertEqual(row["runtime_evidence_accepted_as_full_F_PASS"],"false")
            self.assertTrue(row["final_disposition"].startswith("CONDITIONAL"))
            self.assertTrue(img["direct_screenshot_visual_observation"])

    def test_r01_is_only_a_conditional_S10_reuse(self):
        self.assertEqual(self.after["R01"]["image_sha256s"],
                         self.after["S10"]["image_sha256s"])
        self.assertEqual(self.after["R01"]["image_files"],
                         self.after["S10"]["image_files"])
        self.assertTrue(self.after["R01"]["final_disposition"].startswith("CONDITIONAL"))
        self.assertEqual(self.after["R01"]["runtime_evidence_accepted_as_full_F_PASS"],"false")

    def test_known_Af_4_0_2_vs_4_0_3_source_drift(self):
        orig=self.original["source_files_by_case"]
        self.assertEqual(orig["S05"]["pinned_release_file_equality"],
                         {"state":False,"model":False,"provider":False})
        for k in ("S06","S07","S10"):
            self.assertEqual(orig[k]["pinned_release_file_equality"],
                             {"state":True,"model":True,"provider":True})
        self.assertTrue(self.review["notes"]["AF_versions"])

    def test_correct_hold_counts(self):
        cases=Counter(x["final_disposition"].startswith("CONDITIONAL")
                      for x in self.after.values())
        self.assertEqual(cases[True],25)
        self.assertEqual(cases[False],45)
        self.assertEqual({k for k,r in self.after.items()
                          if r["final_disposition"].startswith("HOLD")},set(self.queue))
        self.assertEqual({k for k in self.queue if k.startswith("R")},{"R06","R08"})
        self.assertEqual(Counter(r["cohort"] for r in self.queue.values()),
                         Counter({"VANILLA":15,"AF":13,"HC":5,"MACAW":10,"RISK":2}))

    def test_not_fully_approved_any_of_70(self):
        self.assertTrue(all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false"
                            for x in self.after.values()))
        self.assertEqual(self.review["reconciled_counts"]["full_F_accepted"],0)
        self.assertEqual(self.review["notes"]["release_or_part_rights_approved"],0)
        self.assertFalse(self.original["evidence_limits"]["original_case_F2_proves_pixelwise_UV_equivalence"])
        self.assertEqual(self.original["evidence_limits"]["int5_semantic_approvals"],0)
        self.assertEqual(self.original["evidence_limits"]["int6_training_redistribution_rights_approved"],0)

    def test_case_count_19_43(self):
        cases=[r for r in self.after.values() if r["target_kind"]=="HISTORICAL_1_5_CASE"]
        self.assertEqual(len(cases),62)
        self.assertEqual(sum(r["final_disposition"].startswith("CONDITIONAL") for r in cases),19)
        self.assertEqual(sum(r["final_disposition"].startswith("HOLD") for r in cases),43)

if __name__=="__main__":
    unittest.main()
