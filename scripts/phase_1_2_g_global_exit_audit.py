#!/usr/bin/env python3
"""Minecraft user-extracted 1.21.11 1-2-G independent six-gate full-scope audit.
Read-only on original A-F/v69 and assets. Outputs only 1-2-G/final/*.
Checks actual original bytes of all 4,669 typed assets, separate 99 sidecars,
six Entry evidence sets, fixed/source inventories, C/B/F/E/D and D syntax.
Runtime engine, official JAR, semantic furniture certification EXCLUDED.
"""
import collections
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GROOT="research/vanilla_models/phase_1-2-G/"
FROOT="research/vanilla_models/phase_1-2-F/"
DROOT="research/vanilla_models/phase_1-2-D/"
CROOT="research/vanilla_models/phase_1-2-C/"
AROOT="research/vanilla_models/v34/"
OUT=ROOT/GROOT/"final"
OUT.mkdir(parents=True,exist_ok=True)
errors=[]
checks=[]
def err(kind,**kw):
    errors.append(dict(kind=kind,**kw))
def check(name,ok,**details):
    checks.append(dict(name=name,pass_=bool(ok),**details))
    if not ok:err("GATE_ASSERT",assertion=name,**details)
def data(path):
    return (ROOT/path).read_bytes()
def gitsha(b):
    return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
def load(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def jload(path):
    return json.loads(data(path).decode("utf-8-sig"))
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def by_path(rows,field="source_path"):
    return {x[field]:x for x in rows}
def tally(rows,col):
    return sum(int(x[col]) for x in rows)
def detail(path):
    return dict(path=path,sha=gitsha(data(path)),size=len(data(path)))
def status(boolean):
    return "PASS" if boolean else "BLOCKED"
def parent_bool(x):
    return str(x).strip().lower() in ("yes","true","1")

def main():
    contract=jload("docs/vanilla_models_1-2/1-2-G_ACCEPTANCE_CONTRACT.json")
    prep=jload(GROOT+"G_SCOPE_PREP_AUDIT.json")
    expected_types={"BLOCK_MODEL_JSON":2390,"BLOCKSTATE_JSON":1168,"BLOCK_TEXTURE_PNG":1111}
    expected_entries=[347,775,945,944,829,829]
    expected_parts=[(150,12,185),(494,96,185),(495,265,185),(494,265,185),(379,265,185),(378,265,186)]
    invPaths=[AROOT+"01_inventory_2390_block_model_paths_git_shas.csv",AROOT+"02_inventory_1168_blockstate_paths_git_shas.csv",AROOT+"03_inventory_1111_block_texture_png_paths_git_shas.csv"]
    invs=[load(p) for p in invPaths]
    # Source inventory is the immutable authority for original typed (path,SHA).
    a={}
    for typ,rows in zip(expected_types.keys(),invs):
        for row in rows:
            k=(typ,row["source_path"])
            if k in a:err("A_DUPLICATE",key=k)
            a[k]=row["git_blob_sha"]
    check("A_SOURCE_INVENTORIES_2390_1168_1111",list(map(len,invs))==[2390,1168,1111],counts=list(map(len,invs)))
    check("A_SOURCE_UNIQUE_PATH_SHA_4669",len(a)==4669,actual=len(a))
    pinned=prep.get("baseline_inventory",{})
    for item,path in zip(["origM","origS","origP"],invPaths):
        check("A_PINNED_SHA_"+item,gitsha(data(path))==pinned.get(item),actual=gitsha(data(path)),expected=pinned.get(item))
    queues=[]
    for i,n in enumerate(expected_entries,1):
        p=GROOT+f"entry{i}/G_ENTRY{i}_QUEUE_{n}.csv"
        rows=load(p);queues.append(rows)
        ctr=collections.Counter(x["asset_type"] for x in rows)
        expect=dict(zip(expected_types.keys(),expected_parts[i-1]))
        check(f"ENTRY{i}_QUEUE_AND_TYPE_COUNTS",len(rows)==n and dict(ctr)==expect,
              rows=len(rows),types=dict(ctr),expected=expect)
        idx=[int(x["G_global_index"]) for x in rows]
        start=1+sum(expected_entries[:i-1])
        check(f"ENTRY{i}_GLOBAL_INDEX_CONTINUITY",idx==list(range(start,start+n)),start=start,end=start+n-1)
    q=[x for group in queues for x in group]
    keys=[(x["asset_type"],x["source_path"]) for x in q]
    check("G_QUEUE_ALL_SIX_UNIQUE_4669",len(keys)==len(set(keys))==4669,actual=len(set(keys)))
    check("G_FIXED_4669_EQUAL_A_PATH_SHA",len(q)==4669 and all(a.get((x["asset_type"],x["source_path"]))==x["git_blob_sha"] for x in q),
          count=len(q),missing_or_sha_error=sum(a.get((x["asset_type"],x["source_path"]))!=x["git_blob_sha"] for x in q))
    fixed=load(GROOT+"G_FIXED_SCOPE_4669.csv")
    fcols=set(fixed[0]) if fixed else set()
    check("G_FIXED_CSV_4669_ROWS",len(fixed)==4669,actual=len(fixed),columns=sorted(fcols))
    if {"asset_type","source_path","git_blob_sha"}.issubset(fcols):
        check("G_FIXED_CSV_TYPED_PATH_SHA_EQUAL_A",set((x["asset_type"],x["source_path"],x["git_blob_sha"]) for x in fixed)==
           set((x["asset_type"],x["source_path"],x["git_blob_sha"]) for x in q))
    else:
        err("G_FIXED_SCHEMA_UNEXPECTED",columns=sorted(fcols))
    # Independent direct source bytes pass, separate from G per-Entry original readers.
    originals=[]
    sidecars=[]
    for x in q:
        typ,path,expected=x["asset_type"],x["source_path"],x["git_blob_sha"]
        try:
            b=data(path)
            actual=gitsha(b)
            if actual!=expected:err("G1_ORIGINAL_SHA_MISMATCH",path=path,expected=expected,actual=actual)
            originals.append(dict(type=typ,path=path,sha=actual,source_sha_match=actual==expected,bytes=len(b)))
            if typ=="BLOCK_TEXTURE_PNG":
                meta=ROOT/(path+".mcmeta")
                if meta.is_file():
                    mb=meta.read_bytes()
                    try: m=json.loads(mb.decode("utf-8"))
                    except Exception as e:err("MCMETA_JSON_PARSE",path=str(meta),message=str(e));m={}
                    sidecars.append(dict(png_path=path,mcmeta_path=path+".mcmeta",git_sha=gitsha(mb),bytes=len(mb),animated="animation" in m))
        except Exception as e:err("G1_ORIGINAL_SOURCE_MISSING",path=path,message=str(e))
    check("G1_4669_RAW_BYTES_DIRECT_GIT_SHA",len(originals)==4669 and not any(not x["source_sha_match"] for x in originals),
          checked=len(originals),source_sha_mismatches=sum(not x["source_sha_match"] for x in originals))
    check("G1_MCMETA_SIDECARS_99",len(sidecars)==99,actual=len(sidecars))
    c_png=load(CROOT+"entry5/C_PNG_UNIQUE_ALL.csv")
    c_pngidx=by_path(c_png,"png_path")
    sideidx=by_path(sidecars,"png_path")
    c_meta=[x for x in c_png if x.get("mcmeta_sha")]
    check("G1_C_MCMETA_97_IN_G99",len(c_meta)==97 and all(sideidx.get(x["png_path"],{}).get("git_sha")==x["mcmeta_sha"] for x in c_meta),C_with_sidecar=len(c_meta))
    # Crosswalk each G Entry to freshly recomputed original bytes from same queue.
    originalidx={ (x["type"],x["path"]):x for x in originals }
    accepted=[]
    per_entry=[]
    for i,n in enumerate(expected_entries,1):
        base=GROOT+f"entry{i}/"
        if i==1:
            ledger=load(base+"G_SOURCE_CROSSWALK.csv")
            byk={(x["asset_type"],x["source_path"]):x for x in ledger}
            fine=all(x["source_git_sha"]==originalidx.get((x["asset_type"],x["source_path"]),{}).get("sha") and
                     x["tree_sha_match"]=="YES" and
                     (x["direct_PNG_binary_read"]=="YES" if x["asset_type"]=="BLOCK_TEXTURE_PNG" else x["direct_JSON_read"]=="YES") for x in ledger)
            audit=jload(base+"G_INDEPENDENT_AUDIT.json")
            count=audit["counts"]
            accepted.append(audit.get("G_entry1_complete") is True and len(audit["source_provenance_errors"])==0)
            canonical=dict(elements=count["geometry_applied_elements"],faces=count["source_face_refs"],uv=count["C_explicit_UV_rederived"],
               bound=count["C_png_linked_face_rows"],unbound=count["C_unbound_face_rows"],E=count["E_exception_models"],D=count["D_original_model_options"],
               Cpng=count["C_RGBA_direct_G_pixel_sha_matches"],Gnew=count["C_not_prior_C_PNG_G_direct_verified"],mcmeta=count["PNG_mcmeta_sha_json_verified"])
        elif i==2:
            ledger=load(base+"G_SOURCE_CROSSWALK.csv")
            byk={(x["asset_type"],x["source_path"]):x for x in ledger}
            fine=all(x["source_git_sha_expected"]==originalidx.get((x["asset_type"],x["source_path"]),{}).get("sha")
                and x["source_git_sha_direct_computed"]==x["source_git_sha_expected"]
                and x["G_source_sha_match"]=="YES" and x["G_source_content_reopened"]=="YES" for x in ledger)
            audit=jload(base+"G_ENTRY2_INDEPENDENT_AUDIT.json")
            v=audit["population_counts"]
            accepted.append(audit.get("G_entry2_accepted") is True and not audit["independent_errors"])
            canonical=dict(elements=v["model_elements"],faces=v["model_faces"],uv=v["explicit_uv"],bound=v["bound_faces"],
                unbound=v["unbound_faces"],E=v["models_E"],D=v["D_source_options"],Cpng=v["PNG_C_RGBA_independent_matches"],Gnew=v["PNG_outside_C"],mcmeta=audit["mcmeta_count"])
        else:
            ledger=load(base+f"G_ENTRY{i}_SOURCE_IDENTITY_{n}.csv")
            byk={(x["type"],x["path"]):x for x in ledger}
            fine=all(x["expected_sha"]==originalidx.get((x["type"],x["path"]),{}).get("sha") and
                     x["actual_sha"]==x["expected_sha"] and x["source_SHA_match"]=="PASS" and x["direct_bytes_read"]=="YES" for x in ledger)
            audit=jload(base+f"G_ENTRY{i}_INDEPENDENT_RECOUNT.json")
            v=audit["counts"]
            accepted.append(audit.get("acceptance")==f"ENTRY{i}_PASS" and not audit["errors"])
            canonical=dict(elements=v["elements"],faces=v["faces"],uv=v["face_explicit_UV"],bound=v["face_PNG_bound"],
                unbound=v["face_template_unbound"],E=v["models_E"],D=v["D_options"],
                Cpng=v["PNG_C_prior_and_RGBA_matched"],Gnew=v["PNG_C_outside_new_G_only"],mcmeta=v["mcmeta_json_direct_read"])
        kqueue={(x["asset_type"],x["source_path"]) for x in queues[i-1]}
        membership=len(ledger)==n and set(byk)==kqueue
        check(f"G_ENTRY{i}_REMOTE_LEDGER_REOPENED_AND_RAW_SOURCE_MATCH",membership and fine and accepted[-1],
              rows=len(ledger),membership=membership,source_rehash_matches=fine,accepted=accepted[-1])
        per_entry.append(dict(entry=i,count=n,approval=accepted[-1],**canonical))
    # Prior B/C/D/E/F immutable scope: source path SHA membership, geometry/exception, counts.
    A_model={k:v for (typ,k),v in a.items() if typ=="BLOCK_MODEL_JSON"}
    A_state={k:v for (typ,k),v in a.items() if typ=="BLOCKSTATE_JSON"}
    A_png={k:v for (typ,k),v in a.items() if typ=="BLOCK_TEXTURE_PNG"}
    bscope=load("research/vanilla_models/phase_1-2-B/entry6/B_SCOPE_2390_STATUS.csv")
    cscope=load(CROOT+"entry5/C_SCOPE_2390_FINAL_STATUS.csv")
    fscope=load(FROOT+"F_FIXED_SCOPE_2390.csv")
    escope=load("research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_86.csv")
    dscope=load(DROOT+"D_FIXED_SCOPE_1168.csv")
    for key,rows,pathkey,shakey,universe in [
       ("B",bscope,"full_source_path","git_blob_sha",A_model),
       ("C",cscope,"source_path","git_blob_sha",A_model),
       ("F",fscope,"source_path","git_blob_sha",A_model),
       ("E",escope,"model_path","model_git_sha",A_model),
       ("D",dscope,"source_path","git_blob_sha",A_state)]:
       check("PRIOR_"+key+"_SCOPE_PATH_SHA",len(rows)==(86 if key=="E" else 1168 if key=="D" else 2390)
            and len(set(x[pathkey] for x in rows))==len(rows)
            and all(universe.get(x[pathkey])==x[shakey] for x in rows),rows=len(rows))
    # Independently count the C face/UV/binding and G per-Entry recomputation.
    cfaces=tally(cscope,"C_applied_faces")
    cuv=tally(cscope,"C_explicit_uv_faces")
    cimplicit=tally(cscope,"C_implicit_uv_key_absent_faces")
    cbound=tally(cscope,"C_bound_png_face_refs")
    cunbound=tally(cscope,"C_template_unbound_face_refs")
    general=sum(x["C_assignment"]!="E_EXCEPTION" for x in cscope)
    check("G2_C_GENERAL_2304_E86",general==2304 and len(escope)==86,prior_C_general=general,prior_E=len(escope))
    check("G2_G_DIRECT_ELEMENTS_5689",sum(x["elements"] for x in per_entry)==5689,actual=sum(x["elements"] for x in per_entry))
    check("G2_G_FACE_23090_C_FACE_23090",sum(x["faces"] for x in per_entry)==cfaces==23090,G_face=sum(x["faces"] for x in per_entry),C_face=cfaces)
    check("G2_C_UV_EXPLICIT_18808_IMPLICIT_4282",cuv==18808 and cimplicit==4282 and sum(x["uv"] for x in per_entry)==cuv,
          C_explicit=cuv,C_implicit=cimplicit,G_explicit=sum(x["uv"] for x in per_entry))
    check("G2_C_PNGBOUND_21590_TEMPLATE_1500",cbound==21590 and cunbound==1500 and
          sum(x["bound"] for x in per_entry)==cbound and sum(x["unbound"] for x in per_entry)==cunbound,
          C_bound=cbound,C_unbound=cunbound)
    heavy=load(CROOT+"entry5/HEAVY_CORE_FACE_ERRATUM.csv")
    check("G2_HEAVY_CORE_CORRECTED_FACE_6",len(heavy)==6 and len(set((x["element_index"],x["direction"]) for x in heavy))==6)
    check("G2_E_EXCEPTION_BY_ENTRIES_86",sum(x["E"] for x in per_entry)==86,by_entry=[x["E"] for x in per_entry])
    # D static syntax and option counts, independently recomputed from D per-block summaries.
    dsrc=jload(DROOT+"entry6/D_FINAL_CLOSURE.json")
    dsummary_paths=[
     DROOT+"entry2/D_BLOCK_SUMMARY.csv",
     DROOT+"entry3/D_ENTRY3_SUBBATCH1_48_SUMMARY.csv",
     DROOT+"entry3/D_ENTRY3_REMAINING_217_SUMMARY.csv",
     DROOT+"entry4/D_ENTRY4_265_SUMMARY.csv",
     DROOT+"entry5/D_ENTRY5_265_SUMMARY.csv",
     DROOT+"entry6/D_ENTRY6_265_SUMMARY.csv"]
    drs=[load(p) for p in dsummary_paths]
    dsyn=380+sum(int(x["syntactic_state_cases"]) for x in drs[0]) +sum(int(x["syntactic_candidates"]) for group in drs[1:] for x in group)
    dapps=1972+sum(int(x["model_application_options"]) for x in drs[0]) +sum(int(x["model_option_applications"]) for group in drs[1:] for x in group)
    check("G3_D1168_AND_G_RULES7592",len(dscope)==1168 and sum(x["D"] for x in per_entry)==7592)
    check("G3_D_SYNTAX_9193_APPLICATIONS_19440",dsyn==9193 and dapps==19440 and dsrc["syntactic_state_rows"]==dsyn and dsrc["state_option_instances"]==dapps,
         syntax=dsyn,applications=dapps)
    d_direct=sum(parent_bool(x["D_direct_model_selected"]) for x in fscope)
    e_d_ref=sum(int(x["D_rule_option_refs"])>0 for x in escope)
    check("G3_D_DIRECT2136_NON254_E84_NON2",d_direct==2136 and 2390-d_direct==254 and e_d_ref==84 and len(escope)-e_d_ref==2,
         D_direct=d_direct,D_not_direct=2390-d_direct,E_D_selected=e_d_ref)
    # PNG/C/F evidence: 1111 rehashed PNG, C1073 C prior, outside 38 G new.
    check("G4_C_PNG_1073_NEW38",len(c_png)==1073 and set(c_pngidx)==set(A_png).intersection(c_pngidx)
          and sum(x["Cpng"] for x in per_entry)==1073 and sum(x["Gnew"] for x in per_entry)==38,
          C=len(c_png),prior_link=sum(x["Cpng"] for x in per_entry),new_G=sum(x["Gnew"] for x in per_entry))
    check("G4_SIDECAR99_C97",len(sidecars)==99 and len(c_meta)==97)
    f3=jload(FROOT+"entry6/F3_SOURCE_VISUAL_SUMMARY.json")
    first=load(FROOT+"entry6/F3_PNG_FIRST_FRAME_332.csv")
    firstOK=len(first)==332 and all(A_png.get(x["original_PNG_path"])==x["original_PNG_git_sha"] and
            c_pngidx.get(x["original_PNG_path"],{}).get("rgba_sha256")==x["original_RGBA_SHA256"] for x in first)
    contacts={x["contact_sheet_path"]:x["contact_sheet_git_sha"] for x in first}
    contact_matches=all(gitsha(data(p))==sha for p,sha in contacts.items())
    check("G4_F_FIRSTFRAME332_CONTACT8",firstOK and len(contacts)==8 and contact_matches,
          F3_PNG=len(first),contacts=len(contacts),source_path_SHA_RGBA=firstOK,contact_SHA_match=contact_matches)
    fc=f3["count"]
    check("G4_F_MODELS340_UNBOUND38_ANIM16",fc["models_with_observed_bound_png"]==340 and
          fc["models_without_bound_png_explicit_source_hold"]==38 and fc["animated_tall_png"]==16,
          linked_models=fc["models_with_observed_bound_png"],unbound_models=fc["models_without_bound_png_explicit_source_hold"],animated_frame_only=fc["animated_tall_png"])
    # G5 different denominators, all explicit unresolved and baseline source hashes unchanged.
    check("G5_INCOMPATIBLE_DENOMINATORS_DISTINCT",len(escope)==86 and cunbound==1500 and 2390-d_direct==254 and
          (1111-len(c_png))==38 and fc["models_without_bound_png_explicit_source_hold"]==38)
    protected=[FROOT+"F_FIXED_SCOPE_2390.csv",DROOT+"D_FIXED_SCOPE_1168.csv",
        "research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_86.csv",CROOT+"entry5/C_PNG_UNIQUE_ALL.csv"]
    pinneditems=dict(F="F",D="D",E="E",Cpng="Cpng")
    paths=dict(F=protected[0],D=protected[1],E=protected[2],Cpng=protected[3])
    for name,p in paths.items():
        check("G5_PROTECTED_PIN_SHA_"+name,gitsha(data(p))==pinned.get(name),actual=gitsha(data(p)),expected=pinned.get(name))
    # F previously approved separate source scope and v69 state and archive.
    fa=jload(FROOT+"entry6/F_FINAL_GATE_AUDIT.json")
    state=jload("handoff/STATE.json")
    check("G5_F_V69_BASELINE_PRIOR150_TOP1",fa["full_model_scope"]==2390 and
        fa["exit_gates"]["F1"]["status"]=="PASS" and contract["other_denominators_not_additive"]["prior_approval"]==150 and
        contract["other_denominators_not_additive"]["v69_P1_rows"]==544 and
        contract["other_denominators_not_additive"]["v69_review_rows"]==544 and
        contract["other_denominators_not_additive"]["prior_top_level_completed"]==1)
    gaps=jload(GROOT+"entry6/G_ENTRY6_PROVENANCE_GAPS.json")
    check("G5_F_PARENT_MISSING_SHA_2_MODELS_4_FIELDS_G_EXPLICIT_RECHECK",gaps["count"]==4 and
        len(set(x["model"] for x in gaps["records"]))==2 and
        all(x["G_recomputed_original_git_blob_sha"]=="38f44bda128d10a5e09614e5ac155c956237681e"
            and x["prior_F_sha"]=="" for x in gaps["records"]),records=gaps["count"])
    # G6 final adjudication requires G1..5 all PASS; G6 remote content SHA after upload is a separate postcommit readback.
    result={gate:{"checks":[x for x in checks if x["name"].startswith(gate)],"status":status(all(x["pass_"] for x in checks if x["name"].startswith(gate)))}
        for gate in ("G1","G2","G3","G4","G5")}
    # G1 includes membership and A provenance by definition; intermediate checks all globally enforced.
    globalOK=(not errors) and all(accepted) and len(originals)==4669
    result["G6"]={"checks":[dict(name="ALL_SUBGATES_AND_SOURCE_RECOUNT",pass_=globalOK),dict(name="POST_COMMIT_REMOTE_SHA_READBACK",pass_=False,reason="PENDING_FINAL_POST_COMMIT_REMOTE_READBACK")],
       "status":"PENDING_REMOTE_FINAL_READBACK" if globalOK else "BLOCKED"}
    counts=dict(raw_assets=len(originals),by_type=dict(collections.Counter(x["type"] for x in originals)),
       model_elements=sum(x["elements"] for x in per_entry),faces=sum(x["faces"] for x in per_entry),
       C_uv_explicit=cuv,C_uv_implicit=cimplicit,C_faces_PNG_bound=cbound,C_face_template_unbound=cunbound,
       D_rules=sum(x["D"] for x in per_entry),D_syntactic_state_cases=dsyn,D_model_option_applications=dapps,
       E_special=sum(x["E"] for x in per_entry),PNG_C_prior_matches=sum(x["Cpng"] for x in per_entry),
       PNG_outside_C=sum(x["Gnew"] for x in per_entry),mcmeta_sidecars=len(sidecars),F3_PNG=len(first),
       G_entries_accepted=sum(accepted),F_prior_parent_sha_gaps=gaps["count"],source_errors=len(errors))
    output=dict(schema="G_GLOBAL_4669_INDEPENDENT_CLOSEOUT/v1",scope="USER_EXTRACTED_MINECRAFT_JAVA_1_21_11",
        contract_sha=gitsha(data("docs/vanilla_models_1-2/1-2-G_ACCEPTANCE_CONTRACT.json")),
        counts=counts,per_entry=per_entry,gate_results=result,all_subgate_checks=checks,
        source_stage_errors=errors,source_scope_pass=globalOK,exit_status="G1_G5_SOURCE_PASS_G6_REMOTE_PENDING" if globalOK else "G_BLOCKED_AT_ENTRY6",
        G6_remote_gate_pending=True,global_final_G_complete=False,whole_stage_1_2_complete=False,
        outside_scope=["Official JAR authenticity","game runtime state and E renderer","full animation playback","PZ furniture identity","Minecraft map/world generation"])
    dump("G_GLOBAL_INDEPENDENT_RECOUNT.json",output)
    # Inventory evidence records one line for each original file, to enable remote row-level readback.
    with (OUT/"G_FINAL_SOURCE_SHA_4669.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["type","path","sha","source_sha_match","bytes"]);w.writeheader();w.writerows(originals)
    with (OUT/"G_FINAL_MCMETA_99.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["png_path","mcmeta_path","git_sha","bytes","animated"]);w.writeheader();w.writerows(sidecars)
    (OUT/"G_GLOBAL_GATE_REPORT.md").write_text("\n".join([
       "# Minecraft Java 1.21.11 — 1-2-G 6개 Entry 독립 종료 감사",
       "","**사용자가 추출한 원본** 4,669개 파일 재개방·SHA 및 선행 B~F 원장 교차. 공식 JAR·게임 runtime 인증은 범위 밖.",
       "**원본 통합 감사: "+("G1~G5 정적 전제 PASS, G6 GitHub 원격 readback 별도 진행" if globalOK else "BLOCKED")+"**",
       "","## 총괄",*[f"- {key}: {val}" for key,val in counts.items()],
       "","## 종료 게이트","",*[f"- {g}: {x['status']}" for g,x in result.items()],
       "","## 원본 누락·예외 설명",
       "- F6의 sculk_mirrored·stone_mirrored 2모델의 F 선행 cube_mirrored 부모 SHA·provider SHA 4필드가 비어 있었음; G 원본 직접 재검증으로 보완하되 F 원본을 변경하거나 F 과거 소스로 소급 인정하지 않음.",
       "- E86의 실제 renderer는 범위 밖 미인증. 템플릿 face 미바인딩1500, 모델 PNG 불명38, C 바깥 PNG38, D 미직접254는 서로 다른 분모.",
       "- F3 332개는 첫 프레임 화면 확인, 애니메이션 전체 재생 아님.",
       "- 1-2 전체 종료는 G 종료와 별도 단계에서 심사. A~F/v69 원본 수정 금지.",
       "","## 오류 목록", *[f"- {e}" for e in errors[:120]],""
    ]),encoding="utf-8")
    print(json.dumps(dict(status=output["exit_status"],counts=counts,checks=len(checks),errors=errors[:15]),ensure_ascii=False))
    return 0 if globalOK else 2
if __name__=="__main__":
    sys.exit(main())
