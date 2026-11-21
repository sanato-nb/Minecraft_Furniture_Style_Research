"""INT-2 1-4 independent source PNG pixel and exit-evidence audit.

Reopens 1,996 pinned new candidate textures plus five original chair controls
from immutable AF/HC source archives, Macaw's pinned JAR and Mojang client JARs.
Verifies hashes, PNG chunk CRCs, actual decode, RGBA SHA, histogram, colours,
dimensions, metadata and recorded 1-4 entry01 measurements independently.
Does NOT claim to reproduce the full 592,312 in-game UV projection.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import struct
import zipfile
import zlib

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HANDOFF="research/furniture_mods/phase_1-3/F/1-3_TEXTURE_UV_HANDOFF.csv"
CHAIR="research/furniture_mods/phase_1-3/F/F_V24_CHAIR_PNG.csv"
HISTORY="research/furniture_mods/phase_1-4/entry01/1-4_PNG_PIXEL_LEDGER.csv.gz"
ENTRY1="research/furniture_mods/phase_1-4/entry01/1-4_ENTRY01_AUDIT.json"
ENTRY2="research/furniture_mods/phase_1-4/entry02/ENTRY02_AUDIT.json"
SUPPORT="research/furniture_mods/phase_1-4/C_followup/SUMMARY.json"
FINAL="research/furniture_mods/phase_1-4/F/EXIT_AUDIT.json"
FIELDNAMES=["texture_id","source_id","resource_id","scope","path",
"sha256_raw","source_sha","git_sha1","png_bytes","width","height",
"pixels","rgba_sha256","transparent","partial_alpha","opaque",
"visible_rgb_colors","top4_visible_rgba_counts","png_bit_depth",
"png_color_type","png_frames","png_crc_chunks","mcmeta_status",
"mcmeta_sha","comparison","differences"]
PINS={
"macaw":("sha256","e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"),
"mc1211":("sha1","30c73b1c5da787909b2f73340419fdf13b9def88"),
"mc12111":("sha1","ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"),
}
PREFIXES={
"AF":"AnotherFurniture",
"HC":"Handcrafted",
}
SIGNATURE=b"\x89PNG\r\n\x1a\n"

def csv_rows(path):
    opener=gzip.open if str(path).endswith(".gz") else open
    with opener(path,"rt",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def raw_source_sha(data,kind):
    if kind=="GIT_BLOB_SHA1":
        return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
    if kind=="SHA256":
        return hashlib.sha256(data).hexdigest()
    raise ValueError("Unrecognized source hash algorithm "+kind)

def verify_png_crc(data,path):
    if not data.startswith(SIGNATURE):
        raise ValueError(f"{path}: invalid PNG signature")
    start=len(SIGNATURE)
    chunks=0
    idat=0
    seen_end=False
    while start<len(data):
        if start+12>len(data):
            raise ValueError(f"{path}: truncated PNG")
        size=struct.unpack_from(">I",data,start)[0]
        stop=start+12+size
        if stop>len(data):
            raise ValueError(f"{path}: out-of-file PNG chunk")
        tag=data[start+4:start+8]
        body=data[start+8:start+8+size]
        oldcrc=struct.unpack_from(">I",data,start+8+size)[0]
        if zlib.crc32(tag+body)&0xffffffff !=oldcrc:
            raise ValueError(f"{path}: PNG CRC differs in {tag!r}")
        if chunks==0 and (tag!=b"IHDR" or size!=13):
            raise ValueError(f"{path}: invalid IHDR")
        idat+=int(tag==b"IDAT")
        chunks+=1
        start=stop
        if tag==b"IEND":
            if size!=0 or start!=len(data):
                raise ValueError(f"{path}: invalid IEND/trailing payload")
            seen_end=True
            break
    if not seen_end or not idat:
        raise ValueError(f"{path}: PNG missing IDAT/IEND")
    return chunks

def png_metrics(data,path):
    chunk_count=verify_png_crc(data,path)
    width,height,depth,colortype=struct.unpack_from(">IIBB",data,16)
    with Image.open(io.BytesIO(data)) as img:
        if img.format!="PNG":
            raise ValueError("Pillow decoded another format "+path)
        frames=getattr(img,"n_frames",1)
        img.verify()
    with Image.open(io.BytesIO(data)) as img:
        img.load()
        im=img.convert("RGBA")
        if im.size!=(width,height):
            raise ValueError("PNG header does not match fully decoded size "+path)
        raw=im.tobytes()
    hist=Counter(raw[i:i+4] for i in range(0,len(raw),4))
    z=sum(n for rgba,n in hist.items() if rgba[3]==0)
    p=sum(n for rgba,n in hist.items() if 0<rgba[3]<255)
    full=sum(n for rgba,n in hist.items() if rgba[3]==255)
    visible=[(rgba,n) for rgba,n in hist.items() if rgba[3]>0]
    dominant=sorted(visible,key=lambda r:(-r[1],r[0]))[:4]
    return {
       "width":width,"height":height,"pixels":width*height,
       "rgba_sha256":hashlib.sha256(raw).hexdigest(),
       "transparent":z,"partial_alpha":p,"opaque":full,
       "visible_rgb_colors":len({rgba[:3] for rgba,n in visible}),
       "top4_visible_rgba_counts":"|".join(rgba.hex()+":"+str(count) for rgba,count in dominant),
       "png_bit_depth":depth,"png_color_type":colortype,
       "png_frames":frames,"png_crc_chunks":chunk_count,
    }

class Sources:
    def __init__(self,args):
        self.archives={}
        self.indices={}
        for mod,name in [("AF","af"),("HC","hc")]:
            archive=zipfile.ZipFile(getattr(args,name))
            index={}
            for entry in archive.namelist():
                if entry.endswith("/"):
                    continue
                tail=entry.partition("/")[2]
                if tail in index:
                    raise ValueError(f"Duplicated source path {mod}:{tail}")
                index[tail]=entry
            self.archives[mod]=archive
            self.indices[mod]=index
        for mod,name in [("MACAW","macaw"),("MC1.21.1","mc1211"),("MC1.21.11","mc12111")]:
            alg,expected=PINS[name]
            raw=getattr(args,name).read_bytes()
            if hashlib.new(alg,raw).hexdigest()!=expected:
                raise ValueError(f"Pinned source binary differs: {mod}")
            archive=zipfile.ZipFile(io.BytesIO(raw))
            if archive.testzip() is not None:
                raise ValueError(f"ZIP CRC error in {mod}")
            self.archives[mod]=archive
            self.indices[mod]={p:p for p in archive.namelist()}
    def fetch(self,mod,path,required=True):
        name=self.indices[mod].get(path)
        if name is None:
            if required:
                raise ValueError(f"Missing pinned original {mod}:{path}")
            return None
        return self.archives[mod].read(name)
    def close(self):
        for z in self.archives.values():
            z.close()

def pixels_audit(root,args):
    source_rows=csv_rows(root/HANDOFF)
    chair_rows=csv_rows(root/CHAIR)
    old_rows=csv_rows(root/HISTORY)
    first=json.loads((root/ENTRY1).read_text(encoding="utf-8"))
    if len(source_rows)!=2256 or len(chair_rows)!=24 or len(old_rows)!=2001:
        raise ValueError("Existing texture source census changed")
    queue={str(r["texture_id"]):r for r in source_rows}
    known={str(r["texture_id"]):r for r in old_rows}
    chair_ids={r["resource_id"] for r in chair_rows}
    if len(queue)!=2256 or len(known)!=2001 or len(chair_ids)!=24:
        raise ValueError("Duplicate texture identity in historical ledger")
    selected={id:r for id,r in queue.items() if r["disposition"]=="PNG_UV_CANDIDATE" or r["resource_id"] in chair_ids}
    if len(selected)!=2001 or set(known)!=set(selected):
        raise ValueError("Pinned original PNG selection differs from 1-4 Entry01")
    sources=Sources(args)
    tally=Counter()
    scope_counter=Counter()
    source_counter=Counter()
    outputs=[]
    errors=[]
    try:
        for tid in sorted(selected,key=int):
            r=selected[tid]
            old=known[tid]
            mod,path,kind=r["source_id"],r["path"],r["source_hash_kind"]
            data=sources.fetch(mod,path)
            sha=raw_source_sha(data,kind)
            if sha!=r["source_sha"]:
                raise ValueError(f"Original source and 1-3-F disagree: {mod}/{path}")
            stats=png_metrics(data,path)
            meta=sources.fetch(mod,path+".mcmeta",required=False)
            meta_sha=raw_source_sha(meta,kind) if meta is not None else ""
            obj=json.loads(meta.decode("utf-8-sig")) if meta is not None else None
            if obj is not None and not isinstance(obj,dict):
                raise ValueError(f"Invalid source .mcmeta JSON {path}")
            meta_status=("ANIMATION" if "animation" in obj else "OTHER") if obj is not None else "NONE"
            scope="NEW_CANDIDATE" if r["disposition"]=="PNG_UV_CANDIDATE" else "PRIOR_CHAIR_CONTROL"
            computed={
                "texture_id":tid,"source_id":mod,"resource_id":r["resource_id"],
                "scope":scope,"path":path,
                "sha256_raw":hashlib.sha256(data).hexdigest(),
                "source_sha":sha,
                "git_sha1":raw_source_sha(data,"GIT_BLOB_SHA1"),
                "png_bytes":len(data),**stats,
                "mcmeta_status":meta_status,"mcmeta_sha":meta_sha,
            }
            fields={
                "pinned_path":path,
                "computed_sha":sha,
                "png_bytes":len(data),
                "width":stats["width"],"height":stats["height"],
                "bit_depth":stats["png_bit_depth"],
                "png_color_type":stats["png_color_type"],
                "rgba8_sha256":stats["rgba_sha256"],
                "content_sha256":computed["sha256_raw"],
                "png_frames":stats["png_frames"],
                "transparent":stats["transparent"],
                "partial_alpha":stats["partial_alpha"],
                "opaque":stats["opaque"],
                "visible_rgb_colors":stats["visible_rgb_colors"],
                "top4_visible_rgba_counts":stats["top4_visible_rgba_counts"],
                "mcmeta_status":meta_status,"mcmeta_sha":meta_sha,
                "scope":scope,"source_id":mod,
                "hash_algorithm":kind,"resource_id":r["resource_id"],
                "texture_id":tid,
            }
            differences=[f for f,value in fields.items() if str(old.get(f))!=str(value)]
            computed["comparison"]="PASS" if not differences else "DIFFERENCE"
            computed["differences"]="|".join(differences)
            if differences and len(errors)<100:
                errors.append({"texture_id":tid,"source":mod,"path":path,"fields":differences})
            outputs.append(computed)
            tally["redecoded_png"]+=1
            tally["pixels"]+=stats["pixels"]
            tally["transparent"]+=stats["transparent"]
            tally["partial_alpha"]+=stats["partial_alpha"]
            tally["opaque"]+=stats["opaque"]
            tally["png_crc_pass"]+=1
            tally["png_rgba_sha_match"]+=int("rgba8_sha256" not in differences)
            tally["png_full_record_matches"]+=int(not differences)
            scope_counter[scope]+=1
            source_counter[mod]+=int(scope=="NEW_CANDIDATE")
    finally:
        sources.close()
    if tally["pixels"]!=4406272 or scope_counter!={"NEW_CANDIDATE":1996,"PRIOR_CHAIR_CONTROL":5}:
        errors.append({"type":"GLOBAL","reason":"Historical source count or pixels mismatch"})
    if dict(source_counter)!=first["new_png_by_source"]:
        errors.append({"type":"GLOBAL","reason":"New png-by-source distribution mismatch"})
    if sum(tally[k] for k in ("transparent","partial_alpha","opaque"))!=tally["pixels"]:
        errors.append({"type":"GLOBAL","reason":"Alpha partition mismatch"})
    return outputs,{
        "schema":"MCFR_INT2_1_4_ORIGINAL_PNG_REAUDIT/v1",
        "baseline_sha":"176f7f34de2336eb7984c4734e97b6eb156c19f4",
        "pinned_texture_pairs":len(queue),
        "png_scopes":dict(scope_counter),
        "new_png_by_source":dict(sorted(source_counter.items())),
        "source_file_metrics":dict(tally),
        "per_png_discrepancies":sum(row["comparison"]!="PASS" for row in outputs),
        "discrepancy_examples":errors,
        "not_verified":["full_592312_face UV original source calculation","GPU atlas UV lock/tint","actual animated frame timing","source use authorization"],
        "ai_training_approved":False
    }

def check_face_evidence(root,report):
    """Independent arithmetic reconciliation of pinned 1-4 results, not rerender."""
    old=json.loads((root/FINAL).read_text(encoding="utf-8"))
    ep2=json.loads((root/ENTRY2).read_text(encoding="utf-8"))
    supp=json.loads((root/SUPPORT).read_text(encoding="utf-8"))
    values=ep2["status_face_counts"]
    cnt=Counter()
    for group in values.values():
        cnt.update(group)
    face_total=sum(cnt.values())+ep2["unbound_faces"]["SLOT_UNBOUND"]+ep2["missing_png_face_instances"]
    supplemental=supp["pixel_support_counts"]
    linked=cnt["STATIC_RECT"]+cnt["ANIMATED_FRAME_RECTS"]+supp["supplemental_source_support_faces"]
    missing=(
        ep2["unbound_faces"]["SLOT_UNBOUND"]+
        ep2["missing_png_face_instances"]+
        supplemental["NO_PINNED_SPRITE_INTERSECTION"]
    )
    checks={
        "face_total":face_total,"ordinary_rect":cnt["STATIC_RECT"]+cnt["ANIMATED_FRAME_RECTS"],
        "supplemental":supp["supplemental_source_support_faces"],
        "sampled":linked,"unsupported":missing,
        "unsupported_unbound":ep2["unbound_faces"]["SLOT_UNBOUND"],
        "unsupported_missing_png":ep2["missing_png_face_instances"],
        "unsupported_no_intersection":supplemental["NO_PINNED_SPRITE_INTERSECTION"],
        "face_balance":linked+missing,
    }
    target={
        "face_total":592312,"ordinary_rect":511709,
        "supplemental":74260,"sampled":585969,"unsupported":6343,
        "unsupported_unbound":6202,"unsupported_missing_png":139,
        "unsupported_no_intersection":2,"face_balance":592312,
    }
    differences={k:{"actual":v,"expected":target[k]} for k,v in checks.items() if v!=target[k]}
    if old["uv"]["faces_with_original_pixel_support"]!=linked or old["uv"]["remaining_without_own_support"]!=missing:
        differences["exit_report"]={"reason":"Old exit report and independent sum differ"}
    report["face_evidence_reconciliation"]={
        "method":"independent_summation_of_saved_1_4_row_counts_not_redecode_of_all_face_pixels",
        "observed":checks,"expected":target,"differences":differences,
        "fraction_with_original_pixel_support":linked/592312,
        "unbound_child_binding_context":supp["unbound_face_contexts"],
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    for name in ("af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    rows,report=pixels_audit(args.root,args)
    check_face_evidence(args.root,report)
    out_csv=args.out/"INT2_1_4_2001_PNG_CHECKS.csv"
    with out_csv.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDNAMES,lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    report["per_png_evidence_sha256"]=hashlib.sha256(out_csv.read_bytes()).hexdigest()
    if (report["per_png_discrepancies"] or report["discrepancy_examples"] or
        report["face_evidence_reconciliation"]["differences"]):
        report["status"]="DISCREPANCY_REQUIRES_REVIEW"
    else:
        report["status"]="PASS_ORIGINAL_PNG_BYTES_CRC_RGBA_AND_FACE_COUNT_RECONCILIATION"
    (args.out/"INT2_1_4_SUMMARY.json").write_text(
        json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8"
    )
    print("INT2_1_4_RESULT_JSON:"+json.dumps(report,ensure_ascii=False,sort_keys=True))
    if report["status"]!="PASS_ORIGINAL_PNG_BYTES_CRC_RGBA_AND_FACE_COUNT_RECONCILIATION":
        raise SystemExit("INT-2 1-4 independent audit produced discrepancies")

if __name__=="__main__":
    main()
