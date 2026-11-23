"""F11F test: source-built Fabric 4.0.3 vs official Modrinth 4.0.2 identity."""
import io
import json
import unittest
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory

from mcfr import int4_f11f_r08_af_dual_fabric_capture as f

class F11FOriginalResearchBoundaries(unittest.TestCase):
    def test_two_sources_are_not_claimed_same_official_distribution(self):
        self.assertEqual(f.VERSION,"1.21.1")
        self.assertEqual(f.SOURCE_VERSION,"4.0.3")
        self.assertEqual(f.OFFICIAL_FABRIC_VERSION,"4.0.2")
        self.assertIn("NOT_OFFICIAL",f.BUILT_SOURCE_KIND)

    def test_pinned_upstream_version(self):
        self.assertEqual(f.UPSTREAM,"57eb624cbb7f408d43398c7434b0d38d312cb55d")
        self.assertEqual(len(f.ORIGINAL_STUDY_STATE_BLOB),40)
        self.assertEqual(len(f.ORIGINAL_STUDY_LEAF_BLOB),40)

    def test_exactly_one_original_representative_model(self):
        cases=f.original_case()
        self.assertEqual(len(cases),1)
        c=cases[0]
        self.assertEqual(c.state(),"another_furniture:acacia_chair[facing=north,tucked=false,variant=1]")
        self.assertEqual(c.camera(),"0.5 122.3 45.5 180 20")
        self.assertEqual(f.models(),{c.case_id:{"model":f.MODEL_TARGET,"y":0}})

    def test_source_runtime_different_blockstate_hashes(self):
        self.assertNotEqual(f.ORIGINAL_STUDY_STATE_BLOB,f.OFFICIAL_RUNTIME_STATE_BLOB)

    def mock_jar(self,folder,version,mutate=False):
        p=Path(folder)/("af-"+version+".jar")
        selector={"variants":{"facing=north,tucked=false,variant=1":{
          "model":f.MODEL_TARGET}}}
        if mutate:selector["variants"]["facing=north,tucked=false,variant=1"]["model"]="other:block/air"
        with ZipFile(p,"w") as z:
            z.writestr(f.STATE_PATH,json.dumps(selector))
            z.writestr(f.MODEL_PATH,json.dumps({"parent":"other:block/cube"}))
            z.writestr("fabric.mod.json",json.dumps({"id":"another_furniture","version":version}))
        return p

    def test_reject_mismatched_official_jar_sha1(self):
        with TemporaryDirectory() as d:
            p=self.mock_jar(d,"4.0.2")
            with self.assertRaisesRegex(ValueError,"4.0.2 official original JAR changed"):
                f.source_metadata(p,"official")

    def test_reject_unverified_source_build_asset_hash(self):
        with TemporaryDirectory() as d:
            p=self.mock_jar(d,"4.0.3")
            with self.assertRaisesRegex(ValueError,"Built 4.0.3 study Git resource"):
                f.source_metadata(p,"study_source_build")

    def test_reject_wrong_release_version(self):
        with TemporaryDirectory() as d:
            p=self.mock_jar(d,"3.0.0")
            with self.assertRaisesRegex(ValueError,"Incorrect version"):
                f.source_metadata(p,"study_source_build")

    def test_reject_wrong_chair_model(self):
        with TemporaryDirectory() as d:
            p=self.mock_jar(d,"4.0.3",mutate=True)
            with self.assertRaisesRegex(ValueError,"Exact original"):
                f.source_metadata(p,"study_source_build")

    def test_reject_nonexistent_jar(self):
        with self.assertRaisesRegex(ValueError,"Missing AF version test JAR"):
            f.source_metadata(Path("/this-file-shall-not-exist/af.jar"),"study_source_build")

    def test_prevent_building_new_user_asset_rights_claim(self):
        self.assertEqual(f.MANIFEST,"INT4_F11F_R08_SINGLE_FABRIC_RELEASE_NATIVE_F2.json")
        self.assertIn("SOURCE_BUILT",f.BUILT_SOURCE_KIND)
        self.assertTrue(f.BASE_KIND.startswith("OFFICIAL_MODRINTH"))

if __name__=="__main__":
    unittest.main()
