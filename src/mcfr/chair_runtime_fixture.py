"""Actual Minecraft chair visual fixture: conservative source-pinned world and pack.

This is NOT a substitute for a real Minecraft client screenshot. The pack
materializes the four chosen PR #32 models in all 4 source facings, then records
per-block server confirmation. For CI, a *local-only* vanilla dedicated server
creates a new flat creative world; the original world never gets modified.

Only after the game actually places all specified states and F2 creates complete
PNG images may the capture phase claim CLIENT_CAPTURED, not semantic approval.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict,dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse

from .foundation import ROOT

DIRS=("north","east","south","west")
X=(-24,-8,8,24)
Y=120

# Namespaced block IDs, state property strings, and source identity are fixed
# to original model choices in the PR #32 blockstate evidence. Do not invent
# Macaw's north=0 model rotation: Macaw has a source y=90 for north.
CHAIRS={
    "1.21.1":(
        ("AF121","another_furniture:acacia_chair","tucked=false,variant=1",40),
        ("AF123","another_furniture:acacia_chair","tucked=true,variant=10",54),
        ("HC11210","handcrafted:warped_chair","color=black,waterlogged=false",68),
    ),
    "1.21.11":(
        ("MACAW67","mcwfurnitures:acacia_chair","",40),
    ),
}
ORIGINAL_BLOCKSTATE={
  "1.21.1":{
    "another_furniture:acacia_chair":{
      "file":"acacia_chair.json",
      "sha":"37643398d7a49fdcfc6f2308ca04c13fb0b43aed",
      "algorithm":"GIT_BLOB_SHA1"
    },
    "handcrafted:warped_chair":{
      "file":"warped_chair.json",
      "sha":"099f32844f15e104687bac10b4a81635821bc8ce",
      "algorithm":"GIT_BLOB_SHA1"
    }
  },
  "1.21.11":{
    "mcwfurnitures:acacia_chair":{
      "file":"acacia_chair.json",
      "sha":"e6405186a33100104cb6dcbddd2cad774f157298cafe8e750dc228cd9ba24b95",
      "algorithm":"SHA256"
    }
  }
}

def source_pose_manifest(root:Path):
    path=root/"project/integration/INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json"
    result=json.loads(path.read_text(encoding="utf-8"))
    assert result["totals"]["original_model_options"]==228
    return result,hashlib.sha256(path.read_bytes()).hexdigest()

def source_direction_rows(root:Path):
    """Source 16 model/selector/y poses from full fixed F source option data.

    Requires explicit 16 direction source CSV; do not read a guessed mapping
    from resource names or assume 0deg north for all mods.
    """
    import csv
    path=root/"project/integration/INT3_CHAIR_16_ORIENTATION_POSES.csv"
    if not path.exists():
        # The complete CSV is a short-lived CI artifact in PR #32. The
        # equivalent pinned source details are in the Git summary, but this
        # fixture only needs selector identity from its explicit configurations.
        return None
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

@dataclass(frozen=True)
class ChairCase:
    case_id:str
    version:str
    model_key:str
    block_id:str
    selector:str
    facing:str
    x:int
    y:int
    z:int
    def state(self):
        return f"{self.block_id}[facing={self.facing}"+(","+self.selector if self.selector else "")+"]"
    def camera(self):
        # Camera south of the chair, looking north; all facings use the same
        # observer geometry. This will not match the diagnostic projection
        # pixel-for-pixel, which is why only source/state evidence is automatic.
        return f"{self.x+0.5:g} {self.y+2.3:g} {self.z+5.5:g} 180 20"

def cases(version):
    if version not in CHAIRS:
        raise ValueError("Unsupported pinned Minecraft client: "+version)
    items=[]
    for key,block,params,z in CHAIRS[version]:
        for facing,x in zip(DIRS,X):
            case_id=f"{key}_{facing}"
            items.append(ChairCase(case_id,version,key,block,params,facing,x,Y,z))
    assert len({item.case_id for item in items})==len(items)
    return tuple(items)

def digest_bytes(blob,method):
    if method=="SHA256":return hashlib.sha256(blob).hexdigest()
    if method=="GIT_BLOB_SHA1":
        return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()
    raise ValueError("Unsupported source blob hash kind "+method)

def verify_installed_mod_sources(version,mod_dir):
    """Source model rules in the actual Fabric JAR must match source-pinned F.

    One of these jars may have been released at 4.0.2 whereas the research
    used 4.0.3. It is NOT safe to assume the files match without reopening.
    """
    from zipfile import ZipFile
    checked={}
    for resource,expected in ORIGINAL_BLOCKSTATE[version].items():
        namespace=resource.split(":",1)[0]
        internal=f"assets/{namespace}/blockstates/{expected['file']}"
        matches=[]
        for jar in sorted(mod_dir.glob("*.jar")):
            with ZipFile(jar) as archive:
                if internal in archive.namelist():
                    matches.append((jar,archive.read(internal)))
        if len(matches)!=1:
            raise ValueError(f"Original {resource} blockstate must appear in exactly one pinned Fabric JAR, got {len(matches)}")
        jar,blob=matches[0]
        digest=digest_bytes(blob,expected["algorithm"])
        if digest!=expected["sha"]:
            raise ValueError(f"Runtime mod JAR source blockstate differs from audited PR #32: {resource} got {digest}")
        checked[resource]={"jar":jar.name,"internal_path":internal,
                           "source_hash":digest,"algorithm":expected["algorithm"]}
    return checked

def pack_lines(version):
    placed=[
        "time set noon",
        "weather clear",
        "difficulty peaceful",
        "gamerule doDaylightCycle false",
        "gamerule doWeatherCycle false",
        "forceload add -28 36 28 72",
    ]
    for item in cases(version):
        # Only local simple single-block source states; no neighboring block
        # connection, linked furniture behavior or direction auto-correction.
        placed.extend((
           f"fill {item.x-3} {item.y-1} {item.z-3} {item.x+3} {item.y-1} {item.z+3} minecraft:smooth_stone",
           f"setblock {item.x} {item.y} {item.z} {item.state()}",
        ))
    placed.append("say MCFR_CHAIR_PLACED")
    verify=[]
    for item in cases(version):
        verify.append(
            f"execute if block {item.x} {item.y} {item.z} {item.state()} run say MCFR_CHAIR_STATE_{item.case_id}=PASS"
        )
        verify.append(
            f"execute unless block {item.x} {item.y} {item.z} {item.state()} run say MCFR_CHAIR_STATE_{item.case_id}=FAIL"
        )
    verify.append("say MCFR_CHAIR_STATES_READ")
    return tuple(placed),tuple(verify)

def make_pack(version,pack):
    pack=Path(pack)
    if pack.exists():
        raise FileExistsError("Cannot overwrite an existing runtime datapack: "+str(pack))
    functions=pack/"data/mcfr_chair/function"
    functions.mkdir(parents=True,exist_ok=False)
    packmeta={"pack":{"description":"MCFR source-pinned 4 model / 16 facing chair visual fixture"}}
    if version=="1.21.1":
        packmeta["pack"]["pack_format"]=48
    elif version=="1.21.11":
        packmeta["pack"].update({"min_format":[94,1],"max_format":[94,1]})
    else:
        raise ValueError("Unsupported Minecraft version: "+version)
    (pack/"pack.mcmeta").write_text(json.dumps(packmeta,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    placed,checks=pack_lines(version)
    (functions/"place.mcfunction").write_text("\n".join(placed)+"\n",encoding="utf-8")
    (functions/"verify.mcfunction").write_text("\n".join(checks)+"\n",encoding="utf-8")
    return {
      "status":"PINNED_CHAIR_GAME_FIXTURE_GENERATED_NOT_CAPTURED",
      "version":version,
      "test_cases":len(cases(version)),
      "models":sorted({item.model_key for item in cases(version)}),
      "source_state_expected":{item.case_id:item.state() for item in cases(version)},
      "source_camera":{item.case_id:item.camera() for item in cases(version)},
      "files_sha256":{
        p.relative_to(pack).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(pack.rglob("*")) if p.is_file()
      },
      "real_client_screenshots":0,
      "runtime_state_confirmations":0,
      "study_visual_role_approved":0,
    }

def create_world(version,world,cache,timeout=180):
    """Create local Creative flat world with official Mojang server, no prior world.

    The server is bound to loopback and immediately shut down after generating
    the save. It is not a public server or a persistent automation.
    """
    from .runtime import ROOT as repository
    # Uses the same existing upstream downloader and pinned version client
    # model so no second install/update mechanism is introduced.
    import runpy
    path=repository/"research/furniture_mods/phase_1-3/runtime_actions/run_probe.py"
    module=runpy.run_path(str(path))
    download=module["download"]
    manifest=json.loads(download("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json",
                                 cache/"manifest.json").read_bytes())
    version_entry=next((v for v in manifest["versions"] if v["id"]==version),None)
    if version_entry is None:raise ValueError("Official version unavailable "+version)
    spec=json.loads(download(version_entry["url"],cache/(version+"-version.json"),version_entry["sha1"]).read_bytes())
    if spec["downloads"]["client"]["sha1"]!=module["CLIENTS"][version]:
        raise ValueError("Official server metadata not paired with pinned client version")
    server=spec["downloads"]["server"]
    jar=download(server["url"],cache/(version+"-server.jar"),server["sha1"])
    session=cache/(version+"-world-session")
    if session.exists() or world.exists():
        raise FileExistsError("Use new scratch server session and destination world")
    session.mkdir(parents=True)
    (session/"eula.txt").write_text("eula=true\n",encoding="utf-8")
    (session/"server.properties").write_text(
        "level-name=world\nlevel-type=minecraft:flat\nlevel-seed=37\n"
        "gamemode=creative\nforce-gamemode=true\ndifficulty=peaceful\n"
        "generate-structures=false\nspawn-protection=0\n"
        "server-ip=127.0.0.1\nserver-port=25579\n"
        "online-mode=false\nmax-players=1\n"
        "view-distance=4\nsimulation-distance=4\n"
        "enable-command-block=true\n",
        encoding="utf-8"
    )
    proc=subprocess.Popen(["java","-Xmx2G","-XX:ActiveProcessorCount=4",
                           "-jar",str(jar),"nogui"],cwd=session,
                          stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,text=True,bufsize=1)
    from threading import Thread,Event
    ready=Event()
    output=[]
    def watch():
        for line in proc.stdout:
            output.append(line.rstrip())
            if "Done (" in line and "For help" in line:
                ready.set()
    worker=Thread(target=watch,daemon=True)
    worker.start()
    try:
        if not ready.wait(timeout) or proc.poll() is not None:
            raise RuntimeError("Pinned dedicated server failed generating clean world: "+
                               "\n".join(output[-30:]))
        proc.stdin.write("stop\n")
        proc.stdin.flush()
        try:proc.wait(timeout=55)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Vanilla server save did not stop cleanly")
        if proc.returncode!=0:
            raise RuntimeError("Vanilla world server exited with code "+str(proc.returncode))
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        worker.join(timeout=3)
    saved=session/"world"
    if not (saved/"level.dat").is_file():
        raise ValueError("New flat world missing original Minecraft level.dat")
    # Allow commands in the *copied* singleplayer world: the capture script
    # uses /function, /tp and /gamemode. Does not edit any user save.
    try:
        import nbtlib
    except ImportError as e:
        raise RuntimeError("Test world generation requires nbtlib") from e
    level=nbtlib.load(saved/"level.dat")
    level["Data"]["allowCommands"]=nbtlib.tag.Byte(1)
    level["Data"]["GameType"]=nbtlib.tag.Int(1)
    level.save(gzipped=True)
    world.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(saved,world,ignore=shutil.ignore_patterns("session.lock"))
    return {
      "schema":"MCFR_INT3_NEW_FLAT_CLIENT_WORLD/v1",
      "status":"GENERATED_WITH_PINNED_VANILLA_SERVER_NOT_YET_OPENED_BY_CLIENT",
      "minecraft_version":version,
      "server_sha1":server["sha1"],
      "paired_client_sha1":spec["downloads"]["client"]["sha1"],
      "save_level_dat_sha256":hashlib.sha256((world/"level.dat").read_bytes()).hexdigest(),
      "client_captures":0,
      "server_only_bound_to_loopback":True,
      "original_world_modified":False
    }

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    pack=sub.add_parser("pack")
    pack.add_argument("--version",choices=tuple(CHAIRS),required=True)
    pack.add_argument("--path",type=Path,required=True)
    new=sub.add_parser("world")
    new.add_argument("--version",choices=tuple(CHAIRS),required=True)
    new.add_argument("--path",type=Path,required=True)
    new.add_argument("--cache",type=Path,required=True)
    args=parser.parse_args(argv)
    result=(make_pack(args.version,args.path) if args.command=="pack"
            else create_world(args.version,args.path,args.cache))
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
