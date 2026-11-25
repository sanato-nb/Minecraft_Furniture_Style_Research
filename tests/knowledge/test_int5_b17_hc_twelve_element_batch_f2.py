"""B17 twelve genuinely distinct HC source elements. Synthetic tests are NOT F2 proof."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw
from mcfr import int5_b17_hc_twelve_element_batch_f2 as batch
from mcfr import int5_b8_hc_cushion_source_preflight as hc


def models():
    elements=[{"from":[0,i,0],"to":[4,i+1,4],
               "faces":{str(n):{"texture":"#wood"} for n in range(6)}}
              for i in range(13)]
    child={"parent":"handcrafted:block/chair/chair",
           "textures":{"wood":"handcrafted:block/chair/warped_chair"}}
    return json.dumps(child).encode(),json.dumps({"elements":elements}).encode()


def image(chair=True,white=False,delete=False):
    im=Image.new("RGB",(1024,684),(180,182,188))
    draw=ImageDraw.Draw(im)
    if chair:
        draw.rectangle((495,398,536,475),fill=(38,125,114))
        if not white and not delete:
            draw.rectangle((505,420,530,440),fill=(10,10,20))
    return im


def sessions(delete=False,wrong_control=False):
    rows={}
    for view in batch.VIEWS:
        rows[view]={"black_before":image(delete=delete),
                    "white":image(white=True),
                    "black_after":image(delete=delete),
                    "air":image(chair=False)}
    if wrong_control:
        ImageDraw.Draw(rows["north"]["white"]).rectangle((500,400,513,417),fill=(240,0,100))
    return rows


class HandcraftedBatch12Tests(unittest.TestCase):
    def tearDown(self):
        batch.select_index(0)

    def test_twelve_distinct_original_and_cushion12_is_not_recounted(self):
        self.assertEqual(batch.INDICES,tuple(range(12)))
        self.assertEqual(len(batch.ROLES),12)
        with self.assertRaisesRegex(ValueError,"already tested"):
            batch.select_index(12)

    def test_each_original_source_is_individually_unverified_role_hypothesis(self):
        for i in batch.INDICES:
            with self.subTest(index=i):
                batch.select_index(i)
                source=batch.source_role_check()
                self.assertEqual(source["original_source_element_index"],str(i))
                self.assertEqual(source["provider_key"],"HC13")
                self.assertEqual(source["original_role_hypothesis"],batch.ROLES[i])
                self.assertEqual(source["part_function_verified"],"false")

    def test_all_twelve_isolated_child_patches_keep_exact_original_order(self):
        child,parent=models()
        original=json.loads(parent)["elements"]
        for i in batch.INDICES:
            with self.subTest(index=i):
                batch.select_index(i)
                data,scope=batch.override_child_only(child,parent)
                revised=json.loads(data)
                self.assertEqual(revised["elements"],[x for n,x in enumerate(original) if n!=i])
                self.assertEqual(sum(len(x["faces"]) for x in revised["elements"]),72)
                self.assertEqual(scope["removed_original_element_index"],i)
                self.assertEqual(scope["other_original_indices_unchanged"],[n for n in range(13) if n!=i])
                self.assertEqual(revised["textures"],json.loads(child)["textures"])

    def test_preexisting_child_elements_not_overwritten(self):
        child,parent=models()
        bad=json.loads(child);bad["elements"]=[]
        with self.assertRaisesRegex(ValueError,"must inherit"):
            batch.override_child_only(json.dumps(bad).encode(),parent)

    def test_wrong_13_element_78_face_parent_fails_closed(self):
        child,parent=models()
        bad=json.loads(parent);bad["elements"][0]["faces"].pop("0")
        with self.assertRaisesRegex(ValueError,"13/78"):
            batch.override_child_only(child,json.dumps(bad).encode())

    def test_explicit_two_original_game_sessions_and_original_cases(self):
        self.assertEqual(batch.pinned_chair_case().case_id,hc.CASE)
        self.assertEqual(batch.state("black_before"),hc.STATE)
        self.assertEqual(batch.state("white"),hc.CTRL_STATE)
        self.assertEqual(batch.STAGES,("black_before","white","black_after","air"))

    def test_synthetic_differential_pixel_change_and_unchanged_white_air(self):
        rows=batch.measure(sessions(),sessions(delete=True))
        for x in rows.values():
            self.assertGreater(x["selected_element_removal_original_vs_modified_black_before_pixels"],0)
            self.assertEqual(x["selected_element_removal_original_vs_modified_black_before_pixels"],
                             x["selected_element_removal_original_vs_modified_black_after_pixels"])
            self.assertEqual(x["white_control_original_vs_modified_pixels"],0)
            self.assertEqual(x["air_control_original_vs_modified_pixels"],0)
            self.assertEqual(x["changed_pixels_outside_original_black_foreground"],0)

    def test_white_child_negative_control_can_fail(self):
        rows=batch.measure(sessions(),sessions(delete=True,wrong_control=True))
        self.assertGreater(rows["north"]["white_control_original_vs_modified_pixels"],0)

    def test_synthetic_zero_pixel_is_not_causal_pass(self):
        rows=batch.measure(sessions(),sessions())
        self.assertTrue(all(v["selected_element_removal_original_vs_modified_black_before_pixels"]==0
                            for v in rows.values()))
        self.assertIn("NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS",
                      Path(batch.__file__).read_text(encoding="utf-8"))

    def test_drop_item_purge_and_server_check_preserved(self):
        code=Path(batch.__file__).read_text(encoding="utf-8")
        self.assertIn("/kill @e[type=minecraft:item]",code)
        self.assertIn("/execute unless entity @e[type=minecraft:item]",code)
        self.assertIn('"dropped_item_entities_zero_at_all_16_F2":True',code)

    def test_no_fake_success_without_16_actual_minecraft_native_F2(self):
        with TemporaryDirectory() as root:
            with self.assertRaises(FileNotFoundError):
                batch.audit(root)

    def test_no_model_semantic_pixel_ownership_or_unauthorized_rights_promotion(self):
        code=Path(batch.__file__).read_text(encoding="utf-8")
        for key in ('"original_element_exclusive_visible_pixel_ownership_approved":False',
                    '"gameplay_seating_or_function_approved":False',
                    '"part_material_or_style_final_approved":False',
                    '"INT6_AI_training_or_redistribution_rights_approved":0'):
            self.assertIn(key,code)

    def test_runtime_HC_world_selection_is_not_shadowed_by_AF_branch(self):
        runtime=(batch.ROOT/"src/mcfr/runtime.py").read_text(encoding="utf-8")
        clauses=[line.strip() for line in runtime.splitlines() if line.strip().startswith("elif args.command in (")]
        self.assertTrue(all("int5-b17-hc-twelve-batch-f2" not in clause for clause in clauses))
        self.assertEqual(runtime.count('elif args.command=="int5-b17-hc-twelve-batch-f2":'),1)

if __name__=="__main__":
    unittest.main()
