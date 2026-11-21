"""INT-3 original-chair geometric visual evidence, without falsely approving semantics.

Four independently pinned 1-3-C chair-template providers are reconstructed
from the audited 1-3-F source coordinates, element rotations and pivots.
Outputs vector, *texture-free* projections: whole-model context (two angles)
and 45 individually highlighted candidate elements. Isometric diagrams
are useful for visual pre-screening, but NOT a Minecraft client render,
a material/style recognition pass or sufficient to approve a part function.

The script NEVER changes prior SQLite, PNG, JAR, or semantic review states.
No network, external Python dependencies, or original mod artwork included.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
from html import escape as xml_escape
import json
import math
from pathlib import Path
import sqlite3
import sys

from .knowledge_db import F_DB, read_source_sqlite
from .knowledge_semantics import C_PARTS, source_part_rows

ROOT=Path(__file__).resolve().parents[2]
TEMPLATES=(
    ("AF","another_furniture:block/template/chair","AF chair"),
    ("AF","another_furniture:block/template/chair_tucked","AF tucked chair"),
    ("HC","handcrafted:block/chair/chair","Handcrafted chair"),
    ("MACAW","mcwfurnitures:block/parent/chair","Macaw parent chair"),
)
ROLES={
    "LEG_OR_LOWER_POST":"#e19a3e",
    "SEAT_LAYER":"#2b9f98",
    "BACKREST_ASSEMBLY":"#707bdb",
    "LOWER_FRAME":"#ce6486",
}
FACE_INDICES=(
    (0,1,2,3),  # z=min
    (4,5,6,7),  # z=max
    (0,4,7,3),  # x=min
    (1,5,6,2),  # x=max
    (3,2,6,7),  # y=max
    (0,1,5,4),  # y=min
)
AZIMUTHS=(43,223)
ELEVATION=29

def coords(value):
    values=tuple(float(x) for x in value.split("|"))
    if len(values)!=3:raise ValueError("Invalid 3-D source vector")
    if any(not math.isfinite(x) for x in values):
        raise ValueError("Nonfinite original 3D source coordinate")
    return values

def rotate_point(point,pivot,axis,angle,rescale):
    if abs(angle)<1e-12:return point
    shift=[point[i]-pivot[i] for i in range(3)]
    indices={"x":(1,2),"y":(2,0),"z":(0,1)}[axis]
    i,j=indices
    a=math.radians(angle)
    cs=math.cos(a)
    sn=math.sin(a)
    if rescale:
        if abs(cs)<1e-7:raise ValueError("Unsupported rescale near 90 degrees")
        factor=1/cs
    else:factor=1.0
    shift[i],shift[j]=factor*(cs*shift[i]-sn*shift[j]),factor*(sn*shift[i]+cs*shift[j])
    return tuple(shift[k]+pivot[k] for k in range(3))

def corners(a,b):
    return (
        (a[0],a[1],a[2]),(b[0],a[1],a[2]),
        (b[0],b[1],a[2]),(a[0],b[1],a[2]),
        (a[0],a[1],b[2]),(b[0],a[1],b[2]),
        (b[0],b[1],b[2]),(a[0],b[1],b[2])
    )

def box_bounds(points):
    return tuple(min(p[axis] for p in points) for axis in range(3))+tuple(
        max(p[axis] for p in points) for axis in range(3))

def build_element(r):
    a=coords(r["source_from"])
    b=coords(r["source_to"])
    # The original C ledger leaves pivot empty when rotation is absent.
    pivot=coords(r["pivot"]) if r["pivot"].strip() else (8.0,8.0,8.0)
    angle=float(r["angle"])
    axis=r["axis"] or "y"
    rescale=bool(r["rescale"])
    vertices=tuple(rotate_point(p,pivot,axis,angle,rescale) for p in corners(a,b))
    recorded=tuple(float(n) for n in r["rotated_bbox"].split("|"))
    computed=box_bounds(vertices)
    if len(recorded)!=6 or any(abs(a-b)>0.00007 for a,b in zip(recorded,computed)):
        raise ValueError("Model element rotated AABB differs from audited C/F source: "
                         +str((r["provider_key"],r["element_index"],computed,recorded)))
    return {
       "provider":r["provider_key"],"index":int(r["element_index"]),
       "role":r["part_candidate"],"evidence":r["part_evidence"],
       "vertices":vertices,"bounds":computed,
       "axis":axis,"angle":angle,"pivot":pivot,"rescale":rescale
    }

def camera(azimuth,elevation=ELEVATION):
    a=math.radians(azimuth)
    b=math.radians(elevation)
    eye=(math.cos(b)*math.cos(a),math.sin(b),math.cos(b)*math.sin(a))
    right=(-math.sin(a),0.0,math.cos(a))
    up=(-math.sin(b)*math.cos(a),math.cos(b),-math.sin(b)*math.sin(a))
    return (eye,right,up)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def project(point,view):
    eye,right,up=view
    return (dot(point,right),dot(point,up),dot(point,eye))

def polygon_paths(elements,angle,selected=None):
    view=camera(angle)
    world=[p for e in elements for p in e["vertices"]]
    if not world:raise ValueError("Zero original elements in render")
    projections=[project(p,view) for p in world]
    minx,maxx=min(p[0] for p in projections),max(p[0] for p in projections)
    miny,maxy=min(p[1] for p in projections),max(p[1] for p in projections)
    span=max(maxx-minx,maxy-miny,1.0)
    polys=[]
    for e in elements:
        transformed=[project(p,view) for p in e["vertices"]]
        for faceidx,indices in enumerate(FACE_INDICES):
            pts=[transformed[i] for i in indices]
            a,b,c=pts[0],pts[1],pts[2]
            # Zero-area planes are diagnostic, not silently discarded.
            area=abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
            if area<1e-8:continue
            highlight=(selected is not None and e["index"]==selected)
            base=(ROLES.get(e["role"],"#9ca9b6") if selected is None
                  else ROLES.get(e["role"],"#dc8d36") if highlight else "#cbd5df")
            # Draw every face back-to-front, not an engine-accurate GPU render.
            shade=(1.0,0.94,0.81,0.76,1.14,0.67)[faceidx]
            polys.append((sum(p[2] for p in pts)/len(pts),e["index"],shade,base,
                          tuple(((x-(minx+maxx)/2)*460/span+260,
                                 ((miny+maxy)/2-y)*460/span+255) for x,y,z in pts),
                          highlight))
    polys.sort(key=lambda p:(p[0],p[1]))
    return polys

def shade(color,factor):
    r,g,b=[int(color[i:i+2],16) for i in (1,3,5)]
    v=[min(255,max(0,int(x*factor))) for x in (r,g,b)]
    return "#"+ "".join(f"{x:02x}" for x in v)

def svg_panel(elements,title,angle,selected=None,isolate=False):
    display=([e for e in elements if e["index"]==selected] if isolate else elements)
    if isolate and len(display)!=1:
        raise ValueError("Cannot isolate a missing or duplicate source element")
    poly=polygon_paths(display,angle,selected=selected)
    label=("WHOLE ASSEMBLY" if selected is None else
           f"ISOLATED e{selected} — NOT AN IN-GAME VIEW" if isolate else
           f"HIGHLIGHT e{selected}")
    text=[
      '<svg xmlns="http://www.w3.org/2000/svg" width="540" height="580" viewBox="0 0 540 580">',
      '<rect width="540" height="580" fill="#f8fafc"/>',
      '<rect x="14" y="66" width="512" height="482" rx="10" fill="#f0f4f8" stroke="#d8e2eb"/>',
      f'<text x="18" y="25" font-family="sans-serif" font-weight="bold" font-size="15" fill="#25394a">{xml_escape(title)}</text>',
      f'<text x="18" y="47" font-family="sans-serif" font-size="13" fill="#647589">VIEW {angle} deg | {label}</text>',
    ]
    # Consistently draw models in the central 540x540 square.
    for _,idx,factor,color,points,highlight in poly:
        pts=" ".join(f"{x:.3f},{y+67:.3f}" for x,y in points)
        text.append(f'<polygon points="{pts}" fill="{shade(color,factor)}" stroke="{"#4c5765" if highlight else "#8d9baa"}" stroke-width="{"1.7" if highlight else "0.65"}"/>')
    if selected is not None:
        chosen=[x for x in elements if x["index"]==selected]
        if len(chosen)!=1:raise ValueError("Selected source element not present")
        e=chosen[0]
        v=camera(angle)
        center=tuple(sum(p[i] for p in e["vertices"])/8 for i in range(3))
        # Convert same central fit to align highlighted label.
        # Visual legends identify selected index even when occluded.
        text.append(f'<text x="20" y="567" font-family="monospace" font-size="13" fill="#334155">e{selected} | {xml_escape(e["role"])} | {xml_escape(e["evidence"])}</text>')
    else:
        text.append(f'<text x="20" y="567" font-family="monospace" font-size="13" fill="#475569">{len(elements)} source elements (textures intentionally omitted)</text>')
    text.append("</svg>")
    return "\n".join(text)+"\n"

def svg_sheet(cards,title,cols=2):
    """Embed SVG panel XML as nested child <svg> nodes; no PNG dependencies."""
    rows=math.ceil(len(cards)/cols)
    width=cols*540
    height=rows*580+48
    parts=[
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
      '<rect width="100%" height="100%" fill="#fff"/>',
      f'<text x="16" y="30" font-family="sans-serif" font-weight="bold" font-size="20">{xml_escape(title)}</text>',
    ]
    for i,content in enumerate(cards):
        raw=content.strip()
        start=raw.find(">")
        close=raw.rfind("</svg>")
        if start<0 or close<0:raise ValueError("Malformed local SVG fragment")
        child=raw[start+1:close]
        x=(i%cols)*540
        y=(i//cols)*580+48
        parts.append(f'<g transform="translate({x},{y})">{child}</g>')
    parts.append("</svg>")
    return "\n".join(parts)+"\n"

def identity(db,source,resource):
    models=list(db.execute(
      "SELECT model_key,path,sha FROM model WHERE source_id=? AND resource_id=?",
      (source,resource)))
    if len(models)!=1:
        raise ValueError("Template original has no unique pinned model SHA: "+source+"/"+resource)
    return tuple(models[0])

def templates(db,candidates):
    records=[]
    for source,resource,title in TEMPLATES:
        key,path,sha=identity(db,source,resource)
        rows=list(db.execute("""
          SELECT provider_key,element_index,source_from,source_to,pivot,axis,angle,rescale,
                 rotated_bbox,part_candidate,part_evidence
          FROM element WHERE provider_key=? ORDER BY element_index""",(key,)))
        if not rows:raise ValueError("Chair provider contains no original elements "+key)
        geom=[build_element(r) for r in rows]
        chosen=[e for e in geom if e["role"]!="UNDETERMINED"]
        if any((key,e["index"]) not in candidates for e in chosen):
            raise ValueError("C source role claim absent from source candidate ledger")
        if any(candidates[(key,e["index"])]!=e["role"] for e in chosen):
            raise ValueError("Original 1-3-C candidate role disagrees with reconstructed model")
        records.append({"source":source,"resource":resource,"model_key":key,"path":path,
                        "sha":sha,"title":title,"elements":geom,"chosen":chosen})
    if len({e["model_key"] for e in records})!=4:raise ValueError("Duplicate role providers")
    if sum(len(r["chosen"]) for r in records)!=45:
        raise ValueError("Expected 45 source-traced candidate elements")
    return records

def write_file(out,relative,content):
    path=out/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(root,out):
    root=Path(root)
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    role_rows=[r for r in source_part_rows(root) if r["candidate_part"]!="UNDETERMINED"]
    candidates={(r["source_key"],int(r["element_index"])):r["candidate_part"]
                for r in role_rows}
    if len(candidates)!=45:
        raise ValueError("Unexpected duplicate original role candidates")
    # The 1-3-C evidence is immutable in this research snapshot; compare to
    # prior approved semantic summary rather than inventing a review decision.
    pinned=json.loads((root/"project/integration/INT3_SEMANTIC_SUMMARY.json").read_text(encoding="utf-8"))
    source_hash=hashlib.sha256((root/C_PARTS).read_bytes()).hexdigest()
    db_hash=hashlib.sha256((root/F_DB).read_bytes()).hexdigest()
    if (source_hash!=pinned["input_sha256"]["1-3-C/PARTS.csv.gz"] or
        db_hash!=pinned["input_sha256"]["1-3-F/furniture_research.sqlite.xz"]):
        raise ValueError("Source image review cannot use an unpinned 1-3-C/1-3-F snapshot")
    with read_source_sqlite(root/F_DB) as db:
        files={}
        records=templates(db,candidates)
        all_provider_keys={r["model_key"] for r in records}
        if set(k for k,i in candidates)!=all_provider_keys:
            raise ValueError("45 source candidates include a non-template provider")
        summary_rows=[]
        overall_cards=[]
        role_categories=Counter()
        geometries=Counter()
        for group in records:
            slug=group["source"].lower()+"_"+group["resource"].split("/")[-1].replace(":","_")
            assembly=[]
            for angle in AZIMUTHS:
                assembly.append(svg_panel(group["elements"],group["title"],angle))
            combined=svg_sheet(assembly,group["title"]+" — source geometry only")
            overview_name=f"overview/{slug}_both_angles.svg"
            files[overview_name]=write_file(out,overview_name,combined)
            overall_cards.extend(assembly)
            geometries["providers"]+=1
            geometries["all_provider_elements"]+=len(group["elements"])
            for e in group["chosen"]:
                role_categories[e["role"]]+=1
                panels=[svg_panel(group["elements"],group["title"],a,e["index"])
                        for a in AZIMUTHS]
                # Each chair has occluded parts. The third isolated view is
                # a diagnostic, not a valid assembled/game appearance.
                panels.append(svg_panel(group["elements"],group["title"],AZIMUTHS[0],
                                        e["index"],isolate=True))
                name=f"candidates/{slug}_element_{e['index']:03d}.svg"
                sha=write_file(out,name,svg_sheet(panels,
                         group["title"]+f" / e{e['index']} — {e['role']}",cols=3))
                files[name]=sha
                summary_rows.append({
                    "source":group["source"],"model_key":group["model_key"],
                    "source_path":group["path"],"source_model_sha":group["sha"],
                    "element_index":e["index"],"candidate_role":e["role"],
                    "candidate_basis":e["evidence"],
                    "bbox":"|".join(f"{v:.8g}" for v in e["bounds"]),
                    "original_rotation_axis":e["axis"],
                    "original_rotation_angle":e["angle"],
                    "svg_path":name,"svg_sha256":sha,
                    "view_angles":"|".join(map(str,AZIMUTHS)),
                    "isolated_element_diagnostic":"YES",
                    "render_method":"GEOMETRY_ONLY_ISOMETRIC_NO_TEXTURES",
                    "visual_human_verified":"NO",
                    "game_runtime_verified":"NO",
                    "decision":"PENDING_RENDERED_AND_IN_GAME_REVIEW",
                })
        files["overview/all_four_templates.svg"]=write_file(
           out,"overview/all_four_templates.svg",
           svg_sheet(overall_cards,"All four pinned original chair providers | 2 angles each",cols=2))
        if len(summary_rows)!=45:raise ValueError("Generated fewer than 45 candidate views")
        ledger_path=out/"review_45_source_element_views.csv"
        with ledger_path.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(summary_rows[0]))
            writer.writeheader()
            writer.writerows(sorted(summary_rows,key=lambda r:(r["source"],r["model_key"],r["element_index"])))
        files[ledger_path.name]=hashlib.sha256(ledger_path.read_bytes()).hexdigest()
        # Offline HTML gallery with explicit no-confirmation notices.
        html=[
          '<!doctype html><html lang="ko"><head><meta charset="utf-8">',
          '<meta name="viewport" content="width=device-width, initial-scale=1">',
          '<title>INT-3 가구 부품 45개 기하 투영 검수판</title>',
          '<style>body{font:14px system-ui,sans-serif;margin:24px auto;max-width:1320px;background:#f7f9fc;color:#203448;padding:0 16px}p{line-height:1.5}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}.card{background:#fff;border:1px solid #d9e2ec;border-radius:10px;padding:12px}img{width:100%;height:auto}small{color:#697a8c}a{color:#205da8}</style></head><body>',
          '<h1>INT-3: 45개 후보 가구 부품 기하 검수판</h1>',
          '<p>주의: 원본 모델 요소/회전/축으로 생성한 <b>진단용 입체 투영도</b>입니다. 원본 모드 PNG·실제 게임 렌더·조명·투명도·시각 검수 결과가 아닙니다. 전부 PENDING으로 남아 있습니다.</p>',
          '<p><a href="overview/all_four_templates.svg">네 모델 전체 조립 투영도</a> · <a href="review_45_source_element_views.csv">45건 원본 추적 CSV</a></p>',
          '<section class="cards">'
        ]
        for row in summary_rows:
            html.append(
              '<article class="card"><b>'+xml_escape(row["source"]+" e"+str(row["element_index"])+" · "+row["candidate_role"])+'</b>'
              '<p><small>'+xml_escape(row["model_key"])+'</small></p>'
              '<a href="'+xml_escape(row["svg_path"])+'"><img alt="Two diagnostic geometric projections" loading="lazy" src="'+xml_escape(row["svg_path"])+'"></a>'
              '<p><small>원본 SHA: '+xml_escape(row["source_model_sha"][:16])
              +'… | 승인: 없음</small></p></article>'
            )
        html.extend(['</section></body></html>'])
        files["review_45_gallery.html"]=write_file(out,"review_45_gallery.html","\n".join(html))
        summary={
           "schema":"MCFR_INT3_GEOMETRY_RENDER_REVIEW/v1",
           "status":"PASS_45_ORIGINAL_ELEMENTS_PROJECTED_FOR_REVIEW_NOT_VISUALLY_APPROVED",
           "sources":{
              "1-3-C_PARTS_gzip_sha256":source_hash,
              "1-3-F_sqlite_xz_sha256":db_hash,
              "previous_1-3-semantic_json_sha256":hashlib.sha256((root/"project/integration/INT3_SEMANTIC_SUMMARY.json").read_bytes()).hexdigest()
           },
           "model_source_keys":[{"source":r["source"],"resource_id":r["resource"],
                                 "model_key":r["model_key"],"sha":r["sha"],
                                 "all_elements":len(r["elements"]),
                                 "candidates":len(r["chosen"])} for r in records],
           "counts":{"template_providers":4,"source_candidate_elements":len(summary_rows),
                     "all_template_elements":geometries["all_provider_elements"],
                     "rendered_model_context_views":8,
                     "rendered_individual_candidate_views":len(summary_rows)*3,
                     "isolated_element_diagnostic_views":len(summary_rows),
                     "candidate_roles":dict(sorted(role_categories.items()))},
           "evidence_files_sha256":dict(sorted(files.items())),
           "visual_review":{"state":"PENDING","human_verified_elements":0,
                            "runtime_verified_elements":0,
                            "newly_approved_material_style_assertions":0,
                            "ai_training_model_approvals":0},
           "limitations":[
              "Projected six-sided element cuboids; no Minecraft model bake, culling or actual image textures",
              "Painter-style depth sorting approximates occlusion; not a physical or game renderer",
              "Every candidate adds a third isolated 3D view to expose parts hidden in assembled projections",
              "45 source labels remain hypotheses pending original textured render and actual visual confirmation",
              "No original JAR, JSON, PNG or images are redistributed",
              "Source model geometry identity is fixed to the 1-3-C/1-3-F input SHA256"
           ],
        }
        (out/"INT3_VISUAL_REVIEW_PREP_SUMMARY.json").write_text(
            json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return summary

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args(argv)
    result=run(args.root,args.out)
    print("INT3_VISUAL_REVIEW_RESULT:"+json.dumps(result,ensure_ascii=False,sort_keys=True))
    if result["counts"]["source_candidate_elements"]!=45:
        raise SystemExit("Only full candidate-source review bundle can pass")
    return 0

if __name__=="__main__":
    sys.exit(main())
