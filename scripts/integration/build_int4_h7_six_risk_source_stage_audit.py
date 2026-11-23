#!/usr/bin/env python3
"""H7: re-open six pinned risk archives and map 21 original substage F2 proofs.

Original Rxx is a risk contract, not a game blockstate case_id. A passed
source stage is NOT a completed risk contract, pixel causality or rights.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,io,json
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PIN={
 "INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv":"f820efd9e85c4cee8df4673a2db4f4d868b4de31",
 "INT4_H6_91_F2_PNG_CAPTURE_SERVER_LOG_LINKS_V1.csv":"90631f3c1963df073019426791953d1790f726d2",
 "INT4_H6_20_REAL_CLIENT_LOG_AND_CAPTURE_SOURCE_V1.csv":"c52de2d71bd73ff21a1d801a79e9aea99532be92",
 "INT4_H6_H03_H05_SCOPE_REASSESSMENT_V1.csv":"7994c9a9eb71dd01e8ca8a695035f7d52c9b3098",
 "INT4_H6_70_CASE_LOG_SOURCE_AUDIT_V1.json":"9a63e0058ccd3344560c4283fbd0551e718feb11",
 "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
}
RISK=("R01","R02","R03","R04","R05","R07")
STAGES={
 "R01":("S10",),
 "R02":("AFV3_north","AFV3_east","AFV3_south","AFV3_west","AFV1_north","AFV1_south"),
 "R03":("reset","join","remove"),
 "R04":("S42","S43"),
 "R05":("bed_placed","bed_sleeping","bed_awake","bed_placed","bed_foot_broken"),
 "R07":("AFV3_north","AFV3_east","AFV3_south","AFV3_west"),
}
ART={
 "R01":("14747628657",),"R02":("14709514487",),
 "R03":("14739219085",),"R04":("14713339690",),
 "R05":("14739601203","14740560536"),"R07":("14709514487",),
}
DOC={
 "R01":"manifest.json","R02":"INT4_AF_VARIANT3_REAL_F2_CAPTURE.json",
 "R03":"INT4_MACAW_TABLE_NEIGHBOR_ACTUAL_GAME.json",
 "R04":"INT4_MACAW_KITCHEN_REAL_F2_CAPTURE.json",
 "R05":"manifest.json","R07":"INT4_AF_VARIANT3_REAL_F2_CAPTURE.json",
}
OUTS=I/"INT4_H7_21_RISK_SUBSTAGE_SOURCE_VERIFIED_V1.csv"
OUTR=I/"INT4_H7_6_RISK_CONTRACT_GAP_MATRIX_V1.csv"
OUTG=I/"INT4_H7_H03_H05_SOURCE_RECHECK_V1.csv"
OUTJ=I/"INT4_H7_SIX_RISK_SOURCE_STAGE_AUDIT_V1.json"
OUTM=I/"INT4_H7_SIX_RISK_STAGE_RESEARCH_REPORT_V1.md"
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def fixed(n):
    b=(ROOT/I/n).read_bytes()
    assert blob(b)==PIN[n],("ORIGINAL_BLOB_SHA_MISMATCH",n)
    return b
def rows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def csvbytes(rs):
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=list(rs[0]),lineterminator="\n")
    w.writeheader();w.writerows(rs)
    return out.getvalue().encode("utf-8")
def jsonbytes(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
def saveto(path,data,verify):
    p=ROOT/path
    if verify:assert p.is_file() and p.read_bytes()==data,("NONDETERMINISTIC",str(path))
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)
    return x
def prove(case,stage,doc,run2):
    if case=="R01":
        assert doc["server_states"]["S10"]["subject"]["exact"] is True
        return "S10_SUBJECT_EXACT_TRUE"
    if case in ("R02","R07"):
        x=next(r for r in doc["states"] if r["case_id"]==stage)
        assert x["server_blockstate_verified"] is True
        facing=stage.split("_")[1]
        v=3 if stage.startswith("AFV3") else 1
        assert "facing="+facing in x["original_state"] and "variant="+str(v) in x["original_state"]
        leaf="acacia_1" if facing=="south" or v==1 else "acacia_3"
        assert x["original_model_target"].endswith("chair/"+leaf)
        assert x["source_version_equivalence"]=="RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE"
        return "AF_"+stage+"_SELECTS_"+leaf.upper()
    if case=="R03":
        states=doc["observed_server_states"]
        t=doc["transitions"]
        assert t["joined_bidirectionally"] is True
        assert t["automatically_disconnected_after_remove"] is True
        assert t["player_item_placement_tested"] is False
        centre=states[stage]["centre"];east=states[stage]["east"]
        assert centre["block"]=="table"
        if stage=="join":
            assert centre["east"] is True and east["block"]=="table" and east["west"] is True
        else:assert centre["east"] is False and east["block"]=="air"
        return "NATURAL_SETBLOCK_NEIGHBOR_"+stage.upper()
    if case=="R04":
        x=next(r for r in doc["states"] if r["case_id"]==stage)
        assert x["server_blockstate_verified"] is True
        assert x["block_id"]=="mcwfurnitures:oak_kitchen_sink"
        assert ("water=true" if stage=="S43" else "water=false") in x["original_state"]
        return "SINK_"+stage+"_STATIC_WATER_SERVER_VERIFIED"
    if case=="R05":
        st=doc["server_states"][stage]
        for key in ("foot_position","head_position"):
            val=st[key]
            if stage=="bed_foot_broken":assert val["block"]=="air"
            else:
                assert val["block"]=="present"
                assert val["occupied"]==("true" if stage=="bed_sleeping" else "false")
                assert val["facing"]=="north"
        if run2:assert stage in ("bed_placed","bed_foot_broken")
        else:
            assert doc["interaction"] is True
            assert doc["sleep_timers"]["check_bed_sleeping"]=="positive"
            assert doc["sleep_timers"]["check_bed_awake"]=="zero"
        return "BED_"+stage.upper()+"_TWO_PARTS_SERVER_VERIFIED"
    raise AssertionError(("UNKNOWN_RISK",case,stage))
def audit(cache,verify=False):
    h3=mod("h7_h3","scripts/integration/build_int4_h3_f70_original_20_zip_91_png_audit.py")
    h6=mod("h7_h6","scripts/integration/build_int4_h6_original_f70_log_state_bridge.py")
    original={k:fixed(k) for k in PIN}
    c70=rows(original["INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"])
    p91=rows(original["INT4_H6_91_F2_PNG_CAPTURE_SERVER_LOG_LINKS_V1.csv"])
    a20=rows(original["INT4_H6_20_REAL_CLIENT_LOG_AND_CAPTURE_SOURCE_V1.csv"])
    gates=rows(original["INT4_H6_H03_H05_SCOPE_REASSESSMENT_V1.csv"])
    f70=rows(original["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"])
    h6data=json.loads(original["INT4_H6_70_CASE_LOG_SOURCE_AUDIT_V1.json"])
    assert (len(c70),len(p91),len(a20),len(gates),len(f70))==(70,91,20,8,70)
    assert h6data["counts"]["cases_with_source_server_exact_metadata"]==64
    assert h6data["counts"]["cases_with_capture_image_filename_sha_match"]==70
    assert set(RISK)=={x["target_id"] for x in c70 if x["has_case_specific_structured_server_exact"]=="false"}
    bycase=defaultdict(list)
    for x in p91:
        if x["target_id"] in RISK:bycase[x["target_id"]].append(x)
    assert {k:len(v) for k,v in bycase.items()}=={k:len(v) for k,v in STAGES.items()}
    assert sum(len(v) for v in bycase.values())==21
    ameta={x["artifact_id"]:x for x in a20}
    aid={a for arr in ART.values() for a in arr}
    assert len(aid)==6
    args={a:{"artifact_id":a,"expected_zip_sha256":ameta[a]["original_zip_sha256"],"run_id":ameta[a]["original_run_id"]} for a in aid}
    archive={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        fut={pool.submit(h3.download_artifact,v,cache):a for a,v in args.items()}
        for job in as_completed(fut):archive[fut[job]]=job.result()
    assert len(archive)==6
    docs={}
    for a in aid:
        x=archive[a]
        assert x["archive_byte_sha256"]==ameta[a]["original_zip_sha256"]
        with ZipFile(io.BytesIO(x["original_blob"])) as z:
            assert z.testzip() is None
            assert "client.log" in z.namelist()
            log=z.read("client.log")
            d={p:json.loads(z.read(p)) for p in z.namelist() if p.endswith(".json")}
        assert sha(log) in ameta[a]["original_client_log_sha256s"].split("|")
        assert sha(log) in set().union(*(h6.log_pins(q) for q in d.values()))
        docs[a]=(d,sha(log))
    stageout=[];caseres={}
    for case in RISK:
        entries=bycase[case]
        assertions=[]
        for index,(x,name) in enumerate(zip(entries,STAGES[case])):
            a=x["artifact_id"]
            assert a in ART[case]
            if case=="R05":assert a==("14739601203" if index<3 else "14740560536")
            else:assert a==ART[case][0]
            assert Path(x["native_F2_member"]).stem==name
            d,log_sha=docs[a]
            doc=d[DOC[case]]
            assert doc["client_log_sha256"]==log_sha
            sourceproof=prove(case,name,doc,case=="R05" and index>=3)
            with ZipFile(io.BytesIO(archive[a]["original_blob"])) as z:
                member=h3.find_member(z,x["native_F2_member"])
                data=z.read(member)
            assert sha(data)==x["verified_native_F2_sha256"]
            with Image.open(io.BytesIO(data)) as im:
                im.load();assert im.format=="PNG" and im.size==(1024,684)
            assert x["capture_json_direct_png_filename_and_sha"]=="true"
            if case in ("R02","R07","R04"):
                state=next(t for t in doc["states"] if t["case_id"]==name)
                assert state["screenshot_file"]==member
                assert state["screenshot_sha256"]==sha(data)
            elif case=="R03":
                assert doc["native_F2"][name]["file"]==member
                assert doc["native_F2"][name]["sha256"]==sha(data)
            else:assert doc["native_f2_sha256"][name]==sha(data)
            stageout.append({
                "risk_id":case,"source_stage":name,"archive_id":a,"original_run_id":x["run_id"],
                "original_zip_sha256":archive[a]["archive_byte_sha256"],
                "source_PNG_member":member,"source_PNG_sha256":sha(data),
                "capture_json":DOC[case],"original_client_log_sha256":log_sha,
                "archived_real_server_state_proof":sourceproof,
                "source_stage_state_verified":"true",
                "new_independent_game_run":"false",
                "full_risk_contract_approved":"false",
                "pixel_UV_causal_approved":"false",
            })
            assertions.append(sourceproof)
        caseres[case]={
            "source_substage_count":len(assertions),
            "actual_original_game_run_count":len(set(x["run_id"] for x in entries)),
            "archived_server_substage_verified":len(assertions),
            "source_state_evidence_keys":assertions,
            "full_risk_contract_approved":False,
        }
    assert len(stageout)==21
    assert caseres["R05"]["actual_original_game_run_count"]==2
    a={x["source_PNG_sha256"] for x in stageout if x["risk_id"]=="R02" and x["source_stage"].startswith("AFV3")}
    b={x["source_PNG_sha256"] for x in stageout if x["risk_id"]=="R07"}
    assert a==b and len(a)==4
    exceptions={
        "R01":"Only source S10 reused; entire furniture category not re-executed",
        "R02":"Six direction/variant states; release-study byte differences and pixel causality open",
        "R03":"Natural setblock neighbor transition, not player item placement",
        "R04":"Two static sink states, not water animation or interaction proof",
        "R05":"Sleep/wake and destruction come from TWO distinct original game runs",
        "R07":"South variant3 selects acacia_1 while other variant3 directions select acacia_3; intent unresolved",
    }
    riskrows=[{
        "risk_id":k,
        "original_F2_stage_occurrences":len(STAGES[k]),
        "distinct_original_game_runs":caseres[k]["actual_original_game_run_count"],
        "exact_source_server_substages":caseres[k]["archived_server_substage_verified"],
        "stage_names":"|".join(STAGES[k]),
        "source_stage_SHA_and_log_verified":"true",
        "risk_contract_final_approved":"false",
        "remaining_condition":exceptions[k],
    } for k in RISK]
    gout=[]
    for row in gates:
        r=dict(row)
        if r["gate_id"]=="H05":
            assert r["review_status"].startswith("CONDITIONAL")
            r["review_status"]="CONDITIONAL_H7_SIX_RISK_SOURCE_SUBSTAGES_VERIFIED_FRAME_CAUSAL_OPEN"
            r["evidence_scope"]="H7 six original ZIPs, 21 reused source image references, real staged server records, no new game execution"
            r["evidence_key"]="H7_6_RISK_CONTRACTS_21_ORIGINAL_SERVER_SUBSTAGES"
            r["remaining_condition"]="PER_FRAME_SERVER_LOG_RENDER_UV_AND_COMPLETE_RISK_CONTRACT_STILL_UNPROVEN"
        else:assert r["gate_id"]!="H03" or r["review_status"]=="HOLD_FULL_F_EXIT"
        r["full_unconditional_exit_satisfied"]="false"
        gout.append(r)
    assert Counter(x["review_status"].split("_")[0] for x in gout)=={"PASS":6,"CONDITIONAL":1,"HOLD":1}
    outs={OUTS:csvbytes(stageout),OUTR:csvbytes(riskrows),OUTG:csvbytes(gout)}
    report={
        "schema":"MCFR_INT4_H7_SIX_RISK_21_ORIGINAL_SUBSTAGES/v1",
        "status":"PASS_SIX_RISK_SOURCE_STAGES_NO_FINAL_H03_H05_EXIT",
        "source_original_git_blob_sha1":PIN,
        "risk_cases":caseres,
        "counts":{
            "risk_ids":6,"source_archives":6,"source_stage_PNG_occurrences":21,
            "source_server_state_substages_verified":21,"risk_contracts_completed":0,
            "new_game_runs":0,"F70_conditional":70,"F_final_unconditional":0,
            "H_scoped_pass":6,"H_conditional":1,"H_hold":1,"H_full_exit":0,
            "INT5_part_roles":0,"INT6_training_redistribution_rights":0,
        },
        "limitations":[
            "Risk Rxx is NOT an original blockstate key; use exact source substage aliases instead.",
            "R02 and R07 share four original screenshots, not independent game executions.",
            "R05 interaction and destruction run separately. Do not combine into one gameplay session.",
            "R03 setblock neighbor updates are not tested player item placement.",
            "R04 static water states do not prove animations, flow or dynamic physics.",
            "R07 source release mismatch and author intent cannot be inferred from image matching.",
            "No screenshot pixel-to-face UV causal approval; all source ZIP, PNG, log, JAR remain outside Git.",
            "Original F70 and H6 classifications unchanged; G/H full acceptance, INT5/INT6 rights unapproved."
        ],
    }
    md="\n".join([
        "# INT-4-H7 6개 위험 시나리오 원본 게임 단계별 재감사","",
        "- 실제 원본 Actions ZIP 6개 및 재사용 원본 F2 21건의 SHA/CRC·client.log·원본 캡처 JSON을 재열람.",
        "- **R01** S10 단일 사례 정확 서버상태 재확인. 동일 범주 전체 일반화 불가.",
        "- **R02** AF 의자 variant3 4방향 + variant1 2개 대조. 원본 선택 모델/릴리스 차이 확인; UV 인과 미확정.",
        "- **R03** Macaw 테이블 reset→join→remove의 연결 true/false 자동 갱신 확인. 플레이어 아이템 설치는 미시험.",
        "- **R04** Macaw 싱크 water=false/true 정적 두 상태 확인. 애니메이션 미입증.",
        "- **R05** 침대 설치·수면 occupied=true·기상 occupied=false, 별도 게임 실행에서 침대 두 부분 파괴 후 air 확인. 단일 연속 실행 아님.",
        "- **R07** AF variant3 남향이 acacia_1 모델을 선택하고 나머지 세 방향은 acacia_3 선택. R02와 같은 F2 재사용, 버그·의도 판정 보류.",
        "- 기존 70/70 조건부, H03 HOLD·H05 CONDITIONAL, H 범위 통과6/조건부1/보류1, 무조건 종료0 유지.",
        "- 이번 작업은 새 게임 재실행이 아니라 원본 아티팩트의 독립 단계별 증거 교차검증. UV·동적 기능·부품 의미·학습/재배포권 미승인.",
        ""
    ]).encode("utf-8")
    outs[OUTM]=md
    report["outputs"]={str(k):{"sha256":sha(v),"rows":21 if k==OUTS else 6 if k==OUTR else 8 if k==OUTG else None} for k,v in outs.items()}
    outs[OUTJ]=jsonbytes(report)
    for p,b in outs.items():saveto(p,b,verify)
    print(json.dumps({"status":report["status"],"counts":report["counts"]},ensure_ascii=False))
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cache",type=Path,default=Path("tmp-int4-h7-risk-zips"))
    p.add_argument("--verify",action="store_true")
    a=p.parse_args();audit(a.cache,a.verify)
if __name__=="__main__":main()
