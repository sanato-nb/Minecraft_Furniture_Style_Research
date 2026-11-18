"""Summarize the vanilla client fixture log and selected screenshot comparisons."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops

INVISIBLE = {'air', 'barrier', 'structure_void'}


def visual_status(name, state):
    if not state:
        return 'NOT_APPLICABLE_UNSELECTED_TEMPLATE'
    if name.startswith('pitcher_crop_top_stage_'):
        return 'UPPER_STATE_PRESENT_NO_SEPARATE_SURFACE'
    if re.fullmatch(r'light_[0-9]{2}', name) or name in INVISIBLE:
        return 'STATE_PRESENT_NO_VISIBLE_SURFACE_IN_SPECTATOR'
    return 'VISIBLE_IN_VANILLA_CLIENT'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--captures', type=Path, required=True)
    args = parser.parse_args()
    out = args.output
    shots = args.captures
    data = args.log.read_text(encoding='utf-8')
    lines = [line for line in data.splitlines() if '[Server thread/INFO]' in line
             and re.search(r'EF_MATCH_|EF_FIXTURE_|Teleported RenderAudit|Changed the block at [246], 121, 132|Stepping 1 tick|game is frozen|game is running normally', line)]
    matches = {}
    for line in lines:
        match = re.search(r'\[([0-9:]+)\].* EF_MATCH_([a-z0-9_]+)$', line)
        if match:
            matches.setdefault(match[2], match[1])
    with (out/'E_FIXTURE_PLAN_86.csv').open(encoding='utf-8', newline='') as stream:
        cases = list(csv.DictReader(stream))
    if len(cases) != 86 or set(matches) != {row['model'] for row in cases if row['state']}:
        raise ValueError('Placement readback did not account for all selectable models')
    for row in cases:
        scene = int(row['scene'])
        first = scene//3*3
        last = min(first+2,12)
        name = row['model']
        row.update(state_readback=matches.get(name,''),
                   screenshot=(f'evidence/scenes_{first:02d}-{last:02d}.jpg' if name != 'moving_piston'
                               else 'evidence/piston_ticks.jpg'),
                   outcome=visual_status(name, row['state']))
    with (out/'E_RUNTIME_OUTCOMES_86.csv').open('w',encoding='utf-8',newline='') as stream:
        csv_writer = csv.DictWriter(stream,cases[0].keys(),lineterminator='\n')
        csv_writer.writeheader()
        csv_writer.writerows(cases)
    box = (70,300,1200,570)
    with Image.open(shots/'crop_upper_present.png') as a, Image.open(shots/'crop_upper_removed.png') as b:
        region_a = a.convert('RGB').crop(box)
        region_b = b.convert('RGB').crop(box)
        if ImageChops.difference(region_a, region_b).getbbox() is not None:
            raise ValueError('The pitcher crop control region differed')
    (out/'E_RUNTIME_LOG_EXCERPT.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hashes = {img.name: hashlib.sha256(img.read_bytes()).hexdigest()
              for img in sorted((out/'evidence').glob('*.jpg'))}
    summary = {
        'minecraft_version':'1.21.11',
        'client_jar_sha1':'ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd',
        'client_profile':'vanilla resources, offline singleplayer, spectator test camera',
        'render_backend':'Mesa llvmpipe OpenGL 4.5 (software)',
        'fixed_models':len(cases),'confirmed_runtime_states':len(matches),
        'observations':Counter(row['outcome'] for row in cases),
        'pitcher_crop_control':{'removed_upper_states':[0,1,2],
                                'pixel_region_xyxy':box,'different_rgb_pixels':0,
                                'region_sha256':hashlib.sha256(region_a.tobytes()).hexdigest()},
        'screenshot_evidence_sha256':hashes,
    }
    (out/'E_RUNTIME_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
