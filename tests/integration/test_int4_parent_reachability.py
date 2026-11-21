"""Fail-closed unit checks for INT-4 48-parent static-source reachability."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.integration import audit_int4_parent_reachability as a


class ReachabilityTests(unittest.TestCase):
    def test_pinned_parent_audit_48_record_evidence_unchanged(self):
        root=Path(__file__).resolve().parents[2]
        d=json.loads((root/a.INT4_LOCK).read_text(encoding="utf-8"))
        self.assertEqual(d["observed"]["summary"]["still_missing_exact_parent_targets"],48)
        self.assertEqual(d["observed"]["summary"]["distinct_unresolved_parent_resource_ids"],3)
        self.assertEqual(d["observed"]["summary"]["overlap_with_historical_no_static"],44)
        self.assertFalse(d["boundaries"]["actual_render_missing_model_proved"])

    def test_path_resource_identity_and_namespaces(self):
        self.assertEqual(a.resource("assets/mcwfurnitures/blockstates/oak_desk.json","blockstates"),
                         "mcwfurnitures:oak_desk")
        self.assertEqual(a.resource("assets/another_furniture/models/block/lantern_post_base.json","models"),
                         "another_furniture:block/lantern_post_base")
        with self.assertRaises(a.OriginalMismatch):
            a.resource("assets/another_furniture/textures/block/foo.png","models")
        with self.assertRaises(a.OriginalMismatch):
            a.resource("assets/foo/blockstates/bar.json","models")

    def test_variants_weighted_options_and_multipart(self):
        source={
            "variants":{"facing=north":[{"model":"mcwfurnitures:block/desk/acacia_desk","weight":2},
                                          {"model":"block/drawer/acacia_drawer_base"}]},
            "multipart":[{"when":{"north":"true"},"apply":[
                            {"model":"block/desk/oak_desk"},{"model":"block/desk/spruce_desk"}]}]
        }
        result=a.static_blockstate_targets(source,"mcwfurnitures","fake")
        self.assertEqual(len(result),4)
        self.assertEqual(result[0][1],"mcwfurnitures:block/desk/acacia_desk")
        self.assertEqual(result[1][1],"mcwfurnitures:block/drawer/acacia_drawer_base")
        self.assertEqual(result[-1][2],"multipart")

    def test_model_parent_inheritance_and_source_distinction(self):
        graph={
          "mcwfurnitures:block/desk/acacia_desk":"mcwfurnitures:block/parent/desk",
          "mcwfurnitures:block/parent/desk":"minecraft:block/cube_all",
          "mcwfurnitures:block/drawer/acacia_drawer_base":"mcwfurnitures:block/parent/drawer_base",
        }
        seen=a.transitive_reachable({"mcwfurnitures:block/desk/acacia_desk"},graph)
        self.assertIn("mcwfurnitures:block/parent/desk",seen)
        self.assertIn("minecraft:block/cube_all",seen)
        self.assertNotIn("mcwfurnitures:block/drawer/acacia_drawer_base",seen)
        self.assertEqual(len(a.transitive_reachable(set(),graph)),0)

    def test_parent_cycle_terminates_without_approval(self):
        graph={"a":"b","b":"a"}
        self.assertEqual(a.transitive_reachable({"a"},graph),{"a","b"})

    def test_item_model_roots_are_separate_from_blockstate_roots(self):
        doc={"model":{
          "type":"minecraft:condition","on_true":{"type":"minecraft:model","model":"mcwfurnitures:item/chair"},
          "on_false":{"type":"minecraft:model","model":"item/fallback"}}}
        self.assertEqual(set(a.item_definition_model_roots(doc,"mcwfurnitures")),
                         {"mcwfurnitures:item/chair","mcwfurnitures:item/fallback"})

    def test_resource_paths_without_namespace_are_safely_inferred(self):
        self.assertEqual(a.normalized_ref("lantern","minecraft"),"minecraft:lantern")
        self.assertEqual(a.normalized_ref("block/parent/desk","mcwfurnitures"),
                         "mcwfurnitures:block/parent/desk")
        for x in ("","../escape","/absolute"):
            with self.assertRaises(a.OriginalMismatch):
                a.normalized_ref(x,"mcwfurnitures")

    def test_blockstate_missing_model_and_empty_selection_rejected(self):
        with self.assertRaisesRegex(a.OriginalMismatch,"Missing model"):
            a.static_blockstate_targets({"variants":{"facing=north":{"x":90}}},"other","bad")
        with self.assertRaisesRegex(a.OriginalMismatch,"no traversable"):
            a.static_blockstate_targets({"variants":{}},"other","empty")


if __name__=="__main__":
    unittest.main()
