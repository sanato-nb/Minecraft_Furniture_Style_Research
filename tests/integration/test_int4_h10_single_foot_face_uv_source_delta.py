"""H10 original Handcrafted single-bed foot face UV delta, not game semantics."""
from __future__ import annotations
import importlib.util,unittest,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"scripts/integration/build_int4_h10_single_foot_face_uv_source_delta.py"
spec=importlib.util.spec_from_file_location("h10_study_face_uv_delta",SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class H10SingleFootSourceOnly(unittest.TestCase):
    def test_original_h9_source_sha_is_immutable(self):
        d=mod.original_h9()
        self.assertEqual(d["counts"]["foot_parent_geometry_changed_pairs"],256)
        self.assertEqual(d["counts"]["head_model_leaf_byte_identical_pairs"],256)
        self.assertEqual(d["counts"]["new_occupied_true_native_F2"],0)
    def test_original_single_parent_source_paths(self):
        self.assertTrue(mod.F0.endswith("fancy_bed/bed_single.json"))
        self.assertTrue(mod.F1.endswith("fancy_bed/bed_single_occupied.json"))
    def test_minimal_one_removed_three_added_element_multiset(self):
        old={"elements":[
          {"from":[0,0,0],"to":[1,1,1],"faces":{}},
          {"from":[1,0,0],"to":[2,1,1],"faces":{}}]}
        new={"elements":[old["elements"][0],
           {"from":[2,0,0],"to":[3,1,1],"faces":{}},
           {"from":[3,0,0],"to":[4,1,1],"faces":{}},
           {"from":[4,0,0],"to":[5,1,1],"faces":{}}]}
        with self.assertRaises(AssertionError):mod.compare_elements(old,new)
    def test_correct_single_source_deltas_count(self):
        old={"elements":[{"tag":str(i)} for i in range(12)]}
        new={"elements":[*old["elements"][:11],*[{"tag":"new"+str(i)} for i in range(3)]]}
        diff=mod.compare_elements(old,new)
        self.assertEqual([x[0] for x in diff],["removed","added","added","added"])
        self.assertEqual(diff[0][1]["tag"],"11")
    def test_source_coordinates_dont_claim_pixel_uv(self):
        s=SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"renderer_pixel_to_face_association":"NOT_VERIFIED"',s)
        self.assertIn('"full_face_to_GPU_pixel_mapping_approved":False',s)
        self.assertIn('"sleep_wake_destroy_gameplay_tested":False',s)
        self.assertIn('"INT6_training_or_redistribution_approved":0',s)
    def test_output_csv_name_unique(self):
        self.assertNotEqual(mod.ELEMENTS,mod.FACES)
        self.assertTrue(mod.REPORT.endswith(".json"))
if __name__=="__main__":unittest.main()
