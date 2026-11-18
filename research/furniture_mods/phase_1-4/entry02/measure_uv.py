"""Reproduce the phase 1-4 static face/texture census from the pinned sources."""
import argparse
from collections import Counter, defaultdict
from contextlib import ExitStack
import csv
from fractions import Fraction
import gzip
import hashlib
import json
import lzma
from pathlib import Path
import runpy
import sqlite3
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[4]
PHASE = ROOT / 'research/furniture_mods/phase_1-3'
ENTRY01 = Path(__file__).resolve().parent.parent / 'entry01'
FIRST = runpy.run_path(str(ENTRY01 / 'measure.py'))
HISTORIC_UV = ROOT / 'research/vanilla_textures/by_stage/1-1-02/TEX02-R008/VERIFY_DEFAULT_UV_BYTECODE.py'
DIRECTIONS = ('down', 'up', 'north', 'south', 'west', 'east')


def default_uv(start, end, direction, sixteen=16):
    x, y, z = start
    X, Y, Z = end
    return dict(zip(DIRECTIONS, (
        (x, sixteen-Z, X, sixteen-z), (x, z, X, Z),
        (sixteen-X, sixteen-Y, sixteen-x, sixteen-y),
        (x, sixteen-Y, X, sixteen-y), (z, sixteen-Y, Z, sixteen-y),
        (sixteen-Z, sixteen-Y, sixteen-z, sixteen-y),
    )))[direction]


def verify_uv_1211(jar):
    """Symbolically evaluate the six float-array constructors in BlockElement."""
    prior = runpy.run_path(str(HISTORIC_UV))
    parser = prior['ClassFile']
    names = ('gfx.class', 'gfx$1.class', 'ji.class', 'gga.class')
    bodies = {name: jar.read(name) for name in names}
    element, mapping, direction, face_uv = (parser(body) for body in bodies.values())
    assert all(name.upper() in [item[1] for item in direction.cp if item and item[0] == 1]
               for name in DIRECTIONS)
    code = mapping.methods['<clinit>', '()V']
    fields = [mapping.resolve(int.from_bytes(code[i+4:i+6], 'big'))
              for i in range(len(code)-9)
              if code[i] == code[i+3] == 0xb2 and code[i+6] == 0xb6]
    assert fields == [f'ji.{name}:Lji;' for name in 'abcdef']
    assign = element.methods['a', '()V']
    refs = {element.resolve(int.from_bytes(assign[i+1:i+3], 'big'))
            for i, op in enumerate(assign[:-2]) if op == 0xb6}
    assert {'gfx.a:(Lji;)[F', 'gga.a:([F)V'} <= refs
    fallback = face_uv.methods['a', '([F)V']
    assert fallback[0] == 0x2a and fallback[1] == 0xb4 and fallback[4] == 0xc7 and fallback[-1] == 0xb1

    code = element.methods['a', '(Lji;)[F']
    switch = code.index(b'\xaa')
    table = (switch+4) & ~3
    assert struct.unpack_from('>ii', code, table+4) == (1, 6)
    offsets = struct.unpack_from('>6i', code, table+12)
    found = {}
    for name, offset in zip(DIRECTIONS, offsets):
        start = switch + offset
        assert code[start:start+3] == b'\x07\xbc\x06'
        i = start + 3
        expressions = []
        for index in range(4):
            assert code[i:i+2] == bytes((0x59, 0x03+index))
            i += 2
            complement = code[i] == 0x12
            if complement:
                assert element.resolve(code[i+1]) == 16.0
                i += 2
            assert code[i:i+2] == b'\x2a\xb4' and code[i+4] == 0xb6
            field = element.resolve(int.from_bytes(code[i+2:i+4], 'big'))
            axis = element.resolve(int.from_bytes(code[i+5:i+7], 'big'))
            assert field in ('gfx.a:Lorg/joml/Vector3f;', 'gfx.b:Lorg/joml/Vector3f;')
            assert axis in [f'org/joml/Vector3f.{a}:()F' for a in 'xyz']
            expr = ('from' if field[4] == 'a' else 'to') + '.' + axis[18]
            i += 7
            if complement:
                assert code[i] == 0x66
                expr = f'(16-{expr})'
                i += 1
            assert code[i] == 0x51
            i += 1
            expressions.append(expr)
        assert code[i] == 0xb0
        found[name] = expressions
        values = dict(zip(('from.x','from.y','from.z','to.x','to.y','to.z'), (1,2,3,7,9,13)))
        expected = tuple(16-values[e[4:-1]] if e.startswith('(') else values[e] for e in expressions)
        assert default_uv((1,2,3), (7,9,13), name) == expected
    assert found == prior['EXPECTED']
    return {'classes_sha256': {name: hashlib.sha256(body).hexdigest() for name, body in bodies.items()},
            'formulas': found}


def read_csv(path, compressed=False):
    opener = gzip.open if compressed else open
    with opener(path, 'rt', encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, fields, rows):
    if path.suffix == '.xz':
        stream = lzma.open(path, 'wt', encoding='utf-8', newline='')
    else:
        stream = path.open('w', encoding='utf-8', newline='')
    with stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(fields)
        writer.writerows(rows)


def vector(value):
    return tuple(map(Fraction, value.split('|')))


def packed(values):
    return '|'.join(map(str, values))


def check_providers(db, sources):
    result = {}
    records = db.execute('''
        SELECT f.provider_key, m.source_id, m.path, m.sha, f.element_index, f.direction,
               f.slot, f.uv, f.uv_declared, f.uv_rotation, f.cullface, f.tintindex,
               e.source_from, e.source_to
        FROM face f JOIN model m ON m.model_key=f.provider_key
        JOIN element e USING(provider_key,element_index)
        ORDER BY f.provider_key,f.element_index,f.direction
    ''')
    docs = {}
    for key, source, path, sha, index, direction, slot, uv, declared, rotation, cull, tint, a, b in records:
        if key not in docs:
            data = sources[source](path)
            kind = 'GIT_BLOB_SHA1' if source in ('AF', 'HC') else 'SHA256'
            assert FIRST['hash_bytes'](data, kind) == sha, path
            docs[key] = json.loads(data, parse_float=Fraction)['elements']
        element = docs[key][index]
        source_face = element['faces'][direction]
        assert tuple(element['from']) == vector(a) and tuple(element['to']) == vector(b), (key,index)
        assert (slot, declared, rotation, cull, tint) == (
            source_face['texture'], int('uv' in source_face), source_face.get('rotation', 0),
            source_face.get('cullface', ''), str(source_face.get('tintindex', ''))
        ), (key, index, direction)
        if declared:
            rectangle = tuple(Fraction(v) for v in source_face['uv'])
            assert rectangle == vector(uv), (key, index, direction)
        else:
            assert not uv
            rectangle = default_uv(vector(a), vector(b), direction)
        extent = tuple(abs(end-start) for start,end in zip(vector(a), vector(b)))
        plane = {'up': (0,2), 'down': (0,2), 'east': (2,1), 'west': (2,1),
                 'north': (0,1), 'south': (0,1)}[direction]
        if rotation in (90,270):
            plane = plane[::-1]
        result[key,index,direction] = rectangle, declared, rotation, tuple(extent[i] for i in plane)
    return result, len(docs)


def png_frames(row, source, first):
    data = source(row['path'])
    algorithm = row['source_hash_kind']
    assert FIRST['hash_bytes'](data, algorithm) == row['source_sha']
    image, frame_count, _, _ = FIRST['decode_png'](data)
    assert frame_count == 1, row
    metadata = source(row['path']+'.mcmeta')
    if first:
        assert hashlib.sha256(image.tobytes()).hexdigest() == first['rgba8_sha256']
        assert (FIRST['hash_bytes'](metadata, algorithm) if metadata is not None else '') == first['mcmeta_sha']
    animation = json.loads(metadata).get('animation') if metadata is not None else None
    if animation is None:
        return [image], None
    assert not set(animation) - {'frametime', 'interpolate'}, animation
    width, height = image.size
    # All four actual sheets have one column of square frames and implicit row order.
    assert height % width == 0 and height > width, row
    frames = [image.crop((0, y, width, y+width)) for y in range(0, height, width)]
    return frames, animation


def measure_region(frames, uv):
    if uv[0] == uv[2] or uv[1] == uv[3]:
        return 'ZERO_UV_AREA', None, []
    if any(v < 0 or v > 16 for v in uv):
        return 'OUTSIDE_TEXTURE_UV', None, []
    box = FIRST['to_pixel_box'](uv, *frames[0].size)
    measured = []
    for frame in frames:
        crop = frame.crop(box)
        stats = FIRST['pixel_metrics'](crop)
        FIRST['verify_pixels'](crop, stats)
        assert sum(stats[:3]) == crop.width * crop.height
        measured.append((*stats, hashlib.sha256(crop.tobytes()).hexdigest()))
    return ('ANIMATED_FRAME_RECTS' if len(frames) > 1 else 'STATIC_RECT'), box, measured


def face_rows(db, faces, region_index, queue):
    for model,provider,index,side,slot,tid,cull,tint in db.execute('''
        SELECT f.model_key,f.provider_key,f.element_index,f.direction,f.slot,f.texture_id,
               d.cullface,d.tintindex
        FROM effective_face_texture f JOIN face d USING(provider_key,element_index,direction)
        ORDER BY f.model_key,f.provider_key,f.element_index,f.direction
    '''):
        uv, declared, rotation, extent = faces[provider,index,side]
        u_density = v_density = ''
        if tid is None:
            status = 'SLOT_UNBOUND'
        elif not queue[tid]['path']:
            status = 'MISSING_PINNED_PNG'
        else:
            status, width, height = region_index[tid,uv]
            u_density = abs(uv[2]-uv[0])*width/16/extent[0] if extent[0] else ''
            v_density = abs(uv[3]-uv[1])*height/16/extent[1] if extent[1] else ''
        yield (model,provider,index,side,slot,tid,'EXPLICIT' if declared else 'DEFAULT',
               packed(uv),rotation,int(uv[0]>uv[2]),int(uv[1]>uv[3]),cull,tint,status,u_density,v_density)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('af', 'hc', 'jars', 'out'):
        parser.add_argument('--'+name, required=True, type=Path)
    parser.add_argument('--faces', type=Path, help='Optional complete per-model CSV or CSV.xz')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    queue = {int(row['texture_id']): row for row in read_csv(PHASE / 'F/1-3_TEXTURE_UV_HANDOFF.csv')}
    first_png = {int(row['texture_id']): row for row in read_csv(ENTRY01/'1-4_PNG_PIXEL_LEDGER.csv.gz', True)}
    first_faces = read_csv(ENTRY01/'1-4_CHAIR_UV_LEDGER.csv.gz', True)

    with ExitStack() as stack:
        db = stack.enter_context(sqlite3.connect(':memory:'))
        db.deserialize(lzma.decompress((PHASE/'F/furniture_research.sqlite.xz').read_bytes()))
        providers = defaultdict(set)
        for source, path in db.execute('SELECT DISTINCT m.source_id,m.path FROM face f JOIN model m ON m.model_key=f.provider_key'):
            providers[source].add(path)
        for row in queue.values():
            if row['path'] and int(row['face_instances']):
                providers[row['source_id']].update((row['path'], row['path']+'.mcmeta'))
        pins = dict(db.execute('SELECT id,pin FROM source'))
        sources = {mod: FIRST['archived'](repo, pins[mod], providers[mod]).get
                   for mod, repo in (('AF', args.af), ('HC', args.hc))}
        jars = {}
        for source, filename, digest in (('MACAW','macaw.jar','sha256'), ('MC1.21.1','1.21.1.jar','sha1'),
                                         ('MC1.21.11','1.21.11.jar','sha1')):
            path = args.jars/filename
            assert hashlib.new(digest, path.read_bytes()).hexdigest() == pins[source]
            jar = jars[source] = stack.enter_context(zipfile.ZipFile(path))
            names = frozenset(jar.namelist())
            sources[source] = lambda name, archive=jar, keys=names: archive.read(name) if name in keys else None

        bytecode = verify_uv_1211(jars['MC1.21.1'])
        faces, provider_count = check_providers(db, sources)
        grouped = defaultdict(Counter)
        missing = Counter()
        unbound = Counter()
        methods = defaultdict(Counter)
        for provider,index,side,tid,resolution,n in db.execute('''
           SELECT provider_key,element_index,direction,texture_id,resolution,count(*)
           FROM effective_face_texture GROUP BY provider_key,element_index,direction,texture_id,resolution
        '''):
            uv, declared, rotation, _ = faces[provider,index,side]
            if tid is None:
                unbound[resolution] += n
                continue
            row = queue[tid]
            if not row['path']:
                missing[tid] += n
                continue
            grouped[tid][uv] += n
            methods[row['disposition']]['explicit' if declared else 'implicit'] += n
            methods[row['disposition']]['reversed'] += n * (uv[0] > uv[2] or uv[1] > uv[3])
            methods[row['disposition']]['rotated'] += n * (rotation != 0)
        assert sum(unbound.values()) == db.execute('SELECT sum(face_count) FROM model_slot WHERE texture_id is null').fetchone()[0]
        for tid,row in queue.items():
            assert sum(grouped.get(tid, {}).values()) + missing[tid] == int(row['face_instances']), row
        regions, summaries, animations, exceptions = [], [], [], []
        totals = defaultdict(Counter)
        region_index = {}
        first_face_match = {(int(r['texture_id']), vector(r['uv'])): r for r in first_faces}
        first_keys_matched = set()
        for tid, groups in sorted(grouped.items()):
            if not groups:
                continue
            row = queue[tid]
            frames, animation = png_frames(row, sources[row['source_id']], first_png.get(tid))
            if animation is not None:
                animations.append((tid,row['resource_id'],len(frames),*frames[0].size,
                                   animation.get('frametime',1),animation.get('interpolate',False)))
            statuses = Counter()
            for uv,n in sorted(groups.items()):
                status, box, samples = measure_region(frames, uv)
                statuses[status] += n
                region_index[tid,uv] = status, *frames[0].size
                key = tid, uv
                if key in first_face_match:
                    prior = first_face_match[key]
                    assert packed(box) == prior['pixel_box'] and len(samples) == 1
                    assert list(map(str, samples[0][:4])) == [prior[k] for k in ('transparent','partial_alpha','opaque','visible_rgb_colors')]
                    assert samples[0][-1] == prior['rgba8_sha256']
                    first_keys_matched.add(key)
                if not samples:
                    exceptions.append((tid, row['resource_id'], packed(uv), status, n))
                for frame, values in enumerate(samples):
                    regions.append((tid,packed(uv),packed(box),frame,n,*values))
            totals[row['disposition']].update(statuses)
            summaries.append((tid, row['resource_id'], row['disposition'], row['source_sha'],
                              *frames[0].size, len(frames), len(groups), sum(groups.values()),
                              *[statuses[key] for key in ('STATIC_RECT','ANIMATED_FRAME_RECTS','ZERO_UV_AREA','OUTSIDE_TEXTURE_UV')]))
        assert first_keys_matched == first_face_match.keys()
        assert len(first_faces) == 1794
        for tid,row in sorted(queue.items()):
            if row['disposition'] == 'SOURCE_EXCEPTION':
                reason = 'MISSING_PINNED_PNG' if missing[tid] else 'MISSING_PNG_WITHOUT_FACE'
                exceptions.append((tid, row['resource_id'], '', reason, missing[tid]))
        if args.faces:
            write_csv(args.faces, ('model_key','provider_key','element_index','direction','slot','texture_id',
                                  'uv_method','uv','uv_rotation','u_reversed','v_reversed','cullface','tintindex',
                                  'status','source_pixels_per_local_u','source_pixels_per_local_v'),
                      face_rows(db, faces, region_index, queue))

    region_columns = ('texture_id','uv','pixel_box','frame','face_instances_per_uv',
                      'transparent','partial_alpha','opaque','visible_rgb_colors','top4_visible_rgba_counts','rgba8_sha256')
    shard_size = 2800
    for offset in range(0, len(regions), shard_size):
        number = offset//shard_size+1
        write_csv(args.out/f'UV_REGIONS_{number:02}.csv.xz', region_columns, regions[offset:offset+shard_size])
    write_csv(args.out/'TEXTURE_UV_COUNTS.csv.xz',
              ('texture_id','resource_id','scope','source_sha','frame_width','frame_height','frame_count',
               'uv_regions','face_instances','static','animated','zero_uv','outside_uv'), summaries)
    write_csv(args.out/'UV_EXCEPTIONS.csv',
              ('texture_id','resource_id','uv','reason','face_instances'), exceptions)
    write_csv(args.out/'ANIMATION_FRAMES.csv',
              ('texture_id','resource_id','frame_count','frame_width','frame_height','declared_frametime','declared_interpolate'), animations)
    audit = {'provider_source_paths_verified': provider_count, 'provider_source_faces_verified': len(faces),
             'status_face_counts': dict(totals), 'uv_declarations_and_orientation': dict(methods),
             'bound_face_instances': sum(int(row['face_instances']) for row in queue.values()),
             'missing_png_textures': sum(row['disposition']=='SOURCE_EXCEPTION' for row in queue.values()),
             'missing_png_textures_with_faces': sum(n>0 for n in missing.values()),
             'missing_png_face_instances': sum(missing.values()),
             'unbound_faces': dict(unbound), 'texture_count_with_path_and_faces': len(summaries),
             'unique_sampled_uv_frame_rows': len(regions), 'exception_rows': len(exceptions),
             'entry01_distinct_texture_uv_pairs_reproduced': len(first_keys_matched),
             'entry01_face_rows': len(first_faces), 'default_uv_1_21_1_bytecode': bytecode}
    encoded = json.dumps(audit, indent=2, sort_keys=True)+'\n'
    (args.out/'ENTRY02_AUDIT.json').write_text(encoded, encoding='utf-8')
    print(encoded)


if __name__ == '__main__':
    main()
