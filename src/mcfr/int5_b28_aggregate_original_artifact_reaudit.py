"""B28: independently reopen all eight B25 official Actions ZIPs and original F2 bytes.

This checker uses no transformed mod assets. It compares original PNG RGB screenshots
at threshold 24 in the same pinned ROI as B23, but recomputes the pixel counts.
Never infer physical role, UV-face ownership or training rights from this result.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from PIL import Image

# All SHA256 hashes were independently calculated from the actual GitHub archive ZIPs.
ARTIFACTS = {
    "AF121_without_leg0": (15100830746, "36f9a7fb1d45a40c1e95efd300b5243adba4c372cedd743d9f4410028f781a47"),
    "AF121_without_leg1": (15099504076, "9c67b0fc2d9436ea62780cfe1c946ed43a9188027b05cf989ffd4d6de6f96627"),
    "AF121_without_leg2": (15100188271, "ea8aa9693630c9aa8b56bd8f22e089b17e65c6730eb49f1435986a5dc725abe0"),
    "AF121_without_leg3": (15100900326, "aa92bc7ab970f411da7137d6e2b6a238db9cd70ce76e656dafe61b1d51dba00c"),
    "AF123_without_leg0": (15101276533, "a37fb7be115017d74fbd6c81e69f57f17193f9d3c17df3846f6f65f235c9c0a3"),
    "AF123_without_leg1": (15101786486, "34db06c2315ffc618c835138698fd4994160e1fa889ad356739025e527d320f7"),
    "AF123_without_leg2": (15101087396, "5fa823971ae8d5614ecd1efe746a9ee815cb9ee70820a9f96483f1e50b6d12fe"),
    "AF123_without_leg3": (15101797047, "b62e4b9c0e3b9c1e94016d11963e9e1b487acce46c02d0389f0159e9f8137905"),
}
CAMERAS = ("south", "north", "east", "west")
RELEASE_SHA1 = "c2f992081bdc4795ed6d87771a3b5f7c71103785"
ROI = (350, 275, 675, 620)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def rgb(z, path):
    with Image.open(io.BytesIO(z.read(path))) as image:
        require(image.format == "PNG" and image.size == (1024, 684), "Non-native F2: " + path)
        return np.asarray(image.convert("RGB"), dtype=np.int16)


def diff(a, b):
    return np.max(np.abs(a - b), axis=2) > 24


def audit_one(directory, key):
    artifact_id, original_sha = ARTIFACTS[key]
    path = directory / ("B25_" + key + ".zip")
    require(path.is_file(), "Missing artifact " + key)
    require(sha256(path.read_bytes()) == original_sha, "Original ZIP SHA mismatch: " + key)
    model, leg = key.split("_without_leg")
    leg = int(leg)
    target = model + "_5"
    support = 32 if model == "AF123" else 0
    metrics = {}
    coordinates = {}
    with ZipFile(path) as z:
        require(z.testzip() is None and len(z.namelist()) == 39, "ZIP CRC or file count")
        b25 = json.loads(z.read("INT5_B25_FOUR_ORIGINAL_LEG_OMISSIONS_SOURCE5_INDEPENDENT_F2_AUDIT_V1.json"))
        b23 = json.loads(z.read("INT5_B23_MULTI_CONTEXT_FOUR_VIEW_INDEPENDENT_F2_AUDIT_V1.json"))
        master = json.loads(z.read("INT5_B23_MULTI_CONTEXT_TWO_REAL_FABRIC_CLIENTS_MANIFEST_V1.json"))
        require(b25["target"] == target and b25["excluded_original_leg_index"] == leg, "Case identity")
        require(b25["context"] == "without_leg" + str(leg), "Case context")
        base = sorted({0, 1, 2, 3, 4, 6} - {leg})
        require(sorted(b25["retained_original_parent_indices_without_source5"]) == base, "Source index mask")
        require(sorted(b25["retained_original_parent_indices_with_source5"]) == sorted(base + [5]), "Source5 mask")
        require(b25["official_original_JAR_SHA1"] == RELEASE_SHA1 == master["official_AF_release_JAR_SHA1"], "JAR SHA1")
        require(master["real_native_F2_total"] == 32 and master["real_server_exact_chair_state_proofs"] == 32, "B25 counts")
        require(master["real_server_exact_support_slab_proofs"] == support, "Support counts")
        require(b25["actual_native_F2_SHA256_verified"] == 32 and b25["original_client_logs_SHA256_verified"] == 2, "B25 audit counts")
        require(b25["H03"] == "HOLD" and b25["H05"] == "CONDITIONAL" and b25["F70_unconditional_approved"] == 0, "Exit gates")
        for field in ("exclusive_single_original_leg_occlusion_cause_proven", "physical_leg_or_seat_role_proven",
                      "original_face_UV_GPU_pixel_owner_verified", "material_style_verified",
                      "third_party_training_or_redistribution_rights_approved"):
            require(b25[field] is False, "Unauthorized approval: " + field)
        images = {}
        chair_markers = 0
        slab_markers = 0
        for mode in ("with_5", "without_5"):
            m = json.loads(z.read(mode + "/manifest.json"))
            log = z.read(mode + "/client.log")
            require(m["exact_game_version"] == "1.21.1" and m["new_real_native_F2"] == 16, "Client version / count")
            require(m["exact_server_state_proofs"] == (32 if support else 16), "Per-client state count")
            require(sha256(log) == m["client_log_sha256"] == b23["real_client_log_SHA256"][mode], "Client log SHA")
            text = log.decode("utf8", "replace")
            require(set(m["f2_records"]) == set(CAMERAS), "Camera set")
            images[mode] = {}
            for camera in CAMERAS:
                frames = {}
                rows = m["f2_records"][camera]
                require(len(rows) == 4, "Four native frames expected")
                for stage, rec in rows.items():
                    file = mode + "/" + rec["image"]
                    require(rec["exact_state_checked"] is True and rec["dimensions"] == [1024, 684], "Native state")
                    require(sha256(z.read(file)) == rec["sha256"], "F2 PNG SHA")
                    for marker in rec["server_markers"].values():
                        require(marker in text, "Missing exact server marker: " + marker)
                        if marker.endswith("SUPPORT=PASS"):
                            slab_markers += 1
                        else:
                            chair_markers += 1
                    frames[stage] = rgb(z, file)
                if model == "AF121":
                    require(set(frames) == {"model1_before", "model1_after", "model3", "air"}, "AF121 stages")
                    before, after = frames["model1_before"], frames["model1_after"]
                else:
                    require(set(frames) == {"chair_plus_slab_before", "chair_plus_slab_after", "slab_only", "empty"}, "AF123 stages")
                    before, after = frames["chair_plus_slab_before"], frames["chair_plus_slab_after"]
                require(not diff(before, after).any(), "A/A temporal instability")
                images[mode][camera] = frames
        require(chair_markers == 32 and slab_markers == support, "Server proof markers")
        for camera in CAMERAS:
            w, wo = images["with_5"][camera], images["without_5"][camera]
            stage = "chair_plus_slab_before" if support else "model1_before"
            negative = "slab_only" if support else "air"
            require(not diff(w[negative], wo[negative]).any(), "Negative control changed")
            delta = diff(w[stage], wo[stage])
            foreground = diff(w[stage], w[negative]) | diff(wo[stage], wo[negative])
            require(not (delta & ~foreground).any(), "Pixels outside original foreground")
            x0, y0, x1, y1 = ROI
            roi_mask = np.zeros_like(delta)
            roi_mask[y0:y1, x0:x1] = True
            require(not (delta & ~roi_mask).any(), "Change outside pinned ROI")
            ys, xs = np.where(delta)
            count = len(xs)
            metric = b23["original_four_camera_source5_addition_metrics"][camera]
            require(count == metric["five_addition_before_pixels"] == metric["five_addition_after_pixels"],
                    "Independent source5 pixel disagreement")
            require(count == int(diff(w["chair_plus_slab_after" if support else "model1_after"],
                                      wo["chair_plus_slab_after" if support else "model1_after"]).sum()),
                    "Repeat camera disagrees")
            metrics[camera] = count
            coordinates[camera] = [[int(x), int(y)] for x, y in zip(xs, ys)]
        values = [metrics[cam] for cam in CAMERAS]
        require(values == b25["pixels_south_north_east_west"], "B25 four-camera audit disagreement")
        decision = ("SOURCE5_ADDS_PIXELS_WHEN_ORIGINAL_LEG_OMITTED" if any(values)
                    else "SOURCE5_STILL_NOT_VISIBLE_WITH_THIS_LEG_OMITTED")
        require(decision == b25["decision"], "Original B25 decision disagreement")
    return {
        "target": target, "omitted_index_hypothesis_only": leg, "artifact_id": artifact_id,
        "original_zip_sha256": original_sha, "native_F2_sha256": 32, "client_log_sha256": 2,
        "server_chair_markers": 32, "support_markers": support,
        "pixels_south_north_east_west": values, "changed_pixel_xy_by_view": coordinates,
        "decision": decision, "sole_physical_occlusion_source_proven": False
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    records = [audit_one(options.directory, key) for key in ARTIFACTS]
    report = {
        "schema": "MCFR_INT5_B28_B25_ALL8_INDEPENDENT_ORIGINAL_F2/v1",
        "source_run": 45784956570, "source_head": "2d725de28e77e4b2633c0b0719f9dc2bfb76c7fd",
        "source_jar_sha1": RELEASE_SHA1, "zip_sha256_crc_verified": 8,
        "native_F2_sha256_verified": sum(r["native_F2_sha256"] for r in records),
        "client_log_sha256_verified": sum(r["client_log_sha256"] for r in records),
        "chair_state_markers_verified": sum(r["server_chair_markers"] for r in records),
        "support_slab_markers_verified": sum(r["support_markers"] for r in records),
        "physical_role_approved": 0, "material_style_approved": 0, "face_UV_exclusive_pixel_approved": 0,
        "third_party_AI_training_distribution_approved": 0,
        "H03": "HOLD", "H05": "CONDITIONAL", "F70_unconditional": 0,
        "records": records
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print("B28_ORIGINAL_8_ARTIFACTS_ALL_RECOMPUTED", len(records), report["native_F2_sha256_verified"])
    for record in records:
        print(record["target"], record["omitted_index_hypothesis_only"],
              record["pixels_south_north_east_west"], record["decision"])


if __name__ == "__main__":
    main()
