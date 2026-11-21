"""INT-2 1-4 independent exception UV pixel crops and child-slot audit.

Rechecks C_followup's unique source-region/frame samples directly from
original pinned sprite PNGs; validates all 6,202 statically unbound face
instances via a second, Python-indexed traversal of the pinned F SQLite,
not by invoking the original C_followup scripts.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
from fractions import Fraction
import hashlib
import io
import json
import lzma
from math import ceil,floor
from pathlib import Path
import sqlite3

from PIL import Image
from audit_int2_mod_textures import Sources,csv_rows,raw_source_sha,verify_png_crc

ROOT=Path(__file__).resolve().parents[2]
HANDOFF="research/furniture_mods/phase_1-3/F/1-3_TEXTURE_UV_HANDOFF.csv"
REGIONS="research/furniture_mods/phase_1-4/C_followup/UV_SOURCE_SUPPORT.csv.xz"
SUMMARY="research/furniture_mods/phase_1-4/C_followup/SUMMARY.json"
DB="research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz"
EXPECTED={
    "CLIPPED_RECT_SUPPORT":5142,
    "EDGE_CONTACT_SUPPORT":8,
    "LINE_SUPPORT":68850,
    "NO_PINNED_SPRITE_INTERSECTION":2,
    "POINT_SUPPORT":260,
}

def region_rows(path):
    with lzma.open(path,"rt",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def axis_uv(l,r,size):
    """Independent clamped closed-UV source-cell coverage with exact rationals."""
    low,high=min(l,r),max(l,r)
    if low==high:
        if low<0 or low>16:
            return None
        pos=low*size/16
        x0=max(0,ceil(pos)-1)
        x1=min(size,floor(pos)+1)
        kind="SPRITE_EDGE" if low in (0,16) else "TEXEL_EDGE" if pos.denominator==1 else "INTERIOR"
        return x0,x1,Fraction(1),kind
    clip_l=max(low,0)
    clip_r=min(high,16)
    if clip_l>clip_r:
        return None
    if clip_l==clip_r:
        k=0 if clip_l==0 else size-1
        return k,k+1,Fraction(0),"EDGE_CONTACT"
    return floor(clip_l*size/16),ceil(clip_r*size/16),(clip_r-clip_l)/(high-low),"SPAN"

def region_metrics(image):
    pix=image.tobytes()
    hist=Counter(pix[i:i+4] for i in range(0,len(pix),4))
    trans=sum(n for rgba,n in hist.items() if rgba[3]==0)
    partial=sum(n for rgba,n in hist.items() if 0<rgba[3]<255)
    opaque=sum(n for rgba,n in hist.items() if rgba[3]==255)
    visible=[(rgba,n) for rgba,n in hist.items() if rgba[3]>0]
    return {
        "transparent":trans,"partial_alpha":partial,"opaque":opaque,
        "visible_rgb":len({rgba[:3] for rgba,n in visible}),
        "dominant_rgba":"|".join(rgba.hex()+":"+str(n) for rgba,n in sorted(visible,key=lambda v:(-v[1],v[0]))[:4]),
        "rgba_sha256":hashlib.sha256(pix).hexdigest(),
    }

def verify_support(root,args):
    historical=region_rows(root/REGIONS)
    ledger=csv_rows(root/HANDOFF)
    queue={r["texture_id"]:r for r in ledger}
    if len(historical)!=1306 or len(queue)!=2256:
        raise ValueError("UV support source population changed")
    expected=json.loads((root/SUMMARY).read_text(encoding="utf-8"))
    source=Sources(args)
    images={}
    differences=[]
    observed=Counter()
    group_frames=defaultdict(set)
    group_weights={}
    valid_records=0
    try:
        for row in historical:
            tid=row["texture_id"]
            source_row=queue[tid]
            key=(tid,row["uv"],row["original_status"])
            count=int(row["face_instances"])
            if key in group_weights and group_weights[key]!=count:
                raise ValueError("One UV group has conflicting model-face weights")
            group_weights[key]=count
            if tid not in images:
                original=source.fetch(source_row["source_id"],source_row["path"])
                if raw_source_sha(original,source_row["source_hash_kind"])!=source_row["source_sha"]:
                    raise ValueError("Source original SHA mismatch in UV support: "+tid)
                verify_png_crc(original,source_row["path"])
                with Image.open(io.BytesIO(original)) as png:
                    png.load()
                    im=png.convert("RGBA")
                meta=source.fetch(source_row["source_id"],source_row["path"]+".mcmeta",required=False)
                animation=json.loads(meta.decode("utf-8-sig")).get("animation") if meta is not None else None
                if animation:
                    if im.height%im.width!=0 or im.height<=im.width:
                        raise ValueError("Unexpected animated sprite format: "+tid)
                    frames=[im.crop((0,y,im.width,y+im.width)) for y in range(0,im.height,im.width)]
                else:
                    frames=[im]
                images[tid]=frames
            frames=images[tid]
            w,h=frames[0].size
            uv=tuple(Fraction(s) for s in row["uv"].split("|"))
            if len(uv)!=4:
                raise ValueError("Bad 1-4 UV source tuple")
            xb=axis_uv(uv[0],uv[2],w)
            yb=axis_uv(uv[1],uv[3],h)
            label=("POINT_SUPPORT" if uv[0]==uv[2] and uv[1]==uv[3]
                   else "LINE_SUPPORT" if uv[0]==uv[2] or uv[1]==uv[3]
                   else "CLIPPED_RECT_SUPPORT")
            if xb is None or yb is None:
                label="NO_PINNED_SPRITE_INTERSECTION"
                computed={"outcome":label,"frame":"","pixel_box":"",
                          "frame_width":w,"frame_height":h,
                          "within_sprite_fraction":"0","u_axis":"","v_axis":"",
                          "transparent":"","partial_alpha":"","opaque":"",
                          "visible_rgb":"","dominant_rgba":"","rgba_sha256":""}
            else:
                if "EDGE_CONTACT" in (xb[3],yb[3]):
                    label="EDGE_CONTACT_SUPPORT"
                idx=int(row["frame"])
                if idx<0 or idx>=len(frames):
                    raise ValueError("Unexpected frame index in independent UV audit")
                box=(xb[0],yb[0],xb[1],yb[1])
                if not (0<=box[0]<box[2]<=w and 0<=box[1]<box[3]<=h):
                    raise ValueError("Impossible source rectangle from UV")
                metrics=region_metrics(frames[idx].crop(box))
                computed={
                    "outcome":label,"frame":idx,"pixel_box":"|".join(map(str,box)),
                    "frame_width":w,"frame_height":h,
                    "within_sprite_fraction":str(xb[2]*yb[2]),
                    "u_axis":xb[3],"v_axis":yb[3],
                    **metrics
                }
                group_frames[key].add(idx)
            wrong=[k for k,v in computed.items() if str(row[k])!=str(v)]
            if wrong and len(differences)<100:
                differences.append({"texture_id":tid,"uv":row["uv"],"fields":wrong})
            valid_records+=int(not wrong)
        group_outcomes=Counter()
        for row in historical:
            key=(row["texture_id"],row["uv"],row["original_status"])
            group_outcomes.setdefault(key,row["outcome"])
        for key,label in group_outcomes.items():
            group_outcomes[label]+=0  # intentionally not used as Counter in following loop
    finally:
        source.close()
    # Count per source-UV group rather than repeated animation frames.
    source_outcomes={}
    for row in historical:
        key=(row["texture_id"],row["uv"],row["original_status"])
        if key in source_outcomes and source_outcomes[key]!=row["outcome"]:
            raise ValueError("Conflicting outcome within one UV group")
        source_outcomes[key]=row["outcome"]
    for key,label in source_outcomes.items():
        observed[label]+=group_weights[key]
        if label!="NO_PINNED_SPRITE_INTERSECTION":
            if group_frames[key]!=set(range(len(images[key[0]]))):
                if len(differences)<100:
                    differences.append({"group":key,"reason":"not all original animation frames compared"})
    result={
       "method":"original_png_sha_and_crc_independent_fractional_UV_to_pixel_region_extraction",
       "source_texture_files":len(images),
       "unique_uv_groups":len(source_outcomes),
       "region_frame_rows":len(historical),
       "region_rows_with_full_metrics_matched":valid_records,
       "face_instances_by_support_type":dict(sorted(observed.items())),
       "source_supported_faces":sum(v for k,v in observed.items() if k!="NO_PINNED_SPRITE_INTERSECTION"),
       "no_sprite_intersection_faces":observed["NO_PINNED_SPRITE_INTERSECTION"],
       "difference_examples":differences,
       "expectations_match":dict(observed)==EXPECTED and valid_records==len(historical)
            and len(source_outcomes)==expected["distinct_uv_exception_groups"]
            and len(images)==expected["exception_texture_paths_checked"],
    }
    return result

def check_child_slot_and_missing(root,args):
    content=lzma.decompress((root/DB).read_bytes())
    db=sqlite3.connect(":memory:")
    db.deserialize(content)
    if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("F normalized sqlite integrity failed")
    if db.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("F normalized sqlite FK violations")
    providers=dict(db.execute("SELECT model_key,provider_key FROM geometry"))
    bound_slots={(model,slot):tid for model,slot,tid in
                 db.execute("SELECT model_key,slot,texture_id FROM model_slot WHERE texture_id IS NOT NULL")}
    bound_texture_ids={tid for tid,path in db.execute("SELECT id,path FROM texture WHERE length(path)>0")}
    descendant=defaultdict(set)
    for leaf,parent in db.execute("SELECT model_key,ancestor_key FROM lineage WHERE position>0"):
        descendant[parent].add(leaf)
    selected={m for (m,) in db.execute("SELECT DISTINCT model_key FROM option WHERE model_key IS NOT NULL")}
    classified=Counter()
    unseen_selected=0
    count_unbound=0
    for model,slot,face_count,provider in db.execute("""
        SELECT s.model_key,s.slot,s.face_count,g.provider_key
          FROM model_slot s JOIN geometry g USING(model_key)
         WHERE s.texture_id IS NULL
    """):
        count_unbound+=int(face_count)
        if model in selected:
            unseen_selected+=int(face_count)
        has_child=any(
            providers.get(child)==provider and bound_slots.get((child,slot)) in bound_texture_ids
            for child in descendant.get(model,set())
        )
        category="BOUND_CHILD_CONTEXT" if has_child else "UNBOUND_NO_BOUND_CHILD"
        classified[category]+=int(face_count)
    db.close()
    af=zipfile.ZipFile(args.af)
    af_paths={p.partition("/")[2] for p in af.namelist()}
    af.close()
    exceptions=[r for r in csv_rows(root/HANDOFF) if r["disposition"]=="SOURCE_EXCEPTION"]
    if len(exceptions)!=8:
        raise ValueError("Source exception denominator changed")
    existing=[]
    for row in exceptions:
        ns,resource=row["resource_id"].split(":",1)
        presumed=f"common/src/main/resources/assets/{ns}/textures/{resource}.png"
        if presumed in af_paths:
            existing.append(presumed)
    return {
      "method":"independent_normalized_db_parent_child_lookup_plus_pinned_git_texture_path_presence",
      "unbound_face_instances":count_unbound,
      "child_binding_context_counts":dict(classified),
      "selected_unbound_face_instances":unseen_selected,
      "missing_png_ids":len(exceptions),
      "face_instances_using_missing_png_ids":sum(int(r["face_instances"]) for r in exceptions),
      "missing_source_paths_falsely_present":existing,
      "passed":count_unbound==6202 and dict(classified)=={"BOUND_CHILD_CONTEXT":6196,"UNBOUND_NO_BOUND_CHILD":6}
          and unseen_selected==0 and len(exceptions)==8
          and sum(int(r["face_instances"]) for r in exceptions)==139 and not existing,
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    for name in ("af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    support=verify_support(args.root,args)
    exceptions=check_child_slot_and_missing(args.root,args)
    report={
      "schema":"MCFR_INT2_1_4_SUPPLEMENTAL_UV_SOURCE_v1",
      "source_support":support,
      "slot_and_missing_source":exceptions,
      "not_checked":[
         "registered game runtime UV-lock and model bake",
         "ordinary rectangle faces beyond chair sample",
         "upstream license and training rights",
      ],
      "status":"PASS_SUPPLEMENTAL_SOURCE_AND_EXCEPTION_CONTEXT"
                if support["expectations_match"] and not support["difference_examples"]
                and exceptions["passed"] else "DISCREPANCY_REQUIRES_REVIEW",
    }
    (args.out/"INT2_1_4_SUPPLEMENTAL_SUMMARY.json").write_text(
         json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    print("INT2_1_4_SUPPLEMENTAL_RESULT:"+json.dumps(report,sort_keys=True,ensure_ascii=False))
    if report["status"]!="PASS_SUPPLEMENTAL_SOURCE_AND_EXCEPTION_CONTEXT":
         raise SystemExit("INT-2 supplemental UV source or child-slot discrepancy")

if __name__=="__main__":
    main()
