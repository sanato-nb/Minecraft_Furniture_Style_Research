"""Source-anchored proof that real in-game chair F2 images are visually isolated.

A successful Minecraft F2 file does not imply an uncontaminated view.
PR #33 staged three 7x7 stone test platforms at z=40/54/68; the north-
facing camera saw those stages in the distance and could mistake them for
floating chair parts. The new fixture puts all 1.21.1 groups on z=40,
separated by >=16 blocks in x. The screenshot test below checks an
upper-sky screen region for achromatic stone-like pixels, and verifies
the selected source chair remains visible.

These counts are a controlled *visual staging* check, not a semantic
role/UV/material/game-physics approval or a general image classifier.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

from .chair_runtime_fixture import cases

SKY_RECT=(0,90,1024,360)
CENTER_RECT=(420,350,605,580)
SKY_STONE_LIMIT=1000
MIN_FOREGROUND_CHROMA=150

def stone_pixels(im):
    """Achromatic high-contrast gray proxy on uniform 1.21.1 sky.

    This is intentionally scoped only to the fixed game/client sky
    and HUD-hidden camera setup. It is not an arbitrary game screenshot
    or machine-learned object detector.
    """
    region=im.crop(SKY_RECT).convert("RGB")
    count=0
    for r,g,b in region.getdata():
        if abs(r-g)<18 and abs(g-b)<22 and 55<r<235:
            count+=1
    return count

def specimen_color_pixels(im):
    region=im.crop(CENTER_RECT).convert("RGB")
    return sum(1 for r,g,b in region.getdata() if
               (r>g+20 and r>b+10) or
               (g>r+10 and g>b+5) or
               (r>b+20 and r>g+4))

def audit(folder,version):
    folder=Path(folder)
    source=json.loads((folder/"INT3_REAL_GAME_CAPTURE.json").read_text(encoding="utf-8"))
    expected=cases(version)
    if source.get("version")!=version:
        raise ValueError("Captured client version differs from selected source fixture")
    if (source.get("status")!="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" or
        len(source.get("states",[]))!=len(expected)):
        raise ValueError("Native F2 capture evidence incomplete")
    byid={r["case_id"]:r for r in source["states"]}
    if set(byid)!={c.case_id for c in expected}:raise ValueError("Wrong source state case set")
    rows=[]
    for item in expected:
        r=byid[item.case_id]
        if r["original_state"]!=item.state() or not r["server_blockstate_verified"]:
            raise ValueError("Source runtime state invalid "+item.case_id)
        p=folder/r["screenshot_file"]
        if p.name!=item.case_id+".png" or hashlib.sha256(p.read_bytes()).hexdigest()!=r["screenshot_sha256"]:
            raise ValueError("F2 screenshot source SHA changed "+item.case_id)
        with Image.open(p) as im:
            if im.size!=(1024,684):
                raise ValueError("Original F2 native image dimensions changed")
            stones=stone_pixels(im) if version=="1.21.1" else None
            foreground=specimen_color_pixels(im)
        # The first client version uses a fixed plain-blue sky; any leftover
        # stone stages in the top viewport invalidate the isolated comparison.
        if stones is not None and stones>=SKY_STONE_LIMIT:
            raise ValueError("Other chair test platforms intrude upon isolated F2: "+
                             f"{item.case_id}, stone_proxy_pixels={stones}")
        if foreground<MIN_FOREGROUND_CHROMA:
            raise ValueError("Selected chair is not confidently visible: "+
                             f"{item.case_id}, chromatic_foreground={foreground}")
        rows.append({
           "case_id":item.case_id,
           "original_model":item.model_key,
           "source_blockstate":item.state(),
           "in_game_F2_sha256":r["screenshot_sha256"],
           "source_camera":item.camera(),
           "staging_platform":f"{item.x-3}|{item.y-1}|{item.z-3}|{item.x+3}|{item.y-1}|{item.z+3}",
           "stone_pixel_count_in_upper_sky":stones if stones is not None else "NOT_SCOPED_CLOUDY_SKY",
           "specimen_chroma_pixels":foreground,
           "background_intrusion_decision":("NO_STAGE_PIXELS_BY_FIXED_BLUE_SKY_TEST"
                                           if version=="1.21.1"
                                           else "SINGLE_GROUP_PLACEMENT_ONLY"),
           "source_part_roles_approved":0,"minecraft_uv_mesh_approved":0
        })
    csvfile=folder/"INT3_ISOLATED_F2_VISIBILITY_EVIDENCE.csv"
    with csvfile.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    doc={
      "schema":"MCFR_INT3_REAL_F2_ISOLATED_STAGING/v1",
      "version":version,
      "state":"PASS_ORIGINAL_F2_CHAIR_VISIBLE_AND_STAGING_ISOLATION_NOT_SEMANTICS",
      "native_f2_count":len(rows),
      "model_keys":sorted({r["original_model"] for r in rows}),
      "all_stages_same_z_plane":len({item.z for item in expected})==1,
      "minimum_distinct_chair_x_separation":min(
          abs(a.x-b.x) for i,a in enumerate(expected) for b in expected[i+1:]),
      "scope_stone_sky_pixels":("1.21.1_FIXED_UNIFORM_BLUE_SKY" if version=="1.21.1"
                                else "NOT_USED_1.21.11_SKY_CLOUDS"),
      "max_stone_sky_pixels":(max(int(r["stone_pixel_count_in_upper_sky"]) for r in rows)
                               if version=="1.21.1" else None),
      "minimum_foreground_chroma_pixels":min(int(r["specimen_chroma_pixels"]) for r in rows),
      "zero_background_staging_intrusions":version=="1.21.1",
      "runtime_model_bake_approved":0,"semantic_role_approved":0,
      "texture_uv_pixel_equality_approved":0,"ai_training_rights_approved":0,
      "evidence_csv_sha256":hashlib.sha256(csvfile.read_bytes()).hexdigest(),
      "native_source_manifest_sha256":hashlib.sha256((folder/"INT3_REAL_GAME_CAPTURE.json").read_bytes()).hexdigest(),
      "limitations":[
         "Scoped screen pixel test detects stone-colored upper-sky intrusions, not general foreground occlusion",
         "A source fixture stage's visibility isn't evidence about furniture geometry or shape",
         "Macaw version 1.21.11 sky clouds preclude the fixed-blue-sky threshold",
         "Source/asset license and role/material/UV agreement remain unapproved"
       ]
    }
    (folder/"INT3_ISOLATED_F2_VISIBILITY_SUMMARY.json").write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return doc

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",type=Path,required=True)
    parser.add_argument("--version",choices=("1.21.1","1.21.11"),required=True)
    args=parser.parse_args(argv)
    print("INT3_F2_ISOLATION:"+json.dumps(audit(args.directory,args.version),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
