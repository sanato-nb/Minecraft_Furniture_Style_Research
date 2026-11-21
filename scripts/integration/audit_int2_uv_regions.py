"""INT-2 1-4: re-crop 29,957 ordinary/animation UV pixel regions.

Reopens 2,171 immutable source textures from official pinned Git/JAR assets,
independently converts original 0-16 UV to frame pixel boxes and recomputes
RGBA metrics for ALL 29,957 historical frame-region samples, representing
511,709 model-face instances by group weights. The weights are taken from
prior 1-4 model linkage and are not a fresh 592,312-face per-model rebuild.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
from fractions import Fraction
import hashlib
import io
import json
import lzma
from math import floor,ceil
from pathlib import Path

from PIL import Image
from audit_int2_mod_textures import Sources,csv_rows,raw_source_sha,verify_png_crc
from audit_int2_uv_support import region_metrics

ROOT=Path(__file__).resolve().parents[2]
PATH="research/furniture_mods/phase_1-4/entry02"
QUEUE="research/furniture_mods/phase_1-3/F/1-3_TEXTURE_UV_HANDOFF.csv"
KNOWN="research/furniture_mods/phase_1-4/entry02/ENTRY02_AUDIT.json"
COLUMNS=["texture_id","uv","frame","status","original_png_sha",
         "pixel_box","pixels","rgba_sha256","comparison","differences"]

def read_xz_rows(path):
    with lzma.open(path,"rt",encoding="utf-8-sig",newline="") as stream:
        yield from csv.DictReader(stream)

def pixel_box(uv,w,h):
    if len(uv)!=4 or uv[0]==uv[2] or uv[1]==uv[3]:
        raise ValueError("Expected nonzero rectangle UV")
    if any(x<0 or x>16 for x in uv):
        raise ValueError("Expected in-sprite UV")
    return (floor(min(uv[0],uv[2])*w/16),
            floor(min(uv[1],uv[3])*h/16),
            ceil(max(uv[0],uv[2])*w/16),
            ceil(max(uv[1],uv[3])*h/16))

def recrop(root,args):
    queue={r["texture_id"]:r for r in csv_rows(root/QUEUE)}
    expected=json.loads((root/KNOWN).read_text(encoding="utf-8"))
    if len(queue)!=2256:
        raise ValueError("Pinned UV queue changed")
    source=Sources(args)
    images={}
    groups={}
    groupframes=defaultdict(set)
    errors=[]
    summary=Counter()
    by_mod=Counter()
    output=args.out/"INT2_1_4_29957_UV_RECHECK.csv"
    try:
        with output.open("w",encoding="utf-8",newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=COLUMNS,lineterminator="\n")
            writer.writeheader()
            for shard in range(1,12):
                file=root/PATH/f"UV_REGIONS_{shard:02}.csv.xz"
                for row in read_xz_rows(file):
                    tid=row["texture_id"]
                    source_row=queue[tid]
                    if tid not in images:
                        raw=source.fetch(source_row["source_id"],source_row["path"])
                        verified_sha=raw_source_sha(raw,source_row["source_hash_kind"])
                        if verified_sha!=source_row["source_sha"]:
                            raise ValueError("Original PNG SHA differs: "+tid)
                        verify_png_crc(raw,source_row["path"])
                        with Image.open(io.BytesIO(raw)) as png:
                            png.load()
                            rgba=png.convert("RGBA")
                        meta=source.fetch(source_row["source_id"],source_row["path"]+".mcmeta",required=False)
                        metadata=json.loads(meta.decode("utf-8-sig")).get("animation") if meta is not None else None
                        if metadata:
                            if rgba.height%rgba.width!=0 or rgba.height<=rgba.width:
                                raise ValueError("Unsupported pinned animation frame layout: "+tid)
                            frames=[rgba.crop((0,y,rgba.width,y+rgba.width))
                                    for y in range(0,rgba.height,rgba.width)]
                        else:
                            frames=[rgba]
                        images[tid]=frames
                        by_mod[source_row["source_id"]]+=1
                    frames=images[tid]
                    frame=int(row["frame"])
                    if frame<0 or frame>=len(frames):
                        raise ValueError(f"{tid}: source frame index out of range")
                    width,height=frames[0].size
                    uv=tuple(Fraction(v) for v in row["uv"].split("|"))
                    box=pixel_box(uv,width,height)
                    if not (0<=box[0]<box[2]<=width and 0<=box[1]<box[3]<=height):
                        raise ValueError("Computed source pixel box outside PNG")
                    sampled=frames[frame].crop(box)
                    crop=region_metrics(sampled)
                    rgba_sha=crop["rgba_sha256"]
                    uv_group=(tid,row["uv"])
                    count=int(row["face_instances_per_uv"])
                    if uv_group in groups and groups[uv_group]!=count:
                        raise ValueError("Historical UV group has inconsistent face instance count")
                    groups[uv_group]=count
                    groupframes[uv_group].add(frame)
                    metrics={
                        "pixel_box":"|".join(map(str,box)),
                        "transparent":crop["transparent"],
                        "partial_alpha":crop["partial_alpha"],
                        "opaque":crop["opaque"],
                        "visible_rgb_colors":crop["visible_rgb"],
                        "top4_visible_rgba_counts":crop["dominant_rgba"],
                        "rgba8_sha256":rgba_sha,
                    }
                    diffs=[k for k,v in metrics.items() if str(row[k])!=str(v)]
                    if diffs and len(errors)<100:
                        errors.append({"texture_id":tid,"uv":row["uv"],"frame":frame,"fields":diffs})
                    summary["sampled_frame_regions"]+=1
                    summary["frame_regions_matching"]+=int(not diffs)
                    summary["region_frame_source_pixels"]+=sampled.width*sampled.height
                    label="ANIMATED_FRAME_RECTS" if len(frames)>1 else "STATIC_RECT"
                    writer.writerow({
                        "texture_id":tid,"uv":row["uv"],"frame":frame,"status":label,
                        "original_png_sha":source_row["source_sha"],
                        "pixel_box":metrics["pixel_box"],"pixels":sampled.width*sampled.height,
                        "rgba_sha256":rgba_sha,
                        "comparison":"PASS" if not diffs else "DIFFERENCE",
                        "differences":"|".join(diffs),
                    })
            for group,n in groups.items():
                if groupframes[group]!=set(range(len(images[group[0]]))):
                    if len(errors)<100:
                        errors.append({"group":group,"reason":"Not every animation frame was represented"})
                summary["supported_face_instances"]+=n
            summary["unique_uv_groups"]=len(groups)
            summary["unique_png_with_face_regions"]=len(images)
    finally:
        source.close()
    target={"sampled_frame_regions":29957,"region_frame_source_pixels":2127316,
            "supported_face_instances":511709,"unique_uv_groups":27778,
            "unique_png_with_face_regions":2171,
            "frame_regions_matching":29957}
    wrong={key:{"actual":summary[key],"expected":value} for key,value in target.items()
           if summary[key]!=value}
    report={
      "schema":"MCFR_INT2_1_4_ALL_ORDINARY_UV_REGION_REAUDIT/v1",
      "method":"independent_pinned_original_texture_and_UV_0_16_crop_per_historical_region_frame",
      "original_texture_files_reopened":len(images),
      "per_source_new_redecode_counts":dict(sorted(by_mod.items())),
      "observed":dict(sorted(summary.items())),
      "expected":target,
      "aggregate_differences":wrong,
      "per_region_discrepancies":summary["sampled_frame_regions"]-summary["frame_regions_matching"],
      "discrepancy_examples":errors,
      "per_region_csv_sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
      "historic_29083_groups_reconciliation":{
         "ordinary_region_groups":len(groups),
         "exception_uv_groups_in_entry02":1298,
         "missing_png_face_groups_in_entry02":7,
         "all_previous_nonzero_face_groups":len(groups)+1298+7,
      },
      "inherited_face_instance_weights":"HISTORIC_1_4_NOT_RECOMPUTED_FROM_MODEL_STATE",
      "not_checked":["all 592312 model-face-to-texture links independently rebuilt",
                      "runtime UVlock,tint,atlas","source AI training rights"],
      "status":"PASS_ORIGINAL_UV_REGION_PIXEL_RECHECK" if not wrong and not errors else "DISCREPANCY_REQUIRES_REVIEW",
    }
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=ROOT)
    for n in ("af","hc","macaw","mc1211","mc12111","out"):
        p.add_argument("--"+n,type=Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    report=recrop(args.root,args)
    (args.out/"INT2_1_4_UV_REGIONS_SUMMARY.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    print("INT2_1_4_UV_REGIONS_RESULT:"+json.dumps(report,sort_keys=True,ensure_ascii=False))
    if report["status"]!="PASS_ORIGINAL_UV_REGION_PIXEL_RECHECK":
        raise SystemExit("INT-2 original UV region re-cropping found mismatches")

if __name__=="__main__":
    main()
