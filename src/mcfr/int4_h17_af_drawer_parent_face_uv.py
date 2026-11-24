"""INT-4 H17: derive AF S20/S21 original face, UV and texel provenance.

This is STATIC source inspection of a SHA-pinned official 4.0.2 Fabric JAR.
It complements, but never replaces, the actual native F2 S20/S21 evidence in H17's
parent PR #97. No per-pixel GPU UV causal inference is implied.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

AF_RELEASE_SHA1 = "c2f992081bdc4795ed6d87771a3b5f7c71103785"
NS = "another_furniture"
BLOCKSTATE_PATH = f"assets/{NS}/blockstates/oak_drawer.json"
STATE_MODELS = {
    "S20": ("facing=north,open=false", f"{NS}:block/drawer/oak"),
    "S21": ("facing=north,open=true", f"{NS}:block/drawer/oak_open"),
}
SOURCE_RESULT_PATH = "project/integration/INT4_H03_H05_S20_S21_REAL_NORTH_F2_RESULT_V1.json"
F2_ORIGINAL_RUN = 45251124211
AUDIT_NAME = "INT4_H17_AF_DRAWER_ORIGINAL_PARENT_FACE_UV_TEXEL_AUDIT_V1.json"


def require(condition, label):
    if not condition:
        raise ValueError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identifier_to_path(identifier, kind):
    require(isinstance(identifier, str) and ":" in identifier, "H17_BAD_RESOURCE_ID")
    namespace, name = identifier.split(":", 1)
    require(namespace == NS and name and all(
        chunk not in ("", ".", "..") for chunk in name.split("/")
    ) and "\\" not in name, "H17_INVALID_MODEL_NAMESPACE_OR_PATH")
    require(kind in ("models", "textures"), "H17_BAD_ASSET_KIND")
    return f"assets/{namespace}/{kind}/{name}." + ("json" if kind == "models" else "png")


def read_json(archive, name):
    return json.loads(archive.read(name).decode("utf-8"))


def resolve_leaf(archive, model_id):
    """Resolve inheritance root -> leaf; a child 'elements' overrides parent."""
    lineage = []
    visited = set()
    current = model_id
    external_vanilla_parent = None
    while True:
        # A mod's geometry-bearing template can inherit vanilla block/block.
        # Do not invent vanilla parent data from an absent Minecraft client JAR.
        if current.startswith("minecraft:"):
            external_vanilla_parent = current
            break
        require(current not in visited, "H17_MODEL_PARENT_CYCLE")
        visited.add(current)
        name = identifier_to_path(current, "models")
        raw = archive.read(name)
        doc = json.loads(raw.decode("utf-8"))
        require(isinstance(doc, dict), "H17_MODEL_NOT_OBJECT")
        lineage.append((name, sha(raw), doc))
        parent = doc.get("parent")
        if not parent:
            break
        if ":" not in parent:
            parent = NS + ":" + parent
        current = parent
        require(len(lineage) < 24, "H17_MODEL_CHAIN_TOO_LONG")
    textures = {}
    elements = None
    provider = None
    for name, _, doc in reversed(lineage):
        textures.update(doc.get("textures", {}))
        if "elements" in doc:
            elements = doc["elements"]
            provider = name
    require(isinstance(elements, list) and len(elements) > 0, "H17_NO_ORIGINAL_PARENT_GEOMETRY")
    return {
        "source_chain_root_to_leaf": [
            {"path": p, "sha256": digest} for p, digest, _ in reversed(lineage)
        ],
        "geometry_provider": provider,
        "external_vanilla_parent_not_opened": external_vanilla_parent,
        "textures": textures,
        "elements": elements,
    }


def resolve_texture(textures, ref):
    """Follow #alias chains while refusing cycles and missing symbols."""
    aliases = []
    candidate = ref
    while isinstance(candidate, str) and candidate.startswith("#"):
        key = candidate[1:]
        require(key not in aliases, "H17_TEXTURE_ALIAS_CYCLE")
        aliases.append(key)
        require(key in textures, "H17_TEXTURE_ALIAS_MISSING_" + key)
        candidate = textures[key]
    require(isinstance(candidate, str) and ":" in candidate, "H17_TEXTURE_TERMINAL_INVALID")
    return candidate, aliases


def flatten_faces(model):
    faces = []
    for idx, element in enumerate(model["elements"]):
        require("from" in element and "to" in element and
                isinstance(element.get("faces"), dict), "H17_BAD_ELEMENT")
        for direction, face in element["faces"].items():
            require(direction in ("north", "south", "east", "west", "up", "down") and
                    isinstance(face, dict) and "texture" in face, "H17_BAD_FACE")
            terminal, aliases = resolve_texture(model["textures"], face["texture"])
            uv = face.get("uv")
            if uv is not None:
                require(len(uv) == 4 and all(isinstance(n, (int, float)) and
                        math.isfinite(n) for n in uv), "H17_INVALID_FACE_UV")
            faces.append({
                "element": idx, "direction": direction, "texture_ref": face["texture"],
                "texture_id": terminal, "texture_alias_chain": aliases,
                "uv": uv, "uv_explicit": uv is not None,
                "face_uv_rotation": face.get("rotation", 0),
                "cullface": face.get("cullface"),
                "element_from": element["from"], "element_to": element["to"],
                "element_rotation": element.get("rotation"),
            })
    return faces


def extract_png(archive, resource_id):
    path = identifier_to_path(resource_id, "textures")
    binary = archive.read(path)
    with Image.open(io.BytesIO(binary)) as im:
        im.load()
        require(im.format == "PNG", "H17_TEXTURE_IS_NOT_PNG")
        pixels = im.convert("RGBA")
    return path, sha(binary), pixels


def texels_in_uv(uv, image_size):
    """Conservative UV rectangle texel coverage; rotation does not alter membership."""
    w, h = image_size
    lo_x, hi_x = sorted((uv[0], uv[2]))
    lo_y, hi_y = sorted((uv[1], uv[3]))
    min_x = max(0, math.floor(lo_x * w / 16))
    max_x = min(w, math.ceil(hi_x * w / 16))
    min_y = max(0, math.floor(lo_y * h / 16))
    max_y = min(h, math.ceil(hi_y * h / 16))
    return {(x, y) for y in range(min_y, max_y) for x in range(min_x, max_x)}


def inspect_jar(jar_file, prior):
    jar = Path(jar_file)
    require(hashlib.sha1(jar.read_bytes()).hexdigest() == AF_RELEASE_SHA1,
            "H17_OFFICIAL_AF_402_RELEASE_SHA1_MISMATCH")
    with ZipFile(jar) as z:
        require(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())),
                "H17_ORIGINAL_JAR_ZIP_INTEGRITY_OR_DUPLICATE")
        state = read_json(z, BLOCKSTATE_PATH)
        cases = {}
        for case, (state_key, expected) in STATE_MODELS.items():
            candidate = state["variants"][state_key]
            require(isinstance(candidate, dict) and candidate.get("model") == expected
                    and candidate.get("y", 0) % 360 == 0,
                    "H17_NORTH_BLOCKSTATE_SELECTOR_OR_ROTATION_DRIFT")
            model = resolve_leaf(z, expected)
            cases[case] = {"model": model, "faces": flatten_faces(model)}
        a = cases["S20"]
        b = cases["S21"]
        require(a["model"]["elements"] == b["model"]["elements"] and
                a["model"]["geometry_provider"] == b["model"]["geometry_provider"],
                "H17_DRAWER_GEOMETRY_CHANGED")
        require(len(a["faces"]) == len(b["faces"]) and len(a["faces"]) > 0,
                "H17_FACE_NUMBER_OR_GEOMETRY_MISMATCH")
        changed_faces = []
        for face_a, face_b in zip(a["faces"], b["faces"]):
            require(face_a["element"] == face_b["element"] and
                    face_a["direction"] == face_b["direction"] and
                    face_a["uv"] == face_b["uv"] and
                    face_a["face_uv_rotation"] == face_b["face_uv_rotation"] and
                    face_a["cullface"] == face_b["cullface"],
                    "H17_ORIGINAL_FACE_GEOMETRY_OR_UV_DIFF")
            if face_a["texture_id"] != face_b["texture_id"]:
                require("front" in face_a["texture_alias_chain"] and
                        "front" in face_b["texture_alias_chain"],
                        "H17_CHANGED_NONFRONT_FACE_TEXTURE")
                changed_faces.append({
                    "element": face_a["element"], "direction": face_a["direction"],
                    "uv": face_a["uv"], "uv_explicit": face_a["uv_explicit"],
                    "uv_rotation": face_a["face_uv_rotation"],
                    "closed_texture": face_a["texture_id"],
                    "open_texture": face_b["texture_id"],
                    "normal_is_north": face_a["direction"] == "north",
                })
        require(changed_faces, "H17_NO_FACE_USES_CHANGED_FRONT_TEXTURE")
        changed_bindings = sorted(k for k in set(a["model"]["textures"]) |
                                  set(b["model"]["textures"])
                                  if a["model"]["textures"].get(k) != b["model"]["textures"].get(k))
        require(changed_bindings == ["front"], "H17_TEXTURE_BINDING_DIFF_NOT_FRONT_ONLY")
        closed_id = a["model"]["textures"]["front"]
        opened_id = b["model"]["textures"]["front"]
        closed_path, closed_sha, closed = extract_png(z, closed_id)
        opened_path, opened_sha, opened = extract_png(z, opened_id)
        require(closed.size == opened.size and closed.size[0] > 0,
                "H17_FRONT_TEXTURE_IMAGE_SIZE_DRIFT")
        w, h = closed.size
        diff = {(x, y) for y in range(h) for x in range(w)
                if closed.getpixel((x, y)) != opened.getpixel((x, y))}
        alpha_diff = sum(closed.getpixel(p)[3] != opened.getpixel(p)[3] for p in diff)
        require(diff and closed_sha != opened_sha, "H17_FRONT_PNG_NO_RGBA_CHANGE")
        eligible = set()
        implicit_uv_faces = 0
        for face in changed_faces:
            if face["uv"] is None:
                implicit_uv_faces += 1
                face["diff_texel_coverage"] = None
            else:
                window = texels_in_uv(face["uv"], (w, h))
                in_face = diff & window
                face["diff_texel_coverage"] = len(in_face)
                eligible |= in_face
    require(prior["source_model"]["official_original_AF_mod_jar_sha1"] == AF_RELEASE_SHA1 and
            prior["verified_new_real_game"]["run_conclusion"] == "success" and
            prior["verified_new_real_game"]["github_actions_run"] == F2_ORIGINAL_RUN and
            prior["verified_new_real_game"]["exact_game_state_markers_2_of_2"] and
            prior["verified_new_real_game"]["new_north_open_closed_RGB24_changed_screen_pixels"] == 1208 and
            prior["study_scope"]["H03_case_fully_approved"] is False,
            "H17_PRIOR_ORIGINAL_F2_SOURCE_EVIDENCE_DRIFT")
    return {
        "schema": "MCFR_INT4_H17_AF_DRAWER_ORIGINAL_PARENT_FACE_UV_TEXEL_V1",
        "status": "PASS_PINNED_ORIGINAL_PARENT_TEXTURE_FACE_UV_STATIC_SOURCE_ONLY",
        "official_AF_402_release_sha1": AF_RELEASE_SHA1,
        "original_blockstate_path": BLOCKSTATE_PATH,
        "original_blockstate_sha256": sha(json.dumps(state, sort_keys=True).encode()),
        "source_cases": {
            case: {
                "state": STATE_MODELS[case][0], "leaf": STATE_MODELS[case][1],
                "source_chain": item["model"]["source_chain_root_to_leaf"],
                "geometry_provider": item["model"]["geometry_provider"],
                "external_vanilla_parent_not_opened": item["model"]["external_vanilla_parent_not_opened"],
                "element_count": len(item["model"]["elements"]),
                "face_count": len(item["faces"]),
            } for case, item in cases.items()
        },
        "changed_texture_slot": "front",
        "changed_face_count": len(changed_faces),
        "changed_faces": changed_faces,
        "only_front_texture_binding_changed": True,
        "geometry_and_face_uv_arrays_identical": True,
        "front_png_sources": {
            "S20": {"path": closed_path, "sha256": closed_sha},
            "S21": {"path": opened_path, "sha256": opened_sha},
        },
        "front_png_size": [w, h],
        "front_png_changed_rgba_texels": len(diff),
        "front_png_changed_alpha_texels": alpha_diff,
        "front_png_changed_rgb_only_texels": len(diff) - alpha_diff,
        "changed_png_texels_inside_explicit_front_face_uv_union": len(diff & eligible),
        "changed_png_texels_outside_explicit_front_face_uv_union": len(diff - eligible),
        "changed_front_faces_with_implicit_uv": implicit_uv_faces,
        "prior_exact_game_run": F2_ORIGINAL_RUN,
        "prior_real_native_F2_count": 2,
        "prior_front_camera_changed_pixels_threshold24": 1208,
        "new_game_runs": 0,
        "full_H03_gate_approved": False, "full_H05_gate_approved": False,
        "F70_unconditional_approved": 0, "INT5_semantics_approved": 0,
        "INT6_learning_or_redistribution_rights_approved": 0,
        "pixel_to_GPU_face_UV_texel_exact_causal_approved": False,
        "limitations": [
            "Texture sources and model/face selectors are inspected statically from one pinned Fabric 4.0.2 release.",
            "An external minecraft: parent is explicitly marked uninspected: inherited vanilla metadata is not certified; geometry must be explicitly provided inside the inspected AF JAR.",
            "An explicit UV rectangle provides candidate texel coverage, not GPU sampling proof; implicit UV is not fabricated.",
            "Previous north native F2 1208 pixels is reused by SHA/run reference, not rerun or independently reaudited here.",
            "Source image/JAR original bytes are neither committed nor uploaded in this derived report.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original-af-jar", type=Path, required=True)
    p.add_argument("--prior-result", type=Path, default=Path(SOURCE_RESULT_PATH))
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    prior = json.loads(args.prior_result.read_text(encoding="utf-8"))
    report = inspect_jar(args.original_af_jar, prior)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "status", "changed_face_count", "front_png_changed_rgba_texels",
        "front_png_changed_alpha_texels",
        "changed_png_texels_inside_explicit_front_face_uv_union",
        "changed_front_faces_with_implicit_uv", "new_game_runs",
    )}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
