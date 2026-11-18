"""Measure source support for UV exceptions without changing the original face ledger."""
import argparse
from collections import Counter, defaultdict
from contextlib import ExitStack
from fractions import Fraction
import csv
import hashlib
import json
import lzma
from math import ceil, floor
from pathlib import Path
import runpy
import sqlite3
import zipfile

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
UPSTREAM = PHASE.parent / 'phase_1-3/F'
BASE = runpy.run_path(str(PHASE/'entry02/measure_uv.py'))
FIRST = BASE['FIRST']
EXPECTED = {'STATIC_RECT':506614, 'ANIMATED_FRAME_RECTS':5095, 'ZERO_UV_AREA':69118,
            'OUTSIDE_TEXTURE_UV':5144, 'MISSING_PINNED_PNG':139, 'SLOT_UNBOUND':6202}
NO_INTERSECTION = 'NO_PINNED_SPRITE_INTERSECTION'
RELEASES = {
    'fabric_402':'3f0e6c276dde5cd6390e9c14bc4c283e4043f25d812c1f5ecc36b7b2f61642b5',
    'neoforge_403':'a416cb33333d7a489c7a7314e918f564787838630b014c281b83adde014457d0'}


def csv_rows(path):
    return BASE['read_csv'](path)


def bucket(uv, size):
    """Map one UV axis to in-sprite source cells and describe exact boundary cases."""
    lo, hi = sorted(uv)
    if hi == lo:
        if not 0 <= lo <= 16:
            return None
        position = lo * size / 16
        # On an exact texel edge, preserve both adjacent source candidates when present.
        x0 = max(0, ceil(position) - 1)
        x1 = min(size, floor(position) + 1)
        edge = 'SPRITE_EDGE' if lo in (0, 16) else 'TEXEL_EDGE' if position.denominator == 1 else 'INTERIOR'
        return x0, x1, Fraction(1), edge
    lower, upper = max(lo, 0), min(hi, 16)
    if lower > upper:
        return None
    if lower == upper:
        cell = 0 if lower == 0 else size - 1
        return cell, cell+1, Fraction(0), 'EDGE_CONTACT'
    return floor(lower * size / 16), ceil(upper * size / 16), (upper-lower)/(hi-lo), 'SPAN'


def group_faces(path, queue):
    groups = defaultdict(Counter)
    original = Counter()
    with lzma.open(path,'rt',newline='',encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            status = row['status']
            original[status] += 1
            if status in ('ZERO_UV_AREA','OUTSIDE_TEXTURE_UV'):
                tid = int(row['texture_id'])
                assert queue[tid]['path']
                groups[tid][BASE['vector'](row['uv']),status] += 1
    assert original == EXPECTED, original
    expected = {(int(r['texture_id']),r['uv'],r['reason']):int(r['face_instances'])
                for r in csv_rows(PHASE/'entry02/UV_EXCEPTIONS.csv')
                if r['reason'] in ('ZERO_UV_AREA','OUTSIDE_TEXTURE_UV')}
    observed = {(tid,BASE['packed'](uv),status):n for tid, rows in groups.items()
                for (uv,status),n in rows.items()}
    assert observed == expected
    return groups


def measure_groups(groups, queue, sources, first):
    output, counts, reasons = [], Counter(), Counter()
    for tid, group in sorted(groups.items()):
        row = queue[tid]
        frames, _ = BASE['png_frames'](row,sources[row['source_id']],first.get(tid))
        for (uv,original), count in sorted(group.items()):
            a,b,c,d = uv
            width,height = frames[0].size
            u,v = bucket((a,c),width), bucket((b,d),height)
            label = ('POINT_SUPPORT' if a==c and b==d else 'LINE_SUPPORT' if a==c or b==d
                     else 'CLIPPED_RECT_SUPPORT')
            if u is None or v is None:
                counts[NO_INTERSECTION] += count
                reasons[original,NO_INTERSECTION] += count
                output.append((tid,row['resource_id'],BASE['packed'](uv),original,NO_INTERSECTION,
                               count,'',width,height,'','0','','','','','','','',''))
                continue
            if 'EDGE_CONTACT' in (u[3],v[3]):
                label = 'EDGE_CONTACT_SUPPORT'
            pixel_box = u[0],v[0],u[1],v[1]
            assert 0 <= pixel_box[0] < pixel_box[2] <= width and 0 <= pixel_box[1] < pixel_box[3] <= height
            counts[label] += count
            reasons[original,label] += count
            for i, frame in enumerate(frames):
                crop = frame.crop(pixel_box)
                metrics = FIRST['pixel_metrics'](crop)
                FIRST['verify_pixels'](crop,metrics)
                assert sum(metrics[:3]) == crop.width*crop.height
                output.append((tid,row['resource_id'],BASE['packed'](uv),original,label,count,i,
                               width,height,BASE['packed'](pixel_box),str(u[2]*v[2]),u[3],v[3],
                               *metrics,hashlib.sha256(crop.tobytes()).hexdigest()))
    return output,counts,reasons


def classify_slots(db):
    selected = {key for key, in db.execute('SELECT DISTINCT model_key FROM option WHERE model_key IS NOT NULL')}
    rows = []
    query = '''
        SELECT s.model_key,m.resource_id,s.slot,s.face_count,g.provider_key
        FROM model_slot s JOIN model m USING(model_key) JOIN geometry g USING(model_key)
        WHERE s.texture_id IS NULL
        ORDER BY s.model_key,s.slot
    '''
    candidates = '''
        SELECT m.resource_id,t.resource_id
        FROM lineage l JOIN model m USING(model_key) JOIN geometry g USING(model_key)
        JOIN model_slot s USING(model_key) JOIN texture t ON t.id=s.texture_id
        WHERE l.ancestor_key=? AND l.position>0 AND g.provider_key=? AND s.slot=? AND length(t.path)>0
        ORDER BY 1,2
    '''
    for key, resource, slot, faces, provider in db.execute(query):
        children = db.execute(candidates,(key,provider,slot)).fetchall()
        status = 'BOUND_CHILD_CONTEXT' if children else 'UNBOUND_NO_BOUND_CHILD'
        rows.append((key,resource,slot,faces,provider,int(key in selected),status,len(children),
                     len({texture for _,texture in children}),*(children[0] if children else ('',''))))
    assert sum(r[3] for r in rows)==EXPECTED['SLOT_UNBOUND'] and not any(r[5] for r in rows)
    return rows


def check_missing(queue, sources, releases):
    rows = []
    for tid,r in sorted(queue.items()):
        if r['disposition']!='SOURCE_EXCEPTION':
            continue
        namespace,path = r['resource_id'].split(':',1)
        jar_path = f'assets/{namespace}/textures/{path}.png'
        assert namespace == 'another_furniture' and not r['path']
        path = 'common/src/main/resources/'+jar_path
        present = sources['AF'](path) is not None
        jars = [jar_path in set(jar.namelist()) for jar in releases]
        assert not present and not any(jars)
        rows.append((tid,r['resource_id'],int(r['face_instances']),jar_path,int(present),*map(int,jars)))
    assert len(rows)==8 and sum(row[2] for row in rows)==EXPECTED['MISSING_PINNED_PNG']
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('af','hc','jars','faces','fabric-402','neoforge-403','out'):
        parser.add_argument('--'+key,type=Path,required=True)
    args = parser.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    queue = {int(row['texture_id']):row for row in csv_rows(UPSTREAM/'1-3_TEXTURE_UV_HANDOFF.csv')}
    groups = group_faces(args.faces,queue)
    first = {int(row['texture_id']):row for row in BASE['read_csv'](
        PHASE/'entry01/1-4_PNG_PIXEL_LEDGER.csv.gz',True)}
    with ExitStack() as stack:
        db = stack.enter_context(sqlite3.connect(':memory:'))
        db.deserialize(lzma.decompress((UPSTREAM/'furniture_research.sqlite.xz').read_bytes()))
        pins = dict(db.execute('SELECT id,pin FROM source'))
        wanted = defaultdict(set)
        for tid in groups:
            row=queue[tid]
            wanted[row['source_id']].update((row['path'],row['path']+'.mcmeta'))
        for r in queue.values():
            if r['disposition']=='SOURCE_EXCEPTION':
                namespace,path = r['resource_id'].split(':',1)
                wanted['AF'].add(f'common/src/main/resources/assets/{namespace}/textures/{path}.png')
        sources = {mod:FIRST['archived'](repo,pins[mod],wanted[mod]).get
                   for mod,repo in (('AF',args.af),('HC',args.hc))}
        for mod,name,kind in (('MACAW','macaw.jar','sha256'),('MC1.21.1','1.21.1.jar','sha1'),
                              ('MC1.21.11','1.21.11.jar','sha1')):
            jar_path = args.jars/name
            assert hashlib.new(kind,jar_path.read_bytes()).hexdigest()==pins[mod]
            jar = stack.enter_context(zipfile.ZipFile(jar_path))
            names=frozenset(jar.namelist())
            sources[mod] = lambda path,jar=jar,names=names: jar.read(path) if path in names else None
        releases = []
        for field,sha in RELEASES.items():
            path = getattr(args,field)
            assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
            releases.append(stack.enter_context(zipfile.ZipFile(path)))
        regions,counts,reasons = measure_groups(groups,queue,sources,first)
        slots = classify_slots(db)
        missing = check_missing(queue,sources,releases)
    BASE['write_csv'](args.out/'UV_SOURCE_SUPPORT.csv.xz',
        ('texture_id resource_id uv original_status outcome face_instances frame frame_width frame_height pixel_box '
         'within_sprite_fraction u_axis v_axis transparent partial_alpha opaque visible_rgb dominant_rgba rgba_sha256').split(),regions)
    BASE['write_csv'](args.out/'SLOT_CHILD_CONTEXT.csv.xz',
        ('model_key model slot face_instances provider_key direct_blockstate_selection outcome bound_child_models '
         'unique_child_textures example_child example_texture').split(),slots)
    BASE['write_csv'](args.out/'MISSING_TEXTURE_RELEASE_CHECK.csv',
        'texture_id resource_id face_instances expected_png pinned_git_exists fabric_402_exists neoforge_403_exists'.split(),missing)
    BASE['write_csv'](args.out/'UV_OUTCOME_COUNTS.csv',
        'original_status outcome face_instances'.split(),[(a,b,count) for (a,b),count in sorted(reasons.items())])
    original_count = EXPECTED['STATIC_RECT']+EXPECTED['ANIMATED_FRAME_RECTS']
    new_count = sum(v for k,v in counts.items() if k!=NO_INTERSECTION)
    slot_counts = Counter()
    for row in slots:
        slot_counts[row[6]] += row[3]
    summary = dict(fixed_faces=sum(EXPECTED.values()), original_full_rect_samples=original_count,
        supplemental_source_support_faces=new_count, face_instances_with_any_source_sample=original_count+new_count,
        pixel_support_counts=counts, unbound_face_contexts=slot_counts,
        unchanged_missing_png_faces=sum(r[2] for r in missing),
        exception_texture_paths_checked=len(groups), uv_support_frame_rows=len(regions),
        distinct_uv_exception_groups=sum(map(len,groups.values())),
        left_without_own_source_samples=sum(EXPECTED.values())-original_count-new_count)
    assert (summary['fixed_faces'], original_count, new_count)==(592312,511709,74260)
    assert len(missing)==8 and slot_counts=={'BOUND_CHILD_CONTEXT':6196,'UNBOUND_NO_BOUND_CHILD':6}
    (args.out/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
