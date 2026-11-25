"""B13 isolated source-model and synthetic-mask negative tests; NOT real game F2."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from mcfr import int5_b13_af123_backrest_element8_native_f2 as b13
from mcfr import int5_af_tucked_slab_control as b4


def element(i):
    faces = 6 if i == 4 else (2 if i == 7 else (5 if i in (0,1,2,3,8,9) else 4))
    return {"from": [0, i, 0], "to": [4, i + 1, 4],
            "faces": {f"face_{n}": {"texture": "#oak"}
                      for n in range(faces)}}

def actual_chain():
    child = b13.model_member(b13.MODEL_ID)
    provider = b13.model_member("another_furniture:block/chair/provider_fixture")
    content = {child: json.dumps({"parent":
                     "another_furniture:block/chair/provider_fixture"}).encode(),
               provider: json.dumps({"elements": [element(i) for i in range(10)]}).encode()}
    return content, provider

def frame(chair=True, slab=True, remove_part=False):
    image = Image.new("RGB", (1024, 684), (200, 200, 200))
    draw = ImageDraw.Draw(image)
    if slab:
        draw.rectangle((490, 400, 520, 424), fill=(140, 120, 85))
    if chair:
        draw.rectangle((492, 425, 530, 480), fill=(170, 95, 45))
        if not remove_part:
            draw.rectangle((497, 430, 512, 442), fill=(255, 150, 70))
    return image

def scenes(remove_part=False):
    return {v: {"chair_plus_slab_before": frame(remove_part=remove_part),
                "slab_only": frame(chair=False),
                "chair_plus_slab_after": frame(remove_part=remove_part),
                "empty": frame(chair=False, slab=False)}
            for v in b4.VIEWS}

class B13SourceAndScreenControls(unittest.TestCase):
    def test_pinned_b3_original_source_role_is_only_hypothesis(self):
        row = b13.source_role_check()
        self.assertEqual(row["provider_key"], "AF1394")
        self.assertEqual(row["original_role_hypothesis"], "BACKREST_ASSEMBLY")
        self.assertEqual(row["source_element_original_face_count"],"5")
        self.assertEqual(row["individual_element_to_original_F2_pixels_approved"], "false")

    def test_actual_original_child_to_provider_chain_is_read(self):
        resources, expected = actual_chain()
        member, model, chain = b13.find_provider(resources)
        self.assertEqual(member, expected)
        self.assertEqual(len(chain), 2)
        self.assertEqual(len(model["elements"]), 10)
        self.assertEqual(sum(len(x["faces"]) for x in model["elements"]), 46)

    def test_isolated_child_override_only_source_index8_five_faces(self):
        parent={"elements":[element(i) for i in range(10)]}
        child={"parent":"another_furniture:block/template/chair_tucked",
               "textures":{"back":"another_furniture:block/chair/back_10/acacia"}}
        raw=json.dumps(child).encode()
        patched,removed=b13.isolated_child_override(raw,parent)
        result=json.loads(patched)
        self.assertEqual(b13.ELEMENT_INDEX,8)
        self.assertEqual(len(parent["elements"]),10)
        self.assertEqual(sum(len(e["faces"]) for e in parent["elements"]),46)
        self.assertEqual(len(removed["faces"]),5)
        self.assertEqual(len(result["elements"]),9)
        self.assertEqual(sum(len(e["faces"]) for e in result["elements"]),41)
        self.assertEqual(result["textures"],child["textures"])
        self.assertEqual(result["elements"],[element(i) for i in range(10) if i!=8])
        self.assertEqual(parent["elements"][8],element(8))

    def test_existing_child_geometry_must_not_be_overwritten(self):
        doc={"parent":"another_furniture:block/template/chair_tucked","elements":[]}
        with self.assertRaisesRegex(ValueError,"inherit unmodified"):
            b13.isolated_child_override(json.dumps(doc).encode(),
                                        {"elements":[element(i) for i in range(10)]})

    def test_child_wrong_parent_or_wrong_face_count_is_rejected(self):
        child={"parent":"minecraft:block/cube_all"}
        with self.assertRaisesRegex(ValueError,"inherit unmodified"):
            b13.isolated_child_override(json.dumps(child).encode(),
                                        {"elements":[element(i) for i in range(10)]})
        child["parent"]="another_furniture:block/template/chair_tucked"
        parent={"elements":[element(i) for i in range(10)]}
        parent["elements"][8]["faces"].pop("face_0")
        with self.assertRaisesRegex(ValueError,"10/46"):
            b13.isolated_child_override(json.dumps(child).encode(),parent)

    def test_legitimate_af123_original_top_slab_state_is_fixed(self):
        case=b4.target_case()
        self.assertEqual(case.state(),
            "another_furniture:acacia_chair[facing=north,tucked=true,variant=10]")
        self.assertEqual(b4.stage_slab_state("chair_plus_slab_before"),
                         "minecraft:oak_slab[type=top]")
        self.assertEqual(b4.stage_chair_state("slab_only"),"minecraft:air")
        self.assertEqual(b4.slab_xyz(),(case.x,case.y,case.z-1))
        self.assertEqual(b4.STAGES,("chair_plus_slab_before","slab_only",
                                    "chair_plus_slab_after","empty"))

    def test_source_model_with_only_nine_elements_is_rejected(self):
        resources, provider = actual_chain()
        model = json.loads(resources[provider])
        model["elements"].pop(8)
        resources[provider] = json.dumps(model).encode()
        with self.assertRaisesRegex(ValueError, "ten expected elements"):
            b13.find_provider(resources)

    def test_missing_or_cyclic_provider_fails_closed(self):
        resources, provider = actual_chain()
        resources.pop(provider)
        with self.assertRaisesRegex(ValueError, "missing or cyclic"):
            b13.find_provider(resources)
        resources, provider = actual_chain()
        resources[provider] = json.dumps({"parent":b13.MODEL_ID}).encode()
        with self.assertRaisesRegex(ValueError, "missing or cyclic"):
            b13.find_provider(resources)

    def test_synthetic_chair_only_remove_element_has_delta_and_negative_controls(self):
        data = b13.evaluate(scenes(), scenes(remove_part=True))
        for metric in data.values():
            self.assertGreater(metric["element8_removal_source_intervention_delta_pixels"], 0)
            self.assertEqual(metric["element8_removal_repeated_delta_pixels"],
                             metric["element8_removal_source_intervention_delta_pixels"])
            self.assertEqual(metric["unchanged_slab_only_negative_control_pixels"], 0)
            self.assertEqual(metric["unchanged_air_negative_control_pixels"], 0)
            self.assertEqual(metric["modified_session_temporal_delta_pixels"], 0)
            self.assertEqual(metric["intervention_pixels_outside_original_visible_chair_foreground"], 0)

    def test_changed_slab_control_cannot_be_hidden(self):
        modified = scenes(remove_part=True)
        ImageDraw.Draw(modified["north"]["slab_only"]).rectangle(
            (493, 403, 503, 414), fill=(0, 0, 0))
        result = b13.evaluate(scenes(), modified)
        self.assertGreater(result["north"]["unchanged_slab_only_negative_control_pixels"], 0)

    def test_source_member_path_and_scope_rejections(self):
        self.assertEqual(b13.model_member(b13.MODEL_ID),
            "assets/another_furniture/models/block/chair/acacia_10_tucked.json")
        with self.assertRaisesRegex(ValueError,"invalid source"):
            b13.model_member("another_furniture:../../secrets")
        with self.assertRaisesRegex(ValueError, "parent outside AF pinned namespace"):
            b13.find_provider({b13.model_member(b13.MODEL_ID):
                              json.dumps({"parent":"minecraft:block/cube_all"}).encode()})

    def test_missing_real_original_f2_is_not_mock_approved(self):
        with TemporaryDirectory() as d:
            with self.assertRaises((FileNotFoundError, ValueError, KeyError)):
                b13.audit(Path(d), Path(d))

    def test_no_ai_or_function_approval_in_research_code(self):
        source = Path(b13.__file__).read_text(encoding="utf-8")
        self.assertIn('"final_INT5_part_meaning_approvals": 0',source)
        self.assertIn('"INT6_AI_training_or_redistribution_approvals": 0',source)
        self.assertIn('"individual_original_element_pixel_ownership_approved": False',source)
        self.assertIn('"modified_member_is_only_target_child_json":True',source)
        self.assertIn('"original_shared_provider_unmodified":True',source)

if __name__ == "__main__":
    unittest.main()
