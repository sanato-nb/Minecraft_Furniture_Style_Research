"""INT-5-B5: remove exactly one pinned AF123 model element in a disposable JAR.

The official Fabric 4.0.2 JAR is SHA checked BEFORE any change. The modified
JAR is only used in an isolated Minecraft run; it is never exported. Compare
that run's genuine native F2 images to the verified, unchanged B4 eight-F2
baseline. A source-element removal can establish a bounded screen response;
it cannot prove original visible pixel ownership, gameplay function or rights.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

from . import int5_af_tucked_slab_control as b4
from . import int4_h12_af_chair_samepose_f2_capture as h12

ROOT = Path(__file__).resolve().parents[2]
JAR_NAME = "another_furniture-fabric-4.0.2.jar"
MODEL_ID = "another_furniture:block/chair/acacia_10_tucked"
ELEMENT_INDEX = 4
PARTS_CSV = ROOT / "project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
PATCH_INFO = "INT5_B5_AF123_ELEMENT4_DISPOSABLE_JAR_PROVENANCE_V1.json"
AUDIT = "INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json"

def require(test, reason):
    if not test:
        raise ValueError("INT5-B5: " + reason)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

def model_member(resource):
    namespace, sep, path = resource.partition(":")
    require(sep and namespace and path.startswith("block/") and
            ".." not in path.split("/"), "invalid source model path")
    return f"assets/{namespace}/models/{path}.json"

def source_role_check():
    with PARTS_CSV.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    chosen = [r for r in rows if r["child_model_key"] == "AF123"
              and r["original_source_element_index"] == str(ELEMENT_INDEX)]
    require(len(chosen) == 1 and chosen[0]["provider_key"] == "AF1394" and
            chosen[0]["original_role_hypothesis"] == "SEAT_LAYER" and
            chosen[0]["source_element_original_face_count"] == "6",
            "source B3 element4 seat hypothesis or face count drift")
    require(chosen[0]["individual_element_to_original_F2_pixels_approved"] == "false",
            "B3 incorrectly promoted original pixel identification")
    return chosen[0]

def find_provider(resources):
    """Follow the actual released child/parent chain; never infer from filename."""
    member = model_member(MODEL_ID)
    visited = []
    for _ in range(10):
        require(member in resources and member not in visited,
                "official 4.0.2 source model missing or cyclic: " + member)
        visited.append(member)
        node = json.loads(resources[member].decode("utf-8-sig"))
        require(isinstance(node, dict), "model is not an object")
        if "elements" in node:
            elements = node["elements"]
            require(isinstance(elements, list) and len(elements) == 10,
                    "actual 4.0.2 provider does not contain ten expected elements")
            require(all(isinstance(el, dict) and
                        isinstance(el.get("faces"), dict) for el in elements),
                    "nonstandard original element")
            require(sum(len(el["faces"]) for el in elements) == 46,
                    "actual released provider has unexpected face count")
            require(len(elements[ELEMENT_INDEX]["faces"]) == 6 and
                    "from" in elements[ELEMENT_INDEX] and
                    "to" in elements[ELEMENT_INDEX],
                    "actual released element4 does not match six-face cuboid")
            return member, node, visited
        parent = node.get("parent")
        require(isinstance(parent, str) and parent.startswith("another_furniture:block/"),
                "original provider parent outside AF pinned namespace")
        member = model_member(parent)
    raise ValueError("INT5-B5: excessive model parent depth")

def prepare_disposable_model_element_probe(game):
    """Only one JSON member changes; immutable official SHA and source role pinned."""
    role = source_role_check()
    jar = Path(game) / "mods" / JAR_NAME
    original = jar.read_bytes()
    original_jar_sha = hashlib.sha1(original).hexdigest()
    require(original_jar_sha == h12.JAR_SHA1, "official runtime JAR SHA1 drift")
    with ZipFile(io.BytesIO(original)) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)) and archive.testzip() is None,
                "source JAR ZIP not unique or CRC invalid")
        contents = {name: archive.read(name) for name in names}
    member, document, chain = find_provider(contents)
    source_member = contents[member]
    removed = document["elements"][ELEMENT_INDEX]
    face_directions = sorted(removed["faces"])
    altered = dict(document)
    altered["elements"] = [el for idx, el in enumerate(document["elements"])
                           if idx != ELEMENT_INDEX]
    require(len(altered["elements"]) == 9 and
            sum(len(e["faces"]) for e in altered["elements"]) == 40,
            "modified provider unexpectedly affects other elements")
    changed = json.dumps(altered, ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    require(changed != source_member, "provider JSON not modified")
    contents[member] = changed
    temp = jar.with_suffix(".b5-disposable")
    with ZipFile(temp, "w") as archive:
        for info in infos:
            archive.writestr(info, contents[info.filename])
    with ZipFile(temp) as archive:
        require(archive.testzip() is None and archive.namelist() == names,
                "patched ZIP lost a member or CRC")
        changed_members = [name for name in names
                           if archive.read(name) != (
                               source_member if name == member
                               else contents[name])]
        require(changed_members == [member], "more than one model resource altered")
        rebuilt = json.loads(archive.read(member).decode("utf-8"))
        require(len(rebuilt["elements"]) == 9 and
                rebuilt["elements"] == altered["elements"],
                "removed element not re-opened correctly")
    patched_sha = hashlib.sha1(temp.read_bytes()).hexdigest()
    require(patched_sha != original_jar_sha, "disposable JAR SHA unchanged")
    temp.replace(jar)
    return {
        "schema": "MCFR_INT5_B5_DISPOSABLE_SINGLE_SOURCE_ELEMENT_REMOVAL/v1",
        "original_jar_name": JAR_NAME,
        "official_jar_sha1_before_modification": original_jar_sha,
        "disposable_jar_sha1_after_modification": patched_sha,
        "selected_original_blockstate": b4.target_case().state(),
        "selected_original_model": MODEL_ID,
        "provider_member": member,
        "resolved_original_model_chain": chain,
        "original_provider_git_blob_sha1": blob(source_member),
        "patched_provider_sha256": sha(changed),
        "original_element_index": ELEMENT_INDEX,
        "original_element_from": removed["from"],
        "original_element_to": removed["to"],
        "original_element_faces": face_directions,
        "original_source_B3_role_hypothesis": role["original_role_hypothesis"],
        "original_released_provider_element_count": 10,
        "disposable_provider_element_count": 9,
        "original_released_face_count": 46,
        "disposable_provider_face_count": 40,
        "modified_uncompressed_jar_member_count": 1,
        "modified_member_is_only_provider_json": True,
        "original_official_jar_retained_outside_modified_test_run": True,
        "modified_jar_and_source_model_never_archived": True,
        "source_4_0_3_vs_release_4_0_2_not_assumed_equivalent": True,
    }

def capture(command, env, game, output, version):
    require(version == "1.21.1", "source experiment requires Fabric 1.21.1")
    provenance = prepare_disposable_model_element_probe(game)
    result = b4.capture(command, env, game, output, version)
    (Path(output) / PATCH_INFO).write_text(
        json.dumps(provenance, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
    return result

def open_frames(directory, manifest):
    require(manifest["native_F2_screenshots"] == 8,
            "native source screenshot count changed")
    frames = {}
    for view in b4.VIEWS:
        frames[view] = {}
        for stage in b4.STAGES:
            record = manifest["views"][view][stage]
            label = b4.label(view, stage)
            require(record["image"] == label + ".png" and
                    record["dimensions"] == [1024, 684],
                    "actual native F2 manifest mismatch " + label)
            data = (Path(directory) / record["image"]).read_bytes()
            require(sha(data) == record["sha256"],
                    "native F2 bytes changed " + label)
            with Image.open(io.BytesIO(data)) as raw:
                raw.load()
                require(raw.format == "PNG" and raw.size == (1024, 684),
                        "source F2 is not original PNG " + label)
                frames[view][stage] = raw.convert("RGB")
    return frames

def evaluate(baseline, modified):
    """Bounded pixel response; screen perturbation != unique source pixel owner."""
    result = {}
    for view in b4.VIEWS:
        a = baseline[view]
        b = modified[view]
        foreground = b4.pixel_delta(a["chair_plus_slab_before"], a["slab_only"])
        before = b4.pixel_delta(a["chair_plus_slab_before"],
                                b["chair_plus_slab_before"])
        after = b4.pixel_delta(a["chair_plus_slab_after"],
                               b["chair_plus_slab_after"])
        slab = b4.pixel_delta(a["slab_only"], b["slab_only"])
        air = b4.pixel_delta(a["empty"], b["empty"])
        patch_temporal = b4.pixel_delta(b["chair_plus_slab_before"],
                                        b["chair_plus_slab_after"])
        result[view] = {
            "original_visible_chair_foreground_pixels": len(foreground),
            "element4_removal_source_intervention_delta_pixels": len(before),
            "element4_removal_repeated_delta_pixels": len(after),
            "modified_session_temporal_delta_pixels": len(patch_temporal),
            "unchanged_slab_only_negative_control_pixels": len(slab),
            "unchanged_air_negative_control_pixels": len(air),
            "intervention_pixels_outside_original_visible_chair_foreground":
                len(before - foreground),
            "intervention_screen_effect_not_unique_element_pixel_ownership": True,
        }
    return result

def audit(baseline_dir, modified_dir):
    baseline_dir = Path(baseline_dir)
    modified_dir = Path(modified_dir)
    original = b4.audit(baseline_dir)
    anchored = json.loads(
        (ROOT / "project/integration/INT5_B4_AF_TUCKED_SLAB_REAL_F2_AUDIT_V1.json")
        .read_text(encoding="utf-8"))
    require(original == anchored and
            original["decision"] ==
            "PASS_REAL_FABRIC_BOTH_VIEW_SUPPORTED_TUCKED_CHAIR_VS_SLAB_CONTROLS",
            "original B4 baseline artifact not equal to committed real F2 audit")
    altered = b4.audit(modified_dir)
    require(altered["original_native_F2_verified"] == 8 and
            altered["exact_server_chair_state_and_slab_pair_checks"] == 16,
            "modified run missing genuine F2 or source server-state confirmations")
    provenance = json.loads((modified_dir / PATCH_INFO).read_text(encoding="utf-8"))
    require(provenance["schema"] ==
            "MCFR_INT5_B5_DISPOSABLE_SINGLE_SOURCE_ELEMENT_REMOVAL/v1" and
            provenance["official_jar_sha1_before_modification"] == h12.JAR_SHA1 and
            provenance["modified_uncompressed_jar_member_count"] == 1 and
            provenance["original_element_index"] == 4 and
            provenance["original_released_face_count"] == 46 and
            provenance["disposable_provider_face_count"] == 40 and
            provenance["modified_jar_and_source_model_never_archived"] is True,
            "original versus single-element disposable-JAR provenance missing")
    base_manifest = json.loads((baseline_dir / b4.ORIGINAL).read_text(encoding="utf-8"))
    mod_manifest = json.loads((modified_dir / b4.ORIGINAL).read_text(encoding="utf-8"))
    require(base_manifest["camera_poses"] == mod_manifest["camera_poses"] and
            base_manifest["pinned_original_source_case"] ==
            mod_manifest["pinned_original_source_case"] == "AF123_north" and
            base_manifest["source_runtime_selected_state"] ==
            mod_manifest["source_runtime_selected_state"] and
            base_manifest["views"].keys() == mod_manifest["views"].keys(),
            "between-session original chair/camera/selector is not identical")
    metrics = evaluate(open_frames(baseline_dir, base_manifest),
                       open_frames(modified_dir, mod_manifest))
    passed_controls = all(
        v["unchanged_slab_only_negative_control_pixels"] == 0 and
        v["unchanged_air_negative_control_pixels"] == 0 and
        v["modified_session_temporal_delta_pixels"] == 0
        for v in metrics.values())
    changed_any = any(
        v["element4_removal_source_intervention_delta_pixels"] > 0 and
        v["element4_removal_repeated_delta_pixels"] > 0
        for v in metrics.values())
    inside = all(
        v["intervention_pixels_outside_original_visible_chair_foreground"] == 0
        for v in metrics.values())
    decision = ("PASS_BOUNDED_AF123_ELEMENT4_REMOVAL_RENDER_RESPONSE"
                if passed_controls and changed_any and inside else
                "CONDITIONAL_ELEMENT_REMOVAL_RENDER_RESPONSE_OR_CONTROL_UNRESOLVED")
    summary = {
        "schema": "MCFR_INT5_B5_ELEMENT4_REMOVAL_NATIVE_F2_AUDIT/v1",
        "decision": decision,
        "official_release_model": MODEL_ID,
        "source_element_index": 4,
        "source_role_hypothesis_not_function": "SEAT_LAYER",
        "original_baseline_F2_sha256": original["native_F2_sha256"],
        "modified_runtime_F2_sha256": altered["native_F2_sha256"],
        "original_client_log_sha256": original["original_client_log_sha256"],
        "modified_client_log_sha256": altered["original_client_log_sha256"],
        "two_separate_real_game_sessions": 2,
        "baseline_F2_verified": 8,
        "disposable_model_F2_verified": 8,
        "modified_session_server_chair_slab_state_checks": 16,
        "provenance": provenance,
        "per_view_effects": metrics,
        "unmodified_controls_equal": passed_controls,
        "visible_screen_effect_detected": changed_any,
        "no_change_outside_original_chair_foreground": inside,
        "individual_original_element_pixel_ownership_approved": False,
        "physical_seating_or_material_approved": False,
        "final_INT5_part_meaning_approvals": 0,
        "INT6_AI_training_or_redistribution_approvals": 0,
        "limits": [
            "One model element is removed only from a disposable copy of the official release JAR, not from the source research or original game asset.",
            "Comparing separate client sessions requires unchanged slab-only and AIR negative controls plus same-session A/A repeat controls.",
            "Removal may change neighboring lighting, occlusion and revealed surfaces; changed pixels are a response to this source intervention, not exclusive unmodified element-face pixel ownership.",
            "The source B3 label SEAT_LAYER is still a hypothesis, not an independently established usable seat or physical material.",
            "Existing original B4 and old strict INT4/H/F gates and INT6 rights are unchanged."
        ],
    }
    (modified_dir / AUDIT).write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--modified", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.baseline, args.modified), ensure_ascii=False))

if __name__ == "__main__":
    main()
