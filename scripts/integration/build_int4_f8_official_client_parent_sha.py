#!/usr/bin/env python3
"""INT-4-F8: pin S22's vanilla cube parent to Mojang's official client JAR.

Sources:
- frozen 1-5 APPLICATIONS.csv S22/HC with Git blob SHA1 for original vanilla cube;
- the original MCFR pinned client hashes in phase 1-3 runtime run_probe.py;
- official Mojang version manifest -> version JSON (SHA1) -> client.jar (SHA1).
No official client JAR or model JSON bytes are committed or redistributed.
Hash equality is distinct from model semantics and actual-game UV approval.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import runpy
import urllib.request
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
ORIGINAL=ROOT/"research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
EXPECTED_RESEARCH_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
ORIGINAL_PARENT_BLOB_SHA1="3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"
PARENT="assets/minecraft/models/block/cube.json"
PARENT_OF_PARENT="assets/minecraft/models/block/block.json"
VERSIONS=("1.21.1","1.21.11")
PINNED_CLIENT_SHA1={
 "1.21.1":"30c73b1c5da787909b2f73340419fdf13b9def88",
 "1.21.11":"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd",
}
MOJANG_MANIFEST="https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
OUTPUT=ROOT/"project/integration/INT4_F8_S22_OFFICIAL_VANILLA_PARENT_BYTES_V1.json"


def sha1(data):return hashlib.sha1(data).hexdigest()
def sha256(data):return hashlib.sha256(data).hexdigest()
def gitblob(data):return sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data)
def canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")


def original_study():
    raw=ORIGINAL.read_bytes()
    assert sha256(raw)==EXPECTED_RESEARCH_SHA256,("ORIGINAL_RESEARCH_CHANGED",sha256(raw))
    import csv
    entries=[r for r in csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
             if r["case"]=="S22"]
    assert len(entries)==1
    entry=entries[0]
    assert (entry["cohort"],entry["minecraft"],entry["block"],
            entry["state"],entry["provider_path"],entry["provider_sha"],
            entry["elements"],entry["faces"])==(
        "HC","1.21.1","handcrafted:oak_drawer",
        "facing=north;shape=single;type=1",PARENT,ORIGINAL_PARENT_BLOB_SHA1,"1","6"),entry
    assert entry["provider"]=="V1211-5"
    return entry


def verified_download(url,local,expected_sha1=None):
    local.parent.mkdir(parents=True,exist_ok=True)
    if local.is_file():
        content=local.read_bytes()
        if expected_sha1 is None or sha1(content)==expected_sha1:
            return content
        local.unlink()
    request=urllib.request.Request(url,headers={"User-Agent":"MCFR-INT4-F8-Official-Client-Source-Check"})
    with urllib.request.urlopen(request,timeout=180) as response:
        data=response.read()
    if expected_sha1 is not None:
        assert sha1(data)==expected_sha1,("REMOTE_OFFICIAL_SHA1_MISMATCH",url,sha1(data))
    local.write_bytes(data)
    return data


def read_releases(cache):
    manifest=json.loads(verified_download(MOJANG_MANIFEST,cache/"manifest.json"))
    versions={r["id"]:r for r in manifest["versions"] if r["id"] in VERSIONS}
    assert set(versions)==set(VERSIONS),("OFFICIAL_MOJANG_VERSION_MISSING",versions)
    return versions


def inspect_client(version,cache,manifest_entry):
    document_bytes=verified_download(
        manifest_entry["url"],cache/(version+"-version.json"),
        manifest_entry["sha1"])
    document=json.loads(document_bytes)
    assert document["id"]==version,("MOJANG_VERSION_MISMATCH",version)
    client=document["downloads"]["client"]
    assert client["sha1"]==PINNED_CLIENT_SHA1[version],(
        "PINNED_MCFR_OFFICIAL_CLIENT_CHANGED",version,client["sha1"])
    jar=verified_download(client["url"],cache/(version+"-official-client.jar"),client["sha1"])
    assert sha1(jar)==client["sha1"]
    with ZipFile(io.BytesIO(jar)) as archive:
        assert archive.testzip() is None
        names=set(archive.namelist())
        assert PARENT in names,("VANILLA_CUBE_MISSING",version)
        cube=archive.read(PARENT)
        cube_json=json.loads(cube.decode("utf-8-sig"))
        assert isinstance(cube_json,dict)
        assert isinstance(cube_json.get("elements"),list)
        assert len(cube_json["elements"])==1
        assert set(cube_json["elements"][0]["faces"])=={
            "down","up","north","south","west","east"}
        assert cube_json.get("parent")=="block/block",(
            "VANILLA_PARENT_CHAIN_CHANGED",version,cube_json.get("parent"))
        next_parent_exists=PARENT_OF_PARENT in names
        next_parent=archive.read(PARENT_OF_PARENT) if next_parent_exists else None
        if next_parent is not None:
            assert isinstance(json.loads(next_parent.decode("utf-8-sig")),dict)
    return {
        "minecraft_version":version,
        "official_version_json_sha1":sha1(document_bytes),
        "official_version_json_url":manifest_entry["url"],
        "pinned_MCFR_client_sha1":PINNED_CLIENT_SHA1[version],
        "official_client_jar_sha1_verified":sha1(jar),
        "official_client_jar_sha256":sha256(jar),
        "cube_asset_path":PARENT,
        "cube_byte_size":len(cube),
        "cube_sha256":sha256(cube),
        "cube_git_blob_sha1":gitblob(cube),
        "cube_json_semantic_sha256":sha256(canon(cube_json)),
        "cube_parent_block_model_ref":cube_json["parent"],
        "cube_element_count":len(cube_json["elements"]),
        "cube_face_count":sum(len(x["faces"]) for x in cube_json["elements"]),
        "next_parent_path":PARENT_OF_PARENT,
        "next_parent_in_official_client":next_parent_exists,
        "next_parent_git_blob_sha1":gitblob(next_parent) if next_parent else None,
        "next_parent_semantic_sha256":sha256(canon(json.loads(next_parent))) if next_parent else None,
    }


def run(cache):
    original=original_study()
    versions=read_releases(cache)
    evidence={v:inspect_client(v,cache,versions[v]) for v in VERSIONS}
    a,b=[evidence[v] for v in VERSIONS]
    comparisons={
        "runtime_1_21_1_cube_raw_Git_blob_equals_frozen_1_5_SHA":
            a["cube_git_blob_sha1"]==ORIGINAL_PARENT_BLOB_SHA1,
        "archived_1_21_11_cube_raw_Git_blob_equals_frozen_1_5_SHA":
            b["cube_git_blob_sha1"]==ORIGINAL_PARENT_BLOB_SHA1,
        "runtime_and_archived_cube_bytes_SHA256_equal":
            a["cube_sha256"]==b["cube_sha256"],
        "runtime_and_archived_cube_parsed_JSON_semantically_equal":
            a["cube_json_semantic_sha256"]==b["cube_json_semantic_sha256"],
        "runtime_and_archived_cube_parent_names_equal":
            a["cube_parent_block_model_ref"]==b["cube_parent_block_model_ref"],
        "runtime_and_archived_parent_block_semantically_equal":
            a["next_parent_semantic_sha256"]==b["next_parent_semantic_sha256"],
    }
    for v,e in evidence.items():
        assert e["official_client_jar_sha1_verified"]==PINNED_CLIENT_SHA1[v]
        assert e["cube_element_count"]==1 and e["cube_face_count"]==6
    # Gate F8 S22 based on ACTUAL historical raw source byte match, not
    # seemingly equivalent syntax. This is narrower than full pixelwise UV.
    exact=comparisons["runtime_1_21_1_cube_raw_Git_blob_equals_frozen_1_5_SHA"]
    report={
        "schema":"MCFR_INT4_F8_S22_MOJANG_OFFICIAL_CLIENT_PARENT_COMPARISON/v1",
        "status":"PASS_TWO_OFFICIAL_JAR_VERIFIED_S22_PARENT_COMPARISON",
        "historical_source":"research/furniture_mods/phase_1-5/B/APPLICATIONS.csv",
        "historical_original_file_SHA256":EXPECTED_RESEARCH_SHA256,
        "historical_case":"S22",
        "historical_parent_provider_label":original["provider"],
        "historical_parent_path":PARENT,
        "historical_original_parent_git_blob_sha1":ORIGINAL_PARENT_BLOB_SHA1,
        "manifest_URL":MOJANG_MANIFEST,
        "official_versions":evidence,
        "comparison":comparisons,
        "F8_S22_parent_binary_exact_eligibility":exact,
        "F8_S22_provisional_disposition":(
            "CONDITIONAL_PARENT_SOURCE_BYTES_PINNED_BUT_NO_FULL_UV_EXIT"
            if exact else
            "HOLD_PARENT_RAW_HASH_DIFF_REVIEW_JSON_SEMANTICS_AND_VERSION"),
        "source_observation_limits":[
            "Original Mojang official clients verified by metadata and cached SHA1; neither JAR nor extracted cube.json bytes committed.",
            "Git blob SHA includes blob header; plain file SHA256/sha1 is a distinct comparison.",
            "1.21.1 live Fabric client is separately evidenced by F7; this extraction reproduces the official pinned client JAR, not a new Minecraft F2 session.",
            "The 1.21.11 parent reference in original study can be a different source version; byte mismatch cannot be silently replaced with semantic equality.",
            "Even raw hash identity does NOT establish baked UV, screenshot pixels, dynamic rendering, behavior, meaning, or AI asset rights.",
        ],
        "counts":{
            "official_client_versions_verified":2,
            "historical_cases_examined":1,
            "new_actual_game_F2_images":0,
            "new_semantic_approval":0,
            "new_AI_training_or_redistribution_rights":0,
        },
    }
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cache",type=Path,required=True)
    p.add_argument("--out",type=Path,default=OUTPUT)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    report=run(a.cache)
    content=(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    if a.verify:
        assert a.out.is_file() and a.out.read_bytes()==content,(
            "F8_NONDETERMINISTIC_OFFICIAL_METADATA",str(a.out))
    else:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_bytes(content)
    print("PASS official Mojang client 1.21.1 & 1.21.11, S22 runtime parent SHA")
    print("runtime_parent_blob",report["official_versions"]["1.21.1"]["cube_git_blob_sha1"])
    print("research_parent_blob",ORIGINAL_PARENT_BLOB_SHA1)
    print("parent_byte_equivalent",report["F8_S22_parent_binary_exact_eligibility"])
    print("parent_JSON_semantically_equal_between_versions",
          report["comparison"]["runtime_and_archived_cube_parsed_JSON_semantically_equal"])


if __name__=="__main__":
    main()
