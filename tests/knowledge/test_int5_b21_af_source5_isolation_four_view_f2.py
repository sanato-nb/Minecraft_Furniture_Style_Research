"""B21 source element5 isolation requires four true Fabric clients and controls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image,ImageDraw

from mcfr import int5_b19_four_unresolved_four_view_f2 as b19
from mcfr import int5_b20_af_reversed_x_three_session_f2 as b20
from mcfr import int5_b21_af_source5_isolation_four_view_f2 as b21

FACE_COUNTS = (5,5,5,5,6,4,4,2,5,5)

def fixture(target):
    pin=b20.PIN[target]
    faces=("north","south","east","west","up","down")
    parent={"elements":[
        {"from":[i,1,1],"to":[i+1,2,2],
         "faces":{f:{"texture":"#wood","uv":[0,0,1,1]}
                  for f in faces[:count]}}
        for i,count in enumerate(FACE_COUNTS)
    ]}
    parent["elements"][5]["from"]=pin["from"][:]
    parent["elements"][5]["to"]=pin["to"][:]
    child={"parent":"another_furniture:block/template/chair"+(
         "_tucked" if target=="AF123_5" else ""),
         "textures":{"wood":"another_furniture:block/chair/bottom/acacia"}}
    return (json.dumps(child).encode(),json.dumps(parent).encode(),
            parent,child)

def scene(target,mode,visible=True,shift=0):
    b21.set_target(target)
    x=Image.new("RGB",(1024,684),(200,200,200))
    d=ImageDraw.Draw(x)
    if visible and mode in ("original_5","normalized_5","positive_6"):
        d.rectangle((470+shift,400,496+shift,425),
                    fill={"original_5":(110,80,45),"normalized_5":(80,90,130),
                          "positive_6":(140,100,50)}[mode])
    return x

def frames(target,positive=True,original=False,normalized=False,
           temporal_drift=False,negative_drift=False):
    b21.set_target(target)
    a,negative,b,air=b19.stages()
    data={}
    for mode in b21.MODES:
        show={"no_faces_5":False,"original_5":original,
              "normalized_5":normalized,"positive_6":positive}[mode]
        data[mode]={}
        for view in b19.VIEWS:
            first=scene(target,mode,show)
            last=scene(target,mode,show,1 if temporal_drift and mode=="original_5" else 0)
            nothing=scene(target,mode,False)
            ctrl=scene(target,mode,negative_drift and mode=="original_5")
            data[mode][view]={a:first,b:last,negative:ctrl,air:nothing}
    return data

class B21SourceIsolationTests(unittest.TestCase):
    def tearDown(self):
        b21.set_target("AF121_5")

    def test_only_two_original_unresolved_source5_targets(self):
        self.assertEqual(b21.TARGETS,("AF121_5","AF123_5"))
        self.assertEqual(b21.MODES,
                         ("no_faces_5","original_5","normalized_5","positive_6"))
        for t in b21.TARGETS:
            self.assertEqual(b21.source_identity(t)["source_faces"],4)

    def test_never_empty_elements_array_inherits_parent(self):
        for t in b21.TARGETS:
            child,parent,*_=fixture(t)
            for mode in b21.MODES:
                raw,info=b21.patch_child(child,parent,t,mode)
                self.assertEqual(len(json.loads(raw)["elements"]),1)
                self.assertTrue(info["no_empty_elements_array_inheritance_fallback"])

    def test_exact_original_element5_and_all_its_original_faces(self):
        for t in b21.TARGETS:
            child,parent,p,orig=fixture(t)
            raw,info=b21.patch_child(child,parent,t,"original_5")
            modified=json.loads(raw)
            self.assertEqual(modified["elements"],[p["elements"][5]])
            self.assertEqual({k:v for k,v in modified.items() if k!="elements"},orig)
            self.assertEqual(info["result_face_count"],4)
            self.assertEqual(info["unselected_original_elements_removed"],9)

    def test_faceless_model_keeps_geometry_without_any_quad(self):
        for t in b21.TARGETS:
            child,parent,p,*_=fixture(t)
            raw,info=b21.patch_child(child,parent,t,"no_faces_5")
            e=json.loads(raw)["elements"][0]
            self.assertEqual(e["faces"],{})
            self.assertEqual(e["from"],p["elements"][5]["from"])
            self.assertEqual(e["to"],p["elements"][5]["to"])
            self.assertEqual(info["result_face_count"],0)

    def test_normalized_model_changes_only_original_source5_x(self):
        for t in b21.TARGETS:
            child,parent,p,*_=fixture(t)
            raw,info=b21.patch_child(child,parent,t,"normalized_5")
            before=p["elements"][5]
            after=json.loads(raw)["elements"][0]
            self.assertEqual(after["from"],[3,*before["from"][1:]])
            self.assertEqual(after["to"],[13,*before["to"][1:]])
            self.assertEqual(after["faces"],before["faces"])
            self.assertTrue(info["all_result_face_objects_from_original_source"])

    def test_positive6_keeps_original_four_faces_and_original_coords(self):
        for t in b21.TARGETS:
            child,parent,p,*_=fixture(t)
            raw,info=b21.patch_child(child,parent,t,"positive_6")
            self.assertEqual(json.loads(raw)["elements"],[p["elements"][6]])
            self.assertEqual(info["selected_original_element_index"],6)

    def test_original_source_drift_or_illegal_mode_rejected(self):
        child,parent,p,*_=fixture("AF121_5")
        with self.assertRaisesRegex(ValueError,"invalid"):
            b21.patch_child(child,parent,"HC11210_3","original_5")
        with self.assertRaisesRegex(ValueError,"invalid"):
            b21.patch_child(child,parent,"AF121_5","elements_empty")
        for change in (
            lambda x:x["elements"][5]["from"].__setitem__(0,12),
            lambda x:x["elements"][5]["faces"].pop("north"),
            lambda x:x["elements"].append(copy.deepcopy(x["elements"][0])),
            lambda x:x["elements"][6]["faces"].pop("south")):
            q=copy.deepcopy(p)
            change(q)
            with self.assertRaises(ValueError):
                b21.patch_child(child,json.dumps(q).encode(),"AF121_5","original_5")

    def test_original5_visible_only_is_bounded_context_specific(self):
        for t in b21.TARGETS:
            m=b21.metrics_for_views(frames(t,original=True,normalized=True))
            self.assertEqual(b21.decision(m),
                             "VISIBLE_ORIGINAL_SOURCE5_ONLY_NOT_VISIBLE_IN_FULL_MODEL")
            self.assertGreater(m["east"]["original_5"]["isolation_before_changed_pixels"],0)

    def test_normalized_only_visible_is_not_full_model_bug_proof(self):
        for t in b21.TARGETS:
            m=b21.metrics_for_views(frames(t,original=False,normalized=True))
            self.assertEqual(b21.decision(m),
                             "ONLY_NORMALIZED_SOURCE5_VISIBLE_IN_ISOLATION")

    def test_no_source5_visible_even_isolated_with_positive6(self):
        for t in b21.TARGETS:
            m=b21.metrics_for_views(frames(t))
            self.assertEqual(b21.decision(m),
                             "ORIGINAL_AND_NORMALIZED_SOURCE5_NOT_VISIBLE_EVEN_ISOLATED")

    def test_missing_positive_or_bad_control_prevents_pass(self):
        t="AF121_5"
        self.assertEqual(b21.decision(b21.metrics_for_views(frames(t,positive=False))),
                         "CONDITIONAL_FAILED_POSITIVE6_VISIBLE_MODEL_CONTROL")
        self.assertEqual(b21.decision(b21.metrics_for_views(
             frames(t,temporal_drift=True,original=True))),
             "CONDITIONAL_FAILED_TEMPORAL_OR_NEGATIVE_F2_CONTROLS")
        self.assertEqual(b21.decision(b21.metrics_for_views(
             frames(t,negative_drift=True,original=True))),
             "CONDITIONAL_FAILED_TEMPORAL_OR_NEGATIVE_F2_CONTROLS")

    def test_real_game_manifest_required_and_four_view_legal_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            for t in b21.TARGETS:
                with self.assertRaises(FileNotFoundError):
                    b21.audit(tmp,t)
                b21.set_target(t)
                self.assertEqual(set(b19.cameras()),set(b19.VIEWS))
                self.assertEqual(len(b19.stages()),4)
                if t=="AF123_5":
                    self.assertEqual(b19.support(b19.stages()[0]),
                                     "minecraft:oak_slab[type=top]")

    def test_rights_meaning_and_original_b19_b20_gates_never_promoted(self):
        code=Path(b21.__file__).read_text(encoding="utf-8")
        for phrase in (
            '"H03":"HOLD"','"H05":"CONDITIONAL"',
            '"F70_unconditional_approved":0',
            '"source5_function_material_style_approved":False',
            '"source5_exclusive_original_face_UV_GPU_pixel_ownership_approved":False',
            '"third_party_AI_training_and_redistribution_rights_approved":False',
            '"B19_43_of_45_bounded_render_response_unchanged":True',
        ):
            self.assertIn(phrase,code)

if __name__=="__main__":
    unittest.main()
