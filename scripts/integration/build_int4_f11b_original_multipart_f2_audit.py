#!/usr/bin/env python3
"""INT-4-F11B official Minecraft 1.21.11 F2 independent source/multipart audit.

Verify pinned actual original ZIP, client log, server state, 12 model leaf and
provider SHA1, 70-row exact scope; no UV/semantic or copyright approvals.
"""
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
import urllib.error,urllib.request
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PREV=OUT/"INT4_F11A_70_TARGET_EVIDENCE_DISPOSITIONS_V10.csv"
NEW=OUT/"INT4_F11B_FIVE_VANILLA_REAL_F2_SOURCE_V1.json"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={str(PREV):"51aea1ec91472c4ff2ad99a6b2ce8f9975854b18",
      str(NEW):"__CAPTURE_SHA__",
      str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179"}
RUN=45098021558
ARTIFACT=0
ZIP_NAME="INT4_F11B_VANILLA_FIVE_ORIGINAL_F2.zip"
ZIP_SHA="__ZIP_SHA__"
CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
STUDY_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
CASES=("V03","V04","V06","V08","V09")
N={"V03":(2,3,16),"V04":(1,1,6),"V06":(1,1,6),"V08":(7,7,11),"V09":(1,1,6)}
OBS={
 "V03":"F2에서 실제 북쪽 이웃에 연결된 참나무 울타리 기둥과 연결부 관찰",
 "V04":"F2에서 바닥의 매우 낮은 참나무 압력판 외형 관찰",
 "V06":"F2에서 참나무 통 외형 관찰; open=true는 서버 상태만 확인, GUI 기능 미승인",
 "V08":"F2에서 조각된 책장 블록 외형 관찰; 정확한 슬롯 픽셀 인과 미승인",
 "V09":"F2에서 흰색 양털 정육면체를 무채색 밝은 전경 픽셀로 관찰",
}
OUT70=OUT/"INT4_F11B_70_TARGET_EVIDENCE_DISPOSITIONS_V11.csv"
OUT12=OUT/"INT4_F11B_7_PENDING_EXACT_F2_TARGETS_V1.csv"
AUDIT=OUT/"INT4_F11B_FIVE_VANILLA_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
REVIEW=OUT/"INT4_F11B_FIVE_CASE_ORIGINAL_IMAGE_REVIEW_V1.md"

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
        if not token:raise FileNotFoundError("Original F11A Actions artifact and GH_TOKEN both missing")
        api=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
        heads={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
               "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-F11A-original-F2-audit"}
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
                 location,headers={"User-Agent":"MCFR-F11A-original-F2-audit"}),timeout=120) as response:
                data=response.read()
        assert sha(data)==ZIP_SHA,("ORIGINAL_REMOTE_ZIP_CHANGED",sha(data))
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    assert sha(data)==ZIP_SHA,("ORIGINAL_ZIP_CHANGED",sha(data))
    return data

def build(archive_path):
    prior=rows(locked(PREV))
    captured=json.loads(locked(NEW))
    source_rows=rows(locked(STUDY))
    assert len(prior)==70 and len({x["target_id"] for x in prior})==70
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior)==58
    assert sum(x["final_disposition"].startswith("HOLD") for x in prior)==12
    assert captured["status"]=="PASS_FIVE_VANILLA_MULTIPART_12111_EXACT_STATE_NATIVE_F2_NOT_FINAL"
    assert captured["original_historical_case_ids"]==list(CASES)
    assert (captured["original_model_applications"],captured["original_source_elements"],
            captured["original_source_faces"],captured["real_game_server_exact_states"],
            captured["real_game_native_F2_count"])==(12,13,45,5,5)
    assert (captured["official_client_sha1"],captured["official_client_sha256"],
            captured["original_applications_source_sha256"])==(CLIENT_SHA1,CLIENT_SHA256,STUDY_SHA)
    assert (captured["full_F_approved"],captured["INT5_part_semantics_approved"],
            captured["INT6_AI_training_or_redistribution_rights_approved"])==(0,0,0)
    selected={key:[x for x in source_rows if x["case"]==key] for key in CASES}
    assert {k:(len(v),sum(int(x["elements"]) for x in v),sum(int(x["faces"]) for x in v))
            for k,v in selected.items()}==N
    before={x["target_id"]:dict(x) for x in prior}
    assert all(before[k]["final_disposition"].startswith("HOLD") for k in CASES)
    actual={}
    with ZipFile(io.BytesIO(archive(archive_path))) as z:
        assert z.testzip() is None
        files=z.namelist()
        assert len(files)==len(set(files))
        assert set(files)=={"INT4_F11B_VANILLA_FIVE_REAL_F2_CAPTURE.json",
                           "INT4_F11B_VANILLA_FIVE_F2_AUDIT.json",
                           "client.log",*(k+".png" for k in CASES)}
        manifest=json.loads(z.read("INT4_F11B_VANILLA_FIVE_REAL_F2_CAPTURE.json"))
        g_audit=json.loads(z.read("INT4_F11B_VANILLA_FIVE_F2_AUDIT.json"))
        assert manifest["schema"]=="MCFR_INT4_F11B_VANILLA_MULTIPART_FIVE_REAL_F2/v1"
        assert manifest["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        assert manifest["minecraft_version"]=="1.21.11"
        assert manifest["source_state_verified_count"]==manifest["minecraft_native_f2_screenshot_count"]==5
        assert g_audit["status"]==captured["status"]
        registry=manifest["original_source_registry"]
        assert (registry["official_client_jar_sha1"],registry["official_client_jar_sha256"],
                registry["source_ledger_sha256"])==(CLIENT_SHA1,CLIENT_SHA256,STUDY_SHA)
        assert registry["original_multipart_selection_independently_checked"] is True
        assert registry["states"]==captured["source_cases"]
        log=z.read("client.log")
        assert sha(log)==captured["client_log_sha256"]==g_audit["client_log_sha256"]==manifest["client_log_sha256"]
        decoded=log.decode("utf-8",errors="replace")
        captured_cases={x["case_id"]:x for x in manifest["states"]}
        assert len(captured_cases)==len(manifest["states"])==5 and set(captured_cases)==set(CASES)
        for k in CASES:
            study=selected[k];root=study[0]
            model=registry["states"][k]
            view=captured_cases[k]
            assert all(x["cohort"]=="VANILLA" and x["minecraft"]=="1.21.11" and
                       x["model_hash_kind"]=="GIT_BLOB_SHA1" and
                       x["state"]==root["state"] and x["state_sha"]==root["state_sha"]
                       for x in study)
            props=json.loads(root["state"])
            state="minecraft:"+root["block"]+("["+(",".join(x+"="+v for x,v in props.items()))+"]" if props else "")
            assert model["original_state"]==view["original_state"]==state
            assert model["blockstate_git_blob_sha1"]==root["state_sha"]
            assert model["selected_model_application_count"]==len(study)
            assert (model["elements"],model["faces"])==N[k][1:]
            assert model["original_applications"]==view["original_model_applications"]
            assert (view["original_model_application_count"],view["original_source_elements"],
                    view["original_source_faces"])==N[k]
            for r,o in zip(study,model["original_applications"]):
                assert (o["original_rule_index"],o["original_option_index"])==(
                    int(r["rule_index"]),int(r["option_index"]))
                assert (o["model_path"],o["model_git_blob_sha1"],o["provider_path"],
                        o["provider_git_blob_sha1"])==(
                    r["model_path"],r["model_sha"],r["provider_path"],r["provider_sha"])
                assert (o["model_x"],o["model_y"],o["model_uvlock"],o["elements"],o["faces"])==(
                    int(r["x"]),int(r["y"]),int(r["uvlock"]),int(r["elements"]),int(r["faces"]))
                if r["model_path"]!=r["provider_path"]:
                    assert any(t["path"]==r["provider_path"] and
                               t["git_blob_sha1"]==r["provider_sha"]
                               for t in o["official_parent_chain_git_blob_sha1"])
            assert view["server_state_verified"] and view["native_f2_verified"]
            assert view["screen_foreground_visible_by_color_or_white_proxy"] is True
            assert view["screenshot_dimensions"]==[1024,684]
            assert view["semantic_or_rights_approved"] is False
            assert "MCFR_CHAIR_STATE_"+k+"=PASS" in decoded
            assert "MCFR_CHAIR_STATE_"+k+"=FAIL" not in decoded
            if k=="V03":
                assert [a["original_rule_index"] for a in model["original_applications"]]==[0,1]
            if k=="V08":
                assert [a["original_rule_index"] for a in model["original_applications"]]==[0,1,4,6,8,10,12]
            if k=="V09":
                assert view["screen_foreground_neutral_white_pixels"]>=300
            native=z.read(k+".png")
            digest=sha(native)
            assert digest==view["screenshot_sha256"]==captured["native_F2_sha256"][k]==g_audit["native_F2_sha256"][k]
            with Image.open(io.BytesIO(native)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            actual[k]={"original_block":root["block"],"state":state,
                       "source_model_applications":len(study),"source_elements":N[k][1],
                       "source_faces":N[k][2],"original_native_F2_sha256":digest,
                       "direct_visual_observation":OBS[k],
                       "original_selected_model_rule_indices":[int(r["rule_index"]) for r in study],
                       "server_game_exact":True,"conditional_not_final":True}
    for row in prior:
        k=row["target_id"]
        if k not in CASES:continue
        row.update({
            "prior_f2_evidence_status":"EXACT_12111_ORIGINAL_MULTIPART_NATIVE_F2_F11B",
            "image_artifact_ids":str(ARTIFACT),"image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+k+".png",
            "image_sha256s":actual[k]["original_native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":OBS[k],
            "source_state_and_release_assessment":"OFFICIAL_VANILLA_12111_12_MULTIPART_MODEL_LEAF_PROVIDER_SERVER_EXACT",
            "final_disposition":"CONDITIONAL_F11B_EXACT_MULTIPART_SOURCE_NATIVE_F2",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":
                "원본 멀티파트/실게임 상태/F2 SHA 근거는 조건부. 사용자 상호작용·UV 픽셀·기능·의미·원본 권리 별도.",
        })
    assert {x["target_id"] for x in prior if x!=before[x["target_id"]]}==set(CASES)
    pending=[x for x in prior if x["final_disposition"].startswith("HOLD")]
    assert (sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior),len(pending))==(63,7)
    expected={"V11","V12","V13","V14","V15","R06","R08"}
    assert {x["target_id"] for x in pending}==expected
    history=[x for x in prior if x["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(history)==62
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in history)==57
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in prior)
    allbytes=csvout(prior,list(prior[0].keys()))
    cols=("target_id","cohort","minecraft_version","category","block",
          "original_source_applications","original_source_faces","final_disposition",
          "additional_required_before_full_acceptance")
    waiting=csvout([{k:x[k] for k in cols} for x in pending],list(cols))
    summary={
      "schema":"MCFR_INT4_F11B_ORIGINAL_MOJANG_MULTIPART_F2_INDEPENDENT_AUDIT/v1",
      "status":"PASS_FIVE_VANILLA_NATIVE_F2_63_CONDITIONAL_7_HOLD_FULL_ZERO",
      "original_source_git_sha1_pins":PINS,
      "official_client_sha1":CLIENT_SHA1,"official_client_sha256":CLIENT_SHA256,
      "real_original_game_run":RUN,"real_original_game_artifact":ARTIFACT,
      "original_zip_sha256":ZIP_SHA,"original_client_log_sha256":captured["client_log_sha256"],
      "cases":actual,"remaining_HOLD_target_ids":sorted(expected),
      "counts":{"fixed_F_targets":70,"historical_original_cases":62,
                "new_real_exact_server_states":5,"new_original_native_F2":5,
                "original_selected_models":12,"original_model_elements":13,"original_model_faces":45,
                "F_conditional_before":58,"F_conditional_after":63,
                "F_HOLD_before":12,"F_HOLD_after":7,
                "historical_original_F2_before":52,"historical_original_F2_after":57,
                "full_F_unconditionally_accepted":0,"INT5_semantics_approved":0,"INT6_AI_rights_approved":0},
      "limitations":[
        "V03 real fence north neighbor and source multipart state proven, not all natural placement dynamics.",
        "V08 seven selected original models proven, not player book UI nor pixel-by-pixel slot causal proof.",
        "V06 barrel open=true state observed on real server; user opening functionality untested.",
        "Original PNGs re-opened visually but no pixel UV or semantic final approval.",
        "Other 65 original F rows and original 1-5 unchanged. No copyrighted assets committed.",
        "G/H/INT5/INT6 remain pending."],
      "output_SHA256":{"F70":sha(allbytes),"pending":sha(waiting)}
    }
    notes="\n".join([
      "# INT-4-F11B 원본 바닐라 멀티파트 5개 F2 실제 게임 검증 및 독립 감사",
      "",
      "- 실제 Minecraft 1.21.11 촬영 Actions: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/"+str(RUN),
      "- 원본 아티팩트 ZIP "+str(ARTIFACT)+" SHA256 "+ZIP_SHA+". 네이티브 F2 5장과 client.log 직접 열어 검증.",
      "- 역사 원본 5개 사례/동시 선택 모델 12개/13요소/45면. V03 울타리 2모델, V08 조각된 책장 7모델 포함.",
      "- 실제 서버 상태 V03 north=true, V04 powered=false, V06 open=true, V08 첫 슬롯 occupied=true, V09 white wool 5/5 PASS.",
      "- V09 흰색 픽셀 관찰 별도 검증. V06 열린 통 상태는 GUI 기능 승인과 구별.",
      "- 고정 70개 조건부 58→63, HOLD 12→7. 원본 역사 연구 F2 연결 52/62→57/62. 최종 무조건 승인 0.",
      "- 남은 대상 V11~V15, R06, R08. UV 인과·자연 상태 전이·기능·부품 의미·AI 학습/재배포권은 별도 보류.",
      "",
    ]).encode("utf-8")
    return {OUT70:allbytes,OUT12:waiting,AUDIT:jsonout(summary),REVIEW:notes}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,default=Path("tmp-f11a-original-game"))
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for path,content in build(a.artifact_dir/ZIP_NAME).items():
        target=ROOT/path
        if a.verify:assert target.exists() and target.read_bytes()==content,("NONDETERMINISTIC",str(path))
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
        print("VERIFIED" if a.verify else "CREATED",path,len(content))
    print("F11B verified 70 targets conditional58 HOLD12 fullF0")

if __name__=="__main__":main()
