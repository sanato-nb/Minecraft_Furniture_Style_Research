#!/usr/bin/env python3
"""INT-4-F11E actual R06 source-locked 3-timepoint F2 independent audit.

Reopen original GitHub Actions ZIP, 3 PNGs, exact server log, monotonic 8s
intervals, independent pixel water/stone controls, original 1-5 S43 source.
Change ONLY R06 in 70-row F ledger, never infer animation from unchanged pixels.
"""
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
import urllib.error,urllib.request
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PREV=OUT/"INT4_F11D_70_TARGET_EVIDENCE_DISPOSITIONS_V13.csv"
NEW=OUT/"INT4_F11E_R06_TEMPORAL_REAL_F2_SOURCE_V1.json"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PIN={
 str(PREV):"2304adf8904415a8e30f7bdae6f35d0e6354cc19",
 str(NEW):"__CAPTURE_GIT_BLOB_SHA1__",
 str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
PINS=PIN
RUN=45104714782
ARTIFACT=__ARTIFACT__
ZIP_NAME="INT4_F11E_R06_TEMPORAL_ORIGINAL_F2.zip"
ZIP_SHA="__ZIP_SHA256__"
STUDY_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
MACAW_SHA256="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
KEYS=("R06_T0","R06_T1","R06_T2")
WATER_ROI=(480,415,545,443)
SINK_ROI=(462,394,564,508)
STONE_ROI=(610,530,690,610)
OUT70=OUT/"INT4_F11E_70_TARGET_EVIDENCE_DISPOSITIONS_V14.csv"
PENDING=OUT/"INT4_F11E_1_PENDING_EXACT_F2_TARGETS_V1.csv"
AUDIT=OUT/"INT4_F11E_R06_TEMPORAL_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
REVIEW=OUT/"INT4_F11E_R06_THREE_TIMEPOINT_DIRECT_VISUAL_REVIEW_V1.md"

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

def pixel_delta(left,right,roi):
    x=left.convert("RGB").crop(roi)
    y=right.convert("RGB").crop(roi)
    assert x.size==y.size
    return sum(1 for a,b in zip(x.getdata(),y.getdata())
               if max(abs(i-j) for i,j in zip(a,b))>=24)

def blue_count(image):
    crop=image.convert("RGB").crop(WATER_ROI)
    return sum(1 for r,g,b in crop.getdata() if b>r+35 and b>g+10 and b>100)

def build(path):
    prior=rows(locked(PREV))
    original=rows(locked(STUDY))
    game=json.loads(locked(NEW))
    assert len(prior)==70 and len({r["target_id"] for r in prior})==70
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==68
    assert sum(r["final_disposition"].startswith("HOLD") for r in prior)==2
    before={r["target_id"]:dict(r) for r in prior}
    assert {k for k,v in before.items() if v["final_disposition"].startswith("HOLD")}=={"R06","R08"}
    source={r["case"]:r for r in original if r["case"] in ("S42","S43")}
    assert set(source)=={"S42","S43"}
    dry,wet=source["S42"],source["S43"]
    assert all(row["cohort"]=="MACAW" and row["minecraft"]=="1.21.11" and
               row["model_hash_kind"]=="SHA256" and row["geometry_status"]=="STATIC_SOURCE"
               for row in (dry,wet))
    assert dry["block"]==wet["block"]=="mcwfurnitures:oak_kitchen_sink"
    assert (dry["state"],int(dry["elements"]),int(dry["faces"]))==(
            "facing=north;water=false",16,55)
    assert (wet["state"],int(wet["elements"]),int(wet["faces"]))==(
            "facing=north;water=true",17,56)
    assert game["schema"]=="MCFR_INT4_F11E_R06_THREE_NATIVE_TEMPORAL_F2_AUDIT/v1"
    assert game["status"]=="PASS_R06_3_TIME_SEPARATED_EXACT_STATE_NATIVE_F2_NO_ANIMATION_CAUSAL_CLAIM"
    assert game["risk_id"]=="R06" and game["historical_source_case"]=="S43"
    assert game["source_mod_jar_sha256"]==MACAW_SHA256
    assert game["real_exact_server_state_checks"]==game["original_native_F2_count"]==3
    assert len(game["time_intervals_seconds"])==2
    assert min(game["time_intervals_seconds"])>=8.0
    assert game["water_animation_causally_proven"] is False
    assert (game["full_F_approved"],game["INT5_semantics_approved"],
            game["INT6_training_or_redistribution_rights_approved"])==(0,0,0)
    assert set(game["native_F2_sha256"])==set(KEYS)
    with ZipFile(io.BytesIO(archive(path))) as z:
        assert z.testzip() is None
        files=z.namelist()
        assert len(files)==len(set(files))
        assert set(files)=={
            "INT4_F11E_R06_TEMPORAL_REAL_F2_CAPTURE.json",
            "INT4_F11E_R06_TEMPORAL_REAL_F2_AUDIT.json",
            "client.log",*(k+".png" for k in KEYS)}
        manifest=json.loads(z.read("INT4_F11E_R06_TEMPORAL_REAL_F2_CAPTURE.json"))
        original_game_audit=json.loads(z.read("INT4_F11E_R06_TEMPORAL_REAL_F2_AUDIT.json"))
        assert manifest["schema"]=="MCFR_INT4_F11E_R06_SOURCE_PINNED_MACAW_TEMPORAL_REAL_F2/v1"
        assert manifest["status"]=="CAPTURED_REAL_S43_THREE_TIME_SEPARATED_F2_NOT_YET_INDEPENDENTLY_AUDITED"
        assert manifest["minecraft_version"]=="1.21.11"
        assert manifest["risk_id"]=="R06" and manifest["source_historical_case_id"]=="S43"
        assert manifest["source_state"]=="mcwfurnitures:oak_kitchen_sink[facing=north,water=true]"
        assert manifest["source_jar_sha256"]==MACAW_SHA256
        assert manifest["historical_source_ledger_sha256"]==STUDY_SHA256
        assert manifest["dry_source_faces"]==55 and manifest["wet_source_faces"]==56
        src=manifest["source_registry"]
        assert src["block_id"]==wet["block"] and src["source_state"]==manifest["source_state"]
        assert src["source_model_sha256"]==wet["model_sha"]
        assert src["source_provider_sha256"]==wet["provider_sha"]
        assert src["source_state_sha256"]==wet["state_sha"]
        assert src["source_faces"]==56 and src["source_elements"]==17
        assert src["source_rule_index"]==int(wet["rule_index"])
        assert src["source_option_index"]==int(wet["option_index"])
        assert src["source_model_rotation_y"]==int(wet["y"])
        assert manifest["game_integrated_server_state_checks"]==3
        assert len(manifest["state_check_evidence"])==3
        assert all(e["PASS"] is True and e["source_state"]==manifest["source_state"]
                   for e in manifest["state_check_evidence"])
        clocks=manifest["real_monotonic_F2_capture_clock_ns"]
        assert set(clocks)==set(KEYS)
        intervals=[round((clocks[KEYS[i]]-clocks[KEYS[i-1]])/1e9,3)
                   for i in (1,2)]
        assert intervals==manifest["real_time_intervals_seconds"]==game["time_intervals_seconds"]
        assert min(intervals)>=8.
        assert manifest["time_change_implies_animation"] is False
        assert original_game_audit["status"]==game["status"]
        assert original_game_audit["pixel_observation"]==game["pixel_observation"]
        assert original_game_audit["native_F2_sha256"]==game["native_F2_sha256"]
        assert original_game_audit["water_animation_causally_proven"] is False
        assert (original_game_audit["full_F_approved"],
                original_game_audit["INT5_semantics_approved"],
                original_game_audit["INT6_training_or_redistribution_rights_approved"])==(0,0,0)
        logfile=z.read("client.log")
        assert sha(logfile)==manifest["original_game_client_log_sha256"]==game["original_client_log_sha256"]
        txt=logfile.decode("utf-8",errors="replace")
        assert txt.count("MCFR_R06_S43_STABLE=PASS")>=3
        assert "MCFR_R06_S43_STABLE=FAIL" not in txt
        assert "MCFR_CHAIR_STATE_S43=PASS" in txt and "MCFR_CHAIR_STATE_S43=FAIL" not in txt
        frames={}
        for k in KEYS:
            png=z.read(k+".png")
            assert sha(png)==manifest["native_F2_png_sha256"][k]==game["native_F2_sha256"][k]
            with Image.open(io.BytesIO(png)) as img:
                img.load()
                assert img.format=="PNG" and img.size==(1024,684)
                frames[k]=img.convert("RGB")
        water={k:blue_count(frames[k]) for k in KEYS}
        assert min(water.values())>=200
        pairs=((KEYS[0],KEYS[1]),(KEYS[1],KEYS[2]),(KEYS[0],KEYS[2]))
        matrix={}
        for a,b in pairs:
            matrix[a+"_vs_"+b]={
                "water_changed_pixels":pixel_delta(frames[a],frames[b],WATER_ROI),
                "sink_changed_pixels":pixel_delta(frames[a],frames[b],SINK_ROI),
                "stone_control_changed_pixels":pixel_delta(frames[a],frames[b],STONE_ROI),
            }
        control=max(x["stone_control_changed_pixels"] for x in matrix.values())
        assert control<=40
        observation={
            "water_roi":list(WATER_ROI),"sink_roi":list(SINK_ROI),
            "stone_control_roi":list(STONE_ROI),
            "foreground_blue_water_pixels_each_frame":water,
            "paired_pixel_differences":matrix,
            "max_background_stone_control_delta":control,
            "water_pixel_changed_observed":any(x["water_changed_pixels"]>0 for x in matrix.values()),
            "color_channel_difference_threshold":24,
        }
        orig=game["pixel_observation"]
        for key,v in observation.items():
            assert orig[key]==v,("R06_ORIGINAL_PIXELS_NOT_REPRODUCIBLE",key)
        verdict=orig["temporal_interpretation"]
        assert verdict==("WATER_REGION_CHANGED_AT_SAMPLED_TIMES_NOT_CAUSAL_ANIMATION_PROOF"
                         if observation["water_pixel_changed_observed"]
                         else "NO_WATER_REGION_CHANGE_AT_SAMPLED_TIMES_NOT_PROOF_ANIMATION_ABSENT")
    note=("동일 Macaw 원본 S43 water=true 위치/상태와 같은 카메라에서 "
          "8초 이상 간격으로 실제 F2 3장을 촬영하고 매시점 서버 재검증. "
          "물 ROI의 관찰된 픽셀 변화 여부는 "+verdict+
          "; 샘플별 정적/변화 관찰은 기능·애니메이션 인과 증명 아님.")
    for entry in prior:
        if entry["target_id"]!="R06":continue
        entry.update({
            "prior_f2_evidence_status":"ACTUAL_ORIGINAL_12111_MACAW_S43_THREE_TIME_SEPARATED_F2_F11E",
            "image_artifact_ids":str(ARTIFACT),"image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+";".join(k+".png" for k in KEYS),
            "image_sha256s":";".join(game["native_F2_sha256"][k] for k in KEYS),
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":note,
            "source_state_and_release_assessment":
                "ACTUAL_MACAW_3_4_2_S43_WATER_TRUE_EXACT_SERVER_3_TIME_F2_STONE_CONTROL",
            "final_disposition":"CONDITIONAL_F11E_R06_THREE_REAL_TIME_F2_NO_WATER_ANIMATION_CAUSAL_APPROVAL",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":
                "실제 시간차 F2 3장·동일 상태 조건부. 물 애니메이션 코드 인과·UV·유체 기능·재배포권 별도.",
        })
    assert {r["target_id"] for r in prior if r!=before[r["target_id"]]}=={"R06"}
    waiting=[r for r in prior if r["final_disposition"].startswith("HOLD")]
    assert len(waiting)==1 and waiting[0]["target_id"]=="R08"
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==69
    history=[r for r in prior if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(history)==62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in history)==62
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in prior)
    all70=csvout(prior,list(prior[0].keys()))
    fields=("target_id","cohort","minecraft_version","category","block",
            "original_source_applications","original_source_faces",
            "final_disposition","additional_required_before_full_acceptance")
    pending=csvout([{k:r[k] for k in fields} for r in waiting],list(fields))
    summary={
      "schema":"MCFR_INT4_F11E_R06_MACAW_REAL_TEMPORAL_F70_INDEPENDENT_AUDIT/v1",
      "status":"PASS_R06_CONDITIONAL_69_HOLD_1_FULL_F_ZERO",
      "locked_source_git_blob_sha1":PINS,
      "real_Minecraft_client_game_actions_run":RUN,
      "original_native_F2_artifact_id":ARTIFACT,
      "original_native_F2_zip_sha256":ZIP_SHA,
      "actual_original_client_log_sha256":game["original_client_log_sha256"],
      "original_mod_jar_sha256":MACAW_SHA256,
      "source_1_5_SHA256":STUDY_SHA256,
      "risk_case":"R06","original_historical_case":"S43",
      "time_separation_seconds":game["time_intervals_seconds"],
      "real_server_state_checks":3,
      "original_native_F2_count":3,
      "source_dry_faces":55,"source_wet_faces":56,
      "direct_original_F2_pixel_review":game["pixel_observation"],
      "water_animation_causally_approved":False,
      "remaining_HOLD_target_ids":["R08"],
      "counts":{"F_target_count":70,"historical_1_5_cases":62,
                "F_conditional_before":68,"F_conditional_after":69,
                "F_HOLD_before":2,"F_HOLD_after":1,
                "historic_F2_before":62,"historic_F2_after":62,
                "F_unconditional_final_approved":0,"INT5_semantics_approved":0,
                "INT6_AI_training_redistribution_rights_approved":0},
      "limits":[
          "Three native F2 at >=8sec intervals, one exact S43 water=true state; not user gameplay.",
          "Pixel change would show sampled images differ, not directly prove animation.",
          "Pixel stability would show sampled still frames, not prove no animation.",
          "Original 1-5 study + previous 69 F ledger rows remain byte unchanged.",
          "R08 official AF 4.0.3 vs 4.0.2 matched state real F2 remains HOLD.",
          "No full F gate, G/H, INT5 semantics or INT6 rights final approval."
      ],
      "output_sha256":{"F70":sha(all70),"pending":sha(pending)},
    }
    md="\n".join([
      "# INT-4-F11E R06 실제 Macaw 싱크 시간차 세 프레임 독립 감사",
      "",
      "- Minecraft 1.21.11 Macaw 3.4.2 원본 S43 물 true 싱크 실제 게임 3시점 네이티브 F2, 8초 이상 간격.",
      "- 각 원본 프레임 전 서버 정확 상태 재조회 3회 PASS; 원본 모델 SHA/JAR SHA256 고정.",
      "- 원본 S42 물 false 16요소·55면 대비 S43 물 true 17요소·56면 (면 +1), 애니메이션 인과 별도.",
      "- 시간 간격(초): "+str(game["time_intervals_seconds"]),
      "- 수면 샘플 판정: "+verdict,
      "- 물 ROI 전경 픽셀: "+str(water)+", 배경 대조 최대 변경 "+str(control)+"px.",
      "- 원본 ZIP SHA256: "+ZIP_SHA+" / Actions 원본 F2 아티팩트 "+str(ARTIFACT),
      "- R06 한 행만 HOLD→CONDITIONAL; 조건부 68→69/70 (98.6%), HOLD 2→1 (R08). 역사62/62 유지.",
      "- 최종 무조건 F 승인 0, 물 기능/움직임 코드 인과·UV·부품 의미·학습/재배포권·G/H 보류.",
      "",
    ]).encode("utf-8")
    return {OUT70:all70,PENDING:pending,AUDIT:jout(summary),REVIEW:md}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,default=Path("tmp-F11E-R06-original"))
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for path,b in build(a.artifact_dir/ZIP_NAME).items():
        destination=ROOT/path
        if a.verify:
            assert destination.is_file() and destination.read_bytes()==b,("NONDETERMINISTIC_R06",str(path))
        else:
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(b)
        print("VERIFIED" if a.verify else "CREATED",path,len(b))
    print("F11E R06 native temporal three F2; F70 conditional69 HOLD1 F-full0")

if __name__=="__main__":
    main()
