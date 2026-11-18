"""Summarize the controlled C/D game runs and compare chair screenshots."""
import argparse
import csv
import json
import re
from pathlib import Path

from PIL import Image, ImageChops


def csv_table(path, fields, rows):
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(fields)
        writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    heights, states, items, excerpts=[], [], [], []
    for v in ('1.21.1','1.21.11'):
        material=(args.runtime/v/'client.log').read_text(encoding='utf-8')
        excerpts.append('=== Minecraft '+v+' ===')
        for line in material.splitlines():
            if 'Server thread/INFO' in line:
                if match:=re.search(r' CD_STATE_(\w+)=([a-z0-9_,]+)$',line):
                    states.append((v,*match.groups()))
                    excerpts.append(line)
                elif match:=re.search(r' CD_ITEM_([a-z0-9_:]+)$',line):
                    items.append((v,match[1]))
                    excerpts.append(line)
            elif 'Render thread/INFO' in line:
                if match:=re.search(r' CD_HEIGHT_(\w+)=(\d+)$',line):
                    heights.append((v,match[1],match[2],f'{int(match[2])/1000-120:.3f}'))
                    excerpts.append(line)
                elif "Unknown block type 'another_furniture:unused/white_awning'" in line:
                    excerpts.append(line)
    with (args.output/'C_EXCEPTION_RECHECK.csv').open(encoding='utf-8',newline='') as stream:
        required={r['model'].replace(':item/',':') for r in csv.DictReader(stream) if r['status']=='GENERATED_ITEM_RUNTIME'}
    assert len(items)==58 and {item for _,item in items}==required
    assert len(heights)==18 and len({label for _,label,*_ in heights})==18
    assert all(y==('120000' if label.endswith('_air') else '121000')
               for _,label,y,_ in heights if label.endswith(('_air','_stone')))
    assert ('1.21.1','hc_bed_click','foot,south') in states and ('1.21.1','hc_bed_south','head,south') in states
    for material in ('birch','spruce'):
        assert {value for _,label,value in states if label=='af_'+material}=={'1','2','3'}
    assert any('Unknown block type' in line for line in excerpts)
    state_rows=list(dict.fromkeys(states))
    assert sum('macaw_matrix_' in label for _,label,_ in state_rows)==16

    box=(110,285,1165,660)
    def chair_image(variant):
        with Image.open(args.runtime/'1.21.1'/f'chair_v{variant}.png') as image:
            return image.crop(box).convert('RGB')
    base=chair_image(1)
    changes={}
    for variant in (2,3):
        diff=ImageChops.difference(base,chair_image(variant))
        changes[variant]=sum(pixel!=(0,0,0) for pixel in diff.get_flattened_data())
    assert changes[2]>0 and changes[3]==0
    csv_table(args.output/'D_OBSERVED_STATES.csv',('minecraft','test','selected_property_values'),state_rows)
    csv_table(args.output/'D_COLLISION_PROBES.csv',('minecraft','sample','armor_stand_y_milliblocks','height_above_floor'),heights)
    csv_table(args.output/'C_ITEM_DISPLAY_READBACK.csv',('minecraft','item_id'),items)
    (args.output/'RUNTIME_LOG_EXCERPT.txt').write_text('\n'.join(excerpts)+'\n',encoding='utf-8')
    summary=dict(item_displays=len(items),distinct_state_observations=len(state_rows),
                 collision_samples=len(heights)-6,collision_controls=6,
                 chair_compare_region=box,chair_different_pixels=changes)
    (args.output/'RUNTIME_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
