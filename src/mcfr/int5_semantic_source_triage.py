"""INT-5-A independently recheck 45 role hypotheses, 94 sample-part claims,
and 21 comparison findings. Measured geometry is NOT observed function/meaning.

Runs from the original pinned 1-3-C/F source, not filenames or aesthetic guesses.
Produces structured candidate/exception rows; no role, style or rights approval.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

from .knowledge_db import F_DB, read_source_sqlite
from .knowledge_semantics import C_PARTS, source_part_rows
from .semantic_visual_evidence import build_element, TEMPLATES

ROOT = Path(__file__).resolve().parents[2]
DEST = Path("project/integration")
SEMANTIC_SUMMARY = DEST / "INT3_SEMANTIC_SUMMARY.json"
VISUAL_SUMMARY = DEST / "INT3_VISUAL_REVIEW_PREP_SUMMARY.json"
SCOPED_EXIT = DEST / "INT4_H03_H05_MODELING_SCOPED_EXIT_V1.json"
FINDING_SOURCE = DEST / "INT2_1_5_21_FINDING_CHECKS.csv"
FINDING_LIMITS = Path("research/furniture_mods/phase_1-5/E/PHASE2_HANDOFF.csv")

OUTPUTS = {
    "parts": DEST / "INT5_A_45_ELEMENT_GEOMETRY_ROLE_REVIEW_V1.csv",
    "samples": DEST / "INT5_A_94_SAMPLE_ROLE_PROVENANCE_V1.csv",
    "findings": DEST / "INT5_A_21_FINDING_SCOPE_REVIEW_V1.csv",
    "summary": DEST / "INT5_A_EVIDENCE_TRIAGE_SUMMARY_V1.json",
}
EXPECTED_BLOBS = {
    SEMANTIC_SUMMARY.as_posix(): "8add16f7a01c8f8fa09176851927a0c76532e606",
    FINDING_SOURCE.as_posix(): "5b05951f9f20509df1ad17e78cabb06e8137b22f",
    FINDING_LIMITS.as_posix(): "466d5abcd56c93d397fbe5b51223e2dfb6d026db",
}
ROLE_COUNTS = {"LEG_OR_LOWER_POST": 16, "BACKREST_ASSEMBLY": 16,
               "LOWER_FRAME": 7, "SEAT_LAYER": 6}


def require(condition, label):
    if not condition:
        raise ValueError("INT5-A fail closed: " + label)


def blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()


def parse_csv(payload):
    result = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
    require(result, "empty original CSV")
    return result


def fixed_sources(root):
    for path, expected in EXPECTED_BLOBS.items():
        actual = blob_sha((root / path).read_bytes())
        require(actual == expected, "original Git blob changed: " + path)
    semantic = json.loads((root / SEMANTIC_SUMMARY).read_text(encoding="utf-8"))
    visual = json.loads((root / VISUAL_SUMMARY).read_text(encoding="utf-8"))
    scoped = json.loads((root / SCOPED_EXIT).read_text(encoding="utf-8"))
    require(semantic["counts"] == {
        "historical_sample": 47, "part_role_candidate": 45,
        "sample_part_candidate": 94, "semantic_geometry": 1911,
        "semantic_review_queue": 59, "verified_material_style": 0,
    }, "pre-existing semantic fixed population changed")
    require(semantic["role_candidate_by_label"] == ROLE_COUNTS and
            semantic["role_candidates_visual_verified"] == 0 and
            semantic["ai_training_eligible_models"] == 0,
            "historical roles were improperly approved")
    require(visual["visual_review"] == {
        "ai_training_model_approvals": 0, "human_verified_elements": 0,
        "newly_approved_material_style_assertions": 0,
        "runtime_verified_elements": 0, "state": "PENDING",
    }, "geometric diagnostic pictures were presented as an actual game review")
    require(scoped["modeling_case_count"] == 70 and
            scoped["modeling_H03"] == "PASS_SCOPED_MODEL_RENDER_EVIDENCE" and
            scoped["modeling_H05"] == "PASS_SCOPED_HISTORICAL_PROVENANCE" and
            scoped["original_strict_H03"] == "HOLD" and
            scoped["original_strict_H05"] == "CONDITIONAL" and
            scoped["INT5_semantics_approved"] == 0,
            "INT4 model-only handoff cannot be promoted to INT5 semantics")
    require(hashlib.sha256((root / C_PARTS).read_bytes()).hexdigest() ==
            semantic["input_sha256"]["1-3-C/PARTS.csv.gz"],
            "source 1-3-C parts bytes changed")
    require(hashlib.sha256((root / F_DB).read_bytes()).hexdigest() ==
            semantic["input_sha256"]["1-3-F/furniture_research.sqlite.xz"],
            "source 1-3-F SQLite compressed bytes changed")
    return semantic, visual, scoped


def shape_rows(root):
    original = source_part_rows(root)
    require(len(original) == 1911, "C geometry census is not 1911")
    source_by = {(r["source_key"], int(r["element_index"])): r for r in original}
    require(len(source_by) == 1911, "C keys duplicated")
    c_roles = {k: x for k,x in source_by.items()
               if x["candidate_part"] != "UNDETERMINED"}
    require(len(c_roles) == 45, "C candidate size not 45")
    require(Counter(x["candidate_part"] for x in c_roles.values()) == ROLE_COUNTS,
            "C label counts changed")

    with read_source_sqlite(root / F_DB) as db:
        models = list(db.execute("SELECT source_id,resource_id,model_key,path,sha FROM model"))
        index = {(r["source_id"],r["resource_id"]):r for r in models}
        templates = [index[(s,r)] for s,r,_ in TEMPLATES]
        require(len({t["model_key"] for t in templates}) == 4,
                "chair template providers not unique")
        require({key[0] for key in c_roles} == {t["model_key"] for t in templates},
                "role candidate attached to unverified provider")
        roles = []
        valid_element_keys = set(source_by)
        for model in templates:
            key = model["model_key"]
            elems = list(db.execute("""
                SELECT provider_key,element_index,source_from,source_to,pivot,axis,
                       angle,rescale,rotated_bbox,part_candidate,part_evidence
                FROM element WHERE provider_key=? ORDER BY element_index""", (key,)))
            built = [build_element(r) for r in elems]
            require(built, "no original geometry in chair")
            model_min = [min(e["bounds"][i] for e in built) for i in range(3)]
            model_max = [max(e["bounds"][i+3] for e in built) for i in range(3)]
            model_spans = [model_max[i] - model_min[i] for i in range(3)]
            require(all(d > 0 for d in model_spans), "zero model extent")
            for item, geom in zip(elems, built):
                k = (key, int(item["element_index"]))
                if k not in c_roles:
                    continue
                c = c_roles[k]
                require(c["candidate_part"] == item["part_candidate"] and
                        c["evidence"] == item["part_evidence"] ==
                        "GEOMETRY_AND_FACE_SLOTS",
                        "C/F role candidate provenance mismatch "+str(k))
                bounds = geom["bounds"]
                span = [bounds[i+3]-bounds[i] for i in range(3)]
                center = [(bounds[i+3]+bounds[i])/2 for i in range(3)]
                relative = [(center[i]-model_min[i])/model_spans[i] for i in range(3)]
                touching = []
                for other in built:
                    if other["index"] == geom["index"]:
                        continue
                    b2=other["bounds"]
                    # AABB overlap OR touching is a geometric diagnostic, not physical contact.
                    if all(bounds[j] <= b2[j+3]+1e-7 and
                           bounds[j+3] >= b2[j]-1e-7 for j in range(3)):
                        touching.append(other["index"])
                roles.append({
                    "provider_key": key,
                    "source_id": model["source_id"],
                    "source_model_path": model["path"],
                    "source_model_sha": model["sha"],
                    "element_index": str(geom["index"]),
                    "original_role_candidate": item["part_candidate"],
                    "original_role_basis": item["part_evidence"],
                    "bbox_rotated": "|".join(f"{v:.7f}" for v in bounds),
                    "span_rotated": "|".join(f"{v:.7f}" for v in span),
                    "relative_model_center_xyz": "|".join(f"{v:.5f}" for v in relative),
                    "model_element_count": str(len(elems)),
                    "aabb_touch_or_overlap_element_count": str(len(touching)),
                    "aabb_neighbor_ids": "|".join(map(str, sorted(touching))),
                    "source_texture_slots": c["texture_slots"],
                    "rotation_axis": item["axis"], "rotation_angle": str(item["angle"]),
                    "geometry_source_consistent": "true",
                    "role_visual_verified": "false",
                    "material_style_verified": "false",
                    "review_decision": "SOURCE_GEOMETRY_MEASURED_ROLE_HYPOTHESIS",
                    "remaining_evidence": "TEXTURED_ORIGINAL_IN_GAME_SCENE_AND_PART_ROLE_INSPECTION",
                })
        require(len(roles) == 45 and
                len({(r["provider_key"],r["element_index"]) for r in roles}) == 45,
                "45 role candidates not independently measured")

        # Existing per-sample roles are assertions in 1-3-F, not distinct approved parts.
        samples = list(db.execute("""
          SELECT sample_id,rule_index,provider_key,element_index,part_candidate,basis
          FROM sample_part ORDER BY sample_id,rule_index,provider_key,element_index"""))
        source_sample_ids = {r["id"] for r in db.execute("SELECT id FROM sample")}
        require(len(source_sample_ids) == 47 and len(samples) == 94,
                "existing sample or part-role population changed")
        sample_out = []
        for r in samples:
            k = (r["provider_key"],int(r["element_index"]))
            require(r["sample_id"] in source_sample_ids and k in valid_element_keys,
                    "sample part points to missing case or source element")
            require(r["part_candidate"] and r["basis"], "sample part without stated basis")
            sample_out.append({
                "sample_id":r["sample_id"],
                "rule_index":str(r["rule_index"]),
                "provider_key":r["provider_key"],
                "element_index":str(r["element_index"]),
                "historical_role_claim":r["part_candidate"],
                "historical_basis":r["basis"],
                "also_in_45_chair_candidates":str(k in c_roles).lower(),
                "source_element_present":"true",
                "function_independently_verified":"false",
                "review_decision":"SAMPLE_SPECIFIC_ROLE_CANDIDATE_ONLY",
            })
    return roles, sample_out


def finding_rows(root):
    source = parse_csv((root / FINDING_SOURCE).read_bytes())
    historic = parse_csv((root / FINDING_LIMITS).read_bytes())
    require(len(source) == len(historic) == 21, "21 comparison findings expected")
    a = {x["finding_id"]: x for x in source}
    b = {x["finding_id"]: x for x in historic}
    require(set(a) == set(b), "original findings have differing IDs")
    require(Counter(x["disposition"] for x in source) ==
            {"CANDIDATE_REQUIRES_REVIEW": 14, "SCOPE_LIMIT_ONLY": 7},
            "comparison 14+7 candidate/limit census changed")
    out = []
    for ident in sorted(a):
        x, h = a[ident],b[ident]
        require(x["category"] == h["category"] and
                x["classification"] == h["classification"] and
                x["axis"] == h["axis"] and x["cases"] == h["cases"] and
                x["disposition"] == h["disposition"],
                "independent original comparison ledgers disagree "+ident)
        require(x["status"] == "PASS" and
                x["measurements_verified"] == "YES" and
                x["limitations_preserved"] == "YES" and
                h["scope_limit"].strip() and h["review_condition"].strip(),
                "finding original measures/scope incomplete "+ident)
        out.append({
            "finding_id": ident, "category":x["category"],
            "original_axis":x["axis"], "original_case_ids":x["cases"],
            "original_disposition":x["disposition"],
            "source_measurements_reconciled":"true",
            "review_condition":h["review_condition"],
            "scope_limit":h["scope_limit"],
            "role_or_universal_style_approved":"false",
            "review_decision":("REVIEW_SCOPED_CANDIDATE" if
                x["disposition"]=="CANDIDATE_REQUIRES_REVIEW" else
                "RETAIN_NON_GENERALIZABLE_COUNTEREXAMPLE"),
        })
    return out


def csv_text(rows):
    out=io.StringIO(newline="")
    writer=csv.DictWriter(out,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def audit(root):
    root=Path(root)
    semantic, visual, scoped = fixed_sources(root)
    parts, samples = shape_rows(root)
    findings = finding_rows(root)
    summary = {
        "schema":"MCFR_INT5_A_ORIGINAL_GEOMETRY_AND_SEMANTIC_TRIAGE_V1",
        "decision":"PASS_SOURCE_CROSSCHECK_ONLY_SEMANTIC_VISUAL_APPROVAL_PENDING",
        "counts":{
            "original_geometry_elements_reopened":1911,
            "chair_source_role_candidates_measured":len(parts),
            "chair_role_candidates_by_label":dict(sorted(Counter(
                r["original_role_candidate"] for r in parts).items())),
            "chair_provider_models":4,
            "sample_specific_claims_reopened":len(samples),
            "comparison_findings_reopened":len(findings),
            "comparison_candidates":14,"non_generalizable_limits":7,
            "pending_semantic_review_queue":59,
            "independent_new_role_visual_approvals":0,
            "new_verified_material_or_style_claims":0,
            "INT6_training_rights_approvals":0,
        },
        "original_source_sha256":{
            "C_PARTS":semantic["input_sha256"]["1-3-C/PARTS.csv.gz"],
            "F_database_xz":semantic["input_sha256"]["1-3-F/furniture_research.sqlite.xz"],
        },
        "origin_git_blobs":dict(sorted(EXPECTED_BLOBS.items())),
        "previous_INT4_scoped_modeling":"70/70",
        "original_INT4_strict_H03_H05":{"H03":"HOLD","H05":"CONDITIONAL"},
        "game_or_visual_observation_new_this_run":0,
        "new_original_3D_model_or_texture_assets_redistributed":0,
        "limits":[
            "45 element AABBs, rotations and neighboring AABBs are source-space metrics, not observed seat/backrest function.",
            "94 historical sample-part labels are scoped annotations; they do not verify 94 distinct functional parts.",
            "14 candidate rules are not universally valid and 7 limitation/counterexample findings must be retained.",
            "No original Minecraft screenshots were opened in this run. The prior 45 SVGs are texture-free diagnostic projections.",
            "No new client F2, texture-level material, GPU bake, semantic human approval or AI training rights inferred.",
        ],
    }
    files = {
        OUTPUTS["parts"].as_posix():csv_text(parts),
        OUTPUTS["samples"].as_posix():csv_text(samples),
        OUTPUTS["findings"].as_posix():csv_text(findings),
    }
    summary["output_sha256"] = {p:hashlib.sha256(c.encode("utf-8")).hexdigest()
                                for p,c in sorted(files.items())}
    files[OUTPUTS["summary"].as_posix()] = (
        json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    return files


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--out",type=Path,default=ROOT)
    ap.add_argument("--verify",action="store_true")
    ap.add_argument("--emit-json",action="store_true",
                    help="Emit exact UTF-8 derived output texts for first-run GitHub commit")
    args=ap.parse_args()
    result=audit(args.root)
    for path,content in result.items():
        dest=args.out/path
        if args.verify:
            require(dest.read_text(encoding="utf-8")==content,
                    "stored derived output differs from original replay "+path)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(content,encoding="utf-8")
    if args.emit_json:
        print("INT5_A_OUTPUT_JSON_BEGIN")
        print(json.dumps(result,ensure_ascii=True,separators=(",",":")))
        print("INT5_A_OUTPUT_JSON_END")
    print("INT5_A_SOURCE_GEOMETRY_45_SAMPLE_CLAIMS_94_FINDINGS_21_PASS")
    print("INT5_A_FUNCTION_OR_MATERIAL_APPROVED_0")
    return 0


if __name__=="__main__":
    sys.exit(main())
