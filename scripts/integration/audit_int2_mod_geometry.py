"""INT-2 1-3 independent original-asset model/parent/geometry audit.

Requires immutable GitHub commit archives (AF, HC), pinned Macaw Fabric JAR
and both original Mojang client JARs. Downloaded source assets are never
committed or included in outputs. Recomputes model-specific C findings
without importing the original C geometry/lineage implementations.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import zipfile

PHASE="research/furniture_mods/phase_1-3"
C=PHASE+"/C/"
B=PHASE+"/B/source_verification/"
EXPECTED={
 "models":{"AF":1629,"HC":12394,"MACAW":2549},
 "static":16464, "no_static":108, "elements":105383,
 "faces":592312,"providers":300,"declared_elements":1911,
 "declared_faces":9760,"parent_missing":48,
}
BUILTIN={"minecraft:builtin/generated","minecraft:builtin/entity","minecraft:builtin/missing"}
OUT_COLS=("mod","path","source_sha","status","geometry_status","own_elements",
          "effective_elements","effective_faces","provider","chain","terminal",
          "faces_unbound","issues")
ERR_LIMIT=100

def read_table(path):
    opener=gzip.open if str(path).endswith(".gz") else open
    with opener(path,"rt",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def sha(data,kind):
    if kind=="git":
        return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
    return hashlib.sha256(data).hexdigest()

def json_unique(data,path):
    def checked(pairs):
        result={}
        for k,v in pairs:
            if k in result:
                raise ValueError(f"Duplicate JSON key in {path}: {k}")
            result[k]=v
        return result
    result=json.loads(data.decode("utf-8-sig"),object_pairs_hook=checked)
    if not isinstance(result,dict):
        raise ValueError(f"Not object JSON: {path}")
    return result

def zip_tree(path):
    archive=zipfile.ZipFile(path)
    index={}
    for filename in archive.namelist():
        if filename.endswith("/"):
            continue
        if "/" not in filename:
            continue
        relative=filename.split("/",1)[1]
        if relative in index:
            raise ValueError(f"Duplicated upstream archive path: {relative}")
        index[relative]=filename
    return archive,index

def norm(ref):
    return ref if ":" in ref else "minecraft:"+ref

def floats(v):
    return tuple(float(x) for x in v.split("|")) if v else ()

def same_vec(ref,values,eps=5e-8):
    old=floats(ref)
    return len(old)==len(values) and all(abs(a-b)<eps for a,b in zip(old,values))

def bbox(elem,rotated=False):
    low=[min(a,b) for a,b in zip(elem["from"],elem["to"])]
    high=[max(a,b) for a,b in zip(elem["from"],elem["to"])]
    if not rotated or not elem.get("rotation") or not elem["rotation"].get("angle"):
        return tuple(low+high)
    rot=elem["rotation"]
    theta=math.radians(float(rot["angle"]))
    c,s=math.cos(theta),math.sin(theta)
    if rot.get("rescale") and abs(c)<1e-11:
        raise ValueError(f"Singular rotation rescale: {rot!r}")
    scale=1/c if rot.get("rescale") else 1
    center=[(x+y)/2 for x,y in zip(low,high)]
    half=[(y-x)/2 for x,y in zip(low,high)]
    pivot=rot["origin"]
    matrix={
      "x":((1.,0.,0.),(0.,c*scale,-s*scale),(0.,s*scale,c*scale)),
      "y":((c*scale,0.,s*scale),(0.,1.,0.),(-s*scale,0.,c*scale)),
      "z":((c*scale,-s*scale,0.),(s*scale,c*scale,0.),(0.,0.,1.))
    }[rot["axis"]]
    rotated_center=[pivot[i]+sum(matrix[i][j]*(center[j]-pivot[j]) for j in range(3)) for i in range(3)]
    radius=[sum(abs(matrix[i][j])*half[j] for j in range(3)) for i in range(3)]
    return tuple(rotated_center[i]-radius[i] for i in range(3))+tuple(rotated_center[i]+radius[i] for i in range(3))

def united(elements,rotated):
    if not elements:
        return ()
    boxes=[bbox(e,rotated) for e in elements]
    return tuple(min(b[i] for b in boxes) for i in range(3))+tuple(max(b[i] for b in boxes) for i in range(3,6))

def slot_status(face_ref,slots):
    # Same Minecraft resource declaration interpretation, implemented independently
    if not isinstance(face_ref,str):
        return "SLOT_UNBOUND"
    seen=set()
    while face_ref.startswith("#"):
        name=face_ref[1:]
        if name in seen:
            return "SLOT_CYCLE"
        seen.add(name)
        if name not in slots or not isinstance(slots[name],str):
            return "SLOT_UNBOUND"
        face_ref=slots[name]
    return "RESOURCE_ID"

def load_originals(root,args):
    archive_by_mod={}
    for mod,path in [("AF",args.af),("HC",args.hc)]:
        archive,index=zip_tree(path)
        archive_by_mod[mod]=(archive,index)
    macaw_data=args.macaw.read_bytes()
    if sha(macaw_data,"sha256")!="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e":
        raise ValueError("Macaw official JAR pinned SHA-256 mismatch")
    macaw=zipfile.ZipFile(args.macaw)
    if macaw.testzip() is not None:
        raise ValueError("Macaw JAR ZIP CRC invalid")
    vanilla={}
    for version,path,expected in (
        ("1.21.1",args.mc1211,"30c73b1c5da787909b2f73340419fdf13b9def88"),
        ("1.21.11",args.mc12111,"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"),
    ):
        data=path.read_bytes()
        if hashlib.sha1(data).hexdigest()!=expected:
            raise ValueError("Mojang pinned client SHA-1 mismatch: "+version)
        vanilla[version]=zipfile.ZipFile(path)
    models={}
    records={}
    oldc=read_table(root / (C+"mod_furniture_catalog.csv.gz"))
    c_by_identity={(r["mod"],r["path"]):r for r in oldc}
    if len(oldc)!=16572 or len(c_by_identity)!=16572:
        raise ValueError("C catalog population/identity mismatch")
    for mod in ("AF","HC","MACAW"):
        rows=read_table(root / (B+f"B_{mod}_SOURCE_BODIES.csv.gz"))
        model_rows=[r for r in rows if r["family"]=="models"]
        if len(model_rows)!=EXPECTED["models"][mod]:
            raise ValueError("B model denominator wrong for "+mod)
        for row in model_rows:
            path=row["path"]
            if mod=="MACAW":
                binary=macaw.read(path)
                digest="sha256"
            else:
                arc,index=archive_by_mod[mod]
                binary=arc.read(index[path])
                digest="git"
            if sha(binary,digest)!=row["sha"] or len(binary)!=int(row["bytes"]):
                raise ValueError("Independent source hash/size mismatch: "+mod+":"+path)
            obj=json_unique(binary,path)
            ident=(mod,row["asset_id"])
            if ident in models:
                raise ValueError("Duplicate resource ID "+str(ident))
            c=c_by_identity[(mod,path)]
            if c["source_hash"]!=row["sha"] or c["model_id"]!=row["asset_id"]:
                raise ValueError("B/C source provenance mismatch: "+mod+":"+path)
            models[ident]=(obj,c,row)
            records[(mod,path)]=(obj,c,row)
    for mod,(arc,index) in archive_by_mod.items():
        arc.close()
    macaw.close()
    return models,records,vanilla,oldc

def calculate(root,args):
    models,records,vanilla,old_catalog=load_originals(root,args)
    c_chains={r["model_key"]:r for r in read_table(root / (C+"MODEL_PARENT_CHAINS.csv.gz"))}
    b_elems={(r["source_key"],int(r["element_index"])):r for r in read_table(root / (C+"mod_model_elements.csv.gz"))}
    b_faces=read_table(root / (C+"MODEL_FACES.csv.gz"))
    c_vanilla={(r["minecraft"],r["model_id"]):r for r in read_table(root / (C+"C_VANILLA_PARENTS.csv"))}
    if len(c_chains)!=16572 or len(b_elems)!=1911 or len(b_faces)!=9760:
        raise ValueError("Historical C static ledger lengths differ from fixed scope")
    vanilla_data={}
    errors=[]
    summaries=[]
    measured=Counter()
    kinds=Counter()
    provider_ids=set()
    unresolvable=[]
    parent_missing_paths=[]
    effective_by_mod=Counter()
    provider_to_elements={}
    def discrepancy(kind,ident,reason):
        measured["discrepancies"]+=1
        if len(errors)<ERR_LIMIT:
            errors.append({"type":kind,"model":ident,"detail":reason})
    def getvanilla(version,ident):
        key=(version,ident)
        if key in vanilla_data:
            return vanilla_data[key]
        rid=ident.split(":",1)[1]
        path="assets/minecraft/models/"+rid+".json"
        try:
            raw=vanilla[version].read(path)
        except KeyError:
            return None
        auditrow=c_vanilla.get(key)
        if not auditrow:
            discrepancy("VANILLA_PARENT",ident,"Parent not declared in frozen C supplementary ledger")
            return None
        if sha(raw,"sha256")!=auditrow["sha256"]:
            raise ValueError("Pinned vanilla parent digest mismatch "+version+":"+ident)
        data=json_unique(raw,path)
        vanilla_data[key]=(data,auditrow)
        return vanilla_data[key]
    def lineage(mod,mc,ident):
        result=[]
        seen=set()
        current=ident
        while True:
            key=(mod,current) if not current.startswith("minecraft:") else ("MC"+mc,current)
            if key in seen:
                return result,"PARENT_CYCLE",current
            seen.add(key)
            if key[0].startswith("MC"):
                resolved=getvanilla(mc,current)
                if resolved is None:
                    return result,"PARENT_MISSING",current
                obj,metadata=resolved
                model_key=metadata["source_key"]
                source_mod="VANILLA"
            else:
                resolved=models.get(key)
                if resolved is None:
                    return result,"PARENT_MISSING",current
                obj,c,_=resolved
                model_key=c["model_key"]
                source_mod=mod
            result.append((model_key,obj,source_mod,current))
            parent=obj.get("parent")
            if not parent:
                return result,"ROOT",""
            current=norm(parent)
            if current in BUILTIN:
                return result,"BUILTIN",current

    for mod,path in sorted(records):
        obj,c,row=records[(mod,path)]
        mc=c["minecraft"]
        chain,term,terminal=lineage(mod,mc,c["model_id"])
        provider=next((r for r in chain if r[1].get("elements")),None)
        elems=provider[1]["elements"] if provider else []
        own=obj.get("elements",[])
        own_faces=sum(len(e.get("faces",{})) for e in own)
        applied_faces=sum(len(e.get("faces",{})) for e in elems)
        if provider and provider[0] not in provider_to_elements:
            provider_to_elements[provider[0]]=elems
        if provider:
            provider_ids.add(provider[0])
        status="LOCAL" if provider else "NONE"
        if provider and provider[2]=="VANILLA":
            status="VANILLA"
        if terminal=="minecraft:builtin/generated":
            status="GENERATED_ITEM_RUNTIME"
        if term in ("PARENT_MISSING","PARENT_CYCLE") or terminal in ("minecraft:builtin/entity","minecraft:builtin/missing"):
            status="UNRESOLVED_PARENT" if not provider else "PARTIAL_OWN_OR_LOCAL_GEOMETRY"
        if term=="PARENT_MISSING":
            parent_missing_paths.append(c["model_id"])
        if not elems:
            unresolvable.append(c["model_id"])
        if len(own)!=int(c["own_elements"]) or own_faces!=int(c["own_faces"]):
            discrepancy("OWN",c["model_id"],"Own element/face mismatch")
        comparison={
            "geometry_status":status,
            "geometry_source_key":provider[0] if provider else "",
            "effective_elements":len(elems),
            "effective_faces":applied_faces,
            "inherited_elements":len(elems)-len(own),
            "inherited_faces":applied_faces-own_faces,
        }
        model_issues=[]
        for col,value in comparison.items():
            if str(value)!=c[col]:
                discrepancy("CATALOG",c["model_id"],f"{col}: expected={c[col]!r} observed={value!r}")
                model_issues.append(col)
        oldchain=c_chains.get(c["model_key"])
        if not oldchain:
            discrepancy("CHAIN",c["model_id"],"Missing historical C chain")
            model_issues.append("chain_missing")
        else:
            keys="|".join(node[0] for node in chain)
            if (keys,term,terminal,len(chain)-1)!=(oldchain["chain_keys"],oldchain["terminal_status"],oldchain["terminal_ref"],int(oldchain["depth"])):
                discrepancy("CHAIN",c["model_id"],"New parent chain differs from old chain")
                model_issues.append("chain_diff")
        if not same_vec(c["raw_bbox"],united(elems,False)) or not same_vec(c["rotated_bbox"],united(elems,True)):
            discrepancy("AABB",c["model_id"],"Effective model bbox differs from C")
            model_issues.append("bbox")
        slots={}
        for _,parent_obj,_,_ in reversed(chain):
            slots.update(parent_obj.get("textures",{}))
        facestat=Counter()
        uv_present=0
        for elem in elems:
            for face in elem.get("faces",{}).values():
                facestat[slot_status(face.get("texture"),slots)]+=1
                uv_present+=int("uv" in face)
        for col,metric in [
            ("faces_resolved",facestat["RESOURCE_ID"]),
            ("faces_unbound",facestat["SLOT_UNBOUND"]),
            ("faces_slot_cycle",facestat["SLOT_CYCLE"]),
            ("faces_explicit_uv",uv_present),
            ("faces_implicit_uv",applied_faces-uv_present),
        ]:
            if int(c[col])!=metric:
                discrepancy("UV_SLOT",c["model_id"],f"{col}: C={c[col]} new={metric}")
                model_issues.append(col)
        measured["model_paths"]+=1
        measured["effective_elements"]+=len(elems)
        measured["effective_faces"]+=applied_faces
        measured["static_models"]+=bool(elems)
        measured["own_elements_declared"]+=len(own)
        measured["own_faces_declared"]+=own_faces
        measured["slot_unbound_faces"]+=facestat["SLOT_UNBOUND"]
        measured["slot_cycle_faces"]+=facestat["SLOT_CYCLE"]
        measured["explicit_uv_faces"]+=uv_present
        measured["parent_missing"]+=int(term=="PARENT_MISSING")
        effective_by_mod[mod]+=len(elems)
        kinds[(mod,status)]+=1
        summaries.append({
            "mod":mod,"path":path,"source_sha":row["sha"],"status":"PASS" if not model_issues else "DIFFERENCE",
            "geometry_status":status,"own_elements":len(own),
            "effective_elements":len(elems),"effective_faces":applied_faces,
            "provider":provider[0] if provider else "",
            "chain":"|".join(n[0] for n in chain),"terminal":term,
            "faces_unbound":facestat["SLOT_UNBOUND"],"issues":"|".join(model_issues),
        })
    if len(provider_ids)!=len(provider_to_elements):
        raise ValueError("Provider bookkeeping mismatch")
    for key,elems in provider_to_elements.items():
        for ix,element in enumerate(elems):
            old=b_elems.get((key,ix))
            if old is None:
                discrepancy("ELEMENT",key,f"Missing original element {ix}")
                continue
            values=[
                ("source_from",element["from"]),
                ("source_to",element["to"]),
                ("raw_bbox",bbox(element,False)),
                ("rotated_bbox",bbox(element,True)),
            ]
            for name,value in values:
                if not same_vec(old[name],value):
                    discrepancy("ELEMENT",key,f"Element index {ix} mismatched {name}")
            rot=element.get("rotation",{})
            for name,value in [("angle",float(rot.get("angle",0))),("rescale",int(rot.get("rescale",False)))]:
                if float(old[name])!=value:
                    discrepancy("ELEMENT",key,f"Element index {ix} mismatched {name}")
            if old["axis"]!=rot.get("axis","") or int(old["face_count"])!=len(element.get("faces",{})):
                discrepancy("ELEMENT",key,f"Element index {ix} axis/face count mismatch")
            measured["provider_elements"]+=1
            measured["provider_faces"]+=len(element.get("faces",{}))
            measured["rotated_elements"]+=bool(rot.get("angle",0))
    # Cross-check every C element was actually resolved from an original provider.
    for key in b_elems:
        if key[0] not in provider_to_elements or key[1]>=len(provider_to_elements[key[0]]):
            discrepancy("HISTORIC_ELEMENT",str(key),"C element not reached by fresh lineage")
    measures={
        "source_verified_model_files":measured["model_paths"],
        "source_model_counts":dict(Counter(r["mod"] for r in summaries)),
        "provider_elements":measured["provider_elements"],
        "provider_faces":measured["provider_faces"],
        "distinct_providers":len(provider_ids),
        "effective_element_instances":measured["effective_elements"],
        "effective_face_instances":measured["effective_faces"],
        "static_models":measured["static_models"],
        "no_static_models":measured["model_paths"]-measured["static_models"],
        "parent_missing":measured["parent_missing"],
        "unbound_face_instances":measured["slot_unbound_faces"],
        "slot_cycle_face_instances":measured["slot_cycle_faces"],
        "explicit_uv_face_instances":measured["explicit_uv_faces"],
        "geometry_status_by_mod":{"|".join(k):v for k,v in sorted(kinds.items())},
    }
    mismatched={
       "model_paths":measured["model_paths"]-sum(EXPECTED["models"].values()),
       "static":measures["static_models"]-EXPECTED["static"],
       "no_static":measures["no_static_models"]-EXPECTED["no_static"],
       "effective_elements":measures["effective_element_instances"]-EXPECTED["elements"],
       "effective_faces":measures["effective_face_instances"]-EXPECTED["faces"],
       "declared_elements":measures["provider_elements"]-EXPECTED["declared_elements"],
       "declared_faces":measures["provider_faces"]-EXPECTED["declared_faces"],
       "providers":measures["distinct_providers"]-EXPECTED["providers"],
       "parent_missing":measures["parent_missing"]-EXPECTED["parent_missing"],
    }
    issues=[k for k,v in mismatched.items() if v!=0]
    status="PASS_SOURCE_GEOMETRY_CATALOG_SCOPE" if not issues and measured["discrepancies"]==0 else "DISCREPANCY_REQUIRES_REVIEW"
    report={
      "schema":"MCFR_INT2_MOD_ORIGINAL_MODEL_REAUDIT/v1",
      "baseline_commit":"176f7f34de2336eb7984c4734e97b6eb156c19f4",
      "upstream_pins":{
        "AF":"57eb624cbb7f408d43398c7434b0d38d312cb55d",
        "HC":"8d21d1665916850c3fa3bdaf1370c50ec2ca7035",
        "MACAW_SHA256":"e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e",
      },
      "measures":measures,"aggregate_differences":mismatched,
      "per_model_discrepancies":sum(s["status"]!="PASS" for s in summaries),
      "discrepancy_count":measured["discrepancies"],"discrepancy_examples":errors,
      "exceptions":{"missing_parent_paths":sorted(parent_missing_paths),
                    "no_static_model_ids":sorted(unresolvable)},
      "status":status,
      "not_checked":["official current version update","runtime render","UV rasterization","actual blockstate transforms","Java/Kotlin mixin runtime semantics","licensing reuse"],
      "ai_training_approved":False,
    }
    for archive in vanilla.values():
        archive.close()
    return summaries,report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[2])
    for name in ("af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    rows,report=calculate(args.root,args)
    with (args.out/"INT2_MOD_16572_MODEL_CHECKS.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=OUT_COLS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.out/"INT2_MOD_SOURCE_SUMMARY.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("INT2_MOD_RESULT:"+json.dumps({
      "status":report["status"],"measures":report["measures"],
      "aggregate_differences":report["aggregate_differences"],
      "per_model_discrepancies":report["per_model_discrepancies"],
      "discrepancy_count":report["discrepancy_count"],
      "discrepancy_examples":report["discrepancy_examples"][:8],
    },ensure_ascii=False,sort_keys=True))
    if report["status"]!="PASS_SOURCE_GEOMETRY_CATALOG_SCOPE":
        raise SystemExit("INT2 MOD model audit failed; inspect artifact")

if __name__=="__main__":
    main()
