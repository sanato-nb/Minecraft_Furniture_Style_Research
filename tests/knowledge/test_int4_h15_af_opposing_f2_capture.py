"""H15 pinned real Fabric opposing-camera chair capture, tests only the contract.

Synthetic frames are test fixtures, NOT substitute original Minecraft screenshots.
"""
from __future__ import annotations
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image,ImageDraw
from mcfr import int4_h15_af_opposing_f2_capture as h15
from mcfr import int4_h12_af_chair_samepose_f2_capture as h12


def fake_img():
    return Image.new("RGB",(1024,684),(200,200,200))


def png(image):
    out=io.BytesIO()
    image.save(out,"PNG")
    return out.getvalue()


class H15ModelTwoCameraSource(unittest.TestCase):
    def test_actual_pinned_H12_case_and_sources(self):
        case=h12.original_case()[0]
        self.assertEqual((case.x,case.y,case.z),h15.BLOCK_XYZ)
        self.assertEqual(case.camera(),h15.EXPECTED_CAMERAS["south"])
        self.assertEqual(h12.JAR_SHA1,"c2f992081bdc4795ed6d87771a3b5f7c71103785")
        self.assertEqual(h15.VERSION,"1.21.1")

    def test_same_block_facing_two_observer_planes(self):
        self.assertEqual(h15.camera_face_candidate("south"),"south")
        self.assertEqual(h15.camera_face_candidate("north"),"north")
        self.assertEqual(h15.EXPECTED_CAMERAS["north"],"-87.5 122.3 35.5 0 20")
        with self.assertRaisesRegex(ValueError,"INVALID_H15_CAMERA_VIEW"):
            h15.camera_face_candidate("east")
        self.assertEqual(h15.STAGES,("model1_before","model3","model1_after","air"))

    def test_original_model_selectors_keep_facing_north(self):
        self.assertEqual(h15.stage_state("model1_before"),h12.state("model1"))
        self.assertEqual(h15.stage_state("model3"),h12.state("model3"))
        self.assertEqual(h15.stage_state("model1_after"),h12.state("model1"))
        self.assertEqual(h15.stage_state("air"),"minecraft:air")
        for name in h15.STAGES:
            self.assertIn("north",h15.stage_state(name) if name!="air" else "north")

    def test_pixel_ROI_A_B_A_air_isolated_foreground(self):
        one=fake_img()
        three=fake_img()
        after=fake_img()
        air=fake_img()
        for im in (one,three,after):
            ImageDraw.Draw(im).rectangle((485,410,545,480),fill=(88,55,30))
        ImageDraw.Draw(three).rectangle((493,433,530,461),fill=(58,100,80))
        result=h15.measure_view(dict(model1_before=one,model3=three,
                                     model1_after=after,air=air))
        self.assertGreater(result["model1_to_model3_changed_pixels"],25)
        self.assertEqual(result["model1_to_model1_temporal_changed_pixels"],0)
        self.assertEqual(result["model_delta_outside_air_foreground"],0)
        self.assertEqual(result["model_delta_bounds_xyxy_inclusive"],[493,433,530,461])

    def test_non_native_screenshot_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"DIMENSION_MISMATCH"):
            h15.pixel_changes(fake_img(),Image.new("RGB",(320,240)))

    def test_audit_fails_without_exact_original_game_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            (folder/h15.ORIGINAL).write_text(json.dumps({"schema":"fake"}))
            with self.assertRaisesRegex(ValueError,"GAME_MANIFEST"):
                h15.audit(folder)

    def test_output_and_source_no_unconditional_approval(self):
        source=Path(h15.__file__).read_text(encoding="utf-8")
        self.assertIn('"source_face_to_screen_pixel_GPU_causality_approved":False',source)
        self.assertIn('"verified_GPU_face_texel_pixel_attribution":False',source)
        self.assertIn('"F70_unconditional_approvals":0',source)
        self.assertIn('"INT6_training_or_redistribution_approved":0',source)
        self.assertNotIn("player_sleep_wake_destroy",source)

    def test_source_window_commands_use_acknowledged_H13_helpers(self):
        src=Path(h15.__file__).read_text(encoding="utf-8")
        self.assertIn("send_minecraft_command(xdo,cmd)",src)
        self.assertIn("confirmed_camera_teleport(proc,logtext,send,refocus,pos)",src)
        self.assertIn("confirmed_spectator_mode(proc,logtext,send,refocus)",src)
        self.assertIn("start=len(logtext())",src)
        self.assertIn("H15_ORIGINAL_TWO_OPPOSING_CAMERA_SOURCE_DRIFT",src)


if __name__=="__main__":
    unittest.main()
