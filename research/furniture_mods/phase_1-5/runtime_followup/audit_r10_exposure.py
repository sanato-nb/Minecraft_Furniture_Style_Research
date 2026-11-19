"""Cross-check all declared-only R10 IDs against the two live client captures."""
from collections import defaultdict
import csv
import hashlib
import io
import json
import lzma
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSIONS = ("1.21.1", "1.21.11")


def rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def read_capture(version):
    raw = lzma.decompress((HERE / f"R10_ENGINE_{version}.tsv.xz").read_bytes())
    records = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
    keys = {(r["kind"], r["case"], r["key"]) for r in records}
    assert len(keys) == len(records)
    totals = {r["case"]: int(r["value"]) for r in records if r["kind"] == "TOTAL"}
    block_rows = [r for r in records if r["kind"] == "BLOCK_SCAN"]
    item_rows = [r for r in records if r["kind"] == "ITEM_SCAN"]
    assert totals == {
        "blocks": len(block_rows), "states": sum(int(r["value"]) for r in block_rows),
        "items": len(item_rows),
    }
    items = defaultdict(set)
    for row in item_rows:
        sprites, _special = row["value"].split("|")
        for sprite in filter(None, sprites.split(";")):
            items[sprite].add(row["case"])
    particle_models = {(r["case"], r["key"]): r["value"]
                       for r in records if r["kind"] == "PARTICLE_MODEL"}
    particles = defaultdict(list)
    for row in records:
        if row["kind"] != "PARTICLE_EVENT":
            continue
        sprite, source = row["case"], row["key"]
        count, actual = row["value"].split("|")
        if int(count) > 0 and actual == sprite:
            particles[sprite].append((source, particle_models[sprite, source], int(count)))
    return items, particles, {**totals, "rows": len(records), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    cases = [r for r in rows(HERE.parent / "D/TEXTURE_EXPOSURE.csv")
             if r["finding"].startswith("DECLARATION_")]
    assert len(cases) == len({r["resource_id"] for r in cases}) == 77
    displayed = {(r["minecraft"], r["item_id"]) for r in
                 rows(HERE.parents[1] / "phase_1-3/followup/C_ITEM_DISPLAY_READBACK.csv")}
    captures = {v: read_capture(v) for v in VERSIONS}
    result = []
    for row in cases:
        version, sprite = row["minecraft"], row["resource_id"]
        item_index, particle_index, _ = captures[version]
        items = sorted(item_index[sprite])
        seen_items = [item for item in items if (version, item) in displayed]
        particles = sorted(particle_index[sprite])
        if row["finding"] == "DECLARATION_WITH_PARTICLE":
            assert particles, sprite
        else:
            assert seen_items, sprite
        result.append((row["texture_id"], version, sprite, row["finding"], "VERIFIED",
                       ";".join(items), ";".join(seen_items),
                       " | ".join(f"{block}[{state}]={count}" for block, state, count in particles)))
    with (HERE / "R10_TEXTURE_DISPLAY.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("texture_id", "minecraft", "resource_id", "declaration", "result",
                         "item_quad_ids", "observed_item_display_ids", "break_particle_blocks_and_counts"))
        writer.writerows(result)
    summary = {
        "captures": {v: captures[v][2] for v in VERSIONS},
        "target_ids": len(cases),
        "verified_ids": len(result),
        "item_quad_ids_matched": sum(bool(r[5]) for r in result),
        "ids_with_item_display_evidence": sum(bool(r[6]) for r in result),
        "ids_with_break_particle_events": sum(bool(r[7]) for r in result),
    }
    assert (summary["item_quad_ids_matched"], summary["ids_with_item_display_evidence"],
            summary["ids_with_break_particle_events"]) == (76, 58, 19)
    (HERE / "R10_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
