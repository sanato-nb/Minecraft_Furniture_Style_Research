#!/usr/bin/env python3
"""TV-001 fixed 12-case/25-frame input preparation; no network or AI API."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

FACES = ("down", "up", "north", "south", "west", "east")
CAMERAS = ("north", "south", "east", "west", "up", "down")
EXPECTED_IMAGES = {"P01": 6, "P02": 2, "P03": 2, "P04": 4, "P05": 4, "P06": 2,
                   "R01": 1, "R02": 2, "R03": 2}
SOURCE_COMMIT = "176f7f34de2336eb7984c4734e97b6eb156c19f4"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def box(frm, to, texture="#all", *, rotation=None, uv_rotation=0):
    faces = {d: {"texture": texture, "uv": [0, 0, 16, 16]} for d in FACES}
    if uv_rotation:
        faces["north"]["rotation"] = uv_rotation
    obj = {"from": frm, "to": to, "faces": faces}
    if rotation:
        obj["rotation"] = rotation
    return obj


def fixtures(base):
    models = base / "assets/test/models/block"
    states = base / "assets/test/blockstates"
    tex = base / "assets/test/textures/block"
    tex.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), (140 + x * 3, 88 + y * 3, 48, 255))
    im.save(tex / "wood.png")
    alpha = im.copy()
    for y in range(16):
        for x in range(16):
            if (x + y) % 4 == 0:
                alpha.putpixel((x, y), (0, 0, 0, 0))
    alpha.save(tex / "alpha.png")
    dump(models / "p01.json", {"textures": {"all": "test:block/wood"},
                                "elements": [box([2, 2, 2], [14, 14, 14])]})
    dump(models / "p02.json", {"textures": {"all": "test:block/wood"},
                                "elements": [box([2, 2, 3], [14, 4, 13]),
                                             box([4, 4, 4], [12, 14, 6], rotation={
                                                 "origin": [8, 8, 8], "axis": "y", "angle": 22.5})]})
    dump(models / "p03_base.json", {"textures": {"all": "test:block/wood"},
                                     "elements": [box([3, 0, 3], [13, 15, 13])]})
    dump(models / "p03_middle.json", {"parent": "test:block/p03_base"})
    dump(models / "p03.json", {"parent": "test:block/p03_middle"})
    dump(models / "p04.json", {"textures": {"all": "test:block/wood"},
                                "elements": [box([3, 0, 3], [13, 5, 13]), box([3, 5, 3], [13, 14, 5])]})
    dump(states / "p04.json", {"variants": {
        "facing=north": {"model": "test:block/p04"},
        "facing=east": {"model": "test:block/p04", "y": 90},
        "facing=south": {"model": "test:block/p04", "y": 180},
        "facing=west": {"model": "test:block/p04", "y": 270}}})
    dump(models / "p05_post.json", {"textures": {"all": "test:block/wood"},
                                     "elements": [box([6, 0, 6], [10, 16, 10])]})
    dump(models / "p05_side.json", {"textures": {"all": "test:block/wood"},
                                     "elements": [box([7, 6, 0], [9, 9, 8])]})
    dump(states / "p05.json", {"multipart": [
        {"apply": {"model": "test:block/p05_post"}},
        {"when": {"north": "true"}, "apply": {"model": "test:block/p05_side"}},
        {"when": {"east": "true"}, "apply": {"model": "test:block/p05_side", "y": 90}}]})
    dump(models / "p06.json", {"textures": {"all": "test:block/alpha"},
                                "elements": [box([0, 0, 0], [16, 16, 16], uv_rotation=90)]})
    dump(models / "n01.json", {"textures": {"all": "test:block/absent"},
                                "elements": [box([0, 0, 0], [16, 16, 16])]})
    dump(models / "n02a.json", {"parent": "test:block/n02b"})
    dump(models / "n02b.json", {"parent": "test:block/n02a"})
    dump(models / "u01.json", {"custom_mesh": {"format": "unsupported"}})


class Resolver:
    def __init__(self, root, fixture_root):
        self.roots = {"minecraft": root / "1.21.11/assets/minecraft",
                      "test": fixture_root / "assets/test"}
        self.seen_files = {}

    def read(self, resource, folder, suffix=".json"):
        namespace, colon, name = resource.partition(":")
        if not colon:
            namespace, name = "minecraft", namespace
        if namespace not in self.roots:
            raise ValueError("UNKNOWN_NAMESPACE: " + namespace)
        if ".." in Path(name).parts or name.startswith("/"):
            raise ValueError("UNSAFE_RESOURCE: " + resource)
        path = self.roots[namespace] / folder / (name + suffix)
        if not path.is_file():
            raise ValueError("MISSING_RESOURCE: " + str(path))
        raw = path.read_bytes()
        self.seen_files[str(path)] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw)

    def model(self, resource, active=()):
        if resource in active:
            raise ValueError("PARENT_CYCLE: " + " -> ".join((*active, resource)))
        data = self.read(resource, "models")
        if "custom_mesh" in data:
            raise ValueError("UNSUPPORTED_FORMAT: custom_mesh")
        base = self.model(data["parent"], (*active, resource)) if "parent" in data else {}
        merged = dict(base)
        merged.update({k: v for k, v in data.items() if k != "textures"})
        merged["textures"] = {**base.get("textures", {}), **data.get("textures", {})}
        if "elements" not in data and "elements" in base:
            merged["elements"] = base["elements"]
        return merged

    def texture(self, model, alias):
        table = model["textures"]
        visited = set()
        while alias.startswith("#"):
            key = alias[1:]
            if key in visited:
                raise ValueError("TEXTURE_CYCLE: " + key)
            visited.add(key)
            if key not in table:
                raise ValueError("MISSING_TEXTURE_ALIAS: " + key)
            alias = table[key]
        namespace, colon, name = alias.partition(":")
        if not colon:
            namespace, name = "minecraft", namespace
        if namespace not in self.roots or ".." in Path(name).parts:
            raise ValueError("INVALID_TEXTURE: " + alias)
        path = self.roots[namespace] / "textures" / (name + ".png")
        if not path.is_file():
            raise ValueError("MISSING_TEXTURE: " + str(path))
        self.seen_files[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        return str(path.resolve())

    def instantiate(self, name, *, x=0, y=0, uvlock=False):
        model = self.model(name)
        if "elements" not in model:
            raise ValueError("NO_ELEMENTS: " + name)
        result = []
        for element in model["elements"]:
            el = {"from": element["from"], "to": element["to"],
                  "rotation": element.get("rotation"), "faces": {}}
            for face, data in element.get("faces", {}).items():
                if face not in FACES:
                    raise ValueError("INVALID_FACE: " + face)
                el["faces"][face] = {"png": self.texture(model, data["texture"]),
                                     "uv": data.get("uv"), "rotation": data.get("rotation", 0)}
            result.append(el)
        return {"model": name, "elements": result, "x": x, "y": y, "uvlock": uvlock}

    def apply_state(self, resource, properties):
        data = self.read(resource, "blockstates")
        key = ",".join(f"{k}={v}" for k, v in sorted(properties.items()))
        if "variants" in data:
            for candidate, model_data in data["variants"].items():
                criteria = dict(kv.split("=", 1) for kv in candidate.split(",") if kv)
                if criteria == properties:
                    return self.apply(model_data)
            raise ValueError("STATE_NOT_FOUND: " + key)
        if "multipart" in data:
            out = []
            for part in data["multipart"]:
                if self.condition(part.get("when"), properties):
                    out.extend(self.apply(part["apply"]))
            return out
        raise ValueError("UNSUPPORTED_STATE: " + resource)

    @staticmethod
    def condition(when, props):
        if when is None:
            return True
        if "OR" in when:
            return any(Resolver.condition(c, props) for c in when["OR"])
        if "AND" in when:
            return all(Resolver.condition(c, props) for c in when["AND"])
        return all(str(props.get(k, "")).lower() in v.lower().split("|") for k, v in when.items())

    def apply(self, definition):
        if isinstance(definition, list):
            # Weighted variants require a separate deterministic selection contract.
            raise ValueError("UNSUPPORTED_WEIGHTED_VARIANT")
        return [self.instantiate(definition["model"], x=definition.get("x", 0),
                                 y=definition.get("y", 0), uvlock=definition.get("uvlock", False))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out.resolve()
    fixtures(out / "fixtures")
    r = Resolver(args.repo.resolve(), out / "fixtures")
    jobs, cases = [], []

    def add(case, label, camera, instances):
        if not instances or not any(i["elements"] for i in instances):
            raise ValueError("Empty case: " + case)
        jobs.append({"id": case + "-" + label, "case": case, "camera": camera, "instances": instances})

    for camera in CAMERAS:
        add("P01", camera, camera, [r.instantiate("test:block/p01")])
    for cam in ("north", "up"):
        add("P02", cam, cam, [r.instantiate("test:block/p02")])
    for cam in ("north", "south"):
        add("P03", cam, cam, [r.instantiate("test:block/p03")])
    for f in ("north", "east", "south", "west"):
        add("P04", f, "north", r.apply_state("test:p04", {"facing": f}))
    for north, east in ((False, False), (True, False), (False, True), (True, True)):
        label = f"n{int(north)}e{int(east)}"
        add("P05", label, "north", r.apply_state("test:p05", {
            "north": str(north).lower(), "east": str(east).lower()}))
    for cam in ("north", "south"):
        add("P06", cam, cam, [r.instantiate("test:block/p06")])
    add("R01", "base", "iso", [r.instantiate("minecraft:block/acacia_planks")])
    for label, north in (("none", "false"), ("north", "true")):
        add("R02", label, "iso", r.apply_state("minecraft:acacia_fence", {
            "north": north, "east": "false", "south": "false", "west": "false"}))
    for label, properties in [
        ("straight", {"facing": "east", "half": "bottom", "shape": "straight"}),
        ("inner", {"facing": "east", "half": "top", "shape": "inner_left"})]:
        add("R03", label, "iso", r.apply_state("minecraft:acacia_stairs", properties))
    for case, resource, expectation in [
        ("N01", "test:block/n01", "MISSING_TEXTURE"),
        ("N02", "test:block/n02a", "PARENT_CYCLE"),
        ("U01", "test:block/u01", "UNSUPPORTED_FORMAT")]:
        try:
            r.instantiate(resource)
            cases.append({"id": case, "result": "FAIL", "expected": expectation})
        except ValueError as exc:
            status = "PASS" if str(exc).startswith(expectation) else "FAIL"
            cases.append({"id": case, "result": status, "expected": expectation, "actual": str(exc)})
    for case, n in EXPECTED_IMAGES.items():
        count = sum(job["case"] == case for job in jobs)
        cases.append({"id": case, "result": "PASS" if count == n else "FAIL",
                      "expected_frames": n, "actual_frames": count})
    if len(cases) != 12 or len(jobs) != 25 or any(c["result"] != "PASS" for c in cases):
        raise RuntimeError(f"Scope check failed: cases={len(cases)}, images={len(jobs)}; {cases}")
    dump(out / "manifest.json", {"contract": "TV-001-v1.1", "source_commit": SOURCE_COMMIT,
                                  "cases": cases, "jobs": jobs, "source_sha256": r.seen_files})
    print(json.dumps({"status": "PASS", "cases": len(cases), "images": len(jobs),
                      "negative_tests": 3, "input_files": len(r.seen_files)}))


if __name__ == "__main__":
    main()
