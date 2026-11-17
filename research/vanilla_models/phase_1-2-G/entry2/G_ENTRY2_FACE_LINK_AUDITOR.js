globalThis.G_ENTRY2_FACES=async function(tools,part,sub=null){
const repo="sanato-nb/Minecraft_Furniture_Style_Research",root="research/vanilla_models/phase_1-2-G/entry2/";
const ps=[...Array.from({length:4},(_,i)=>root+"rollup/G_ENTRY2_RECHECK_PART_"+String(i).padStart(2,"0")+".json"),
root+"parents/G_ENTRY2_PARENT_AUX_BATCH_00.json",root+"parents/G_ENTRY2_PARENT_AUX_BATCH_01.json"];
const raw=await Promise.all(ps.map(path=>tools.mcp__GitHub__fetch_file({repository_full_name:repo,path})));
const groups=raw.slice(0,4).map(x=>JSON.parse(x.result.content).rows),models=new Map(groups.flat().filter(x=>x.type==="BLOCK_MODEL_JSON").map(x=>[x.path,{sha:x.sha,json:x.raw_json}]));
for(const r of raw.slice(4).flatMap(x=>JSON.parse(x.result.content).rows))models.set(r.path,{sha:r.computed_sha,json:r.full_json});
const mpath=ref=>{if(!ref)return null;const s=ref.includes(":")?ref.split(":")[1]:ref;return "1.21.11/assets/minecraft/models/"+(s.startsWith("block/")?s:"block/"+s)+".json"};
const texpath=ref=>{if(!ref)return"";const s=ref.includes(":")?ref.split(":")[1]:ref;return "1.21.11/assets/minecraft/textures/"+s+".png"};
const out=[],modelSummary=[],errors=[];
for(const r of groups[part].filter(x=>x.type==="BLOCK_MODEL_JSON").slice(sub==="a"?0:sub==="b"?98:0,sub==="a"?98:sub==="b"?196:undefined)){
 const chain=[],used=new Set();let at=r.path;while(at){if(used.has(at)||!models.has(at)){errors.push({path:r.path,issue:"MISSING_OR_CYCLIC_PARENT:"+at});break}used.add(at);chain.push({path:at,...models.get(at)});at=mpath(models.get(at).json.parent??null)}
 const provider=chain.find(x=>Array.isArray(x.json.elements)&&x.json.elements.length>0);
 const textures={};for(let k=chain.length-1;k>=0;k--)Object.assign(textures,chain[k].json.textures||{});
 function resolve(raw){let t=raw,seen=new Set(),trace=[];while(typeof t==="string"&&t.startsWith("#")){const key=t.slice(1);if(seen.has(key))return{value:"",trace,reason:"CYCLE"};seen.add(key);trace.push(key);t=textures[key]}return{value:typeof t==="string"&&t.length?t:"",trace,reason:t?"":"TEMPLATE_UNBOUND"}}
 const elems=provider?.json.elements||[];let bound=0,unbound=0,UV=0;
 for(let i=0;i<elems.length;i++)for(const [direction,face] of Object.entries(elems[i].faces||{})){
 const z=resolve(face.texture),yes=Boolean(z.value);if(yes)bound++;else unbound++;
 if(Object.hasOwn(face,"uv"))UV++;
 out.push({model_path:r.path,model_sha:r.sha,provider_path:provider?.path||"",provider_sha:provider?.sha||"",
 element_index:i,face_direction:direction,face_texture_original:face.texture||"",texture_alias_chain:z.trace.join(">"),
 resolved_source_texture_path:yes?texpath(z.value):"",G_PNG_bound:yes?"YES":"TEMPLATE_UNBOUND",
 UV_key_explicit:Object.hasOwn(face,"uv")?"YES":"NO",UV_original_json:JSON.stringify(face.uv??null),
 cullface_key_explicit:Object.hasOwn(face,"cullface")?"YES":"NO",cullface_value:face.cullface??"",
 tintindex_key_explicit:Object.hasOwn(face,"tintindex")?"YES":"NO",tintindex_value:face.tintindex??"",face_raw_json:JSON.stringify(face)});
 }
 modelSummary.push({model:r.path,faces:bound+unbound,bound,unbound,UV});
}
const fields=Object.keys(out[0]||{});const esc=x=>{let s=String(x??"");return /[,"\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s};
const csv=fields.join(",")+"\n"+out.map(x=>fields.map(k=>esc(x[k])).join(",")).join("\n")+"\n";
const name=root+"face_shards/G_ENTRY2_SOURCE_FACE_TEXTURE_PART_"+String(part).padStart(2,"0")+(sub||"")+".csv";
const created=await tools.mcp__GitHub__create_file({repository_full_name:repo,path:name,content:csv,message:"1-2-G Entry2: 실제 부모 모델 기반 face·UV·텍스처 독립 원장 "+(part+1)+"/4",branch:"main"});
return{part,models:modelSummary.length,faces:out.length,UV:modelSummary.reduce((a,x)=>a+x.UV,0),bound:modelSummary.reduce((a,x)=>a+x.bound,0),unbound:modelSummary.reduce((a,x)=>a+x.unbound,0),errors,bytes:csv.length,path:name,commit:created.result.commit_sha};
};