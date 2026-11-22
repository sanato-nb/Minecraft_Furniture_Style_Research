"""INT-4-F5: diagnostic, NOT acceptance, of S02 chair & S34 couch state loss.

Observe the exact *actual* server block properties from original released mod
JAR blockstate variants, both isolated and with controlled neighbor arrangements.
Do not treat a screenshot with incorrect blockstate as an accepted historical F2.
Existing experimental runner/renderer remains unchanged unless opt-in flag used.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json

from . import int4_nonchair_runtime as runner
from . import int4_f4_chair_bench_couch_capture as baseline

CASES=("S02","S34")
VERSION="1.21.1"
SUBJECT=runner.ORIGIN
AF_TABLE="another_furniture:oak_table"
S02_STATE="another_furniture:oak_chair[facing=north,tucked=true,variant=1]"
S34_STATE="handcrafted:oak_couch[color=white,facing=north,shape=inner_left,waterlogged=false]"
S34_NEIGHBOR="handcrafted:oak_couch[color=white,facing=north,shape=single,waterlogged=false]"
CHALLENGE_STAGES=(
    "S02_ISOLATED",
    "S02_TABLE_EAST",
    "S02_TABLE_SOUTH",
    "S34_ISOLATED",
    "S34_NEIGHBOR_EAST",
    "S34_NEIGHBOR_WEST",
    "S34_NEIGHBOR_NORTH",
    "S34_NEIGHBOR_SOUTH",
    "S34_L_EAST_NORTH",
    "S34_L_EAST_SOUTH",
    "S34_L_WEST_NORTH",
    "S34_L_WEST_SOUTH",
)
CARDINALS={"east":(1,0),"west":(-1,0),"north":(0,-1),"south":(0,1)}
SOURCE_BLOBS={
    "AF":("another_furniture-fabric-4.0.2.jar","assets/another_furniture/blockstates/oak_chair.json"),
    "HC":("handcrafted-fabric-1.21.1-4.0.3.jar","assets/handcrafted/blockstates/oak_couch.json"),
}
EXPECTED_ORIGINAL={
    "S02":("another_furniture:oak_chair","facing=north;tucked=true;variant=1"),
    "S34":("handcrafted:oak_couch","color=white;facing=north;shape=inner_left;waterlogged=false"),
}


def require(condition,message):
    if not condition:raise AssertionError(message)


def original_source():
    f4,h=baseline.original_7_cases()
    result={case:f4[case] for case in CASES}
    for case,row in result.items():
        require((row["block"],row["state"])==EXPECTED_ORIGINAL[case],
                f"source original case changed: {case}")
    return result,h


def _values(document):
    require(isinstance(document.get("variants"),dict),"Not a variants blockstate JSON")
    all_values=defaultdict(set)
    for selector in document["variants"]:
        if not selector:continue
        for atom in selector.split(","):
            key,sep,value=atom.partition("=")
            require(bool(sep and key and value),f"Invalid source blockstate selector {atom!r}")
            all_values[key].add(value)
    return {k:sorted(v) for k,v in sorted(all_values.items())}


def release_properties(mods):
    original_source()
    values={}
    source={}
    for case,cohort in (("S02","AF"),("S34","HC")):
        file,key=SOURCE_BLOBS[cohort]
        with ZipFile(Path(mods)/file) as jar:
            blockstate=jar.read(key)
            props=_values(json.loads(blockstate))
            original=EXPECTED_ORIGINAL[case][1]
            for part in original.split(";"):
                name,_,v=part.partition("=")
                require(v in props.get(name,()),f"Absent valid release property {case}/{part}")
            source[case]={
                "jar":file,"original_state_path":key,
                "blockstate_raw_sha256":hashlib.sha256(blockstate).hexdigest(),
                "property_values":props,
            }
            values[case]=props
            if case=="S02":
                values["_table_present"]="assets/another_furniture/blockstates/oak_table.json" in jar.namelist()
    require("tucked" in values["S02"] and "shape" in values["S34"],
            "The historical risk properties are missing in release")
    return values,source


def stages(values):
    require(set(values)>={"S02","S34","_table_present"},"Release property inventory required")
    x,y,z=SUBJECT
    central=runner.position(*SUBJECT)
    clear=f"fill {x-1} {y} {z-1} {x+1} {y} {z+1} minecraft:air"
    data={}
    # Each trial resets all adjacent blocks first. A single isolated target is
    # never accepted as an inner corner by mere model selector compatibility.
    def add(name,case,subject_state,neighbors):
        block=EXPECTED_ORIGINAL[case][0]
        moves=[clear]
        for dx,dz,neighbor in neighbors:
            require(-1<=dx<=1 and -1<=dz<=1 and (dx or dz),
                    "Neighbor exceeds the bounded diagnostic fixture")
            moves.append(f"setblock {x+dx} {y} {z+dz} {neighbor}")
        moves.append(f"setblock {central} {subject_state}")
        expected=runner.state(block,EXPECTED_ORIGINAL[case][1])
        predicates={
            "subject":{
                "block":f"{central} {block}",
                "exact":f"{central} {expected}",
            },
            "actual":runner.probe(block,SUBJECT,values[case]),
        }
        require("present" in predicates["actual"], "Missing release property probes")
        data[name]=(moves,predicates)

    add("S02_ISOLATED","S02",S02_STATE,[])
    if values["_table_present"]:
        for side in ("east","south"):
            dx,dz=CARDINALS[side]
            add(f"S02_TABLE_{side.upper()}","S02",S02_STATE,[(dx,dz,AF_TABLE)])
    add("S34_ISOLATED","S34",S34_STATE,[])
    for side in ("east","west","north","south"):
        dx,dz=CARDINALS[side]
        add(f"S34_NEIGHBOR_{side.upper()}","S34",S34_STATE,[(dx,dz,S34_NEIGHBOR)])
    for sides in (("east","north"),("east","south"),("west","north"),("west","south")):
        add("S34_L_"+"_".join(sides).upper(),"S34",S34_STATE,
            [(CARDINALS[side][0],CARDINALS[side][1],S34_NEIGHBOR) for side in sides])
    require(len(data)==(12 if values["_table_present"] else 10),
            f"Unexpected trial count: {len(data)}")
    return data


def capture(command,env,game,output,version):
    require(version==VERSION,"Original diagnostics require Minecraft 1.21.1")
    original_source()
    return runner.capture(command,env,game,output,version,
                          case_ids=CASES,source_only=True,diagnostic_mode=True)


def audit(directory,output=None):
    """Independent reparse of original client log & native F2 via shared runner."""
    folder=Path(directory)
    originals,digest=original_source()
    report=runner.audit(folder)
    require(report["minecraft"]==VERSION and report["status"]=="SERVER_STATES_AND_F2_RECORDED",
            "Fabric runner did not complete")
    require(report["diagnostic_mode"] is True,"Trial mode metadata absent")
    require(report["f_source_only"] is True and report["f_target_case_ids"]==list(CASES),
            "Original case coverage changed")
    values=report["property_values"]
    specs=stages(values)
    require(set(report["server_states"])==set(specs),
            "Server trial count incomplete")
    require(set(report["native_f2_sha256"])==set(specs),
            "Actual-game native F2 count incomplete")
    for case,cohort in (("S02","AF"),("S34","HC")):
        props=report["source"]["diagnostic_release_properties"][case]["property_values"]
        require(props==values[case],"JAR sourced valid properties were changed")
    case_audit={}
    for stage in specs:
        entry=report["server_states"][stage]
        require(entry["actual"]["block"]=="present",f"No target block at {stage}")
        case="S02" if stage.startswith("S02") else "S34"
        actual={k:v for k,v in entry["actual"].items() if k!="block"}
        require(set(actual)==set(values[case]),f"Incomplete actual state at {stage}")
        require(all(actual[k] in values[case][k] for k in actual),
                f"Unrecognized actual release property in {stage}")
        case_audit[stage]={
            "case":case,
            "requested_exact_original_state":EXPECTED_ORIGINAL[case][1],
            "exact_server_state_persisted":entry["subject"]["exact"],
            "actual_release_properties":actual,
            "native_f2_sha256":report["native_f2_sha256"][stage],
            "neighbor_fixture":specs[stage][0][1:-1],
        }
    output_data={
        "schema":"MCFR_INT4_F5_TWO_PROPERTY_DIAGNOSTIC_REAL_FABRIC/v1",
        "status":"PASS_REAL_FABRIC_EXACT_PROPERTY_ENUM_AND_F2_NOT_SEMANTIC_EXIT",
        "minecraft":VERSION,
        "historic_1_5_applications_sha256":digest,
        "historic_case_ids":list(CASES),
        "original_case_git_model_sha1":{k:v["model_sha"] for k,v in originals.items()},
        "release_state_property_source":report["source"]["diagnostic_release_properties"],
        "game_client_log_sha256":report["client_log_sha256"],
        "cases":case_audit,
        "trial_count":len(case_audit),
        "actual_original_case_F2_reacceptance":"PENDING_CAUSAL_AND_VISUAL_AUDIT",
        "evidence_limits":{
            "properties_read_from_release_JAR_variants":True,
            "server_property_values_observed_directly":True,
            "all_f2_images_reopened_in_shared_runner":True,
            "pixelwise_uv_or_functional_semantics_approved":False,
            "int5_parts_or_int6_rights_approvals":0,
        },
    }
    if output:
        dest=Path(output)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(output_data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                        encoding="utf-8")
    return output_data


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--directory",required=True,type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    print(json.dumps(audit(args.directory,args.output),ensure_ascii=False,indent=2))
