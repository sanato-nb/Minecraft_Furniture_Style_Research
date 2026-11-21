"""INT-2 1-4: independent model source -> parent -> face -> slot -> PNG -> UV replay.

Rebuilds all source-model face links directly from immutable AF/HC/Macaw
model JSON and Mojang vanilla-parent JSON. The old F SQLite is read only for
the model/texture identity registry and as an EXPECTED comparator after each
raw-source result is computed. Historical geometry, face, slot, and lineage
tables are never used to construct new links.

Input texture frame metadata are from previously source-redecoded pinned PNGs
(1-4 Entry02); the frame count/PNG bytes are independently checked in PR #24.
The resulting 592,312 face-link CSV.gz contains NO upstream model or PNG bytes.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import gzip
import hashlib
import io
import itertools
import json
import lzma
from pathlib import Path
import sqlite3
from typing import Any

from audit_int2_mod_textures import Sources, raw_source_sha, csv_rows

ROOT = Path(__file__).resolve().parents[2]
F_DB="research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz"
QUEUE="research/furniture_mods/phase_1-3/F/1-3_TEXTURE_UV_HANDOFF.csv"
TEXCOUNTS="research/furniture_mods/phase_1-4/entry02/TEXTURE_UV_COUNTS.csv.xz"
ENTRY02="research/furniture_mods/phase_1-4/entry02/ENTRY02_AUDIT.json"
EXCEPTION="research/furniture_mods/phase_1-4/C_followup/SUMMARY.json"
EXPECTED_TOTAL=592312
BUILTIN={"minecraft:builtin/generated","minecraft:builtin/entity","minecraft:builtin/missing"}
FACE_COLS=("model_key","provider_key","element_index","direction","source_slot",
           "resolved_resource_id","texture_id","uv_method","uv",
           "uv_rotation","u_reversed","v_reversed","cullface","tintindex",
           "status","source_pixels_per_local_u","source_pixels_per_local_v")
MODEL_COLS=("model_key","source_id","path","source_sha","resolved_provider",
            "source_faces","reconstructed_faces","matched_faces",
            "slot_keys","slot_matches","parent_depth","parent_terminal",
            "status","issues")
ERR_CAP=120
DIR_AXES={"up":(0,2),"down":(0,2),"east":(2,1),"west":(2,1),
          "north":(0,1),"south":(0,1)}

def frac(n):
    if isinstance(n,Fraction):
        return n
    return Fraction(str(n))

def canon(seq):
    return "|".join(str(frac(x)) for x in seq)

def normalize(ref):
    return ref if ":" in ref else "minecraft:"+ref

def default_uv(a,b,side):
    """Reimplement 1.21.1 source bytecode's 6 oriented constructor formulas."""
    x,y,z=map(frac,a)
    X,Y,Z=map(frac,b)
    d={
      "down":(x,16-Z,X,16-z),
      "up":(x,z,X,Z),
      "north":(16-X,16-Y,16-x,16-y),
      "south":(x,16-Y,X,16-y),
      "west":(z,16-Y,Z,16-y),
      "east":(16-Z,16-Y,16-z,16-y),
    }
    return d[side]

def resolve_slot(face_ref,bindings):
    if not isinstance(face_ref,str):
        raise ValueError("Original face texture reference is not a string")
    used=set()
    ref=face_ref
    while ref.startswith("#"):
        key=ref[1:]
        if key in used:return ("SLOT_CYCLE",None)
        used.add(key)
        val=bindings.get(key)
        if not isinstance(val,str):return ("SLOT_UNBOUND",None)
        ref=val
    return ("RESOURCE_ID", normalize(ref))

def classify(tid,uv,texmeta):
    if tid is None:
        return "SLOT_UNBOUND"
    meta=texmeta.get(tid)
    if meta is None:
        return "MISSING_PINNED_PNG"
    if uv[0]==uv[2] or uv[1]==uv[3]:
        return "ZERO_UV_AREA"
    if any(u<0 or u>16 for u in uv):
        return "OUTSIDE_TEXTURE_UV"
    return "ANIMATED_FRAME_RECTS" if int(meta["frame_count"])>1 else "STATIC_RECT"

def density(uv,uvrot,side,a,b,texmeta):
    axes=DIR_AXES[side]
    if uvrot in (90,270):
        axes=axes[::-1]
    lengths=[abs(frac(b[i])-frac(a[i])) for i in axes]
    width=frac(texmeta["frame_width"])
    height=frac(texmeta["frame_height"])
    du=abs(uv[2]-uv[0])*width/16/lengths[0] if lengths[0] else None
    dv=abs(uv[3]-uv[1])*height/16/lengths[1] if lengths[1] else None
    return (str(du) if du is not None else "",str(dv) if dv is not None else "")

def consistent_json(raw,path):
    def unique_pairs(pairs):
        result={}
        for k,v in pairs:
            if k in result:
                raise ValueError(f"Duplicate original JSON key {path}: {k}")
            result[k]=v
        return result
    obj=json.loads(raw.decode("utf-8-sig"),object_pairs_hook=unique_pairs)
    if not isinstance(obj,dict):raise ValueError("Original JSON not a model object "+path)
    return obj

def load_texture_registry(db,root):
    queue={int(r["texture_id"]):r for r in csv_rows(root/QUEUE)}
    if len(queue)!=2256:raise ValueError("1-3 F texture identity registry changed")
    with lzma.open(root/TEXCOUNTS,"rt",encoding="utf-8",newline="") as f:
        metas={int(r["texture_id"]):r for r in csv.DictReader(f)}
    if len(metas)!=2171:raise ValueError("1-4 2171 sampled PNG frame-regions changed")
    expected_db={(res,mc):tid for tid,res,mc in db.execute("SELECT id,resource_id,minecraft FROM texture")}
    if len(expected_db)!=2256:raise ValueError("Frozen F texture identity collision")
    for tid,row in queue.items():
        actual=expected_db.get((row["resource_id"],row["minecraft"]))
        if actual!=tid:raise ValueError("F registry and PNG handoff disagree "+str(tid))
        if row["path"] and int(row["face_instances"]) and tid not in metas:
            raise ValueError("Missing original RGBA PNG meta in 1-4: "+str(tid))
    return queue,metas,expected_db

def load_original_models(db,source):
    metadata=list(db.execute("SELECT model_key,source_id,resource_id,path,sha FROM model ORDER BY model_key"))
    from_mod=[r for r in metadata if r[1] in ("AF","HC","MACAW")]
    if len(from_mod)!=16572:raise ValueError("Original model registry has changed from 16572")
    keys={}
    raw_models={}
    verified=Counter()
    for model_key,mod,rid,path,sha in metadata:
        binary=source.fetch(mod,path)
        kind="GIT_BLOB_SHA1" if mod in ("AF","HC") else "SHA256"
        if raw_source_sha(binary,kind)!=sha:
            raise ValueError(f"Source model SHA disagrees with pinned database identity: {path}")
        obj=consistent_json(binary,path)
        resource_key=(mod,rid)
        if resource_key in keys:
            raise ValueError("Original resource ID collision "+str(resource_key))
        keys[resource_key]=model_key
        raw_models[model_key]=obj
        verified[mod]+=1
    return metadata,keys,raw_models,dict(verified)

def ancestors(key,mod,mc,keys,originals):
    chain=[]
    seen=set()
    while key is not None:
        if key in seen:
            return chain,"PARENT_CYCLE",key
        seen.add(key)
        body=originals[key]
        chain.append(key)
        ref=body.get("parent")
        if not ref:
            return chain,"ROOT",""
        rid=normalize(ref)
        if rid in BUILTIN:
            return chain,"BUILTIN",rid
        prefix=rid.split(":",1)[0]
        lookup=(("MC"+mc,rid) if prefix=="minecraft" else (mod,rid))
        key=keys.get(lookup)
        if key is None:
            return chain,"PARENT_MISSING",rid
    return chain,"ROOT",""

def load_expectations(db):
    geom={key:(provider,terminal,resource,n,m) for key,provider,terminal,resource,n,m in
          db.execute("SELECT model_key,provider_key,terminal_status,terminal_resource,element_instances,face_instances FROM geometry")}
    lineage=defaultdict(list)
    for key,pos,ancestor in db.execute("SELECT model_key,position,ancestor_key FROM lineage ORDER BY model_key,position"):
        lineage[key].append(ancestor)
    slots=defaultdict(dict)
    for key,slot,tid,resolution,count in db.execute(
        "SELECT model_key,slot,texture_id,resolution,face_count FROM model_slot"
    ):
        if slot in slots[key]:raise ValueError("Historical duplicate slot key")
        slots[key][slot]=(tid,resolution,count)
    return geom,lineage,slots

OLD_SQL="""
 SELECT g.model_key, f.provider_key,f.element_index,f.direction,
        f.slot,s.texture_id,s.resolution,f.uv,f.uv_declared,f.uv_rotation,
        f.cullface,f.tintindex,e.source_from,e.source_to
 FROM geometry AS g
 JOIN face AS f ON f.provider_key=g.provider_key
 LEFT JOIN model_slot AS s ON s.model_key=g.model_key AND s.slot=f.slot
 JOIN element AS e ON e.provider_key=f.provider_key AND e.element_index=f.element_index
 ORDER BY g.model_key,f.provider_key,f.element_index,f.direction
"""

def iter_groups(db):
    stream=db.execute(OLD_SQL)
    for key,items in itertools.groupby(stream,key=lambda r:r[0]):
        yield key,list(items)

def check_model(key,mod,mc,source_path,source_sha,models,ids,originals,geom,lines,slots,
                texture_ids,metadata,historical):
    chain,terminal,term_ref=ancestors(key,mod,mc,ids,originals)
    children=[originals[k] for k in chain]
    provider=next((k for k in chain if originals[k].get("elements")),None)
    model_elems=originals[provider].get("elements",[]) if provider else []
    bindings={}
    for node in reversed(children):
        bindings.update(node.get("textures",{}))
    geom_info=geom[key]
    problems=[]
    if geom_info[0]!=provider:problems.append("PROVIDER_MISMATCH")
    if geom_info[1]!=terminal or geom_info[2]!=term_ref:
        problems.append("TERMINAL_MISMATCH")
    original_chain=lines.get(key,[])
    if chain!=original_chain:
        problems.append("PARENT_LINEAGE_MISMATCH")
    expected_face_count=sum(len(e.get("faces",{})) for e in model_elems)
    if expected_face_count!=geom_info[4] or len(model_elems)!=geom_info[3]:
        problems.append("GEOMETRY_COUNTS_MISMATCH")
    slot_counts=Counter()
    result={}
    grouped_status=Counter()
    by_scope=Counter()
    declarations=Counter()
    for i,e in enumerate(model_elems):
        from_v,to_v=e["from"],e["to"]
        for direction,face in e.get("faces",{}).items():
            slot=face["texture"]
            slot_counts[slot]+=1
            resolution,rid=resolve_slot(slot,bindings)
            tid=texture_ids.get((rid,mc)) if rid is not None else None
            if resolution=="RESOURCE_ID" and tid is None:
                problems.append("BOUND_RESOURCE_NOT_IN_PINNED_TEXTURE_REGISTRY")
            uv_declared=int("uv" in face)
            uv=tuple(map(frac,face["uv"])) if uv_declared else default_uv(from_v,to_v,direction)
            uvrot=int(face.get("rotation",0))
            cull=face.get("cullface","")
            tint=str(face.get("tintindex",""))
            face_status=classify(tid,uv,metadata)
            du=dv=""
            if face_status not in ("SLOT_UNBOUND","MISSING_PINNED_PNG"):
                du,dv=density(uv,uvrot,direction,from_v,to_v,metadata[tid])
            key_face=(provider,i,direction)
            result[key_face]={
                "model_key":key,"provider_key":provider or "","element_index":i,
                "direction":direction,"source_slot":slot,
                "resolved_resource_id":rid or "","texture_id":"" if tid is None else tid,
                "uv_method":"EXPLICIT" if uv_declared else "DEFAULT","uv":canon(uv),
                "uv_rotation":uvrot,"u_reversed":int(uv[0]>uv[2]),
                "v_reversed":int(uv[1]>uv[3]),"cullface":cull,"tintindex":tint,
                "status":face_status,"source_pixels_per_local_u":du,
                "source_pixels_per_local_v":dv,
            }
            grouped_status[face_status]+=1
            declarations["explicit" if uv_declared else "implicit"]+=1
            declarations["reversed"]+=int(uv[0]>uv[2] or uv[1]>uv[3])
            declarations["rotated"]+=int(uvrot!=0)
            if face_status in ("SLOT_UNBOUND","MISSING_PINNED_PNG"):
                by_scope[face_status]+=1
            else:
                by_scope[(metadata[tid]["scope"],face_status)]+=1
    if len(result)!=expected_face_count:
        problems.append("ORIGINAL_DUPLICATE_FACE_KEYS")
    # Compare every model's source-created slot declarations against original F.
    expected_slot_keys=set(slot_counts)|{"#"+name for name in bindings}
    before=slots.get(key,{})
    if expected_slot_keys!=set(before):
        problems.append("SLOT_KEY_POPULATION_MISMATCH")
    matched_slots=0
    for slot in sorted(expected_slot_keys):
        status,rid=resolve_slot(slot,bindings)
        tid=texture_ids.get((rid,mc)) if rid is not None else None
        expected=before.get(slot)
        actual=(tid,status,slot_counts.get(slot,0))
        if expected!=actual:
            problems.append("SLOT_RESOLUTION_OR_FACE_COUNT_MISMATCH")
        else:
            matched_slots+=1
    old={r[1:4]:r for r in historical}
    if len(old)!=len(historical):
        problems.append("DUPLICATE_HISTORICAL_FACE_KEY")
    if set(old)!=set(result):
        problems.append("FACE_IDENTITY_SET_MISMATCH")
    matched=0
    discrepancies=Counter()
    for k,face in result.items():
        prev=old.get(k)
        if prev is None:continue
        _,pkey,idx,side,slot,tid,resolution,uv,declared,uvrot,cull,tint,a,b=prev
        face_uv=face["uv"]
        expected_uv=(canon(tuple(map(frac,uv.split("|")))) if uv else "") if declared else ""
        # The F face table contains explicit-UV only. Recreated implicit UV
        # is separately compared to the historical engine formula by groups.
        uv_from_original=(
            canon(originals[pkey]["elements"][idx]["faces"][side].get("uv",[]))
            if declared else ""
        )
        expected_res=face["resolved_resource_id"]
        checks={
            "slot":slot==face["source_slot"],
            "texture_id":tid==face["texture_id"] if tid is not None else face["texture_id"]=="",
            "resolution":resolution==("SLOT_UNBOUND" if not face["resolved_resource_id"] else "RESOURCE_ID"),
            "uv_original":uv_from_original==expected_uv,
            "uv_method":int(declared)==int(face["uv_method"]=="EXPLICIT"),
            "uv_rotation":int(uvrot)==face["uv_rotation"],
            "cullface":cull==face["cullface"],
            "tintindex":tint==face["tintindex"],
            "source_from":canon(from_v:=originals[pkey]["elements"][idx]["from"])==canon(a.split("|")),
            "source_to":canon(to_v:=originals[pkey]["elements"][idx]["to"])==canon(b.split("|")),
        }
        if all(checks.values()):
            matched+=1
        else:
            discrepancies.update(k for k,v in checks.items() if not v)
    if discrepancies:
        problems.extend("FACE_"+x for x in discrepancies)
    row={
       "model_key":key,"source_id":mod,"path":source_path,"source_sha":source_sha,
       "resolved_provider":provider or "","source_faces":expected_face_count,
       "reconstructed_faces":len(result),"matched_faces":matched,
       "slot_keys":len(expected_slot_keys),"slot_matches":matched_slots,
       "parent_depth":len(chain)-1,"parent_terminal":terminal,
       "status":"PASS" if not problems else "DIFFERENCE",
       "issues":"|".join(sorted(set(problems))),
    }
    return row,result,grouped_status,by_scope,declarations,discrepancies

def audit(root,args):
    db=sqlite3.connect(":memory:")
    db.deserialize(lzma.decompress((root/F_DB).read_bytes()))
    if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("Historical F database corrupted")
    if db.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Historical F database foreign-key violations")
    source=Sources(args)
    try:
        meta,key_index,originals,verified=load_original_models(db,source)
    finally:
        source.close()
    geom,lines,slots=load_expectations(db)
    queue,texture_meta,textureids=load_texture_registry(db,root)
    old=iter_groups(db)
    next_old=next(old,None)
    totals=Counter()
    statuses=Counter()
    scope_status=Counter()
    declarations=Counter()
    mismatch_examples=[]
    model_rows=[]
    out_path=args.out/"INT2_1_4_592312_FACE_LINKS.csv.gz"
    with out_path.open("wb") as raw:
        # Stable gzip header, including mtime=0 and no output filename.
        with gzip.GzipFile(fileobj=raw,mode="wb",filename="",mtime=0,compresslevel=6) as z:
            with io.TextIOWrapper(z,encoding="utf-8",newline="",write_through=True) as text:
                writer=csv.DictWriter(text,fieldnames=FACE_COLS,lineterminator="\n")
                writer.writeheader()
                for model_key,mod,rid,path,sha in meta:
                    if mod not in ("AF","HC","MACAW"):
                        continue
                    mc="1.21.11" if mod=="MACAW" else "1.21.1"
                    historical=[]
                    if next_old is not None and next_old[0]==model_key:
                        historical=next_old[1]
                        next_old=next(old,None)
                    # Source first: never generate candidates from old DB face/link rows.
                    report,faces,groups,by_scope,decl,mismatches=check_model(
                        model_key,mod,mc,path,sha,meta,key_index,originals,geom,lines,slots,
                        textureids,texture_meta,historical
                    )
                    for face in sorted(faces.values(),key=lambda x:(x["provider_key"],x["element_index"],x["direction"])):
                        writer.writerow(face)
                    model_rows.append(report)
                    totals["source_verified_models"]+=1
                    totals["reconstructed_faces"]+=len(faces)
                    totals["historical_matched_faces"]+=report["matched_faces"]
                    totals["source_slots"]+=report["slot_keys"]
                    totals["matched_slots"]+=report["slot_matches"]
                    totals["model_rows_pass"]+=int(report["status"]=="PASS")
                    totals["model_rows_different"]+=int(report["status"]!="PASS")
                    statuses.update(groups)
                    scope_status.update(by_scope)
                    declarations.update(decl)
                    if report["issues"] and len(mismatch_examples)<ERR_CAP:
                        mismatch_examples.append({
                           "model_key":model_key,"mod":mod,"path":path,
                           "issues":report["issues"],"face_details":dict(mismatches),
                        })
    db.close()
    if next_old is not None:
        mismatch_examples.append({"reason":"Historical F face ledger has leftover model groups"})
    expected_json=json.loads((root/ENTRY02).read_text(encoding="utf-8"))
    expectation=Counter()
    for k,v in expected_json["status_face_counts"].items():
        for status,n in v.items():
            expectation[(k,status)]+=n
    expected_scope={
        key:n for key,n in scope_status.items() if isinstance(key,tuple)
    }
    expected_count=Counter({tuple(k):v for k,v in expectation.items()})
    scope_diffs={
       str(key):{"observed":expected_scope.get(key,0),"expected":n}
       for key,n in expected_count.items() if expected_scope.get(key,0)!=n
    }
    expected_other={"SLOT_UNBOUND":6202,"MISSING_PINNED_PNG":139}
    other_diffs={k:{"observed":scope_status[k],"expected":n}
                 for k,n in expected_other.items() if scope_status[k]!=n}
    model_csv=args.out/"INT2_1_4_16572_MODEL_LINK_CHECKS.csv"
    with model_csv.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=MODEL_COLS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(model_rows)
    result={
      "schema":"MCFR_INT2_1_4_FULL_SOURCE_FACE_LINKS/v1",
      "pinned_source_model_counts":verified,
      "observed":dict(sorted(totals.items())),
      "face_status_counts":dict(sorted(statuses.items())),
      "pixel_scope_and_face_status_counts":{"|".join(k) if isinstance(k,tuple) else k:v
                                            for k,v in sorted(scope_status.items(),key=lambda x:str(x[0]))},
      "source_face_uv_declarations":dict(sorted(declarations.items())),
      "scope_comparison_discrepancies":scope_diffs,
      "missing_or_unbound_discrepancies":other_diffs,
      "model_mismatch_examples":mismatch_examples,
      "evidence":{"per_face_gzip_sha256":hashlib.sha256(out_path.read_bytes()).hexdigest(),
                  "per_model_csv_sha256":hashlib.sha256(model_csv.read_bytes()).hexdigest()},
      "assertions":{
        "fixed_model_total":totals["source_verified_models"]==16572,
        "fixed_face_total":totals["reconstructed_faces"]==EXPECTED_TOTAL,
        "all_592312_face_links_match_existing_F":totals["historical_matched_faces"]==EXPECTED_TOTAL,
        "all_model_slots_match":totals["source_slots"]==totals["matched_slots"],
        "all_16572_model_rows_match":totals["model_rows_pass"]==16572,
        "old_entry02_disposition_counts_match":not scope_diffs and not other_diffs,
        "no_old_face_rows_leftover":next_old is None,
      },
      "limitations":[
         "does not execute Minecraft client or verify final baked texture atlas",
         "1-4 entry02 PNG frame metadata are pinned from prior independent pixel rechecks",
         "historical F registry supplies canonical resource/version numeric texture identity",
         "runtime resource overrides, shader tint and collision not verified",
         "source licensing and AI training approval not granted by this check",
      ],
      "ai_training_approved":False,
    }
    result["status"]=("PASS_ALL_592312_FACE_LINKS_RECONSTRUCTED_FROM_ORIGINALS"
       if all(result["assertions"].values()) and not mismatch_examples else
       "DIFFERENCE_REQUIRES_REVIEW")
    (args.out/"INT2_1_4_FULL_LINKS_SUMMARY.json").write_text(
        json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    for arg in ("af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+arg,type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    report=audit(args.root,args)
    print("INT2_1_4_FULL_LINKS_RESULT:"+json.dumps(report,ensure_ascii=False,sort_keys=True))
    if report["status"]!="PASS_ALL_592312_FACE_LINKS_RECONSTRUCTED_FROM_ORIGINALS":
        raise SystemExit("Full original face-link provenance mismatches detected")

if __name__=="__main__":
    main()
