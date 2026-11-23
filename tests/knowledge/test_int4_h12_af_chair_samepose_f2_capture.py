"""H12 real AF same-camera native F2 regression, not model or GPU simulation."""
from __future__ import annotations
import json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from mcfr import int4_h12_af_chair_samepose_f2_capture as h12
from mcfr.chair_runtime_fixture import pack_lines,make_pack
from tempfile import TemporaryDirectory

class H12SourceControlledF2(unittest.TestCase):
    def test_version_original_study_and_jar_pins(self):
        self.assertEqual(h12.VERSION,"1.21.1")
        self.assertEqual(h12.JAR_SHA1,"c2f992081bdc4795ed6d87771a3b5f7c71103785")
        self.assertEqual(h12.H11_SHA1,"1869ee05afce779bd37233ba1cc74850d736160f")
    def test_selector_same_north_facing_but_different_model_resources(self):
        self.assertEqual(h12.SELECTIONS["model1"],"facing=north,tucked=false,variant=1")
        self.assertEqual(h12.SELECTIONS["model3"],"facing=north,tucked=false,variant=3")
        self.assertNotEqual(h12.MODELS["model1"],h12.MODELS["model3"])
        with self.assertRaises(ValueError):h12.state("south")
    def test_one_original_AF121_north_fixture(self):
        selected=h12.original_case()
        self.assertEqual(len(selected),1)
        self.assertEqual(selected[0].state(),h12.state("model1"))
        self.assertEqual(selected[0].facing,"north")
        self.assertEqual((selected[0].x,selected[0].y,selected[0].z),(-88,120,40))
    def test_actual_source_pack_places_only_original_chair_variant1(self):
        placed,checks=pack_lines("1.21.1",h12.original_case())
        self.assertEqual(sum(x.startswith("setblock") for x in placed),1)
        self.assertIn("variant=1","\n".join(placed))
        self.assertNotIn("variant=3","\n".join(placed))
        self.assertIn("AF121_north=PASS","\n".join(checks))
    def test_native_real_client_camera_unchanged_across_four_f2(self):
        s=Path(h12.__file__).read_text(encoding="utf-8")
        self.assertIn('server_cmd("/tp @s "+pose',s)
        self.assertEqual(h12.STAGES,("model1_before","model3","model1_after","air"))
        for v in ("model1_before","model3","model1_after","air"):
            self.assertIn('check_state("'+v+'"',s)
        self.assertEqual(s.count('server_cmd("/tp @s "+pose'),1)
    def test_sample_ROI_measurements_reveal_texture_and_foreground_controls(self):
        from PIL import Image
        images={k:Image.new("RGB",(1024,684),(185,200,225)) for k in h12.STAGES}
        for key in ("model1_before","model1_after","model3"):
            ImageDraw.Draw(images[key]).rectangle((470,385,546,490),fill=(70,42,24))
        ImageDraw.Draw(images["model3"]).rectangle((486,420,500,441),fill=(190,30,60))
        comparison=h12.metrics(images)
        self.assertGreater(comparison["model1_to_model3"],25)
        self.assertGreater(comparison["model1_to_air"],250)
        self.assertEqual(comparison["model1_before_to_model1_after_temporal_control"],0)
        self.assertEqual(comparison["model_difference_outside_foreground"],0)
    def test_no_gameplay_or_semantic_or_GPU_approval(self):
        s=Path(h12.__file__).read_text(encoding="utf-8")
        self.assertIn('"face_pixel_UV_causality_approved":False',s)
        self.assertIn('"F70_unconditional_approvals":0',s)
        self.assertIn('"INT6_training_rights_approved":0',s)
        self.assertIn('"player_sleep_wake_destroy_tests_run":False',s)
    def test_unchanged_H11_source_original_does_not_assert_F70_completion(self):
        data=json.loads(h12.H11.read_text(encoding="utf-8"))
        self.assertEqual(data["counts"]["changed_binding_faces_with_any_different_texel"],2)
        self.assertEqual(data["counts"]["changed_texels_in_union_of_12_face_UV_footprints"],54)
        self.assertEqual(data["counts"]["F70_unconditional_approvals"],0)
        self.assertEqual(h12.blob(h12.H11.read_bytes()),h12.H11_SHA1)

if __name__=="__main__":unittest.main()
