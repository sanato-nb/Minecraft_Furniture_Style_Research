"""INT5 B8: source-accurate isolation and synthetic controls, not fake F2 PASS."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image,ImageDraw

from mcfr import int5_b8_hc_cushion_element12_native_f2 as b8
from mcfr import int5_b8_hc_cushion_source_preflight as pre


def model_samples():
    elems=[]
    faces=("down","east","north","south","up","west")
    for i in range(13):
        elems.append({
            "from":[0,i,0],"to":[2,i+1,2],
            "faces":{name:{"texture":"#1" if i==12 else "#0"}
                     for name in faces}
        })
    parent={"elements":elems,"textures":{"0":"#wood","1":"#cushion"}}
    child={"parent":"handcrafted:block/chair/chair",
           "textures":{"wood":"handcrafted:block/chair/warped_chair",
                       "cushion":"handcrafted:block/chair/cushion/black_cushion"}}
    return json.dumps(child).encode(),json.dumps(parent).encode()


def picture(chair=True,cushion=True,white=False):
    im=Image.new("RGB",(1024,684),(180,182,188))
    draw=ImageDraw.Draw(im)
    if chair:
        draw.rectangle((495,398,536,475),fill=(40,132,120))
        if cushion:
            draw.rectangle((499,424,532,442),fill=(242,242,242) if white else
                           (40,40,46))
    return im


def sample_sessions(patched=False,wrong_white=False,wrong_air=False):
    frames={}
    for view in b8.VIEWS:
        frames[view]={
            "black_before":picture(cushion=not patched),
            "white":picture(white=True),
            "black_after":picture(cushion=not patched),
            "air":picture(chair=False),
        }
    if wrong_white:
        ImageDraw.Draw(frames["north"]["white"]).rectangle(
            (502,425,522,438),fill=(255,0,255))
    if wrong_air:
        ImageDraw.Draw(frames["south"]["air"]).rectangle(
            (502,425,522,438),fill=(255,0,255))
    return frames


class HCCushionElement12Tests(unittest.TestCase):
    def test_B6_HC_source_still_unverified_function_and_exact_candidate(self):
        r=b8.source_role_check()
        self.assertEqual((r["child_model_key"],r["provider_key"],
                          r["original_source_element_index"]),
                         ("HC11210","HC13","12"))
        self.assertEqual(r["source_texture_role_cue"],
                         "ROLE_NAMED_ORIGINAL_CUSHION_PNG")

    def test_exact_original_fixture_and_two_cameras(self):
        self.assertEqual(b8.pinned_chair_case().case_id,pre.CASE)
        self.assertEqual(b8.CASE_XYZ,(40,120,40))
        self.assertEqual(b8.CAMERAS["south"],"40.5 122.3 45.5 180 20")
        self.assertEqual(b8.CAMERAS["north"],"40.5 122.3 35.5 0 20")
        self.assertEqual(b8.state("black_before"),pre.STATE)
        self.assertEqual(b8.state("white"),pre.CTRL_STATE)
        self.assertEqual(b8.state("air"),"minecraft:air")

    def test_runtime_HC_fixture_branch_cannot_be_shadowed_by_AF_cases(self):
        path=b8.ROOT/"src/mcfr/runtime.py"
        source=path.read_text(encoding="utf-8")
        clauses=[x.strip() for x in source.splitlines()
                 if x.strip().startswith("elif args.command in (")]
        self.assertTrue(all(
            "int5-b8-hc-cushion12-native-f2" not in c for c in clauses),
            "B8 will accidentally launch AF121 or AF123 chair fixture")
        self.assertEqual(source.count(
            'elif args.command=="int5-b8-hc-cushion12-native-f2":'),1)
        self.assertIn('selected=(pinned_chair_case(),)',source)

    def test_source_study_and_official_pinned_mod_4_0_3(self):
        self.assertEqual(pre.SHA1,"a9579fecd7ed429c282be21d5c921d220197acc6")
        self.assertEqual(pre.SOURCE_PARENT_BLOB,
                         "c5d9fbc054a897673f972fe2559376123751ba9b")
        self.assertEqual(pre.ELEMENT,12)

    def test_original_single_child_only_element12_13_to_12_and_78_to_72(self):
        child,parent=model_samples()
        patch,result=b8.override_child_only(child,parent)
        m=json.loads(patch)
        self.assertEqual(len(m["elements"]),12)
        self.assertEqual(sum(len(e["faces"]) for e in m["elements"]),72)
        self.assertEqual(result["removed_original_element_index"],12)
        self.assertTrue(result["child_parent_and_texture_aliases_unchanged"])
        self.assertEqual(m["parent"],"handcrafted:block/chair/chair")
        self.assertEqual(m["textures"],json.loads(child)["textures"])

    def test_unexpected_original_parent_element_count_fails_closed(self):
        child,parent=model_samples()
        broken=json.loads(parent)
        broken["elements"]=broken["elements"][:12]
        with self.assertRaisesRegex(ValueError,"13/78"):
            b8.override_child_only(child,json.dumps(broken).encode())

    def test_unexpected_modified_black_child_existing_elements_fails(self):
        child,parent=model_samples()
        broken=json.loads(child)
        broken["elements"]=[]
        with self.assertRaisesRegex(ValueError,"must inherit"):
            b8.override_child_only(json.dumps(broken).encode(),parent)

    def test_single_source_removal_real_screen_response_synthetic_only(self):
        m=b8.measure(sample_sessions(),sample_sessions(patched=True))
        for view in b8.VIEWS:
            x=m[view]
            self.assertGreater(
                x["cushion12_removal_original_vs_modified_black_before_pixels"],0)
            self.assertEqual(x["cushion12_removal_original_vs_modified_black_before_pixels"],
                             x["cushion12_removal_original_vs_modified_black_after_pixels"])
            for key in (
                "white_control_original_vs_modified_pixels",
                "air_control_original_vs_modified_pixels",
                "original_black_before_vs_after_temporal_pixels",
                "modified_black_before_vs_after_temporal_pixels",
                "changed_pixels_outside_original_black_foreground",
            ):
                self.assertEqual(x[key],0)

    def test_handcrafted_dropped_item_must_be_purged_and_server_verified(self):
        code=Path(b8.__file__).read_text(encoding="utf-8")
        self.assertIn('/kill @e[type=minecraft:item]',code)
        self.assertIn('/execute unless entity @e[type=minecraft:item]',code)
        self.assertIn('"dropped_items_zero_game_server_marker":no_items',code)
        self.assertIn('"dropped_items_zero_game_server_verified":True',code)
        self.assertIn('"dropped_item_entities_zero_at_all_16_F2":True',code)

    def test_white_child_mutation_detected_as_negative_control(self):
        m=b8.measure(sample_sessions(),
                     sample_sessions(patched=True,wrong_white=True))
        self.assertGreater(m["north"]["white_control_original_vs_modified_pixels"],0)

    def test_air_change_detected_as_negative_control(self):
        m=b8.measure(sample_sessions(),
                     sample_sessions(patched=True,wrong_air=True))
        self.assertGreater(m["south"]["air_control_original_vs_modified_pixels"],0)

    def test_missing_real_original_mod_f2_never_mistaken_for_pass(self):
        with TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                b8.audit(Path(folder))

    def test_code_must_never_promote_rights_material_function_or_owner(self):
        code=Path(b8.__file__).read_text(encoding="utf-8")
        self.assertIn('"original_element_exclusive_visible_pixel_ownership_approved":False',code)
        self.assertIn('"gameplay_seating_or_function_approved":False',code)
        self.assertIn('"part_material_or_style_final_approved":False',code)
        self.assertIn('"INT6_AI_training_or_redistribution_rights_approved":0',code)
        self.assertIn('"F70_unconditional_approvals":0',code)

if __name__=="__main__":unittest.main()
