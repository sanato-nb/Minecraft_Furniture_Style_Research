"""INT-3 audit of a manually inspected geometry-only chair role review ledger.

A geometry contact sheet annotates existing hypotheses with colors; it is
not independent proof of furniture function. This validates the exact
pinned models, all 45 original source element indices and SHA, and ensures
no texture/runtime/material/training claim is silently elevated.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[2]
REVIEW="project/integration/INT3_45_CHAIR_GEOMETRY_REVIEW.csv"
SOURCE_F="research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz"
R="GROUP_LEVEL_SHAPE_PLAUSIBLE"
P="PENDING_TEXTURE_AND_GAME_VISUAL"
RIGHTS="PENDING_ORIGINAL_LICENSE_REVIEW"
ROLE_COUNTS={"BACKREST_ASSEMBLY":16,"LEG_OR_LOWER_POST":16,"LOWER_FRAME":7,"SEAT_LAYER":6}

def verify(root,render_summary):
    doc=json.loads(render_summary.read_text(encoding="utf-8"))
    if doc["status"]!="PASS_RAW_SOURCE_FOUR_PROVIDER_GEOMETRY_RECONSTRUCTED":
        raise ValueError("No fresh original source-based model render success")
    if doc["role_candidate_visual_approval"]!=0 or doc["runtime_recheck"]:
        raise ValueError("Model geometry alone cannot approve original client rendering")
    png=render_summary.parent/"INT3_45_CHAIR_GEOMETRY_CONTACT_SHEET.png"
    if hashlib.sha256(png.read_bytes()).hexdigest()!=doc["sheet_sha256"]:
        raise ValueError("Rendered contact sheet image SHA mismatch")
    with (root/REVIEW).open("r",encoding="utf-8",newline="") as f:
        entries=list(csv.DictReader(f))
    keys=[(r["source_id"],r["resource_id"],int(r["element_index"])) for r in entries]
    if len(keys)!=45 or len(set(keys))!=45:
        raise ValueError("Expected all 45 unique original provider element reviews")
    registered={(r["mod"],r["resource"]):r for r in doc["providers"]}
    if len(registered)!=4:
        raise ValueError("Four original model sources not found")
    totals=Counter()
    with sqlite3.connect(":memory:") as db:
        db.row_factory=sqlite3.Row
        db.deserialize(lzma.decompress((root/SOURCE_F).read_bytes()))
        if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
            raise ValueError("F DB integrity check failure")
        for r in entries:
            key=(r["source_id"],r["resource_id"])
            model=registered.get(key)
            if model is None:
                raise ValueError("Review contains unrendered or unpinned source: "+str(key))
            if r["original_model_sha"]!=model["sha"]:
                raise ValueError("Reviewer model SHA is not the original SHA")
            if r["visual_contact_sheet_sha256"]!=doc["sheet_sha256"]:
                raise ValueError("Reviewer sheet checksum is not the visible source render")
            if (r["inspection_basis"]!="TWO_ANGLE_GEOMETRY_RENDER"
                or r["geometry_layout_assessment"]!=R
                or r["material_runtime_status"]!=P
                or r["asset_rights_status"]!=RIGHTS
                or len(r["independent_group_observation"].strip())<35):
                raise ValueError("Review claim scope exceeded available rendered evidence")
            row=db.execute("""
                SELECT m.source_id,m.resource_id,m.sha,e.part_candidate,e.part_evidence
                FROM element e JOIN model m ON m.model_key=e.provider_key
                WHERE m.source_id=? AND m.resource_id=? AND e.element_index=?
                """,(key[0],key[1],int(r["element_index"]))).fetchone()
            if row is None or row["sha"]!=r["original_model_sha"]:
                raise ValueError("Manual visual review is not backed by the original model")
            if row["part_candidate"]!=r["source_role_candidate"] or row["part_evidence"]!="GEOMETRY_AND_FACE_SLOTS":
                raise ValueError("Historical role evidence and review scope disagree")
            totals[r["source_role_candidate"]]+=1
    if dict(totals)!=ROLE_COUNTS:
        raise ValueError("Incorrect historical role grouping in 45 reviews")
    if any(model["element_count"]!=sum(key==(r["source_id"],r["resource_id"]) for r in entries)
           for key,model in registered.items()):
        raise ValueError("Some original provider elements were not included in visual assessment")
    raw=(root/REVIEW).read_bytes()
    return {
       "schema":"MCFR_INT3_GEOMETRY_ONLY_MANUAL_VISUAL_ASSESSMENT/v1",
       "status":"PASS_45_SOURCE_ANCHORED_GEOMETRY_LAYOUT_ASSESSMENTS",
       "inspection_scope":"COLORED_TWO_ANGLE_SOURCE_GEOMETRY_NOT_TEXTURED_OR_GAME_RENDER",
       "review_rows":len(entries),
       "provider_models":len(registered),
       "role_counts":dict(sorted(totals.items())),
       "layout_plausible_count":sum(r["geometry_layout_assessment"]==R for r in entries),
       "game_texture_visual_verified":0,
       "human_approved_universal_roles":0,
       "license_approval":0,
       "original_source_sha_verification":True,
       "source_render_sha256":doc["sheet_sha256"],
       "per_element_review_csv_sha256":hashlib.sha256(raw).hexdigest(),
       "visual_inference_limit":"Palette marks hypotheses; shapes and two camera views show plausible placement but cannot independently prove function or textures.",
    }

def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root",type=Path,default=ROOT)
    cli.add_argument("--render-summary",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    a=cli.parse_args()
    result=verify(a.root,a.render_summary)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("INT3_REVIEW_CROSSCHECK:"+json.dumps(result,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
