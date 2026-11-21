"""INT-4: independently traverse the 48 historical missing-parent model paths.

Read only fixed AF 4.0.3 Git archive, Macaw 3.4.2 JAR, two Mojang client
JARs and the historical 1-3 B/INT-2 records. Check original child bytes,
parent resource identity, full reachable chain, alternative model filenames
(as *leads* only), own geometry, and overlap with no-static. Never synthesize
a nonexistent parent or promote a geometry/material/AI-use approval.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[2]
B="research/furniture_mods/phase_1-3/B/source_verification/"
SUM="project/integration/INT2_MOD_SOURCE_SUMMARY.json"
ERR="project/integration/INT2_MOD_EXCEPTIONS.csv"
PINS={
    "MACAW_SHA256":"e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e",
    "MINECRAFT_1211_SHA1":"30c73b1c5da787909b2f73340419fdf13b9def88",
    "MINECRAFT_12111_SHA1":"ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd",
    "AF_COMMIT":"57eb624cbb7f408d43398c7434b0d38d312cb55d",
}
BUILTIN={"minecraft:builtin/generated","minecraft:builtin/entity","minecraft:builtin/missing"}


class OriginalMismatch(ValueError):
    pass


def require(ok,description):
    if not ok:
        raise OriginalMismatch(description)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def sha1blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()


def parse_json(data,name):
    def no_duplicate(pairs):
        row={}
        for key,val in pairs:
            require(key not in row,"Duplicate key "+key+" in "+name)
            row[key]=val
        return row
    x=json.loads(data.decode("utf-8-sig"),object_pairs_hook=no_duplicate)
    require(isinstance(x,dict),"JSON source must be object: "+name)
    return x


def read_csv_bytes(data):
    return list(csv.DictReader(data.decode("utf-8-sig").splitlines()))


def model_rel(resource):
    namespace,sep,name=resource.partition(":")
    require(sep and namespace and name and ".." not in name and
            not name.startswith("/"),"Malformed source resource id")
    return f"assets/{namespace}/models/{name}.json"


class OriginalArchives:
    def __init__(self,af_path,macaw_path,vanilla_1211,vanilla_12111):
        self.paths=(Path(af_path),Path(macaw_path),Path(vanilla_1211),Path(vanilla_12111))
        self.af=self.macaw=self.mc1211=self.mc12111=None
    def __enter__(self):
        af,macaw,m1211,m12111=self.paths
        require(sha256(macaw.read_bytes())==PINS["MACAW_SHA256"],"Macaw release SHA mismatch")
        require(hashlib.sha1(m1211.read_bytes()).hexdigest()==PINS["MINECRAFT_1211_SHA1"],
                "Minecraft 1.21.1 official client SHA mismatch")
        require(hashlib.sha1(m12111.read_bytes()).hexdigest()==PINS["MINECRAFT_12111_SHA1"],
                "Minecraft 1.21.11 official client SHA mismatch")
        self.af=zipfile.ZipFile(af)
        self.macaw=zipfile.ZipFile(macaw)
        self.mc1211=zipfile.ZipFile(m1211)
        self.mc12111=zipfile.ZipFile(m12111)
        require(all(z.testzip() is None for z in (self.af,self.macaw,self.mc1211,self.mc12111)),
                "Original ZIP source CRC verification failed")
        names=[n for n in self.af.namelist() if not n.endswith("/")]
        self.af_index={}
        for path in names:
            base="/common/src/main/resources/"
            if base not in path:continue
            rel=path.split(base,1)[1]
            if rel.startswith("assets/"):
                require(rel not in self.af_index,"AF duplicate common resource path")
                self.af_index[rel]=path
        require(any("models/block/lantern_post_base.json" in n for n in self.af_index),
                "Pinned AF archive lacks expected model source")
        self.macaw_names=set(self.macaw.namelist())
        self.mc1211_names=set(self.mc1211.namelist())
        self.mc12111_names=set(self.mc12111.namelist())
        return self
    def __exit__(self,*args):
        for z in (self.af,self.macaw,self.mc1211,self.mc12111):
            if z:z.close()
    def find(self,mod,resource):
        rel=model_rel(resource)
        if resource.startswith("minecraft:"):
            archive,names=(self.mc12111,self.mc12111_names) if mod=="MACAW" else (self.mc1211,self.mc1211_names)
            return archive.read(rel) if rel in names else None
        if mod=="AF" and resource.startswith("another_furniture:"):
            loc=self.af_index.get(rel)
            return self.af.read(loc) if loc else None
        if mod=="MACAW" and resource.startswith("mcwfurnitures:"):
            return self.macaw.read(rel) if rel in self.macaw_names else None
        raise OriginalMismatch("Unexpected cross-namespace source-model reference "+mod+":"+resource)
    def maybe_basename(self,mod,resource):
        """Possible same-filename leads only. Never count as a valid parent."""
        rel=model_rel(resource)
        basename=rel.rsplit("/",1)[-1]
        universe=self.af_index if mod=="AF" else self.macaw_names
        return sorted(x for x in universe
                      if x.startswith(("assets/another_furniture/" if mod=="AF" else "assets/mcwfurnitures/")+"models/")
                      and x.rsplit("/",1)[-1]==basename and x!=rel)[:12]


def resolve_one(mod,child_resource,originals):
    walk=[]
    current=child_resource
    seen=set()
    first=None
    while True:
        if current in seen:
            return {"terminal_status":"PARENT_CYCLE","terminal_ref":current,"chain":walk}
        seen.add(current)
        if current in BUILTIN:
            return {"terminal_status":"BUILTIN","terminal_ref":current,"chain":walk}
        blob=originals.find(mod,current)
        if blob is None:
            return {"terminal_status":"PARENT_MISSING","terminal_ref":current,"chain":walk,
                    "other_same_basename_paths":originals.maybe_basename(mod,current)
                    if not current.startswith("minecraft:") else []}
        kind="GIT_BLOB_SHA1" if mod=="AF" else ("MOJANG_VANILLA_SHA1_BLOB" if current.startswith("minecraft:") else "SHA256")
        obj=parse_json(blob,current)
        elements=obj.get("elements",[])
        require(isinstance(elements,list),"Original model elements field not list")
        current_faces=sum(len(x.get("faces",{})) for x in elements)
        walk.append({
            "resource_id":current,
            "sha":sha1blob(blob) if kind!="SHA256" else sha256(blob),
            "sha_kind":kind,
            "own_elements":len(elements),"own_faces":current_faces,
            "declared_parent":obj.get("parent", ""),
        })
        if first is None:first=walk[0]
        raw=obj.get("parent")
        if not raw:
            return {"terminal_status":"ROOT","terminal_ref":"","chain":walk}
        require(isinstance(raw,str),"Original model parent reference not string")
        current=raw if ":" in raw else "minecraft:"+raw


def check_history(root,roster):
    d=(root/SUM).read_bytes()
    ex=(root/ERR).read_bytes()
    source=json.loads(d)
    rows=read_csv_bytes(ex)
    require(source["status"]=="PASS_SOURCE_GEOMETRY_CATALOG_SCOPE",
            "Original 1-3 static audit not passed")
    require(source["measures"]["parent_missing"]==48 and
            source["measures"]["no_static_models"]==108 and
            source["measures"]["source_verified_model_files"]==16572,
            "Original 48/108/16572 denominator drift")
    require(sha256(ex)==source["exception_csv_sha256"],
            "Historical exception CSV immutable SHA mismatch")
    missing=[x["resource_id"] for x in rows if x["exception_type"]=="PARENT_MISSING"]
    no_static={x["resource_id"] for x in rows if x["exception_type"]=="NO_STATIC_OR_UNRESOLVED"}
    require(len(missing)==len(set(missing))==48
            and set(missing)==set(source["exceptions"]["missing_parent_paths"]),
            "Historical 48 missing parent paths inconsistent with source audit")
    require(len(no_static)==108 and no_static==set(source["exceptions"]["no_static_model_ids"]),
            "Historical no-static 108 paths do not match their original audit")
    require(set(roster)==set(missing),"48 exception list differs")
    return {"INT2_MOD_SOURCE_SUMMARY.json":sha256(d),
            "INT2_MOD_EXCEPTIONS.csv":sha256(ex)},no_static


def collect_model_pins(root):
    pins={}
    for mod in ("AF","MACAW"):
        path=root/(B+f"B_{mod}_SOURCE_BODIES.csv.gz")
        raw=path.read_bytes()
        with gzip.open(path,"rt",encoding="utf-8-sig",newline="") as f:
            records=list(csv.DictReader(f))
        for row in records:
            if row["family"]=="models":
                raw_path=row["path"]
                prefix="common/src/main/resources/"
                if mod=="AF":
                    require(raw_path.startswith(prefix),
                            "Unexpected original AF source path convention")
                    normalized=raw_path[len(prefix):]
                else:
                    normalized=raw_path
                require(normalized not in pins,
                        "Duplicate historical normalized source file path")
                pins[normalized]=(mod,row["sha"],int(row["bytes"]))
    require(len(pins)==1629+2549,"Historical AF/Macaw source-model population drift")
    return pins,{mod:sha256((root/(B+f"B_{mod}_SOURCE_BODIES.csv.gz")).read_bytes())
                 for mod in ("AF","MACAW")}


def examine(root,archives):
    root=Path(root)
    summary=json.loads((root/SUM).read_text(encoding="utf-8"))
    roster=summary["exceptions"]["missing_parent_paths"]
    original_hashes,no_static=check_history(root,roster)
    pins,pin_shas=collect_model_pins(root)
    originals=archives
    rows=[]
    for resource in roster:
        mod="AF" if resource.startswith("another_furniture:") else "MACAW"
        require(mod=="AF" and resource.startswith("another_furniture:") or
                mod=="MACAW" and resource.startswith("mcwfurnitures:"),
                "Unexpected 48-case source namespace")
        rel=model_rel(resource)
        require(rel in pins,"Original 1-3B inventory missing exception source file: "+rel)
        pin_mod,pin_sha,pin_bytes=pins[rel]
        require(pin_mod==mod,"Historical file cohort mismatch")
        raw=originals.find(mod,resource)
        require(raw is not None and len(raw)==pin_bytes and
                (sha1blob(raw) if mod=="AF" else sha256(raw))==pin_sha,
                "Original 1-3B path/content mismatch: "+resource)
        data=resolve_one(mod,resource,originals)
        root_node=data["chain"][0]
        require(root_node["resource_id"]==resource and root_node["sha"]==pin_sha,
                "Resolved original child source not the B-pinned byte body")
        row={
            "mod":mod,"child_resource":resource,"child_source_sha":pin_sha,
            "child_source_bytes":len(raw),
            "child_declared_parent":root_node["declared_parent"],
            "own_geometry_elements":root_node["own_elements"],
            "own_geometry_faces":root_node["own_faces"],
            "parent_chain_nodes_present":len(data["chain"]),
            "missing_terminal_resource":data["terminal_ref"],
            "terminal_state":data["terminal_status"],
            "child_in_historical_no_static_108":resource in no_static,
            "missing_parent_exact_path_exists":data["terminal_status"]!="PARENT_MISSING",
            "same_basename_other_model_paths_only": "|".join(data.get("other_same_basename_paths",[])),
            "game_client_render_or_missingno_verified":False,
            "parent_repair_applied":False,
            "semantic_style_or_training_approved":False,
        }
        rows.append(row)
    require(len(rows)==48 and len({x["child_resource"] for x in rows})==48,
            "Original missing-parent path denominator not 48")
    # This is an investigation of the *recorded* missing parent set, so a
    # subsequently resolved resource is an important discrepancy, not a PASS.
    require(all(row["terminal_state"]=="PARENT_MISSING" for row in rows),
            "Previously missing model parent resolved in original: investigate source ledger")
    children_by_mod=Counter(r["mod"] for r in rows)
    require(dict(children_by_mod)=={"AF":4,"MACAW":44},
            "Historical source missing-parent family scope unexpectedly changed")
    overlap=sum(x["child_in_historical_no_static_108"] for x in rows)
    require(overlap==44,"Missing-parent/no-static overlap must stay 44")
    roots=Counter(x["missing_terminal_resource"] for x in rows)
    own=Counter("WITH_OWN_ELEMENTS" if x["own_geometry_elements"] else "NO_OWN_ELEMENTS"
                for x in rows)
    output={
        "schema":"MCFR_INT4_ORIGINAL_PARENT_GAPS_48_INDEPENDENT_CHAIN_AUDIT/v1",
        "status":"PASS_48_ORIGINAL_PARENT_PATHS_RECONFIRMED_UNRESOLVED_NOT_RUNTIME_VISUAL",
        "summary":{
            "historical_source_models_total":16572,
            "historical_parent_missing_cases":48,
            "historical_no_static_or_unresolved_cases":108,
            "independently_reopened_exception_models":48,
            "still_missing_exact_parent_targets":48,
            "with_own_source_geometry":own["WITH_OWN_ELEMENTS"],
            "without_own_source_geometry":own["NO_OWN_ELEMENTS"],
            "overlap_with_historical_no_static":overlap,
            "no_static_outside_missing_parent":108-overlap,
            "by_mod":dict(sorted(children_by_mod.items())),
            "distinct_unresolved_parent_resource_ids":len(roots),
            "unresolved_parent_ref_occurrences":dict(sorted(roots.items())),
            "alternate_basename_leads_present":sum(bool(r["same_basename_other_model_paths_only"])
                                                   for r in rows),
            "model_parent_paths_repaired":0,
            "visual_runtime_missing_model_proved":0,
            "source_license_or_ai_training_approved":0,
        },
        "input_evidence_sha256":{**original_hashes,**pin_shas},
        "pinned_originals":PINS,
        "limitations":[
            "Original missing model-parent paths are not equivalent to 48 visually broken in-game blocks",
            "All 48 historic identities and all no-static intersections are kept; 44 overlapped records are not additive",
            "A similarly named model file elsewhere would not automatically be a valid parent or a safe path correction",
            "Source-owned geometry may remain even if a referenced parent is absent",
            "No runtime Minecraft client rendering, UV bake, lighting, semantics, copyright or training permissions proven",
        ],
    }
    return rows,output


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--af",required=True,type=Path)
    p.add_argument("--macaw",required=True,type=Path)
    p.add_argument("--mc1211",required=True,type=Path)
    p.add_argument("--mc12111",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args(argv)
    require(not args.out.exists(),"Do not overwrite prior audit results")
    with OriginalArchives(args.af,args.macaw,args.mc1211,args.mc12111) as archive:
        rows,report=examine(args.root,archive)
    args.out.mkdir(parents=True,exist_ok=False)
    csv_path=args.out/"INT4_PARENT_48_ORIGINAL_CHAIN_RESULTS.csv"
    with csv_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    report["csv_sha256"]=sha256(csv_path.read_bytes())
    out=args.out/"INT4_PARENT_48_ORIGINAL_SUMMARY.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                   encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
