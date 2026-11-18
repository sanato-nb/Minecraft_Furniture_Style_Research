"""Write a vanilla 1.21.11 datapack with one fixture per directly selectable E model."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

DATA = Path('research/vanilla_models')
E_LEDGER = DATA / 'phase_1-2-E/entry4/E_RENDER_EXCEPTIONS_86.csv'
D_RULES = DATA / 'phase_1-2-D'
SLOTS_PER_VIEW = 7


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def get_cases():
    choices = defaultdict(set)
    for path in sorted(D_RULES.glob('entry*/*RULES.csv')):
        for row in read_csv(path):
            if 'model_path' not in row:
                continue
            block = row.get('block') or Path(row['blockstate_path']).stem
            variant = row.get('variant_key', '')
            choices[row['model_path']].add((block, variant))
    cases = []
    for index, row in enumerate(read_csv(E_LEDGER)):
        path = row['model_path']
        name = Path(path).stem
        candidates = choices[path]
        defaults = {'banner': 'white_banner', 'bed': 'red_bed', 'water': 'water'}
        selected = defaults.get(name, name)
        if candidates:
            block, variant = min(candidates, key=lambda pair: (pair[0] != selected, pair))
            state = f'minecraft:{block}' + (f'[{variant}]' if variant else '')
        else:
            state = ''
        cases.append(dict(model=name, model_sha=row['model_sha'], state=state,
                          scene=index//SLOTS_PER_VIEW, x=(index%SLOTS_PER_VIEW-3)*2,
                          y=120, z=12+index//SLOTS_PER_VIEW*12))
    return cases


def scene_setup(cases):
    commands = [
        'time set noon', 'weather clear', 'forceload add -16 0 16 180',
    ]
    for z in sorted({case['z'] for case in cases}):
        commands.extend([
            f'fill -9 119 {z-2} 9 119 {z+2} minecraft:smooth_stone',
            f'fill -9 120 {z+3} 9 123 {z+3} minecraft:light_gray_concrete',
        ])
    return commands


def setup_case(case):
    name, state, x, y, z = (case[key] for key in ('model','state','x','y','z'))
    if not state:
        return []
    if name == 'moving_piston':
        return [
            f'setblock {x} {y} {z+1} minecraft:piston[facing=north]',
            f'setblock {x} {y} {z+2} minecraft:air',
        ]
    steps = []
    if name.endswith('_hanging_sign'):
        steps.append(f'setblock {x} {y+1} {z} minecraft:smooth_stone')
    if name == 'bed':
        state = 'minecraft:red_bed[facing=south,part=foot]'
        steps.append(f'setblock {x} {y} {z+1} minecraft:red_bed[facing=south,part=head] strict')
    if name in ('water','lava'):
        for nx, nz in ((x-1,z),(x+1,z),(x,z-1),(x,z+1)):
            steps.append(f'setblock {nx} {y} {nz} minecraft:glass')
    if name.startswith('pitcher_crop_top_stage_'):
        age = name[-1]
        steps.extend([
            f'setblock {x} {y-2} {z} minecraft:dirt',
            f'setblock {x} {y-1} {z} minecraft:farmland',
            f'setblock {x} {y} {z} minecraft:pitcher_crop[age={age},half=lower] strict',
        ])
        y += 1
        case['y'] = y
    case['state'] = state
    return [*steps, f'setblock {x} {y} {z} {state} strict']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    args = parser.parse_args()
    cases = get_cases()
    assert len(cases) == 86 and sum(bool(row['state']) for row in cases) == 84
    funcs = args.pack / 'data/render_audit/function'
    funcs.mkdir(parents=True, exist_ok=True)
    (args.pack/'pack.mcmeta').write_text(json.dumps({
        'pack': {'description':'Vanilla E render audit fixture',
                 'min_format':[94,1], 'max_format':[94,1]}
    }) + '\n')
    (funcs/'platforms.mcfunction').write_text('\n'.join(scene_setup(cases))+'\n')
    setup = [line for case in cases for line in setup_case(case)]
    (funcs/'place.mcfunction').write_text('\n'.join([*setup,'say EF_FIXTURE_PLACED'])+'\n')
    verify = [f"execute if block {r['x']} {r['y']} {r['z']} {r['state']} run say EF_MATCH_{r['model']}"
              for r in cases if r['state']]
    (funcs/'verify.mcfunction').write_text('\n'.join([*verify,'say EF_FIXTURE_READBACK_END'])+'\n')
    with args.plan.open('w',encoding='utf-8',newline='') as stream:
        writer = csv.DictWriter(stream, cases[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(cases)


if __name__ == '__main__':
    main()
