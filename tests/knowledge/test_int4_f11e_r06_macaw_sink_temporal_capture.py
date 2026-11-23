"""F11E actual R06 Macaw S43 temporal F2 source and fail-closed pixel test."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image,ImageDraw
from mcfr import int4_f11e_r06_macaw_sink_temporal_capture as temporal
from mcfr import int4_macaw_kitchen_capture as kitchen
from mcfr.chair_runtime_fixture import make_pack

class R06TemporalOriginalSource(unittest.TestCase):
    def test_exact_original_macaw_S43_historical_source(self):
        rows,ledger,prior=kitchen.source_rows()
        row=rows["S43"]
        self.assertEqual((row["cohort"],row["minecraft"],row["block"],
                          row["state"],row["model_hash_kind"]),
                         ("MACAW","1.21.11","mcwfurnitures:oak_kitchen_sink",
                          "facing=north;water=true","SHA256"))
        self.assertEqual(int(row["elements"]),17)
        self.assertEqual(int(row["faces"]),56)
        self.assertEqual(len(ledger),64)
        self.assertEqual(len(prior),64)

    def test_S42_original_dry_sink_is_negative_source_control(self):
        rows,_,_=kitchen.source_rows()
        a,b=rows["S42"],rows["S43"]
        self.assertEqual(a["state"],"facing=north;water=false")
        self.assertEqual((int(a["elements"]),int(a["faces"])),(16,55))
        self.assertEqual((int(b["elements"]),int(b["faces"])),(17,56))
        self.assertEqual(a["block"],b["block"])

    def test_exactly_one_source_S43_in_disposable_world(self):
        selected=temporal.capture_cases()
        self.assertEqual(len(selected),1)
        self.assertEqual(selected[0].case_id,"S43")
        self.assertEqual(selected[0].state(),
                         "mcwfurnitures:oak_kitchen_sink[facing=north,water=true]")

    def test_fails_if_wrong_minecraft_release(self):
        with self.assertRaises(ValueError):temporal.capture_cases("1.21.1")

    def test_time_verify_datapack_does_not_change_original_state(self):
        with TemporaryDirectory() as temp:
            pack=Path(temp)/"r06"
            make_pack(temporal.VERSION,pack,selected_cases=temporal.capture_cases())
            original=(pack/"data/mcfr_chair/function/place.mcfunction").read_bytes()
            recorded=temporal.prepare_r06_datapack(pack)
            self.assertEqual((pack/"data/mcfr_chair/function/place.mcfunction").read_bytes(),original)
            script=(pack/"data/mcfr_r06/function/verify.mcfunction").read_text()
            self.assertIn(temporal.capture_cases()[0].state(),script)
            self.assertIn("MCFR_R06_S43_STABLE=PASS",script)
            self.assertIn("MCFR_R06_S43_STABLE=FAIL",script)
            self.assertEqual(recorded["verify_sha256"],
                             temporal.sha(script.encode()))

    def test_three_real_timepoints_two_gaps_at_least_8_seconds(self):
        self.assertEqual(temporal.ORDER,("R06_T0","R06_T1","R06_T2"))
        self.assertGreaterEqual(temporal.MIN_INTERVAL_SECONDS,8)
        self.assertEqual(len(temporal.ORDER)-1,2)

    def test_original_water_roi_has_blue_water_pixels(self):
        im=Image.new("RGB",(1024,684),(120,120,120))
        ImageDraw.Draw(im).rectangle(temporal.WATER_ROI,fill=(20,24,248))
        self.assertGreater(temporal.blue_water_pixels(im),temporal.MIN_WATER_BLUE_PIXELS)

    def test_unchanged_synthetic_water_is_valid_static_observation(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)
            image=Image.new("RGB",(1024,684),(120,120,120))
            ImageDraw.Draw(image).rectangle(temporal.WATER_ROI,fill=(20,24,248))
            for key in temporal.ORDER:image.save(folder/(key+".png"))
            m=temporal.compare_frames(folder)
            self.assertFalse(m["water_pixel_changed_observed"])
            self.assertIn("NO_WATER_REGION_CHANGE",m["temporal_interpretation"])
            self.assertTrue(all(x["stone_control_changed_pixels"]==0
                                for x in m["paired_pixel_differences"].values()))

    def test_synthetic_water_variation_without_ground_variation(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)
            for n,key in enumerate(temporal.ORDER):
                image=Image.new("RGB",(1024,684),(120,120,120))
                ImageDraw.Draw(image).rectangle(temporal.WATER_ROI,
                                               fill=(20,24,180+n*18))
                image.save(folder/(key+".png"))
            m=temporal.compare_frames(folder)
            self.assertTrue(m["water_pixel_changed_observed"])
            self.assertEqual(m["max_background_stone_control_delta"],0)
            self.assertIn("NOT_CAUSAL_ANIMATION_PROOF",m["temporal_interpretation"])

    def test_stone_control_drift_must_fail_closed(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)
            for i,key in enumerate(temporal.ORDER):
                image=Image.new("RGB",(1024,684),(120,120,120))
                ImageDraw.Draw(image).rectangle(temporal.WATER_ROI,fill=(20,24,248))
                if i:
                    ImageDraw.Draw(image).rectangle(temporal.STONE_CONTROL_ROI,fill=(240,200,200))
                image.save(folder/(key+".png"))
            with self.assertRaises(ValueError):temporal.compare_frames(folder)

    def test_original_JAR_sha_must_be_pinned(self):
        self.assertEqual(temporal.MACAW_SHA256,kitchen.MACAW_SHA256)
        self.assertEqual(len(temporal.MACAW_SHA256),64)

if __name__=="__main__":
    unittest.main()
