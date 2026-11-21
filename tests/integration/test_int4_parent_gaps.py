"""INT-4 48 parent-gaps chain audit regression tests, stdlib only.

Synthetic model bodies test reference traversal; the real workflow separately
opens immutable upstream archives and verifies all 48 source byte hashes.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

from scripts.integration import audit_int4_parent_gaps as a


class MiniArchive:
    def __init__(self,mapping):
        self.mapping=mapping
    def find(self,mod,resource):
        return self.mapping.get((mod,resource))
    def maybe_basename(self,mod,resource):
        return ["assets/example/models/block/desk.json"]


class ParentGapAuditTests(unittest.TestCase):
    def test_historical_48_and_108_scope_and_no_duplicates(self):
        root=Path(__file__).resolve().parents[2]
        d=json.loads((root/a.SUM).read_text())
        roster=d["exceptions"]["missing_parent_paths"]
        hashes,nonstatic=a.check_history(root,roster)
        self.assertEqual(len(roster),48)
        self.assertEqual(len(nonstatic),108)
        self.assertEqual(len(set(roster)&nonstatic),44)
        self.assertEqual(sum(x.startswith("another_furniture:") for x in roster),4)
        self.assertEqual(sum(x.startswith("mcwfurnitures:") for x in roster),44)
        self.assertEqual(len(hashes),2)

    def test_original_source_model_pin_index_population(self):
        root=Path(__file__).resolve().parents[2]
        index,sha=a.collect_model_pins(root)
        self.assertEqual(len(index),1629+2549)
        self.assertIn("assets/mcwfurnitures/models/block/desk/acacia_desk.json",index)
        self.assertIn("assets/another_furniture/models/block/lantern_post_base.json",index)
        self.assertEqual(len(sha),2)

    def test_af_minecraft_missing_parent_preserves_own_elements(self):
        body=json.dumps({
            "parent":"minecraft:block/lantern",
            "elements":[{"from":[0,0,0],"to":[1,1,1],"faces":{"north":{"texture":"#all"}}}]
        }).encode()
        z=MiniArchive({("AF","another_furniture:block/lantern_post_base"):body})
        report=a.resolve_one("AF","another_furniture:block/lantern_post_base",z)
        self.assertEqual(report["terminal_status"],"PARENT_MISSING")
        self.assertEqual(report["terminal_ref"],"minecraft:block/lantern")
        self.assertEqual(report["chain"][0]["own_elements"],1)
        self.assertEqual(report["chain"][0]["own_faces"],1)
        self.assertEqual(report["chain"][0]["sha"],a.sha1blob(body))

    def test_macaw_shared_missing_parent_keeps_no_static(self):
        child=json.dumps({"parent":"mcwfurnitures:block/parent/desk","textures":{"0":"a:b"}}).encode()
        z=MiniArchive({("MACAW","mcwfurnitures:block/desk/acacia_desk"):child})
        report=a.resolve_one("MACAW","mcwfurnitures:block/desk/acacia_desk",z)
        self.assertEqual(report["terminal_ref"],"mcwfurnitures:block/parent/desk")
        self.assertEqual(report["terminal_status"],"PARENT_MISSING")
        self.assertEqual(report["chain"][0]["own_elements"],0)
        self.assertNotIn("assets/example",report["terminal_ref"])

    def test_valid_chain_does_not_claim_missing_parent(self):
        z=MiniArchive({
          ("MACAW","mcwfurnitures:block/drawer/acacia_drawer_base"):
            b'{"parent":"mcwfurnitures:block/parent/drawer_base"}',
          ("MACAW","mcwfurnitures:block/parent/drawer_base"):
            b'{"elements":[{"from":[0,0,0],"to":[1,1,1]}]}'
        })
        report=a.resolve_one("MACAW","mcwfurnitures:block/drawer/acacia_drawer_base",z)
        self.assertEqual(report["terminal_status"],"ROOT")
        self.assertEqual(len(report["chain"]),2)

    def test_parent_cycle_detected(self):
        z=MiniArchive({
            ("MACAW","mcwfurnitures:block/foo"):b'{"parent":"mcwfurnitures:block/bar"}',
            ("MACAW","mcwfurnitures:block/bar"):b'{"parent":"mcwfurnitures:block/foo"}',
        })
        doc=a.resolve_one("MACAW","mcwfurnitures:block/foo",z)
        self.assertEqual(doc["terminal_status"],"PARENT_CYCLE")

    def test_source_json_duplicate_keys_rejected(self):
        with self.assertRaisesRegex(a.OriginalMismatch,"Duplicate key"):
            a.parse_json(b'{"parent":"one","parent":"two"}',"duplicate")

    def test_invalid_model_name_rejected(self):
        with self.assertRaisesRegex(a.OriginalMismatch,"Malformed"):
            a.model_rel("mcwfurnitures:block/../../danger")
        with self.assertRaisesRegex(a.OriginalMismatch,"Malformed"):
            a.model_rel("model_without_namespace")

    def test_no_parent_substitution_or_license_approval_sneaks_in(self):
        root=Path(__file__).resolve().parents[2]
        original=json.loads((root/a.SUM).read_text())
        bad=list(original["exceptions"]["missing_parent_paths"])
        bad.pop()
        with self.assertRaisesRegex(a.OriginalMismatch,"48 missing parent"):
            a.check_history(root,bad)


if __name__=="__main__":
    unittest.main()
