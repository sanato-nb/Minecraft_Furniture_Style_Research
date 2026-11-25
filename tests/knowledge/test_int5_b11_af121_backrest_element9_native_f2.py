"""B11: original source parent isolation and synthetic negative tests; no fake F2."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageDraw

from mcfr import int5_b11_af121_backrest_element9_native_f2 as b11
from mcfr import int4_h15_af_opposing_f2_capture as h15


def original_synthetic_models():
    def elem(i):
        n=6 if i==4 else (5 if i in (0,1,2,3,8,9)
                           else 2 if i==7 else 4)
        return {"from":[0,i,0],"to":[2,i+1,2],
                "faces":{str(j):{"texture":"#bottom"} for j in range(n)}}
    parent={"elements":[elem(i) for i in range(10)],
            "ambientocclusion":True}
    child1={"parent":"another_furniture:block/template/chair",
            "textures":{"bottom":"another_furniture:block/chair/bottom/acacia",
                        "seat":"another_furniture:block/chair/seat/acacia"}}
    child3={"parent":"another_furniture:block/template/chair",
            "textures":{"bottom":"another_furniture:block/chair/bottom/acacia",
                        "back":"another_furniture:block/chair/back_3/acacia"}}
    return tuple(json.dumps(x).encode("utf-8") for x in (child1,child3,parent))


def frame(has_chair=True,has_backrest=True,alternative=False):
    image=Image.new("RGB",(1024,684),(205,205,205))
    draw=ImageDraw.Draw(image)
    if has_chair:
        draw.rectangle((495,400,535,468),fill=(127,80,40) if not alternative
                       else (110,61,30))
        if has_backrest:
            draw.rectangle((500,425,530,440),fill=(230,141,67))
    return image


def scenes(remove=False,change_control=False):
    result={}
    for view in b11.VIEWS:
        result[view]={
            "model1_before":frame(has_backrest=not remove),
            "model3":frame(alternative=True),
            "model1_after":frame(has_backrest=not remove),
            "air":frame(False),
        }
    if change_control:
        ImageDraw.Draw(result["north"]["model3"]).rectangle(
            (503,410,517,422),fill=(0,0,0))
    return result


class B11IndependentSourceEvidenceTests(unittest.TestCase):

    def test_original_B6_source_AF121_element9_is_unverified_backrest_hypothesis(self):
        source=b11.original_role()
        self.assertEqual(source["provider_key"],"AF1393")
        self.assertEqual(source["source_element_original_face_count"],"5")
        self.assertEqual(source["causal_screen_response_status"],
                         "NOT_INDIVIDUALLY_CAUSAL_TESTED")
        self.assertEqual(source["source_texture_role_cue"],
                         "ROLE_NAMED_ORIGINAL_BACK_PNG")

    def test_exact_original_element9_identity_not_prior_B10_element8(self):
        self.assertEqual(b11.SOURCE_INDEX,9)
        self.assertEqual(b11.SOURCE_KEY,("AF121","AF1393",9))
        source=Path(b11.__file__).read_text(encoding="utf-8")
        self.assertIn('"original_source_part_key":"/".join(',source)
        self.assertNotIn('"original_source_part_key":"AF121/AF1393/8"',source)

    def test_original_template_10_elements_46_faces_and_single_child_only_override(self):
        child,control,parent=original_synthetic_models()
        patch,scope=b11.isolated_child_override(child,control,parent)
        obj=json.loads(patch)
        self.assertEqual(len(obj["elements"]),9)
        self.assertEqual(sum(len(x["faces"]) for x in obj["elements"]),41)
        self.assertEqual(scope["nonremoved_original_element_indices"],
                         [0,1,2,3,4,5,6,7,8])
        self.assertEqual(obj["textures"],json.loads(child)["textures"])
        self.assertEqual(scope["original_child_parent"],
                         "another_furniture:block/template/chair")

    def test_child_with_existing_elements_cannot_be_silently_rewritten(self):
        child,control,parent=original_synthetic_models()
        doc=json.loads(child);doc["elements"]=[]
        with self.assertRaisesRegex(ValueError,"both inherit"):
            b11.isolated_child_override(json.dumps(doc).encode(),control,parent)

    def test_control_child_wrong_parent_is_detected(self):
        child,control,parent=original_synthetic_models()
        doc=json.loads(control);doc["parent"]="minecraft:block/cube_all"
        with self.assertRaisesRegex(ValueError,"both inherit"):
            b11.isolated_child_override(child,json.dumps(doc).encode(),parent)

    def test_unexpected_source_geometry_or_index7_face_count_is_rejected(self):
        child,control,parent=original_synthetic_models()
        doc=json.loads(parent);doc["elements"][9]["faces"].pop("0")
        with self.assertRaisesRegex(ValueError,"46-face template"):
            b11.isolated_child_override(child,control,json.dumps(doc).encode())

    def test_two_camera_original_H15_case_is_unchanged(self):
        self.assertEqual(b11.CAMERAS,h15.EXPECTED_CAMERAS)
        self.assertEqual(b11.BLOCK_XYZ,(-88,120,40))
        self.assertEqual(b11.STAGES,("model1_before","model3","model1_after","air"))
        self.assertEqual(b11.h12.state("model1"),
                         "another_furniture:acacia_chair[facing=north,tucked=false,variant=1]")
        self.assertEqual(b11.h12.state("model3"),
                         "another_furniture:acacia_chair[facing=north,tucked=false,variant=3]")

    def test_synthetic_single_child_removal_changes_only_model1_foreground(self):
        metrics=b11.compare_frames(scenes(),scenes(remove=True))
        for view,m in metrics.items():
            self.assertGreater(
                m["removed_element9_original_vs_patched_model1_before_pixels"],0)
            self.assertEqual(
                m["removed_element9_original_vs_patched_model1_before_pixels"],
                m["removed_element9_original_vs_patched_model1_after_pixels"])
            for key in ("original_model3_untouched_child_negative_pixels",
                        "original_AIR_untouched_world_negative_pixels",
                        "original_model1_A_A_temporal_pixels",
                        "patched_model1_A_A_temporal_pixels",
                        "patched_model1_changed_pixels_outside_original_foreground"):
                self.assertEqual(m[key],0)

    def test_control_variant3_mutation_rejected_by_negative_metric(self):
        m=b11.compare_frames(scenes(),scenes(remove=True,change_control=True))
        self.assertGreater(m["north"]["original_model3_untouched_child_negative_pixels"],0)
        self.assertEqual(m["south"]["original_model3_untouched_child_negative_pixels"],0)

    def test_no_real_F2_no_pass(self):
        with TemporaryDirectory() as root:
            with self.assertRaises((FileNotFoundError,ValueError,KeyError)):
                b11.audit(Path(root),Path(root)/"missing.zip")

    def test_no_unauthorized_final_semantic_or_source_rights_promotion(self):
        code=Path(b11.__file__).read_text(encoding="utf-8")
        self.assertIn('"unique_original_element_pixel_ownership_approved":False',code)
        self.assertIn('"part_seating_or_function_approved":False',code)
        self.assertIn('"part_material_or_style_approved":False',code)
        self.assertIn('"INT6_AI_training_or_redistribution_rights_approved":0',code)

if __name__=="__main__":
    unittest.main()
