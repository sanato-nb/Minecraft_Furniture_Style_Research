#!/usr/bin/env python3
"""Rebuild v10 research SQLite locally from tracked v8 DB and SQL patch.
No original Minecraft asset files are downloaded or distributed.
"""
import argparse
import pathlib
import shutil
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="Rebuild v10 research snapshot")
parser.add_argument("--base", type=pathlib.Path, default=ROOT/"data/MC_Furniture_Style_Stage1_Research_v8.sqlite")
parser.add_argument("--migration", type=pathlib.Path, default=ROOT/"data/migrations/v8_to_v10.sql")
parser.add_argument("--output", type=pathlib.Path, default=ROOT/"data/MC_Furniture_Style_Stage1_Research_v10.sqlite")
args = parser.parse_args()
if args.base.resolve() == args.output.resolve():
    parser.error("Do not overwrite the tracked v8 database.")
if not args.base.is_file() or not args.migration.is_file():
    parser.error("Missing input v8 SQLite or SQL migration.")
args.output.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(args.base, args.output)
conn = sqlite3.connect(args.output)
try:
    conn.executescript(args.migration.read_text(encoding="utf-8"))
    conn.commit()
    expect={"texture_stats_v4":150,"models":55,"uv_faces_v6":90,"assembly_cases_v7":21,
            "special_model_layers_v9":19,"special_animation_clips_v9":15,"validation_audit_v10":6}
    for table,n in expect.items():
        count=conn.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
        if count!=n: raise RuntimeError(f"{table}: {count} != {n}")
    ok=conn.execute("PRAGMA integrity_check").fetchone()[0]
    if ok!="ok": raise RuntimeError("SQLite integrity: "+str(ok))
    if conn.execute("PRAGMA foreign_key_check").fetchall():raise RuntimeError("FK errors")
    print("v10 SQLite rebuilt:", args.output)
except Exception:
    conn.close()
    args.output.unlink(missing_ok=True)
    raise
finally:
    conn.close()
