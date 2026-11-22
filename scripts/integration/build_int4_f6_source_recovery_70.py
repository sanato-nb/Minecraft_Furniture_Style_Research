#!/usr/bin/env python3
"""INT-4-F6: verify original Fabric client F2 ZIP and update only S02/S34 in 70 ledger."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,os,tempfile,urllib.request,urllib.error
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlsplit

from mcfr import int4_f6_source_causal_replay as f6
from mcfr import int4_nonchair_runtime as runner

ROOT=Path(__file__).resolve().parents[2]
BASE=Path("project/integration/INT4_F4_70_TARGET_EVIDENCE_DISPOSITIONS_V4.csv")
PRIOR=Path("project/integration/INT4_F5_TWO_HOLD_NORMALIZATION_AUDIT_V1.json")
QUEUE=Path("project/integration/INT4_F4_33_PENDING_EXACT_F2_TARGETS_V1.csv")
PINS={
    str(BASE):"755e5d5e6364507f4bba09ca2e6e7d9052f3479d",
    str(PRIOR):"f2c98909a38961c4682a9ce46cfd33642e30a4b3",
    str(QUEUE):"5703023f3ced32471705ae6fca143db4d8a3fdc0",
}
RUN=45028305708
ARTIFACT=14756442623
ZIP_SHA="650897691042552ad71ca67e729598e3e9798d0d4d8e197683638d04981924ec"
ARTIFACT_NAME="int4-f6-causal-chair-tuck-inner-couch-real-game-F2.zip"
STUDY={"S02":"S02_NORTH_TABLE_TUCK","S34":"S34_NORTH_WEST_INNER_LEFT"}
VIEWS={
"S02":"실제 원본 F2 화면에 의자와 북쪽 탁자가 붙어 배치되고 참나무 의자가 넣어진 외형이 보임; 서버 tucked=true 확인",
"S34":"실제 원본 F2 화면에 흰 좌판 참나무 소파가 안쪽 L형 코너로 이어지고 서버 shape=inner_left 확인",
}
OUT=Path("project/integration")
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def pinned(p):
    b=(ROOT/p).read_bytes()
    assert blob(b)==PINS[str(p)],("INPUT_SOURCE_GIT_SHA_CHANGED",str(p),blob(b))
    return b
def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8"),newline="")))
def csvraw(records,keys):
    buff=io.StringIO(newline="")
    w=csv.DictWriter(buff,fieldnames=keys,lineterminator="\n")
    w.writeheader();w.writerows(records)
    return buff.getvalue().encode()
def jsonraw(obj):return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def get_artifact(p):
    if p.is_file():return p.read_bytes()
    token=os.environ.get("GH_TOKEN")
    if not token:raise FileNotFoundError("Missing original F6 game artifact and GH_TOKEN")
    url="https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/"+str(ARTIFACT)+"/zip"
    h={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
       "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-F6-audit"}
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**k):return None
    try:
        with urllib.request.build_opener(NoRedirect).open(
                urllib.request.Request(url,headers=h),timeout=90) as z:
            data=z.read()
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308):raise
        u=e.headers["Location"]
        dest=urlsplit(u)
        assert dest.scheme=="https" and dest.netloc and dest.netloc!="api.github.com"
        with urllib.request.urlopen(
                urllib.request.Request(u,headers={"User-Agent":"MCFR-F6-audit"}),timeout=90) as z:
            data=z.read()
    assert sha(data)==ZIP_SHA,("ZIP_DATA_DRIFT",sha(data))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return data

def build(path):
    prior=json.loads(pinned(PRIOR).decode())
    baseline=rows(pinned(BASE))
    pending=rows(pinned(QUEUE))
    assert len(baseline)==70 and len({r["target_id"] for r in baseline})==70
    assert len(pending)==33 and len({r["target_id"] for r in pending})==33
    assert prior["counts"]["F70_conditional_current"]==37
    assert prior["counts"]["F70_hold_current"]==33
    old={r["target_id"]:dict(r) for r in baseline}
    assert all(old[k]["final_disposition"].startswith("HOLD") for k in STUDY)
    data=get_artifact(path)
    assert sha(data)==ZIP_SHA
    with tempfile.TemporaryDirectory(prefix="mcfr-f6-") as tmp:
        folder=Path(tmp)
        with ZipFile(io.BytesIO(data)) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert len(names)==12 and len(set(names))==12
            assert set(names)=={"manifest.json","client.log",
                                *(s+".png" for s in f6.TRIALS)}
            for name in names:
                assert "/" not in name and ".." not in name
                (folder/name).write_bytes(z.read(name))
        raw=runner.audit(folder)
        result=f6.audit(folder)
        assert raw["diagnostic_mode"]=="f6"
        assert raw["f_target_case_ids"]==["S02","S34"]
        assert raw["minecraft"]=="1.21.1"
        assert result["status"]=="PASS_REAL_CLIENT_TEN_SOURCE_CODE_CONDITION_TRIALS_NOT_FULL_F_EXIT"
        assert result["pinned_upstream_source_provenance"]==f6.SOURCE_PINS
        assert len(result["cases"])==10
        exact={k for k,v in result["cases"].items() if v["server_exact_requested_state"]}
        assert exact=={"S02_NORTH_TABLE_TUCK","S02_NORTH_TOP_SLAB_TUCK",
                       "S34_NORTH_WEST_INNER_LEFT"},("WRONG_EXACT_CASES",exact)
        assert all(v["upstream_code_hypothesis_matches_game"] for v in result["cases"].values())
        assert len(set(raw["native_f2_sha256"].values()))==10
        original,digest=f6.original_source()
        assert digest==raw["source"]["ledger_sha256"]
        assert set(raw["source"]["representative_states"])==set(STUDY)
        for case in STUDY:
            selected=raw["source"]["representative_states"][case]
            row=original[case]
            assert selected["historical_selection_matches_release"] is True
            assert selected["historical_model_geometry"]=={
                "elements":int(row["elements"]),"faces":int(row["faces"])}
            assert selected["state"]==runner.state(row["block"],row["state"])
            assert set(selected["source_files"])=={row["state_path"],row["model_path"],row["provider_path"]}
            for k in ("state","model","provider"):
                file=selected["source_files"][row[k+"_path"]]
                assert file["historical_git_blob_sha1"]==row[k+"_sha"]
                assert file["git_blob_byte_match"]==(case=="S34")
        from PIL import Image
        for key,value in result["cases"].items():
            file=folder/(key+".png")
            with Image.open(file) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            assert sha(file.read_bytes())==value["native_F2_sha256"]

    for item in baseline:
        case=item["target_id"]
        if case not in STUDY:continue
        stage=STUDY[case]
        x=result["cases"][stage]
        assert x["original_case"]==case and x["server_exact_requested_state"] is True
        item.update({
            "prior_f2_evidence_status":"REAL_CLIENT_SOURCE_CONDITION_EXACT_NATIVE_F2_MANUALLY_REVIEWED",
            "image_artifact_ids":str(ARTIFACT),"image_run_ids":str(RUN),
            "image_files":ARTIFACT_NAME+":"+stage+".png",
            "image_sha256s":x["native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":VIEWS[case],
            "source_state_and_release_assessment":(
                "AF_RESEARCH_SOURCE_RELEASE_BYTE_DRIFT_PRESERVED_SERVER_CAUSAL_CONDITION_PASS"
                if case=="S02" else
                "HC_STUDY_SOURCE_4_0_3_RELEASE_BYTE_EQUAL_SERVER_CAUSAL_CONDITION_PASS"),
            "final_disposition":"CONDITIONAL_F6_REAL_EXACT_ORIGINAL_STATE_F2_NOT_FULL_F_EXIT",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":(
                "원본 소스 모델/서버 상태/네이티브 F2 확인. 실제 상호작용·픽셀 UV·부품 의미·AI 원본 사용 권한 승인 별도"),
        })
    assert {r["target_id"] for r in baseline if r!=old[r["target_id"]]}==set(STUDY)
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in baseline)==39
    assert sum(r["final_disposition"].startswith("HOLD") for r in baseline)==31
    assert sum(r["target_kind"]=="HISTORICAL_1_5_CASE" and
               r["final_disposition"].startswith("CONDITIONAL") for r in baseline)==33
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in baseline)
    queue31=[r for r in pending if r["target_id"] not in STUDY]
    assert len(queue31)==31
    assert {r["target_id"] for r in queue31}=={
        r["target_id"] for r in baseline if r["final_disposition"].startswith("HOLD")}
    from collections import Counter
    counts=Counter(r["cohort"] for r in queue31)
    assert counts==Counter({"VANILLA":15,"AF":3,"HC":1,"MACAW":10,"RISK":2}),counts
    matrix=[]
    cols=["trial","historic_case","exact_original_state","actual_game_properties",
          "original_game_png_sha256","source_code_prediction_matches","full_exit"]
    for name,item in result["cases"].items():
        matrix.append({"trial":name,"historic_case":item["original_case"],
                       "exact_original_state":str(item["server_exact_requested_state"]).lower(),
                       "actual_game_properties":json.dumps(item["actual_game_properties"],sort_keys=True),
                       "original_game_png_sha256":item["native_F2_sha256"],
                       "source_code_prediction_matches":str(item["upstream_code_hypothesis_matches_game"]).lower(),
                       "full_exit":"false"})
    data70=csvraw(baseline,list(baseline[0]))
    data31=csvraw(queue31,list(pending[0]))
    data10=csvraw(matrix,cols)
    report={
        "schema":"MCFR_INT4_F6_EXACT_TWO_CASES_F2_70_INDEPENDENT_AUDIT/v1",
        "status":"PASS_S02_S34_EXACT_STATE_RECOVERED_TWO_CASES_CONDITIONAL_NOT_FINAL_F_EXIT",
        "source_previous_git_blob_sha":PINS,
        "source_historical_application_sha256":digest,
        "source_upstream_java_commits_and_blob_shas":f6.SOURCE_PINS,
        "game_execution_run":RUN,
        "game_execution_run_url":f"https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}",
        "game_execution_conclusion":"failure_from_sorted_json_key_order_in_post_capture_auditor_not_game_capture",
        "original_actions_artifact_id":ARTIFACT,
        "original_actions_zip_sha256":ZIP_SHA,
        "original_client_log_sha256":raw["client_log_sha256"],
        "source_correct_original_case_stage":STUDY,
        "original_case_png_hashes":{k:result["cases"][v]["native_F2_sha256"] for k,v in STUDY.items()},
        "counts":{
            "original_F2_captures":10,"unique_native_F2_sha":10,
            "exact_requested_states_in_10_trials":3,
            "new_exact_historical_1_5_cases":2,
            "historic_1_5_source_cases":62,
            "historic_exact_F2_before":31,"historic_exact_F2_after":33,
            "fixed_F_target_units":70,
            "conditional_before":37,"conditional_after":39,
            "HOLD_before":33,"HOLD_after":31,
            "fully_accepted_F_targets":0,"new_INT5_semantic_approvals":0,
            "new_INT6_training_redistribution_rights_approvals":0,
        },
        "remaining_HOLD_cohorts":dict(counts),
        "limits":[
            "Actual Fabric release server states and original native F2 images were independently revalidated after original capture strict-auditor key-order failure.",
            "Only S02/S34 updated among 70 fixed target units; all previous original cases and unrelated evidence remain unchanged.",
            "AF 4.0.3 source Git vs 4.0.2 game release JSON byte mismatch preserved. HC model source byte match verified.",
            "S02 player natural sneaking right click was not tested; /setblock source condition and neighbor updates were tested.",
            "F2 proves matching original block state in game, not pixelwise UV causation, seat physics, semantic parts or asset rights.",
            "No full INT4-F exit, INT5 part semantic approval or INT6 AI training/redistribution grant."
        ],
        "output_files":{
            "f70":{"rows":70,"sha256":sha(data70)},
            "pending":{"rows":31,"sha256":sha(data31)},
            "matrix":{"rows":10,"sha256":sha(data10)},
        },
    }
    markdown="\n".join([
        "# INT-4-F6 실제 Fabric 소스 조건 기반 원본 특수 상태 재현",
        "",
        "- Minecraft 1.21.1 Fabric 실제 실행 원본 F2 10장, 1024x684, PNG 10개 고유 SHA 및 client.log 독립 검증.",
        "- S02: 북쪽 앞 참나무 테이블과 위쪽 반 블록 배치에서 tucked=true 유지 각 1회. 동쪽 대조와 전방 받침 제거 시 tucked=false.",
        "- S34: 북쪽 이웃 소파 facing=west일 때 shape=inner_left 정확 유지. east/남쪽/차단 이웃 대조는 다른 shape로 판독.",
        "- 사용한 원본 Java 코드: AnotherFurniture ChairBlock/TuckableBlock, Handcrafted ModularSeatBlock 고정 Git SHA. 코드 기대 결과와 게임 서버 결과를 구분해 검증.",
        "- 최초 게임 실행의 실패 상태는 실제 촬영 후 감사 프로그램의 sorted-JSON-key-order 검증 오류. 원본 게임 로그와 PNG를 별도로 재파싱하여 증거만 수용.",
        "- 70 대상 37조건부/33HOLD -> 39조건부/31HOLD, 최종 승인 0. 원본 역사 F2 31/62 -> 33/62.",
        "- 미해결 31: 바닐라15, AF3, HC1, Macaw10, 위험R06/R08 2.",
        "- 실제 플레이어 상호작용, 픽셀 UV 인과, 부품 의미, AI 원본 이용권 및 INT4-G/H 최종 승인은 아직 보류.",
        "",
    ]).encode("utf-8")
    return {
        OUT/"INT4_F6_70_TARGET_EVIDENCE_DISPOSITIONS_V5.csv":data70,
        OUT/"INT4_F6_31_PENDING_EXACT_F2_TARGETS_V1.csv":data31,
        OUT/"INT4_F6_10_SOURCE_CONDITIONS_GAME_MATRIX_V1.csv":data10,
        OUT/"INT4_F6_70_INDEPENDENT_SOURCE_AUDIT_V1.json":jsonraw(report),
        OUT/"INT4_F6_SOURCE_REPLAY_REPORT_V1.md":markdown,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for target,data in build(a.artifact_dir/"original-f6.zip").items():
        path=ROOT/target
        if a.verify:
            assert path.read_bytes()==data,("OUTPUT_BYTES_NOT_DETERMINISTIC",str(target))
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        print("verified" if a.verify else "created",target,len(data))
    print("PASS 10 real F2 and 3 exact game-state trials, 2 original study cases, 70=39 conditional+31 HOLD")

if __name__=="__main__":main()
