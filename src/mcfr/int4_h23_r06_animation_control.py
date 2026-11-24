"""H23 controlled original vs frozen water texture in disposable real clients.

Only .mcmeta is changed: one frame (0), no PNG/class/model change. Reuse
the existing exact S43 fixture/camera/capture implementation. Old three F2
are not assigned exact frame indices; new A/B captures test causality.
"""
import argparse
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
from . import int4_f11e_r06_macaw_sink_temporal_capture as r
from . import int4_macaw_kitchen_capture as k
TEX="assets/mcwfurnitures/textures/block/water_still.png"
META=TEX+".mcmeta"
PNG_SHA="d5d63ddd36311d6b064123750715fe551fbeccb5cb1f677ef93027e9305791de"
META_SHA="e9b8025fde1b09b0a4d2a38427b04f98f28a593045be6d177eb2b29164c872b0"
BASE=Path("project/integration/INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json")
CAPTURE="INT4_H23_CONTROL_CAPTURE.json"
def req(ok,msg):
    if not ok:raise ValueError("H23 "+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def freeze(jar,mode):
    req(mode in ("original","frozen"),"unknown experiment mode")
    raw=jar.read_bytes()
    req(sha(raw)==k.MACAW_SHA256,"original JAR pin")
    with ZipFile(io.BytesIO(raw)) as z:
        req(z.testzip() is None and len(z.namelist())==len(set(z.namelist())),"original archive")
        entries=z.infolist()
        old={n:z.read(n) for n in z.namelist()}
    req(sha(old[TEX])==PNG_SHA and sha(old[META])==META_SHA,"texture source pin")
    req(json.loads(old[META])=={"animation":{"frametime":2}},"original animation")
    with Image.open(io.BytesIO(old[TEX])) as im:
        req(im.size==(16,512),"original sprite dimensions")
        rgba=im.convert("RGBA")
        frames=[rgba.crop((0,i*16,16,(i+1)*16)).tobytes() for i in range(32)]
        crops=[rgba.crop((1,i*16+2,13,i*16+11)).tobytes() for i in range(32)]
    req(len(set(frames))>1 and len(set(crops))>1,"no actual source animation changes")
    changed=[]
    if mode=="frozen":
        replacement=json.dumps({"animation":{"frametime":2,"frames":[0]}},separators=(",",":")).encode()
        out=jar.with_suffix(".tmp")
        with ZipFile(out,"w") as z:
            for e in entries:z.writestr(e,replacement if e.filename==META else old[e.filename])
        with ZipFile(out) as z:
            req(z.testzip() is None and z.namelist()==list(old),"patched archive")
            changed=[n for n in old if z.read(n)!=old[n]]
            req(changed==[META],"only animation metadata may change")
        out.replace(jar)
    return {"mode":mode,"official_original_jar_sha256":sha(raw),"runtime_jar_sha256":sha(jar.read_bytes()),
            "changed_members":changed,"original_texture_sha256":PNG_SHA,"original_mcmeta_sha256":META_SHA,
            "source_frames":32,"distinct_source_frames":len(set(frames)),"distinct_source_uv_crops":len(set(crops)),
            "source_uv":[1,2,13,11],"declared_frame_time_ticks":2,"selected_frame_indices":[0] if mode=="frozen" else list(range(32))}
def capture(command,env,game,output,version):
    mode=os.environ.get("MCFR_H23_MODE")
    original=k.validate_running_source(Path(game)/"mods")
    jar=Path(game)/"mods"/original["mod_jar"]
    intervention=freeze(jar,mode)
    # r.capture normally reopens and validates the original installed JAR.
    # The already verified original source registry is reused ONLY for this
    # isolated temporary test; actual modified JAR is separately byte-audited.
    validate=k.validate_running_source
    try:
        def verified(mods):
            req(Path(mods).resolve()==jar.parent.resolve() and sha(jar.read_bytes())==intervention["runtime_jar_sha256"],"runtime JAR changed after preflight")
            return original
        k.validate_running_source=verified
        report=r.capture(command,env,game,output,version)
    finally:k.validate_running_source=validate
    root=Path(output)
    log=(root/"client.log").read_text(encoding="utf-8",errors="replace")
    req(any("Reloading ResourceManager:" in line and "mcwfurnitures" in line for line in log.splitlines()),"Macaw resource reload absent")
    # Validate the original capture pipeline without relabeling frozen JAR as official.
    result=r.audit(root)
    out={"intervention":intervention,"capture":result,"actual_runtime_jar_differs_from_official":mode=="frozen"}
    (root/CAPTURE).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    return report
def analyze(original,frozen,out):
    dirs={"original":Path(original),"frozen":Path(frozen)}
    data={};images={}
    for mode,path in dirs.items():
        d=json.loads((path/CAPTURE).read_text());p=d["intervention"];c=d["capture"]
        req(p["mode"]==mode and p["official_original_jar_sha256"]==k.MACAW_SHA256 and p["changed_members"]==([META] if mode=="frozen" else []),"control intervention")
        req((p["runtime_jar_sha256"]!=k.MACAW_SHA256)==(mode=="frozen"),"runtime identity")
        req(p["original_texture_sha256"]==PNG_SHA and p["original_mcmeta_sha256"]==META_SHA and p["selected_frame_indices"]==([0] if mode=="frozen" else list(range(32))),"source control")
        req(c==r.audit(path),"native F2 re-audit mismatch")
        req(c["real_exact_server_state_checks"]==3 and c["original_native_F2_count"]==3,"same-state controls")
        ims={}
        for key in r.ORDER:
            with Image.open(path/(key+".png")) as im:ims[key]=im.convert("RGB")
        images[mode]=ims
        pairs={}
        for a,b in itertools.combinations(r.ORDER,2):
            x,y=ims[a],ims[b];aa=x.load();bb=y.load()
            coords=[(i,j) for j in range(x.height) for i in range(x.width) if max(abs(t-u) for t,u in zip(aa[i,j],bb[i,j]))>=24]
            def inroi(pt,roi):return roi[0]<=pt[0]<roi[2] and roi[1]<=pt[1]<roi[3]
            water=[pt for pt in coords if inroi(pt,r.WATER_ROI)]
            blue=lambda p:p[2]>p[0]+35 and p[2]>p[1]+10 and p[2]>100
            pairs[a+"_"+b]={"water_changed":len(water),"water_both_blue":sum(blue(aa[pt]) and blue(bb[pt]) for pt in water),
              "sink_nonwater_changed":sum(inroi(pt,r.SINK_ROI) and not inroi(pt,r.WATER_ROI) for pt in coords),
              "stone_changed":sum(inroi(pt,r.STONE_CONTROL_ROI) for pt in coords)}
        data[mode]={"intervention":p,"capture":c,"pair_diffs":pairs}
    orig=list(data["original"]["pair_diffs"].values());freeze=list(data["frozen"]["pair_diffs"].values())
    passed=(sum(x["water_changed"]>0 for x in orig)>=2 and all(x["water_changed"]==x["water_both_blue"] and x["sink_nonwater_changed"]==x["stone_changed"]==0 for x in orig) and all(x["water_changed"]==x["sink_nonwater_changed"]==x["stone_changed"]==0 for x in freeze))
    # Cross-session controls: non-water furniture and stone must match.
    cross=r.pixel_delta(images["original"][r.ORDER[0]],images["frozen"][r.ORDER[0]],r.STONE_CONTROL_ROI)
    x,y=images["original"][r.ORDER[0]],images["frozen"][r.ORDER[0]]
    nonwater=0
    for j in range(r.SINK_ROI[1],r.SINK_ROI[3]):
        for i in range(r.SINK_ROI[0],r.SINK_ROI[2]):
            if r.WATER_ROI[0]<=i<r.WATER_ROI[2] and r.WATER_ROI[1]<=j<r.WATER_ROI[3]:continue
            nonwater+=max(abs(a-b) for a,b in zip(x.getpixel((i,j)),y.getpixel((i,j))))>=24
    passed=passed and cross==nonwater==0
    report={"schema":"MCFR_INT4_H23_R06_CONTROLLED_ANIMATION_METADATA_V1","status":"PASS_R06_CONTROLLED_ANIMATION_SCOPE" if passed else "CONDITIONAL_R06_CONTROL_INCONCLUSIVE",
      "source_H22_git_blob":hashlib.sha1(b"blob "+str(len(BASE.read_bytes())).encode()+b"\0"+BASE.read_bytes()).hexdigest(),
      "sessions":data,"cross_session_stone_changed":cross,"cross_session_sink_nonwater_changed":nonwater,
      "new_game_runs":2,"new_F2":6,"R06_animation_source_causal_scope":passed,
      "old_F2_exact_frame_index_proven":False,"exact_GPU_texel_causality":False,"legacy_F70_unconditional":0,"INT5":0,"INT6":0,
      "limits":["Original and frozen metadata in separately started disposable clients, same exact state and camera; no old-frame index or full GPU proof.",
        "Changes below RGB24 threshold not excluded. No original JAR or PNG distributed."]}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("H23_RESULT",json.dumps(report,sort_keys=True,separators=(",",":")))
    req(passed,"controlled difference not established; keep conditional")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for n in ("original","frozen","output"):p.add_argument("--"+n,required=True)
    a=p.parse_args();analyze(a.original,a.frozen,a.output)
