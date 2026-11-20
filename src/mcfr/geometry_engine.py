"""Reusable 1-3-C geometry analysis for registered Vanilla and Mods model JSON.

The historical 1-3-C analyzer remains the canonical implementation of shape
calculations. This module adapts its functions to the H2/H3 pinned-source
catalog, without modifying historical evidence or duplicating geometry math.
Static geometry is not equivalent to an in-game rendering observation.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, closing
from functools import lru_cache
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from zipfile import BadZipFile

from . import research_db as catalog, research_engine as engine


LEGACY_PATH = Path("research/furniture_mods/phase_1-3/C/analyze_geometry.py")
DIRECTIONS = frozenset(("down", "up", "north", "south", "east", "west"))


@lru_cache(maxsize=1)
def legacy_core():
    """Load *the existing* 1-3-C code, not a reimplementation of its math."""
    path = catalog.ROOT / LEGACY_PATH
    spec = importlib.util.spec_from_file_location("_mcfr_legacy_1_3_c_geometry", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load historical 1-3-C analyzer: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # Needed for the historical @dataclass.
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def parse_model(body: bytes, path: str) -> dict:
    """Match H3 strict JSON rules, then validate 1-3-C geometry inputs."""
    def unique_fields(pairs):
        result = dict(pairs)
        if len(result) != len(pairs):
            raise ValueError("Duplicate JSON object keys")
        return result

    def reject_constant(value):
        raise ValueError(f"Invalid JSON constant: {value}")

    try:
        model = json.loads(body, object_pairs_hook=unique_fields, parse_constant=reject_constant)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"Invalid model JSON {path}: {exc}") from exc
    if not isinstance(model, dict):
        raise ValueError(f"Model JSON must be an object: {path}")
    if "parent" in model and (not isinstance(model["parent"], str) or not model["parent"]):
        raise ValueError(f"Invalid parent: {path}")
    textures = model.get("textures", {})
    if not isinstance(textures, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in textures.items()):
        raise ValueError(f"Invalid textures: {path}")
    elements = model.get("elements", [])
    if not isinstance(elements, list):
        raise ValueError(f"Invalid elements: {path}")

    def vector(value, size, field):
        if not isinstance(value, list) or len(value) != size or any(
            type(n) not in (int, float) or not math.isfinite(n) for n in value
        ):
            raise ValueError(f"Invalid {field}: {path}")

    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            raise ValueError(f"Invalid element {index}: {path}")
        for name in ("from", "to"):
            vector(element.get(name), 3, f"element {index}.{name}")
        rotation = element.get("rotation")
        if rotation is not None:
            if not isinstance(rotation, dict):
                raise ValueError(f"Invalid rotation: {path}")
            vector(rotation.get("origin"), 3, f"element {index}.rotation.origin")
            angle = rotation.get("angle")
            if (rotation.get("axis") not in ("x", "y", "z")
                or type(angle) not in (int, float) or not math.isfinite(angle)):
                raise ValueError(f"Invalid rotation axis/angle: {path}")
            if type(rotation.get("rescale", False)) is not bool:
                raise ValueError(f"Invalid rotation rescale: {path}")
            if angle and rotation.get("rescale") and abs(angle) not in (22.5, 45):
                raise ValueError(f"1-3-C only supports rescale at 22.5 or 45 degrees: {path}")
        faces = element.get("faces", {})
        if not isinstance(faces, dict) or any(face not in DIRECTIONS for face in faces):
            raise ValueError(f"Invalid faces: {path}")
        for direction, face in faces.items():
            if not isinstance(face, dict) or not isinstance(face.get("texture"), str):
                raise ValueError(f"Invalid face texture {index}.{direction}: {path}")
            if "uv" in face:
                vector(face["uv"], 4, f"element {index}.{direction}.uv")
            face_rotation = face.get("rotation", 0)
            if type(face_rotation) is not int or face_rotation not in (0, 90, 180, 270):
                raise ValueError(f"Invalid face UV rotation: {path}")
    return model


def model_layout(path: str) -> tuple[str, str]:
    parts = catalog.relative_path(path).split("/")
    try:
        index = parts.index("assets")
    except ValueError as exc:
        raise ValueError(f"Expected an assets/<namespace>/models/...json path: {path}") from exc
    if (len(parts) < index + 5 or parts[index + 2] != "models"
        or not path.endswith(".json")):
        raise ValueError(f"Expected an assets/<namespace>/models/...json path: {path}")
    return ("/".join(parts[:index]) + "/" if index else ""), parts[index + 1]


def model_reference(reference: str, prefix: str) -> tuple[str, str | None]:
    core = legacy_core()
    if not isinstance(reference, str) or not reference:
        raise ValueError("Invalid parent model reference")
    ident = core.normalize(reference)
    if ident in core.BUILTIN:
        return ident, None
    namespace, name = ident.split(":", 1)
    valid = "abcdefghijklmnopqrstuvwxyz0123456789_-."
    if (not namespace or not name or any(c not in valid for c in namespace)
        or any(not part or part in (".", "..") or any(c not in valid for c in part)
               for part in name.split("/"))):
        raise ValueError(f"Invalid model reference: {reference}")
    return ident, catalog.relative_path(f"{prefix}assets/{namespace}/models/{name}.json")


def registered_asset(db, release: str, path: str):
    row = db.execute(
        "SELECT * FROM asset WHERE release_key = ? AND source_path = ? AND kind = 'model'",
        (release, path),
    ).fetchone()
    return dict(row) if row else None


def registered_vanilla_parent(db, release: str, ident: str):
    rows = db.execute(
        "SELECT source_path FROM asset WHERE release_key = ? AND kind = 'model' AND resource_id = ?",
        (release, ident),
    ).fetchall()
    if len(rows) > 1:
        raise ValueError(f"Ambiguous registered Vanilla model: {ident}")
    return rows[0]["source_path"] if rows else None


def _geometry_signature(core, calculated) -> str:
    topology = []
    for element, _, _ in calculated:
        rotation = element.get("rotation", {})
        applied = ([rotation["origin"], rotation["axis"], rotation["angle"],
                    bool(rotation.get("rescale", False))]
                   if rotation.get("angle", 0) else [])
        topology.append([element["from"], element["to"], applied, sorted(element["faces"])])
    return core.hash_data(json.dumps(topology, separators=(",", ":")).encode())


def analyze(db, release_key: str, source: Path, root_asset: str,
            *, vanilla_release: str | None = None, vanilla_source: Path | None = None) -> dict:
    """Analyze pinned input with 1-3-C geometry; optionally resolve a pinned Vanilla lineage."""
    catalog.require_schema(db)
    root_asset = catalog.relative_path(root_asset)
    model_layout(root_asset)
    root_row = registered_asset(db, release_key, root_asset)
    release_row = db.execute("SELECT * FROM release WHERE release_key = ?", (release_key,)).fetchone()
    if root_row is None or release_row is None:
        raise ValueError("Root model is not registered as a model asset in this release")
    if (vanilla_release is None) != (vanilla_source is None):
        raise ValueError("Specify --vanilla-release and --vanilla-source together")
    release = dict(release_row)
    extra_release = None
    if vanilla_release is not None:
        row = db.execute("SELECT * FROM release WHERE release_key = ?", (vanilla_release,)).fetchone()
        if row is None or row["profile"] != "vanilla":
            raise ValueError("External Vanilla release must be registered with profile=vanilla")
        extra_release = dict(row)
        if extra_release["minecraft_version"] != release["minecraft_version"]:
            raise ValueError("External Vanilla Minecraft version differs from target release")

    core = legacy_core()
    models, chain, issues, seen = [], [], [], set()
    with ExitStack() as stack:
        primary_read, primary_pin = stack.enter_context(engine.source_reader(Path(source), release))
        readers = {"primary": (primary_read, primary_pin, release, Path(source))}
        if extra_release:
            extra_read, extra_pin = stack.enter_context(
                engine.source_reader(Path(vanilla_source), extra_release))
            readers["vanilla"] = (extra_read, extra_pin, extra_release, Path(vanilla_source))

        location = ("primary", root_asset)
        while location is not None:
            tag, path = location
            if location in seen:
                issues.append({"kind": "parent_cycle", "path": path, "release_key": readers[tag][2]["release_key"]})
                break
            seen.add(location)
            read, pin, src_release, src_path = readers[tag]
            try:
                body = read(path)
            except (FileNotFoundError, KeyError):
                # A 1-3-C feature: use independently pinned Vanilla models as parents
                # when a mod JAR/source does not bundle the minecraft namespace.
                if tag == "primary" and extra_release:
                    _, namespace = model_layout(path)
                    if namespace == "minecraft":
                        ident = "minecraft:" + path.split("/models/", 1)[1][:-5]
                        external = registered_vanilla_parent(db, vanilla_release, ident)
                        if external:
                            location = ("vanilla", external)
                            continue
                issues.append({"kind": "missing_or_external_parent", "path": path})
                break
            registered = registered_asset(db, src_release["release_key"], path)
            if registered:
                digest = engine.asset_digest(body, registered["hash_algorithm"])
                if digest != registered["digest"]:
                    raise ValueError(f"Catalog hash mismatch: {path}")
                if registered["byte_count"] is not None and len(body) != registered["byte_count"]:
                    raise ValueError(f"Catalog byte count mismatch: {path}")
            else:
                issues.append({"kind": "uncatalogued_parent", "path": path})
            parsed = parse_model(body, path)
            chain.append({
                "path": path, "sha256": hashlib.sha256(body).hexdigest(),
                "catalog_verified": registered is not None,
                "source_pin": pin, "release_key": src_release["release_key"],
            })
            models.append(parsed)
            parent = parsed.get("parent")
            if not parent:
                break
            prefix, _ = model_layout(path)
            ident, next_path = model_reference(parent, prefix)
            if next_path is None:
                chain[-1]["builtin_parent"] = ident
                break
            if tag == "vanilla":
                external = registered_vanilla_parent(db, vanilla_release, ident)
                if external is None:
                    issues.append({"kind": "missing_or_external_parent", "reference": ident})
                    break
                location = ("vanilla", external)
            else:
                location = ("primary", next_path)

    textures = {}
    for parsed in reversed(models):
        textures.update(parsed.get("textures", {}))
    provider = next(((row, model) for row, model in zip(chain, models)
                     if model.get("elements")), None)
    calculated = []
    if provider is not None:
        model = core.Model("COMMON", "COMMON", release["minecraft_version"],
                           "", provider[0]["path"], provider[0]["sha256"], "", provider[1])
        try:
            calculated = core.geometry(model)
        except (AssertionError, TypeError, KeyError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError(f"1-3-C geometry failed: {exc}") from exc
    else:
        issues.append({"kind": "no_static_elements", "detail": "No explicit elements in the model chain"})

    elements = []
    for index, (element, raw, rotated) in enumerate(calculated):
        distances = [(core.separation(rotated, item[2]), other)
                     for other, item in enumerate(calculated) if index != other]
        nearest = min(distances, key=lambda pair: (max(0, pair[0]), abs(pair[0]), pair[1])) if distances else None
        faces = {}
        for direction, face in sorted(element.get("faces", {}).items()):
            status, resource = core.face_slot(face["texture"], textures)
            if status != "RESOURCE_ID":
                issues.append({"kind": "unresolved_texture" if status == "SLOT_UNBOUND" else "texture_alias_cycle",
                               "at": f"{index}.{direction}", "reference": face["texture"]})
            data = {
                "texture": face["texture"], "resolved_texture": resource or None,
                "texture_status": status, "uv": face.get("uv"),
                "uv_explicit": "uv" in face, "rotation": face.get("rotation", 0),
            }
            for field in ("cullface", "tintindex"):
                if field in face:
                    data[field] = face[field]
            if "uv" not in face:
                issues.append({"kind": "implicit_uv", "at": f"{index}.{direction}"})
            faces[direction] = data
        elements.append({
            "from": element["from"], "to": element["to"], "rotation": element.get("rotation"),
            "geometry_type": core.classify_element(element),
            "raw_bbox": list(raw), "rotated_bbox": list(rotated),
            "outside_raw": core.outside(raw), "outside_rotated": core.outside(rotated),
            "nearest_element": nearest[1] if nearest else None,
            "rotated_aabb_signed_gap": nearest[0] if nearest else None,
            "faces": faces,
        })
    raw_bbox = core.union([item[1] for item in calculated])
    rotated_bbox = core.union([item[2] for item in calculated])
    return {
        "status": "PARTIAL" if any(item["kind"] != "implicit_uv" for item in issues) else "PASS",
        "evidence_class": "STATIC_MODEL_JSON_OBSERVATION",
        "geometry_engine": "historical_1-3-C",
        "geometry_source": str(LEGACY_PATH),
        "geometry_source_sha256": hashlib.sha256((catalog.ROOT / LEGACY_PATH).read_bytes()).hexdigest(),
        "release_key": release_key, "root_asset": root_asset,
        "source_pin": primary_pin, "source_pinning": release["pin_digest"],
        "model_chain": chain, "textures": textures,
        "element_count": len(elements), "face_count": sum(len(e["faces"]) for e in elements),
        "elements_from": provider[0]["path"] if provider else None,
        "raw_bbox": list(raw_bbox), "rotated_bbox": list(rotated_bbox),
        "geometry_signature": _geometry_signature(core, calculated) if calculated else None,
        "elements": elements, "issues": issues,
        "limitations": [
            "1-3-C is a static model analysis, not a game-rendering or runtime observation.",
            "Implicit UV projection, blockstate transforms and custom renderers are not resolved.",
            "External Vanilla parents need a separately registered, version-matched source.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--release", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--vanilla-release", help="Optional version-matched registered Vanilla release key")
    parser.add_argument("--vanilla-source", type=Path, help="Optional pinned Vanilla source directory or JAR")
    parser.add_argument("--out", type=Path, help="Optional local JSON report destination")
    args = parser.parse_args(argv)
    try:
        with closing(catalog.open_db(args.db, "ro")) as db:
            result = analyze(db, args.release, args.source, args.asset,
                             vanilla_release=args.vanilla_release, vanilla_source=args.vanilla_source)
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    except (OSError, ValueError, KeyError, BadZipFile) as exc:
        parser.error(str(exc))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
