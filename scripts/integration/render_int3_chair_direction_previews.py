"""INT-3 original texture diagnostic: 4 children by 4 source blockstate facings.

Depends on prior, independently verified source-selection CSV and pinned
1-3-F/PNG original archives. Reuses PR31 renderer for UV/PNG; rotates geometry
according to the literal blockstate JSON 'y' and preserves texture faces when
uvlock=0. This is NOT a game-client model bake, screenshots or behavioral test.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image,ImageDraw

from audit_int2_mod_textures import Sources
import render_int3_textured_chairs as texture
import render_int3_chair_geometry as original
from audit_int3_chair_blockstates import DIRECTIONS,STUDY_PARENT_KEYS,STUDY_MODEL_KEYS

ROOT=Path(__file__).resolve().parents[2]

def run(args):
    root=Path(args.root)
    output=Path(args.out)
    output.mkdir(parents=True,exist_ok=True)
    audit=json.loads((output/"INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json").read_text(encoding="utf-8"))
    if audit["totals"]["study_orientation_pose_rows"]!=16:
        raise ValueError("Missing prior source-state pose audit")
    ledger=output/"INT3_CHAIR_16_ORIENTATION_POSES.csv"
    if hashlib.sha256(ledger.read_bytes()).hexdigest()!=audit["sha256"]["selected_source_geometry_orientation_rows_csv"]:
        raise ValueError("Source 16-pose audit CSV sha mismatch")
    with ledger.open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    by={(r["model_key"],r["facing"]):r for r in rows}
    if set(by)!={(k,d) for k in STUDY_MODEL_KEYS for d in DIRECTIONS}:
        raise ValueError("Selected 4 child models x 4 state facings incomplete")
    source=Sources(args)
    db=original.load_db(root)
    try:
        providers,original_model_evidence,roles=texture.read_original_shapes(db,source)
        entries={key:texture.assemble_model(db,source,providers,provider,key)
                 for key,provider in STUDY_PARENT_KEYS.items()}
        if sum(len(x["selected_faces"]) for x in entries.values())!=229:
            raise ValueError("Texture source face set no longer pinned to 229")
        previews=[]
        counts={}
        images=[]
        for key in sorted(STUDY_MODEL_KEYS):
            entry=entries[key]
            for direction in DIRECTIONS:
                state=by[key,direction]
                rotation=int(state["y"])
                if rotation not in (0,90,180,270) or int(state["x"])!=0 or int(state["uvlock"])!=0:
                    raise ValueError("Fixed-state orientation has non-ordinary model bake attributes")
                png,drawn=texture.preview(entry,yaw=45,block_y=rotation)
                previews.append({"model_key":key,"direction":direction,"state_selector":state["selector"],
                                 "rotation_y":rotation,"drawn_visible_faces":drawn,
                                 "source_faces":len(entry["selected_faces"]),
                                 "child_model_sha":entry["model_sha"],"state_sha":state["source_sha"],
                                 "pixel_origin":"ORIGINAL_SHA_VERIFIED_PNG_SPRITE",
                                 "render_status":"GEOMETRY_UV_DIAGNOSTIC_NOT_GAME_CLIENT"})
                images.append(png)
                counts[key]=len(entry["selected_faces"])
        W,H=texture.PANEL
        sheet=Image.new("RGB",(W*4,H*4),(241,245,250))
        for i,im in enumerate(images):
            sheet.paste(im,((i%4)*W,(i//4)*H))
        outfile=output/"INT3_4_CHAIRS_16_SOURCE_STATE_TEXTURED_VIEWS.png"
        sheet.save(outfile,optimize=False)
        table=output/"INT3_CHAIR_16_TEXTURED_DIRECTION_SOURCE_EVIDENCE.csv"
        with table.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(previews[0]))
            writer.writeheader()
            writer.writerows(previews)
        result={
           "schema":"MCFR_INT3_16_TEXTURED_BLOCKSTATE_POSES_v1",
           "status":"PASS_ORIGINAL_CHAIR_16_DIRECTION_TEXTURE_DIAGNOSTIC_NOT_RUNTIME",
           "models":4,"original_source_faces":229,"directional_texture_panels":len(previews),
           "unique_source_pngs":len({(v["source"],v["path"]) for e in entries.values()
                                     for v in e["textures"].values()}),
           "source_orientation_manifest_sha256":hashlib.sha256(ledger.read_bytes()).hexdigest(),
           "source_blockstate_document_sha256":hashlib.sha256(
               (output/"INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json").read_bytes()).hexdigest(),
           "original_texture_contact_sheet_sha256":hashlib.sha256(outfile.read_bytes()).hexdigest(),
           "per_pose_csv_sha256":hashlib.sha256(table.read_bytes()).hexdigest(),
           "per_model_original_face_counts":dict(sorted(counts.items())),
           "runtime_model_bake_verifications":0,"runtime_screenshots":0,
           "source_variants_manually_corrected":0,
           "copyright_training_approvals":0,
           "known_limitations":[
               "Rotated original cuboid corner geometry according to literal y attribute, not Mojang baked model or GPU atlas",
               "UV pixels sample the source PNG face independently of engine UV lock, AO, tint and culling",
               "Fixed selected variant and waterlogged=false per pose; other 228 source options are saved separately",
               "All 16 views are static sprite diagnostics, NOT Minecraft client screenshots",
           ],
        }
        (output/"INT3_CHAIR_16_TEXTURED_POSE_SUMMARY.json").write_text(
            json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
        print("INT3_CHAIR_POSE_PREVIEW_RESULT:"+json.dumps(result,sort_keys=True,ensure_ascii=False))
        return result
    finally:
        db.close()
        source.close()

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("root","af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=name!="root",default=ROOT if name=="root" else None)
    run(parser.parse_args(argv))

if __name__=="__main__":
    main()
