"""고정 Git 원본 및 공식 Modrinth JAR을 읽어 출처·정적 참조 원장을 생성한다."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE.parent

def csv_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def save_csv(name, rows):
    target = HERE / name
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    data = buffer.getvalue().encode()
    target.write_bytes(gzip.compress(data, mtime=0) if name.endswith(".gz") else data)

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

def git_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def git_objects(repo, ids):
    unique_ids = list(dict.fromkeys(ids))
    raw = io.BytesIO(git(repo, "cat-file", "--batch") if not unique_ids else subprocess.check_output(
        ["git", "-C", str(repo), "cat-file", "--batch"], input=("\n".join(unique_ids) + "\n").encode()))
    for oid in unique_ids:
        header = raw.readline().decode().split()
        assert header[:2] == [oid, "blob"], header
        data = raw.read(int(header[2]))
        assert raw.read(1) == b"\n" and git_sha(data) == oid, oid
        yield oid, data
    assert not raw.read()

def asset_id(path):
    _, tail = path.split("assets/", 1)
    namespace, family, rel = tail.split("/", 2)
    return f"{namespace}:{rel.removesuffix('.json')}"

def asset_group(path):
    return path.split("assets/", 1)[1].split("/", 2)[1]

def resolve(ref, models):
    if not ref:
        return "NONE"
    if not isinstance(ref, str):
        return "NON_STRING"
    key = ref if ":" in ref else "minecraft:" + ref
    if key.startswith("minecraft:"):
        return "MINECRAFT_EXTERNAL"
    candidates = models.get(key, [])
    if len(candidates) > 1:
        return "MULTIPLE_LOCAL_PATHS"
    if candidates:
        return "LOCAL"
    if key.split(":", 1)[0] in models.namespaces:
        return "MISSING_LOCAL"
    return "OTHER_NAMESPACE"

class ModelIndex(defaultdict):
    def __init__(self, documents):
        super().__init__(list)
        for row, body in documents:
            if row["family"] == "models":
                self[row["asset_id"]].append((row, body))
        self.namespaces = {key.split(":", 1)[0] for key in self}

def choose_models(value):
    return value if isinstance(value, list) else [value]

def state_choices(body):
    variants = body.get("variants", {})
    multipart = body.get("multipart", [])
    assert isinstance(variants, dict) and isinstance(multipart, list)
    for key, value in variants.items():
        for option in choose_models(value):
            yield "variants", key, option
    for i, rule in enumerate(multipart):
        for option in choose_models(rule["apply"]):
            yield "multipart", str(i), option

def item_model_refs(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == "model" and isinstance(v, str):
                yield v
            elif isinstance(v, (dict, list)):
                yield from item_model_refs(v)
    elif isinstance(value, list):
        for member in value:
            yield from item_model_refs(member)

def parse_asset(data):
    def no_duplicates(pairs):
        converted = dict(pairs)
        if len(converted) != len(pairs):
            raise ValueError("duplicate JSON keys")
        return converted
    try:
        return json.loads(data, object_pairs_hook=no_duplicates), "STRICT_JSON"
    except (ValueError, UnicodeError):
        # 같은 바이트는 보존한 채 중복 키 JSON을 별도로 구분한다.
        try:
            return json.loads(data), "DUPLICATE_KEYS"
        except (ValueError, UnicodeError):
            return {}, "PARSE_ERROR"

def upstream_inventory():
    models = [r for p in sorted(B.glob("B_MODEL_INVENTORY_*.csv")) for r in csv_rows(p)]
    states = csv_rows(B / "B_BLOCKSTATE_INVENTORY.csv")
    code = csv_rows(B / "B_JAVA_KOTLIN_SOURCE_INDEX.csv")
    return models, states, code

def verify_git(mod, repo, registry, models, states, code):
    pin = registry["source_pin"]
    assert git(repo, "rev-parse", pin + "^{tree}").decode().strip() == registry["source_tree_sha"]
    origin = {}
    for line in git(repo, "ls-tree", "-lr", "-z", pin).split(b"\0"):
        if not line:
            continue
        meta, path = line.decode().split("\t", 1)
        _, typ, sha, size = meta.split()
        if typ == "blob":
            origin[path] = (sha, int(size))
    namespace = {"AF":"another_furniture", "HC":"handcrafted"}[mod]
    groups = {g:{p for p in origin if f"/assets/{namespace}/{g}/" in p and p.endswith(".json")}
              for g in ("models", "blockstates")}
    for kind, rows in (("models",models), ("blockstates",states)):
        paths = [r["source_path"] for r in rows]
        assert len(paths) == len(set(paths)) and set(paths) == groups[kind], (mod, kind)
    license_bytes = git(repo, "show", f'{pin}:{registry["license_path"]}')
    assert git_sha(license_bytes) == registry["license_blob_sha"]
    rows = models + states + code
    for row in rows:
        path = row["source_path"]
        assert origin[path] == (row["git_blob_sha"], int(row["bytes"])), path
    data_by_sha = dict(git_objects(repo, [r["git_blob_sha"] for r in rows]))
    documents = []
    for row in models + states:
        path = row["source_path"]
        data = data_by_sha[row["git_blob_sha"]]
        assert len(data) == int(row["bytes"])
        body, parse = parse_asset(data)
        declared_id = row.get("model_id") or row["blockstate_id"]
        assert asset_id(path) == declared_id
        documents.append((dict(mod_id=mod, family=asset_group(path), path=path,
                               asset_id=declared_id, sha=row["git_blob_sha"], bytes=len(data),
                               parse=parse, entry_id=row["entry_id"]), body))
    return documents, len(code)

def verify_macaw(jar, version, project):
    data = jar.read_bytes()
    assert version["id"] == "xhmciaUD" and version["project_id"] == project["id"] == "dtWC90iB"
    primary, = [f for f in version["files"] if f["primary"]]
    sha1 = hashlib.sha1(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    assert len(data) == primary["size"]
    assert {"sha1":sha1, "sha512":sha512} == primary["hashes"]
    with zipfile.ZipFile(io.BytesIO(data)) as arc:
        assert arc.testzip() is None
        names = arc.namelist()
        assert len(names) == len(set(names))
        meta = json.loads(arc.read("fabric.mod.json"))
        assert meta["version"] == version["version_number"] and meta["id"] == "mcwfurnitures"
        assert meta["depends"]["minecraft"].lstrip("~") in version["game_versions"]
        documents = []
        for path in sorted(names):
            if not path.startswith("assets/mcwfurnitures/") or not path.endswith(".json"):
                continue
            family = asset_group(path)
            if family not in ("models", "blockstates", "items"):
                continue
            binary = arc.read(path)
            body, parse = parse_asset(binary)
            documents.append((dict(mod_id="MACAW", family=family, path=path, asset_id=asset_id(path),
                                   sha=hashlib.sha256(binary).hexdigest(), bytes=len(binary),
                                   parse=parse, entry_id=""), body))
        info = dict(version_id=version["id"], project_id=project["id"], mod_version=meta["version"],
                    minecraft=version["game_versions"], loaders=version["loaders"], url=primary["url"],
                    filename=primary["filename"], bytes=len(data), sha1=sha1, sha512=sha512,
                    sha256=hashlib.sha256(data).hexdigest(), zip_crc_check="PASS",
                    zip_entries=len(names), class_paths=sum(n.endswith(".class") for n in names),
                    distribution_license=project["license"]["id"], mod_metadata_license=meta["license"],
                    embedded_license_name="LICENSE_modid",
                    embedded_license_sha256=hashlib.sha256(arc.read("LICENSE_modid")).hexdigest(),
                    embedded_license_header=arc.read("LICENSE_modid").decode().splitlines()[:3])
    return documents, info

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("af", "hc", "jar", "version", "project"):
        parser.add_argument("--"+arg, required=True, type=Path)
    args = parser.parse_args()
    registries = {r["mod_id"]:r for r in csv_rows(B/"SOURCE_REGISTRY.csv")}
    models, states, code = upstream_inventory()
    docs = []
    code_counts = {}
    for mod, repo in (("AF",args.af), ("HC",args.hc)):
        group, code_counts[mod] = verify_git(mod, repo, registries[mod], *(
            [r for r in source if r["mod_id"] == mod] for source in (models, states, code)))
        docs.extend(group)
    macaw, jar_info = verify_macaw(args.jar, json.loads(args.version.read_text()), json.loads(args.project.read_text()))
    docs.extend(macaw)
    counts = Counter((r["mod_id"], r["family"]) for r,_ in docs)
    assert counts[("AF","models")] == 1629 and counts[("AF","blockstates")] == 177
    assert counts[("HC","models")] == 12394 and counts[("HC","blockstates")] == 267
    assert counts[("MACAW","models")] == 2549 and counts[("MACAW","blockstates")] == 714 and counts[("MACAW","items")] == 716
    entries = []
    groups = defaultdict(list)
    for r,_ in macaw:
        family = r["family"]
        kind = r["asset_id"].split(":",1)[1].split("/",1)[0] if family == "models" else family
        groups[(family,kind)].append(r)
    for (family,kind), group in sorted(groups.items()):
        for i in range(0,len(group),150):
            batch = group[i:i+150]
            entry = f"B{110+len(entries):04d}"
            for r in batch:
                r["entry_id"] = entry
            entries.append(dict(entry_id=entry,mod_id="MACAW", asset_family=family, resource_kind=kind,
                                file_count=len(batch), start_source_path=batch[0]["path"], end_source_path=batch[-1]["path"],
                                next_stage={"models":"1-3-C","blockstates":"1-3-D","items":"1-3-F"}[family],
                                processing_status="SOURCE_SHA_VERIFIED_ANALYSIS_PENDING"))
    index = ModelIndex(docs)
    exceptions = []
    status_counts = Counter()
    for row, body in docs:
        family = row["family"]
        row["parent"] = body.get("parent","")
        row["parent_status"] = resolve(row["parent"],index) if family == "models" else "N/A"
        if row["parent_status"] == "LOCAL":
            row["parent_path"] = index[row["parent"]][0][0]["path"]
        else:
            row["parent_path"] = ""
        row["own_elements"] = ""
        row["own_faces"] = ""
        if family == "models":
            elements = body.get("elements", [])
            row["own_elements"] = len(elements)
            row["own_faces"] = sum(len(e.get("faces", {})) for e in elements)
        if family == "blockstates":
            choices = [(f"{rule}:{key}", option["model"]) for rule,key,option in state_choices(body)]
        elif family == "items":
            choices = [("item_model",ref) for ref in item_model_refs(body)]
        else:
            choices = [("parent", row["parent"])] if row["parent"] else []
        row["references"] = len(choices)
        row["distinct_references"] = len({ref for _,ref in choices})
        statuses = Counter()
        for rule, ref in choices:
            result = resolve(ref,index)
            statuses[result] += 1
            if result in ("MULTIPLE_LOCAL_PATHS","MISSING_LOCAL","OTHER_NAMESPACE","NON_STRING"):
                exceptions.append(dict(mod_id=row["mod_id"],family=family,path=row["path"],
                                       source_sha=row["sha"],rule=rule,reference=ref,status=result))
        if row["parse"] != "STRICT_JSON":
            exceptions.append(dict(mod_id=row["mod_id"],family=family,path=row["path"],
                                   source_sha=row["sha"],rule="JSON",reference="",status=row["parse"]))
        row["local_references"] = statuses["LOCAL"]
        row["minecraft_external_references"] = statuses["MINECRAFT_EXTERNAL"]
        row["other_references"] = len(choices)-row["local_references"]-row["minecraft_external_references"]
        for result, count in statuses.items():
            status_counts[(row["mod_id"],family,result)] += count
    # 소스 명령과 분리해 원장 집합·참조·회차를 재집계한다.
    all_rows = [r for r,_ in docs]
    assert len({(r["mod_id"],r["path"]) for r in all_rows}) == len(all_rows)
    for name, subset in (("AF", [r for r in all_rows if r["mod_id"]=="AF"]),
                         ("HC", [r for r in all_rows if r["mod_id"]=="HC"]),
                         ("MACAW", [r for r in all_rows if r["mod_id"]=="MACAW"])):
        save_csv(f"B_{name}_SOURCE_BODIES.csv.gz", subset)
    save_csv("B_MACAW_ENTRY_QUEUE.csv",entries)
    save_csv("B_REFERENCE_EXCEPTIONS.csv.gz",exceptions)
    data_status = Counter((r["mod_id"], r["family"],r["parse"]) for r in all_rows)
    audit = dict(github_baseline="8a94f9a3fe2b3720318a97f1b91221b55809d417",
                 counts={"|".join(k):v for k,v in sorted(counts.items())}, code_original_sha_verified=code_counts,
                 parse_status={"|".join(k):v for k,v in sorted(data_status.items())},
                 references={"|".join(k):v for k,v in sorted(status_counts.items())},
                 exception_records=len(exceptions), exception_unique_paths=len({r["path"] for r in exceptions}),
                 entry_counts=dict(prior=109,macaw=len(entries),total=109+len(entries)),
                 old_verified_paths=587, current_model_state_paths=sum(v for k,v in counts.items() if k[1]!="items"),
                 macaw=jar_info, pushed_original_assets=0)
    (HERE/"B_SOURCE_BODY_AUDIT.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
