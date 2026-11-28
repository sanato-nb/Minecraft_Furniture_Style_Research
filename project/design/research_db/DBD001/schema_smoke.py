"""7-E syntax/structure smoke only. Not the locked 16-case acceptance suite."""
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from contextlib import closing
from mcfr import research_db

ROOT=Path(__file__).resolve().parents[4]
DIR=Path(__file__).resolve().parent

def catalog(db):
    return list(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"))

def main():
    scope=json.loads((DIR/"scope_lock.json").read_text())
    for row in scope["inputs"]:
        b=(ROOT/row["path"]).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==row["git_blob"],row["path"]
    with tempfile.TemporaryDirectory() as tmp:
        original=Path(tmp)/"v4.sqlite"
        copy=Path(tmp)/"design.sqlite"
        research_db.initialize(original)
        before_hash=hashlib.sha256(original.read_bytes()).hexdigest()
        with closing(sqlite3.connect(original)) as src, closing(sqlite3.connect(copy)) as dst:
            src.backup(dst)
        with closing(sqlite3.connect(copy)) as db:
            db.execute("PRAGMA foreign_keys=ON")
            before=catalog(db)
            version=db.execute("PRAGMA user_version").fetchone()[0]
            db.executescript("BEGIN IMMEDIATE;\n"+(DIR/"schema_proposal.sql").read_text()+"\nCOMMIT;")
            after=catalog(db)
            assert all(x in after for x in before)
            assert version==db.execute("PRAGMA user_version").fetchone()[0]==4
            assert db.execute("PRAGMA integrity_check").fetchall()==[("ok",)]
            assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
            names={x[1] for x in after}
            areas=json.loads((DIR/"area_map.json").read_text())["areas"]
            assert [x["id"] for x in areas]==scope["data_areas"]
            assert all(set(x["entities"])<=names for x in areas)
            for view in ("knowledge_search_view","source_inventory_view"):
                db.execute("SELECT * FROM "+view+" LIMIT 1").fetchall()
            # Prepare representative insert statements via EXPLAIN to catch
            # malformed foreign key parent definitions even on an empty DB.
            for name in [x[1] for x in after if x[0]=="table" and x not in before]:
                cols=[x[1] for x in db.execute('PRAGMA table_info("'+name+'")')]
                quoted=",".join('"'+c+'"' for c in cols)
                db.execute('EXPLAIN INSERT INTO "'+name+'" ('+quoted+') VALUES ('+','.join("?" for _ in cols)+')',[None]*len(cols)).fetchall()
            new=[x for x in after if x not in before]
            report={"gate":"7-E-SMOKE","status":"PASS","existing_tables":sum(x[0]=="table" for x in before),
                    "new_tables":sum(x[0]=="table" for x in new),"new_views":sum(x[0]=="view" for x in new),
                    "new_indexes":sum(x[0]=="index" for x in new),"areas":len(areas),
                    "pinned_inputs":len(scope["inputs"]),"user_version":version,"original_unchanged":True,
                    "sql_sha256":hashlib.sha256((DIR/"schema_proposal.sql").read_bytes()).hexdigest(),
                    "limits":"DDL creation, FK statement preparation and empty view queries only; T01-T16 not executed."}
        assert hashlib.sha256(original.read_bytes()).hexdigest()==before_hash
    print("DBD001_E_SMOKE "+json.dumps(report,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
