#!/usr/bin/env python3
"""R007 shader-source-only audit for user-extracted Minecraft 1.21.11.
Requires Python standard library only. It does not run Minecraft or inspect actual render passes.
Usage: python REPRODUCE_SHADER_AUDIT.py /path/to/cloned/Minecraft_Furniture_Style_Research
"""
from pathlib import Path
from hashlib import sha1
import re
import sys
SOURCES = {
 "assets/minecraft/shaders/core/terrain.fsh":"67e9a8efd74333b3e9b879b851236705f77d1960",
 "assets/minecraft/shaders/core/terrain.vsh":"a685eab73b407de7c3e0770a842fa5cea995b611",
 "assets/minecraft/shaders/include/chunksection.glsl":"a8db49f002a90180016e2f06ab6a4015618fb98d",
 "assets/minecraft/shaders/include/globals.glsl":"bd5515ec85151c3820f5e4ef728835f797bfa981",
 "assets/minecraft/shaders/include/fog.glsl":"cbdcb2d138d2c24f178465b2ed79be3fb16f290b",
 "assets/minecraft/shaders/include/projection.glsl":"c405b8f8b58e52dcf18749041befb9b3f4ebfd8a",
}
def git_blob_sha(data):
    return sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def main(root):
    base=root/"1.21.11"
    decoded={}
    for path,expected in SOURCES.items():
        data=(base/path).read_bytes()
        actual=git_blob_sha(data)
        assert actual==expected,(path,actual,expected)
        decoded[path]=data.decode("utf-8")
    f=decoded["assets/minecraft/shaders/core/terrain.fsh"]
    v=decoded["assets/minecraft/shaders/core/terrain.vsh"]
    g=decoded["assets/minecraft/shaders/include/globals.glsl"]
    c=decoded["assets/minecraft/shaders/include/chunksection.glsl"]
    assertions=[
        ("shader nearest gradient sample","textureGrad(sampler, uv, du, dv)" in f),
        ("shader RGSS explicit LOD","textureLod(source, sampleUV, mipLevelLow)" in f and "textureLod(source, sampleUV, mipLevelHigh)" in f),
        ("shader RGSS branch","UseRgss == 1" in f and "sampleRGSS" in f and "sampleNearest" in f),
        ("shader conditional cutout","#ifdef ALPHA_CUTOUT" in f and "discard;" in f),
        ("terrain vertex UV","texCoord0 = UV0;" in v),
        ("chunk section uniforms","ivec2 TextureSize" in c and "float ChunkVisibility" in c),
        ("global RGSS uniform","int UseRgss" in g),
        ("terrain vertex chunk relative position","ChunkPosition - CameraBlockPos" in v),
    ]
    imports=0
    for p in ("assets/minecraft/shaders/core/terrain.fsh","assets/minecraft/shaders/core/terrain.vsh"):
        for name in re.findall(r"#moj_import\s+<minecraft:([^>]+)>",decoded[p]):
            dependency="assets/minecraft/shaders/include/"+name
            assert dependency in decoded,(p,name)
            imports+=1
    assert imports==7,imports
    for label,passed in assertions:
        print(("PASS" if passed else "FAIL")+" "+label)
    assert all(b for _,b in assertions)
    print("6 distinct original source paths matched expected Git blob SHA, 7/7 resolved import edges")
    print("No proof of shader selected for glass / alpha blend / sort / actual mipmap / in-game output")
if __name__=="__main__":
    assert len(sys.argv)==2,"Pass repository clone root as sole argument"
    main(Path(sys.argv[1]))
