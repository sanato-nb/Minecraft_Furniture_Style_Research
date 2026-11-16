import csv, hashlib, json, subprocess
from pathlib import Path
from collections import defaultdict, Counter
from PIL import Image

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'research/vanilla_models/phase_1-2-F/entry4'
Q=list(csv.DictReader(open(OUT/'F_ENTRY4_QUEUE_494.csv')))
def dump(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def sha(p):
    b=p.read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def modelpath(ref):
    ref=ref.split(':')[-1]
    return ROOT/'1.21.11/assets/minecraft/models'/ (ref+'.json')
def texpath(ref):
    ref=ref.split(':')[-1]
    return ROOT/'1.21.11/assets/minecraft/textures'/(ref+'.png')
def rel(p): return str(p.relative_to(ROOT))
def read(p): return json.loads(p.read_text())
def write(name, rows):
    if not rows:return
    with open(OUT/name,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

# Parse source blockstates independently of the prior D join table.
d=defaultdict(list)
for p in sorted((ROOT/'1.21.11/assets/minecraft/blockstates').glob('*.json')):
    raw=read(p)
    for kind, rules in raw.items():
        if kind=='variants': iterable=[(k,v) for k,v in rules.items()]
        elif kind=='multipart': iterable=[(dump(x.get('when',{})),x.get('apply',[])) for x in rules]
        else:continue
        for ri,(condition,choices) in enumerate(iterable):
            opts=choices if isinstance(choices,list) else [choices]
            for ai,opt in enumerate(opts):
                if not isinstance(opt,dict) or 'model' not in opt:continue
                m=modelpath(opt['model'])
                d[rel(m)].append(dict(model_path=rel(m),blockstate_path=rel(p),blockstate_sha=sha(p),rule_kind=kind.upper(),rule_index=ri,condition=condition,alternative_index=ai,alternative_count=len(opts),x_present='x' in opt,x=opt.get('x',''),y_present='y' in opt,y=opt.get('y',''),uvlock_present='uvlock' in opt,uvlock=opt.get('uvlock',''),weight_present='weight' in opt,weight=opt.get('weight','')))

sources=[]; geometries=[]; elements=[]; visuals=[]; assemblies=[]; styles=[]; unresolved=[]; pngs={}; choices=[]
for q in Q:
    path=q['source_path']; p=ROOT/path; actual=sha(p)
    if actual!=q['git_blob_sha']: raise ValueError((path,actual,q['git_blob_sha']))
    chain=[]; seen=set(); cur=p; provider=None; geo=[]; bindings={}
    while cur.exists() and rel(cur) not in seen:
        seen.add(rel(cur)); obj=read(cur); chain.append(dict(path=rel(cur),sha=sha(cur),parent_ref=obj.get('parent'),own_elements=len(obj.get('elements',[]))))
        for k,v in obj.get('textures',{}).items():bindings.setdefault(k,v)
        if provider is None and 'elements' in obj:provider=cur;geo=obj['elements']
        if not obj.get('parent'):break
        cur=modelpath(obj['parent'])
    else:
        raise ValueError(('parent missing or cycle',path,str(cur)))
    ex=q['E_exception_owned']=='YES'
    if ex and geo: raise ValueError(('E geometry',path))
    if not ex and not geo: raise ValueError(('missing geometry',path))
    dims=[]; allpts=[]; zero=thin=rot=inv=outside=faces=uv=0
    slotrefs=set()
    for i,e in enumerate(geo):
        fr=e['from'];to=e['to']; ds=[abs(b-a) for a,b in zip(fr,to)]
        dims+=ds;allpts += [fr,to]; rot+=bool(e.get('rotation'));zero+=0 in ds;thin+=min(ds)<=1
        inv+=any(b<a for a,b in zip(fr,to));outside+=any(v<0 or v>16 for v in fr+to)
        fc=e.get('faces',{});faces+=len(fc);uv+=sum('uv' in v for v in fc.values())
        slotrefs|={v.get('texture','') for v in fc.values()}
        elements.append(dict(model_path=path,model_sha=actual,provider_path=rel(provider),provider_sha=sha(provider),element_index=i,from_json=dump(fr),to_json=dump(to),axis_thickness_json=dump(ds),rotation_json=dump(e.get('rotation')),face_keys_json=dump(list(fc)),face_count=len(fc),face_UV_explicit=sum('uv' in v for v in fc.values()),zero_thickness=0 in ds,thin_le_1=min(ds)<=1))
    def resolve(ref):
        seen_slots=set()
        while ref.startswith('#'):
            key=ref[1:]
            if key in seen_slots or key not in bindings:return None
            seen_slots.add(key);ref=bindings[key]
        return texpath(ref)
    refs=slotrefs|({'#particle'} if ex else set())
    linked=[];missing=[]
    for ref in sorted(refs):
        tp=resolve(ref)
        if tp is None:missing.append(ref)
        elif tp.exists():
            linked.append((rel(tp),sha(tp)))
            pngs[rel(tp)]=sha(tp)
        else:missing.append(ref+'=>'+str(tp))
    bboxlo=[min(pt[i] for pt in allpts) for i in range(3)] if allpts else []
    bboxhi=[max(pt[i] for pt in allpts) for i in range(3)] if allpts else []
    extent=[b-a for a,b in zip(bboxlo,bboxhi)]
    tags=[]
    if ex:tags=['E_SOURCE_EXCEPTION']
    else:
        if len(geo)==1 and geo[0]['from']==[0,0,0] and geo[0]['to']==[16,16,16] and not rot:tags.append('EXACT_FULL_CUBE')
        if len(geo)>1:tags.append('MULTI_ELEMENT')
        if thin:tags.append('THIN_ELEMENT')
        if zero:tags.append('ZERO_THICKNESS')
        if rot:tags.append('ROTATED_ELEMENT')
        if inv or outside:tags.append('INVERTED_OR_OUTSIDE_16')
        if not tags:tags.append('AXIS_ALIGNED_CUBOIDS')
    matched=d.get(path,[])
    if bool(matched)!=(q['D_direct_model_selected']=='YES'):raise ValueError(('D mismatch',path))
    for v in matched:choices.append(dict(model_path=path,model_sha=actual,**{k:val for k,val in v.items() if k!='model_path'}))
    first=linked[0] if linked else None
    status='F_ENTRY4_SOURCE_GEOMETRY_ASSEMBLY_CHECKED_VISUAL_PENDING'
    base=dict(model_path=path,model_sha=actual,F_queue_index=q['F_queue_index'],priority=q['priority'],source_json_direct='YES',parent_chain_json=dump(chain),geometry_provider_path=rel(provider) if provider else '',geometry_provider_sha=sha(provider) if provider else '',E_exception=ex)
    sources.append(dict(**base,F_PNG_first_frame_observed='NO_VISUAL_REVIEW',D_direct_selected=q['D_direct_model_selected'],F_status=status))
    g=dict(model_path=path,model_sha=actual,geometry_provider_path=base['geometry_provider_path'],geometry_provider_sha=base['geometry_provider_sha'],element_count=len(geo) if not ex else 'N/A',face_count=faces if not ex else 'N/A',UV_explicit=uv if not ex else 'N/A',UV_key_absent=faces-uv if not ex else 'N/A',bbox_min_json=dump(bboxlo),bbox_max_json=dump(bboxhi),bbox_extent_json=dump(extent),axis_thickness_json=dump(dims),zero_elements=zero if not ex else 'N/A',thin_elements=thin if not ex else 'N/A',rotated_elements=rot if not ex else 'N/A',inverted_elements=inv if not ex else 'N/A',outside_elements=outside if not ex else 'N/A',tags='|'.join(tags),primary_archetype=tags[0])
    geometries.append(g)
    visuals.append(dict(model_path=path,model_sha=actual,C_prior_face_rows=q['C_geometry_faces_prior'],F_original_PNG_paths_sha_json=dump(linked),F_PNG_unique_count=len(linked),F_first_frame_direct_visual_observed='NO',F_observed_first_PNG_note='',detail_vs_geometry='UNRESOLVED_VISUAL_REVIEW',source_confidence='SOURCE_BINDING_ONLY',runtime_renderer_verified=False,unresolved_slots_json=dump(missing)))
    assemblies.append(dict(model_path=path,model_sha=actual,D_direct_selected=q['D_direct_model_selected'],D_original_rule_choices=len(matched),blockstate_paths_json=dump(sorted({v['blockstate_path'] for v in matched})),source_grade='ORIGINAL_BLOCKSTATE_RULES_STATIC',in_game_state_registry_verified=False))
    hypothesis='일반 elements가 없어 실제 형상은 미확인.' if ex else ('얇은 판·면 후보; 면의 방향과 이미지 확인 후 가구 전용 적용을 판단.' if thin else '원본 입체 비례를 가구 표면·지지 구조와 비교할 후보; 시각 검토 전 확정 보류.')
    styles.append(dict(**base,**{k:v for k,v in g.items() if k not in ('model_path','model_sha','geometry_provider_path','geometry_provider_sha')},source_PNG_paths_json=dump(linked),F_PNG_first_frame_observed='NO_VISUAL_REVIEW',C_prior_face_rows=q['C_geometry_faces_prior'],D_direct_selected=q['D_direct_model_selected'],D_original_rule_choices=len(matched),D_blockstate_paths_json=assemblies[-1]['blockstate_paths_json'],furniture_transfer_hypothesis=hypothesis,runtime_renderer='UNVERIFIED_RUNTIME_RENDERER' if ex else 'NOT_EXECUTED',F_status=status,F_structure_reason=f'원본 {len(geo)} 요소, bbox {extent}, 얇은 요소 {thin}, 0두께 {zero}, 회전 {rot}. 원형 활용은 가설.',F_visual_vs_geometry='PNG_VISUAL_REVIEW_PENDING',F_D_assembly_evidence='원본 blockstate 선택 '+str(len(matched))+'건; 게임 등록 상태 미확인'))
    if ex:unresolved.append(dict(model_path=path,model_sha=actual,issue='E_RUNTIME_RENDERER_UNVERIFIED',evidence='E source exception',status='OUT_OF_F_SOURCE_RUNTIME_SCOPE'))
    if missing:unresolved.append(dict(model_path=path,model_sha=actual,issue='TEXTURE_UNBOUND_OR_MISSING',evidence=dump(missing),status='OPEN'))
    unresolved.append(dict(model_path=path,model_sha=actual,issue='PNG_VISUAL_OBSERVATION_PENDING',evidence=dump(linked),status='OPEN'))

for path,s in sorted(pngs.items()):
    with Image.open(ROOT/path) as im:
        pix=im.convert('RGBA').crop((0,0,im.width,min(im.width,im.height)))
        a=list(pix.getdata());co=Counter(v[:3] for v in a if v[3])
        pngs[path]=dict(png_path=path,png_sha=s,width=im.width,height=im.height,first_frame_visible_pixels=sum(v[3]>0 for v in a),first_frame_transparent_pixels=sum(v[3]==0 for v in a),first_frame_partial_alpha_pixels=sum(0<v[3]<255 for v in a),first_frame_unique_RGB=len(co),dominant_RGB=dump(co.most_common(1)[0][0]) if co else '',observed_visual_note='',image_evidence_status='PIXELS_DECODED_VISUAL_REVIEW_PENDING')
for name,rows in [('F_MODEL_SOURCE_STATUS.csv',sources),('F_GEOMETRY_FEATURES.csv',geometries),('F_GEOMETRY_ELEMENTS.csv',elements),('F_TEXTURE_VISUAL_EVIDENCE.csv',visuals),('F_ASSEMBLY_LINKS.csv',assemblies),('F_D_ORIGINAL_RULE_CHOICES.csv',choices),('STYLE_OBSERVATIONS.csv',styles),('F_UNRESOLVED.csv',unresolved),('F_PNG_PIXEL_DECODE_STATUS.csv',list(pngs.values()))]:write(name,rows)
summary=dict(queue=len(Q),source_sha_verified=len(sources),general=sum(not r['E_exception'] for r in sources),E=sum(r['E_exception'] for r in sources),elements=len(elements),faces=sum(int(g['face_count']) for g in geometries if g['face_count']!='N/A'),D_direct=sum(r['D_direct_selected']=='YES' for r in assemblies),D_rule_choices=len(choices),PNG_unique=len(pngs),PNG_visually_observed=0,source_phase='PASS',style_complete=0)
(OUT/'F_ENTRY4_SOURCE_FIRST_PASS_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(summary)
