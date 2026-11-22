#!/usr/bin/env python3
"""F10 independent original Minecraft F2 evidence and frozen 70-case adjudication.

Fail closed on original SHA, official client source manifest/server log, PNG
pixels and original Macaw 3.4.2 blockstate/model/provider paths and SHA256.
Update ONLY S13/S24/S25/S35/S36. Conditional evidence != UV/functional,
part semantics, natural adjacency, licensing or unconditional F acceptance.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from collections import Counter
from zipfile import ZipFile

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
DIR=Path("project/integration")
PREV=DIR/"INT4_F9_70_TARGET_EVIDENCE_DISPOSITIONS_V8.csv"
F9_AUDIT=DIR/"INT4_F9_FIVE_MACAW_NATIVE_F2_INDEPENDENT_AUDIT_V1.json"
F10_CAPTURE=DIR/"INT4_F10_MACAW_FIVE_ACTUAL_F2_SOURCE_V1.json"
HISTORICAL=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
LOCKS={
 str(PREV):"387dd0d50d2bcf48a3a4210742ccb9623f5ee9a6",
 str(F9_AUDIT):"9443a031d6965d9e3acd425d0e0326185d3d6dc4",
 str(F10_CAPTURE):"4ab10ecd62f339d9ca26d9e51acc48b635684a06",
 str(HISTORICAL):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
RUN=45039429134
ARTIFACT=14761291650
ZIP_NAME="INT4_F10_MACAW_FIVE_OFFICIAL_ORIGINAL_F2.zip"
ZIP_SHA256="e35a901c649cdab24cb3065e9df44d8cafa7f8c81cff696f23a1eb66ca59cb22"
MACAW_JAR_SHA256="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
HIST_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
CASES=("S13","S24","S25","S35","S36")
ELEMENTS={"S13":1,"S24":6,"S25":5,"S35":11,"S36":7}
FACES={"S13":6,"S24":31,"S25":26,"S35":66,"S36":42}
EXPECTED={
 "S13":("mcwfurnitures:oak_coffee_table","connection=center"),
 "S24":("mcwfurnitures:oak_drawer","connection=middle;facing=north"),
 "S25":("mcwfurnitures:oak_wardrobe","connection=base;facing=north;hinge=left"),
 "S35":("mcwfurnitures:white_couch","facing=north;shape=single"),
 "S36":("mcwfurnitures:white_couch","facing=north;shape=left_corner"),
}
OBS={
 "S13":"원본 F2에서 낮고 평평한 갈색 판형 커피 테이블 중심 부품이 보임. 전체 테이블 완성 형태 아님.",
 "S24":"원본 F2에서 좁은 세로형 목재 서랍 연결 부품이 보임. 실제 열림/닫힘 기능 미검증.",
 "S25":"원본 F2에서 세로 무늬의 작은 목재 옷장 기본 부품이 보임. 전체 다단 옷장 완성 형태 아님.",
 "S35":"원본 F2에서 흰색의 낮은 소파 단일 부품이 보임. 좌석 기능 미검증.",
 "S36":"원본 F2에서 흰색 코너형 소파 부품이 보임. 무채색 흰색 픽셀 가시성으로 별도 확인.",
}
OUT70=DIR/"INT4_F10_70_TARGET_EVIDENCE_DISPOSITIONS_V9.csv"
PENDING=DIR/"INT4_F10_17_PENDING_EXACT_F2_TARGETS_V1.csv"
SUMMARY=DIR/"INT4_F10_FIVE_MACAW_ORIGINAL_NATIVE_F2_INDEPENDENT_AUDIT_V1.json"
REPORT=DIR/"INT4_F10_FIVE_CASE_ORIGINAL_IMAGE_REVIEW_V1.md"

def sha256(data):return hashlib.sha256(data).hexdigest()
def blob(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def locked(path):
    raw=(ROOT/path).read_bytes()
    assert blob(raw)==LOCKS[str(path)],("ORIGINAL_GIT_BLOB_DRIFT",str(path),blob(raw))
    return raw
def csvrows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"),newline="")))
def dumpcsv(records,columns):
    buf=io.StringIO(newline="")
    writer=csv.DictWriter(buf,fieldnames=columns,lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buf.getvalue().encode("utf-8")
def dumpjson(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")

def original_zip(path):
    if path.is_file():
        content=path.read_bytes()
    else:
        key=os.environ.get("GH_TOKEN")
        if not key:
            raise FileNotFoundError("Original F10 Actions ZIP not present and GH_TOKEN unset")
        url=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
        header={"Authorization":f"Bearer {key}","Accept":"application/vnd.github+json",
                "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-INT4-F10-source-locked-audit"}
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):return None
        try:
            with urllib.request.build_opener(NoRedirect).open(
                urllib.request.Request(url,headers=header),timeout=120) as response:
                content=response.read()
        except urllib.error.HTTPError as exc:
            if exc.code not in (301,302,303,307,308):
                raise
            location=exc.headers.get("Location","")
            parsed=urlsplit(location)
            assert parsed.scheme=="https" and parsed.netloc and parsed.netloc!="api.github.com"
            with urllib.request.urlopen(
                urllib.request.Request(location,headers={"User-Agent":"MCFR-INT4-F10-source-locked-audit"}),
                timeout=120) as response:
                content=response.read()
        assert sha256(content)==ZIP_SHA256,("ORIGINAL_ZIP_REMOTE_SHA_CHANGED",sha256(content))
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(content)
    assert sha256(content)==ZIP_SHA256,("ORIGINAL_ZIP_SHA_CHANGED",sha256(content))
    return content

def build(path):
    baseline=csvrows(locked(PREV))
    f9=json.loads(locked(F9_AUDIT).decode("utf-8"))
    live=json.loads(locked(F10_CAPTURE).decode("utf-8"))
    historical_bytes=locked(HISTORICAL)
    historical=csvrows(historical_bytes)
    assert sha256(historical_bytes)==HIST_SHA256
    assert len(baseline)==70 and len({r["target_id"] for r in baseline})==70
    assert (sum(r["final_disposition"].startswith("CONDITIONAL") for r in baseline),
            sum(r["final_disposition"].startswith("HOLD") for r in baseline))==(48,22)
    assert f9["counts"]["F_conditional_now"]==48 and f9["counts"]["F_HOLD_now"]==22
    assert f9["counts"]["historical_F2_conditional_now"]==42
    assert live["status"]=="PASS_EXACT_FIVE_ORIGINAL_1_21_11_MACAW_SOURCE_STATES_ACTUAL_F2"
    assert live["minecraft"]=="1.21.11"
    assert live["case_ids"]==list(CASES)
    assert (live["server_exact_blockstates"],live["native_F2_original_images"])==(5,5)
    assert (live["original_model_elements"],live["original_model_faces"])==(30,171)
    assert live["macaw_mod_jar_sha256"]==MACAW_JAR_SHA256
    assert live["original_source_sha256"]==HIST_SHA256
    assert live["full_F_accepted"]==live["INT5_part_semantics_approved"]==live["INT6_rights_approved"]==0
    original={case:[r for r in historical if r["case"]==case] for case in CASES}
    assert all(len(rows)==1 for rows in original.values())
    assert all(r["final_disposition"].startswith("HOLD") for r in baseline if r["target_id"] in CASES)

    archive=original_zip(path)
    verified={}
    with ZipFile(io.BytesIO(archive)) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        assert set(names)=={"INT4_F10_MACAW_FIVE_REAL_F2_CAPTURE.json",
                           "INT4_F10_MACAW_FIVE_F2_AUDIT.json",
                           "INT4_F10_MACAW_FIVE_F2_CONTACT.png","client.log",
                           *(case+".png" for case in CASES)}
        m=json.loads(z.read("INT4_F10_MACAW_FIVE_REAL_F2_CAPTURE.json"))
        a=json.loads(z.read("INT4_F10_MACAW_FIVE_F2_AUDIT.json"))
        assert m["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        assert m["minecraft_version"]=="1.21.11" and m["actual_game_capture"] is True
        assert m["source_state_verified_count"]==m["minecraft_native_f2_screenshot_count"]==5
        assert m["semantic_part_roles_approved"]==m["material_style_approved"]==m["copyright_or_ai_training_approved"]==0
        assert a["status"]=="PASS_FIVE_ORIGINAL_MACAW_F10_NATIVE_F2_AND_EXACT_SERVER_STATE_NOT_FINAL"
        assert a["source_cases"]==list(CASES)
        assert a["source_1_5_face_counts"]==FACES
        assert a["native_f2_count"]==a["server_verified_states"]==5
        assert a["white_couch_neutral_proxy_threshold"]==300
        assert m["original_source_registry"]["mod_jar_sha256"]==MACAW_JAR_SHA256
        assert m["original_source_registry"]["historical_application_sha256"]==HIST_SHA256
        assert a["original_source_sha256"]==HIST_SHA256
        assert sha256(z.read("client.log"))==m["client_log_sha256"]==live["client_log_sha256"]
        assert sha256(z.read("INT4_F10_MACAW_FIVE_REAL_F2_CAPTURE.json"))==a["f2_manifest_sha256"]
        assert sha256(z.read("INT4_F10_MACAW_FIVE_F2_CONTACT.png"))==a["contact_sheet_sha256"]
        assert a["boundaries"]==live["boundaries"]
        assert a["boundaries"]["explicit_setblock_source_states_verified"] is True
        assert a["boundaries"]["natural_connected_block_update_rules_tested"] is False
        assert a["boundaries"]["face_uv_render_pixel_causality_proven"] is False
        assert a["boundaries"]["int5_part_roles_approved"]==a["boundaries"]["int6_training_or_redistribution_rights_approved"]==0
        data={r["case_id"]:r for r in m["states"]}
        src=m["original_source_registry"]["states"]
        assert len(m["states"])==5 and set(data)==set(src)==set(CASES)
        game_log=z.read("client.log").decode("utf-8",errors="replace")
        for case in CASES:
            row=original[case][0]
            proof=data[case]
            selected=src[case]
            blk,properties=EXPECTED[case]
            expected_state=blk+"["+properties.replace(";",",")+"]"
            assert row["cohort"]=="MACAW" and row["minecraft"]=="1.21.11"
            assert (row["block"],row["state"])==(blk,properties)
            assert row["model_hash_kind"]=="SHA256" and row["geometry_status"]=="STATIC_SOURCE"
            assert (int(row["elements"]),int(row["faces"]))==(ELEMENTS[case],FACES[case])
            assert selected["original_state"]==proof["original_state"]==expected_state
            assert selected["model_path"]==proof["original_model_path"]==row["model_path"]
            assert selected["model_sha256"]==proof["original_model_sha256"]==row["model_sha"]
            assert selected["provider_sha256"]==proof["original_provider_sha256"]==row["provider_sha"]
            assert selected["blockstate_sha256"]==row["state_sha"]
            assert selected["original_model_y"]==proof["original_model_y"]==int(row["y"])
            assert selected["elements"]==ELEMENTS[case] and selected["faces"]==FACES[case]
            assert proof["server_state_verified"] is True and proof["native_f2_verified"] is True
            assert proof["semantic_or_rights_approved"] is False
            assert proof["connection_formed_naturally_tested"] is False
            assert proof["screen_foreground_visible_by_color_or_white_proxy"] is True
            chroma=proof["screen_foreground_chroma_pixels"]
            white=proof["screen_foreground_neutral_white_pixels"]
            assert (chroma>=150 or (case in ("S35","S36") and white>=300))
            assert a["visibility_foreground_chroma"][case]==chroma
            assert a["visibility_foreground_neutral_white"][case]==white
            assert proof["screenshot_dimensions"]==[1024,684]
            assert proof["screenshot_file"]==case+".png"
            logs=[line for line in game_log.splitlines() if
                  "[Server thread/" in line and
                  f"[RenderAudit] MCFR_CHAIR_STATE_{case}=" in line]
            assert len(logs)==1 and logs[0].endswith("=PASS"),("REAL_SERVER_STATE_MISMATCH",case,logs)
            png=z.read(case+".png")
            digest=sha256(png)
            assert digest==proof["screenshot_sha256"]==a["f2_sha256"][case]==live["native_F2_SHA256"][case]
            with Image.open(io.BytesIO(png)) as image:
                image.load()
                assert image.format=="PNG" and image.size==(1024,684)
            verified[case]={
               "exact_original_game_server_state":True,
               "original_source_model_and_provider_SHA256_matches_release":True,
               "source_geometry_elements":ELEMENTS[case],
               "source_geometry_faces":FACES[case],
               "actual_native_F2_sha256":digest,
               "color_pixels":chroma,
               "neutral_white_pixels":white,
               "direct_original_image_observation":OBS[case],
               "conditional_only":True,
               "natural_neighbor_updates_and_player_actions_verified":False,
               "UV_function_part_semantics_and_rights_approved":False,
            }
    assert len(set(v["actual_native_F2_sha256"] for v in verified.values()))==5
    previous={r["target_id"]:dict(r) for r in baseline}
    for item in baseline:
        case=item["target_id"]
        if case not in CASES:continue
        item.update({
          "prior_f2_evidence_status":"F10_REAL_CLIENT_MACAW_1_21_11_SERVER_SOURCE_NATIVE_F2",
          "image_artifact_ids":str(ARTIFACT),
          "image_run_ids":str(RUN),
          "image_files":ZIP_NAME+":"+case+".png",
          "image_sha256s":verified[case]["actual_native_F2_sha256"],
          "original_zip_sha256s":ZIP_SHA256,
          "newly_reopened_original_png":"true",
          "direct_visual_observation_this_turn":"true",
          "human_observation_text":OBS[case],
          "source_state_and_release_assessment":"MACAW_3_4_2_EXACT_SOURCE_STATE_RELEASE_PARENT_MODEL_SHA256_AND_ORIGINAL_F2_MATCH",
          "final_disposition":"CONDITIONAL_F10_EXACT_MACAW_ORIGINAL_STATE_MODEL_NATIVE_F2",
          "runtime_evidence_accepted_as_full_F_PASS":"false",
          "additional_required_before_full_acceptance":(
              "원본 1.21.11 블록상태·JAR 원본 모델/부모 SHA·실게임 F2 일치. "
              "연결형의 주변 블록 자연 변화/플레이어 입력, UV 픽셀 인과, 사용 기능, "
              "부품 의미, AI 학습·배포권 및 F 종료는 별도 검증."),
        })
    changed={r["target_id"] for r in baseline if previous[r["target_id"]]!=r}
    assert changed==set(CASES),("UNRELATED_F_TARGET_CHANGED",changed)
    ncond=sum(r["final_disposition"].startswith("CONDITIONAL") for r in baseline)
    nhold=sum(r["final_disposition"].startswith("HOLD") for r in baseline)
    assert (ncond,nhold)==(53,17)
    historic=[r for r in baseline if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(historic)==62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in historic)==47
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in baseline)
    pending=[r for r in baseline if r["final_disposition"].startswith("HOLD")]
    remaining=dict(sorted(Counter(r["cohort"] or "RISK" for r in pending).items()))
    assert remaining=={"RISK":2,"VANILLA":15}
    raw70=dumpcsv(baseline,list(baseline[0].keys()))
    columns=["target_id","cohort","minecraft_version","category","block",
             "original_source_applications","original_source_faces","final_disposition",
             "additional_required_before_full_acceptance"]
    raw17=dumpcsv([{k:r[k] for k in columns} for r in pending],columns)
    summary={
      "schema":"MCFR_INT4_F10_FIVE_MACAW_ORIGINAL_F2_INDEPENDENT_SOURCE_70_AUDIT/v1",
      "status":"PASS_FIVE_REAL_F2_MACAW_53_CONDITIONAL_17_HOLD_FULL_ZERO",
      "input_original_git_blob_sha1":LOCKS,
      "original_real_minecraft_run":RUN,
      "original_real_minecraft_artifact":ARTIFACT,
      "original_client_zip_sha256":ZIP_SHA256,
      "original_client_log_sha256":live["client_log_sha256"],
      "cases":verified,
      "remaining_HOLD_by_cohort":remaining,
      "counts":{
         "fixed_F_total":70,
         "original_1_5_historical_cases":62,
         "new_1_21_11_original_native_F2":5,
         "new_original_source_elements":30,
         "new_original_source_faces":171,
         "real_server_exact_states":5,
         "new_conditionally_linked_F_cases":5,
         "F_conditional_before":48,
         "F_conditional_after":53,
         "F_HOLD_before":22,
         "F_HOLD_after":17,
         "historical_1_5_conditional_F2_before":42,
         "historical_1_5_conditional_F2_after":47,
         "F_unconditional_final_approved":0,
         "new_INT5_semantic_part_approvals":0,
         "new_INT6_AI_training_and_redistribution_rights":0,
      },
      "limitations":[
        "All five original Macaw 3.4.2 1.21.11 /setblock source states read back exactly in real game; these are not naturally formed neighbor connections.",
        "S36 neutral white center ROI visual foreground 1519 pixels: case-specific proxy validated on actual PNG, not pixel UV causality.",
        "Selected source geometry can be a small component, not an assembled/full-size furniture item.",
        "All native F2 screenshots, server-log and model SHA match; functional semantics, texture UV, collisions and distribution rights not approved.",
        "Exactly five 70-target case rows changed, and prior 65 rows and all historical 1-5 sources are unchanged.",
        "Original JARs, PNGs and cube model JSON are not committed to Git; Actions original ZIP expires.",
        "F full exit, G/H, INT5 and INT6 remain pending.",
      ],
      "outputs":{
        "F70":{"sha256":sha256(raw70),"rows":70},
        "pending":{"sha256":sha256(raw17),"rows":17},
      },
    }
    readme="\n".join([
      "# INT-4-F10 Macaw 연결형 5개 역사 사례 — 원본 게임 F2 독립 감사",
      "",
      f"- 실제 [Minecraft 1.21.11 Fabric 게임 Actions #{RUN}](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}) 성공.",
      f"- [원본 F2 5장·client.log ZIP #{ARTIFACT}](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}/artifacts/{ARTIFACT}); ZIP SHA256 {ZIP_SHA256}.",
      "- 원형 Macaw's Furniture 3.4.2의 state/selected leaf/provider SHA256 및 실제 서버 상태와 5장 1024×684 F2를 모두 일치 검수.",
      "- S13 낮은 평판형 커피 테이블 중심 부품(6면), S24 세로형 서랍 연결 부품(31면), S25 세로형 옷장 기본 부품(26면) 관찰.",
      "- S35 흰색 단일 소파 부품(66면), S36 흰색 왼쪽 코너 소파 부품(42면) 관찰. S36은 갈색 색상 픽셀 83이므로 무채색 흰색 1519개 픽셀 검증을 추가 적용.",
      "- 총 5개의 서로 다른 원형 사례, 30요소/171면. 연결형 자연 인접 상태나 기능적 의미가 승인된 것은 아님.",
      "- 원장 고정 70: **조건부 48→53, HOLD 22→17, 역사 1-5 정확 F2 42/62→47/62**, 최종 무조건 승인은 0.",
      "- 남은 HOLD 17: **바닐라 V01~V15 15개 + 고위험 R06/R08 2개**. Macaw 원본 1-5 사례에 대한 F2 연결 HOLD 0.",
      "- 기존 연구 원본 CSV·AF/HC/Macaw 증거 파일·메인 브랜치를 변경하지 않고 독립 Draft F10 파생 결과만 저장.",
      "",
    ]).encode("utf-8")
    return {OUT70:raw70,PENDING:raw17,SUMMARY:dumpjson(summary),REPORT:readme}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--artifact-dir",type=Path,default=Path("temporary-int4-F10-original-client"))
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    for path,data in build(args.artifact_dir/ZIP_NAME).items():
        dest=ROOT/path
        if args.verify:
            assert dest.is_file() and dest.read_bytes()==data,("DETERMINISTIC_OUTPUT_MISMATCH",str(path))
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
        print("VERIFIED" if args.verify else "CREATED",path,len(data))
    print("PASS F10 five exact original native F2: F70 conditional 53/HOLD 17/full 0")

if __name__=="__main__":
    main()
