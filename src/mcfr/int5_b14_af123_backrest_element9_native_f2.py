"""INT-5-B14: remove exactly one pinned AF123 model element in a disposable JAR.

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
ELEMENT_INDEX = 9
PARTS_CSV = ROOT / "project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
PATCH_INFO = "INT5_B14_AF123_ELEMENT9_DISPOSABLE_JAR_PROVENANCE_V1.json"
AUDIT = "INT5_B14_AF123_ELEMENT9_NATIVE_F2_CAUSAL_AUDIT_V1.json"

def require(test, reason):
    if not test:
        raise ValueError("INT5-B14: " + reason)

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
            chosen[0]["original_role_hypothesis"] == "BACKREST_ASSEMBLY" and
            chosen[0]["source_element_original_face_count"] == "5",
            "source B3 element9 backrest hypothesis or face count drift")
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
            require(len(elements[ELEMENT_INDEX]["faces"]) == 5 and
                    "from" in elements[ELEMENT_INDEX] and
                    "to" in elements[ELEMENT_INDEX],
                    "actual released element9 does not match original 5-face backrest support")
            return member, node, visited
        parent = node.get("parent")
        require(isinstance(parent, str) and parent.startswith("another_furniture:block/"),
                "original provider parent outside AF pinned namespace")
        member = model_member(parent)
    raise ValueError("INT5-B14: excessive model parent depth")

def isolated_child_override(child_bytes, provider_document):
    """Only original AF123 child override; never modify the shared provider."""
    child = json.loads(child_bytes.decode("utf-8-sig"))
    require(isinstance(child, dict) and
            child.get("parent") == "another_furniture:block/template/chair_tucked" and
            "elements" not in child,
            "original acacia10 child must inherit unmodified tucked template")
    elements = provider_document.get("elements")
    require(isinstance(elements, list) and len(elements) == 10 and
            sum(len(e["faces"]) for e in elements) == 46 and
            len(elements[ELEMENT_INDEX]["faces"]) == 5,
            "original AF123 provider 10/46 and target element9 5 faces required")
    modified = dict(child)
    modified["elements"] = [el for i, el in enumerate(elements) if i != ELEMENT_INDEX]
    require(len(modified["elements"]) == 9 and
            sum(len(e["faces"]) for e in modified["elements"]) == 41 and
            all(el == elements[i] for j, el in enumerate(modified["elements"])
                for i in ([j] if j < ELEMENT_INDEX else [j+1])) and
            {k:v for k,v in modified.items() if k != "elements"} == child,
            "source index9 only removal affected another source geometry or child binding")
    patched = json.dumps(modified, ensure_ascii=False, separators=(",", ":")).encode()
    require(patched != child_bytes, "AF123 child patch is not effective")
    return patched, elements[ELEMENT_INDEX]


def prepare_disposable_model_element_probe(game):
    """Official source pinned, single CHILD member changed in temporary Fabric JAR."""
    role = source_role_check()
    jar = Path(game) / "mods" / JAR_NAME
    original = jar.read_bytes()
    official_sha = hashlib.sha1(original).hexdigest()
    require(official_sha == h12.JAR_SHA1, "official AF 4.0.2 JAR SHA drift")
    with ZipFile(io.BytesIO(original)) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)) and archive.testzip() is None,
                "official source JAR member names or CRC invalid")
        originals = {n:archive.read(n) for n in names}
    provider_member, provider, chain = find_provider(originals)
    child_member = model_member(MODEL_ID)
    require(chain == [
        "assets/another_furniture/models/block/chair/acacia_10_tucked.json",
        "assets/another_furniture/models/block/template/chair_tucked.json"
    ] and provider_member == chain[1] and child_member == chain[0],
        "AF123 released child/parent model identity mismatch")
    require(blob(originals[provider_member]) ==
            "bbfd54f73fd764015ce320082ba531bd314a6dfd",
            "original pinned B5 official template parent Git blob drift")
    patch, removed = isolated_child_override(originals[child_member], provider)
    resources = dict(originals)
    resources[child_member] = patch
    tmp = jar.with_suffix(".b14-disposable")
    with ZipFile(tmp,"w") as archive:
        for info in infos:
            archive.writestr(info,resources[info.filename])
    with ZipFile(tmp) as archive:
        require(archive.testzip() is None and archive.namelist() == names,
                "temporary modified source JAR CRC/member list invalid")
        differences = [n for n in names if archive.read(n) != originals[n]]
        require(differences == [child_member] and
                all(archive.read(n) == originals[n]
                    for n in names if n != child_member),
                "B14 changed shared parent, texture, control, or any other JAR member")
        reread = json.loads(archive.read(child_member))
        require(reread.get("parent") == "another_furniture:block/template/chair_tucked" and
                len(reread["elements"]) == 9 and
                sum(len(e["faces"]) for e in reread["elements"]) == 41,
                "patched AF123 target child not original remaining 9/41")
    patched_sha = hashlib.sha1(tmp.read_bytes()).hexdigest()
    require(patched_sha != official_sha,"patched disposable JAR identical to official")
    tmp.replace(jar)
    require(hashlib.sha1(jar.read_bytes()).hexdigest() == patched_sha,
            "B14 disposable JAR was not installed")
    return {
        "schema":"MCFR_INT5_B14_CHILD_ONLY_SOURCE_ELEMENT9_REMOVAL/v1",
        "original_jar_name":JAR_NAME,
        "official_jar_sha1_before_modification":official_sha,
        "disposable_jar_sha1_after_modification":patched_sha,
        "selected_original_blockstate":b4.target_case().state(),
        "selected_original_model":MODEL_ID,
        "provider_member":provider_member,
        "modified_child_member":child_member,
        "resolved_original_model_chain":chain,
        "original_provider_git_blob_sha1":blob(originals[provider_member]),
        "original_child_git_blob_sha1":blob(originals[child_member]),
        "patched_child_sha256":sha(patch),
        "original_element_index":ELEMENT_INDEX,
        "original_element_from":removed["from"],
        "original_element_to":removed["to"],
        "original_element_faces":sorted(removed["faces"]),
        "original_source_B3_role_hypothesis":role["original_role_hypothesis"],
        "original_released_provider_element_count":10,
        "disposable_child_element_count":9,
        "original_released_face_count":46,
        "disposable_child_face_count":41,
        "modified_uncompressed_jar_member_count":1,
        "modified_member_is_only_target_child_json":True,
        "original_shared_provider_unmodified":True,
        "all_other_uncompressed_members_byte_identical":True,
        "original_official_jar_retained_outside_modified_test_run":True,
        "modified_jar_and_source_model_never_archived":True,
        "source_4_0_3_vs_release_4_0_2_not_assumed_equivalent":True,
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
            "element9_removal_source_intervention_delta_pixels": len(before),
            "element9_removal_repeated_delta_pixels": len(after),
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
            "MCFR_INT5_B14_CHILD_ONLY_SOURCE_ELEMENT9_REMOVAL/v1" and
            provenance["official_jar_sha1_before_modification"] == h12.JAR_SHA1 and
            provenance["modified_uncompressed_jar_member_count"] == 1 and
            provenance["original_element_index"] == 9 and
            provenance["original_released_face_count"] == 46 and
            provenance["disposable_child_face_count"] == 41 and
            provenance["modified_member_is_only_target_child_json"] is True and
            provenance["original_shared_provider_unmodified"] is True and
            provenance["all_other_uncompressed_members_byte_identical"] is True and
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
        v["element9_removal_source_intervention_delta_pixels"] > 0 and
        v["element9_removal_repeated_delta_pixels"] > 0
        for v in metrics.values())
    inside = all(
        v["intervention_pixels_outside_original_visible_chair_foreground"] == 0
        for v in metrics.values())
    decision = ("PASS_BOUNDED_AF123_ELEMENT9_REMOVAL_RENDER_RESPONSE"
                if passed_controls and changed_any and inside else
                "CONDITIONAL_ELEMENT_REMOVAL_RENDER_RESPONSE_OR_CONTROL_UNRESOLVED")
    summary = {
        "schema": "MCFR_INT5_B14_ELEMENT9_REMOVAL_NATIVE_F2_AUDIT/v1",
        "decision": decision,
        "official_release_model": MODEL_ID,
        "source_element_index": 9,
        "source_role_hypothesis_not_function": "BACKREST_ASSEMBLY",
        "original_source_part_key": "AF123/AF1394/9",
        "original_F2_baseline_B4_zip_sha256": "4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35",
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
            "Only one AF123 child JSON overrides original index9; shared tucked parent, all textures and every other source JAR resource remain identical.",
            "Comparing separate client sessions requires unchanged slab-only and AIR negative controls plus same-session A/A repeat controls.",
            "Removal may change neighboring lighting, occlusion and revealed surfaces; changed pixels are a response to this source intervention, not exclusive unmodified element-face pixel ownership.",
            "The B3 BACKREST_ASSEMBLY texture cue is still a hypothesis, not independently verified physical backrest function or material.",
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
