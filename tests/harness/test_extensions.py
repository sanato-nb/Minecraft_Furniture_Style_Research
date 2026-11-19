from contextlib import closing
from importlib.util import find_spec
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from mcfr import ai_review, cross_research, extensions, research_db as catalog
from mcfr import research_engine as engine, update_watch, visual_check


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(self.enterContext(TemporaryDirectory()))
        path = self.work / "research.sqlite"
        catalog.initialize(path)
        self.db = self.enterContext(closing(catalog.open_db(path, "rw")))

    def test_mod_watch_filters_and_records_only_changes(self):
        def release(ident, day, *, game="1.21.11", loader="fabric", channel="release"):
            return {
                "id": ident, "version_number": f"3.4.{day}", "date_published": f"2026-01-{day:02}T00:00:00Z",
                "version_type": channel, "game_versions": [game], "loaders": [loader],
                "files": [{"filename": "fixture.jar", "hashes": {"sha512": "a" * 128}, "primary": True, "size": 20}],
            }

        first = [release("match", 1), release("beta", 9, channel="beta"),
                 release("other-game", 5, game="1.21.1"), release("forge", 6, loader="forge")]
        def check(rows):
            provider = Mock(return_value=rows)
            result = update_watch.check(self.db, "dtWC90iB", "1.21.11", "fabric", load=provider)
            self.assertIn("/dtWC90iB/version?", provider.call_args.args[0])
            return result

        self.assertEqual(check(first)["latest"]["id"], "match")
        self.assertEqual(check(first)["status"], "UNCHANGED")
        newer = [release("new", 2), *first]
        self.assertEqual(check(newer)["status"], "UPDATE_DETECTED")
        self.assertEqual(check(first)["status"], "OLDER_FEED")
        self.assertEqual(check(newer)["status"], "UNCHANGED")
        self.assertEqual(self.db.execute("SELECT count(*) FROM upstream_observation").fetchone()[0], 2)

    def test_vanilla_has_separate_stable_channel(self):
        feed = {"latest": {"release": "1.21.11", "snapshot": "snapshot"}, "versions": [
            {"id": "snapshot", "type": "snapshot"},
            {"id": "1.21.11", "type": "release", "releaseTime": "2026-01-01T00:00:00Z",
             "url": "https://example.invalid/manifest", "sha1": "a" * 40},
        ]}
        observed = update_watch.check(self.db, "vanilla", load=lambda _: feed)
        self.assertEqual(observed["status"], "BASELINE")
        self.assertEqual(observed["latest"]["id"], "1.21.11")

    def test_batch_watch_continues_after_feed_error_and_checks_duplicates_first(self):
        mod = {"target": "adorn", "game_version": "1.21.11", "loader": "fabric"}
        targets = [mod, {"target": "vanilla"}]
        feed = {"latest": {"release": "1.21.11"}, "versions": [
            {"id": "1.21.11", "type": "release", "releaseTime": "2026-01-01T00:00:00Z",
             "url": "https://example.invalid/manifest", "sha1": "a" * 40},
        ]}
        provider = Mock()
        with self.assertRaisesRegex(ValueError, "Duplicate watch target"):
            update_watch.check_many(self.db, [*targets, {**mod, "loader": "FABRIC"}], load=provider)
        provider.assert_not_called()

        for expected in ("BASELINE", "UNCHANGED"):
            provider.side_effect = [TimeoutError("upstream timed out"), feed]
            result = update_watch.check_many(self.db, targets, load=provider)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["updates_detected"], 0)
            self.assertEqual([row["status"] for row in result["targets"]], ["ERROR", expected])
            self.assertEqual(result["targets"][0]["error"], "upstream timed out")
        self.assertEqual(self.db.execute("SELECT count(*) FROM upstream_observation").fetchone()[0], 1)

    def verified(self, name, target, body, mode="REVALIDATE"):
        path = f"{name}.json"
        (self.work / path).write_bytes(body)
        release = {
            "release_key": name, "profile": "mods", "target_id": target, "version": "1",
            "minecraft_version": "1.21.11", "loader": "fabric", "pin_algorithm": "SHA256",
            "pin_digest": "a" * 64, "source": "test fixture",
        }
        with catalog.write_transaction(self.db):
            catalog.register_release(self.db, release, [{
                "source_path": path, "kind": "model", "resource_id": f"{target}:block/chair",
                "hash_algorithm": "SHA256", "digest": engine.asset_digest(body, "SHA256"),
            }])
            catalog.create_run(self.db, name, name, mode, None)
        plan = engine.plan_run(self.db, name)
        return engine.record_execution(self.db, plan, "source", engine.verify_source(plan, self.work))["execution_id"]

    def test_cross_research_and_coverage_use_verified_scope(self):
        left = self.verified("left", "first", b'{"elements":[]}')
        right = self.verified("right", "second", b'{"elements":[{}]}')
        result = cross_research.compare(self.db, left, right)
        self.assertEqual(result["shared_profiles"], 1)
        self.assertEqual(result["profiles"], [{"kind": "model", "observation": {"top_level_keys": ["elements"]},
                                               "left": 1, "right": 1}])
        self.assertEqual(extensions.coverage(self.db, "left")["total"]["verified_percent"], 100)
        with self.assertRaisesRegex(ValueError, "different targets"):
            cross_research.compare(self.db, left, left)

    def test_reuse_matches_scope_and_preserves_fresh_independence(self):
        execution = self.verified("left", "first", b'{"elements":[]}')
        different = self.verified("other", "other", b'{"elements":[]}')
        fresh = self.verified("fresh", "fresh", b'{"elements":[]}', mode="FRESH")
        provider = Mock(return_value={
            "id": "resp_fixture", "status": "completed", "output": [],
            "usage": {"input_tokens": 20, "output_tokens": 3, "total_tokens": 23},
        })

        def review(name, origin, reuse=True):
            prepared = ai_review.prepare(self.db, name, origin, "test-model", 64, [])
            return ai_review.dispatch(self.db, name, prepared["approval_sha256"],
                                      reuse_identical=reuse, send=provider)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "fixture"}):
            review("original", execution)
            self.assertEqual(review("cached", execution)["reused_from"], "original")
            self.assertNotIn("reused_from", review("different", different))
            review("fresh-original", fresh)
            self.assertNotIn("reused_from", review("fresh-after", fresh))
        self.assertEqual(provider.call_count, 4)
        totals = extensions.usage(self.db)["models"]["test-model"]
        self.assertEqual(totals["cache_hits"], 1)
        self.assertEqual(totals["total_tokens"], 92)

    @unittest.skipUnless(find_spec("PIL"), "Pillow is required for visual comparisons")
    def test_real_reference_and_alpha_only_change(self):
        from PIL import Image

        reference = catalog.ROOT / "project/audits/runtime/macaws-furniture.png"
        audit = json.loads(reference.with_name("REPLAY_AUDIT.json").read_text())
        digest = audit["captures"][reference.name]["sha256"]
        self.assertEqual(visual_check.compare(reference, reference, reference_sha256=digest)["changed_pixels"], 0)
        modified = self.work / "modified.png"
        with Image.open(reference) as source:
            rgba = source.convert("RGBA")
        pixel = rgba.getpixel((8, 12))
        rgba.putpixel((8, 12), (*pixel[:3], pixel[3] ^ 1))
        rgba.save(modified)
        difference = visual_check.compare(reference, modified, reference_sha256=digest)
        self.assertEqual(difference["changed_pixels"], 1)
        self.assertEqual(difference["difference_box"], [8, 12, 9, 13])
        with self.assertRaisesRegex(ValueError, "pinned SHA-256"):
            visual_check.compare(reference, modified, reference_sha256="a" * 64)
