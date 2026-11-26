"""B25: eight original-source5 leave-one-leg-out Fabric experiments in one batch.

Exactly four additional hypotheses per original AF121 and AF123 chair. Every
experiment compares original source5 on/off with source6 and original source4
seat source held; three of the four indices 0..3 remain, one is omitted.

Reuses B23 verified official Minecraft Fabric native F2 capture/audit path
without editing or recomputing any source UV/texture/face coordinates.
Interpretation remains *bounded screen-render interaction*, not physical leg
function, single-cause occlusion, semantic/material/style or asset rights.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from . import int5_b23_multigroup_source5_context_f2 as b23
from . import int5_b20_af_reversed_x_three_session_f2 as b20
from . import int4_h12_af_chair_samepose_f2_capture as h12

TARGETS=b23.TARGETS
VERSION=b23.VERSION
OMIT_LEG_CONTEXTS={
    "without_leg0":(1,2,3,4),
    "without_leg1":(0,2,3,4),
    "without_leg2":(0,1,3,4),
    "without_leg3":(0,1,2,4),
}
AUDIT="INT5_B25_FOUR_ORIGINAL_LEG_OMISSIONS_SOURCE5_INDEPENDENT_F2_AUDIT_V1.json"

def need(ok,reason):
    if not ok: raise ValueError("INT5-B25: "+reason)

def setup(context):
    need(context in OMIT_LEG_CONTEXTS,"only exactly four omitted-original-leg context masks")
    need(set(OMIT_LEG_CONTEXTS[context])==set((0,1,2,3,4))-
         {int(context[-1])} and 4 in OMIT_LEG_CONTEXTS[context],
         "exact parent indices 0..4 with one original leg omitted must be preserved")
    need(not set(OMIT_LEG_CONTEXTS).intersection(b23.CONTEXTS) or
         all(b23.CONTEXTS[k]==OMIT_LEG_CONTEXTS[k] for k in
             set(OMIT_LEG_CONTEXTS).intersection(b23.CONTEXTS)),
         "B23 original named context must not be redefined")
    b23.CONTEXTS.update(OMIT_LEG_CONTEXTS)
    return context

def evidence_selected(context,mode):
    setup(context)
    indices=b23.choose(context,mode)
    missing=int(context[-1])
    expected=tuple(sorted(({0,1,2,3}-{missing}) |
                           {4,6} |
                           ({5} if mode=="with_5" else set())))
    need(indices==expected,
         "original source6, source4, three legs with source5 single intervention")
    return indices

def capture(command,env,game,out,version,target,context):
    need(target in TARGETS and version==VERSION,"original two target 1.21.1 only")
    setup(context)
    for mode in b23.MODES:evidence_selected(context,mode)
    return b23.capture(command,env,game,out,version,target,context)

def audit(directory,target,context):
    need(target in TARGETS and context in OMIT_LEG_CONTEXTS,
         "original target and a single withheld leg context required")
    setup(context)
    data=b23.audit(directory,target,context)
    pin=b20.PIN[target]
    need(data["target"]==target and data["context"]==context
         and data["original_Fabric_release_JAR_SHA1"]==h12.JAR_SHA1
         and data["real_Fabric_clients"]==2
         and data["new_F2_sha256_verified"]==32
         and data["client_log_sha256_verified"]==2
         and data["real_original_server_chair_states"]==32
         and data["real_original_server_support_states"]==
         (32 if target=="AF123_5" else 0)
         and data["status"].startswith("PASS_")
         and data["original_face_UV_exclusive_GPU_pixel_owner_approved"]==0
         and data["role_function_material_style_approved_45"]==0
         and data["third_party_training_or_redistribution_rights_approved"]==0
         and data["H03"]=="HOLD" and data["H05"]=="CONDITIONAL"
         and data["F70_unconditional_approved"]==0,
         "real B23 native F2, temporal/negative or strict original gate failed")
    for mode in b23.MODES:
        source=data["source_child_only_proofs"][mode]
        need(source["selected_original_element_indices"]==
             list(evidence_selected(context,mode)) and
             source["original_source5_from"]==pin["from"] and
             source["original_source5_to"]==pin["to"] and
             source["original_parent_git_blob"]==pin["parent_blob"] and
             source["original_child_git_blob"]==pin["child_blob"] and
             source["faces_uv_textures_coordinates_identical_to_original_parent"] is True
             and source["changed_uncompressed_JAR_members"]==[pin["child"]] and
             source["original_or_patched_JAR_distributed"] is False,
             "original source5 and rest exact child/parent provenance not verified")
    views=data["original_four_camera_source5_addition_metrics"]
    pixels={v:views[v]["five_addition_before_pixels"] for v in b23.b19.VIEWS}
    outcome=("SOURCE5_ADDS_PIXELS_WHEN_ORIGINAL_LEG_OMITTED"
             if any(pixels.values()) else
             "SOURCE5_STILL_NOT_VISIBLE_WITH_THIS_LEG_OMITTED")
    result={
        "schema":"MCFR_INT5_B25_ONE_LEG_OMITTED_EXACT_ORIGINAL_FABRIC_F2/v1",
        "target":target,"context":context,"excluded_original_leg_index":int(context[-1]),
        "retained_original_parent_indices_without_source5":
            list(evidence_selected(context,"without_5")),
        "retained_original_parent_indices_with_source5":
            list(evidence_selected(context,"with_5")),
        "official_original_JAR_SHA1":h12.JAR_SHA1,
        "real_game_clients":2,"actual_native_F2_SHA256_verified":32,
        "original_client_logs_SHA256_verified":2,
        "original_server_chair_state_proofs":32,
        "original_server_support_slab_state_proofs":32 if target=="AF123_5" else 0,
        "pixels_south_north_east_west":[pixels[v] for v in b23.b19.VIEWS],
        "original_B23_strict_controls_and_source_audit":data,
        "decision":outcome,
        "independent_original_5_vs_absent_screen_intervention":True,
        "exclusive_single_original_leg_occlusion_cause_proven":False,
        "physical_leg_or_seat_role_proven":False,
        "original_face_UV_GPU_pixel_owner_verified":False,
        "material_style_verified":False,
        "third_party_training_or_redistribution_rights_approved":False,
        "B19_original_43_of_45_source_removal_visible_still_unchanged":True,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "note":"One omitted original index plus source5 on/off under fixed original source6 and seat4; no unique physical leg or GPU occlusion role is implied.",
    }
    folder=Path(directory)
    (folder/AUDIT).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target",choices=TARGETS,required=True)
    parser.add_argument("--context",choices=OMIT_LEG_CONTEXTS,required=True)
    parser.add_argument("--directory",type=Path,required=True)
    args=parser.parse_args()
    result=audit(args.directory,args.target,args.context)
    print(json.dumps({"target":args.target,"context":args.context,
                     "pixels":result["pixels_south_north_east_west"],
                     "decision":result["decision"]},
                     ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
