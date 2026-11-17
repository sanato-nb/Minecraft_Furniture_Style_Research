/* G2 independent original JSON/parent/geometry/face/UV/D model choice recheck.
   Read G2 original batch rollups (not prior F summaries alone), 16 auxiliary
   original parent JSONs, historical F geometry and C face counts. Does not
   classify runtime rendered appearance or approve outside-scope models.
*/
globalThis.G_ENTRY2_INDEPENDENT=(()=>{
const modelPath=ref=>{if(ref==null)return null;const r=ref.includes(":")?ref.split(":")[1]:ref;return "1.21.11/assets/minecraft/models/"+(r.startsWith("block/")?r:"block/"+r)+".json"};
function csv(s){const out=[];let row=[],cell="",q=false;for(let i=0;i<s.length;i++){let c=s[i];if(c==='"'){if(q&&s[i+1]==='"'){cell+='"';i++}else q=!q}else if(c===','&&!q){row.push(cell);cell=""}else if((c==='\n'||c==='\r')&&!q){if(c==='\r'&&s[i+1]==='\n')i++;row.push(cell);if(row.some(x=>x))out.push(row);row=[];cell=""}else cell+=c}if(cell||row.length){row.push(cell);out.push(row)}const h=out.shift().map(x=>x.trim());return out.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]??""])))}
function derive(chain){
 const m=chain.map(x=>x.raw_json),provider=chain.find(x=>Array.isArray(x.raw_json.elements)&&x.raw_json.elements.length>0);
 const elements=provider?.raw_json.elements||[];
 const merged={};for(let i=chain.length-1;i>=0;i--)Object.assign(merged,chain[i].raw_json.textures||{});
 function resolve(ref){const visited=new Set();let v=ref;for(let n=0;n<40;n++){
 if(typeof v!=="string"||!v.trim())return {value:null,reason:"EMPTY"};
 if(!v.startsWith("#"))return {value:v,reason:null};
 const key=v.slice(1);if(visited.has(key))return{value:null,reason:"TEXTURE_ALIAS_CYCLE"};visited.add(key);v=merged[key]
 }return{value:null,reason:"TEXTURE_ALIAS_DEPTH"}}
 const face=[];
 for(let ei=0;ei<elements.length;ei++){const el=elements[ei];for(const [direction,f] of Object.entries(el.faces||{})){
 const r=resolve(f.texture);face.push({element_index:ei,direction,explicit_uv:Object.hasOwn(f,"uv"),texture_ref:f.texture??null,resolved_texture:r.value,unbound_reason:r.reason})
 }}
 return{provider_path:provider?.path||null,provider_sha:provider?.sha||null,elements:elements.length,
 faces:face.length,UV_explicit:face.filter(x=>x.explicit_uv).length,UV_implicit:face.filter(x=>!x.explicit_uv).length,
 bound_faces:face.filter(x=>x.resolved_texture!==null).length,unbound_faces:face.filter(x=>x.resolved_texture===null).length,
 unresolved_refs:face.filter(x=>x.resolved_texture===null).map(x=>({el:x.element_index,dir:x.direction,ref:x.texture_ref,reason:x.unbound_reason})),
 face_samples:face.slice(0,4),source_element_provider:provider?.raw_json.elements||[]}
}
function recount(records,aux,fRows,gRows,cRows,dRows,priorPNG){
 const errors=[],F=new Map(fRows.map(x=>[x.model_path,x])),G=new Map(gRows.map(x=>[x.model_path,x])),C=new Map(cRows.map(x=>[x.source_path,x]));
 const all=new Map();
 for(const r of records.filter(x=>x.type==="BLOCK_MODEL_JSON"))all.set(r.path,{path:r.path,sha:r.sha,raw_json:r.raw_json});
 for(const r of aux){if(r.match)all.set(r.path,{path:r.path,sha:r.recomputed_sha,raw_json:r.full_json});else errors.push({type:"AUX_PARENT_SHA",path:r.path})}
 const results=[];
 for(const rec of records.filter(x=>x.type==="BLOCK_MODEL_JSON")){
 const f=F.get(rec.path),g=G.get(rec.path),c=C.get(rec.path),err=[];
 let expectedChain=[];try{expectedChain=JSON.parse(f?.parent_chain_json||"[]")}catch(e){err.push("F_PARENT_CHAIN_PARSE")}
 const chain=[],visited=new Set();let next=rec.path;
 while(next){if(visited.has(next)){err.push("PARENT_CYCLE");break}visited.add(next);
 const node=all.get(next);if(!node||!node.raw_json){err.push("MISSING_PARENT_ORIGINAL:"+next);break}
 chain.push(node);next=modelPath(node.raw_json.parent??null);
 if(chain.length>30){err.push("PARENT_DEPTH");break}}
 if(expectedChain.length!==chain.length)err.push("F_PARENT_CHAIN_LENGTH:"+expectedChain.length+"/"+chain.length);
 for(let j=0;j<Math.min(chain.length,expectedChain.length);j++){
 const e=expectedChain[j],a=chain[j];
 if(e.path!==a.path||e.sha!==a.sha||String(e.parent_ref??"")!==String(a.raw_json.parent??"")||
 Number(e.own_elements)!==(a.raw_json.elements?.length??0))err.push("F_PARENT_CHAIN_VALUE_AT_"+j)
 }
 const geo=derive(chain);
 if(f?.geometry_provider_path!== (geo.provider_path||"") || String(f?.geometry_provider_sha??"")!==String(geo.provider_sha??""))err.push("F_PROVIDER_PATH_SHA");
 const isE=f?.E_exception==="True";
 if(isE&&geo.faces!==0)err.push("E_SPECIAL_WITH_FACE");
 if(!isE){
 if([g?.element_count,g?.face_count,g?.UV_explicit,g?.UV_key_absent].join("|")!==[geo.elements,geo.faces,geo.UV_explicit,geo.UV_implicit].join("|"))err.push("F_FACE_ELEMENT_UV");
 if([c?.C_applied_faces,c?.C_explicit_uv_faces,c?.C_implicit_uv_key_absent_faces].join("|")!==[geo.faces,geo.UV_explicit,geo.UV_implicit].join("|"))err.push("C_FACE_UV");
 if([c?.C_bound_png_face_refs,c?.C_template_unbound_face_refs].join("|")!==[geo.bound_faces,geo.unbound_faces].join("|"))err.push("C_FACE_BINDING");
 }
 if(rec.sha!==f?.model_sha||rec.sha!==c?.git_blob_sha)err.push("F_C_SHA_MISMATCH");
 if(err.length)errors.push({type:"MODEL_SOURCE_GEOMETRY",path:rec.path,errors:err});
 results.push({path:rec.path,sha:rec.sha,parent_chain_depth:chain.length,provider_path:geo.provider_path,provider_sha:geo.provider_sha,
 E_special:isE,element_count:geo.elements,face_count:geo.faces,explicit_uv:geo.UV_explicit,implicit_uv:geo.UV_implicit,
 bound_faces:geo.bound_faces,unbound_faces:geo.unbound_faces,unbound_refs:geo.unresolved_refs,errors:err});
 }
 const choices=records.filter(x=>x.type==="BLOCKSTATE_JSON");const png=records.filter(x=>x.type==="BLOCK_TEXTURE_PNG");
 const d=choices.reduce((acc,r)=>acc+(r.analysis?.original_choice_count||0),0);
 const Dexpected=dRows.length;
 if(d!==Dexpected)errors.push({type:"D_OPTIONS_COUNT",new:d,prior:Dexpected});
 const distinct=new Set();const ruleRefs=[];for(let r of choices){for(let c of r.analysis?.choices||[]){if(c.model_path)distinct.add(c.model_path);ruleRefs.push({blockstate_path:r.path,model_path:c.model_path,rule_kind:c.kind,rule_index:c.rule_index,condition:c.condition,flags:c.explicit,apply:c.apply})}}
 const counts={source_records:records.length,models:results.length,blockstates:choices.length,PNG:png.length,
 original_source_sha_all_pass:records.filter(r=>r.ok&&r.computed_sha===r.sha&&!r.errors.length).length,
 parent_auxiliary_original_verified:aux.filter(x=>x.match).length,models_E:results.filter(x=>x.E_special).length,
 models_C_general:results.filter(x=>!x.E_special).length,model_elements:results.reduce((a,x)=>a+x.element_count,0),
 model_faces:results.reduce((a,x)=>a+x.face_count,0),explicit_uv:results.reduce((a,x)=>a+x.explicit_uv,0),implicit_uv:results.reduce((a,x)=>a+x.implicit_uv,0),
 bound_faces:results.reduce((a,x)=>a+x.bound_faces,0),unbound_faces:results.reduce((a,x)=>a+x.unbound_faces,0),
 D_source_options:d,D_reference_distinct_models:distinct.size,PNG_C_prior_verified:png.filter(x=>x.analysis?.C_prior_in_scope).length,
 PNG_C_RGBA_independent_matches:png.filter(x=>x.analysis?.C_prior_RGBA_metadata_match===true).length,
 PNG_outside_C:png.filter(x=>x.analysis?.C_prior_in_scope===false).length,
 PNG_raw_byte_sum:png.reduce((a,x)=>a+(x.analysis?.original_bytes??0),0),
 errors:errors.length};
 return {schema:"G_ENTRY2_INDEPENDENT_RECOUNT_SOURCE_FROM_G_ORIGINAL/v1",counts,errors,model_recount:results,
 D_rule_model_links:ruleRefs,
 scope_limits:["Parent original JSON verification may include 16 outside fixed Entry2 scope; no extra G 4669 target credited.","No runtime renderer, official JAR, or in-game state registry.","Prior C outside PNG must not be retroactively claimed as C verified.","F prior visual observation is not a newly performed G manual visual inspection."]};
}
return{csv,derive,recount};
})();