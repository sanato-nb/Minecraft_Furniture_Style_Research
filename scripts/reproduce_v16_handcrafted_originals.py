#!/usr/bin/env python3
"""Reproduce v16 from a local checkout of the exact Handcrafted source assets.

No third-party dependencies, no uploads or downloads. Only reads source files and
research CSV/JSON. The caller must obtain the upstream repo separately.
"""
import argparse
import csv
import hashlib
import json
import struct
import zlib
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / 'research' / 'furniture_mods'

def rows(filename):
    with (REPORT / filename).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def digest(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()

def read_source(src, path, sha):
    raw = (src / path).read_bytes()
    actual = digest(raw)
    assert actual == sha, (path, 'SHA changed', actual, sha)
    return raw

def pixel_stats(raw):
    assert raw.startswith(b'\x89PNG\r\n\x1a\n')
    pos = 8
    w = h = depth = mode = None
    palette, alpha, idats = [], [], []
    while pos < len(raw):
        length = struct.unpack_from('>I', raw, pos)[0]
        tag = raw[pos+4:pos+8]
        chunk = raw[pos+8:pos+8+length]
        pos += length+12
        if tag == b'IHDR':
            w, h, depth, mode, compression, filtering, interlace = struct.unpack('>IIBBBBB', chunk)
            assert compression == filtering == interlace == 0
        elif tag == b'PLTE':
            palette = [tuple(chunk[i:i+3]) for i in range(0, len(chunk), 3)]
        elif tag == b'tRNS':
            alpha = list(chunk)
        elif tag == b'IDAT':
            idats.append(chunk)
        elif tag == b'IEND':
            break
    assert depth == 8 and mode in (2, 3, 6), (depth,mode)
    channels = {2:3,3:1,6:4}[mode]
    stride = w*channels
    data = zlib.decompress(b''.join(idats))
    assert len(data) == h*(1+stride)
    prev = bytearray(stride)
    pos = vis = invis = partial = 0
    colors = set()
    for y in range(h):
        filt = data[pos]
        pos += 1
        line = bytearray(data[pos:pos+stride]); pos += stride
        for x in range(stride):
            left = line[x-channels] if x>=channels else 0
            above = prev[x]
            diag = prev[x-channels] if x>=channels else 0
            if filt == 0: pred=0
            elif filt == 1: pred=left
            elif filt == 2: pred=above
            elif filt == 3: pred=(left+above)//2
            elif filt == 4:
                p=left+above-diag
                da,db,dc=abs(p-left),abs(p-above),abs(p-diag)
                pred=left if da<=db and da<=dc else above if db<=dc else diag
            else: raise AssertionError(f'PNG filter {filt}')
            line[x]=(line[x]+pred)&255
        for x in range(w):
            ofs=x*channels
            if mode==6:
                rgba=tuple(line[ofs:ofs+4])
            elif mode==2:
                rgba=(*line[ofs:ofs+3],255)
            else:
                i=line[ofs]
                rgba=(*palette[i], alpha[i] if i<len(alpha) else 255)
            if rgba[3] == 0:
                invis+=1
            else:
                vis+=1
                colors.add(rgba)
                if rgba[3] < 255:
                    partial+=1
        prev=line
    assert pos==len(data) and vis+invis==w*h
    return dict(width=w,height=h,visible_pixels=vis,transparent_pixels=invis,
                partial_pixels=partial,unique_visible_rgba=len(colors))

def main(source):
    pngs=rows('v16/handcrafted_12_new_png_pixel_metrics.csv')
    assert len(pngs)==12
    for item in pngs:
        raw=read_source(source,item['path'],item['upstream_blob_sha'])
        actual=pixel_stats(raw)
        for key,value in actual.items():
            assert value==int(item[key]),(item['name'],key,value,item[key])
        assert len(raw)==int(item['png_bytes'])
    prior=rows('v13/handcrafted_png_12_pixel_metrics.csv')
    pixelmap={r['name']:(int(r['width']),int(r['height'])) for r in prior}
    pixelmap.update({r['name']:(int(r['width']),int(r['height'])) for r in pngs})
    leafinfo=json.loads((REPORT/'v16/handcrafted_16_leaf_original_verification.json').read_text(encoding='utf-8'))
    summary=json.loads((REPORT/'v16/v16_original_face_mapping_audit.json').read_text(encoding='utf-8'))
    leafrows=rows('v16/handcrafted_16_leaf_face_summary.csv')
    expected_leaf={r['leaf']:r for r in leafrows}
    faces=modfaces=vanilla=aligned=outside=zero=mirrored=0
    parents={}
    for leaf in leafinfo['source_measurements']:
        parent=leaf['parent'].removeprefix('handcrafted:block/')
        doc=json.loads(read_source(source,leaf['path'],leaf['sha']))
        if parent not in parents:
            fp=f'common/src/main/resources/assets/handcrafted/models/block/{parent}.json'
            parents[parent]=json.loads(read_source(source,fp,expected_leaf[leaf['name']]['parent_sha']))
        model=parents[parent]
        assert doc['parent']==leaf['parent']
        assert not doc.get('elements')
        textures={**model.get('textures',{}),**doc.get('textures',{})}
        local_faces=0
        for element in model.get('elements',[]):
            for face in element.get('faces',{}).values():
                faces+=1;local_faces+=1
                ref=face['texture']
                for _ in range(16):
                    if not ref.startswith('#'): break
                    ref=textures[ref[1:]]
                assert not ref.startswith('#'),(leaf['name'],ref)
                uv=face['uv']
                if uv[0]==uv[2] or uv[1]==uv[3]: zero+=1
                if uv[2]<uv[0] or uv[3]<uv[1]: mirrored+=1
                if ref.startswith('handcrafted:block/'):
                    modfaces+=1
                    name=ref.removeprefix('handcrafted:block/')
                    w,h=pixelmap[name]
                    px=[uv[i]*(w if i%2==0 else h)/16 for i in range(4)]
                    if all(abs(p-round(p))<1e-6 for p in px): aligned+=1
                    if not all(-1e-6<=p<=(w if i%2==0 else h)+1e-6 for i,p in enumerate(px)):
                        outside+=1
                elif ref.startswith('minecraft:block/'):
                    vanilla+=1
                else: raise AssertionError((leaf['name'],ref))
        assert local_faces==int(expected_leaf[leaf['name']]['face_instances'])
    actual=dict(original_json_sha_matched_30=len(leafinfo['source_measurements'])+len(parents),
                face_instances=faces,handcrafted_faces=modfaces,vanilla_faces=vanilla,
                aligned_faces=aligned,outside_png=outside,zero_area=zero,flipped_uv=mirrored)
    for k,v in actual.items():
        assert v==summary['stats'][k],(k,v,summary['stats'][k])
    print('PASS: 12 PNG fully decoded, 16 leaves + 14 parents SHA verified,',
          f'{faces} inherited faces, {aligned}/{modfaces} mod UV aligned,',
          f'{vanilla} vanilla faces unresolved')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('upstream_handcrafted_dir',type=Path,
        help='local checkout of terrarium-earth/Handcrafted at pinned 8d21d166... source commit')
    args=parser.parse_args()
    main(args.upstream_handcrafted_dir)
