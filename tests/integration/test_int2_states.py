"""Unit tests for independent source state-domain enumeration."""
import runpy
from pathlib import Path
import unittest

f = runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/integration/audit_int2_states.py"))
accumulate=f["accumulate"]
is_match=f["is_match"]
compute_cases=f["compute_cases"]
historical_options=f["historical_options"]
historical_hits=f["historical_hits"]
parse_json=f["parse_json"]


class StateExpansionTests(unittest.TestCase):
    def test_variant_alternative_options(self):
        model={
            "variants": {
                "facing=north": [{"model": "minecraft:block/chair", "weight": 2},
                                 {"model": "minecraft:block/chair_alt", "y": 90}],
                "": {"model": "minecraft:block/default"},
            }
        }
        result=compute_cases("1.21.11/assets/minecraft/blockstates/example.json",model)
        self.assertEqual(len(result["cases"]),2)
        self.assertEqual(result["applications"],3)
        self.assertEqual(result["option_count"],3)
        self.assertEqual(result["cases"]["example|facing=north"][0],(0,))
        self.assertIn("example|<empty>",result["cases"])

    def test_multipart_and_or_with_boolean_complements(self):
        model={
            "multipart":[
                {"apply":{"model":"minecraft:block/base"}},
                {"when":{"OR":[{"north":"true"},{"south":"true"}]},
                 "apply":[{"model":"minecraft:block/north"},{"model":"minecraft:block/other"}]},
                {"when":{"AND":[{"east":"true"},{"west":"true"}]},
                 "apply":{"model":"minecraft:block/east"}}
            ]
        }
        result=compute_cases("1.21.11/assets/minecraft/blockstates/fence.json",model)
        self.assertEqual(len(result["cases"]),16)
        # base always 1; OR true for 12/16 yields 2 alternatives;
        # AND true only for 4/16 yields 1.
        self.assertEqual(result["applications"],16+24+4)
        self.assertEqual(result["cases"]["fence|east=false,north=false,south=false,west=false"][0],(0,))

    def test_non_boolean_property_syntax(self):
        model={
            "multipart":[
                {"when":{"north":"low|tall"},"apply":{"model":"minecraft:block/north"}},
                {"when":{"up":"true"},"apply":{"model":"minecraft:block/up"}},
            ]
        }
        result=compute_cases("1.21.11/assets/minecraft/blockstates/wall.json",model)
        # north low/tall only, up true/false
        self.assertEqual(len(result["cases"]),4)
        self.assertEqual(result["applications"],6)

    def test_historical_option_normalization(self):
        historic={"model_options":[
            {"rule_index":7,"alternative_index":1,
             "model_ref":"minecraft:block/a","x_value":90,"y_value":None,
             "uvlock_value":False,"weight_value":3}
        ]}
        pair=historical_options(historic)
        self.assertEqual(pair,((7,1,"minecraft:block/a",90,None,False,3),))
        self.assertEqual(historical_hits([7, 2]),(7,2))
        self.assertEqual(historical_hits("7|2"),(7,2))

    def test_duplicate_keys_not_accepted(self):
        with self.assertRaisesRegex(ValueError,"duplicate JSON key"):
            parse_json(b'{"variants": {}, "variants": {"": {}}}',"bad.json")


if __name__=="__main__":
    unittest.main()
