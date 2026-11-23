#!/usr/bin/env python3
"""Independent F11A source-locked vanilla 1.21.11 original-F2 adjudication."""
import argparse,csv,hashlib,io,json,os
from pathlib import Path
from zipfile import ZipFile
import urllib.error,urllib.request
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
PREV=OUT/"INT4_F10_70_TARGET_EVIDENCE_DISPOSITIONS_V9.csv"
NEW=OUT/"INT4_F11A_FIVE_VANILLA_REAL_F2_SOURCE_V1.json"
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={str(PREV):"44fdf3672a96afb4956a42cae8c11f195e24535b",
      str(NEW):"7a0773e665d96a683a442c4620b1337ef8da506d",
      str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179"}
RUN=45095295065
ARTIFACT=14783186548
ZIP_NAME="INT4_F11A_VANILLA_FIVE_ORIGINAL_F2.zip"
ZIP_SHA="a72ed16c3665e1511e300fedc388c81ccb0413f5105fcc7b2d6ba49a13dc6827"
CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
STUDY_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
CASES=("V01","V02","V05","V07","V10")
FACE={"V01":11,"V02":6,"V05":6,"V07":6,"V10":6}
ELEMENT={"V01":2,"V02":1,"V05":1,"V07":1,"V10":1}
OBS={
 "V01":"실제 F2에서 계단의 높이 차이가 있는 윗면과 참나무 옆면 관찰",
 "V02":"실제 F2에서 반 블록의 낮은 높이와 참나무 재질을 관찰",
 "V05":"실제 F2에서 참나무 판재 및 통 테두리와 고리 형태를 관찰",
 "V07":"실제 F2에서 갈색 나무 테두리와 여러 색의 책장 책 텍스처를 관찰",
 "V10":"실제 F2에서 참나무 판자 무늬의 정육면체 한 블록을 관찰",
}
OUT70=OUT/"INT4_F11A_70_TARGET_EVIDENCE_DISPOSITIONS_V10.csv"
OUT12=OUT/"INT4_F11A_12_PENDING_EXACT_F2_TARGETS_V1.csv"
AUDIT=OUT/"INT4_F11A_FIVE_VANILLA_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json"
REVIEW=OUT/"INT4_F11A_FIVE_CASE_ORIGINAL_IMAGE_REVIEW_V1.md"

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
    prior=rows(locked(PREV)); cap=json.loads(locked(NEW)); study=rows(locked(STUDY))
    assert len(prior)==70 and len({r["target_id"] for r in prior})==70
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==53
    assert sum(r["final_disposition"].startswith("HOLD") for r in prior)==17
    assert cap["status"]=="PASS_FIVE_OFFICIAL_VANILLA_12111_EXACT_STATE_F2_NOT_FINAL_APPROVAL"
    assert cap["original_historical_case_ids"]==list(CASES)
    assert cap["official_client_sha1"]==CLIENT_SHA1 and cap["official_client_sha256"]==CLIENT_SHA256
    assert cap["source_1_5_ledger_sha256"]==STUDY_SHA
    assert (cap["real_game_server_exact_states"],cap["real_game_native_original_F2_PNG"],
            cap["source_model_applications"],cap["source_elements"],cap["source_faces"])==(5,5,5,6,35)
    assert (cap["full_INT4_F_approved"],cap["INT5_part_semantics_approved"],
            cap["INT6_training_or_distribution_rights_approved"])==(0,0,0)
    study_by={k:[x for x in study if x["case"]==k] for k in CASES}
    assert all(len(v)==1 for v in study_by.values())
    before={r["target_id"]:dict(r) for r in prior}
    assert all(before[k]["final_disposition"].startswith("HOLD") for k in CASES)
    reviewed={}
    with ZipFile(io.BytesIO(archive(archive_path))) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names)) and set(names)=={
          "INT4_F11_VANILLA_FIVE_F2_AUDIT.json",
          "INT4_F11_VANILLA_FIVE_REAL_F2_CAPTURE.json",
          "client.log",*(k+".png" for k in CASES)}
        actual=json.loads(z.read("INT4_F11_VANILLA_FIVE_REAL_F2_CAPTURE.json"))
        audit=json.loads(z.read("INT4_F11_VANILLA_FIVE_F2_AUDIT.json"))
        assert actual["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        assert audit["status"]==cap["status"]
        assert actual["minecraft_version"]=="1.21.11"
        assert actual["source_state_verified_count"]==actual["minecraft_native_f2_screenshot_count"]==5
        assert actual["original_source_registry"]["official_client_jar_sha1"]==CLIENT_SHA1
        assert actual["original_source_registry"]["official_client_jar_sha256"]==CLIENT_SHA256
        assert actual["original_source_registry"]["source_ledger_sha256"]==STUDY_SHA
        assert actual["original_source_registry"]["hash_algorithm"]=="GIT_BLOB_SHA1"
        assert sha(z.read("client.log"))==cap["client_log_sha256"]==audit["client_log_sha256"]==actual["client_log_sha256"]
        observed={r["case_id"]:r for r in actual["states"]}
        assert len(observed)==len(actual["states"])==5 and set(observed)==set(CASES)
        for k in CASES:
            r=study_by[k][0];selected=cap["source_cases"][k];view=observed[k]
            assert r["cohort"]=="VANILLA" and r["minecraft"]=="1.21.11"
            assert r["model_hash_kind"]=="GIT_BLOB_SHA1"
            assert (int(r["elements"]),int(r["faces"]))==(ELEMENT[k],FACE[k])
            props=json.loads(r["state"])
            full="minecraft:"+r["block"]+("["+(",".join(x+"="+v for x,v in props.items()))+"]" if props else "")
            assert selected["original_state"]==view["original_state"]==full
            assert selected["model_path"]==r["model_path"]==view["original_model_path"]
            assert selected["model_git_blob_sha1"]==view["original_model_git_blob_sha1"]==r["model_sha"]
            assert selected["provider_git_blob_sha1"]==view["original_provider_git_blob_sha1"]==r["provider_sha"]
            assert selected["blockstate_git_blob_sha1"]==r["state_sha"]
            assert selected["original_model_y"]==view["original_model_y"]==int(r["y"])
            assert (selected["elements"],selected["faces"])==(ELEMENT[k],FACE[k])
            chain=selected["official_parent_chain_git_blob_sha1"]
            assert len(chain)==(2 if k in ("V05","V07","V10") else 1)
            assert any(x["path"]==r["provider_path"] and x["git_blob_sha1"]==r["provider_sha"] for x in chain)
            assert view["server_state_verified"] and view["native_f2_verified"]
            assert view["screenshot_dimensions"]==[1024,684]
            assert view["semantic_or_rights_approved"] is False
            assert view["screen_foreground_visible_by_color_or_white_proxy"] is True
            assert cap["f2_foreground_chroma"][k]>=35
            raw=z.read(k+".png")
            h=sha(raw)
            assert h==view["screenshot_sha256"]==audit["f2_sha256"][k]==cap["f2_sha256"][k]
            with Image.open(io.BytesIO(raw)) as im:
                im.load()
                assert im.size==(1024,684) and im.format=="PNG"
            reviewed[k]={"block":r["block"],"elements":ELEMENT[k],"faces":FACE[k],
                         "state_exact":True,"original_model_sha1":r["model_sha"],
                         "source_parent_chain":chain,"native_F2_sha256":h,
                         "original_image_visual_observation":OBS[k],
                         "disposition":"CONDITIONAL_SOURCE_AND_REAL_F2_NOT_FINAL"}
    for row in prior:
        k=row["target_id"]
        if k not in CASES:continue
        row.update({
            "prior_f2_evidence_status":"REAL_OFFICIAL_12111_SOURCE_EXACT_NATIVE_F2_F11A",
            "image_artifact_ids":str(ARTIFACT),
            "image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+k+".png",
            "image_sha256s":reviewed[k]["native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":OBS[k],
            "source_state_and_release_assessment":"OFFICIAL_12111_MODEL_PARENT_BLOCKSTATE_GIT_BLOB_SHA1_MATCH",
            "final_disposition":"CONDITIONAL_F11A_EXACT_VANILLA_12111_NATIVE_F2_NOT_FULL_F",
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":"정확한 원본 상태·모델·서버·F2 근거만 수용. UV 픽셀·부품 기능/의미·권리·전체 F 게이트는 별도.",
        })
    assert {r["target_id"] for r in prior if r!=before[r["target_id"]]}==set(CASES)
    pending=[r for r in prior if r["final_disposition"].startswith("HOLD")]
    assert len(pending)==12
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==58
    historical=[r for r in prior if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(historical)==62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in historical)==52
    remains={"V03","V04","V06","V08","V09","V11","V12","V13","V14","V15","R06","R08"}
    assert {r["target_id"] for r in pending}==remains
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in prior)
    c70=csvout(prior,list(prior[0]))
    columns=("target_id","cohort","minecraft_version","category","block",
             "original_source_applications","original_source_faces",
             "final_disposition","additional_required_before_full_acceptance")
    cp=csvout([{k:r[k] for k in columns} for r in pending],list(columns))
    summary={
      "schema":"MCFR_INT4_F11A_5_VANILLA_ORIGINAL_12111_F2_INDEPENDENT_AUDIT/v1",
      "status":"PASS_FIVE_REAL_VANILLA_F2_58_CONDITIONAL_12_HOLD_FULL_ZERO",
      "pinned_source_git_blob_SHA1":PINS,
      "official_mojang_12111_client_sha1":CLIENT_SHA1,
      "official_mojang_12111_client_sha256":CLIENT_SHA256,
      "original_real_game_run":RUN,
      "original_real_game_artifact":ARTIFACT,
      "original_real_game_zip_sha256":ZIP_SHA,
      "original_client_log_sha256":cap["client_log_sha256"],
      "cases":reviewed,
      "pending_HOLD_ids":sorted(remains),
      "counts":{"F_fixed_targets":70,"historic_source_cases":62,
                "new_real_client_exact_states":5,"new_native_original_F2":5,
                "new_model_applications":5,"new_elements":6,"new_faces":35,
                "F_conditional_before":53,"F_conditional_after":58,
                "F_HOLD_before":17,"F_HOLD_after":12,
                "historical_original_F2_conditional_before":47,
                "historical_original_F2_conditional_after":52,
                "F_full_approved":0,"INT5_semantics_new_approved":0,
                "INT6_AI_training_redistribution_rights_approved":0},
      "limits":["Five actual native F2 are qualitative visual evidence, not GPU pixel UV causality.",
                "V05/V07/V10 final geometry carrier is two parent hops, not direct parent.",
                "Other 65 F10 case rows and original 1-5 study were not changed.",
                "V03,V04,V06,V08,V09,V11-V15 and R06/R08 are not accepted in this batch.",
                "No original Minecraft client, models or PNGs committed to Git.",
                "No final F approval or G/H/INT5/INT6 acceptance."],
      "output_sha256":{"F70":sha(c70),"pending":sha(cp)}
    }
    md="\n".join([
      "# INT-4-F11A 바닐라 1.21.11 5개 사례 실제 F2 독립 감사",
      "",
      "- 공식 Minecraft 1.21.11 실제 게임 Actions #"+str(RUN)+" 성공. 아티팩트 #"+str(ARTIFACT)+"에 원본 F2 5개·client.log 보관.",
      "- V01 계단(2요소·11면), V02 하단 반 블록, V05 닫힌 통, V07 책장, V10 참나무 판자(각 1요소·6면). 총 5역사 사례/6요소/35면.",
      "- 원본 selected leaf/parent/source state Git blob SHA1, 공식 클라이언트 SHA256/1, 서버 상태, PNG 및 로그 원본 해시 모두 검증.",
      "- V05: barrel → cube_bottom_top → cube. V07: bookshelf → cube_column → cube. V10: oak_planks → cube_all → cube. 직접 부모와 기하 제공자 구분.",
      "- 실제 PNG 다섯 장을 재열람해 계단 단차·반 블록 얇은 두께·통의 고리·책장 책·나무 판자 큐브를 확인함.",
      "- 고정 F70 조건부 53→58/70, HOLD 17→12/70. 역사 원본 사례 조건부 F2 47→52/62. 최종 무조건 승인 0.",
      "- 남은 V03 V04 V06 V08 V09 V11 V12 V13 V14 V15 및 R06 R08은 별도. 기능/UV/의미/AI 이용권 최종 승인 없음.",
      "",
    ]).encode("utf-8")
    return {OUT70:c70,OUT12:cp,AUDIT:jout(summary),REVIEW:md}

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
    print("F11A verified 70 targets conditional58 HOLD12 fullF0")

if __name__=="__main__":main()
