#!/usr/bin/env python3
"""Offline verifier for Minecraft Java 1.21.11 official client files.
Usage: python VERIFY_OFFICIAL_JAR.py manifest.json 1.21.11.json client.jar STATE.json
Supply authentic Mojang HTTPS manifest and matching files separately.
This does NOT run the game or certify rendered UV/lighting.
"""
import hashlib, json, sys, zipfile
from pathlib import Path
VERSION="1.21.11"
END={"deepslate_top":"9f2f5e0a67b4a007244cf7064e09da7e693322cfd21b1884190bcd6b26e91aec","blackstone_top":"9eb9bce7a27defc49dd8a2b2dc74f4c7710dc3bbcaa5108a6c1193c82922935d"}
def digest(p,algorithm):
    h=hashlib.new(algorithm)
    with open(p,"rb") as f:
        for part in iter(lambda:f.read(1<<20),b""):h.update(part)
    return h.hexdigest()
def main(args):
    if len(args)!=4:raise SystemExit(__doc__)
    manifest,version,client,state=map(Path,args)
    m=json.loads(manifest.read_text(encoding="utf-8"))
    candidates=[x for x in m["versions"] if x["id"]==VERSION and x["type"]=="release"]
    if len(candidates)!=1:raise ValueError("Manifest version ambiguity")
    mh=digest(version,"sha1")
    if mh!=candidates[0]["sha1"]:raise ValueError("Version JSON SHA-1 does not match manifest")
    v=json.loads(version.read_text(encoding="utf-8"))
    if v.get("id")!=VERSION:raise ValueError("Version mismatch")
    expected=v["downloads"]["client"]
    observed=digest(client,"sha1")
    if observed!=expected["sha1"] or client.stat().st_size!=expected["size"]:
        raise ValueError("JAR SHA-1 or byte count mismatch")
    s=json.loads(state.read_text(encoding="utf-8"))
    if s["stage_id"]!="1-1-02" or len(s["items"])!=17:raise ValueError("Wrong stage scope")
    result=[]
    with zipfile.ZipFile(client) as z:
        for it in s["items"]:
            p=z.read(it["source_path"])
            actual=hashlib.sha256(p).hexdigest()
            result.append({"item_id":it["item_id"],"texture_id":it["texture_id"],"jar_png_sha256":actual,
                           "matches_legacy_mirror":actual==it["v4_sha256"]})
        extra={}
        for name,sha in END.items():
            p=z.read("assets/minecraft/textures/block/"+name+".png")
            got=hashlib.sha256(p).hexdigest()
            extra[name]={"jar_sha256":got,"matches_mirror":got==sha}
    doc={"version":VERSION,"stage":"1-1-02","jar_sha1":observed,"jar_sha256":digest(client,"sha256"),
         "jar_size_bytes":client.stat().st_size,"version_json_sha1":mh,"official_jar_vs_mirror_png":result,
         "supplemental_end_face_checks":extra,
         "jar_origin_note":"caller must establish provenance of downloaded Mojang HTTPS files",
         "ingame_static_render_verified":False,"animation_study_deferred":True}
    print(json.dumps(doc,ensure_ascii=False,indent=2))
    if not all(x["matches_legacy_mirror"] for x in result):raise SystemExit("Some official PNG assets differ from mirror")
if __name__=="__main__":main(sys.argv[1:])
