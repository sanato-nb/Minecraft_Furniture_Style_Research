"""Trace the 48 parent exceptions through the actual mod JAR resource trees."""
from argparse import ArgumentParser
from collections import defaultdict
import csv
import json
from pathlib import Path
import re
from zipfile import ZipFile

from run_comparison_probe import input_rows

HERE = Path(__file__).resolve().parent
MODEL = re.compile(r"assets/([^/]+)/models/(.+)\.json")
ROOT = re.compile(r"assets/([^/]+)/(blockstates|items)/(.+)\.json")


def ids(value, default_namespace):
    if isinstance(value, dict):
        for key, entry in value.items():
            if key in {"model", "parent"} and isinstance(entry, str):
                yield entry if ":" in entry else f"{default_namespace}:{entry}"
            elif isinstance(entry, (dict, list)):
                yield from ids(entry, default_namespace)
    elif isinstance(value, list):
        for item in value:
            yield from ids(item, default_namespace)


def read_mod(archive, vanilla, old_items):
    model_refs = {}
    roots = defaultdict(set)
    with ZipFile(archive) as pack, ZipFile(vanilla) as official:
        paths = set(pack.namelist()) | set(official.namelist())
        for path in sorted(pack.namelist()):
            if match := MODEL.fullmatch(path):
                namespace, name = match.groups()
                resource = f"{namespace}:{name}"
                model_refs[resource] = set(ids(json.loads(pack.read(path)), namespace))
                if old_items and name.startswith("item/"):
                    roots[resource].add(path)
            elif match := ROOT.fullmatch(path):
                for resource in ids(json.loads(pack.read(path)), match.group(1)):
                    roots[resource].add(path)
    return paths, model_refs, roots


def trace(paths, models, roots, entries):
    # Propagate all packaged blockstate and item roots through the model graph.
    reachable = defaultdict(set)
    pending = [(model, path) for model, files in roots.items() for path in files]
    while pending:
        model, path = pending.pop()
        if path in reachable[model]:
            continue
        reachable[model].add(path)
        pending.extend((ref, path) for ref in models.get(model, ()))
    for row in entries:
        resource = row["model_resource"]
        yield (
            row["mod"], row["model_key"], resource, int(resource in models),
            int(row["missing_exact_path"] in paths), len(reachable[resource]),
            ";".join(sorted(reachable[resource])),
        )


def main():
    parser = ArgumentParser(description=__doc__)
    for name in ("af", "hc", "macaw", "vanilla-old", "vanilla-new"):
        parser.add_argument(f"--{name}", required=True, type=Path)
    args = parser.parse_args()
    cases = input_rows(HERE.parent / "D/PARENT_EXCEPTIONS.csv")
    output = []
    for mod, path in (("AF", args.af), ("HC", args.hc), ("MACAW", args.macaw)):
        old = mod != "MACAW"
        data = read_mod(path, args.vanilla_old if old else args.vanilla_new, old)
        output += list(trace(*data, (row for row in cases if row["mod"] == mod)))
    assert len(output) == 48
    with (HERE / "PARENT_DEPLOYMENT.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("mod", "model_key", "resource", "model_in_jar", "exact_parent_in_jar",
                         "packaged_blockstate_or_item_roots", "root_paths"))
        writer.writerows(output)


if __name__ == "__main__":
    main()
