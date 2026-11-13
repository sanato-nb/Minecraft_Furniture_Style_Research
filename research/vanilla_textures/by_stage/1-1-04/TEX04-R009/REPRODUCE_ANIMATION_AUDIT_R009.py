#!/usr/bin/env python3
"""TEX04-R009 — vanilla-source animation audit for 9 wool textures.
Usage: python REPRODUCE_ANIMATION_AUDIT_R009.py /path/to/1.21.11 OUT_DIR
Requires only Python 3 standard library; reads user-extracted source files.
Does not run or certify Minecraft GUI, a Mojang JAR, or third-party mods.
"""
from pathlib import Path
import hashlib, json, struct, zlib, csv, sys

COLORS=("white","red","blue","black","green","yellow","purple","cyan","orange")
SHA256={
"white":"70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5",
"red":"07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464",
"blue":"2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db",
"black":"8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9",
"green":"a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad",
"yellow":"cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2",
"purple":"f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9",
"cyan":"68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303",
"orange":"de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68"
}
POSITIVE={
"water_still": (16,512,2,0),
"lava_still": (16,320,2,38),
"fire_0": (16,512,1,32)
}
def check_png(path):
    b=path.read_bytes()
    assert b[:8]==b"\x89PNG\r\n\x1a\n",path
    offset=8; ct=[];w=h=bit=colour=None
    while offset<len(b):
        assert offset+12<=len(b),path
        n=struct.unpack(">I",b[offset:offset+4])[0]
        name=b[offset+4:offset+8]
        data=b[offset+8:offset+8+n]
        assert len(data)==n and offset+12+n<=len(b)
        check=struct.unpack(">I",b[offset+8+n:offset+12+n])[0]
        assert zlib.crc32(name+data)&0xffffffff==check,(path,name)
        label=name.decode("ascii")
        ct.append(label)
        if label=="IHDR":
            w,h,bit,colour=struct.unpack(">IIBB",data[:10])
        offset+=12+n
    assert offset==len(b) and ct[0]=="IHDR" and ct[-1]=="IEND"
    assert w and h
    return {"bytes":len(b),"width":w,"height":h,"bit_depth":bit,"colour_type":colour,"chunk_types":ct,
            "has_apng_chunks":bool({"acTL","fcTL","fdAT"}&set(ct)),
            "sha256":hashlib.sha256(b).hexdigest()}
def rows_to_csv(path,header,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def main(root,out):
    assert (root/"assets/minecraft").is_dir(),root
    out.mkdir(parents=True,exist_ok=True)
    block=root/"assets/minecraft/textures/block"
    atlas=read_json(root/"assets/minecraft/atlases/blocks.json")
    assert any(x.get("type")=="minecraft:directory" and x.get("source")=="block" and x.get("prefix")=="block/" for x in atlas["sources"])
    rows=[]
    for c in COLORS:
        pid=c+"_wool"
        file=block/(pid+".png")
        m=check_png(file)
        assert m["sha256"]==SHA256[c]
        assert (m["width"],m["height"],m["bit_depth"],m["colour_type"])==(16,16,8,3)
        assert m["chunk_types"]==["IHDR","PLTE","IDAT","IEND"]
        meta=file.with_name(file.name+".mcmeta")
        assert not meta.exists(),meta
        leaf=read_json(root/("assets/minecraft/models/block/"+pid+".json"))
        bs=read_json(root/("assets/minecraft/blockstates/"+pid+".json"))
        item=read_json(root/("assets/minecraft/items/"+pid+".json"))
        assert leaf=={"parent":"minecraft:block/cube_all","textures":{"all":"minecraft:block/"+pid}}
        assert bs=={"variants":{"":{"model":"minecraft:block/"+pid}}}
        assert item=={"model":{"type":"minecraft:model","model":"minecraft:block/"+pid}}
        rows.append([pid,str(file.relative_to(root)),m["sha256"],m["width"],m["height"],m["bytes"],"|".join(m["chunk_types"]),0,0,1,1,1,1,0])
    for parent in ("cube_all","cube","block"):
        read_json(root/("assets/minecraft/models/block/"+parent+".json"))
    rows_to_csv(out/"WOOL_ANIMATION_SOURCE_AUDIT_9.csv",
        ["texture_id","png_relpath","sha256","width","height","png_bytes","chunk_names","apng_chunks","mcmeta_exists","frame_capacity","leaf_link","blockstate_link","item_link","vanilla_texture_animation"],rows)
    controls=[]
    for pid,(w,h,frametime,numexplicit) in POSITIVE.items():
        image=check_png(block/(pid+".png"))
        meta=read_json(block/(pid+".png.mcmeta"))
        an=meta["animation"]
        assert (image["width"],image["height"])==(w,h)
        assert not image["has_apng_chunks"]
        assert an.get("frametime",1)==frametime
        frames=an.get("frames",[])
        assert len(frames)==numexplicit
        frame_capacity=h//w
        assert h%w==0
        assert all(0<=int(t if isinstance(t,int) else t["index"])<frame_capacity for t in frames)
        controls.append([pid,image["width"],image["height"],frame_capacity,1,frametime,numexplicit,0])
    rows_to_csv(out/"ANIMATED_POSITIVE_CONTROLS_3.csv",
        ["texture_id","png_width","png_height","square_frame_capacity","mcmeta_exists","frametime_ticks","explicit_frame_entries","apng_chunks"],controls)
    result={
     "source_texture_count":len(rows),"source_animated_wool_count":0,
     "source_missing_wool_mcmeta_count":len(rows),"single_frame_wool_count":len(rows),
     "validated_block_model_json":len(rows),"validated_blockstate_json":len(rows),"validated_item_json":len(rows),
     "animated_source_positive_controls":len(controls),
     "in_game_footage_verified":0
    }
    (out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    if len(sys.argv)!=3:
        raise SystemExit("python REPRODUCE_ANIMATION_AUDIT_R009.py /path/to/1.21.11 OUT_DIR")
    main(Path(sys.argv[1]),Path(sys.argv[2]))
