#!/usr/bin/env python3
"""INT-4-F5: independently join real Fabric 12-case original F2, server logs and original SHA.

Diagnostic-only: S02/S34 cannot pass the historical specific state without an exact
game server state at that frame. Neither model JSON presence nor screenshot existence
approves true/inner_left or semantic/AI asset rights. Original game images stay in
retention-limited GitHub Actions artifact, not this repository.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from zipfile import ZipFile

from mcfr import int4_nonchair_runtime as runner
from mcfr import int4_f5_state_diagnostic as diag

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
FIXED=I/"INT4_F5_TWO_STATE_ACTUAL_CLIENT_DIAGNOSTIC_V1.json"
PREVIOUS=I/"INT4_F4_70_TARGET_EVIDENCE_DISPOSITIONS_V4.csv"
F4=I/"INT4_F4_DIRECT_VISUAL_PARTIAL_ACCEPTANCE_SUMMARY_V1.json"
SOURCE=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={
    str(FIXED):"491fa696daeed31284ae47695dd0ad7741004f15",
    str(PREVIOUS):"755e5d5e6364507f4bba09ca2e6e7d9052f3479d",
    str(F4):"37c070d9c1a02fc2c93e264e4daaee72b1a552bf",
    str(SOURCE):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
RUN=45026378323
ARTIFACT=14755154139
ZIP_NAME="INT4_F5_12_Actual_Fabric_Property_Diagnostic.zip"
ZIP_SHA="d55d60a7165851f164231cfd7e5c70824e5a076225bca0ce3df5a4a5eb858d83"
PNG_CASES=("S02","S34")
SCHEMA="MCFR_INT4_F5_REAL_FABRIC_PROPERTY_AND_ORIGINAL_IMAGE_PROVENANCE_AUDIT/v1"
VISUAL={
 "S02_ISOLATED":"원본 F2에서 낮은 나무 의자 1개가 보임",
 "S02_TABLE_EAST":"나무 의자 오른쪽(화면 기준)에 목재 테이블이 추가된 모습이 보임",
 "S02_TABLE_SOUTH":"의자 앞쪽에 목재 테이블이 추가된 모습이 보임",
 "S34_ISOLATED":"밝은 좌판의 낮은 소파형 블록 한 개가 보임",
 "S34_NEIGHBOR_EAST":"원본 F2에서 소파 두 개가 좌우 연결된 형태가 보임",
 "S34_NEIGHBOR_WEST":"원본 F2에서 소파 두 개가 좌우 연결된 형태가 보임",
 "S34_NEIGHBOR_NORTH":"원본 F2에서 앞뒤로 배치된 소파 두 개가 보임",
 "S34_NEIGHBOR_SOUTH":"원본 F2에서 앞뒤로 배치된 소파 두 개가 보임",
 "S34_L_EAST_NORTH":"원본 F2에서 L형으로 놓인 소파 3개가 보임",
 "S34_L_EAST_SOUTH":"원본 F2에서 L형으로 놓인 소파 3개가 보임",
 "S34_L_WEST_NORTH":"원본 F2에서 L형으로 놓인 소파 3개가 보임",
 "S34_L_WEST_SOUTH":"원본 F2에서 L형으로 놓인 소파 3개가 보임",
}
FIELDS=[
    "trial_id","historic_case","requested_original_properties","neighbor_layout",
    "server_requested_exact","actual_facing","actual_tucked","actual_variant",
    "actual_shape","actual_color","actual_waterlogged",
    "native_f2_sha256","native_f2_dimensions","visual_observation_ko",
    "original_study_state_approved","f_stage_final_approval"
]
REPORT_OUT=I/"INT4_F5_12_REAL_GAME_PROPERTY_MATRIX_V1.csv"
JSON_OUT=I/"INT4_F5_TWO_HOLD_NORMALIZATION_AUDIT_V1.json"
MD_OUT=I/"INT4_F5_PROPERTY_DIAGNOSTIC_REPORT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def pin(path):
    b=(ROOT/path).read_bytes()
    assert blob(b)==PINS[str(path)],("INPUT_GIT_BLOB_DRIFT",str(path),blob(b))
    return b

def read_csv(b):
    return list(csv.DictReader(io.StringIO(b.decode("utf-8"),newline="")))
def csv_data(rows,fields):
    output=io.StringIO(newline="")
    w=csv.DictWriter(output,fieldnames=fields,lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return output.getvalue().encode()
def json_data(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def fetch_artifact(path):
    if path.exists():return path.read_bytes()
    token=os.environ.get("GH_TOKEN")
    if not token:raise FileNotFoundError("Original F5 ZIP required or set GH_TOKEN")
    url="https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/"+str(ARTIFACT)+"/zip"
    h={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
       "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-INT4-F5-source-auditor"}
    class RejectRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    try:
        with urllib.request.build_opener(RejectRedirect).open(
                urllib.request.Request(url,headers=h),timeout=90) as resp: b=resp.read()
    except urllib.error.HTTPError as ex:
        if ex.code not in (301,302,303,307,308):raise
        next_url=ex.headers.get("Location","")
        p=urlsplit(next_url)
        assert p.scheme=="https" and p.netloc and p.netloc!="api.github.com",(
            "UNEXPECTED_REDIRECT",next_url[:100])
        with urllib.request.urlopen(urllib.request.Request(next_url,headers={"User-Agent":"MCFR-INT4-F5-source-auditor"}),timeout=90) as resp:
            b=resp.read()
    assert sha(b)==ZIP_SHA,("ORIGINAL_ZIP_DRIFT",sha(b))
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    return b


def build(original_zip):
    audit=json.loads(pin(FIXED).decode())
    baseline=read_csv(pin(PREVIOUS))
    previous=json.loads(pin(F4).decode())
    study=pin(SOURCE)
    assert sha(study)=="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
    assert len(baseline)==70 and len({x["target_id"] for x in baseline})==70
    assert previous["counts"]["conditional"]==37 and previous["counts"]["hold"]==33
    assert previous["counts"]["historic_case_exact_F2_mapped_now"]==31
    assert previous["counts"]["unconditional_accepted"]==0
    assert audit["status"]=="PASS_REAL_FABRIC_EXACT_PROPERTY_ENUM_AND_F2_NOT_SEMANTIC_EXIT"
    assert audit["minecraft"]=="1.21.1" and audit["historic_case_ids"]==list(PNG_CASES)
    assert audit["trial_count"]==12 and len(audit["cases"])==12
    assert len(OBS)==12 and set(OBS)==set(audit["cases"])
    previous_by={r["target_id"]:r for r in baseline}
    assert all(previous_by[x]["final_disposition"].startswith("HOLD") for x in PNG_CASES)

    raw=fetch_artifact(original_zip)
    assert sha(raw)==ZIP_SHA
    with ZipFile(io.BytesIO(raw)) as zip_:
        assert zip_.testzip() is None
        names=zip_.namelist()
        assert len(names)==len(set(names))
        assert set(names)=={"manifest.json","client.log",*(trial+".png" for trial in audit["cases"])}
        manifest=json.loads(zip_.read("manifest.json"))
        assert manifest["diagnostic_mode"] is True
        assert manifest["minecraft"]=="1.21.1"
        assert manifest["source"]["ledger_sha256"]==sha(study)
        assert manifest["f_target_case_ids"]==list(PNG_CASES)
        assert manifest["f_source_only"] is True
        assert sha(zip_.read("client.log"))==manifest["client_log_sha256"]==audit["game_client_log_sha256"]
        expected=diag.stages(manifest["property_values"])
        assert expected.keys()==audit["cases"].keys()==manifest["server_states"].keys()
        regenerated=runner.read_states(
            zip_.read("client.log").decode("utf-8",errors="replace"),
            "1.21.1",manifest["property_values"],
            case_ids=PNG_CASES,source_only=True,diagnostic_mode=True)
        assert regenerated==manifest["server_states"]
        assert set(manifest["native_f2_sha256"])==set(audit["cases"])
        assert manifest["source"]["diagnostic_release_properties"]==audit["release_state_property_source"]

        table=[]
        cases={}
        for name in expected:
            entry=audit["cases"][name]
            m=manifest["server_states"][name]
            case=entry["case"]
            assert case in PNG_CASES
            assert entry["requested_exact_original_state"]==diag.EXPECTED_ORIGINAL[case][1]
            assert entry["exact_server_state_persisted"]==m["subject"]["exact"] is False
            actual=dict(entry["actual_release_properties"])
            assert actual=={k:v for k,v in m["actual"].items() if k!="block"}
            assert m["actual"]["block"]=="present"
            assert set(actual)==set(audit["release_state_property_source"][case]["property_values"])
            assert entry["neighbor_fixture"]==expected[name][0][1:-1]
            img=zip_.read(name+".png")
            assert sha(img)==entry["native_f2_sha256"]==manifest["native_f2_sha256"][name]
            # PNG pixels/dimensions were reopened in the original F5 runner; verify here again.
            from PIL import Image
            with Image.open(io.BytesIO(img)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            vals=audit["release_state_property_source"][case]["property_values"]
            assert all(v in vals[k] for k,v in actual.items())
            if case=="S02":
                assert actual=={"facing":"north","tucked":"false","variant":"1"},name
                assert "TABLE" in name or name=="S02_ISOLATED"
            else:
                assert actual=={
                    "color":"white","facing":"north",
                    "shape":("right" if ("EAST" in name) else "left" if ("WEST" in name) else "single"),
                    "waterlogged":"false"
                },name
                assert actual["shape"]!="inner_left"
            table.append({
                "trial_id":name,"historic_case":case,
                "requested_original_properties":entry["requested_exact_original_state"],
                "neighbor_layout":"|".join(entry["neighbor_fixture"]) or "ISOLATED",
                "server_requested_exact":"false",
                "actual_facing":actual.get("facing",""),
                "actual_tucked":actual.get("tucked",""),
                "actual_variant":actual.get("variant",""),
                "actual_shape":actual.get("shape",""),
                "actual_color":actual.get("color",""),
                "actual_waterlogged":actual.get("waterlogged",""),
                "native_f2_sha256":sha(img),
                "native_f2_dimensions":"1024x684",
                "visual_observation_ko":OBS[name],
                "original_study_state_approved":"false",
                "f_stage_final_approval":"false",
            })
            cases[name]={"source_model_key":(previous["cases"][case]["original_model_key"]),
                         "state":actual,"native_f2_sha256":sha(img)}
    assert len(table)==12 and sum(x["historic_case"]=="S02" for x in table)==3
    counts=Counter(x["actual_shape"] for x in table if x["historic_case"]=="S34")
    assert counts=={"single":3,"left":3,"right":3},counts
    assert all(x["server_requested_exact"]=="false" for x in table)
    assert len(set(x["native_f2_sha256"] for x in table))==12
    assert cases["S02_ISOLATED"]["native_f2_sha256"]==previous["cases"]["S02"]["native_png_sha256"]
    assert cases["S34_ISOLATED"]["native_f2_sha256"]==previous["cases"]["S34"]["native_png_sha256"]
    raw_csv=csv_data(table,FIELDS)
    result={
        "schema":SCHEMA,
        "status":"PASS_12_NATIVE_F2_PROPERTY_PROBES_ZERO_TARGET_EXACT_NO_HOLD_RELEASE",
        "source_previous_git_blob":PINS,
        "source_game_action_id":RUN,
        "source_game_action_url":"https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/"+str(RUN),
        "source_artifact_id":ARTIFACT,
        "source_zip_sha256":ZIP_SHA,
        "source_client_log_sha256":manifest["client_log_sha256"],
        "source_original_historical_application_sha256":sha(study),
        "research_release_original_provenance":audit["release_state_property_source"],
        "counts":{
            "original_fixed_F_target_units":70,"historic_study_cases":62,
            "actual_client_trials":12,"actual_native_F2_images":12,"native_PNG_distinct_SHA":12,
            "S02_tucked_false_actual":3,"S02_tucked_true_actual":0,
            "S34_shape_single_actual":3,"S34_shape_left_actual":3,"S34_shape_right_actual":3,
            "S34_shape_inner_left_actual":0,"exact_requested_original_state_success":0,
            "newly_accepted_historic_case_F2":0,
            "F70_conditional_previous":37,"F70_conditional_current":37,
            "F70_hold_previous":33,"F70_hold_current":33,
            "F70_final_unconditional_approval":0,
            "historic_exact_F2_linked":31,"historic_exact_F2_remaining":31,
            "AI_semantic_new_approvals":0,"AI_training_redistribution_new_rights":0,
        },
        "case_outcomes":{
            "S02":{"status":"HOLD_EXACT_TUCKED_TRUE_NOT_REPRODUCED",
                   "source_original_requested":"tucked=true",
                   "observed_properties":"tucked=false across isolated + east/south oak_table",
                   "cause":"Unknown: possible mod neighbor/placement logic; no player interaction tested"},
            "S34":{"status":"HOLD_EXACT_INNER_LEFT_NOT_REPRODUCED",
                   "source_original_requested":"shape=inner_left",
                   "observed_properties":"isolated/north/south=single; east/left-right L=right; west/left-right L=left",
                   "cause":"Unknown: neighbor orientation and full inner-corner placement not exhausted"},
        },
        "known_limitations":[
            "All original vanilla/Fabric game states, blockstate source hashes, 12 screenshot hashes and client server log verified.",
            "Original 1-5 S02/S34 state was NOT reproduced in any trial; no historical case upgrade.",
            "Other furniture already passed in previous 70-target ledger; historical source rows remain unchanged.",
            "A successful diagnostic CI does not mean test subjects S02/S34 have passed exact historical render requirements.",
            "No baked UV causal attribution, part semantic/functional approval, natural item placement or mod redistribution rights inferred.",
            "Temporary GitHub Actions archive expires under retention; Git stores metadata only.",
        ],
        "outputs":{"matrix":{"rows":12,"sha256":sha(raw_csv)}},
    }
    data=json_data(result)
    md="\n".join([
        "# INT-4-F5 — 원본 게임 12회 속성 변화 독립 증거 감사",
        "",
        f"- 원본 Fabric 1.21.1 캡처/클라이언트 로그: [Actions #{RUN}](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN})",
        f"- 12개 원본 F2 PNG + 서버 로그 아티팩트: [원본 ZIP](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}/artifacts/{ARTIFACT})",
        "- **S02 의자** 고립·목재 테이블 동쪽·남쪽 3회 모두 \`tucked=false\`. 연구 원본 \`true\`는 유효한 원본 blockstate 속성이나 실제 배치에서 유지되지 않음.",
        "- **S34 소파** 고립/북쪽/남쪽 3회 \`single\`, 동쪽 단독/동쪽 포함 L형 3회 \`right\`, 서쪽 단독/서쪽 포함 L형 3회 \`left\`. \`inner_left\` 재현 0회.",
        "- 서버 로그를 진단 모드로 독립 재파싱해 실제 전체 속성값과 해시 12장, 연구 모델 경로를 재검증함.",
        "- 실제 F2 비교판을 사람이 열어 가구/이웃 배치를 관찰했으나 형상 차이의 인과·UV 및 모드 의도·AI 권리는 확정하지 않음.",
        "- **기존 70개 판정 유지: 조건부 37 / 보류 33 / 최종 승인 0, 역사 정확 F2 31/62.** 이 진단에 의한 보류 해제 0개.",
        "- 다음: S02 실사용 플레이어 상호작용·책상 위치/방향, S34 이웃의 서로 다른 방향 조합과 실제 코너 구성/호환 블록 로직을 분리 검증.",
        "",
    ]).encode()
    return {REPORT_OUT:raw_csv,JSON_OUT:data,MD_OUT:md}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",default="temporary-artifacts",type=Path)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    for path,raw in build(args.artifact_dir/ZIP_NAME).items():
        dest=ROOT/path
        if args.verify:
            assert dest.exists() and dest.read_bytes()==raw,("OUTPUT_NONDETERMINISTIC",str(path))
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(raw)
        print("VERIFIED" if args.verify else "CREATED",path,len(raw))
    print("PASS 12 original F2, S02/S34 both HOLD, 70 =37 conditional+33 HOLD")

if __name__=="__main__":main()
