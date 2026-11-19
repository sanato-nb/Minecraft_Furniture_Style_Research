from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from mcfr import ai_review, research_db as catalog, research_engine as engine, source_jobs


class ResearchWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(self.enterContext(TemporaryDirectory()))
        self.path = self.work / "research.sqlite"
        catalog.initialize(self.path)
        self.db = self.enterContext(closing(catalog.open_db(self.path, "rw")))
        self.release = {
            "release_key": "fixture", "profile": "mods", "target_id": "test", "version": "1",
            "minecraft_version": "1.21.11", "loader": "fabric", "pin_algorithm": "SHA256",
            "pin_digest": "a" * 64, "source": "fixture",
        }

    def add_files(self, start, stop):
        entries = []
        for index in range(start, stop):
            path = f"chair-{index:03}.json"
            body = b'{"elements":[]}'
            (self.work / path).write_bytes(body)
            entries.append({
                "source_path": path, "kind": "model", "resource_id": f"test:chair_{index}",
                "hash_algorithm": "SHA256", "digest": hashlib.sha256(body).hexdigest(),
            })
        with catalog.write_transaction(self.db):
            catalog.register_release(self.db, self.release, entries)
            catalog.create_run(self.db, "run", "fixture", "FRESH", None)

    def test_interruption_and_resume_after_reopening_database(self):
        self.add_files(0, 66)
        verify = engine.verify_entry

        def interrupt(entry, read):
            if entry["source_path"] == "chair-065.json":
                raise KeyboardInterrupt
            return verify(entry, read)

        with patch.object(engine, "verify_entry", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                source_jobs.scan(self.db, "job", "run", self.work)
        self.assertEqual(source_jobs.status(self.db, "job")["next_asset"], 64)
        self.assertEqual(engine.read_executions(self.db, "run"), [])

        def pending_only(entry, read):
            self.assertIn(entry["source_path"], {"chair-064.json", "chair-065.json"})
            return verify(entry, read)

        with closing(catalog.open_db(self.path, "rw")) as reopened:
            with patch.object(engine, "verify_entry", side_effect=pending_only) as verification:
                final = source_jobs.scan(reopened, "job", "run", self.work)
                self.assertEqual(verification.call_count, 2)
            self.assertEqual(final["status"], "PASS")
            self.assertEqual(source_jobs.scan(reopened, "job", "run", self.work), final)
        self.assertEqual(engine.read_executions(self.db, "run")[0]["report"]["verified"], 66)
        self.assertEqual(self.db.execute("SELECT count(*) FROM source_checkpoint").fetchone()[0], 0)

    def test_checkpoint_refuses_changed_catalog_scope(self):
        self.add_files(0, 2)
        self.assertEqual(source_jobs.scan(self.db, "job", "run", self.work, 1)["status"], "PENDING")
        self.add_files(2, 3)
        with self.assertRaisesRegex(ValueError, "saved scope"):
            source_jobs.scan(self.db, "job", "run", self.work)
        self.assertEqual(source_jobs.status(self.db, "job")["next_asset"], 1)

    def test_approval_binds_payload_and_blocks_duplicate_delivery(self):
        self.add_files(0, 2)
        execution = source_jobs.scan(self.db, "job", "run", self.work)["execution_id"]
        asset = "chair-000.json"
        with self.assertRaisesRegex(ValueError, "verified execution"):
            ai_review.prepare(self.db, "foreign", execution, "fixture-model", 64, ["other.json"])
        with self.assertRaisesRegex(ValueError, "Output token"):
            ai_review.prepare(self.db, "oversize", execution, "fixture-model", 3000, [])
        review = ai_review.prepare(self.db, "review", execution, "fixture-model", 64, [asset])
        digest = review["approval_sha256"]
        sent = []

        def provider(body, key):
            sent.append(json.loads(body))
            self.assertEqual(key, "fixture-token")
            with closing(catalog.open_db(self.path, "rw")) as concurrent:
                with self.assertRaisesRegex(ValueError, "claimed or sent"):
                    ai_review.dispatch(concurrent, "review", digest, send=provider)
            return {"id": "resp_fixture", "status": "completed", "output": [
                {"type": "message", "content": [{"type": "output_text", "text": "An inference."}]}
            ], "usage": {"input_tokens": 23, "output_tokens": 3}}

        with patch.dict(os.environ, {"OPENAI_API_KEY": "fixture-token"}):
            with self.assertRaisesRegex(ValueError, "Approval digest"):
                ai_review.dispatch(self.db, "review", "wrong", send=provider)
            self.assertFalse(sent)
            complete = ai_review.dispatch(self.db, "review", digest, send=provider)
            with self.assertRaisesRegex(ValueError, "claimed or sent"):
                ai_review.dispatch(self.db, "review", digest, send=provider)
        self.assertEqual(sent, [review["request"]])
        self.assertFalse(sent[0]["store"])
        self.assertEqual(json.loads(sent[0]["input"])["observations"][0]["source_path"], asset)
        self.assertNotIn("chair-001.json", sent[0]["input"])
        self.assertEqual(complete["state"], "COMPLETE")
        self.assertEqual(complete["result"]["evidence_class"], "AI_INFERENCE")
        self.assertEqual(engine.read_executions(self.db, "run")[0]["status"], "PASS")

    def test_unconfirmed_provider_call_is_not_retried(self):
        self.add_files(0, 1)
        execution = source_jobs.scan(self.db, "job", "run", self.work)["execution_id"]
        review = ai_review.prepare(self.db, "review", execution, "fixture-model", 64, [])

        def timeout(body, key):
            raise TimeoutError("fixture request may have been received")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "fixture-token"}):
            result = ai_review.dispatch(self.db, "review", review["approval_sha256"], send=timeout)
            self.assertEqual(result["state"], "UNCONFIRMED")
            with self.assertRaisesRegex(ValueError, "claimed or sent"):
                ai_review.dispatch(self.db, "review", review["approval_sha256"], send=timeout)
