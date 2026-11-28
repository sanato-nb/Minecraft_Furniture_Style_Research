"""Independent bounded fixture checks, not a general Minecraft parser or renderer."""
import json
import struct
import zlib
import design_contract as c

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:
            c.require(k not in d,"duplicate JSON key")
            d[k]=v
        return d
    def invalid(x):raise ValueError("nonfinite JSON")
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid)

def source(db,snap,oid,read):
    o=c.one(db,"SELECT * FROM research_object WHERE snapshot_id=? AND object_id=?",(snap,oid))
    a=c.one(db,"SELECT * FROM asset WHERE release_key=? AND source_path=?",(o["asset_release"],o["asset_path"]))
    link=c.one(db,"SELECT evidence_id FROM object_evidence WHERE snapshot_id=? AND object_id=? AND evidence_class='SOURCE'",(snap,oid))
    c.require_evidence(db,link["evidence_id"],read)
    e=c.one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(link["evidence_id"],))
    raw=read(e)
    c.require(a["hash_algorithm"]=="SHA256" and a["digest"]==c.sha(raw) and a["byte_count"]==len(raw),"asset body mismatch")
    return o,a,raw

def pointer(doc,p):
    if p=="":return doc
    c.require(p.startswith("/"),"invalid JSON pointer")
    for part in p[1:].split("/"):
        key=part.replace("~1","/").replace("~0","~")
        try:doc=doc[int(key)] if isinstance(doc,list) else doc[key]
        except (KeyError,IndexError,ValueError,TypeError) as exc:raise ValueError("pointer not found") from exc
    return doc

def validate_model(db,snap,mid,read):
    o,a,raw=source(db,snap,mid,read)
    c.require(a["kind"]=="model" and o["json_pointer"]=="","model origin")
    doc=strict_json(raw)
    m=c.one(db,"SELECT * FROM model_definition WHERE snapshot_id=? AND object_id=?",(snap,mid))
    declared="elements" in doc
    c.require(m["parent_raw"]==doc.get("parent") and m["elements_declared"]==declared and m["declared_element_count"]==(len(doc["elements"]) if declared else None),"model declaration mismatch")
    chain=[];cur=mid
    while True:
        c.require(cur not in chain,"parent cycle")
        chain.append(cur)
        oo,aa,rr=source(db,snap,cur,read)
        dd=strict_json(rr)
        if "elements" in dd:break
        parent=dd.get("parent")
        c.require(parent is not None,"missing provider")
        cur=c.one(db,"SELECT object_id FROM research_object WHERE snapshot_id=? AND object_kind='MODEL' AND asset_release=? AND asset_path=(SELECT source_path FROM asset WHERE release_key=? AND resource_id=? AND kind='model')",(snap,aa["release_key"],aa["release_key"],parent))["object_id"]
    c.require(m["provider_id"]==cur and m["resolution"]=="RESOLVED","provider mismatch")
    elements=c.rows(db,"SELECT * FROM model_element WHERE snapshot_id=? AND model_id=? ORDER BY ordinal",(snap,mid))
    c.require(len(elements)==(len(doc["elements"]) if declared else 0),"element denominator mismatch")
    for i,e in enumerate(elements):
        eo,ea,eraw=source(db,snap,e["object_id"],read)
        c.require(ea["source_path"]==a["source_path"] and eo["json_pointer"]=="/elements/"+str(i) and e["ordinal"]==i,"element origin")
        el=pointer(strict_json(eraw),eo["json_pointer"])
        c.require([e["from_"+k] for k in "xyz"]==el["from"] and [e["to_"+k] for k in "xyz"]==el["to"],"coordinate mismatch")
        faces=c.rows(db,"SELECT * FROM model_face WHERE snapshot_id=? AND element_id=?",(snap,e["object_id"]))
        c.require({f["direction"] for f in faces}==set(el["faces"]),"face denominator mismatch")
        for face in faces:
            fo,fa,fraw=source(db,snap,face["object_id"],read)
            c.require(fa["source_path"]==a["source_path"] and fo["json_pointer"]==eo["json_pointer"]+"/faces/"+face["direction"],"face origin")
            fd=pointer(strict_json(fraw),fo["json_pointer"])
            c.require(face["texture_raw"]==fd["texture"] and (json.loads(face["declared_uv_json"]) if face["declared_uv_json"] else None)==fd.get("uv") and face["uv_rotation"]==fd.get("rotation") and face["cullface"]==fd.get("cullface") and face["tintindex"]==fd.get("tintindex"),"face declaration mismatch")
    return cur

def rgba_png(raw):
    """Only fixture PNG RGBA8, noninterlaced, filter zero; all other forms rejected."""
    c.require(raw[:8]==b"\x89PNG\r\n\x1a\n","PNG signature")
    p=8;chunks=[];size=None;ended=False
    while p+12<=len(raw):
        n=struct.unpack(">I",raw[p:p+4])[0];k=raw[p+4:p+8];v=raw[p+8:p+8+n]
        c.require(p+12+n<=len(raw),"PNG truncated")
        crc=struct.unpack(">I",raw[p+8+n:p+12+n])[0]
        c.require(zlib.crc32(k+v)==crc,"PNG CRC")
        p+=12+n
        if k==b"IHDR":
            c.require(size is None and len(v)==13,"IHDR")
            w,h,depth,color,comp,filt,inter=struct.unpack(">IIBBBBB",v)
            c.require(0<w<=256 and 0<h<=256 and (depth,color,comp,filt,inter)==(8,6,0,0,0),"fixture PNG format")
            size=w,h
        elif k==b"IDAT":chunks.append(v)
        elif k==b"IEND":
            c.require(n==0,"IEND");ended=True;break
        else:raise ValueError("unsupported fixture PNG chunk")
    c.require(ended and p==len(raw) and size is not None and chunks,"PNG completeness")
    w,h=size
    dec=zlib.decompressobj()
    data=dec.decompress(b"".join(chunks),h*(1+4*w)+1)
    c.require(dec.eof and not dec.unused_data and len(data)==h*(1+4*w),"PNG decoded length")
    stride=1+4*w
    c.require(all(data[i*stride]==0 for i in range(h)),"unsupported PNG filter")
    return w,h,b"".join(data[i*stride+1:(i+1)*stride] for i in range(h))

def validate_texture(db,snap,tid,read):
    _,a,raw=source(db,snap,tid,read)
    c.require(a["kind"]=="texture","texture source kind")
    w,h,pixels=rgba_png(raw)
    t=c.one(db,"SELECT * FROM texture_definition WHERE snapshot_id=? AND object_id=?",(snap,tid))
    c.require((t["width"],t["height"],t["color_mode"])==(w,h,"RGBA"),"texture dimensions")
    frames=c.rows(db,"SELECT * FROM texture_frame WHERE snapshot_id=? AND texture_id=?",(snap,tid))
    c.require(bool(frames),"no frames")
    for f in frames:
        c.validate_frame(db,snap,f["object_id"])
        sample=b"".join(pixels[(y*w+f["x"])*4:(y*w+f["x"]+f["width"])*4] for y in range(f["y"],f["y"]+f["height"]))
        c.require(c.sha(sample)==f["rgba_sha256"],"frame pixel hash")
    return w,h

def validate_state(db,snap,sid,read):
    _,a,raw=source(db,snap,sid,read)
    c.require(a["kind"]=="blockstate","state source kind")
    doc=strict_json(raw)
    state=c.one(db,"SELECT * FROM state_definition WHERE snapshot_id=? AND object_id=?",(snap,sid))
    c.require(state["state_form"]=="MULTIPART" and set(doc)=={"multipart"},"fixture multipart only")
    rr=c.rows(db,"SELECT * FROM state_rule WHERE snapshot_id=? AND state_id=? ORDER BY rule_ordinal",(snap,sid))
    c.require(len(rr)==len(doc["multipart"]),"rule count")
    for i,rule in enumerate(rr):
        rawrule=doc["multipart"][i]
        c.require(rule["rule_ordinal"]==i and json.loads(rule["condition_json"])==rawrule["when"],"condition mismatch")
        opt=c.one(db,"SELECT * FROM state_option WHERE snapshot_id=? AND state_id=? AND rule_ordinal=?",(snap,sid,i))
        aopt=rawrule["apply"]
        c.require(opt["model_raw"]==aopt["model"] and opt["y_rotation"]==aopt.get("y") and opt["uvlock"]==aopt.get("uvlock"),"option mismatch")
        target=c.one(db,"SELECT o.object_id FROM research_object o JOIN asset a ON a.release_key=o.asset_release AND a.source_path=o.asset_path WHERE o.snapshot_id=? AND o.object_kind='MODEL' AND a.resource_id=? AND a.release_key=?",(snap,aopt["model"],a["release_key"]))
        c.require(opt["model_id"]==target["object_id"],"option target mismatch")
        for app in c.rows(db,"SELECT * FROM state_application WHERE snapshot_id=? AND state_id=? AND rule_ordinal=?",(snap,sid,i)):
            assignment=json.loads(app["assignment_json"])
            matched=all(assignment.get(k)==v for k,v in rawrule["when"].items())
            c.require(matched and app["selection_status"]=="SELECTED" and json.loads(app["transform_json"])=={"y":aopt["y"]},"state application mismatch")
    return len(rr)

def validate_render(db,sid,output,read):
    o=c.one(db,"SELECT o.*,c.width,c.height,c.unit_id FROM render_output o JOIN render_case c ON c.scope_id=o.scope_id AND c.case_id=o.case_id WHERE o.scope_id=? AND o.output_id=?",(sid,output))
    c.require(o["generation_status"]=="GENERATED","not generated")
    c.require_evidence(db,o["png_evidence_id"],read)
    e=c.one(db,"SELECT * FROM evidence_item WHERE evidence_id=?",(o["png_evidence_id"],))
    w,h,_=rgba_png(read(e))
    c.require((w,h)==(o["width"],o["height"]),"render dimensions")
    return o
