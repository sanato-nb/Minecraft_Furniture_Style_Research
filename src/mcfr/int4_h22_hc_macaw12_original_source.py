"""H22: reconcile twelve historical HC/Macaw model cases with original runtime assets.

Read only pinned originals and existing exact F2 provenance. Preserve legacy F
approval and keep R06 temporal causality separate from S43 static source UV.
"""
import argparse
from collections import Counter,defaultdict
import csv,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
from . import int4_h21_af16_release_comparison as h

I=h.I; B=h.B
IDS=set("S16 S17 S18 S19 S28 S29 S38 S39 S40 S41 S42 S43".split())
HC=set("S16 S17 S38 S39 S40".split())
HC_GIT="8d21d1665916850c3fa3bdaf1370c50ec2ca7035"
HC_SHA="a9579fecd7ed429c282be21d5c921d220197acc6"
MAC_SHA="28f0929b6005bc28b1bde475579c13020420ae9f"
MAC256="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
MC_SHA={"HC":"30c73b1c5da787909b2f73340419fdf13b9def88","MACAW":"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"}
PINS={
 str(B/"APPLICATIONS.csv"):"56e6f4c21c50714b97079ec61f7219bea845f179",
 str(B/"FACES.csv.xz"):"761d2a62ab5010aa5a4d4311218153b2f80678df",
 str(B/"ANIMATION_FRAMES.csv.xz"):"b76f1fb05096f069562465727dd2b4f5605f5a49",
 str(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv"):"fdd0a872dfee1f938a74637a914b91956a71f82e",
 str(I/"INT4_F70_MODELING_CONTRACT_SUMMARY_V3.json"):"7bb110bf8c9bd38c705ef0892edb58ed4c26d173",
 str(I/"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv"):"54fbaa1b89c29c46106ade51638f8170306a15b0",
 str(I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"):"f820efd9e85c4cee8df4673a2db4f4d868b4de31",
 str(I/"INT4_NONCHAIR_RUNTIME_RESULT.json"):"6c84593b921c972589132cdee9c48b0716af6eb9",
 str(I/"INT4_MACAW_TABLE_SHELF_F2_SOURCE_RESULT.json"):"2423aaf1c89c6bfd54d9eef0f91489249078a5d4",
 str(I/"INT4_MACAW_KITCHEN_F2_SOURCE_RESULT.json"):"707139b52a93e4abbb9c1899b39d7b5b1fb4ebbb",
 str(I/"INT4_HANDCRAFTED_BED_F2_SOURCE_RESULT.json"):"107b2b2c47a19cd8fb36939cc7f516111ed7548b",
}
def req(ok,msg):
    if not ok:raise ValueError("H22 "+msg)
def resource(ref,kind):
    ns,name=h.norm(ref).split(":",1)
    req(ns in ("minecraft","handcrafted","mcwfurnitures") and all(x not in ("",".","..") for x in name.split("/")),"invalid resource "+ref)
    return f"assets/{ns}/{kind}/{name}."+("png" if kind=="textures" else "json")
def opt(o):
    return (resource(o["model"],"models"),o.get("x",0),o.get("y",0),bool(o.get("uvlock",False)),o.get("weight",1))
def load(name):return h.doc((I/name).read_bytes())
def idx(path,k):
    r=h.rows(path);d={x[k]:x for x in r};req(len(r)==len(d),"duplicate "+str(path));return d

class Source(h.Source):
    def __init__(self,git,release,vanilla,cohort):
        self.z={"study":git if cohort=="HC" else release,"release":release,"vanilla":vanilla}
        self.names={s:set(z.namelist()) for s,z in self.z.items()}
        self.files={};self.pairs={};self.cohort=cohort
        for s,z in self.z.items():req(z.testzip() is None and len(z.namelist())==len(self.names[s]),"bad original archive "+cohort+" "+s)
        if cohort=="HC":
            roots={p.split("/",1)[0] for p in self.names["study"]}
            req(len(roots)==1 and next(iter(roots)).endswith("-"+HC_GIT),"study Git root")
            self.root=next(iter(roots))+"/"
    def read(self,side,path,optional=False):
        if self.cohort=="MACAW" and side=="study":side="release"
        return super().read(side,path,optional)

def model(src,side,leaf):
    chain=[];seen=set();p=leaf
    while p:
        req(p not in seen and len(chain)<30,"parent cycle")
        seen.add(p);d=h.doc(src.read(side,p));chain.append((p,d))
        p=resource(d["parent"],"models") if d.get("parent") else None
    slots={};elements=None;provider=None;settings={}
    for p,d in reversed(chain):
        slots.update(d.get("textures",{}))
        if "elements" in d:elements=d["elements"];provider=p
        for k in ("ambientocclusion","render_type","gui_light","display"):
            if k in d:settings[k]=d[k]
    req(isinstance(elements,list) and elements,"missing source geometry")
    return dict(chain=[p for p,_ in reversed(chain)],provider=provider,elements=elements,textures=slots,settings=settings)

def capture(id,old,non,table,kitchen,bed):
    digest=old["original_f2_sha256s"];run=int(old["original_f2_run_ids"])
    if id in {"S16","S17","S39","S40"}:
        n=non["runs"]["1.21.1"];c=n["source"]["representative_states"][id]
        req(run==44986580186 and n["source"]["release_jar_sha1"]["HC"]==HC_SHA and n["native_f2_sha256"][id]==digest and n["server_states"][id]["subject"]["exact"] and c["historical_selection_matches_release"],"HC nonchair original capture "+id)
        return {"run":run,"F2_sha256":digest,"release_pin":HC_SHA,"source_record":"INT4_NONCHAIR_RUNTIME_RESULT.json","manifest_source_files":c["source_files"],"manifest_options":c["release_model_applications"]}
    if id=="S38":
        n=bed["first_paired_background_controlled_f2"];a=n["observed"]
        req(run==n["run_id"] and n["source_release_mod_jar_sha1"]==HC_SHA and n["source_git_commit"]==HC_GIT and n["selected_original_git_source_equal_release_json"][id] and a["native_f2_sha256"][id]==digest and a["server_verified"]==2 and a["same_camera_bed_vs_air_changed_pixels"][id]==465,"HC bed exact capture")
        return {"run":run,"F2_sha256":digest,"release_pin":HC_SHA,"source_record":"INT4_HANDCRAFTED_BED_F2_SOURCE_RESULT.json","air_control_changed_pixels":465}
    if id in {"S18","S19","S28","S29"}:
        a=table["first_actual_game_audit"]
        req(run==table["first_successful_workflow_run_id"] and table["original_mod_jar_sha256"]==MAC256 and a["f2_sha256"][id]==digest and a["server_verified_states"]==4 and a["boundaries"]["explicit_setblock_source_states_verified"],"Macaw table/shelf capture "+id)
        return {"run":run,"F2_sha256":digest,"release_pin":MAC256,"source_record":"INT4_MACAW_TABLE_SHELF_F2_SOURCE_RESULT.json","source_faces":a["source_1_5_face_counts"][id]}
    a=kitchen["first_successful_actual_game_audit"]
    req(run==kitchen["first_successful_ci_run"] and kitchen["scope"]["source_macaw_mod_jar_original_sha256"]==MAC256 and a["f2_sha256_by_case"][id]==digest and a["server_source_verified_count"]==3,"Macaw kitchen capture "+id)
    return {"run":run,"F2_sha256":digest,"release_pin":MAC256,"source_record":"INT4_MACAW_KITCHEN_F2_SOURCE_RESULT.json","water_face_delta":a["source_water_face_delta"]}

def audit(args):
    files={k:Path(getattr(args,k)) for k in ("hc_git","hc_jar","macaw_jar","mc1211","mc12111")}
    for key,pin in {"hc_jar":HC_SHA,"macaw_jar":MAC_SHA,"mc1211":MC_SHA["HC"],"mc12111":MC_SHA["MACAW"]}.items():
        req(hashlib.sha1(files[key].read_bytes()).hexdigest()==pin,"original SHA1 "+key)
    req(h.sha(files["macaw_jar"].read_bytes())==MAC256,"Macaw original SHA256")
    for p,d in PINS.items():req(h.blob(Path(p).read_bytes())==d,"historic ledger changed "+p)
    old=idx(I/"INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv","target_id")
    log=idx(I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv","target_id")
    fresh=idx(I/"INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv","target_id")
    apps=[a for a in h.rows(B/"APPLICATIONS.csv") if a["case"] in IDS]
    req(len(apps)==12 and {a["case"] for a in apps}==IDS,"historical cases")
    faces=defaultdict(list)
    for f in h.rows(B/"FACES.csv.xz"):
        if f["case"] in IDS:faces[h.appkey(f)].append(f)
    anim=[r for r in h.rows(B/"ANIMATION_FRAMES.csv.xz") if r["case"] in IDS]
    non=load("INT4_NONCHAIR_RUNTIME_RESULT.json");table=load("INT4_MACAW_TABLE_SHELF_F2_SOURCE_RESULT.json")
    kitchen=load("INT4_MACAW_KITCHEN_F2_SOURCE_RESULT.json");bed=load("INT4_HANDCRAFTED_BED_F2_SOURCE_RESULT.json")
    result={};assets={}
    with ZipFile(files["hc_git"]) as g,ZipFile(files["hc_jar"]) as hc,ZipFile(files["macaw_jar"]) as mc,ZipFile(files["mc1211"]) as v1,ZipFile(files["mc12111"]) as v2:
        for cohort,src in (("HC",Source(g,hc,v1,"HC")),("MACAW",Source(None,mc,v2,"MACAW"))):
            for a in sorted((x for x in apps if x["cohort"]==cohort),key=lambda x:x["case"]):
                id=a["case"];pr=old[id];k=h.appkey(a);state=h.strip(a["state_path"]);leaf=h.strip(a["model_path"]);provider=h.strip(a["provider_path"]);kind=a["model_hash_kind"]
                req(pr["modeling_status"]=="CONDITIONAL_MODELING" and (id in HC)==(cohort=="HC"),"unexpected prior case")
                for field,p in (("state",state),("model",leaf),("provider",provider)):
                    req(h.rawhash(src.read("study",p),kind)==a[field+"_sha"],"historical JSON hash "+id+" "+field)
                c=capture(id,pr,non,table,kitchen,bed)
                for flag in ("ZIP_CRC_and_all_PNG_SHA_verified","whole_client_log_sha_matched_capture_report","has_case_specific_structured_server_exact","has_capture_record_exact_image_name_and_sha"):
                    req(log[id][flag]=="true","F2 source "+id+" "+flag)
                req(fresh[id]["source_case_manifest_exact_meta"]=="true" and fresh[id]["historical_human_visual_qualitative_text_present"]=="true","prior reopened capture "+id)
                props=h.state_props(a["state"])
                s=h.select(h.doc(src.read("study",state)),props);t=h.select(h.doc(src.read("release",state)),props)
                expected=h.source_option(a)
                req(len(s)==len(t)==1 and s[0][:2]==(int(a["rule_index"]),int(a["option_index"])) and opt(s[0][2])==opt(t[0][2])==expected,"selected model "+id)
                if "manifest_options" in c:
                    req([tuple(x) for x in c["manifest_options"]]==[expected],"manifest option "+id)
                    for p,entry in c["manifest_source_files"].items():
                        pp=h.strip(p)
                        req(h.blob(src.read("study",pp))==entry["historical_git_blob_sha1"] and h.sha(src.read("release",pp))==entry["release_sha256"],"capture manifest original file "+id)
                s=model(src,"study",leaf);t=model(src,"release",leaf)
                req(s==t and s["provider"]==provider,"effective model mismatch "+id)
                used={state,*s["chain"]}
                for p in used:req(src.compare(p,"json")["raw_equal"],"original JSON byte mismatch "+id+" "+p)
                f=h.inspect_faces(s);req(len(f)==int(a["faces"])==len(faces[k]) and len(s["elements"])==int(a["elements"]),"geometry population "+id)
                req(set(f)=={(x["element_index"],x["direction"]) for x in faces[k]},"face keys "+id)
                if "source_faces" in c:req(c["source_faces"]==len(f),"capture source face count")
                counts=Counter()
                animation_details=[]
                for r in faces[k]:
                    face=f[(r["element_index"],r["direction"])]
                    p=resource(face["resource"],"textures")
                    req(face["resource"]==h.norm(r["resource_id"]) and p==h.strip(r["png_path"]),"face binding "+id+" "+p)
                    req(h.fval(face["uv"])==h.fval(r["uv"].split("|")) and face["uv_method"]==r["uv_method"] and face["rotation"]==int(r["uv_rotation"]) and str(face["cullface"])==r["cullface"] and str(face["tintindex"])==r["tintindex"],"UV/cull/tint "+id)
                    req(h.rawhash(src.read("study",p),r["png_hash_kind"])==r["png_sha"],"historical PNG digest "+id+" "+p)
                    cmp=src.compare(p,"png");used.add(p)
                    req(cmp["raw_equal"] and cmp["equivalent"],"texture source differs "+id)
                    counts[r["status"]]+=1
                    if r["status"]=="ANIMATED_FRAME_RECTS":
                        rr=[q for q in anim if h.appkey(q)==k and q["element_index"]==r["element_index"] and q["direction"]==r["direction"]]
                        req(len(rr)==int(r["png_frames"]) and {int(q["frame"]) for q in rr}==set(range(len(rr))),"animation frame rows")
                        meta=src.read("release",p+".mcmeta",True)
                        req(meta is not None and "animation" in h.doc(meta),"animated source metadata")
                        animation_details.append({"element":r["element_index"],"direction":r["direction"],"texture":p,"png_size":cmp["release_size"],"png_sha256":cmp["release_sha256"],"mcmeta_sha256":h.sha(meta),"animation_metadata":h.doc(meta),"historical_frame_count":len(rr),"uv":face["uv"],"uv_rotation":face["rotation"]})
                req(sum(counts.values())==int(pr["source_faces"]) and counts["ZERO_UV_AREA"]==int(pr["documented_zero_uv_faces"]) and counts["ANIMATED_FRAME_RECTS"]==int(pr["animated_source_faces"]),"historical face status counts "+id)
                result[id]={"cohort":cohort,"block":a["block"],"state":a["state"],"selected_option":list(expected),"provider":provider,"parent_chain":s["chain"],"elements":len(s["elements"]),"faces":len(f),"historical_face_status_counts":dict(counts),"all_selected_JSON_bytes_equal":True,"all_selected_texture_bytes_equal":True,"historical_uv_and_png_hash_faces_verified":len(f),"existing_capture":c,"assets":sorted(used),"animated_source_faces":animation_details,"modeling_status":"PASS_MODELING_SCOPE"}
            assets[cohort]=dict(sorted(src.pairs.items()))
    req(set(result)==IDS,"incomplete results")
    totals=Counter()
    for r in result.values():totals.update(r["historical_face_status_counts"])
    out={"schema":"MCFR_INT4_H22_HC_MACAW12_ORIGINAL_SOURCE_AND_EXISTING_F2_V1","source_ledger_git_blobs":PINS,
         "source_pins":{"HC_git_commit":HC_GIT,"HC_release_sha1":HC_SHA,"MACAW_release_sha1":MAC_SHA,"MACAW_release_sha256":MAC256,"vanilla_sha1":MC_SHA},
         "case_count":len(result),"applications":len(apps),"elements":sum(r["elements"] for r in result.values()),"faces":sum(r["faces"] for r in result.values()),"face_status_counts":dict(totals),
         "cases":result,"asset_comparisons":assets,"asset_counts":{c:{"json":sum(x["kind"]=="json" for x in v.values()),"png":sum(x["kind"]=="png" for x in v.values())} for c,v in assets.items()},
         "new_game_runs":0,"new_F2":0,"legacy_F70_unconditional":0,"INT5":0,"INT6":0,"R06_temporal_causality_approved":False,
         "limits":["HC Git 4.0.3 vs official Fabric 4.0.3 byte equality of selected assets; Macaw study already uses identical official release pin, not independent versions.","Existing exact server and F2 provenance reused; not new scene or GPU evidence.","S38 isolated selected head cushion, not complete natural bed; S43 source animation metadata only, no timing causality.","No original asset bytes distributed."]}
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print("H22_SUMMARY",json.dumps({k:out[k] for k in ("case_count","applications","elements","faces","face_status_counts","asset_counts")},sort_keys=True))
    print("H22_S43_ANIMATION",json.dumps(result["S43"]["animated_source_faces"],sort_keys=True))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for k in ("hc-git","hc-jar","macaw-jar","mc1211","mc12111","output"):p.add_argument("--"+k,required=True)
    audit(p.parse_args())
