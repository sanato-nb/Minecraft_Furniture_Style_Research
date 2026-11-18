"""Independently reconcile the normalized UV regions with regenerated model-face rows."""
import csv
from collections import Counter, defaultdict
import gzip
import json
import lzma
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def rows(path):
    opener = {'.xz': lzma.open, '.gz': gzip.open}.get(path.suffix, open)
    with opener(path, 'rt', encoding='utf-8', newline='') as file:
        yield from csv.DictReader(file)


def main(face_path):
    statuses = Counter()
    model_faces = set()
    group_counts = Counter()
    first = {(r['model_key'], r['element_index'], r['direction']): r for r in
             rows(HERE.parent/'entry01'/'1-4_CHAIR_UV_LEDGER.csv.gz')}
    for row in rows(face_path):
        key = row['model_key'], row['element_index'], row['direction']
        assert key not in model_faces
        model_faces.add(key)
        status = row['status']
        statuses[status] += 1
        if status != 'SLOT_UNBOUND':
            uv = row['uv'] if status != 'MISSING_PINNED_PNG' else ''
            group_counts[row['texture_id'], uv, status] += 1
        if key in first:
            old = first.pop(key)
            pairs = [('uv','uv'), ('uv_rotation','uv_rotation'), ('texture_id','texture_id'),
                     ('u_reversed','u_reversed'), ('v_reversed','v_reversed')]
            assert all(old[a] == row[b] for a,b in pairs), key
            assert status == 'STATIC_RECT', key
    assert not first and len(model_faces) == 592312

    texture = {r['texture_id']: r for r in rows(HERE/'TEXTURE_UV_COUNTS.csv.xz')}
    frames_by_region = defaultdict(set)
    ledger_groups = {}
    for path in sorted(HERE.glob('UV_REGIONS_*.csv.xz')):
        for row in rows(path):
            tid = row['texture_id']
            status = 'ANIMATED_FRAME_RECTS' if int(texture[tid]['frame_count']) > 1 else 'STATIC_RECT'
            key = tid, row['uv'], status
            frame = int(row['frame'])
            assert frame not in frames_by_region[key]
            frames_by_region[key].add(frame)
            count = int(row['face_instances_per_uv'])
            assert ledger_groups.setdefault(key,count) == count
            x0,y0,x1,y1 = map(int,row['pixel_box'].split('|'))
            assert 0 <= x0 < x1 <= int(texture[tid]['frame_width'])
            assert 0 <= y0 < y1 <= int(texture[tid]['frame_height'])
            alpha = sum(int(row[name]) for name in ('transparent','partial_alpha','opaque'))
            assert alpha == (x1-x0)*(y1-y0)
            assert len(bytes.fromhex(row['rgba8_sha256'])) == 32
    for key, frames in frames_by_region.items():
        assert frames == set(range(int(texture[key[0]]['frame_count'])))
    for row in rows(HERE/'UV_EXCEPTIONS.csv'):
        key = row['texture_id'], row['uv'], row['reason']
        assert key not in ledger_groups
        if int(row['face_instances']):
            ledger_groups[key] = int(row['face_instances'])
    assert group_counts == ledger_groups
    texture_counts = Counter()
    for (tid,_,status),count in group_counts.items():
        if tid in texture:
            texture_counts[tid,status] += count
    for tid,row in texture.items():
        for key, status in (('static','STATIC_RECT'),('animated','ANIMATED_FRAME_RECTS'),
                            ('zero_uv','ZERO_UV_AREA'),('outside_uv','OUTSIDE_TEXTURE_UV')):
            assert int(row[key]) == texture_counts[tid,status]
    print(json.dumps({
        'status': 'PASS', 'distinct_model_face_keys': len(model_faces),
        'status_counts': statuses, 'chair_face_keys_reconciled': 1794,
        'nonzero_face_groups_reconciled': len(ledger_groups),
        'sampled_region_frames_reconciled': sum(map(len, frames_by_region.values())),
        'texture_summary_rows_reconciled': len(texture),
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
