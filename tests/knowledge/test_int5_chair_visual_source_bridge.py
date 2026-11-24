"""INT-5-B source-only F2 bridge: independent positive and negative controls."""
import csv
import io
import json
import unittest
from mcfr import int5_chair_visual_source_bridge as b


class INT5ChairEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = b.pinned()
        cls.roles,cls.shots,cls.report = b.calculate(cls.original)

    def test_45_source_parts_and_16_real_game_shots_correlate_without_roles(self):
        self.assertEqual(len(self.roles),45)
        self.assertEqual(len(self.shots),16)
        self.assertEqual(self.report["counts"]["source_faces_across_children"],229)
        self.assertEqual(self.report["counts"]["unique_source_PNG"],8)
        self.assertTrue(all(x["semantic_part_role_verified"]=="false" for x in self.roles))
        self.assertTrue(all(x["element_level_visual_role_approved"]=="false" for x in self.shots))

    def test_4_distinct_models_and_four_direction_shots_each(self):
        from collections import Counter
        self.assertEqual(Counter(x["source_id"] for x in self.roles),{"AF":20,"HC":13,"MACAW":12})
        for x in self.roles:
            self.assertEqual(len(x["same_child_native_F2_case_ids"].split("|")),4)
            self.assertEqual(len(x["same_child_native_F2_sha256s"].split("|")),4)
            self.assertTrue(x["source_provider_git_sha"])
            self.assertEqual(x["model_parent_json_byte_identity_in_runtime"],"NOT_VERIFIED")

    def test_af_release_difference_must_remain_unresolved(self):
        self.assertEqual(sum(x["source_and_runtime_blockstate_sha_match"]=="false"
                             for x in self.roles),20)
        self.assertEqual(sum(x["source_and_runtime_blockstate_sha_match"]=="true"
                             for x in self.roles),25)
        self.assertEqual(self.report["counts"]["AF_candidates_with_known_research_vs_release_state_file_diff"],20)

    def test_historic_source_sha_blob_matches_exact_git_records(self):
        for name,data in self.original.items():
            self.assertEqual(b.git_blob_sha(data),b.PINS[name])

    def test_16_f2_real_server_and_image_sha_are_distinct(self):
        self.assertEqual(len({x["case_id"] for x in self.shots}),16)
        self.assertEqual(len({x["native_F2_sha256"] for x in self.shots}),16)
        self.assertTrue(all(x["original_server_state_verified"]=="true" for x in self.shots))
        self.assertEqual(self.report["counts"]["specific_element_to_F2_pixel_observations"],0)

    def test_no_accidental_training_or_material_approvals(self):
        self.assertEqual(self.report["counts"]["role_approvals"],0)
        self.assertEqual(self.report["counts"]["material_style_approvals"],0)
        self.assertEqual(self.report["counts"]["INT6_training_redistribution_rights_approved"],0)
        self.assertEqual(self.report["counts"]["new_F2_directly_visual_inspected"],0)

    def test_exact_one_original_f2_sha_tamper_blocks_mapping(self):
        changed=dict(self.original)
        path="INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json"
        doc=json.loads(changed[path])
        doc["collected"]["per_image"][0]["sha256"]="bad"
        changed[path]=json.dumps(doc).encode("utf-8")
        with self.assertRaisesRegex(ValueError,"F2 source/camera/selected model"):
            b.calculate(changed)

    def test_original_source_provider_mismatch_blocks_mapping(self):
        changed=dict(self.original)
        path="INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json"
        doc=json.loads(changed[path])
        doc["models"][0]["parent_sha"]="fake"
        changed[path]=json.dumps(doc).encode("utf-8")
        with self.assertRaisesRegex(ValueError,"nonunique original provider SHA|no unique parent/texture child"):
            b.calculate(changed)

    def test_original_blockstate_release_drift_must_not_be_erased(self):
        changed=dict(self.original)
        path="INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json"
        doc=json.loads(changed[path])
        for version in doc["collected"]["versions"]:
            for key,s in version["blockstate_source"].items():
                if key=="another_furniture:acacia_chair":
                    s["byte_identical_to_research"]=True
        changed[path]=json.dumps(doc).encode("utf-8")
        with self.assertRaisesRegex(ValueError,"source/runtime equal claim but digest differs"):
            b.calculate(changed)

    def test_stored_derived_rows_and_hashes_replay(self):
        data=b.outputs(self.original)
        for path,payload in data.items():
            target=b.ROOT/path
            if target.exists():
                self.assertEqual(target.read_text(encoding="utf-8"),payload,
                                 "committed INT5-B source evidence mismatch "+path)


if __name__=="__main__":
    unittest.main()
