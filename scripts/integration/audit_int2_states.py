"""Independent 1-2-D state-domain expansion and per-case evidence comparison.

Reads only pinned 1.21.11 blockstates plus historical output as a reference:
the new enumeration does not import or call historical D algorithms.
Expected denominators: 1,168 blockstates; 9,193 syntactic candidates;
19,440 state->model-option applications. These are source-syntax test
candidates, *not* proof of registered in-game states or actual rendering.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G_LEDGER = "research/vanilla_models/phase_1-2-G/final/G_FINAL_SOURCE_SHA_4669.csv"
D_SCOPE = "research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv"
D_HISTORY = "research/vanilla_models/phase_1-2-D"
OUTPUT_COLUMNS = (
    "blockstate_path", "git_blob_sha", "syntax_kind", "declared_rules",
    "declared_options", "syntactic_cases", "cases_with_matches",
    "model_option_applications", "history_cases", "history_applications",
    "cases_compared", "case_differences", "status",
)
ENTRY_CASES = [
    ("entry1", "D_STATE_ASSEMBLY.csv"),
    ("entry2", "D_STATE_ASSEMBLY.jsonl"),
    ("entry3", "D_ENTRY3_SUBBATCH1_48_STATES.jsonl"),
    ("entry3", "D_ENTRY3_REMAINING_217_STATES.jsonl"),
    ("entry4", "D_ENTRY4_265_STATES.jsonl"),
    ("entry5", "D_ENTRY5_265_STATES.jsonl"),
    ("entry6", "D_ENTRY6_265_STATES.jsonl"),
]


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def from_json(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def source_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def parse_json(data, path):
    def duplicate_guard(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"{path}: duplicate JSON key '{key}'")
            out[key] = value
        return out
    obj = json.loads(data.decode("utf-8-sig"), object_pairs_hook=duplicate_guard)
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: JSON root not object")
    return obj


def alternatives(raw):
    if not isinstance(raw, (list, dict)):
        raise ValueError(f"Invalid rule apply: {raw!r}")
    opts = raw if isinstance(raw, list) else [raw]
    if not opts or any(not isinstance(option, dict) or not isinstance(option.get("model"), str) for option in opts):
        raise ValueError("Rule apply must contain at least one model")
    return opts


def get_rules(data):
    if ("variants" in data) == ("multipart" in data):
        raise ValueError("Exactly one of variants/multipart is required")
    if "variants" in data:
        return "variants", [(key, alternatives(value)) for key, value in data["variants"].items()]
    return "multipart", [(part.get("when", {}), alternatives(part["apply"])) for part in data["multipart"]]


def accumulate(when, domain):
    if not isinstance(when, dict):
        raise ValueError(f"Invalid multipart condition: {when!r}")
    for prop, clause in when.items():
        if prop in ("OR", "AND"):
            if not isinstance(clause, list):
                raise ValueError(f"Invalid logical condition for {prop}")
            for child in clause:
                accumulate(child, domain)
        else:
            domain[prop].update(str(clause).split("|"))


def is_match(when, state):
    if not when:
        return True
    if "OR" in when:
        return any(is_match(child, state) for child in when["OR"])
    if "AND" in when:
        return all(is_match(child, state) for child in when["AND"])
    return all(str(state.get(prop)) in str(rule_value).split("|")
               for prop, rule_value in when.items())


def syntax_cases(data):
    syntax, rules = get_rules(data)
    if syntax == "variants":
        for index, (source_key, _) in enumerate(rules):
            yield source_key or "<empty>", (index,)
    else:
        domain = defaultdict(set)
        for condition, _ in rules:
            accumulate(condition, domain)
        for name in domain:
            if domain[name] == {"true"}:
                domain[name].add("false")
            elif domain[name] == {"false"}:
                domain[name].add("true")
        names = sorted(domain)
        size = 1
        for name in names:
            size *= len(domain[name])
        if size > 4096 or len(names) > 16:
            raise ValueError("Bounded syntax domain exceeded")
        for values in itertools.product(*(sorted(domain[name]) for name in names)):
            state = dict(zip(names, values))
            key = ",".join(f"{name}={state[name]}" for name in names) or "<empty>"
            matched = tuple(i for i, (condition, _) in enumerate(rules)
                            if is_match(condition, state))
            yield key, matched


def canonical_option(rule_index, alternative_index, option):
    return (
        int(rule_index), int(alternative_index), option["model"],
        *[option.get(name) for name in ("x", "y", "uvlock", "weight")],
    )


def compute_cases(path, data):
    name = Path(path).stem
    syntax, rules = get_rules(data)
    all_cases = {}
    applications = 0
    for state_name, hit_indices in syntax_cases(data):
        state_id = f"{name}|{state_name}"
        if state_id in all_cases:
            raise ValueError(f"Duplicate generated case id: {state_id}")
        records = []
        for rule_index in hit_indices:
            for alternative_index, option in enumerate(rules[rule_index][1]):
                records.append(canonical_option(rule_index, alternative_index, option))
        all_cases[state_id] = (tuple(hit_indices), tuple(records))
        applications += len(records)
    return {
        "syntax": syntax,
        "rule_count": len(rules),
        "option_count": sum(len(rule[1]) for rule in rules),
        "cases": all_cases, "applications": applications,
    }


def historical_options(record):
    if "model_options_json" in record:
        rows = json.loads(record["model_options_json"])
    elif "simultaneous_model_groups" in record:
        rows = [
            alt for group in record["simultaneous_model_groups"]
            for alt in group["alternatives"]
        ]
    else:
        rows = record["model_options"]
    return tuple(
        canonical_option(
            row["rule_index"],
            row.get("alternative_index", row.get("choice_index")),
            {
                "model": row["model_ref"],
                **{
                    key: row.get(key + "_value", row.get(key))
                    for key in ("x", "y", "uvlock", "weight")
                },
            },
        )
        for row in rows
    )


def historical_hits(raw):
    if isinstance(raw, list):
        return tuple(int(value) for value in raw)
    if isinstance(raw, str):
        if not raw.strip():
            return ()
        return tuple(int(value) for value in raw.split("|"))
    raise ValueError(f"Historical matched rules malformed: {raw!r}")


def load_historical_cases(root):
    result = {}
    per_source = defaultdict(dict)
    legacy_empty_id_aliases = 0
    for section, filename in ENTRY_CASES:
        path = root / D_HISTORY / section / filename
        records = read_csv(path) if filename.endswith(".csv") else from_json(path)
        for record in records:
            state_id = record["state_id"]
            # 1-2-D Entry2 encoded the empty variant as "block|", while
            # later entries recorded "block|<empty>". Both represent the
            # same *source* empty variant; record the normalization count.
            if state_id.endswith("|"):
                state_id += "<empty>"
                legacy_empty_id_aliases += 1
            src = record["blockstate_path"]
            if state_id in result:
                raise ValueError(f"Historic duplicate state key: {state_id}")
            pair = (historical_hits(record["matched_rules"]), historical_options(record))
            result[state_id] = pair
            per_source[src][state_id] = pair
    return result, per_source, legacy_empty_id_aliases


def audit(root):
    g_rows = read_csv(root / G_LEDGER)
    d_rows = read_csv(root / D_SCOPE)
    assert len(d_rows) == 1168 and len({r["source_path"] for r in d_rows}) == 1168
    g = {r["path"]: r for r in g_rows if r["type"] == "BLOCKSTATE_JSON"}
    assert len(g) == 1168 and set(g) == {r["source_path"] for r in d_rows}
    hist_cases, hist_by_source, legacy_empty_id_aliases = load_historical_cases(root)
    source_reports = []
    discrepancies = []
    current_cases = set()
    totals = Counter()
    sources_by_type = Counter()
    for row in sorted(d_rows, key=lambda record: record["source_path"]):
        path = row["source_path"]
        raw = (root / path).read_bytes()
        sha = source_sha(raw)
        if sha != row["git_blob_sha"] or sha != g[path]["sha"]:
            raise ValueError(f"Source SHA changed: {path}")
        data = parse_json(raw, path)
        original = compute_cases(path, data)
        cases = original["cases"]
        ncompared = 0
        for state_id, actual in cases.items():
            if state_id in current_cases:
                raise ValueError(f"Recomputed duplicate state key: {state_id}")
            current_cases.add(state_id)
            prior = hist_cases.get(state_id)
            if prior != actual:
                if len(discrepancies) < 100:
                    discrepancies.append({
                        "state_id": state_id, "source_path": path,
                        "reason": "MISSING_HISTORY" if prior is None else "CASE_CONTENT_DIFFERENCE",
                        "expected": repr(prior)[:450], "actual": repr(actual)[:450],
                    })
            else:
                ncompared += 1
        historic = hist_by_source.get(path, {})
        application_count = sum(len(pair[1]) for pair in historic.values())
        passed = (
            len(cases) == len(historic)
            and original["applications"] == application_count
            and len(cases) == ncompared
        )
        if not passed and len(discrepancies) < 100:
            discrepancies.append({
                "source_path": path, "reason": "SOURCE_AGGREGATE_DIFFERENCE",
                "current_candidates": len(cases), "historical_candidates": len(historic),
                "current_applications": original["applications"],
                "historical_applications": application_count,
            })
        totals["source_paths"] += 1
        totals["source_rules"] += original["option_count"]
        totals["state_candidates"] += len(cases)
        totals["option_applications"] += original["applications"]
        totals["case_matches"] += ncompared
        sources_by_type[original["syntax"]] += 1
        source_reports.append({
            "blockstate_path": path, "git_blob_sha": sha,
            "syntax_kind": original["syntax"],
            "declared_rules": original["rule_count"],
            "declared_options": original["option_count"],
            "syntactic_cases": len(cases),
            "cases_with_matches": sum(bool(rule_indices) for rule_indices, _ in cases.values()),
            "model_option_applications": original["applications"],
            "history_cases": len(historic),
            "history_applications": application_count,
            "cases_compared": ncompared,
            "case_differences": len(cases)-ncompared,
            "status": "PASS" if passed else "DIFFERENCE",
        })
    extra_history = set(hist_cases) - current_cases
    if extra_history and len(discrepancies) < 100:
        discrepancies.append({
            "reason": "HISTORY_HAS_EXTRA_CASES",
            "count": len(extra_history), "examples": sorted(extra_history)[:10],
        })
    criteria = {
        "source_paths": 1168,
        "source_rules": 7592,
        "state_candidates": 9193,
        "option_applications": 19440,
        "case_matches": 9193,
    }
    mismatched_denominators = {
        key: {"new": totals[key], "expected": expected}
        for key, expected in criteria.items() if totals[key] != expected
    }
    result = {
        "schema": "MCFR_INT2_D_STATE_REAUDIT/v1",
        "baseline_sha": "176f7f34de2336eb7984c4734e97b6eb156c19f4",
        "method": "independent_original_json_enumeration_per_case_vs_historical_D_evidence",
        "observed": dict(totals),
        "expected": criteria,
        "state_structures": dict(sorted(sources_by_type.items())),
        "historic_case_records": len(hist_cases),
        "historic_empty_id_format_aliases": legacy_empty_id_aliases,
        "historic_case_surplus": len(extra_history),
        "per_source_discrepancies": sum(r["status"] != "PASS" for r in source_reports),
        "mismatched_denominators": mismatched_denominators,
        "discrepancies": discrepancies,
        "not_checked": [
            "actual_game_registered_property_values",
            "runtime_render_or_weighted_random_sampling",
            "baked_model_rotation",
            "UV_lock_and_baked_quad_coordinates",
            "Minecraft_official_distribution_archive_authenticity",
        ],
        "ai_training_approved": False,
    }
    result["status"] = (
        "PASS_INDEPENDENT_SYNTAX_ENUMERATION_AND_PER_CASE_MATCH"
        if not mismatched_denominators and not discrepancies and not extra_history
        else "DIFFERENCE_REQUIRES_INVESTIGATION"
    )
    return source_reports, result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows, report = audit(args.root)
    with (args.out / "INT2_D_1168_SOURCE_CROSSCHECK.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "INT2_D_SUMMARY.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("INT2_D_RESULT:" + json.dumps(report, ensure_ascii=False, sort_keys=True))
    if report["status"] != "PASS_INDEPENDENT_SYNTAX_ENUMERATION_AND_PER_CASE_MATCH":
        raise SystemExit("INT-2 D discrepancy detected; review evidence artifact")


if __name__ == "__main__":
    main()
