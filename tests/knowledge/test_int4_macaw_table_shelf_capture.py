"""Source-pinned INT-4 Macaw table/bookshelf four-state capture regressions.

Synthetic screenshots below only test validator behavior. The separate real
Fabric/Xvfb Actions job must capture actual native F2 evidence.
"""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from mcfr import int4_macaw_table_shelf_capture as study
from mcfr.chair_runtime_fixture import make_pack,cases

ROOT=Path(__file__).resolve().parents[2]

class TableShelfTests(unittest.TestCase):
    def test_four_historic_states_models_and_distances(self):
        rows,appsha,prior=study.source_rows()
        self.assertEqual(set(rows),set(study.ORDER))
        self.assertEqual(len(appsha),len(prior))
        self.assertEqual(len(appsha),64)
        cases4=study.capture_cases()
        self.assertEqual([c.state() for c in cases4],[
            "mcwfurnitures:oak_table[east=false,north=false,south=false,west=false]",
            "mcwfurnitures:oak_table[east=true,north=true,south=true,west=true]",
            "mcwfurnitures:oak_bookshelf[connection=base,facing=north]",
            "mcwfurnitures:oak_bookshelf[connection=middle,facing=north]"])
        self.assertEqual([int(rows[k]["faces"]) for k in study.ORDER],[31,6,31,19])
        self.assertEqual([int(rows[k]["elements"]) for k in study.ORDER],[6,1,10,8])
        self.assertEqual([int(rows[k]["y"]) for k in study.ORDER],[0,0,180,180])
        self.assertEqual({c.z for c in cases4},{40})
        self.assertTrue(all(abs(c.x-d.x)>=16
            for i,c in enumerate(cases4) for d in cases4[i+1:]))
        with self.assertRaises(ValueError):study.capture_cases("1.21.1")

    def test_existing_16_chair_cases_are_unmodified(self):
        self.assertEqual(len(cases("1.21.1")),12)
        self.assertEqual(len(cases("1.21.11")),4)
        with TemporaryDirectory() as t:
            root=Path(t)/"pack"
            out=make_pack("1.21.11",root,study.capture_cases())
            self.assertEqual(out["test_cases"],4)
            place=(root/"data/mcfr_chair/function/place.mcfunction").read_text()
            verify=(root/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertIn("east=true",place)
            self.assertIn("connection=middle",place)
            self.assertEqual(place.count("setblock "),4)
            self.assertEqual(verify.count("=PASS"),4)
            self.assertEqual(verify.count("=FAIL"),4)

    def test_actual_mod_jar_must_be_fixed_source(self):
        with TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError,"Exactly one pinned Macaw"):
                study.verify_running_source(Path(t))
            fake=Path(t)/"fake.jar"
            with ZipFile(fake,"w") as z:
                z.writestr("assets/mcwfurnitures/blockstates/oak_bookshelf.json","{}")
            with self.assertRaisesRegex(ValueError,"SHA256 differs"):
                study.verify_running_source(Path(t))

    @unittest.skipUnless(importlib.util.find_spec("PIL") is not None,
                         "Pillow visual validator regression optional in nonvisual CI")
    def test_synthetic_manifest_verify_and_corruption_rejects(self):
        from PIL import Image
        with TemporaryDirectory() as t:
            folder=Path(t)
            rows,appsha,checkpoint=study.source_rows()
            record=[]
            registry={
                "mod_jar_sha256":study.MACAW_SHA256,
                "historical_application_sha256":appsha,
                "previous_int4_checkpoint_sha256":checkpoint,
                "states":{},
            }
            for case in study.capture_cases():
                cid=case.case_id
                img=folder/(cid+".png")
                Image.new("RGB",(1024,684),(167,91,50)).save(img)
                registry["states"][cid]={
                    "model_path":rows[cid]["model_path"],
                    "model_sha256":rows[cid]["model_sha"],
                    "provider_sha256":rows[cid]["provider_sha"],
                    "original_model_y":int(rows[cid]["y"]),
                    "faces":int(rows[cid]["faces"])}
                record.append({
                    "case_id":cid,"original_state":case.state(),
                    "original_model_path":rows[cid]["model_path"],
                    "original_model_sha256":rows[cid]["model_sha"],
                    "original_provider_sha256":rows[cid]["provider_sha"],
                    "original_model_y":int(rows[cid]["y"]),
                    "server_state_verified":True,"native_f2_verified":True,
                    "connection_formed_naturally_tested":False,
                    "semantic_or_rights_approved":False,
                    "screen_foreground_chroma_pixels":420,
                    "screenshot_file":img.name,"screenshot_dimensions":[1024,684],
                    "screenshot_sha256":hashlib.sha256(img.read_bytes()).hexdigest()})
            m={
                "schema":"MCFR_INT4_MACAW_LINKED_TABLE_SHELF_REAL_F2/v1",
                "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
                "actual_game_capture":True,
                "source_state_verified_count":4,
                "minecraft_native_f2_screenshot_count":4,
                "semantic_part_roles_approved":0,"material_style_approved":0,
                "copyright_or_ai_training_approved":0,
                "original_source_registry":registry,"states":record
            }
            f=folder/study.MANIFEST
            f.write_text(json.dumps(m))
            v=study.audit(folder)
            self.assertEqual(v["server_verified_states"],4)
            self.assertFalse(v["boundaries"]["natural_connected_block_update_rules_tested"])
            self.assertEqual(v["source_1_5_face_counts"],{"S18":31,"S19":6,"S28":31,"S29":19})
            validsha=record[0]["screenshot_sha256"]
            m["states"][0]["screenshot_sha256"]="0"*64
            f.write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError,"F2 PNG image SHA changed"):
                study.audit(folder)
            m["states"][0]["screenshot_sha256"]=validsha
            m["copyright_or_ai_training_approved"]=1
            f.write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError,"no semantic approvals"):
                study.audit(folder)

if __name__=="__main__":
    unittest.main()
