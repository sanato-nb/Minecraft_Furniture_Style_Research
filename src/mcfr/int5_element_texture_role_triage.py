"""INT-5-B3: 45 exact element source textures vs 16 original game scenes.

Scope: independent original PNG/UV source-role *cues*, with visual chair-assembly
observations. This is NOT per-element F2 pixel segmentation, gameplay function,
material science, training rights or generalization to other furniture.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path

from . import int5_native_f2_image_reopen as origin

ROOT=Path(__file__).resolve().parents[2]
D=Path("project/integration")
PINNED={
    "INT5_B2_45_ELEMENT_SOURCE_TEXTURE_FACE_REVIEW_V1.csv":
        "13775fadcbe3f385cf853a2c5fe923a06a33a9ae",
    "INT5_B2_16_NATIVE_F2_DIRECT_SCENE_REVIEW_V1.csv":
        "a2f8b9c1ea5a559036e0ee92e32b5de5b626542a",
    "INT5_B2_REAL_ORIGINAL_IMAGE_REOPEN_RESULT_V1.json":
        "7c6885c415bf312c1352b81961d53df64970cfcc",
}
OUT={
    "parts":D/"INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv",
    "groups":D/"INT5_B3_15_ROLE_GROUP_SCREEN_EVIDENCE_V1.csv",
    "summary":D/"INT5_B3_45_ROLE_TEXTURE_SOURCE_SCOPE_RESULT_V1.json",
}
ROLE_COUNTS={"LEG_OR_LOWER_POST":16,"BACKREST_ASSEMBLY":16,
             "LOWER_FRAME":7,"SEAT_LAYER":6}
PROVIDERS={"AF121":10,"AF123":10,"HC11210":13,"MACAW67":12}
FACES={"AF121":46,"AF123":46,"HC11210":78,"MACAW67":59}
GROUP_COUNT=15


def require(ok,why):
    if not ok: raise ValueError("INT5-B3 source/scene claim rejected: "+why)


def read_pinned(root=ROOT):
    raw={}
    for filename,sha in PINNED.items():
        source=(Path(root)/D/filename).read_bytes()
        require(origin.gitblob(source)==sha,"upstream Git blob drift "+filename)
        raw[filename]=source
    return raw


def csv_rows(data):
    records=list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    require(records,"empty sourced record")
    return records


def cue_for(model,role,face_rows):
    """Use actual source texture paths, not inferred role from a model name."""
    paths={x["original_png_path"] for x in face_rows}
    if model in ("AF121","AF123"):
        if role=="SEAT_LAYER":
            target="textures/block/chair/seat/acacia.png"
            if any(x.endswith(target) for x in paths):
                return "ROLE_NAMED_ORIGINAL_SEAT_PNG"
        if role=="BACKREST_ASSEMBLY":
            target=("/textures/block/chair/back_1/acacia.png" if model=="AF121"
                    else "/textures/block/chair/back_10/acacia.png")
            if any(x.endswith(target) for x in paths):
                return "ROLE_NAMED_ORIGINAL_BACK_PNG"
    if model=="HC11210" and role=="SEAT_LAYER":
        if any(x.endswith("/textures/block/chair/cushion/black_cushion.png")
               for x in paths):
            return "ROLE_NAMED_ORIGINAL_CUSHION_PNG"
    if model=="MACAW67" and role=="SEAT_LAYER":
        if any(x.endswith("/textures/block/stripped_acacia_log.png") for x in paths):
            return "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME"
    return "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF"


def adjudicate(raw,archives,b2raw):
    original_parts,original_shots,orig_summary=origin.calculate(b2raw,archives)
    B2=json.loads(raw["INT5_B2_REAL_ORIGINAL_IMAGE_REOPEN_RESULT_V1.json"])
    require(B2["counts"]==orig_summary["counts"] and
            B2["artifact_zips_sha256"]==orig_summary["artifact_zips_sha256"],
            "upstream B2 real-original scene proof not replayed exactly")
    p=csv_rows(raw["INT5_B2_45_ELEMENT_SOURCE_TEXTURE_FACE_REVIEW_V1.csv"])
    scenes=csv_rows(raw["INT5_B2_16_NATIVE_F2_DIRECT_SCENE_REVIEW_V1.csv"])
    require(len(p)==len(original_parts)==45 and len(scenes)==len(original_shots)==16,
            "upstream original part/screenshot counts changed")
    source_part={(x["child_model_key"],x["source_element_index"]):x for x in original_parts}
    require(len(source_part)==45,"upstream element index duplicated")
    require(len({(x["child_model_key"],x["source_element_index"]) for x in p})==45,
            "B2 part index duplicated")
    for x in p:
        expected=source_part[(x["child_model_key"],x["source_element_index"])]
        require(x==expected,"B2 pinned part row is not derived from original image/UV")
    scene_by={x["case_id"]:x for x in original_shots}
    require(len(scene_by)==16,"upstream images duplicated")
    for x in scenes:
        require(x==scene_by[x["case_id"]],
                "B2 pinned scene row diverges from directly reopened original PNG")
    # Source provenance actual face-by-face, re-opened from original texture ZIP.
    source,rt,texture,_=origin.source_data(b2raw)
    faces,by_element,checked,sha=origin.read_artifacts(archives,source,rt,texture)
    require(len(faces)==229 and len(by_element)==45 and len(checked)==16,
            "original source face/real PNG bytes no longer match")
    screen_by_model=defaultdict(list)
    for row in scenes:
        screen_by_model[row["source_model_key"]].append(row)
    require({k:len(v) for k,v in screen_by_model.items()}==
            {k:4 for k in PROVIDERS},"expected 4 cardinal direction scenes")
    expected_group_grade={
       "AF121":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
       "AF123":"CHAIR_PARTLY_OCCLUDED_BY_ADJACENT_LIGHT_TABLE",
       "HC11210":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
       "MACAW67":"WHOLE_CHAIR_SEAT_BACK_SUPPORT_SHAPES_VISIBLE",
    }
    for key,shots in screen_by_model.items():
        require(all(x["whole_object_appearance_grade"]==expected_group_grade[key]
                    and x["human_reviewed_original_scene_in_this_turn"]=="true"
                    and x["individual_source_element_pixels_approved"]=="false"
                    and len(x["real_original_PNG_sha256"])==64 for x in shots),
                "visualized source group/improper per-element approval "+key)
    role_evidence=[]
    for row in p:
        child=row["child_model_key"]
        index=row["source_element_index"]
        role=row["original_role_hypothesis"]
        source_faces=by_element[(row["source_provider_key"],index)]
        require(role in ROLE_COUNTS and
                len(source_faces)==int(row["source_element_face_count"]),
                "source face count or candidate changed "+child+":"+index)
        cue=cue_for(child,role,source_faces)
        named=cue.startswith("ROLE_NAMED_ORIGINAL_")
        uniq=cue=="UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME"
        if child=="AF123" and role=="SEAT_LAYER":
            observed="GROUP_SEAT_OCCLUDED_BY_ADJACENT_TABLE_NO_ELEMENT_ASSIGNMENT"
            disposition="ORIGINAL_TEXTURE_ROLE_CUE_SEAT_OCCLUDED"
        elif named:
            observed=("ASSEMBLY_GROUP_APPEARANCE_VISIBLE_ELEMENT_PIXEL_NOT_LOCATED"
                      if child!="AF123" or role=="BACKREST_ASSEMBLY"
                      else "ASSEMBLY_GROUP_PARTLY_OCCLUDED_ELEMENT_PIXEL_NOT_LOCATED")
            disposition="SOURCE_TEXTURE_ROLE_CUE_AND_WHOLE_GROUP_APPEARANCE_CORROBORATED"
        elif uniq:
            observed="WHOLE_SEAT_CONTRAST_VISIBLE_EXACT_ELEMENT_PIXEL_NOT_LOCATED"
            disposition="UNIQUE_SOURCE_TEXTURE_CONTRAST_ONLY_NO_FUNCTION"
        else:
            observed=("WHOLE_ASSEMBLY_PARTLY_OCCLUDED_NO_ELEMENT_PIXEL_MATCH"
                      if child=="AF123" else
                      "WHOLE_ASSEMBLY_VISIBLE_NO_ELEMENT_PIXEL_MATCH")
            disposition="GEOMETRY_AND_SOURCE_UV_ONLY_ROLE_HYPOTHESIS"
        # Absence of a semantic cue is NOT a contradiction, and cue is NOT a
        # physical function or a unique pixel-accurate attribution.
        role_evidence.append({
            "child_model_key":child,
            "provider_key":row["source_provider_key"],
            "original_source_element_index":index,
            "original_role_hypothesis":role,
            "source_element_original_face_count":str(len(source_faces)),
            "original_textures_used":"|".join(sorted({
                r["original_png_path"] for r in source_faces})),
            "original_texture_source_hashes":"|".join(sorted({
                r["original_png_sha"] for r in source_faces})),
            "role_discriminating_texture_cue":cue,
            "face_count_using_role_cue":str(sum(
                cue_for(child,role,[f])==cue for f in source_faces
            ) if named or uniq else 0),
            "source_related_real_F2_cases":"|".join(sorted(
                x["case_id"] for x in screen_by_model[child])),
            "original_game_scene_observation":observed,
            "research_and_runtime_source_caveat":(
                "AF_SOURCE_4_0_3_RELEASE_4_0_2_NOT_BYTE_IDENTICAL" if child.startswith("AF")
                else "BLOCKSTATE_SHA_EQUAL_PARENT_JSON_RUNTIME_NOT_FULLY_PROVEN"),
            "individual_element_to_original_F2_pixels_approved":"false",
            "part_function_verified":"false",
            "material_or_style_verified":"false",
            "training_or_redistribution_rights_approved":"false",
            "decision":disposition,
        })
    role_evidence.sort(key=lambda r:(r["child_model_key"],int(r["original_source_element_index"])))
    require(len(role_evidence)==45,"45 source-role records missing")
    roles=Counter(r["original_role_hypothesis"] for r in role_evidence)
    require(roles==ROLE_COUNTS,"source candidate role population changed")
    cues=Counter(r["role_discriminating_texture_cue"] for r in role_evidence)
    require(cues=={
        "ROLE_NAMED_ORIGINAL_SEAT_PNG":2,
        "ROLE_NAMED_ORIGINAL_BACK_PNG":6,
        "ROLE_NAMED_ORIGINAL_CUSHION_PNG":1,
        "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME":1,
        "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF":35,
    },"actual texture-source discriminators have changed")
    require(Counter(r["decision"] for r in role_evidence)=={
        "SOURCE_TEXTURE_ROLE_CUE_AND_WHOLE_GROUP_APPEARANCE_CORROBORATED":8,
        "ORIGINAL_TEXTURE_ROLE_CUE_SEAT_OCCLUDED":1,
        "UNIQUE_SOURCE_TEXTURE_CONTRAST_ONLY_NO_FUNCTION":1,
        "GEOMETRY_AND_SOURCE_UV_ONLY_ROLE_HYPOTHESIS":35,
    },"source role/visible group breakdown changed")

    groups=[]
    for key in PROVIDERS:
        by_role=defaultdict(list)
        for x in role_evidence:
            if x["child_model_key"]==key:
                by_role[x["original_role_hypothesis"]].append(x)
        for role,subset in sorted(by_role.items()):
            count_named=sum(x["role_discriminating_texture_cue"].startswith(
                "ROLE_NAMED_ORIGINAL") for x in subset)
            grades=sorted(set(x["decision"] for x in subset))
            scene_grade=expected_group_grade[key]
            groups.append({
                "child_model_key":key,
                "original_role_group_hypothesis":role,
                "source_element_count":str(len(subset)),
                "element_indices":"|".join(x["original_source_element_index"] for x in subset),
                "total_source_faces_in_group":str(sum(
                    int(x["source_element_original_face_count"]) for x in subset)),
                "role_named_source_texture_elements":str(count_named),
                "observed_original_native_F2_scenes":"4",
                "group_scene_visibility":(
                    "CHILD_MODEL_PARTLY_OCCLUDED_SOURCE_SCENE" if key=="AF123"
                    else "CHILD_MODEL_GROUP_ASSEMBLY_APPEARANCE_VISIBLE"),
                "texture_role_evidence_grades":"|".join(grades),
                "source_group_render_appearance_scope_only":"true",
                "actual_element_function_verified":"false",
                "unique_element_screen_pixels_approved":"false",
                "decision":"GROUP_APPEARANCE_SOURCE_HYPOTHESIS_NOT_FUNCTIONAL_CERTIFICATION",
            })
    groups.sort(key=lambda x:(x["child_model_key"],x["original_role_group_hypothesis"]))
    require(len(groups)==GROUP_COUNT and
            sum(int(x["source_element_count"]) for x in groups)==45 and
            sum(int(x["total_source_faces_in_group"]) for x in groups)==229,
            "15 groups do not partition 45 source elements/229 UV faces")
    report={
        "schema":"MCFR_INT5_B3_ORIGINAL_45_ELEMENT_TEXTURE_ROLE_CUE_TRIAGE_V1",
        "decision":"PASS_INDEPENDENT_SOURCE_UV_ROLE_CUE_AND_WHOLE_GROUP_VISUAL_TRIAGE_ONLY",
        "counts":{
            "source_elements_reopened":45,
            "original_source_faces_reopened":229,
            "native_F2_screenshots_reopened":16,
            "role_groups_context_checked":15,
            "named_source_texture_role_cue_elements":9,
            "role_cue_and_visible_group_appearance_consistent":8,
            "AF_tucked_seat_cue_obscured":1,
            "distinct_texture_without_role_name":1,
            "generic_texture_only_role_hypotheses":35,
            "new_exact_element_to_screen_pixel_identifications":0,
            "element_function_semantics_final_approvals":0,
            "INT6_training_or_redistribution_approvals":0,
            "new_minecraft_runs_or_screenshots":0,
        },
        "original_source_git_blobs":dict(sorted(PINNED.items())),
        "original_actions_artifact_ids":dict(sorted(origin.ARTIFACTS.items())),
        "source_versus_runtime_AF_drift_preserved":True,
        "caveat":"9/45 role-specific filename/UV cues and 8 group-compatible visual contexts do not prove 8 individually identified or functionally validated JSON elements.",
        "limits":[
            "Texture filename cues such as chair/seat, chair/back or cushion can corroborate a source author's intended appearance; they cannot alone prove actual seat usage, physics, or element-to-pixel mappings.",
            "AF tucked seat element's source seat texture cue exists but neighboring table obscures relevant screenshot region.",
            "Macaw stripped_acacia_log provides a distinctive color texture for element 0 without an inherently seat-specific texture name.",
            "Other 35 source parts have shared/generic texture; no filename-only material or structural function inference is permitted.",
            "Scene grades refer to whole-chair group shape, never per-element unique pixel segmentation.",
            "Minecraft F2 screenshots and third-party textures/JARs remain outside new GitHub commits; no AI training/redistribution rights claimed.",
        ],
    }
    return role_evidence,groups,report


def as_csv(rows):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return f.getvalue()


def output_files(raw,archives,b2raw):
    parts,groups,report=adjudicate(raw,archives,b2raw)
    files={OUT["parts"].as_posix():as_csv(parts),
           OUT["groups"].as_posix():as_csv(groups)}
    report["output_sha256"]={k:hashlib.sha256(v.encode("utf-8")).hexdigest()
                             for k,v in sorted(files.items())}
    files[OUT["summary"].as_posix()]=json.dumps(
        report,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    return files


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--archive-dir",type=Path,required=True)
    parser.add_argument("--out",type=Path,default=ROOT)
    parser.add_argument("--verify",action="store_true")
    parser.add_argument("--emit-json",action="store_true")
    a=parser.parse_args()
    archives=origin.download_archives(a.archive_dir)
    files=output_files(read_pinned(a.root),archives,origin.read_pinned(a.root))
    for path,content in files.items():
        p=a.out/path
        if a.verify:
            require(p.read_text(encoding="utf-8")==content,
                    "GitHub output drift "+path)
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(content,encoding="utf-8")
    if a.emit_json:
        print("INT5_B3_OUTPUT_JSON_BEGIN")
        print(json.dumps(files,ensure_ascii=True,separators=(",",":")))
        print("INT5_B3_OUTPUT_JSON_END")
    print("INT5_B3_SOURCE_ELEMENT45_UV229_ROLE_NAMED9_GROUP_COMPATIBLE8_OCCLUDED1")
    print("INT5_B3_ELEMENT_PIXEL_OR_FUNCTION_APPROVED_0")


if __name__=="__main__":
    main()
