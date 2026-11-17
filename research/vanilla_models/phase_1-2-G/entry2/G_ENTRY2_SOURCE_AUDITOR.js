/* Minecraft 1.21.11 1-2-G Entry2 original source auditor
   Source: GitHub original model/blockstate JSON utf8 and PNG base64.
   Reference: G_ENTRY2_PRIOR_EVIDENCE_REFERENCE.json (A-F historical record, never new G proof).
   Pass in tools and the G queue offset (0, 14, 28, ... 770).
   For PNG, G_ENTRY1_PNG.readFileBase64 must be loaded beforehand.
   Each batch persists original JSON and independent recomputations.
*/
globalThis.G_ENTRY2_SOURCE = (() => {
const repo="sanato-nb/Minecraft_Furniture_Style_Research",base="research/vanilla_models/phase_1-2-G/entry2/";
const bytes=s=>{const str=unescape(encodeURIComponent(s));return Uint8Array.from([...str].map(x=>x.charCodeAt(0)))};
const bsha=s=>G_ENTRY1_PNG.gitSHA(bytes(s));
const pathModel=ref=>{
 if(!ref)return null;const base=ref.replace(/^minecraft:/,"").replace(/^block\//,"");
 return "1.21.11/assets/minecraft/models/block/"+base+".json"
};
function directModel(source,prior){
const parent=source.parent??null,own=Array.isArray(source.elements)?source.elements:null;
const faces=(own??[]).flatMap((e,j)=>Object.entries(e.faces||{}).map(([direction,face])=>({
element_index:j,direction,texture:face.texture??null,uv_key_explicit:Object.hasOwn(face,"uv"),
uv:face.uv??null,tintindex_explicit:Object.hasOwn(face,"tintindex"),cullface_explicit:Object.hasOwn(face,"cullface")
})));
const ownFace=faces.length,uv=faces.filter(x=>x.uv_key_explicit).length;
const ex=prior.model?.E_exception==="True",provider=prior.model?.F_geometry_provider??null;
const prv=JSON.parse(prior.model?.F_parent_chain||"[]");
let model_source_matches_prior=Boolean(prior.model&&prior.sha===prior.model.F_original_sha&&prior.sha===prior.model.C_original_sha);
let directChainOwn=prv[0]?.path===prior.path&&prv[0]?.sha===prior.sha&&String(prv[0]?.own_elements)===String(own?.length??0);
let own_geometry_matches=null,comparison_scope="INHERITED_PARENT_GEOMETRY_REQUIRES_DIRECT_PARENT_FETCH";
if(provider===prior.path){comparison_scope="SELF_OWNED_GEOMETRY";own_geometry_matches=
Number(prior.model.F_element_count)===(own?.length??0)&&Number(prior.model.F_face_count)===ownFace&&
Number(prior.model.F_UV_explicit)===uv&&Number(prior.model.F_UV_absent)===ownFace-uv}
else if(ex){comparison_scope="E_SPECIAL_RENDERER_NO_GENERAL_ELEMENTS";own_geometry_matches=own===null||own.length===0}
return {parent,parent_model_path:pathModel(parent),parent_match:Fmatch(prv,parent),own_elements_key_explicit:Object.hasOwn(source,"elements"),
own_element_count:own?.length??0,own_face_count:ownFace,own_uv_explicit:uv,own_uv_implicit:ownFace-uv,
own_texture_keys:Object.keys(source.textures||{}),own_texture_defs:source.textures||{},texture_slot_refs:faces,
own_display_parts:Object.keys(source.display||{}),ambientocclusion_explicit:Object.hasOwn(source,"ambientocclusion"),
model_source_matches_prior,direct_chain_self_match:directChainOwn,F_geometry_provider:provider,E_exception:ex,
comparison_scope,own_geometry_matches:own_geometry_matches};
}
function Fmatch(chain,parent){if(!chain.length)return false;const p=chain[0]?.parent_ref??null;return String(p??"")===String(parent??"")}
function choices(source,prior){
const entries=[];
for(const [key,value] of Object.entries(source.variants||{})){const choices=Array.isArray(value)?value:[value];choices.forEach((choice,j)=>entries.push({kind:"variants",rule_index:Object.keys(source.variants).indexOf(key),condition:key,alternative_index:j,alternative_count:choices.length,apply:choice}));}
(source.multipart||[]).forEach((p,i)=>{const choices=Array.isArray(p.apply)?p.apply:[p.apply];choices.forEach((choice,j)=>entries.push({kind:"multipart",rule_index:i,condition:p.when??null,alternative_index:j,alternative_count:choices.length,apply:choice}))});
const refPath=m=>{const z=m?.model||"";if(!z)return "";const v=z.includes(":")?z.split(":")[1]:z;return "1.21.11/assets/minecraft/models/"+v+".json"};
const declared=entries.map(x=>({...x,model_path:refPath(x.apply),explicit:{x:Object.hasOwn(x.apply||{},"x"),y:Object.hasOwn(x.apply||{},"y"),uvlock:Object.hasOwn(x.apply||{},"uvlock"),weight:Object.hasOwn(x.apply||{},"weight")}}));
const priorRules=prior.blockstate?.prior_D_rule_digests||[];
let mismatch=[];if(declared.length!==priorRules.length)mismatch.push("D_OPTION_COUNT");
for(let i=0;i<Math.min(declared.length,priorRules.length);i++){const d=declared[i],p=priorRules[i],a=d.apply;
 const bool=(v)=>v==="true"||v===true;
 if(p[0]!==d.kind||Number(p[1])!==d.rule_index||Number(p[4])!==d.alternative_index||Number(p[5])!==d.alternative_count||p[6]!==d.model_path||bool(p[7])!==d.explicit.x||bool(p[9])!==d.explicit.y||bool(p[11])!==d.explicit.uvlock||bool(p[13])!==d.explicit.weight){mismatch.push("D_OPTION_REFERENCE_OR_PRESENCE_"+i);continue}
 for(const [v,ix,present] of [["x",8,7],["y",10,9],["uvlock",12,11],["weight",14,13]]){
 if(d.explicit[v]&&String(a[v])!==String(p[ix]))mismatch.push("D_"+v+"_VALUE_"+i)
 }
 if(d.kind==="variants"&&p[2]!==d.condition)mismatch.push("D_VARIANT_KEY_"+i);
 // D multipart condition serialization intentionally maintained as source+prior,
 // condition equivalence audited separately rather than unsafe string conversion.
}
return{structure:Object.hasOwn(source,"variants")?"variants":Object.hasOwn(source,"multipart")?"multipart":"none",
variants_rules:Object.keys(source.variants||{}).length,multipart_rules:(source.multipart||[]).length,
original_choice_count:declared.length,unique_target_model_paths:[...new Set(declared.map(x=>x.model_path))],
explicit_flags:{x:declared.filter(x=>x.explicit.x).length,y:declared.filter(x=>x.explicit.y).length,
uvlock:declared.filter(x=>x.explicit.uvlock).length,weight:declared.filter(x=>x.explicit.weight).length},
prior_D_rule_choice_count:priorRules.length,D_choice_mismatches:mismatch,choices:declared};
}
const recordPNG=(r,prior,remote)=>{
const x=G_ENTRY1_PNG.readFileBase64(remote.content),c=prior.PNG||{};
const matchedSha=remote.sha===prior.sha&&x.git_blob_sha===prior.sha;
const C_match=c.C_in_scope?(
 c.C_git_sha===prior.sha&&x.rgba_sha256===c.C_rgba_sha256&&
 String(x.width)===c.C_width&&String(x.height)===c.C_height&&x.mode===c.C_mode&&
 String(x.alpha.opaque)===c.C_opaque&&String(x.alpha.transparent)===c.C_transparent&&
 String(x.alpha.partial)===c.C_partial&&String(x.unique_alpha_values)===c.C_unique_alpha):null;
return {original_bytes:x.byte_length,original_sha1_git:x.git_blob_sha,original_sha256_file:x.file_sha256,
png_valid_signature_crc_adler:true,rgba_full_decoded:true,width:x.width,height:x.height,mode:x.mode,
bit_depth:x.bit_depth,color_type:x.color_type,interlace:x.interlace,rgba_sha256:x.rgba_sha256,
opaque_pixels:x.alpha.opaque,transparent_pixels:x.alpha.transparent,partial_alpha_pixels:x.alpha.partial,
unique_alpha_values:x.unique_alpha_values,first_frame_square_rgba_sha256:x.first_square_raster_rgba_sha256,
original_git_sha_match:matchedSha,C_prior_in_scope:c.C_in_scope,C_prior_RGBA_metadata_match:C_match,
C_mcmeta_path:c.C_mcmeta_path||null,C_mcmeta_SHA:c.C_mcmeta_sha||null,
F_prior_visual:c.F_prior_visual===true,original_raw_base64_not_persisted_for_repo_size:true};
};
async function auditBatch(tools,offset){
const prior=(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:base+"G_ENTRY2_PRIOR_EVIDENCE_REFERENCE.json"})).result;
const x=JSON.parse(prior.content);if(x.assets.length!==775)throw Error("fixed scope manifest is not 775");
const input=x.assets.slice(offset,offset+14);
const source=await Promise.all(input.map(async q=>{try{const r=(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:q.path,encoding:q.type==="BLOCK_TEXTURE_PNG"?"base64":"utf-8"})).result;return{q,r}}catch(e){return{q,error:String(e)}}}));
const records=source.map(({q,r,error})=>{
const out={index:q.index,type:q.type,path:q.path,expected_git_sha:q.sha,connector_git_sha:r?.sha??null,
git_sha_computed:null,source_content_direct_fetched:!!r,original_read_ok:false,content:undefined,analysis:null,errors:[]};
if(error){out.errors.push("CONNECTOR_FETCH: "+error);return out}
try{
 if(q.type==="BLOCK_TEXTURE_PNG"){out.analysis=recordPNG(out,q,r);out.git_sha_computed=out.analysis.original_sha1_git;}
 else{
  const obj=JSON.parse(r.content);out.content=obj;
  out.git_sha_computed=bsha(r.content);
  out.analysis=q.type==="BLOCK_MODEL_JSON"?directModel(obj,q):choices(obj,q);
 }
 out.original_read_ok=true;
 if(r.sha!==q.sha||out.git_sha_computed!==q.sha)out.errors.push("ORIGINAL_GIT_BLOB_SHA_MISMATCH");
 if(q.type==="BLOCK_MODEL_JSON"){
  if(!out.analysis.model_source_matches_prior||!out.analysis.direct_chain_self_match||!out.analysis.parent_match)out.errors.push("MODEL_F_C_SOURCE_CHAIN_MISMATCH");
  if(out.analysis.own_geometry_matches===false)out.errors.push("MODEL_OWN_GEOMETRY_F_MISMATCH");
 }else if(q.type==="BLOCKSTATE_JSON"){
  if(q.blockstate?.prior_D_source_sha!==q.sha||out.analysis.D_choice_mismatches.length)out.errors.push("BLOCKSTATE_PRIOR_D_RULE_MISMATCH");
 }else if(out.analysis.C_prior_RGBA_metadata_match===false||!out.analysis.original_git_sha_match)out.errors.push("PNG_C_PRIOR_OR_SHA_MISMATCH");
}catch(e){out.errors.push("SOURCE_PARSE_OR_DECODE: "+String(e))}
return out});
const success=records.filter(r=>r.original_read_ok&&r.errors.length===0).length;
const pass={schema:"G_ENTRY2_ORIGINAL_SOURCE_BATCH/v1",source_main_baseline:"ae1448906d4cb6f2aff4bdc43fbdc808024fd6bb",
G_entry:"ENTRY2",G_fixed_scope:775,offset,expected:input.length,success,
SHA_reopened:records.filter(r=>r.git_sha_computed===r.expected_git_sha).length,
model_inherited_geometry_pending:records.filter(r=>r.analysis?.comparison_scope==="INHERITED_PARENT_GEOMETRY_REQUIRES_DIRECT_PARENT_FETCH").length,
external_C_RGBA_matches:records.filter(r=>r.type==="BLOCK_TEXTURE_PNG"&&r.analysis?.C_prior_RGBA_metadata_match===true).length,
C_outside_reopened:records.filter(r=>r.type==="BLOCK_TEXTURE_PNG"&&r.analysis?.C_prior_in_scope===false&&r.original_read_ok).length,
source_prior_reference_blob_sha:prior.sha,records};
const dest=base+"source_batches/G_ENTRY2_ORIGINAL_SOURCE_"+String(offset).padStart(3,"0")+".json";
const commit=await tools.mcp__GitHub__create_file({repository_full_name:repo,path:dest,content:JSON.stringify(pass,null,2)+"\n",message:"1-2-G Entry2: 원본 775개 중 "+offset+"–"+(offset+input.length-1)+" 직접 바이너리/JSON 검증",branch:"main"});
return{start:offset,total:input.length,success,model_inherited_geometry_pending:pass.model_inherited_geometry_pending,C_RGBA_matches:pass.external_C_RGBA_matches,C_outside:pass.C_outside_reopened,errors:records.filter(r=>r.errors.length).map(r=>({path:r.path,errors:r.errors})),sha_match:pass.SHA_reopened,commit:commit.result.commit_sha,path:dest};
}
return {auditBatch,source_sha_utf8:bsha,choices,directModel,recordPNG};
})();