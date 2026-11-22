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
ORIGINAL_PARENT_RECORDED_HASH="3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"
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
        "facing=north;shape=single;type=1",PARENT,ORIGINAL_PARENT_RECORDED_HASH,"1","6"),entry
    assert entry["provider"]=="V1211-5"
    assert entry["model_hash_kind"]=="GIT_BLOB_SHA1" and len(entry["provider_sha"])==64
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


def _changed_json_paths(left,right,prefix=""):
    """Return only changed JSON field paths (never original game asset values)."""
    if left==right:return []
    if isinstance(left,dict) and isinstance(right,dict):
        out=[]
        for key in sorted(set(left)|set(right)):
            sub=(prefix+"." if prefix else "")+str(key)
            if key not in left or key not in right:out.append(sub)
            else:out.extend(_changed_json_paths(left[key],right[key],sub))
        return out
    if isinstance(left,list) and isinstance(right,list) and len(left)==len(right):
        out=[]
        for i,(a,b) in enumerate(zip(left,right)):
            out.extend(_changed_json_paths(a,b,prefix+f"[{i}]"))
        return out
    return [prefix]


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
        "next_parent_world_fields_semantic_sha256":sha256(canon({k:v for k,v in json.loads(next_parent).items() if k not in ("display","gui_light")})) if next_parent else None,
        "next_parent_top_level_fields":sorted(json.loads(next_parent).keys()) if next_parent else [],
    }


def run(cache):
    original=original_study()
    versions=read_releases(cache)
    evidence={v:inspect_client(v,cache,versions[v]) for v in VERSIONS}
    a,b=[evidence[v] for v in VERSIONS]
    # Compare only metadata change paths; don't store copyrighted block models.
    raw_parents={}
    for v in VERSIONS:
        with ZipFile(cache/(v+"-official-client.jar")) as package:
            raw_parents[v]=json.loads(package.read(PARENT_OF_PARENT).decode("utf-8-sig"))
    changed_paths=_changed_json_paths(raw_parents["1.21.1"],raw_parents["1.21.11"])
    parent_changes_only_display_metadata=all(
        path=="gui_light" or path.startswith("display.") or path=="display"
        for path in changed_paths)
    comparisons={
        "runtime_1_21_1_cube_raw_Git_blob_equals_frozen_1_5_SHA":
            a["cube_git_blob_sha1"]==ORIGINAL_PARENT_RECORDED_HASH,
        "runtime_1_21_1_cube_SHA256_equals_frozen_1_5_recorded_hash":
            a["cube_sha256"]==ORIGINAL_PARENT_RECORDED_HASH,
        "archived_1_21_11_cube_raw_Git_blob_equals_frozen_1_5_SHA":
            b["cube_git_blob_sha1"]==ORIGINAL_PARENT_RECORDED_HASH,
        "archived_1_21_11_cube_SHA256_equals_frozen_1_5_recorded_hash":
            b["cube_sha256"]==ORIGINAL_PARENT_RECORDED_HASH,
        "runtime_and_archived_cube_bytes_SHA256_equal":
            a["cube_sha256"]==b["cube_sha256"],
        "runtime_and_archived_cube_parsed_JSON_semantically_equal":
            a["cube_json_semantic_sha256"]==b["cube_json_semantic_sha256"],
        "runtime_and_archived_cube_parent_names_equal":
            a["cube_parent_block_model_ref"]==b["cube_parent_block_model_ref"],
        "runtime_and_archived_parent_block_semantically_equal":
            a["next_parent_semantic_sha256"]==b["next_parent_semantic_sha256"],
        "runtime_and_archived_parent_block_world_fields_equal":
            a["next_parent_world_fields_semantic_sha256"]==b["next_parent_world_fields_semantic_sha256"],
        "parent_block_changes_only_item_display_metadata":parent_changes_only_display_metadata,
    }
    for v,e in evidence.items():
        assert e["official_client_jar_sha1_verified"]==PINNED_CLIENT_SHA1[v]
        assert e["cube_element_count"]==1 and e["cube_face_count"]==6
    # Gate F8 S22 based on ACTUAL historical raw source byte match, not
    # seemingly equivalent syntax. This is narrower than full pixelwise UV.
    exact=comparisons["runtime_1_21_1_cube_SHA256_equals_frozen_1_5_recorded_hash"]
    report={
        "schema":"MCFR_INT4_F8_S22_MOJANG_OFFICIAL_CLIENT_PARENT_COMPARISON/v1",
        "status":"PASS_TWO_OFFICIAL_JAR_VERIFIED_S22_PARENT_COMPARISON",
        "historical_source":"research/furniture_mods/phase_1-5/B/APPLICATIONS.csv",
        "historical_original_file_SHA256":EXPECTED_RESEARCH_SHA256,
        "historical_case":"S22",
        "historical_parent_provider_label":original["provider"],
        "historical_parent_path":PARENT,
        "historical_original_parent_recorded_hash":ORIGINAL_PARENT_RECORDED_HASH,
        "historical_row_declared_hash_kind":original["model_hash_kind"],
        "historical_row_provider_sha_has_64_hex_chars":len(original["provider_sha"])==64,
        "historical_row_provider_sha_cannot_be_git_blob_sha1":len(original["provider_sha"])!=40,
        "corrected_provider_sha_algorithm_by_official_source":"SHA256",
        "original_source_row_needs_hash_kind_correction":True,
        "manifest_URL":MOJANG_MANIFEST,
        "official_versions":evidence,
        "comparison":comparisons,
        "inherited_block_block_changed_JSON_property_paths":changed_paths,
        "parent_block_inherited_world_fields_are_equal":comparisons["runtime_and_archived_parent_block_world_fields_equal"],
        "F8_S22_parent_binary_exact_eligibility":exact,
        "S22_frozen_parent_sha256_revalidated_against_official_runtime":exact,
        "F8_S22_provisional_disposition":(
            "CONDITIONAL_OFFICIAL_CUBE_SHA256_MATCHES_RESEARCH_HASH_KIND_LABEL_WRONG"
            if exact else
            "HOLD_OFFICIAL_CUBE_SHA256_DIFFERENCE_REQUIRES_SOURCE_REVIEW"),
        "source_observation_limits":[
            "Original Mojang official clients verified by metadata and cached SHA1; neither JAR nor extracted cube.json bytes committed.",
            "The historical S22 row declares model_hash_kind=GIT_BLOB_SHA1 but provider_sha has 64 characters and matches official cube SHA256 (not the 40-char Git blob SHA1). The original row is preserved and a separate correction is recorded.",
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
    print("research_parent_recorded_SHA256",ORIGINAL_PARENT_RECORDED_HASH)
    print("parent_byte_equivalent",report["F8_S22_parent_binary_exact_eligibility"])
    print("parent_JSON_semantically_equal_between_versions",
          report["comparison"]["runtime_and_archived_cube_parsed_JSON_semantically_equal"])


if __name__=="__main__":
    main()
