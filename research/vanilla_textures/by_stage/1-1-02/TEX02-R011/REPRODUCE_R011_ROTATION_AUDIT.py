#!/usr/bin/env python3
"""TEX02-R011 source-rotation audit; zero dependencies, NO Minecraft launch.
Inputs: user-extracted Java 1.21.11/ classes, R007 and R010 frozen CSVs.
Matrix outputs are derived from classfile constructor/group source, not in-game frames.
"""
import argparse, csv, hashlib, json
from pathlib import Path

CLASS_SHA={
    "f.class":"f2723f067abf293075e66021711ce37387c92def",
    "g.class":"f4883aaac8f997dceb60b8f5e9a076e7a16c6fef",
    "h.class":"c4594ee6c1938cf051fcb5968a3c108788ffe1ac",
    "inm.class":"672b186c8a8457082fec756114b443a48dc151d1",
}
DIRECTIONS={"down":(0,-1,0),"up":(0,1,0),"north":(0,0,-1),
            "south":(0,0,1),"west":(-1,0,0),"east":(1,0,0)}

class ClassFile:
    def __init__(self, data):
        self.data=data;self.pos=0
        assert self.num(4)==0xCAFEBABE
        self.minor=self.num(2);self.major=self.num(2);N=self.num(2)
        self.cp=[None]*N;i=1
        while i<N:
            tag=self.num(1)
            if tag==1: val=self.read(self.num(2)).decode("utf8","replace")
            elif tag in (3,4):val=self.num(4)
            elif tag in (5,6):
                self.cp[i]=(tag,self.read(8));i+=2;continue
            elif tag in (7,8,16,19,20):val=self.num(2)
            elif tag in (9,10,11,12,17,18):val=(self.num(2),self.num(2))
            elif tag==15:val=(self.num(1),self.num(2))
            else:raise ValueError("unknown constant pool tag "+str(tag))
            self.cp[i]=(tag,val);i+=1
        self.access=self.num(2);self.selfname=self.ref(self.num(2))
        self.parentname=self.ref(self.num(2))
        for _ in range(self.num(2)):self.num(2)
        for _ in range(self.num(2)):
            self.num(2);self.num(2);self.num(2);self.skip_attributes()
        self.methods={}
        for _ in range(self.num(2)):
            self.num(2);name=self.ref(self.num(2));descriptor=self.ref(self.num(2))
            code=b""
            for _ in range(self.num(2)):
                attr=self.ref(self.num(2));data=self.read(self.num(4))
                if attr=="Code":
                    sz=int.from_bytes(data[4:8],"big");code=data[8:8+sz]
            self.methods[name,descriptor]=code
    def read(self,n):
        out=self.data[self.pos:self.pos+n]
        if len(out)!=n:raise ValueError("truncated class file")
        self.pos+=n;return out
    def num(self,n):return int.from_bytes(self.read(n),"big")
    def ref(self,idx):
        if not idx:return ""
        tag,val=self.cp[idx]
        if tag==1:return val
        if tag in (7,8,16,19,20):return self.ref(val)
        if tag in (9,10,11):return self.ref(val[0])+"."+self.ref(val[1])
        if tag==12:return self.ref(val[0])+":"+self.ref(val[1])
        return str(val)
    def skip_attributes(self):
        for _ in range(self.num(2)):
            self.num(2);self.read(self.num(4))
    def method(self,name,desc):return self.methods[name,desc]
    def has_ref(self,value):
        return any(self.ref(i).find(value)>=0 for i in range(1,len(self.cp)) if self.cp[i])

def cp2(code,i,cl):
    return cl.ref((code[i]<<8)|code[i+1]),i+2
def small_int(code,i):
    v=code[i]
    if 3<=v<=8:return v-3,i+1
    if v==16:return code[i+1],i+2
    raise ValueError(f"unexpected integer opcode {v:02x} at {i}")

def parse_h(cl):
    code=cl.method("<clinit>","()V");pos=0;out={}
    while pos<len(code) and code[pos]==0xbb:
        assert code[pos+3]==0x59 and code[pos+4]==0x12
        label=cl.ref(code[pos+5]);p=pos+6
        ordinal,p=small_int(code,p)
        xyz=[]
        for _ in range(3):
            v,p=small_int(code,p);xyz.append(v)
        assert code[p]==0xb7 and code[p+3]==0xb3
        enum_ref,p2=cp2(code,p+4,cl)
        out[enum_ref]=xyz;pos=p+6
    assert len(out)==6 and out["h.a:Lh;"]==[0,1,2]
    return out

def parse_f(cl):
    code=cl.method("<clinit>","()V");p=0;enums={}
    while p<len(code) and code[p]==0xbb:
        assert code[p+3]==0x59 and code[p+4]==0x13
        label,p=cp2(code,p+5,cl)
        ordinal,p=small_int(code,p)
        assert code[p]==0x13
        display_name,p=cp2(code,p+1,cl)
        assert code[p]==0xb2
        perm,p=cp2(code,p+1,cl)
        flags=[]
        for _ in range(3):
            flip,p=small_int(code,p);flags.append(flip)
        assert code[p]==0xb7 and code[p+3]==0xb3
        field,p=cp2(code,p+4,cl)
        enums[field]=dict(ordinal=ordinal,name=label,long_name=display_name,perm=perm,flips=flags)
    assert len(enums)==48 and code[p]==0xb8
    # After the 48 f enum constants comes a table initializer and nine public aliases.
    assert code[p]==0xb8 and code[p+3]==0xb3
    p+=6;aliases={}
    while p+5<len(code) and code[p]==0xb2 and code[p+3]==0xb3:
        src,p2=cp2(code,p+1,cl);dst,p3=cp2(code,p+4,cl)
        aliases[dst]=src;p+=6
    assert len(aliases)==9
    assert aliases["f.Y:Lf;"]=="f.s:Lf;"
    assert aliases["f.ab:Lf;"]=="f.u:Lf;"
    return enums,aliases

def parse_g(cl):
    code=cl.method("<clinit>","()V");p=0;result={}
    while p<len(code) and code[p]==0xbb:
        assert code[p+3]==0x59 and code[p+4]==0x12
        label=cl.ref(code[p+5]);p+=6
        ordinal,p=small_int(code,p);quarter,p=small_int(code,p)
        fields=[]
        for _ in range(3):
            assert code[p]==0xb2
            name,p=cp2(code,p+1,cl);fields.append(name)
        assert code[p]==0xb7 and code[p+3]==0xb3
        enumfield,p=cp2(code,p+4,cl)
        result[quarter]=dict(field=enumfield,ordinal=ordinal,name=label,axes=fields)
    assert len(result)==4
    code=cl.method("a","(Lg;Lg;Lg;)Lf;")
    assert code==bytes.fromhex("2c b4 00 38 2b b4 00 36 2a b4 00 34 b6 00 61 b6 00 61 b0")
    return result

def matrix_f(spec,perms):
    perm=perms[spec["perm"]];flips=spec["flips"]
    matrix=[[0]*3 for _ in range(3)]
    for local_axis,world_axis in enumerate(perm):
        matrix[world_axis][local_axis]=-1 if flips[world_axis] else 1
    return matrix
def mmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def matrix_key(M):return tuple(n for row in M for n in row)
def apply(M,xyz):return tuple(sum(M[i][k]*xyz[k] for k in range(3)) for i in range(3))

def csvrows(path):
    with path.open(newline="",encoding="utf8") as f:return list(csv.DictReader(f))
def writecsv(path,rows):
    with path.open("w",newline="",encoding="utf8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader();writer.writerows(rows)

def run(root,prior_faces,prior_states,prior_seams,out):
    cls={}
    for path,expected_sha in CLASS_SHA.items():
        data=(root/path).read_bytes()
        git_sha=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
        assert git_sha==expected_sha,(path,git_sha)
        cls[path]=ClassFile(data)
        assert cls[path].major==65
    h=parse_h(cls["h.class"]);f,aliases=parse_f(cls["f.class"]);g=parse_g(cls["g.class"])
    assert cls["f.class"].has_ref("org/joml/Matrix3f.scaling:")
    assert cls["f.class"].has_ref("org/joml/Matrix3f.mul:")
    assert cls["inm.class"].has_ref("f.b:()Lorg/joml/Matrix3fc;")
    by_matrix={matrix_key(matrix_f(spec,h)):{"enum":field,**spec} for field,spec in f.items()}
    assert len(by_matrix)==48
    def variant_rotation(x,y,z):
        def axis(quarter,k):
            field=g[quarter%4]["axes"][k]
            field=aliases.get(field,field)
            return matrix_f(f[field],h)
        # Code g.a(gx,gy,gz): Fz.compose(Fy.compose(Fx))
        M=mmul(axis(z//90,2),mmul(axis(y//90,1),axis(x//90,0)))
        key=matrix_key(M)
        assert key in by_matrix
        return M,by_matrix[key]
    previous=csvrows(prior_faces);states=csvrows(prior_states);seams=csvrows(prior_seams)
    assert len(states)==31 and len(previous)==186 and len(seams)==134
    record={}
    for row in previous:
        key=row["texture_id"],row["prop"],row["index"],row["local_face"]
        assert key not in record
        record[key]=row
    audit=[];corrections=[]
    for state in states:
        x,y,z=map(int,(state["x"],state["y"],state["z"]))
        M,spec=variant_rotation(x,y,z)
        for local,vector in DIRECTIONS.items():
            key=state["block"],state["property"],state["variant_index"],local
            old=record[key]
            world_vec=apply(M,vector)
            (correct_face,)=tuple(k for k,v in DIRECTIONS.items() if v==world_vec)
            changed=correct_face!=old["world_face_math"]
            row=dict(block=state["block"],property=state["property"],
              variant_index=state["variant_index"],x=x,y=y,z=z,
              source_enum=spec["name"],local_face=local,
              old_R007=old["world_face_math"],source_matrix_direction=correct_face,
              changed=changed,ingame_verified=False)
            audit.append(row)
            if changed:corrections.append(row)
    impacted=[r for r in seams if r["texture_group"]=="deepslate" and r["property"] in ("axis=x","axis=z")]
    assert len(audit)==186 and len(corrections)==32 and len(impacted)==64
    # Fixed 5 actual variant transforms: regression guards.
    expected={(0,0,0):"IDENTITY",(0,180,0):"ROT_180_FACE_XZ",
              (90,0,0):"ROT_90_X_NEG",(90,180,0):"ROT_180_EDGE_YZ_POS",
              (90,90,0):"ROT_120_PPP"}
    for tup,name in expected.items():
        _,spec=variant_rotation(*tup)
        assert spec["name"]==name,(tup,spec["name"])
    out.mkdir(parents=True,exist_ok=True)
    writecsv(out/"REGENERATED_186_WORLD_FACE_AUDIT.csv",audit)
    writecsv(out/"REGENERATED_32_R007_MISMATCHES.csv",corrections)
    writecsv(out/"REGENERATED_64_REEVALUATE_SEAMS.csv",impacted)
    print(json.dumps(dict(classfile_source_count=4,rotation_matrices=5,
       prior_face_count=186,match=154,corrections=len(corrections),
       prior_synthetic_seam_rows=134,needs_reprojection=len(impacted),
       user_game_render_measurements=0,official_jar_authentication=False),indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True,type=Path,help="User extracted 1.21.11 directory")
    p.add_argument("--r007-faces",required=True,type=Path)
    p.add_argument("--r010-states",required=True,type=Path)
    p.add_argument("--r007-seams",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    run(a.root,a.r007_faces,a.r010_states,a.r007_seams,a.out)
