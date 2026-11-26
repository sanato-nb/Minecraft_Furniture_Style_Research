"""B20 signed reversed-X original source5 / child flatten / three real games."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from mcfr import int5_b20_af_reversed_x_three_session_f2 as b20
from mcfr import int5_b19_four_unresolved_four_view_f2 as b19

FACE_NUM=(5,5,5,5,6,4,4,2,5,5)

def fixture(target):
    pin=b20.PIN[target]
    parent={"elements":[]}
    for i,n in enumerate(FACE_NUM):
        faces={k:{"uv":[0,0,2,2],"texture":"#all"} for k in
               ("north","south","east","west","up","down")[:n]}
        parent["elements"].append({
            "from":[0,1,2],"to":[2,3,4],"faces":faces})
    parent["elements"][5]["from"]=pin["from"].copy()
    parent["elements"][5]["to"]=pin["to"].copy()
    child={"parent":"another_furniture:block/template/chair"+(
         "_tucked" if target=="AF123_5" else ""),
         "textures":{"all":"another_furniture:block/chair/acacia"}}
    return json.dumps(child).encode(),json.dumps(parent).encode(),parent,child

def scene(stage,extra=False):
    img=Image.new("RGB",(1024,684),(193,197,202))
    if stage in ("model1_before","model1_after",
                 "chair_plus_slab_before","chair_plus_slab_after"):
        p=ImageDraw.Draw(img)
        p.rectangle((485,384,522,462),fill=(58,110,77))
        if extra:p.rectangle((514,390,532,412),fill=(150,50,50))
    return img

class B20Source5Tests(unittest.TestCase):
    def tearDown(self):b19.set_target("AF121_5")

    def test_only_two_stable_four_view_unobserved_original_sources(self):
        self.assertEqual(b20.TARGETS,("AF121_5","AF123_5"))
        for t in b20.TARGETS:
            with self.subTest(t=t):
                row=b20.source_identity(t)
                self.assertEqual(row["source_element_index"],5)
                self.assertEqual(row["source_faces"],4)
                self.assertEqual(row["B18_prior_south_pixels"],0)
                self.assertEqual(row["B18_prior_north_pixels"],0)

    def test_flatten_is_identical_to_all_parent_elements(self):
        for t in b20.TARGETS:
            child,parent,parsed,orig_child=fixture(t)
            raw,metadata=b20.patch_child(child,parent,t,"flattened")
            x=json.loads(raw)
            self.assertEqual(x["elements"],parsed["elements"])
            self.assertEqual({k:v for k,v in x.items() if k!="elements"},orig_child)
            self.assertEqual(metadata["source_faces"],4)
            self.assertFalse(metadata["changed_X_endpoints_only"])

    def test_normalized_swaps_only_original_source5_x_endpoints(self):
        for t in b20.TARGETS:
            child,parent,parsed,original=fixture(t)
            raw,meta=b20.patch_child(child,parent,t,"normalized")
            now=json.loads(raw)
            old=parsed["elements"][5]
            x=now["elements"][5]
            self.assertEqual(x["from"],[3,*old["from"][1:]])
            self.assertEqual(x["to"],[13,*old["to"][1:]])
            self.assertEqual(x["faces"],old["faces"])
            self.assertEqual(now["elements"][:5],parsed["elements"][:5])
            self.assertEqual(now["elements"][6:],parsed["elements"][6:])
            self.assertEqual({k:v for k,v in x.items() if k not in ("from","to")},
                             {k:v for k,v in old.items() if k not in ("from","to")})
            self.assertEqual(sum(len(e["faces"]) for e in now["elements"]),46)
            self.assertTrue(meta["changed_X_endpoints_only"])

    def test_wrong_source_coordinates_or_faces_fail_closed(self):
        child,parent,parsed,_=fixture("AF121_5")
        for change in (lambda p:p["elements"][5]["from"].__setitem__(0,12),
                       lambda p:p["elements"][5]["faces"].pop("north"),
                       lambda p:p["elements"].append(copy.deepcopy(p["elements"][0]))):
            p=copy.deepcopy(parsed)
            change(p)
            with self.assertRaisesRegex(ValueError,"original|source"):
                b20.patch_child(child,json.dumps(p).encode(),"AF121_5","normalized")

    def test_illegal_target_or_mutation_mode_fail_closed(self):
        child,parent,*_=fixture("AF121_5")
        for t,mode in (("HC11210_3","normalized"),("AF121_5","removed"),
                       ("AF121_6","flattened")):
            with self.assertRaisesRegex(ValueError,"unknown model/mode"):
                b20.patch_child(child,parent,t,mode)

    def test_source_case_stages_and_legal_top_slab_preserved(self):
        for t in b20.TARGETS:
            b20.set_target(t)
            self.assertEqual(b19.VERSION,b20.VERSION)
            self.assertEqual(set(b19.cameras()),{"south","north","east","west"})
            self.assertEqual(len(b19.stages()),4)
            self.assertEqual(b19.coords()[1],120)
            if t=="AF123_5":
                self.assertEqual(b19.support("chair_plus_slab_before"),
                                 "minecraft:oak_slab[type=top]")
                self.assertEqual(b19.support("slab_only"),
                                 "minecraft:oak_slab[type=top]")

    def test_three_way_measure_changes_new_geometry_without_false_outside_failure(self):
        for t in b20.TARGETS:
            b20.set_target(t)
            base={v:{s:scene(s) for s in b19.stages()} for v in b19.VIEWS}
            flat={v:{s:scene(s) for s in b19.stages()} for v in b19.VIEWS}
            norm={v:{s:scene(s,extra=s in (b19.stages()[0],b19.stages()[2]))
                     for s in b19.stages()} for v in b19.VIEWS}
            m=b20.compare_three(base,flat,norm)
            self.assertEqual(b20.decision(m),
                             "PASS_BOUNDED_REVERSED_X_ENDPOINT_NORMALIZATION_RENDER_RESPONSE")
            for x in m.values():
                self.assertEqual(set(x["original_vs_flattened_all_four_stage_pixels"]),set(b19.stages()))
                self.assertEqual(sum(x["original_vs_flattened_all_four_stage_pixels"].values()),0)
                self.assertGreater(x["normalized_vs_flattened_before_pixels"],0)
                self.assertEqual(x["normalized_vs_flattened_before_pixels"],
                                 x["normalized_vs_flattened_after_pixels"])
                self.assertEqual(x["normalized_difference_outside_union_of_both_chair_foregrounds_pixels"],0)

    def test_flatten_drift_prevents_a_causal_claim(self):
        m={"south":{
            "original_vs_flattened_all_four_stage_pixels":{k:0 for k in b19.stages()},
            "normalized_vs_flattened_before_pixels":12,
            "normalized_vs_flattened_after_pixels":12,
            "unmodified_negative_control_pixels":0,
            "unmodified_air_and_slab_pixels":0,
            "flattened_A_A_temporal_pixels":0,
            "normalized_A_A_temporal_pixels":0,
            "normalized_difference_outside_union_of_both_chair_foregrounds_pixels":0,
        }}
        self.assertEqual(b20.decision(m),
                         "PASS_BOUNDED_REVERSED_X_ENDPOINT_NORMALIZATION_RENDER_RESPONSE")
        m["south"]["original_vs_flattened_all_four_stage_pixels"][b19.stages()[0]]=1
        self.assertEqual(b20.decision(m),"CONDITIONAL_FAILED_FLATTEN_OR_RENDER_CONTROLS")

    def test_zero_screen_response_not_promoted_as_proven_source(self):
        m={"south":{
            "original_vs_flattened_all_four_stage_pixels":{k:0 for k in b19.stages()},
            "normalized_vs_flattened_before_pixels":0,
            "normalized_vs_flattened_after_pixels":0,
            "unmodified_negative_control_pixels":0,
            "unmodified_air_and_slab_pixels":0,
            "flattened_A_A_temporal_pixels":0,
            "normalized_A_A_temporal_pixels":0,
            "normalized_difference_outside_union_of_both_chair_foregrounds_pixels":0,
        }}
        self.assertEqual(b20.decision(m),
                         "NO_VISIBLE_RESPONSE_AFTER_ORIGINAL_X_ENDPOINT_NORMALIZATION")

    def test_no_fake_audit_without_actual_game_screenshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            for t in b20.TARGETS:
                with self.assertRaises(FileNotFoundError):
                    b20.audit(tmp,t)

    def test_source_and_rights_are_unchanged_and_jar_never_distributed(self):
        code=Path(b20.__file__).read_text(encoding="utf-8")
        for value in (
            "original_X_reversed_source5_root_cause_exclusively_proven",
            "source_face_UV_exclusive_GPU_pixel_ownership_approved",
            "physical_function_material_style_approved",
            "INT6_AI_training_redistribution_rights_approved",
            '"H03":"HOLD"','"H05":"CONDITIONAL"',
            '"F70_unconditional_approved":0',
            "original_release_JAR_or_artwork_distributed",
        ):
            self.assertIn(value,code)

if __name__=="__main__":
    unittest.main()
