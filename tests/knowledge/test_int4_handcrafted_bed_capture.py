"""INT-4 real Handcrafted bed F2 provenance and nonapproval regressions.

Synthetic PNGs in this file are validator fixtures, never gameplay evidence.
"""
from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import hashlib,importlib.util,json,unittest

from mcfr import int4_handcrafted_bed_capture as study
from mcfr.chair_runtime_fixture import make_pack,cases as original_chairs

class HandcraftedBedTests(unittest.TestCase):
    def test_historical_source_cases_and_two_part_coordinates(self):
        rows,ledger_sha=study.source_rows()
        self.assertEqual(set(rows),{"S37","S38"})
        self.assertEqual(len(ledger_sha),64)
        self.assertEqual([x.state() for x in study.cases()],[
            "handcrafted:oak_fancy_bed[color=white,facing=north,occupied=false,part=foot,shape=single]",
            "handcrafted:oak_fancy_bed[color=white,facing=north,occupied=false,part=head,shape=single]"])
        self.assertEqual([int(rows[x]["elements"]) for x in study.ORDER],[12,1])
        self.assertEqual([int(rows[x]["faces"]) for x in study.ORDER],[72,6])
        self.assertEqual(len({c.x for c in study.cases()}),2)
        self.assertEqual({x.z for x in study.cases()},{40})
        with self.assertRaises(ValueError):study.cases("1.21.11")

    def test_fixture_pack_does_not_mutate_existing_chair_presets(self):
        self.assertEqual(len(original_chairs("1.21.1")),12)
        self.assertEqual(len(original_chairs("1.21.11")),4)
        with TemporaryDirectory() as temp:
            pack=Path(temp)/"hcbed"
            meta=make_pack("1.21.1",pack,study.cases())
            self.assertEqual(meta["test_cases"],2)
            place=(pack/"data/mcfr_chair/function/place.mcfunction").read_text()
            checks=(pack/"data/mcfr_chair/function/verify.mcfunction").read_text()
            self.assertEqual(place.count("setblock "),2)
            self.assertIn("part=foot",place)
            self.assertIn("part=head",place)
            self.assertEqual(checks.count("=PASS"),2)

    def test_unique_selected_variant_and_original_source_paths(self):
        variants={"variants":{
          "color=white,facing=north,occupied=false,part=foot,shape=single":{
             "model":"handcrafted:block/oak_fancy_bed_single_white_foot"},
          "color=white,facing=north,occupied=false,part=head,shape=single":{
             "model":"handcrafted:block/oak_fancy_bed_single_white_head"}}}
        for name in study.ORDER:
            row=study.source_rows()[0][name]
            _,_,opt=study.selected_options(variants,row["state"])
            self.assertIn("handcrafted:block/oak_fancy_bed_single_white_",opt["model"])
        self.assertEqual(study.ref("common/src/main/generated/resources/assets/handcrafted/blockstates/oak_fancy_bed.json"),
                         "assets/handcrafted/blockstates/oak_fancy_bed.json")
        with self.assertRaises(ValueError):
            study.selected_options({"variants":{}},"facing=north")

    def test_missing_real_handcrafted_release_or_source_archive_rejected(self):
        with TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError,"Exactly one pinned"):
                study.preflight(Path(temp),Path(temp)/"none.zip")
            with ZipFile(Path(temp)/"bad.jar","w") as z:
                z.writestr("assets/handcrafted/blockstates/oak_fancy_bed.json","{}")
            with self.assertRaisesRegex(ValueError,"SHA-1 changed"):
                study.preflight(Path(temp),Path(temp)/"none.zip")

    @unittest.skipUnless(importlib.util.find_spec("PIL") is not None,
                         "Pillow only required for synthetic regression")
    def test_synthetic_png_evidence_validated_and_tamper_rejected(self):
        from PIL import Image
        with TemporaryDirectory() as temp:
            root=Path(temp);rows,ledger=study.source_rows()
            states=[];cases={}
            for item in study.cases():
                cid=item.case_id;source=rows[cid]
                picture=root/(cid+".png")
                Image.new("RGB",(1024,684),(165,99,55)).save(picture)
                cases[cid]={
                  "model_path":source["model_path"],
                  "model_git_blob_sha1":source["model_sha"],
                  "provider_git_blob_sha1":source["provider_sha"],
                  "faces":int(source["faces"])}
                states.append({
                  "case_id":cid,"original_state":item.state(),
                  "source_model_path":source["model_path"],
                  "source_model_git_blob_sha1":source["model_sha"],
                  "source_provider_git_blob_sha1":source["provider_sha"],
                  "source_faces":int(source["faces"]),
                  "server_source_state_verified":True,"native_F2_verified":True,
                  "foreground_chroma_pixels":400,
                  "screenshot_file":picture.name,"screenshot_dimensions":[1024,684],
                  "screenshot_sha256":hashlib.sha256(picture.read_bytes()).hexdigest(),
                  "natural_bed_pair_placement_tested":False,
                  "semantic_or_ai_rights_approved":False})
            data={
              "schema":"MCFR_INT4_HC_BED_FOOT_HEAD_ACTUAL_F2/v1",
              "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
              "actual_Fabric_client":True,
              "server_state_confirmed":2,"native_F2_count":2,
              "semantic_part_roles_approved":0,"material_style_approved":0,
              "ai_training_and_redistribution_rights_approved":0,
              "original_source_registry":{
                "HC_release_SHA1":study.HC_RELEASE_SHA1,
                "original_1_5_application_csv_sha256":ledger,"cases":cases},
              "states":states}
            (root/study.MANIFEST).write_text(json.dumps(data))
            checked=study.audit(root)
            self.assertEqual(checked["actual_F2_count"],2)
            self.assertFalse(checked["limitations"]["natural_bed_two_part_behavior_tested"])
            orig=states[0]["screenshot_sha256"]
            states[0]["screenshot_sha256"]="0"*64
            (root/study.MANIFEST).write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,"image SHA mismatch"):
                study.audit(root)
            states[0]["screenshot_sha256"]=orig
            data["ai_training_and_redistribution_rights_approved"]=1
            (root/study.MANIFEST).write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,"proof incomplete"):
                study.audit(root)

if __name__=="__main__":unittest.main()
