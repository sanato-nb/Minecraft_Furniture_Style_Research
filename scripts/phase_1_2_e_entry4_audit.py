"""Independently recalculate the fixed E source-exception scope."""
import csv,hashlib,io,json
from collections import Counter,defaultdict
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/vanilla_models/phase_1-2-E'
OUT=BASE/'entry4'
def sha(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def rows(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))
def model_path(ref):
 ns,name=ref.split(':',1) if ':' in ref else ('minecraft',ref)
 return f'1.21.11/assets/{ns}/models/{name}.json'
def main():
 q=rows(BASE/'E_FIXED_SCOPE_86.csv');assert len(q)==len({r['model_path'] for r in q})==86
 expected={'ENTRY1':30,'ENTRY2':28,'ENTRY3':28};assert Counter(x['entry'] for x in q)==expected
 sources={};snapshots={};linked=[];png_ledger={};previous=[]
 for n,count in enumerate((30,28,28),1):
  b=BASE/f'entry{n}';s=rows(b/f'E_ENTRY{n}_MODEL_SOURCE.csv');snap=json.loads((b/f'E_ENTRY{n}_ORIGINAL_{count}.json').read_text())['sources']
  assert len(s)==len(snap)==count
  for x in s:assert x['model_path'] not in sources;sources[x['model_path']]=x
  for x in snap:assert x['path'] not in snapshots;snapshots[x['path']]=x
  linked+=rows(b/f'E_ENTRY{n}_D_BLOCKSTATE_LINKS.csv')
  for x in rows(b/f'E_ENTRY{n}_PARTICLE_PNG_UNIQUE.csv'):
   p=x['png_path'];assert p not in png_ledger or png_ledger[p]['png_sha']==x['png_sha'] and png_ledger[p]['rgba_sha256']==x['rgba_sha256'];png_ledger[p]=x
  previous.append(json.loads((b/f'E_ENTRY{n}_INDEPENDENT_RECHECK.json').read_text()))
 assert len(sources)==len(snapshots)==86 and all(x['pass'] and x['mismatches']==0 for x in previous)
 assert set(sources)=={x['model_path'] for x in q}
 seen_p=[];chain_count=0;ao=[];particle_count=0;missing=[];template=[]
 for r in q:
  p=r['model_path'];raw=(ROOT/p).read_bytes();d=json.loads(raw);s=sources[p];t=snapshots[p]
  assert raw.decode()==t['json_text'] and sha(raw)==r['model_git_sha']==s['model_sha']==t['sha']
  assert int(s['own_elements'])==len(d.get('elements',[]))==0 and (s['parent_key_present']=='True')==('parent' in d)
  cursor=d;visited={p};parents=[]
  while cursor.get('parent'):
   pp=model_path(cursor['parent']);assert pp not in visited;visited.add(pp);pr=(ROOT/pp).read_bytes();cursor=json.loads(pr)
   parents.append({'path':pp,'sha':sha(pr),'elements':len(cursor.get('elements',[]))})
   assert not cursor.get('elements')
  chain_count+=len(parents)
  if 'parent_chain_json' in s:assert json.loads(s['parent_chain_json'])==parents
  assert s['geometry_source_verdict']=='NO_GENERAL_ELEMENTS_IN_SOURCE_CHAIN' and s['renderer_path_grade']=='UNVERIFIED_RUNTIME_RENDERER'
  tex=d.get('textures',{});assert set(tex) in (set(),{'particle'})
  particle=tex.get('particle')
  if particle:
   particle_count+=1
   if particle=='minecraft:missingno':assert not s['particle_png_path'];missing.append(p)
   else:
    png='1.21.11/assets/minecraft/textures/'+particle.split(':')[-1]+'.png';assert s['particle_png_path']==png
    raw_png=(ROOT/png).read_bytes();im=Image.open(io.BytesIO(raw_png));im.load();v=png_ledger[png]
    assert sha(raw_png)==s['particle_png_sha']==v['png_sha'] and hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()==v['rgba_sha256']
    assert (im.width,im.height)==(int(v['width']),int(v['height']));seen_p.append(png)
  else:assert not s['particle_png_path'];template.append(p)
  if 'ambientocclusion' in d:ao.append(p)
 assert len(set(seen_p))==len(png_ledger)
 occurrence=Counter()
 for row in rows(ROOT/'research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv'):
  raw=(ROOT/row['source_path']).read_bytes();assert sha(raw)==row['git_blob_sha']
  d=json.loads(raw);apps=d['variants'].values() if 'variants' in d else (part['apply'] for part in d['multipart'])
  for app in apps:
   for opt in app if isinstance(app,list) else [app]:
    p=model_path(opt['model'])
    if p in sources:occurrence[(p,row['source_path'],opt['model'])]+=1
 ledger=Counter((x['model_path'],x['blockstate_path'],x['model_ref']) for x in linked)
 assert occurrence==ledger
 for r in q:
  p=r['model_path'];refs=[(k,n) for k,n in occurrence.items() if k[0]==p]
  assert int(r['D_rule_option_refs'])==int(sources[p]['D_rule_option_refs'])==sum(n for _,n in refs)
  assert set(json.loads(r['D_blockstate_paths_json']))=={k[1] for k,_ in refs}
 unreferenced=sorted(set(sources)-{k[0] for k in occurrence})
 assert len(occurrence)==len(ledger) and sum(occurrence.values())==178
 assert len({k[0] for k in occurrence})==84 and [p.rsplit('/',1)[-1] for p in unreferenced]==['block.json','thin_block.json']
 assert chain_count==1 and len(missing)==1 and len(template)==2 and len(ao)==3 and particle_count==84
 OUT.mkdir(exist_ok=True)
 exceptions=[];unresolved=[]
 for r in q:
  p=r['model_path'];s=sources[p];d=json.loads((ROOT/p).read_text())
  kind=('NO_PARTICLE_PARENT_DISPLAY_TEMPLATE' if p.endswith('/thin_block.json') else
        'NO_PARTICLE_DISPLAY_TEMPLATE' if p.endswith('/block.json') else
        'MISSINGNO_SENTINEL_NO_PNG' if p.endswith('/air.json') else
        'NO_ELEMENTS_PARTICLE_WITH_AMBIENTOCCLUSION' if 'ambientocclusion' in d else
        'NO_ELEMENTS_PARTICLE_ONLY')
  exceptions.append({'entry':r['entry'],'model_path':p,'model_sha':s['model_sha'],
      'source_exception_type':kind,'D_rule_option_refs':s['D_rule_option_refs'],
      'general_elements_source':0,'runtime_renderer_grade':'UNVERIFIED_RUNTIME_RENDERER',
      'visible_geometry_inference':'NOT_SUPPORTED_BY_PARTICLE_PNG'})
  unresolved.append({'model_path':p,'runtime_renderer_path':'UNVERIFIED_RUNTIME_RENDERER',
      'official_JAR_or_ingame_evidence':'NONE_IN_E_SCOPE',
      'source_exception_type':kind,'future_evidence_needed':'OFFICIAL_CLIENT_OR_INGAME_RENDER_VERIFICATION',
      'E_source_scope_disposition':'CLOSED_AS_EXPLICIT_UNVERIFIED_BOUNDARY'})
 for name,data in [('E_RENDER_EXCEPTIONS_86.csv',exceptions),('UNRESOLVED.csv',unresolved)]:
  with (OUT/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
 audit={'schema':'E_FINAL_SOURCE_EXCEPTION_AUDIT/v1','baseline_remote_head':'4464c545054f93136cce445d45bf3fecb4bcfcf0','fixed_queue_sha':sha((BASE/'E_FIXED_SCOPE_86.csv').read_bytes()),'entry_source_rows':expected,'unique_source_JSON_body_SHA_checked':86,'source_parent_links':chain_count,'source_or_inherited_elements':0,'particle_declarations':particle_count,'missingno_without_source_PNG':missing,'no_particle_templates':template,'ambientocclusion_key_models':ao,'distinct_actual_particle_PNG_SHA_RGBA_checked':len(png_ledger),'model_particle_PNG_links_checked':len(seen_p),'D_original_blockstates_recomputed':1168,'D_model_selection_refs':sum(occurrence.values()),'D_referenced_E_models':84,'D_unreferenced_E_models':unreferenced,'previous_independent_checks_passed':3,'runtime_renderer_verified':0,'official_JAR_authenticated':False,'ingame_renderer_tested':False,'gates':{'E1':'PASS_FIXED_SCOPE_86','E2':'PASS_SOURCE_86_OF_86','E3':'PASS_SOURCE_EVIDENCE_AND_UNVERIFIED_RUNTIME_LABELS_86_OF_86','E4':'PASS_INDEPENDENT_SOURCE_RECALCULATION_REMOTE_READBACK_PENDING'},'mismatches':0,'E_whole_stage_complete':False,'top_level_substages_complete':1,'top_level_substages_total':5,'entry5_allowed':False}
 (OUT/'E_FINAL_SOURCE_EXCEPTION_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(audit,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
