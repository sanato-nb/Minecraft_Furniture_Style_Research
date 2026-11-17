/* 1-2-G Entry1 reproducible byte-level PNG auditor.
   Input: GitHub fetch_file(encoding="base64") content, NOT UTF-8 decoded PNG.
   No third-party dependencies. Decodes zlib/deflate and PNG filters; hashes
   raw file, Git blob, full RGBA pixel buffer independently of Pillow/C.
   SHA-256 of full raster is not identical to Git's blob SHA-1.
   Noninterlaced PNG, color types 0/2/3/4/6 supported. Unsupported cases fail closed.
*/
globalThis.G_ENTRY1_PNG = (() => {
const U=x=>x>>>0, rol=(x,n)=>(x<<n)|(x>>>(32-n)), rr=(x,n)=>(x>>>n)|(x<<(32-n));
const primes=[];for(let p=2;primes.length<64;p++)if(primes.every(q=>p%q))primes.push(p);
const K=primes.map(p=>U(Math.floor((Math.cbrt(p)%1)*4294967296)));
const INITIAL=primes.slice(0,8).map(p=>U(Math.floor((Math.sqrt(p)%1)*4294967296)));
function hash(data,alg){
 const b=new Uint8Array(Math.ceil((data.length+9)/64)*64);b.set(data);b[data.length]=128;
 const len=BigInt(data.length)*8n;for(let j=0;j<8;j++)b[b.length-1-j]=Number(len>>BigInt(j*8)&255n);
 let h=alg==="sha1"?[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]:INITIAL.slice();
 for(let pos=0;pos<b.length;pos+=64){
 const w=new Uint32Array(alg==="sha1"?80:64);
 for(let j=0;j<16;j++)w[j]=U((b[pos+j*4]<<24)|(b[pos+j*4+1]<<16)|(b[pos+j*4+2]<<8)|b[pos+j*4+3]);
 if(alg==="sha1"){
 for(let j=16;j<80;j++)w[j]=rol(w[j-3]^w[j-8]^w[j-14]^w[j-16],1);
 let[a,c,d,e,f]=h;
 for(let j=0;j<80;j++){
 let t,k;if(j<20){t=(c&d)|(~c&e);k=0x5a827999}else if(j<40){t=c^d^e;k=0x6ed9eba1}else if(j<60){t=(c&d)|(c&e)|(d&e);k=0x8f1bbcdc}else{t=c^d^e;k=0xca62c1d6}
 const z=U(rol(a,5)+t+f+k+w[j]);f=e;e=d;d=rol(c,30);c=a;a=z;
 }
 h=[U(h[0]+a),U(h[1]+c),U(h[2]+d),U(h[3]+e),U(h[4]+f)];
 }else{
 for(let j=16;j<64;j++){const a=rr(w[j-15],7)^rr(w[j-15],18)^(w[j-15]>>>3),c=rr(w[j-2],17)^rr(w[j-2],19)^(w[j-2]>>>10);w[j]=U(w[j-16]+a+w[j-7]+c)}
 let[a,c,d,e,f,g,i,jj]=h;for(let j=0;j<64;j++){
 const x=U(jj+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&i))+K[j]+w[j]);
 const y=U((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)));
 jj=i;i=g;g=f;f=U(e+x);e=d;d=c;c=a;a=U(x+y);
 }
 h=[U(h[0]+a),U(h[1]+c),U(h[2]+d),U(h[3]+e),U(h[4]+f),U(h[5]+g),U(h[6]+i),U(h[7]+jj)];
 }}return h.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function fromBase64(s){const tab="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];let acc=0,n=0;for(let ch of s){if(ch==="=")break;const z=tab.indexOf(ch);if(z<0)continue;acc=(acc<<6)|z;n+=6;if(n>=8){n-=8;out.push((acc>>n)&255)}}return Uint8Array.from(out)}
function gitSHA(b){const h=("blob "+b.length+"\\0").replace("\\0","\0").split("").map(x=>x.charCodeAt(0));const all=new Uint8Array(h.length+b.length);all.set(h);all.set(b,h.length);return hash(all,"sha1")}
function u32(b,o){return U(b[o]*16777216+(b[o+1]<<16)+(b[o+2]<<8)+b[o+3])}
function concat(parts){const out=new Uint8Array(parts.reduce((v,p)=>v+p.length,0));let o=0;for(let p of parts){out.set(p,o);o+=p.length}return out}
function unzlib(b,want){
 if((b[0]&15)!==8||((b[0]<<8)|b[1])%31!==0||(b[1]&32))throw Error("zlib header");
 let at=16,pos=0,out=new Uint8Array(want);
 function take(n){let v=0;for(let k=0;k<n;k++){if((at>>3)>=b.length-4)throw Error("deflate EOF");v|=((b[at>>3]>>(at&7))&1)<<k;at++}return v}
 function table(lens){let cnt=Array(16).fill(0),next=Array(16).fill(0),map=new Map(),max=0;for(let n of lens)if(n){cnt[n]++;max=Math.max(max,n)}let code=0;for(let k=1;k<=15;k++){code=(code+cnt[k-1])*2;next[k]=code}for(let sym=0;sym<lens.length;sym++){const n=lens[sym];if(!n)continue;let v=next[n]++,rev=0;for(let k=0;k<n;k++)rev=(rev<<1)|((v>>k)&1);map.set(n*65536+rev,sym)}return{map,max}}
 function symbol(t){let v=0;for(let k=1;k<=t.max;k++){v|=take(1)<<(k-1);const s=t.map.get(k*65536+v);if(s!==undefined)return s}throw Error("Huffman code")}
 const LB=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258],LE=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0];
 const DB=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577],DE=[0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13];
 let last=false,loops=0;while(!last){if(++loops>10000)throw Error("deflate block overflow");last=!!take(1);const typ=take(2);
 if(typ===0){at=Math.ceil(at/8)*8;const n=take(16),inv=take(16);if((n^inv)!==65535)throw Error("stored block length");for(let j=0;j<n;j++){if(pos>=want)throw Error("inflate overflow");out[pos++]=take(8)}continue}
 let lit,dist;
 if(typ===1){lit=table(Array.from({length:288},(_,i)=>i<=143?8:i<=255?9:i<=279?7:8));dist=table(Array(32).fill(5))}
 else if(typ===2){const nl=take(5)+257,nd=take(5)+1,nc=take(4)+4,order=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15],lens=Array(19).fill(0);
 for(let i=0;i<nc;i++)lens[order[i]]=take(3);const ct=table(lens),code=[];
 while(code.length<nl+nd){const s=symbol(ct);if(s<=15)code.push(s);else if(s===16){if(!code.length)throw Error("repeat 16");let n=take(2)+3;while(n--)code.push(code.at(-1))}else if(s===17){let n=take(3)+3;while(n--)code.push(0)}else{let n=take(7)+11;while(n--)code.push(0)}if(code.length>nl+nd)throw Error("code length overflow")}
 lit=table(code.slice(0,nl));dist=table(code.slice(nl));
 }else throw Error("deflate block type");
 let guard=0;for(;;){if(++guard>want*3+100)throw Error("deflate output guard");const s=symbol(lit);if(s===256)break;if(s<256){if(pos>=want)throw Error("literal overrun");out[pos++]=s;continue}
 const z=s-257;if(z<0||z>=LB.length)throw Error("length symbol");let n=LB[z]+take(LE[z]),di=symbol(dist);if(di>=DB.length)throw Error("distance symbol");const back=DB[di]+take(DE[di]);if(back>pos)throw Error("backref source underflow");while(n--){if(pos>=want)throw Error("backref overflow");out[pos]=out[pos-back];pos++}}
 }
 if(pos!==want)throw Error("deflate size mismatch "+pos+"/"+want);
 let a=1,c=0;for(let x of out){a=(a+x)%65521;c=(c+a)%65521}
 if(U((c<<16)|a)!==u32(b,b.length-4))throw Error("Adler32 mismatch");
 return out;
}
const CRCT=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;return U(c)});
function crc(b,from,to){let x=0xffffffff;for(let i=from;i<to;i++)x=CRCT[(x^b[i])&255]^(x>>>8);return U(x^0xffffffff)}
function png(b){
 if([137,80,78,71,13,10,26,10].some((v,i)=>v!==b[i]))throw Error("PNG signature");
 let o=8,ih=null,pal=null,trns=null,idat=[],chunks=[],endSeen=false;
 while(o+12<=b.length){const n=u32(b,o),end=o+8+n;if(end+4>b.length)throw Error("PNG chunk overrun");
 const kind=String.fromCharCode(...b.slice(o+4,o+8));if(crc(b,o+4,end)!==u32(b,end))throw Error("PNG CRC "+kind);
 chunks.push(kind);const chunk=b.slice(o+8,end);if(kind==="IHDR")ih=chunk;else if(kind==="PLTE")pal=chunk;else if(kind==="tRNS")trns=chunk;else if(kind==="IDAT")idat.push(chunk);
 o=end+4;if(kind==="IEND"){endSeen=true;break}}
 if(!endSeen||o!==b.length||!ih||ih.length!==13||!idat.length)throw Error("PNG structure");
 const w=u32(ih,0),h=u32(ih,4),depth=ih[8],typ=ih[9],channels={0:1,2:3,3:1,4:2,6:4}[typ],interlace=ih[12];
 if(!channels||w<1||h<1||w*h>10000000||ih[10]!==0||ih[11]!==0||interlace!==0)throw Error("unsupported PNG color/interlace");
 if(![1,2,4,8,16].includes(depth))throw Error("unsupported PNG bit depth");
 const stride=Math.ceil(w*channels*depth/8),bpp=Math.max(1,Math.ceil(channels*depth/8));
 const raw=unzlib(concat(idat),h*(stride+1)),rows=new Uint8Array(stride*h);let pos=0;
 for(let y=0;y<h;y++){const filter=raw[pos++];if(filter>4)throw Error("PNG filter");for(let x=0;x<stride;x++){
 const v=raw[pos++],i=y*stride+x,a=x>=bpp?rows[i-bpp]:0,u=y?rows[i-stride]:0,c=y&&x>=bpp?rows[i-stride-bpp]:0;
 let pred=0;if(filter===1)pred=a;else if(filter===2)pred=u;else if(filter===3)pred=Math.floor((a+u)/2);else if(filter===4){const z=a+u-c,da=Math.abs(z-a),du=Math.abs(z-u),dc=Math.abs(z-c);pred=da<=du&&da<=dc?a:du<=dc?u:c}
 rows[i]=(v+pred)&255}}
 const rgba=new Uint8Array(w*h*4),alpha={opaque:0,transparent:0,partial:0},unique=new Set();
 const get=(y,x,c)=>{const bit=(x*channels+c)*depth,i=y*stride+(bit>>3);return depth===8||depth===16?rows[i]:(rows[i]>>(8-depth-(bit&7)))&((1<<depth)-1)};
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){let R=0,G=0,B=0,A=255;
 if(typ===3){const j=get(y,x,0);if(!pal||j*3+2>=pal.length)throw Error("palette index");R=pal[j*3];G=pal[j*3+1];B=pal[j*3+2];A=trns&&j<trns.length?trns[j]:255}
 else if(typ===2){R=get(y,x,0);G=get(y,x,1);B=get(y,x,2);if(trns&&R===trns[1]&&G===trns[3]&&B===trns[5])A=0}
 else if(typ===6){R=get(y,x,0);G=get(y,x,1);B=get(y,x,2);A=get(y,x,3)}
 else if(typ===0){R=G=B=Math.round(255*get(y,x,0)/((1<<Math.min(depth,8))-1));if(trns&&R===trns[1])A=0}
 else if(typ===4){R=G=B=get(y,x,0);A=get(y,x,1)}
 const j=(y*w+x)*4;rgba[j]=R;rgba[j+1]=G;rgba[j+2]=B;rgba[j+3]=A;unique.add(A);
 if(A===255)alpha.opaque++;else if(A===0)alpha.transparent++;else alpha.partial++;
 }
 return {width:w,height:h,bit_depth:depth,color_type:typ,interlace,mode:({0:"L",2:"RGB",3:"P",4:"LA",6:"RGBA"})[typ],alpha,unique_alpha_values:unique.size,chunk_types:chunks.join("|"),
 rgba_sha256:hash(rgba,"sha256"),
 first_square_raster_rgba_sha256:h>=w?hash(rgba.slice(0,w*w*4),"sha256"):"",
 first16_rows_rgba_sha256:h>=16?hash(rgba.slice(0,16*w*4),"sha256"):""};
}
return {fromBase64,hash,gitSHA,png,readFileBase64:s=>{const b=fromBase64(s);return {byte_length:b.length,git_blob_sha:gitSHA(b),file_sha256:hash(b,"sha256"),...png(b)}}};
})();

/* Connector batch entrypoint. Execute from a code-mode session with:
   (0,eval)(await fetch_file(...).result.content);
   await G_ENTRY1_PNG.runBatch(tools, 0); // then starts 18, 36, ..., 180
   Each batch writes a provenance-stamped JSON evidence checkpoint.
   The script deliberately does not approve Entry1 by itself.
*/
G_ENTRY1_PNG.csvObjects=function(s){
 const lines=[],row=[],h=[];let out=[],cur="",quot=false;
 for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){if(quot&&s[i+1]==='"'){cur+='"';i++}else quot=!quot}
 else if(c===','&&!quot){row.push(cur);cur=""}
 else if((c==='\n'||c==='\r')&&!quot){if(c==='\r'&&s[i+1]==='\n')i++;row.push(cur);if(row.some(x=>x!==""))out.push(row.splice(0));else row.length=0;cur=""}
 else cur+=c}
 if(row.length||cur){row.push(cur);out.push(row.slice())}
 const header=out.shift()||[];
 return out.map(x=>Object.fromEntries(header.map((key,i)=>[key,x[i]??""])));
};
G_ENTRY1_PNG.runBatch=async function(tools,start){
 const repo="sanato-nb/Minecraft_Furniture_Style_Research";
 const root="research/vanilla_models/phase_1-2-G/entry1/";
 const get=async path=>(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path})).result;
 const [queue,prior,cross]=await Promise.all([
   get(root+"G_ENTRY1_QUEUE_347.csv"),
   get("research/vanilla_models/phase_1-2-C/entry5/C_PNG_UNIQUE_ALL.csv"),
   get(root+"G_SOURCE_CROSSWALK.csv")
 ]);
 const all=this.csvObjects(queue.content).filter(x=>x.asset_type==="BLOCK_TEXTURE_PNG");
 if(all.length!==185)throw Error("unexpected number of Entry1 PNG paths: "+all.length);
 const C=new Map(this.csvObjects(prior.content).map(x=>[x.png_path,x]));
 const G=new Map(this.csvObjects(cross.content).map(x=>[x.source_path,x]));
 const input=all.slice(start,start+18),results=[];
 for(const row of await Promise.all(input.map(async q=>{
   try{return {q,remote:(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:q.source_path,encoding:"base64"})).result}}
   catch(e){return {q,error:String(e)}}
 }))){
  const {q,remote,error}=row,c=C.get(q.source_path),g=G.get(q.source_path);
  const r={index:Number(q.G_global_index),source_path:q.source_path,expected_git_blob_sha:q.git_blob_sha,
  bytes:0,binary_fetched:false,signature_valid:false,git_blob_sha_computed:"",github_content_sha:"",
  git_sha_match:false,file_sha256:"",png_crc_and_zlib_adler32:"NOT_CHECKED",png_decode:"NOT_CHECKED",
  width:null,height:null,mode:"",bit_depth:null,color_type:null,interlace:null,
  rgba_sha256:"",opaque_pixels:null,transparent_pixels:null,partial_alpha_pixels:null,unique_alpha_values:null,
  C_status:c?"C_PRIOR_RGBA_VERIFIED":"C_OUTSIDE_PRIOR_1073",
  C_expected_rgba_sha256:c?.rgba_sha256??"",C_rgba_match:c?false:null,C_dimensions_mode_alpha_match:c?false:null,
  C_mcmeta_path:c?.mcmeta_path??"",C_mcmeta_git_sha:c?.mcmeta_sha??"",
  F_visual_prior:g?.F_visual_prior??"",first_square_raster_rgba_sha256:"",
  error:""};
  try{
   if(error)throw Error("base64 fetch: "+error);
   const data=this.readFileBase64(remote.content);
   r.binary_fetched=true;r.bytes=data.byte_length;r.signature_valid=true;
   r.git_blob_sha_computed=data.git_blob_sha;r.github_content_sha=remote.sha;
   r.git_sha_match=data.git_blob_sha===q.git_blob_sha&&remote.sha===q.git_blob_sha;
   r.file_sha256=data.file_sha256;r.png_crc_and_zlib_adler32="PASS_FULL_CRC_ADLER";
   r.png_decode="PASS_FULL_RASTER_RGBA";r.width=data.width;r.height=data.height;
   r.mode=data.mode;r.bit_depth=data.bit_depth;r.color_type=data.color_type;r.interlace=data.interlace;
   r.rgba_sha256=data.rgba_sha256;r.opaque_pixels=data.alpha.opaque;
   r.transparent_pixels=data.alpha.transparent;r.partial_alpha_pixels=data.alpha.partial;
   r.unique_alpha_values=data.unique_alpha_values;
   r.first_square_raster_rgba_sha256=data.first_square_raster_rgba_sha256;
   if(c){
    r.C_rgba_match=r.rgba_sha256===c.rgba_sha256;
    r.C_dimensions_mode_alpha_match=[
     r.width,r.height,r.mode,r.opaque_pixels,r.transparent_pixels,r.partial_alpha_pixels,r.unique_alpha_values
    ].join("|") === [
     c.width,c.height,c.mode,c.opaque_pixels,c.transparent_pixels,c.partial_alpha_pixels,c.unique_alpha_values
    ].join("|");
   }
   if(!r.git_sha_match||r.C_rgba_match===false||r.C_dimensions_mode_alpha_match===false)
    throw Error("Independent Git SHA / C RGBA / C dimension-mode-alpha mismatch");
  }catch(e){r.error=String(e)}
  results.push(r);
 }
 const body={schema:"G_ENTRY1_PNG_BINARY_BATCH/v1",baseline_head:"2d6c570e2a1406f603451faa35c4de5f4eb5ed18",
  source_queue_blob_sha:queue.sha,prior_C_blob_sha:prior.sha,prior_crosswalk_blob_sha:cross.sha,
  start_index:start,end_index_exclusive:start+input.length,
  count:results.length,success_count:results.filter(x=>x.binary_fetched&&x.git_sha_match&&x.png_decode==="PASS_FULL_RASTER_RGBA"&&!x.error).length,
  records:results};
 const fileName=root+"binary_batches/G_ENTRY1_PNG_BINARY_BATCH_"+String(start).padStart(3,"0")+".json";
 const commit=await tools.mcp__GitHub__create_file({repository_full_name:repo,path:fileName,
   content:JSON.stringify(body,null,2)+"\n",message:"1-2-G Entry1: PNG 원본 바이너리 배치 "+start+"~"+(start+input.length-1)+" 검증",branch:"main"});
 return {start,number:results.length,success:body.success_count,errors:results.filter(x=>x.error).map(x=>({path:x.source_path,error:x.error})),file:fileName,commit:commit.result.commit_sha,
  C_matched:results.filter(x=>x.C_rgba_match).length,C_outside:results.filter(x=>x.C_status==="C_OUTSIDE_PRIOR_1073").length};
};
