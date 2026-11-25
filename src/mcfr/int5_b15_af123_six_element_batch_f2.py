"""INT-5-B15: six independent AF123 original element interventions, one CI matrix.

Each job runs a fresh pinned official Fabric 4.0.2 JAR and removes precisely
one element from the child model, preserving every other uncompressed member.
No modified JAR or licensed textures are distributed in Git/artifacts.
Changed screen pixels indicate bounded source-intervention response, NOT
exclusive original face/UV-to-pixel ownership, function, material or rights.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

from . import int5_af_tucked_slab_control as b4
from . import int5_b14_af123_backrest_element9_native_f2 as b14
from . import int4_h12_af_chair_samepose_f2_capture as h12

ROOT = Path(__file__).resolve().parents[2]
INDICES = (0, 1, 2, 3, 5, 6)
FACES = {0: 5, 1: 5, 2: 5, 3: 5, 5: 4, 6: 4}
ROLES = {0: "LEG_OR_LOWER_POST", 1: "LEG_OR_LOWER_POST",
         2: "LEG_OR_LOWER_POST", 3: "LEG_OR_LOWER_POST",
         5: "LOWER_FRAME", 6: "LOWER_FRAME"}
JAR_NAME = "another_furniture-fabric-4.0.2.jar"
MODEL = "another_furniture:block/chair/acacia_10_tucked"
CHILD = "assets/another_furniture/models/block/chair/acacia_10_tucked.json"
PARENT = "assets/another_furniture/models/block/template/chair_tucked.json"
PROVENANCE = "INT5_B15_DISPOSABLE_SOURCE_ELEMENT_PROVENANCE_V1.json"
AUDIT = "INT5_B15_ELEMENT_NATIVE_F2_AUDIT_V1.json"
BASELINE_ZIP_SHA = "4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35"

def require(ok, message):
    if not ok:
        raise ValueError("INT5-B15: " + message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_role(index):
    require(index in INDICES, "not a selected, previously untested AF123 source element")
    with (ROOT / "project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv").open(
            encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    matches = [row for row in rows if row["child_model_key"] == "AF123"
               and row["provider_key"] == "AF1394"
               and row["original_source_element_index"] == str(index)]
    require(len(matches) == 1, "B3 source index not unique")
    row = matches[0]
    require(row["original_role_hypothesis"] == ROLES[index] and
            row["source_element_original_face_count"] == str(FACES[index]) and
            row["individual_element_to_original_F2_pixels_approved"] == "false" and
            row["part_function_verified"] == "false" and
            row["material_or_style_verified"] == "false" and
            row["training_or_redistribution_rights_approved"] == "false",
            "B3 original source face, provisional role, or approval boundary changed")
    return row

def override_child(original_child, parent, index):
    source_role(index)
    child = json.loads(original_child.decode("utf-8-sig"))
    require(child.get("parent") == "another_furniture:block/template/chair_tucked"
            and "elements" not in child, "child must inherit original shared parent")
    elements = parent.get("elements")
    require(isinstance(elements, list) and len(elements) == 10 and
            sum(len(e["faces"]) for e in elements) == 46 and
            len(elements[index]["faces"]) == FACES[index],
            "pinned original 10/46 source and exact target face count required")
    patched = dict(child)
    patched["elements"] = [el for n,el in enumerate(elements) if n != index]
    require(patched["elements"] == elements[:index] + elements[index+1:] and
            len(patched["elements"]) == 9 and
            sum(len(e["faces"]) for e in patched["elements"]) == 46-FACES[index] and
            {k:v for k,v in patched.items() if k != "elements"} == child,
            "not exactly one removed source element")
    raw = json.dumps(patched, ensure_ascii=False, separators=(",", ":")).encode()
    require(raw != original_child, "child override has no effect")
    return raw, elements[index]

def prepare(game, index):
    role = source_role(index)
    jar = Path(game) / "mods" / JAR_NAME
    original = jar.read_bytes()
    require(hashlib.sha1(original).hexdigest() == h12.JAR_SHA1,
            "official Fabric 4.0.2 JAR SHA mismatch")
    with ZipFile(io.BytesIO(original)) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)) and z.testzip() is None,
                "official JAR CRC or duplicate member failed")
        entries = {name:z.read(name) for name in names}
    member, provider, chain = b14.find_provider(entries)
    require(member == PARENT and chain == [CHILD,PARENT] and
            blob(entries[PARENT]) == "bbfd54f73fd764015ce320082ba531bd314a6dfd" and
            blob(entries[CHILD]) == "71fd514e28b36b47b45cc6a38594b4d11059e6ff",
            "official pinned released child/provider source changed")
    altered, removed = override_child(entries[CHILD], provider, index)
    tmp = jar.with_suffix(".b15-disposable")
    with ZipFile(tmp,"w") as z:
        for info in infos:
            z.writestr(info, altered if info.filename == CHILD else entries[info.filename])
    with ZipFile(tmp) as z:
        require(z.testzip() is None and z.namelist() == names,
                "temporary JAR ZIP CRC or member ordering changed")
        difference = [n for n in names if z.read(n) != entries[n]]
        require(difference == [CHILD] and
                all(z.read(n) == entries[n] for n in names if n != CHILD),
                "any non-child source or original texture was changed")
        result = json.loads(z.read(CHILD))
        require(len(result["elements"]) == 9 and
                sum(len(e["faces"]) for e in result["elements"]) == 46-FACES[index],
                "disposable child model elements/faces incorrect")
    patched_sha = hashlib.sha1(tmp.read_bytes()).hexdigest()
    require(patched_sha != h12.JAR_SHA1, "disposable model is identical to official")
    tmp.replace(jar)
    require(hashlib.sha1(jar.read_bytes()).hexdigest() == patched_sha,
            "disposable JAR was not installed")
    return {
        "schema": "MCFR_INT5_B15_SINGLE_CHILD_ELEMENT_REMOVAL/v1",
        "source_key": f"AF123/AF1394/{index}",
        "original_element_index": index,
        "original_role_hypothesis_not_function": role["original_role_hypothesis"],
        "original_element_faces": sorted(removed["faces"]),
        "original_element_from": removed["from"],
        "original_element_to": removed["to"],
        "original_element_face_count": FACES[index],
        "original_provider_elements": 10, "original_provider_faces": 46,
        "disposable_child_elements": 9,
        "disposable_child_faces": 46-FACES[index],
        "official_release_sha1": h12.JAR_SHA1,
        "disposable_jar_sha1": patched_sha,
        "pinned_parent_git_blob": blob(entries[PARENT]),
        "pinned_child_git_blob": blob(entries[CHILD]),
        "modified_child_sha256": sha(altered),
        "model": MODEL,
        "original_blockstate": b4.target_case().state(),
        "only_one_original_uncompressed_member_changed": True,
        "shared_parent_and_other_resources_byte_identical": True,
        "original_jar_retained_outside_probe": True,
        "original_jar_and_disposable_jar_never_distributed": True,
    }

def capture(command, env, game, output, version, index):
    require(version == "1.21.1", "official AF123 source requires 1.21.1")
    source_role(index)
    metadata = prepare(game,index)
    result = b4.capture(command,env,game,output,version)
    (Path(output)/PROVENANCE).write_text(
        json.dumps(metadata,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return result

def metrics(original, changed):
    # Original-source intervention is isolated to one child and controlled
    # by repeated A, unchanged slab-only, unchanged AIR and foreground mask.
    return b14.evaluate(original, changed)

def audit(baseline_dir, modified_dir, index):
    source_role(index)
    baseline_dir,modified_dir=Path(baseline_dir),Path(modified_dir)
    original=b4.audit(baseline_dir)
    pinned=json.loads((ROOT/"project/integration/INT5_B4_AF_TUCKED_SLAB_REAL_F2_AUDIT_V1.json").read_text(encoding="utf-8"))
    require(original == pinned and
            original["decision"] ==
            "PASS_REAL_FABRIC_BOTH_VIEW_SUPPORTED_TUCKED_CHAIR_VS_SLAB_CONTROLS",
            "historic original B4 baseline differs from pinned source audit")
    modified=b4.audit(modified_dir)
    require(modified["original_native_F2_verified"] == 8 and
            modified["exact_server_chair_state_and_slab_pair_checks"] == 16,
            "new independent real game F2 or exact chair/slab server state missing")
    prov=json.loads((modified_dir/PROVENANCE).read_text(encoding="utf-8"))
    require(prov["source_key"] == f"AF123/AF1394/{index}" and
            prov["original_element_face_count"] == FACES[index] and
            prov["disposable_child_faces"] == 46-FACES[index] and
            prov["official_release_sha1"] == h12.JAR_SHA1 and
            prov["only_one_original_uncompressed_member_changed"] is True and
            prov["shared_parent_and_other_resources_byte_identical"] is True,
            "disposable JAR does not prove single unchanged-source intervention")
    base_doc=json.loads((baseline_dir/b4.ORIGINAL).read_text(encoding="utf-8"))
    mod_doc=json.loads((modified_dir/b4.ORIGINAL).read_text(encoding="utf-8"))
    require(base_doc["camera_poses"] == mod_doc["camera_poses"] and
            base_doc["pinned_original_source_case"] ==
            mod_doc["pinned_original_source_case"] == "AF123_north" and
            base_doc["source_runtime_selected_state"] ==
            mod_doc["source_runtime_selected_state"],
            "original and modified F2 camera, server state, or model selection differ")
    raw=metrics(b14.open_frames(baseline_dir,base_doc),
                b14.open_frames(modified_dir,mod_doc))
    normalized={}
    for view,row in raw.items():
        normalized[view]={
            "foreground_pixels": row["original_visible_chair_foreground_pixels"],
            "intervention_before_pixels": row["element9_removal_source_intervention_delta_pixels"],
            "intervention_repeated_pixels": row["element9_removal_repeated_delta_pixels"],
            "slab_control_delta_pixels": row["unchanged_slab_only_negative_control_pixels"],
            "air_control_delta_pixels": row["unchanged_air_negative_control_pixels"],
            "temporal_delta_pixels": row["modified_session_temporal_delta_pixels"],
            "outside_original_chair_foreground_pixels": row["intervention_pixels_outside_original_visible_chair_foreground"],
        }
    controls=all(x["slab_control_delta_pixels"]==0 and
                 x["air_control_delta_pixels"]==0 and
                 x["temporal_delta_pixels"]==0 and
                 x["outside_original_chair_foreground_pixels"]==0
                 for x in normalized.values())
    visible=any(x["intervention_before_pixels"]>0 and
                x["intervention_repeated_pixels"]>0
                for x in normalized.values())
    decision=("PASS_BOUNDED_SINGLE_SOURCE_RENDER_RESPONSE" if controls and visible
              else "NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS" if controls
              else "CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS")
    report={
        "schema":"MCFR_INT5_B15_SINGLE_ELEMENT_NATIVE_F2_AUDIT/v1",
        "source_key":f"AF123/AF1394/{index}",
        "decision":decision,
        "pinned_source_original_element":index,
        "role_hypothesis_not_function":ROLES[index],
        "provenance":prov,
        "baseline_zip_sha256":BASELINE_ZIP_SHA,
        "original_B4_native_F2_sha256":original["native_F2_sha256"],
        "modified_native_F2_sha256":modified["native_F2_sha256"],
        "original_B4_client_log_sha256":original["original_client_log_sha256"],
        "new_client_log_sha256":modified["original_client_log_sha256"],
        "original_real_F2_count":8,
        "modified_real_F2_count":8,
        "modified_exact_chair_and_support_state_checks":16,
        "per_view":normalized,
        "stable_negative_controls":controls,
        "detected_bounded_visual_response":visible,
        "unique_original_face_UV_to_GPU_pixel_approval":False,
        "part_function_material_style_approval":False,
        "AI_training_or_redistribution_rights_approval":False,
        "limits":[
            "Single removed source geometry can alter neighboring occlusion and lighting: changed pixels are not uniquely attributable to original faces.",
            "Invisible elements may yield NO_VISIBLE_SOURCE_RESPONSE without proving the original element is absent.",
            "Only exactly AF123 supported north tucked variant10, this release 4.0.2, two cameras and their stable controls are tested.",
            "This run is not an INT5 semantic/functional approval or INT6 license grant.",
        ],
    }
    (modified_dir/AUDIT).write_text(
        json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--index",type=int,choices=INDICES,required=True)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--modified",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.baseline,a.modified,a.index)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    if result["decision"]=="CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
