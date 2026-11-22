"""INT-4-F6: replay ACTUAL original-source chair tuck + Handcrafted inner corner.

The original 1-5 S02/S34 source cases remain immutable. This experiment tests
specific predicates discovered in pinned upstream Java SOURCE, not inferred
from the screenshots or invented historical case identities.

AnotherFurniture 1.21.1: crispytwig/AnotherFurniture@57eb624c...
- ChairBlock.java blob 09fc2ea4a4985e13721021be9233b2ff065b367b
- TuckableBlock.java blob d459c34b5ea464985611a1c39473d884fedb9218
Handcrafted pinned: terrarium-earth/Handcrafted@8d21d166...
- ModularSeatBlock.java blob bbe428e318a7810f694ad2db640cf6d89b27aa5f
This source is an algorithmic hypothesis. Exact pinned 4.0.2 game JAR
server state AND actual native F2 are the experimental authority.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from . import int4_f5_state_diagnostic as f5
from . import int4_nonchair_runtime as runner

VERSION="1.21.1"
CASES=f5.CASES
MODE="f6"
ORIGIN=runner.ORIGIN
X,Y,Z=ORIGIN
POINT=runner.position(*ORIGIN)
CHAIR=f5.EXPECTED_ORIGINAL["S02"][0]
COUCH=f5.EXPECTED_ORIGINAL["S34"][0]
CHAIR_TARGET=f5.S02_STATE
COUCH_TARGET=f5.S34_STATE
PLAIN_TOP_SLAB="minecraft:oak_slab[type=top,waterlogged=false]"
TABLE=f5.AF_TABLE
COUCH_NORTH_WEST=f"{COUCH}[color=white,facing=west,shape=single,waterlogged=false]"
COUCH_NORTH_EAST=f"{COUCH}[color=white,facing=east,shape=single,waterlogged=false]"
COUCH_NORTH_NORTH=f"{COUCH}[color=white,facing=north,shape=single,waterlogged=false]"
SOURCE_PINS={
 "af_git_commit":"57eb624cbb7f408d43398c7434b0d38d312cb55d",
 "af_chair_block_git_blob":"09fc2ea4a4985e13721021be9233b2ff065b367b",
 "af_tuckable_block_git_blob":"d459c34b5ea464985611a1c39473d884fedb9218",
 "hc_git_commit":"8d21d1665916850c3fa3bdaf1370c50ec2ca7035",
 "hc_modular_seat_git_blob":"bbe428e318a7810f694ad2db640cf6d89b27aa5f",
}
TRIALS=(
 "S02_NORTH_TABLE_TUCK",
 "S02_NORTH_TOP_SLAB_TUCK",
 "S02_EAST_SLAB_CONTROL",
 "S02_NORTH_SLAB_REMOVED",
 "S34_NORTH_WEST_INNER_LEFT",
 "S34_NORTH_EAST_INNER_RIGHT",
 "S34_SOUTH_WEST_OUTER_LEFT",
 "S34_SOUTH_EAST_OUTER_RIGHT",
 "S34_NORTH_NORTH_SINGLE",
 "S34_NORTH_WEST_EAST_OCCUPIED",
)
EXPECTED_SHAPES={
 "S34_NORTH_WEST_INNER_LEFT":"inner_left",
 "S34_NORTH_EAST_INNER_RIGHT":"inner_right",
 "S34_SOUTH_WEST_OUTER_LEFT":"outer_left",
 "S34_SOUTH_EAST_OUTER_RIGHT":"outer_right",
 "S34_NORTH_NORTH_SINGLE":"single",
 "S34_NORTH_WEST_EAST_OCCUPIED":"right",
}
EXPECTED_TUCKED={
 "S02_NORTH_TABLE_TUCK":"true",
 "S02_NORTH_TOP_SLAB_TUCK":"true",
 "S02_EAST_SLAB_CONTROL":"false",
 "S02_NORTH_SLAB_REMOVED":"false",
}
HISTORY_EXPECTED_EXACT={"S02_NORTH_TABLE_TUCK","S02_NORTH_TOP_SLAB_TUCK","S34_NORTH_WEST_INNER_LEFT"}


def check(x,msg):
    if not x:raise AssertionError(msg)


def original_source():
    rows,sha=f5.original_source()
    check(set(rows)==set(CASES),"F6 original 1-5 cases changed")
    return rows,sha


def stages(props):
    check(set(props)>={"S02","S34","_table_present"},"Real game JAR property inventory missing")
    original_source()
    checks={}
    clear=f"fill {X-1} {Y} {Z-1} {X+1} {Y} {Z+1} minecraft:air"
    def add(name,case,neighbors,place,after=()):
        expected=f5.EXPECTED_ORIGINAL[case]
        model=expected[0]
        cmds=[clear,*neighbors,f"setblock {POINT} {place}",*after]
        checks[name]=(cmds,{
            "subject":{
                "block":f"{POINT} {model}",
                "exact":f"{POINT} {runner.state(*expected)}",
            },
            "actual":runner.probe(model,ORIGIN,props[case]),
        })
    north=f"{X} {Y} {Z-1}"
    south=f"{X} {Y} {Z+1}"
    east=f"{X+1} {Y} {Z}"
    add("S02_NORTH_TABLE_TUCK","S02",[f"setblock {north} {TABLE}"],CHAIR_TARGET)
    add("S02_NORTH_TOP_SLAB_TUCK","S02",[f"setblock {north} {PLAIN_TOP_SLAB}"],CHAIR_TARGET)
    add("S02_EAST_SLAB_CONTROL","S02",[f"setblock {east} {PLAIN_TOP_SLAB}"],CHAIR_TARGET)
    add("S02_NORTH_SLAB_REMOVED","S02",[f"setblock {north} {PLAIN_TOP_SLAB}"],
        CHAIR_TARGET,(f"setblock {north} minecraft:air",))
    add("S34_NORTH_WEST_INNER_LEFT","S34",[f"setblock {north} {COUCH_NORTH_WEST}"],COUCH_TARGET)
    add("S34_NORTH_EAST_INNER_RIGHT","S34",[f"setblock {north} {COUCH_NORTH_EAST}"],COUCH_TARGET)
    add("S34_SOUTH_WEST_OUTER_LEFT","S34",[f"setblock {south} {COUCH_NORTH_WEST}"],COUCH_TARGET)
    add("S34_SOUTH_EAST_OUTER_RIGHT","S34",[f"setblock {south} {COUCH_NORTH_EAST}"],COUCH_TARGET)
    add("S34_NORTH_NORTH_SINGLE","S34",[f"setblock {north} {COUCH_NORTH_NORTH}"],COUCH_TARGET)
    add("S34_NORTH_WEST_EAST_OCCUPIED","S34",[
        f"setblock {north} {COUCH_NORTH_WEST}",
        f"setblock {east} {COUCH_NORTH_NORTH}",
    ],COUCH_TARGET)
    check(tuple(checks)==TRIALS,"Causal stage order diverged")
    return checks


def capture(command,env,game,output,version):
    check(version==VERSION,"INT-4-F6 requires pinned Minecraft 1.21.1")
    original_source()
    return runner.capture(command,env,game,output,version,
                          case_ids=CASES,source_only=True,diagnostic_mode=MODE)


def audit(directory,output=None):
    folder=Path(directory)
    original,historical_sha=original_source()
    report=runner.audit(folder)
    check(report["status"]=="SERVER_STATES_AND_F2_RECORDED","Real client F2 not recorded")
    check(report["minecraft"]==VERSION,"Wrong game version")
    check(report.get("diagnostic_mode")==MODE and report.get("f_source_only") is True,
          "Wrong run mode or legacy output mixed")
    check(report.get("f_target_case_ids")==list(CASES),"Original source IDs not preserved")
    plan=stages(report["property_values"])
    check(tuple(report["server_states"])==TRIALS and set(report["native_f2_sha256"])==set(TRIALS),
          "Missing native F2 or server probes")
    targets={}
    for key,(commands,_) in plan.items():
        obs=report["server_states"][key]
        case="S02" if key.startswith("S02") else "S34"
        state={k:v for k,v in obs["actual"].items() if k!="block"}
        check(obs["actual"]["block"]=="present",f"Subject block missing: {key}")
        check(set(state)==set(report["property_values"][case]),f"State incomplete: {key}")
        check(all(v in report["property_values"][case][k] for k,v in state.items()),
              f"Invalid release property in game: {key}")
        check(len(report["native_f2_sha256"][key])==64,f"Invalid native PNG hash: {key}")
        true_state=obs["subject"]["exact"]
        if true_state:
            check(key in HISTORY_EXPECTED_EXACT,"Unexpected success in negative control: "+key)
        targets[key]={
            "original_case":case,
            "requested_original_state":f5.EXPECTED_ORIGINAL[case][1],
            "server_exact_requested_state":true_state,
            "actual_game_properties":state,
            "upstream_code_expected_property":(
                {"tucked":EXPECTED_TUCKED[key]} if case=="S02"
                else {"shape":EXPECTED_SHAPES[key]}),
            "upstream_code_hypothesis_matches_game":(
                state["tucked"]==EXPECTED_TUCKED[key] if case=="S02"
                else state["shape"]==EXPECTED_SHAPES[key]),
            "neighbor_placement_commands":commands[1:-1],
            "native_F2_sha256":report["native_f2_sha256"][key],
            "F2_original_dimensions":[1024,684],
            "F2_reopened_in_shared_audit":True,
            "new_part_or_rights_approval":False,
        }
    check(len(targets)==10,"Wrong ten independent trials")
    # A correct original state is a CONDITIONAL research outcome, not automatic
    # F full exit: controlled visual review and part UV semantics are separate.
    recovered=[k for k,v in targets.items() if v["server_exact_requested_state"]]
    result={
        "schema":"MCFR_INT4_F6_SOURCE_CONDITION_REAL_FABRIC_NATIVE_F2/v1",
        "status":"PASS_REAL_CLIENT_TEN_SOURCE_CODE_CONDITION_TRIALS_NOT_FULL_F_EXIT",
        "minecraft":VERSION,
        "pinned_upstream_source_provenance":SOURCE_PINS,
        "historical_application_sha256":historical_sha,
        "historical_case_ids":list(CASES),
        "game_client_log_sha256":report["client_log_sha256"],
        "installed_mod_release_source":report["source"]["diagnostic_release_properties"],
        "cases":targets,
        "counts":{
            "native_client_stages":10,
            "native_F2_images":10,
            "real_game_exact_historical_state_stages":len(recovered),
            "original_case_ids_with_exact_game_state":sorted({
                targets[k]["original_case"] for k in recovered}),
            "not_yet_semantically_approved":2,
            "int5_int6_new_approvals":0,
        },
        "observed_recovered_stages":recovered,
        "limits":[
            "Java source code predicts shape changes; real Minecraft 1.21.1 installed JAR and server output determine actual results.",
            "Source file Git SHAs are pinned but AF study Git version vs Fabric release bytes differ as documented in F4/F5.",
            "10 native F2 PNGs and logs are separate temporary Actions artifacts, not embedded in repository.",
            "A successful original server property is conditionally useful; original image subject and UV/meaning need independent review.",
            "INT-4-G/H and INT-5 semantic, INT-6 AI training/redistribution rights remain not approved.",
        ],
    }
    if output:
        out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    print(json.dumps(audit(a.directory,a.output),ensure_ascii=False,indent=2))
