"""Fixed T01-T16 design fixture tests. PARTIAL is not PASS."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import traceback
import struct
import zlib
from contextlib import closing
from mcfr import research_db as old, legacy_catalog
import design_contract as c
import fixture_oracle as oracle

DIR=Path(__file__).resolve().parent
ROOT=DIR.parents[3]
H="a"*64
NOW="2026-11-28T00:00:00Z"
SQL=(DIR/"schema_proposal.sql").read_text()
LOCK=json.loads((DIR/"scope_lock.json").read_text())
def put(db,table,**kw):
    db.execute("INSERT INTO "+table+" ("+",".join(kw)+") VALUES ("+",".join("?" for _ in kw)+")",tuple(kw.values()))
def bad(fn):
    try:fn()
    except (sqlite3.IntegrityError,ValueError):return
    raise AssertionError("negative control was accepted")
def rollback_test(db,fn):
    db.execute("SAVEPOINT negative")
    try:bad(fn)
    finally:
        db.execute("ROLLBACK TO negative");db.execute("RELEASE negative")
def connect(path):
    db=sqlite3.connect(path)
    db.row_factory=sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db
def schema(db):
    return c.rows(db,"SELECT type,name,tbl_name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name")
def png(w=1,h=1):
    def chunk(k,v):return struct.pack(">I",len(v))+k+v+struct.pack(">I",zlib.crc32(k+v))
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+chunk(b"IDAT",zlib.compress((b"\0"+b"\xff\0\0\xff"*w)*h))+chunk(b"IEND",b"")
def ev(db,folder,eid,raw):
    p=folder/eid
    p.write_bytes(raw)
    put(db,"evidence_item",evidence_id=eid,content_sha256=c.sha(raw),byte_count=len(raw),locator=eid,storage_kind="LOCAL_ARCHIVE",retention_state="VERIFIED_AVAILABLE",verified_at=NOW,rights_state="ALLOWED",origin_kind="DERIVED")
    return c.sha(raw)
def release(key,pin="1"*40):
    return dict(release_key=key,profile="mods",target_id="fixture",version="1",minecraft_version="1.21.11",loader="fixture",pin_algorithm="GIT_COMMIT_SHA1",pin_digest=pin,source="fixture")
def asset(path,kind,digest="b"*64):
    return dict(source_path=path,kind=kind,resource_id="fixture:"+path,hash_algorithm="SHA256",digest=digest,byte_count=1,evidence_path=None)
def obj(db,oid,kind,path=None,snapshot="snap"):
    put(db,"research_object",snapshot_id=snapshot,object_id=oid,object_kind=kind,object_key=oid,asset_release="fixture" if path else None,asset_path=path,json_pointer="/" if path else None)
def model(db,id,parent,provider,declared,res="RESOLVED"):
    obj(db,id,"MODEL",id+".json")
    put(db,"model_definition",snapshot_id="snap",object_id=id,parent_raw=parent,model_format="vanilla",elements_declared=declared,declared_element_count=1 if declared else None,raw_properties_json="{}",provider_id=provider,resolution=res)
def result(db,id,req,status,ev_id=None,ind=0,attempt="a1",output=None):
    put(db,"validation_result",scope_id="s",result_id=id,requirement_id=req,attempt_id=attempt,render_output_id=output,status=status,actual_json="{}",evidence_id=ev_id,independent_reference=ind,reason="fixture")
def fixture(db,folder):
    folder.mkdir()
    read=lambda e:(folder/e["locator"]).read_bytes()
    for id,raw in [("plan",b"fixture-plan"),("manifest",b"draft"),("source",b"fixture-source"),("calculated",b"fixture-calculated"),("reference",b"independent-expectation"),("render",png()),("support2",b"second-fixture-example"),("approval",b"fixture-review"),("checkpoint",b"fixture-result")]:
        ev(db,folder,id,raw)
    source_docs={
        "base.json":("model",{"textures":{"wood":"fixture:tex"},"elements":[{"from":[0,0,0],"to":[16,8,16],"faces":{"north":{"texture":"#wood","uv":[0,0,16,8]}}}]}),
        "child.json":("model",{"parent":"fixture:base","textures":{"missing":"#not_defined"}}),
        "state.json":("blockstate",{"multipart":[{"when":{"north":"true"},"apply":{"model":"fixture:child","y":90,"uvlock":True}}]})
    }
    bodies={p:(k,c.canonical(doc).encode()) for p,(k,doc) in source_docs.items()}
    bodies["tex.png"]=("texture",png(16,16))
    registered=[]
    for p,(kind,raw) in bodies.items():
        ev(db,folder,"raw-"+p,raw)
        a=asset(p,kind,c.sha(raw));a.update(resource_id="fixture:"+p.rsplit(".",1)[0],byte_count=len(raw))
        registered.append(a)
    old.register_release(db,release("fixture"),registered)
    old.create_run(db,"run","fixture","NEW",None)
    put(db,"research_scope",scope_id="s",run_id="run",revision=1,manifest_evidence_id="manifest",plan_evidence_id="plan",manifest_sha256=c.sha(b"draft"),plan_sha256=c.sha(b"fixture-plan"),lifecycle="DRAFT")
    put(db,"scope_source",scope_id="s",source_ordinal=0,asset_release="fixture",asset_path="base.json",included=1,reason="fixture")
    for u,k in [("u1","MODEL"),("u2","RENDER")]:
        put(db,"scope_unit",scope_id="s",unit_id=u,unit_kind=k,unit_key=u,source_ordinal=0,required=1,definition_json="{}")
    put(db,"research_task",scope_id="s",task_id="task",task_kind="fixture",ordinal=0,input_sha256=H,tool_version="fixture-v1",config_json="{}")
    for i in (1,2):
        put(db,"research_attempt",scope_id="s",task_id="task",attempt_id="a"+str(i),attempt_no=i,input_sha256=H,lifecycle="RUNNING" if i==1 else "FINISHED",started_at=NOW,ended_at=None if i==1 else NOW,environment_json="{}")
    put(db,"analysis_snapshot",snapshot_id="snap",scope_id="s",attempt_id="a1",input_sha256=H,analyzer_version="fixture",config_sha256=H)
    model(db,"base",None,"base",1)
    model(db,"child","fixture:base","base",0)
    obj(db,"el","ELEMENT","base.json")
    put(db,"model_element",snapshot_id="snap",object_id="el",model_id="base",ordinal=0,from_x=0,from_y=0,from_z=0,to_x=16,to_y=8,to_z=16,raw_properties_json="{}",coordinate_system="MC_MODEL_16")
    obj(db,"face","FACE","base.json")
    put(db,"model_face",snapshot_id="snap",object_id="face",element_id="el",direction="north",texture_raw="#wood",declared_uv_json="[0,0,16,8]",raw_properties_json="{}")
    obj(db,"tex","TEXTURE","tex.png")
    put(db,"texture_definition",snapshot_id="snap",object_id="tex",width=16,height=16,color_mode="RGBA")
    obj(db,"frame","FRAME")
    put(db,"texture_frame",snapshot_id="snap",object_id="frame",texture_id="tex",frame_ordinal=0,x=0,y=0,width=16,height=16,rgba_sha256=c.sha(b"\xff\0\0\xff"*256))
    put(db,"model_slot",snapshot_id="snap",model_id="base",slot="wood",declared_value="fixture:tex",texture_id="tex",resolution="RESOLVED")
    put(db,"model_slot",snapshot_id="snap",model_id="child",slot="missing",declared_value="#not_defined",resolution="MISSING")
    obj(db,"state","STATE","state.json")
    put(db,"state_definition",snapshot_id="snap",object_id="state",state_form="MULTIPART",raw_properties_json="{}")
    put(db,"state_rule",snapshot_id="snap",state_id="state",rule_ordinal=0,rule_form="MULTIPART",condition_json='{"north":"true"}')
    put(db,"state_option",snapshot_id="snap",state_id="state",rule_ordinal=0,option_ordinal=0,model_raw="fixture:child",model_id="child",resolution="RESOLVED",y_rotation=90,uvlock=1)
    obj(db,"app","APPLICATION")
    put(db,"state_application",snapshot_id="snap",object_id="app",state_id="state",rule_ordinal=0,option_ordinal=0,assignment_json='{"north":"true"}',selection_context="fixture",transform_json='{"y":90}',selection_status="SELECTED")
    obj(db,"instance","INSTANCE")
    put(db,"geometry_instance",snapshot_id="snap",object_id="instance",assembly_id="app",assembly_kind="APPLICATION",element_id="el",instance_ordinal=0,transform_json='{"y":90}',bbox_json="[0,0,0,16,8,16]",coordinate_system="MC_MODEL_16")
    obj(db,"binding","BINDING")
    put(db,"face_binding",snapshot_id="snap",object_id="binding",instance_id="instance",element_id="el",face_id="face",context_key="fixture",texture_id="tex",frame_id="frame",resolution="RESOLVED",base_uv_json="[0,0,16,8]",base_uv_method="DECLARED",transformed_uv_json="[0,0,0,8,16,8,16,0]",transform_method="fixture",uv_status="PASS")
    put(db,"reference_edge",snapshot_id="snap",edge_id="parent",from_object_id="child",edge_kind="PARENT",declared_reference="fixture:base",target_release="fixture",target_path="base.json",resolution="RESOLVED",detail="")
    put(db,"reference_edge",snapshot_id="snap",edge_id="missing",from_object_id="child",edge_kind="TEXTURE_ALIAS",declared_reference="#not_defined",resolution="MISSING",detail="fixture")
    put(db,"measurement",measurement_id="height",snapshot_id="snap",object_id="base",metric="height",method_version="fixture-v1",input_sha256=H,context_key="local",unit="block",coordinate_system="MC_MODEL_16",evidence_class="CALCULATED",numeric_value=.5,numerator=8,denominator=16,status="PASS",reason="")
    put(db,"measurement_evidence",measurement_id="height",evidence_id="calculated",locator_detail="fixture")
    for oid,path,pointer in [("base","base.json",""),("child","child.json",""),("el","base.json","/elements/0"),("face","base.json","/elements/0/faces/north"),("tex","tex.png",None),("state","state.json","")]:
        db.execute("UPDATE research_object SET json_pointer=? WHERE snapshot_id='snap' AND object_id=?",(pointer,oid))
        put(db,"object_evidence",snapshot_id="snap",object_id=oid,evidence_id="raw-"+path,evidence_class="SOURCE",locator_detail=pointer or "")
    put(db,"render_case",scope_id="s",case_id="case",unit_id="u2",snapshot_id="snap",object_id="app",camera_json="{}",settings_json="{}",width=1,height=1)
    put(db,"render_output",scope_id="s",output_id="output",case_id="case",attempt_id="a1",generation_status="GENERATED",png_evidence_id="render",environment_json="{}",reason="")
    for id,unit,kind,ref in [("structure","u1","STRUCTURE",None),("generation","u2","GENERATION",None),("accuracy","u2","ACCURACY_UV","reference")]:
        put(db,"validation_requirement",scope_id="s",requirement_id=id,unit_id=unit,check_kind=kind,mandatory=1,expected_json="{}",reference_evidence_id=ref)
    mraw=c.canonical({"scope_fingerprint":c.scope_fingerprint(db,"s")}).encode()
    (folder/"manifest").write_bytes(mraw)
    db.execute("UPDATE evidence_item SET content_sha256=?,byte_count=? WHERE evidence_id='manifest'",(c.sha(mraw),len(mraw)))
    db.execute("UPDATE research_scope SET lifecycle='LOCKED',locked_at=?,approved_by='fixture',manifest_sha256=? WHERE scope_id='s'",(NOW,c.sha(mraw)))
    put(db,"task_checkpoint",scope_id="s",attempt_id="a1",batch_no=0,next_position=1,input_sha256=H,result_evidence_id="checkpoint",result_sha256=c.sha(b"fixture-result"),committed_at=NOW)
    db.execute("UPDATE research_attempt SET lifecycle='FINISHED',ended_at=? WHERE attempt_id='a1'",(NOW,))
    result(db,"struct","structure","PASS","calculated")
    result(db,"gen","generation","PASS","render",output="output")
    result(db,"falseaccuracy","accuracy","PASS","render",output="output")
    put(db,"render_output",scope_id="s",output_id="output2",case_id="case",attempt_id="a2",generation_status="GENERATED",png_evidence_id="render",environment_json="{}",reason="")
    result(db,"accurate","accuracy","PASS","render",1,"a2",output="output2")
    for term,kind,label in [("chair","FURNITURE","chair"),("part","PART","seat"),("tech","TECHNIQUE","layering")]:
        put(db,"semantic_term",term_id=term,term_kind=kind,label=label,definition="fixture")
    for id,term,certainty,review,cls,rev,key in [("old","chair","ESTIMATED","PARTIAL","INFERRED",1,"category"),("confirmed","chair","CONFIRMED","PASS","INFERRED",2,"category"),("unknown","part","UNKNOWN","HOLD","UNKNOWN",1,"part"),("candidate","tech","ESTIMATED","PARTIAL","INFERRED",1,"tech"),("approved","tech","CONFIRMED","PASS","INFERRED",1,"approved")]:
        put(db,"claim",claim_id=id,snapshot_id="snap",object_id="base",term_id=term,claim_key=key,revision=rev,statement="fixture "+id,evidence_class=cls,certainty=certainty,review_status=review,conditions_json='{"fixture":true}',limitations="synthetic only",reviewer="fixture" if certainty=="CONFIRMED" else None,reviewed_at=NOW if certainty=="CONFIRMED" else None)
    for id in ("confirmed","candidate","approved"):
        put(db,"claim_evidence",claim_id=id,evidence_id="source",role="SUPPORT",locator_detail="fixture")
    put(db,"claim_evidence",claim_id="approved",evidence_id="support2",role="SUPPORT",locator_detail="fixture2")
    put(db,"technique",technique_id="candidate",claim_id="candidate",disposition="CANDIDATE",applicability_json='{"fixture":true}')
    put(db,"technique",technique_id="approved",claim_id="approved",disposition="APPROVED",applicability_json='{"fixture":true}',approval_evidence_id="approval",approved_by="fixture",approved_at=NOW)
    put(db,"technique_step",technique_id="approved",step_ordinal=0,instruction="fixture step",conditions_json="{}",evidence_id="source")
    for aid,kind,sel in [("model-pass","MODEL",{"structure":"struct"}),("render-pass","RENDER",{"generation":"gen","accuracy":"accurate"})]:
        value=c.assessment(db,"s",kind,sel,read)
        put(db,"run_assessment",scope_id="s",assessment_id=aid,revision=1,unit_kind=kind,reason="fixture",assessed_at=NOW,**value)
        for req,res in sel.items():put(db,"assessment_result",scope_id="s",assessment_id=aid,requirement_id=req,result_id=res)
    db.commit()
    return read

def main(out):
    reports=[]
    def test(id,fn,limit=None):
        try:
            detail=fn()
            rec=dict(id=id,status="PARTIAL" if limit else "PASS",detail=detail,limit=limit)
        except Exception as exc:
            rec=dict(id=id,status="FAIL",detail=str(exc),traceback=traceback.format_exc())
        reports.append(rec)
        print("DBD001_TEST "+c.canonical(rec),flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        folder=Path(tmp)
        orig=folder/"original.sqlite"
        copy=folder/"copy.sqlite"
        old.initialize(orig)
        with closing(old.open_db(orig,"rw")) as db:
            with old.write_transaction(db):
                first=legacy_catalog.import_catalog(db,ROOT,old.register_release)
            before=schema(db)
            before_rows={n:db.execute("SELECT count(*) FROM "+n).fetchone()[0] for n in LOCK["existing_tables"]}
            with closing(connect(copy)) as dst:db.backup(dst)
        orig_hash=c.sha(orig.read_bytes())
        with closing(connect(copy)) as db:
            c.apply_proposal(db,SQL)
            def t01():
                assert all(x in schema(db) for x in before)
                assert old.db_identity(db)==(old.APP_ID,4)
                assert {n:db.execute("SELECT count(*) FROM "+n).fetchone()[0] for n in LOCK["existing_tables"]}==before_rows
                with old.write_transaction(db):assert legacy_catalog.import_catalog(db,ROOT,old.register_release)["assets_added"]==0
                return {"existing_tables":8,"unchanged_rows":before_rows}
            test("T01",t01)
            def t02():
                assert first["assets_added"]==25387
                assert sorted(first["assets_added_by_release"].values())==[2994,3999,4768,13626]
                with old.write_transaction(db):second=legacy_catalog.import_catalog(db,ROOT,old.register_release)
                assert second["assets_added"]==0
                return {"initial":first,"repeat":second}
            test("T02",t02)
            read=fixture(db,folder/"evidence")
            def t03():
                rollback_test(db,lambda:old.register_release(db,release("fixture","2"*40),[]))
                rollback_test(db,lambda:old.register_release(db,release("fixture"),[asset("base.json","model","c"*64)]))
                rollback_test(db,lambda:c.register_guard(db,"fixture","base.json","SHA256","c"*64,1))
                put(db,"unregistered_source",release_key="fixture",source_path="unsupported",format="bin",content_sha256=H,byte_count=1,support_state="UNSUPPORTED",evidence_id="source")
                rollback_test(db,lambda:c.register_guard(db,"fixture","unsupported","SHA256",H,1))
                assert old.register_release(db,release("fixture-new","2"*40),[asset("base.json","model","c"*64)])==1
                db.commit()
                return "version distinct; conflicting existing key/digest and cross-catalog path blocked by guard"
            test("T03",t03)
            def t04():
                assert c.validate_checkpoint(db,"s","a1",read)==1
                def mutate():
                    db.execute("UPDATE scope_unit SET unit_key='changed' WHERE unit_id='u1'")
                    c.locked_scope(db,"s",read)
                rollback_test(db,mutate)
                def mutate_checkpoint():
                    db.execute("UPDATE task_checkpoint SET result_sha256=? WHERE attempt_id='a1'",(H,))
                    c.validate_checkpoint(db,"s","a1",read)
                rollback_test(db,mutate_checkpoint)
                rollback_test(db,lambda:db.execute("DELETE FROM scope_unit WHERE unit_id='u1'"))
                rollback_test(db,lambda:db.execute("UPDATE research_scope SET lifecycle='DRAFT' WHERE scope_id='s'"))
                rollback_test(db,lambda:put(db,"scope_unit",scope_id="s",unit_id="extra",unit_kind="MODEL",unit_key="extra",required=1,definition_json="{}"))
                assert c.append_checkpoint(db,"s","a1",1,"checkpoint",read,committed_at=NOW) is False
                rollback_test(db,lambda:c.append_checkpoint(db,"s","a1",1,"support2",read,committed_at=NOW))
                db.execute("SAVEPOINT resume")
                rollback_test(db,lambda:c.append_checkpoint(db,"s","a1",2,"support2",read,committed_at=NOW))
                db.execute("UPDATE research_attempt SET lifecycle='RUNNING' WHERE attempt_id='a1'")
                assert c.append_checkpoint(db,"s","a1",2,"support2",read,committed_at=NOW)
                assert c.validate_checkpoint(db,"s","a1",read)==2
                db.execute("ROLLBACK TO resume");db.execute("RELEASE resume")
                assert c.validate_checkpoint(db,"s","a1",read)==1
                for recursive in (0,1):
                    db.execute("PRAGMA recursive_triggers="+str(recursive))
                    rollback_test(db,lambda:db.execute("INSERT OR REPLACE INTO research_scope SELECT * FROM research_scope WHERE scope_id='s'"))
                return "locked definition and REPLACE blocked; finished append rejected; retry and rollback verified"
            test("T04",t04,"local transaction fixture; cross-job restart and full execution writer not implemented")
            def t05():
                assert c.one(db,"SELECT provider_id,declared_element_count FROM model_definition WHERE object_id='child'")=={"provider_id":"base","declared_element_count":None}
                assert c.one(db,"SELECT to_y FROM model_element WHERE object_id='el'")["to_y"]==8
                assert c.one(db,"SELECT numeric_value FROM measurement WHERE measurement_id='height'")["numeric_value"]==.5
                rollback_test(db,lambda:put(db,"model_definition",snapshot_id="snap",object_id="face",model_format="fixture",elements_declared=0,raw_properties_json="{}",resolution="UNKNOWN"))
                assert oracle.validate_model(db,"snap","base",read)=="base"
                assert oracle.validate_model(db,"snap","child",read)=="base"
                def coord():
                    db.execute("UPDATE model_element SET to_y=9 WHERE object_id='el'")
                    oracle.validate_model(db,"snap","base",read)
                rollback_test(db,coord)
                def ptr():
                    db.execute("UPDATE research_object SET json_pointer='/elements/99' WHERE object_id='el'")
                    oracle.validate_model(db,"snap","base",read)
                rollback_test(db,ptr)
                bad(lambda:oracle.strict_json(b'{"a":1,"a":2}'))
                return "actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked"
            test("T05",t05)
            def t06():
                c.validate_binding(db,"snap","binding")
                assert c.one(db,"SELECT texture_id,resolution FROM model_slot WHERE slot='missing'")=={"texture_id":None,"resolution":"MISSING"}
                def frame():
                    db.execute("UPDATE texture_frame SET width=17 WHERE object_id='frame'")
                    c.validate_frame(db,"snap","frame")
                rollback_test(db,frame)
                def uv():
                    db.execute("UPDATE face_binding SET base_uv_json='[1,2]' WHERE object_id='binding'")
                    c.validate_binding(db,"snap","binding")
                rollback_test(db,uv)
                assert oracle.validate_texture(db,"snap","tex",read)==(16,16)
                def pixel():
                    db.execute("UPDATE texture_frame SET rgba_sha256=? WHERE object_id='frame'",(H,))
                    oracle.validate_texture(db,"snap","tex",read)
                rollback_test(db,pixel)
                bad(lambda:oracle.rgba_png(png()[:-1]))
                return "actual synthetic RGBA PNG bytes, frame pixel SHA, bounds, UV dimensionality and missing slot checked"
            test("T06",t06,"fixture RGBA frame extraction verified; full UV transform accuracy not verified")
            def t07():
                assert c.one(db,"SELECT uvlock,y_rotation FROM state_option")=={"uvlock":1,"y_rotation":90}
                assert c.one(db,"SELECT resolution,target_path FROM reference_edge WHERE edge_id='missing'")=={"resolution":"MISSING","target_path":None}
                c.reject_cycles([("child","base")])
                bad(lambda:c.reject_cycles([("child","base"),("base","child")]))
                rollback_test(db,lambda:db.execute("UPDATE state_option SET model_id='absent' WHERE state_id='state'"))
                assert oracle.validate_state(db,"snap","state",read)==1
                def state():
                    db.execute("UPDATE state_application SET assignment_json='{}' WHERE object_id='app'")
                    oracle.validate_state(db,"snap","state",read)
                rollback_test(db,state)
                def option():
                    db.execute("UPDATE state_option SET y_rotation=180 WHERE state_id='state'")
                    oracle.validate_state(db,"snap","state",read)
                rollback_test(db,option)
                return "actual multipart source condition, selected option, model target, transform and negative controls"
            test("T07",t07,"simple multipart fixture verified; complete namespace and condition resolver not verified")
            def t08():
                assert c.one(db,"SELECT generation_status FROM render_output WHERE output_id='output'")["generation_status"]=="GENERATED"
                assert c.assessment(db,"s","RENDER",{"generation":"gen"},read)["status"]=="PARTIAL"
                assert c.assessment(db,"s","RENDER",{"generation":"gen","accuracy":"falseaccuracy"},read)["status"]=="PARTIAL"
                assert c.assessment(db,"s","RENDER",{"generation":"gen","accuracy":"accurate"},read)["status"]=="PASS"
                assert struct.unpack(">II",read(c.one(db,"SELECT * FROM evidence_item WHERE evidence_id='render'"))[16:24])==(1,1)
                assert oracle.validate_render(db,"s","output",read)["attempt_id"]=="a1"
                assert oracle.validate_render(db,"s","output2",read)["attempt_id"]=="a2"
                bad(lambda:oracle.rgba_png(png()[:-1]))
                return "actual PNG decode, render dimensions, independent-reference metadata and attempt links checked"
            test("T08",t08,"synthetic PNG checked; full case/output/result consistency and independent visual accuracy not verified")
            def t09():
                assert c.one(db,"SELECT certainty FROM claim WHERE claim_id='unknown'")["certainty"]=="UNKNOWN"
                assert c.one(db,"SELECT to_y FROM model_element WHERE object_id='el'")["to_y"]==8
                rollback_test(db,lambda:db.execute("UPDATE claim SET certainty='CONFIRMED' WHERE claim_id='unknown'"))
                return "UNKNOWN independent of geometry; invalid confirmation rejected"
            test("T09",t09)
            def t10():
                assert c.validate_measurement(db,"height",read)["numeric_value"]==.5
                def ratio():
                    db.execute("UPDATE measurement SET numeric_value=9 WHERE measurement_id='height'")
                    c.validate_measurement(db,"height",read)
                rollback_test(db,ratio)
                def units():
                    db.execute("UPDATE measurement SET unit='' WHERE measurement_id='height'")
                    c.validate_measurement(db,"height",read)
                rollback_test(db,units)
                return "ratio, unit and finite value guards"
            test("T10",t10,"no independent style or comparative measurement method validation")
            def t11():
                c.approval_guard(db,"approved",read)
                bad(lambda:c.approval_guard(db,"candidate",read))
                def support():
                    db.execute("DELETE FROM claim_evidence WHERE claim_id='approved' AND evidence_id='support2'")
                    c.approval_guard(db,"approved",read)
                rollback_test(db,support)
                return "candidate blocked; two distinct support bodies and steps required"
            test("T11",t11,"distinct bodies not necessarily independent source cases; no full approval transition or claim relation cycle enforcement")
            def t12():
                assert c.assessment(db,"s","MODEL",{},read)["status"]=="HOLD"
                assert c.assessment(db,"s","MODEL",{"structure":"struct"},read)["status"]=="PASS"
                assert c.validate_saved_assessment(db,"s","model-pass",read)["passed"]==1
                db.execute("SAVEPOINT stale")
                result(db,"fail","structure","FAIL",attempt="a2")
                assert c.latest_results(db,"s","MODEL")=={"structure":"fail"}
                assert c.assessment(db,"s","MODEL",{"structure":"fail"},read)["status"]=="FAIL"
                bad(lambda:c.validate_saved_assessment(db,"s","model-pass",read))
                assert not c.export(db,read,label="chair")["items"]
                db.execute("ROLLBACK TO stale");db.execute("RELEASE stale")
                assert c.assessment(db,"s","RENDER",{"generation":"gen"},read)["status"]=="PARTIAL"
                rollback_test(db,lambda:db.execute("UPDATE run_assessment SET expected=2 WHERE assessment_id='model-pass'"))
                db.commit()
                return "four verdicts, denominator, latest result selection and stale PASS rejection"
            test("T12",t12)
            def t13():
                x=c.export(db,read,label="chair",metric="height",unit="block",min_value=.4,release="fixture")
                assert [i["claim"]["claim_id"] for i in x["items"]]==["confirmed"]
                assert not c.export(db,read,label="chair",metric="height",unit="pixel",min_value=.4)["items"]
                assert json.loads(c.canonical(x))==x
                assert {i["claim"]["claim_id"] for i in c.export(db,read,label="layering")["items"]}=={"approved"}
                db.execute("SAVEPOINT missinggroup")
                db.execute("DELETE FROM assessment_result WHERE assessment_id='render-pass'")
                db.execute("DELETE FROM run_assessment WHERE assessment_id='render-pass'")
                assert not c.export(db,read,label="chair")["items"]
                db.execute("ROLLBACK TO missinggroup");db.execute("RELEASE missinggroup")
                db.execute("SAVEPOINT unfinished")
                db.execute("UPDATE research_attempt SET lifecycle='RUNNING' WHERE attempt_id='a2'")
                assert not c.export(db,read,label="chair")["items"]
                db.execute("ROLLBACK TO unfinished");db.execute("RELEASE unfinished")
                db.execute("SAVEPOINT counterexample")
                put(db,"claim_evidence",claim_id="confirmed",evidence_id="support2",role="COUNTEREXAMPLE",locator_detail="fixture")
                assert not c.export(db,read,label="chair")["items"]
                db.execute("ROLLBACK TO counterexample");db.execute("RELEASE counterexample")
                p=folder/"evidence"/"source";raw=p.read_bytes()
                try:
                    p.write_bytes(b"corrupt")
                    assert not c.export(db,read,label="chair")["items"]
                    assert c.export(db,read,label="chair",confirmed_only=False)["items"][0]["usable"] is False
                finally:p.write_bytes(raw)
                put(db,"claim_relation",claim_id="confirmed",related_claim_id="unknown",relation="CONTRADICTS",reason="fixture")
                assert not c.export(db,read,label="chair")["items"]
                db.commit()
                return "revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls"
            test("T13",t13,"design prototype; production permission and source case authorization not integrated")
            def t14():
                for p in ("TEX05-R004/SOURCE_LEDGER.csv","TEX05-R007/BLOCK_VS_TERRAIN_SHADER.csv"):
                    put(db,"legacy_disposition",history_commit="fixture",history_path=p,git_blob="f"*40,classification="REVALIDATE",import_state="QUARANTINED",reason="fixture",evidence_id="source")
                    bad(lambda:c.legacy_guard(db,"fixture",p,read))
                    def bypass():
                        db.execute("UPDATE legacy_disposition SET import_state='APPROVED',approval_evidence_id='approval' WHERE history_path=?",(p,))
                        c.legacy_guard(db,"fixture",p,read)
                    rollback_test(db,bypass)
                for p in ("duplicate1","duplicate2"):
                    put(db,"legacy_disposition",history_commit="fixture",history_path=p,git_blob="e"*40,classification="DUPLICATE_CANDIDATE",import_state="NOT_APPROVED",reason="fixture",evidence_id="source")
                assert db.execute("SELECT count(*) FROM legacy_disposition WHERE git_blob=?",("e"*40,)).fetchone()[0]==2
                db.commit()
                return "two malformed CSV names quarantined; identical blob paths preserved"
            test("T14",t14,"fixture guard only; no transformation approval/import runner")
            def t15():
                db.commit()
                before2=schema(db)
                try:c.apply_proposal(db,SQL)
                except sqlite3.Error:pass
                else:raise AssertionError("reapplication accepted")
                assert schema(db)==before2
                try:c.apply_proposal(db,"CREATE TABLE rollback_fixture (id INTEGER); INVALID SQL;")
                except sqlite3.Error:pass
                else:raise AssertionError("invalid SQL accepted")
                assert schema(db)==before2
                assert c.sha(orig.read_bytes())==orig_hash
                return "reapplication rejected atomically; partial DDL rolled back; source unchanged"
            test("T15",t15)
            def t16():
                db.commit()
                restore=folder/"restored.sqlite"
                with closing(connect(restore)) as dst:db.backup(dst)
                shutil.copytree(folder/"evidence",folder/"restored-evidence")
                with closing(connect(restore)) as rb:
                    rr=lambda e:(folder/"restored-evidence"/e["locator"]).read_bytes()
                    assert all(c.evidence_ok(rb,x["evidence_id"],rr) for x in c.rows(rb,"SELECT evidence_id FROM evidence_item"))
                    assert [tuple(x) for x in rb.execute("PRAGMA integrity_check")]==[("ok",)]
                    assert not rb.execute("PRAGMA foreign_key_check").fetchall()
                    assert c.validate_checkpoint(rb,"s","a1",rr)==1
                assert c.sha(orig.read_bytes())==orig_hash
                return "local backup restored, evidence hashes, checkpoint and FK verified"
            test("T16",t16,"local temporary restore only; real artifact expiry and cross-job restore not exercised")
            assert not db.execute("PRAGMA foreign_key_check").fetchall()
            assert [tuple(x) for x in db.execute("PRAGMA integrity_check")]==[("ok",)]
    assert [x["id"] for x in reports]==[x["id"] for x in LOCK["required_checks"]]
    counts={s:sum(x["status"]==s for x in reports) for s in ("PASS","PARTIAL","HOLD","FAIL")}
    data=dict(gate="7-G",executed=len(reports),counts=counts,status="FAIL" if counts["FAIL"] else "PARTIAL" if counts["PARTIAL"] or counts["HOLD"] else "PASS",scope_sha256=c.sha((DIR/"scope_lock.json").read_bytes()),schema_sha256=c.sha(SQL.encode()),contract_sha256=c.sha((DIR/"design_contract.py").read_bytes()),test_sha256=c.sha(Path(__file__).read_bytes()),tests=reports)
    out.mkdir(parents=True,exist_ok=True)
    (out/"G_results.json").write_text(c.canonical(data)+"\n",encoding="utf-8")
    print("DBD001_G_SUMMARY "+c.canonical({k:v for k,v in data.items() if k!="tests"}),flush=True)
    return int(counts["FAIL"]>0)
if __name__=="__main__":
    import sys
    raise SystemExit(main(Path(sys.argv[1])))
