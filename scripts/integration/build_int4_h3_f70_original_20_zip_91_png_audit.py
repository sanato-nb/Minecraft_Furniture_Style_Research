#!/usr/bin/env python3
"""INT-4-H3: reopen EVERY referenced historical native F2 artifact.

The pinned F11F F70 ledger records 70 targets, 91 PNG occurrences and 20
distinct GitHub Actions artifacts. This script downloads actual original
archive bytes with Actions read permission, verifies each source ZIP SHA256,
ZIP CRC, each PNG SHA256 and image decoder, metadata action/run IDs, and
rebuilds deterministic evidence-only ledgers. PNG decoding is NOT equivalent
to independent human scene appraisal or all original server logs/state tests.
"""
from __future__ import annotations

import argparse,csv,hashlib,io,json,os,urllib.error,urllib.request
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile, BadZipFile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
LEDGER=I/"INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"
LEDGER_BLOB="0cfbf3b1b174efc968de35c8466e2af8a9cd41c7"
REPO="sanato-nb/Minecraft_Furniture_Style_Research"
OUT_ARCHIVES=I/"INT4_H3_20_ORIGINAL_ARTIFACT_ZIP_SHA_AUDIT_V1.csv"
OUT_IMAGES=I/"INT4_H3_91_NATIVE_F2_ORIGINAL_PNG_SHA_AUDIT_V1.csv"
OUT_TARGETS=I/"INT4_H3_70_CASE_ORIGINAL_F2_REOPEN_V1.csv"
OUT_JSON=I/"INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"
OUT_MD=I/"INT4_H3_F70_20_ARCHIVES_91_PNG_REOPEN_REPORT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(data):return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"),newline="")))
def csvout(data,header=None):
    f=io.StringIO(newline="")
    writer=csv.DictWriter(f,fieldnames=header or list(data[0]),lineterminator="\n")
    writer.writeheader();writer.writerows(data)
    return f.getvalue().encode("utf-8")
def write(path,data,verify):
    target=ROOT/path
    if verify:
        assert target.exists() and target.read_bytes()==data,("NONDETERMINISTIC_RESULT",str(path))
    else:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    return {"sha256":sha(data),"size_bytes":len(data)}

def require_token():
    token=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:raise RuntimeError("GITHUB_TOKEN with Actions:read required to reopen original bytes")
    return token
def headers():
    return {"Authorization":"Bearer "+require_token(),
            "Accept":"application/vnd.github+json",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"MCFR-INT4-H3-F70-full-native-F2-original-reopen"}
def get_api(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers()),timeout=75) as resp:
        return json.load(resp)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def download_artifact(art, cache):
    id=art["artifact_id"]
    dest=cache/(id+".zip")
    if dest.is_file():blob=dest.read_bytes()
    else:
        url=f"https://api.github.com/repos/{REPO}/actions/artifacts/{id}/zip"
        try:
            with urllib.request.build_opener(NoRedirect).open(
                urllib.request.Request(url,headers=headers()),timeout=120) as response:
                blob=response.read()
        except urllib.error.HTTPError as error:
            if error.code not in (301,302,303,307,308):
                raise
            redirect=error.headers.get("Location","")
            parts=urlsplit(redirect)
            assert parts.scheme=="https" and parts.netloc and parts.netloc!="api.github.com",(
                "UNSAFE_ARTIFACT_REDIRECT",id)
            with urllib.request.urlopen(urllib.request.Request(
                redirect,headers={"User-Agent":"MCFR-INT4-H3-original-F2"}),timeout=120) as response:
                blob=response.read()
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(blob)
    assert len(blob)>150,("EMPTY_ARCHIVE",id)
    outer_sha=sha(blob)
    expected=art["expected_zip_sha256"]
    # Some artifact packaging retains a separately named inner historical
    # ZIP; only accept the exact author-pinned original digest, never a
    # replacement archive with arbitrary PNG files.
    if outer_sha==expected:
        origin=blob
        zip_kind="ACTIONS_ARCHIVE_ORIGINAL_SHA256"
        zip_member=""
    else:
        with ZipFile(io.BytesIO(blob)) as z:
            assert z.testzip() is None
            inner=[n for n in z.namelist() if n.lower().endswith(".zip")]
            candidate=[(n,z.read(n)) for n in inner if sha(z.read(n))==expected]
            assert len(candidate)==1,("ARCHIVE_SHA_MISMATCH_NO_PINNED_INNER",id,outer_sha,expected,inner[:15])
            zip_member,origin=candidate[0]
        zip_kind="PINNED_ZIP_INSIDE_ACTIONS_ARCHIVE"
    assert sha(origin)==expected,("ORIGINAL_SOURCE_SHA_DRIFT",id)
    with ZipFile(io.BytesIO(origin)) as z:
        assert z.testzip() is None,("ORIGINAL_ZIP_CRC_FAIL",id)
        namelist=z.namelist()
        assert len(namelist)==len(set(namelist)),("DUPLICATE_ZIP_MEMBERS",id)
        pngs=[n for n in namelist if n.lower().endswith(".png")]
        logs=[n for n in namelist if n.lower().endswith(".log")]
        assert pngs,("NO_ORIGINAL_NATIVE_PNG_IN_ARTIFACT",id)
    return {"artifact_id":id,"original_blob":origin,"archive_byte_sha256":expected,
            "outer_sha256":outer_sha,"zip_kind":zip_kind,"inner_zip_member":zip_member,
            "native_png_member_count":len(pngs),"log_member_count":len(logs),
            "original_zip_member_count":len(namelist)}

def split_multiples(value):
    return [p.strip() for p in value.replace(";","|").split("|") if p.strip()]
def expand(r):
    files=split_multiples(r["image_files"])
    digests=split_multiples(r["image_sha256s"])
    artifacts=split_multiples(r["image_artifact_ids"])
    runs=split_multiples(r["image_run_ids"])
    archives=split_multiples(r["original_zip_sha256s"])
    assert files and len(digests)==len(files),("PNG_REFERENCE_COUNT_MISMATCH",r["target_id"])
    assert len(artifacts) in (1,len(files)),("ARTIFACT_REFERENCE_COUNT_MISMATCH",r["target_id"])
    assert len(runs) in (1,len(files)),("RUN_REFERENCE_COUNT_MISMATCH",r["target_id"])
    assert len(archives) in (1,len(files)),("ZIP_REFERENCE_COUNT_MISMATCH",r["target_id"])
    assert all(len(v)==64 for v in digests+archives),("MALFORMED_SHA",r["target_id"])
    lastarchive=None
    out=[]
    for n,file in enumerate(files):
        if ":" in file:
            archive,photo=file.split(":",1)
            assert archive.lower().endswith(".zip")
            lastarchive=archive
        else:
            assert lastarchive is not None,("MISSING_PRECEDING_ZIP_PREFIX",r["target_id"])
            archive,photo=lastarchive,file
        assert not photo.startswith("/") and ".." not in Path(photo).parts and photo.lower().endswith(".png")
        out.append({
            "target_id":r["target_id"],
            "target_kind":r["target_kind"],
            "original_target_status":r["final_disposition"],
            "reference_index":n,
            "declared_source_zip_filename":archive,
            "declared_native_png_member":photo,
            "artifact_id":artifacts[n] if len(artifacts)==len(files) else artifacts[0],
            "run_id":runs[n] if len(runs)==len(files) else runs[0],
            "expected_zip_sha256":archives[n] if len(archives)==len(files) else archives[0],
            "expected_png_sha256":digests[n],
        })
    return out

def find_member(z,member):
    names=z.namelist()
    if member in names:return member
    if "./"+member in names:return "./"+member
    candidates=[n for n in names if n.endswith("/"+member)]
    assert len(candidates)==1,("ORIGINAL_PNG_MEMBER_UNRESOLVED",member,candidates[:5],
                              [n for n in names if n.lower().endswith(".png")][:12])
    return candidates[0]

def build(cache, verify=False):
    ledgerbytes=(ROOT/LEDGER).read_bytes()
    assert gitblob(ledgerbytes)==LEDGER_BLOB,("ORIGINAL_F70_LEDGER_GIT_BLOB_DRIFT")
    targets=rows(ledgerbytes)
    assert len(targets)==70 and len({r["target_id"] for r in targets})==70
    assert sum(r["target_kind"]=="HISTORICAL_1_5_CASE" for r in targets)==62
    assert sum(r["target_kind"]=="RISK_SCENARIO" for r in targets)==8
    assert all(r["final_disposition"].startswith("CONDITIONAL")
               and r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in targets)
    refs=[ref for r in targets for ref in expand(r)]
    assert len(refs)==91,("EXPECTED_91_F2_REFERENCES",len(refs))
    archives={}
    for e in refs:
        key=e["artifact_id"]
        if key in archives:
            old=archives[key]
            assert (old["expected_zip_sha256"],old["run_id"])==(
                e["expected_zip_sha256"],e["run_id"]),("CONFLICTING_ARTIFACT_PINS",key)
        else:
            archives[key]={"artifact_id":key,
                "expected_zip_sha256":e["expected_zip_sha256"],"run_id":e["run_id"]}
    assert len(archives)==20,("EXPECTED_20_DISTINCT_ORIGINAL_ARTIFACTS",len(archives))
    assert len({e["run_id"] for e in refs})==19
    remote={}
    for key in sorted(archives,key=int):
        meta=get_api(f"https://api.github.com/repos/{REPO}/actions/artifacts/{key}")
        assert str(meta["id"])==key and meta["expired"] is False,("ARTIFACT_EXPIRED_OR_CHANGED",key)
        assert meta["size_in_bytes"]>100
        if "workflow_run" in meta and meta["workflow_run"]:
            assert str(meta["workflow_run"]["id"])==archives[key]["run_id"],(
                "MISMATCH_ARTIFACT_WORKFLOW_RUN",key)
        remote[key]={
          "id":key,"name":meta["name"],"run_id":archives[key]["run_id"],
          "expected_zip_sha256":archives[key]["expected_zip_sha256"],
          "artifact_size_bytes":meta["size_in_bytes"],
          "expired":meta["expired"]}
    # Download at most four original archive bytes at once; no artist asset
    # is checked into Git and no author JAR/texture is redistributed.
    collected={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(download_artifact,art,cache):key for key,art in archives.items()}
        for future in as_completed(futures):
            key=futures[future]
            collected[key]=future.result()
    results=[]
    for ref in refs:
        source=collected[ref["artifact_id"]]
        with ZipFile(io.BytesIO(source["original_blob"])) as zin:
            file=find_member(zin,ref["declared_native_png_member"])
            png=zin.read(file)
        actual=sha(png)
        assert actual==ref["expected_png_sha256"],(
            "F2_ORIGINAL_PNG_HASH_MISMATCH",ref["target_id"],file,actual)
        with Image.open(io.BytesIO(png)) as im:
            im.load()
            assert im.format=="PNG" and im.size[0]>64 and im.size[1]>64,(
                "INVALID_ORIGINAL_PNG",ref["target_id"],file)
            width,height=im.size
        results.append({
            "target_id":ref["target_id"],"target_kind":ref["target_kind"],
            "artifact_id":ref["artifact_id"],"run_id":ref["run_id"],
            "recorded_zip_name":ref["declared_source_zip_filename"],
            "original_recorded_png_path":ref["declared_native_png_member"],
            "original_real_zip_png_member":file,
            "recorded_zip_sha256":ref["expected_zip_sha256"],
            "verified_original_png_sha256":actual,
            "expected_original_png_sha256":ref["expected_png_sha256"],
            "actual_png_width":width,"actual_png_height":height,
            "original_png_bytes":len(png),
            "artifact_original_zip_sha_and_png_reopened":"PASS",
            "actual_visible_game_state_and_model_independently_reapproved":"false",
            "full_F_contract_approved":"false",
        })
    assert len(results)==91 and {r["target_id"] for r in results}=={r["target_id"] for r in targets}
    adata=[]
    for key in sorted(archives,key=int):
        meta=remote[key]
        source=collected[key]
        adata.append({
            "artifact_id":key,"original_run_id":meta["run_id"],
            "original_gitHub_artifact_name":meta["name"],
            "source_expected_original_zip_sha256":meta["expected_zip_sha256"],
            "source_reopened_zip_sha256":source["archive_byte_sha256"],
            "actions_artifact_transport_sha256":source["outer_sha256"],
            "zip_verified_form":source["zip_kind"],
            "inner_zip_member_when_applicable":source["inner_zip_member"],
            "original_zip_members":source["original_zip_member_count"],
            "original_zip_png_members":source["native_png_member_count"],
            "original_zip_log_members":source["log_member_count"],
            "number_of_referenced_png_occurrences":sum(x["artifact_id"]==key for x in refs),
            "github_artifact_unexpired":"true","original_zip_crc_pass":"true",
            "unconditional_F_acceptance":"false",
        })
    target_rows=[]
    grouped=defaultdict(list)
    for ref in results:grouped[ref["target_id"]].append(ref)
    for t in targets:
        native=grouped[t["target_id"]]
        assert native
        target_rows.append({
            "target_id":t["target_id"],"target_kind":t["target_kind"],
            "original_F_status":t["final_disposition"],
            "reopened_original_PNG_occurrences":len(native),
            "unique_artifact_ids":len({r["artifact_id"] for r in native}),
            "all_expected_image_bytes_SHA_accepted":"true",
            "original_image_format_decode_verified":"true",
            "per_case_server_log_state_independently_reaudited":"false",
            "per_case_original_visual_appearance_human_reapproved":"false",
            "full_F_contract_accepted":"false",
        })
    out_a=csvout(adata)
    out_i=csvout(results)
    out_t=csvout(target_rows)
    output_meta={
        "schema":"MCFR_INT4_H3_ALL_20_ORIGINAL_ARTIFACTS_91_NATIVE_F2_PNG_BYTES/v1",
        "status":"PASS_ALL_F70_ORIGINAL_PNG_ARCHIVE_SHA_AND_CRC_NO_FULL_F_CONTRACT",
        "original_F70_git_blob_SHA1":LEDGER_BLOB,
        "fixed_case_count":70,
        "historical_1_5_cases":62,
        "risk_scenarios":8,
        "recorded_original_PNG_occurrences":91,
        "original_distinct_actions_archive_downloaded":20,
        "original_distinct_actions_runs":19,
        "original_actions_artifacts_expired":0,
        "all_20_archive_expected_zip_sha256_verified":True,
        "all_20_archive_CRC_checked":True,
        "all_91_native_F2_PNG_sha256_verified":True,
        "all_91_PNG_decoded":True,
        "native_F2_new_visual_human_per_case_review_performed":False,
        "every_original_case_server_state_log_reopened_and_reapproved":False,
        "F_unconditional_full_exit_approved":0,
        "G_unconditional_exit_approved":0,
        "H_full_exit_approved":0,
        "INT5_semantics_approved":0,
        "INT6_artist_training_or_redistribution_rights_approved":0,
        "limits":[
            "Every documented original screenshot is reopened byte-for-byte and SHA matched; this does not replace independent scene interpretation.",
            "The source F70 ledger records 91 PNG occurrences, and some may be identical/shared by cases or repeated scenarios.",
            "Archived run/artifact metadata is linked by artifact ID; independent per-case gameplay state and log interpretation remains outstanding.",
            "The original model/game release SHA and runtime F2 interpretation remain conditional from prior independent studies.",
            "A genuine screenshot can match SHA but prove only its photographed time/state, not all UV faces or version-wide equivalence.",
            "No original PNG/JAR is committed or redistributed in repository changes.",
        ],
        "outputs":{
            "artifact20_sha256":sha(out_a),
            "png91_sha256":sha(out_i),
            "target70_sha256":sha(out_t),
        },
    }
    summary=(json.dumps(output_meta,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    files={
       OUT_ARCHIVES:out_a,OUT_IMAGES:out_i,OUT_TARGETS:out_t,OUT_JSON:summary,
    }
    for path,blob in files.items():write(path,blob,verify)
    md=[
       "# INT-4-H3 원본 F70 아카이브 20개·PNG 증거 91건 직접 재검수",
       "",
       "- 역사 원장 고정 F70 SHA, 사례 62개+위험 8개, PNG 참조 91건, 원본 Actions artifact ZIP 20개/실행 19건.",
       "- GitHub Actions 원본 아티팩트 재다운로드, 원래 SHA256, 원본 ZIP CRC, 원본 PNG 91개 전체 SHA256 및 PNG 디코딩을 실제 검사.",
       "- 같은 F2가 연구 사례와 R 위험에 재사용된 경우 한 번의 원본 PNG가 두 개의 별도 실게임 실험이라고 재계산하지 않음.",
       "- **이 검사는 원본 파일 bytes/CRC 존재를 입증하지만, 화면의 가구 상태·모델·UV를 새로 사람처럼 판독하거나 전체 서버 로그의 인과를 승인한 것이 아님.**",
       "- H05 원본 ZIP/PNG SHA 재열람 차단 문제는 대상 범위에서 해소할 수 있지만 원래 F 계약의 실화면/서버 인과는 별도.",
       "- F/G/H 무조건 종료 승인, INT5 의미, INT6 AI 훈련/재배포 권한 승인 전부 0 유지.",
       "",
    ]
    write(OUT_MD,("\n".join(md)+"\n").encode("utf-8"),verify)
    print(json.dumps({"status":output_meta["status"],"artifacts":20,"original_PNG":91,
        "cases":70,"full_F_exit":0,"all_original_PNG_sha_matched":True},ensure_ascii=False))
    return output_meta

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cache",required=True,type=Path)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    build(args.cache,args.verify)
if __name__=="__main__":main()
