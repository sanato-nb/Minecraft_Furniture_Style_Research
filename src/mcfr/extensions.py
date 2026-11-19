"""Check upstream releases, capture differences, research coverage and AI usage."""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import json
from pathlib import Path
import sqlite3

from . import cross_research, research_db as catalog, research_engine as engine, update_watch, visual_check


def coverage_counts(counts):
    selected, verified, failed = (counts[key] for key in ("selected", "verified", "failed"))
    return {"selected": selected, "verified": verified, "failed": failed, "unverified": selected - verified - failed,
            "verified_percent": round(100 * verified / selected, 2) if selected else None}


def coverage(db, run_id):
    plan = engine.plan_run(db, run_id)
    by_kind = defaultdict(Counter)
    for entry in plan["selected"]:
        by_kind[entry["kind"]]["selected"] += 1
    execution = db.execute(
        "SELECT execution_id, report_json FROM research_execution WHERE run_id = ? AND backend = 'source' "
        "AND scope_sha256 = ? ORDER BY finished_at DESC, rowid DESC LIMIT 1", (run_id, plan["scope_sha256"]),
    ).fetchone()
    if execution is not None:
        for asset in json.loads(execution["report_json"]).get("assets", []):
            by_kind[asset["kind"]]["verified" if asset["status"] == "PASS" else "failed"] += 1
    return {
        "run_id": run_id, "scope_sha256": plan["scope_sha256"], "scope_counts": plan["counts"],
        "execution_id": execution["execution_id"] if execution is not None else None,
        "total": coverage_counts(sum(by_kind.values(), Counter())),
        "by_kind": {kind: coverage_counts(counts) for kind, counts in sorted(by_kind.items())},
    }


def usage(db):
    models = defaultdict(Counter)
    for row in db.execute("SELECT request_json, result_json, state, reused_from FROM ai_review"):
        usage_by_model = models[json.loads(row["request_json"])["model"]]
        if row["reused_from"] is not None:
            usage_by_model["cache_hits"] += 1
        elif row["state"] in {"DISPATCHING", "UNCONFIRMED"}:
            usage_by_model["unconfirmed_calls"] += 1
        elif row["state"] == "COMPLETE":
            usage_by_model["recorded_responses"] += 1
            tokens = json.loads(row["result_json"]).get("usage", {})
            for name in ("input_tokens", "output_tokens", "total_tokens"):
                if type(tokens.get(name)) is int and tokens[name] >= 0:
                    usage_by_model[name] += tokens[name]
            if not tokens:
                usage_by_model["responses_without_usage"] += 1
        else:
            usage_by_model["prepared"] += 1
    return {"models": dict(sorted(models.items())), "unit": "provider_reported_tokens"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    watch = commands.add_parser("check-update")
    watch.add_argument("target", help="vanilla or a Modrinth slug/project ID")
    watch.add_argument("--game-version", default="")
    watch.add_argument("--loader", default="")
    watches = commands.add_parser("check-updates", help="Check every target in a JSON watch list")
    watches.add_argument("--targets", type=Path, default=catalog.ROOT / "registry/upstream-targets.json")
    visual = commands.add_parser("visual")
    visual.add_argument("reference", type=Path)
    visual.add_argument("candidate", type=Path)
    visual.add_argument("--reference-sha256")
    cross = commands.add_parser("compare")
    cross.add_argument("left_execution")
    cross.add_argument("right_execution")
    commands.add_parser("coverage").add_argument("run_id")
    commands.add_parser("usage")

    args = parser.parse_args(argv)
    try:
        if args.command == "visual":
            result = visual_check.compare(args.reference, args.candidate, reference_sha256=args.reference_sha256)
        else:
            if args.db is None:
                parser.error("--db is required for this command")
            mode = "rw" if args.command in {"check-update", "check-updates"} else "ro"
            with closing(catalog.open_db(args.db, mode)) as db:
                catalog.require_schema(db, minimum=4)
                if mode == "ro":
                    db.execute("BEGIN")
                if args.command == "check-update":
                    result = update_watch.check(db, args.target, args.game_version, args.loader)
                elif args.command == "check-updates":
                    result = update_watch.check_many(db, json.loads(args.targets.read_text(encoding="utf-8")))
                elif args.command == "compare":
                    result = cross_research.compare(db, args.left_execution, args.right_execution)
                elif args.command == "coverage":
                    result = coverage(db, args.run_id)
                else:
                    result = usage(db)
    except (ImportError, KeyError, OSError, TypeError, ValueError, sqlite3.Error) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    expected = {"visual": "MATCH", "check-updates": "PASS"}
    return int(args.command in expected and result["status"] != expected[args.command])


if __name__ == "__main__":
    raise SystemExit(main())
