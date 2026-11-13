#!/usr/bin/env python3
"""TEX02-R013 source-pinned model-choice and weighted-selector audit.

Run against the USER-EXTRACTED Minecraft 1.21.11 classfiles and assets:
    python VERIFY_R013_SELECTION.py --root 1.21.11 --out r013_check

Only standard Python 3 required. This verifies bytecode file identity plus
selected bytecode patterns, reconstructs 31 JSON choice slots, 19 state
groups and 29 structural outcomes. It does NOT execute the Minecraft client,
its RNG, its model baker, or any GPU render.
"""
import argparse
import csv
import hashlib
import json
from collections import OrderedDict
from pathlib import Path

BLOBS = {
    "hqf.class": "f9ea4f2c0ac5456e852f705786a4b3903e423590",
    "hqf$b.class": "dcf525c8779e72c7483993af2acd96035034552c",
    "hqh$b.class": "3ae60215f10fc5433e4ea5ff37ef8fe8aee2d714",
    "hqo$a.class": "eebeaca62efbd4332cabed9b222e1d23d900c7f6",
    "ioj$a.class": "f3975f20278d18a39303d81393686ff0c3de6c01",
    "ioj.class": "d6f961ace90f5846affd9f05498a5b90781e83ae",
    "cbm.class": "b955e5a65fe391aca206f86e844e398fbe110535",
    "cbn.class": "06beacc3dbb751045895507672a2015e0aaec596",
    "cbn$c.class": "4beaebeeee6ad3b740c093c6c68e779800f99aba",
    "cbn$b.class": "5736524f3f20852a4913ad0d26742aa71ea7cf01",
    "bgr.class": "c5dda84653eb3ff0088cb6d9a0f26b2a7c79e44d",
    "hqn.class": "c72e56d607e70925eb6d1aa98a395a7b9e0d5579",
    "hqm.class": "95cb65ef4868307e8d2a0696be33e78ef2327a31",
    "inw.class": "0e9d9dc53507d3ed87ba73bb268cd6305ab8633f",
    "inw$a.class": "0c8e5d9e66043f4b24681290493dc2e219c2af69",
    "iof.class": "836b9d3e3f6b4e30aba767af49d557a5eb16ead3",
    "hqb.class": "6c8c5d47f5092f8a884737c22eb3ef51bde53603",
    "cbo.class": "b429bf95b79329d8afe2934046a15bc3b227a2b2",
}
BLOCKS = """
stone cobblestone stone_bricks deepslate_bricks polished_andesite bricks
tuff_bricks granite polished_granite diorite polished_diorite andesite
deepslate deepslate_tiles blackstone polished_blackstone chiseled_stone_bricks
""".split()
# These are METHOD opcode sequences decoded from the expected classfiles.
# Full Git-blob hash is checked before using them.
CODE_PATTERNS = {
    "hqh$b.class": [bytes.fromhex("b2 00 fc 12 fe 04 b8 01 04")], # Codec weight=1
    "ioj.class": [bytes.fromhex("2a b4 00 16 2b b6 00 35 c0 00 06")],
    "cbn.class": [bytes.fromhex("2b 2a b4 00 4c b9 00 9d 02 00")],
    "cbn$c.class": [bytes.fromhex("b8 00 34")], # Arrays.fill repeated weight slots
    "hqn.class": [bytes.fromhex("b9 00 96 01 00")], # inw.c
    "inw$a.class": [bytes.fromhex("2a bb 00 0b 59 23 24 25")],
}
def git_sha(blob):
    return hashlib.sha1(b"blob " + str(len(blob)).encode("ascii") + b"\x00" + blob).hexdigest()

def verify_classes(root):
    for file, expected in BLOBS.items():
        raw = (root / file).read_bytes()
        assert raw[:4] == bytes.fromhex("cafebabe"), file
        digest = git_sha(raw)
        assert digest == expected, (file, "unexpected source revision", digest)
        for seq in CODE_PATTERNS.get(file, []):
            assert seq in raw, (file, "required source opcode fragment missing")
    # R013 only verifies that inw$a is an interface with an abstract Vec3 method;
    # it does NOT identify which implementation is used by the game runtime.
    return len(BLOBS)

def write_table(path, rows):
    assert rows
    with path.open("w", newline="", encoding="utf8") as h:
        w=csv.DictWriter(h, fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def run(root,out):
    classes=verify_classes(root)
    slots,groups,unique=[],[],[]
    for block in BLOCKS:
        source_path=root/"assets"/"minecraft"/"blockstates"/(block+".json")
        source_bytes=source_path.read_bytes()
        doc=json.loads(source_bytes)
        assert "variants" in doc and "multipart" not in doc, block
        for prop,value in doc["variants"].items():
            array=isinstance(value,list)
            choices=value if array else [value]
            assert choices, block
            vals=[int(x.get("weight",1)) for x in choices]
            assert all(n>0 for n in vals),block
            total=sum(vals)
            counted=OrderedDict()
            for index,(opt,weight) in enumerate(zip(choices, vals)):
                assert "weight" not in opt,(block,prop,index)
                key=(opt["model"],int(opt.get("x",0)),int(opt.get("y",0)),
                     int(opt.get("z",0)),bool(opt.get("uvlock",False)))
                if key not in counted:
                    counted[key]={"count":0,"weight":0,"indices":[]}
                counted[key]["count"]+=1
                counted[key]["weight"]+=weight
                counted[key]["indices"].append(index)
                slots.append({
                    "block":block,"property":prop,"index":index,
                    "model":key[0],"x":key[1],"y":key[2],"z":key[3],"uvlock":key[4],
                    "source_weight_explicit":False,"effective_weight":weight,
                    "group_total_weight":total,
                    "conditional_probability":f"{weight}/{total}",
                    "conditional_probability_percent":f"{100*weight/total:.3f}",
                    "runtime_observed":False
                })
            groups.append({
                "block":block,"property":prop,"is_json_array":array,
                "choices":len(choices),"total_weight":total,
                "unique_structural_outcomes":len(counted),
                "selector_class":"ioj" if array else "hqo",
                "optimized_cbNc_for_this_group":array and total<64,
                "runtime_sample_count":0,
                "source_json_git_blob":git_sha(source_bytes)
            })
            for key,aggregate in counted.items():
                unique.append({
                    "block":block,"property":prop,"model":key[0],
                    "x":key[1],"y":key[2],"z":key[3],"uvlock":key[4],
                    "source_indices":":".join(map(str,aggregate["indices"])),
                    "aggregate_weight":aggregate["weight"],
                    "total_weight":total,
                    "conditional_probability":f"{aggregate['weight']}/{total}",
                    "conditional_probability_percent":f"{100*aggregate['weight']/total:.3f}",
                    "runtime_observed":False
                })
    assert len(BLOCKS)==17 and len(slots)==31 and len(groups)==19 and len(unique)==29
    assert sum(g["is_json_array"] for g in groups)==4
    assert sum(g["choices"]==1 for g in groups)==15
    assert all(g["total_weight"] in (1,4) for g in groups)
    assert all(g["optimized_cbNc_for_this_group"] for g in groups if g["is_json_array"])
    x=[r for r in unique if r["block"]=="deepslate" and r["property"]=="axis=x"]
    assert len(x)==2 and all(r["aggregate_weight"]==2 for r in x)
    assert sorted([r["source_indices"] for r in x])==["0:2","1:3"]
    out.mkdir(parents=True,exist_ok=True)
    write_table(out/"R013_REGENERATED_31_CHOICE_SLOTS.csv",slots)
    write_table(out/"R013_REGENERATED_19_GROUPS.csv",groups)
    write_table(out/"R013_REGENERATED_29_OUTCOMES.csv",unique)
    print(json.dumps({
        "client_class_source_git_sha_verified":classes,
        "blockstate_jsons_parsed":len(BLOCKS),
        "variant_entries":len(slots),
        "group_count":len(groups),"weighted_array_group_count":4,
        "singleton_group_count":15,"unique_model_rotation_uv_outcomes":len(unique),
        "deepslate_axis_x_structural_outcomes":2,
        "deepslate_axis_x_each_conditional_probability":"2/4",
        "actual_minecraft_rng_calls_executed":0,
        "actual_minecraft_render_verified":0
    },indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True,help="User-extracted 1.21.11 folder")
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    run(a.root,a.out)
