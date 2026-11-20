"""Inspect Minecraft JSON model geometry, faces, UVs and inherited resources.

This is *static* evidence, not a rendering or in-game verification. Models are
read only from a pinned source and catalogued root assets are hash-checked.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
import math
from pathlib import Path
from zipfile import BadZipFile

from . import research_db as catalog, research_engine as engine


FACES = frozenset(("down", "up", "north", "south", "east", "west"))
BUILTIN = frozenset(("builtin/generated", "builtin/entity"))


def reference_path(reference: str, namespace: str) -> str | None:
    if not isinstance(reference, str) or not reference:
        raise ValueError("Invalid model parent reference")
    if ":" in reference:
        namespace, name = reference.split(":", 1)
    else:
        name = reference
    if name in BUILTIN and namespace == "minecraft":
        return None
    if not namespace or not name or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789_-. /" for ch in namespace + name):
        raise ValueError("Invalid model resource location")
    if "/" in namespace or " " in namespace or ".." in name.split("/"):
        raise ValueError("Invalid model resource location")
    return catalog.relative_path(f"assets/{namespace}/models/{name}.json")


def namespace_of(path: str) -> str:
    parts = catalog.relative_path(path).split("/")
    if len(parts) < 5 or parts[0] != "assets" or parts[2] != "models" or not path.endswith(".json"):
        raise ValueError("Expected an assets/<namespace>/models/...json path")
    return parts[1]


def point(value, where):
    if not isinstance(value, list) or len(value) != 3 or any(
        type(n) not in (int, float) or not math.isfinite(n) for n in value
    ):
        raise ValueError(f"Invalid three-dimensional coordinate at {where}")
    return value


def uv_rect(value, where):
    if not isinstance(value, list) or len(value) != 4 or any(
        type(n) not in (int, float) or not math.isfinite(n) for n in value
    ):
        raise ValueError(f"Invalid explicit UV at {where}")
    return value


def face_data(face: dict, textures: dict, issues: list, where: str) -> dict:
    if not isinstance(face, dict) or not isinstance(face.get("texture"), str):
        raise ValueError(f"Invalid face texture at {where}")
    token = face["texture"]
    visited = set()
    while token.startswith("#"):
        key = token[1:]
        if key in visited:
            issues.append({"kind": "texture_alias_cycle", "at": where, "reference": key})
            token = None
            break
        visited.add(key)
        token = textures.get(key)
        if not isinstance(token, str):
            issues.append({"kind": "unresolved_texture", "at": where, "reference": key})
            token = None
            break
    rotation = face.get("rotation", 0)
    if type(rotation) is not int or rotation not in (0, 90, 180, 270):
        raise ValueError(f"Invalid face UV rotation at {where}")
    data = {"texture": face["texture"], "resolved_texture": token,
            "uv": uv_rect(face["uv"], where) if "uv" in face else None,
            "uv_explicit": "uv" in face, "rotation": rotation}
    for key in ("cullface", "tintindex"):
        if key in face:
            data[key] = face[key]
    if data["uv"] is None:
        issues.append({"kind": "implicit_uv", "at": where,
                       "detail": "UV rectangle not declared; in-game projection is not calculated"})
    return data


def geometry(elements, textures, issues):
    if not isinstance(elements, list):
        raise ValueError("Model elements must be an array")
    output = []
    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            raise ValueError(f"Invalid element {index}")
        start = point(element.get("from"), f"element {index}.from")
        end = point(element.get("to"), f"element {index}.to")
        rotation = element.get("rotation")
        if rotation is not None:
            if not isinstance(rotation, dict):
                raise ValueError(f"Invalid element rotation {index}")
            point(rotation.get("origin"), f"element {index}.rotation.origin")
            if rotation.get("axis") not in ("x", "y", "z") or type(rotation.get("angle")) not in (int, float):
                raise ValueError(f"Invalid rotation axis/angle at element {index}")
        faces = element.get("faces", {})
        if not isinstance(faces, dict) or any(key not in FACES for key in faces):
            raise ValueError(f"Invalid faces for element {index}")
        output.append({
            "from": start, "to": end, "rotation": rotation,
            "shade": element.get("shade", True),
            "faces": {key: face_data(value, textures, issues, f"{index}.{key}")
                      for key, value in sorted(faces.items())},
        })
    return output


def analyze(db, release_key: str, source: Path, root_asset: str) -> dict:
    root_asset = catalog.relative_path(root_asset)
    namespace_of(root_asset)
    release_row = db.execute("SELECT * FROM release WHERE release_key = ?", (release_key,)).fetchone()
    asset_row = db.execute(
        "SELECT * FROM asset WHERE release_key = ? AND source_path = ? AND kind = 'model'",
        (release_key, root_asset),
    ).fetchone()
    if release_row is None or asset_row is None:
        raise ValueError("Root model is not registered as a model asset in this release")
    release = dict(release_row)
    registered = {row["source_path"]: dict(row) for row in db.execute(
        "SELECT * FROM asset WHERE release_key = ? AND kind = 'model'", (release_key,)
    )}
    issues, chain, parsed = [], [], []
    source = Path(source)
    with engine.source_reader(source, release) as (read, source_pin):
        current = root_asset
        seen = set()
        while current is not None:
            if current in seen:
                issues.append({"kind": "parent_cycle", "path": current})
                break
            seen.add(current)
            try:
                body = read(current)
            except (FileNotFoundError, KeyError):
                issues.append({"kind": "missing_or_external_parent", "path": current})
                break
            digest = hashlib.sha256(body).hexdigest()
            pinned = registered.get(current)
            if pinned is not None and engine.asset_digest(body, pinned["hash_algorithm"]) != pinned["digest"]:
                raise ValueError(f"Catalog hash mismatch: {current}")
            if pinned is None and source.is_dir():
                issues.append({"kind": "uncatalogued_parent", "path": current})
            try:
                data = json.loads(body)
            except (ValueError, UnicodeDecodeError) as exc:
                raise ValueError(f"Invalid model JSON {current}: {exc}") from exc
            if not isinstance(data, dict):
                raise ValueError(f"Model JSON must be an object: {current}")
            chain.append({"path": current, "sha256": digest,
                          "catalog_verified": pinned is not None,
                          "source_pin": source_pin})
            parsed.append(data)
            parent = data.get("parent")
            if parent is None:
                break
            next_path = reference_path(parent, namespace_of(current))
            if next_path is None:
                chain[-1]["builtin_parent"] = parent
                break
            current = next_path

    textures = {}
    for model in reversed(parsed):
        defined = model.get("textures", {})
        if not isinstance(defined, dict):
            raise ValueError("Model textures must be an object")
        textures.update(defined)
    owner = next(((item, data) for item, data in zip(chain, parsed) if "elements" in data), None)
    elements = geometry(owner[1]["elements"], textures, issues) if owner is not None else []
    if owner is None:
        issues.append({"kind": "no_static_elements",
                       "detail": "Generated, entity or custom-rendered geometry cannot be inferred"})
    return {
        "status": "PARTIAL" if any(issue["kind"] != "implicit_uv" for issue in issues) else "PASS",
        "evidence_class": "STATIC_MODEL_JSON_OBSERVATION",
        "release_key": release_key, "root_asset": root_asset,
        "source_pin": source_pin, "source_pinning": release["pin_digest"],
        "model_chain": chain, "textures": textures,
        "element_count": len(elements), "elements_from": owner[0]["path"] if owner else None,
        "elements": elements, "issues": issues,
        "limitations": [
            "Explicit element coordinates and UV declarations are reported without in-game transformations.",
            "Implicit UV projection, blockstate transforms, custom renderers and pixel colors are not resolved.",
            "A mod archive may reference external vanilla model parents not bundled inside that archive.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--release", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--out", type=Path, help="Optional JSON report destination outside the repo")
    args = parser.parse_args(argv)
    try:
        with closing(catalog.open_db(args.db, "ro")) as db:
            catalog.require_schema(db)
            result = analyze(db, args.release, args.source, args.asset)
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
