"""Offline full-original and mutated-evidence regression tests for INT-4."""
from copy import deepcopy
from pathlib import Path
import unittest

from mcfr import int4_chair_evidence_gate as g

ROOT = Path(__file__).resolve().parents[2]


class INT4ChairEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real = g.read(ROOT)

    def test_complete_original_source_crosslinks_no_approvals(self):
        rows, doc = g.audit(self.real)
        self.assertEqual(len(rows), 45)
        self.assertEqual(doc["counts"]["pr33_element_direction_metadata_links"], 180)
        self.assertEqual(doc["counts"]["unresolved_pixel_source_faces"], 6343)
        self.assertEqual(doc["int5_role_approved"], 0)
        self.assertEqual(doc["int3_exit"], "PASS_FIXED_SOURCE_RELATIONSHIPS_ONLY")
        self.assertEqual({r["child_key"] for r in rows},
                         {"AF121", "AF123", "HC11210", "MACAW67"})
        self.assertTrue(all(r["pr34_evidence_scope"] ==
                            "COHORT_NOT_PR33_INDIVIDUAL_IMAGE_BYTES" for r in rows))

    def test_missing_f2_is_rejected(self):
        e = deepcopy(self.real)
        e["f2"]["collected"]["per_image"].pop()
        with self.assertRaisesRegex(g.AuditError, "F2"):
            g.audit(e)

    def test_wrong_macaw_rotation_is_rejected(self):
        e = deepcopy(self.real)
        photo = next(x for x in e["f2"]["collected"]["per_image"]
                     if x["case_id"] == "MACAW67_north")
        photo["y"] = 0
        with self.assertRaisesRegex(g.AuditError, "rotation"):
            g.audit(e)

    def test_wrong_model_parent_sha_is_rejected(self):
        e = deepcopy(self.real)
        e["uv"]["models"][0]["parent_sha"] = "0" * 40
        with self.assertRaisesRegex(g.AuditError, "provider SHA"):
            g.audit(e)

    def test_duplicate_original_element_is_rejected(self):
        e = deepcopy(self.real)
        e["parts"][1]["element_index"] = e["parts"][0]["element_index"]
        with self.assertRaisesRegex(g.AuditError, "Duplicate"):
            g.audit(e)

    def test_forged_semantic_approval_is_rejected(self):
        e = deepcopy(self.real)
        e["sem"]["role_candidates_visual_verified"] = 1
        with self.assertRaisesRegex(g.AuditError, "approved"):
            g.audit(e)

    def test_af_uv_mismatch_changes_result_to_fail(self):
        e = deepcopy(self.real)
        e["af"]["models"]["uv_changed"] = 1
        with self.assertRaisesRegex(g.AuditError, "AF 4.0.2"):
            g.audit(e)

    def test_unresolved_selector_cannot_be_silently_deleted(self):
        e = deepcopy(self.real)
        e["states"]["totals"]["source_anomaly_rows"] = 0
        with self.assertRaisesRegex(g.AuditError, "anomalous"):
            g.audit(e)

    def test_unresolved_pixel_source_cannot_be_promoted(self):
        e = deepcopy(self.real)
        e["db"]["face_pixel_support"]["SLOT_UNBOUND"] = 0
        with self.assertRaisesRegex(g.AuditError, "pixel support"):
            g.audit(e)


if __name__ == "__main__":
    unittest.main()
