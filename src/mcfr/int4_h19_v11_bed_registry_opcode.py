"""INT-4-H19: exact static BlockEntityType.BED -> BedRenderer constructor link.

Inspect original Mojang Minecraft Java 1.21.11 mappings and pinned client JAR,
including the registry method's bytecode PC and invokedynamic bootstrap target.
H19 never asserts a live Java invocation, generated geometry or exact GPU UV.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from . import int4_h18_v11_bed_renderer_bytecode as h18

BLOCK_ENTITY_TYPE = "net.minecraft.world.level.block.entity.BlockEntityType"
RENDERER = "net.minecraft.client.renderer.blockentity.BedRenderer"
REGISTRY = "net.minecraft.client.renderer.blockentity.BlockEntityRenderers"
PREVIOUS_LEDGER = Path("project/integration/INT4_H18_V11_BED_RENDERER_STATIC_BYTECODE_SOURCE_V1.json")
PARENT_STATUS = "PASS_PINNED_OFFICIAL_MOJANG_MAPPING_BED_RENDERER_REGISTRY_STATIC_BYTECODE_LINK"
AUDIT_FILE = "INT4_H19_V11_BED_TYPE_TO_RENDERER_INVOKEDYNAMIC_BYTECODE_AUDIT_V1.json"


def require(value, reason):
    if not value:
        raise ValueError(reason)


def mapped_field(mapping, original_owner, name):
    """Exact original class block & declaration, not a fuzzy BED substring."""
    header = original_owner + " -> "
    lines = mapping.splitlines()
    found = []
    inside = False
    for line in lines:
        if not line or line.startswith("#"):
            continue
        if not line[0].isspace():
            if inside:
                break
            inside = line.startswith(header)
            continue
        if not inside:
            continue
        hit = re.fullmatch(r"\s*(?P<decl>.+?)\s+"+re.escape(name)+
                           r"\s+->\s+(?P<obf>[A-Za-z_$][A-Za-z0-9_$]*)",line)
        if hit:
            declaration = hit.group("decl")
            require("static" in declaration.split() and
                    "final" in declaration.split() and
                    "BlockEntityType" in declaration,
                    "H19_BED_FIELD_DECLARATION_NOT_STATIC_FINAL_ENTITY_TYPE")
            found.append(hit.group("obf"))
    require(len(found)==1,"H19_ORIGINAL_BED_FIELD_MAPPING_MISSING_OR_AMBIGUOUS")
    return found[0]


def instructions(javap):
    """Only JVM instruction lines from javap; other blocks may reuse numbers."""
    return [
        {"pc":int(m.group(1)),"opcode":m.group(2),
         "comment":m.group(3) or "","line":row.strip()}
        for row in javap.splitlines()
        if (m:=re.match(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)"
                        r"(?:.*?//\s*(.*))?$",row))
    ]


def bootstrap_section(javap, index):
    """Find exact BootstrapMethods table entry for one InvokeDynamic slot."""
    if "BootstrapMethods:" not in javap:
        return []
    part = javap.split("BootstrapMethods:",1)[1]
    lines = part.splitlines()
    result=[]
    inside=False
    for line in lines:
        m = re.match(r"^  (\d+):\s+#\d+",line)
        if m:
            if inside:
                break
            inside=int(m.group(1))==index
            if inside:
                result.append(line.strip())
            continue
        if inside:
            if re.match(r"^[A-Za-z][A-Za-z ]*:",line):
                break
            result.append(line.strip())
    return result


def find_bed_registration(javap, field_owner, field_name, renderer_owner):
    """Match one continuous getstatic BED -> lambda BedRenderer::new -> register.

    The invokedynamic bootstrap index must resolve to the actual ctor owner.
    Constant-pool presence anywhere else does NOT qualify.
    """
    ins=instructions(javap)
    target=re.compile(r"(?:^| )Field "+re.escape(field_owner)+r"\."+
                      re.escape(field_name)+r":L"+re.escape(field_owner)+r";")
    candidates=[]
    diagnostics=[]
    for i,item in enumerate(ins):
        if item["opcode"]!="getstatic" or not target.search(item["comment"]):
            continue
        diagnostics.append([o["line"] for o in ins[i:i+5]])
        require(i+2<len(ins),"H19_BED_FIELD_GETSTATIC_NO_FOLLOWING_OPERATIONS")
        next_op = ins[i+1]
        if next_op["opcode"]!="invokedynamic":
            continue
        match=re.search(r"InvokeDynamic #(\d+):",next_op["comment"])
        if not match:
            continue
        idx=int(match.group(1))
        bootstrap=bootstrap_section(javap,idx)
        expected=re.compile(r"REF_newInvokeSpecial\s+"+re.escape(renderer_owner)+
                            r'\."<init>":')
        if not any(expected.search(x) for x in bootstrap):
            continue
        register=ins[i+2]
        if register["opcode"]!="invokestatic":
            continue
        # A registration method in the same class normally prints Method
        # a:(LBlockEntityType;LProvider;)V. Require exact type descriptor.
        if ("L"+field_owner+";") not in register["comment"]:
            continue
        candidates.append({
            "block_entity_type_BED_getstatic_pc":item["pc"],
            "bed_renderer_lambda_invokedynamic_pc":next_op["pc"],
            "registration_invokestatic_pc":register["pc"],
            "bootstrap_index":idx,
            "register_method_reference_summary":register["comment"],
            "bed_field_reference_summary":item["comment"],
            "lambda_reference_summary":next_op["comment"],
            "bootstrap_constructor_method_handle_verified":True,
        })
    if not candidates:
        raise ValueError("H19_EXACT_BED_TYPE_TO_BED_RENDERER_BYTECODE_PAIR_NOT_PROVEN "
                         +json.dumps(diagnostics[:4],ensure_ascii=False))
    require(len(candidates)==1,"H19_BED_REGISTRATION_PAIR_DUPLICATED_OR_AMBIGUOUS")
    return candidates[0]


def audit(version_json, mapping_file, original_client, prior_v11, h18_ledger, javap="javap"):
    root=h18.audit(version_json,mapping_file,original_client,prior_v11,javap)
    require(root["status"]==PARENT_STATUS and
            root["registered_class_compiled_bytecode_proof"] is True and
            root["jvm_render_method_invocation_during_V11_F2_traced"] is False,
            "H19_UPSTREAM_H18_STATIC_AUDIT_CHANGED")
    led=json.loads(Path(h18_ledger).read_text(encoding="utf-8"))
    require(led["schema"]=="MCFR_INT4_H18_V11_MOJANG_BED_RENDERER_SOURCE_CHAIN_KNOWLEDGE_V1" and
            led["registry_proof"]["precise_blockentitytype_BED_field_registration_pair_independently_verified"] is False and
            led["pinned_official"]["client_mappings_sha1"]==root["official_inputs"]["client_mappings_sha1"] and
            led["pinned_official"]["client_jar_sha256"]==root["official_inputs"]["official_client_sha256"],
            "H19_H18_LEDGER_BOUNDARY_OR_OFFICIAL_SHA_DRIFT")
    original_mappings=Path(mapping_file).read_text(encoding="utf-8")
    classes=h18.parse_class_mappings(original_mappings)
    require(BLOCK_ENTITY_TYPE in classes and REGISTRY in classes and RENDERER in classes,
            "H19_REQUIRED_CLASS_MAPPING_ABSENT")
    field=mapped_field(original_mappings,BLOCK_ENTITY_TYPE,"BED")
    owner=classes[BLOCK_ENTITY_TYPE].replace(".","/")
    renderer_owner=classes[RENDERER].replace(".","/")
    registry_obf=classes[REGISTRY]
    registry_javap=h18.javap_output(Path(original_client),registry_obf,javap)
    require(h18.sha256(registry_javap.encode())==root["registry_javap_sha256"] and
            root["registry_to_bed_renderer_owner_references"]==5,
            "H19_H18_REGISTRY_BYTECODE_TEXT_DIFFERENT")
    pair=find_bed_registration(registry_javap,owner,field,renderer_owner)
    require(pair["block_entity_type_BED_getstatic_pc"] <
            pair["bed_renderer_lambda_invokedynamic_pc"] <
            pair["registration_invokestatic_pc"],"H19_REGISTRATION_OPCODE_ORDER_UNEXPECTED")
    return {
        "schema":"MCFR_INT4_H19_V11_MOJANG_BED_FIELD_EXACT_STATIC_REGISTRY_PAIR/v1",
        "status":"PASS_OFFICIAL_12111_BED_FIELD_TO_RENDERER_CTOR_SAME_REGISTRATION_SEQUENCE",
        "source":"official Mojang 1.21.11 client JAR + exact client_mappings",
        "source_pins":root["official_inputs"],
        "historical_V11_case":"V11",
        "original_bed_model_elements":root["original_v11_source"]["ordinary_elements"],
        "original_bed_model_faces":root["original_v11_source"]["ordinary_faces"],
        "block_entity_type_owner":owner,
        "official_BED_static_field_mapped_name":field,
        "registry_owner":registry_obf.replace(".","/"),
        "bed_renderer_owner":renderer_owner,
        "registration":pair,
        "registry_javap_sha256":root["registry_javap_sha256"],
        "parent_h18_repo_ledger":"project/integration/INT4_H18_V11_BED_RENDERER_STATIC_BYTECODE_SOURCE_V1.json",
        "parent_h18_registry_static_class_proof":True,
        "parent_V11_actual_game_run":45103243455,
        "parent_V11_actual_native_F2_count":4,
        "parent_V11_air_vs_bed_changed_pixels":6446,
        "new_game_runs":0,
        "new_native_F2":0,
        "jvm_BedRenderer_invocation_during_previous_game_confirmed":False,
        "exact_model_geometry_and_per_face_UV_extracted":False,
        "screen_pixel_to_GPU_texel_causality_confirmed":False,
        "F70_unconditional_approved":0,
        "H03":"HOLD","H05":"CONDITIONAL",
        "INT5_semantic_approvals":0,
        "INT6_training_or_redistribution_approvals":0,
        "limitations":[
            "Same static block registration bytecode sequence proves original BED field is paired with BedRenderer constructor handle; it does not prove runtime calls in an earlier screenshot.",
            "No original Mojang mapping/client/class bytes or full disassembly copied to the repository.",
            "Field, bootstrap and call-site PC offsets are static original Java bytecode, not geometry or GPU UV.",
            "Existing four V11 native F2 screenshots and two exact server states are linked to the preserved original F11D ledger, not rerun.",
        ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--version-json",type=Path,required=True)
    p.add_argument("--client-mappings",type=Path,required=True)
    p.add_argument("--official-client",type=Path,required=True)
    p.add_argument("--prior-V11",type=Path,required=True)
    p.add_argument("--h18-ledger",type=Path,default=PREVIOUS_LEDGER)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.version_json,args.client_mappings,args.official_client,
                 args.prior_V11,args.h18_ledger)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","official_BED_static_field_mapped_name","registration",
        "new_game_runs","jvm_BedRenderer_invocation_during_previous_game_confirmed")},
        ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
