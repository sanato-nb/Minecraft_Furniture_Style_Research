"""INT-4-H18: source-pinned Minecraft 1.21.11 V11 BedRenderer bytecode study.

An official client JAR + matching Mojang ProGuard map + javap are inspected.
This traces STATIC class ownership and renderer registry references, NOT a Java
method invocation during the earlier V11 native F2 capture.
No Mojang client/mapping/JAR/class bytecode is redistributed in the result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from zipfile import ZipFile

VERSION="1.21.11"
VERSION_JSON_SHA1="a969d96978af7b52dba8df44e177f48ec4ebe0d8"
CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
ORIGINAL_V11="project/integration/INT4_F11D_V11_WHITE_BED_REAL_F2_SOURCE_V1.json"
CLASS_NAMES=(
    "net.minecraft.client.renderer.blockentity.BedRenderer",
    "net.minecraft.client.renderer.blockentity.BlockEntityRenderers",
    "net.minecraft.client.renderer.blockentity.BlockEntityRenderDispatcher",
)
OPTIONAL_CLASSES=(
    "net.minecraft.client.renderer.blockentity.state.BedRenderState",
    "net.minecraft.world.level.block.entity.BedBlockEntity",
    "net.minecraft.world.level.block.entity.BlockEntityType",
    "net.minecraft.client.renderer.special.BedSpecialRenderer",
)
EXACT_MODEL_BLOB="9406a8491ed2532d4878b0a91b16a0e5f8d93d80"
EXACT_BLOCKSTATE_BLOB="6577c90a27efb34a7099150253c0bf557d75214c"


def require(condition, error):
    if not condition:
        raise ValueError(error)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def parse_class_mappings(text):
    result={}
    for line in text.splitlines():
        if not line or line[0].isspace() or line[0]=="#":
            continue
        m=re.fullmatch(r"([\w.$]+) -> ([\w.$]+):",line)
        if m:
            require(m.group(1) not in result,"H18_DUPLICATE_ORIGINAL_CLASS_MAPPING")
            result[m.group(1)]=m.group(2)
    return result


def class_ref_lines(javap_text, official_name):
    """Only exact class owner tokens, never obfuscation-name substring matches."""
    internal=official_name.replace(".","/")
    token=re.compile(r"(?<![A-Za-z0-9_$])"+re.escape(internal)+r"(?![A-Za-z0-9_$])")
    return [line.strip() for line in javap_text.splitlines()
            if token.search(line)]


def version_preflight(version_json_raw, client_bytes, mapping_bytes):
    require(sha1(version_json_raw)==VERSION_JSON_SHA1,"H18_OFFICIAL_VERSION_METADATA_SHA1_DRIFT")
    doc=json.loads(version_json_raw.decode("utf-8"))
    require(doc["id"]==VERSION and
            doc["downloads"]["client"]["sha1"]==CLIENT_SHA1,
            "H18_MOJANG_VERSION_OR_CLIENT_PIN_DRIFT")
    require(sha1(client_bytes)==CLIENT_SHA1 and
            sha256(client_bytes)==CLIENT_SHA256,
            "H18_OFFICIAL_VANILLA_12111_CLIENT_SHA_DRIFT")
    spec=doc["downloads"].get("client_mappings")
    require(isinstance(spec,dict) and
            re.fullmatch("[a-f0-9]{40}",spec.get("sha1","") or "") and
            sha1(mapping_bytes)==spec["sha1"],
            "H18_MOJANG_MAPPING_NOT_PINNED_TO_OFFICIAL_VERSION")
    return {"client_mappings_sha1":spec["sha1"],
            "official_version_json_sha1":VERSION_JSON_SHA1,
            "official_client_sha1":CLIENT_SHA1,
            "official_client_sha256":CLIENT_SHA256}


def javap_output(jar, official_class, javap="javap"):
    proc=subprocess.run([javap,"-c","-p","-v","-classpath",str(jar),official_class],
                        capture_output=True,text=True,timeout=100)
    require(proc.returncode==0 and "Constant pool:" in proc.stdout,
            "H18_JAVAP_FAILED_"+official_class+":"+proc.stderr[-200:])
    return proc.stdout


def prior_v11_check(ledger,client):
    require(ledger.get("historical_case_id")=="V11" and
            ledger.get("official_client_sha256")==CLIENT_SHA256 and
            ledger.get("original_no_ordinary_elements_or_faces") is True and
            ledger.get("real_game_two_exact_server_blockstates")==2 and
            ledger.get("actual_original_native_F2_PNG_count")==4 and
            ledger["same_camera_air_vs_bed_pixel_contrast"]["air_control_changed_pixels"]==0 and
            ledger["same_camera_air_vs_bed_pixel_contrast"]["bed_vs_air_changed_pixels"]==6446 and
            ledger["direct_special_renderer_java_call_verified"] is False,
            "H18_PREVIOUS_V11_NATIVE_F2_EVIDENCE_BOUNDARY_DRIFT")
    with ZipFile(client) as archive:
        require(archive.testzip() is None,"H18_OFFICIAL_CLIENT_CRC_FAILURE")
        model=archive.read("assets/minecraft/models/block/bed.json")
        states=archive.read("assets/minecraft/blockstates/white_bed.json")
        require(git_blob(model)==EXACT_MODEL_BLOB and
                git_blob(states)==EXACT_BLOCKSTATE_BLOB and
                not json.loads(model.decode("utf-8")).get("elements"),
                "H18_V11_ORIGINAL_BED_MODEL_OR_STATE_DRIFT")
    return {"model_git_blob_sha1":git_blob(model),
            "blockstate_git_blob_sha1":git_blob(states),
            "ordinary_elements":0,"ordinary_faces":0,
            "existing_F2":4,"existing_F2_BED_vs_AIR_pixels":6446,
            "existing_air_baseline_diff_pixels":0}


def audit(version_json,mapping_file,client,previous,java_tool="javap"):
    version_raw=Path(version_json).read_bytes()
    mappings_raw=Path(mapping_file).read_bytes()
    client=Path(client)
    official=client.read_bytes()
    preflight=version_preflight(version_raw,official,mappings_raw)
    old=prior_v11_check(json.loads(Path(previous).read_text(encoding="utf-8")),client)
    classes=parse_class_mappings(mappings_raw.decode("utf-8"))
    missing=[name for name in CLASS_NAMES if name not in classes]
    require(not missing,"H18_OFFICIAL_MOJANG_BED_CLASS_MAPPING_MISSING:"+str(missing))
    chosen={name:classes[name] for name in CLASS_NAMES+OPTIONAL_CLASSES if name in classes}
    with ZipFile(client) as z:
        for name in CLASS_NAMES:
            path=classes[name].replace(".","/")+".class"
            require(path in z.namelist(),"H18_OFFICIAL_CLIENT_MAPPED_CLASS_MISSING_"+name)
    bed_class=CLASS_NAMES[0]
    register_class=CLASS_NAMES[1]
    dispatch_class=CLASS_NAMES[2]
    bed_dump=javap_output(client,classes[bed_class],java_tool)
    register_dump=javap_output(client,classes[register_class],java_tool)
    dispatch_dump=javap_output(client,classes[dispatch_class],java_tool)
    bed_owner=classes[bed_class].replace(".","/")
    bed_refs=class_ref_lines(register_dump,bed_owner)
    require(len(bed_refs)>0,"H18_ORIGINAL_BLOCK_ENTITY_RENDERER_REGISTRY_NO_BED_RENDERER_REF")
    require("<init>" in bed_dump and "Code:" in bed_dump,
            "H18_BED_RENDERER_HAS_NO_COMPILED_CONSTRUCTOR_OR_CODE")
    require("Code:" in register_dump and "Code:" in dispatch_dump,
            "H18_NO_COMPILED_RENDERER_REGISTRY_OR_DISPATCH_BYTECODE")
    known_related={}
    for k,v in chosen.items():
        if k in CLASS_NAMES:
            continue
        lines=class_ref_lines(bed_dump,v)
        known_related[k]={"mapped_obfuscated":v,
                          "bed_renderer_classfile_ref_count":len(lines)}
    # Mapped classfile references establish a concrete static registry-to-
    # renderer link. The earlier PNG is a separate actual-client observation.
    # Do not invent a completed live JVM invocation or UV-to-pixel proof.
    return {
        "schema":"MCFR_INT4_H18_MOJANG_12111_V11_BED_RENDERER_CLASSFILE_LINK_V1",
        "status":"PASS_PINNED_OFFICIAL_MOJANG_MAPPING_BED_RENDERER_REGISTRY_STATIC_BYTECODE_LINK",
        "official_inputs":preflight,
        "original_v11_source":old,
        "original_class_mappings":chosen,
        "verified_compiled_bed_renderer_class":classes[bed_class].replace(".","/")+".class",
        "verified_compiled_registry_class":classes[register_class].replace(".","/")+".class",
        "verified_compiled_dispatcher_class":classes[dispatch_class].replace(".","/")+".class",
        "registry_to_bed_renderer_owner_references":len(bed_refs),
        "registry_reference_evidence_lines":bed_refs[:15],
        "bed_renderer_compiled_bytecode_sha256":sha256(bed_dump.encode("utf-8")),
        "registry_javap_sha256":sha256(register_dump.encode("utf-8")),
        "dispatcher_javap_sha256":sha256(dispatch_dump.encode("utf-8")),
        "bed_renderer_related_mapped_class_references":known_related,
        "previous_actual_game_run":45103243455,
        "previous_actual_game_F2_count":4,
        "new_actual_game_runs":0,
        "jvm_render_method_invocation_during_V11_F2_traced":False,
        "registered_class_compiled_bytecode_proof":True,
        "geometry_from_regular_bed_block_model":False,
        "bed_model_geometry_and_per_face_UV_from_BedRenderer_extracted":False,
        "game_renderer_pixel_exact_causal_approved":False,
        "H03":"HOLD","H05":"CONDITIONAL","F70_conditional":70,"F70_unconditional":0,
        "INT5_semantic_approvals":0,"INT6_AI_training_and_asset_redistribution_approvals":0,
        "limits":[
            "Official Mojang 1.21.11 version metadata SHA1, client SHA1+SHA256 and client_mappings SHA1 are exact checked.",
            "Classfile registration reference is STATIC compiled code evidence, not live invocation tracing in the original V11 F2 session.",
            "Mapped renderer class and related model classes are not full geometry, UV sampler, or GPU per-pixel causal evidence.",
            "Existing 4 native F2/screenshots and two server states are taken from the pinned previous Git research ledger; not rerun or newly independently opened in H18.",
            "Official client JAR, mappings and full javap disassembly remain temporary and are never committed/uploaded.",
        ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--version-json",required=True,type=Path)
    p.add_argument("--client-mappings",required=True,type=Path)
    p.add_argument("--official-client",required=True,type=Path)
    p.add_argument("--prior-V11",default=Path(ORIGINAL_V11),type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    a=p.parse_args()
    result=audit(a.version_json,a.client_mappings,a.official_client,a.prior_V11,a.javap)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
        "status","original_class_mappings","registry_to_bed_renderer_owner_references",
        "new_actual_game_runs","jvm_render_method_invocation_during_V11_F2_traced")},
        ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
