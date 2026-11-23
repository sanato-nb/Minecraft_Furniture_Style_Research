"""F11D real vanilla 1.21.11 bed: zero-model source, real head/foot commands, AIR controls."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image,ImageDraw
from mcfr import int4_f11d_vanilla_white_bed_special_capture as bed
from mcfr import int4_f11c_vanilla_kitchen_decor_four_capture as prior
from mcfr.chair_runtime_fixture import make_pack

class F11DVanillaBedSpecialSource(unittest.TestCase):
    def test_frozen_original_v11_one_application_no_geometry(self):
        r=bed.original_case()
        self.assertEqual((r["case"],r["cohort"],r["minecraft"],r["block"]),
                         ("V11","VANILLA","1.21.11","white_bed"))
        self.assertEqual(r["geometry_status"],"NO_ORDINARY_ELEMENTS")
        self.assertEqual((int(r["elements"]),int(r["faces"])),(0,0))
        self.assertFalse(r["provider_path"])

    def test_original_bed_blockstate_and_model_git_blob_pins(self):
        self.assertEqual(bed.STATE_SHA1,"6577c90a27efb34a7099150253c0bf557d75214c")
        self.assertEqual(bed.MODEL_SHA1,"9406a8491ed2532d4878b0a91b16a0e5f8d93d80")
        self.assertEqual(bed.original_case()["model_hash_kind"],"GIT_BLOB_SHA1")
        self.assertEqual(bed.original_case()["state"],"{}")

    def test_original_mojang_client_12111_pin(self):
        self.assertEqual(bed.MOJANG_CLIENT_SHA1,prior.MOJANG_CLIENT_SHA1)
        self.assertEqual(bed.MOJANG_CLIENT_SHA256,prior.MOJANG_CLIENT_SHA256)
        self.assertEqual(bed.STUDY_SHA256,prior.PIN_LEDGER_SHA256)

    def test_foot_head_are_two_distinct_runtime_states(self):
        self.assertEqual(bed.feet().state(),
                         "minecraft:white_bed[facing=north,part=foot,occupied=false]")
        self.assertEqual(bed.head(),
                         "minecraft:white_bed[facing=north,part=head,occupied=false]")
        self.assertEqual(bed.feet().z,bed.Z)
        self.assertEqual(bed.capture_cases()[0].case_id,"V11")
        self.assertEqual(len(bed.capture_cases()),1)

    def test_wrong_release_is_fail_closed(self):
        with self.assertRaises(ValueError):bed.capture_cases("1.21.1")

    def test_noninteracting_strict_bed_is_two_real_vanilla_blocks(self):
        with TemporaryDirectory() as temp:
            pack=Path(temp)/"bed"
            make_pack(bed.VERSION,pack,selected_cases=bed.capture_cases())
            evidence=bed.prepare_bed_datapack(pack)
            self.assertEqual(set(evidence),{"construct","confirm_air","verify"})
            p=pack/"data/mcfr_bed/function"
            lines=(p/"construct.mcfunction").read_text().splitlines()
            self.assertEqual(lines[:2],
                             [f"setblock {bed.X} {bed.Y} {bed.Z} {bed.feet().state()} strict",
                              f"setblock {bed.X} {bed.Y} {bed.Z-1} {bed.head()} strict"])
            self.assertEqual(lines[-1],"say MCFR_BED_CONSTRUCTED")
            self.assertEqual((p/"verify.mcfunction").read_text().count("=PASS"),2)
            self.assertIn("MCFR_BED_AIR_HEAD=PASS",(p/"confirm_air.mcfunction").read_text())
            stage=(pack/"data/mcfr_chair/function/place.mcfunction").read_text()
            self.assertNotIn(bed.feet().state(),stage)
            self.assertIn(f"setblock {bed.X} {bed.Y} {bed.Z} minecraft:air strict",stage)

    def test_unchanged_stone_platform_surrounds_both_bed_halves(self):
        with TemporaryDirectory() as temp:
            pack=Path(temp)/"bed"
            make_pack(bed.VERSION,pack,selected_cases=bed.capture_cases())
            bed.prepare_bed_datapack(pack)
            stage=(pack/"data/mcfr_chair/function/place.mcfunction").read_text()
            self.assertIn("minecraft:smooth_stone",stage)
            self.assertIn(f"setblock {bed.X} {bed.Y} {bed.Z-1} minecraft:air strict",stage)

    def test_synthetic_pixel_difference_control(self):
        with TemporaryDirectory() as temp:
            directory=Path(temp)
            background=Image.new("RGB",(1024,684),(80,90,100))
            background.save(directory/"V11_AIR_A.png")
            background.save(directory/"V11_AIR_B.png")
            front=background.copy()
            ImageDraw.Draw(front).rectangle((450,380,550,420),fill=(250,250,250))
            front.save(directory/"V11_BED.png")
            front.save(directory/"V11_BED_SIDE.png")
            m=bed.image_metrics(directory)
            self.assertEqual(m["air_control_changed_pixels"],0)
            self.assertGreater(m["bed_vs_air_changed_pixels"],700)

    def test_synthetic_identical_air_and_bed_must_fail(self):
        with TemporaryDirectory() as temp:
            directory=Path(temp)
            background=Image.new("RGB",(1024,684),(80,90,100))
            for name in ("V11_AIR_A","V11_AIR_B","V11_BED","V11_BED_SIDE"):
                background.save(directory/(name+".png"))
            with self.assertRaises(ValueError):bed.image_metrics(directory)

    def test_special_renderer_callsite_and_AI_rights_still_unapproved(self):
        self.assertNotIn("V11",prior.ORDER)
        self.assertEqual(bed.MIN_BED_AIR_CHANGED,700)
        self.assertNotIn("R06",bed.CASE)
        self.assertNotIn("R08",bed.CASE)

if __name__=="__main__":
    unittest.main()
