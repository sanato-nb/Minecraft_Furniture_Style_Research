"""Independently audit scope membership, source joins and key cross-category observations."""
from collections import Counter, defaultdict
import csv
import hashlib
import json
import lzma
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=HERE.parent/'B'


def read(path):
    opener=lzma.open if path.suffix=='.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def main():
    result=json.loads((HERE/'C_AUDIT.json').read_bytes())
    assert all(hashlib.sha256((B/path).read_bytes()).hexdigest()==digest
               for path,digest in result['input_sha256'].items())
    findings=read(HERE/'CROSS_CATEGORY_FINDINGS.csv')
    coverage=read(HERE/'CATEGORY_COVERAGE.csv')
    cases={r['case']:r for r in read(B/'CASES.csv')}
    case_maps={r['category']:set(r['vanilla_cases'].split('|')+r['mod_cases'].split('|')) for r in coverage}
    assert len(case_maps)==len(coverage)==9
    assert all(members=={i for i,r in cases.items() if category in r['category'].split('|')}
               for category,members in case_maps.items())
    assert len(findings)==len({r['finding_id'] for r in findings})==21
    classes=Counter(r['classification'] for r in findings)
    assert classes==result['classifications']
    for row in findings:
        ids=set(row['cases'].split('|'))
        assert ids<=case_maps[row['category']]
        assert set(row['cohorts'].split('|'))=={cases[i]['cohort'] for i in ids}
        assert json.loads(row['measurement'])
    for row in coverage:
        assert set(row['findings'].split('|'))=={r['finding_id'] for r in findings if r['category']==row['category']}

    faces=defaultdict(list)
    for row in read(B/'FACES.csv.xz'):
        faces[row['case']].append(row)
    for closed,opened in (('V05','V06'),('S20','S21')):
        assert cases[closed]['bbox']==cases[opened]['bbox']
        for field,common in (('rgba_sha256',5),('resource_id',5),('uv',6)):
            assert sum((Counter(r[field] for r in faces[closed]) &
                        Counter(r[field] for r in faces[opened])).values())==common
    bookshelf=[{r['png_sha'] for r in faces[i] if r['resource_id']=='minecraft:block/bookshelf'}
               for i in ('V07','S28')]
    assert len(bookshelf[0])==1 and bookshelf[0]==bookshelf[1]
    for empty,full in (('V12','V13'),('S42','S43')):
        assert int(cases[full]['elements'])==int(cases[empty]['elements'])+1
        assert len(faces[full])==len(faces[empty])+1
        water=[r for r in faces[full] if r['status']=='ANIMATED_FRAME_RECTS']
        assert len(water)==1 and water[0]['direction']=='up'
        assert not any(r['status']=='ANIMATED_FRAME_RECTS' for r in faces[empty])
    assert not faces['V11'] and cases['V11']['bbox']==''
    print(json.dumps(dict(status='PASS',findings=len(findings),categories=len(coverage),cases=len(cases),
                          independently_cross_checked_axes=['opening_surface','bookshelf_png','water_surface','bed_boundary']),
                     indent=2,sort_keys=True))


if __name__=='__main__':
    main()
