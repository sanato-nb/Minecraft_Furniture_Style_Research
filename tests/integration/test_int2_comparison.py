"""Test isolated comparison evidence derivation, independent of historic 1-5 code."""
import sys
from pathlib import Path
import unittest
from fractions import Fraction

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/integration"))
from audit_int2_comparison import matching_rules,eval_multipart,face_diff,surface_compare,sample,spans,derive_claim


class SourceComparisonTests(unittest.TestCase):
    def test_variants_select_correct_rule(self):
        doc={"variants":{"facing=north,open=false":{"model":"a"},
                         "facing=north,open=true":[{"model":"b"},{"model":"c"}]}}
        self.assertEqual([r[0] for r in matching_rules(doc,{"facing":"north","open":"true"})],[1])
        self.assertEqual([r[0] for r in matching_rules(doc,{"facing":"north","open":"false"})],[0])
        self.assertEqual(matching_rules(doc,{"facing":"south","open":"false"}),[])

    def test_multipart_or_and(self):
        doc={"multipart":[
             {"apply":{"model":"base"}},
             {"when":{"OR":[{"north":"true"},{"south":"true"}]},"apply":{"model":"edge"}},
             {"when":{"AND":[{"east":"true"},{"up":"high|tall"}]},"apply":{"model":"corner"}},
        ]}
        rules=matching_rules(doc,{"north":"true","south":"false","east":"true","up":"tall"})
        self.assertEqual([idx for idx,_ in rules],[0,1,2])

    def test_disallow_multipart_wrong_boolean(self):
        self.assertFalse(eval_multipart({"north":"true"},{"north":"false"}))

    def test_face_change_keeps_same_local_keys(self):
        old=[{"element_index":"0","direction":"north","resource_id":"x","uv":"0|0|16|16","rgba_sha256":"a"}]
        new=[{"element_index":"0","direction":"north","resource_id":"y","uv":"0|0|16|16","rgba_sha256":"b"}]
        d=face_diff("x","y",{"x":old,"y":new},{"x":[1],"y":[2]})
        self.assertEqual(d,{"resource_id":["0/north"],"uv":[],"rgba_sha256":["0/north"]})

    def test_samples_from_measurements(self):
        r={k:str(i) for i,k in enumerate(
             ("applications","elements","faces","zero_thickness_elements","faces_measured","faces_at_density_1x1"),1)}
        self.assertEqual(sample(r)["faces"],3)

    def test_claim_kind_error(self):
        with self.assertRaisesRegex(ValueError,"Unknown claim axis"):
            derive_claim({"axis":"FAKE"}, {}, {}, {}, {}, {})


if __name__=="__main__":
    unittest.main()
