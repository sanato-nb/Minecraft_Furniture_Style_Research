"""H21 exact 16 AF historical selections: pinned Git 4.0.3 vs official Fabric 4.0.2.

Only derived hashes and comparison facts are persisted. No game launch or
new F2, no original source files, no all-version equivalence/rights claim.
"""
import argparse
from collections import Counter,defaultdict
import csv
from fractions import Fraction
import hashlib
import io
import json
import lzma
from pathlib import Path
import runpy
from zipfile import ZipFile
from PIL import Image

AF="c2f992081bdc4795ed6d87771a3b5f7c71103785"
AF256="3f0e6c276dde5cd6390e9c14bc4c283e4043f25d812c1f5ecc36b7b2f61642b5"
MC="30c73b1c5da787909b2f73340419fdf13b9def88"
GIT="57eb624cbb7f408d43398c7434b0d38d312cb55d"
IDS=set("S01 S02 S03 S04 S05 S14 S15 S20 S21 S26 S30 S31 S32 S44 S45 S46".split())
B=Path("research/furniture_mods/phase_1-5/B")
I=Path("project/integration")
def req(ok,msg):
    if not ok:raise ValueError("H21 "+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rawhash(b,kind):
    req(kind in ("SHA256","GIT_BLOB_SHA1"),"unknown original hash kind "+kind)
    return sha(b) if kind=="SHA256" else blob(b)
def rows(path):
    op=lzma.open if path.suffix==".xz" else open
    with op(path,"rt",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def doc(b):
    def unique(pairs):
        d=dict(pairs)
        req(len(d)==len(pairs),"duplicate JSON key")
        return d
    return json.loads(b,object_pairs_hook=unique)
def resource(ref,kind):
    ns,name=ref.split(":",1) if ":" in ref else ("minecraft",ref)
    req(ns in ("minecraft","another_furniture") and all(x not in ("",".","..") for x in name.split("/")),"bad resource "+ref)
    return f"assets/{ns}/{kind}/{name}."+("png" if kind=="textures" else "json")
def norm(ref):return ref if ":" in ref else "minecraft:"+ref
def state_props(s):return dict(p.split("=") for p in s.replace(";",",").split(",") if p)
def matches(when,props):
    if not when:return True
    for k,v in when.items():
        if k=="AND":
            if not all(matches(w,props) for w in v):return False
        elif k=="OR":
            if not any(matches(w,props) for w in v):return False
        elif props.get(k) not in str(v).split("|"):return False
    return True
def select(d,props):
    req(("variants" in d)!=("multipart" in d),"invalid blockstate")
    out=[]
    if "variants" in d:
        for i,(selector,opts) in enumerate(d["variants"].items()):
            if state_props(selector)==props:
                out.extend((i,j,o) for j,o in enumerate(opts if isinstance(opts,list) else [opts]))
        req(len({i for i,_,_ in out})==1,"ambiguous or missing variant")
    else:
        for i,r in enumerate(d["multipart"]):
            if matches(r.get("when"),props):
                opts=r["apply"]
                out.extend((i,j,o) for j,o in enumerate(opts if isinstance(opts,list) else [opts]))
    req(bool(out),"empty selected applications")
    return out
def option(o):
    return (resource(o["model"],"models"),o.get("x",0),o.get("y",0),bool(o.get("uvlock",False)),o.get("weight",1))
def strip(p):return "assets/"+p.split("assets/",1)[1]
def appkey(a):return a["case"],a["rule_index"],a["option_index"]
def source_option(a):return (strip(a["model_path"]),int(a["x"]),int(a["y"]),bool(int(a["uvlock"])),int(a["weight"]))

class Source:
    def __init__(self,git,release,vanilla):
        self.z={"study":git,"release":release,"vanilla":vanilla}
        self.names={s:set(z.namelist()) for s,z in self.z.items()}
        self.files={};self.pairs={}
        for s,z in self.z.items():req(z.testzip() is None and len(z.namelist())==len(self.names[s]),"bad ZIP "+s)
        roots={p.split("/",1)[0] for p in self.names["study"]}
        req(roots=={"AnotherFurniture-"+GIT},"pinned git root drift")
        self.root=next(iter(roots))+"/"
        req("mod_version=4.0.3" in self.z["study"].read(self.root+"gradle.properties").decode().replace(" ",""),"study version")
    def read(self,side,path,optional=False):
        k=(side,path)
        if k in self.files:return self.files[k]
        if path.startswith("assets/minecraft/"):
            zside="vanilla";actual=path
        elif side=="study":
            zside=side
            candidates=[self.root+"common/src/main/"+r+"/"+path for r in ("resources","generated/resources")]
            found=[x for x in candidates if x in self.names[zside]]
            req(len(found)<=1,"ambiguous Git asset "+path)
            actual=found[0] if found else None
        else:zside=side;actual=path
        if not actual or actual not in self.names[zside]:
            req(optional,"missing "+side+" "+path)
            return None
        result=self.z[zside].read(actual)
        self.files[k]=result
        return result
    def compare(self,path,kind):
        if path in self.pairs:return self.pairs[path]
        a,b=self.read("study",path),self.read("release",path)
        result={"path":path,"kind":kind,"study_git_blob_sha1":blob(a),"release_sha256":sha(b),"raw_equal":a==b}
        if kind=="json":
            result["equivalent"]=doc(a)==doc(b)
        else:
            with Image.open(io.BytesIO(a)) as im:
                req(im.format=="PNG","study texture not PNG")
                aa=im.convert("RGBA")
            with Image.open(io.BytesIO(b)) as im:
                req(im.format=="PNG","release texture not PNG")
                bb=im.convert("RGBA")
            result.update(study_size=list(aa.size),release_size=list(bb.size),
                          study_rgba_sha256=sha(aa.tobytes()),release_rgba_sha256=sha(bb.tobytes()),
                          rgba_equal=aa.size==bb.size and aa.tobytes()==bb.tobytes())
            ma,mb=self.read("study",path+".mcmeta",True),self.read("release",path+".mcmeta",True)
            result["animation_metadata_equal"]=(ma is None and mb is None) or (ma is not None and mb is not None and doc(ma)==doc(mb))
            result["study_mcmeta_sha256"]=sha(ma) if ma else None
            result["release_mcmeta_sha256"]=sha(mb) if mb else None
            result["equivalent"]=result["rgba_equal"] and result["animation_metadata_equal"]
        self.pairs[path]=result
        return result

def model(src,side,leaf):
    chain=[];seen=set();p=leaf
    while p:
        req(p not in seen and len(chain)<30,"parent cycle "+p)
        seen.add(p);raw=src.read(side,p);d=doc(raw)
        chain.append((p,d))
        ref=d.get("parent")
        p=resource(ref,"models") if ref else None
    textures={};elements=None;provider=None;settings={}
    for p,d in reversed(chain):
        textures.update(d.get("textures",{}))
        if "elements" in d:elements=d["elements"];provider=p
        for k in ("ambientocclusion","render_type","gui_light","display"):
            if k in d:settings[k]=d[k]
    req(isinstance(elements,list) and elements,"missing model geometry")
    return {"chain":[p for p,_ in reversed(chain)],"provider":provider,"elements":elements,"textures":textures,"settings":settings}
def resolve(slots,ref):
    seen=set()
    while ref.startswith("#"):
        k=ref[1:];req(k not in seen and k in slots,"unresolved texture "+ref)
        seen.add(k);ref=slots[k]
    return norm(ref)
def fval(seq):return tuple(Fraction(str(x)) for x in seq)
def uv_values(e,d,face):
    if "uv" in face:return fval(face["uv"]),"EXPLICIT"
    x,y,z=fval(e["from"]);X,Y,Z=fval(e["to"])
    return {"down":(x,16-Z,X,16-z),"up":(x,z,X,Z),
            "north":(16-X,16-Y,16-x,16-y),"south":(x,16-Y,X,16-y),
            "west":(z,16-Y,Z,16-y),"east":(16-Z,16-Y,16-z,16-y)}[d],"DEFAULT"
def inspect_faces(m):
    out={}
    for n,e in enumerate(m["elements"]):
        for direction,face in e["faces"].items():
            u,method=uv_values(e,direction,face)
            out[(str(n),direction)]={"uv":[str(v) for v in u],"uv_method":method,
                "resource":resolve(m["textures"],face["texture"]),
                "rotation":face.get("rotation",0),"cullface":face.get("cullface",""),"tintindex":face.get("tintindex","")}
    return out

def audit(args):
    release=Path(args.release);mc=Path(args.vanilla);git=Path(args.study)
    req(hashlib.sha1(release.read_bytes()).hexdigest()==AF and sha(release.read_bytes())==AF256,"official AF hash")
    req(hashlib.sha1(mc.read_bytes()).hexdigest()==MC,"official vanilla SHA1")
    pins={
      str(B/"APPLICATIONS.csv"):"56e6f4c21c50714b97079ec61f7219bea845f179",
      str(B/"FACES.csv.xz"):"761d2a62ab5010aa5a4d4311218153b2f80678df",
      str(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv"):"4c220f4026bb187ce9a61634073fb4e4cf9247e7",
      str(I/"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv"):"54fbaa1b89c29c46106ade51638f8170306a15b0",
      str(I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"):"f820efd9e85c4cee8df4673a2db4f4d868b4de31",
      str(I/"INT4_NONCHAIR_RUNTIME_RESULT.json"):"6c84593b921c972589132cdee9c48b0716af6eb9",
      str(I/"INT4_H03_H05_S20_S21_REAL_NORTH_F2_RESULT_V1.json"):"ddb2e728f8f5973024251ceb2fc52f65d7e347db",
    }
    for p,h in pins.items():req(blob(Path(p).read_bytes())==h,"frozen source drift "+p)
    apps=[a for a in rows(B/"APPLICATIONS.csv") if a["cohort"]=="AF"]
    req({a["case"] for a in apps}==IDS and len(apps)==21,"AF application denominator")
    group=defaultdict(list)
    for f in rows(B/"FACES.csv.xz"):
        if f["case"] in IDS:group[appkey(f)].append(f)
    old={r["target_id"]:r for r in rows(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv")}
    h6={r["target_id"]:r for r in rows(I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv")}
    h97={r["target_id"]:r for r in rows(I/"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv")}
    nonchair=doc((I/"INT4_NONCHAIR_RUNTIME_RESULT.json").read_bytes())["runs"]["1.21.1"]
    drawer=doc((I/"INT4_H03_H05_S20_S21_REAL_NORTH_F2_RESULT_V1.json").read_bytes())
    result={}
    with ZipFile(git) as g,ZipFile(release) as r,ZipFile(mc) as v:
        src=Source(g,r,v)
        for id in sorted(IDS):
            aa=[a for a in apps if a["case"]==id];first=aa[0]
            state=strip(first["state_path"]);props=state_props(first["state"])
            src.compare(state,"json")
            sd=doc(src.read("study",state));rd=doc(src.read("release",state))
            sm=select(sd,props);rm=select(rd,props)
            expected=Counter(source_option(a) for a in aa)
            req(Counter(option(x) for _,_,x in sm)==expected,"historical selected apps "+id)
            selectors_equal=Counter(option(x) for _,_,x in rm)==expected
            issues=[] if selectors_equal else ["release_selected_application_difference"]
            state_eq=src.pairs[state]["equivalent"]
            application_results=[]
            used={state}
            for a in aa:
                k=appkey(a);leaf=strip(a["model_path"]);provider=strip(a["provider_path"])
                req(blob(src.read("study",state))==a["state_sha"] and blob(src.read("study",leaf))==a["model_sha"] and blob(src.read("study",provider))==a["provider_sha"],"historical JSON hashes "+id)
                chosen={(i,j):o for i,j,o in sm}
                req(option(chosen[(int(a["rule_index"]),int(a["option_index"]))])==source_option(a),"historical option key "+id)
                s=model(src,"study",leaf);t=model(src,"release",leaf)
                req(s["provider"]==provider,"historical provider "+id)
                chain_equal=s["chain"]==t["chain"]
                for p in set(s["chain"])|set(t["chain"]):
                    src.compare(p,"json");used.add(p)
                sf,tf=inspect_faces(s),inspect_faces(t)
                req(len(s["elements"])==int(a["elements"]) and len(sf)==int(a["faces"]),"historical model count "+id)
                history=group[k]
                req(len(history)==len(sf) and {(f["element_index"],f["direction"]) for f in history}==set(sf),"historical face keys "+id)
                for f in history:
                    face=sf[(f["element_index"],f["direction"])]
                    tex=resource(face["resource"],"textures")
                    req(face["resource"]==norm(f["resource_id"]) and tex==strip(f["png_path"]),"historical face texture "+id)
                    req(fval(face["uv"])==fval(f["uv"].split("|")) and face["uv_method"]==f["uv_method"] and int(f["uv_rotation"])==face["rotation"] and str(face["cullface"])==f["cullface"] and str(face["tintindex"])==f["tintindex"],"historical face UV "+id+" "+str((f,face)))
                    req(rawhash(src.read("study",tex),f["png_hash_kind"])==f["png_sha"],"historical PNG digest "+id+" "+tex)
                    src.compare(tex,"png");used.add(tex)
                for face in tf.values():
                    tex=resource(face["resource"],"textures");src.compare(tex,"png");used.add(tex)
                dims_equal=s["elements"]==t["elements"]
                face_equal=sf==tf
                chain_json_equal=chain_equal and all(src.pairs[p]["equivalent"] for p in s["chain"])
                if not (chain_json_equal and dims_equal and face_equal and s["settings"]==t["settings"]):
                    issues.append("selected_effective_model_difference:"+leaf)
                application_results.append({"historical_rule":int(a["rule_index"]),"historical_option":int(a["option_index"]),
                   "leaf":leaf,"provider":provider,"x":int(a["x"]),"y":int(a["y"]),"uvlock":bool(int(a["uvlock"])),
                   "elements":len(s["elements"]),"faces":len(sf),"parent_chain":s["chain"],
                   "chain_json_equal":chain_json_equal,"elements_equal":dims_equal,"face_uv_bindings_equal":face_equal,
                   "historical_face_png_hash_and_uv_rows_verified":len(history)})
            texs=sorted(p for p in used if src.pairs[p]["kind"]=="png")
            if any(not src.pairs[p]["equivalent"] for p in texs):issues.append("texture_RGBA_or_animation_difference")
            # Reuse prior exact original capture provenance rather than simulate.
            pr=old[id];h=h6[id];q=h97[id]
            req(pr["modeling_status"]=="CONDITIONAL_MODELING" and pr["original_f2_sha256s"],"prior disposition "+id)
            capture=all(h[k]=="true" for k in ("ZIP_CRC_and_all_PNG_SHA_verified","whole_client_log_sha_matched_capture_report","has_case_specific_structured_server_exact","has_capture_record_exact_image_name_and_sha")) and q["source_case_manifest_exact_meta"]=="true"
            visual={"existing_run":pr["original_f2_run_ids"],"existing_F2_sha256":pr["original_f2_sha256s"],"existing_exact_capture_evidence":capture}
            if id in ("S14","S15"):
                n=nonchair["source"]["representative_states"][id]
                capture=capture and nonchair["source"]["release_jar_sha1"]["AF"]==AF and nonchair["server_states"][id]["subject"]["exact"] and nonchair["native_f2_sha256"][id]==pr["original_f2_sha256s"] and n["historical_selection_matches_release"] and Counter(tuple(x) for x in n["release_model_applications"])==expected
                visual["historic_nonchair_manifest_release_pin_and_selection_verified"]=capture
            if id in ("S20","S21"):
                p=drawer["verified_new_real_game"]
                capture=capture and drawer["source_model"]["official_original_AF_mod_jar_sha1"]==AF and p["exact_game_state_markers_2_of_2"] and p["independent_actual_PNG_SHA_and_dimensions_2_of_2"] and p["new_north_open_closed_RGB24_changed_screen_pixels"]==1208
                visual.update(front_run=p["github_actions_run"],front_F2_sha256=p[id.lower()+"_native_F2_sha256"],front_pair_changed_pixels=1208)
            if not capture:issues.append("original_exact_F2_source_link_incomplete")
            result[id]={"state":first["state"],"block":first["block"],"selected_options_equal":selectors_equal,"entire_blockstate_JSON_equal":state_eq,
                "applications":application_results,"texture_paths":texs,"all_compared_paths":sorted(used),
                "existing_visual_evidence":visual,"issues":sorted(set(issues)),
                "modeling_status":"PASS_MODELING_SCOPE" if not issues else "CONDITIONAL_MODELING"}
        pairs=src.pairs
    counts=Counter(x["modeling_status"] for x in result.values())
    out={"schema":"MCFR_INT4_H21_AF16_PINNED_SOURCE_RELEASE_MODEL_UV_V1",
         "study_commit":GIT,"release_jar_sha1":AF,"release_jar_sha256":AF256,"vanilla_client_sha1":MC,
         "source_ledger_git_blobs":pins,"case_count":16,"application_count":len(apps),"face_count":sum(len(x) for x in group.values()),
         "counts":dict(counts),"cases":result,"asset_comparisons":dict(sorted(pairs.items())),
         "asset_counts":{"json":sum(x["kind"]=="json" for x in pairs.values()),"png":sum(x["kind"]=="png" for x in pairs.values()),
                         "raw_equal":sum(x["raw_equal"] for x in pairs.values()),"equivalent":sum(x["equivalent"] for x in pairs.values())},
         "new_game_runs":0,"new_F2":0,"legacy_F70_unconditional":0,"INT5":0,"INT6":0,
         "limits":["Selected historical world states only; no blanket 4.0.2/4.0.3 equivalence.",
                   "Git source assets vs official release assets, not an official Fabric 4.0.3 release.",
                   "Original F2 state evidence reused; no fresh live GPU per-face attribution or visual reinspection.",
                   "Shared vanilla inheritance resolved against official Minecraft 1.21.1 client.",
                   "No original asset bytes distributed."]}
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print("H21_SUMMARY",json.dumps({k:out[k] for k in ("case_count","application_count","face_count","counts","asset_counts")},sort_keys=True))
    print("H21_CASES",json.dumps({k:v["issues"] for k,v in result.items()},sort_keys=True))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("study","release","vanilla","output"):p.add_argument("--"+name,required=True)
    audit(p.parse_args())
