"""Focused regression coverage for the H2-H4 audit fixes."""
from contextlib import closing
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from mcfr import handoff, model_analysis, policy, research_db as catalog


class EnhancedModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = self.enterContext(TemporaryDirectory())
        self.root = Path(self.temp)
        self.db_path = self.root / "input.sqlite"
        catalog.initialize(self.db_path)
        self.db = self.enterContext(closing(catalog.open_db(self.db_path, "rw")))
        self.paths = {}

    def model(self, name, content):
        path = f"assets/minecraft/models/block/{name}.json"
        body = json.dumps(content).encode()
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        self.paths[path] = body
        return path

    def register(self, names=None):
        release = {"release_key": "vanilla", "profile": "vanilla", "target_id": "minecraft",
                   "version": "test", "minecraft_version": "1.21.11", "loader": "vanilla",
                   "pin_algorithm": "GIT_COMMIT_SHA1", "pin_digest": "b" * 40, "source": "fixture"}
        names = list(self.paths) if names is None else names
        assets = [{"source_path": path, "kind": "model", "resource_id": "minecraft:block/" + Path(path).stem,
                   "hash_algorithm": "SHA256", "digest": hashlib.sha256(self.paths[path]).hexdigest()}
                  for path in names]
        with catalog.write_transaction(self.db):
            catalog.register_release(self.db, release, assets)

    def test_parent_chain_geometry_and_texture_alias(self):
        parent = self.model("parent", {
            "textures": {"body": "minecraft:block/oak_planks"},
            "elements": [{"from": [0, 1, 0], "to": [16, 15, 16],
                          "rotation": {"origin": [8, 8, 8], "axis": "y", "angle": 22.5},
                          "faces": {"north": {"uv": [0, 1, 16, 15], "texture": "#body", "rotation": 90}}}],
        })
        child = self.model("chair", {"parent": "minecraft:block/parent", "textures": {"body": "#replacement", "replacement": "minecraft:block/spruce_planks"}})
        self.register()
        report = model_analysis.analyze(self.db, "vanilla", self.root, child)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual([row["path"] for row in report["model_chain"]], [child, parent])
        self.assertEqual(report["element_count"], 1)
        face = report["elements"][0]["faces"]["north"]
        self.assertEqual(face["resolved_texture"], "minecraft:block/spruce_planks")
        self.assertEqual(face["uv"], [0, 1, 16, 15])
        self.assertEqual(face["rotation"], 90)
        self.assertTrue(all(row["catalog_verified"] for row in report["model_chain"]))

    def test_parent_cycle_and_missing_alias_are_partial(self):
        root = self.model("a", {"parent": "minecraft:block/b", "textures": {"x": "#missing"}})
        self.model("b", {"parent": "minecraft:block/a",
                         "elements": [{"from": [0, 0, 0], "to": [16, 16, 16],
                                       "faces": {"north": {"texture": "#x"}}}]})
        self.register()
        report = model_analysis.analyze(self.db, "vanilla", self.root, root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertIn("parent_cycle", [r["kind"] for r in report["issues"]])
        self.assertIn("unresolved_texture", [r["kind"] for r in report["issues"]])

    def test_directory_uncatalogued_parent_marked_partial(self):
        root = self.model("a", {"parent": "minecraft:block/b"})
        self.model("b", {"elements": [{"from": [0, 0, 0], "to": [1, 1, 1], "faces": {}}]})
        self.register([root])
        report = model_analysis.analyze(self.db, "vanilla", self.root, root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertIn("uncatalogued_parent", [x["kind"] for x in report["issues"]])

    def test_root_hash_drift_refused(self):
        root = self.model("chair", {"elements": []})
        self.register()
        (self.root / root).write_text('{"elements":[1]}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Catalog hash mismatch"):
            model_analysis.analyze(self.db, "vanilla", self.root, root)

    def test_pinned_archive_with_external_parent_is_partial(self):
        root = self.model("chair", {"parent": "minecraft:block/unbundled"})
        body = self.paths[root]
        archive = self.root / "example.jar"
        with ZipFile(archive, "w") as z:
            z.writestr(root, body)
        self.db.execute("DELETE FROM release")
        # The uncommitted fixture registration is not needed until the real archive pin is known.
        self.db.commit()
        release = {"release_key": "archive", "profile": "mods", "target_id": "test",
                   "version": "test", "minecraft_version": "1.21.11", "loader": "fabric",
                   "pin_algorithm": "SHA256", "pin_digest": hashlib.sha256(archive.read_bytes()).hexdigest(),
                   "source": "fixture"}
        asset = {"source_path": root, "kind": "model", "resource_id": "minecraft:block/chair",
                 "hash_algorithm": "SHA256", "digest": hashlib.sha256(body).hexdigest()}
        with catalog.write_transaction(self.db):
            catalog.register_release(self.db, release, [asset])
        report = model_analysis.analyze(self.db, "archive", archive, root)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["source_pin"], "archive_and_asset_hashes")
        self.assertIn("missing_or_external_parent", [x["kind"] for x in report["issues"]])


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = self.enterContext(TemporaryDirectory())
        self.root = Path(self.temp)
        self.db = self.root / "original.sqlite"
        catalog.initialize(self.db)

    def test_export_verify_restore_round_trip(self):
        folder = self.root / "handoff"
        result = handoff.export(self.db, folder)
        self.assertEqual(result["status"], "EXPORTED")
        self.assertEqual(handoff.verify(folder)["status"], "VERIFIED")
        dest = self.root / "restored.sqlite"
        self.assertEqual(handoff.restore(folder, dest)["status"], "RESTORED")
        self.assertEqual(handoff.db_checks(self.db), handoff.db_checks(dest))
        with self.assertRaises(FileExistsError):
            handoff.restore(folder, dest)

    def test_handoff_detects_corruption_and_stops_restore(self):
        folder = self.root / "handoff"
        handoff.export(self.db, folder)
        with (folder / "research.sqlite").open("ab") as file:
            file.write(b"tampered")
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            handoff.verify(folder)
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            handoff.restore(folder, self.root / "new.sqlite")
        self.assertFalse((self.root / "new.sqlite").exists())


class PolicyTests(unittest.TestCase):
    def test_registration_evidence_is_required_and_checked(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harness/shared").mkdir(parents=True)
            (root / "harness/shared/config.json").write_text(
                '{"require_evidence":true,"ai_api_enabled":false}', encoding="utf-8")
            manifest = {"release": {}, "assets": [{"source_path": "foo.json"}]}
            with self.assertRaisesRegex(ValueError, "requires an evidence_path"):
                policy.check_registration(manifest, root)
            (root / "proof.md").write_text("source reviewed", encoding="utf-8")
            fixed = policy.check_registration({**manifest, "evidence_path": "proof.md"}, root)
            self.assertEqual(fixed["assets"][0]["evidence_path"], "proof.md")
            with self.assertRaisesRegex(ValueError, "outside repository"):
                policy.check_registration({**manifest, "evidence_path": "../secret.txt"}, root)

    def test_api_is_default_off_and_requires_opt_in(self):
        with patch.object(policy, "configuration", return_value={
            "require_evidence": True, "ai_api_enabled": False,
        }):
            with self.assertRaisesRegex(ValueError, "disabled"):
                policy.require_api_permission()
            policy.require_api_permission(explicitly_approved=True)


if __name__ == "__main__":
    unittest.main()
