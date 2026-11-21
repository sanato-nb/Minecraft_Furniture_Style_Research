"""INT-3 source-pinned chair blockstate selectors, rotations and F cross-audit.

This is not a Minecraft client bake or runtime validation. Reopen the *pinned*
upstream AF/HC/Macaw blockstate bytes, compare each rule and model option to
1-3-F, retain raw source selectors including odd cross-variant references,
and compute source-geometry diagnostic AABBs for 4 textured study chairs.

Do not "correct" a surprising model target: exact source mappings and
explicit mismatch candidates are the research result.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

from audit_int2_mod_textures import Sources,raw_source_sha
import render_int3_chair_geometry as geometry

ROOT=Path(__file__).resolve().parents[2]
BLOCKS=(
    ("AF","another_furniture","acacia_chair"),
    ("HC","handcrafted","warped_chair"),
    ("MACAW","mcwfurnitures","acacia_chair"),
)
STUDY_MODEL_KEYS={"AF121","AF123","HC11210","MACAW67"}
STUDY_PARENT_KEYS={"AF121":"AF1393","AF123":"AF1394",
                   "HC11210":"HC13","MACAW67":"MACAW1424"}
EXPECTED_FACE_COUNTS={"AF121":46,"AF123":46,"HC11210":78,"MACAW67":59}
DIRECTIONS=("north","east","south","west")
ROTATIONS=(0,90,180,270)

def raw_source_hash(mod,raw):
    return raw_source_sha(raw,"GIT_BLOB_SHA1" if mod in ("AF","HC") else "SHA256")

def strict_json(raw):
    def unique(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError("Original JSON has duplicate object key "+key)
            result[key]=value
        return result
    def nan(x):raise ValueError("Non-finite numeric constant in original JSON: "+x)
    return json.loads(raw.decode("utf-8-sig"),object_pairs_hook=unique,parse_constant=nan)

def selector_dict(selector):
    if selector=="":
        return {}
    items=selector.split(",")
    pairs=[part.split("=",1) for part in items]
    if any(len(p)!=2 or not p[0] or not p[1] for p in pairs):
        raise ValueError("Invalid source blockstate selector "+selector)
    result=dict(pairs)
    if len(result)!=len(items):raise ValueError("Repeated source selector field")
    return result

def state_index(db,mod,filename):
    suffix="/blockstates/"+filename+".json"
    rows=list(db.execute("""
      SELECT id,source_id,state_id,path,sha,kind
      FROM state WHERE source_id=? AND path LIKE ?
      ORDER BY id""",(mod,"%"+suffix)))
    if len(rows)!=1:
        raise ValueError(f"Expected exactly one source state {mod}/{filename}; found "+str(len(rows)))
    return rows[0]

def canonical_target(target,mod):
    if not isinstance(target,str) or not target:raise ValueError("Source model target not a string")
    return target if ":" in target else {"AF":"another_furniture","HC":"handcrafted","MACAW":"mcwfurnitures"}[mod]+":"+target

def original_options(source_value):
    seq=source_value if isinstance(source_value,list) else [source_value]
    if not seq or not all(isinstance(x,dict) for x in seq):
        raise ValueError("Invalid source variant blockstate options")
    return seq

def compare_state_rule(db,sid,selector,values,mod):
    incoming=selector_dict(selector)
    rules=list(db.execute("""
       SELECT rule_index,selector,condition,form
       FROM rule WHERE state_id=?""",(sid,)))
    known=[]
    for r in rules:
        try:
            if selector_dict(r["selector"])==incoming:
                known.append(r)
        except ValueError:
            if r["selector"]==selector:known.append(r)
    if len(known)!=1:
        raise ValueError(f"Cannot identify source variant selector in historical F: {mod}:{selector}; examples="+
                         str([(r["rule_index"],r["selector"]) for r in rules[:4]]))
    rule=known[0]
    options=list(db.execute("""
        SELECT o.option_index,o.model_key,o.unresolved_target,o.x,o.y,o.uvlock,o.weight,m.resource_id
        FROM option o LEFT JOIN model m ON m.model_key=o.model_key
        WHERE o.state_id=? AND o.rule_index=? ORDER BY o.option_index
    """,(sid,rule["rule_index"])))
    original=original_options(values)
    if len(options)!=len(original):
        raise ValueError("F option count differs from original source: "+mod+":"+selector)
    result=[]
    for n,(o,src) in enumerate(zip(options,original)):
        if int(o["option_index"])!=n:
            raise ValueError("F option_index is not original source ordering")
        target=canonical_target(src["model"],mod)
        actual=o["resource_id"] if o["model_key"] else o["unresolved_target"]
        if actual!=target:
            raise ValueError(f"Original blockstate model target differs: {mod} {selector} ({actual} != {target})")
        expected=(int(src.get("x",0)),int(src.get("y",0)),
                  int(bool(src.get("uvlock",False))),int(src.get("weight",1)))
        recorded=(int(o["x"]),int(o["y"]),int(o["uvlock"]),int(o["weight"]))
        if expected!=recorded:
            raise ValueError(f"Original blockstate option x/y/uvlock/weight differs: {mod} {selector} {recorded}/{expected}")
        if any(v%90!=0 for v in expected[:2]):
            raise ValueError("Original non-quarter-turn option is outside conservative pose scope")
        result.append({"model_key":o["model_key"] or "",
                       "model_resource_id":target,
                       "x":expected[0],"y":expected[1],"uvlock":expected[2],
                       "weight":expected[3],"option_index":n,
                       "rule_index":int(rule["rule_index"])})
    return result

def anomalous_variant_groups(variant_records):
    """Note cross-facing model changes inside otherwise identical property groups.

    This is a *review flag*, not an error in the source or an automatic fix.
    """
    by=defaultdict(list)
    for row in variant_records:
        fields=selector_dict(row["selector"])
        facing=fields.pop("facing",None)
        if facing in DIRECTIONS and row["option_index"]==0:
            by[tuple(sorted(fields.items()))].append((facing,row))
    review=[]
    for props,entries in by.items():
        if len(entries)!=4:continue
        targets={r["model_resource_id"] for _,r in entries}
        if len(targets)<=1:continue
        majority=Counter(r["model_resource_id"] for _,r in entries).most_common()
        for facing,row in entries:
            review.append({
               "selector":row["selector"],"source_model":row["model_resource_id"],
               "group_props":",".join(k+"="+v for k,v in props),
               "facing":facing,"other_targets":"|".join(sorted(targets)),
               "review_reason":"SOURCE_CROSS_FACING_MODEL_TARGET_VARIATION",
               "status":"NOT_CORRECTED_REQUIRES_INTENT_REVIEW",
            })
    return review

def rotate_y(pos,angle):
    x,y,z=pos
    s=round(math.sin(math.radians(angle)))
    c=round(math.cos(math.radians(angle)))
    dx,dz=x-8,z-8
    return (8+c*dx+s*dz,y,8-s*dx+c*dz)

def bounds(cubes):
    pts=[p for cube in cubes for p in cube]
    if not pts:raise ValueError("Selected geometry has no elements")
    return tuple(min(p[i] for p in pts) for i in range(3))+tuple(
         max(p[i] for p in pts) for i in range(3))

def bbox_token(vals):
    return "|".join(f"{x:.6f}" for x in vals)

def model_pose_bounds(db,key,y):
    row=db.execute("""SELECT provider_key,face_instances FROM geometry WHERE model_key=?""",(key,)).fetchone()
    if row is None or row["provider_key"]!=STUDY_PARENT_KEYS[key]:
        raise ValueError("Child model geometry provider was changed")
    if int(row["face_instances"])!=EXPECTED_FACE_COUNTS[key]:
        raise ValueError("Original face count changed in fixed study model")
    shapes=[]
    for e in db.execute("""
      SELECT source_from,source_to,pivot,axis,angle,rescale FROM element
      WHERE provider_key=? ORDER BY element_index""",(row["provider_key"],)):
        raw=tuple(tuple(float(v) for v in e[name].split("|")) for name in ("source_from","source_to"))
        a,b=raw
        if len(a)!=3 or len(b)!=3:raise ValueError("Source element isn't a 3-D cuboid")
        shape={"a":a,"b":b,"axis":e["axis"],"angle":e["angle"],
               "pivot":tuple(float(v) for v in e["pivot"].split("|")) if e["pivot"] else (8,8,8),
               "rescale":bool(e["rescale"])}
        shapes.append([rotate_y(p,y) for p in geometry.cube_points(shape)])
    return bbox_token(bounds(shapes)),len(shapes)

def audit_one(db,sources,mod,namespace,name):
    registered=state_index(db,mod,name)
    raw=sources.fetch(mod,registered["path"])
    sha=raw_source_hash(mod,raw)
    if sha!=registered["sha"]:
        raise ValueError(f"Original {mod} blockstate SHA changed from F: {registered['path']}")
    original=strict_json(raw)
    if not isinstance(original,dict):
        raise ValueError("Blockstate root is not an object")
    if set(original)!={"variants"}:
        raise ValueError(f"Unmodeled source blockstate form in {mod} {name}: {list(original)}")
    variants=original["variants"]
    if not isinstance(variants,dict):
        raise ValueError("Source variants is not a dictionary")
    ledger=[]
    counts=Counter()
    for selector,body in variants.items():
        assignments=selector_dict(selector)
        if "facing" in assignments and assignments["facing"] not in DIRECTIONS:
            raise ValueError("Unexpected original orientation "+selector)
        options=compare_state_rule(db,registered["id"],selector,body,mod)
        for option in options:
            ledger.append({
              "source":mod,"state_id":registered["state_id"],
              "state_path":registered["path"],"state_sha":sha,
              "selector":selector,"facing":assignments.get("facing",""),
              **option,
            })
            counts["options"]+=1
            counts["y_"+str(option["y"])]+=1
            counts["x_"+str(option["x"])]+=1
            counts["uvlock_"+str(option["uvlock"])]+=1
    F_rules=db.execute("SELECT COUNT(*) FROM rule WHERE state_id=?",(registered["id"],)).fetchone()[0]
    F_options=db.execute("SELECT COUNT(*) FROM option WHERE state_id=?",(registered["id"],)).fetchone()[0]
    if F_rules!=len(variants) or F_options!=len(ledger):
        raise ValueError(f"Historical source state census mismatch: {mod}: F({F_rules},{F_options}) Original({len(variants)},{len(ledger)})")
    if len({r["selector"] for r in ledger})!=len(variants):
        raise ValueError("Original state included weighted/ambiguous options; visit option-level identity")
    anomalies=anomalous_variant_groups(ledger)
    return ledger,{
      "mod":mod,"resource_block":namespace+":"+name,
      "source_state_id":registered["state_id"],"source_path":registered["path"],
      "source_sha":sha,"variants":len(variants),"options":len(ledger),
      "unique_models":len({r["model_resource_id"] for r in ledger}),
      "source_option_stats":dict(sorted(counts.items())),
      "review_anomalous_selector_rows":len(anomalies),
      "review_groups":anomalies,
      "historical_F_mismatches":0,
    }

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("root","af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=name!="root",default=ROOT if name=="root" else None)
    args=parser.parse_args(argv)
    args.out.mkdir(parents=True,exist_ok=True)
    sources=Sources(args)
    db=geometry.load_db(args.root)
    try:
        states=[]
        reports=[]
        for mod,namespace,block in BLOCKS:
            rows,summary=audit_one(db,sources,mod,namespace,block)
            states.extend(rows)
            reports.append(summary)
        selected=defaultdict(list)
        for state in states:
            if state["model_key"] in STUDY_MODEL_KEYS:
                selected[state["model_key"]].append(state)
        if set(selected)!=STUDY_MODEL_KEYS:
            raise ValueError("One selected original model missing from source blockstate: "+
                             str({k:len(v) for k,v in selected.items()}))
        poses=[]
        for key in sorted(STUDY_MODEL_KEYS):
            for facing in DIRECTIONS:
                matches=[x for x in selected[key] if x["facing"]==facing]
                if not matches:raise ValueError("Missing original direction "+key+"/"+facing)
                # Prefer a primary observational state (waterlogged=false).
                # Other original variants remain in the full source audit CSV.
                matches.sort(key=lambda r:("waterlogged=true" in r["selector"],
                                           "variant=3" in r["selector"],r["selector"]))
                chosen=matches[0]
                if chosen["x"]!=0 or chosen["uvlock"]!=0:
                    raise ValueError("Current fixed chair face UV rotation needs an additional renderer")
                box,n=model_pose_bounds(db,key,chosen["y"])
                poses.append({
                    "model_key":key,"source_state":chosen["state_id"],
                    "selector":chosen["selector"],"facing":facing,
                    "model_resource_id":chosen["model_resource_id"],
                    "x":chosen["x"],"y":chosen["y"],"uvlock":chosen["uvlock"],
                    "source_geometry_elements":n,
                    "rotated_bbox_source_units":box,
                    "source_sha":chosen["state_sha"],
                    "runtime_renderer_verified":"NO",
                    "visual_role_verified":"NO",
                })
            original_bbox,_=model_pose_bounds(db,key,0)
            after_360,_=model_pose_bounds(db,key,360)
            if original_bbox!=after_360:
                raise ValueError("Four successive quarter turns fail source geometry closure "+key)
        bymod={r["mod"]:r for r in reports}
        rows_path=args.out/"INT3_CHAIR_ALL_SOURCE_BLOCKSTATE_OPTIONS.csv"
        fieldnames=list(states[0])
        with rows_path.open("w",newline="",encoding="utf-8") as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted(states,key=lambda x:(x["source"],x["state_id"],x["selector"],x["option_index"])))
        pose_path=args.out/"INT3_CHAIR_16_ORIENTATION_POSES.csv"
        with pose_path.open("w",newline="",encoding="utf-8") as file:
            writer=csv.DictWriter(file,fieldnames=list(poses[0]))
            writer.writeheader()
            writer.writerows(poses)
        counts=Counter(s["source"] for s in states)
        result={
          "schema":"MCFR_INT3_CHAIR_SOURCE_BLOCKSTATES_v1",
          "status":"PASS_PINNED_BLOCKSTATE_OPTIONS_AND_GEOMETRY_POSES_UNLESS_REVIEWED_EXCEPTIONS",
          "source_states":reports,
          "totals":{
             "original_states":len(reports),
             "original_variant_rules":sum(s["variants"] for s in reports),
             "original_model_options":len(states),
             "matched_historical_F_options":len(states),
             "study_child_models":len(selected),
             "study_orientation_pose_rows":len(poses),
             "source_anomaly_rows":sum(s["review_anomalous_selector_rows"] for s in reports)
          },
          "source_option_count_by_mod":dict(sorted(counts.items())),
          "selected_model_state_option_counts":{k:len(v) for k,v in sorted(selected.items())},
          "sha256":{
            "all_original_option_rows_csv":hashlib.sha256(rows_path.read_bytes()).hexdigest(),
            "selected_source_geometry_orientation_rows_csv":hashlib.sha256(pose_path.read_bytes()).hexdigest(),
          },
          "boundaries":{
            "original_blockstate_sha_and_F_option_alignment":"PASS",
            "original_geometry_provider_and_4_quarter_turn_bbox_closure":"PASS",
            "original_texture_face_recheck":"SEPARATE_PR31_229_FACES",
            "actual_minecraft_client_bake_or_gameplay_verified":False,
            "visually_verified_chair_role_count":0,
            "automatic_style_material_training_permission_count":0,
            "source_anomaly_corrections_applied":0,
            "rendering_and_uvlock_runtime_claims":"NONE",
          }
        }
        (args.out/"INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json").write_text(
            json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
        print("INT3_CHAIR_BLOCKSTATE_RESULT:"+json.dumps(result,sort_keys=True,ensure_ascii=False))
    finally:
        db.close()
        sources.close()

if __name__=="__main__":
    main()
