"""Independent 1-3 original source and geometry auditor unit regression tests."""
from pathlib import Path
import runpy
import unittest

f=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/integration/audit_int2_mod_geometry.py"))
box=f["bbox"]
compare=f["same_vec"]
slots=f["slot_status"]
unique=f["json_unique"]


class ModIndependentAuditTests(unittest.TestCase):
    def test_origin_and_rotated_aabb(self):
        rect={"from":[0,0,4],"to":[16,16,12]}
        self.assertEqual(box(rect),(0,0,4,16,16,12))
        r={**rect,"rotation":{"axis":"y","angle":90,"origin":[8,8,8]}}
        self.assertTrue(compare("4|0|0|12|16|16",box(r,True)))
        r["rotation"]["angle"]=45
        r["rotation"]["rescale"]=True
        bounds=box(r,True)
        self.assertTrue(all(abs(x)<100 for x in bounds))
        self.assertTrue(all(bounds[i] <= bounds[i+3] for i in range(3)))

    def test_degenerate_and_inverted_coords(self):
        rect={"from":[17,8,7],"to":[-1,8,7],
              "rotation":{"axis":"x","angle":22.5,"origin":[8,8,8]}}
        x=box(rect,True)
        self.assertAlmostEqual(x[0],-1)
        self.assertAlmostEqual(x[3],17)
        self.assertTrue(x[4]==8 or x[4]>8)

    def test_slot_unbound_and_cycle(self):
        self.assertEqual(slots("#a",{"a":"#b","b":"#a"}),"SLOT_CYCLE")
        self.assertEqual(slots("#missing",{}),"SLOT_UNBOUND")
        self.assertEqual(slots("minecraft:block/stone",{}),"RESOURCE_ID")
        self.assertEqual(slots("#a",{"a":"minecraft:block/stone"}),"RESOURCE_ID")

    def test_duplicate_json_keys_fail(self):
        with self.assertRaisesRegex(ValueError,"Duplicate JSON key"):
            unique(b'{"parent":"a","parent":"b"}',"fixture.json")


if __name__=="__main__":
    unittest.main()
