"""Design-only executable contracts. Not a production DB writer."""
import hashlib
import json
import math
import sqlite3
from pathlib import Path

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False)

def rows(db, sql, args=()):
    return [dict(r) for r in db.execute(sql,args)]

def one(db,sql,args=()):
    rr=rows(db,sql,args)
    require(len(rr)==1,"expected one row")
    return rr[0]

def evidence_ok(db,eid,read):
    if eid is None: return False
    try:
        e=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(eid,))
        if e["retention_state"]!="VERIFIED_AVAILABLE": return False
        raw=read(e)
        return len(raw)==e["byte_count"] and sha(raw)==e["content_sha256"]
    except (ValueError,OSError,KeyError,TypeError):
        return False

def require_evidence(db,eid,read):
    require(evidence_ok(db,eid,read),"missing or mismatched evidence")

def register_guard(db,release,path,algorithm,digest,size):
    require(not rows(db,"SELECT 1 FROM unregistered_source WHERE release_key=? AND source_path=?",(release,path)),"cross-catalog duplicate")
    for e in rows(db,"SELECT hash_algorithm,digest,byte_count FROM asset WHERE release_key=? AND source_path=?",(release,path)):
        require(e["hash_algorithm"]!=algorithm or e["digest"]==digest,"digest conflict")
        require(e["byte_count"] is None or size is None or e["byte_count"]==size,"size conflict")
    for e in rows(db,"SELECT digest,byte_count FROM asset_hash WHERE release_key=? AND source_path=? AND algorithm=?",(release,path,algorithm)):
        require(e["digest"]==digest and (size is None or e["byte_count"]==size),"additional hash conflict")

def scope_payload(db,sid):
    return {table:rows(db,f"SELECT * FROM {table} WHERE scope_id=? ORDER BY {order}",(sid,)) for table,order in (
        ("scope_source","source_ordinal"),("scope_unit","unit_id"),("validation_requirement","requirement_id"),
        ("research_task","ordinal"),("render_case","case_id"))}

def scope_fingerprint(db,sid):
    return sha(canonical(scope_payload(db,sid)).encode())

def locked_scope(db,sid,read):
    s=one(db,"SELECT * FROM research_scope WHERE scope_id=?",(sid,))
    require(s["lifecycle"]=="LOCKED","scope not locked")
    for name in ("manifest","plan"):
        eid=s[name+"_evidence_id"]
        require_evidence(db,eid,read)
        e=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(eid,))
        require(e["content_sha256"]==s[name+"_sha256"],"scope evidence mismatch")
    manifest=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(s["manifest_evidence_id"],))
    require(json.loads(read(manifest))["scope_fingerprint"]==scope_fingerprint(db,sid),"locked scope changed")
    return s

def append_checkpoint(db,sid,aid,next_position,eid,read,*,committed_at):
    """Caller owns transaction; retry is idempotent only for exactly matching last result."""
    pos=validate_checkpoint(db,sid,aid,read)
    a=one(db,"SELECT * FROM research_attempt WHERE scope_id=? AND attempt_id=?",(sid,aid))
    require_evidence(db,eid,read)
    e=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(eid,))
    existing=rows(db,"SELECT * FROM task_checkpoint WHERE scope_id=? AND attempt_id=? ORDER BY batch_no DESC",(sid,aid))
    if next_position==pos and existing:
        require(existing[0]["result_evidence_id"]==eid and existing[0]["result_sha256"]==e["content_sha256"],"conflicting checkpoint retry")
        return False
    require(a["lifecycle"]=="RUNNING","new checkpoint requires running attempt")
    require(type(next_position)==int and next_position>pos,"checkpoint position not increasing")
    db.execute("INSERT INTO task_checkpoint(scope_id,attempt_id,batch_no,next_position,input_sha256,result_evidence_id,result_sha256,committed_at) VALUES(?,?,?,?,?,?,?,?)",
               (sid,aid,len(existing),next_position,a["input_sha256"],eid,e["content_sha256"],committed_at))
    return True

def validate_checkpoint(db,sid,aid,read):
    s=locked_scope(db,sid,read)
    a=one(db,"SELECT * FROM research_attempt WHERE scope_id=? AND attempt_id=?",(sid,aid))
    task=one(db,"SELECT * FROM research_task WHERE scope_id=? AND task_id=?",(sid,a["task_id"]))
    require(a["input_sha256"]==task["input_sha256"],"attempt input changed")
    if a["legacy_execution_id"] is not None:
        e=one(db,"SELECT run_id FROM research_execution WHERE execution_id=?",(a["legacy_execution_id"],))
        require(e["run_id"]==s["run_id"],"execution run mismatch")
    pos=0
    for i,c in enumerate(rows(db,"SELECT * FROM task_checkpoint WHERE scope_id=? AND attempt_id=? ORDER BY batch_no",(sid,aid))):
        require(c["batch_no"]==i and c["next_position"]>pos and c["input_sha256"]==a["input_sha256"],"checkpoint sequence/input")
        require_evidence(db,c["result_evidence_id"],read)
        e=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(c["result_evidence_id"],))
        require(e["content_sha256"]==c["result_sha256"],"checkpoint result hash")
        pos=c["next_position"]
    return pos

def vector(raw,n):
    v=json.loads(raw)
    require(type(v)==list and len(v)==n and all(type(x) in (int,float) and math.isfinite(x) for x in v),"invalid vector")
    return v

def validate_frame(db,snapshot,frame):
    f=one(db,"SELECT f.*,t.width AS tw,t.height AS th FROM texture_frame f JOIN texture_definition t ON t.snapshot_id=f.snapshot_id AND t.object_id=f.texture_id WHERE f.snapshot_id=? AND f.object_id=?",(snapshot,frame))
    require(f["x"]+f["width"]<=f["tw"] and f["y"]+f["height"]<=f["th"],"frame outside texture")

def validate_binding(db,snapshot,binding):
    b=one(db,"SELECT b.*,f.declared_uv_json FROM face_binding b JOIN model_face f ON f.snapshot_id=b.snapshot_id AND f.object_id=b.face_id WHERE b.snapshot_id=? AND b.object_id=?",(snapshot,binding))
    if b["base_uv_method"] in ("DECLARED","DEFAULT"):
        base=vector(b["base_uv_json"],4)
        if b["base_uv_method"]=="DECLARED": require(base==vector(b["declared_uv_json"],4),"declared UV mismatch")
    if b["transformed_uv_json"] is not None: vector(b["transformed_uv_json"],8)
    if b["frame_id"]: validate_frame(db,snapshot,b["frame_id"])

def reject_cycles(edges):
    graph={}
    for a,b in edges: graph.setdefault(a,[]).append(b)
    seen=set()
    active=set()
    def visit(n):
        require(n not in active,"cycle")
        if n in seen:return
        active.add(n)
        for x in graph.get(n,[]):visit(x)
        active.remove(n);seen.add(n)
    for n in graph:visit(n)

def validate_measurement(db,mid,read):
    m=one(db,"SELECT * FROM measurement WHERE measurement_id=?",(mid,))
    require(bool(m["unit"].strip() and m["coordinate_system"].strip() and m["method_version"].strip()),"missing measurement context")
    for k in ("numeric_value","numerator","denominator"):
        require(m[k] is None or math.isfinite(m[k]),"nonfinite measurement")
    if m["numerator"] is not None:
        require(m["numeric_value"] is not None and math.isclose(m["numeric_value"],m["numerator"]/m["denominator"],rel_tol=1e-9,abs_tol=1e-12),"ratio mismatch")
    if m["status"]=="PASS":
        ev=rows(db,"SELECT evidence_id FROM measurement_evidence WHERE measurement_id=?",(mid,))
        require(ev and all(evidence_ok(db,x["evidence_id"],read) for x in ev),"measurement evidence")
    return m

def render_result_guard(db,sid,q,v,read):
    require(v["render_output_id"] is not None,"render result lacks output")
    o=one(db,"SELECT o.*,c.unit_id,c.width,c.height FROM render_output o JOIN render_case c ON c.scope_id=o.scope_id AND c.case_id=o.case_id WHERE o.scope_id=? AND o.output_id=?",(sid,v["render_output_id"]))
    require(o["unit_id"]==q["unit_id"] and o["attempt_id"]==v["attempt_id"],"render case/attempt mismatch")
    require(o["generation_status"]=="GENERATED","render not generated")
    require_evidence(db,o["png_evidence_id"],read)
    if q["check_kind"]=="GENERATION":
        require(v["evidence_id"]==o["png_evidence_id"],"generation evidence mismatch")
    if q["check_kind"].startswith("ACCURACY"):
        require(v["independent_reference"]==1,"independent reference required")
        ref=q["reference_evidence_id"]
        require_evidence(db,ref,read)
        require_evidence(db,v["evidence_id"],read)
        def evidence(eid):
            return one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(eid,))
        refrow,obs,png=map(evidence,(ref,v["evidence_id"],o["png_evidence_id"]))
        require(len({refrow["content_sha256"],obs["content_sha256"],png["content_sha256"]})==3,"reference, observation and render must be distinct bodies")
        record=json.loads(read(obs))
        require(record=={"output_sha256":png["content_sha256"],"reference_sha256":refrow["content_sha256"],"case_id":o["case_id"],"attempt_id":o["attempt_id"],"check_kind":q["check_kind"],"matched":True},"accuracy report not bound to output/reference")

def assessment(db,sid,kind,selected,read):
    locked_scope(db,sid,read)
    units=rows(db,"SELECT unit_id FROM scope_unit WHERE scope_id=? AND unit_kind=? AND required=1 ORDER BY unit_id",(sid,kind))
    counts=dict(expected=len(units),attempted=0,passed=0,partial=0,held=0,failed=0)
    used=set()
    for u in units:
        reqs=rows(db,"SELECT * FROM validation_requirement WHERE scope_id=? AND unit_id=? AND mandatory=1",(sid,u["unit_id"]))
        require(reqs,"required unit has no mandatory checks")
        states=[]
        for q in reqs:
            rid=q["requirement_id"]
            if rid not in selected: states.append("UNATTEMPTED");continue
            used.add(rid)
            v=one(db,"SELECT * FROM validation_result WHERE scope_id=? AND result_id=? AND requirement_id=?",(sid,selected[rid],rid))
            state=v["status"]
            if state=="PASS":
                if not evidence_ok(db,v["evidence_id"],read):state="HOLD"
                if q["check_kind"]=="GENERATION" or q["check_kind"].startswith("ACCURACY"):
                    try:render_result_guard(db,sid,q,v,read)
                    except (ValueError,KeyError,TypeError,OSError):state="HOLD"
            states.append(state)
        if all(x=="UNATTEMPTED" for x in states):continue
        counts["attempted"]+=1
        if "FAIL" in states:counts["failed"]+=1
        elif all(x=="PASS" for x in states):counts["passed"]+=1
        elif "PASS" in states or "PARTIAL" in states:counts["partial"]+=1
        else:counts["held"]+=1
    require(set(selected)==used,"unexpected selection")
    if counts["failed"]:status="FAIL"
    elif counts["expected"] and counts["passed"]==counts["expected"]:status="PASS"
    elif counts["passed"] or counts["partial"]:status="PARTIAL"
    else:status="HOLD"
    return dict(status=status,**counts)

def latest_results(db,sid,kind):
    """Latest recorded result per mandatory requirement; attempt order is local to one task."""
    selected={}
    reqs=rows(db,"SELECT q.requirement_id FROM validation_requirement q JOIN scope_unit u ON u.scope_id=q.scope_id AND u.unit_id=q.unit_id WHERE q.scope_id=? AND q.mandatory=1 AND u.required=1 AND u.unit_kind=?",(sid,kind))
    for q in reqs:
        rid=q["requirement_id"]
        rr=rows(db,"SELECT v.result_id,a.task_id,a.attempt_no,a.lifecycle FROM validation_result v JOIN research_attempt a ON a.scope_id=v.scope_id AND a.attempt_id=v.attempt_id WHERE v.scope_id=? AND v.requirement_id=? ORDER BY a.attempt_no DESC",(sid,rid))
        if not rr:continue
        require(len({x["task_id"] for x in rr})==1,"ambiguous result across tasks")
        require(rr[0]["lifecycle"]=="FINISHED","latest result attempt not finished")
        selected[rid]=rr[0]["result_id"]
    return selected

def validate_saved_assessment(db,sid,aid,read):
    a=one(db,"SELECT * FROM run_assessment WHERE scope_id=? AND assessment_id=?",(sid,aid))
    selected={r["requirement_id"]:r["result_id"] for r in rows(db,"SELECT * FROM assessment_result WHERE scope_id=? AND assessment_id=?",(sid,aid))}
    require(selected==latest_results(db,sid,a["unit_kind"]),"stale or incomplete selected results")
    computed=assessment(db,sid,a["unit_kind"],selected,read)
    require(all(a[k]==v for k,v in computed.items()),"assessment mismatch")
    return computed

def technique_support_cases(db,claim_id,read):
    claim=one(db,"SELECT c.*,s.scope_id FROM claim c JOIN analysis_snapshot s USING(snapshot_id) WHERE claim_id=?",(claim_id,))
    supports=rows(db,"SELECT DISTINCT e.* FROM claim_evidence ce JOIN evidence_item e USING(evidence_id) WHERE ce.claim_id=? AND ce.role='SUPPORT'",(claim_id,))
    cases=[]
    for e in supports:
        require_evidence(db,e["evidence_id"],read)
        matches=rows(db,"SELECT DISTINCT o.asset_release,o.asset_path,a.digest,a.hash_algorithm,a.byte_count,r.pin_digest FROM object_evidence oe JOIN research_object o USING(snapshot_id,object_id) JOIN asset a ON a.release_key=o.asset_release AND a.source_path=o.asset_path JOIN release r ON r.release_key=a.release_key JOIN scope_source ss ON ss.asset_release=a.release_key AND ss.asset_path=a.source_path WHERE oe.snapshot_id=? AND oe.evidence_id=? AND oe.evidence_class='SOURCE' AND o.object_kind='MODEL' AND a.kind='model' AND ss.scope_id=? AND ss.included=1",(claim["snapshot_id"],e["evidence_id"],claim["scope_id"]))
        require(len(matches)==1,"support not bound to exactly one scoped model source")
        a=matches[0]
        require(a["hash_algorithm"]=="SHA256" and a["digest"]==e["content_sha256"] and a["byte_count"]==e["byte_count"],"support source hash mismatch")
        cases.append(dict(release=a["asset_release"],path=a["asset_path"],pin=a["pin_digest"],sha256=a["digest"],evidence_id=e["evidence_id"]))
    require(len({(x["release"],x["path"]) for x in cases})>=2 and len({x["sha256"] for x in cases})>=2,"two distinct source cases required")
    return sorted(cases,key=lambda x:(x["release"],x["path"],x["evidence_id"]))

def technique_approval_payload(db,tid,read):
    t=one(db,"SELECT t.*,c.certainty,c.review_status,c.revision,c.statement,c.conditions_json,c.limitations,c.snapshot_id,c.object_id,c.claim_key FROM technique t JOIN claim c USING(claim_id) WHERE technique_id=?",(tid,))
    require(t["certainty"]=="CONFIRMED" and t["review_status"]=="PASS","claim not reviewed")
    latest=one(db,"SELECT MAX(revision) AS revision FROM claim WHERE snapshot_id=? AND object_id=? AND claim_key=?",(t["snapshot_id"],t["object_id"],t["claim_key"]))
    require(latest["revision"]==t["revision"],"stale claim")
    require(not rows(db,"SELECT 1 FROM claim_evidence WHERE claim_id=? AND role='COUNTEREXAMPLE'",(t["claim_id"],)),"counterexample evidence")
    require(not rows(db,"SELECT 1 FROM claim_relation WHERE (claim_id=? OR related_claim_id=?) AND relation IN ('CONTRADICTS','COUNTEREXAMPLE')",(t["claim_id"],t["claim_id"])),"contradiction")
    reject_cycles([(x["claim_id"],x["related_claim_id"]) for x in rows(db,"SELECT claim_id,related_claim_id FROM claim_relation WHERE relation='SUPERSEDES'")])
    support=technique_support_cases(db,t["claim_id"],read)
    steps=rows(db,"SELECT * FROM technique_step WHERE technique_id=? ORDER BY step_ordinal",(tid,))
    require(steps and all(s["step_ordinal"]==i and s["instruction"].strip() and evidence_ok(db,s["evidence_id"],read) for i,s in enumerate(steps)),"steps/evidence missing")
    applicability=json.loads(t["applicability_json"])
    require(type(applicability)==dict and bool(applicability),"application conditions missing")
    return dict(technique_id=tid,claim_id=t["claim_id"],revision=t["revision"],statement=t["statement"],conditions=json.loads(t["conditions_json"]),limitations=t["limitations"],applicability=applicability,support_cases=support,steps=steps,approved_by=t["approved_by"],approved_at=t["approved_at"])

def approval_guard(db,tid,read):
    t=one(db,"SELECT * FROM technique WHERE technique_id=?",(tid,))
    require(t["disposition"]=="APPROVED" and t["approved_by"] and t["approved_at"],"not approved")
    require_evidence(db,t["approval_evidence_id"],read)
    e=one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(t["approval_evidence_id"],))
    require(json.loads(read(e))==technique_approval_payload(db,tid,read),"approval manifest mismatch")

def scoped_claim_source(db,claim,read):
    require(claim["asset_release"] and claim["asset_path"],"claim lacks original asset")
    require(bool(rows(db,"SELECT 1 FROM scope_source WHERE scope_id=? AND asset_release=? AND asset_path=? AND included=1",(claim["scope_id"],claim["asset_release"],claim["asset_path"]))),"source outside locked scope")
    require(bool(rows(db,"SELECT 1 FROM scope_unit u JOIN scope_source ss ON ss.scope_id=u.scope_id AND ss.source_ordinal=u.source_ordinal WHERE u.scope_id=? AND u.required=1 AND ss.included=1 AND ss.asset_release=? AND ss.asset_path=?",(claim["scope_id"],claim["asset_release"],claim["asset_path"]))),"claim asset lacks required validation unit")
    a=one(db,"SELECT * FROM asset WHERE release_key=? AND source_path=?",(claim["asset_release"],claim["asset_path"]))
    links=rows(db,"SELECT e.* FROM object_evidence oe JOIN evidence_item e USING(evidence_id) WHERE oe.snapshot_id=? AND oe.object_id=? AND oe.evidence_class='SOURCE'",(claim["snapshot_id"],claim["object_id"]))
    require(bool(links),"source body evidence absent")
    for e in links:
        require_evidence(db,e["evidence_id"],read)
        raw=read(e)
        digest={"SHA256":lambda:sha(raw),"SHA1":lambda:hashlib.sha1(raw).hexdigest(),"GIT_BLOB_SHA1":lambda:hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()}.get(a["hash_algorithm"])
        require(digest is not None and digest()==a["digest"] and (a["byte_count"] is None or a["byte_count"]==len(raw)),"source asset mismatch")
    return links

def export(db,read,*,label=None,term_kind=None,confirmed_only=True,metric=None,unit=None,min_value=None,release=None,allowed_releases=None):
    # Caller supplies an explicit release allowlist; None is a local fixture-only unrestricted read.
    require(allowed_releases is None or isinstance(allowed_releases,(set,frozenset,list,tuple)),"invalid release allowlist")
    require(min_value is None or (metric is not None and unit is not None and math.isfinite(min_value)),"metric/unit required")
    candidates=rows(db,"SELECT v.* FROM knowledge_search_view v WHERE (? IS NULL OR v.label=?) AND (? IS NULL OR v.term_kind=?) AND (? IS NULL OR v.asset_release=?) AND v.revision=(SELECT MAX(c.revision) FROM claim c WHERE c.snapshot_id=v.snapshot_id AND c.object_id=v.object_id AND c.claim_key=v.claim_key) ORDER BY v.claim_id",(label,label,term_kind,term_kind,release,release))
    result=[]
    for c in candidates:
        if allowed_releases is not None and c["asset_release"] not in allowed_releases:continue
        links=rows(db,"SELECT ce.role,ce.locator_detail,e.* FROM claim_evidence ce JOIN evidence_item e USING(evidence_id) WHERE claim_id=? ORDER BY role,evidence_id,locator_detail",(c["claim_id"],))
        relations=rows(db,"SELECT * FROM claim_relation WHERE claim_id=? OR related_claim_id=? ORDER BY claim_id,related_claim_id,relation",(c["claim_id"],c["claim_id"]))
        # Restricted/unknown evidence must not be emitted, even in candidate mode.
        source_rights=rows(db,"SELECT e.rights_state FROM object_evidence oe JOIN evidence_item e USING(evidence_id) WHERE oe.snapshot_id=? AND oe.object_id=? AND oe.evidence_class='SOURCE'",(c["snapshot_id"],c["object_id"]))
        if any(x["rights_state"]!="ALLOWED" for x in links+source_rights):continue
        for x in links: x["body_verified"]=evidence_ok(db,x["evidence_id"],read)
        assess=rows(db,"SELECT a.* FROM run_assessment a WHERE scope_id=? AND revision=(SELECT MAX(b.revision) FROM run_assessment b WHERE b.scope_id=a.scope_id AND b.unit_kind=a.unit_kind) ORDER BY unit_kind",(c["scope_id"],))
        groups={r["unit_kind"] for r in rows(db,"SELECT DISTINCT unit_kind FROM scope_unit WHERE scope_id=? AND required=1",(c["scope_id"],))}
        ok=bool(groups) and {a["unit_kind"] for a in assess}==groups
        try:
            locked_scope(db,c["scope_id"],read)
            source_links=scoped_claim_source(db,c,read)
            require(all(x["rights_state"]=="ALLOWED" for x in source_links),"source export rights not allowed")
            for a in assess: require(validate_saved_assessment(db,c["scope_id"],a["assessment_id"],read)["status"]=="PASS","assessment not pass")
            if c["term_kind"]=="TECHNIQUE":
                require(c["technique_id"] is not None,"technique record required")
                approval_guard(db,c["technique_id"],read)
        except ValueError:ok=False
        ok=ok and c["certainty"]=="CONFIRMED" and c["review_status"]=="PASS" and any(x["role"]=="SUPPORT" and x["body_verified"] for x in links) and all(x["body_verified"] for x in links)
        # Do not promote unresolved contradictions to reusable knowledge.
        if any(x["relation"] in ("CONTRADICTS","COUNTEREXAMPLE") for x in relations) or any(x["role"]=="COUNTEREXAMPLE" for x in links):ok=False
        measures=[]
        for m in rows(db,"SELECT * FROM measurement WHERE snapshot_id=? AND object_id=? AND (? IS NULL OR metric=?) AND (? IS NULL OR unit=?) ORDER BY measurement_id",(c["snapshot_id"],c["object_id"],metric,metric,unit,unit)):
            if rows(db,"SELECT 1 FROM measurement_evidence me JOIN evidence_item e USING(evidence_id) WHERE me.measurement_id=? AND e.rights_state<>\'ALLOWED\'",(m["measurement_id"],)):continue
            try:validate_measurement(db,m["measurement_id"],read)
            except ValueError:continue
            if m["status"]=="PASS" and (min_value is None or (m["numeric_value"] is not None and m["numeric_value"]>=min_value)):measures.append(m)
        if metric is not None and not measures:continue
        if confirmed_only and not ok:continue
        result.append(dict(claim=c,usable=bool(ok),evidence=links,relations=relations,measurements=measures,assessments=assess))
    return {"format":"DBD001-design-export-v1","filters":dict(label=label,term_kind=term_kind,confirmed_only=confirmed_only,metric=metric,unit=unit,min_value=min_value,release=release),"items":result}

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def legacy_guard(db,commit,path,read):
    import csv
    import io
    x=one(db,"SELECT * FROM legacy_disposition WHERE history_commit=? AND history_path=?",(commit,path))
    require(x["import_state"] in ("APPROVED","IMPORTED"),"not approved")
    require_evidence(db,x["approval_evidence_id"],read)
    require_evidence(db,x["evidence_id"],read)
    def body(eid):
        return read(one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(eid,)))
    raw=body(x["evidence_id"])
    require(git_blob(raw)==x["git_blob"],"legacy Git blob mismatch")
    requires_derived=x["classification"]!="REUSABLE_LIMITED" or path.endswith(("TEX05-R004/SOURCE_LEDGER.csv","TEX05-R007/BLOCK_VS_TERRAIN_SHADER.csv"))
    derived=None
    if requires_derived:
        require_evidence(db,x["derived_evidence_id"],read)
        derived=body(x["derived_evidence_id"])
        require(derived!=raw,"derived body must differ from original")
        if path.endswith(".csv"):
            records=list(csv.reader(io.StringIO(derived.decode("utf-8-sig")),strict=True))
            require(len(records)>=2 and len(records[0])>0 and all(len(z)==len(records[0]) for z in records),"derived CSV column mismatch")
    approval=json.loads(body(x["approval_evidence_id"]))
    expected=dict(history_commit=commit,history_path=path,git_blob=x["git_blob"],classification=x["classification"],original_sha256=sha(raw),derived_sha256=sha(derived) if derived is not None else None)
    require(all(approval.get(k)==v for k,v in expected.items()) and bool(approval.get("transform_version")) and bool(approval.get("reviewer")),"legacy approval not bound to transformation")
    return x

def logical_db_digest(db):
    """Canonical digest of all user-table rows, including duplicate rows and SQLite value types."""
    def encode(v):
        if isinstance(v,bytes):return ["blob",v.hex()]
        if isinstance(v,float):return ["real",v.hex()]
        if isinstance(v,int):return ["integer",str(v)]
        if v is None:return ["null",None]
        return ["text",v]
    out={}
    for row in rows(db,"SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        name=row["name"]
        quoted='"'+name.replace('"','""')+'"'
        cursor=db.execute("SELECT * FROM "+quoted)
        columns=[x[0] for x in cursor.description]
        records=sorted(canonical([encode(x) for x in item]) for item in cursor)
        out[name]={"rows":len(records),"sha256":sha(canonical({"columns":columns,"rows":records}).encode())}
    return {"app_id":db.execute("PRAGMA application_id").fetchone()[0],"user_version":db.execute("PRAGMA user_version").fetchone()[0],"tables":out}

def backup_manifest(db,read):
    items=[]
    for e in rows(db,"SELECT * FROM evidence_item ORDER BY evidence_id"):
        require_evidence(db,e["evidence_id"],read)
        items.append({k:e[k] for k in ("evidence_id","content_sha256","byte_count","locator","storage_kind","rights_state")})
    return {"evidence":items,"schema":rows(db,"SELECT type,name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"),"logical_db":logical_db_digest(db)}

def validate_restore(db,manifest,read):
    require(db.execute("PRAGMA integrity_check").fetchone()[0]=="ok" and not db.execute("PRAGMA foreign_key_check").fetchall(),"restored SQLite integrity")
    require(backup_manifest(db,read)==manifest,"restore manifest mismatch")

def apply_proposal(db,sql):
    try:
        db.executescript("BEGIN IMMEDIATE;\n"+sql+"\nCOMMIT;")
    except sqlite3.Error:
        db.rollback()
        raise
