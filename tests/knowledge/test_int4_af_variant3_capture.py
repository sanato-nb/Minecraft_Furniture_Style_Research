"""Offline, original-case-scoped tests for INT4 AF variant3 real F2 extension.

Synthetic images are regression fixtures ONLY, never claimed as real game F2.
The live workflow separately launches and audits Minecraft Fabric 1.21.1.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from mcfr import chair_runtime_fixture as fix
from mcfr import chair_runtime_capture as cap
from mcfr import int4_af_variant3_capture as experiment

class Variant3RuntimeTests(unittest.TestCase):
    def test_six_directions_controls_model_rotation_and_sep(self):
        cs=experiment.capture_cases()
        self.assertEqual(len(cs),6)
        self.assertEqual({x.case_id for x in cs},
                         {f"AFV3_{d}" for d in fix.DIRS} | {"AFV1_north","AFV1_south"})
        m=experiment.exact_expected_models()
        self.assertEqual([m[f"AFV3_{d}"]["model"] for d in fix.DIRS],
                         [experiment.MODEL_3,experiment.MODEL_3,
                          experiment.MODEL_1,experiment.MODEL_3])
        self.assertEqual([m[f"AFV3_{d}"]["y"] for d in fix.DIRS],[0,90,180,270])
        self.assertEqual(m["AFV1_north"]["model"],experiment.MODEL_1)
        self.assertEqual(m["AFV1_south"]["model"],experiment.MODEL_1)
        self.assertEqual({x.z for x in cs},{40})
        self.assertEqual(len({x.x for x in cs}),6)
        with self.assertRaises(ValueError):experiment.capture_cases("1.21.11")

    def test_original_16_and_fixture_remain_unmodified(self):
        self.assertEqual(len(fix.cases("1.21.1")),12)
        self.assertEqual(len(fix.cases("1.21.11")),4)
        with TemporaryDirectory() as t:
            dest=Path(t)/"variant3"
            meta=fix.make_pack("1.21.1",dest,experiment.capture_cases())
            self.assertEqual(meta["test_cases"],6)
            placed=(dest/"data/mcfr_chair/function/place.mcfunction").read_text()
            checked=(dest/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertEqual(placed.count("setblock "),6)
            self.assertNotIn("minecraft:oak_slab[type=top]",placed)
            self.assertEqual(checked.count("=PASS"),6)
            self.assertEqual(checked.count("=FAIL"),6)
            self.assertIn("variant=3",placed)
            self.assertIn("variant=1",placed)
            self.assertEqual(len(fix.make_pack.__code__.co_varnames)>0,True)

    def test_source_expected_registry_is_pinned_to_pixel_audit(self):
        sha=experiment.assert_original_pinned_record(Path(__file__).resolve().parents[2])
        self.assertEqual(len(sha),64)
        self.assertEqual(experiment.EXPECTED_SHA_RUNTIME,
                         "3a806533856f169a502373bda43a76eeabc1e689")

    def test_empty_or_duplicate_source_case_and_missing_targets_are_rejected(self):
        cases=experiment.capture_cases()
        with self.assertRaises(ValueError):fix.pack_lines("1.21.1",())
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            fix.pack_lines("1.21.1",(cases[0],cases[0]))
        with TemporaryDirectory() as t:
            with self.assertRaises(ValueError):
                cap.validate_source_targets("1.21.1",Path(t),cases,{})

    def test_exact_case_model_runtime_jar_validation_rejects_south_corruption(self):
        cs=experiment.capture_cases()
        expectations=experiment.exact_expected_models()
        with TemporaryDirectory() as t:
            folder=Path(t)
            variants={"facing="+x.facing+","+x.selector:
                      {"model":expectations[x.case_id]["model"],
                       "y":expectations[x.case_id]["y"]} for x in cs}
            # north & south variant1 and variant3 are distinct property selectors.
            self.assertEqual(len(variants),6)
            blob=json.dumps({"variants":variants}).encode()
            other=json.dumps({"variants":{}}).encode()
            afpath=folder/"af.jar"
            hcpath=folder/"hc.jar"
            with ZipFile(afpath,"w") as z:
                z.writestr("assets/another_furniture/blockstates/acacia_chair.json",blob)
            with ZipFile(hcpath,"w") as z:
                z.writestr("assets/handcrafted/blockstates/warped_chair.json",other)
            pins={
              "another_furniture:acacia_chair":{
                **fix.ORIGINAL_BLOCKSTATE["1.21.1"]["another_furniture:acacia_chair"],
                "sha":fix.digest_bytes(blob,"GIT_BLOB_SHA1")},
              "handcrafted:warped_chair":{
                **fix.ORIGINAL_BLOCKSTATE["1.21.1"]["handcrafted:warped_chair"],
                "sha":fix.digest_bytes(other,"GIT_BLOB_SHA1")}
            }
            with patch.dict(fix.ORIGINAL_BLOCKSTATE,{"1.21.1":pins}):
                found,_=cap.validate_source_targets(
                    "1.21.1",folder,selected_cases=cs,
                    expected_case_models=expectations)
            self.assertEqual(found["AFV3_south"]["model_target"],experiment.MODEL_1)
            self.assertEqual(found["AFV3_north"]["model_target"],experiment.MODEL_3)
            variants["facing=south,tucked=false,variant=3"]["model"]=experiment.MODEL_3
            corrupt=json.dumps({"variants":variants}).encode()
            afpath.unlink()
            with ZipFile(afpath,"w") as z:
                z.writestr("assets/another_furniture/blockstates/acacia_chair.json",corrupt)
            pins["another_furniture:acacia_chair"]["sha"]=fix.digest_bytes(
                corrupt,"GIT_BLOB_SHA1")
            with patch.dict(fix.ORIGINAL_BLOCKSTATE,{"1.21.1":pins}):
                with self.assertRaisesRegex(ValueError,"pinned source model/rotation"):
                    cap.validate_source_targets("1.21.1",folder,cs,expectations)

    @staticmethod
    def make_synthetic_report(folder):
        from PIL import Image, ImageDraw
        cs=experiment.capture_cases()
        exp=experiment.exact_expected_models()
        states=[]
        for c in cs:
            image=Image.new("RGB",(1024,684),(112,187,246))
            dr=ImageDraw.Draw(image)
            dr.rectangle((444,388,580,532),fill=(177,85,35))
            path=folder/(c.case_id+".png")
            image.save(path)
            states.append({
                "case_id":c.case_id,"original_state":c.state(),
                "original_model_target":exp[c.case_id]["model"],
                "original_model_y":exp[c.case_id]["y"],
                "screenshot_file":path.name,
                "screenshot_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                "screenshot_dimensions":[1024,684],
                "server_blockstate_verified":True,
                "native_F2_client_capture":True,
                "source_blockstate_digest":experiment.EXPECTED_SHA_STUDY,
                "running_mod_source_digest":experiment.EXPECTED_SHA_RUNTIME,
                "visual_semantic_approved":False
            })
        d={
            "schema":"MCFR_INT4_AF_VARIANT3_REAL_F2_CAPTURE/v1",
            "capture_profile":"INT4_AF_VARIANT3_4_FACING_PLUS_2_VARIANT1_CONTROLS",
            "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
            "version":"1.21.1","actual_game_capture":True,
            "minecraft_native_f2_screenshot_count":6,
            "source_state_verified_count":6,
            "human_verified_roles":0,
            "materials_or_styles_approved":0,
            "copyright_or_ai_training_approved":0,
            "original_blockstate_source_registry":{
                experiment.BLOCK:{
                    "runtime_source_hash":experiment.EXPECTED_SHA_RUNTIME,
                    "research_source_hash":experiment.EXPECTED_SHA_STUDY,
                    "scope":"RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE"
                }
            },
            "states":states
        }
        (folder/experiment.MANIFEST).write_text(json.dumps(d),encoding="utf-8")
        return d

    def test_image_diagnostic_is_not_causal_confirmation(self):
        from PIL import Image
        a=Image.new("RGB",(1024,684),(170,100,70))
        b=Image.new("RGB",(1024,684),(165,100,70))
        result=experiment.paired_pixel_diagnostics(a,b)
        self.assertGreater(result["unaligned_different_rgb_pixels"],0)
        self.assertIs(result["diff_caused_by_back_texture_approved"],False)

    def test_synthetic_inputs_verify_validator_but_do_not_prove_real_game(self):
        # Only tests logic; acceptance requires the separate launched Fabric CI.
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            self.make_synthetic_report(folder)
            result=experiment.audit(folder)
            self.assertEqual(result["scope"]["actual_f2_screenshots"],6)
            self.assertEqual(result["scope"]["server_verified_blocks"],6)
            self.assertEqual(result["scope"]["min_case_x_separation"],16)
            self.assertEqual(result["scope"]["max_stone_proxy_upper_sky_pixels"],0)
            self.assertFalse(result["control_pair_diagnostics"]["north"]["same_source_model"])
            self.assertTrue(result["control_pair_diagnostics"]["south"]["same_source_model"])
            self.assertEqual(result["nonapprovals"]["part_roles_approved"],0)
            self.assertTrue((folder/"INT4_AF_VARIANT3_F2_6_CONTACT_SHEET.png").is_file())

    def test_mutated_f2_sha_rejected(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            doc=self.make_synthetic_report(folder)
            doc["states"][0]["screenshot_sha256"]="0"*64
            (folder/experiment.MANIFEST).write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"screenshot SHA invalid"):
                experiment.audit(folder)

    def test_mutated_actual_source_model_rejected(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            doc=self.make_synthetic_report(folder)
            doc["states"][2]["original_model_target"]=experiment.MODEL_3
            (folder/experiment.MANIFEST).write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Source model"):
                experiment.audit(folder)

    def test_unapproved_roles_cannot_be_promoted(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            doc=self.make_synthetic_report(folder)
            doc["human_verified_roles"]=1
            (folder/experiment.MANIFEST).write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"safe evidence boundary failed"):
                experiment.audit(folder)

if __name__=="__main__":
    unittest.main()
