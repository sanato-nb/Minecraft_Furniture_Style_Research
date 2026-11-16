"""Build the bounded 1-2-C Entry3–5 allocation from the immutable B ledger."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/vanilla_models/phase_1-2-C"
B = ROOT / "research/vanilla_models/phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv"
OUT = BASE / "C_FIXED_SCOPE_2390.csv"
FIELDS = ("asset_type", "full_source_path", "git_blob_sha", "priority", "B_first_owner_scope",
          "B_geometry_source_status", "geometry_provider_source_path", "geometry_provider_blob_SHA",
          "C_assignment", "C_status_at_contract", "C_exception_owner")


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    source = read_csv(B)
    assert len(source) == 2390 and len({r["full_source_path"] for r in source}) == 2390
    completed = {}
    for entry in ("entry1", "entry2"):
        for r in read_csv(BASE / entry / "MODEL_SOURCE_EVIDENCE.csv"):
            assert r["leaf_path"] not in completed
            completed[r["leaf_path"]] = (entry, r["leaf_sha"])
    assert len(completed) == 108

    candidates = {p: [] for p in ("P1", "P2", "P3")}
    deferred = []
    for r in source:
        if r["B_first_owner_scope"] == "E_FIRST_P1_30_DEFERRED":
            deferred.append(r)
        elif r["B_first_owner_scope"] == "B_FIRST_2360":
            if r["geometry_provider_source_path"]:
                if r["full_source_path"] in completed:
                    assert completed[r["full_source_path"]][1] == r["git_blob_sha"]
                else:
                    candidates[r["priority"]].append(r)
            else:
                deferred.append(r)
        else:
            raise AssertionError((r["full_source_path"], r["B_first_owner_scope"]))
    assert {p: len(a) for p, a in candidates.items()} == {"P1": 463, "P2": 998, "P3": 735}
    assert len(deferred) == 86
    assignment = {}
    # Interleave sorted paths; the P2 offset yields exactly 732 per future Entry.
    for priority, values in candidates.items():
        for i, r in enumerate(sorted(values, key=lambda x: x["full_source_path"])):
            slot = (i + (1 if priority == "P2" else 0)) % 3
            assignment[r["full_source_path"]] = f"ENTRY{slot + 3}"

    result = []
    for r in source:
        path = r["full_source_path"]
        if path in completed:
            scope = completed[path][0].upper()
            status = "SOURCE_COHORT_CHECKED"
            owner = ""
        elif path in assignment:
            scope = assignment[path]
            status = "SCHEDULED_NOT_C_VERIFIED"
            owner = ""
        else:
            scope = "E_EXCEPTION"
            status = "NO_GENERAL_GEOMETRY_OR_E_FIRST"
            owner = "1-2-E"
        result.append({k: r.get(k, "") for k in FIELDS[:-3]} | {
            "C_assignment": scope, "C_status_at_contract": status, "C_exception_owner": owner})

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result)
    counts = Counter(r["C_assignment"] for r in result)
    by_priority = {e: dict(Counter(r["priority"] for r in result if r["C_assignment"] == e))
                   for e in ("ENTRY1", "ENTRY2", "ENTRY3", "ENTRY4", "ENTRY5")}
    assert counts == {"ENTRY1": 12, "ENTRY2": 96, "ENTRY3": 732, "ENTRY4": 732,
                      "ENTRY5": 732, "E_EXCEPTION": 86}
    assert by_priority["ENTRY3"] == {"P1": 155, "P2": 332, "P3": 245}
    assert by_priority["ENTRY4"] == {"P1": 154, "P2": 333, "P3": 245}
    assert by_priority["ENTRY5"] == {"P1": 154, "P2": 333, "P3": 245}
    summary = {"schema": "C_FIXED_5_ENTRY_CONTRACT", "game": "Minecraft Java 1.21.11",
               "baseline_remote_head": "e18163fda258b0be6a6b1ca1910298f1a80f18b4",
               "asset_identity_count": len(result), "direct_face_scope": 2304, "E_exceptions": 86,
               "completed_entry_count": 2, "maximum_total_entries": 5, "remaining_execution_entries": 3,
               "assignments": dict(counts), "priority_by_entry": by_priority,
               "status": "SCHEDULE_FIXED_NOT_C_COMPLETE",
               "source_B_ledger": str(B.relative_to(ROOT)),
               "manifest": str(OUT.relative_to(ROOT))}
    (BASE / "C_FIXED_SCOPE_AUDIT.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
