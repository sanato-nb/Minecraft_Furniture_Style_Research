"""INT-5-B8: PINNED official Handcrafted 4.0.3 source model preflight.

No guess based on names: resolve each real released model parent and texture
alias, identify the original F2 blockstate from the released blockstate table,
and verify a distinct untouched white-cushion control before modifying anything.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

MOD="handcrafted-fabric-1.21.1-4.0.3.jar"
SHA1="a9579fecd7ed429c282be21d5c921d220197acc6"
CASE="HC11210_north"
CHILD="handcrafted:block/warped_chair_black"
CONTROL="handcrafted:block/warped_chair_white"
STATE="handcrafted:warped_chair[facing=north,color=black,waterlogged=false]"
CTRL_STATE="handcrafted:warped_chair[facing=north,color=white,waterlogged=false]"
ORIGINAL="assets/handcrafted/blockstates/warped_chair.json"
ELEMENT=12
PREFIX="assets/handcrafted/models/"
SOURCE_PARENT_BLOB="c5d9fbc054a897673f972fe2559376123751ba9b"

def require(cond,why):
    if not cond:raise ValueError("INT5-B8 PRECHECK: "+why)

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def member(name):
    namespace,colon,path=name.partition(":")
    require(colon and namespace=="handcrafted" and path and
            ".." not in path.split("/"),"invalid original HC model parent")
    return f"assets/{namespace}/models/{path}.json"

def resolve(resources,selected):
    path=member(selected)
    seen=[]
    layers=[]
    for _ in range(12):
        require(path in resources and path not in seen,
                "original selected HC model missing or cyclic "+path)
        seen.append(path)
        doc=json.loads(resources[path].decode("utf-8-sig"))
        require(isinstance(doc,dict),"original model document malformed")
        layers.append((path,doc))
        if "elements" in doc:
            require(isinstance(doc["elements"],list),
                    "source elements is not a list")
            return layers, doc["elements"]
        parent=doc.get("parent")
        require(isinstance(parent,str) and parent.startswith("handcrafted:"),
                "unexpected external parent or no elements")
        path=member(parent)
    raise ValueError("INT5-B8 model parent exceeded known bounded chain")

def parse_state(s):
    block,_,props=s.partition("[")
    require(block=="handcrafted:warped_chair" and props.endswith("]"),
            "unsupported HC source state")
    result={}
    for part in props[:-1].split(","):
        k,sep,v=part.partition("=")
        require(sep and k not in result and v,"bad state props")
        result[k]=v
    return result

def select_variant(states,blockstate):
    desired=parse_state(blockstate)
    all_options=states.get("variants")
    require(isinstance(all_options,dict) and len(all_options)==136,
            "HC source blockstate must have 136 original variants")
    matched=[]
    for key, option in all_options.items():
        props=dict(x.split("=",1) for x in key.split(","))
        if props==desired:matched.append((key,option))
    require(len(matched)==1,"missing/ambiguous exact original state selection")
    return matched[0]

def original_release_preflight(jar):
    data=Path(jar).read_bytes()
    require(hashlib.sha1(data).hexdigest()==SHA1,
            "official 4.0.3 Handcrafted JAR sha1 mismatch")
    with ZipFile(io.BytesIO(data)) as arc:
        names=arc.namelist()
        require(len(set(names))==len(names) and arc.testzip() is None,
                "official JAR duplicate names/CRC")
        resources={name:arc.read(name) for name in names
                   if name.startswith("assets/handcrafted/models/") and
                   name.endswith(".json")}
        states=arc.read(ORIGINAL)
    state=json.loads(states.decode("utf-8-sig"))
    actual_state={}
    for name,properties,model in (
        ("black",STATE,CHILD),("white",CTRL_STATE,CONTROL)
    ):
        key,selected=select_variant(state,properties)
        require(isinstance(selected,dict) and selected.get("model")==model,
                "selected source model differs from F2 original "+name)
        require(selected.get("x",0)==0 and selected.get("uvlock",False) is False,
                "unexpected original source x rotation or UV lock")
        actual_state[name]={"selector":key,"model":selected["model"],
                            "y":selected.get("y",0)}
    black,geo=resolve(resources,CHILD)
    white,controlgeo=resolve(resources,CONTROL)
    require(len(geo)==13 and sum(len(x.get("faces",{})) for x in geo)==78
            and len(geo[ELEMENT].get("faces",{}))==6,
            "original selected black chair does not have exact 13/78/index12=6")
    original_provider=black[-1][0]
    black_paths=[p for p,_ in black]
    white_paths=[p for p,_ in white]
    # Original seat cuboid must actually reference a cushion slot resolved
    # from the released child + any parent textures, not just role name.
    aliases={}
    for _,doc in reversed(black):
        aliases.update(doc.get("textures",{}))
    def texref(v):
        seen=set()
        while v.startswith("#"):
            need=v[1:]
            require(need in aliases and need not in seen,
                    "unbound/cyclic actual cushion slot")
            seen.add(need)
            v=aliases[need]
        return v
    cushion=[texref(face["texture"]) for face in geo[ELEMENT]["faces"].values()]
    require(any("chair/cushion/black_cushion" in path for path in cushion),
            "actual index12 does not bind original black cushion texture")
    white_aliases={}
    for _,doc in reversed(white):white_aliases.update(doc.get("textures",{}))
    # Distinct white child ensures target-only patch has an independent control.
    require(white_paths[0]!=black_paths[0],
            "white control must use a distinct unmodified model")
    actual={
        "schema":"MCFR_INT5_B8_PINNED_HC_RELEASE_SOURCE_PREFLIGHT/v1",
        "official_jar_sha1":SHA1,"official_jar_name":MOD,
        "source_case":CASE,
        "original_black_case":actual_state["black"],
        "original_white_control_case":actual_state["white"],
        "black_model_chain":black_paths,
        "white_model_chain":white_paths,
        "original_black_provider":original_provider,
        "original_black_provider_git_blob_sha1":blob(resources[original_provider]),
        "research_source_provider_study_blob_sha1":SOURCE_PARENT_BLOB,
        "source_provider_study_and_released_bytes_equal":blob(resources[original_provider])==SOURCE_PARENT_BLOB,
        "black_child_original_blob_sha1":blob(resources[black_paths[0]]),
        "white_child_original_blob_sha1":blob(resources[white_paths[0]]),
        "original_black_13_elements_78_faces":True,
        "source_element_index":ELEMENT,"source_element_face_count":6,
        "source_element_from":geo[ELEMENT].get("from"),
        "source_element_to":geo[ELEMENT].get("to"),
        "source_element_texture_resources":cushion,
        "original_runtime_black_texture_aliases":aliases,
        "white_control_distinct_child":True,
        "white_control_provider":white[-1][0],
        "original_source_jars_or_assets_exported":False,
        "part_function_or_material_approved":False,
        "INT6_rights_approved":False,
    }
    return actual

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(original_release_preflight(args.jar),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":main()
