"""INT-4-F7: four historically frozen AF/HC source cases, actual native Fabric F2.

Source-first evidence. S30 has two simultaneously selected models, not two cases;
S22's minecraft:block/cube parent is VANILLA, not shipped by Handcrafted's JAR.
Game screenshots and server values cannot alone resolve that external parent SHA.
Never turn a successful screenshot into UV/semantic/redistribution approval.
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

from . import int4_nonchair_runtime as runner

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.1"
ORIGINAL_LEDGER=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PREVIOUS_AUDIT=Path("project/integration/INT4_NONCHAIR_15_CASES_AUDIT_RESULT.json")
CASES=("S03","S04","S22","S30")
EXPECTED={
  "S03":("AF","another_furniture:birch_chair",
         "facing=south;tucked=false;variant=3",1,10,46),
  "S04":("AF","another_furniture:spruce_chair",
         "facing=south;tucked=false;variant=3",1,10,46),
  "S22":("HC","handcrafted:oak_drawer",
         "facing=north;shape=single;type=1",1,1,6),
  "S30":("AF","another_furniture:oak_bench",
         "back=true;facing=north;horizontal_1=single;horizontal_2=single",2,10,46),
}
EXTERNAL_VANILLA_PARENT="assets/minecraft/models/block/cube.json"
EXTERNAL_VANILLA_GIT_SHA="3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"
SOURCE_SHA="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"


def check(value,message):
    if not value:raise AssertionError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def original_cases():
    raw=(ROOT/ORIGINAL_LEDGER).read_bytes()
    previous=json.loads((ROOT/PREVIOUS_AUDIT).read_text(encoding="utf-8"))
    check(digest(raw)==SOURCE_SHA==previous["observed"]["source_ledger_sha256"][str(ORIGINAL_LEDGER)],
          "Original 1-5 source ledger SHA drift")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    selection={}
    for case in CASES:
        group=[r for r in rows if r["case"]==case]
        cohort,block,state,n,elems,faces=EXPECTED[case]
        check(len(group)==n,f"Source count changed: {case}")
        check(len({(r["cohort"],r["block"],r["state"],r["minecraft"]) for r in group})==1,
              f"Source case inconsistent: {case}")
        first=group[0]
        check((first["cohort"],first["block"],first["state"],first["minecraft"])==
              (cohort,block,state,VERSION),f"Historical original case changed {case}")
        check(sum(int(r["elements"]) for r in group)==elems and
              sum(int(r["faces"]) for r in group)==faces,
              f"Historical research geometry changed {case}")
        check(all(r["geometry_status"]=="STATIC_SOURCE" and r["state_sha"] and
                  r["model_sha"] and r["provider_sha"] for r in group),
              "Original exact source blob evidence missing: "+case)
        check(len({r["model_path"] for r in group})==n,"Duplicate selected model "+case)
        selection[case]=group
    check(sum(x[4] for x in EXPECTED.values())==31 and
          sum(x[5] for x in EXPECTED.values())==144,
          "Original research denominators changed")
    check(any(r["provider_path"]==EXTERNAL_VANILLA_PARENT and
              r["provider_sha"]==EXTERNAL_VANILLA_GIT_SHA for r in selection["S22"]),
          "S22 original vanilla parent changed")
    check(len(selection["S30"])==2 and
          {int(x["faces"]) for x in selection["S30"]}=={12,34},
          "S30 requires BOTH simultaneous selected model geometries")
    return selection,digest(raw)


def capture(command,env,game,output,version):
    check(version==VERSION,"F7 requires exact original Fabric 1.21.1 runtime")
    original_cases()
    return runner.capture(command,env,game,output,version,case_ids=CASES,source_only=True)


def audit(directory,output=None):
    folder=Path(directory)
    originals,sha=original_cases()
    report=runner.audit(folder)
    check(report["status"]=="SERVER_STATES_AND_F2_RECORDED",
          "Native game source F2 capture not completed")
    check(report["minecraft"]==VERSION and report["f_source_only"] is True and
          report["f_target_case_ids"]==list(CASES),
          "F7 original case IDs or runtime mode changed")
    check(set(report["server_states"])==set(CASES) and
          set(report["native_f2_sha256"])==set(CASES),
          "F7 server game state or actual screenshot missing")
    src=report["source"]
    check(src["ledger_sha256"]==sha,"Game release crosslink does not match source ledger")
    check(set(src["representative_states"])==set(CASES),"Missing original release selection")
    outcome={}
    for case in CASES:
        base=originals[case]
        record=src["representative_states"][case]
        expected_block=runner.state(base[0]["block"],base[0]["state"])
        check(record["state"]==expected_block,"Unexpected original game selector: "+case)
        check(record["historical_model_geometry"]=={
            "elements":EXPECTED[case][4],"faces":EXPECTED[case][5]},
            "Original model denominator mismatch: "+case)
        want={r[k+"_path"]:r[k+"_sha"] for r in base
              for k in ("state","model","provider")}
        observed=record["source_files"]
        check(set(observed)==set(want),"Actual/JAR source path coverage mismatch: "+case)
        for path,gsha in want.items():
            check(observed[path]["historical_git_blob_sha1"]==gsha,
                  "Original Git SHA was silently modified: "+case+"/"+path)
        missing=[p for p in observed if observed[p].get("release_path_absent",False)]
        if case=="S22":
            check(missing==[EXTERNAL_VANILLA_PARENT] and
                  want[EXTERNAL_VANILLA_PARENT]==EXTERNAL_VANILLA_GIT_SHA,
                  "S22 VANILLA parent must be an explicit external parent exception")
        else:
            check(not missing,"Unexpected original release source missing: "+case)
        image=folder/(case+".png")
        check(image.is_file() and
              digest(image.read_bytes())==report["native_f2_sha256"][case],
              "Native F2 PNG image SHA missing or mismatched: "+case)
        selection=record["historical_selection_matches_release"]
        game_exact=report["server_states"][case]["subject"]["exact"]
        outcome[case]={
            "historical_block":base[0]["block"],
            "requested_exact_original_state":expected_block,
            "release_selector_matches_all_original_models":selection,
            "release_model_application_count":len(record["release_model_applications"]),
            "original_model_application_count":len(base),
            "original_geometry_elements":EXPECTED[case][4],
            "original_geometry_faces":EXPECTED[case][5],
            "original_git_source_sha_by_path":want,
            "release_source_file_meta":observed,
            "vanilla_external_parent_resolved_in_installed_mod_jar":False if case=="S22" else None,
            "external_vanilla_parent_independent_runtime_sha_approved":False if case=="S22" else None,
            "game_server_exact_requested_state":game_exact,
            "native_F2_sha256":report["native_f2_sha256"][case],
            "native_F2_size":[1024,684],
            "runtime_model_and_state_conditional_eligibility":selection and game_exact,
            "image_human_review":"PENDING_INDEPENDENT_ORIGINAL_PNG_REOPEN",
            "UV_semantic_or_redistribution_approved":False,
        }
        check(outcome[case]["release_model_application_count"]==len(base) if selection
              else True,"Original model count mismatch in release: "+case)
    result={
        "schema":"MCFR_INT4_F7_AF_VARIANT3_BENCH_HC_EXTERNAL_VANILLA_PARENT_F2/v1",
        "status":"NATIVE_F2_4_CASES_CAPTURED_SOURCE_MODEL_AND_SERVER_PER_CASE_REVIEW",
        "minecraft":VERSION,"historical_case_ids":list(CASES),
        "original_1_5_application_csv_sha256":sha,
        "original_effective_elements":31,"original_effective_faces":144,
        "original_source_applications":5,
        "native_f2_png_count":4,
        "native_f2_distinct_sha_count":len({r["native_F2_sha256"] for r in outcome.values()}),
        "original_client_log_sha256":report["client_log_sha256"],
        "installed_mod_release_sha":src["release_jar_sha1"],
        "source_cases":outcome,
        "counts":{
            "real_game_exact_state":sum(bool(x["game_server_exact_requested_state"]) for x in outcome.values()),
            "original_model_selection_matched_release":sum(bool(x["release_selector_matches_all_original_models"]) for x in outcome.values()),
            "newly_approved_1_5_cases":0,
            "unconditionally_completed_F_cases":0,
            "newly_approved_INT5_parts_or_INT6_training_rights":0,
        },
        "limits":[
            "AF pinned study source Git v4.0.3 and released Fabric v4.0.2 are not assumed byte-identical.",
            "S03 and S04 case selector variant=3 may source a model leaf named *_1; this is a source-led discrepancy, not guessed geometry.",
            "S30 exactly two simultaneous model applications (34 and 12 faces), NEVER count them as two different historical cases.",
            "S22 vanilla minecraft:block/cube parent SHA is original 1-5 research evidence, not a file inside the Handcrafted JAR. Release-external parent SHA must remain separately unapproved until independently validated.",
            "No game GUI user interaction, pixel-perfect UV/visibility attribution, functional semantics or original asset copyright rights inferred.",
            "Actual PNG screenshots not committed; save as retention-limited Github Actions artifacts only."
        ],
    }
    if output:
        path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--directory",required=True,type=Path)
    p.add_argument("--output",type=Path)
    opts=p.parse_args()
    print(json.dumps(audit(opts.directory,opts.output),ensure_ascii=False,indent=2))
