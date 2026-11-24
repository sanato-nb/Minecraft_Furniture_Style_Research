"""Fail-closed regression controls for immutable INT-4 original D/F contracts."""
import copy
import json
import unittest
from mcfr import int4_original_df_gate_reaudit as d


class OriginalDFGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = d.read_pinned()
        cls.source, cls.proof = d.fetch_upstream()

    def test_actual_D_F_source_reassessment(self):
        result = d.adjudicate(self.original, self.source, self.proof)
        self.assertEqual(result["D"]["original_blockstates_examined"], 1158)
        self.assertEqual(result["D"]["original_selector_options_examined"], 78456)
        self.assertEqual(len(result["D"]["six_exception_rows_actual_source_verified"]), 6)
        self.assertEqual(result["D"]["strict_original_scope_HOLD"], 1)
        self.assertFalse(result["D"]["full_D_unconditional_approved"])
        self.assertEqual(result["F"]["original_F2_image_links"], 70)
        self.assertEqual(result["F"]["original_strict_F_conditional"], 70)
        self.assertFalse(result["F"]["full_F_unconditional_approved"])
        self.assertEqual(result["F"]["modeling_only_contract_from_H23"], "70/70")
        self.assertEqual(result["original_H_gates"], {"H03": "HOLD", "H05": "CONDITIONAL"})

    def test_original_AF_three_git_JSONs_and_java_pinned(self):
        self.assertEqual(set(self.proof["pinned_blobs"]), set(d.AF_FILES))
        self.assertFalse(self.proof["entire_registry_runtime_reachability_proven"])
        self.assertTrue(self.proof["missing_model_confirmed_in_this_git_tree"])
        self.assertFalse(self.proof["AFBlocks_java_named_awning_reference"])

    def test_D_one_modified_source_state_fails(self):
        bad = dict(self.original)
        needle = b"another_furniture:birch_chair"
        assert needle in bad["INT4_D_1158_STATE_DISPOSITIONS_V1.csv"]
        bad["INT4_D_1158_STATE_DISPOSITIONS_V1.csv"] = bad[
            "INT4_D_1158_STATE_DISPOSITIONS_V1.csv"].replace(needle, b"fake:birch_chair", 1)
        with self.assertRaisesRegex(ValueError, "D and G5 state keys differ"):
            d.adjudicate(bad, self.source, self.proof)

    def test_F_missing_visual_sha_fails(self):
        bad = dict(self.original)
        data = bad["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"]
        original = d.csv_rows(data)
        original[0]["image_sha256s"] = ""
        import csv, io
        f = io.StringIO()
        writer = csv.DictWriter(f, fieldnames=list(original[0]))
        writer.writeheader()
        writer.writerows(original)
        bad["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"] = f.getvalue().encode()
        with self.assertRaisesRegex(ValueError, "lack native image"):
            d.adjudicate(bad, self.source, self.proof)

    def test_illicit_full_F_approval_rejected(self):
        bad = dict(self.original)
        txt = bad["INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"]
        assert b",false,false,false" in txt
        bad["INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"] = txt.replace(
            b",false,false,false", b",false,false,true", 1)
        with self.assertRaisesRegex(ValueError, "full F final status"):
            d.adjudicate(bad, self.source, self.proof)

    def test_bogus_AF_source_variant_rejected(self):
        bad = dict(self.source)
        txt = bad["blockstates/birch_chair.json"]
        old = '"model": "another_furniture:block/chair/birch_1"'
        self.assertIn(old, txt)
        # Change only exactly selected south variant3, preserving baseline.
        obj = json.loads(txt)
        obj["variants"]["facing=south,tucked=false,variant=3"]["model"] = "another_furniture:block/chair/birch_3"
        bad["blockstates/birch_chair.json"] = json.dumps(obj)
        with self.assertRaisesRegex(ValueError, "source variant3->1 mismatch"):
            d.adjudicate(self.original, bad, self.proof)

    def test_whole_registry_absence_not_inferred_from_one_class(self):
        result = d.adjudicate(self.original, self.source, self.proof)
        self.assertTrue(all(not x["full_registered_runtime_state_approved"] for x in
                            result["D"]["six_exception_rows_actual_source_verified"]))
        self.assertTrue(all(not x["full_F_unconditional_approved"] for x in
                            result["F"]["original_per_case_classifications"]))
        self.assertFalse(result["cross_gate_not_approved"]["INT4_H_full_exit"])


if __name__ == "__main__":
    unittest.main()
