from contextlib import closing
import hashlib
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from mcfr import legacy_catalog, research_db


class ResearchDatabaseTests(unittest.TestCase):
    def setUp(self):
        work = self.enterContext(TemporaryDirectory())
        self.path = Path(work) / "research #1.sqlite"
        research_db.initialize(self.path)
        self.db = self.enterContext(closing(research_db.open_db(self.path, "rw")))
        research_db.require_schema(self.db)

    def test_legacy_catalog_import_is_idempotent_and_read_only(self):
        root = research_db.ROOT
        catalog = {
            "minecraft-java-1.21.11-git": {"model": 2390, "blockstate": 1168, "texture": 1111, "texture_sidecar": 99},
            "another-furniture-4.0.3-git": {"model": 1629, "blockstate": 177, "texture": 1188},
            "handcrafted-4.0.3-git": {"model": 12394, "blockstate": 267, "texture": 965},
            "macaws-furniture-3.4.2-fabric": {"model": 2549, "blockstate": 714, "texture": 20, "item_definition": 716},
        }
        tracked_evidence = [
            *legacy_catalog.DATABASES.values(),
            legacy_catalog.MOD_F / "1-3_TEXTURE_UV_HANDOFF.csv",
            legacy_catalog.VANILLA_FINAL / "G_FINAL_SOURCE_SHA_4669.csv",
        ]
        before = [(path, hashlib.sha256((root / path).read_bytes()).digest()) for path in tracked_evidence]
        with research_db.write_transaction(self.db):
            first = legacy_catalog.import_catalog(self.db, root, research_db.register_release)
        with research_db.write_transaction(self.db):
            repeat = legacy_catalog.import_catalog(self.db, root, research_db.register_release)
        self.assertEqual(first["assets_added"], 25387)
        self.assertEqual(repeat["assets_added"], 0)
        summary = research_db.summary(self.db)
        self.assertEqual({row["release_key"]: row["assets_by_kind"] for row in summary["releases"]}, catalog)
        self.assertEqual(summary["runs"], [])
        for name in legacy_catalog.DATABASES:
            with self.subTest(name=name):
                info = legacy_catalog.database_info(root, name)
                self.assertEqual(info["integrity"], "ok")
                self.assertTrue(info["tables"])
        for path, digest in before:
            self.assertEqual(hashlib.sha256((root / path).read_bytes()).digest(), digest)
        self.assertEqual(self.db.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_research_modes_and_retry(self):
        previous = self.release("old", "example", "1.0")
        current = self.release("new", "example", "2.0")
        another = self.release("other", "another_example", "1.0")
        with research_db.write_transaction(self.db):
            for version in (previous, current, another):
                research_db.register_release(self.db, version, [])
            for mode in ("NEW", "REVALIDATE", "FRESH"):
                self.assertIsNone(research_db.create_run(self.db, mode, "new", mode, None)["baseline_release_key"])
            intended = research_db.create_run(self.db, "diff", "new", "INCREMENTAL", "old")
            self.assertEqual(research_db.create_run(self.db, "diff", "new", "INCREMENTAL", "old"), intended)
        with self.assertRaisesRegex(ValueError, "same profile and target"), research_db.write_transaction(self.db):
            research_db.create_run(self.db, "wrong-target", "new", "INCREMENTAL", "other")
        with self.assertRaisesRegex(ValueError, "Only INCREMENTAL"), research_db.write_transaction(self.db):
            research_db.create_run(self.db, "fresh-with-baseline", "new", "FRESH", "old")
        with self.assertRaisesRegex(ValueError, "Conflicting metadata"), research_db.write_transaction(self.db):
            research_db.create_run(self.db, "diff", "new", "FRESH", None)

    def test_failed_batch_rolls_back_earlier_writes(self):
        release = self.release("old", "example", "1.0")
        asset = {
            "source_path": "assets/example/models/block/chair.json", "kind": "model",
            "resource_id": "example:block/chair", "hash_algorithm": "SHA256", "digest": "a" * 64,
        }
        invalid = {**asset, "source_path": "assets/example/models/block/table.json", "digest": "broken"}
        with self.assertRaises(sqlite3.IntegrityError), research_db.write_transaction(self.db):
            research_db.register_release(self.db, release, [asset, invalid])
        self.assertEqual(research_db.summary(self.db)["releases"], [])
        with research_db.write_transaction(self.db):
            self.assertEqual(research_db.register_release(self.db, release, [asset]), 1)
        with self.assertRaisesRegex(ValueError, "Conflicting asset"), research_db.write_transaction(self.db):
            research_db.register_release(self.db, release, [{**asset, "digest": "b" * 64}])

    def test_init_rejects_other_sqlite_and_query_mode_is_read_only(self):
        other = self.path.with_name("old.sqlite")
        with closing(sqlite3.connect(other)) as db:
            db.execute("CREATE TABLE evidence (original TEXT)")
        before = other.read_bytes()
        with self.assertRaisesRegex(ValueError, "another application"):
            research_db.initialize(other)
        self.assertEqual(other.read_bytes(), before)
        research_db.initialize(self.path)
        with closing(research_db.open_db(self.path, "ro")) as db:
            with self.assertRaises(sqlite3.OperationalError):
                db.execute("CREATE TABLE accidental_write (id INTEGER)")

    @staticmethod
    def release(key, target, version):
        return {
            "release_key": key, "profile": "mods", "target_id": target, "version": version,
            "minecraft_version": "1.21.11", "loader": "fabric", "pin_algorithm": "SHA256",
            "pin_digest": "0" * 64, "source": "example release",
        }
