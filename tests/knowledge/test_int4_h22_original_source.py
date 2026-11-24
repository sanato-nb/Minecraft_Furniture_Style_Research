import unittest
from mcfr import int4_h22_hc_macaw12_original_source as m
class H22(unittest.TestCase):
    def test_scope(self):
        self.assertEqual(len(m.IDS),12)
        self.assertEqual(len(m.HC),5)
        self.assertNotIn("R06",m.IDS)
    def test_macaw_namespace(self):
        self.assertEqual(m.resource("mcwfurnitures:block/parent/table_single","models"),"assets/mcwfurnitures/models/block/parent/table_single.json")
    def test_hc_namespace(self):
        self.assertEqual(m.resource("handcrafted:block/oak","textures"),"assets/handcrafted/textures/block/oak.png")
    def test_invalid_resource(self):
        with self.assertRaisesRegex(ValueError,"invalid resource"):
            m.resource("handcrafted:../foo","models")
    def test_rotation_in_selection(self):
        self.assertNotEqual(m.opt({"model":"mcwfurnitures:block/a","y":90}),m.opt({"model":"mcwfurnitures:block/a","y":180}))
    def test_source_capture_cannot_substitute_wrong_digest(self):
        with self.assertRaises((ValueError,KeyError)):
            m.capture("S38",{"original_f2_sha256s":"wrong","original_f2_run_ids":"1"},{},{},{},{"first_paired_background_controlled_f2":{"run_id":2,"observed":{}}})
if __name__=="__main__":unittest.main()
