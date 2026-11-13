#!/usr/bin/env python3
"""TEX02-R015 -- SOURCE-derived, NOT in-game observed block model selection.

Requires Python >= 3.9 and the user's extracted Minecraft Java 1.21.11 tree.
Example:
  python VERIFY_R015_POSITION_SEED.py \
    --root 1.21.11 \
    --r013-slots research/vanilla_textures/by_stage/1-1-02/TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv \
    --out ./r015_regenerated

Do NOT infer that every subclass overrides no getSeed method. The predictions
apply to the DEFAULT eog.a(BlockState,BlockPos) -> bgj coordinate hash path.
Normal placed-world breaking and chunk-rebuild paths reset RNG before model
selection. The hpy non-world single-block path explicitly uses a fixed seed 42.
No original game was executed or rendered by this verifier.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EXPECTED_GIT_BLOBS = {
    "hpw.class":"8eb9a7e281fc91d8466823451f5e662f6d168d60",
    "htp.class":"fb4b050995f58c73b7e9970bd42f40b98a7a0f5f",
    "hpy.class":"079f96415a68d41461f35e88d713e2aa7a910bc1",
    "hpv.class":"0a342c41475f4b181ceabb65692ac2b8025d4cbe",
    "eog$a.class":"35c882743a59ae8d99fee1da9dfe0f21e8c6aa7c",
    "eog.class":"bee52d0356520a1872a94b0a15b0c98ea5407154",
    "bgj.class":"89604a1a7dfc4e63be8bc0eb170352b59c7f5374",
    "eur.class":"90617f9abceb3596e047accf8659a50e78df1a88",
    "euf.class":"ad7284b632a86ce7e2f58c686c461c8027ee8e59",
    "evf.class":"27cda5fa260b97c1c5a34ef39102c07c0b9b30e3",
    "bgr.class":"c5dda84653eb3ff0088cb6d9a0f26b2a7c79e44d",
    "hqh.class":"d9578e0174edc24b857ba9b2b21f1aed21e78bbf",
    "cbn.class":"06beacc3dbb751045895507672a2015e0aaec596",
    "cbn$c.class":"4beaebeeee6ad3b740c093c6c68e779800f99aba",
    "ioj.class":"d6f961ace90f5846affd9f05498a5b90781e83ae",
}
PREVIOUS_SLOTS_GIT_BLOB="18f02c6f44fd18f2a522fca81b2f73ba7409f829"
# Source method-code patterns; full class identity is independently checked.
SOURCE_CODE_FRAGMENTS = {
    "eog.class":["2c b8 02 07 ad"],  # default a(BlockState,BlockPos) -> bgj.a(Vec3i)
    "eog$a.class":["2a b6 00 ff 2a b6 00 73 2b b6 02 74 ad"],
    "bgj.class":["1a 12 eb 68 85 1c 85 14 00 ec 69 83 1b 85 83 42"],
    "bgr.class":["b8 00 10 b8 00 13 b0", "bb 00 1c 59 1e b7 00 1d b0"],
    "eur.class":["1f 14 00 13 83 14 00 10 7f", "20 14 00 13 69 14 00 16 61 14 00 10 7f"],
    "euf.class":["1b 85 2a 10 1f b9 00 13 02 00 85 69 10 1f 7b 88 ac"],
    "hpw.class":["2a b4 00 27 2b 2c b6 00 53 b9 00 56 03 00"],
    "htp.class":["19 0b 19 0f 19 0e b6 00 9f b9 00 a2 03 00"],
    "hpy.class":["2c 14 01 6a b8 01 70 b9 01 75 02 00"],
    "cbn.class":["2b 2a b4 00 4c b9 00 9d 02 00"],
}
MASK64=(1<<64)-1
MASK48=(1<<48)-1
LCG_MUL=25214903917
LCG_ADD=11

def git_blob_hash(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\x00"+b).hexdigest()

def java_signed(value,bits):
    value&=(1<<bits)-1
    return value-(1<<bits) if value&(1<<(bits-1)) else value

def position_seed(x,y,z):
    """Exact default source bgj.b(III) method, preserving int/long overflows."""
    # Minecraft Java executes x*3129871 with *32-bit int* overflow first,
    # then widens to long. z*116129781L is already 64-bit.
    mixed=java_signed(
        java_signed(x*3129871,32) ^ java_signed(z*116129781,64) ^ y,64)
    hashed=java_signed(mixed*mixed*42317861+mixed*11,64)
    return hashed >>16 # Arithmetic signed 64-bit right shift

def first_random_four(seed):
    """bgr.a()->eur and eur.b(seed), eur.c(31), euf.a(4) exact path."""
    init=(seed ^ LCG_MUL)&MASK48
    next_state=(init*LCG_MUL+LCG_ADD)&MASK48
    next31=next_state>>(48-31)
    selected=(4*next31)>>31
    assert selected in (0,1,2,3)
    return init,next_state,next31,selected

def verify_originals(source):
    if source is None:
        return 0
    for path,sha in EXPECTED_GIT_BLOBS.items():
        data=(source/path).read_bytes()
        assert data[:4]==bytes.fromhex("cafebabe"), path
        assert git_blob_hash(data)==sha, ("unexpected 1.21.11 class",path)
        for frag in SOURCE_CODE_FRAGMENTS.get(path,()):
            assert bytes.fromhex(frag) in data, ("bytecode anchor absent",path,frag)
    return len(EXPECTED_GIT_BLOBS)

def write_csv(path,rows):
    assert rows
    with path.open("w",encoding="utf8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def reconstruct(args):
    original_classes=verify_originals(args.root)
    assert git_blob_hash(args.r013_slots.read_bytes())==PREVIOUS_SLOTS_GIT_BLOB
    with args.r013_slots.open(encoding="utf8",newline="") as handle:
        slots=list(csv.DictReader(handle))
    assert len(slots)==31
    groups=[("stone",""),("deepslate","axis=x"),("deepslate","axis=y"),("deepslate","axis=z")]
    indexed={}
    for block,prop in groups:
        candidates=sorted(
            (r for r in slots if r["block"]==block and r["property"]==prop),
            key=lambda item:int(item["variant_index"]))
        assert len(candidates)==4
        assert [int(r["variant_index"]) for r in candidates]==[0,1,2,3]
        assert all(int(r["effective_weight"])==1 for r in candidates)
        indexed[(block,prop)]=candidates

    # Spot-checks independently computed from original bytecode formula.
    known=[
        ((0,64,0), 2644866, 3),
        ((1,64,0), 133335324866887, 3),
        ((0,64,1), -30368174053401, 3),
        ((-1,64,0),133335324865837,2),
        ((0,0,0),0,2),
        ((10,64,20),-74319395303090,2),
    ]
    for xyz,expect_seed,expect_idx in known:
        actual=position_seed(*xyz)
        assert actual==expect_seed,(xyz,actual,expect_seed)
        assert first_random_four(actual)[3]==expect_idx

    positions,choices,collisions=[],[],[]
    seen=defaultdict(list)
    for x in range(-3,4):
        for z in range(-3,4):
            y=64
            seed=position_seed(x,y,z)
            init,post,rand31,index=first_random_four(seed)
            positions.append(dict(
                x=x,y=y,z=z,default_blockstate_seed_signed_long=seed,
                LCG_seed_after_java48_mask=init,LCG_first_step_state=post,
                LCG_next31_bits=rand31,weighted_nextInt_4_slot=index,
                stone_index=index,deepslate_axis_x_index=index,
                deepslate_axis_y_index=index,deepslate_axis_z_index=index,
                source_default_not_subclass_override=True,game_observed=False))
            seen[seed].append((x,y,z,index))
            for block,prop in groups:
                model=indexed[(block,prop)][index]
                choices.append(dict(
                    x=x,y=y,z=z,group=block+("_"+prop.replace("=","_") if prop else ""),
                    selected_variant_index=index,
                    selected_model=model["source_model"],
                    selected_x=model["x"],selected_y=model["y"],selected_z=model["z"],
                    uvlock=model["uvlock"],effective_weight=1,
                    seed=seed,source_default_only=True,actual_game_observed=False))
    for s,points in seen.items():
        if len(points)>1:
            assert len(points)==2
            a,b=points
            assert a[3]==b[3]
            collisions.append(dict(
                default_hash_seed=s,first_x=a[0],first_y=a[1],first_z=a[2],
                second_x=b[0],second_y=b[1],second_z=b[2],
                same_first_model_index=a[3],virtual_position_only=True))
    assert len(positions)==49 and len(choices)==196
    assert len(seen)==39 and len(collisions)==10
    frequency=[sum(p["weighted_nextInt_4_slot"]==i for p in positions)
               for i in range(4)]
    assert frequency==[6,12,19,12]
    preview_idx=first_random_four(42)[3]
    assert preview_idx==2
    preview=[]
    for block,prop in groups:
        item=indexed[(block,prop)][preview_idx]
        preview.append(dict(
            block=block,property=prop,fixed_nonworld_seed=42,
            selected_variant_index=preview_idx,
            selected_model=item["source_model"],
            selected_x=item["x"],selected_y=item["y"],selected_z=item["z"],
            context="hpy single block method if this hqh model is passed",
            actual_ingame_item_model_observed=False))
    args.out.mkdir(parents=True,exist_ok=True)
    write_csv(args.out/"R015_REGENERATED_49_POSITION_SEEDS.csv",positions)
    write_csv(args.out/"R015_REGENERATED_196_MODEL_CHOICES.csv",choices)
    write_csv(args.out/"R015_REGENERATED_10_SEED_COLLISIONS.csv",collisions)
    write_csv(args.out/"R015_REGENERATED_4_FIXED42_PREVIEW.csv",preview)
    print(json.dumps(dict(
        original_class_sha_verified=original_classes,
        prior_slots_sha_verified=True,
        virtual_positions=49,distinct_seeds=39,collision_pairs=10,
        source_default_model_choice_rows=196,
        first_indices_distribution=frequency,
        nonworld_fixed_seed_42_first_choice_index=preview_idx,
        minecraft_runtime_random_draws_measured=0,ingame_static_render_verified=0
    ),indent=2,ensure_ascii=False))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,help="Full USER-EXTRACTED 1.21.11 folder")
    p.add_argument("--r013-slots",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    if a.root is None:
        p.error("--root is required to verify original source bytecode SHA")
    reconstruct(a)
