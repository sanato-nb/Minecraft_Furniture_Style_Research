"""INT-3 semantic evidence layer: import ONLY anchored geometric and role claims.

Reads:
 * 1-3-C original PARTS.csv.gz (1,911 original provider elements, 45
   geometry-and-face-slot chair component role *candidates*);
 * 1-3-F SQLite normalized element and sampled part links;
 * INT-3 existing knowledge SQLite and scoped 1-5 finding handoff.

No texture file name is interpreted as a material, no 'style' tags inferred,
no chair-seat function treated as verified. Source rights remain unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

from .knowledge_db import F_DB, read_source_sqlite, stable_digest, open_knowledge

ROOT=Path(__file__).resolve().parents[2]
SCHEMA=Path(__file__).with_name("knowledge_semantics_schema.sql")
C_PARTS=Path("research/furniture_mods/phase_1-3/C/PARTS.csv.gz")
ROLE_SET=frozenset(("LEG_OR_LOWER_POST","SEAT_LAYER","BACKREST_ASSEMBLY","LOWER_FRAME"))
ROLE_AUDIT_STATUS="HYPOTHESIS_NEEDS_VISUAL_CONFIRMATION"
EXPECTED_GEOMETRY=1911
EXPECTED_ROLE_CANDIDATES=45
EXPECTED_REVIEW_FINDINGS=14

def vec(s):
    return tuple(Fraction(x) for x in s.split("|"))

def shape_axes(a,b):
    changes=tuple(y-x for x,y in zip(a,b))
    zero="".join(axis for axis,d in zip("xyz",changes) if d==0)
    reverse="".join(axis for axis,d in zip("xyz",changes) if d<0)
    volume=abs(changes[0]*changes[1]*changes[2])
    return zero,reverse,str(volume)

def source_part_rows(root):
    path=root/C_PARTS
    if not path.is_file():
        raise FileNotFoundError("Original 1-3-C part evidence missing: "+str(path))
    with gzip.open(path,"rt",encoding="utf-8-sig",newline="") as stream:
        records=list(csv.DictReader(stream))
    if len(records)!=EXPECTED_GEOMETRY:
        raise ValueError("Original C element population changed")
    keys={(r["source_key"],int(r["element_index"])) for r in records}
    if len(keys)!=EXPECTED_GEOMETRY:
        raise ValueError("Original C part evidence contains duplicated element identity")
    return records

def append_semantics(db,root,origin):
    # The base DB was built from independently source-checked ledgers in INT-3.
    if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok" or db.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Base integrated DB integrity failed")
    if db.execute("SELECT COUNT(*) FROM model_face_link").fetchone()[0]!=592312:
        raise ValueError("Full source-linked face census not present")
    if db.execute("SELECT COUNT(*) FROM ai_training_eligible_model").fetchone()[0]!=0:
        raise ValueError("Cannot automatically enrich already-approved training assets")
    if db.execute("SELECT COUNT(*) FROM candidate_finding").fetchone()[0]!=14:
        raise ValueError("Legacy review candidate count changed")
    if db.execute("SELECT COUNT(*) FROM geometry_element").fetchone()[0]!=1911:
        raise ValueError("Base geometry census changed")

    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    c_rows=source_part_rows(root)
    f_rows={(r["provider_key"],r["element_index"]):r
            for r in origin.execute("""
            SELECT provider_key,element_index,source_from,source_to,
                   part_candidate,part_evidence
            FROM element
            """)}
    if len(f_rows)!=1911:raise ValueError("1-3-F element ledger truncated")
    modelhash={r[0]:r[1] for r in db.execute("SELECT model_key,source_sha FROM model")}
    audit_disagreements=[]
    candidate_counts=Counter()
    primitives=Counter()
    for part in c_rows:
        key=part["source_key"],int(part["element_index"])
        expected=f_rows.get(key)
        if expected is None:
            raise ValueError("C element absent from F and knowledge DB: "+repr(key))
        candidate=part["candidate_part"]
        evidence=part["evidence"]
        if candidate!=expected["part_candidate"] or evidence!=expected["part_evidence"]:
            raise ValueError("1-3-C part claim diverges from independently audited F: "+repr(key))
        a,b=vec(expected["source_from"]),vec(expected["source_to"])
        zero,reverse,volume=shape_axes(a,b)
        c_size=vec(part["size"])
        c_center=vec(part["center"])
        if (len(c_size)!=3 or len(c_center)!=3 or
            any(abs(abs(y-x)-size)>Fraction(1,1000000)
                for x,y,size in zip(a,b,c_size)) or
            any(abs((x+y)/2-center)>Fraction(1,1000000)
                for x,y,center in zip(a,b,c_center))):
            raise ValueError("1-3-C element size or center differs from F source: "+repr(key))
        if candidate=="UNDETERMINED":
            if evidence!="GEOMETRY_ONLY":
                raise ValueError("Undetermined element must not claim a verified role")
            grade="MEASURED_GEOMETRY"
        else:
            if evidence!="GEOMETRY_AND_FACE_SLOTS" or candidate not in ROLE_SET:
                raise ValueError("Unknown or improperly evidenced C role: "+candidate)
            grade="ROLE_CANDIDATE_GEOMETRY_AND_SLOTS"
            candidate_counts[candidate]+=1
        db.execute("""INSERT INTO semantic_geometry(
            provider_key,element_index,source_geometry_type,source_size,source_center,
            source_texture_slots,primitive_zero_axes,primitive_reversed_axes,
            local_volume_model_units3,original_role_candidate,original_role_evidence,evidence_grade)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (key[0],key[1],part["geometry_type"],part["size"],part["center"],
             part["texture_slots"],zero,reverse,volume,candidate,evidence,grade))
        primitives[part["geometry_type"]]+=1
        if candidate!="UNDETERMINED":
            db.execute("""INSERT INTO part_role_candidate(
                 provider_key,element_index,role_label,role_basis,source_model_key,source_model_sha)
                 VALUES(?,?,?,?,?,?)""",
               (key[0],key[1],candidate,evidence,key[0],modelhash[key[0]]))
            db.execute("""INSERT INTO semantic_review_queue(
                 queue_id,review_kind,provider_key,element_index,request,evidence_source)
                 VALUES (?,?,?,?,?,?)""",
                ("ROLE:"+key[0]+":"+str(key[1]),"ELEMENT_ROLE_VISUAL",
                 key[0],key[1],"Check rendered geometry, occlusion and part role before accepting original "+candidate,
                 str(C_PARTS)))
    if sum(candidate_counts.values())!=EXPECTED_ROLE_CANDIDATES:
        raise ValueError("C role candidate census no longer equals 45")

    # The E->F sample-part semantics may apply to assembled category cases
    # rather than a globally reusable model role: keep that source context.
    legacy_samples=list(origin.execute("""
        SELECT id,category,state_id,assignment,bbox FROM sample ORDER BY id
    """))
    if len(legacy_samples)!=47:raise ValueError("1-3-E fixed mod case sample count changed")
    db.executemany("INSERT INTO historical_sample(sample_id,scope,state_id,assignment,bbox) VALUES(?,?,?,?,?)",
                   (tuple(x) for x in legacy_samples))
    original_sample_part=0
    role_words=Counter()
    for r in origin.execute("""
        SELECT sample_id,rule_index,provider_key,element_index,part_candidate,basis
        FROM sample_part ORDER BY sample_id,rule_index,provider_key,element_index
    """):
        db.execute("""INSERT INTO sample_part_candidate(
            sample_id,rule_index,provider_key,element_index,role_label,basis)
            VALUES(?,?,?,?,?,?)""",tuple(r))
        role_words[r["part_candidate"]]+=1
        original_sample_part+=1

    # Never promote 14 1-5 comparison candidates into a universal style rule.
    candidates=list(db.execute("""
       SELECT finding_id,classification,scope_limit,review_condition
       FROM comparison_finding WHERE disposition='CANDIDATE_REQUIRES_REVIEW'
       ORDER BY finding_id
    """))
    if len(candidates)!=EXPECTED_REVIEW_FINDINGS:
        raise ValueError("1-5 review candidate census changed")
    for fid,classification,lim,condition in candidates:
        if not lim.strip() or not condition.strip():
            raise ValueError("Unscoped comparison finding cannot become an AI style rule: "+fid)
        db.execute("""INSERT INTO semantic_review_queue(
          queue_id,review_kind,finding_id,request,evidence_source)
          VALUES(?,?,?,?,?)""",
          ("FINDING:"+fid,"FINDING_SCOPE_CONFIRMATION",fid,
           "Recheck specified case scope, counterexamples and conditions: "+condition,
           "research/furniture_mods/phase_1-5/E/PHASE2_HANDOFF.csv"))
    return {"geometry_by_source_type":dict(sorted(primitives.items())),
            "role_candidate_by_label":dict(sorted(candidate_counts.items())),
            "sample_role_claims_by_label":dict(sorted(role_words.items())),
            "source_historical_sample_part_rows":original_sample_part}

def inspect_semantics(db):
    db.execute("PRAGMA foreign_keys=ON")
    if db.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("Integrated semantic DB SQLite failed integrity_check")
    if db.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("Integrated semantic DB foreign-key violations")
    tables=("semantic_geometry","part_role_candidate","historical_sample",
            "sample_part_candidate","semantic_review_queue","verified_material_style")
    counts={name:db.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] for name in tables}
    if counts["semantic_geometry"]!=1911 or counts["part_role_candidate"]!=45:
        raise ValueError("Unjustified role annotation count differs from 45")
    if counts["historical_sample"]!=47 or counts["semantic_review_queue"]!=59:
        raise ValueError("Fixed source cases or constrained review queue differ")
    if counts["verified_material_style"]!=0:
        raise ValueError("Material/style semantics were auto-approved without visual proof")
    if db.execute("SELECT COUNT(*) FROM ai_approved_semantic_part").fetchone()[0]!=0:
        raise ValueError("Role candidates were incorrectly promoted to verified function")
    if db.execute("SELECT COUNT(*) FROM ai_training_eligible_model").fetchone()[0]!=0:
        raise ValueError("No third-party model may be auto-approved for training")
    if db.execute("SELECT COUNT(*) FROM candidate_role_review").fetchone()[0]!=45:
        raise ValueError("Role visual review queue is missing source model context")
    unknown=db.execute("""
        SELECT COUNT(*) FROM semantic_geometry
        WHERE original_role_candidate='UNDETERMINED'
          AND evidence_grade!='MEASURED_GEOMETRY'
    """).fetchone()[0]
    if unknown:raise ValueError("Geometry-only parts were spuriously labeled")
    conflicts=db.execute("""
        SELECT COUNT(*) FROM semantic_geometry g JOIN geometry_element e
        USING(provider_key,element_index)
        WHERE g.original_role_candidate!=e.part_candidate OR
              g.original_role_evidence!=e.part_evidence
    """).fetchone()[0]
    if conflicts:raise ValueError("Original source 1-3-C and 1-3-F claim provenance changed")
    review_status=dict(db.execute("SELECT review_kind,COUNT(*) FROM semantic_review_queue GROUP BY review_kind"))
    if review_status!={"ELEMENT_ROLE_VISUAL":45,"FINDING_SCOPE_CONFIRMATION":14}:
        raise ValueError("Incorrect independent visual review denominator")
    group_counts=dict(db.execute("""
         SELECT role_label,COUNT(*) FROM part_role_candidate GROUP BY role_label ORDER BY role_label
    """))
    return {
      "schema":"MCFR_INT3_SEMANTIC_EVIDENCE/v1",
      "status":"PASS_SOURCE_SCOPED_GEOMETRY_AND_ROLE_CANDIDATES",
      "counts":counts,
      "role_candidate_counts":group_counts,
      "geometry_only_elements":1911-45,
      "review_status":review_status,
      "role_candidates_visual_verified":0,
      "material_style_verified":0,
      "ai_training_eligible_models":0,
      "vetted_universal_style_rules":0,
      "scope_note":"Original geometric shapes and 45 chair-role hypotheses; no automatic semantic approval."
    }

SEMANTIC_DIGEST={
"semantic_geometry":["provider_key","element_index","source_geometry_type","source_size","original_role_candidate","original_role_evidence"],
"part_role_candidate":["provider_key","element_index","role_label","role_basis","source_model_sha","claim_status"],
"historical_sample":["sample_id","scope","state_id","assignment"],
"sample_part_candidate":["sample_id","rule_index","provider_key","element_index","role_label","basis"],
"semantic_review_queue":["queue_id","review_kind","provider_key","element_index","finding_id","state"],
}

def execute(root:Path,db_path:Path,output:Path):
    if not db_path.is_file():raise FileNotFoundError(str(db_path))
    with read_source_sqlite(root/F_DB) as f,sqlite3.connect(db_path) as db:
        db.row_factory=sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            observations=append_semantics(db,root,f)
            checks=inspect_semantics(db)
            digests={name:stable_digest(db,name,cols) for name,cols in SEMANTIC_DIGEST.items()}
            result={**checks,**observations,
                    "input_sha256":{
                      "1-3-C/PARTS.csv.gz":hashlib.sha256((root/C_PARTS).read_bytes()).hexdigest(),
                      "1-3-F/furniture_research.sqlite.xz":hashlib.sha256((root/F_DB).read_bytes()).hexdigest()
                    },
                    "logical_sha256":digests,
                    "human_review_approval_count":0,
                    "original_assets_redistributed":False}
            db.commit()
        except BaseException:
            db.rollback()
            raise
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def query(db_path:Path,provider_key:str,element_index:int):
    with open_knowledge(db_path) as db:
        rows=db.execute("""
          SELECT g.*,p.role_label,p.role_basis,p.claim_status
          FROM semantic_geometry g
          LEFT JOIN part_role_candidate p USING(provider_key,element_index)
          WHERE g.provider_key=? AND g.element_index=?""",(provider_key,element_index)).fetchall()
        if len(rows)!=1:raise LookupError("Unknown original model provider/element key")
        result=dict(rows[0])
        result["role_verified"]=False
        result["style_verified"]=False
        result["material_verified"]=False
        result["model_source"]=dict(db.execute("""
          SELECT source_id,resource_id,source_path,source_sha
          FROM model WHERE model_key=?""",(provider_key,)).fetchone())
        return result

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    build=sub.add_parser("extend")
    build.add_argument("--root",type=Path,default=ROOT)
    build.add_argument("--db",type=Path,required=True)
    build.add_argument("--out",type=Path,required=True)
    check=sub.add_parser("validate")
    check.add_argument("--db",type=Path,required=True)
    item=sub.add_parser("element")
    item.add_argument("--db",type=Path,required=True)
    item.add_argument("--provider",required=True)
    item.add_argument("--index",type=int,required=True)
    args=parser.parse_args(argv)
    if args.command=="extend":
        out=execute(args.root,args.db,args.out)
    elif args.command=="validate":
        with open_knowledge(args.db) as db:out=inspect_semantics(db)
    else:
        out=query(args.db,args.provider,args.index)
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
