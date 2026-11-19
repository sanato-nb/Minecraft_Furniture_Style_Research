from contextlib import closing, redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from mcfr import research_db as catalog, research_engine as engine


class ResearchEngineTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(self.enterContext(TemporaryDirectory()))
        self.path = self.work / "catalog.sqlite"
        catalog.initialize(self.path)
        self.db = self.enterContext(closing(catalog.open_db(self.path, "rw")))

    def command(self, *args, code=0):
        output = StringIO()
        with redirect_stdout(output):
            actual = engine.main(["--db", str(self.path), *args])
        self.assertEqual(actual, code)
        return json.loads(output.getvalue())

    def register(self, key, files, pin="a" * 64):
        release = {
            "release_key": key, "profile": "mods", "target_id": "example", "version": key,
            "minecraft_version": "1.21.11", "loader": "fabric", "pin_algorithm": "SHA256",
            "pin_digest": pin, "source": "test fixture",
        }
        catalog.register_release(self.db, release, [{
            "source_path": name, "kind": "model", "resource_id": f"example:block/{Path(name).stem}",
            "hash_algorithm": "SHA256", "digest": hashlib.sha256(raw).hexdigest(),
        } for name, raw in files.items()])

    def test_incremental_directory_attempts_keep_success_and_failure(self):
        source = self.work / "source"
        source.mkdir()
        with catalog.write_transaction(self.db):
            self.register("old", {"same.json": b"{}", "changed.json": b"{}", "removed.json": b"{}"})
            self.register("new", {"same.json": b"{}", "changed.json": b'{"elements":[]}', "added.json": b"{}"})
            catalog.create_run(self.db, "diff", "new", "INCREMENTAL", "old")
            catalog.create_run(self.db, "repeat", "new", "INCREMENTAL", "old")
        plan = self.command("plan", "diff", "--details")
        self.assertEqual(plan["counts"], {"all": 0, "added": 1, "changed": 1, "unchanged": 1, "removed": 1})
        self.assertEqual(plan["removed"], ["removed.json"])
        self.assertEqual([asset["source_path"] for asset in plan["selected"]], ["added.json", "changed.json"])
        self.assertEqual(self.command("plan", "repeat")["scope_sha256"], plan["scope_sha256"])

        (source / "added.json").write_bytes(b"{}")
        (source / "changed.json").write_bytes(b"{}")
        failed = self.command("execute", "diff", "--source", str(source), code=1)
        self.assertEqual(failed["report"]["failed"], 1)
        (source / "changed.json").write_bytes(b'{"elements":[]}')
        successful = self.command("execute", "diff", "--source", str(source))
        self.assertEqual(successful["report"]["verified"], 2)
        attempts = self.command("show", "diff", "--details")
        self.assertEqual({entry["status"] for entry in attempts}, {"PASS", "FAIL"})
        self.assertEqual({entry["scope_sha256"] for entry in attempts}, {plan["scope_sha256"]})
        details = next(entry["report"] for entry in attempts if entry["status"] == "PASS")
        self.assertEqual(details["assets"][1]["observations"], {"top_level_keys": ["elements"]})

    def test_archive_pin_and_fresh_scope(self):
        archive = self.work / "source.jar"
        with ZipFile(archive, "w") as output:
            output.writestr("a.json", "{}")
        with catalog.write_transaction(self.db):
            self.register("fixed", {"a.json": b"{}"}, hashlib.sha256(archive.read_bytes()).hexdigest())
            catalog.create_run(self.db, "fresh", "fixed", "FRESH", None)
        run = self.command("execute", "fresh", "--source", str(archive))
        self.assertEqual(run["report"]["pin_check"], "archive_and_asset_hashes")
        with archive.open("ab") as output:
            output.write(b"changed")
        failed = self.command("execute", "fresh", "--source", str(archive), code=1)
        self.assertIn("differs from the registered release pin", failed["report"]["error"])

    def test_upgrade_preserves_a_version_1_run(self):
        old = self.work / "old.sqlite"
        with closing(catalog.open_db(old, "rwc")) as db, catalog.write_transaction(db):
            catalog.apply_schema(db, "research_schema.sql")
            db.execute(f"PRAGMA application_id = {catalog.APP_ID}")
            db.execute("PRAGMA user_version = 1")
            db.execute("INSERT INTO release VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       ("old", "vanilla", "minecraft", "1", "1", "vanilla", "SHA256", "a" * 64, "fixture"))
            run = catalog.create_run(db, "from-v1", "old", "REVALIDATE", None)
            self.assertEqual(catalog.summary(db)["schema_version"], 1)
        catalog.initialize(old)
        catalog.initialize(old)
        with closing(catalog.open_db(old, "ro")) as db:
            catalog.require_schema(db, minimum=2)
            self.assertEqual(catalog.summary(db)["runs"], [run])
            self.assertEqual(engine.read_executions(db, "from-v1"), [])
