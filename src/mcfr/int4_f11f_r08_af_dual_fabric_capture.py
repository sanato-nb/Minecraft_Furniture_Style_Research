"""INT-4-F11F R08: same Fabric loader, official 4.0.2 vs pinned source-built 4.0.3.

Do not present source-built 4.0.3 as an official Modrinth Fabric release:
at the time of review, the author's published 4.0.3 file uses NeoForge.
The upstream 4.0.3 commit contains explicit Fabric module and Gradle build.
Only one acacia_chair north variant=1 state is selected per identical-camera
Minecraft 1.21.1 run, to avoid extrapolating all 88 blockstate variants.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
from zipfile import ZipFile
from .chair_runtime_fixture import ChairCase,digest_bytes
from .chair_runtime_capture import capture_chairs

UPSTREAM="57eb624cbb7f408d43398c7434b0d38d312cb55d"
VERSION="1.21.1"
BLOCK="another_furniture:acacia_chair"
SOURCE_VERSION="4.0.3"
OFFICIAL_FABRIC_VERSION="4.0.2"
BUILT_SOURCE_KIND="PINNED_GIT_COMMIT_FABRIC_SOURCE_BUILT_NOT_OFFICIAL_RELEASE"
BASE_KIND="OFFICIAL_MODRINTH_FABRIC_RELEASE_4_0_2"
OFFICIAL_JAR="another_furniture-fabric-4.0.2.jar"
BUILT_JAR="another_furniture-fabric-4.0.3-study-source.jar"
PINNED_OFFICIAL_JAR_SHA1="c2f992081bdc4795ed6d87771a3b5f7c71103785"
ORIGINAL_STUDY_STATE_BLOB="37643398d7a49fdcfc6f2308ca04c13fb0b43aed"
ORIGINAL_STUDY_LEAF_BLOB="609dea1eda246be610ed0a5762f3bb5f0ce9db92"
OFFICIAL_RUNTIME_STATE_BLOB="3a806533856f169a502373bda43a76eeabc1e689"
STATE_PATH="assets/another_furniture/blockstates/acacia_chair.json"
MODEL_PATH="assets/another_furniture/models/block/chair/acacia_1.json"
MANIFEST="INT4_F11F_R08_SINGLE_FABRIC_RELEASE_NATIVE_F2.json"
BLOCK_STATE="another_furniture:acacia_chair[facing=north,tucked=false,variant=1]"
MODEL_TARGET="another_furniture:block/chair/acacia_1"
CASE_ID="R08_acacia_north_variant1"

def sha(b):return hashlib.sha256(b).hexdigest()
def verify(x,msg):
    if not x:raise ValueError(msg)

def original_case():
    return (ChairCase(CASE_ID,VERSION,"AF121",BLOCK,"tucked=false,variant=1",
                      "north",0,120,40),)

def models():
    return {CASE_ID:{"model":MODEL_TARGET,"y":0}}

def source_metadata(jar,kind):
    path=Path(jar)
    verify(path.is_file(),"Missing AF version test JAR: "+str(path))
    data=path.read_bytes()
    with ZipFile(path) as z:
        verify(z.testzip() is None,"AF JAR corrupted")
        verify(STATE_PATH in z.namelist() and MODEL_PATH in z.namelist(),
               "Missing original study 4.0.3 chair model or exact blockstate")
        state=z.read(STATE_PATH); leaf=z.read(MODEL_PATH)
        meta=json.loads(z.read("fabric.mod.json"))
        release=json.loads(state)["variants"].get("facing=north,tucked=false,variant=1")
    verify(meta["id"]=="another_furniture","Wrong target mod")
    verify(meta["version"]==(OFFICIAL_FABRIC_VERSION if kind=="official" else SOURCE_VERSION),
           "Incorrect version in built Fabric mod metadata")
    verify(release is not None and release.get("model")==MODEL_TARGET and
           release.get("y",0)==0 and not release.get("uvlock",False),
           "Exact original 4.0.3 acacia chair state model selection mismatch")
    s=digest_bytes(state,"GIT_BLOB_SHA1")
    m=digest_bytes(leaf,"GIT_BLOB_SHA1")
    if kind=="official":
        verify(hashlib.sha1(data).hexdigest()==PINNED_OFFICIAL_JAR_SHA1,
               "4.0.2 official original JAR changed")
        verify(s==OFFICIAL_RUNTIME_STATE_BLOB,
               "Official 4.0.2 acacia chair blockstate original source changed")
    elif kind=="study_source_build":
        verify(s==ORIGINAL_STUDY_STATE_BLOB and m==ORIGINAL_STUDY_LEAF_BLOB,
               "Built 4.0.3 study Git resource does not equal frozen original Git SHA")
    else:
        raise ValueError("Only official/verified source-built release kinds allowed")
    return {
      "installed_jar_sha256":sha(data),
      "installed_jar_sha1":hashlib.sha1(data).hexdigest(),
      "jar_file":path.name,
      "release_kind":(BASE_KIND if kind=="official" else BUILT_SOURCE_KIND),
      "version":meta["version"],
      "minecraft":VERSION,
      "selected_exact_original_state":BLOCK_STATE,
      "selected_model":release["model"],
      "selected_y":release.get("y",0),
      "selected_blockstate_git_blob_sha1":s,
      "selected_model_git_blob_sha1":m,
      "source_study_Git_commit":UPSTREAM if kind=="study_source_build" else None,
      "not_an_official_published_Fabric_4_0_3":kind=="study_source_build",
    }

def install_research_jar(args,game):
    moddir=Path(game)/"mods"
    original=moddir/OFFICIAL_JAR
    verify(original.is_file(),"Original officially pinned 4.0.2 JAR not downloaded")
    source_metadata(original,"official")
    selected=getattr(args,"af_source_jar",None)
    if selected:
        incoming=Path(selected).resolve()
        verify(incoming.is_file() and incoming.parent!=moddir,
               "Require independently built 4.0.3 JAR outside original mods")
        source_metadata(incoming,"study_source_build")
        dest=moddir/BUILT_JAR
        verify(not dest.exists(),"Source replacement destination not scratch-clean")
        original.unlink()
        shutil.copyfile(incoming,dest)
        verify(len(list(moddir.glob("another_furniture*.jar")))==1,
               "Unexpected AF JAR mixture")
        return source_metadata(dest,"study_source_build")
    verify(len(list(moddir.glob("another_furniture*.jar")))==1,
           "Original 4.0.2 release JAR not isolated")
    return source_metadata(original,"official")

def capture(command,env,game,output,version):
    verify(version==VERSION,"Must be pinned original Minecraft 1.21.1")
    af=list((Path(game)/"mods").glob("another_furniture*.jar"))
    verify(len(af)==1,"Require exactly one active Another Furniture JAR")
    kind="official" if af[0].name==OFFICIAL_JAR else "study_source_build"
    meta=source_metadata(af[0],kind)
    result=capture_chairs(command,env,game,output,version,
                          selected_cases=original_case(),
                          expected_case_models=models())
    item=result["states"][0]
    verify(item["case_id"]==CASE_ID and item["original_state"]==BLOCK_STATE and
           item["server_blockstate_verified"] is True and
           item["original_model_target"]==MODEL_TARGET,
           "Source-only model & real server state diverged")
    img=Path(output)/(CASE_ID+".png")
    verify(img.is_file() and sha(img.read_bytes())==item["screenshot_sha256"],
           "Native original client F2 lost")
    original_log=Path(output)/"client.log"
    report={
       "schema":"MCFR_INT4_F11F_R08_SINGLE_FABRIC_SOURCE_ACTUAL_GAME/v1",
       "status":"ONE_REAL_FABRIC_SOURCE_RELEASE_F2_CAPTURED_NOT_CROSS_RELEASE_APPROVED",
       "risk_case":"R08","minecraft":VERSION,
       "release":meta,"native_F2_name":img.name,
       "native_F2_sha256":item["screenshot_sha256"],
       "native_F2_dimensions":item["screenshot_dimensions"],
       "actual_server_original_state_PASS":True,
       "client_log_sha256":sha(original_log.read_bytes()),
       "source_4_0_3_is_official_Fabric_distribution":False,
       "full_F_unconditionally_approved":False,
       "INT5_semantics_approved":False,
       "INT6_AI_training_redistribution_approved":False,
       "limitations":[
           "A source-built Fabric 4.0.3 is not an officially released 4.0.3 Fabric artifact.",
           "Actual 4.0.2 Fabric is original Modrinth SHA1-pinned release.",
           "One north variant1 state only, not 88-state equivalence.",
           "Native F2s are not pixel-perfect aligned UV proofs.",
           "4.0.3 NeoForge published release not run in this same-loader test.",
       ],
    }
    (Path(output)/MANIFEST).write_text(
        json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report
