"""7-H independent design closure audit; read historical DBs without migration."""
import hashlib
import json
import lzma
import sqlite3
import sys
from pathlib import Path
from contextlib import closing
from mcfr import research_db
import tempfile

DIR=Path(__file__).resolve().parent
ROOT=DIR.parents[3]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":"))
def q(x):return '"'+x.replace('"','""')+'"'
def main(out):
    lock=load(DIR/"scope_lock.json")
    assert lock["state"]=="LOCKED_BEFORE_DESIGN"
    for row in lock["inputs"]:assert blob((ROOT/row["path"]).read_bytes())==row["git_blob"],row["path"]
    fixed=[x["id"] for x in lock["required_checks"]]
    areas=load(DIR/"area_map.json")["areas"]
    assert [x["id"] for x in areas]==lock["data_areas"]
    assert set().union(*(set(x["tests"]) for x in areas))==set(fixed)
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/"v4.sqlite";research_db.initialize(path)
        with closing(sqlite3.connect(path)) as db:
            db.execute("PRAGMA foreign_keys=ON")
            before=db.execute("SELECT type,name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name").fetchall()
            db.executescript((DIR/"schema_proposal.sql").read_text())
            after=db.execute("SELECT type,name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name").fetchall()
            assert all(x in after for x in before)
            names={x[1] for x in after}
            for x in areas:assert set(x["entities"])<=names
            assert db.execute("PRAGMA integrity_check").fetchall()==[("ok",)]
            assert not db.execute("PRAGMA foreign_key_check").fetchall()
            design_counts={typ:sum(x[0]==typ for x in after if x not in before) for typ in ("table","view","index","trigger")}
            assert design_counts["table"]==43 and design_counts["view"]==2 and design_counts["index"]==11
    past=[]
    for n in ("FIRST","SECOND","THIRD","FOURTH","FIFTH","SIXTH"):
        e=load(DIR/("G_"+n+"_EVIDENCE.json"))
        tests=e["tests"];s=e["summary"]
        assert [x["id"] for x in tests]==fixed
        assert s["executed"]==len(fixed) and s["scope_sha256"]==sha((DIR/"scope_lock.json").read_bytes())
        assert s["counts"]=={k:sum(x["status"]==k for x in tests) for k in ("PASS","PARTIAL","HOLD","FAIL")}
        assert e["workflow_status"]=="success"
        past.append({"run":e["run"],"commit":e["verified_commit"],"counts":s["counts"]})
    g=load(out/"G_results.json")
    assert [x["id"] for x in g["tests"]]==fixed
    assert g["counts"]=={k:sum(x["status"]==k for x in g["tests"]) for k in ("PASS","PARTIAL","HOLD","FAIL")}
    for filename,key in [("scope_lock.json","scope_sha256"),("schema_proposal.sql","schema_sha256"),("design_contract.py","contract_sha256"),("design_tests.py","test_sha256"),("fixture_oracle.py","oracle_sha256")]:
        assert g[key]==sha((DIR/filename).read_bytes())
    # Full DDL/column/index/FK inspection of the nine pinned historical SQLite paths.
    history=load(ROOT/"project/audits/research_quality/RQ001/E_FINAL_EVIDENCE.json")["databases"]
    inspected=[]
    for e in history:
        p=ROOT/e["path"];raw=p.read_bytes()
        assert blob(raw)==e["expected_git_blob"] and len(raw)==e["expected_bytes"]
        decoded=lzma.decompress(raw) if p.suffix==".xz" else raw
        assert sha(decoded)==e["decoded_sha256"]
        with closing(sqlite3.connect(":memory:")) as db:
            db.deserialize(decoded);db.execute("PRAGMA query_only=ON")
            assert db.execute("PRAGMA integrity_check").fetchall()==[("ok",)]
            assert not db.execute("PRAGMA foreign_key_check").fetchall()
            tables=[]
            ddl=db.execute("SELECT type,name,tbl_name,sql FROM sqlite_schema ORDER BY type,name").fetchall()
            for typ,name,_,_ in ddl:
                if typ!="table" or name.startswith("sqlite_"):continue
                tables.append({"name":name,"rows":db.execute("SELECT count(*) FROM "+q(name)).fetchone()[0],"columns":db.execute("PRAGMA table_info("+q(name)+")").fetchall(),"foreign_keys":db.execute("PRAGMA foreign_key_list("+q(name)+")").fetchall(),"indexes":[{"definition":ix,"columns":db.execute("PRAGMA index_xinfo("+q(ix[1])+")").fetchall()} for ix in db.execute("PRAGMA index_list("+q(name)+")").fetchall()]})
            assert len(tables)==e["table_count"]
            assert {x["name"]:x["rows"] for x in tables}=={x["name"]:x["rows"] for x in e["tables"]}
            inspected.append({"path":e["path"],"git_blob":blob(raw),"decoded_sha256":sha(decoded),"ddl":ddl,"tables":tables})
        assert p.read_bytes()==raw
    assert len(inspected)==9 and len({x["git_blob"] for x in inspected})==8
    historical_bytes=(canonical(inspected)+"\n").encode()
    (out/"H_historical_ddl.json").write_bytes(historical_bytes)
    result={"gate":"7-H","execution_status":"PASS","design_quality":g["status"],"closure":"CLOSED_PARTIAL" if g["status"]=="PARTIAL" else "REVIEW_REQUIRED","scope_inputs":len(lock["inputs"]),"mapped_areas":len(areas),"fixed_tests":len(fixed),"design_counts":design_counts,"past_records":past,"current_counts":g["counts"],"current_result_sha256":sha((out/"G_results.json").read_bytes()),"historical_paths":len(inspected),"historical_unique":len({x["git_blob"] for x in inspected}),"historical_tables":sum(len(x["tables"]) for x in inspected),"historical_rows":sum(t["rows"] for x in inspected for t in x["tables"]),"historical_ddl_sha256":sha(historical_bytes),"production_migration":"NOT_PERFORMED","semantic_validation":"NOT_PERFORMED","limits":"Physical historical DDL and row-count comparison; no semantic import or full game validation. Closure still requires reviewer disposition."}
    (out/"H_review.json").write_text(canonical(result)+"\n",encoding="utf-8")
    print("DBD001_H_SUMMARY "+canonical(result),flush=True)
if __name__=="__main__":main(Path(sys.argv[1]))
