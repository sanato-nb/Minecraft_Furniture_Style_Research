"""B15 independent unit/negative tests; synthetic PNG != genuine game evidence."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image, ImageDraw
from mcfr import int5_b15_af123_six_element_batch_f2 as batch
from mcfr import int5_af_tucked_slab_control as b4

def element(i):
    faces={0:5,1:5,2:5,3:5,4:6,5:4,6:4,7:2,8:5,9:5}[i]
    return {"from":[0,i,0],"to":[4,i+1,4],
            "faces":{str(n):{"texture":"#src"} for n in range(faces)}}

def frames(hide=False,slab_change=False):
    result={}
    for view in b4.VIEWS:
        v={}
        for stage in b4.STAGES:
            im=Image.new("RGB",(1024,684),(220,220,220))
            draw=ImageDraw.Draw(im)
            if stage!="empty":
                draw.rectangle((490,400,520,420),fill=(110,110,110))
                if slab_change and stage=="slab_only":
                    draw.rectangle((500,400,510,410),fill=(0,0,0))
            if stage.startswith("chair_plus"):
                draw.rectangle((490,421,540,470),fill=(140,80,30))
                if not hide:
                    draw.rectangle((497,427,505,443),fill=(250,120,20))
            v[stage]=im
        result[view]=v
    return result

class SixElementBatchTests(unittest.TestCase):
    def test_exact_six_new_elements_and_B3_source_identification(self):
        self.assertEqual(batch.INDICES,(0,1,2,3,5,6))
        self.assertEqual(sum(batch.FACES.values()),28)
        for i in batch.INDICES:
            role=batch.source_role(i)
            self.assertEqual(role["original_source_element_index"],str(i))
            self.assertEqual(role["source_element_original_face_count"],str(batch.FACES[i]))
            self.assertEqual(role["individual_element_to_original_F2_pixels_approved"],"false")

    def test_already_done_indices_not_scheduled_again(self):
        for i in (-1,4,7,8,9,10):
            with self.subTest(index=i),self.assertRaisesRegex(ValueError,"not a selected"):
                batch.source_role(i)

    def test_each_removed_element_is_the_only_geometry_change(self):
        provider={"elements":[element(i) for i in range(10)]}
        source={"parent":"another_furniture:block/template/chair_tucked",
                "textures":{"bottom":"another_furniture:block/chair/bottom/acacia"}}
        for i in batch.INDICES:
            with self.subTest(i=i):
                altered,removed=batch.override_child(json.dumps(source).encode(),provider,i)
                child=json.loads(altered)
                self.assertEqual(child["elements"],[element(j) for j in range(10) if j!=i])
                self.assertEqual(len(child["elements"]),9)
                self.assertEqual(sum(len(x["faces"]) for x in child["elements"]),46-batch.FACES[i])
                self.assertEqual(removed,element(i))
                self.assertEqual(child["textures"],source["textures"])
                self.assertEqual(len(provider["elements"]),10)

    def test_parent_or_existing_child_elements_fail_closed(self):
        parent={"elements":[element(i) for i in range(10)]}
        wrong={"parent":"minecraft:block/cube_all"}
        with self.assertRaisesRegex(ValueError,"child must inherit"):
            batch.override_child(json.dumps(wrong).encode(),parent,0)
        wrong["parent"]="another_furniture:block/template/chair_tucked"
        wrong["elements"]=[]
        with self.assertRaisesRegex(ValueError,"child must inherit"):
            batch.override_child(json.dumps(wrong).encode(),parent,0)

    def test_wrong_face_count_or_unexpected_missing_geometry_fails(self):
        parent={"elements":[element(i) for i in range(10)]}
        child={"parent":"another_furniture:block/template/chair_tucked"}
        parent["elements"][5]["faces"].pop("0")
        with self.assertRaisesRegex(ValueError,"10/46"):
            batch.override_child(json.dumps(child).encode(),parent,5)

    def test_legal_top_slab_and_version_are_original(self):
        self.assertEqual(b4.target_case().state(),
          "another_furniture:acacia_chair[facing=north,tucked=true,variant=10]")
        self.assertEqual(b4.stage_slab_state("chair_plus_slab_before"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(batch.MODEL,b4.MODEL)

    def test_synthetic_pixel_response_only_for_chair_and_repeated_A(self):
        v=batch.metrics(frames(),frames(hide=True))
        for row in v.values():
            self.assertGreater(row["element9_removal_source_intervention_delta_pixels"],0)
            self.assertEqual(row["element9_removal_source_intervention_delta_pixels"],
                             row["element9_removal_repeated_delta_pixels"])
            self.assertEqual(row["unchanged_slab_only_negative_control_pixels"],0)
            self.assertEqual(row["unchanged_air_negative_control_pixels"],0)
            self.assertEqual(row["modified_session_temporal_delta_pixels"],0)
            self.assertEqual(row["intervention_pixels_outside_original_visible_chair_foreground"],0)

    def test_synthetic_bad_slab_control_is_detected(self):
        v=batch.metrics(frames(),frames(hide=True,slab_change=True))
        self.assertGreater(v["south"]["unchanged_slab_only_negative_control_pixels"],0)

    def test_synthetic_no_visible_response_is_not_a_pass(self):
        v=batch.metrics(frames(),frames())
        self.assertEqual(v["north"]["element9_removal_source_intervention_delta_pixels"],0)

    def test_missing_actual_original_game_images_fail_closed(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises((FileNotFoundError,ValueError,KeyError)):
                batch.audit(Path(tmp),Path(tmp),0)

    def test_contract_no_semantic_training_or_pixel_ownership_promotion(self):
        source=Path(batch.__file__).read_text(encoding="utf-8")
        self.assertIn('"unique_original_face_UV_to_GPU_pixel_approval":False',source)
        self.assertIn('"part_function_material_style_approval":False',source)
        self.assertIn('"AI_training_or_redistribution_rights_approval":False',source)
        self.assertIn('NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS',source)

if __name__=="__main__":
    unittest.main()
