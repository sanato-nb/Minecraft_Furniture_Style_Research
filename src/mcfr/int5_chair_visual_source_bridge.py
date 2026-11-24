"""INT-5-B1: join real chair F2 provenance to 45 source part hypotheses.

Scope is whole-object visual-source traceability, NOT pixel/part segmentation,
semantic function or training/asset redistribution approval. No third-party
texture/JAR/image bytes are copied into the output.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = Path("project/integration")
PINS = {
    "INT5_A_45_ELEMENT_GEOMETRY_ROLE_REVIEW_V1.csv": "a88dcaf534a912f48375757b34ade6f9a15f7f97",
    "INT3_45_CHAIR_GEOMETRY_REVIEW.csv": "2a2fea79d9e7b5290a77230fb21c10ed96d9a91e",
    "INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json": "581ab19382d2f39b56589937fff66cc2045b9f87",
    "INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json": "ace5ae8b48874be5272bde8b2a46e67564f4636e",
    "INT3_ISOLATED_F2_FINAL_SUMMARY.json": "fd76011fae63caaf3d9bea9b93be2bef29cd79c9",
    "INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json": "31a2ffe6073e609feaf0d063a5b3b71c4e57e993",
    "INT5_A_EVIDENCE_TRIAGE_SUMMARY_V1.json": "cacaf8361860f88134c6911bf6f6678031b0ef38",
}
FILES = {
    "parts": D / "INT5_B_45_ELEMENT_TEXTURING_F2_SOURCE_BRIDGE_V1.csv",
    "shots": D / "INT5_B_16_NATIVE_F2_DIRECTION_SOURCE_BRIDGE_V1.csv",
    "summary": D / "INT5_B_VISUAL_SOURCE_BRIDGE_RESULT_V1.json",
}
DIRECTIONS = ("north","east","south","west")
SOURCE_COUNTS = {"AF":20,"HC":13,"MACAW":12}
ROLES = {"LEG_OR_LOWER_POST":16,"BACKREST_ASSEMBLY":16,"LOWER_FRAME":7,"SEAT_LAYER":6}
EXPECT_FACE_COUNT = {"AF121":46,"AF123":46,"HC11210":78,"MACAW67":59}
EXPECT_PNG_COUNT = {"AF121":3,"AF123":3,"HC11210":2,"MACAW67":2}


def require(test, reason):
    if not test:
        raise ValueError("INT5-B source bridge: "+reason)


def git_blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def pinned(root=ROOT):
    contents={}
    for name,expected in PINS.items():
        data=(Path(root)/D/name).read_bytes()
        require(git_blob_sha(data)==expected, "frozen Git source drift "+name)
        contents[name]=data
    return contents


def csv_records(content):
    reader=csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    rows=list(reader)
    require(rows and len(rows[0]) == len(reader.fieldnames or []),
            "CSV missing source columns")
    return rows


def indexed(rows, key):
    result={r[key]:r for r in rows}
    require(len(rows)==len(result), "duplicate record by "+key)
    return result


def calculate(raw):
    def j(name):return json.loads(raw[name])
    A=csv_records(raw["INT5_A_45_ELEMENT_GEOMETRY_ROLE_REVIEW_V1.csv"])
    prior=csv_records(raw["INT3_45_CHAIR_GEOMETRY_REVIEW.csv"])
    textures=j("INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json")
    runtime=j("INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json")
    isolation=j("INT3_ISOLATED_F2_FINAL_SUMMARY.json")
    selector=j("INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json")
    a_summary=j("INT5_A_EVIDENCE_TRIAGE_SUMMARY_V1.json")
    require(len(A)==len(prior)==45 and
            a_summary["counts"]["chair_source_role_candidates_measured"]==45 and
            a_summary["counts"]["independent_new_role_visual_approvals"]==0,
            "INT5-A roles are not 45 unapproved source candidates")
    require(Counter(r["original_role_candidate"] for r in A)==ROLES and
            Counter(r["source_id"] for r in A)==SOURCE_COUNTS,
            "INT5-A roles/provider census changed")
    require(textures["boundary"]["actual_minecraft_client_render_verified"] is False
            and textures["boundary"]["part_function_approved"]==0 and
            textures["original_faces"]==229 and
            textures["source_png_count"]==8 and
            textures["boundary"]["source_original_png_json_jar_exported"] is False,
            "texture source diagram is being confused with real game or rights")
    require(len(textures["models"])==len(textures["model_providers"])==4,
            "four source textured children/providers expected")
    require(textures["four_child_source_face_counts"]==EXPECT_FACE_COUNT,
            "229 source face model populations drift")

    providers=indexed(textures["model_providers"],"sha")
    children=indexed(textures["models"],"parent_sha")
    require(len(providers)==len(children)==4,"nonunique original provider SHA")
    all_image=runtime["collected"]["per_image"]
    require(len(all_image)==16 and
            runtime["count"]["total_native_screenshots"]==16 and
            runtime["count"]["server_state_verified"]==16 and
            runtime["count"]["selected_source_targets_y_matched"]==16 and
            runtime["count"]["approved_parts"]==0 and
            runtime["count"]["manual_source_to_client_exact_equivalences"]==0,
            "native F2 audit scope changed")
    img_by_parent=defaultdict(list)
    child_by_key=indexed(textures["models"],"child_key")
    require(set(child_by_key)==set(EXPECT_FACE_COUNT),"four child ID change")
    expected_block={
        "AF121":"another_furniture:acacia_chair",
        "AF123":"another_furniture:acacia_chair",
        "HC11210":"handcrafted:warped_chair",
        "MACAW67":"mcwfurnitures:acacia_chair",
    }
    version_by_model={"AF121":"1.21.1","AF123":"1.21.1",
                      "HC11210":"1.21.1","MACAW67":"1.21.11"}
    expected_y={"AF121":(0,90,180,270),"AF123":(0,90,180,270),
                "HC11210":(0,90,180,270),"MACAW67":(90,180,270,0)}
    require(len({r["case_id"] for r in all_image})==16 and
            len({r["sha256"] for r in all_image})==16,
            "native F2 identity/hash duplicated")
    for row in all_image:
        key=row["case_id"].split("_")[0]
        require(key in child_by_key, "unexpected F2 child "+key)
        require(row["case_id"] in {key+"_"+d for d in DIRECTIONS},
                "wrong case direction for "+key)
        require(row["model"]==child_by_key[key]["child_resource"] and
                row["version"]==version_by_model[key] and
                row["block"].startswith(expected_block[key]+"[") and
                row["native_game_F2"] is True and
                row["in_game_state_verified"] is True and
                len(row["sha256"])==64,
                "F2 source/camera/selected model not pinned "+row["case_id"])
        img_by_parent[child_by_key[key]["parent_sha"]].append(row)
    require({r["case_id"] for r in all_image} ==
            {key+"_"+d for key in child_by_key for d in DIRECTIONS},
            "missing four orientations per source child")
    for key,child in child_by_key.items():
        require(child["total_faces_source"]==EXPECT_FACE_COUNT[key] and
                child["original_png_count"]==EXPECT_PNG_COUNT[key] and
                child["uv_stats"]["explicit_uv"]==EXPECT_FACE_COUNT[key],
                "source faces/UV/PNG declared counts drift "+key)
        shots=img_by_parent[child["parent_sha"]]
        require(len(shots)==4 and
                tuple(next(x for x in shots if x["case_id"]==key+"_"+d)["y"]
                      for d in DIRECTIONS)==expected_y[key],
                "source-selected blockstate rotations mismatch "+key)

    source_states=indexed(selector["source_states"],"resource_block")
    require(set(source_states)==set(expected_block.values()),
            "original blockstate declaration unexpectedly changed")
    require(selector["boundaries"]["visually_verified_chair_role_count"]==0,
            "original source state was mislabeled semantic pass")
    # Validate each of 16 exact run / server / release relations from the
    # original runtime evidence, never infer JAR parent JSON parity.
    versions=indexed(runtime["collected"]["versions"],"version")
    require(len(versions)==2,"expected two Minecraft versions")
    expected_jar_by_mod={}
    for version,entry in versions.items():
        require(entry["server_verified"]==entry["game_F2"]==
                (12 if version=="1.21.1" else 4),"F2 run version batch mismatch")
        for block,state in entry["blockstate_source"].items():
            actual=source_states[block]
            require(state["research_source_hash"]==actual["source_sha"],
                    "original research blockstate hash mismatch "+block)
            require(state["scope"] in (
                "RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE",
                "BYTE_IDENTICAL_TO_PINNED_RESEARCH"),
                "unexpected release equivalence status")
            if state["byte_identical_to_research"]:
                require(state["runtime_source_hash"]==state["research_source_hash"],
                        "source/runtime equal claim but digest differs")
            else:
                require(state["runtime_source_hash"]!=state["research_source_hash"],
                        "source/runtime divergent claim but digest equal")
            expected_jar_by_mod[block]=state
    require(not expected_jar_by_mod["another_furniture:acacia_chair"]["byte_identical_to_research"] and
            expected_jar_by_mod["handcrafted:warped_chair"]["byte_identical_to_research"] and
            expected_jar_by_mod["mcwfurnitures:acacia_chair"]["byte_identical_to_research"],
            "known AF runtime source drift cannot be erased")
    require(isolation["newly_recaptured_native_game_F2_photos"]==16 and
            isolation["visually_approved_new_roles"]==0 and
            isolation["game_engine_uv_bake_pixel_verified"]==0 and
            isolation["model_parent_json_runtime_vs_research_sha_matched"]=="NOT_VERIFIED",
            "isolated screenshot summary overpromoted to element semantics")
    prior_by=indexed(prior,"original_model_sha") if False else {
        (r["source_id"],r["original_model_sha"],r["element_index"]):r for r in prior}
    require(len(prior_by)==45,"previous 45 geometry source keys duplicated")
    body=[]
    for r in sorted(A,key=lambda x:(x["source_id"],x["source_model_sha"],int(x["element_index"]))):
        sha=r["source_model_sha"]
        require(sha in providers and sha in children,"no unique parent/texture child for "+sha)
        p=providers[sha]; child=children[sha]
        key=(r["source_id"],sha,r["element_index"])
        require(key in prior_by,"original geometric visual role record missing "+str(key))
        old=prior_by[key]
        require(old["source_role_candidate"]==r["original_role_candidate"] and
                old["geometry_layout_assessment"]=="GROUP_LEVEL_SHAPE_PLAUSIBLE" and
                old["material_runtime_status"]=="PENDING_TEXTURE_AND_GAME_VISUAL" and
                old["asset_rights_status"]=="PENDING_ORIGINAL_LICENSE_REVIEW",
                "historic geometry observation was modified/overpromoted")
        require(p["mod"]==r["source_id"] and
                p["element_count"]==int(r["model_element_count"]) and
                p["source_path"]==r["source_model_path"] and
                sha==p["sha"]==child["parent_sha"] and
                p["role_counts"][r["original_role_candidate"]] >= 1,
                "parent provenance/role count mismatch")
        images=sorted(img_by_parent[sha],key=lambda i:DIRECTIONS.index(i["case_id"].split("_")[-1]))
        block=expected_block[child["child_key"]]
        release=expected_jar_by_mod[block]
        for im in images:
            require(im["source_equivalence_scope"]==release["scope"] and
                    im["source_runtime_sha"]==release["runtime_source_hash"] and
                    im["source_research_sha"]==release["research_source_hash"],
                    "capture metadata differs from runtime release "+im["case_id"])
        body.append({
            "source_id":r["source_id"],
            "provider_key":r["provider_key"],
            "source_model_path":r["source_model_path"],
            "source_provider_git_sha":sha,
            "element_index":r["element_index"],
            "original_role_candidate":r["original_role_candidate"],
            "geometry_layout_observation":old["independent_group_observation"],
            "texture_child_model":child["child_resource"],
            "texture_child_source_git_sha":child["child_sha"],
            "source_faces_entire_child":str(child["total_faces_source"]),
            "source_png_count_entire_child":str(child["original_png_count"]),
            "same_child_original_native_F2_count":"4",
            "same_child_native_F2_case_ids":"|".join(i["case_id"] for i in images),
            "same_child_native_F2_sha256s":"|".join(i["sha256"] for i in images),
            "source_and_runtime_blockstate_sha_match":str(
                release["byte_identical_to_research"]).lower(),
            "model_parent_json_byte_identity_in_runtime":"NOT_VERIFIED",
            "specific_element_pixels_verified":"false",
            "semantic_part_role_verified":"false",
            "materials_style_verified":"false",
            "INT6_ai_training_or_redistribution_rights_approved":"false",
            "decision":"SOURCE_PART_TO_WHOLE_OBJECT_F2_CONTEXT_LINKED_ONLY",
            "next_evidence":"EXACT_F2_ORIGINAL_VISUAL_INSPECTION_AND_ELEMENT_REGION_MATCH",
        })
    shots=[]
    for im in sorted(all_image,key=lambda i:i["case_id"]):
        child=child_by_key[im["case_id"].split("_")[0]]
        release=expected_jar_by_mod[expected_block[child["child_key"]]]
        shots.append({
            "case_id":im["case_id"],"native_F2_file":im["file"],
            "native_F2_sha256":im["sha256"],"minecraft_version":im["version"],
            "exact_runtime_blockstate":im["block"],
            "selected_model_resource":im["model"],
            "model_parent_provider_git_sha":child["parent_sha"],
            "child_model_source_git_sha":child["child_sha"],
            "blockstate_study_sha":im["source_research_sha"],
            "blockstate_runtime_sha":im["source_runtime_sha"],
            "original_F2_source_run_id":str(runtime["ci_run"]),
            "original_server_state_verified":"true",
            "release_source_byte_equal":str(release["byte_identical_to_research"]).lower(),
            "original_scene_directly_reinspected_this_INT5_run":"false",
            "element_level_visual_role_approved":"false",
            "decision":"REAL_F2_WHOLE_CHAIR_SOURCE_ONLY",
        })
    require(len(body)==45 and len(shots)==16 and
            Counter(x["source_id"] for x in body)==SOURCE_COUNTS,
            "INT5-B derived source joins incomplete")
    summary={
        "schema":"MCFR_INT5_B_CHAIR_45_SOURCE_TO_16_NATIVE_F2_SCOPED_BRIDGE_V1",
        "status":"PASS_SOURCE_TEXTURING_AND_WHOLE_OBJECT_F2_PROVENANCE__SEMANTICS_NOT_APPROVED",
        "counts":{
            "source_role_candidates_linked":45,
            "original_provider_models":4,
            "original_children_textured":4,
            "source_faces_across_children":229,
            "unique_source_PNG":8,
            "original_native_F2_same_child_direction_views":16,
            "different_versions":2,
            "F2_per_child":4,
            "AF_candidates_with_known_research_vs_release_state_file_diff":20,
            "HC_MACAW_candidates_with_blockstate_sha_equal_only":25,
            "new_F2_directly_visual_inspected":0,
            "specific_element_to_F2_pixel_observations":0,
            "role_approvals":0,
            "material_style_approvals":0,
            "INT6_training_redistribution_rights_approved":0,
        },
        "source_github_git_blobs":dict(sorted(PINS.items())),
        "research_and_release_differences_preserved":True,
        "prior_16_native_F2_run":runtime["ci_run"],
        "prior_isolation_native_F2_recapture":isolation["newly_recaptured_native_game_F2_photos"],
        "context":"Whole-object F2 screenshots apply to the same selected source child/parent; none identifies individual source element pixels.",
        "limitations":[
            "Screen images in original Actions are reused by exact identity/hash metadata, not downloaded and visually inspected anew here.",
            "Source PNG and face UV are confirmed for the four textured children at whole-model level, not independently mapped for every one of 45 element faces in this bridge.",
            "AF study 4.0.3 blockstate bytes differ from official Fabric 4.0.2 for acacia, and complete runtime model parent SHA parity is unverified for all providers.",
            "A geometry plausible candidate plus a visible whole chair is NOT proof of functional seat/backrest/leg role, material, or Minecraft baked per-face UV.",
            "No new game run or F2 screenshot; previous 16 re-captured isolation views not counted as 16 new independent model/part approvals.",
            "No third-party textures/models/game images copied or approved for AI training, learning rights or redistribution.",
        ],
    }
    return body,shots,summary


def csv_out(records):
    s=io.StringIO(newline="")
    writer=csv.DictWriter(s,fieldnames=list(records[0]),lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return s.getvalue()


def outputs(raw):
    roles,shots,summary=calculate(raw)
    texts={
        FILES["parts"].as_posix():csv_out(roles),
        FILES["shots"].as_posix():csv_out(shots),
    }
    summary["output_sha256"]={k:hashlib.sha256(v.encode("utf-8")).hexdigest()
                              for k,v in sorted(texts.items())}
    texts[FILES["summary"].as_posix()] = json.dumps(
        summary,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    return texts


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--out",type=Path,default=ROOT)
    parser.add_argument("--verify",action="store_true")
    parser.add_argument("--emit-json",action="store_true")
    a=parser.parse_args()
    data=outputs(pinned(a.root))
    for name,text in data.items():
        target=a.out/name
        if a.verify:
            require(target.read_text(encoding="utf-8")==text,
                    "persisted evidence bridge differs from source replay: "+name)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(text,encoding="utf-8")
    if a.emit_json:
        print("INT5_B_OUTPUT_JSON_BEGIN")
        print(json.dumps(data,ensure_ascii=True,separators=(",",":")))
        print("INT5_B_OUTPUT_JSON_END")
    print("INT5_B_45_PARTS_4_MODELS_229_FACES_16_F2_RECONCILED_NO_SEMANTIC_APPROVAL")


if __name__=="__main__":
    main()
