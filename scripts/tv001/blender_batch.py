#!/usr/bin/env python3
"""TV-001 Blender batch renderer. Single process handles many jobs, checkpoints by content."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import bpy
from mathutils import Vector

DIRECTIONS = {
    "north": (0, 2.5, .25), "south": (0, -2.5, .25),
    "east": (2.5, 0, .25), "west": (-2.5, 0, .25),
    "up": (0, 0, 2.5), "down": (0, 0, -2.5),
    "iso": (2.2, -2.7, 2.0),
}
FACE_ORDER = ("down", "up", "north", "south", "west", "east")
IMAGE_CACHE = {}
MATERIAL_CACHE = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def stable_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def rotate(point, axis, deg, origin):
    if not deg:
        return point
    v = [point[i] - origin[i] for i in range(3)]
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y, z = v
    if axis == "x":
        v = (x, y * c - z * s, y * s + z * c)
    elif axis == "y":
        v = (x * c + z * s, y, -x * s + z * c)
    elif axis == "z":
        v = (x * c - y * s, x * s + y * c, z)
    else:
        raise ValueError("Unsupported element rotation axis: " + axis)
    return [v[i] + origin[i] for i in range(3)]


def coordinates(element, face):
    (x0, y0, z0), (x1, y1, z1) = element["from"], element["to"]
    return {
        "down": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        "up": [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)],
        "north": [(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)],
        "south": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
        "west": [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)],
        "east": [(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)],
    }[face]


def mc_to_blender(v):
    return ((v[0] - 8) / 16, -(v[2] - 8) / 16, (v[1] - 8) / 16)


def material(path):
    if path in MATERIAL_CACHE:
        return MATERIAL_CACHE[path]
    if path not in IMAGE_CACHE:
        img = bpy.data.images.load(path, check_existing=True)
        img.alpha_mode = "STRAIGHT"
        img.use_fake_user = True
        img.colorspace_settings.name = "sRGB"
        IMAGE_CACHE[path] = img
    mat = bpy.data.materials.new(name="TV001/" + Path(path).name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = IMAGE_CACHE[path]
    tex.interpolation = "Closest"
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    mat.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    if hasattr(mat, "blend_method"):
        try:
            mat.blend_method = "CLIP"
            mat.alpha_threshold = 0.5
        except (TypeError, AttributeError):
            pass
    MATERIAL_CACHE[path] = mat
    return mat


def uv_points(face):
    uv = face.get("uv") or [0, 0, 16, 16]
    u0, v0, u1, v1 = [value / 16 for value in uv]
    corners = [(u0, 1 - v1), (u1, 1 - v1), (u1, 1 - v0), (u0, 1 - v0)]
    shift = int(face.get("rotation", 0) / 90) % 4
    return corners[-shift:] + corners[:-shift] if shift else corners


def locked_uv_points(face, direction, instance):
    """Pinned 1.21.11 fixed-scope correction, not a general UV-lock implementation."""
    if not instance["uvlock"] or not (instance["x"] or instance["y"]):
        return uv_points(face)
    if (instance["x"], instance["y"]) != (180, 0):
        raise ValueError("UNSUPPORTED_UVLOCK_TRANSFORM")
    if face.get("uv") is None or face.get("rotation", 0) != 0:
        raise ValueError("UNSUPPORTED_UVLOCK_FACE")
    u0, v0, u1, v1 = face["uv"]
    canonical = [(u0,v0),(u0,v1),(u1,v1),(u1,v0)]
    if direction in ("north","south","west","east"):
        canonical = [(16-u,16-v) for u,v in canonical]
    # hoa source corner order to mesh polygon order.
    order = (0,1,2,3) if direction == "up" else (1,2,3,0)
    return [(canonical[i][0]/16,1-canonical[i][1]/16) for i in order]


def make_element(element, instance, number):
    verts, polygons, uvs, texture_paths = [], [], [], []
    for direction in FACE_ORDER:
        face = element["faces"].get(direction)
        if face is None:
            continue
        quad = coordinates(element, direction)
        rot = element.get("rotation")
        if rot:
            quad = [rotate(p, rot["axis"], rot["angle"], rot.get("origin", [8, 8, 8])) for p in quad]
        if instance["x"]:
            quad = [rotate(p, "x", instance["x"], [8, 8, 8]) for p in quad]
        if instance["y"]:
            quad = [rotate(p, "y", instance["y"], [8, 8, 8]) for p in quad]
        base = len(verts)
        verts.extend(mc_to_blender(p) for p in quad)
        polygons.append((base, base + 1, base + 2, base + 3))
        uvs.append(locked_uv_points(face, direction, instance))
        texture_paths.append(face["png"])
    if not polygons:
        return
    mesh = bpy.data.meshes.new("TV001_mesh")
    mesh.from_pydata(verts, [], polygons)
    mesh.update()
    ob = bpy.data.objects.new("TV001_element_%s" % number, mesh)
    bpy.context.collection.objects.link(ob)
    uv_layer = mesh.uv_layers.new(name="UVMap")
    indices = {}
    for i, poly in enumerate(mesh.polygons):
        path = texture_paths[i]
        if path not in indices:
            indices[path] = len(mesh.materials)
            mesh.materials.append(material(path))
        poly.material_index = indices[path]
        for j, loop_idx in enumerate(poly.loop_indices):
            uv_layer.data[loop_idx].uv = uvs[i][j]
    return ob


def reset_scene():
    for obj in list(bpy.data.objects):
        if obj.type == "MESH":
            bpy.data.objects.remove(obj, do_unlink=True)


def setup():
    scene = bpy.context.scene
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    else:
        raise RuntimeError("Compatible EEVEE engine not available")
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = True
    scene.camera = None
    world = bpy.data.worlds.new("TV001_world")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Strength"].default_value = 0.75
    camera_data = bpy.data.cameras.new("TV001_camera")
    camera = bpy.data.objects.new("TV001_camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 1.8
    lamp_data = bpy.data.lights.new("TV001_light", "AREA")
    lamp = bpy.data.objects.new("TV001_light", lamp_data)
    scene.collection.objects.link(lamp)
    lamp.location = (1.7, -2.0, 3.2)
    lamp_data.energy = 350
    lamp_data.shape = "DISK"
    lamp_data.size = 4.0
    return camera


def camera_at(camera, name):
    camera.location = DIRECTIONS[name]
    forward = Vector((0, 0, 0)) - camera.location
    camera.rotation_euler = forward.to_track_quat("-Z", "Y").to_euler()


def load_checkpoint(path):
    if not path.exists():
        return {"jobs": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def checkpoint(path, data):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=0)
    opts = ap.parse_args(argv)
    root = opts.out.resolve()
    root.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(opts.manifest.read_text(encoding="utf-8"))
    jobs = manifest["jobs"]
    if len(jobs) != 25:
        raise RuntimeError("TV-001 requires exactly 25 fixed render jobs")
    state_path = root / "render_checkpoint.json"
    state = load_checkpoint(state_path)
    camera = setup()
    rendered = skipped = 0
    renderer_sha = digest(Path(__file__).read_bytes())
    for job in jobs:
        name = job["id"]
        inp_sha = digest(stable_json({"job": job, "renderer_sha256": renderer_sha}))
        destination = root / (name + ".png")
        old = state["jobs"].get(name, {})
        if (old.get("input_sha256") == inp_sha and destination.is_file()
                and digest(destination.read_bytes()) == old.get("png_sha256")):
            skipped += 1
            continue
        if opts.limit and rendered >= opts.limit:
            break
        reset_scene()
        for inst in job["instances"]:
            for idx, el in enumerate(inst["elements"]):
                make_element(el, inst, idx)
        camera_at(camera, job["camera"])
        bpy.context.scene.render.filepath = str(destination)
        bpy.ops.render.render(write_still=True)
        data = destination.read_bytes()
        state["jobs"][name] = {"input_sha256": inp_sha, "png_sha256": digest(data),
                               "bytes": len(data), "camera": job["camera"]}
        checkpoint(state_path, state)
        rendered += 1
    remaining = len(jobs) - len(state["jobs"])
    print("TV001_BATCH " + json.dumps({"rendered": rendered, "skipped": skipped,
                                        "remaining": remaining, "jobs": len(jobs),
                                        "texture_cache": len(IMAGE_CACHE)}))


if __name__ == "__main__":
    arguments = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(arguments)
