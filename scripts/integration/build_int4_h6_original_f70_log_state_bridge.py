#!/usr/bin/env python3
"""INT-4-H6: 20 original ZIPs: client.log + capture JSON to 91 PNGs and 70 cases.

A verified game log's bytes, a capture JSON state flag, a native screenshot SHA,
and an exact renderer/UV causal contract are four DIFFERENT assertions.
Never infer one from another. No original game assets are committed.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,io,json,re
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PINS={
 "INT4_H3_20_ORIGINAL_ARTIFACT_ZIP_SHA_AUDIT_V1.csv":"430d39155c9b4287e8b5eb3deea55ac01e66f4e4",
 "INT4_H3_91_NATIVE_F2_ORIGINAL_PNG_SHA_AUDIT_V1.csv":"fb6632667be7405369933b962446dc076f380277",
 "INT4_H3_70_CASE_ORIGINAL_F2_REOPEN_V1.csv":"ded3b656337609152d222a661081933f71ef012a",
 "INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json":"e67f9c5f2ca4bac01f3e878811ed433f9713109b",
 "INT4_H5_EIGHT_REASSESSED_SCOPED_EXIT_GATES_V1.csv":"39e56986c7e590c7d7ba562900a618f44325fbb5",
 "INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json":"b4af9222fb3ba5e0713b7dd55bc890a3f01fb777",
 "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
}
OUT_ARCH=I/"INT4_H6_20_REAL_CLIENT_LOG_AND_CAPTURE_SOURCE_V1.csv"
OUT_PNG=I/"INT4_H6_91_F2_PNG_CAPTURE_SERVER_LOG_LINKS_V1.csv"
OUT_CASE=I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"
OUT_GATE=I/"INT4_H6_H03_H05_SCOPE_REASSESSMENT_V1.csv"
OUT_JSON=I/"INT4_H6_70_CASE_LOG_SOURCE_AUDIT_V1.json"
OUT_MD=I/"INT4_H6_H03_H05_SERVER_LOG_SCOPE_REPORT_V1.md"
CLIENT_LOG_SHA_KEYS={
    "client_log_sha256","original_client_log_sha256",
    "original_game_client_log_sha256","game_client_log_sha256",
    "original_game_log_sha256",
}
STATE_KEYS={"server_state_verified","server_blockstate_verified",
            "server_exact_state_verified","server_state_exact",
            "server_state_match","server_verified","server_source_state_verified"}

def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def original(name):
    b=(ROOT/I/name).read_bytes()
    assert gitblob(b)==PINS[name],("FROZEN_SOURCE_GIT_SHA_CHANGED",name)
    return b
def csvin(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def csvout(rows):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return f.getvalue().encode("utf-8")
def jout(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def save(path,b,verify):
    f=ROOT/path
    if verify:assert f.exists() and f.read_bytes()==b,("NONDETERMINISTIC_OUTPUT",str(path))
    else:
        f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
def module_h3():
    p=ROOT/"scripts/integration/build_int4_h3_f70_original_20_zip_91_png_audit.py"
    spec=importlib.util.spec_from_file_location("mcfr_h3_source",p)
    h3=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h3)
    assert h3.LEDGER_BLOB==PINS["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"]
    return h3

def log_pins(obj):
    found=set()
    def scan(o,depth=0):
        if depth>24:return
        if isinstance(o,dict):
            for k,v in o.items():
                if k in CLIENT_LOG_SHA_KEYS and isinstance(v,str) and re.fullmatch("[0-9a-f]{64}",v):
                    found.add(v)
                elif isinstance(v,(dict,list)):scan(v,depth+1)
        elif isinstance(o,list):
            for v in o:scan(v,depth+1)
    scan(obj)
    return found

def structured_exact(doc,case):
    if not isinstance(doc,dict):return []
    good=[]
    states=doc.get("server_states",{})
    if isinstance(states,dict) and isinstance(states.get(case),dict):
        x=states[case].get("subject")
        if isinstance(x,dict) and x.get("exact") is True:
            good.append("server_states."+case+".subject.exact")
    entries=doc.get("states",[])
    if isinstance(entries,list):
        for x in entries:
            if isinstance(x,dict) and x.get("case_id")==case and any(x.get(k) is True for k in STATE_KEYS):
                good.append("states[case_id="+case+"].server_verified")
    if doc.get("risk_id")==case:
        checks=doc.get("state_check_evidence")
        if isinstance(checks,list) and checks and all(isinstance(x,dict) and x.get("PASS") is True for x in checks):
            good.append("risk_state_check_evidence_all_PASS")
    # Original F6 stores exact historical property under named source-condition
    # trials, not as server_states[S02] and server_states[S34].
    f6_trials={
        "S02":[("S02_NORTH_TABLE_TUCK","tucked","true"),
               ("S02_NORTH_TOP_SLAB_TUCK","tucked","true")],
        "S34":[("S34_NORTH_WEST_INNER_LEFT","shape","inner_left")],
    }
    if case in f6_trials and isinstance(states,dict):
        for trial,property_name,expected in f6_trials[case]:
            row=states.get(trial,{})
            if (isinstance(row,dict) and
                isinstance(row.get("subject"),dict) and row["subject"].get("exact") is True and
                isinstance(row.get("actual"),dict) and row["actual"].get(property_name)==expected):
                good.append("F6_source_condition_trial="+trial+".subject.exact+actual_property")
    # V11 white bed uses two exact server parts (not cuboid elements).
    if (case=="V11" and doc.get("original_historical_case_id")=="V11" and
        doc.get("server_foot_exact") is True and doc.get("server_head_exact") is True):
        good.append("V11_bed_both_foot_head_server_exact")
    # R08 has two actual Fabric runs and each separate version records this
    # risk case explicitly. Do not infer compatibility beyond tested state.
    if (case=="R08" and doc.get("risk_case")=="R08" and
        doc.get("actual_server_original_state_PASS") is True):
        good.append("R08_single_release_original_server_state_PASS")
    return good

def png_filename_sha_in_capture(doc,png_path,pngsha):
    if not isinstance(doc,dict):return []
    names={png_path,Path(png_path).name}
    found=[]
    entries=doc.get("states",[])
    if isinstance(entries,list):
        for x in entries:
            if isinstance(x,dict) and x.get("screenshot_file") in names and x.get("screenshot_sha256")==pngsha:
                found.append("states[].screenshot_file+SHA")
    for k in ("native_f2_sha256","native_F2_sha256","f2_sha256","native_F2_png_sha256","f2_sha256_by_case"):
        m=doc.get(k)
        if isinstance(m,dict):
            for ident,v in m.items():
                if v==pngsha and (ident in names or ident+".png" in names or ident==Path(png_path).stem):
                    found.append(k+"["+str(ident)+"]")
    # The Macaw R03 neighbor experiment uses a 3-stage native_F2 dict,
    # not the generic states[] format. Match both original filename and SHA.
    seq=doc.get("native_F2")
    if isinstance(seq,dict):
        for stage,entry in seq.items():
            if (isinstance(entry,dict) and entry.get("file") in names and
                entry.get("sha256")==pngsha):
                found.append("native_F2["+str(stage)+"].file+SHA")
    return sorted(set(found))

def log_line_mentions(data,case):
    token=re.compile(r"(?<![A-Za-z0-9_])"+re.escape(case)+r"(?![A-Za-z0-9_])")
    mentions=[line for line in data.splitlines() if token.search(line)]
    exact=sum(bool(re.search(r"\b(exact|PASS|verified)\b",line,re.I)) for line in mentions)
    return len(mentions),exact

def audit(cache,verify=False):
    h3=module_h3()
    sources={n:original(n) for n in PINS}
    archives=csvin(sources["INT4_H3_20_ORIGINAL_ARTIFACT_ZIP_SHA_AUDIT_V1.csv"])
    images=csvin(sources["INT4_H3_91_NATIVE_F2_ORIGINAL_PNG_SHA_AUDIT_V1.csv"])
    cases=csvin(sources["INT4_H3_70_CASE_ORIGINAL_F2_REOPEN_V1.csv"])
    ledger=csvin(sources["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"])
    gates=csvin(sources["INT4_H5_EIGHT_REASSESSED_SCOPED_EXIT_GATES_V1.csv"])
    h3meta=json.loads(sources["INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"])
    h5meta=json.loads(sources["INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json"])
    assert (len(archives),len(images),len(cases),len(ledger),len(gates))==(20,91,70,70,8)
    assert set(x["target_id"] for x in cases)==set(x["target_id"] for x in ledger)
    assert len(set(x["target_id"] for x in cases))==70
    assert h3meta["all_91_native_F2_PNG_sha256_verified"] is True
    assert h5meta["H_all_eight_gates_fully_satisfied"] is False
    assert all(x["original_F_status"].startswith("CONDITIONAL") for x in cases)
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in ledger)
    meta={x["artifact_id"]:x for x in archives}
    assert len(meta)==20 and {x["artifact_id"] for x in images}==set(meta)
    for x in images:
        a=meta[x["artifact_id"]]
        assert (x["run_id"],x["recorded_zip_sha256"])==(
            a["original_run_id"],a["source_expected_original_zip_sha256"])
        assert x["expected_original_png_sha256"]==x["verified_original_png_sha256"]
    origins={id:{"artifact_id":id,"run_id":row["original_run_id"],
                "expected_zip_sha256":row["source_expected_original_zip_sha256"]}
             for id,row in meta.items()}
    collected={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(h3.download_artifact,a,cache):id for id,a in origins.items()}
        for fut in as_completed(futures):
            id=futures[fut];collected[id]=fut.result()
    assert len(collected)==20
    decoded={};audited=[]
    for id in sorted(meta,key=int):
        item=collected[id]
        assert item["archive_byte_sha256"]==meta[id]["source_expected_original_zip_sha256"]
        with ZipFile(io.BytesIO(item["original_blob"])) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert len(names)==len(set(names))
            logs={n:z.read(n) for n in names if n.lower().endswith(".log")}
            docs={}
            for n in names:
                if n.lower().endswith(".json"):
                    b=z.read(n)
                    if len(b)>2000000:continue
                    d=json.loads(b)
                    if isinstance(d,dict):docs[n]=d
        assert logs and all(len(b)>100 for b in logs.values()),("ORIGINAL_CLIENT_LOG_NOT_FOUND",id)
        hashes={n:sha(b) for n,b in logs.items()}
        pins=set().union(*(log_pins(x) for x in docs.values())) if docs else set()
        matched=pins.intersection(hashes.values())
        unmatched=pins.difference(hashes.values())
        decoded[id]={
            "docs":docs,
            "logs":{n:b.decode("utf-8",errors="replace") for n,b in logs.items()},
            "log_sha":hashes,
            "matched":matched,
            "unmatched":unmatched,
        }
        audited.append({
            "artifact_id":id,
            "original_run_id":meta[id]["original_run_id"],
            "original_zip_sha256":item["archive_byte_sha256"],
            "original_zip_crc_verified":"true",
            "original_client_log_count":len(logs),
            "original_client_log_sha256s":"|".join(sorted(hashes.values())),
            "capture_json_file_count":len(docs),
            "declared_full_client_log_SHA_count":len(pins),
            "declared_full_client_log_SHA_matches_original_bytes":len(matched),
            "declared_full_client_log_SHA_without_match":len(unmatched),
            "at_least_one_full_client_log_PIN_matches":"true" if matched else "false",
            "unconditional_F_approved":"false",
        })
    linked=[];percase=defaultdict(list)
    for r in images:
        id=r["artifact_id"];source=decoded[id]
        with ZipFile(io.BytesIO(collected[id]["original_blob"])) as z:
            actual=h3.find_member(z,r["original_real_zip_png_member"])
            b=z.read(actual)
        photo=r["original_recorded_png_path"]
        assert sha(b)==r["expected_original_png_sha256"]
        exact=[];image=[]
        for filename,d in source["docs"].items():
            exact.extend(filename+":"+s for s in structured_exact(d,r["target_id"]))
            image.extend(filename+":"+s for s in png_filename_sha_in_capture(
                d,photo,r["expected_original_png_sha256"]))
        mentions=0;logexact=0
        for log in source["logs"].values():
            a,c=log_line_mentions(log,r["target_id"])
            mentions+=a;logexact+=c
        record={
            "target_id":r["target_id"],"target_kind":r["target_kind"],
            "artifact_id":id,"run_id":r["run_id"],
            "native_F2_member":actual,"verified_native_F2_sha256":sha(b),
            "original_client_log_count":len(source["logs"]),
            "whole_client_log_sha_declared_and_matches":"true" if source["matched"] else "false",
            "case_specific_structured_server_exact":"true" if exact else "false",
            "case_specific_json_evidence":"|".join(sorted(set(exact))),
            "capture_json_direct_png_filename_and_sha":"true" if image else "false",
            "png_json_evidence":"|".join(sorted(set(image))),
            "client_log_case_id_mentioned_lines":mentions,
            "client_log_case_id_and_exact_words_same_line":logexact,
            "case_client_log_correlated_to_same_F2_frame":"false",
            "manual_qualitative_visual_or_UV_reapproved":"false",
            "full_F_exit_approved":"false",
        }
        linked.append(record);percase[r["target_id"]].append(record)
    assert len(linked)==91 and len(percase)==70
    result=[]
    for row in cases:
        id=row["target_id"];group=percase[id]
        strong=any(x["case_specific_structured_server_exact"]=="true" for x in group)
        full=any(x["whole_client_log_sha_declared_and_matches"]=="true" for x in group)
        picture=any(x["capture_json_direct_png_filename_and_sha"]=="true" for x in group)
        logid=sum(int(x["client_log_case_id_mentioned_lines"]) for x in group)
        logexact=sum(int(x["client_log_case_id_and_exact_words_same_line"]) for x in group)
        if strong and full and picture and logexact:
            quality="SERVER_JSON_LOG_SHA_IMAGE_SHA_AND_CASE_LINE_BUT_FRAME_CAUSAL_OPEN"
        elif strong and full and picture:
            quality="SERVER_JSON_LOG_SHA_AND_IMAGE_SHA_BUT_NO_CASE_LINE"
        elif strong and full:
            quality="SERVER_JSON_AND_LOG_SHA_NO_DIRECT_IMAGE_JOIN"
        elif strong:
            quality="SERVER_JSON_ONLY_WITHOUT_FULL_LOG_SHA_JOIN"
        elif full:
            quality="ORIGINAL_LOG_SHA_BUT_NO_CASE_SPECIFIC_SERVER_EXACT"
        else:
            quality="ORIGINAL_LOG_AND_NATIVE_F2_BUT_CASE_STATE_TRACE_OPEN"
        result.append({
            "target_id":id,"target_kind":row["target_kind"],
            "original_native_F2_occurrences":row["reopened_original_PNG_occurrences"],
            "original_F70_disposition":row["original_F_status"],
            "artifact_ids":"|".join(sorted({x["artifact_id"] for x in group},key=int)),
            "ZIP_CRC_and_all_PNG_SHA_verified":"true",
            "all_source_artifacts_have_original_logs":"true",
            "whole_client_log_sha_matched_capture_report":"true" if full else "false",
            "has_case_specific_structured_server_exact":"true" if strong else "false",
            "has_capture_record_exact_image_name_and_sha":"true" if picture else "false",
            "explicit_case_id_log_lines":logid,
            "explicit_case_id_and_exact_same_log_lines":logexact,
            "source_evidence_quality":quality,
            "full_frame_log_state_causality_reapproved":"false",
            "fresh_human_game_scene_UV_review_performed":"false",
            "full_F_exit_approved":"false",
        })
    assert len(result)==70 and set(x["target_id"] for x in result)==set(percase)
    changed=[];review=[]
    for row in gates:
        r=dict(row)
        if r["gate_id"]=="H05":
            assert r["review_status"].startswith("CONDITIONAL")
            r["review_status"]="CONDITIONAL_ARCHIVED_LOG_AND_CAPTURE_JSON_SOURCE_JOIN_FRAME_CAUSAL_OPEN"
            r["evidence_scope"]="H3 original 20 ZIP/91 PNG SHA+CRC; H6 reopened 20 ZIP client.log bytes and source capture JSON, mapped 70 targets and 91 image references while preserving frame/UV limits"
            r["evidence_key"]="H6_20_ORIGINAL_ARCHIVED_LOGS_CASE70_F2PNG91"
            r["remaining_condition"]="PER_FRAME_ORIGINAL_SERVER_LOG_STATE_AND_HUMAN_SCENE_UV_REVIEW_STILL_REQUIRED"
            changed.append("H05")
        else:
            assert r["gate_id"]!="H03" or r["review_status"]=="HOLD_FULL_F_EXIT"
        r["full_unconditional_exit_satisfied"]="false"
        review.append(r)
    assert changed==["H05"]
    assert Counter(x["review_status"].split("_")[0] for x in review)=={
        "PASS":6,"CONDITIONAL":1,"HOLD":1}
    counts={
        "original_archives":20,
        "original_client_logs":sum(int(r["original_client_log_count"]) for r in audited),
        "archives_with_capture_json":sum(int(r["capture_json_file_count"])>0 for r in audited),
        "archives_with_matching_pinned_client_log":sum(r["at_least_one_full_client_log_PIN_matches"]=="true" for r in audited),
        "archives_with_unmatched_reported_whole_log_SHA":sum(int(r["declared_full_client_log_SHA_without_match"])>0 for r in audited),
        "original_PNG_occurrences":91,
        "original_target_cases":70,
        "cases_with_source_server_exact_metadata":sum(x["has_case_specific_structured_server_exact"]=="true" for x in result),
        "cases_with_reopened_log_sha_matched_report":sum(x["whole_client_log_sha_matched_capture_report"]=="true" for x in result),
        "cases_with_capture_image_filename_sha_match":sum(x["has_capture_record_exact_image_name_and_sha"]=="true" for x in result),
        "cases_with_exact_case_id_in_log":sum(int(x["explicit_case_id_log_lines"])>0 for x in result),
        "cases_with_same_line_case_id_and_exact":sum(int(x["explicit_case_id_and_exact_same_log_lines"])>0 for x in result),
        "new_full_frame_causality_approvals":0,
        "new_manual_per_case_scene_UV_approvals":0,
        "full_F_unconditional_approvals":0,
        "H_scoped_pass":6,"H_conditional":1,"H_hold":1,"H_full_exit_approvals":0,
        "INT5_part_semantics_approved":0,"INT6_training_and_redistribution_rights_approved":0,
    }
    assert counts["original_client_logs"]>=20
    assert 0<=counts["cases_with_source_server_exact_metadata"]<=70
    assert 0<=counts["cases_with_same_line_case_id_and_exact"]<=70
    summary={
        "schema":"MCFR_INT4_H6_20_ORIGINAL_GAME_LOGS_CASE70_NATIVE_F2_SOURCE_BRIDGE/v1",
        "status":"PASS_H6_SOURCE_LOG_TRACEABILITY_H05_CONDITIONAL_H03_HOLD_FULL_EXIT_ZERO",
        "source_original_git_blobs":PINS,
        "counts":counts,
        "per_case_evidence_quality":dict(sorted(Counter(x["source_evidence_quality"] for x in result).items())),
        "unmatched_original_report_whole_log_SHA":{
            id:sorted(d["unmatched"]) for id,d in sorted(decoded.items(),key=lambda p:int(p[0])) if d["unmatched"]
        },
        "F70_original_dispositions_unchanged":True,
        "other_seven_H_gates_unchanged":True,
        "limitations":[
            "Capturing a case JSON boolean and checking the original log SHA do not prove exact frame-to-server-state causality.",
            "A game client screenshot log line documents capture, not necessarily a unique case state.",
            "Shared risk-case screenshots do not prove independent re-execution, especially R02/R05/R07.",
            "No original client log, PNG, ZIP, Minecraft asset or mod JAR is committed.",
            "Game UV per-face pixel mapping, dynamic Java behavior, human scene interpretation, rights and final exit remain unapproved.",
        ],
    }
    doc="\n".join([
        "# INT-4-H6 원본 실게임 로그·캡처 JSON·F2 연결 독립 감사",
        "",
        f"- 실제 원본 ZIP **20개**, 원본 client.log **{counts['original_client_logs']}개** 재열람. ZIP CRC와 원본 SHA는 H3 증거 대조.",
        f"- 원본 캡처 JSON이 있는 아카이브 **{counts['archives_with_capture_json']}/20**.",
        f"- 캡처 JSON에 기록된 전체 client.log SHA와 실제 바이트 일치 아카이브 **{counts['archives_with_matching_pinned_client_log']}/20**.",
        f"- 사례별 원본 서버 정확 상태 JSON 메타데이터 발견 **{counts['cases_with_source_server_exact_metadata']}/70**.",
        f"- 원본 캡처 JSON에서 PNG 파일명+SHA 동시 연결 **{counts['cases_with_capture_image_filename_sha_match']}/70**.",
        f"- 실제 로그에 사례 ID 언급 **{counts['cases_with_exact_case_id_in_log']}/70**; 같은 로그 줄에 exact 표시 **{counts['cases_with_same_line_case_id_and_exact']}/70**.",
        "- **H03 HOLD**, **H05 CONDITIONAL** 유지. 검수용 8개 게이트에서 6개 범위 통과, 조건부1, 보류1, 최종 승인0.",
        "- 원본 F70 70개 모두 조건부이며 실화면/시간/블록상태 인과와 UV·버전 계약은 무조건 승인하지 않음.",
        "- 이번 재검수는 기존 게임 실행이 남긴 메타데이터와 실제 로그 바이트의 출처 검증으로, 새로운 Minecraft 게임 실행이나 새 사람 시각 판독이 아님.",
        "- GitHub 원본 문서·main/기존 PR 불변, 원본 게임 파일 미커밋, INT5 의미/INT6 원본 학습·재배포 권한 승인 0.",
        "",
    ]).encode("utf-8")
    blobs={OUT_ARCH:csvout(audited),OUT_PNG:csvout(linked),
           OUT_CASE:csvout(result),OUT_GATE:csvout(review),
           OUT_MD:doc}
    summary["outputs"]={str(p):{"sha256":sha(b),"rows":20 if p==OUT_ARCH else 91 if p==OUT_PNG else 70 if p==OUT_CASE else 8 if p==OUT_GATE else None} for p,b in blobs.items()}
    blobs[OUT_JSON]=jout(summary)
    for p,b in blobs.items():save(p,b,verify)
    print(json.dumps({"status":summary["status"],"counts":counts,"case_quality":summary["per_case_evidence_quality"]},ensure_ascii=False))
    return summary

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--cache",type=Path,default=Path("tmp-h6-original-actions"))
    a.add_argument("--verify",action="store_true")
    x=a.parse_args();audit(x.cache,x.verify)
if __name__=="__main__":main()
