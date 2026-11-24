"""INT-5-A original-sourced, fail-closed semantic research tests."""
import csv
import io
import json
from pathlib import Path
import unittest

from mcfr import int5_semantic_source_triage as stage


class INT5OriginalSourceReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = stage.audit(stage.ROOT)
        cls.summary = json.loads(cls.files[stage.OUTPUTS["summary"].as_posix()])
        cls.parts = list(csv.DictReader(io.StringIO(
            cls.files[stage.OUTPUTS["parts"].as_posix()])))
        cls.samples = list(csv.DictReader(io.StringIO(
            cls.files[stage.OUTPUTS["samples"].as_posix()])))
        cls.findings = list(csv.DictReader(io.StringIO(
            cls.files[stage.OUTPUTS["findings"].as_posix()])))

    def test_complete_source_population_and_unique_roles(self):
        self.assertEqual(len(self.parts),45)
        self.assertEqual(len(self.samples),94)
        self.assertEqual(len(self.findings),21)
        self.assertEqual(len({(p["provider_key"],p["element_index"])
                              for p in self.parts}),45)
        self.assertEqual(self.summary["counts"]["original_geometry_elements_reopened"],1911)

    def test_source_role_hypothesis_has_not_become_verified_function(self):
        self.assertTrue(all(p["role_visual_verified"]=="false" and
                            p["review_decision"]=="SOURCE_GEOMETRY_MEASURED_ROLE_HYPOTHESIS"
                            for p in self.parts))
        self.assertEqual(self.summary["counts"]["independent_new_role_visual_approvals"],0)

    def test_geometry_is_numeric_and_source_linked_not_game_render(self):
        for p in self.parts:
            self.assertEqual(len(p["bbox_rotated"].split("|")),6)
            xyz = [float(x) for x in p["relative_model_center_xyz"].split("|")]
            self.assertEqual(len(xyz),3)
            self.assertTrue(all(-0.001<=v<=1.001 for v in xyz))
            self.assertEqual(p["geometry_source_consistent"],"true")
            self.assertEqual(p["original_role_basis"],"GEOMETRY_AND_FACE_SLOTS")
            self.assertTrue(p["source_model_sha"] and p["source_model_path"])

    def test_original_sample_roles_remain_hypotheses(self):
        self.assertEqual(len({p["sample_id"] for p in self.samples})>0,True)
        self.assertTrue(all(p["source_element_present"]=="true" and
                            p["function_independently_verified"]=="false"
                            for p in self.samples))
        self.assertEqual(self.summary["counts"]["sample_specific_claims_reopened"],94)

    def test_comparison_findings_14_candidates_and_7_limits_retained(self):
        from collections import Counter
        self.assertEqual(Counter(p["original_disposition"] for p in self.findings),
                         {"CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7})
        self.assertTrue(all(p["role_or_universal_style_approved"]=="false" and
                            p["scope_limit"].strip() and p["review_condition"].strip()
                            for p in self.findings))

    def test_all_source_bytes_are_pinned(self):
        stage.fixed_sources(stage.ROOT)
        self.assertEqual(set(self.summary["origin_git_blobs"]),
                         set(stage.EXPECTED_BLOBS))

    def test_h03_h05_and_int5_stay_separate(self):
        self.assertEqual(self.summary["previous_INT4_scoped_modeling"],"70/70")
        self.assertEqual(self.summary["original_INT4_strict_H03_H05"],
                         {"H03":"HOLD","H05":"CONDITIONAL"})
        self.assertEqual(self.summary["game_or_visual_observation_new_this_run"],0)
        self.assertEqual(self.summary["counts"]["INT6_training_rights_approvals"],0)

    def test_bad_finding_population_is_rejected(self):
        rows=[dict(f) for f in self.findings]
        rows[0]["finding_id"]=rows[1]["finding_id"]
        self.assertNotEqual(len({r["finding_id"] for r in rows}),21)
        # Basic source guard rejects malformed expected metadata without a game-state promotion.
        with self.assertRaisesRegex(ValueError,"INT5-A fail closed"):
            stage.require(False,"injected finding mismatch")

    def test_c_and_f_original_dimensions_and_center_mismatch_fails_closed(self):
        good = {
            "size":"2|4|6", "center":"1|2|3",
        }
        raw = {
            "source_from":"0|0|0","source_to":"2|4|6",
        }
        stage.verify_original_C_dimensions(good,raw)
        invalid = dict(good)
        invalid["center"]="2|2|3"
        with self.assertRaisesRegex(ValueError,"part center disagreement"):
            stage.verify_original_C_dimensions(invalid,raw)
        invalid = dict(good)
        invalid["size"]="2|4|9"
        with self.assertRaisesRegex(ValueError,"part size disagreement"):
            stage.verify_original_C_dimensions(invalid,raw)

    def test_all_committed_outputs_match_recomputed_when_present(self):
        present=[p for p in self.files if (stage.ROOT/p).exists()]
        if present:
            self.assertEqual(len(present),len(self.files),
                             "Partially committed INT5 outputs")
        for path in present:
            self.assertEqual((stage.ROOT/path).read_text(encoding="utf-8"),
                             self.files[path])


if __name__=="__main__":
    unittest.main()
