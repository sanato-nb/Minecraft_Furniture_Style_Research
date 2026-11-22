"""Project tagged texels onto three exposed occupied Handcrafted bed faces."""
from io import BytesIO
import json
from zipfile import ZipFile

from . import int4_nonchair_runtime as prior

VIEWS = {
    "sleeping_south": "0.5 118.88 44.5 180 0",
    "sleeping_east": "3.9375 118.97375 40.3125 90 0",
}
# Element indices are zero-based within the occupied S37 parent.
FACES = {
    "footboard_south": (5, "south", "sleeping_south", [4.125, 7.875, 6.125, 8.125], 0,
                        (35, 46, 63, 64)),
    "headboard_up": (6, "up", "sleeping_overhead", [9.25, 2.75, 7.25, 2.375], 180,
                     (60, 71, 19, 21)),
    "sheet_east": (11, "east", "sleeping_east", [10.625, 2, 12.625, 2.375], 0,
                   (87, 90, 16, 18)),
}
COLORS = ((255, 20, 20), (20, 255, 20), (20, 20, 255), (255, 235, 20))


def texels(face):
    x0, x1, y0, y1 = FACES[face][-1]
    return dict(zip(("nw_red", "ne_green", "sw_blue", "se_yellow"),
                    ((x0, y0), (x1, y0), (x0, y1), (x1, y1))))


def prepare(mods, source_zip, variant, textures, *, apply):
    """Verify each original asset and optionally extend the observer-only overlay."""
    from PIL import Image

    jar_path = mods / "handcrafted-fabric-1.21.1-4.0.3.jar"
    results = {}
    with ZipFile(jar_path) as jar, ZipFile(source_zip) as git:
        provider = jar.read(variant["provider"])
        prior.require(prior.sha256(provider) == variant["provider_sha256"], "Occupied model changed")
        model = json.loads(provider)
        for name, (index, normal, view, uv, rotation, _) in FACES.items():
            element = model["elements"][index]
            mapping = element["faces"][normal]
            prior.require(element["rotation"]["angle"] == 0 and mapping["uv"] == uv and
                          mapping.get("rotation", 0) == rotation, f"Original face changed: {name}")
            slot = model["textures"][mapping["texture"][1:]]
            namespace, path = variant["textures"][slot[1:]].split(":", 1)
            asset = f"assets/{namespace}/textures/{path}.png"
            raw = jar.read(asset)
            prior.require(prior.bed.source_zip_file(git, "common/src/main/resources/" + asset) == raw,
                          f"Original texture differs from JAR: {asset}")
            if asset not in textures:
                with Image.open(BytesIO(raw)) as original:
                    textures[asset] = original.convert("RGBA")
            image = textures[asset]
            prior.require(image.size == (128, 128), f"Unexpected texture size: {asset}")
            tags = texels(name)
            if apply:
                for (x, y), rgb in zip(tags.values(), COLORS):
                    for column in (x, x + 1):
                        image.putpixel((column, y), (*rgb, 255))
            results[name] = {
                "element": index, "normal": normal, "view": view, "uv": uv, "rotation": rotation,
                "bounds": [element["from"], element["to"]], "texture": asset,
                "texture_sha256": prior.sha256(raw), "slot_chain": [mapping["texture"], slot],
                "tags": {tag: {"texel": list(xy), "painted_width": 2, "painted_height": 1, "rgb": list(rgb)}
                         for (tag, xy), rgb in zip(tags.items(), COLORS)},
            }
    return results


def project(face, sample_xy, focal, overhead):
    normal = face["normal"]
    u0, v0, u1, v1 = face["uv"]
    if face["rotation"] == 180:
        u0, v0, u1, v1 = u1, v1, u0, v0
    x, y = sample_xy
    s, t = ((x + 1) / 8 - u0) / (u1 - u0), ((y + .5) / 8 - v0) / (v1 - v0)
    (x0, y0, z0), (x1, y1, z1) = ([value / 16 for value in bound] for bound in face["bounds"])
    pose = overhead if normal == "up" else VIEWS[face["view"]]
    cx, cy, cz, _, _ = map(float, pose.split())
    if normal == "up":
        dx, dy, depth = x0 + (x1 - x0) * s - cx, 40 + z0 + (z1 - z0) * t - cz, cy + 1.62 - 120 - y1
    else:
        dy = cy + 1.62 - (120 + y1 - (y1 - y0) * t)
        if normal == "south":
            dx, depth = x0 + (x1 - x0) * s - cx, cz - 40 - z1
        else:
            dx, depth = cz - (40 + z1 - (z1 - z0) * s), cx - x1
    return round(512 + focal * dx / depth), round(342 + focal * dy / depth)


def audit(folder, manifest, overhead, tag_matches):
    from PIL import Image

    floor = manifest["uv_projection"]["floor_width_pixels"]
    camera_y = float(overhead.split()[1])
    focal = floor / 10 * (camera_y + 1.62 - 120)
    samples = {}
    for name, face in manifest["uv_source"]["additional_faces"].items():
        with Image.open(folder / f"{face['view']}.png") as original:
            image = original.convert("RGB")
        row = {}
        for tag, spec in face["tags"].items():
            xy = project(face, spec["texel"], focal, overhead)
            rgb = image.getpixel(xy)
            matched = tag_matches(rgb, tag)
            prior.require(matched == manifest["uv_probe"],
                          f"UV {name}/{tag} did not match expected probe at {xy}: {rgb}")
            row[tag] = {"xy": list(xy), "rgb": list(rgb), "matched": matched}
        samples[name] = row
    prior.require(samples.keys() == FACES.keys(), "Missing face evidence")
    return samples
