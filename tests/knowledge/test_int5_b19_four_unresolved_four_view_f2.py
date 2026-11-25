"""B19 four previously not-visible original source members, four cardinal cameras."""
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from PIL import Image,ImageDraw

from mcfr import int5_b19_four_unresolved_four_view_f2 as b19

def image(stage,missing=False):
    img=Image.new("RGB",(1024,684),(205,208,211))
    paint=ImageDraw.Draw(img)
    if stage in ("model1_before","model1_after","black_before","black_after",
                 "chair_plus_slab_before","chair_plus_slab_after"):
        paint.rectangle((493,385,542,479),fill=(83,115,93))
        if not missing:
            paint.rectangle((505,401,522,433),fill=(230,80,40))
    if stage=="air":pass
    return img

class FourUnresolvedSourceTests(unittest.TestCase):
    def tearDown(self):b19.set_target("AF121_5")

    def test_exact_four_prior_no_visible_original_elements(self):
        self.assertEqual(set(b19.TARGETS),
                         {"AF121_5","AF123_5","HC11210_3","HC11210_4"})
        self.assertEqual(sum(v[3] for v in b19.TARGETS.values()),20)
        for target in b19.TARGETS:
            with self.subTest(target=target):
                b19.set_target(target)
                s=b19.source()
                self.assertTrue(s["B18_prior_state"].endswith("NO_VISIBLE_RESPONSE"))
                self.assertEqual(s["B18_prior_south_pixels"],0)
                self.assertEqual(s["B18_prior_north_pixels"],0)
                self.assertEqual(s["source_element_index"],b19.TARGETS[target][2])
                self.assertEqual(s["source_faces"],b19.TARGETS[target][3])

    def test_unknown_elements_fail_closed(self):
        for val in ("AF121_6","HC11210_5","MACAW67_0","AF123_0"):
            with self.assertRaisesRegex(ValueError,"not one of four"):
                b19.set_target(val)

    def test_three_source_families_use_original_correct_pinned_cases(self):
        positions={"AF121_5":(-88,120,40),"AF123_5":(-24,120,40),
                   "HC11210_3":(40,120,40),"HC11210_4":(40,120,40)}
        for name,pos in positions.items():
            with self.subTest(target=name):
                b19.set_target(name)
                self.assertEqual(b19.coords(),pos)
                self.assertEqual(b19.case().facing,"north")
                self.assertEqual(b19.identity()["source_case"],name.split("_")[0]+"_north")

    def test_four_actual_distinct_camera_poses(self):
        self.assertEqual(b19.VIEWS,("south","north","east","west"))
        for target in b19.TARGETS:
            b19.set_target(target)
            cam=b19.cameras()
            self.assertEqual(set(cam),set(b19.VIEWS))
            self.assertEqual(len(set(cam.values())),4)
            self.assertIn("90 20",cam["east"])
            self.assertIn("-90 20",cam["west"])
            self.assertIn("180 20",cam["south"])
            self.assertIn("0 20",cam["north"])
            self.assertEqual(len(b19.stages()),4)

    def test_af123_tucked_requires_legal_top_slab_at_every_chair_state(self):
        b19.set_target("AF123_5")
        self.assertEqual(b19.support("chair_plus_slab_before"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b19.support("chair_plus_slab_after"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b19.support("slab_only"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b19.block("slab_only"),"minecraft:air")
        self.assertEqual(b19.support("empty"),"minecraft:air")

    def test_af121_negative_is_original_distinct_variant3(self):
        b19.set_target("AF121_5")
        self.assertEqual(b19.stages(),("model1_before","model3","model1_after","air"))
        self.assertNotEqual(b19.block("model1_before"),b19.block("model3"))
        self.assertEqual(b19.block("air"),"minecraft:air")

    def test_hc_white_control_and_item_entity_audit_present(self):
        for name in ("HC11210_3","HC11210_4"):
            b19.set_target(name)
            self.assertEqual(b19.stages(),("black_before","white","black_after","air"))
            self.assertNotEqual(b19.block("black_before"),b19.block("white"))
        code=Path(b19.__file__).read_text(encoding="utf-8")
        self.assertIn("/kill @e[type=minecraft:item]",code)
        self.assertIn("/execute unless entity @e[type=minecraft:item]",code)

    def test_pinned_child_patch_dispatch_uses_prior_proven_implementations(self):
        c=Path(b19.__file__).read_text(encoding="utf-8")
        for phrase in ("af1.prepare_disposable_child(game)",
                       "af10.prepare(game,5)",
                       "hc17.prepare_disposable_child(game,pre)"):
            self.assertIn(phrase,c)
        self.assertIn("copytree(world,snapshot",c)
        self.assertIn("shutil.copytree(snapshot,world",c)

    def test_synthetic_four_view_change_and_zero_controls(self):
        for target in b19.TARGETS:
            b19.set_target(target)
            before,control,after,air=b19.stages()
            baseline={view:{s:image(s) for s in b19.stages()} for view in b19.VIEWS}
            modified={view:{s:image(s,True) if s in (before,after) else image(s)
                            for s in b19.stages()} for view in b19.VIEWS}
            result=b19.compare(baseline,modified)
            self.assertEqual(set(result),set(b19.VIEWS))
            for metrics in result.values():
                self.assertGreater(metrics["new_source_intervention_before_pixels"],0)
                self.assertEqual(metrics["new_source_intervention_before_pixels"],
                                 metrics["new_source_intervention_after_pixels"])
                for key in ("unchanged_negative_control_pixels",
                            "unchanged_air_and_support_pixels",
                            "baseline_A_A_temporal_pixels",
                            "modified_A_A_temporal_pixels",
                            "intervention_outside_original_foreground_pixels"):
                    self.assertEqual(metrics[key],0)

    def test_zero_pixels_are_not_an_automatic_causal_pass(self):
        b19.set_target("HC11210_3")
        values={view:{s:image(s) for s in b19.stages()} for view in b19.VIEWS}
        self.assertTrue(all(m["new_source_intervention_before_pixels"]==0
                            for m in b19.compare(values,values).values()))
        self.assertIn("NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_FOUR_VIEW_CONTROLS",
                      Path(b19.__file__).read_text(encoding="utf-8"))

    def test_no_fake_research_without_actual_minecraft_logs_and_images(self):
        with TemporaryDirectory() as tmp:
            for target in b19.TARGETS:
                b19.set_target(target)
                with self.assertRaises(FileNotFoundError):
                    b19.audit(tmp)

    def test_scope_never_promotes_physical_function_or_rights(self):
        c=Path(b19.__file__).read_text(encoding="utf-8")
        for phrase in ('"exclusive_source_face_GPU_pixel_ownership_approved":False',
                       '"physical_function_material_style_approved":False',
                       '"AI_training_redistribution_rights_approved":False',
                       '"F70_unconditional_approved":0'):
            self.assertIn(phrase,c)

if __name__=="__main__":
    unittest.main()
