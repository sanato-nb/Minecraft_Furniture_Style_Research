"""INT-3 provenance-first Minecraft furniture knowledge integration.

Builds an intentionally *separate* SQLite sidecar from fixed audited source
ledgers: 1-3-F geometry/model/texture, 1-4-E UV PNG metadata and 1-5-E
comparison. It never modifies historical files or H2's operational database.

An independent INT-2 raw JSON replay (#26) has checked every one of the
592,312 links. This importer is not that replay: it materializes the audited
F relationships, reconstructs implied UV and classifies evidence. Audit
manifest and license NOT_REVIEWED remain attached; no training samples and
no original upstream model/PNG/JAR bytes are exported.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import json
import lzma
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = Path(__file__).with_name("knowledge_schema.sql")
F_DB = "research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz"
UV_DB = "research/furniture_mods/phase_1-4/entry04/research_texture_uv.sqlite.xz"
COMP_DB = "research/furniture_mods/phase_1-5/E/comparison.sqlite.xz"
AUDITS = {
    "FACES": ("project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json",
              "PASS_ALL_592312_FACE_LINKS_RECONSTRUCTED_FROM_ORIGINALS",
              "all 592312 static model faces rederived from pinned model JSON"),
    "GEOMETRY": ("project/integration/INT2_MOD_SOURCE_SUMMARY.json",
                 "PASS_SOURCE_GEOMETRY_CATALOG_SCOPE",
                 "all 16572 source model bodies and 9760 provider faces"),
    "PNG": ("project/integration/INT2_1_4_SUMMARY.json",
            "PASS_ORIGINAL_PNG_BYTES_CRC_RGBA_AND_FACE_COUNT_RECONCILIATION",
            "2001 pinned original PNGs independently RGBA redecoded"),
    "UV": ("project/integration/INT2_1_4_UV_REGIONS_SUMMARY.json",
           "PASS_ORIGINAL_UV_REGION_PIXEL_RECHECK",
           "29957 ordinary/animated UV region frame samples"),
    "SUPPLEMENT": ("project/integration/INT2_1_4_SUPPLEMENTAL_SUMMARY.json",
                   "PASS_SUPPLEMENTAL_SOURCE_AND_EXCEPTION_CONTEXT",
                   "1306 point-line-clip samples and 6202 slot exceptions"),
    "COMPARISON": ("project/integration/INT2_1_5_SUMMARY.json",
                   "PASS_PINNED_COMPARISON_21_CLAIMS_SOURCED_AND_REDERIVED",
                   "62 cases and 21 limited comparison findings"),
}
FACE_STATUSES={
 "STATIC_RECT":506614,"ANIMATED_FRAME_RECTS":5095,
 "ZERO_UV_AREA":69118,"OUTSIDE_TEXTURE_UV":5144,
 "SLOT_UNBOUND":6202,"MISSING_PINNED_PNG":139
}
FULL_TOTAL=592312
DEFAULT_AXES={"up":(0,2),"down":(0,2),"east":(2,1),"west":(2,1),
              "north":(0,1),"south":(0,1)}

def fraction(value: str | int | float) -> Fraction:
    return Fraction(str(value))

def coordinates(value: str) -> tuple[Fraction,...]:
    return tuple(fraction(x) for x in value.split("|"))

def pack(v) -> str:
    return "|".join(str(x) for x in v)

def implicit_uv(start,end,side):
    x,y,z=start
    X,Y,Z=end
    vectors={
      "down":(x,16-Z,X,16-z), "up":(x,z,X,Z),
      "north":(16-X,16-Y,16-x,16-y),
      "south":(x,16-Y,X,16-y),
      "west":(z,16-Y,Z,16-y),
      "east":(16-Z,16-Y,16-z,16-y),
    }
    return vectors[side]

def status(texture_id,uv,frames):
    if texture_id is None:return "SLOT_UNBOUND"
    if texture_id not in frames:return "MISSING_PINNED_PNG"
    if uv[0]==uv[2] or uv[1]==uv[3]:return "ZERO_UV_AREA"
    if any(x<0 or x>16 for x in uv):return "OUTSIDE_TEXTURE_UV"
    return "ANIMATED_FRAME_RECTS" if frames[texture_id][2]>1 else "STATIC_RECT"

def pixel_support(face_status,uv):
    if face_status=="SLOT_UNBOUND":return "SLOT_UNBOUND"
    if face_status=="MISSING_PINNED_PNG":return "SOURCE_PNG_MISSING"
    if face_status=="OUTSIDE_TEXTURE_UV":
        if (max(min(uv[0],uv[2]),0)>min(max(uv[0],uv[2]),16) or
            max(min(uv[1],uv[3]),0)>min(max(uv[1],uv[3]),16)):
            return "NO_SOURCE_INTERSECTION"
    return "SOURCE_REGION_REMEASURED"

def density(uv,rotation,direction,source_from,source_to,frame):
    axes=DEFAULT_AXES[direction]
    if rotation in (90,270):axes=axes[::-1]
    sizes=[abs(source_to[i]-source_from[i]) for i in axes]
    w,h,_=frame
    return (
      str(abs(uv[2]-uv[0])*w/16/sizes[0]) if sizes[0] else None,
      str(abs(uv[3]-uv[1])*h/16/sizes[1]) if sizes[1] else None
    )

def read_source_sqlite(path:Path):
    if not path.is_file():raise FileNotFoundError(f"Required audited database absent: {path}")
    body=lzma.decompress(path.read_bytes())
    conn=sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.deserialize(body)
    if conn.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("Upstream SQLite integrity check failed: "+str(path))
    if conn.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Upstream SQLite FK check failed: "+str(path))
    conn.row_factory=sqlite3.Row
    return conn

def audit_manifests(root):
    record={}
    for name,(path,expected,note) in AUDITS.items():
        raw=(root/path).read_bytes()
        doc=json.loads(raw)
        if doc.get("status")!=expected:
            raise ValueError(f"INT-3 input audit {name} is NOT in the approved static scope: {doc.get('status')}")
        if doc.get("ai_training_approved") is True:
            raise ValueError("A source audit unexpectedly declares training approval; review manually")
        record[name]={"path":path,"sha256":hashlib.sha256(raw).hexdigest(),
                      "status":expected,"note":note,"doc":doc}
    faces=record["FACES"]["doc"]
    if faces["observed"]["reconstructed_faces"]!=FULL_TOTAL or not all(faces["assertions"].values()):
        raise ValueError("Source-to-face independent replay is not complete")
    if record["COMPARISON"]["doc"]["observed"]["findings_rederived_from_B_measurements"]!=21:
        raise ValueError("21 comparison findings not independently verified")
    if record["PNG"]["doc"]["source_file_metrics"]["png_full_record_matches"]!=2001:
        raise ValueError("Original PNG evidence mismatch")
    if record["UV"]["doc"]["observed"]["frame_regions_matching"]!=29957:
        raise ValueError("Original ordinary UV crop evidence mismatch")
    if record["SUPPLEMENT"]["doc"]["source_support"]["region_rows_with_full_metrics_matched"]!=1306:
        raise ValueError("Supplemental UV crop evidence mismatch")
    return record

def load_model_registry(out,origin):
    source_rows=[tuple(r) for r in origin.execute(
        "SELECT id,version,minecraft,origin,pin_kind,pin,asset_hash_kind FROM source ORDER BY id")]
    if len(source_rows)!=5:raise ValueError("Pinned source release census differs")
    out.executemany("""
      INSERT INTO source_release(source_id,version,minecraft_version,origin,pin_kind,pin_digest,asset_hash_kind)
      VALUES (?,?,?,?,?,?,?)""",source_rows)
    models=origin.execute("""
      SELECT m.model_key,m.source_id,m.resource_id,m.path,m.sha,m.kind,m.static_grade,
             g.provider_key,COALESCE(g.terminal_status,'AUXILIARY_PARENT'),
             COALESCE(g.terminal_resource,''),COALESCE(g.element_instances,0),
             COALESCE(g.face_instances,0)
      FROM model m LEFT JOIN geometry g USING(model_key) ORDER BY m.model_key
    """)
    out.executemany("""
      INSERT INTO model(model_key,source_id,resource_id,source_path,source_sha,
       model_kind,static_grade,provider_key,terminal_status,terminal_resource,
       effective_elements,effective_faces,audit_evidence_id)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?, 'FACES')""",(tuple(row) for row in models))
    out.executemany("INSERT INTO model_parent VALUES (?,?,?)",
        (tuple(r) for r in origin.execute(
            "SELECT model_key,position,ancestor_key FROM lineage ORDER BY model_key,position")))
    out.executemany("INSERT INTO geometry_element VALUES (?,?,?,?,?,?,?,?,?)",
        (tuple(r) for r in origin.execute("""
          SELECT provider_key,element_index,source_from,source_to,rotated_bbox,
                 angle,axis,part_candidate,part_evidence
          FROM element ORDER BY provider_key,element_index""")))
    out.executemany("INSERT INTO provider_face VALUES (?,?,?,?,?,?,?,?,?)",
        (tuple(r) for r in origin.execute("""
          SELECT provider_key,element_index,direction,slot,uv,uv_declared,
                 uv_rotation,cullface,tintindex
          FROM face ORDER BY provider_key,element_index,direction""")))
    return {"source_releases":len(source_rows)}

def load_textures(out,original,uv_source):
    f_textures={r["id"]:r for r in original.execute("SELECT * FROM texture")}
    uv_textures={r["id"]:r for r in uv_source.execute("SELECT * FROM texture")}
    uvmeta={r["texture_id"]:(r["frame_width"],r["frame_height"],r["frame_count"])
            for r in uv_source.execute("SELECT * FROM texture_uv_counts")}
    if len(f_textures)!=2256 or len(uv_textures)!=2256 or len(uvmeta)!=2171:
        raise ValueError("1-4 texture identity/UV census changed")
    for tid,r in f_textures.items():
        second=uv_textures[tid]
        if (r["resource_id"],r["minecraft"])!=(second["resource_id"],second["minecraft"]):
            raise ValueError(f"1-3 and 1-4 texture identity mismatch: {tid}")
        disposition=second["disposition"]
        evidence=("ORIGINAL_PNG_REDECODED" if disposition=="PNG_UV_CANDIDATE"
                  else "HISTORIC_RGBA_SNAPSHOT" if disposition=="PRIOR_RGBA_SHA_MATCH"
                  else "SOURCE_MISSING" if disposition=="SOURCE_EXCEPTION"
                  else "DECLARED_ONLY" if disposition=="DECLARED_SLOT_ONLY"
                  else None)
        if evidence is None:raise ValueError("Unknown texture disposition: "+disposition)
        if tid in uvmeta and evidence in ("DECLARED_ONLY","SOURCE_MISSING"):
            raise ValueError("Unexpected UV region for unavailable source PNG")
        meta=uvmeta.get(tid,(None,None,None))
        out.execute("""
          INSERT INTO texture(texture_id,resource_id,minecraft_version,source_id,source_path,
             source_sha,texture_status,disposition,frame_width,frame_height,frame_count,
             pixel_evidence,audit_evidence_id)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (tid,r["resource_id"],r["minecraft"],r["source_id"],r["path"],r["sha"],
           r["texture_status"],disposition,*meta,evidence,"PNG"))
    out.executemany("INSERT INTO model_slot VALUES(?,?,?,?,?)",
       (tuple(r) for r in original.execute("""
          SELECT model_key,slot,texture_id,resolution,face_count
          FROM model_slot ORDER BY model_key,slot
       """)))
    return uvmeta

FACE_SQL="""
 SELECT link.model_key,link.provider_key,link.element_index,link.direction,
        link.slot,link.texture_id,link.uv,link.uv_declared,link.uv_rotation,
        def.cullface,def.tintindex,part.source_from,part.source_to
 FROM effective_face_texture AS link
 JOIN face AS def USING(provider_key,element_index,direction)
 JOIN element AS part USING(provider_key,element_index)
 ORDER BY link.model_key,link.provider_key,link.element_index,link.direction
"""

def insert_faces(out,origin,uvmeta):
    results=Counter()
    batch=[]
    for raw in origin.execute(FACE_SQL):
        model,provider,index,direction,slot,tid,declared_uv,is_declared,rotation,cull,tint,from_s,to_s=raw
        start,end=coordinates(from_s),coordinates(to_s)
        uv=coordinates(declared_uv) if is_declared else implicit_uv(start,end,direction)
        reason=status(tid,uv,uvmeta)
        pixel=pixel_support(reason,uv)
        du=dv=None
        if tid is not None and tid in uvmeta:
            du,dv=density(uv,rotation,direction,start,end,uvmeta[tid])
        batch.append((model,provider,index,direction,tid,slot,pack(uv),
          "EXPLICIT" if is_declared else "DEFAULT",rotation,cull,tint,du,dv,
          reason,pixel))
        results[reason]+=1
        results["faces"]+=1
        results["pixel_support_"+pixel]+=1
        if len(batch)>=10000:
            out.executemany("""INSERT INTO model_face_link VALUES(
                 ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",batch)
            batch.clear()
    if batch:
        out.executemany("""INSERT INTO model_face_link VALUES(
                 ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",batch)
    return dict(results)

def source_asset_to_model_map(original,comparison):
    lookup={(r["source_id"],r["path"]):r["model_key"] for r in
            original.execute("SELECT model_key,source_id,path FROM model")}
    result={}
    for r in comparison.execute("SELECT asset_id,source_scope,minecraft,path FROM asset WHERE kind='MODEL'"):
        source=r["source_scope"]
        mc=r["minecraft"]
        mapped="MC"+mc if source=="VANILLA" else source
        result[r["asset_id"]]=lookup.get((mapped,r["path"]))
    return result

def comparison_knowledge(out,original,comparison):
    out.executemany("INSERT INTO study_case(case_id,cohort,minecraft_version,block,bbox) VALUES (?,?,?,?,?)",
        (tuple(r) for r in comparison.execute("""
            SELECT case_id,cohort,minecraft,block,bbox FROM study_case ORDER BY case_id
        """)))
    links=source_asset_to_model_map(original,comparison)
    application_links=Counter()
    applications=comparison.execute("""
      SELECT a.case_id,a.rule_index,a.option_index,a.x,a.y,a.uvlock,
             ms.asset_id AS model_asset,ps.asset_id AS provider_asset
      FROM application a
      LEFT JOIN application_source ms ON ms.case_id=a.case_id
           AND ms.rule_index=a.rule_index AND ms.option_index=a.option_index AND ms.role='model'
      LEFT JOIN application_source ps ON ps.case_id=a.case_id
           AND ps.rule_index=a.rule_index AND ps.option_index=a.option_index AND ps.role='provider'
      ORDER BY a.case_id,a.rule_index,a.option_index
    """)
    for r in applications:
        model_id=links.get(r["model_asset"])
        provider_id=links.get(r["provider_asset"])
        linked=model_id is not None
        application_links["MODEL_LINKED" if linked else "UNMATCHED_SCOPE"]+=1
        out.execute("INSERT INTO case_application VALUES(?,?,?,?,?,?,?,?,?,?,?)",
          (r["case_id"],r["rule_index"],r["option_index"],r["model_asset"],
           model_id,r["provider_asset"],provider_id,r["x"],r["y"],r["uvlock"],
           "MODEL_LINKED" if linked else "UNMATCHED_SCOPE"))
    for r in comparison.execute("""
      SELECT f.finding_id,f.category,f.classification,f.axis,f.measurement,
             f.observation,f.scope_limit,h.disposition,h.review_condition
      FROM finding f JOIN phase2_handoff h USING(finding_id) ORDER BY finding_id
    """):
        json.loads(r["measurement"])
        out.execute("INSERT INTO comparison_finding VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (*tuple(r),"COMPARISON"))
    out.executemany("INSERT INTO finding_case VALUES(?,?)",
         (tuple(r) for r in comparison.execute(
             "SELECT finding_id,case_id FROM finding_case ORDER BY finding_id,case_id")))
    out.executemany("INSERT INTO runtime_condition(finding_id,test_id) VALUES(?,?)",
         (tuple(r) for r in comparison.execute(
             "SELECT finding_id,test_id FROM handoff_runtime ORDER BY finding_id,test_id")))
    out.executemany("INSERT INTO evidence_exception VALUES(?,?,?,?,?)",(
        ("PARENT_MISSING",r["model_key"],r["declared_parent"],
         int(r["direct_state_option"]), "1-5-E.parent_exception")
        for r in comparison.execute("SELECT * FROM parent_exception ORDER BY model_key")))
    out.executemany("INSERT INTO evidence_exception VALUES(?,?,?,?,?)",(
        ("STATE_OPTION",f'{r["state_id"]}|{r["rule_index"]}|{r["option_index"]}',r["finding"],
         None,"1-5-E.state_exception")
        for r in comparison.execute("SELECT * FROM state_exception ORDER BY state_id,rule_index,option_index")))
    out.executemany("INSERT INTO evidence_exception VALUES(?,?,?,?,?)",(
        ("TEXTURE",str(r["texture_id"]),r["finding"],
         r["face_instances"],"1-5-E.texture_exception")
        for r in comparison.execute("SELECT * FROM texture_exception ORDER BY texture_id")))
    return dict(application_links)

def count(out,table):
    return out.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

def inspect(db):
    db.execute("PRAGMA foreign_keys=ON")
    if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("INT-3 knowledge database integrity check failed")
    fk=db.execute("PRAGMA foreign_key_check").fetchall()
    if fk:raise ValueError("INT-3 foreign key violations: "+repr(fk[:5]))
    tables=(
      "source_release","evidence_manifest","knowledge_provenance","model",
      "model_parent","geometry_element","provider_face","texture","model_slot",
      "model_face_link","study_case","case_application","comparison_finding",
      "finding_case","runtime_condition","evidence_exception")
    counts={name:count(db,name) for name in tables}
    checks={"source_release":5,"evidence_manifest":6,"model":16579,
            "geometry_element":1911,"provider_face":9760,"texture":2256,
            "model_slot":81641,"model_face_link":FULL_TOTAL,"study_case":62,
            "case_application":74,"comparison_finding":21,"finding_case":70,
            "runtime_condition":16,"evidence_exception":139}
    for key,expected in checks.items():
        if counts[key]!=expected:
            raise ValueError(f"INT-3 {key} row count {counts[key]} differs from {expected}")
    source_counts=dict(db.execute("SELECT source_id,COUNT(*) FROM model GROUP BY source_id"))
    kind_counts=dict(db.execute("SELECT face_status,COUNT(*) FROM model_face_link GROUP BY face_status"))
    if kind_counts!=FACE_STATUSES:
        raise ValueError("Historical and integrated 592312 face status counts differ")
    support=dict(db.execute("SELECT pixel_support,COUNT(*) FROM model_face_link GROUP BY pixel_support"))
    if support!={"SOURCE_REGION_REMEASURED":585969,
                "SLOT_UNBOUND":6202,"SOURCE_PNG_MISSING":139,"NO_SOURCE_INTERSECTION":2}:
        raise ValueError("Independent source region and reference coverage disagree: "+str(support))
    handoff=dict(db.execute("SELECT disposition,COUNT(*) FROM comparison_finding GROUP BY disposition"))
    if handoff!={"CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7}:
        raise ValueError("Scope limits were dropped or elevated")
    rights=db.execute("""SELECT COUNT(*) FROM source_release WHERE license_review!='NOT_REVIEWED'
                         OR training_approved!=0 OR redistribution_approved!=0""").fetchone()[0]
    if rights:raise ValueError("AI training rights must not be implicitly cleared")
    if count(db,"ai_training_eligible_model")!=0:
        raise ValueError("Potential copyright-sensitive model unexpectedly training-eligible")
    mismatches=db.execute("""
      SELECT m.model_key,m.effective_faces,COUNT(f.direction) FROM model m
      LEFT JOIN model_face_link f ON f.model_key=m.model_key
      WHERE m.source_id IN ('AF','HC','MACAW')
      GROUP BY m.model_key HAVING COUNT(f.direction)!=m.effective_faces
      LIMIT 3
    """).fetchall()
    if mismatches:raise ValueError("Model-to-face declared counts differ: "+str(mismatches))
    bad_slots=db.execute("""
      SELECT COUNT(*) FROM model_face_link f LEFT JOIN model_slot s
       ON s.model_key=f.model_key AND s.slot=f.source_slot
      WHERE s.slot IS NULL OR COALESCE(s.texture_id,-1)!=COALESCE(f.texture_id,-1)
    """).fetchone()[0]
    if bad_slots:raise ValueError("Integrated face model-slot binding mismatch count "+str(bad_slots))
    failed_templates=db.execute("""
      SELECT COUNT(*) FROM comparison_finding WHERE
       (classification='UNVERIFIED_OR_COUNTEREXAMPLE' AND disposition!='SCOPE_LIMIT_ONLY')
       OR (classification!='UNVERIFIED_OR_COUNTEREXAMPLE' AND disposition!='CANDIDATE_REQUIRES_REVIEW')
    """).fetchone()[0]
    if failed_templates:raise ValueError("Comparison counterexamples lost scope limits")
    return {
        "schema":"MCFR_INT3_KNOWLEDGE_INTEGRATION/v1",
        "status":"PASS_FIXED_SCOPE_SOURCE_LINKS_AND_RESEARCH_INTEGRATION",
        "table_counts":counts,
        "model_by_source":source_counts,
        "face_status":kind_counts,
        "face_pixel_support":support,
        "comparison_disposition":handoff,
        "ai_training_eligible_models":0,
        "runtime_rechecks_in_int3":0,
        "rights_approval_count":0,
        "historical_sources_overwritten":False,
        "scope_limit":"Audited static evidence, NOT game runtime or licensed model training permission"
    }

def stable_digest(db,table,columns):
    """Digest complete logical rows, not SQLite pages/file timestamps."""
    hash=hashlib.sha256()
    fields=",".join(columns)
    keys=",".join(str(i+1) for i in range(len(columns)))
    for row in db.execute(f"SELECT {fields} FROM {table} ORDER BY {keys}"):
        hash.update(json.dumps(list(row),ensure_ascii=False,separators=(",",":")).encode())
        hash.update(b"\n")
    return hash.hexdigest()

def build(root:Path,out:Path,force:bool=False):
    if out.exists() and not force:
        raise FileExistsError("Existing knowledge DB is protected. Use --force for explicit replacement.")
    audits=audit_manifests(root)
    origin=read_source_sqlite(root/F_DB)
    uv=read_source_sqlite(root/UV_DB)
    compare=read_source_sqlite(root/COMP_DB)
    out.parent.mkdir(parents=True,exist_ok=True)
    temporary=out.with_suffix(out.suffix+".int3tmp")
    if temporary.exists():
        raise FileExistsError("Temporary knowledge DB already exists: "+str(temporary))
    db=sqlite3.connect(temporary)
    try:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript(SCHEMA.read_text(encoding="utf-8"))
        for name,item in audits.items():
            db.execute("INSERT INTO evidence_manifest VALUES(?,?,?,?,?,?)",
                       (name,item["path"],item["sha256"],item["status"],
                        "INDEPENDENT_RAW_ORIGINAL_AUDIT" if name in ("FACES","GEOMETRY","PNG","UV","SUPPLEMENT")
                        else "INDEPENDENT_COMPARISON_REDERIVATION",item["note"]))
        for family,table,key,audit,confidence in [
            ("model","1-3-F.model + geometry","source_id/path SHA -> model_key","FACES","STATIC_ORIGINAL_REPLAY_VERIFIED"),
            ("face","1-3-F.effective_face_texture + original 1-4 UV","model/provider/element/direction","FACES","STATIC_ORIGINAL_REPLAY_VERIFIED"),
            ("texture","1-3-F.texture + 1-4-E.texture_uv_counts","resource_id/minecraft version","PNG","PIXEL_SOURCE_REGION_REMEASURED"),
            ("finding","1-5-E.finding + phase2_handoff","finding_id and case ID","COMPARISON","COMPARISON_SAMPLE_REDERIVED"),
            ("runtime","1-5-E.runtime_check + handoff_runtime","test ID","COMPARISON","HISTORIC_RUNTIME_ONLY"),
            ("exception","1-5-E parent/state/texture exception","typed source key","SUPPLEMENT","UNRESOLVED_EXCEPTION"),
        ]:
            db.execute("INSERT INTO knowledge_provenance VALUES(?,?,?,?,?)",
                       (family,table,key,audit,confidence))
        load_model_registry(db,origin)
        uvmeta=load_textures(db,origin,uv)
        face_summary=insert_faces(db,origin,uvmeta)
        application_links=comparison_knowledge(db,origin,compare)
        db.commit()
        report=inspect(db)
        report["source_input_hashes"]={
          source:hashlib.sha256((root/path).read_bytes()).hexdigest()
          for source,path in [("1-3-F",F_DB),("1-4-E",UV_DB),("1-5-E",COMP_DB)]
        }
        report["independent_audit_manifests"]={
          k:{"path":v["path"],"sha256":v["sha256"],"status":v["status"]}
          for k,v in audits.items()
        }
        report["case_source_model_links"]=application_links
        report["computed_face_counts"]=face_summary
        report["logical_sha256"]={
          "model":stable_digest(db,"model",["model_key","source_id","resource_id","source_sha","provider_key","terminal_status","effective_faces"]),
          "texture":stable_digest(db,"texture",["texture_id","resource_id","minecraft_version","disposition","pixel_evidence"]),
          "model_face_link":stable_digest(db,"model_face_link",["model_key","provider_key","element_index","direction","texture_id","source_slot","uv","face_status","pixel_support"]),
          "comparison_finding":stable_digest(db,"comparison_finding",["finding_id","classification","measurement_json","scope_limit","disposition","review_condition"]),
        }
        db.execute("PRAGMA optimize")
        db.commit()
        db.close()
        if out.exists() and force:
            out.unlink()
        os.replace(temporary,out)
        report["output_db_bytes"]=out.stat().st_size
        return report
    except Exception:
        db.close()
        temporary.unlink(missing_ok=True)
        raise
    finally:
        origin.close()
        uv.close()
        compare.close()

def open_knowledge(file):
    if not file.is_file():raise FileNotFoundError(str(file))
    conn=sqlite3.connect(f"file:{file.resolve()}?mode=ro",uri=True)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def print_model(conn,identity):
    row=conn.execute("""
      SELECT m.*,s.version,s.minecraft_version,s.license_review,s.training_approved
      FROM model m JOIN source_release s USING(source_id)
      WHERE m.model_key=? OR m.resource_id=?
      ORDER BY m.model_key LIMIT 1""",(identity,identity)).fetchone()
    if row is None:raise LookupError("No fixed research model: "+identity)
    data=dict(row)
    data["face_status_counts"]=dict(conn.execute("""
      SELECT face_status,COUNT(*) FROM model_face_link
      WHERE model_key=? GROUP BY face_status""",(data["model_key"],)))
    data["slot_examples"]=[dict(x) for x in conn.execute("""
      SELECT slot,texture_id,resolution,face_count FROM model_slot WHERE model_key=?
      AND face_count>0 ORDER BY face_count DESC,slot LIMIT 12""",(data["model_key"],))]
    return data

def print_finding(conn,identity):
    r=conn.execute("SELECT * FROM comparison_finding WHERE finding_id=?",(identity,)).fetchone()
    if r is None:raise LookupError("No fixed finding: "+identity)
    data=dict(r)
    data["measurement_json"]=json.loads(data["measurement_json"])
    data["cases"]=[x[0] for x in conn.execute("""
      SELECT case_id FROM finding_case WHERE finding_id=? ORDER BY case_id""",(identity,))]
    data["runtime_checks"]=[x[0] for x in conn.execute("""
      SELECT test_id FROM runtime_condition WHERE finding_id=? ORDER BY test_id""",(identity,))]
    data["ai_training_approved"]=False
    return data

def main(argv=None):
    cli=argparse.ArgumentParser(description=__doc__)
    sub=cli.add_subparsers(dest="command",required=True)
    b=sub.add_parser("build")
    b.add_argument("--root",type=Path,default=ROOT)
    b.add_argument("--out",type=Path,required=True)
    b.add_argument("--report",type=Path)
    b.add_argument("--force",action="store_true")
    for name in ("summary","model","finding","validate"):
        p=sub.add_parser(name)
        p.add_argument("--db",type=Path,required=True)
        if name in ("model","finding"):p.add_argument("--id",required=True)
    opts=cli.parse_args(argv)
    if opts.command=="build":
        result=build(opts.root,opts.out,opts.force)
        if opts.report:
            opts.report.parent.mkdir(parents=True,exist_ok=True)
            opts.report.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    else:
        with open_knowledge(opts.db) as db:
            if opts.command=="model":result=print_model(db,opts.id)
            elif opts.command=="finding":result=print_finding(db,opts.id)
            else:
                result=inspect(db)
                if opts.command=="summary":
                    result["source_releases"]=[dict(x) for x in db.execute(
                       "SELECT source_id,version,minecraft_version,license_review,training_approved FROM source_release ORDER BY source_id")]
    print(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False))
    return 0

if __name__=="__main__":
    sys.exit(main())
