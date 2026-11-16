"""Attest the bare-face slot resolution using the supplied 1.21.11 client classes."""
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/vanilla_models/phase_1-2-C/entry5"
MODEL = ROOT / "1.21.11/assets/minecraft/models/block/heavy_core.json"
PNG = ROOT / "1.21.11/assets/minecraft/textures/block/heavy_core.png"


def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def main():
    source = json.loads(MODEL.read_text())
    assert source["textures"]["all"] == "block/heavy_core"
    faces = [(ei, direction, face) for ei, element in enumerate(source["elements"])
             for direction, face in element["faces"].items()]
    assert len(faces) == 6 and all(face["texture"] == "all" for ei, d, face in faces)
    with (OUT.parent / "entry4/UNRESOLVED_NON_TEMPLATE.csv").open(newline="") as f:
        prior = list(csv.DictReader(f))
    assert len(prior) == 6 and all(r["model"] == "heavy_core" and r["source_sha"] == blob(MODEL) for r in prior)
    command = ["java", "--module", "jdk.jdeps/com.sun.tools.javap.Main", "-classpath", str(ROOT / "1.21.11"), "-c", "-p"]
    slot_code = subprocess.check_output(command + ["hqp"], text=True)
    dispatch_code = subprocess.check_output(command + ["iog"], text=True)
    slot_excerpt = slot_code.split("  public ins a(java.lang.String);", 1)[1].split("  public static hqp$a", 1)[0]
    dispatch_excerpt = dispatch_code.split("  public default ilp a(hqp, java.lang.String, iny);", 1)[1]
    assert "java/lang/String.substring" in slot_excerpt and "java/util/Map.get" in slot_excerpt
    assert "bipush        35" in slot_excerpt and "hqp.a:(Ljava/lang/String;)Lins;" in dispatch_excerpt
    assert "ifnull" in dispatch_excerpt and "a:(Ljava/lang/String;Liny;)Lilp;" in dispatch_excerpt
    class_shas = {name: blob(ROOT / f"1.21.11/{name}.class") for name in ("hqp", "iog")}
    (OUT / "HEAVY_CORE_CLIENT_BYTECODE_EVIDENCE.txt").write_text(
        "Source: user-provided Minecraft Java 1.21.11 extracted client classes. Static javap -c -p output.\n"
        + "hqp.class Git blob: " + class_shas["hqp"] + "\n"
        + "iog.class Git blob: " + class_shas["iog"] + "\n\n"
        + "hqp.a(String) strips an optional leading '#' and looks up the resulting key in the slot map:\n"
        + "  public ins a(java.lang.String);" + slot_excerpt + "\n"
        + "iog.a(hqp,String,iny) calls slot lookup first and falls back to direct path only on null:\n"
        + "  public default ilp a(hqp, java.lang.String, iny);" + dispatch_excerpt)
    with Image.open(PNG) as im:
        rgba = im.convert("RGBA")
        alpha = Counter(v[3] for v in rgba.get_flattened_data())
        pixel = {"png_path": rel(PNG), "png_sha": blob(PNG), "width": im.width, "height": im.height,
                 "mode": im.mode, "rgba_sha256": hashlib.sha256(rgba.tobytes()).hexdigest(),
                 "opaque_pixels": alpha[255], "transparent_pixels": alpha[0],
                 "partial_alpha_pixels": sum(n for a, n in alpha.items() if 0 < a < 255)}
    (OUT / "HEAVY_CORE_PNG_RGBA_EVIDENCE.json").write_text(json.dumps(pixel, indent=2) + "\n")
    records = [dict(model="heavy_core", element_index=ei, direction=direction,
                    original_face_texture=face["texture"], original_uv=json.dumps(face["uv"]),
                    model_path=rel(MODEL), model_sha=blob(MODEL),
                    slot_key="all", slot_value=source["textures"]["all"],
                    resolved_texture="minecraft:block/heavy_core", png_path=rel(PNG), png_sha=blob(PNG),
                    client_slot_lookup_class_sha=class_shas["hqp"], client_dispatch_class_sha=class_shas["iog"],
                    correction="Entry4 missing_png interpretation superseded; original Entry4 rows preserved")
               for ei, direction, face in faces]
    with (OUT / "HEAVY_CORE_FACE_ERRATUM.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, records[0]); writer.writeheader(); writer.writerows(records)
    print(json.dumps({"corrected_face_refs": len(records), "png_path": rel(PNG), "png_pixels": pixel["width"] * pixel["height"],
                      "class_sha": class_shas, "model_sha": blob(MODEL)}, indent=2))


if __name__ == "__main__":
    main()
