"""H11 original AF face-UV / original PNG texel intersection unit tests.

Synthetic UV tests are NOT real Minecraft render evidence.
"""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"scripts/integration/build_int4_h11_af_variant3_uv_texel_source.py"
spec=importlib.util.spec_from_file_location("int4_h11_af",FILE)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class AFSourceTexelUVCoverage(unittest.TestCase):
    def test_historical_sources_reopened_with_exact_sha(self):
        prior,risk=h.old_evidence()
        self.assertEqual(prior["model_face_comparison"]["changed_texture_binding_faces"],12)
        self.assertEqual(prior["texture_png_runtime"]["rgba_different_pixel_count"],54)
        self.assertEqual(risk["R07"]["source_substage_count"],4)
        self.assertEqual(risk["R07"]["actual_original_game_run_count"],1)

    def test_model_direct_texture_slots_and_upstream_pins(self):
        self.assertEqual(h.src.EXPECTED_SHA["models/block/template/chair.json"],
                         "d9b64a818021f1a64b0cba13d16d18d6fea65d01")
        self.assertEqual(h.src.EXPECTED_SHA["textures/block/chair/back_1/acacia.png"],
                         "55f3bbf986c0c10b731cc0e67038402f30340972")
        self.assertEqual(h.src.EXPECTED_SHA["textures/block/chair/back_3/acacia.png"],
                         "e2282f2620fc8fbbcfd3bb69ab2a435e5421bbe8")

    def test_reversed_uv_rectangle_yields_same_footprint(self):
        self.assertEqual(h.footprint([2,3,5,7],(16,16)),
                         h.footprint([5,7,2,3],(16,16)))
        self.assertEqual(len(h.footprint([2,3,5,7],(16,16))),12)

    def test_zero_area_and_outside_texture_fail_closed(self):
        for uv in ([3,1,3,5],[-1,0,2,3],[0,0,17,6],[5,2,8,2],[1,2,3]):
            with self.assertRaises(AssertionError):h.footprint(uv,(16,16))

    def test_fractional_positive_area_includes_two_horizontal_texels(self):
        self.assertEqual(h.footprint([2.25,1,3.25,2],(16,16)),
                         {(2,1),(3,1)})

    def test_boundary_only_touch_does_not_count_neighbor(self):
        self.assertEqual(h.footprint([3,2,4,4],(16,16)),
                         {(3,2),(3,3)})

    def test_full_16x16_texture_would_intersect_256_texels(self):
        self.assertEqual(len(h.footprint([16,16,0,0],(16,16))),256)

    def test_differences_are_source_rgba_not_perceptual_classifications(self):
        from PIL import Image
        from io import BytesIO
        def png(img):
            b=BytesIO();img.save(b,format="PNG");return b.getvalue()
        a=Image.new("RGBA",(16,16),(0,0,0,255))
        b=a.copy()
        for x in range(6):
            for y in range(9):b.putpixel((x,y),(255,0,0,255))
        size,diff=h.difference(png(a),png(b))
        self.assertEqual(size,(16,16))
        self.assertEqual(len(diff),54)
        self.assertIn((0,0),diff)
        self.assertNotIn((10,10),diff)

    def test_gameplay_and_gpu_causal_restrictions_preserved(self):
        s=FILE.read_text(encoding="utf-8")
        self.assertIn('"actual_GPU_face_to_texel_sampling_approved":False',s)
        self.assertIn('"INT5_parts_semantics_approved":0',s)
        self.assertIn('"INT6_training_rights_approved":0',s)
        self.assertIn('"new_real_Minecraft_executions":0',s)

if __name__=="__main__":unittest.main()
