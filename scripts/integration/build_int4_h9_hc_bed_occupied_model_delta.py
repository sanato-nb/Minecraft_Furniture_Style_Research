#!/usr/bin/env python3
"""INT-4-H9 source-grounded bed occupancy model / geometry / face-UV audit.

No new sleep, wake, destroy or user interaction test; model research only.
Data: 1024 source selectors, 512 occupancy pairs, 256 model leaves,
four geometry parent pairs, immutable S37/S38 + actual unoccupied F2 pins.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
COMMIT="8d21d1665916850c3fa3bdaf1370c50ec2ca7035"
SOURCE="common/src/main/generated/resources/assets/handcrafted/"
BLOCK=SOURCE+"blockstates/oak_fancy_bed.json"
MODELS=SOURCE+"models/block/"
PARENTS="common/src/main/resources/assets/handcrafted/models/block/fancy_bed/"
LEDGER=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
F2DOC=Path("project/integration/INT4_HANDCRAFTED_BED_F2_SOURCE_RESULT.json")
PINS={
    BLOCK:"0dfb7493ac098a7e5549db6663bffd9310c1882a",
    str(LEDGER):"56e6f4c21c50714b97079ec61f7219bea845f179",
    str(F2DOC):"107b2b2c47a19cd8fb36939cc7f516111ed7548b",
    PARENTS+"bed_single.json":"01dcc76679443d37f3efa45d974e2acbc071cfc1",
    PARENTS+"bed_single_occupied.json":"296e103447bfaaa6dd5d3a20d39169c1612474bc",
    PARENTS+"cushion.json":"3b9147f7d5309913004d7dadb45e2b09dc98bb4f",
    MODELS+"oak_fancy_bed_single_white_foot.json":"14c6bad5a40e3130cd8fa5725ce5260b74662bc2",
    MODELS+"oak_fancy_bed_single_white_head.json":"81117620d95782b093fa23b396af04cf42f6729a",
}
COLORS=("black","blue","brown","cyan","gray","green","light_blue","light_gray","lime",
        "magenta","orange","pink","purple","red","white","yellow")
FACING=("east","north","south","west")
SHAPES=("left","middle","right","single")
PARTS=("foot","head")
O_PAIRS=OUT/"INT4_H9_512_OCCUPIED_SOURCE_MODEL_PAIRS_V1.csv"
O_GEOM=OUT/"INT4_H9_4_SHAPES_GEOMETRY_FACE_UV_DELTA_V1.csv"
O_JSON=OUT/"INT4_H9_HC_BED_OCCUPIED_SOURCE_AUDIT_V1.json"
O_MD=OUT/"INT4_H9_HC_BED_MODELING_SCOPE_REPORT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(value,reason):
    if not value:raise AssertionError(reason)
def canonical(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def jsonout(d):return (json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode("utf-8")
def csvout(data):
    stream=io.StringIO(newline="")
    w=csv.DictWriter(stream,fieldnames=list(data[0]),lineterminator="\n")
    w.writeheader();w.writerows(data)
    return stream.getvalue().encode("utf-8")
def write(path,b,verify):
    p=ROOT/path
    if verify:check(p.is_file() and p.read_bytes()==b,"OUTPUT_CHANGED "+str(path))
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)

class SourceZip:
    def __init__(self,file):
        self.zip=ZipFile(file)
        check(self.zip.testzip() is None,"SOURCE_ZIP_CRC")
        names=self.zip.namelist()
        check(len(names)==len(set(names)),"DUPLICATE_SOURCE_ZIP_FILES")
        self.paths={}
        for name in names:
            if "/" in name:
                key=name.split("/",1)[1]
                check(key not in self.paths,"SOURCE_DUPLICATE_RELATIVE_PATH")
                self.paths[key]=name
        self.cache={}
    def raw(self,key):
        if key not in self.cache:
            check(key in self.paths,"UPSTREAM_SOURCE_MISSING "+key)
            b=self.zip.read(self.paths[key])
            if key in PINS:check(gitblob(b)==PINS[key],"PINNED_SOURCE_SHA_CHANGED "+key)
            self.cache[key]=b
        return self.cache[key]
    def read(self,key):return json.loads(self.raw(key))

def path_of(resource):
    check(isinstance(resource,str) and resource.startswith("handcrafted:block/"),"BAD_MODEL_RESOURCE")
    return MODELS+resource[len("handcrafted:block/"):]+".json"

def parse_selector(key):
    pair=[p.split("=",1) for p in key.split(",")]
    check(len(pair)==5 and all(len(x)==2 for x in pair),"UNKNOWN_SELECTOR")
    d=dict(pair)
    check(set(d)=={"color","facing","occupied","part","shape"},"UNKNOWN_SELECTOR_FIELDS")
    check(d["color"] in COLORS and d["facing"] in FACING and
          d["occupied"] in ("false","true") and
          d["part"] in PARTS and d["shape"] in SHAPES,"UNKNOWN_SELECTOR_VALUES")
    return d

def counts(p):
    e=p.get("elements",[])
    check(isinstance(e,list),"MODEL_ELEMENTS_ARRAY_REQUIRED")
    return len(e),sum(len(x.get("faces",{})) for x in e)

def model_diff(prior,current):
    old=Counter(canonical(x) for x in prior.get("elements",[]))
    new=Counter(canonical(x) for x in current.get("elements",[]))
    removed=old-new;added=new-old
    faces=lambda c:sum(n*len(json.loads(s).get("faces",{})) for s,n in c.items())
    return {
      "identical_element_records":sum((old&new).values()),
      "removed_element_records":sum(removed.values()),
      "added_element_records":sum(added.values()),
      "removed_face_UV_records":faces(removed),
      "added_face_UV_records":faces(added),
    }

def original_study():
    p=ROOT/LEDGER
    check(gitblob(p.read_bytes())==PINS[str(LEDGER)],"HISTORIC_APPLICATION_SOURCE_CHANGED")
    records=list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8-sig"))))
    original={k:[r for r in records if r["case"]==k] for k in ("S37","S38")}
    check(all(len(x)==1 for x in original.values()),"MISSING_HISTORICAL_BED_CASE")
    p=ROOT/F2DOC
    check(gitblob(p.read_bytes())==PINS[str(F2DOC)],"HISTORIC_BED_F2_SHA_CHANGED")
    doc=json.loads(p.read_text(encoding="utf-8"))
    f=doc["first_paired_background_controlled_f2"]["observed"]
    check(f["source_cases"]==["S37","S38"] and f["server_verified"]==2 and
          f["original_face_counts"]=={"S37":72,"S38":6} and
          f["status"]=="PASS_TWO_REAL_FABRIC_F2_PINNED_BED_SOURCE_STATES_NOT_NATURAL_ASSEMBLY",
          "ORIGINAL_OCCUPIED_FALSE_F2_SCOPE_CHANGED")
    return original,f["native_f2_sha256"]

def audit(source_zip,verify=False):
    src=SourceZip(source_zip)
    variants=src.read(BLOCK)["variants"]
    check(len(variants)==1024,"EXPECTED_1024_BED_VARIANTS")
    normal={}
    for key,option in variants.items():
        d=parse_selector(key)
        dims=(d["color"],d["facing"],d["shape"],d["part"])
        if d["occupied"]=="false":
            check(dims not in normal,"DUPLICATE_FALSE")
            normal[dims]=(key,option)
    check(len(normal)==512,"EXPECTED_512_UNOCCUPIED_VARIANTS")
    check(len({x[0] for x in normal})==16 and len({x[1] for x in normal})==4 and
          len({x[2] for x in normal})==4 and len({x[3] for x in normal})==2,
          "INCOMPLETE_COLOR_DIRECTION_SHAPE_PART_SPACE")
    model_names=set();pairs=[];head_equal=0;foot_parent_change=0
    for dims,(key,a) in sorted(normal.items()):
        color,direction,shape,part=dims
        twin=key.replace("occupied=false","occupied=true")
        check(twin in variants,"MISSING_OCCUPIED_TRUE_TWIN")
        b=variants[twin]
        check(a["model"]!=b["model"],"MODEL_RESOURCE_PATH_NOT_CHANGED")
        check(all(a.get(k,0 if k in ("x","y") else False if k=="uvlock" else 1)==
                  b.get(k,0 if k in ("x","y") else False if k=="uvlock" else 1)
                  for k in ("x","y","uvlock","weight")),"MODEL_SELECTOR_TRANSFORM_DIFF")
        pa=path_of(a["model"]);pb=path_of(b["model"])
        model_names.update((pa,pb))
        fa=src.raw(pa);fb=src.raw(pb);ja=json.loads(fa);jb=json.loads(fb)
        check(ja.get("textures")==jb.get("textures"),"TEXTURE_SLOT_BINDINGS_CHANGED")
        if part=="foot":
            check(fa!=fb and ja.get("parent")=="handcrafted:block/fancy_bed/bed_"+shape and
                  jb.get("parent")=="handcrafted:block/fancy_bed/bed_"+shape+"_occupied",
                  "FOOT_OCCUPIED_PARENT_SELECTION_WRONG")
            check({k:v for k,v in ja.items() if k!="parent"}==
                  {k:v for k,v in jb.items() if k!="parent"},
                  "FOOT_OTHER_LEAF_FIELD_CHANGED")
            foot_parent_change+=1
        else:
            check(fa==fb and ja.get("parent")=="handcrafted:block/fancy_bed/cushion",
                  "HEAD_IDENTICAL_SOURCE_LEAF_EXPECTED")
            head_equal+=1
        pairs.append({
            "color":color,"facing":direction,"shape":shape,"part":part,
            "model_unoccupied":a["model"],"model_occupied":b["model"],
            "model_unoccupied_git_sha1":gitblob(fa),
            "model_occupied_git_sha1":gitblob(fb),
            "parent_unoccupied":ja.get("parent",""),
            "parent_occupied":jb.get("parent",""),
            "rotation_y":a.get("y",0),
            "uvlock":str(a.get("uvlock",False)).lower(),
            "leaf_bytes_identical":str(fa==fb).lower(),
            "texture_bindings_identical":str(ja.get("textures")==jb.get("textures")).lower(),
            "source_model_geometry_change":str(part=="foot").lower(),
            "original_game_occupied_true_F2_verified":"false",
        })
    check(len(pairs)==512 and len(model_names)==256 and
          (foot_parent_change,head_equal)==(256,256),
          "PAIR_FULL_POPULATION_DENOMINATOR_WRONG")
    original,f2=original_study()
    for case,part,expected_faces in (("S37","foot",72),("S38","head",6)):
        r=original[case][0]
        path=MODELS+"oak_fancy_bed_single_white_"+part+".json"
        check(r["block"]=="handcrafted:oak_fancy_bed" and
              r["state"]=="color=white;facing=north;occupied=false;part="+part+";shape=single",
              "ORIGINAL_S37_S38_STATE_CHANGED "+case)
        check(r["model_sha"]==gitblob(src.raw(path)) and
              r["state_sha"]==gitblob(src.raw(BLOCK)) and
              int(r["faces"])==expected_faces,
              "ORIGINAL_S37_S38_SOURCE_SHA_OR_FACES_CHANGED "+case)
    geom=[]
    for shape in SHAPES:
        a=PARENTS+"bed_"+shape+".json"
        b=PARENTS+"bed_"+shape+"_occupied.json"
        ja=src.read(a);jb=src.read(b)
        check(ja.get("parent")==jb.get("parent") and
              ja.get("textures")==jb.get("textures"),"PARENT_PROVIDER_INHERITANCE_DIFF")
        elems0,faces0=counts(ja)
        elems1,faces1=counts(jb)
        check(elems1>elems0 and faces1>faces0,"NO_SOURCE_OCCUPIED_GEOMETRY_CHANGE")
        geom.append({
           "shape":shape,
           "unoccupied_provider_git_sha1":gitblob(src.raw(a)),
           "occupied_provider_git_sha1":gitblob(src.raw(b)),
           "unoccupied_elements":elems0,"occupied_elements":elems1,
           "unoccupied_faces":faces0,"occupied_faces":faces1,
           "delta_elements":elems1-elems0,"delta_faces":faces1-faces0,
           **model_diff(ja,jb),
           "same_parent_base":True,"same_texture_slot_bindings":True,
           "native_F2_pixel_per_face_UV_verified":False,
        })
    single=next(x for x in geom if x["shape"]=="single")
    check([single[k] for k in ("unoccupied_elements","unoccupied_faces","occupied_elements","occupied_faces")]
          ==[12,72,14,84],"HISTORIC_SINGLE_OCCUPIED_12_TO_14_CHANGED")
    check(counts(src.read(PARENTS+"cushion.json"))==(1,6),
          "HISTORIC_HEAD_CUSHION_SOURCE_CHANGED")
    out={
      "schema":"MCFR_INT4_H9_HANDCRAFTED_BED_OCCUPIED_VISUAL_MODEL_SOURCE_V1",
      "status":"PASS_1024_STATE_512_PAIR_256_MODEL_FOOT_GEOMETRY_SOURCE_VALIDATED",
      "upstream":{"repo":"terrarium-earth/Handcrafted","commit":COMMIT,
                  "blockstate_git_sha1":PINS[BLOCK]},
      "source_sha_pins":PINS,
      "counts":{"source_selector_variants":1024,"occupied_false_true_pairs":512,
                "unique_selected_model_leaf_files":256,"model_path_changes":512,
                "foot_parent_geometry_changed_pairs":256,
                "head_model_leaf_byte_identical_pairs":256,
                "shapes_with_foot_geometry_UV_source_delta":4,
                "new_gameplay_sessions":0,"new_occupied_true_native_F2":0,
                "full_F_H_approvals":0,"INT5_semantics_approved":0,
                "INT6_AI_training_redistribution_rights_approved":0},
      "four_foot_parent_geometry_comparisons":geom,
      "original_S37_S38_occupied_false_F2_sha256":f2,
      "source_interpretation":{
          "occupied_visual_modeling_relevant":True,
          "foot_source_geometry_faces_uv_records_change":True,
          "head_only_model_resource_names_change_not_leaf_bytes":True,
          "bed_lifecycle_gameplay_not_required_for_model_research":True,
          "existing_H03_H05_and_F70_dispositions_unchanged":True},
      "limitations":[
        "Pinned static source JSON geometry and face UV, NOT actual GPU per-face UV pixel attribution.",
        "Head model path changes but source JSON bytes do not; do NOT claim a changed head shape.",
        "Foot leaf texture bindings stay identical while chosen parent elements/faces differ; textures pixels not independently compared.",
        "Previous original S37/S38 F2 only prove occupied=false states; no occupied=true actual F2.",
        "No need to run sleep-wake-destroy gameplay sequence for model authoring goal.",
        "Original study data, F70, H03/H05, model authoring meanings and asset distribution rights unchanged."
      ],
    }
    results={O_PAIRS:csvout(pairs),O_GEOM:csvout(geom)}
    out["derived_files_sha256"]={str(p):sha(b) for p,b in results.items()}
    results[O_JSON]=jsonout(out)
    md="\n".join([
      "# INT-4-H9 Handcrafted 침대 occupied 속성의 모델·면·UV 출처 연구",
      "",
      "- 원본 Handcrafted "+COMMIT+"의 oak_fancy_bed 블록상태 1,024개 전수 검증.",
      "- 16색×4방향×4형태×2부분×2점유 = 1,024 선택자, occupied 대응 512쌍, 고유 leaf JSON 256개.",
      "- 모델 선택 경로는 512쌍 모두 달라지지만 모델 기하 변경과 동의어가 아님.",
      "- foot 256쌍: 선택 부모가 bed_<shape>에서 bed_<shape>_occupied로 변경, 4형태 모두 요소·면 UV 출처 변화. leaf 텍스처 슬롯 바인딩 동일.",
      "- head 256쌍: occupied 이름으로 모델 경로는 변경되나 실제 leaf JSON은 쌍별 바이트 동일, 같은 cushion 부모 1요소·6면.",
      "- 대표 원본 S37 single foot: 12요소·72면에서 14요소·84면으로 변경. S38 head: 1요소·6면 불변.",
      "- 이전 실제 F2 S37/S38은 occupied=false만 검증했으며 occupied=true F2는 아직 0장.",
      "- 게임 잠자기·깨기·파괴의 연속 동작 검증은 모델링 필수 목록에서 제외. occupied=true의 정적 비교 F2와 UV 인과 검증만 관련.",
      "- H03/H05와 F70 전면 최종 승인, INT5 의미 및 INT6 권리 승인 조건은 변경하지 않음.",
      "",
    ]).encode("utf-8")
    results[O_MD]=md
    for p,b in results.items():write(p,b,verify)
    print(json.dumps({"status":out["status"],"counts":out["counts"],
                      "geometry":geom},ensure_ascii=False))
    return out

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-zip",required=True,type=Path)
    a.add_argument("--verify",action="store_true")
    opts=a.parse_args()
    audit(opts.source_zip,opts.verify)

if __name__=="__main__":main()
