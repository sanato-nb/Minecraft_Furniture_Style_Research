"""INT-4 source reachability of the 48 originally missing-parent furniture models.

Do not equate "a JSON model exists" with "an actual game block uses it".
Provenance and 48 source bytes are checked by the preceding parent audit.
Here we reopen both pinned AF Git assets and Macaw's pinned Fabric JAR,
scan ALL static blockstate model selections, model-parent links and item
model roots, and determine which missing-parent children could actually
be reached by a static blockstate selection.

No runtime game screenshots, block registration, dynamic Java model
loaders, semantic roles or distribution/training licenses are implied.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict,deque
import csv
import hashlib
import json
from pathlib import Path

from audit_int4_parent_gaps import (OriginalArchives,OriginalMismatch,
                                    ROOT,require,check_history,collect_model_pins,
                                    model_rel,parse_json,sha256,sha1blob,PINS)

INT4_LOCK="project/integration/INT4_PARENT_48_ORIGINAL_AUDIT_RESULT.json"
WORKFLOW_ROOTS=("AF","MACAW")
PREFIXES={"AF":"assets/another_furniture/","MACAW":"assets/mcwfurnitures/"}


def resource(path,kind):
    """assets/ns/{kind}/sub/path.json -> ns:sub/path."""
    bits=path.split("/")
    require(len(bits)>=4 and bits[0]=="assets" and bits[2]==kind and
            path.endswith(".json"),"Unexpected pinned archive resource path: "+path)
    return bits[1]+":"+("/".join(bits[3:]))[:-5]


def normalized_ref(value,default_ns):
    require(isinstance(value,str) and value and
            ".." not in value and not value.startswith("/"),"Invalid source model resource reference")
    return value if ":" in value else default_ns+":"+value


def inspect_model_option(obj,default_ns,source):
    """Yield model targets from every variants/multipart apply declaration."""
    if isinstance(obj,list):
        for part in obj:
            yield from inspect_model_option(part,default_ns,source)
    elif isinstance(obj,dict):
        if "model" not in obj:
            raise OriginalMismatch("Missing model field in source blockstate option: "+source)
        yield normalized_ref(obj["model"],default_ns)
    else:
        raise OriginalMismatch("Invalid original blockstate option: "+source)


def static_blockstate_targets(blockstate,default_ns,source):
    require(isinstance(blockstate,dict),"Blockstate root is not JSON object")
    choices=[]
    if "variants" in blockstate:
        require(isinstance(blockstate["variants"],dict),"Invalid blockstate variants mapping: "+source)
        for selector,option in blockstate["variants"].items():
            for target in inspect_model_option(option,default_ns,source):
                choices.append((selector,target,"variants"))
    if "multipart" in blockstate:
        require(isinstance(blockstate["multipart"],list),"Invalid multipart source array: "+source)
        for i,row in enumerate(blockstate["multipart"]):
            require(isinstance(row,dict) and "apply" in row,
                    "Invalid multipart apply model: "+source)
            for target in inspect_model_option(row["apply"],default_ns,source):
                choices.append((str(i),target,"multipart"))
    if not choices:
        raise OriginalMismatch("Blockstate has no traversable static model options: "+source)
    return choices


def item_definition_model_roots(obj,default_ns):
    """Explicit modern item definitions use a model node containing type and model."""
    output=[]
    def walk(node):
        if isinstance(node,dict):
            if node.get("type")=="minecraft:model" and isinstance(node.get("model"),str):
                output.append(normalized_ref(node["model"],default_ns))
            for value in node.values():walk(value)
        elif isinstance(node,list):
            for value in node:walk(value)
    walk(obj)
    return output


def transitive_reachable(start,parent_of):
    """Traverse only explicit source-model inheritance, not guessed resource names."""
    found=set()
    pending=deque(sorted(start))
    while pending:
        current=pending.popleft()
        if current in found:
            continue
        found.add(current)
        par=parent_of.get(current)
        if par and par not in found:
            pending.append(par)
    return found


def catalog(archive,mod):
    """Read all original AF or Macaw JSON resource definitions in the pinned inputs."""
    prefix=PREFIXES[mod]
    if mod=="AF":
        relevant=sorted(k for k in archive.af_index if k.startswith(prefix))
        def get(path):
            return archive.af.read(archive.af_index[path])
    else:
        relevant=sorted(k for k in archive.macaw_names if k.startswith(prefix))
        def get(path):
            return archive.macaw.read(path)
    models={}; states={}; item_defs={}
    source_file_count=Counter()
    for path in relevant:
        if not path.endswith(".json"):
            continue
        kind=path.split("/")[2]
        if kind not in ("models","blockstates","items"):
            continue
        name=resource(path,kind)
        obj=parse_json(get(path),path)
        target={"models":models,"blockstates":states,"items":item_defs}[kind]
        require(name not in target,"Duplicate upstream model namespace ID: "+name)
        target[name]=obj
        source_file_count[kind]+=1
    require(models and states,"Pinned mod resource definitions have no models/blockstates: "+mod)
    return models,states,item_defs,dict(source_file_count)


def measure_roster(root,archives):
    root=Path(root)
    lock=json.loads((root/INT4_LOCK).read_text())
    observed=lock["observed"]
    require(lock["boundaries"]["source48_original_models_reopened"] is True and
            observed["summary"]["historical_parent_missing_cases"]==48 and
            observed["summary"]["still_missing_exact_parent_targets"]==48 and
            observed["summary"]["distinct_unresolved_parent_resource_ids"]==3 and
            observed["summary"]["overlap_with_historical_no_static"]==44 and
            lock["boundaries"]["all_int4_research_complete"] is False,
            "Previous 48 original-source audit checkpoint changed")
    prior_hash=sha256((root/INT4_LOCK).read_bytes())
    roster=json.loads((root/"project/integration/INT2_MOD_SOURCE_SUMMARY.json").read_text())["exceptions"]["missing_parent_paths"]
    hashes,no_static=check_history(root,roster)
    pins,pinshas=collect_model_pins(root)
    rows=[]
    results={}
    for mod in WORKFLOW_ROOTS:
        models,states,item_defs,counts=catalog(archives,mod)
        namespace={"AF":"another_furniture","MACAW":"mcwfurnitures"}[mod]
        direct=defaultdict(set)
        for state_id,obj in states.items():
            for selector,target,typ in static_blockstate_targets(obj,namespace,state_id):
                direct[target].add(state_id+" | "+typ+" | "+selector)
        parents={}
        incoming=defaultdict(set)
        for name,body in models.items():
            if "parent" in body:
                parent=normalized_ref(body["parent"],namespace)
                parents[name]=parent
                incoming[parent].add(name)
        item_seeds=set()
        for item_id,obj in item_defs.items():
            item_seeds.update(item_definition_model_roots(obj,namespace))
        # Model/item files count as item-root candidates, not proof of registration.
        declared_item_model_roots={name for name in models if name.startswith(namespace+":item/")}
        state_chain=transitive_reachable(direct,parents)
        item_chain=transitive_reachable(item_seeds|declared_item_model_roots,parents)
        missing_mod=sorted(x for x in roster if x.startswith(namespace+":"))
        require(len(missing_mod)==(4 if mod=="AF" else 44),
                "Missing-parent membership of original mode changed")
        for child in missing_mod:
            require(child in models,"Historical exception model not found in original asset catalog: "+child)
            path=model_rel(child)
            require(path in pins and pins[path][0]==mod,"Historical model input path missing: "+child)
            raw=archives.find(mod,child)
            require(raw is not None and len(raw)==pins[path][2] and
                    (sha1blob(raw) if mod=="AF" else sha256(raw))==pins[path][1],
                    "Direct blockstate reachability model byte not historical pin: "+child)
            # The parent audit already established absence of its exact parent.
            parent=parents.get(child)
            require(parent and parent in observed["summary"]["unresolved_parent_ref_occurrences"],
                    "Source model no longer points to the historically absent parent: "+child)
            require(parent not in models,
                    "Historically missing target unexpectedly exists in same mod model catalog: "+parent)
            own=models[child].get("elements",[])
            require(isinstance(own,list),"Source geometry is not a list: "+child)
            rows.append({
                "mod":mod,"child_resource":child,"source_sha":pins[path][1],
                "missing_parent_resource":parent,
                "own_elements":len(own),
                "direct_blockstate_selection_entries":len(direct.get(child,())),
                "blockstate_inheritance_reachable":child in state_chain,
                "item_model_root_or_parent_reachable":child in item_chain,
                "other_model_parent_references":len(incoming.get(child,())),
                "direct_blockstate_ids":"|".join(sorted({x.split(" | ",1)[0] for x in direct.get(child,())})),
                "direct_blockstate_source_option_keys":"|".join(sorted(direct.get(child,()))),
                "referenced_model_parent_candidates":"|".join(sorted(incoming.get(child,()))[:15]),
                "static_blockstate_unreferenced":child not in state_chain,
                "no_static_historical_overlap":child in no_static,
                "client_runtime_visual_fault_approved":False,
                "mod_dynamic_model_loading_examined":False,
                "manual_parent_repair_applied":False,
                "ai_semantic_or_rights_approval":False,
            })
        results[mod]={
            "original_resource_jsons_by_type":counts,
            "blockstate_direct_option_targets":sum(map(len,direct.values())),
            "unique_blockstate_referenced_model_ids":len(direct),
            "static_blockstate_parent_chain_reachable_ids":len(state_chain),
            "item_model_root_definitions":len(item_defs),
            "item_parent_chain_reachable_ids":len(item_chain),
        }
    require(len(rows)==48 and len({x["child_resource"] for x in rows})==48,
            "Missing-source parent roster incomplete after scanning blockstates")
    cnt=Counter((x["mod"],"BLOCKSTATE_REACHABLE" if x["blockstate_inheritance_reachable"] else "NOT_BLOCKSTATE_REACHABLE")
                for x in rows)
    used=[x for x in rows if x["blockstate_inheritance_reachable"]]
    ref_mods=Counter(x["mod"] for x in used)
    summary={
        "schema":"MCFR_INT4_PARENT_48_BLOCKSTATE_SOURCE_REACHABILITY/v1",
        "status":"PINNED_STATIC_BLOCKSTATE_SELECTION_REACHABILITY_ONLY_NOT_GAME_RENDER",
        "root_parent_audit_lock_sha256":prior_hash,
        "historical_source_hashes":{**hashes,**pinshas},
        "original_pinned_assets":PINS,
        "source_census":results,
        "summary":{
            "historical_missing_parent_model_paths":48,
            "missing_parent_target_ids":3,
            "historical_no_static_overlap":44,
            "catalog_models_checked_exact_sha":48,
            "in_static_blockstate_source_selection_or_parent_chain":len(used),
            "not_reachable_from_static_blockstates":48-len(used),
            "direct_selected_from_static_blockstates":sum(bool(x["direct_blockstate_selection_entries"]) for x in rows),
            "item_model_or_parent_chain_reachable":sum(bool(x["item_model_root_or_parent_reachable"]) for x in rows),
            "reachable_by_mod":dict(sorted(ref_mods.items())),
            "source_per_model_reachability_counts":{mod:dict(sorted(
                (name,n) for (m,name),n in cnt.items() if m==mod))
                for mod in WORKFLOW_ROOTS},
            "actual_game_render_failure_proven":0,
            "source_model_repair_applied":0,
            "ai_semantics_or_training_rights_approved":0
        },
        "limits":[
            "No case is considered actually placed or displayed by this static reachability scan",
            "Blockstate options may not correspond to registered runtime blocks or practically achievable combinations",
            "A model not reached by static blockstates could still load via custom model loaders, Java, dynamic state, resource packs or items",
            "Missing model parent does not prove an in-game broken mesh or texture",
            "Current report is restricted to pinned AF 4.0.3 Git commit and Macaw 3.4.2 Fabric JAR and prior audited missing-parent roster",
            "No existing original models, parent links or historical evidence files are modified"
        ],
    }
    return rows,summary


def main(argv=None):
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root",type=Path,default=ROOT)
    cli.add_argument("--af",type=Path,required=True)
    cli.add_argument("--macaw",type=Path,required=True)
    cli.add_argument("--mc1211",type=Path,required=True)
    cli.add_argument("--mc12111",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    args=cli.parse_args(argv)
    require(not args.out.exists(),"Do not overwrite earlier source audit results")
    with OriginalArchives(args.af,args.macaw,args.mc1211,args.mc12111) as arc:
        rows,summary=measure_roster(args.root,arc)
    args.out.mkdir(parents=True,exist_ok=False)
    path=args.out/"INT4_PARENT_48_BLOCKSTATE_REACHABILITY.csv"
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader();w.writerows(rows)
    summary["row_csv_sha256"]=sha256(path.read_bytes())
    (args.out/"INT4_PARENT_48_BLOCKSTATE_REACHABILITY_SUMMARY.json").write_text(
        json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
