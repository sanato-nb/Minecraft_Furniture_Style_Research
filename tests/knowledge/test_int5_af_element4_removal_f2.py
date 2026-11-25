"""B5 isolated source-model and synthetic-mask negative tests; NOT real game F2."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from mcfr import int5_af_element4_removal_f2 as b5
from mcfr import int5_af_tucked_slab_control as b4


def element(i):
    faces = 6 if i == 4 else (5 if i < 4 else 4)
    return {"from": [0, i, 0], "to": [4, i + 1, 4],
            "faces": {f"face_{n}": {"texture": "#oak"}
                      for n in range(faces)}}

def actual_chain():
    child = b5.model_member(b5.MODEL_ID)
    provider = b5.model_member("another_furniture:block/chair/provider_fixture")
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

class B5SourceAndScreenControls(unittest.TestCase):
    def test_pinned_b3_original_source_role_is_only_hypothesis(self):
        row = b5.source_role_check()
        self.assertEqual(row["provider_key"], "AF1394")
        self.assertEqual(row["original_role_hypothesis"], "SEAT_LAYER")
        self.assertEqual(row["individual_element_to_original_F2_pixels_approved"], "false")

    def test_actual_original_child_to_provider_chain_is_read(self):
        resources, expected = actual_chain()
        member, model, chain = b5.find_provider(resources)
        self.assertEqual(member, expected)
        self.assertEqual(len(chain), 2)
        self.assertEqual(len(model["elements"]), 10)
        self.assertEqual(sum(len(x["faces"]) for x in model["elements"]), 46)

    def test_source_model_with_only_nine_elements_is_rejected(self):
        resources, provider = actual_chain()
        model = json.loads(resources[provider])
        model["elements"].pop(4)
        resources[provider] = json.dumps(model).encode()
        with self.assertRaisesRegex(ValueError, "ten expected elements"):
            b5.find_provider(resources)

    def test_missing_or_cyclic_provider_fails_closed(self):
        resources, provider = actual_chain()
        resources.pop(provider)
        with self.assertRaisesRegex(ValueError, "missing or cyclic"):
            b5.find_provider(resources)
        resources, provider = actual_chain()
        resources[provider] = json.dumps({"parent":b5.MODEL_ID}).encode()
        with self.assertRaisesRegex(ValueError, "missing or cyclic"):
            b5.find_provider(resources)

    def test_synthetic_chair_only_remove_element_has_delta_and_negative_controls(self):
        data = b5.evaluate(scenes(), scenes(remove_part=True))
        for metric in data.values():
            self.assertGreater(metric["element4_removal_source_intervention_delta_pixels"], 0)
            self.assertEqual(metric["element4_removal_repeated_delta_pixels"],
                             metric["element4_removal_source_intervention_delta_pixels"])
            self.assertEqual(metric["unchanged_slab_only_negative_control_pixels"], 0)
            self.assertEqual(metric["unchanged_air_negative_control_pixels"], 0)
            self.assertEqual(metric["modified_session_temporal_delta_pixels"], 0)
            self.assertEqual(metric["intervention_pixels_outside_original_visible_chair_foreground"], 0)

    def test_changed_slab_control_cannot_be_hidden(self):
        modified = scenes(remove_part=True)
        ImageDraw.Draw(modified["north"]["slab_only"]).rectangle(
            (493, 403, 503, 414), fill=(0, 0, 0))
        result = b5.evaluate(scenes(), modified)
        self.assertGreater(result["north"]["unchanged_slab_only_negative_control_pixels"], 0)

    def test_source_member_path_and_scope_rejections(self):
        self.assertEqual(b5.model_member(b5.MODEL_ID),
            "assets/another_furniture/models/block/chair/acacia_10_tucked.json")
        with self.assertRaisesRegex(ValueError,"invalid source"):
            b5.model_member("another_furniture:../../secrets")
        with self.assertRaisesRegex(ValueError, "parent outside AF pinned namespace"):
            b5.find_provider({b5.model_member(b5.MODEL_ID):
                              json.dumps({"parent":"minecraft:block/cube_all"}).encode()})

    def test_missing_real_original_f2_is_not_mock_approved(self):
        with TemporaryDirectory() as d:
            with self.assertRaises((FileNotFoundError, ValueError, KeyError)):
                b5.audit(Path(d), Path(d))

    def test_no_ai_or_function_approval_in_research_code(self):
        source = Path(b5.__file__).read_text(encoding="utf-8")
        self.assertIn('"final_INT5_part_meaning_approvals": 0',source)
        self.assertIn('"INT6_AI_training_or_redistribution_approvals": 0',source)
        self.assertIn('"individual_original_element_pixel_ownership_approved": False',source)

if __name__ == "__main__":
    unittest.main()
