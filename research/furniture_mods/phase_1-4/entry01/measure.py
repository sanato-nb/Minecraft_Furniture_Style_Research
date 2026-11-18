"""1-4 첫 회차. 고정 PNG와 v24 의자 모델·UV의 정적 픽셀 영역을 검사한다."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
import io
import json
import lzma
from math import ceil, floor
from pathlib import Path
import sqlite3
import struct
import subprocess
import tarfile
import zipfile
from contextlib import ExitStack

import numpy as np
from PIL import Image


def csv_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def write_rows(path, rows):
    file = io.StringIO(newline='')
    writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    data = file.getvalue().encode('utf-8')
    if path.suffix == '.gz':
        data = gzip.compress(data, mtime=0)
    path.write_bytes(data)


def git(*args):
    return subprocess.check_output(['git', *map(str, args)])


def hash_bytes(data, kind):
    if kind == 'GIT_BLOB_SHA1':
        return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    if kind == 'SHA256':
        return hashlib.sha256(data).hexdigest()
    raise ValueError(kind)


def archived(repo, commit, wanted):
    found = {}
    with subprocess.Popen(['git', '-C', str(repo), 'archive', commit], stdout=subprocess.PIPE) as process:
        with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
            for item in archive:
                if item.isfile() and item.name in wanted:
                    found[item.name] = archive.extractfile(item).read()
        if process.wait():
            raise RuntimeError(f'git archive failed for {commit}')
    return found


def pixel_metrics(image):
    histogram = Counter(image.getdata() if not hasattr(image, 'get_flattened_data') else image.get_flattened_data())
    transparent = sum(count for rgba, count in histogram.items() if rgba[3] == 0)
    partial = sum(count for rgba, count in histogram.items() if 0 < rgba[3] < 255)
    opaque = sum(count for rgba, count in histogram.items() if rgba[3] == 255)
    visible = [(rgba, count) for rgba, count in histogram.items() if rgba[3] > 0]
    dominant = sorted(visible, key=lambda item: (-item[1], item[0]))[:4]
    return transparent, partial, opaque, len({rgba[:3] for rgba, _ in visible}), '|'.join(
        bytes(rgba).hex() + ':' + str(count) for rgba, count in dominant)


def verify_pixels(image, metrics):
    data = np.asarray(image)
    alpha = data[..., 3]
    alpha_count = np.bincount(alpha.ravel(), minlength=256)
    colors = len(np.unique(data[alpha > 0][:, :3], axis=0))
    assert tuple(map(int, (alpha_count[0], alpha_count[1:255].sum(), alpha_count[255], colors))) == metrics[:4]


def decode_png(data):
    with Image.open(io.BytesIO(data)) as image:
        assert image.format == 'PNG'
        image.verify()
    with Image.open(io.BytesIO(data)) as image:
        frame_count = image.n_frames
        rgba = image.convert('RGBA')
    width, height, depth, color = struct.unpack('>IIBB', data[16:26])
    assert rgba.size == (width, height)
    return rgba, frame_count, depth, color


def normalize(texture):
    return texture if ':' in texture else 'minecraft:' + texture


def resolve(slot, textures):
    seen = set()
    while slot.startswith('#'):
        name = slot[1:]
        assert name not in seen, name
        seen.add(name)
        slot = textures[name]
    return normalize(slot)


def to_pixel_box(uv, width, height):
    u0, v0, u1, v1 = uv
    if u0 == u1 or v0 == v1:
        return None
    return (floor(min(u0,u1)*width/16), floor(min(v0,v1)*height/16),
            ceil(max(u0,u1)*width/16), ceil(max(v0,v1)*height/16))


def measure_chairs(db, chair_models, source_docs, png_by_id, images):
    metrics_for_box = lru_cache(None)(lambda texture, box: pixel_metrics(images[texture].crop(box)))
    outputs = []
    for row in chair_models:
        path = row['source_path']
        leaf_bytes = source_docs[path]
        parent_path = path.split('/models/',1)[0]+'/models/'+row['parent_template'].split(':',1)[1]+'.json'
        parent_bytes = source_docs[parent_path]
        assert hash_bytes(leaf_bytes, 'GIT_BLOB_SHA1') == row['source_sha']
        assert hash_bytes(parent_bytes, 'GIT_BLOB_SHA1') == row['parent_sha']
        leaf, parent = map(json.loads, (leaf_bytes, parent_bytes))
        assert leaf['parent'] == row['parent_template'] and not leaf.get('elements')
        assert parent['parent'] == 'minecraft:block/block'
        textures = {**parent.get('textures',{}), **leaf.get('textures',{})}
        published = db.execute('''
             SELECT m.model_key, p.resource_id AS parent_ref, p.sha AS parent_sha,
                    f.element_index, f.direction, f.uv, f.uv_declared, f.uv_rotation,
                    f.slot, t.resource_id, t.id, t.sha
             FROM effective_face_texture f JOIN model m ON m.model_key=f.model_key
             JOIN model p ON p.model_key=f.provider_key JOIN texture t ON t.id=f.texture_id
             WHERE m.source_id='AF' AND m.resource_id=? AND m.sha=?
             ORDER BY f.element_index,f.direction
        ''', (row['leaf'],row['source_sha'])).fetchall()
        source_faces = {(i,d): config for i, element in enumerate(parent['elements'])
                        for d,config in element['faces'].items()}
        assert len(published) == len(source_faces) == int(row['inherited_faces']) == 46
        assert {(f['element_index'],f['direction']) for f in published} == set(source_faces)
        for f in published:
            config = source_faces[f['element_index'],f['direction']]
            assert (f['parent_ref'],f['parent_sha'],f['slot']) == (row['parent_template'],row['parent_sha'],config['texture'])
            assert config.get('rotation',0)==f['uv_rotation'] and f['uv_declared'] and 'uv' in config
            uv = tuple(Fraction(str(v)) for v in config['uv'])
            assert uv == tuple(map(Fraction,f['uv'].split('|')))
            resource = resolve(config['texture'],textures)
            assert resource == f['resource_id']
            tex = png_by_id[f['id']]
            assert tex['computed_sha']==f['sha'] and tex['mcmeta_status']!='ANIMATION' and tex['png_frames']==1
            box = to_pixel_box(uv,tex['width'],tex['height'])
            status = 'ZERO_UV_AREA'
            trans=partial=opaque=distinct=0
            palette = region_sha = ''
            if box:
                assert 0 <= box[0] < box[2] <= tex['width'] and 0 <= box[1] < box[3] <= tex['height'], (resource,uv)
                region = images[f['id']].crop(box)
                metrics = metrics_for_box(f['id'],box)
                verify_pixels(region,metrics)
                trans,partial,opaque,distinct,palette = metrics
                region_sha = hashlib.sha256(region.tobytes()).hexdigest()
                status = 'SAMPLED_STATIC_RECTANGLE'
            outputs.append(dict(model_key=f['model_key'],model_ref=row['leaf'],model_sha=row['source_sha'],
                                parent_ref=f['parent_ref'],parent_sha=f['parent_sha'],element_index=f['element_index'],
                                direction=f['direction'],texture_slot=f['slot'],texture_id=f['id'],resource_id=resource,
                                texture_sha=f['sha'],texture_scope=tex['scope'],uv=f['uv'],uv_rotation=f['uv_rotation'],
                                u_reversed=int(uv[0]>uv[2]),v_reversed=int(uv[1]>uv[3]),
                                pixel_box='|'.join(map(str,box)) if box else '',status=status,
                                transparent=trans,partial_alpha=partial,opaque=opaque,visible_rgb_colors=distinct,
                                top4_visible_rgba_counts=palette,rgba8_sha256=region_sha))
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('repo','af','hc','jars','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    phase = args.repo/'research/furniture_mods/phase_1-3'
    args.out.mkdir(parents=True,exist_ok=True)
    ledger = csv_rows(phase/'F/1-3_TEXTURE_UV_HANDOFF.csv')
    chairs = csv_rows(phase/'F/F_V24_CHAIR_PNG.csv')
    chair_models = csv_rows(phase/'A/A_CHAIR_39_RELATIONS.csv')
    chair_ids = {r['resource_id']:r for r in chairs}
    assert len(chair_ids)==24 and len(chair_models)==39
    status_counts = Counter(r['disposition'] for r in ledger)
    assert status_counts == {'PNG_UV_CANDIDATE':1996,'PRIOR_RGBA_SHA_MATCH':175,'DECLARED_SLOT_ONLY':77,'SOURCE_EXCEPTION':8}
    targets = [r for r in ledger if r['disposition']=='PNG_UV_CANDIDATE' or r['resource_id'] in chair_ids]
    assert len(targets)==2001
    sources = json.loads((phase/'G/G_SOURCE_RECOUNT.json').read_bytes())['source_records']
    vanilla = json.loads((phase/'C/C_AUDIT.json').read_bytes())['vanilla_sources']
    paths = defaultdict(set)
    for row in targets:
        paths[row['source_id']].update([row['path'],row['path']+'.mcmeta'])
    for row in chair_models:
        base = row['source_path'].split('/models/',1)[0]
        paths['AF'].update([row['source_path'],base+'/models/'+row['parent_template'].split(':',1)[1]+'.json'])
    with ExitStack() as stack:
        def open_jar(path):
            return stack.enter_context(zipfile.ZipFile(path))
        readers = {mod:archived(repo,sources[mod]['pin'],paths[mod]).get
                   for mod,repo in [('AF',args.af),('HC',args.hc)]}
        jar = args.jars/'macaw.jar'
        assert hashlib.sha256(jar.read_bytes()).hexdigest()==sources['MACAW']['sha256']
        archives={'MACAW':open_jar(jar)}
        for v, record in vanilla.items():
            jar=args.jars/(v+'.jar')
            assert hashlib.sha1(jar.read_bytes()).hexdigest()==record['sha1']
            archives['MC'+v]=open_jar(jar)
        names={key:set(z.namelist()) for key,z in archives.items()}
        for key, z in archives.items():
            readers[key]=lambda p,z=z,n=names[key]:z.read(p) if p in n else None
        png_by_id = {}
        images = {}
        png_report=[]
        for row in targets:
            texture_id, resource_id, path, source, kind = (row[k] for k in
                ('texture_id','resource_id','path','source_id','source_hash_kind'))
            read = readers[source]
            png = read(path)
            assert png is not None, path
            sha = hash_bytes(png,kind)
            assert sha==row['source_sha'], path
            image,frames,depth,color = decode_png(png)
            metrics = pixel_metrics(image)
            verify_pixels(image,metrics)
            meta = read(path+'.mcmeta')
            meta_status = 'NONE'
            if meta is not None:
                assert isinstance(json.loads(meta),dict),path
                meta_status = 'ANIMATION' if 'animation' in json.loads(meta) else 'OTHER'
            in_chairs = resource_id in chair_ids
            scope = 'NEW_CANDIDATE' if row['disposition']=='PNG_UV_CANDIDATE' else 'PRIOR_CHAIR_CONTROL'
            if in_chairs:
                assert (path,sha)==(chair_ids[resource_id]['pinned_path'],chair_ids[resource_id]['source_sha'])
                images[int(texture_id)]=image
            report = dict(texture_id=texture_id,resource_id=resource_id,minecraft=row['minecraft'],
                          source_id=source,scope=scope,priority_chair=int(in_chairs),hash_algorithm=kind,
                          pinned_path=path,computed_sha=sha,png_bytes=len(png),width=image.width,height=image.height,
                          bit_depth=depth,png_color_type=color,
                          pixels_per_u=float(Fraction(image.width,16)),pixels_per_v=float(Fraction(image.height,16)),
                          content_sha256=hashlib.sha256(png).hexdigest(),rgba8_sha256=hashlib.sha256(image.tobytes()).hexdigest(),
                          png_frames=frames,mcmeta_status=meta_status,
                          mcmeta_sha=hash_bytes(meta,kind) if meta is not None else '',
                          transparent=metrics[0],partial_alpha=metrics[1],opaque=metrics[2],
                          visible_rgb_colors=metrics[3],top4_visible_rgba_counts=metrics[4])
            png_by_id[int(texture_id)]=report
            png_report.append(report)
        db=stack.enter_context(sqlite3.connect(':memory:'))
        db.row_factory=sqlite3.Row
        db.deserialize(lzma.decompress((phase/'F/furniture_research.sqlite.xz').read_bytes()))
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        db_textures = db.execute('SELECT id,resource_id,minecraft,source_id,texture_status,path,sha FROM texture').fetchall()
        fields = ('texture_id','resource_id','minecraft','source_id','texture_status','path','source_sha')
        assert {tuple(str(v) if v is not None else '' for v in row) for row in db_textures} == {
            tuple(r[k] for k in fields) for r in ledger}
        for prior in csv_rows(phase/'F/F_PRIOR_RGBA_LEDGER.csv'):
            path = args.repo/prior['ledger_path']
            assert hash_bytes(path.read_bytes(),'GIT_BLOB_SHA1') == prior['ledger_blob_sha']
            rows = csv_rows(path)
            if rows and 'newly_sampled' in rows[0]:
                rows = [r for r in rows if r['newly_sampled']=='1']
            assert len(rows)==int(prior['rows_recounted'])
        source_docs = {p:readers['AF'](p) for p in paths['AF'] if p.endswith('.json')}
        uv_report = measure_chairs(db,chair_models,source_docs,png_by_id,images)
        assert len(uv_report)==1794 and len({r['resource_id'] for r in uv_report})==24
        db_counts = dict(db.execute('''
            SELECT texture_id, sum(face_count) FROM model_slot
            WHERE texture_id IS NOT NULL GROUP BY texture_id
        '''))
        assert all(db_counts.get(int(r['texture_id']),0)==int(r['face_instances']) for r in ledger)
        assignment_counts=Counter(r['texture_id'] for r in uv_report)
        outstanding=[]
        for r in ledger:
            if r['disposition']!='PNG_UV_CANDIDATE':
                continue
            tid=int(r['texture_id'])
            face_count=db_counts[tid]
            done=assignment_counts[tid]
            assert face_count>=done and face_count>0
            outstanding.append(dict(texture_id=tid,resource_id=r['resource_id'],minecraft=r['minecraft'],
                                    static_model_face_instances=face_count,entry01_uv_measured=done,
                                    entry01_uv_pending=face_count-done,mcmeta_status=png_by_id[tid]['mcmeta_status']))
        missing=[]
        af_tree=set(git('-C',args.af,'ls-tree','-r','--name-only','-z',sources['AF']['pin']).decode().split('\0'))
        for row in ledger:
            if row['disposition']!='SOURCE_EXCEPTION':
                continue
            namespace, identifier = row['resource_id'].split(':',1)
            suffix=f'/assets/{namespace}/textures/{identifier}.png'
            assert namespace=='another_furniture' and not any(p.endswith(suffix) for p in af_tree)
            missing.append(dict(texture_id=row['texture_id'],resource_id=row['resource_id'],
                                model_face_uses=row['face_instances'],source_status='EXACT_PATH_ABSENT_IN_PINNED_GIT',
                                next_check='loader/version/alternate resource mapping'))
    write_rows(args.out/'1-4_PNG_PIXEL_LEDGER.csv.gz',png_report)
    write_rows(args.out/'1-4_CHAIR_UV_LEDGER.csv.gz',uv_report)
    write_rows(args.out/'1-4_SOURCE_EXCEPTIONS.csv',missing)
    write_rows(args.out/'1-4_NEW_UV_QUEUE.csv.gz',outstanding)
    new=[r for r in png_report if r['scope']=='NEW_CANDIDATE']
    result=dict(status='ENTRY01_MEASURED',input_dispositions=status_counts,
                newly_decoded_png=len(new),previous_png_controls_redecoded=len(png_report)-len(new),
                new_png_distinct_content_sha256=len({r['content_sha256'] for r in new}),
                new_png_by_source=Counter(r['source_id'] for r in new),
                new_png_dimension_counts=Counter(f"{r['width']}x{r['height']}" for r in new),
                new_png_with_transparent_pixels=sum(r['transparent']>0 for r in new),
                new_png_with_partial_alpha=sum(r['partial_alpha']>0 for r in new),
                new_png_with_animation_metadata=sum(r['mcmeta_status']=='ANIMATION' for r in new),
                new_png_with_apng_frames=sum(r['png_frames']>1 for r in new),
                chair_models=len(chair_models),chair_png=len(chair_ids),
                chair_uv_status=Counter(r['status'] for r in uv_report),
                chair_uv_for_new_png=sum(r['texture_scope']=='NEW_CANDIDATE' for r in uv_report),
                chair_uv_reversed_faces=sum(bool(r['u_reversed'] or r['v_reversed']) for r in uv_report),
                chair_uv_rotated_faces=sum(r['uv_rotation']!=0 for r in uv_report),
                chair_sampled_rectangles_with_transparency=sum(r['transparent']>0 for r in uv_report),
                chair_sampled_rectangles_with_partial_alpha=sum(r['partial_alpha']>0 for r in uv_report),
                new_candidate_uv_face_instances=sum(r['static_model_face_instances'] for r in outstanding),
                new_candidate_uv_sampled=sum(r['entry01_uv_measured'] for r in outstanding),
                new_candidate_uv_pending=sum(r['entry01_uv_pending'] for r in outstanding),
                missing_exact_paths=len(missing),independent_pixel_counters_agreed=True)
    (args.out/'1-4_ENTRY01_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
