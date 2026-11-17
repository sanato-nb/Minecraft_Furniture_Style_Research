/* 1-2-G Entry3. Reproducible direct original source inspection and SHA/RGBA.
   Requires G_ENTRY1_PNG_AUDITOR.js loaded as globalThis.G_ENTRY1_PNG.
   Each invocation fetches original bytes from GitHub, re-hashes, writes evidence.
   Scope: user-extracted 1.21.11 assets; no official JAR/runtime certification.
*/
globalThis.G_ENTRY3_SOURCE=(()=>{
"use strict";
const repo="sanato-nb/Minecraft_Furniture_Style_Research";
const root="research/vanilla_models/phase_1-2-G/entry3/";
const queuePath=root+"G_ENTRY3_QUEUE_945.csv";
const priorCPath="research/vanilla_models/phase_1-2-C/entry5/C_PNG_UNIQUE_ALL.csv";
const utf8=s=>Uint8Array.from([...unescape(encodeURIComponent(s))].map(c=>c.charCodeAt(0)));
function csv(text){
 let rows=[],row=[],cell="",quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){cell+='"';i++}else quoted=!quoted}
 else if(c===','&&!quoted){row.push(cell);cell=""}
 else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(cell);if(row.some(v=>v!==""))rows.push(row);row=[];cell=""}
 else cell+=c}
 if(row.length||cell){row.push(cell);rows.push(row)}
 const header=rows.shift();return rows.map((r,i)=>Object.fromEntries(header.map((k,j)=>[k,r[j]??""])));
}
function inspectModel(obj){
 const el=Array.isArray(obj.elements)?obj.elements:[],faces=el.flatMap((e,i)=>Object.entries(e.faces||{}).map(([d,f])=>({element:i,direction:d,texture:f.texture??null,UV_explicit:Object.hasOwn(f,"uv"),cullface_explicit:Object.hasOwn(f,"cullface"),tintindex_explicit:Object.hasOwn(f,"tintindex")})));
 return{parent:obj.parent??null,has_elements:Object.hasOwn(obj,"elements"),own_elements:el.length,own_faces:faces.length,
 own_UV_explicit:faces.filter(f=>f.UV_explicit).length,own_texture_definitions:obj.textures??{},own_element_data:obj.elements??null,
 ambientocclusion_key_present:Object.hasOwn(obj,"ambientocclusion"),display_keys:Object.keys(obj.display||{})};
}
function inspectState(obj){
 const rules=[],opts=[];
 for(const [i,[condition,val]] of Object.entries(Object.entries(obj.variants||{}))){const choices=Array.isArray(val)?val:[val];choices.forEach((apply,j)=>opts.push({kind:"variants",rule_index:Number(i),condition,alternative_index:j,alternatives:choices.length,apply}))}
 (obj.multipart||[]).forEach((rule,i)=>{const choices=Array.isArray(rule.apply)?rule.apply:[rule.apply];choices.forEach((apply,j)=>opts.push({kind:"multipart",rule_index:i,condition:rule.when??null,alternative_index:j,alternatives:choices.length,apply}))});
 return{kind:Object.hasOwn(obj,"variants")?"variants":Object.hasOwn(obj,"multipart")?"multipart":"other",
 variants_rules:Object.keys(obj.variants||{}).length,multipart_rules:(obj.multipart||[]).length,
 original_choice_count:opts.length,original_choices:opts,
 model_ref_paths:[...new Set(opts.map(x=>x.apply?.model).filter(Boolean))],
 explicit_x:opts.filter(x=>Object.hasOwn(x.apply||{},"x")).length,explicit_y:opts.filter(x=>Object.hasOwn(x.apply||{},"y")).length,
 explicit_uvlock:opts.filter(x=>Object.hasOwn(x.apply||{},"uvlock")).length,explicit_weight:opts.filter(x=>Object.hasOwn(x.apply||{},"weight")).length};
}
async function run(tools,offset=0,limit=70){
 if(!globalThis.G_ENTRY1_PNG?.gitSHA||!globalThis.G_ENTRY1_PNG?.readFileBase64)throw Error("Load original G_ENTRY1_PNG_AUDITOR.js first");
 const [qRes,cRes]=await Promise.all([tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:queuePath}),tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:priorCPath})]);
 const q=csv(qRes.result.content),prior=new Map(csv(cRes.result.content).map(x=>[x.png_path,x]));
 if(q.length!==945)throw Error("Entry3 fixed queue not 945: "+q.length);
 if(offset<0||offset>=q.length||limit<1||limit>100)throw Error("Invalid batch");
 const slice=q.slice(offset,offset+limit);
 const records=new Array(slice.length);
 let cursor=0;
 async function worker(){
  for(;;){
   const i=cursor++;if(i>=slice.length)return;
   const t=slice[i],type=t.asset_type;
   const r={queue_index:offset+i+1,global_index:Number(t.G_global_index),type,path:t.source_path,expected_sha:t.git_blob_sha,
    returned_sha:null,computed_git_sha:null,source_read:false,source_valid:false,original_json:null,analysis:null,errors:[]};
   try{
    const x=(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:r.path,encoding:type==="BLOCK_TEXTURE_PNG"?"base64":"utf-8"})).result;
    r.returned_sha=x.sha;r.source_read=true;
    if(type==="BLOCK_TEXTURE_PNG"){
     const b=G_ENTRY1_PNG.readFileBase64(x.content);
     const c=prior.get(r.path);
     r.computed_git_sha=b.git_blob_sha;
     r.analysis={bytes:b.byte_length,file_sha256:b.file_sha256,signature_crc_adler_decoded:true,width:b.width,height:b.height,bit_depth:b.bit_depth,color_type:b.color_type,interlace:b.interlace,
       mode:b.mode,rgba_sha256:b.rgba_sha256,first_square_raster_rgba_sha256:b.first_square_raster_rgba_sha256,
       alpha:b.alpha,unique_alpha_values:b.unique_alpha_values,chunk_types:b.chunk_types,
       C_prior_in_scope:!!c,C_prior_rgba_metadata_match:c?(
       c.png_sha===r.expected_sha&&c.rgba_sha256===b.rgba_sha256&&Number(c.width)===b.width&&Number(c.height)===b.height&&c.mode===b.mode&&
       Number(c.opaque_pixels)===b.alpha.opaque&&Number(c.transparent_pixels)===b.alpha.transparent&&Number(c.partial_alpha_pixels)===b.alpha.partial&&
       Number(c.unique_alpha_values)===b.unique_alpha_values):null,
       C_prior_mcmeta_path:c?.mcmeta_path||null,C_prior_mcmeta_sha:c?.mcmeta_sha||null};
     if(r.analysis.C_prior_rgba_metadata_match===false)r.errors.push("C_PRIOR_PIXEL_METADATA_DIFFERENCE");
    }else{
     r.computed_git_sha=G_ENTRY1_PNG.gitSHA(utf8(x.content));
     r.original_json=JSON.parse(x.content);
     r.analysis=type==="BLOCK_MODEL_JSON"?inspectModel(r.original_json):type==="BLOCKSTATE_JSON"?inspectState(r.original_json):null;
     if(!r.analysis)r.errors.push("UNKNOWN_ASSET_TYPE");
    }
    if(r.returned_sha!==r.expected_sha||r.computed_git_sha!==r.expected_sha)r.errors.push("GIT_BLOB_SHA_MISMATCH");
    r.source_valid=r.errors.length===0;
   }catch(e){r.errors.push("SOURCE_FETCH_PARSE_OR_DECODE:"+String(e))}
   records[i]=r;
  }
 }
 await Promise.all(Array.from({length:10},()=>worker()));
 const counters={total:records.length,passed:records.filter(x=>x.source_valid).length,models:records.filter(x=>x.type==="BLOCK_MODEL_JSON").length,
 blockstates:records.filter(x=>x.type==="BLOCKSTATE_JSON").length,PNG:records.filter(x=>x.type==="BLOCK_TEXTURE_PNG").length,
 PNG_C_matched:records.filter(x=>x.analysis?.C_prior_rgba_metadata_match===true).length,PNG_outside_C:records.filter(x=>x.type==="BLOCK_TEXTURE_PNG"&&!x.analysis?.C_prior_in_scope).length,
 source_SHA_matched:records.filter(x=>x.returned_sha===x.expected_sha&&x.computed_git_sha===x.expected_sha).length,
 original_JSON_stored:records.filter(x=>x.original_json!==null).length};
 const result={schema:"G_ENTRY3_DIRECT_ORIGINAL_CONTENT_BATCH/v1",baseline_queue_sha:qRes.result.sha,prior_C_sha:cRes.result.sha,offset,limit:records.length,counters,records};
 const dest=root+"source_batches/G_ENTRY3_ORIGINAL_SOURCE_"+String(offset).padStart(3,"0")+".json";
 const created=await tools.mcp__GitHub__create_file({repository_full_name:repo,path:dest,
 content:JSON.stringify(result)+"\n",message:"1-2-G Entry3: 원본 직접 검사 "+(offset+1)+"~"+(offset+records.length)+" /945",branch:"main"});
 return{offset,records:records.length,counters,errors:records.filter(x=>x.errors.length).map(x=>({path:x.path,errors:x.errors})),destination:dest,commit:created.result.commit_sha};
}
return{run,csv,inspectModel,inspectState};
})();
