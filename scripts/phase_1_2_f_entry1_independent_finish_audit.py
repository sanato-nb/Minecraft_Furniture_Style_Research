"""Independent checks of final F Entry1, using source bytes and original D rules."""
import csv,json,hashlib,collections
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];B=R/'research/vanilla_models/phase_1-2-F/entry1'
def rows(n):
 with (B/n).open(newline='') as f:return list(csv.DictReader(f))
def sha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def path(ref):
 a=ref.split(':',1);return f'1.21.11/assets/{a[0] if len(a)==2 else "minecraft"}/models/{a[-1]}.json'
def main():
 q=rows('F_ENTRY1_QUEUE_150.csv');s=rows('STYLE_OBSERVATIONS.csv');g=rows('F_GEOMETRY_FEATURES.csv');t=rows('F_TEXTURE_VISUAL_EVIDENCE.csv');a=rows('F_ASSEMBLY_LINKS.csv');v=rows('F_PNG_DIRECT_VISUAL_OBSERVATIONS.csv');d=rows('F_D_ORIGINAL_RULE_CHOICES.csv');status=rows('F_MODEL_SOURCE_STATUS.csv')
 assert len(q)==len(s)==len(g)==len(t)==len(a)==len(status)==150 and len({x['source_path'] for x in q})==150
 assert len(v)==195 and len({x['png_path'] for x in v})==195 and len(d)==403
 Q={x['source_path']:x for x in q};S={x['source_path']:x for x in s};G={x['source_path']:x for x in g};T={x['model_path']:x for x in t};A={x['model_path']:x for x in a}
 assert set(Q)==set(S)==set(G)==set(T)==set(A)
 tags=collections.Counter();faces=elements=visual=unbound=e=uv_explicit=uv_absent=0
 for p,x in Q.items():
  raw=(R/p).read_bytes();assert sha(raw)==x['git_blob_sha']==S[p]['git_blob_sha'];body=json.loads(raw)
  assert S[p]['original_F_json_direct_read']=='YES' and S[p]['original_F_json_SHA_matches']=='YES'
  provider=G[p]['geometry_provider'];pp=json.loads((R/provider).read_text()) if provider else body
  if provider:assert sha((R/provider).read_bytes())==G[p]['provider_git_sha']
  el=pp.get('elements',[])
  if x['E_exception_owned']=='YES':
   e+=1;assert not el and S[p]['E_runtime_renderer_class_verified'] in ('NOT_TESTED','NO_UNVERIFIED_E') and S[p]['F_texture_detail_vs_geometry']=='PARTICLE_IMAGE_NOT_RENDERER_SURFACE'
  else:
   assert len(el)==int(G[p]['applied_elements']);elements+=len(el)
   assert sum(len(z.get('faces',{})) for z in el)==int(G[p]['B_element_face_sum'])==int(x['C_geometry_faces_prior']);faces+=int(G[p]['B_element_face_sum'])
   allfaces=[f for z in el for f in z.get('faces',{}).values()]
   explicit=sum('uv' in f for f in allfaces);absent=sum('uv' not in f for f in allfaces)
   assert explicit==int(S[p]['C_explicit_UV_faces_prior']) and absent==int(S[p]['C_implicit_UV_key_absent_faces_prior'])
   uv_explicit+=explicit;uv_absent+=absent
   assert sum(any(abs(z['to'][i]-z['from'][i])<=1 for i in range(3)) for z in el)==int(G[p]['thin_le_1_elements'])
   assert sum(any(z['to'][i]==z['from'][i] for i in range(3)) for z in el)==int(G[p]['zero_thickness_elements'])
   assert sum('rotation' in z for z in el)==int(G[p]['rotated_elements'])
   mins=[min(z[side][i] for z in el for side in ('from','to')) for i in range(3)];maxs=[max(z[side][i] for z in el for side in ('from','to')) for i in range(3)]
   assert json.loads(G[p]['bbox_min'])==mins and json.loads(G[p]['bbox_max'])==maxs
   assert json.loads(G[p]['bbox_extent'])==[maxs[i]-mins[i] for i in range(3)]
  pngs=json.loads(S[p]['F_direct_source_PNG_paths']);assert len(pngs)==int(S[p]['F_direct_source_PNG_count'])==int(T[p]['F_direct_source_PNG_count'])
  assert (T[p]['F_original_PNG_image_directly_seen']=='true')==bool(pngs)
  visual+=bool(pngs);unbound+=not bool(pngs)
  if x['D_direct_model_selected']=='YES':assert int(A[p]['F_D_original_rule_choices'])>0
  else:assert int(A[p]['F_D_original_rule_choices'])==0 and S[p]['F_D_assembly_status']=='NOT_DIRECT_D_SELECTED_ROLE_UNDETERMINED'
  assert S[p]['F_record_status']=='F_ENTRY1_SOURCE_STYLE_ACCEPTED_WITH_EXPLICIT_RENDER_OR_TEMPLATE_LIMIT'
  tags[S[p]['primary_geometry_archetype']]+=1
 assert (e,elements,faces,visual,unbound)==(8,371,1373,141,9)
 for x in v:
  p=x['png_path'];raw=(R/p).read_bytes();assert sha(raw)==x['git_blob_sha'];im=Image.open(R/p);im.load();assert (im.width,im.height)==(int(x['width']),int(x['height']))
  assert (B/x['contact_sheet']).exists()
  if x['C_sha_match']=='YES':assert x['C_prior_blob_sha']==x['git_blob_sha']
 # Rebuild exact D source choice keys from the 151 blockstate JSON bodies.
 expected=set();known={x['source_path'] for x in q};bs={x['blockstate_path'] for x in d};assert len(bs)==151
 for bp in bs:
  raw=(R/bp).read_bytes();obj=json.loads(raw)
  rules=[('VARIANT',str(k),val) for k,val in obj['variants'].items()] if 'variants' in obj else [('MULTIPART',json.dumps(z.get('when',{}),sort_keys=True),z['apply']) for z in obj['multipart']]
  for ri,(kind,cond,apps) in enumerate(rules):
   for ai,opt in enumerate(apps if isinstance(apps,list) else [apps]):
    mp=path(opt['model'])
    if mp in known:expected.add((mp,bp,sha(raw),kind,str(ri),cond,str(ai),str('x' in opt),str(opt.get('x','')),str('y' in opt),str(opt.get('y','')),str('uvlock' in opt),str(opt.get('uvlock','')),str('weight' in opt)))
 observed={(x['model_path'],x['blockstate_path'],x['blockstate_sha'],x['rule_kind'],x['rule_index'],x['rule_condition'],x['alternative_index'],x['x_key_present'],x['x_value_if_present'],x['y_key_present'],x['y_value_if_present'],x['uvlock_key_present'],x['uvlock_value_if_present'],x['weight_key_present']) for x in d}
 assert observed==expected and len(expected)==len(d)
 assert len([p for p in known if int(A[p]['F_D_original_rule_choices'])>0])==137
 assert len(rows('F_TEXTURE_C_SLOT_PNG_LINKS.csv'))==546 and len(rows('F_D_STATE_MODEL_SOURCE_LINKS.csv'))==1180
 assert len(rows('F_UNRESOLVED.csv'))==17
 out={'schema':'F_ENTRY1_COMPLETION_INDEPENDENT_AUDIT/v1','baseline_head':'1cc28bd82dab286c61fa155a3dfe2b6d43c803b2','queue_models_source_SHA':150,'prior_structural_source_models_rechecked':150,'general_geometry_models':142,'E_source_exceptions':8,'elements_recomputed':elements,'face_refs_match_prior_C':faces,'UV_explicit_key_faces_recomputed':uv_explicit,'UV_key_absent_faces_recomputed':uv_absent,'unique_PNG_first_frames_source_sha_and_dimensions_rechecked':195,'models_with_direct_source_PNG_visual_evidence':visual,'unbound_template_models_explicitly_limited':unbound,'D_original_blockstates_reparsed':151,'D_original_rule_choices_recomputed':len(d),'D_direct_models_rule_verified':137,'D_not_directly_selected_models':13,'prior_C_slot_links_reused':546,'prior_D_state_model_links_reused':1180,'runtime_renderer_verified':0,'unresolved_explicit_limits':17,'primary_archetype_counts':dict(tags),'F_Entry1_source_style_accepted':150,'F_cumulative_source_style_accepted':150,'F_whole_stage_complete':False,'mismatches':0,'pass':True}
 (B/'F_ENTRY1_COMPLETION_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
