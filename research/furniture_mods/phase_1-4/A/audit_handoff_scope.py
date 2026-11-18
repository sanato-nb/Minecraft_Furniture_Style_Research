"""Reconcile the frozen 1-3 texture handoff against its database and prior evidence."""
from collections import Counter
import csv
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[4]
INPUT = ROOT / 'research/furniture_mods/phase_1-3/F'
PRIOR_COLUMNS = {
    'another_texture_53_png_source_manifest.csv': ('texture', 'sha', ''),
    'another_new_14_png_unique_source_metrics.csv': ('texture', 'source_sha', ''),
    'shutter_43_png_original_source_manifest.csv': ('texture', 'source_git_sha', 'newly_sampled'),
    'new_42_png_first_measured_in_v23.csv': ('texture', 'git_sha', ''),
    'handcrafted_png_12_pixel_metrics.csv': ('name', 'sha', ''),
    'handcrafted_12_new_png_pixel_metrics.csv': ('name', 'upstream_blob_sha', ''),
}


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def main():
    ledger = rows(INPUT / '1-3_TEXTURE_UV_HANDOFF.csv')
    by_id = {int(r['texture_id']): r for r in ledger}
    by_resource = {(r['resource_id'], r['minecraft']): r for r in ledger}
    assert len(by_id) == len(by_resource) == len(ledger) == 2256

    expected_prior = {}
    totals = Counter()
    evidence = rows(INPUT / 'F_PRIOR_RGBA_LEDGER.csv')
    for report in evidence:
        path = ROOT / report['ledger_path']
        sha = git_blob(path)
        assert sha == report['ledger_blob_sha'], path
        raw = rows(path)
        unit = report['evidence_unit']
        if unit == 'PNG':
            resource, hash_field, flag = PRIOR_COLUMNS[path.name]
            selected = [(line, row) for line, row in enumerate(raw, 2) if not flag or row[flag] == '1']
            for line, row in selected:
                texture = row[resource]
                if report['mod'] == 'HC':
                    texture = 'handcrafted:block/' + texture
                assert texture not in expected_prior, texture
                expected_prior[texture] = (report['ledger_path'], sha, str(line), row[hash_field])
            count = len(selected)
        else:
            assert unit == 'FACE_RGBA'
            count = len(raw)
        assert count == int(report['rows_recounted']), path
        totals[unit] += count
    assert totals == {'PNG': 175, 'FACE_RGBA': 4113}

    with sqlite3.connect(':memory:') as db:
        db.deserialize(lzma.decompress((INPUT / 'furniture_research.sqlite.xz').read_bytes()))
        assert db.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
        assert db.execute('PRAGMA foreign_key_check').fetchall() == []
        counts = {tid: (faces, unused) for tid, faces, unused in db.execute(
            'SELECT texture_id, sum(face_count), sum(face_count=0) FROM model_slot GROUP BY texture_id'
        )}
        textures = db.execute(
            'SELECT id, resource_id, minecraft, source_id, texture_status, path, sha FROM texture'
        ).fetchall()
    assert {row[0] for row in textures} == set(by_id)
    groups = Counter()
    source_totals = Counter()
    candidate_faces = 0
    for tid, resource, version, source, status, path, sha in textures:
        row = by_id[tid]
        fields = ('resource_id', 'minecraft', 'source_id', 'texture_status', 'path', 'source_sha')
        assert tuple(row[field] for field in fields) == (
            resource, version, source or '', status, path or '', sha or ''
        ), tid
        faces, unused = counts.get(tid, (0, 0))
        assert (faces, unused) == (int(row['face_instances']), int(row['non_face_slot_count'])), tid
        prior = expected_prior.get(resource) if version == '1.21.1' else None
        if prior:
            assert prior == (row['previous_ledger'], row['previous_ledger_blob_sha'],
                             row['previous_ledger_line'], sha), tid
            group = 'PRIOR_RGBA_SHA_MATCH'
        elif not path or not sha:
            assert not path and not sha
            group = 'SOURCE_EXCEPTION'
        elif faces:
            group = 'PNG_UV_CANDIDATE'
            source_totals[source] += 1
            candidate_faces += faces
        else:
            assert unused > 0
            group = 'DECLARED_SLOT_ONLY'
        assert row['disposition'] == group, tid
        groups[group] += 1
    assert groups == {'PNG_UV_CANDIDATE': 1996, 'PRIOR_RGBA_SHA_MATCH': 175,
                      'DECLARED_SLOT_ONLY': 77, 'SOURCE_EXCEPTION': 8}
    assert source_totals == {'AF': 1036, 'HC': 885, 'MACAW': 18, 'MC1.21.1': 15, 'MC1.21.11': 42}

    chair = rows(INPUT / 'F_V24_CHAIR_PNG.csv')
    assert len(chair) == len({row['resource_id'] for row in chair}) == 24
    chair_groups = Counter()
    for row in chair:
        item = by_resource[row['resource_id'], '1.21.1']
        assert (item['path'], item['source_sha'], item['priority']) == (
            row['pinned_path'], row['source_sha'], 'V24_CHAIR'
        )
        expected = {'QUEUE_1_4': 'PNG_UV_CANDIDATE', 'REFERENCE_PRIOR_RGBA': 'PRIOR_RGBA_SHA_MATCH'}
        assert item['disposition'] == expected[row['disposition']]
        chair_groups[row['disposition']] += 1
    assert chair_groups == {'QUEUE_1_4': 19, 'REFERENCE_PRIOR_RGBA': 5}

    print(json.dumps({
        'status': 'PASS',
        'texture_id_version_pairs': len(ledger),
        'handoff_dispositions': dict(sorted(groups.items())),
        'new_candidate_source_counts': dict(sorted(source_totals.items())),
        'new_candidate_static_face_instances': candidate_faces,
        'prior_evidence_ledger_blobs_verified': len(evidence),
        'prior_evidence_rows': dict(sorted(totals.items())),
        'v24_chair_texture_dispositions': dict(sorted(chair_groups.items())),
        'input_blobs': {name: git_blob(INPUT / name) for name in (
            '1-3_TEXTURE_UV_HANDOFF.csv', 'F_PRIOR_RGBA_LEDGER.csv',
            'F_V24_CHAIR_PNG.csv', 'furniture_research.sqlite.xz'
        )},
    }, indent=2))


if __name__ == '__main__':
    main()
