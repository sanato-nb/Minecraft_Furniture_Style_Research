#!/usr/bin/env python3
"""1-2-G Entry6 direct audit of the user-extracted Minecraft Java 1.21.11 sources.
Never certifies the official JAR, game renderer, animation playback, or PZ meaning.
Writes only new phase_1-2-G/entry6 evidence; does not change A-F or v69 originals.
"""
import collections
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
G = "research/vanilla_models/phase_1-2-G/entry6/"
OUT = ROOT / G
OUT.mkdir(parents=True, exist_ok=True)
PNG_C = "research/vanilla_models/phase_1-2-C/entry5/C_PNG_UNIQUE_ALL.csv"
MODEL_C = "research/vanilla_models/phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv"
F_STATUS = "research/vanilla_models/phase_1-2-F/entry6/F_MODEL_SOURCE_STATUS.csv"
F_GEO = "research/vanilla_models/phase_1-2-F/entry6/F_GEOMETRY_FEATURES.csv"
D_ONE = "research/vanilla_models/phase_1-2-D/entry6/D_ENTRY6_265_RULES.csv"
D_TWO = None  # D Entry6 single consolidated original-rule ledger
F_VIS = "research/vanilla_models/phase_1-2-F/entry6/F3_PNG_FIRST_FRAME_332.csv"
Q = G + "G_ENTRY6_QUEUE_829.csv"

def source(path):
    return (ROOT / path).read_bytes()

def gitsha(b):
    return hashlib.sha1(("blob " + str(len(b)) + "\0").encode("ascii") + b).hexdigest()

def readrows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def index(path, col):
    return {x[col]:x for x in readrows(path)}

def dump(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def writecsv(name,records,fields):
    with (OUT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader();w.writerows(records)

def b(x):
    return str(x).strip().lower() in ("1","true","yes")

def strval(x):
    return "" if x is None else str(x)

def modelpath(ref):
    if not ref:return None
    x=ref.split(":",1)[-1]
    if not x.startswith(("block/","item/")):x="block/"+x
    return "1.21.11/assets/minecraft/models/"+x+".json"

def state_options(obj):
    opts=[]
    for i,(condition,apply) in enumerate((obj.get("variants") or {}).items()):
        alternatives=apply if isinstance(apply,list) else [apply]
        for j,a in enumerate(alternatives):
            opts.append(dict(kind="variants",index=i,condition=condition,option=j,count=len(alternatives),apply=a))
    for i,r in enumerate(obj.get("multipart",[]) or []):
        alternatives=r["apply"] if isinstance(r["apply"],list) else [r["apply"]]
        for j,a in enumerate(alternatives):
            opts.append(dict(kind="multipart",index=i,condition=r.get("when"),option=j,count=len(alternatives),apply=a))
    return opts

def resolved_faces(objchain):
    provider=next((p for p,data,sha in objchain if isinstance(data.get("elements"),list) and len(data["elements"])>0),None)
    items=(next(data["elements"] for p,data,sha in objchain if p==provider) if provider else [])
    merged={}
    for path,data,sha in objchain[::-1]:merged.update(data.get("textures") or {})
    faces=[]
    for ei,elem in enumerate(items):
        for direction,face in (elem.get("faces") or {}).items():
            tex=face.get("texture")
            visited=set()
            cur=tex
            reason=""
            for k in range(45):
                if not isinstance(cur,str) or not cur:
                    cur=None;reason="MISSING_TEXTURE_SLOT";break
                if not cur.startswith("#"):break
                slot=cur[1:]
                if slot in visited:cur=None;reason="TEXTURE_CYCLE";break
                visited.add(slot)
                cur=merged.get(slot)
            else:cur=None;reason="ALIAS_DEPTH"
            faces.append(dict(element=ei,direction=direction,texture_raw=tex,
                resolved_texture=cur,unbound_reason=reason,uv_key_explicit="uv" in face,
                cullface_key_explicit="cullface" in face,tintindex_key_explicit="tintindex" in face))
    return provider,items,faces

def json_sha_and_obj(path,expected,errors):
    try:
        raw=source(path);actual=gitsha(raw)
        if actual!=expected:errors.append(dict(path=path,kind="SOURCE_SHA",expected=expected,actual=actual))
        return actual,json.loads(raw.decode("utf-8"))
    except Exception as e:
        errors.append(dict(path=path,kind="JSON_READ",message=str(e)));return None,None

def pixel(path,expected,prior,errors):
    try:
        raw=source(path);actual=gitsha(raw)
        if actual!=expected:errors.append(dict(path=path,kind="PNG_GIT_SHA",expected=expected,actual=actual))
        if raw[:8]!=b"\x89PNG\r\n\x1a\n":raise ValueError("PNG signature mismatch")
        with Image.open(io.BytesIO(raw)) as im:
            im.load()
            mode=im.mode;size=im.size
            rgba=im.convert("RGBA").tobytes()
            alpha=rgba[3::4]
            opaque=alpha.count(255);transparent=alpha.count(0);partial=len(alpha)-opaque-transparent
            record=dict(path=path,git_blob_sha=actual,bytes=len(raw),file_sha256=hashlib.sha256(raw).hexdigest(),
                png_signature="PASS",pillow_full_decode="PASS",width=size[0],height=size[1],mode=mode,
                rgba_sha256=hashlib.sha256(rgba).hexdigest(),opaque_pixels=opaque,transparent_pixels=transparent,
                partial_alpha_pixels=partial,unique_alpha_values=len(set(alpha)),
                prior_C_verified="YES" if prior else "NO_G_DIRECT_ONLY",
                C_RGBA_match="NOT_IN_C_PRIOR" if not prior else "PENDING")
            if prior:
                fields={"png_sha":actual,"width":size[0],"height":size[1],"mode":mode,
                    "rgba_sha256":record["rgba_sha256"],"opaque_pixels":opaque,"transparent_pixels":transparent,
                    "partial_alpha_pixels":partial,"unique_alpha_values":len(set(alpha))}
                match=all(str(prior[k])==str(v) for k,v in fields.items())
                record["C_RGBA_match"]="PASS" if match else "MISMATCH"
                if not match:errors.append(dict(path=path,kind="C_RGBA_PIXEL_DIMENSION_MODE_ALPHA",source=fields,prior=prior))
            side=Path(str(ROOT/path)+".mcmeta")
            if side.exists():
                sb=side.read_bytes();meta=json.loads(sb.decode("utf-8"))
                if prior and prior.get("mcmeta_sha") and gitsha(sb)!=prior["mcmeta_sha"]:
                    errors.append(dict(path=str(side.relative_to(ROOT)),kind="MCMETA_SOURCE_SHA"))
                record["mcmeta_sha"]=gitsha(sb)
                record["mcmeta_animation_static"]="YES" if "animation" in meta else "NO"
                record["mcmeta_animation_value"]=json.dumps(meta.get("animation",None),ensure_ascii=False,separators=(",",":"))
            else:
                record["mcmeta_sha"]=""
                record["mcmeta_animation_static"]="NO"
                record["mcmeta_animation_value"]=""
                if prior and prior.get("mcmeta_path"):errors.append(dict(path=path,kind="C_MCMETA_MISSING"))
            return record
    except Exception as e:
        errors.append(dict(path=path,kind="PNG_BYTES_DECODE",message=str(e)))
        return dict(path=path,git_blob_sha="",pillow_full_decode="FAIL")

def main():
    queue=readrows(Q);errors=[];warnings=[]
    if len(queue)!=829:errors.append(dict(kind="QUEUE_COUNT",actual=len(queue),expected=829))
    expected_types=collections.Counter(r["asset_type"] for r in queue)
    if expected_types!={"BLOCK_MODEL_JSON":378,"BLOCKSTATE_JSON":265,"BLOCK_TEXTURE_PNG":186}:
        errors.append(dict(kind="QUEUE_TYPE_COUNTS",counts=dict(expected_types)))
    keys=[(r["asset_type"],r["source_path"]) for r in queue]
    if len(set(keys))!=len(keys):errors.append(dict(kind="QUEUE_DUPLICATES"))
    if [int(r["G_global_index"]) for r in queue]!=list(range(3841,4670)):
        errors.append(dict(kind="QUEUE_GLOBAL_INDEX_RANGE"))
    f=index(F_STATUS,"model_path");fg=index(F_GEO,"model_path")
    c=index(MODEL_C,"source_path");pngc=index(PNG_C,"png_path")
    d1=readrows(D_ONE);d2=[]
    dmap=collections.defaultdict(list)
    for row in d1+d2:dmap[row["blockstate_path"]].append(row)
    fvis=index(F_VIS,"original_PNG_path")
    identity=[];model_rows=[];state_rows=[];png_rows=[];options_all=[];face_rows=[];mcmeta=[]
    orig_sources={};sha_by_path={}
    for r in queue:
        typ,path,sha=r["asset_type"],r["source_path"],r["git_blob_sha"]
        if typ=="BLOCK_TEXTURE_PNG":
            p=pixel(path,sha,pngc.get(path),errors);png_rows.append(p)
            identity.append(dict(type=typ,path=path,expected_sha=sha,actual_sha=p.get("git_blob_sha",""),
                direct_bytes_read="YES" if p.get("pillow_full_decode")=="PASS" else "NO",
                source_SHA_match="PASS" if p.get("git_blob_sha")==sha else "FAIL",prior_stage="C" if path in pngc else "G_NEW"))
            continue
        actual,obj=json_sha_and_obj(path,sha,errors)
        if obj is not None:orig_sources[path]=obj;sha_by_path[path]=actual
        identity.append(dict(type=typ,path=path,expected_sha=sha,actual_sha=actual or "",
            direct_bytes_read="YES" if obj is not None else "NO",
            source_SHA_match="PASS" if actual==sha else "FAIL",prior_stage="F" if typ=="BLOCK_MODEL_JSON" else "D"))
    for r in queue:
        typ,path,sha=r["asset_type"],r["source_path"],r["git_blob_sha"]
        obj=orig_sources.get(path)
        if obj is None:continue
        if typ=="BLOCK_MODEL_JSON":
            hist=f.get(path);geo=fg.get(path);prior=c.get(path)
            if not hist or not geo or not prior:errors.append(dict(path=path,kind="MISSING_PRIOR_F_GEO_C"));continue
            if any(z!=sha for z in (hist["model_sha"],geo["model_sha"],prior["git_blob_sha"])):
                errors.append(dict(path=path,kind="PRIOR_SOURCE_SHA_DIFFERENCE"))
            nodes=[];seen=set();nextpath=path
            while nextpath is not None:
                if nextpath in seen:errors.append(dict(path=path,kind="PARENT_CYCLE"));break
                seen.add(nextpath)
                if nextpath in orig_sources:node=orig_sources[nextpath];node_sha=sha_by_path[nextpath]
                else:
                    raw_path=ROOT/nextpath
                    if not raw_path.is_file():errors.append(dict(path=path,kind="PARENT_FILE_MISSING",parent=nextpath));break
                    node_sha,node=json_sha_and_obj(nextpath,gitsha(raw_path.read_bytes()),errors)
                if node is None:break
                nodes.append((nextpath,node,node_sha));nextpath=modelpath(node.get("parent"))
                if len(nodes)>30:errors.append(dict(path=path,kind="PARENT_DEPTH_GT_30"));break
            try:prior_chain=json.loads(hist["parent_chain_json"])
            except Exception:prior_chain=[];errors.append(dict(path=path,kind="F_PARENT_CHAIN_JSON"))
            if len(prior_chain)!=len(nodes):
                errors.append(dict(path=path,kind="F_PARENT_DEPTH",prior=len(prior_chain),actual=len(nodes)))
            else:
                for (p0,o,s),old in zip(nodes,prior_chain):
                    if (p0,s,o.get("parent"),len(o["elements"]) if isinstance(o.get("elements"),list) else None)!=(
                        old.get("path"),old.get("sha"),old.get("parent_ref"),old.get("own_elements")):
                        errors.append(dict(path=path,kind="F_PARENT_CHAIN_VALUE",parent=p0));break
            provider,elements,faces=resolved_faces(nodes)
            psha=next((s for p,o,s in nodes if p==provider),"")
            is_e=b(hist["E_exception"])
            values=dict(elements=len(elements),faces=len(faces),explicit_uv=sum(x["uv_key_explicit"] for x in faces),
                        implicit_uv=sum(not x["uv_key_explicit"] for x in faces),
                        bound=sum(x["resolved_texture"] is not None for x in faces),
                        unbound=sum(x["resolved_texture"] is None for x in faces))
            f_expected=[geo["element_count"],geo["face_count"],geo["UV_explicit"],geo["UV_key_absent"]]
            c_expected=[prior["C_applied_faces"],prior["C_explicit_uv_faces"],prior["C_implicit_uv_key_absent_faces"],
                        prior["C_bound_png_face_refs"],prior["C_template_unbound_face_refs"]]
            if not is_e and [str(values[k]) for k in ["elements","faces","explicit_uv","implicit_uv"]]!=f_expected:
                errors.append(dict(path=path,kind="F_ELEMENT_FACE_UV",actual=values,prior=f_expected))
            if [str(values[k]) for k in ["faces","explicit_uv","implicit_uv","bound","unbound"]]!=c_expected:
                errors.append(dict(path=path,kind="C_FACE_UV_BINDING",actual=values,prior=c_expected))
            if (provider or "")!=(hist["geometry_provider_path"] or "") or (psha or "")!=(hist["geometry_provider_sha"] or ""):
                errors.append(dict(path=path,kind="F_GEOMETRY_PROVIDER_SHA"))
            if is_e and faces:errors.append(dict(path=path,kind="E_EXCEPTION_HAS_GENERAL_FACES"))
            record=dict(path=path,sha=sha,parents=len(nodes),parent_chain_json=json.dumps([dict(path=p,sha=s,parent=o.get("parent")) for p,o,s in nodes],ensure_ascii=False),
               provider_path=provider or "",provider_sha=psha,E_exception="YES" if is_e else "NO",**values)
            model_rows.append(record)
            for face in faces:face_rows.append(dict(model_path=path,model_sha=sha,provider_path=provider or "",provider_sha=psha,**face))
        elif typ=="BLOCKSTATE_JSON":
            choices=state_options(obj);drows=dmap.get(path,[])
            newrules=[]
            for choice in choices:
                apply=choice["apply"]
                if not isinstance(apply,dict):errors.append(dict(path=path,kind="D_APPLY_NOT_OBJECT"));continue
                newrules.append(dict(blockstate_path=path,sha=sha,kind=choice["kind"],rule_index=choice["index"],
                    condition_json=json.dumps(choice["condition"],ensure_ascii=False,separators=(",",":")),
                    alternative_index=choice["option"],alternative_count=choice["count"],
                    model_ref=apply.get("model",""),model_path=modelpath(apply.get("model")) or "",
                    raw_apply_json=json.dumps(apply,ensure_ascii=False,separators=(",",":")),
                    x_key_present="x" in apply,y_key_present="y" in apply,uvlock_key_present="uvlock" in apply,weight_key_present="weight" in apply))
            # Normalize independently stored D subbatches: both are the original 265.
            dr={}
            for d in drows:
                dkind=d["rule_type"].lower()
                k=(dkind,int(d["rule_index"]),int(d.get("option_index",d.get("alternative_index","0"))))
                if k in dr:errors.append(dict(path=path,kind="D_DUPLICATE_RULE_OPTION",key=k))
                dr[k]=d
            for x in newrules:
                key=(x["kind"],int(x["rule_index"]),int(x["alternative_index"]))
                d=dr.get(key)
                if d is None:errors.append(dict(path=path,kind="D_SOURCE_OPTION_MISSING",key=key));continue
                try:oldapply=json.loads(d["raw_apply"])
                except Exception:oldapply=None
                if oldapply!=json.loads(x["raw_apply_json"]):
                    errors.append(dict(path=path,kind="D_ORIGINAL_APPLY_MISMATCH",key=key))
                if d["model_path"]!=x["model_path"]:
                    errors.append(dict(path=path,kind="D_MODEL_PATH_MISMATCH",key=key))
                flagfields={"x":"x_key_present","y":"y_key_present","uvlock":"uvlock_key_present","weight":"weight_key_present"}
                for flag,field in flagfields.items():
                    if b(d.get(flag+"_explicit"))!=x[field]:errors.append(dict(path=path,kind="D_FLAG_"+flag,key=key))
                if x["kind"]=="variants":
                    if d.get("variant_key","")!=json.loads(x["condition_json"]):
                        errors.append(dict(path=path,kind="D_VARIANT_CONDITION",key=key))
                elif d.get("multipart_when_json"):
                    try:old=json.loads(d["multipart_when_json"])
                    except Exception:old=None
                    # A missing 'when' and a D prior '{}' both encode an unconditional multipart base.
                    source_cond=json.loads(x["condition_json"])
                    if old!=source_cond and not (old=={} and source_cond is None):
                        errors.append(dict(path=path,kind="D_MULTIPART_CONDITION",key=key))
                if int(d.get("options_in_rule",d.get("alternative_count","1")))!=x["alternative_count"]:
                    errors.append(dict(path=path,kind="D_ALTERNATIVE_COUNT",key=key))
            if len(newrules)!=len(drows):errors.append(dict(path=path,kind="D_OPTION_COUNT",new=len(newrules),prior=len(drows)))
            state_rows.append(dict(path=path,sha=sha,variants=len(obj.get("variants") or {}),multipart=len(obj.get("multipart") or []),
                choices=len(newrules),D_prior_choices=len(drows),distinct_model_targets=len(set(x["model_path"] for x in newrules))))
            options_all.extend(newrules)

    for p in png_rows:
        if p.get("mcmeta_sha"):mcmeta.append(p)
        p["F_prior_visual"] = "YES" if p["path"] in fvis else "NO"
        if p["path"] in fvis:
            prior_F=fvis[p["path"]]
            if prior_F["original_PNG_git_sha"]!=p["git_blob_sha"] or prior_F["original_RGBA_SHA256"]!=p["rgba_sha256"]:
                errors.append(dict(path=p["path"],kind="F3_SOURCE_OR_RGBA_SHA_MISMATCH"))
            p["F3_contact_sheet_path"]=prior_F["contact_sheet_path"]
            p["F3_contact_sheet_sha"]=prior_F["contact_sheet_git_sha"]
            p["F3_first_frame_RGBA_SHA256"]=prior_F["first_frame_RGBA_SHA256"]
        else:
            p["F3_contact_sheet_path"]=""
            p["F3_contact_sheet_sha"]=""
            p["F3_first_frame_RGBA_SHA256"]=""
    source_good=sum(x["direct_bytes_read"]=="YES" and x["source_SHA_match"]=="PASS" for x in identity)
    counts=dict(source_paths=len(queue),model_JSON=len(model_rows),blockstate_JSON=len(state_rows),PNG=len(png_rows),
        source_direct_bytes_and_sha_pass=source_good,models_E=sum(x["E_exception"]=="YES" for x in model_rows),
        models_general=sum(x["E_exception"]=="NO" for x in model_rows),
        elements=sum(x["elements"] for x in model_rows),faces=len(face_rows),
        face_explicit_UV=sum(x["explicit_uv"] for x in model_rows),face_implicit_UV=sum(x["implicit_uv"] for x in model_rows),
        face_PNG_bound=sum(x["bound"] for x in model_rows),face_template_unbound=sum(x["unbound"] for x in model_rows),
        D_options=len(options_all),D_distinct_model_targets=len(set(x["model_path"] for x in options_all)),
        PNG_C_prior_and_RGBA_matched=sum(x.get("C_RGBA_match")=="PASS" for x in png_rows),
        PNG_C_outside_new_G_only=sum(x.get("prior_C_verified")=="NO_G_DIRECT_ONLY" for x in png_rows),
        PNG_original_bytes=sum(x.get("bytes",0) for x in png_rows),
        mcmeta_json_direct_read=len(mcmeta),
        mcmeta_animation_static=sum(x.get("mcmeta_animation_static")=="YES" for x in mcmeta),
        F_prior_visual_png=sum(x.get("F_prior_visual")=="YES" for x in png_rows),errors=len(errors))
    fields=list(identity[0].keys())
    writecsv("G_ENTRY6_SOURCE_IDENTITY_829.csv",identity,fields)
    writecsv("G_ENTRY6_MODEL_GEOMETRY_RECOUNT.csv",model_rows,list(model_rows[0]))
    writecsv("G_ENTRY6_D_ORIGINAL_OPTIONS.csv",options_all,list(options_all[0]))
    writecsv("G_ENTRY6_PNG_BINARY_AUDIT.csv",png_rows,list(png_rows[0]))
    # Face evidence is split for GitHub file size constraints.
    for i,start in enumerate(range(0,len(face_rows),2200)):
        part=face_rows[start:start+2200]
        writecsv("G_ENTRY6_ORIGINAL_FACES_%02d.csv"%i,part,list(part[0]))
    dump("G_ENTRY6_INDEPENDENT_RECOUNT.json",dict(schema="G_ENTRY6_CHECKOUT_INDEPENDENT_AUDIT/v1",counts=counts,
        original_source_830_expected=False,errors=errors,warnings=warnings,
        acceptance="ENTRY6_PASS" if not errors and source_good==829 else "ENTRY6_NOT_APPROVED",
        upstream_pinned_sha={p:gitsha(source(p)) for p in [Q,MODEL_C,PNG_C,F_STATUS,F_GEO,D_ONE,F_VIS]},
        caveats=["No Minecraft official JAR certification","No game runtime renderer/state space","No animation playback","No new image semantics: F visual is historical"]))
    report=["# 1-2-G Entry6 — 원본 829개 직접 소스 감사",
        "","GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.",
        "**Entry6 판정: "+("소스 감사 PASS (원격 readback·단계 승인 별도)" if not errors and source_good==829 else "미승인 — 오류·차단 확인 필요")+"**",
        "","## 원본 조사 수량"]
    report += ["- 직접 파일 원본/해시: %d / 829"%source_good,
        "- 모델 JSON: %d / 378"%counts["model_JSON"],
        "- blockstate JSON: %d / 265"%counts["blockstate_JSON"],
        "- PNG 해시/디코드/RGBA: %d / 186"%(sum(x.get("pillow_full_decode")=="PASS" for x in png_rows)),
        "- 모델 요소 %d, face %d (원본 재계산)"%(counts["elements"],counts["faces"]),
        "- D 원문 선택: %d, 서로 다른 참조 모델 %d"%(counts["D_options"],counts["D_distinct_model_targets"]),
        "- 선행 C PNG RGBA 일치 %d / C 외 G 신규 %d"%(counts["PNG_C_prior_and_RGBA_matched"],counts["PNG_C_outside_new_G_only"]),
        "- mcmeta %d, 정적 애니메이션 메타 %d"%(counts["mcmeta_json_direct_read"],counts["mcmeta_animation_static"]),
        "- 선행 F 시각 관찰 증거 연결 %d (이번 G의 신규 육안 관찰은 아님)"%counts["F_prior_visual_png"],
        "- 기록된 오류 %d개"%len(errors),
        "","## 한계","- 공식 JAR 인증·게임 렌더·state registry·애니메이션 재생은 범위 외 미검증.",
        "- E 특수 renderer, C 템플릿 미바인딩은 소관별로 계속 기록. PNG 내용 검증은 물체 정체/재질 확정이 아님.",
        "- **전체 G 게이트 G1~G6는 계속 0/6이며 Entry6은 마지막 회차이며 G 글로벌 종료 게이트 G1~G6 별도 통과 전 G 전체 완료 선언 금지.**",
        "- A~F/v69 파일 변경 없음. 현 시점 글로벌 G 진행은 Entry1~Entry5 승인 3,840/4,669 + Entry6 실검증별도.",
        "","## 생성한 근거","G_ENTRY6_SOURCE_IDENTITY_829.csv, G_ENTRY6_MODEL_GEOMETRY_RECOUNT.csv, G_ENTRY6_D_ORIGINAL_OPTIONS.csv, G_ENTRY6_PNG_BINARY_AUDIT.csv, G_ENTRY6_ORIGINAL_FACES_*.csv, G_ENTRY6_INDEPENDENT_RECOUNT.json."]
    (OUT/"G_ENTRY6_REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    print(json.dumps(dict(counts=counts,acceptance="SOURCE_CHECK_PASS" if not errors and source_good==829 else "BLOCKED",errors=errors[:15]),ensure_ascii=False))
    return 0 if not errors and source_good==829 else 2

if __name__=="__main__":
    sys.exit(main())
