"""Regressions for reusing the untouched historical 1-3-C shape analyzer."""
from contextlib import closing
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mcfr import geometry_engine as geometry, research_db as catalog


class GeometryEngineTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(TemporaryDirectory()))
        self.db_path = self.root / "operational.sqlite"
        catalog.initialize(self.db_path)
        self.db = self.enterContext(closing(catalog.open_db(self.db_path, "rw")))

    def put(self, path, body, *, directory=None):
        directory = directory or self.root
        dest = directory / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        return {"source_path": path, "kind": "model",
                "resource_id": geometry.model_reference(
                    "minecraft:block/" + Path(path).stem, "")[0],
                "hash_algorithm": "SHA256", "digest": hashlib.sha256(body).hexdigest()}

    def register(self, key, assets, *, profile="mods", version="1.21.11"):
        release = {"release_key": key, "profile": profile, "target_id": "minecraft" if profile == "vanilla" else "sample",
                   "version": "fixture", "minecraft_version": version,
                   "loader": "vanilla" if profile == "vanilla" else "fabric",
                   "pin_algorithm": "GIT_COMMIT_SHA1", "pin_digest": "e" * 40, "source": "fixture"}
        with catalog.write_transaction(self.db):
            catalog.register_release(self.db, release, assets)

    def test_historical_1_3_c_is_used_without_copy(self):
        core = geometry.legacy_core()
        self.assertTrue(Path(core.__file__).samefile(catalog.ROOT / geometry.LEGACY_PATH))
        self.assertTrue(callable(core.geometry))
        self.assertTrue(callable(core.separation))
        self.assertTrue(callable(core.classify_element))

    def test_rotated_bounds_gap_shape_and_signature(self):
        model = {
            "elements": [
                {"from": [0, 0, 0], "to": [2, 2, 2],
                 "faces": {"north": {"texture": "minecraft:block/stone"}}},
                {"from": [2, 0, 0], "to": [4, 2, 2], "faces": {}},
            ]
        }
        path = "assets/sample/models/block/table.json"
        self.register("mod", [self.put(path, json.dumps(model).encode())])
        report = geometry.analyze(self.db, "mod", self.root, path)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["geometry_engine"], "historical_1-3-C")
        self.assertEqual(report["raw_bbox"], [0, 0, 0, 4, 2, 2])
        self.assertEqual(report["rotated_bbox"], [0, 0, 0, 4, 2, 2])
        self.assertEqual(report["elements"][0]["geometry_type"], "SOLID")
        self.assertEqual(report["elements"][0]["nearest_element"], 1)
        self.assertEqual(report["elements"][0]["rotated_aabb_signed_gap"], 0)
        self.assertEqual(len(report["geometry_signature"]), 64)
        self.assertEqual(report["face_count"], 1)

    def test_element_rotation_is_applied_by_1_3_c(self):
        path = "assets/sample/models/block/turn.json"
        model = {"elements": [{
            "from": [0, 0, 0], "to": [4, 2, 6],
            "rotation": {"origin": [0, 0, 0], "axis": "y", "angle": 90},
            "faces": {},
        }]}
        self.register("mod", [self.put(path, json.dumps(model).encode())])
        report = geometry.analyze(self.db, "mod", self.root, path)
        self.assertEqual(report["elements"][0]["raw_bbox"], [0, 0, 0, 4, 2, 6])
        for measured, expected in zip(report["elements"][0]["rotated_bbox"], [0, 0, -4, 6, 2, 0]):
            self.assertAlmostEqual(measured, expected, places=8)

    def test_reject_duplicate_keys_and_nonfinite_rotation(self):
        path = "assets/sample/models/block/invalid.json"
        for body, message in (
            (b'{"elements":[],"elements":[]}', "Duplicate JSON object keys"),
            (b'{"elements":[{"from":[0,0,0],"to":[1,1,1],'
             b'"rotation":{"origin":[0,0,0],"axis":"y","angle":NaN},"faces":{}}]}',
             "Invalid JSON constant"),
        ):
            self.put(path, body)
            with self.assertRaisesRegex(ValueError, message):
                geometry.parse_model(body, path)

    def test_external_vanilla_parent_from_registered_version(self):
        mod = "assets/sample/models/block/chair.json"
        vanilla = "1.21.11/assets/minecraft/models/block/parent.json"
        external = self.root / "vanilla-source"
        mod_asset = self.put(mod, b'{"parent":"minecraft:block/parent"}')
        vanilla_asset = self.put(vanilla, b'{"elements":[{"from":[0,0,0],"to":[16,16,16],'
                                        b'"faces":{"north":{"texture":"minecraft:block/oak_planks","uv":[0,0,16,16]}}}]}',
                                 directory=external)
        # External catalogue entries are indexed by resource ID, not by mod path prefix.
        vanilla_asset["resource_id"] = "minecraft:block/parent"
        self.register("mod", [mod_asset])
        self.register("vanilla", [vanilla_asset], profile="vanilla")
        report = geometry.analyze(self.db, "mod", self.root, mod,
                                  vanilla_release="vanilla", vanilla_source=external)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["element_count"], 1)
        self.assertEqual([r["release_key"] for r in report["model_chain"]], ["mod", "vanilla"])
        self.assertTrue(all(r["catalog_verified"] for r in report["model_chain"]))

    def test_external_parent_requires_version_match(self):
        mod = "assets/sample/models/block/chair.json"
        self.register("mod", [self.put(mod, b'{"parent":"minecraft:block/parent"}')])
        self.register("old-vanilla", [], profile="vanilla", version="1.21.1")
        with self.assertRaisesRegex(ValueError, "version differs"):
            geometry.analyze(self.db, "mod", self.root, mod,
                             vanilla_release="old-vanilla", vanilla_source=self.root)


if __name__ == "__main__":
    unittest.main()
