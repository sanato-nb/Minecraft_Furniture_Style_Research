#!/usr/bin/env python3
"""F11F R08: independent original two-game F2 archive + one-row F70 update."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlsplit
import urllib.error,urllib.request
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PRIOR=OUT/"INT4_F11E_70_TARGET_EVIDENCE_DISPOSITIONS_V14.csv"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={str(PRIOR):"53885f7286bcd901f7e2bbefed4692502f02c0af",
      str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179"}
RUN,ARTIFACT=45108332421,14788254210
ZIP_NAME="INT4_F11F_R08_original_dual_Fabric_F2.zip"
ZIP_SHA="a546c6cc8d4777da472a4efc645dd57d06784cf78723dbb53081f0d9319f5b88"
PHOTO="R08_acacia_north_variant1.png"
PNG_SHA="5e3d5494985e7af7dea54bc8b6ee3443c85a3146e30c3e459fb01d1ca6d2d31e"
STATE="another_furniture:acacia_chair[facing=north,tucked=false,variant=1]"
MODEL="another_furniture:block/chair/acacia_1"
GIT="57eb624cbb7f408d43398c7434b0d38d312cb55d"
OLD_STATE_BLOB="3a806533856f169a502373bda43a76eeabc1e689"
NEW_STATE_BLOB="37643398d7a49fdcfc6f2308ca04c13fb0b43aed"
NEW_MODEL_BLOB="609dea1eda246be610ed0a5762f3bb5f0ce9db92"
OUT70=OUT/"INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"
OUTZERO=OUT/"INT4_F11F_0_PENDING_EXACT_F2_TARGETS_V1.csv"
OUTAUDIT=OUT/"INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
OUTREPORT=OUT/"INT4_F11F_R08_DIRECT_VISUAL_SOURCE_REVIEW_V1.md"
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def frozen(path):
    b=(ROOT/path).read_bytes()
    assert gitblob(b)==PINS[str(path)],("ORIGINAL_CHANGED",str(path))
    return b
def crows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def cout(items,fields):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
    w.writeheader();w.writerows(items)
    return f.getvalue().encode()
def jout(j):return (json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode()
def download(path):
    if path.exists():b=path.read_bytes()
    else:
        token=os.environ.get("GH_TOKEN")
        if not token:raise FileNotFoundError("R08 original Actions F2 ZIP/ GH_TOKEN absent")
        u=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
        headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
                 "User-Agent":"MCFR-F11F-independent","X-GitHub-Api-Version":"2022-11-28"}
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*a,**k):return None
        try:
            with urllib.request.build_opener(NoRedirect).open(
                 urllib.request.Request(u,headers=headers),timeout=120) as resp:b=resp.read()
        except urllib.error.HTTPError as e:
            if e.code not in (301,302,303,307,308):raise
            target=e.headers.get("Location","")
            url=urlsplit(target)
            assert url.scheme=="https" and url.netloc and url.netloc!="api.github.com"
            with urllib.request.urlopen(urllib.request.Request(
                 target,headers={"User-Agent":"MCFR-F11F-independent"}),timeout=120) as resp:b=resp.read()
        assert sha(b)==ZIP_SHA
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    assert sha(b)==ZIP_SHA
    return b

def build(file):
    prior=crows(frozen(PRIOR))
    original=crows(frozen(STUDY))
    assert len(prior)==70 and len({r["target_id"] for r in prior})==70 and len(original)>=62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==69
    assert [r["target_id"] for r in prior if r["final_disposition"].startswith("HOLD")]==["R08"]
    original_rows={r["target_id"]:dict(r) for r in prior}
    assert sum(r["target_kind"]=="HISTORICAL_1_5_CASE" for r in prior)==62
    with ZipFile(io.BytesIO(download(file))) as zipf:
        assert zipf.testzip() is None
        names=zipf.namelist()
        required={"r08-two-source-releases-comparison.json",
                  *(prefix+filename for prefix in ("r08-402-native-F2/","r08-403-native-F2/")
                  for filename in ("INT4_F11F_R08_SINGLE_FABRIC_RELEASE_NATIVE_F2.json",
                                   "INT3_REAL_GAME_CAPTURE.json","client.log",PHOTO))}
        assert len(names)==len(set(names)) and set(names)==required
        pair=json.loads(zipf.read("r08-two-source-releases-comparison.json"))
        assert pair["status"]=="DUAL_FABRIC_NATIVE_F2_SOURCE_BUILD_COMPARISON_NOT_OFFICIAL_403_RELEASE"
        assert pair["historical_risk_case"]=="R08" and pair["same_loader"]=="fabric"
        assert pair["minecraft_version"]=="1.21.1"
        assert pair["original_4_0_3_study_git_commit"]==GIT
        assert pair["exact_same_original_state"]==STATE and pair["selected_model"]==MODEL
        checks=pair["gates"]
        assert checks["two_real_same_loader_Fabric_1_21_1_client_F2"] is True
        assert checks["source_built_fabric_4_0_3_matches_pinned_Git_state_and_model"] is True
        assert checks["published_official_fabric_4_0_2"] is True
        for field in ("published_official_fabric_4_0_3","official_4_0_3_NeoForge_client_F2",
                      "all_88_source_option_visual_parity","direct_pixel_attribution_to_model_UV",
                      "INT4_F_final_unconditional_approval","INT5_semantics",
                      "INT6_training_or_redistribution_rights"):
            assert checks[field] is False,field
        images=[]
        evidence={}
        for prefix,version,sourcehash in (
              ("r08-402-native-F2/","4.0.2",OLD_STATE_BLOB),
              ("r08-403-native-F2/","4.0.3",NEW_STATE_BLOB)):
            manifest=json.loads(zipf.read(prefix+"INT4_F11F_R08_SINGLE_FABRIC_RELEASE_NATIVE_F2.json"))
            captured=json.loads(zipf.read(prefix+"INT3_REAL_GAME_CAPTURE.json"))
            rel=manifest["release"]
            assert manifest["status"]=="ONE_REAL_FABRIC_SOURCE_RELEASE_F2_CAPTURED_NOT_CROSS_RELEASE_APPROVED"
            assert manifest["risk_case"]=="R08" and manifest["minecraft"]=="1.21.1"
            assert manifest["actual_server_original_state_PASS"] is True
            assert manifest["native_F2_sha256"]==PNG_SHA
            assert manifest["native_F2_dimensions"]==[1024,684]
            assert rel["version"]==version and rel["selected_exact_original_state"]==STATE
            assert rel["selected_model"]==MODEL and rel["selected_y"]==0
            assert rel["selected_blockstate_git_blob_sha1"]==sourcehash
            if version=="4.0.3":
                assert rel["source_study_Git_commit"]==GIT
                assert rel["selected_model_git_blob_sha1"]==NEW_MODEL_BLOB
                assert rel["not_an_official_published_Fabric_4_0_3"] is True
                assert rel["release_kind"]=="PINNED_GIT_COMMIT_FABRIC_SOURCE_BUILT_NOT_OFFICIAL_RELEASE"
            else:
                assert rel["installed_jar_sha1"]=="c2f992081bdc4795ed6d87771a3b5f7c71103785"
                assert rel["release_kind"]=="OFFICIAL_MODRINTH_FABRIC_RELEASE_4_0_2"
            assert sha(zipf.read(prefix+"client.log"))==manifest["client_log_sha256"]
            log=zipf.read(prefix+"client.log").decode(errors="replace")
            assert "MCFR_CHAIR_STATE_R08_acacia_north_variant1=PASS" in log
            assert "MCFR_CHAIR_STATE_R08_acacia_north_variant1=FAIL" not in log
            assert captured["actual_game_capture"] is True
            assert captured["source_state_verified_count"]==1
            assert captured["minecraft_native_f2_screenshot_count"]==1
            assert captured["states"][0]["server_blockstate_verified"] is True
            assert captured["states"][0]["original_state"]==STATE
            image=zipf.read(prefix+PHOTO)
            assert sha(image)==PNG_SHA==captured["states"][0]["screenshot_sha256"]
            with Image.open(io.BytesIO(image)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
                brown=sum(1 for r,g,b in im.convert("RGB").crop((465,390,560,530)).getdata()
                          if r>g+12 and g>b+5 and r>65 and b<150)
                assert brown==3542,("CHAIR_FOREGROUND_NOT_REPRODUCED",version,brown)
            images.append(image)
            evidence[version]={"jar_SHA256":rel["installed_jar_sha256"],
                               "blockstate_git_blob_sha1":sourcehash,
                               "model_git_blob_sha1":rel["selected_model_git_blob_sha1"],
                               "actual_server_PASS":True,"visible_chair_brown_pixels":brown,
                               "native_F2_SHA256":PNG_SHA}
        assert images[0]==images[1]
        assert pair["descriptive_image_noncausal"]["roi_changed_pixel_count"]==0
    r=next(x for x in prior if x["target_id"]=="R08")
    r.update({
        "prior_f2_evidence_status":"R08_TWO_ACTUAL_FABRIC_GAME_F2_GIT_403_SOURCE_BUILD_VS_OFFICIAL_402",
        "image_artifact_ids":str(ARTIFACT),"image_run_ids":str(RUN),
        "image_files":ZIP_NAME+":r08-402-native-F2/"+PHOTO+";"+ZIP_NAME+":r08-403-native-F2/"+PHOTO,
        "image_sha256s":PNG_SHA+";"+PNG_SHA,"original_zip_sha256s":ZIP_SHA,
        "newly_reopened_original_png":"true","direct_visual_observation_this_turn":"true",
        "human_observation_text":"두 실제 F2 모두 중앙의 밝은 갈색 목재 의자 직접 관찰, ROI 3,542 갈색 픽셀, 원본 PNG 바이트 완전 동일. 오직 이 대표 블록 상태만.",
        "source_state_and_release_assessment":"GIT_403_SOURCE_BUILT_FABRIC_PINNED_VS_OFFICIAL_MODRINTH_FABRIC_402_SHA_PINNED_NOT_PUBLISHED_403_NEOFORGE",
        "final_disposition":"CONDITIONAL_F11F_R08_GIT403_FABRIC_STUDY_VS_OFFICIAL402_SINGLE_STATE_MATCHED_REAL_F2",
        "runtime_evidence_accepted_as_full_F_PASS":"false",
        "additional_required_before_full_acceptance":"연구 4.0.3 Git 소스 빌드 Fabric과 공식 Fabric 4.0.2의 북향 의자 variant1 상태만 실게임 조건부 대조. 공식 4.0.3 NeoForge는 미시험. 전체 88상태·기능·UV·AI권리 및 F/G/H 최종 종료는 별도.",
    })
    assert {x["target_id"] for x in prior if x!=original_rows[x["target_id"]]}=={"R08"}
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior)==70
    assert all(not x["final_disposition"].startswith("HOLD") and
               x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in prior)
    raw70=cout(prior,list(prior[0]))
    pending_columns=("target_id","cohort","minecraft_version","category","block",
                     "original_source_applications","original_source_faces",
                     "final_disposition","additional_required_before_full_acceptance")
    rawzero=cout([],list(pending_columns))
    summary={"schema":"MCFR_INT4_F11F_R08_ORIGINAL_DUAL_FABRIC_F2_INDEPENDENT_AUDIT/v1",
             "status":"PASS_70_CONDITIONAL_ZERO_HOLD_ZERO_FINAL_F_WITH_NEOFORGE_403_EXCEPTION",
             "source_pinned_git_blobs":PINS,"run":RUN,"artifact_id":ARTIFACT,
             "original_zip_SHA256":ZIP_SHA,"native_two_F2_sha256":PNG_SHA,
             "versions":evidence,
             "official_4_0_3_NeoForge_not_tested":True,
             "counts":{"F_targets":70,"historical_cases":62,
                       "F_conditional_before":69,"F_conditional_after":70,
                       "F_HOLD_before":1,"F_HOLD_after":0,
                       "F_unconditional_final_approvals":0,
                       "G_approvals":0,"H_exit_approvals":0,
                       "INT5_semantics_approved":0,
                       "INT6_training_or_redistribution_rights_approved":0},
             "limits":["The study 4.0.3 JAR was built from pinned Git Fabric sources, not an official published 4.0.3 Fabric release.",
                       "Official 4.0.3 NeoForge was not executed.",
                       "Only the north variant1 acacia chair state was compared, not all 88 states.",
                       "Identical selected screenshots cannot prove whole release, baked UV causality, function, roles or rights.",
                       "F70 conditional evidence saturation is not complete F/G/H research acceptance."],
             "output_sha256":{"ledger":sha(raw70),"pending":sha(rawzero)}}
    markdown="\n".join([
        "# INT-4-F11F R08 실제 원본 F2 독립 비교",
        "",
        "- 실제 Minecraft 1.21.1 [Actions #45108332421](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45108332421) 초록 성공.",
        "- 4.0.2 공식 Fabric vs 4.0.3 고정 Git 소스 자체 빌드 Fabric; 공식 4.0.3 NeoForge 배포와 구분.",
        "- 동일 블록 acacia_chair facing=north tucked=false variant=1, 소스 모델 acacia_1, 두 서버 상태 PASS.",
        "- 원본 F2 2장 1024x684, SHA256 완전 동일, 3,542개 목재색 의자 전경 픽셀 존재.",
        "- 블록상태 4.0.2/4.0.3 원본 SHA 서로 다름; 선택한 소스 모델 SHA·JAR SHA를 개별 기록.",
        "- 대표 연구 Git vs 실게임 릴리스 상태 범위에서만 R08 조건부 인정.",
        "- **고정 F 대상 70/70 조건부, 보류 0. 최종 무조건 F 승인 0, G/H 종료 미승인.**",
        "- 4.0.3 공식 NeoForge, 전체 88 상태, 원본 UV/부품 의미/행동/AI 학습·재배포권은 미승인.",
        "",
    ]).encode()
    return {OUT70:raw70,OUTZERO:rawzero,OUTAUDIT:jout(summary),OUTREPORT:markdown}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--zip-dir",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for path,data in build(a.zip_dir/ZIP_NAME).items():
        out=ROOT/path
        if a.verify:
            assert out.is_file() and out.read_bytes()==data,("NONDETERMINISM",str(path))
        else:
            out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
        print("VERIFIED" if a.verify else "CREATED",path,len(data))
    print("PASS 70/70 conditional; 0 HOLD; 0 F final; G/H still pending")

if __name__=="__main__":main()
