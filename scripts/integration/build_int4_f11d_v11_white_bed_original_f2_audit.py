#!/usr/bin/env python3
"""F11D independent source/real F2 auditor: ONLY historical V11 white bed.

Do not confuse zero ordinary JSON model faces with missing bed geometry.
A client F2 pixel difference corroborates a non-ordinary rendering path
without proving BedRenderer method execution or approving asset reuse.
"""
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
import urllib.error,urllib.request
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PREV=OUT/"INT4_F11C_70_TARGET_EVIDENCE_DISPOSITIONS_V12.csv"
NEW=OUT/"INT4_F11D_V11_WHITE_BED_REAL_F2_SOURCE_V1.json"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={str(PREV):"a620081ec70cca537b2ea281c548fbaff2151bf7",
      str(NEW):"ad3a66fed30a9c961431325db2bb65befa31d25c",
      str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179"}
RUN=45103243455
ARTIFACT=14786302262
ZIP_NAME="INT4_F11D_V11_WHITE_BED_ORIGINAL_F2.zip"
ZIP_SHA="38c626d1076aebeb4e61c5d237d0318ef05bfcfd741f3f81cd11bfe4acc9ebc8"
CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
STUDY_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
MODEL_SHA1="9406a8491ed2532d4878b0a91b16a0e5f8d93d80"
STATE_SHA1="6577c90a27efb34a7099150253c0bf557d75214c"
IMAGES=("V11_AIR_A","V11_AIR_B","V11_BED","V11_BED_SIDE")
ROI=(345,260,680,600)
F70=OUT/"INT4_F11D_70_TARGET_EVIDENCE_DISPOSITIONS_V13.csv"
PENDING=OUT/"INT4_F11D_2_PENDING_EXACT_F2_TARGETS_V1.csv"
AUDIT=OUT/"INT4_F11D_V11_WHITE_BED_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
REVIEW=OUT/"INT4_F11D_V11_SPECIAL_RENDER_IMAGE_REVIEW_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def locked(p):
    b=(ROOT/p).read_bytes()
    assert blob(b)==PINS[str(p)],("PINNED_ORIGINAL_CHANGED",str(p),blob(b))
    return b
def rows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def csvout(rs,fields):
    s=io.StringIO(newline="")
    w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n")
    w.writeheader();w.writerows(rs)
    return s.getvalue().encode("utf-8")
def jout(o):return (json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode("utf-8")

def archive(path):
    if path.exists():data=path.read_bytes()
    else:
        token=os.getenv("GH_TOKEN")
        if not token:raise FileNotFoundError("Original F11D Actions artifact and GH_TOKEN both missing")
        api=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
        heads={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
               "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-F11D-original-F2-audit"}
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*a,**k):return None
        try:
            with urllib.request.build_opener(NoRedirect).open(
                    urllib.request.Request(api,headers=heads),timeout=120) as response:
                data=response.read()
        except urllib.error.HTTPError as e:
            if e.code not in (301,302,303,307,308):raise
            location=e.headers.get("Location","")
            target=urlsplit(location)
            assert target.scheme=="https" and target.netloc and target.netloc!="api.github.com"
            with urllib.request.urlopen(urllib.request.Request(
                 location,headers={"User-Agent":"MCFR-F11D-original-F2-audit"}),timeout=120) as response:
                data=response.read()
        assert sha(data)==ZIP_SHA,("ORIGINAL_REMOTE_ZIP_CHANGED",sha(data))
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    assert sha(data)==ZIP_SHA,("ORIGINAL_ZIP_CHANGED",sha(data))
    return data

def original_pixel_diff(a,b):
    a=a.convert("RGB").crop(ROI)
    b=b.convert("RGB").crop(ROI)
    assert a.size==b.size
    return sum(1 for p,q in zip(a.getdata(),b.getdata())
               if max(abs(x-y) for x,y in zip(p,q))>=24)

def build(original_zip):
    rows70=rows(locked(PREV))
    study=rows(locked(STUDY))
    prior={x["target_id"]:dict(x) for x in rows70}
    actual=json.loads(locked(NEW))
    assert len(rows70)==len(prior)==70
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in rows70)==67
    assert sum(x["final_disposition"].startswith("HOLD") for x in rows70)==3
    historical=[x for x in study if x["case"]=="V11"]
    assert len(historical)==1
    r=historical[0]
    assert (r["cohort"],r["minecraft"],r["category"],r["block"],r["state"],
            r["geometry_status"],r["model_hash_kind"],int(r["elements"]),int(r["faces"]))==(
            "VANILLA","1.21.11","BED","white_bed","{}","NO_ORDINARY_ELEMENTS","GIT_BLOB_SHA1",0,0)
    assert r["model_sha"]==MODEL_SHA1 and r["state_sha"]==STATE_SHA1
    assert not r["provider_path"] and not r["provider_sha"]
    assert actual["status"]=="PASS_V11_REAL_TWO_PART_BED_AIR_CONTROL_NATIVE_F2_NOT_FINAL_GATE"
    assert actual["schema"]=="MCFR_INT4_F11D_REAL_V11_TWO_PART_SPECIAL_F2_SOURCE_AUDIT/v1"
    assert actual["historical_case_id"]=="V11"
    assert actual["official_client_sha256"]==CLIENT_SHA256
    assert actual["original_study_sha256"]==STUDY_SHA
    assert actual["source_model_git_blob_sha1"]==MODEL_SHA1
    assert actual["source_blockstate_git_blob_sha1"]==STATE_SHA1
    assert actual["original_no_ordinary_elements_or_faces"] is True
    assert actual["real_game_two_exact_server_blockstates"]==2
    assert actual["actual_original_native_F2_PNG_count"]==4
    assert actual["direct_special_renderer_java_call_verified"] is False
    assert (actual["full_F_approved"]==actual["INT5_part_semantics_approved"]==
            actual["INT6_AI_training_or_redistribution_rights_approved"]==0)
    assert prior["V11"]["final_disposition"].startswith("HOLD")
    with ZipFile(io.BytesIO(archive(original_zip))) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        assert set(names)=={"INT4_F11D_V11_WHITE_BED_REAL_F2_CAPTURE.json",
                           "INT4_F11D_V11_WHITE_BED_NATIVE_F2_AUDIT.json",
                           "client.log",*(name+".png" for name in IMAGES)}
        manifest=json.loads(z.read("INT4_F11D_V11_WHITE_BED_REAL_F2_CAPTURE.json"))
        audit=json.loads(z.read("INT4_F11D_V11_WHITE_BED_NATIVE_F2_AUDIT.json"))
        assert manifest["schema"]=="MCFR_INT4_F11D_REAL_MOJANG_12111_WHITE_BED_SPECIAL_F2/v1"
        assert manifest["status"]=="ACTUAL_V11_BED_AIR_CONTROL_AND_TWO_PART_F2_NOT_YET_INDEPENDENTLY_AUDITED"
        assert manifest["minecraft_version"]=="1.21.11"
        assert manifest["original_historical_case_id"]=="V11"
        assert manifest["server_foot_exact"] is True and manifest["server_head_exact"] is True
        assert manifest["original_foot_state"]=="minecraft:white_bed[facing=north,part=foot,occupied=false]"
        assert manifest["original_head_state"]=="minecraft:white_bed[facing=north,part=head,occupied=false]"
        assert manifest["head_position"]==[0,120,39] and manifest["foot_position"]==[0,120,40]
        src=manifest["original_source_and_renderer_boundary"]
        assert src["official_client_sha256"]==CLIENT_SHA256
        assert src["historical_study_sha256"]==STUDY_SHA
        assert src["model_git_blob_sha1"]==MODEL_SHA1
        assert src["blockstate_git_blob_sha1"]==STATE_SHA1
        assert src["model_ordinary_elements"]==src["model_ordinary_faces"]==0
        assert src["ordinary_geometry_provider"] is None
        assert src["block_entity_renderer_direct_instrumentation_approved"] is False
        assert audit["status"]==actual["status"]
        assert audit["source_model_git_blob_sha1"]==MODEL_SHA1
        assert audit["source_blockstate_git_blob_sha1"]==STATE_SHA1
        assert audit["direct_special_renderer_java_call_verified"] is False
        assert (audit["full_F_approved"]==audit["INT5_part_semantics_approved"]==
                audit["INT6_AI_training_or_redistribution_rights_approved"]==0)
        rawlog=z.read("client.log")
        assert sha(rawlog)==manifest["original_client_log_sha256"]==actual["client_log_sha256"]
        game_log=rawlog.decode("utf-8",errors="replace")
        for token in ("MCFR_BED_AIR_FOOT=PASS","MCFR_BED_AIR_HEAD=PASS",
                      "MCFR_BED_FOOT=PASS","MCFR_BED_HEAD=PASS","MCFR_BED_CONSTRUCTED",
                      "MCFR_BED_STATES_READ"):
            assert token in game_log,("MISSING_REAL_SERVER_PASS",token)
        assert "MCFR_BED_FOOT=FAIL" not in game_log and "MCFR_BED_HEAD=FAIL" not in game_log
        assert set(actual["native_F2_png_sha256"])==set(IMAGES)
        assert manifest["actual_native_F2_images"]==actual["native_F2_png_sha256"]
        images={}
        for image_id in IMAGES:
            raw=z.read(image_id+".png")
            assert sha(raw)==actual["native_F2_png_sha256"][image_id]
            with Image.open(io.BytesIO(raw)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
                images[image_id]=im.convert("RGB")
        air_diff=original_pixel_diff(images["V11_AIR_A"],images["V11_AIR_B"])
        bed_diff=original_pixel_diff(images["V11_AIR_B"],images["V11_BED"])
        assert air_diff<=250 and bed_diff>=700 and bed_diff>5*air_diff
        assert actual["same_camera_air_vs_bed_pixel_contrast"]==manifest[
            "same_camera_air_control_and_bed_pixel_metrics"]
        metrics=actual["same_camera_air_vs_bed_pixel_contrast"]
        assert (air_diff,bed_diff)==(metrics["air_control_changed_pixels"],
                                     metrics["bed_vs_air_changed_pixels"])
        assert audit["same_camera_air_vs_bed_pixel_contrast"]==metrics
    note=("원본 V11 일반 JSON 모델에는 요소·면 0개. 실제 공식 클라이언트에서 "
          "발/머리 두 상태와 같은 카메라의 빈 공간 2장 대비 침대 정면·측면 원본 F2 확인. "
          "Java 렌더러 호출은 직접 추적하지 않아 추론 경계와 함께 조건부만 수용.")
    for entry in rows70:
        if entry["target_id"]!="V11":continue
        entry.update({
            "prior_f2_evidence_status":"OFFICIAL_12111_V11_ZERO_ORDINARY_MODEL_VS_AIR_NATIVE_F2",
            "image_artifact_ids":str(ARTIFACT),"image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+";".join(x+".png" for x in IMAGES),
            "image_sha256s":";".join(actual["native_F2_png_sha256"][x] for x in IMAGES),
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":note,
            "source_state_and_release_assessment":
                "MOJANG_12111_TWO_PART_BED_AND_ZERO_FACE_MODEL_ORIGINAL_AIR_CONTROL_F2",
            "final_disposition":"CONDITIONAL_F11D_V11_SPECIAL_BED_SOURCE_NATIVE_F2_NO_JAVA_METHOD_TRACE",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":
                "렌더러 직접 호출 및 일반 모델 외 기하 좌표는 미검증. "
                "자연 설치·충돌·수면·UV·의미·사용권 별도 최종 심사 필요.",
        })
    assert {x["target_id"] for x in rows70 if x!=prior[x["target_id"]]}=={"V11"}
    remaining=[x for x in rows70 if x["final_disposition"].startswith("HOLD")]
    assert {x["target_id"] for x in remaining}=={"R06","R08"}
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in rows70)==68
    hist=[x for x in rows70 if x["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(hist)==62 and sum(x["final_disposition"].startswith("CONDITIONAL") for x in hist)==62
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in rows70)
    allbytes=csvout(rows70,list(rows70[0]))
    cols=("target_id","cohort","minecraft_version","category","block",
          "original_source_applications","original_source_faces",
          "final_disposition","additional_required_before_full_acceptance")
    still=csvout([{k:x[k] for k in cols} for x in remaining],list(cols))
    summary={
      "schema":"MCFR_INT4_F11D_INDEPENDENT_V11_REAL_BED_F70/v1",
      "status":"PASS_V11_NATIVE_BED_F2_CONDITIONAL_68_HOLD_2_FINAL_ZERO",
      "upstream_original_git_blob_SHA1":PINS,
      "actual_original_game_run":RUN,
      "actual_original_game_artifact":ARTIFACT,
      "native_original_zip_sha256":ZIP_SHA,
      "official_client_sha256":CLIENT_SHA256,
      "original_study_sha256":STUDY_SHA,
      "V11_evidence":{
          "ordinary_model_elements":0,"ordinary_model_faces":0,
          "real_two_part_server_states":2,
          "native_F2_images":4,
          "air_baseline_changed_pixels":air_diff,"actual_bed_minus_air_pixels":bed_diff,
          "original_source_model_git_blob_SHA1":MODEL_SHA1,
          "original_source_blockstate_git_blob_SHA1":STATE_SHA1,
          "Java_renderer_callsite_instrumented":False,
          "native_images_sha256":actual["native_F2_png_sha256"],
      },
      "counts":{"F_targets":70,"historic_original_cases":62,
                "conditional_before":67,"conditional_after":68,
                "HOLD_before":3,"HOLD_after":2,
                "historic_F2_before":61,"historic_F2_after":62,
                "unconditional_final_F_pass":0,"INT5_semantics_approved":0,
                "INT6_AI_training_or_redistribution_rights_approved":0},
      "remaining_HOLD_target_ids":["R06","R08"],
      "scope_limits":[
          "Exact source 0 ordinary elements and real F2 evidence do not prove BedRenderer method execution.",
          "Strict bed placement head/foot is not natural player placement, sleeping or collision verification.",
          "UV pixel causality, furniture part meaning, asset rights and G/H gate approval remain absent.",
          "Original study and other 69 F70 ledger rows were never changed.",
          "Macaw time-separated R06 and AF dual-release R08 remain HOLD.",
      ],
      "output_sha256":{"F70":sha(allbytes),"pending":sha(still)},
    }
    md="\n".join([
      "# INT-4-F11D 바닐라 V11 침대 특수렌더 실제 F2 독립 감사",
      "",
      "- 역사 V11 일반 모델 원본 요소/면 0/0 및 원본 모델 SHA1 "+MODEL_SHA1+" 직접 검사.",
      "- 실제 Mojang 1.21.11 서버 foot/head 두 블록 상태 PASS; strict 배치로 원본 상태 고정.",
      "- 같은 카메라 AIR 대조 2장과 침대 정면·측면 원본 F2 2장 총 4장·SHA 확인.",
      "- 빈 상태 두 F2 차분 "+str(air_diff)+"px, 침대 대비 "+str(bed_diff)+"px (ROI "+str(ROI)+").",
      "- 이는 비일반 렌더 경로가 필요하다는 조건부 근거. Java 렌더러 메서드 직접 추적/3D 추출 승인 아님.",
      "- F70 조건부 67→68, HOLD 3→2. 원형 1-5 사례 F2 61→62/62. 무조건 최종 승인 0.",
      "- 보류 R06 물 싱크 시간차 두 화면, R08 AF 서로 다른 릴리스 실게임 비교. G/H·INT5·INT6 미승인.",
      "",
    ]).encode("utf-8")
    return {F70:allbytes,PENDING:still,AUDIT:jout(summary),REVIEW:md}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--artifact-dir",type=Path,default=Path("tmp-F11D-original-native"))
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    for name,data in build(args.artifact_dir/ZIP_NAME).items():
        out=ROOT/name
        if args.verify:
            assert out.is_file() and out.read_bytes()==data,("NONDETERMINISTIC_F11D",str(name))
        else:
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(data)
        print("VERIFIED" if args.verify else "CREATED",name,len(data))
    print("F11D exact V11, source0 faces, original F2 4, conditional68 HOLD2 final0")

if __name__=="__main__":
    main()
