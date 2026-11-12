#!/usr/bin/env python3
"""Verify v14 cross-record binding audit without copying copyrighted assets."""
from collections import Counter
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/furniture_mods'

def csv_rows(rel):
    with (BASE / rel).open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))

leaves = csv_rows('v12/handcrafted_generated_leaf_sample_16.csv')
manifest = {r['name']: r for r in csv_rows('v12/handcrafted_png_header_12.csv')}
pixels = {r['name']: r for r in csv_rows('v13/handcrafted_png_12_pixel_metrics.csv')}
uv = {'handcrafted:block/' + r['model'] for r in csv_rows('v13/uv_to_pixel_alignment_13_models.csv') if r['mod'] == 'Handcrafted'}
outputs = csv_rows('v14/handcrafted_texture_bindings_51.csv')
cover = csv_rows('v14/handcrafted_leaf_coverage_16.csv')
unsampled = csv_rows('v14/unsampled_mod_png_priority_12.csv')
summary = json.loads((BASE / 'v14/v14_binding_audit_summary.json').read_text(encoding='utf-8'))
assert len(leaves) == len(cover) == 16 and len(outputs) == 51 and len(unsampled) == 12
expected = {}
for l in leaves:
    mapping = json.loads(l['textures'])
    assert len(mapping) == int(l['texture_slots'])
    for slot, ref in mapping.items():
        expected[(l['name'], slot)] = (ref, l)
assert len(expected) == len(outputs)
statuses = Counter()
missing = Counter()
for o in outputs:
    ref, source = expected[(o['leaf'], o['slot'])]
    assert o['texture_reference'] == ref
    assert o['model_git_blob_sha'] == source['git_blob_sha']
    assert o['parent'] == source['parent']
    assert int(o['parent_in_v13_uv_sample']) == int(source['parent'] in uv)
    if ref.startswith('handcrafted:block/'):
        name = ref[len('handcrafted:block/'):]
        m, p = manifest.get(name), pixels.get(name)
        if m and p:
            assert m['git_blob_sha'] == p['sha'] == o['png_manifest_git_sha'] == o['v13_pixel_git_sha']
            assert (m['width'], m['height']) == (p['width'], p['height'])
            expected_status = 'v13_png_sample_hash_matched'
        else:
            missing[name] += 1
            expected_status = 'mod_png_not_in_v13_sample'
    elif ref.startswith('minecraft:block/'):
        expected_status = 'vanilla_asset_not_checked_v14'
    else:
        expected_status = 'reference_unrecognized'
    assert o['status'] == expected_status
    statuses[expected_status] += 1
assert statuses == Counter({'v13_png_sample_hash_matched': 19, 'mod_png_not_in_v13_sample': 16, 'vanilla_asset_not_checked_v14': 16})
assert len(missing) == 12
assert {r['png']: int(r['referenced_by_bindings']) for r in unsampled} == dict(missing)
assert sum(int(r['all_mod_slots_sampled']) for r in cover) == 7
assert sum(int(r['v13_png_sampled_mod_slots']) > 0 for r in cover) == 13
assert sum(int(r['uv_parent_in_v13_sample']) for r in cover) == 9
assert (summary['texture_slot_bindings'], summary['mod_v13_png_sha_matched_bindings'], summary['unsampled_mod_distinct_png']) == (51, 19, 12)
assert summary['face_to_png_coordinate_verified'] is False
print('v14 binding audit verified: 16 leaves, 51 slots, 19 sampled PNG references, 12 unsampled PNG names')
