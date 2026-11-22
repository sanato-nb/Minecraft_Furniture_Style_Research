#!/usr/bin/env python3
"""INT-4-F9 independent 5 native Macaw F2/SHA/client-log and 70-target audit.

Source: original 1-5 application rows, original pinned Macaw JAR release SHA,
F8 70-case ledger, actual five-source game report, GitHub Actions archived
original client screenshots. Fail closed on any drift; only S08/09/11/12/23
may change. Conditional SOURCE+F2 != final UV, semantics, functionality, rights.
"""
import argparse,csv,hashlib,io,json,os,urllib.request,urllib.error
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PREVIOUS=I/"INT4_F8_70_TARGET_EVIDENCE_DISPOSITIONS_V7.csv"
F8=I/"INT4_F8_S22_OFFICIAL_PARENT_INDEPENDENT_AUDIT_V1.json"
F9=I/"INT4_F9_MACAW_FIVE_ACTUAL_F2_SOURCE_V1.json"
SOURCE=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={
 str(PREVIOUS):"3d994185cb56f11980cc037854bbc62d6262ac11",
 str(F8):"5cf6d293675444c894053c9ec1c664fa36893a53",
 str(F9):"39a02df9723fdba35e131e854cb55515924793cd",
 str(SOURCE):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
RUN=45035905411
ARTIFACT=14759742774
ZIP_NAME="INT4_F9_MACAW_FIVE_ORIGINAL_CLIENT_F2.zip"
ZIP_SHA256="495378b596adb3d99105f45d01613d6366afe19efee9c802913db570a7a0bcb0"
MACAW_JAR="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
ORIGINAL_STUDY_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
CASES=("S08","S09","S11","S12","S23")
EXPECTED_FACES={"S08":59,"S09":31,"S11":52,"S12":11,"S23":26}
EXPECTED_ELEMENTS={"S08":12,"S09":6,"S11":14,"S12":2,"S23":5}
OBS={
 "S08":"원본 F2에서 등받이와 좌판을 갖춘 작은 나무 의자 확인.",
 "S09":"원본 F2에서 등받이 없는 낮은 목재 스툴형 물체 확인.",
 "S11":"원본 F2에서 상판 아래 받침 구조가 있는 작은 목재 엔드 테이블 확인.",
 "S12":"원본 F2에서 비교적 낮은 목제 상판과 아래 기둥이 보이는 커피 테이블 확인.",
 "S23":"원본 F2에서 수직 목재 무늬의 수납형 블록 외형 확인. 실제 서랍 기능은 별도 미검증.",
}
OUT70=I/"INT4_F9_70_TARGET_EVIDENCE_DISPOSITIONS_V8.csv"
OUT22=I/"INT4_F9_22_PENDING_EXACT_F2_TARGETS_V1.csv"
SUMMARY=I/"INT4_F9_FIVE_MACAW_NATIVE_F2_INDEPENDENT_AUDIT_V1.json"
REPORT=I/"INT4_F9_MACAW_FIVE_DIRECT_VISUAL_AUDIT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def locked(path):
    b=(ROOT/path).read_bytes()
    assert blob(b)==PINS[str(path)],("ORIGINAL_GIT_BLOB_CHANGED",str(path),blob(b))
    return b
def rows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def csvout(data,columns):
    s=io.StringIO(newline="")
    writer=csv.DictWriter(s,fieldnames=columns,lineterminator="\n")
    writer.writeheader();writer.writerows(data)
    return s.getvalue().encode()
def jsonout(d):
    return (json.dumps(d,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode()

def download_original(path):
    if path.is_file():return path.read_bytes()
    token=os.environ.get("GH_TOKEN")
    if not token:raise FileNotFoundError("Original F9 GitHub Actions ZIP missing")
    url=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
    headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
             "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-INT4-F9-native-audit"}
    class RejectRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    try:
        with urllib.request.build_opener(RejectRedirect).open(
            urllib.request.Request(url,headers=headers),timeout=120) as result:
            b=result.read()
    except urllib.error.HTTPError as exc:
        if exc.code not in (301,302,303,307,308):raise
        target=exc.headers.get("Location","")
        u=urlsplit(target)
        assert u.scheme=="https" and u.netloc and u.netloc!="api.github.com"
        with urllib.request.urlopen(
            urllib.request.Request(target,headers={"User-Agent":"MCFR-INT4-F9-native-audit"}),
            timeout=120) as response:
            b=response.read()
    assert sha(b)==ZIP_SHA256,("ORIGINAL_ZIP_SHA_CHANGED",sha(b))
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    return b

def build(zip_path):
    earlier=rows(locked(PREVIOUS))
    checkpoint=json.loads(locked(F8))
    report=json.loads(locked(F9))
    study=locked(SOURCE)
    assert sha(study)==ORIGINAL_STUDY_SHA
    assert len(earlier)==70 and len({r["target_id"] for r in earlier})==70
    assert (sum(r["final_disposition"].startswith("CONDITIONAL") for r in earlier),
            sum(r["final_disposition"].startswith("HOLD") for r in earlier))==(43,27)
    assert checkpoint["counts"]["conditional_after"]==43
    assert checkpoint["counts"]["HOLD_after"]==27
    assert checkpoint["counts"]["F_full_unconditional_approval"]==0
    assert report["status"]=="PASS_FIVE_SOURCE_SELECTED_ACTUAL_NATIVE_F2_NOT_SEMANTIC_EXIT"
    assert report["minecraft"]=="1.21.11"
    assert report["case_ids"]==list(CASES)
    assert (report["historical_elements"],report["historical_faces"])==(39,179)
    assert (report["server_exact_states"],report["actual_native_F2"])==(5,5)
    assert report["actual_mod_jar_SHA256"]==MACAW_JAR
    assert report["historical_source_SHA256"]==ORIGINAL_STUDY_SHA
    assert report["human_visual_review"]=="PENDING_ORIGINAL_NATIVE_F2_INDEPENDENT_REOPEN"
    assert report["f_full_approval"]==report["int5_semantic_approval"]==report["int6_rights_approval"]==0
    original_rows={k:[r for r in rows(study) if r["case"]==k] for k in CASES}
    assert all(len(v)==1 for v in original_rows.values())
    assert all(r["final_disposition"].startswith("HOLD") for r in earlier if r["target_id"] in CASES)
    data=download_original(zip_path)
    assert sha(data)==ZIP_SHA256
    checked={}
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        assert set(names)=={
          "INT4_F9_MACAW_FIVE_F2_AUDIT.json",
          "INT4_F9_MACAW_FIVE_REAL_F2_CAPTURE.json",
          "INT4_F9_MACAW_FIVE_F2_CONTACT.png",
          "client.log",
          *(k+".png" for k in CASES)}
        m=json.loads(z.read("INT4_F9_MACAW_FIVE_REAL_F2_CAPTURE.json"))
        a=json.loads(z.read("INT4_F9_MACAW_FIVE_F2_AUDIT.json"))
        assert m["minecraft_version"]=="1.21.11"
        assert m["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        assert m["source_state_verified_count"]==m["minecraft_native_f2_screenshot_count"]==5
        assert a["status"]=="PASS_FIVE_ORIGINAL_MACAW_F9_NATIVE_F2_AND_EXACT_SERVER_STATE_NOT_FINAL"
        assert a["source_cases"]==list(CASES)
        assert a["native_f2_count"]==a["server_verified_states"]==5
        assert a["source_1_5_face_counts"]==EXPECTED_FACES
        assert m["original_source_registry"]["mod_jar_sha256"]==MACAW_JAR
        assert m["original_source_registry"]["historical_application_sha256"]==ORIGINAL_STUDY_SHA
        assert a["original_source_sha256"]==ORIGINAL_STUDY_SHA
        assert sha(z.read("client.log"))==m["client_log_sha256"]==report["client_log_sha256"]
        assert sha(z.read("INT4_F9_MACAW_FIVE_REAL_F2_CAPTURE.json"))==a["f2_manifest_sha256"]
        assert sha(z.read("INT4_F9_MACAW_FIVE_F2_CONTACT.png"))==a["contact_sheet_sha256"]
        b=a["boundaries"]
        assert b["explicit_setblock_source_states_verified"] is True
        assert b["natural_connected_block_update_rules_tested"] is False
        assert b["face_uv_render_pixel_causality_proven"] is False
        assert b["int5_part_roles_approved"]==b["int6_training_or_redistribution_rights_approved"]==0
        assert report["boundaries"]==b
        entries={r["case_id"]:r for r in m["states"]}
        assert len(m["states"])==5 and set(entries)==set(CASES)
        client=z.read("client.log").decode("utf-8",errors="replace")
        for case in CASES:
            row=original_rows[case][0]
            record=entries[case]
            source=m["original_source_registry"]["states"][case]
            state=row["block"]+("["+row["state"].replace(";",",")+"]" if row["state"] else "")
            assert row["cohort"]=="MACAW" and row["minecraft"]=="1.21.11"
            assert row["model_hash_kind"]=="SHA256"
            assert row["geometry_status"]=="STATIC_SOURCE"
            assert (int(row["elements"]),int(row["faces"]))==(EXPECTED_ELEMENTS[case],EXPECTED_FACES[case])
            assert source["original_state"]==record["original_state"]==state
            assert source["blockstate_sha256"]==row["state_sha"]
            assert source["model_sha256"]==row["model_sha"]==record["original_model_sha256"]
            assert source["provider_sha256"]==row["provider_sha"]==record["original_provider_sha256"]
            assert source["model_path"]==row["model_path"]==record["original_model_path"]
            assert source["original_model_y"]==record["original_model_y"]==int(row["y"])
            assert source["elements"]==EXPECTED_ELEMENTS[case] and source["faces"]==EXPECTED_FACES[case]
            assert record["server_state_verified"] is True and record["native_f2_verified"] is True
            assert record["connection_formed_naturally_tested"] is False
            assert record["semantic_or_rights_approved"] is False
            assert record["screenshot_file"]==case+".png"
            assert record["screen_foreground_chroma_pixels"]>=150
            assert record["screenshot_dimensions"]==[1024,684]
            evidence=[line for line in client.splitlines() if
                    "[Server thread/" in line and
                    f"[RenderAudit] MCFR_CHAIR_STATE_{case}=" in line]
            assert len(evidence)==1 and evidence[0].endswith("=PASS"),(
                 "CLIENT_SERVER_CASE_NOT_EXACT",case,evidence)
            picture=z.read(case+".png")
            expected_hash=report["actual_native_F2_sha256_by_case"][case]
            assert sha(picture)==expected_hash==a["f2_sha256"][case]==record["screenshot_sha256"]
            with Image.open(io.BytesIO(picture)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            checked[case]={
                "original_exact_server_state":True,
                "original_blockstate":state,
                "selected_model_sha256":row["model_sha"],
                "selected_provider_sha256":row["provider_sha"],
                "selected_faces":EXPECTED_FACES[case],
                "native_F2_sha256":sha(picture),
                "observation":OBS[case],
                "conditional_only":True,
                "natural_connected_state_tested":False,
                "F_full_or_INT5_INT6_rights_approved":False,
            }
        assert len({x["native_F2_sha256"] for x in checked.values()})==5
    previous={r["target_id"]:dict(r) for r in earlier}
    for record in earlier:
        k=record["target_id"]
        if k not in CASES:continue
        record.update({
            "prior_f2_evidence_status":"F9_REAL_MACAW_1_21_11_EXACT_SERVER_AND_NATIVE_F2",
            "image_artifact_ids":str(ARTIFACT),
            "image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+k+".png",
            "image_sha256s":checked[k]["native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA256,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":OBS[k],
            "source_state_and_release_assessment":"MACAW_3_4_2_RELEASE_JAR_MODEL_PROVIDER_STATE_SHA256_MATCH_ORIGINAL_GAME",
            "final_disposition":"CONDITIONAL_F9_SOURCE_STATE_MODEL_AND_ACTUAL_GAME_F2_VERIFIED",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":(
              "정확 게임상태·원본 모델/부모 SHA와 F2를 조건부 연결. 자연 인접 연결·"
              "픽셀 UV/충돌/기능/부품 의미/원본 이미지 권리 및 최종 F 승인은 별도 검증 필요."),
        })
    changes={r["target_id"] for r in earlier if previous[r["target_id"]]!=r}
    assert changes==set(CASES),("UNRELATED_CASE_CHANGED",changes)
    conditional=sum(r["final_disposition"].startswith("CONDITIONAL") for r in earlier)
    hold=sum(r["final_disposition"].startswith("HOLD") for r in earlier)
    assert (conditional,hold)==(48,22)
    historical=[r for r in earlier if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(historical)==62 and sum(r["final_disposition"].startswith("CONDITIONAL") for r in historical)==42
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in earlier)
    pending=[r for r in earlier if r["final_disposition"].startswith("HOLD")]
    hold_groups=dict(sorted(Counter(r["cohort"] or "RISK" for r in pending).items()))
    assert hold_groups=={"MACAW":5,"RISK":2,"VANILLA":15}
    all_csv=csvout(earlier,list(earlier[0]))
    pend_fields=["target_id","cohort","minecraft_version","category","block","original_source_applications",
                 "original_source_faces","final_disposition","additional_required_before_full_acceptance"]
    pend_csv=csvout([{k:r[k] for k in pend_fields} for r in pending],pend_fields)
    summary={
       "schema":"MCFR_INT4_F9_MACAW_FIVE_NATIVE_F2_FULL_INDEPENDENT_70_AUDIT/v1",
       "status":"PASS_FIVE_MACAW_ORIGINAL_F2_48_CONDITIONAL_22_HOLD_FINAL_ZERO",
       "pinned_original_git_blob_sha1":PINS,
       "actual_game_run_id":RUN,
       "actual_game_url":f"https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}",
       "actual_game_artifact_id":ARTIFACT,
       "original_client_zip_sha256":ZIP_SHA256,
       "original_client_log_sha256":report["client_log_sha256"],
       "cases":checked,
       "remaining_holds_by_cohort":hold_groups,
       "counts":{
           "fixed_total_F_targets":70,
           "historical_study_case_denominator":62,
           "original_game_F2_added":5,
           "original_model_applications":5,
           "original_elements":39,
           "original_faces":179,
           "server_exact_original_states":5,
           "new_conditional_cases":5,
           "F_conditional_prior":43,
           "F_conditional_now":48,
           "F_HOLD_prior":27,
           "F_HOLD_now":22,
           "historical_F2_conditional_prior":37,
           "historical_F2_conditional_now":42,
           "unconditional_final_F_acceptance":0,
           "new_INT5_semantic_parts_approved":0,
           "new_INT6_AI_training_redistribution_rights_approved":0,
       },
       "limits":[
          "Exact game /setblock states and native F2 are proven, but natural connected-block behavior NOT tested.",
          "Each official Macaw 3.4.2 model/provider/blockstate SHA256 matches original 1-5 source.",
          "Visual observations are qualitative; no pixelwise UV causality, function, collisions, entity meaning or rights.",
          "No copyrighted JAR/PNG committed to Git, only metadata and SHA evidence.",
          "Other 65 historic F target rows and all prior F8/A-E source artifacts remain unchanged.",
          "Full INT-4-F and INT-4-G/H acceptance and INT5/INT6 remain pending.",
       ],
       "outputs":{"F70":{"rows":70,"sha256":sha(all_csv)},
                  "pending":{"rows":22,"sha256":sha(pend_csv)}},
    }
    report_md="\n".join([
      "# INT-4-F9 — Macaw 원본 5사례 Fabric 1.21.11 실제 F2 검증 및 독립 감사",
      "",
      f"- [실제 Minecraft 1.21.11 Actions #{RUN}](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}) 성공.",
      f"- 네이티브 F2 원본 5장·client.log·manifest GitHub Actions 아티팩트 ID {ARTIFACT}, ZIP SHA256 {ZIP_SHA256}.",
      "- S08 oak_chair: 실제 F2 등받이 있는 작은 나무 의자, 정확 north 상태·모델/부모 SHA 확인.",
      "- S09 oak_stool_chair: 실제 F2 등받이 없는 낮은 나무 스툴, 속성 없는 게임상태 정확 확인.",
      "- S11 oak_end_table: 실제 F2 목재 소형 테이블, east/north/south/west 모두 false 상태 확인.",
      "- S12 oak_coffee_table: 실제 F2 목제 상판과 기둥, connection=with_leg 상태 확인.",
      "- S23 oak_drawer: 실제 F2 나무무늬 수납형 블록, connection=single/facing=north 상태 확인. 서랍 기능은 미검증.",
      "- 연구 1-5 원본 5사례 / 39요소 / 179면. Macaw 3.4.2 JAR 및 각 state/model/provider SHA256와 네이티브 F2/서버 로그 독립 대조.",
      "- **70개 원장** 조건부 43→48 / HOLD 27→22 / 역사 정확 F2 연결 37/62→42/62 / 무조건 승인 0.",
      "- 남은 보류 Macaw S13·S24·S25·S35·S36 5건, 바닐라 15건, 고위험 R06·R08 2건.",
      "- 이 실험은 명시적 /setblock 기반. 인접 구조 자연 생성, UV 픽셀 인과·기능·부품 의미 및 AI 자산 권리 확인/승인 아님.",
      "",
    ]).encode()
    return {OUT70:all_csv,OUT22:pend_csv,SUMMARY:jsonout(summary),REPORT:report_md}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,default=Path("temp-original-F9"))
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for name,content in build(a.artifact_dir/ZIP_NAME).items():
        target=ROOT/name
        if a.verify:
            assert target.is_file() and target.read_bytes()==content,("NONDETERMINISTIC_AUDIT",str(name))
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
        print("VERIFIED" if a.verify else "CREATED",name,len(content))
    print("PASS F9 five native original Macaw F2, 70=48 conditional+22 hold, final F=0")

if __name__=="__main__":main()
