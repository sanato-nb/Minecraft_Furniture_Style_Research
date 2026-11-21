"""Independently test Minecraft raw model -> texture slot/face UV projection."""
import sys
from pathlib import Path
from fractions import Fraction
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
from audit_int2_full_face_links import (
    ancestors, classify, default_uv, density, normalize, resolve_slot, canon
)

class FullFaceOriginalReplayTests(unittest.TestCase):
    def test_unqualified_parent_is_minecraft_namespace(self):
        self.assertEqual(normalize("block/block"),"minecraft:block/block")
        self.assertEqual(normalize("handcrafted:block/chair"),"handcrafted:block/chair")

    def test_default_uv_6_face_formulas(self):
        start=(1,2,3)
        end=(7,9,13)
        exp={
            "down":(1,3,7,13),"up":(1,3,7,13),
            "north":(9,7,15,14),"south":(1,7,7,14),
            "west":(3,7,13,14),"east":(3,7,13,14),
        }
        for side,values in exp.items():
            self.assertEqual(default_uv(start,end,side),tuple(map(Fraction,values)))

    def test_fractional_source_uv_preserved(self):
        self.assertEqual(canon([0,1.5,16,14.5]),"0|3/2|16|29/2")

    def test_slot_alias_direct_and_cycle(self):
        binding={"layer0":"#wood","wood":"minecraft:block/oak_planks",
                 "a":"#b","b":"#a"}
        self.assertEqual(resolve_slot("#layer0",binding),("RESOURCE_ID","minecraft:block/oak_planks"))
        self.assertEqual(resolve_slot("#not_found",binding),("SLOT_UNBOUND",None))
        self.assertEqual(resolve_slot("#a",binding),("SLOT_CYCLE",None))
        self.assertEqual(resolve_slot("handcrafted:block/chair",binding),("RESOURCE_ID","handcrafted:block/chair"))

    def test_missing_and_zero_uv_categories(self):
        uv=tuple(map(Fraction,[0,0,16,16]))
        m={42:{"frame_count":"1","frame_width":"16","frame_height":"16"},
           99:{"frame_count":"4","frame_width":"16","frame_height":"16"}}
        self.assertEqual(classify(None,uv,m),"SLOT_UNBOUND")
        self.assertEqual(classify(41,uv,m),"MISSING_PINNED_PNG")
        self.assertEqual(classify(42,(Fraction(0),Fraction(2),Fraction(0),Fraction(4)),m),"ZERO_UV_AREA")
        self.assertEqual(classify(42,(Fraction(-1),Fraction(0),Fraction(9),Fraction(8)),m),"OUTSIDE_TEXTURE_UV")
        self.assertEqual(classify(42,uv,m),"STATIC_RECT")
        self.assertEqual(classify(99,uv,m),"ANIMATED_FRAME_RECTS")

    def test_implicit_uv_pixel_per_local_unit(self):
        meta={"frame_width":"16","frame_height":"16"}
        uv=tuple(map(Fraction,[0,0,16,16]))
        self.assertEqual(density(uv,0,"up",[0,0,0],[16,8,16],meta),("1","1"))
        self.assertEqual(density(uv,90,"up",[0,0,0],[16,8,16],meta),("1","1"))

    def test_parent_traversal_finds_vanilla_parent(self):
        models={"A":{"parent":"minecraft:block/cube","textures":{"all":"#layer0"}},
                "B":{"elements":[{"from":[0,0,0],"to":[16,16,16],"faces":{"up":{"texture":"#all"}}}]}}
        ix={("MC1.21.1","minecraft:block/cube"):"B"}
        keys,term,end=ancestors("A","HC","1.21.1",ix,models)
        self.assertEqual(keys,["A","B"])
        self.assertEqual((term,end),("ROOT",""))

    def test_parent_missing_is_reported_not_fabricated(self):
        models={"A":{"parent":"other:block/not_present"}}
        keys,term,end=ancestors("A","HC","1.21.1",{},models)
        self.assertEqual((keys,term,end),(["A"],"PARENT_MISSING","other:block/not_present"))


if __name__=="__main__":
    unittest.main()
