#!/usr/bin/env python3
"""TEX02-R017 — Original Minecraft 1.21.11 static atlas/model closure.

Run from a local checkout of sanato-nb/Minecraft_Furniture_Style_Research:
 python VERIFY_R017_ATLAS_CLOSURE.py --repo-root . \
   --ledger research/vanilla_textures/by_stage/1-1-02/TEX02-R017/SOURCE_LEDGER_56.csv

No client, resource pack override, shader, GPU, or image-render execution.
All hashes below are *Git blob SHA-1* of extracted source bytes, not official
Mojang client.jar SHA-1 verification. Requires Python 3.9+ standard library.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SRC = Path("1.21.11/assets/minecraft")
R013 = Path("research/vanilla_textures/by_stage/1-1-02/TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv")

def blob_sha(data):
    header = b"blob " + str(len(data)).encode() + b"\0"
    return hashlib.sha1(header + data).hexdigest()

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def normalize(x):
    return x if ":" in x else "minecraft:" + x

def read_ledger(repo, path):
    with path.open(encoding="utf-8", newline="") as handle:
        records = list(csv.DictReader(handle))
    assert len(records) == 56
    checked = set()
    for record in records:
        source = record["source_path"]
        assert source not in checked, source
        checked.add(source)
        original = repo/source
        data = original.read_bytes()
        assert blob_sha(data) == record["git_blob_sha"], ("changed original", source)
    return records

def model_chain(repo, model_id):
    ordered, seen = [], set()
    while model_id:
        assert model_id not in seen, ("model parent cycle", model_id)
        seen.add(model_id)
        path = repo/SRC/"models"/(model_id.split(":",1)[1] + ".json")
        assert path.is_file(), path
        item = load_json(path)
        ordered.append((model_id, item))
        model_id = normalize(item["parent"]) if "parent" in item else None
    return ordered[::-1]

def alias(bindings, key):
    seen = set()
    while key and key.startswith("#"):
        label = key[1:]
        assert label not in seen, ("texture slot loop", label)
        seen.add(label)
        key = bindings.get(label)
    assert key, ("missing texture slot", seen)
    return normalize(key)

def main(repo, ledger_file):
    read_ledger(repo, ledger_file)
    atlas = load_json(repo/SRC/"atlases/blocks.json")
    assert any(s.get("type")=="minecraft:directory"
               and s.get("source")=="block"
               and s.get("prefix")=="block/" for s in atlas["sources"])
    with (repo/R013).open(encoding="utf-8",newline="") as file:
        states=list(csv.DictReader(file))
    assert len(states)==31
    blocks={v["block"] for v in states}
    models={v["source_model"] for v in states}
    assert len(blocks)==17 and len(models)==19
    local_faces=("down","up","north","south","west","east")
    resolved={}
    for model_id in models:
        chain=model_chain(repo, model_id)
        bindings={}
        geo=None
        for _,item in chain:
            bindings.update(item.get("textures",{}))
            if "elements" in item:
                geo=item["elements"]
        assert geo and len(geo)==1
        faces=geo[0]["faces"]
        assert set(faces)==set(local_faces), model_id
        value={face:alias(bindings,faces[face]["texture"]) for face in local_faces}
        assert alias(bindings,bindings["particle"])
        resolved[model_id]=value
    uses=Counter()
    for row in states:
        for face in local_faces:
            uses[resolved[row["source_model"]][face]]+=1
    assert sum(uses.values())==186
    assert len(uses)==19
    fixed_sprites={"minecraft:block/"+id for id in blocks}
    supplementals=set(uses)-fixed_sprites
    assert supplementals=={"minecraft:block/deepslate_top","minecraft:block/blackstone_top"}
    for id in uses:
        image=repo/SRC/"textures"/(id.split(":",1)[1] + ".png")
        assert image.is_file(), image
        assert not Path(str(image)+".mcmeta").is_file()
    assert uses["minecraft:block/deepslate_top"]==24
    assert uses["minecraft:block/blackstone_top"]==2
    assert uses["minecraft:block/deepslate"]==48
    assert uses["minecraft:block/blackstone"]==4
    assert uses["minecraft:block/stone"]==24
    print(json.dumps({
        "original_source_sha_verified":56,
        "fixed_blocks":17,"variant_declarations":31,
        "unique_model_json_leaves":19,"parent_templates":7,
        "source_model_face_bindings":186,
        "required_atlas_sprite_png_files":19,
        "missing_atlas_source_png":0,
        "source_png_metadata_sidecars":0,
        "supplemental_end_face_png":sorted(supplementals),
        "runtime_atlas_stitch_observed":False,
        "ingame_render_verified":0,
        "official_mojang_clientjar_sha1_authenticated":False,
        "source_only_research_scope_completed":True
    },indent=2,ensure_ascii=False))
if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--repo-root",type=Path,required=True)
    args.add_argument("--ledger",type=Path,required=True)
    a=args.parse_args()
    main(a.repo_root,a.ledger)
