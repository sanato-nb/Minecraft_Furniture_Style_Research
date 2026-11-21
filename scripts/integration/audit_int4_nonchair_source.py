"""INT-4 independently reopen representative non-chair furniture source state/model/UV links.

Scope: 15 historical 1-5 mod cases across TABLE, SHELVING, BED and KITCHEN.
Independently select source variants/multipart rules and model options; check
actual pinned original file SHA, inherited provider geometry, UV declarations,
resolved face texture slots and original PNG availability. Not a new Minecraft
client rendering, an AI modeling rule or a third-party assets rights approval.
Original mod/source binary files never enter committed results.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import json
from pathlib import Path
import struct

try:
    from scripts.integration.audit_int2_mod_textures import Sources,raw_source_sha
except ModuleNotFoundError as err:
    if err.name not in ("scripts","scripts.integration"):
        raise
    from audit_int2_mod_textures import Sources,raw_source_sha

ROOT=Path(__file__).resolve().parents[2]
BASE="research/furniture_mods/phase_1-5/B/"
APPS=BASE+"APPLICATIONS.csv"
CASES=BASE+"CASES.csv"
CLAIMS="project/integration/INT2_1_5_21_FINDING_CHECKS.csv"
SOURCE_CROSS="project/integration/INT2_MOD_SOURCE_SUMMARY.json"
REACHABILITY="project/integration/INT4_PARENT_48_BLOCKSTATE_AUDIT_RESULT.json"
# Historic 1-5 representative cases. Never add variants or infer cases not in B.
CASE_IDS=(
 "S14","S15","S16","S17","S18","S19", # three-mod connected table
 "S28","S29",                           # Macaw bookshelf base / middle
 "S37","S38",                           # Handcrafted bed foot / head
 "S39","S40","S41",                     # Handcrafted vs Macaw counter
 "S42","S43",                           # Macaw sink water=false / true
)
CLAIM_CASES={
 "C06":("S14","S15","S16","S17","S18","S19"),
 "C12":("S28","S29"),"C16":("S37","S38"),
 "C18":("S39","S40"),"C19":("S39","S40","S41"),
 "C17":("S42","S43"),
}
CATEGORY={
 "S14":"LARGE_TABLE","S15":"LARGE_TABLE","S16":"LARGE_TABLE",
 "S17":"LARGE_TABLE","S18":"LARGE_TABLE","S19":"LARGE_TABLE",
 "S28":"SHELVING","S29":"SHELVING",
 "S37":"BED","S38":"BED",
 "S39":"KITCHEN","S40":"KITCHEN","S41":"KITCHEN",
 "S42":"KITCHEN","S43":"KITCHEN",
}
EXPECTED={
 "S14":(5,13,42),"S15":(1,1,6),"S16":(1,10,60),
 "S17":(1,2,12),"S18":(1,6,31),"S19":(1,1,6),
 "S28":(1,10,31),"S29":(1,8,19),
 "S37":(1,12,72),"S38":(1,1,6),
 "S39":(1,2,12),"S40":(1,2,12),"S41":(1,2,11),
 "S42":(1,16,55),"S43":(1,17,56),
}
MOD_EXPECT={"AF":6,"HC":6,"MACAW":3}
PNG_MAGIC=b"\x89PNG\r\n\x1a\n"

class EvidenceError(ValueError):pass

def ensure(ok,msg):
    if not ok:raise EvidenceError(msg)

def sha(data):return hashlib.sha256(data).hexdigest()

def read_rows(path):
    raw=Path(path).read_bytes()
    return list(csv.DictReader(raw.decode("utf-8-sig").splitlines())),sha(raw)

def obj(data,label):
    def unique(pairs):
        result={}
        for k,v in pairs:
            ensure(k not in result,"Duplicate JSON key in "+label+": "+k)
            result[k]=v
        return result
    value=json.loads(data.decode("utf-8-sig"),object_pairs_hook=unique)
    ensure(isinstance(value,dict),"JSON root invalid: "+label)
    return value

def state_map(spec):
    result={}
    for part in spec.split(";"):
        if not part:continue
        k,sep,value=part.partition("=")
        ensure(bool(sep and k and value and k not in result),"Invalid historic property state: "+spec)
        result[k]=value
    return result

def selector_map(selector):
    result={}
    for part in selector.split(","):
        if not part:continue
        k,sep,value=part.partition("=")
        ensure(bool(sep and k and value and k not in result),"Malformed source selector: "+selector)
        result[k]=value
    return result

def is_when(when,props):
    if when is None or when=={}:return True
    ensure(isinstance(when,dict),"Invalid multipart when")
    def meets(k,v):
        if k=="OR":
            ensure(isinstance(v,list),"Invalid OR multipart alternatives")
            return any(is_when(x,props) for x in v)
        if k=="AND":
            ensure(isinstance(v,list),"Invalid AND multipart alternatives")
            return all(is_when(x,props) for x in v)
        return props.get(k) in str(v).split("|")
    return all(meets(k,v) for k,v in when.items())

def match_state(source,properties):
    """Return matched (source rule index, source option index, source option)."""
    matches=[]
    if "variants" in source:
        entries=source["variants"]
        ensure(isinstance(entries,dict),"Original variants must be object")
        for i,(selector,options) in enumerate(entries.items()):
            parsed=selector_map(selector)
            if parsed==properties:
                for j,option in enumerate(options if isinstance(options,list) else [options]):
                    ensure(isinstance(option,dict),"Original option must be object")
                    matches.append((i,j,option))
    elif "multipart" in source:
        entries=source["multipart"]
        ensure(isinstance(entries,list),"Original multipart must be list")
        for i,row in enumerate(entries):
            ensure(isinstance(row,dict) and "apply" in row,"Original multipart row missing apply")
            if is_when(row.get("when",{}),properties):
                options=row["apply"]
                for j,option in enumerate(options if isinstance(options,list) else [options]):
                    ensure(isinstance(option,dict),"Original multipart option must be object")
                    matches.append((i,j,option))
    else:
        raise EvidenceError("No original static state declaration")
    return matches

def model_path_for_ref(ref):
    ensure(isinstance(ref,str) and ref and ".." not in ref,"Invalid model target")
    if ":" not in ref:
        ref="minecraft:"+ref
    name,body=ref.split(":",1)
    ensure(name and body and not body.startswith("/"),"Invalid model target")
    return f"assets/{name}/models/{body}.json"

def texture_path_for_ref(ref):
    ensure(isinstance(ref,str) and ref and ".." not in ref,"Invalid texture reference")
    if ":" not in ref:ref="minecraft:"+ref
    name,body=ref.split(":",1)
    return f"assets/{name}/textures/{body}.png"

def pin_mod(path,cohort):
    # Prefixes are intrinsic to original git zip/jar paths; don't remove them.
    prefix=path.split("assets/",1)[0]
    ensure("assets/" in path and
           path.startswith(prefix+"assets/"),
           "Original resource has no assets prefix: "+path)
    if cohort=="MACAW":
        ensure(prefix=="","Macaw fixed original JAR unexpectedly has Git source prefix")
    elif cohort in ("AF","HC"):
        ensure(prefix.startswith("common/src/main/"),
               "Git source resource path not rooted in common resources: "+path)
    return path.split("assets/",1)[1].split("/",1)[0]

def load_original(sources,cohort,path,expected_sha,kind,cache):
    key=(cohort,path)
    if key not in cache:
        raw=sources.fetch(cohort,path,required=True)
        actual=raw_source_sha(raw,kind)
        ensure(actual==expected_sha,
               "Original source file SHA differs for "+cohort+":"+path)
        cache[key]=(obj(raw,path),len(raw))
    return cache[key]

def archive_asset(sources,cohort,ns,texture):
    path=texture_path_for_ref(texture)
    actual_ns=path.split("/")[1]
    source=("MC1.21.11" if cohort=="MACAW" else "MC1.21.1") if actual_ns=="minecraft" else cohort
    raw=sources.fetch(source,path,required=False)
    if raw is None:return {"status":"SOURCE_PNG_MISSING","source":source,"path":path}
    ensure(raw.startswith(PNG_MAGIC) and len(raw)>=24,
           "Non-PNG source referenced by original face: "+path)
    w,h=struct.unpack_from(">II",raw,16)
    ensure(w>0 and h>0,"Zero-size original PNG")
    return {"status":"ORIGINAL_PNG_BYTES_PRESENT","source":source,
            "path":path,"sha256":sha(raw),"width":w,"height":h}

def resolve_face_texture(face,slots):
    value=face.get("texture","")
    if not value:return "FACE_TEXTURE_UNDECLARED",""
    seen=set()
    while value.startswith("#"):
        key=value[1:]
        if key in seen:return "CYCLIC_TEXTURE_SLOT",""
        seen.add(key)
        if key not in slots:return "SLOT_UNBOUND",""
        value=slots[key]
        if not isinstance(value,str):return "INVALID_TEXTURE_SLOT",""
    return "TEXTURE_RESOURCE_RESOLVED",value

def verify_application(row,case,sources,cache,png_cache):
    cohort=row["cohort"]
    ensure(cohort in ("AF","HC","MACAW"),"Unexpected mod source")
    kind="SHA256" if cohort=="MACAW" else "GIT_BLOB_SHA1"
    ensure(row["model_hash_kind"]==kind and row["geometry_status"]=="STATIC_SOURCE",
           "Historical application hash algorithm/status changed")
    state,bs=load_original(sources,cohort,row["state_path"],row["state_sha"],kind,cache)
    stateprops=state_map(row["state"])
    matched=match_state(state,stateprops)
    idx=(int(row["rule_index"]),int(row["option_index"]))
    options={(i,j):item for i,j,item in matched}
    ensure(len(matched)==len(options) and idx in options,
           "Historic application source selector not reachable: "+row["case"])
    src=options[idx]
    ensure(model_path_for_ref(src.get("model"))==row["model_path"],
           "Actual original blockstate selected a different model: "+row["case"])
    for key in ("x","y","uvlock","weight"):
        actual=src.get(key,1 if key=="weight" else False if key=="uvlock" else 0)
        exp=(bool(int(row[key])) if key=="uvlock" else int(row[key]))
        ensure(actual==exp,"Original "+key+" option differs: "+row["case"])
    leaf,_=load_original(sources,cohort,row["model_path"],row["model_sha"],kind,cache)
    provider,_=load_original(sources,cohort,row["provider_path"],row["provider_sha"],kind,cache)
    ensure(case["cohort"]==cohort and case["block"]==row["block"] and
           case["minecraft"]==row["minecraft"] and case["category"]==row["category"],
           "Original comparison case identity drift: "+row["case"])
    ensure(cohort=="MACAW" or row["minecraft"]=="1.21.1",
           "Original research-version scope changed")
    if row["provider_path"]!=row["model_path"]:
        parent=leaf.get("parent")
        ensure(isinstance(parent,str) and model_path_for_ref(parent)==
               row["provider_path"].split("assets/",1)[-1].join([]) if False else True,
               "This branch not reached")
        # Compare resource portion while allowing 'common/src/.../' Git prefix.
        expected_ref=row["provider_path"].split("assets/",1)[1]
        ensure(model_path_for_ref(parent)=="assets/"+expected_ref,
               "Child parent does not actually point to pinned provider: "+row["case"])
    elements=provider.get("elements",leaf.get("elements",[]))
    ensure(isinstance(elements,list),"Provider elements not JSON list")
    elem_count=len(elements)
    face_count=sum(len(el.get("faces",{})) for el in elements)
    ensure(elem_count==int(row["elements"]) and face_count==int(row["faces"]),
           "Historic model geometry count differs from pinned original provider: "+row["case"])
    slots={**provider.get("textures",{}),**leaf.get("textures",{})}
    bound=Counter();png_refs=set();face_samples=0;missing_source=set();sample_shapes=set()
    for element in elements:
        ensure(isinstance(element,dict),"Original geometry element invalid")
        for orient,face in element.get("faces",{}).items():
            ensure(isinstance(face,dict),"Original face declaration invalid")
            status,ref=resolve_face_texture(face,slots)
            bound[status]+=1
            if status=="TEXTURE_RESOURCE_RESOLVED":
                if ref not in png_cache:
                    png_cache[ref]=archive_asset(sources,cohort,"",ref)
                png=png_cache[ref]
                bound[png["status"]]+=1
                if png["status"]=="SOURCE_PNG_MISSING":missing_source.add(ref)
                else:
                    png_refs.add((ref,png["source"],png["sha256"]))
                    sample_shapes.add((png["width"],png["height"]))
            face_samples+=1
    ensure(face_samples==face_count,"Face declarations not completely traversed")
    return {
       "case":row["case"],"cohort":cohort,"category":row["category"],
       "block_id":row["block"],"state":row["state"],
       "source_rule_index":row["rule_index"],"source_option_index":row["option_index"],
       "model_path":row["model_path"],"model_source_sha":row["model_sha"],
       "provider_path":row["provider_path"],"provider_source_sha":row["provider_sha"],
       "source_blockstate_sha":row["state_sha"],
       "selected_model_x":row["x"],"selected_model_y":row["y"],"source_uvlock":row["uvlock"],
       "element_count":elem_count,"face_count":face_count,
       "resolved_face_texture_slots":bound["TEXTURE_RESOURCE_RESOLVED"],
       "unresolved_face_texture_slots":face_count-bound["TEXTURE_RESOURCE_RESOLVED"],
       "source_png_present_face_refs":bound["ORIGINAL_PNG_BYTES_PRESENT"],
       "source_png_missing_face_refs":bound["SOURCE_PNG_MISSING"],
       "distinct_original_png_sources":len(png_refs),
       "png_source_sha256_pairs":"|".join(f"{a}:{c}" for a,b,c in sorted(png_refs)),
       "declared_original_png_dimensions":"|".join(f"{w}x{h}" for w,h in sorted(sample_shapes)),
       "source_missing_png_resources":"|".join(sorted(missing_source)),
       "original_source_crosschecked":True,
       "client_runtime_render_proven":False,
       "modeling_semantics_approved":False,
       "source_license_ai_training_approved":False,
    }

def check_pairs(bycase,case_records):
    for case,expected in EXPECTED.items():
        parts=bycase.get(case,[])
        ensure(len(parts)==expected[0],"Comparison selected model option count drift: "+case)
        ensure(sum(p["element_count"] for p in parts)==expected[1] and
               sum(p["face_count"] for p in parts)==expected[2],
               "Original source element/face count mismatch for "+case)
        ensure(case_records[case]["elements"]==str(expected[1]) and
               case_records[case]["faces"]==str(expected[2]),
               "Historic B comparison surface census drift for "+case)
    pairs=[
      ("TABLE_MULTIPART_AF","S14","S15"),
      ("TABLE_CONNECTED_MACAW","S18","S19"),
      ("BOOKSHELF_CONNECTION","S28","S29"),
      ("BED_FOOT_HEAD","S37","S38"),
      ("COUNTER_FINISH_HC","S39","S40"),
      ("SINK_WATER_MACAW","S42","S43"),
    ]
    out=[]
    for kind,left,right in pairs:
        l,r=bycase[left],bycase[right]
        lm={x["model_source_sha"] for x in l}
        rm={x["model_source_sha"] for x in r}
        out.append({
           "comparison":kind,"left_case":left,"right_case":right,
           "left_application_options":len(l),"right_application_options":len(r),
           "left_element_count":sum(x["element_count"] for x in l),
           "right_element_count":sum(x["element_count"] for x in r),
           "left_face_count":sum(x["face_count"] for x in l),
           "right_face_count":sum(x["face_count"] for x in r),
           "shared_leaf_model_sha":bool(lm&rm),
           "client_visual_equivalence_approved":False,
           "semantic_universal_rule_approved":False,
        })
    ensure(out[-1]["right_face_count"]==out[-1]["left_face_count"]+1,
           "Original filled sink face-count change not reproduced")
    return out

def audit(root,args):
    root=Path(root)
    app,app_sha=read_rows(root/APPS)
    cases,case_sha=read_rows(root/CASES)
    claims,claim_sha=read_rows(root/CLAIMS)
    bycase={r["case"]:r for r in cases}
    ensure(len(bycase)==len(cases)==62 and
           set(CASE_IDS).issubset(bycase) and len(CASE_IDS)==len(set(CASE_IDS))==15,
           "Historical 1-5 case ledger changed")
    selected=[x for x in app if x["case"] in CASE_IDS]
    ensure(len(app)==74 and len(selected)==19 and
           {x["case"] for x in selected}==set(CASE_IDS),
           "Historical 74 model applications / selected 19 drift")
    ensure(set(CATEGORY)==set(CASE_IDS),"Case category mapping drift")
    for case in CASE_IDS:
        ensure(bycase[case]["category"]==CATEGORY[case],
               "Original chosen study furniture category changed")
    claimmap={r["finding_id"]:r for r in claims}
    ensure(len(claimmap)==len(claims)==21 and
           set(CLAIM_CASES).issubset(claimmap) and
           all(claimmap[key]["status"]=="PASS" and
               claimmap[key]["runtime_evidence_status"]=="HISTORIC_ONLY_NOT_REEXECUTED" and
               set(required).issubset(set(claimmap[key]["cases"].split("|")))
               for key,required in CLAIM_CASES.items()),
           "1-5 C claims or follow-up scope changed")
    prior=json.loads((root/REACHABILITY).read_text())
    ensure(prior["observed"]["summary"]["historical_missing_parent_model_paths"]==48 and
           prior["observed"]["summary"]["in_static_blockstate_source_selection_or_parent_chain"]==0,
           "Previous INT4 unused missing-parent scope changed")
    original=Sources(args)
    cache={};pngcache={}
    try:
        rows=[verify_application(row,bycase[row["case"]],original,cache,pngcache)
              for row in selected]
    finally:
        original.close()
    result=defaultdict(list)
    for row in rows:result[row["case"]].append(row)
    related=check_pairs(result,bycase)
    mod_cases=Counter(bycase[case]["cohort"] for case in CASE_IDS)
    ensure(dict(mod_cases)=={"AF":2,"HC":6,"MACAW":7},
           "Historical selected case source-family scope drift")
    counts=Counter()
    for row in rows:
        counts["elements"]+=row["element_count"]
        counts["faces"]+=row["face_count"]
        counts["faces_resolved"]+=row["resolved_face_texture_slots"]
        counts["faces_unresolved"]+=row["unresolved_face_texture_slots"]
        counts["png_present_face_refs"]+=row["source_png_present_face_refs"]
        counts["png_missing_face_refs"]+=row["source_png_missing_face_refs"]
    ensure(counts["faces"]==sum(EXPECTED[c][2] for c in CASE_IDS),
           "Source geometry differs from historical 15-case face census")
    report={
      "schema":"MCFR_INT4_NONCHAIR_15_CASES_ORIGINAL_SOURCE_CROSSCHECK/v1",
      "status":"PASS_SOURCE_SELECTED_MODELS_GEOMETRY_TEXTURE_REFERENCE_SCOPE_NOT_CLIENT_VISUAL",
      "historical_research_scope":{
          "1_5_cases_total":62,"1_5_applications_total":74,
          "1_5_C_claims_total":21,
          "case_ids":list(CASE_IDS),
          "historic_C_comparison_ids":list(CLAIM_CASES),
          "categories":sorted(set(CATEGORY.values())),
          "mod_cohorts":dict(sorted(mod_cases.items())),
      },
      "results":{
          "cases_checked":len(CASE_IDS),
          "application_options_reopened":len(rows),
          "distinct_source_file_metadata_checked":len(cache),
          "distinct_texture_resource_ids_checked":len(pngcache),
          "paired_case_comparisons":len(related),
          **dict(counts),
      },
      "source_ledger_sha256":{
          APPS:app_sha,CASES:case_sha,CLAIMS:claim_sha,
          REACHABILITY:sha((root/REACHABILITY).read_bytes())
      },
      "scope_boundaries":{
          "original_json_source_hashes_and_selected_geometry_checked":True,
          "original_png_reference_presence_checked":True,
          "full_png_rgba_or_packed_atlas_equality_proven":False,
          "minecraft_client_render_reexecuted":False,
          "runtime_blockstate_practically_achievable":False,
          "original_1_5_histories_overwritten":False,
          "part_role_or_style_approved":0,
          "source_copyright_or_ai_training_rights_approved":0,
          "int4_all_furniture_audited":False,
      },
    }
    return rows,related,report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("af","hc","macaw","mc1211","mc12111"):
        p.add_argument("--"+x,type=Path,required=True)
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args(argv)
    ensure(not args.out.exists(),"Refuse to overwrite prior case audit outputs")
    rows,pairs,doc=audit(args.root,args)
    args.out.mkdir(parents=True)
    def write(name,records):
        path=args.out/name
        with path.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator="\n")
            writer.writeheader();writer.writerows(records)
        return sha(path.read_bytes())
    doc["csv_sha256"]={
      "INT4_NONCHAIR_19_ORIGINAL_APPLICATIONS.csv":write("INT4_NONCHAIR_19_ORIGINAL_APPLICATIONS.csv",rows),
      "INT4_NONCHAIR_6_PAIR_CROSSCHECKS.csv":write("INT4_NONCHAIR_6_PAIR_CROSSCHECKS.csv",pairs)
    }
    (args.out/"INT4_NONCHAIR_15_CASES_SUMMARY.json").write_text(
        json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8")
    print(json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
