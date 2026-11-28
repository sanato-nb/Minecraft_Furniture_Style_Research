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

def approval_guard(db,tid,read):
    t=one(db,"SELECT t.*,c.certainty,c.review_status FROM technique t JOIN claim c USING(claim_id) WHERE technique_id=?",(tid,))
    require(t["disposition"]=="APPROVED" and t["certainty"]=="CONFIRMED" and t["review_status"]=="PASS","not approved")
    require_evidence(db,t["approval_evidence_id"],read)
    support=rows(db,"SELECT e.* FROM claim_evidence c JOIN evidence_item e USING(evidence_id) WHERE c.claim_id=? AND c.role='SUPPORT'",(t["claim_id"],))
    require(len({e["content_sha256"] for e in support if evidence_ok(db,e["evidence_id"],read)})>=2,"two distinct supporting bodies required for fixture")
    steps=rows(db,"SELECT * FROM technique_step WHERE technique_id=? ORDER BY step_ordinal",(tid,))
    require(steps and all(s["step_ordinal"]==i and s["instruction"].strip() and evidence_ok(db,s["evidence_id"],read) for i,s in enumerate(steps)),"steps/evidence missing")
    require(bool(json.loads(t["applicability_json"])),"application conditions missing")

def export(db,read,*,label=None,term_kind=None,confirmed_only=True,metric=None,unit=None,min_value=None,release=None):
    require(min_value is None or (metric is not None and unit is not None and math.isfinite(min_value)),"metric/unit required")
    candidates=rows(db,"SELECT v.* FROM knowledge_search_view v WHERE (? IS NULL OR v.label=?) AND (? IS NULL OR v.term_kind=?) AND (? IS NULL OR v.asset_release=?) AND v.revision=(SELECT MAX(c.revision) FROM claim c WHERE c.snapshot_id=v.snapshot_id AND c.object_id=v.object_id AND c.claim_key=v.claim_key) ORDER BY v.claim_id",(label,label,term_kind,term_kind,release,release))
    result=[]
    for c in candidates:
        links=rows(db,"SELECT ce.role,ce.locator_detail,e.* FROM claim_evidence ce JOIN evidence_item e USING(evidence_id) WHERE claim_id=? ORDER BY role,evidence_id,locator_detail",(c["claim_id"],))
        relations=rows(db,"SELECT * FROM claim_relation WHERE claim_id=? OR related_claim_id=? ORDER BY claim_id,related_claim_id,relation",(c["claim_id"],c["claim_id"]))
        for x in links: x["body_verified"]=evidence_ok(db,x["evidence_id"],read)
        assess=rows(db,"SELECT a.* FROM run_assessment a WHERE scope_id=? AND revision=(SELECT MAX(b.revision) FROM run_assessment b WHERE b.scope_id=a.scope_id AND b.unit_kind=a.unit_kind) ORDER BY unit_kind",(c["scope_id"],))
        groups={r["unit_kind"] for r in rows(db,"SELECT DISTINCT unit_kind FROM scope_unit WHERE scope_id=? AND required=1",(c["scope_id"],))}
        ok=bool(groups) and {a["unit_kind"] for a in assess}==groups
        try:
            locked_scope(db,c["scope_id"],read)
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
            try:validate_measurement(db,m["measurement_id"],read)
            except ValueError:continue
            if m["status"]=="PASS" and (min_value is None or (m["numeric_value"] is not None and m["numeric_value"]>=min_value)):measures.append(m)
        if metric is not None and not measures:continue
        if confirmed_only and not ok:continue
        # Metadata only, no restricted raw bytes.
        result.append(dict(claim=c,usable=bool(ok),evidence=links,relations=relations,measurements=measures,assessments=assess))
    return {"format":"DBD001-design-export-v1","filters":dict(label=label,term_kind=term_kind,confirmed_only=confirmed_only,metric=metric,unit=unit,min_value=min_value,release=release),"items":result}

def legacy_guard(db,commit,path,read):
    x=one(db,"SELECT * FROM legacy_disposition WHERE history_commit=? AND history_path=?",(commit,path))
    require(x["import_state"] in ("APPROVED","IMPORTED"),"not approved")
    require_evidence(db,x["approval_evidence_id"],read)
    require_evidence(db,x["evidence_id"],read)
    if x["classification"]!="REUSABLE_LIMITED":require_evidence(db,x["derived_evidence_id"],read)
    if path.endswith("TEX05-R004/SOURCE_LEDGER.csv") or path.endswith("TEX05-R007/BLOCK_VS_TERRAIN_SHADER.csv"):
        require_evidence(db,x["derived_evidence_id"],read)
    return x

def apply_proposal(db,sql):
    try:
        db.executescript("BEGIN IMMEDIATE;\n"+sql+"\nCOMMIT;")
    except sqlite3.Error:
        db.rollback()
        raise
