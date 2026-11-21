"""Original selector/pose mapping audits must not auto-correct unusual sources."""
from collections import Counter
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
import audit_int3_chair_blockstates as state

class BlockstateSourceTests(unittest.TestCase):
    def test_selector_order_not_a_semantic_difference(self):
        self.assertEqual(state.selector_dict("facing=north,variant=3,tucked=false"),
                         state.selector_dict("tucked=false,facing=north,variant=3"))
        with self.assertRaises(ValueError):
            state.selector_dict("facing=north,facing=south")

    def test_variant3_anomaly_preserved_as_review_not_fixed(self):
        labels=[]
        for variant in range(1,4):
            for direction in state.DIRECTIONS:
                model=f"another_furniture:block/chair/acacia_{variant}"
                if variant==3 and direction=="south":
                    model="another_furniture:block/chair/acacia_1"
                labels.append({
                   "source":"AF","selector":f"facing={direction},tucked=false,variant={variant}",
                   "option_index":0,"model_resource_id":model
                })
        review=state.anomalous_variant_groups(labels)
        self.assertEqual(len(review),4)
        self.assertTrue(any(x["selector"].endswith("variant=3") and
                            x["facing"]=="south" and x["source_model"].endswith("acacia_1")
                            for x in review))

    def test_90_degree_rotation_preserves_y_and_closes_360(self):
        p=(1,3,12)
        self.assertEqual(state.rotate_y(p,90),(12,3,15))
        self.assertEqual(state.rotate_y(p,180),(15,3,4))
        self.assertEqual(state.rotate_y(p,360),p)
        q=p
        for _ in range(4):q=state.rotate_y(q,90)
        self.assertEqual(q,p)

    def test_source_model_namespace(self):
        self.assertEqual(state.canonical_target("block/chair","AF"),
                         "another_furniture:block/chair")
        self.assertEqual(state.canonical_target("minecraft:block/oak_planks","HC"),
                         "minecraft:block/oak_planks")
        with self.assertRaises(ValueError):
            state.canonical_target("", "HC")

    def test_bbox_tokens_deterministic(self):
        self.assertEqual(state.bbox_token((1,2,3,4,5,6)),
                         "1.000000|2.000000|3.000000|4.000000|5.000000|6.000000")

    def test_fixed_model_source_229_face_scope(self):
        self.assertEqual(set(state.STUDY_MODEL_KEYS),{"AF121","AF123","HC11210","MACAW67"})
        self.assertEqual(sum(state.EXPECTED_FACE_COUNTS.values()),229)
        self.assertEqual(len(state.BLOCKS),3)

if __name__=="__main__":
    unittest.main()
