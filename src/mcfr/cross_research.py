"""Compare observed asset profiles across verified releases."""

from collections import Counter
import json

from . import research_engine as engine


def observed_execution(db, execution_id):
    row = db.execute(
        "SELECT e.scope_sha256, e.report_json, r.mode, s.release_key, s.target_id, s.profile "
        "FROM research_execution e JOIN research_run r USING(run_id) JOIN release s USING(release_key) "
        "WHERE e.execution_id = ? AND e.backend = 'source' AND e.status = 'PASS'",
        (execution_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"Expected a passing source execution: {execution_id}")
    data = dict(row)
    report = json.loads(data.pop("report_json"))
    profiles = Counter(
        (entry["kind"], engine._json(entry["observations"]))
        for entry in report["assets"] if entry["status"] == "PASS"
    )
    return {**data, "execution_id": execution_id, "observed_assets": report["verified"],
            "scope_counts": report["catalog_scope_counts"]}, profiles


def compare(db, left_id, right_id):
    left, left_profiles = observed_execution(db, left_id)
    right, right_profiles = observed_execution(db, right_id)
    if (left["profile"], left["target_id"]) == (right["profile"], right["target_id"]):
        raise ValueError("Cross research requires two different targets")
    profiles = [{
        "kind": kind, "observation": json.loads(signature),
        "left": left_profiles[(kind, signature)], "right": right_profiles[(kind, signature)],
    } for kind, signature in sorted(left_profiles.keys() | right_profiles.keys())]
    return {"evidence_class": "STATIC_OBSERVATION_COMPARISON", "left": left, "right": right,
            "shared_profiles": len(left_profiles.keys() & right_profiles.keys()), "profiles": profiles}
