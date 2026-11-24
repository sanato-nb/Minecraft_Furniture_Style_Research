"""INT-4 H26: invoke official Mojang 1.21.11 FaceBakery.defaultFaceUV.

Evidence is bounded to the source-local face-UV rectangle returned by the
unaltered compiled Mojang JVM method and official vanilla PNGs. This does not
invoke the full quad bake, texture atlas, UV lock or a real Minecraft renderer.
Original assets are read on Actions, never committed.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import tempfile
from zipfile import ZipFile

from . import int4_h20_v11_bed_mesh_uv as h20
from . import int4_h25_adorn_release_source as h25

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "project/integration/INT4_H26_ADORN_MOJANG_DEFAULT_UV_RESULT_V1.json"
H25_JSON = ROOT / "project/integration/INT4_H25_ADORN_761_SELECTED_MODEL_SOURCE_V1.json"
FACE_CSV = ROOT / "project/integration/INT4_H26_ADORN_139_ORIGINAL_SOURCE_FACE_UV_V1.csv"
FACE_CSV_FIELDS = ("face_id", "model", "geometry_provider", "element_index", "direction",
                   "texture", "source_uv_provenance", "uv_u0", "uv_v0", "uv_u1", "uv_v1",
                   "uv_rotation_degrees", "original_cullface", "original_tintindex",
                   "full_quad_baked", "native_F2_verified")
H25_CSV = ROOT / "project/integration/INT4_H25_ADORN_761_STATE_SELECTOR_CASES_V1.csv"
H25_JSON_BLOB = "5aefb171ab57d48aebba213ccedc8dbad268fbba"
H25_CSV_BLOB = "762c6f0b6b650b9ac4e137486f886e037149124a"
MOJANG_MANIFEST_SHA1 = "a969d96978af7b52dba8df44e177f48ec4ebe0d8"
MOJANG_CLIENT_SHA1 = "ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
MOJANG_CLIENT_SHA256 = "1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
MOJANG_MAPPINGS_SHA256 = "517799a8485e107e932dc1bd27c002b2d0b9207eb2396b685bcfe6c3321a9fbd"
VANILLA_PNGS = {
    "minecraft:block/acacia_log": "cdf7c1971c2bb95e4ddfdb6b53bd0be69a341415e43030629bb4c72b339b83c1",
    "minecraft:block/acacia_planks": "3f84918024e190f2767e03631d8c35b31fa5cd9235d7b114738224297dca6797",
    "minecraft:block/iron_block": "dafa9944ba49fe71958553eded50e87d7bea9c7410cfe568745989bede101c49",
    "minecraft:block/orange_stained_glass": "136ad613ee1da3520bc980cc8376abd3cf1dddb886cf89eaf37820ca051711ab",
    "minecraft:block/stone": "b5e10adc72442bfb257ce7ba0b9bbe36475a0c8cdfec89b80dc9517203ff3e9f",
}
DIRECTIONS = ("down", "up", "north", "south", "west", "east")
MOJANG_NAMES = (
    "net.minecraft.client.renderer.block.model.FaceBakery",
    "net.minecraft.core.Direction",
    "net.minecraft.client.renderer.block.model.BlockElementFace$UVs",
)
PROBE = ROOT / "tools/research/H26MojangDefaultUvProbe.java"


def need(ok: bool, explanation: str) -> None:
    if not ok:
        raise ValueError("H26 official Mojang UV source: " + explanation)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_h25() -> dict:
    need(h25.git_blob(H25_JSON.read_bytes()) == H25_JSON_BLOB, "pinned H25 source result drift")
    need(h25.git_blob(H25_CSV.read_bytes()) == H25_CSV_BLOB, "pinned H25 21-state CSV drift")
    report = json.loads(H25_JSON.read_text(encoding="utf-8"))
    need(report["scope"]["verified_exact_selected_states"] == 21 and
         report["scope"]["verified_source_model_profiles"] == 5,
         "H25 model count changed")
    need(report["legacy_gates_unchanged"] == {
        "modeling_F70_scope_from_H23": "70/70",
        "strict_F70_unconditional": 0,
        "H03": "HOLD", "H05": "CONDITIONAL",
        "INT5": 0, "INT6": 0, "GPU_per_face_approved": False,
    }, "parent F70/INT5/INT6 status drift")
    return report


def mapped_section(raw: str, classname: str) -> tuple[str, list[str]]:
    pattern = r"(?m)^" + re.escape(classname) + r" -> ([\w$]+):$"
    hits = list(re.finditer(pattern, raw))
    need(len(hits) == 1, "mapped original class missing/duplicate " + classname)
    r = hits[0]
    lines = []
    for line in raw[r.end():].splitlines()[1:]:
        if line and not line.startswith((" ", "#")):
            break
        if line.startswith("    "):
            lines.append(line.strip())
    return r.group(1), lines


def mapped_member(lines: list[str], original: str, suffix: str = "") -> str:
    expression = r"(?:^|\s)" + re.escape(original) + re.escape(suffix) + r"\s+->\s+(\w+)$"
    hits = [m.group(1) for line in lines if (m := re.search(expression, line))]
    need(len(hits) == 1, "Mojang mapped member not unique: " + original + suffix)
    return hits[0]


def original_uv_mapping(raw: str) -> dict:
    bakery, methods = mapped_section(raw, MOJANG_NAMES[0])
    direction, enum_fields = mapped_section(raw, MOJANG_NAMES[1])
    uvs, uv_members = mapped_section(raw, MOJANG_NAMES[2])
    # Method descriptor is required, not merely an obfuscated class name.
    methods = [line for line in methods if " defaultFaceUV(" in line]
    need(len(methods) == 1 and
         "BlockElementFace$UVs defaultFaceUV(org.joml.Vector3fc,org.joml.Vector3fc,net.minecraft.core.Direction)" in methods[0],
         "original Mojang FaceBakery.defaultFaceUV signature changed")
    method = mapped_member(methods, "defaultFaceUV", "(org.joml.Vector3fc,org.joml.Vector3fc,net.minecraft.core.Direction)")
    members = [mapped_member(uv_members, n + "()", "") for n in ("minU", "minV", "maxU", "maxV")]
    need(members == ["a", "b", "c", "d"],
         "H26 reflection probe must match UV accessor mappings")
    dmap = {d: mapped_member(enum_fields, d.upper()) for d in DIRECTIONS}
    need(len(set(dmap.values())) == 6, "Direction enum mapped constants duplicate")
    return {
        "face_bakery_class": bakery,
        "direction_class": direction,
        "uv_record_class": uvs,
        "default_uv_method": method,
        "direction_enum_names": dmap,
        "record_accessor_names": members,
    }



def historical_default_uv_formula(element: dict, direction: str, face: dict
                                  ) -> tuple[tuple[Fraction, ...], str]:
    """Independently cross-check the same documented H21 direction formulas.

    Deliberately no import of the full H21 pipeline, which loads optional image
    libraries. The actual original JVM FaceBakery call remains authoritative.
    """
    if "uv" in face:
        return tuple(Fraction(str(v)) for v in face["uv"]), "EXPLICIT"
    x, y, z = (Fraction(str(v)) for v in element["from"])
    X, Y, Z = (Fraction(str(v)) for v in element["to"])
    rect = {
        "down": (x, 16-Z, X, 16-z),
        "up": (x, z, X, Z),
        "north": (16-X, 16-Y, 16-x, 16-y),
        "south": (x, 16-Y, X, 16-y),
        "west": (z, 16-Y, Z, 16-y),
        "east": (16-Z, 16-Y, 16-z, 16-y),
    }
    need(direction in rect, "unsupported face for default UV formula")
    return rect[direction], "DEFAULT"


def original_model_faces(jar: ZipFile, parent: dict) -> list[dict]:
    rows = []
    for mi, model in enumerate(h25.MODELS):
        meta = parent["resolved_models"][model]
        chain = meta["source_parent_chain_leaf_first"]
        models = [json.loads(jar.read(p)) for p in chain]
        texture_slots = {}
        for m in reversed(models):
            texture_slots.update(m.get("textures", {}))
        providers = [(p, obj) for p, obj in zip(chain, models) if "elements" in obj]
        need(bool(providers), "no element source " + model)
        provider, desc = providers[0]
        source_elements = desc["elements"]
        need(len(source_elements) == meta["source_elements"], "H25 source geometry drift")
        for i, element in enumerate(source_elements):
            frm, to = element["from"], element["to"]
            need(len(frm) == len(to) == 3 and
                 all(isinstance(x, (int, float)) for x in frm + to), "invalid coordinate source")
            for d in sorted(element["faces"]):
                face = element["faces"][d]
                need(d in DIRECTIONS, "unexpected direction")
                tex = h25.resolve_texture(face["texture"], texture_slots)
                explicit = face.get("uv")
                if explicit is not None:
                    need(len(explicit) == 4, "malformed explicit UV")
                uv_prior, method = historical_default_uv_formula(element, d, face)
                need((explicit is None) == (method == "DEFAULT"), "prior default UV class mismatch")
                row = {
                    "id": "M" + str(mi) + "E" + str(i) + "F" + d,
                    "model": model,
                    "geometry_provider": provider,
                    "element": i,
                    "direction": d,
                    "from": frm,
                    "to": to,
                    "texture": tex,
                    "uv_source": "MOJANG_ORIGINAL_FACEBAKERY_DEFAULT_METHOD" if explicit is None else "ORIGINAL_ADORN_EXPLICIT_UV",
                    "original_face_uv_rotation_degrees": int(face.get("rotation", 0)),
                    "element_rotation_declaration": element.get("rotation"),
                    "cullface": face.get("cullface"),
                    "tintindex": face.get("tintindex"),
                    "independent_h21_source_uv_formula": [float(x) for x in uv_prior],
                    "declared_explicit_uv": explicit,
                }
                rows.append(row)
    need(len(rows) == 139 and len({r["id"] for r in rows}) == 139,
         "five H25 source profiles not 139 unique faces")
    counts = Counter(r["uv_source"] for r in rows)
    need(counts == {"MOJANG_ORIGINAL_FACEBAKERY_DEFAULT_METHOD": 107,
                   "ORIGINAL_ADORN_EXPLICIT_UV": 32},
         "five-model 107 default/32 explicit source face partition changed")
    for model in h25.MODELS:
        p = parent["resolved_models"][model]
        same = [r for r in rows if r["model"] == model]
        need(len(same) == p["source_faces"] and
             sum(r["uv_source"] == "MOJANG_ORIGINAL_FACEBAKERY_DEFAULT_METHOD" for r in same)
             == p["implicit_uv_faces_require_bake"], "model original face count drift")
        need(Counter(r["texture"] for r in same) == p["resolved_face_textures"],
             "original face texture resolver drift")
    return rows


def invoke_original_mojang_uv(
    rows: list[dict], client: Path, mappings: dict, libraries: list[str]
) -> tuple[dict[str, list[float]], dict]:
    implicit = [r for r in rows if r["declared_explicit_uv"] is None]
    need(len(implicit) == 107, "unexpected number of original default UV invocations")
    data = "\n".join("\t".join(
        [r["id"], r["direction"]] + [str(v) for v in (r["from"] + r["to"])]
    ) for r in implicit) + "\n"
    with tempfile.TemporaryDirectory(prefix="h26_original_uv_") as tmp:
        root = Path(tmp)
        subprocess.run(["javac", "-d", str(root), str(PROBE)], check=True,
                       capture_output=True, text=True, timeout=60)
        args = [
            "java", "-cp", str(root) + ":" + str(client) + ":" + ":".join(libraries),
            "mcfr.research.H26MojangDefaultUvProbe",
            mappings["face_bakery_class"], mappings["direction_class"],
            mappings["default_uv_method"], mappings["uv_record_class"],
        ] + [mappings["direction_enum_names"][d] for d in DIRECTIONS]
        run = subprocess.run(args, input=data, capture_output=True, text=True,
                             timeout=120)
        need(run.returncode == 0, "original JVM defaultFaceUV invocation failed: " +
             run.stderr[-3500:])
        need("H26_MOJANG_ORIGINAL_DEFAULT_FACE_UV_INVOKED=107" in run.stderr,
             "JVM original default UV method was not invoked for 107 faces")
        out = {}
        for line in run.stdout.splitlines():
            cells = line.split("\t")
            need(len(cells) == 6 and cells[0] == "UV",
                 "unexpected vanilla JVM output")
            id = cells[1]
            need(id not in out, "duplicate UV call result")
            vals = [float(x) for x in cells[2:]]
            need(len(vals) == 4 and all(math.isfinite(x) for x in vals),
                 "bad original JVM UV")
            out[id] = vals
        need(set(out) == {r["id"] for r in implicit}, "missing default UV face")
        return out, {
            "calls": len(out), "java_probe_git_blob_sha1": h25.git_blob(PROBE.read_bytes()),
            "original_method": "FaceBakery.defaultFaceUV",
            "not_full_quad_bake": True, "not_real_game_F2": True,
        }


def audit(args: argparse.Namespace) -> dict:
    manifest = args.version_json.read_bytes()
    need(sha1(manifest) == MOJANG_MANIFEST_SHA1, "Mojang version manifest SHA-1 changed")
    meta = json.loads(manifest)
    need(meta["id"] == "1.21.11", "wrong Mojang game version")
    client = args.official_client.read_bytes()
    need(sha1(client) == meta["downloads"]["client"]["sha1"] == MOJANG_CLIENT_SHA1 and
         sha256(client) == MOJANG_CLIENT_SHA256, "Mojang official client sha mismatch")
    mapping_raw = args.client_mappings.read_bytes()
    need(sha1(mapping_raw) == meta["downloads"]["client_mappings"]["sha1"] and
         sha256(mapping_raw) == MOJANG_MAPPINGS_SHA256,
         "official Mojang class mappings changed")
    mapped = original_uv_mapping(mapping_raw.decode("utf-8"))
    parent = load_h25()
    need(sha256(args.adorn_jar.read_bytes()) == h25.RELEASE_SHA256,
         "Adorn official release SHA changed")
    # Independently recompute all H25 original tag/JAR model selectors.
    need(h25.audit(args.adorn_jar) == parent,
         "H25 official selected source cache does not match independent upstream")
    with ZipFile(args.official_client) as moj, ZipFile(args.adorn_jar) as adorn:
        need(moj.testzip() is None and adorn.testzip() is None,
             "Mojang/Adorn original jar archive CRC invalid")
        vanilla = {}
        for resource, expected in sorted(VANILLA_PNGS.items()):
            member = "assets/minecraft/textures/" + resource.split(":", 1)[1] + ".png"
            raw = moj.read(member)
            need(sha256(raw) == expected, "Mojang original vanilla PNG SHA differs: " + resource)
            need(raw[:8] == b"\x89PNG\r\n\x1a\n", "not PNG")
            wh = list(struct.unpack(">II", raw[16:24]))
            need(all(x > 0 for x in wh), "bad PNG image dimensions")
            vanilla[resource] = {
                "jar_member": member,
                "sha256": expected, "size": wh,
                "source": "OFFICIAL_MOJANG_1_21_11_CLIENT_JAR",
            }
        faces = original_model_faces(adorn, parent)
    with tempfile.TemporaryDirectory(prefix="h26_mojang_lib_") as tmp:
        libpaths, libsha = h20.download_libraries(meta, Path(tmp))
        got, probe = invoke_original_mojang_uv(faces, args.official_client, mapped, libpaths)
    need(len(libsha) == len(libpaths) and bool(libsha),
         "official Mojang library SHA count wrong")
    for face in faces:
        fid = face["id"]
        uv = got[fid] if fid in got else [float(x) for x in face["declared_explicit_uv"]]
        independent = face.pop("independent_h21_source_uv_formula")
        need(all(math.isclose(a, b, abs_tol=0.00001, rel_tol=0)
                 for a, b in zip(uv, independent)),
             "actual Mojang default UV mismatches independent H21 rule: " + fid)
        face["source_uv_texel_units"] = uv
        face["source_uv_normalized_to_16"] = [x / 16 for x in uv]
        if face["declared_explicit_uv"] is not None:
            need(fid not in got, "explicit UV incorrectly replaced by default")
        else:
            need(fid in got, "implicit UV not covered by original JVM")
    group = {m: [r for r in faces if r["model"] == m] for m in h25.MODELS}
    selectors = parent["selected_state_cases"]
    sums = Counter()
    per_state = []
    for case in selectors:
        selected = [r["model"] for r in case["selected"]]
        take = [r for model in selected for r in group[model]]
        defaults = sum(r["declared_explicit_uv"] is None for r in take)
        explicit = len(take) - defaults
        external = sum(r["texture"] in vanilla for r in take)
        need(len(take) == case["sum_source_faces"], "H25 selected state faces differ")
        need(external == sum(parent["resolved_models"][m]["external_minecraft_face_count"]
                             for m in selected),
             "H25 selected vanilla PNG face source count differs")
        per_state.append({
            "block": case["block"], "state": case["state"],
            "selected_models": selected, "mojang_default_uv_source_faces": defaults,
            "adorn_explicit_uv_source_faces": explicit,
            "resolved_vanilla_png_source_faces": external,
            "original_game_F2": False,
        })
        sums.update({"face_records": len(take), "default_uv": defaults, "explicit_uv": explicit,
                     "vanilla_external": external, "model_applications": len(selected)})
    need(sums["face_records"] == 656 and sums["default_uv"] == 400 and
         sums["explicit_uv"] == 256 and sums["vanilla_external"] == 120 and
         sums["model_applications"] == 29 and len(per_state) == 21,
         "21-state weighted source face totals drift")
    need(set(vanilla) == {r["texture"] for r in faces if r["texture"].startswith("minecraft:")},
         "vanilla source PNG references not fully covered")
    return {
        "schema": "MCFR_INT4_H26_ADORN_761_MOJANG_FACEBAKERY_ORIGINAL_UV_V1",
        "official_source": {
            "mojang_minecraft_version": "1.21.11",
            "mojang_version_json_sha1": MOJANG_MANIFEST_SHA1,
            "mojang_client_jar_sha1": MOJANG_CLIENT_SHA1,
            "mojang_client_jar_sha256": MOJANG_CLIENT_SHA256,
            "mojang_mappings_sha256": MOJANG_MAPPINGS_SHA256,
            "adorn_761_jar_sha256": h25.RELEASE_SHA256,
            "H25_original_json_git_blob": H25_JSON_BLOB,
            "H25_original_csv_git_blob": H25_CSV_BLOB,
        },
        "original_mojang_mapping": mapped,
        "original_vanilla_pngs": vanilla,
        "original_jvm_default_uv_probe": probe,
        "original_library_sha1": libsha,
        "five_model_unique_source_faces": faces,
        "twenty_one_state_source_uv_count": per_state,
        "counts": {
            "vanilla_original_pngs": len(vanilla),
            "source_models": len(group),
            "source_unique_faces": len(faces),
            "source_unique_mojang_default_uv_faces": len(got),
            "source_unique_adorn_explicit_uv_faces": len(faces) - len(got),
            "selected_state_cases": len(per_state),
            "state_weighted_face_records": sums["face_records"],
            "state_weighted_original_mojang_default_uv": sums["default_uv"],
            "state_weighted_adorn_explicit_uv": sums["explicit_uv"],
            "state_weighted_vanilla_png_face_references": sums["vanilla_external"],
            "state_weighted_model_applications": sums["model_applications"],
            "new_actual_game_runs": 0,
            "new_native_F2": 0,
        },
        "preserved_approvals": parent["legacy_gates_unchanged"],
        "limits": [
            "The original Mojang FaceBakery.defaultFaceUV method ran in an isolated JVM for 107 unique source faces.",
            "This is not the full baked quad, UV lock, element/facing rotation, sprite atlas interpolation or native game F2.",
            "The five PNG SHA values prove original vanilla texture bytes, not observed in-game GPU texel selection.",
            "21-case totals repeat the same source faces across state selections; not 656 unique geometry faces.",
            "Existing H23 separate modeling contract 70/70 unchanged; strict final F70, INT5 meaning, INT6 rights not approved.",
            "Original client/adorn JAR, vanilla/adorn PNG, and Mojang mapping files are not redistributed.",
        ],
    }



def source_face_csv_rows(result: dict) -> list[dict[str, str]]:
    def number(value) -> str:
        val = float(value)
        return str(int(val)) if val.is_integer() else str(val)
    rows = []
    for face in result["five_model_unique_source_faces"]:
        uv = face["source_uv_texel_units"]
        need(len(uv) == 4, "source UV CSV has invalid face rectangle")
        row = {
            "face_id": face["id"],
            "model": face["model"],
            "geometry_provider": face["geometry_provider"],
            "element_index": str(face["element"]),
            "direction": face["direction"],
            "texture": face["texture"],
            "source_uv_provenance": face["uv_source"],
            "uv_u0": number(uv[0]),
            "uv_v0": number(uv[1]),
            "uv_u1": number(uv[2]),
            "uv_v1": number(uv[3]),
            "uv_rotation_degrees": str(face["original_face_uv_rotation_degrees"]),
            "original_cullface": str(face["cullface"]) if face["cullface"] is not None else "",
            "original_tintindex": str(face["tintindex"]) if face["tintindex"] is not None else "",
            "full_quad_baked": "false",
            "native_F2_verified": "false",
        }
        need(tuple(row) == FACE_CSV_FIELDS, "source UV CSV schema differs")
        rows.append(row)
    need(len(rows) == 139 and len({r["face_id"] for r in rows}) == 139,
         "source UV CSV must have 139 distinct original faces")
    return rows


def verify_face_csv(result: dict, filename: Path = FACE_CSV) -> None:
    with filename.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        need(tuple(reader.fieldnames or ()) == FACE_CSV_FIELDS,
             "H26 source face CSV column schema changed")
        got = list(reader)
    need(got == source_face_csv_rows(result),
         "H26 139-row face CSV does not match real Mojang JVM original UV")
    print("H26_PERSISTED_139_FACE_CSV_ORIGINAL_JVM_MATCH")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--version-json", type=Path, required=True)
    p.add_argument("--official-client", type=Path, required=True)
    p.add_argument("--client-mappings", type=Path, required=True)
    p.add_argument("--adorn-jar", type=Path, required=True)
    p.add_argument("--output", type=Path, default=OUT)
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    result = audit(a)
    if a.verify:
        need(json.loads(a.output.read_text(encoding="utf-8")) == result,
             "persisted H26 original UV result not identical to independent re-run")
        verify_face_csv(result)
        print("H26_5_VANILLA_PNGS_107_ORIGINAL_JVM_DEFAULT_FACE_UV_400_STATE_WEIGHTED_PASS")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        print("H26_RESULT_JSON_START")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        print("H26_RESULT_JSON_END")


if __name__ == "__main__":
    main()
