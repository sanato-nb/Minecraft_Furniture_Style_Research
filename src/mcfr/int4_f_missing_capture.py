"""INT-4-F2: four 1-5 source-specific missing F2 states in a real Fabric client.

Reuses the already independently tested nonchair runtime and real source/world
launcher WITHOUT replacing its previous six state / bed / bookshelf history.
All captured images and installed JARs remain in temporary Actions artifacts.
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

from . import int4_nonchair_runtime as runner

ROOT=Path(__file__).resolve().parents[2]
SOURCE="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
PREVIOUS="project/integration/INT4_NONCHAIR_15_CASES_AUDIT_RESULT.json"
FIXED_VERSION="1.21.1"
CASES=("S05","S06","S07","S10")
EXPECTED={
    "S05":("AF","another_furniture:white_stool","low=false",5,26),
    "S06":("HC","handcrafted:oak_chair","color=none;facing=north;waterlogged=false",13,78),
    "S07":("HC","handcrafted:oak_chair","color=white;facing=north;waterlogged=false",13,78),
    "S10":("HC","handcrafted:oak_side_table","color=none;facing=north;waterlogged=false",11,66),
}

def check(value,msg):
    if not value:
        raise AssertionError(msg)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def original_4_cases():
    raw=(ROOT/SOURCE).read_bytes()
    old=json.loads((ROOT/PREVIOUS).read_text(encoding="utf-8"))
    check(sha256(raw)==old["observed"]["source_ledger_sha256"][SOURCE],
          "1-5 B original ledger bytes changed from verified nonchair source")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    subset={case:[row for row in rows if row["case"]==case] for case in CASES}
    for case,rr in subset.items():
        check(len(rr)==1, "Duplicate/missing exact case "+case)
        row=rr[0]
        check((row["cohort"],row["block"],row["state"],int(row["elements"]),int(row["faces"]))==EXPECTED[case],
              "Original source case changed: "+case)
        check(row["minecraft"]==FIXED_VERSION and
              row["geometry_status"]=="STATIC_SOURCE" and
              row["state_sha"] and row["model_sha"] and row["provider_sha"],
              "Original pinned model provenance missing: "+case)
    return {k:v[0] for k,v in subset.items()},sha256(raw)

def capture(command,env,game,output,version):
    check(version==FIXED_VERSION,"F2 missing cases require exact Minecraft 1.21.1")
    original_4_cases()
    # Historical native F2 runner performs independently checked original
    # release JAR SHA1, selected model/parent SHA and exact server state readback.
    return runner.capture(command,env,game,output,version,case_ids=CASES,source_only=True)

def audit(folder,output=None):
    folder=Path(folder)
    originals,ledger=original_4_cases()
    report=runner.audit(folder)
    check(report["status"]=="SERVER_STATES_AND_F2_RECORDED","Real F2 capture did not complete")
    check(report["minecraft"]==FIXED_VERSION,"Minecraft runtime version changed")
    check(report["f_target_case_ids"]==list(CASES) and report["f_source_only"] is True,
          "Wrong original source case selection or extra context")
    check(set(report["server_states"])==set(CASES),"4 required server state readbacks missing")
    check(set(report["native_f2_sha256"])==set(CASES),"4 original F2 screenshots missing")
    observed=report["source"]["representative_states"]
    check(set(observed)==set(CASES),"Source case to runtime model lineage missing")
    summary={}
    for case in CASES:
        row=originals[case]
        model=observed[case]
        check(report["server_states"][case]["subject"]["exact"] is True,
              "Exact original state did not persist in game: "+case)
        check(model["state"]==runner.state(row["block"],row["state"]),
              "Original full block state mismatch: "+case)
        check(model["historical_selection_matches_release"],
              "Original research model selection differs from deployed JAR: "+case)
        check(model["historical_model_geometry"]=={
            "elements":int(row["elements"]),"faces":int(row["faces"])},
            "Original model element/face denominator changed: "+case)
        # The release can differ in raw bytes (AF 4.0.3 Git vs 4.0.2 JAR).
        # Document raw SHA comparison per file and never elevate parsed selectors
        # into release-wide exact-byte equivalence.
        files=model["source_files"]
        check(set(files)=={row["state_path"],row["model_path"],row["provider_path"]},
              "Wrong original model/source/parent paths: "+case)
        check(all(files[row[k+"_path"]]["historical_git_blob_sha1"]==row[k+"_sha"]
                  for k in ("state","model","provider")),
              "Historical model source SHA was modified: "+case)
        image=folder/(case+".png")
        check(image.is_file() and sha256(image.read_bytes())==report["native_f2_sha256"][case],
              "Real client PNG missing/hash differs: "+case)
        summary[case]={
            "case":case,
            "block_and_exact_state":model["state"],
            "cohort":row["cohort"],
            "minecraft_version":row["minecraft"],
            "original_model_key":row["model"],
            "original_blockstate_git_blob_sha1":row["state_sha"],
            "original_model_git_blob_sha1":row["model_sha"],
            "original_provider_git_blob_sha1":row["provider_sha"],
            "pinned_release_file_equality":{
                k:files[row[k+"_path"]]["git_blob_byte_match"]
                for k in ("state","model","provider")},
            "original_source_model_selection_equals_release":True,
            "server_exact_state_readback":True,
            "native_f2_sha256":report["native_f2_sha256"][case],
            "native_f2_dimensions":[1024,684],
            "new_qualitative_visual_image_review":"PENDING_MANUAL_IMAGE_OPEN",
            "actual_baked_UV_or_screenshot_to_source_causal_approval":False,
        }
    check(sum(EXPECTED[c][3] for c in CASES)==42,"Original 4 source elements changed")
    check(sum(EXPECTED[c][4] for c in CASES)==248,"Original 4 source faces changed")
    result={
        "schema":"MCFR_INT4_F2_FOUR_MISSING_CASE_FABRIC_NATIVE_F2/v1",
        "status":"PASS_EXACT_FOUR_ORIGINAL_CASE_SERVER_F2_SHA_NOT_SEMANTIC_RENDER_EXIT",
        "minecraft":"1.21.1",
        "cases":list(CASES),
        "historical_application_csv_sha256":ledger,
        "original_research_case_model_elements":42,
        "original_research_case_model_faces":248,
        "native_f2_png_count":4,
        "client_log_sha256":report["client_log_sha256"],
        "source_files_by_case":summary,
        "evidence_limits":{
            "natural_item_placement_or_GUI_tested":False,
            "source_release_all_models_byte_identical_assumed":False,
            "original_case_F2_proves_pixelwise_UV_equivalence":False,
            "actual_games_4_cases_tested":True,
            "human_visual_approval_automated":False,
            "int5_semantic_approvals":0,
            "int6_training_redistribution_rights_approved":0,
        }
    }
    if output:
        dest=Path(output)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--directory",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    print(json.dumps(audit(args.directory,args.output),ensure_ascii=False,indent=2))
