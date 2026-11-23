#!/usr/bin/env python3
"""INT-4-H11: pinned AF acacia chair face UV vs actually different texture texels.

Face UV rectangle / texel-square intersection is a *source-only potential*
footprint. It is NEVER proof of rendered per-face UV, culling, sampling,
author intent, semantics, or asset rights.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from collections import Counter
from io import BytesIO
from pathlib import Path
from PIL import Image
from mcfr import int4_af_variant3_texture_audit as src
from mcfr import af_release_version_audit as af

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
OLD=OUT/"INT4_AF_VARIANT3_PIXEL_AUDIT_RESULT.json"
H7=OUT/"INT4_H7_SIX_RISK_SOURCE_STAGE_AUDIT_V1.json"
PINS={
 str(OLD):"7530144389e1589af4c1c891ded3e9531886519d",
 str(H7):"fc0c28d005b45bf83e800535bfaac8ef1f3a9ea5",
}
FACES=OUT/"INT4_H11_AF_VARIANT3_12_FACE_UV_TEXEL_COVERAGE_V1.csv"
SELECTORS=OUT/"INT4_H11_AF_VARIANT3_4_DIRECTION_MODEL_SELECTORS_V1.csv"
AUDIT=OUT/"INT4_H11_AF_VARIANT3_SOURCE_UV_TEXEL_AUDIT_V1.json"
REPORT=OUT/"INT4_H11_AF_VARIANT3_MODEL_TEXTURE_UV_RESEARCH_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def require(cond,message):
    if not cond:raise AssertionError(message)
def csv_bytes(rows):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return f.getvalue().encode("utf-8")
def as_json(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def write(path,data,verify):
    p=ROOT/path
    if verify:require(p.is_file() and p.read_bytes()==data,"NOT_DETERMINISTIC "+str(path))
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)

def old_evidence():
    d={}
    for name,pin in PINS.items():
        binary=(ROOT/name).read_bytes()
        require(blob(binary)==pin,"OLD_GIT_SHA_CHANGED "+name)
        d[name]=json.loads(binary)
    orig=d[str(OLD)]["evidence"];risk=d[str(H7)]["risk_cases"]
    require(orig["status"]=="COMPLETE_SOURCE_TEXTURE_DIFFERENCE_NOT_GAME_PIXEL_OR_INT5_APPROVAL" and
            orig["source_selector_discontinuities"]==1 and
            orig["discontinuous_direction"]=="south" and
            orig["model_face_comparison"]["changed_texture_binding_faces"]==12 and
            orig["model_face_comparison"]["geometry_equal"] is True and
            orig["model_face_comparison"]["uv_equal"] is True and
            orig["texture_png_study"]["rgba_different_pixel_count"]==54 and
            orig["texture_png_runtime"]["rgba_different_pixel_count"]==54,
            "HISTORIC_SOURCE_PNG_FACE_EVIDENCE_CHANGED")
    require(all(z["rgba_different_pixel_count"]==0 for z in
                orig["textures_study_vs_runtime"].values()),
            "SOURCE_RUNTIME_TEXTURE_PIXELS_NOT_EQUAL")
    require(risk["R07"]["archived_server_substage_verified"]==4 and
            risk["R07"]["actual_original_game_run_count"]==1 and
            risk["R07"]["full_risk_contract_approved"] is False,
            "H7_SOURCE_F2_CASE_IDENTITIES_CHANGED")
    return orig,risk

def footprint(uv,size):
    """Integer texel squares with positive-area overlap; UV may be reversed."""
    require(isinstance(uv,list) and len(uv)==4 and
            all(isinstance(n,(float,int)) and math.isfinite(n) for n in uv),
            "NON_NUMERIC_SOURCE_UV")
    u0,v0,u1,v1=uv
    lo_u,hi_u=sorted((u0,u1));lo_v,hi_v=sorted((v0,v1))
    w,h=size
    require(0<=lo_u<hi_u<=w and 0<=lo_v<hi_v<=h,
            "SOURCE_UV_OUTSIDE_OR_ZERO_AREA")
    return {(x,y) for x in range(max(0,math.floor(lo_u)),min(w,math.ceil(hi_u)))
            for y in range(max(0,math.floor(lo_v)),min(h,math.ceil(hi_v)))
            if max(x,lo_u)<min(x+1,hi_u) and max(y,lo_v)<min(y+1,hi_v)}

def difference(b0,b1):
    with Image.open(BytesIO(b0)) as a,Image.open(BytesIO(b1)) as b:
        a.load();b.load()
        require(a.size==b.size==(16,16),"SOURCE_TEXTURE_SIZE_CHANGED")
        p0=list(a.convert("RGBA").getdata())
        p1=list(b.convert("RGBA").getdata())
        texels={(i%16,i//16) for i,(x,y) in enumerate(zip(p0,p1)) if x!=y}
    require(len(texels)==54,"ORIGINAL_54_RGBA_TEXELS_NOT_VERIFIED")
    return (16,16),texels

def build(verify=False):
    prior,risk=old_evidence()
    files={}
    # Reopen exactly the upstream Git commit, verifying every original Git blob.
    for rel,pin in src.EXPECTED_SHA.items():
        data=(src.fetch_pinned_png(rel) if rel in src.TEXTURES else af.fetch_research(rel))
        require(isinstance(data,bytes) and af.digest_bytes(data,"GIT_BLOB_SHA1")==pin,
                "REOPENED_SOURCE_GIT_BLOB_MISMATCH "+rel)
        files[rel]=data
    block=json.loads(files["blockstates/acacia_chair.json"])
    rows=src.state_rows(block,block)
    require(len(rows)==4,"FOUR_CARDINAL_SELECTORS_REQUIRED")
    models={name:json.loads(files[name]) for name in (*src.CHILDREN,src.PARENT)}
    changed,stats=src.compare_inherited_models(models)
    require(stats["element_count_each"]==10 and stats["face_count_each"]==46 and
            stats["changed_texture_binding_faces"]==12 and
            stats["unchanged_texture_binding_faces"]==34 and
            stats["geometry_equal"] and stats["uv_equal"],
            "ORIGINAL_FACE_MODEL_STRUCTURE_CHANGED")
    e1=af.effective(src.CHILDREN[0],models)
    e3=af.effective(src.CHILDREN[1],models)
    size,diff=difference(*[files[k] for k in src.TEXTURES])
    require(src.image_difference(*[files[k] for k in src.TEXTURES])[
            "rgba_different_pixel_count"]==54,
            "ORIGINAL_PNG_PIXEL_DIFF_RECOMPUTATION_CHANGED")
    uv_rows=[]
    union=set();touched_faces=0;by_element=Counter()
    for changed_face in sorted(changed,key=lambda v:(v["element_index"],v["face"])):
        i,face=changed_face["element_index"],changed_face["face"]
        uv=e1["uv"][i][face]
        require(uv==e3["uv"][i][face] and "uv" in uv,"FACE_UV_DIFFERENT")
        support=footprint(uv["uv"],size)
        overlap=support&diff
        union.update(support)
        by_element[i]+=1
        touched_faces+=bool(overlap)
        uv_rows.append({
            "source_element_index":i,"face":face,
            "inherited_source_face_uv":json.dumps(uv["uv"],separators=(",",":")),
            "face_uv_rotation":uv.get("rotation",0),
            "texture_acacia_1":changed_face["acacia_1_texture_resource"],
            "texture_acacia_3":changed_face["acacia_3_texture_resource"],
            "potential_texel_squares_intersected":len(support),
            "source_changed_texels_in_uv":len(overlap),
            "source_texel_overlap_ratio":str(len(overlap))+"/"+str(len(support)),
            "same_model_geometry":True,"same_face_UV":True,
            "original_game_F2_face_visibility":"NOT_TESTED",
            "actual_GPU_face_to_texel_sampling_approved":False,
        })
    require(len(uv_rows)==12 and dict(by_element)=={7:2,8:5,9:5},
            "SOURCE_BACK_FACE_COUNT_CHANGED")
    selectors=[]
    for row in rows:
        side=row["direction"]
        require(row["different_model_from_variant3_majority"]==(side=="south"),
                "SOUTH_SELECTION_EXPLAINABILITY_CHANGED")
        selectors.append({
            "facing":side,"tucked":False,"variant":3,
            "original_selector":row["selector"],"actual_source_model":row["model"],
            "y_rotation":row["y"],
            "back_texture_name":"back_1" if side=="south" else "back_3",
            "source_elements":10,"source_faces":46,
            "same_geometry_and_uv_other_model":True,
            "original_real_F2_source_state_available":True,
            "new_F2_in_this_study":False,
            "author_intent_or_bug_correction_approved":False,
        })
    in_union=diff&union
    result={
       "schema":"MCFR_INT4_H11_AF_VARIANT3_SOURCE_FACE_UV_TEXEL_OVERLAP/v1",
       "status":"PASS_12_CHANGED_SOURCE_FACES_UV_TEXEL_COVERAGE_WITHOUT_GPU_CAUSAL_APPROVAL",
       "source":{"repo":"crispytwig/AnotherFurniture","commit":af.UPSTREAM,
                 "study_version":"4.0.3","actual_game_release":"4.0.2",
                 "fixed_git_blob_sha1":src.EXPECTED_SHA,
                 "previous_source_audit_gitblob_sha1":PINS[str(OLD)],
                 "H7_real_game_original_provenance_gitblob_sha1":PINS[str(H7)]},
       "counts":{
         "source_blockstate_selectors":len(block["variants"]),
         "variant3_direction_selectors":len(selectors),
         "south_only_acacia_1_discontinuities":1,
         "equal_inherited_elements_each":10,
         "equal_inherited_faces_each":46,
         "face_texture_bindings_changed":12,
         "face_texture_bindings_same":34,
         "different_original_back_texture_RGBA_texels":len(diff),
         "changed_texels_in_union_of_12_face_UV_footprints":len(in_union),
         "different_texels_outside_changed_face_UV_footprints":len(diff-in_union),
         "changed_binding_faces_with_any_different_texel":touched_faces,
         "original_R07_game_F2_case_refs_reused":4,
         "distinct_original_R07_game_executions":1,
         "new_real_Minecraft_executions":0,
         "F70_conditionally_evidenced":70,"F70_unconditional_approvals":0,
         "H03_full_exit":0,"H05_full_exit":0,
         "INT5_parts_semantics_approved":0,"INT6_training_rights_approved":0,
       },
       "prior_parity":{
         "research_vs_runtime_blockstate_semantic_equal":
            prior["study_runtime_blockstate_json_semantically_equal"],
         "research_vs_runtime_model_semantic_equal":
            prior["study_runtime_models_json_semantically_equal"],
         "each_back_png_identical_between_study_and_runtime":all(
             k["equal_rgba_pixels"] for k in prior["textures_study_vs_runtime"].values())},
       "limits":[
         "UV footprint means source UV rectangle intersects a 16x16 source texel square by positive area. It does not guarantee sampling by Minecraft.",
         "Actual face visibility, UV face rotation, culling, lighting, GPU model baking and exact screenshot face-pixel attribution are not proven.",
         "One south variant3 source model selects acacia_1 in BOTH researched and runtime resource tables; whether unintended is unknown.",
         "The existing R07 four native F2 reference stages are reused only as archived evidence from ONE actual game run.",
         "4.0.3 versus 4.0.2 raw byte source mismatch is not blanket release-wide semantic equivalence.",
         "Original asset files are not committed; no F70/H gate full approval, INT5 semantics or INT6 image training redistribution right changes."
       ],
    }
    outputs={FACES:csv_bytes(uv_rows),SELECTORS:csv_bytes(selectors)}
    result["output_sha256"]={str(p):sha(b) for p,b in outputs.items()}
    outputs[AUDIT]=as_json(result)
    report=(
       "# INT-4-H11 Another Furniture 방향별 의자 모델과 텍스처 UV 겹침 연구\n\n"
       "- 원본 Git commit: "+af.UPSTREAM+"; 원본 총 블록상태 "+str(len(block["variants"]))+"개.\n"
       "- variant=3, tucked=false: 북/동/서 acacia_3, 남 acacia_1. 원본과 기존 런타임 관찰에서 해당 선택은 일치.\n"
       "- 두 리프는 동일한 10 요소, 46 면, 동일 면 UV. 변경은 등받이 back_1/back_3 텍스처 참조 12면, 불변 34면.\n"
       "- back_1/back_3 원본 16x16 RGBA 비교: 54개 다른 텍셀.\n"
       "- 12개 변경 면의 UV 양의 면적 겹침 범위에 포함되는 다른 원본 텍셀: "+str(len(in_union))+"/54.\n"
       "- 다른 텍셀과 겹치는 변경 면: "+str(touched_faces)+"/12.\n"
       "- 모든 숫자는 원본 텍스처 UV 직사각형과 텍셀 사각형의 잠재적 교집합이다. 실제 GPU 샘플링, 가시성, 면별 F2 인과는 미검증.\n"
       "- H7 R07 기존 실제 F2 4개는 한 번의 게임 실행에서 온 자료이며 신규 실게임 횟수 0.\n"
       "- 원본 4.0.3과 배포 4.0.2 모델/블록상태 의미와 PNG는 기존 감사에서 일치 확인. 전체 버전 동일성이나 제작자 의도는 승인하지 않음.\n"
       "- 게임 기능 시험 제외. 기존 F70/H03/H05/INT5/INT6 승인 경계 유지.\n"
    ).encode("utf-8")
    outputs[REPORT]=report
    for p,b in outputs.items():write(p,b,verify)
    print(json.dumps({"status":result["status"],"counts":result["counts"]},ensure_ascii=False))
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    build(args.verify)

if __name__=="__main__":main()
