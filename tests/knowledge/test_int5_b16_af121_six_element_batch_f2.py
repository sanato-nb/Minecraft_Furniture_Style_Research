"""B16: six unique original AF121 elements, fail-closed and synthetic controls.
These unit tests are NOT evidence that actual Minecraft F2 images were captured.
"""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from mcfr import int5_b16_af121_six_element_batch_f2 as b16
from mcfr import int4_h15_af_opposing_f2_capture as h15


def originals():
    faces={0:5,1:5,2:5,3:5,4:6,5:4,6:4,7:2,8:5,9:5}
    elements=[{"from":[0,i,0],"to":[4,i+1,4],
               "faces":{str(n):{"texture":"#src"} for n in range(faces[i])}}
              for i in range(10)]
    parent={"elements":elements}
    child={"parent":"another_furniture:block/template/chair",
           "textures":{"src":"another_furniture:block/chair/bottom/acacia"}}
    control={"parent":"another_furniture:block/template/chair",
             "textures":{"src":"another_furniture:block/chair/back_3/acacia"}}
    return tuple(json.dumps(v).encode() for v in (child,control,parent))


def frame(chair=True,control=False,omit=False):
    im=Image.new("RGB",(1024,684),(202,202,202))
    draw=ImageDraw.Draw(im)
    if chair:
        draw.rectangle((485,405,536,471),fill=(123,80,50) if not control else (100,60,30))
        if not control and not omit:
            draw.rectangle((493,411,503,439),fill=(240,140,20))
    return im


def samples(omit=False,wrong_control=False):
    data={}
    for view in h15.VIEWS:
        data[view]={
            "model1_before":frame(omit=omit),
            "model3":frame(control=True),
            "model1_after":frame(omit=omit),
            "air":frame(chair=False),
        }
    if wrong_control:
        ImageDraw.Draw(data["south"]["model3"]).rectangle((495,410,505,430),fill=(0,0,0))
    return data


class AF121SixSourceElementTests(unittest.TestCase):
    def tearDown(self):
        b16.select_index(0)

    def test_selected_original_six_ids_and_28_source_faces(self):
        self.assertEqual(tuple(b16.FACES),(0,1,2,3,5,6))
        self.assertEqual(sum(b16.FACES.values()),28)
        for idx in b16.FACES:
            b16.select_index(idx)
            self.assertEqual(b16.SOURCE_KEY,("AF121","AF1393",idx))
            self.assertEqual(b16.SOURCE_INDEX,idx)

    def test_existing_4_7_8_9_are_excluded_and_disallowed(self):
        for idx in (-1,4,7,8,9,10):
            with self.subTest(index=idx),self.assertRaisesRegex(ValueError,"not a selected"):
                b16.select_index(idx)

    def test_six_b3_original_face_and_role_candidates_not_approved(self):
        for idx in b16.FACES:
            with self.subTest(index=idx):
                b16.select_index(idx)
                row=b16.original_role()
                self.assertEqual(row["original_role_hypothesis"],b16.ROLES[idx])
                self.assertEqual(int(row["source_element_original_face_count"]),b16.FACES[idx])
                self.assertEqual(row["part_function_verified"],"false")

    def test_each_child_override_excludes_only_selected_original_source_element(self):
        child,control,parent=originals()
        parent_elements=json.loads(parent)["elements"]
        for idx in b16.FACES:
            with self.subTest(index=idx):
                b16.select_index(idx)
                raw,scope=b16.isolated_child_override(child,control,parent)
                changed=json.loads(raw)
                self.assertEqual(changed["elements"],[x for i,x in enumerate(parent_elements) if i!=idx])
                self.assertEqual(len(changed["elements"]),9)
                self.assertEqual(sum(len(x["faces"]) for x in changed["elements"]),46-b16.FACES[idx])
                self.assertEqual(scope["removed_source_index"],idx)
                self.assertEqual(scope["child_new_face_count"],46-b16.FACES[idx])
                self.assertEqual(changed["textures"],json.loads(child)["textures"])

    def test_child_already_has_elements_is_not_eligible(self):
        child,control,parent=originals()
        document=json.loads(child);document["elements"]=[]
        with self.assertRaisesRegex(ValueError,"both inherit"):
            b16.isolated_child_override(json.dumps(document).encode(),control,parent)

    def test_control_sibling_modified_or_missing_parent_is_rejected(self):
        child,control,parent=originals()
        document=json.loads(control);document["parent"]="minecraft:block/cube_all"
        with self.assertRaisesRegex(ValueError,"both inherit"):
            b16.isolated_child_override(child,json.dumps(document).encode(),parent)

    def test_source_face_count_mutation_is_rejected(self):
        child,control,parent=originals()
        document=json.loads(parent);document["elements"][5]["faces"].pop("0")
        b16.select_index(5)
        with self.assertRaisesRegex(ValueError,"46-face template"):
            b16.isolated_child_override(child,control,json.dumps(document).encode())

    def test_h15_original_cameras_state_and_unmodified_model3(self):
        self.assertEqual(b16.CAMERAS,h15.EXPECTED_CAMERAS)
        self.assertEqual(b16.BLOCK_XYZ,(-88,120,40))
        self.assertEqual(b16.STAGES,("model1_before","model3","model1_after","air"))
        self.assertEqual(b16.h12.state("model1"),
          "another_furniture:acacia_chair[facing=north,tucked=false,variant=1]")
        self.assertEqual(b16.h12.state("model3"),
          "another_furniture:acacia_chair[facing=north,tucked=false,variant=3]")

    def test_synthetic_screen_response_is_bounded_and_repeated(self):
        for metrics in b16.compare_frames(samples(),samples(omit=True)).values():
            self.assertGreater(metrics["removed_selected_element_original_vs_patched_model1_before_pixels"],0)
            self.assertEqual(metrics["removed_selected_element_original_vs_patched_model1_before_pixels"],
                             metrics["removed_selected_element_original_vs_patched_model1_after_pixels"])
            for key in ("original_model3_untouched_child_negative_pixels",
                        "original_AIR_untouched_world_negative_pixels",
                        "original_model1_A_A_temporal_pixels",
                        "patched_model1_A_A_temporal_pixels",
                        "patched_model1_changed_pixels_outside_original_foreground"):
                self.assertEqual(metrics[key],0)

    def test_bad_variant3_control_does_not_hide(self):
        metrics=b16.compare_frames(samples(),samples(omit=True,wrong_control=True))
        self.assertGreater(metrics["south"]["original_model3_untouched_child_negative_pixels"],0)

    def test_zero_pixel_change_has_no_positive_screen_response(self):
        data=b16.compare_frames(samples(),samples())
        for v in data.values():
            self.assertEqual(v["removed_selected_element_original_vs_patched_model1_before_pixels"],0)
        code=Path(b16.__file__).read_text(encoding="utf-8")
        self.assertIn("NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS",code)

    def test_no_original_F2_zip_rejects_fake_pass(self):
        with TemporaryDirectory() as tmp:
            b16.select_index(0)
            with self.assertRaises((FileNotFoundError,ValueError,KeyError)):
                b16.audit(Path(tmp),Path(tmp)/"not-a-real-H15.zip")

    def test_no_pixel_ownership_semantic_training_license_promotion(self):
        code=Path(b16.__file__).read_text(encoding="utf-8")
        for expected in ('"unique_original_element_pixel_ownership_approved":False',
                         '"part_seating_or_function_approved":False',
                         '"part_material_or_style_approved":False',
                         '"INT6_AI_training_or_redistribution_rights_approved":0'):
            self.assertIn(expected,code)

if __name__=="__main__":
    unittest.main()
