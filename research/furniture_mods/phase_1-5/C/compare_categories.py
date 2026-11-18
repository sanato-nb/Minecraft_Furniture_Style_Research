"""Classify source-backed comparisons for the nine frozen furniture categories."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import hashlib
import json
import lzma
from pathlib import Path

HERE=Path(__file__).resolve().parent
B=HERE.parent/'B'
VANILLA='VANILLA_SHARED'
MULTI='MULTI_MOD_SHARED'
SPECIFIC='MOD_SPECIFIC'
LIMIT='UNVERIFIED_OR_COUNTEREXAMPLE'
APP=('case','rule_index','option_index')


def read(path):
    opener=lzma.open if path.suffix=='.xz' else open
    with opener(path,'rt',encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def write(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def group(rows):
    result=defaultdict(list)
    for r in rows:
        result[r['case']].append(r)
    return result


def keyed(row,columns):
    return tuple(row[c] for c in columns)


def main(out):
    case_rows=read(B/'CASES.csv')
    cases={r['case']:r for r in case_rows}
    face_rows=read(B/'FACES.csv.xz')
    element_rows=read(B/'ELEMENTS.csv')
    app_rows=read(B/'APPLICATIONS.csv')
    faces,elements,apps=map(group,(face_rows,element_rows,app_rows))
    element_key=APP+('element_index',)
    by_element={keyed(r,element_key):r for r in element_rows}
    assert len(by_element)==390 and len(cases)==62 and len(face_rows)==1844 and len(app_rows)==74
    assert len({keyed(r,element_key+('direction',)) for r in face_rows})==1844
    claims=[]

    def counts(*ids):
        return {i:{k:int(cases[i][k]) for k in ('applications','elements','faces','zero_thickness_elements',
                                               'faces_measured','faces_at_density_1x1')} for i in ids}

    def spans(*ids):
        return {i:cases[i]['span_blocks'] for i in ids}

    def resource_set(case):
        return {r['resource_id'] for r in faces[case]}

    def panel_diff(a,b):
        # All callers compare one application per case. Ordinal keys are meaningful for these matched models.
        assert len(apps[a])==len(apps[b])==1
        assert [r['local_size'] for r in elements[a]]==[r['local_size'] for r in elements[b]]
        local=('element_index','direction')
        old={keyed(r,local):r for r in faces[a]}
        new={keyed(r,local):r for r in faces[b]}
        assert len(old)==len(faces[a]) and len(new)==len(faces[b]) and old.keys()==new.keys()
        outcome={}
        for field in ('resource_id','uv','rgba_sha256'):
            outcome[field]=['/'.join(k) for k in sorted(old) if old[k][field]!=new[k][field]]
        return outcome

    def face_multiset(case):
        return Counter((by_element[keyed(r,element_key)]['assembly_bbox'],
                        *keyed(r,('direction','resource_id','uv','uv_rotation','cullface','tintindex','status','rgba_sha256')))
                       for r in faces[case])

    def compare_surfaces(a,b):
        x,y=face_multiset(a),face_multiset(b)
        return {'unchanged':sum((x&y).values()),'removed':sum((x-y).values()),'added':sum((y-x).values())}

    def add(category,tag,axis,ids,measurement,claim,limit):
        assert len(ids)==len(set(ids)) and all(category in cases[i]['category'].split('|') for i in ids)
        cohorts={cases[i]['cohort'] for i in ids}
        if tag==VANILLA:
            assert 'VANILLA' in cohorts and len(cohorts)>=2
        elif tag==MULTI:
            assert len(cohorts)>=2 and 'VANILLA' not in cohorts
        elif tag==SPECIFIC:
            assert len(cohorts)==1 and 'VANILLA' not in cohorts
        else:
            assert tag==LIMIT
        claims.append(dict(finding_id=f'C{len(claims)+1:02}',category=category,classification=tag,axis=axis,
                           cases='|'.join(ids),cohorts='|'.join(sorted(cohorts)),
                           measurement=json.dumps(measurement,sort_keys=True,ensure_ascii=False),
                           observation=claim,scope_limit=limit))

    category='SEATING_CHAIR'
    ids=('V01','S01','S06','S08')
    assert [len(elements[i]) for i in ids]==[2,10,13,12]
    assert [tuple(map(Fraction,cases[i]['span_blocks'].split('|')))[1]>1 for i in ids]==[False,False,True,True]
    add(category,LIMIT,'STAIR_ANALOGUE_HEIGHT',ids,spans(*ids),
        '오크 계단과 AF 의자는 높이 1블록이며 HC와 Macaw 오크 의자는 1블록을 넘는다.',
        '계단은 단차 외형 대조군이며 착석 기능·좌판 구조의 등가 근거는 없다.')
    diff=panel_diff('S01','S02')
    assert not any(diff.values()) and cases['S01']['bbox']!=cases['S02']['bbox']
    add(category,SPECIFIC,'TUCKED_GEOMETRY',('S01','S02'),dict(changed_faces=diff,bounds={i:cases[i]['bbox'] for i in ('S01','S02')}),
        'AF 오크 의자는 넣은 상태에서 경계가 Z축 방향으로 이동하며 46면의 PNG·UV·화소가 유지된다.',
        '선택한 오크 의자의 두 상태에 한정한다.')
    diff=panel_diff('S06','S07')
    assert len(diff['resource_id'])==len(diff['rgba_sha256'])==6 and not diff['uv']
    assert all(x.startswith('12/') for x in diff['rgba_sha256'])
    add(category,SPECIFIC,'CUSHION_SLOT',('S06','S07'),diff,
        'HC 오크 의자의 쿠션 설정은 동일 UV에서 요소 12의 여섯 면만 PNG와 화소를 교체한다.',
        '영면적이거나 가려진 면의 게임 내 표시는 별도 확인이 필요하다.')

    category='SMALL_TABLE'
    ids=('V02','S12','S13')
    assert spans(*ids)=={'V02':'1|0.5|1','S12':'1|1|1','S13':'1|0.125|1'}
    assert len(elements['V02'])==len(elements['S13'])==1
    add(category,VANILLA,'SLAB_COMPONENT',ids,spans(*ids),
        '하단 반 블록과 다리 없는 Macaw 커피 테이블 중앙형은 양쪽 모두 폭과 깊이가 1블록인 단일 판재다.',
        '높이는 0.5와 0.125블록으로 다르며 적용 구조의 비교다.')
    ids=('S10','S11','S12','S13')
    alpha=sum(r['pixels']!='' and r['alpha_zero']==r['pixels'] for r in faces['S10'])
    assert alpha==11 and int(cases['S10']['zero_thickness_elements'])==5 and resource_set('S12')==resource_set('S13')
    add(category,LIMIT,'OVERLAY_AND_CONNECTION',ids,dict(samples=counts(*ids),hc_fully_transparent_faces=alpha),
        'HC 사이드 테이블의 완전 투명 실측 면은 11개다. Macaw 커피 테이블은 한 상태에서 다리가 빠져 요소가 2→1로 바뀐다.',
        '영면적 UV와 완전 투명 실측 면은 다른 판정이며 HC·Macaw 전체 제품군으로 일반화하지 않는다.')

    category='LARGE_TABLE'
    pairs=(('S14','S15'),('S16','S17'),('S18','S19'))
    ids=tuple(i for pair in pairs for i in pair)
    heights={b:max(Fraction(r['local_size'].split('|')[1]) for r in elements[b])/16 for _,b in pairs}
    assert list(heights.values())==[Fraction(3,16),Fraction(1,4),Fraction(5,16)]
    assert all(len(elements[a])>len(elements[b]) for a,b in pairs)
    add(category,MULTI,'CONNECTED_TABLE_TOP',ids,dict(samples=counts(*ids),
        connected_positive_y_blocks={k:str(v) for k,v in heights.items()}),
        '세 모드의 대표 오크 테이블에서 지지 요소가 줄어드는 상태를 확인했다. 대응 상판 높이는 3/16, 4/16, 5/16블록이다.',
        '연결 속성의 이름과 조립 조건은 모드별로 다르다.')
    ids=('V03','V04','S14','S15')
    assert len(apps['V03'])==2 and len(apps['S14'])==5 and len(apps['S15'])==1
    add(category,VANILLA,'MULTIPART_AND_THIN_PART',ids,dict(samples=counts(*ids),spans=spans('V04','S15')),
        '오크 울타리와 AF 테이블의 선택 상태가 기본 모델과 조건부 부품을 조립한다. 압력판은 별도의 두께 대조군이다.',
        '울타리의 기둥·연결부와 테이블 상판·다리의 기능은 다르다.')

    category='STORAGE'
    left,right=panel_diff('V05','V06'),panel_diff('S20','S21')
    assert left=={'resource_id':['0/up'],'uv':[],'rgba_sha256':['0/up']}
    assert right=={'resource_id':['0/north'],'uv':[],'rgba_sha256':['0/north']}
    assert all(cases[a]['bbox']==cases[b]['bbox'] for a,b in (('V05','V06'),('S20','S21')))
    add(category,VANILLA,'OPEN_SURFACE_SWAP',('V05','V06','S20','S21'),dict(vanilla=left,af=right),
        '바닐라 통과 AF 서랍의 열림 상태에서 조립 경계와 UV가 유지되고, PNG와 원본 화소가 바뀌는 로컬 면은 각각 한 개다.',
        '통의 로컬 up과 서랍의 로컬 north는 상태 회전 전 면 방향이다.')
    ids=('S20','S22','S23','S24','S25')
    assert [len(elements[i]) for i in ids]==[1,1,5,6,5]
    handle=next(r for r in faces['S23'] if 'oak_handle' in r['resource_id'])
    assert by_element[keyed(handle,element_key)]['local_size']=='0.1|1|4'
    add(category,LIMIT,'HANDLE_PART_COUNTEREXAMPLE',ids,dict(samples=counts(*ids),macaw_handle_model_units='0.1|1|4'),
        'AF·HC 기준 서랍은 1요소이며 Macaw 서랍 표본은 5요소에 돌출 손잡이를 포함한다.',
        '모든 수납장에 단일 큐브 방식이나 독립 손잡이 방식을 적용할 근거는 없다.')

    category='SHELVING'
    ids=('V07','S28')
    same={i:{r['png_sha'] for r in faces[i] if r['resource_id']=='minecraft:block/bookshelf'} for i in ids}
    assert same['V07']==same['S28'] and len(same['V07'])==1
    add(category,VANILLA,'SHARED_BOOKSHELF_PNG',ids,
        dict(shared_source_sha256=next(iter(same['V07'])),samples=counts(*ids)),
        '바닐라 책장과 Macaw 기본 책장이 같은 바닐라 책장 PNG를 사용한다. 모델 요소는 각각 1개와 10개다.',
        '동일 PNG는 모델 조립이나 크롭 영역 전체의 일치를 뜻하지 않는다.')
    ids=('V08','S27')
    blank=sum(r['pixels']!='' and r['pixels']==r['alpha_zero'] for r in faces['S27'])
    assert int(cases['V08']['zero_thickness_elements'])==6 and blank==2
    add(category,VANILLA,'ZERO_THICKNESS_OVERLAY',ids,dict(samples=counts(*ids),hc_fully_transparent_faces=blank),
        '조각된 책장과 HC 선반은 모두 기본 몸체와 별도의 0두께 표면을 가진다. 선택한 HC 선반의 실측 면 두 개는 완전 투명했다.',
        '슬롯의 시각·상호작용 효과와 선반의 빈 오버레이는 별개다.')
    assert resource_set('S28')==resource_set('S29') and compare_surfaces('S28','S29')['unchanged']==3
    add(category,SPECIFIC,'BOOKSHELF_CONNECTION',('S28','S29'),compare_surfaces('S28','S29'),
        'Macaw 책장 연결 상태는 같은 PNG 경로 집합을 유지하며 형상·UV 배치를 바꾼다.',
        '요소 AABB와 로컬 면 방향을 포함한 정적 서명 기준이다.')

    category='SOFA_BENCH'
    ids=('S33','S34','S35','S36')
    assert all(resource_set(a)==resource_set(b) and len(elements[a])>len(elements[b])
               for a,b in (('S33','S34'),('S35','S36')))
    add(category,MULTI,'CORNER_COUCH_LAYOUT',ids,counts(*ids),
        'HC와 Macaw 소파의 코너 상태는 PNG 경로 집합을 유지하면서 요소 수가 각각 8→6, 11→7로 줄었다.',
        '동일 PNG의 UV 배치까지 유지된다는 근거는 없다.')
    ids=('V01','V02','S30','S31','S32')
    assert resource_set('S30')==resource_set('S31') and len(elements['S30'])-len(elements['S31'])==3
    add(category,LIMIT,'BENCH_BACK_AND_STAIR',ids,dict(samples=counts(*ids),spans=spans('V01','V02','S30','S31')),
        'AF 벤치에서 등받이를 제외하면 요소 세 개가 빠진다. 계단·반 블록은 높이와 단차만 비교한다.',
        '등받이 없는 판재와 좌대·등받이 조립을 동일한 소파 구성으로 묶을 근거는 없다.')

    category='BED'
    assert not elements['V11'] and not faces['V11'] and all(cases[i]['cohort']=='HC' for i in ('S37','S38'))
    add(category,LIMIT,'BED_SPECIAL_RENDER',('V09','V11','S37','S38'),counts('V09','V11','S37','S38'),
        '바닐라 흰색 침대는 정적 일반 요소 0개로 기록된다. HC 발치와 머리맡의 모델 면 72개와 6개는 정적 원본에서 확인했다.',
        '바닐라 양털은 표면 대조군이며 특수 렌더 침대의 월드 형상은 미확인이다.')
    assert spans('S37')['S37']=='1|1|2' and len(elements['S38'])==1
    add(category,SPECIFIC,'BED_FOOT_HEAD',('S37','S38'),dict(samples=counts('S37','S38'),spans=spans('S37','S38')),
        'HC 발치 모델의 깊이는 2블록이며, 머리맡의 대응 상태에는 모델 요소 하나가 있다.',
        '두 상태의 원본 조립 범위이며 겹침·실제 표시와 배치 결과는 별도 검토한다.')

    category='KITCHEN'
    pairs=(('V12','V13'),('S42','S43'))
    ids=tuple(i for pair in pairs for i in pair)
    change={a+'/'+b:compare_surfaces(a,b) for a,b in pairs}
    for a,b in pairs:
        assert cases[a]['bbox']==cases[b]['bbox'] and len(elements[b])==len(elements[a])+1
        assert change[a+'/'+b]==dict(unchanged=len(faces[a]),removed=0,added=1)
        animation=[r for r in faces[b] if r['status']=='ANIMATED_FRAME_RECTS']
        assert len(animation)==1 and animation[0]['direction']=='up'
    add(category,VANILLA,'WATER_SURFACE_ADDITION',ids,dict(face_multisets=change,spans=spans(*ids)),
        '바닐라 가마솥과 Macaw 싱크대 모두 물 상태에서 기존 면이 유지되고 상향 애니메이션 면 한 개가 추가된다.',
        '정적 면 다중집합을 비교했다. 물 표면 위치·시트의 UV와 런타임 물 동작은 각각 다를 수 있다.')
    diff=panel_diff('S39','S40')
    assert len(diff['resource_id'])==6 and len(diff['rgba_sha256'])==5 and not diff['uv']
    add(category,SPECIFIC,'COUNTER_FINISH',('S39','S40'),diff,
        'HC 조리대 타입 변경은 하부 요소 여섯 면의 PNG 경로를 바꾸며 그중 다섯 면의 원본 RGBA 지문이 달랐다.',
        '다른 PNG 경로가 항상 다른 크롭 화소를 의미하지 않는다.')
    assert all(len(elements[i])==2 and cases[i]['span_blocks']=='1|1|1' for i in ('S39','S40','S41'))
    add(category,MULTI,'COUNTER_TWO_PARTS',('S39','S40','S41'),counts('S39','S40','S41'),
        'HC와 Macaw 조리대 표본은 모두 2요소의 1블록 외곽 조립이다.',
        '같은 개수와 외곽이어도 상판 두께·재질·UV는 모델마다 확인한다.')

    category='LIGHT_DECOR'
    ids=('V14','S44','S45')
    diff=panel_diff('S44','S45')
    assert not diff['resource_id'] and len(diff['uv'])==len(diff['rgba_sha256'])==4
    assert int(cases['V14']['faces_with_first_frame_alpha_zero'])==4
    add(category,LIMIT,'LAMP_UV_AND_EMISSION',ids,dict(samples=counts(*ids),af_changed=diff),
        'AF 램프 점등 전후 같은 텍스처에서 측면 네 곳의 UV와 크롭 화소가 바뀐다. 바닐라 랜턴의 원본 첫 프레임에는 투명 화소가 있는 면 네 개가 있다.',
        '광량·렌더 효과·발광 판정은 런타임 근거가 필요하다.')
    ids=('V15','S46','S47')
    assert [len(elements[i]) for i in ids]==[5,5,3] and len(set(spans(*ids).values()))==3
    add(category,LIMIT,'PLANT_CONTAINER_SUBTYPES',ids,dict(samples=counts(*ids),spans=spans(*ids)),
        '바닐라 빈 화분, AF 화단 상자, HC 화분은 부피와 요소 조립이 다르다.',
        '화단 상자와 화분을 동일 하위 유형으로 합치거나 빈 내부의 렌더를 판정할 근거는 없다.')

    categories=sorted({c for r in case_rows for c in r['category'].split('|')})
    coverage=[]
    for c in categories:
        src=[r for r in case_rows if c in r['category'].split('|')]
        control=[r for r in src if r['cohort']=='VANILLA']
        mod=[r for r in src if r['cohort']!='VANILLA']
        entries=[r for r in claims if r['category']==c]
        assert control and mod and entries
        coverage.append(dict(category=c,vanilla_cases='|'.join(r['case'] for r in control),
                             mod_cases='|'.join(r['case'] for r in mod),mod_cohorts='|'.join(sorted({r['cohort'] for r in mod})),
                             findings='|'.join(r['finding_id'] for r in entries)))
    assert len(coverage)==9
    assert {i for r in coverage for col in ('vanilla_cases','mod_cases') for i in r[col].split('|')}==cases.keys()
    assert all(len({r['finding_id'] for r in claims if r['category']==c})>=2 for c in categories)
    out.mkdir(parents=True,exist_ok=True)
    write(out/'CATEGORY_COVERAGE.csv',coverage)
    write(out/'CROSS_CATEGORY_FINDINGS.csv',claims)
    result=dict(status='PASS',category_count=len(coverage),case_count=len(cases),finding_count=len(claims),
                classifications=dict(Counter(r['classification'] for r in claims)),
                input_sha256={name:hashlib.sha256((B/name).read_bytes()).hexdigest()
                              for name in ('CASES.csv','APPLICATIONS.csv','ELEMENTS.csv','FACES.csv.xz')})
    encoded=json.dumps(result,sort_keys=True,indent=2)+'\n'
    (out/'C_AUDIT.json').write_text(encoded,encoding='utf-8')
    print(encoded)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    main(p.parse_args().out)
