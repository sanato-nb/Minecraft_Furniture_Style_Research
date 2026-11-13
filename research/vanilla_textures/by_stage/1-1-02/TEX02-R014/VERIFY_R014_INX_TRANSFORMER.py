#!/usr/bin/env python3
"""TEX02-R014: recheck source-only inx vertex-interner context + R012 corners.

Requires Python 3.9+, NO external dependencies. For local use with the
user-extracted Minecraft Java 1.21.11 folder and frozen study CSVs.

    python VERIFY_R014_INX_TRANSFORMER.py \
      --root 1.21.11 \
      --r012-faces TEX02-R012/REBAKED_UV_AUDIT_186.csv \
      --r012-hoa TEX02-R012/HOA_FACE_CORNERS_24.csv \
      --r011-matrices TEX02-R011/ROTATION_GROUP_MATRICES_5.csv \
      --r013-slots TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv \
      --out ./r014_regenerated

Does NOT execute Minecraft client bytecode, an OpenGL renderer or GPU samples.
Evidence is original Java bytecode file identity and deterministic normalized
full-cube source projection. Guava's Interner.intern is treated as retaining
vector component *values*, although returned object identity may be changed.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

CLASS_GIT_BLOBS = {
    "inx.class": "176e5b8176abac37c563bbdc40c7a113a57e9b3f",
    "inx$d.class": "9f94b3f0d327db052de34f4351cdc94fd7a55622",
    "inx$c.class": "12e3d8e6f914e9d4c2a81d2b5dd04d11af302543",
    "inx$b.class": "c5a912de05193ebae946fa611b5567fa6d4cd2f3",
    "inx$b$1.class": "baa80d3e67a5c02a3625c4eda1f1f23c6d4190d1",
    "inx$a.class": "daedc42ed16691a4f7b31609906e051977f2b23e",
    "inw.class": "0e9d9dc53507d3ed87ba73bb268cd6305ab8633f",
    "inw$a.class": "0c8e5d9e66043f4b24681290493dc2e219c2af69",
    "hqn.class": "c72e56d607e70925eb6d1aa98a395a7b9e0d5579",
    "hqi.class": "5b64584e8cc09a8db90f802e0021bc0533e81ab1",
    "inm.class": "672b186c8a8457082fec756114b443a48dc151d1",
}
# Frozen original method bodies in inx$d.class / inx$c.class / inx$b$1.class,
# whose containing class has separately been SHA-verified in full.
CLASS_OPCODE_FRAGMENTS = {
    "inx$d.class": [
        "2a b7 00 13 2a b8 00 19 b5 00 1b b1",
        "2a b4 00 1b 2b b9 00 24 02 00 c0 00 26 b0",
    ],
    "inx$c.class": ["2a b4 00 46 b0"],
    "inx$b$1.class": ["2a b4 00 21 b0"],
    "inx.class": ["bb 00 07 59 b7 00 6b 4e 2a b4 00 5f 2b 2d b8 00 6e"],
    "hqn.class": ["b9 00 96 01 00"],  # invokeinterface inw.c():inw$a
}
CSV_GIT_BLOBS = {
    "r012_faces": "b0a1925d36a0b61b0d5b1db46fc8dbdfffe9fe75",
    "r012_hoa": "d1bc3ee8c4c696c00419b7fda3ccf76075911878",
    "r011_matrices": "99e73caf1f302751fa0aa8a89c7bebd7be61f7b0",
    "r013_slots": "18f02c6f44fd18f2a522fca81b2f73ba7409f829",
}
def git_sha(data):
    head = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(head + data).hexdigest()

def check_classes(root):
    for name, expected in CLASS_GIT_BLOBS.items():
        data=(root/name).read_bytes()
        assert data[:4]==bytes.fromhex("cafebabe"), name
        assert git_sha(data)==expected, (name, "class source Git SHA differs")
        for opcode in CLASS_OPCODE_FRAGMENTS.get(name, []):
            assert bytes.fromhex(opcode) in data, (name, "opcode proof missing")
    # Evidence: inx$d creates a strong Guava interner. Its 14-byte
    # Vector3fc method contains only: this.interner.intern(input), cast, return.
    # This verifies absence of coordinate arithmetic in this method, NOT
    # an instrumented runtime observation.
    return len(CLASS_GIT_BLOBS)

def read_frozen_csv(path, sha):
    raw=path.read_bytes()
    assert git_sha(raw)==sha, (path,"prior study CSV revision changed")
    with path.open("r",newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path,rows):
    assert rows
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main(args):
    nclasses=check_classes(args.root)
    faces=read_frozen_csv(args.r012_faces,CSV_GIT_BLOBS["r012_faces"])
    hoa=read_frozen_csv(args.r012_hoa,CSV_GIT_BLOBS["r012_hoa"])
    matrices=read_frozen_csv(args.r011_matrices,CSV_GIT_BLOBS["r011_matrices"])
    slots=read_frozen_csv(args.r013_slots,CSV_GIT_BLOBS["r013_slots"])
    assert (len(faces),len(hoa),len(matrices),len(slots)) == (186,24,5,31)
    slots_keys={(v["block"],v["property"],v["variant_index"]) for v in slots}
    assert len(slots_keys)==31

    loc={}
    for c in hoa:
        face=c["face"]
        loc.setdefault(face,[None]*4)
        idx=int(c["vertex_index"])
        assert 0<=idx<4 and loc[face][idx] is None
        loc[face][idx]=(int(c["normalized_x"]),
                        int(c["normalized_y"]),
                        int(c["normalized_z"]))
    assert len(loc)==6 and all(all(v is not None for v in arr) for arr in loc.values())
    matrix={}
    for m in matrices:
        angles=(int(m["x"]),int(m["y"]),int(m["z"]))
        matrix[angles]=tuple(tuple(map(int,m["matrix_row"+axis].split(":")))
                             for axis in "XYZ")
    assert len(matrix)==5
    vertices=[]
    face_checks=[]
    for row in faces:
        key=(row["texture_id"],row["property"],row["variant_index"])
        assert key in slots_keys
        M=matrix[(int(row["x"]),int(row["y"]),int(row["z"]))]
        origin=loc[row["local_face"]]
        canonical=loc[row["R012_world_face"]]
        old_mapping=tuple(map(int,row["R012_world_vertex_to_source_vertex_mapping"].split(":")))
        assert len(old_mapping)==4 and sorted(old_mapping)==[0,1,2,3]
        perm=[]
        for i,pos in enumerate(origin):
            v=tuple(sum(a*(pos[j]-.5) for j,a in enumerate(r))+.5 for r in M)
            assert all(c in (0.0,1.0) for c in v)
            world_i=canonical.index(v)
            assert old_mapping[world_i]==i
            perm.append(world_i)
            txt=lambda p:":".join(str(int(x)) for x in p)
            vertices.append(dict(
                texture_id=row["texture_id"],property=row["property"],
                variant_index=row["variant_index"],source_model=row["model"],
                local_face=row["local_face"],world_face=row["R012_world_face"],
                source_local_vertex_index=i,canonical_world_vertex_index=world_i,
                local_normalized_position=txt(pos),
                source_rotated_normalized_position=txt(v),
                inx_d_interning_return_normalized_position=txt(v),
                component_values_preserved=True,
                source_proof="inx$d.Interner.intern(Vector3fc)",
                actual_minecraft_quad_captured=False))
        assert sorted(perm)==[0,1,2,3]
        face_checks.append(dict(
            texture_id=row["texture_id"],property=row["property"],
            variant_index=row["variant_index"],local_face=row["local_face"],
            world_face=row["R012_world_face"],
            R012_UV_corners_changed_vs_R007=row["UV_corner_coordinates_changed"],
            R012_direction_changed_vs_R007=row["world_direction_changed"],
            canonical_vertex_mapping_matches_R012=True,
            inx_transformer_is_strong_interner=True,
            coordinate_component_values_unchanged=True,
            inx_d_coordinate_arithmetic_occurred=False,
            R012_mapping_update_needed_due_to_inx_transformer=False,
            source_projection_not_runtime=True))
    assert len(vertices)==744 and len(face_checks)==186
    assert sum(x["R012_UV_corners_changed_vs_R007"]=="true" for x in face_checks)==40
    assert sum(x["R012_direction_changed_vs_R007"]=="true" for x in face_checks)==32
    args.out.mkdir(parents=True,exist_ok=True)
    write_csv(args.out/"REGENERATED_INX_D_VERTEX_VALUES_744.csv",vertices)
    write_csv(args.out/"REGENERATED_R012_CONTEXT_RECHECK_186.csv",face_checks)
    print(json.dumps({
        "user_extracted_1_21_11_classfiles_SHA_verified":nclasses,
        "prior_immutable_source_CSVs_SHA_verified":len(CSV_GIT_BLOBS),
        "original_source_model_variant_slots":31,
        "prior_source_derived_faces_checked":186,
        "prior_source_derived_corner_vertices_checked":744,
        "prior_R007_uv_corner_differences_preserved":40,
        "prior_R007_world_face_differences_preserved":32,
        "inx_interner_coordinate_value_changes":0,
        "R012_geometry_projection_revisions_due_to_inx":0,
        "actual_minecraft_runtime_baked_quads_observed":0,
        "actual_ingame_static_renders":0
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--root",type=Path,required=True)
    cli.add_argument("--r012-faces",type=Path,required=True)
    cli.add_argument("--r012-hoa",type=Path,required=True)
    cli.add_argument("--r011-matrices",type=Path,required=True)
    cli.add_argument("--r013-slots",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    main(cli.parse_args())
