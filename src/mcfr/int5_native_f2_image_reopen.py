"""INT-5-B2: reopen original 16 native client F2 PNG + 229 source UV faces.

Real PNG bytes are downloaded into a transient CI directory, decoded and hash
checked. Prior source roles are NOT promoted to proven object functions, texture
rights or per-element game pixel identity. Limited human scene annotations were
made after personally inspecting all 16 reopened native F2 screenshots.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[2]
D=Path("project/integration")
GITHUB_REPO="sanato-nb/Minecraft_Furniture_Style_Research"
PINS={
 "INT5_B_45_ELEMENT_TEXTURING_F2_SOURCE_BRIDGE_V1.csv":"f7ca2ab4b6764df53369213b6772f5ff51525e65",
 "INT5_B_VISUAL_SOURCE_BRIDGE_RESULT_V1.json":"ce03b2fef34e1f8f95cd7475ce5218b5d4f19625",
 "INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json":"ace5ae8b48874be5272bde8b2a46e67564f4636e",
 "INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json":"581ab19382d2f39b56589937fff66cc2045b9f87",
}
ARTIFACTS={
 "native_1_21_1":14703481861,
 "native_1_21_11":14702933021,
 "textured_face_uv":14700114922,
}
TARGETS={
 "rows":D/"INT5_B2_45_ELEMENT_SOURCE_TEXTURE_FACE_REVIEW_V1.csv",
 "images":D/"INT5_B2_16_NATIVE_F2_DIRECT_SCENE_REVIEW_V1.csv",
 "summary":D/"INT5_B2_REAL_ORIGINAL_IMAGE_REOPEN_RESULT_V1.json",
}
# Individually examined native source F2 screenshots; observations apply to
# whole chairs and large visible component groups, NOT individual JSON elements.
VISUAL={
 "AF121":{
  "visual_judgment":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
  "visual_observation":"원본 4방향에 주황색 목제 의자의 좌면판, 등받이 프레임, 하부 지지 형상이 보임",
  "view_limitation":"화면에는 각 요소 번호·면·정확한 텍스처 좌표 표시가 없음",
 },
 "AF123":{
  "visual_judgment":"CHAIR_PARTLY_OCCLUDED_BY_ADJACENT_LIGHT_TABLE",
  "visual_observation":"원본 4방향에 주황색 의자가 있고 인접한 밝은색 상판/테이블이 시야에서 의자의 좌면 일부를 가림",
  "view_limitation":"tucked 의자의 개별 좌판과 테이블 상판이 구별되지 않는 시점이 있어 역할을 확정할 수 없음",
 },
 "HC11210":{
  "visual_judgment":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
  "visual_observation":"원본 4방향에 청록색 의자 프레임과 어두운 좌면, 세로 등받이 부품 및 하부 지지대가 보임",
  "view_limitation":"검정색 좌면의 정확한 요소 경계·UV 및 기능/착석 여부는 확인하지 않음",
 },
 "MACAW67":{
  "visual_judgment":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
  "visual_observation":"원본 4방향에 회갈색 프레임, 주황색 좌면 및 가로 등받이 구조가 있는 의자가 보임",
  "view_limitation":"부품이 그려진 픽셀과 특정 JSON 요소 번호 사이의 인과 매핑은 별도",
 },
}
CASE_VERSIONS={"AF121":"1.21.1","AF123":"1.21.1","HC11210":"1.21.1","MACAW67":"1.21.11"}
PART_POPULATION={"AF1393":10,"AF1394":10,"HC13":13,"MACAW1424":12}
FACE_POPULATION={"AF121":46,"AF123":46,"HC11210":78,"MACAW67":59}


def require(condition,message):
    if not condition: raise ValueError("INT5-B2: "+message)


def sha256(payload): return hashlib.sha256(payload).hexdigest()


def gitblob(payload):
    return hashlib.sha1(b"blob "+str(len(payload)).encode()+b"\0"+payload).hexdigest()


def read_pinned(root=ROOT):
    found={}
    for filename,pin in PINS.items():
        value=(Path(root)/D/filename).read_bytes()
        require(gitblob(value)==pin,"source Git SHA drift: "+filename)
        found[filename]=value
    return found


def rows_csv(data):
    records=list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    require(records,"empty original source CSV")
    return records


def source_data(pinned):
    source=rows_csv(pinned["INT5_B_45_ELEMENT_TEXTURING_F2_SOURCE_BRIDGE_V1.csv"])
    runtime=json.loads(pinned["INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json"])
    texture=json.loads(pinned["INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json"])
    previous=json.loads(pinned["INT5_B_VISUAL_SOURCE_BRIDGE_RESULT_V1.json"])
    require(len(source)==45 and previous["counts"]["source_role_candidates_linked"]==45 and
            previous["counts"]["role_approvals"]==0 and
            texture["original_faces"]==229 and
            runtime["count"]["total_native_screenshots"]==16 and
            runtime["count"]["approved_parts"]==0,
            "previous source records were promoted/truncated")
    return source,runtime,texture,previous


def download_archives(folder:Path):
    folder.mkdir(parents=True,exist_ok=True)
    token=os.getenv("GITHUB_TOKEN","")
    for tag,aid in ARTIFACTS.items():
        path=folder/(tag+".zip")
        if path.exists(): continue
        require(bool(token),"GITHUB_TOKEN required to reopen real Actions PNG ZIP "+tag)
        req=urllib.request.Request(
            "https://api.github.com/repos/"+GITHUB_REPO+
            "/actions/artifacts/"+str(aid)+"/zip",
            headers={"Authorization":"Bearer "+token,
                     "Accept":"application/vnd.github+json",
                     "X-GitHub-Api-Version":"2022-11-28",
                     "User-Agent":"MCFR-INT5-B2-source-visual-audit/1"})
        with urllib.request.urlopen(req,timeout=90) as response:
            payload=response.read()
        require(zipfile.is_zipfile(io.BytesIO(payload)),
                "downloaded Actions artifact is not ZIP: "+tag)
        path.write_bytes(payload)
    return {tag:(folder/(tag+".zip")).read_bytes() for tag in ARTIFACTS}


def png_dimensions_and_verify(data):
    """CRC-validate every PNG chunk, inflate IDAT, check every scanline filter.

    Actual raster data is decompressed; no reliance on just a header/SHA. This
    lightweight source integrity decoder does not perform GPU texture baking.
    """
    import struct
    import zlib
    require(data.startswith(b"\x89PNG\r\n\x1a\n"),"not a PNG image")
    pos=8
    dim=None
    compressed=[]
    seen_end=False
    while pos+12<=len(data):
        size=struct.unpack(">I",data[pos:pos+4])[0]
        tag=data[pos+4:pos+8]
        start=pos+8
        end=start+size
        require(end+4<=len(data),"truncated PNG chunk")
        chunk=data[start:end]
        crc=struct.unpack(">I",data[end:end+4])[0]
        require(zlib.crc32(tag+chunk)&0xffffffff==crc,
                "PNG chunk CRC mismatch")
        if tag==b"IHDR":
            require(size==13 and dim is None,"invalid PNG IHDR")
            width,height,depth,ctype,compression,filter_method,interlace=struct.unpack(
                ">IIBBBBB",chunk)
            require(width>0 and height>0 and depth==8 and
                    ctype in (2,6) and compression==filter_method==interlace==0,
                    "unexpected original F2 PNG pixel format")
            dim=(width,height,3 if ctype==2 else 4)
        if tag==b"IDAT":compressed.append(chunk)
        if tag==b"IEND":
            require(size==0 and end+4==len(data),"trailing/malformed PNG")
            seen_end=True
            break
        pos=end+4
    require(dim is not None and compressed and seen_end,"incomplete PNG")
    width,height,bpp=dim
    raster=zlib.decompress(b"".join(compressed))
    stride=width*bpp+1
    require(len(raster)==stride*height,"PNG decompressed raster size mismatch")
    require(all(raster[y*stride] in (0,1,2,3,4) for y in range(height)),
            "invalid PNG scanline filter")
    return (width,height)


def read_artifacts(archives,source,runtime,texture):
    assert set(archives)==set(ARTIFACTS)
    raw={}
    archive_sha={}
    for tag,data in archives.items():
        require(zipfile.is_zipfile(io.BytesIO(data)),"broken ZIP "+tag)
        archive_sha[tag]=sha256(data)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            require(z.testzip() is None,"ZIP CRC verification failed "+tag)
            raw[tag]={name:z.read(name) for name in z.namelist()}
    expected_sheet=texture["contact_sheet_sha256"]
    tex=raw["textured_face_uv"]
    face=tex["INT3_229_ORIGINAL_FACE_UV_TEXTURE_EVIDENCE.csv"]
    diagnostic=tex["INT3_4_CHAIRS_ORIGINAL_UV_TEXTURE_DIAGNOSTIC.png"]
    require(sha256(face)==texture["face_csv_sha256"],
            "229 original face CSV SHA mismatch")
    require(sha256(diagnostic)==expected_sheet,
            "original textured source contact sheet SHA mismatch")
    require(png_dimensions_and_verify(diagnostic)[0]>700,
            "source diagnostic picture not decoded")
    face_rows=rows_csv(face)
    require(len(face_rows)==229,"expected 229 source faces")
    face_model_count=Counter(x["model_key"] for x in face_rows)
    require(face_model_count==FACE_POPULATION,
            "face model populations drift")
    require(len({x["original_png_path"] for x in face_rows})==8,
            "exactly eight underlying source PNG paths expected")
    require(all(x["game_visual_verified"]=="NO" for x in face_rows),
            "source face had been falsely asserted as game pixel approved")
    grouped=defaultdict(list)
    for x in face_rows:
        grouped[(x["provider_key"],x["element_index"])].append(x)
        require(len(x["original_png_sha"])==40 and x["uv"] and
                x["source_evidence"].startswith("ORIGINAL_CHILD_MODEL"),
                "source face texture UV hash/reference missing")
    require(len(grouped)==45 and
            Counter(k[0] for k in grouped)==PART_POPULATION,
            "exact 45 source elements missing from original 229 UV faces")

    original_images={v["case_id"]:v for v in runtime["collected"]["per_image"]}
    require(len(original_images)==16,"16 original source screenshot metadata expected")
    checked=[]
    for tag,version,count in (("native_1_21_1","1.21.1",12),
                              ("native_1_21_11","1.21.11",4)):
        files=raw[tag]
        manifest=json.loads(files["INT3_REAL_GAME_CAPTURE.json"])
        expected_run=next(x for x in runtime["collected"]["versions"] if x["version"]==version)
        require(manifest["client_version_verified"]==version and
                manifest["minecraft_native_f2_screenshot_count"]==count and
                manifest["source_state_verified_count"]==count and
                sha256(files["client.log"])==expected_run["client_log_sha256"]==
                manifest["client_log_sha256"] and
                not manifest["manual_sprite_comparison_complete"],
                "real game capture manifest/log changed "+tag)
        require(len(manifest["states"])==count,
                "original capture state count changed "+tag)
        for x in manifest["states"]:
            name=x["case_id"]
            require(name in original_images,"unknown real F2 case "+name)
            original=original_images[name]
            img=files[x["screenshot_file"]]
            exact_hash=sha256(img)
            dimensions=png_dimensions_and_verify(img)
            require(exact_hash==x["screenshot_sha256"]==original["sha256"] and
                    x["original_state"]==original["block"] and
                    x["original_model_target"]==original["model"] and
                    list(dimensions)==x["screenshot_dimensions"] and
                    list(dimensions)==[original["width"],original["height"]] and
                    x["server_blockstate_verified"] and
                    original["in_game_state_verified"],
                    "real original PNG/model/blockstate mismatch "+name)
            key=x["model_key"]
            require(name.startswith(key+"_") and
                    original["version"]==version==CASE_VERSIONS[key],
                    "screenshot version/model mismatch "+name)
            checked.append({
                "case_id":name,
                "source_model_key":key,
                "minecraft_version":version,
                "original_archive_artifact_id":str(ARTIFACTS[tag]),
                "real_original_PNG_sha256":exact_hash,
                "decoded_dimensions":str(dimensions[0])+"x"+str(dimensions[1]),
                "server_state":x["original_state"],
                "selected_original_model":x["original_model_target"],
                "actual_original_F2_bytes_reopened":"true",
                "human_reviewed_original_scene_in_this_turn":"true",
                "whole_object_appearance_grade":VISUAL[key]["visual_judgment"],
                "whole_object_observation":VISUAL[key]["visual_observation"],
                "view_limitation":VISUAL[key]["view_limitation"],
                "individual_source_element_pixels_approved":"false",
                "semantic_part_function_approved":"false",
                "INT6_training_redistribution_permission":"false",
            })
    require(len(checked)==16 and
            len({x["case_id"] for x in checked})==16,
            "16 native PNG images not inspected")
    return face_rows,grouped,checked,archive_sha


def calculate(raw,archives):
    source,runtime,texture,_=source_data(raw)
    faces,by_element,checked,archive_sha=read_artifacts(archives,source,runtime,texture)
    original_child={v["parent_key"]:v["child_key"] for v in texture["models"]}
    source_child_by_key={v["parent_key"]:v for v in texture["models"]}
    seen={}
    parts=[]
    for part in source:
        ident=(part["provider_key"],part["element_index"])
        require(ident in by_element,"missing exact source element texture faces "+repr(ident))
        f=by_element[ident]
        model=part["texture_child_model"]
        source_child=source_child_by_key[part["provider_key"]]
        key=source_child["child_key"]
        require(source_child["child_resource"]==model and
                len(f)>0 and all(face["model_key"]==key for face in f),
                "element UV and child source mismatch")
        require(part["specific_element_pixels_verified"]=="false" and
                part["semantic_part_role_verified"]=="false",
                "previous INT5-B1 improperly approved per-element meaning")
        paths=sorted(set(x["original_png_path"] for x in f))
        sha=sorted(set(x["original_png_sha"] for x in f))
        parts.append({
            "source_provider_key":part["provider_key"],
            "source_element_index":part["element_index"],
            "original_role_hypothesis":part["original_role_candidate"],
            "source_provider_sha":part["source_provider_git_sha"],
            "child_model_key":key,
            "child_model_sha":part["texture_child_source_git_sha"],
            "source_element_face_count":str(len(f)),
            "source_element_png_paths":"|".join(paths),
            "source_element_png_git_sha1":"|".join(sha),
            "exact_source_uv_face_keys":"|".join(
                x["face_direction"]+":"+x["uv"]+":"+x["uv_rotation"] for x in f),
            "same_child_direct_original_F2_reopened":"4",
            "whole_object_scene_grade":VISUAL[key]["visual_judgment"],
            "individual_element_F2_pixels_located":"false",
            "function_role_approved":"false",
            "material_style_approved":"false",
            "INT6_training_rights_approved":"false",
            "decision":"SOURCE_FACE_UV_CONFIRMED_WHOLE_CHAIR_SCREEN_OBSERVED_ELEMENT_FUNCTION_PENDING",
        })
        seen[ident]=len(f)
    require(len(parts)==45 and sum(seen.values())==229 and
            len(seen)==45,"source face count cannot be mapped to 45 role candidates")
    judge=Counter(x["whole_object_appearance_grade"] for x in checked)
    require(judge=={
        "WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE":12,
        "CHAIR_PARTLY_OCCLUDED_BY_ADJACENT_LIGHT_TABLE":4,
    },"actual human whole-object observation distribution unexpected")
    summary={
        "schema":"MCFR_INT5_B2_16_ORIGINAL_NATIVE_PNG_DIRECT_REOPEN_229_FACE_UV_45_PART/v1",
        "status":"PASS_16_ORIGINAL_NATIVE_F2_BYTES_VISUALLY_REVIEWED__PART_PIXEL_AND_FUNCTION_NOT_YET_APPROVED",
        "counts":{
            "original_archives_downloaded":3,
            "native_screenshot_PNG_opened_SHA_decoded":16,
            "native_1_21_1_images":12,
            "native_1_21_11_images":4,
            "original_client_logs_SHA_verified":2,
            "original_source_texture_uv_contact_sheet_opened":1,
            "original_source_faces_reopened":229,
            "original_source_face_to_part_keys_linked":45,
            "whole_chair_scenes_with_clear_group_forms":12,
            "whole_chair_scenes_partly_occluded":4,
            "source_part_individual_F2_pixel_mapping_approved":0,
            "part_function_approved":0,
            "style_or_material_approved":0,
            "INT6_training_redistribution_rights_approved":0,
            "new_Minecraft_game_runs":0,
            "new_game_F2_captures":0,
        },
        "source_pinned_git_blobs":dict(sorted(PINS.items())),
        "original_actions_artifact_ids":dict(sorted(ARTIFACTS.items())),
        "artifact_zips_sha256":dict(sorted(archive_sha.items())),
        "manual_scene_scope":"Direct visual inspection of 16 existing 1024x684 F2 images and original-texture UV source diagnostic; per-model whole-object appearance only.",
        "limitations":[
            "Direct visual inspection supports visible chair assemblies and selected color/texture contrast, not unique pixel segmentation for each of 45 source elements.",
            "AF tucked four views have adjacent light table masking portions of chair seat; cannot conclude exact source tucked transform from whole-object screenshot.",
            "Original source UV face link is fixed by provider/element and original PNG hashes but does not prove baked GPU UV for all faces.",
            "Original AF research blockstate versus runtime release bytes differ; prior INT5-B1 release caveat preserved.",
            "No game execution or new F2; all three original GitHub Actions ZIP assets are downloaded only to temporary CI or local inspection storage.",
            "No original assets/screenshots included in GitHub research commits; no third-party AI learning or redistribution rights inferred.",
        ],
    }
    return sorted(parts,key=lambda x:(x["source_provider_key"],int(x["source_element_index"]))),sorted(checked,key=lambda x:x["case_id"]),summary


def as_csv(rows):
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def output_files(raw,archives):
    parts,shots,summary=calculate(raw,archives)
    files={
        TARGETS["rows"].as_posix():as_csv(parts),
        TARGETS["images"].as_posix():as_csv(shots),
    }
    summary["derived_csv_sha256"]={
        k:sha256(v.encode("utf-8")) for k,v in sorted(files.items())
    }
    files[TARGETS["summary"].as_posix()]=json.dumps(
        summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    return files


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--archive-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,default=ROOT)
    p.add_argument("--verify",action="store_true")
    p.add_argument("--emit-json",action="store_true")
    a=p.parse_args()
    artifacts=download_archives(a.archive_dir)
    files=output_files(read_pinned(a.root),artifacts)
    for name,content in files.items():
        path=a.out/name
        if a.verify: require(path.read_text(encoding="utf-8")==content,
                             "persisted direct original F2 audit differs: "+name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding="utf-8")
    if a.emit_json:
        print("INT5_B2_OUTPUT_JSON_BEGIN")
        print(json.dumps(files,ensure_ascii=True,separators=(",",":")))
        print("INT5_B2_OUTPUT_JSON_END")
    print("INT5_B2_NATIVE_F2_16_PNG_BYTES_CRC_SHA_DECODED_SOURCE_UV_229_PARTS_45")
    print("INT5_B2_GROUP_SCENE_12_CLEAR_4_PARTLY_OCCLUDED_PER_ELEMENT_SEMANTIC_APPROVAL_0")


if __name__=="__main__":
    main()
