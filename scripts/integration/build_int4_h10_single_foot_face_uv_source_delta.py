#!/usr/bin/env python3
"""INT-4-H10 original source detailed face-UV delta of occupied fancy bed foot.

Static model source. Four changed element records, 24 face UV records;
NOT a rendered screenshot or GPU pixel-to-UV provenance.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,io,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
H9="scripts/integration/build_int4_h9_hc_bed_occupied_model_delta.py"
H9_AUDIT="project/integration/INT4_H9_HC_BED_OCCUPIED_SOURCE_AUDIT_V1.json"
H9_AUDIT_GIT_BLOB="f6e5db38c22ed66d29d18c430336ef0e8f29d78e"
MODELROOT="common/src/main/resources/assets/handcrafted/models/block/fancy_bed/"
F0=MODELROOT+"bed_single.json"
F1=MODELROOT+"bed_single_occupied.json"
ELEMENTS="project/integration/INT4_H10_OCCUPIED_SINGLE_FOOT_FOUR_ELEMENT_CHANGES_V1.csv"
FACES="project/integration/INT4_H10_OCCUPIED_SINGLE_FOOT_24_SOURCE_FACE_UV_V1.csv"
REPORT="project/integration/INT4_H10_OCCUPIED_SINGLE_FOOT_FACE_UV_SOURCE_AUDIT_V1.json"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def assertion(ok,message):
    if not ok:raise AssertionError(message)
def h9_import():
    spec=importlib.util.spec_from_file_location("mcfr_h10_facedelta_source_h9",ROOT/H9)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def original_h9():
    b=(ROOT/H9_AUDIT).read_bytes()
    assertion(blob(b)==H9_AUDIT_GIT_BLOB,"H9 original source audit changed")
    d=json.loads(b)
    assertion(d["status"]=="PASS_1024_STATE_512_PAIR_256_MODEL_FOOT_GEOMETRY_SOURCE_VALIDATED",
              "H9 source population not verified")
    assertion(d["counts"]["occupied_false_true_pairs"]==512,"H9 paired states changed")
    assertion(d["counts"]["new_occupied_true_native_F2"]==0,
              "H9 evidence scope drift")
    return d
def compare_elements(previous,next_model):
    old=previous["elements"]
    new=next_model["elements"]
    key=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    past=Counter(key(x) for x in old)
    current=Counter(key(x) for x in new)
    removed=list((past-current).elements())
    added=list((current-past).elements())
    assertion((len(old),len(new),len(removed),len(added))==(12,14,1,3),
              "single foot source element change unexpected")
    return [("removed",json.loads(x)) for x in removed]+[
           ("added",json.loads(x)) for x in added]
def csv_bytes(rows):
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return out.getvalue().encode("utf-8")
def json_bytes(data):
    return (json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+"\n").encode("utf-8")
def stage(path,b,verify):
    p=ROOT/path
    if verify:assertion(p.exists() and p.read_bytes()==b,"H10 source audit changed "+path)
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def build(source_zip,verify=False):
    h9=h9_import()
    origin=original_h9()
    z=h9.SourceZip(source_zip)
    old=z.read(F0);new=z.read(F1)
    assertion(blob(z.raw(F0))=="01dcc76679443d37f3efa45d974e2acbc071cfc1","source old SHA")
    assertion(blob(z.raw(F1))=="296e103447bfaaa6dd5d3a20d39169c1612474bc","source true SHA")
    assertion(old.get("parent")==new.get("parent"),"parent level changed")
    assertion(old.get("textures")==new.get("textures"),"texture slot bindings changed")
    changes=compare_elements(old,new)
    element_rows=[];face_rows=[]
    for i,(action,element) in enumerate(changes):
        rotation=element.get("rotation",{})
        face_details=element.get("faces",{})
        assertion(len(face_details)==6,"changed element face count not six")
        idx=f"{action}_{i+1:02d}"
        element_rows.append({
          "change_id":idx,"disposition":action,
          "from_xyz":json.dumps(element["from"],separators=(",",":")),
          "to_xyz":json.dumps(element["to"],separators=(",",":")),
          "rotation_axis":rotation.get("axis",""),
          "rotation_degrees":rotation.get("angle",0),
          "rotation_origin_xyz":json.dumps(rotation.get("origin",[]),separators=(",",":")),
          "source_face_count":len(face_details),
          "source_element_sha256":sha(json.dumps(element,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")),
          "source_parent_model":F0 if action=="removed" else F1,
          "renderer_pixel_face_UV_proved":"false",
        })
        for name in sorted(face_details):
            f=face_details[name]
            face_rows.append({
              "change_id":idx,"disposition":action,"face":name,
              "face_source_texture_slot":f.get("texture",""),
              "UV_raw":json.dumps(f.get("uv",[]),separators=(",",":")),
              "face_UV_rotation":f.get("rotation",0),
              "cullface":f.get("cullface",""),
              "tintindex":f.get("tintindex",""),
              "element_rotation_axis":rotation.get("axis",""),
              "element_rotation_degrees":rotation.get("angle",0),
              "renderer_pixel_to_face_association":"NOT_VERIFIED",
            })
    assertion(len(element_rows)==4 and len(face_rows)==24,"wrong source element-face delta counts")
    assert sum(x["disposition"]=="removed" for x in element_rows)==1
    assert sum(x["disposition"]=="added" for x in element_rows)==3
    # Two changed elements are tilted on the X axis; no inference about
    # actual face visibility, UV pixel mapping or material from #1 token.
    tilted=[x for x in element_rows if x["rotation_axis"]=="x"]
    assertion(len(tilted)==2 and all(x["rotation_degrees"]==22.5 for x in tilted),
              "tilted occupied source elements changed")
    assert all(x["face_source_texture_slot"]=="#1" for x in face_rows)
    data={
      "status":"PASS_PINNED_SINGLE_BED_FOOT_FOUR_CHANGED_ELEMENTS_24_SOURCE_FACE_UV",
      "schema":"MCFR_INT4_H10_HC_BED_OCCUPIED_SINGLE_SOURCE_FACE_DELTA/v1",
      "upstream_repo":"terrarium-earth/Handcrafted",
      "upstream_commit":h9.COMMIT,
      "H9_original_audit_git_blob_sha1":H9_AUDIT_GIT_BLOB,
      "original_parent_source_sha1":{"occupied_false":blob(z.raw(F0)),
                                      "occupied_true":blob(z.raw(F1))},
      "element_counts":{"occupied_false":12,"occupied_true":14,
                        "unchanged":11,"removed":1,"added":3},
      "face_counts":{"occupied_false":72,"occupied_true":84,
                     "removed_face_UV_records":6,"added_face_UV_records":18,
                     "changed_face_UV_records":24},
      "rotated_elements":{"added_x_axis_22_5_degree":2},
      "same_texture_slot_bindings":True,
      "scope":{
        "modeling_geometry_and_source_UV":True,
        "actual_occupied_F2_captured_here":False,
        "full_face_to_GPU_pixel_mapping_approved":False,
        "sleep_wake_destroy_gameplay_tested":False,
        "H03_H05_full_exit":False,
        "INT5_semantics_approved":0,
        "INT6_training_or_redistribution_approved":0,
      },
      "limits":[
         "Each face UV is copied as coordinate metadata from the pinned upstream model; raw model asset files are not stored.",
         "Element rotational origin and 22.5 degree tilt are source geometry, not observed screenshot pixels.",
         "Source model parent alone is not proof that the runtime occupied state persisted when photographed.",
         "No original Handcrafted textures or JAR bytes are redistributed."
      ],
    }
    outputs={ELEMENTS:csv_bytes(element_rows),FACES:csv_bytes(face_rows)}
    data["outputs_sha256"]={p:sha(v) for p,v in outputs.items()}
    outputs[REPORT]=json_bytes(data)
    for p,v in outputs.items():stage(p,v,verify)
    print(json.dumps({"status":data["status"],"elements":data["element_counts"],
                      "faces":data["face_counts"]},ensure_ascii=False))
    return data
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-zip",required=True,type=Path)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    build(args.source_zip,args.verify)
