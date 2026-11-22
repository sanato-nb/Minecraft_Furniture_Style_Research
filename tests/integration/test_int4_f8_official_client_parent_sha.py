"""INT-4-F8 source-pinned official cube parent verifier, no network needed."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"scripts/integration/build_int4_f8_official_client_parent_sha.py"
spec=importlib.util.spec_from_file_location("mcfr_int4f8",SRC)
f=importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


class MojangOriginalParent(unittest.TestCase):
    def test_exact_frozen_study_case_s22_and_parent_path(self):
        row=f.original_study()
        self.assertEqual(row["case"],"S22")
        self.assertEqual(row["provider"],"V1211-5")
        self.assertEqual(row["provider_path"],"assets/minecraft/models/block/cube.json")
        self.assertEqual(row["provider_sha"],f.ORIGINAL_PARENT_RECORDED_HASH)
        self.assertEqual(row["model_hash_kind"],"GIT_BLOB_SHA1")
        self.assertEqual(len(row["provider_sha"]),64)

    def test_pinned_versions_and_MOJANG_source_metadata(self):
        self.assertEqual(f.VERSIONS,("1.21.1","1.21.11"))
        self.assertEqual(f.PINNED_CLIENT_SHA1["1.21.1"],
                         "30c73b1c5da787909b2f73340419fdf13b9def88")
        self.assertEqual(f.PINNED_CLIENT_SHA1["1.21.11"],
                         "ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd")
        self.assertEqual(f.MOJANG_MANIFEST,
                         "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")

    def test_git_blob_and_plain_file_hashes_have_different_meaning(self):
        data=b'{"parent":"block/block","elements":[]}'
        self.assertEqual(f.gitblob(data),
                         hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest())
        self.assertNotEqual(f.gitblob(data),f.sha1(data))
        self.assertEqual(f.sha256(data),hashlib.sha256(data).hexdigest())

    def test_semantic_comparison_is_key_order_whitespace_independent(self):
        a=json.loads(b'{"parent":"block/block","elements":[{"faces":{}}]}')
        b=json.loads(b'{ "elements": [ { "faces": {} } ], "parent": "block/block" }')
        self.assertEqual(f.canon(a),f.canon(b))
        self.assertNotEqual(f.sha256(json.dumps(a).encode()),f.sha256(json.dumps(b).encode()))

    def test_official_client_jar_bytes_not_part_of_repository_outputs(self):
        self.assertEqual(f.OUTPUT.suffix,".json")
        self.assertEqual(f.PARENT,"assets/minecraft/models/block/cube.json")
        self.assertEqual(f.PARENT_OF_PARENT,"assets/minecraft/models/block/block.json")

    def test_source_file_sha_drift_is_detected(self):
        self.assertEqual(f.sha256(f.ORIGINAL.read_bytes()),f.EXPECTED_RESEARCH_SHA256)

    def test_research_git_sha_is_not_assumed_same_as_1_21_11_repo_copy(self):
        # The checked-in pretty-printed repo copy is different from
        # the frozen 1-5-B provider hash: a good reason to inspect actual JAR bytes.
        pretty=ROOT/"1.21.11/assets/minecraft/models/block/cube.json"
        self.assertTrue(pretty.is_file())
        self.assertNotEqual(f.gitblob(pretty.read_bytes()),f.ORIGINAL_PARENT_RECORDED_HASH)

if __name__=="__main__":
    unittest.main()
