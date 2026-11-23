#!/usr/bin/env python3
"""F11C independent original Mojang 1.21.11 source+native F2 audit.

Only V12-V15 are eligible for conditional source/static F2 linkage.
V11 ordinary-model-zero bed stays HOLD, as do time risk R06 and version risk R08.
"""
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
import urllib.error,urllib.request
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PREV=OUT/"INT4_F11B_70_TARGET_EVIDENCE_DISPOSITIONS_V11.csv"
NEW=OUT/"INT4_F11C_FOUR_VANILLA_REAL_F2_SOURCE_V1.json"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={str(PREV):"962bcb50ba28dfbc10ba668069ed22f2a55798e4",
      str(NEW):"f150816ec73b31d617040822d190b9a61ffe058d",
      str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179"}
RUN=45100631875
ARTIFACT=14784814227
ZIP_NAME="INT4_F11C_FOUR_ORIGINAL_F2.zip"
ZIP_SHA="99f27ecfc1c284b03d4a5a1f29f332f849b3d3247dc5cd801694620f54ce6eaa"
CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
STUDY_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
CASES=("V12","V13","V14","V15")
GEOMETRY={"V12":(13,58),"V13":(14,59),"V14":(4,15),"V15":(5,22)}
OBS={
 "V12":"원본 F2에서 비어 있는 회색 벽과 안쪽 공간이 있는 가마솥 형태 관찰",
 "V13":"원본 F2에서 가마솥 윗부분의 물 표면과 용기 외형 관찰, 시간차 애니메이션 미검증",
 "V14":"원본 F2에서 매달리지 않은 소형 랜턴 외형 관찰, 전체 애니메이션 프레임 미검증",
 "V15":"원본 F2에서 낮은 적갈색 빈 화분 외형 관찰",
}
OUT70=OUT/"INT4_F11C_70_TARGET_EVIDENCE_DISPOSITIONS_V12.csv"
OUT3=OUT/"INT4_F11C_3_PENDING_EXACT_F2_TARGETS_V1.csv"
AUDIT=OUT/"INT4_F11C_FOUR_VANILLA_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
REVIEW=OUT/"INT4_F11C_FOUR_CASE_ORIGINAL_IMAGE_REVIEW_V1.md"

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
        if not token:raise FileNotFoundError("Original F11C Actions artifact and GH_TOKEN both missing")
        api=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT}/zip"
        heads={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
               "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-F11C-original-F2-audit"}
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
                 location,headers={"User-Agent":"MCFR-F11C-original-F2-audit"}),timeout=120) as response:
                data=response.read()
        assert sha(data)==ZIP_SHA,("ORIGINAL_REMOTE_ZIP_CHANGED",sha(data))
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    assert sha(data)==ZIP_SHA,("ORIGINAL_ZIP_CHANGED",sha(data))
    return data

def build(original_zip_path):
    prior=rows(locked(PREV))
    captured=json.loads(locked(NEW))
    study=rows(locked(STUDY))
    assert len(prior)==70 and len({x["target_id"] for x in prior})==70
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior)==63
    assert sum(x["final_disposition"].startswith("HOLD") for x in prior)==7
    assert captured["status"]=="PASS_FOUR_MOJANG_12111_EXACT_VANILLA_STATES_NATIVE_F2_NOT_FINAL"
    assert captured["historical_case_ids"]==list(CASES)
    assert (captured["real_game_exact_server_states"],captured["original_native_F2_PNG"],
            captured["original_source_model_applications"],
            captured["original_source_elements"],captured["original_source_faces"])==(4,4,4,36,154)
    assert (captured["official_client_sha1"],captured["official_client_sha256"],
            captured["original_1_5_ledger_sha256"])==(CLIENT_SHA1,CLIENT_SHA256,STUDY_SHA)
    assert (captured["unconditionally_full_F_approved"],captured["INT5_part_semantics_approved"],
            captured["INT6_training_or_redistribution_rights_approved"])==(0,0,0)
    grouped={k:[x for x in study if x["case"]==k] for k in CASES}
    assert all(len(v)==1 for v in grouped.values())
    prior_by={x["target_id"]:dict(x) for x in prior}
    assert all(prior_by[k]["final_disposition"].startswith("HOLD") for k in CASES)
    checked={}
    with ZipFile(io.BytesIO(archive(original_zip_path))) as z:
        assert z.testzip() is None
        files=z.namelist()
        assert len(files)==len(set(files))
        assert set(files)=={
            "INT4_F11C_VANILLA_FOUR_REAL_F2_CAPTURE.json",
            "INT4_F11C_VANILLA_FOUR_F2_AUDIT.json",
            "client.log",*(k+".png" for k in CASES)}
        manifest=json.loads(z.read("INT4_F11C_VANILLA_FOUR_REAL_F2_CAPTURE.json"))
        gameaudit=json.loads(z.read("INT4_F11C_VANILLA_FOUR_F2_AUDIT.json"))
        assert manifest["schema"]=="MCFR_INT4_F11C_VANILLA_FOUR_REAL_F2/v1"
        assert manifest["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        assert manifest["minecraft_version"]=="1.21.11"
        assert manifest["source_state_verified_count"]==manifest["minecraft_native_f2_screenshot_count"]==4
        assert gameaudit["status"]==captured["status"]
        original_source=manifest["original_source_registry"]
        assert (original_source["official_client_jar_sha1"],
                original_source["official_client_jar_sha256"],
                original_source["source_ledger_sha256"])==(CLIENT_SHA1,CLIENT_SHA256,STUDY_SHA)
        assert original_source["hash_algorithm"]=="GIT_BLOB_SHA1"
        assert original_source["states"]==captured["source_cases"]
        logdata=z.read("client.log")
        assert sha(logdata)==manifest["client_log_sha256"]==captured["client_log_sha256"]==gameaudit["client_log_sha256"]
        log=logdata.decode("utf-8",errors="replace")
        # Independent real-image water control. These original F2 images
        # have the same relative camera/stone stage, but different cauldron
        # water level. This is NOT temporal animation evidence.
        with Image.open(io.BytesIO(z.read("V12.png"))) as empty, Image.open(
            io.BytesIO(z.read("V13.png"))
        ) as filled:
            r=(475,390,555,450)
            aa=empty.convert("RGB").crop(r)
            bb=filled.convert("RGB").crop(r)
            water_delta=sum(1 for a,b in zip(aa.getdata(),bb.getdata())
                            if max(abs(x-y) for x,y in zip(a,b))>=24)
        assert water_delta>=800
        assert captured["native_F2_visibility_pixels"]["V13"]["paired_water_difference"]==water_delta
        observations={r["case_id"]:r for r in manifest["states"]}
        assert len(observations)==len(manifest["states"])==4 and set(observations)==set(CASES)
        for case in CASES:
            studyrow=grouped[case][0]
            model=captured["source_cases"][case]
            real=observations[case]
            assert studyrow["cohort"]=="VANILLA" and studyrow["minecraft"]=="1.21.11"
            assert studyrow["geometry_status"]=="STATIC_SOURCE"
            assert studyrow["model_hash_kind"]=="GIT_BLOB_SHA1"
            assert (int(studyrow["elements"]),int(studyrow["faces"]))==GEOMETRY[case]
            props=json.loads(studyrow["state"])
            exact="minecraft:"+studyrow["block"]+(
                "["+(",".join(k+"="+v for k,v in props.items()))+"]" if props else "")
            assert model["original_state"]==real["original_state"]==exact
            assert model["model_path"]==studyrow["model_path"]==real["original_model_path"]
            assert model["model_git_blob_sha1"]==studyrow["model_sha"]==real["original_model_git_blob_sha1"]
            assert model["provider_git_blob_sha1"]==studyrow["provider_sha"]==real["original_provider_git_blob_sha1"]
            assert model["blockstate_git_blob_sha1"]==studyrow["state_sha"]
            assert model["original_model_y"]==int(studyrow["y"])==real["original_model_y"]
            assert (model["elements"],model["faces"])==GEOMETRY[case]
            chain=model["official_parent_chain_git_blob_sha1"]
            if studyrow["model_path"]==studyrow["provider_path"]:
                assert len(chain)==0
            else:
                assert any(x["path"]==studyrow["provider_path"] and
                           x["git_blob_sha1"]==studyrow["provider_sha"] for x in chain)
            assert real["server_state_verified"] is True
            assert real["native_f2_verified"] is True
            assert real["screenshot_dimensions"]==[1024,684]
            assert real["screen_foreground_visible_by_color_or_white_proxy"] is True
            assert real["semantic_or_rights_approved"] is False
            assert "[RenderAudit] MCFR_CHAIR_STATE_"+case+"=PASS" in log
            assert "[RenderAudit] MCFR_CHAIR_STATE_"+case+"=FAIL" not in log
            if case=="V12":
                assert real["screen_foreground_neutral_dark_pixels"]>=200
                assert captured["native_F2_visibility_pixels"][case]["dark_gray"]>=200
            png=z.read(case+".png")
            digest=sha(png)
            assert digest==real["screenshot_sha256"]==captured["native_F2_sha256"][case]==gameaudit["native_F2_sha256"][case]
            with Image.open(io.BytesIO(png)) as image:
                image.load()
                assert image.format=="PNG" and image.size==(1024,684)
            checked[case]={
                "water_vs_empty_original_F2_delta_pixels":water_delta if case=="V13" else 0,
                "original_block":studyrow["block"],
                "exact_original_state":exact,
                "original_model_git_blob_sha1":studyrow["model_sha"],
                "original_geometry_provider_git_blob_sha1":studyrow["provider_sha"],
                "source_elements":int(studyrow["elements"]),
                "source_faces":int(studyrow["faces"]),
                "actual_original_native_F2_sha256":digest,
                "original_F2_direct_visual_observation":OBS[case],
                "server_exact_state":True,
                "conditional_source_F2_only":True,
            }
    for item in prior:
        key=item["target_id"]
        if key not in CASES:continue
        item.update({
            "prior_f2_evidence_status":"OFFICIAL_12111_F11C_ORIGINAL_4_NATIVE_F2_AND_EXACT_SERVER",
            "image_artifact_ids":str(ARTIFACT),
            "image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+key+".png",
            "image_sha256s":checked[key]["actual_original_native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":OBS[key],
            "source_state_and_release_assessment":"PINNED_MOJANG_12111_SOURCE_BLOCKSTATE_SELECTED_MODEL_GEOMETRY_AND_GAME_F2",
            "final_disposition":"CONDITIONAL_F11C_VANILLA_EXACT_STATIC_F2_NOT_ANIMATION_FINAL",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":
                "실게임 상태·원본 모델·네이티브 정지 F2 조건부. 수면/랜턴 시간 애니메이션, UV 인과, 기능, 의미, 권리 별도.",
        })
    assert {x["target_id"] for x in prior if x!=prior_by[x["target_id"]]}==set(CASES)
    waiting=[x for x in prior if x["final_disposition"].startswith("HOLD")]
    assert len(waiting)==3
    assert {x["target_id"] for x in waiting}=={"V11","R06","R08"}
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior)==67
    historical=[x for x in prior if x["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(historical)==62
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in historical)==61
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in prior)
    full=csvout(prior,list(prior[0].keys()))
    fields=("target_id","cohort","minecraft_version","category","block",
            "original_source_applications","original_source_faces","final_disposition",
            "additional_required_before_full_acceptance")
    pend=csvout([{k:r[k] for k in fields} for r in waiting],list(fields))
    result={
        "schema":"MCFR_INT4_F11C_4_VANILLA_ORIGINAL_12111_F2_INDEPENDENT_AUDIT/v1",
        "status":"PASS_FOUR_MOJANG_12111_NATIVE_F2_CONDITIONAL_67_HOLD_3_FINAL_ZERO",
        "pinned_study_source_git_blob_sha1":PINS,
        "official_client_sha1":CLIENT_SHA1,"official_client_sha256":CLIENT_SHA256,
        "real_original_game_actions_run":RUN,"real_original_game_artifact_id":ARTIFACT,
        "real_native_original_zip_sha256":ZIP_SHA,
        "real_original_game_client_log_sha256":captured["client_log_sha256"],
        "cases":checked,"remaining_HOLD_ids":["R06","R08","V11"],
        "counts":{
            "fixed_F_target_count":70,"historical_1_5_cases":62,
            "new_real_game_exact_states":4,"new_original_native_F2":4,
            "new_original_selected_model_applications":4,"new_original_elements":36,
            "new_original_faces":154,"F_conditional_before":63,"F_conditional_after":67,
            "F_HOLD_before":7,"F_HOLD_after":3,
            "historical_F2_conditional_before":57,"historical_F2_conditional_after":61,
            "F_unconditionally_accepted":0,
            "new_INT5_semantic_part_approvals":0,
            "new_INT6_training_redistribution_rights_approvals":0,
        },
        "limits":[
           "V11 white bed 0 ordinary JSON elements and special renderer not accepted.",
           "V13 water cauldron / V14 lantern include animated texture facets; a still F2 does not validate time.",
           "R06 water sink animated two-time frame and R08 matched different AF releases remain HOLD.",
           "Exact game and source evidence is conditional, not GPU pixel UV causality, functionality or material semantics.",
           "Previous 66 F target rows and frozen 1-5 study unchanged.",
           "No game PNG/JAR/models committed to Git; no F unconditional, G/H, INT5 or INT6 approval.",
        ],
        "output_SHA256":{"F70":sha(full),"pending":sha(pend)},
    }
    md="\n".join([
        "# INT-4-F11C 바닐라 가마솥·물·랜턴·화분 4건 실제 F2 재감사",
        "",
        "- 공식 Minecraft 1.21.11 원본 클라이언트 SHA1/256, 역사 1-5 Git blob SHA1, 실게임 네이티브 F2 4장을 독립 감사함.",
        "- Actions 원본 런 "+str(RUN)+" / 아티팩트 "+str(ARTIFACT)+" / 원본 ZIP SHA256 "+ZIP_SHA,
        "- V12 빈 가마솥 13요소 58면, V13 물 가마솥(level=3) 14요소 59면, V14 랜턴(hanging=false) 4요소 15면, V15 화분 5요소 22면.",
        "- 총 4개 역사 사례, 모델4·36요소·154면. 공식 클라이언트 source/parent Git blob SHA, 실제 서버 상태, 원본 4개 이미지와 client.log SHA 대조.",
        "- 바닐라 V13 수면 일부, V14 랜턴의 원본 텍스처에 애니메이션 면이 존재하지만 이번 것은 정지 F2이지 시간차 인과 검증이 아님.",
        "- 70개 조건부 63→67, HOLD 7→3; 역사 원본 57/62→61/62. 최종 무조건 승인 0.",
        "- 남은 V11 특수 렌더 침대, R06 물 싱크 시간차, R08 AF 두 버전 동일 상태 실게임 비교. G/H 및 INT5/INT6 보류.",
        "",
    ]).encode("utf-8")
    return {OUT70:full,OUT3:pend,AUDIT:jout(result),REVIEW:md}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,default=Path("temporary-F11C-original-F2"))
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    for path,data in build(args.artifact_dir/ZIP_NAME).items():
        out=ROOT/path
        if args.verify:
            assert out.is_file() and out.read_bytes()==data,("NONDETERMINISTIC_F11C",str(path))
        else:
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(data)
        print("VERIFIED" if args.verify else "CREATED",path,len(data))
    print("PASS F11C original 4 PNG, 4 selected models, F70 conditional67 HOLD3 full0")

if __name__=="__main__":
    main()
