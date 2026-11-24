import unittest
from mcfr import int4_h21_af16_release_comparison as m
class AF16(unittest.TestCase):
    def test_scope(self):
        self.assertEqual(len(m.IDS),16)
    def test_variant_order(self):
        props={"facing":"north","open":"false"}
        d={"variants":{"open=false,facing=north":{"model":"another_furniture:block/drawer/oak"}}}
        self.assertEqual(len(m.select(d,props)),1)
    def test_multipart_and_rotation(self):
        d={"multipart":[{"apply":{"model":"another_furniture:block/top"}},
          {"when":{"OR":[{"leg":"true"},{"all":"true"}]},"apply":{"model":"another_furniture:block/leg","y":90}}]}
        self.assertEqual(len(m.select(d,{"leg":"true"})),2)
        self.assertEqual(len(m.select(d,{"leg":"false"})),1)
    def test_ambiguous_variant_fails(self):
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            m.select({"variants":{"a=b,c=d":{},"c=d,a=b":{}}},{"a":"b","c":"d"})
    def test_texture_alias_cycle(self):
        with self.assertRaisesRegex(ValueError,"unresolved"):
            m.resolve({"a":"#b","b":"#a"},"#a")
    def test_duplicate_json(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            m.doc(b'{"a":1,"a":2}')
    def test_default_uv(self):
        self.assertEqual(m.uv_values({"from":[2,3,4],"to":[5,6,7]},"north",{})[0],(11,10,14,13))
    def test_selected_option_includes_rotation(self):
        self.assertNotEqual(m.option({"model":"minecraft:block/cube","y":90}),m.option({"model":"minecraft:block/cube","y":180}))
if __name__=="__main__":unittest.main()
