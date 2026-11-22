"""Tests against accidental promotion of missing pixels into screen/render defects."""
import importlib.util
from pathlib import Path
import unittest


def module():
    script=Path(__file__).resolve().parents[2]/"scripts/integration/build_int4_c_pixel_exception_ledger.py"
    spec=importlib.util.spec_from_file_location("int4_c_dispositions",script)
    result=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(result)
    return result


a=module()


class PixelExceptionTests(unittest.TestCase):
    def test_precedence_null_texture_over_uv(self):
        self.assertEqual(a.face_classification(None,"","60|0|70|20"),"SLOT_UNBOUND")

    def test_precedence_missing_path_over_uv(self):
        self.assertEqual(a.face_classification(123,"","60|0|70|20"),"MISSING_PINNED_PNG")

    def test_uv_zero_area(self):
        self.assertEqual(a.face_classification(1,"some.png","0|0|0|16"),"ZERO_UV_AREA")

    def test_uv_outside(self):
        self.assertEqual(a.face_classification(1,"some.png","0|36|10|60"),"OUTSIDE_TEXTURE_UV")

    def test_uv_valid(self):
        self.assertEqual(a.face_classification(1,"some.png","0|0|16|16"),
                         "RENDERABLE_RECT_FROM_SOURCE_DECLARATION")

    def test_static_template_child_is_not_png_sample(self):
        case=a.compose_exception("SLOT_UNBOUND","BOUND_CHILD_CONTEXT","BOUND_CHILD_CONTEXT")
        self.assertEqual(case[0],"SLOT_UNBOUND_BOUND_CHILD_CONTEXT")
        self.assertIn("NOT_DIRECT_PIXEL_SUPPORT",case[3])

    def test_no_child_is_held(self):
        case=a.compose_exception("SLOT_UNBOUND","UNBOUND_NO_BOUND_CHILD",
                                 "UNBOUND_NO_BOUND_CHILD")
        self.assertEqual(case[0],"SLOT_UNBOUND_NO_BOUND_CHILD")
        self.assertTrue(case[3].startswith("HOLD"))

    def test_missing_png_has_no_fabricated_source(self):
        case=a.compose_exception("MISSING_PINNED_PNG","","")
        self.assertEqual(case[0],"MISSING_PINNED_PNG")
        self.assertTrue(case[3].startswith("HOLD"))

    def test_no_intersection_requires_outside_status(self):
        with self.assertRaises(AssertionError):
            a.compose_exception("ZERO_UV_AREA","","NO_PINNED_SPRITE_INTERSECTION")

    def test_pin_change_must_fail(self):
        path="project/integration/INT2_1_4_SUMMARY.json"
        before=a.PATHS[path]
        try:
            a.PATHS[path]="0"*40
            with self.assertRaises(AssertionError):
                a.locked(path)
        finally:
            a.PATHS[path]=before

    def test_legacy_decimal_uv_matches_rational_source_group(self):
        self.assertEqual(a.canonical_uv("-5|1|1|1.5"),"-5|1|1|3/2")
        self.assertEqual(a.canonical_uv("-5|1|1|3/2"),"-5|1|1|3/2")

    def test_source_implicit_uv_formula(self):
        # Original 1.21.1 Java BlockElement formula pinned in 1-4 entry02.
        self.assertEqual(a.source_default_uv("1|2|3","7|9|13","down"),"1|3|7|13")
        self.assertEqual(a.source_default_uv("1|2|3","7|9|13","up"),"1|3|7|13")
        self.assertEqual(a.source_default_uv("1|2|3","7|9|13","north"),"9|7|15|14")
        self.assertEqual(a.source_default_uv("1|2|3","7|9|13","east"),"3|7|13|14")

    def test_invalid_uv_rejected(self):
        with self.assertRaises(AssertionError):
            a.uv_values("0|16|32")


if __name__=="__main__":
    unittest.main()
