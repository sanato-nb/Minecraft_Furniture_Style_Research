"""Regression guards for INT-4 Macaw kitchen real-client F2 experiments.

Synthetic local images below exercise validation only; they are NEVER
real-game evidence or a substitute for the CI Java/Fabric F2 run.
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from mcfr import int4_macaw_kitchen_capture as kitchen
from mcfr.chair_runtime_fixture import make_pack

ROOT=Path(__file__).resolve().parents[2]


class KitchenCaptureTests(unittest.TestCase):
    def test_macaw_case_ids_and_original_source_properties(self):
        rows,sha,prior=kitchen.source_rows()
        self.assertEqual(set(rows),set(kitchen.ORDER))
        self.assertEqual(len(sha),64)
        self.assertEqual(len(prior),64)
        cases=kitchen.capture_cases()
        self.assertEqual([x.case_id for x in cases],list(kitchen.ORDER))
        self.assertEqual([x.state() for x in cases],[
            "mcwfurnitures:oak_counter[facing=north]",
            "mcwfurnitures:oak_kitchen_sink[facing=north,water=false]",
            "mcwfurnitures:oak_kitchen_sink[facing=north,water=true]"])
        self.assertEqual(len({x.x for x in cases}),3)
        self.assertEqual({x.z for x in cases},{40})
        with self.assertRaises(ValueError):kitchen.capture_cases("1.21.1")

    def test_existing_fixture_engine_keeps_default_case_population(self):
        from mcfr.chair_runtime_fixture import cases
        self.assertEqual(len(cases("1.21.1")),12)
        self.assertEqual(len(cases("1.21.11")),4)
        with TemporaryDirectory() as scratch:
            meta=make_pack("1.21.11",Path(scratch)/"pack",kitchen.capture_cases())
            self.assertEqual(meta["test_cases"],3)
            pack=Path(scratch)/"pack"
            cmds=(pack/"data/mcfr_chair/function/place.mcfunction").read_text()
            checks=(pack/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertEqual(cmds.count("setblock "),3)
            self.assertIn("water=true",cmds)
            self.assertIn("water=false",cmds)
            self.assertEqual(checks.count("=PASS"),3)
            self.assertEqual(checks.count("=FAIL"),3)

    def test_original_geometry_and_model_paths_from_study(self):
        rows,_,_=kitchen.source_rows()
        self.assertEqual([int(rows[k]["faces"]) for k in kitchen.ORDER],[11,55,56])
        self.assertEqual([int(rows[k]["elements"]) for k in kitchen.ORDER],[2,16,17])
        self.assertEqual([int(rows[k]["y"]) for k in kitchen.ORDER],[180,180,180])
        self.assertEqual(kitchen.model_path("mcwfurnitures:block/counter/oak_counter"),
                         "assets/mcwfurnitures/models/block/counter/oak_counter.json")

    def test_corrupt_model_selection_rejected(self):
        with self.assertRaisesRegex(ValueError,"Malformed"):
            kitchen.parse_selector("facing=north,facing=south")
        with self.assertRaisesRegex(ValueError,"Malformed"):
            kitchen.parse_selector("west")
        with self.assertRaisesRegex(ValueError,"Invalid"):
            kitchen.model_path("../bad")

    def test_missing_or_wrong_real_macaw_jar_rejected(self):
        with TemporaryDirectory() as tmp:
            mod=Path(tmp)
            with self.assertRaisesRegex(ValueError,"one real mod JAR"):
                kitchen.validate_running_source(mod)
            with ZipFile(mod/"fake.jar","w") as jar:
                jar.writestr("assets/mcwfurnitures/blockstates/oak_kitchen_sink.json",b"{}")
            with self.assertRaisesRegex(ValueError,"binary differs"):
                kitchen.validate_running_source(mod)

    @unittest.skipUnless(__import__("importlib").util.find_spec("PIL") is not None,
                         "Pillow required for synthetic image validation unit tests")
    def test_synthetic_f2_validator_requires_hash_and_no_semantic_promotion(self):
        from PIL import Image
        with TemporaryDirectory() as temp:
            root=Path(temp)
            rows,appsha,prior=kitchen.source_rows()
            registry={
                "mod_jar":"fabric-macaw-original.jar",
                "mod_jar_sha256":kitchen.MACAW_SHA256,
                "historical_application_csv_sha256":appsha,
                "prior_int4_source_checkpoint_sha256":prior,
                "states":{},
            }
            evid=[]
            for case in kitchen.capture_cases():
                row=rows[case.case_id]
                png=root/(case.case_id+".png")
                Image.new("RGB",(1024,684),(160,110,80)).save(png)
                registry["states"][case.case_id]={
                    "source_model_sha256":row["model_sha"],
                    "source_faces":int(row["faces"]),
                }
                evid.append({
                    "case_id":case.case_id,
                    "original_state":case.state(),
                    "original_model_sha256":row["model_sha"],
                    "screenshot_file":png.name,
                    "screenshot_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
                    "screenshot_dimensions":[1024,684],
                    "server_blockstate_verified":True,
                    "native_F2_client_capture":True,
                    "semantic_material_or_rights_approved":False,
                })
            document={
                "schema":"MCFR_INT4_MACAW_KITCHEN_ACTUAL_GAME_F2/v1",
                "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
                "actual_game_capture":True,
                "source_state_verified_count":3,
                "minecraft_native_f2_screenshot_count":3,
                "semantic_part_roles_approved":0,
                "material_style_approved":0,
                "copyright_or_ai_training_approved":0,
                "original_source_registry":registry,
                "states":evid,
            }
            target=root/kitchen.MANIFEST
            target.write_text(json.dumps(document))
            report=kitchen.audit(root)
            self.assertEqual(report["actual_native_f2_count"],3)
            self.assertEqual(report["source_water_face_delta"],1)
            self.assertFalse(report["scope"]["game_runtime_water_mechanism_tested"])
            self.assertEqual(report["scope"]["human_part_role_review_approved"],0)
            oldsha=document["states"][0]["screenshot_sha256"]
            document["states"][0]["screenshot_sha256"]="0"*64
            target.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError,"screenshot SHA mismatch"):
                kitchen.audit(root)
            document["states"][0]["screenshot_sha256"]=oldsha
            document["copyright_or_ai_training_approved"]=1
            target.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError,"nonapproval"):
                kitchen.audit(root)


if __name__=="__main__":
    unittest.main()
