"""B18 original Macaw 12 source-element isolation and synthetic-only controls."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image,ImageDraw

from mcfr import int5_b18_macaw_twelve_element_batch_f2 as b18

def models():
    elements=[]
    for i,faces in enumerate(b18.FACES):
        elements.append({"from":[0,i,0],"to":[4,i+1,4],
                         "faces":{str(f):{"texture":"#original"} for f in range(faces)}})
    child={"parent":"mcwfurnitures:block/parent/chair",
           "textures":{"original":"minecraft:block/acacia_log"}}
    return json.dumps(child).encode(),json.dumps({"elements":elements}).encode(),elements

def picture(block="chair",absent=False):
    im=Image.new("RGB",(1024,684),(210,211,212))
    d=ImageDraw.Draw(im)
    if block=="chair":
        d.rectangle((498,400,536,470),fill=(100,90,70))
        if not absent:
            d.rectangle((505,419,517,440),fill=(240,105,20))
    elif block=="control":
        d.rectangle((500,410,530,438),fill=(160,115,50))
    return im

def frames(absent=False,control_drift=False):
    out={}
    for view in b18.VIEWS:
        out[view]={
            "chair_before":picture(absent=absent),
            "control":picture("control"),
            "chair_after":picture(absent=absent),
            "air":picture("air"),
        }
    if control_drift:
        ImageDraw.Draw(out["north"]["control"]).rectangle((505,420,510,430),fill=(0,0,0))
    return out

class Macaw12BatchTests(unittest.TestCase):
    def tearDown(self):
        b18.set_index(0)

    def test_original_twelve_independent_source_ids_and_faces(self):
        self.assertEqual(b18.INDICES,tuple(range(12)))
        self.assertEqual(b18.FACES,(5,4,5,5,5,5,5,5,5,4,5,6))
        self.assertEqual(sum(b18.FACES),59)
        for index in b18.INDICES:
            b18.set_index(index)
            row=b18.source_role_check()
            self.assertEqual(row["original_role_hypothesis"],b18.ROLES[index])
            self.assertEqual(row["individual_element_to_original_F2_pixels_approved"],"false")

    def test_out_of_range_indices_cannot_be_promoted(self):
        for i in (-1,12,13):
            with self.assertRaisesRegex(ValueError,"not in 12"):
                b18.set_index(i)

    def test_real_1_21_11_original_chair_state_and_opposing_cameras(self):
        self.assertEqual(b18.case().state(),"mcwfurnitures:acacia_chair[facing=north]")
        self.assertEqual(b18.coords(),(-24,120,40))
        self.assertEqual(b18.cameras()["south"],"-23.5 122.3 45.5 180 20")
        self.assertEqual(b18.cameras()["north"],"-23.5 122.3 34.5 0 20")
        self.assertEqual(b18.state("control"),"minecraft:oak_stairs[facing=north]")
        self.assertEqual(b18.state("air"),"minecraft:air")

    def test_child_exactly_one_removed_at_each_index_parent_unchanged(self):
        child,parent,elements=models()
        for index in b18.INDICES:
            with self.subTest(index=index):
                replacement,meta=b18.override_child(child,parent,index)
                doc=json.loads(replacement)
                self.assertEqual(doc["elements"],[el for j,el in enumerate(elements) if j!=index])
                self.assertEqual(meta["removed_source_index"],index)
                self.assertEqual(meta["source_face_count"],b18.FACES[index])
                self.assertEqual(meta["remaining_source_indices"],[j for j in range(12) if j!=index])
                self.assertEqual(meta["disposable_child_faces"],59-b18.FACES[index])
                self.assertEqual(doc["textures"],json.loads(child)["textures"])

    def test_invalid_child_existing_elements_rejected(self):
        child,parent,_=models()
        doc=json.loads(child);doc["elements"]=[]
        with self.assertRaisesRegex(ValueError,"must inherit"):
            b18.override_child(json.dumps(doc).encode(),parent,0)

    def test_original_provider_face_count_mutation_rejected(self):
        child,parent,_=models()
        doc=json.loads(parent);doc["elements"][0]["faces"].pop("0")
        with self.assertRaisesRegex(ValueError,"12/59"):
            b18.override_child(child,json.dumps(doc).encode(),0)

    def test_wrong_selected_face_count_rejected(self):
        child,parent,_=models()
        doc=json.loads(parent)
        # Keep 59 total, but swap a face from element0 to element1.
        doc["elements"][0]["faces"].pop("0")
        doc["elements"][1]["faces"]["new"]={"texture":"#original"}
        with self.assertRaisesRegex(ValueError,"12/59"):
            b18.override_child(child,json.dumps(doc).encode(),0)

    def test_synthetic_pixels_respond_in_both_A_sessions_only(self):
        result=b18.measure(frames(),frames(absent=True))
        for row in result.values():
            self.assertGreater(row["selected_source_element_removed_before_pixels"],0)
            self.assertEqual(row["selected_source_element_removed_before_pixels"],
                             row["selected_source_element_removed_after_pixels"])
            self.assertEqual(row["unchanged_vanilla_control_pixels"],0)
            self.assertEqual(row["air_negative_control_pixels"],0)
            self.assertEqual(row["original_session_temporal_pixels"],0)
            self.assertEqual(row["modified_session_temporal_pixels"],0)
            self.assertEqual(row["changed_pixels_outside_original_chair_foreground"],0)

    def test_synthetic_wrong_vanilla_control_detected(self):
        result=b18.measure(frames(),frames(absent=True,control_drift=True))
        self.assertGreater(result["north"]["unchanged_vanilla_control_pixels"],0)

    def test_no_render_change_is_not_an_incausal_pass(self):
        result=b18.measure(frames(),frames())
        self.assertTrue(all(x["selected_source_element_removed_before_pixels"]==0 for x in result.values()))
        self.assertIn("NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS",
                      Path(b18.__file__).read_text(encoding="utf-8"))

    def test_unknown_real_F2_cannot_be_faked_into_success(self):
        with TemporaryDirectory() as root:
            with self.assertRaises(FileNotFoundError):
                b18.audit(root)

    def test_no_licenses_or_materials_are_promoted(self):
        src=Path(b18.__file__).read_text(encoding="utf-8")
        for phrase in ('"exclusive_GPU_source_face_pixel_ownership_approved":False',
                       '"part_function_material_style_semantics_approved":False',
                       '"INT6_AI_training_and_redistribution_rights_approved":False',
                       'all_other_original_zip_members_byte_identical'):
            self.assertIn(phrase,src)

if __name__=="__main__":
    unittest.main()
