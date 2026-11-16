"""Index prior P1 evidence and prove unbound model templates have child models."""
import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = os.environ.get("C_ENTRY", "entry4")
OUT = ROOT / f"research/vanilla_models/phase_1-2-C/{ENTRY}"
MODEL = ROOT / "1.21.11/assets/minecraft/models/block"


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, result):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, result[0])
        w.writeheader()
        w.writerows(result)


def main():
    children = defaultdict(list)
    for p in MODEL.glob("*.json"):
        source = json.loads(p.read_text())
        parent = source.get("parent", "").split(":")[-1]
        if parent.startswith("block/"):
            children[parent[6:]].append(p)
    issues = rows(OUT / "UNRESOLVED.csv")
    counts = Counter(r["model"] for r in issues if r["issue"] == "missing_slot")
    templates = []
    for name, n in sorted(counts.items()):
        path = MODEL / (name + ".json")
        raw = path.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        descendants = sorted(children[name])
        assert descendants, (name, n)
        templates.append(dict(model=name, source_path=str(path.relative_to(ROOT)), source_sha=sha,
                              unbound_face_refs=n, direct_children=len(descendants),
                              example_child=str(descendants[0].relative_to(ROOT)),
                              classification="source template with child binding pending"))
    write(OUT / "UNBOUND_TEMPLATE_EVIDENCE.csv", templates)
    abnormal = []
    for issue in issues:
        if issue["issue"] == "missing_slot" and children[issue["model"]]:
            continue
        source_path = MODEL / (issue["model"] + ".json")
        raw = source_path.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        slots = json.loads(raw)["textures"]
        slot_candidate = slots.get(issue["ref"], "")
        candidate_path = ROOT / "1.21.11/assets/minecraft/textures" / (slot_candidate.removeprefix("minecraft:") + ".png")
        candidate_sha = ""
        if slot_candidate and candidate_path.exists():
            candidate_raw = candidate_path.read_bytes()
            candidate_sha = hashlib.sha1(b"blob " + str(len(candidate_raw)).encode() + b"\0" + candidate_raw).hexdigest()
        abnormal.append(dict(model=issue["model"], issue=issue["issue"], source_path=str(source_path.relative_to(ROOT)),
                             source_sha=sha, face_ref=issue["ref"], source_texture_slots=json.dumps(
                                 slots, ensure_ascii=False, separators=(",", ":")),
                             slot_name_match_candidate=slot_candidate,
                             candidate_png_path=str(candidate_path.relative_to(ROOT)) if candidate_sha else "",
                             candidate_png_sha=candidate_sha,
                             status="unresolved_bare_face_ref_slot_candidate_not_authenticated"))
    if abnormal:
        write(OUT / "UNRESOLVED_NON_TEMPLATE.csv", abnormal)
    else:
        (OUT / "UNRESOLVED_NON_TEMPLATE.csv").write_text(
            "model,issue,source_path,source_sha,face_ref,source_texture_slots,slot_name_match_candidate,candidate_png_path,candidate_png_sha,status\n")

    selected = {r["leaf_path"]: r for r in rows(OUT / "MODEL_SOURCE_EVIDENCE.csv") if r["priority"] == "P1"}
    v69 = rows(ROOT / "research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv")
    fields = [k for k in v69[0] if re.match(r"^v\d+_", k) and re.search(r"uv|texture|png|pixel|face_material", k, re.I)
              and not re.search(r"fully_|complete|certified|renderer|source_only", k, re.I)]
    historical = []
    for r in v69:
        if r["source_path"] not in selected:
            continue
        assert selected[r["source_path"]]["leaf_sha"] == r["source_git_blob_sha"]
        evidence = {k: r[k] for k in fields if r[k].strip() not in ("", "0", "false", "False", "no", "NO", "null", "None")}
        historical.append(dict(model=r["source_model"].removesuffix(".json"), source_path=r["source_path"],
                               source_sha=r["source_git_blob_sha"], prior_C_field_count=len(evidence),
                               prior_C_field_values_json=json.dumps(evidence, ensure_ascii=False, separators=(",", ":")),
                               evidence_level="v69_columns_value_index_only_not_semantic_certification"))
    assert len(historical) == 154
    write(OUT / "SELECTED_P1_PRIOR_C_FIELDS.csv", historical)
    print(json.dumps(dict(template_models=len(templates), unbound_faces=sum(counts.values()),
                          non_template_refs=len(abnormal), P1_prior_rows=len(historical))))


if __name__ == "__main__":
    main()
