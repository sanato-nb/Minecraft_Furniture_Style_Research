#!/usr/bin/env python3
"""Independent source-coordinate vs actual Blender mesh-loop check for R03."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(values):
    return tuple(round(float(x),6) for x in values)


def expected_face(face):
    # hoa / hoa$a / hoa$b confirmed by run 46120428348.
    a,b,c = face["from"]
    d,e,f = face["to"]
    vertices = {
        "down": [(a,b,f),(a,b,c),(d,b,c),(d,b,f)],
        "up": [(a,e,c),(a,e,f),(d,e,f),(d,e,c)],
        "north": [(d,e,c),(d,b,c),(a,b,c),(a,e,c)],
        "south": [(a,e,f),(a,b,f),(d,b,f),(d,e,f)],
        "west": [(a,e,c),(a,b,c),(a,b,f),(a,e,f)],
        "east": [(d,e,f),(d,b,f),(d,b,c),(d,e,c)],
    }[face["direction"]]
    # Independent X180 position transform and UV origin conversion.
    return {key(((x-8)/16,(z-8)/16,(8-y)/16)):key((u/16,1-v/16))
            for (x,y,z),(u,v) in zip(vertices,face["expected_locked_canonical_uv"])}


def check_mode(renderer, instance, ref):
    renderer.reset_scene()
    results = []
    for i, element in enumerate(instance["elements"]):
        mesh = renderer.make_element(element, instance, i).data
        actual = []
        for p in mesh.polygons:
            actual.append({key(mesh.vertices[mesh.loops[j].vertex_index].co):
                           key(mesh.uv_layers.active.data[j].uv) for j in p.loop_indices})
        faces = [f for f in ref["faces"] if f["element"] == i]
        assert len(actual) == len(faces)
        consumed = set()
        for f in faces:
            expected = expected_face(f)
            matches = [j for j, m in enumerate(actual) if set(m) == set(expected)]
            assert len(matches) == 1 and matches[0] not in consumed, (i,f["direction"],matches)
            consumed.add(matches[0])
            found = actual[matches[0]]
            loops = [{"position":list(p),"expected":list(uv),"actual":list(found[p]),
                      "pass":found[p]==uv} for p,uv in expected.items()]
            results.append({"element":i,"face":f["direction"],"source_uv_changed":f["changed"],
                            "loops":loops,"pass":all(x["pass"] for x in loops)})
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--report",type=Path,required=True)
    args = p.parse_args(sys.argv[sys.argv.index("--")+1:])
    sys.path.insert(0,str(args.repo/"scripts/tv001"))
    import blender_batch as renderer
    refpath = args.repo/"project/audits/tv001/TV001_B_R03_UV_REFERENCE_2026-11-28.json"
    ref, manifest = read(refpath),read(args.manifest)
    assert manifest["source_commit"] == ref["source_pin"]
    jobs = [j for j in manifest["jobs"] if j["id"] == "R03-inner"]
    assert len(jobs)==1 and len(jobs[0]["instances"])==1
    inst = jobs[0]["instances"][0]
    assert (inst["x"],inst["y"],inst["uvlock"])==(180,0,True)
    assert len(inst["elements"])==3 and len(ref["faces"])==15
    for f in ref["faces"]:
        e = inst["elements"][f["element"]]
        face = e["faces"][f["direction"]]
        assert e["from"]==f["from"] and e["to"]==f["to"]
        assert face["uv"]==f["uv"] and face["rotation"]==f["rotation"]
    locked = check_mode(renderer,inst,ref)
    unlocked = copy.deepcopy(inst)
    unlocked["uvlock"]=False
    control = check_mode(renderer,unlocked,ref)
    face_pass = sum(x["pass"] for x in locked)
    loop_pass = sum(l["pass"] for x in locked for l in x["loops"])
    negative = sum(x["source_uv_changed"] and not x["pass"] for x in control)
    status = "PASS" if (len(locked),face_pass,loop_pass,negative)==(15,15,60,11) else "FAIL"
    report = {"status":status,"case":"R03-inner","face_total":len(locked),"face_pass":face_pass,
              "loop_total":sum(len(x["loops"]) for x in locked),"loop_pass":loop_pass,
              "negative_control_changed_faces_rejected":negative,"reference_sha256":sha(refpath),
              "manifest_sha256":sha(args.manifest),"renderer_sha256":sha(Path(renderer.__file__)),
              "source_confirmation_run":46120428348,"faces":locked,"negative_control":control,
              "limits":"Mesh loop association only; no full texture/atlas or per-pixel oracle."}
    args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("TV001_R03_UV_MESH "+json.dumps({k:v for k,v in report.items() if k not in ("faces","negative_control")}))
    if status!="PASS":
        raise SystemExit(1)


if __name__=="__main__":
    main()
