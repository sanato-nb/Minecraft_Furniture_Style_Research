// Pure JavaScript helper for v17 research. No network or side effects.
// Returns helpers via expression evaluation. Built to process pinned upstream
// textures and generate derived sample metrics only; never republish PNG pixels.
(()=>{
function csvRead(s){let rows=[],row=[],v="",q=false;for(let i=0;i<s.length;i++){const c=s[i];if(q){if(c==='"'&&s[i+1]==='"'){v+='"';i++;}else if(c==='"')q=false;else v+=c;}else if(c==='"')q=true;else if(c===','){row.push(v);v="";}else if(c==='\n'){row.push(v.replace(/\r$/,""));if(row.some(x=>x!==""))rows.push(row);row=[];v="";}else v+=c;}if(v||row.length){row.push(v);rows.push(row);}const h=rows.shift();return rows.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]??""])));}
function csvWrite(rows){if(!rows.length)throw Error("no rows");const cols=Object.keys(rows[0]);const q=x=>{const s=String(x??"");return /[,"\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};return [cols.join(","),...rows.map(r=>cols.map(k=>q(r[k])).join(","))].join("\n")+"\n";}
const alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",lut=Object.fromEntries([...alphabet].map((c,i)=>[c,i]));
function base64Decode(s){let v=0,n=0,o=[];for(const c of s){if(c==="=")break;if(lut[c]===undefined)continue;v=((v<<6)|lut[c])>>>0;n+=6;if(n>=8){n-=8;o.push((v>>>n)&255);}}return new Uint8Array(o);}
const u32=(a,p)=>(a[p]*16777216+a[p+1]*65536+a[p+2]*256+a[p+3])>>>0;
function inflate(z){
 let p=2,b=0,n=0,o=[];
 const read=k=>{while(n<k){if(p>=z.length)throw Error("deflate EOF");b|=z[p++]<<n;n+=8;}const v=b&((1<<k)-1);b>>>=k;n-=k;return v;};
 function tree(lengths){const max=Math.max(...lengths),cnt=Array(max+1).fill(0),next=Array(max+1).fill(0),map=Array.from({length:max+1},()=>new Map());for(const len of lengths)if(len)cnt[len]++;let code=0;for(let k=1;k<=max;k++){code=(code+(cnt[k-1]||0))*2;next[k]=code;}for(let s=0;s<lengths.length;s++)if(lengths[s])map[lengths[s]].set(next[lengths[s]]++,s);return {max,map};}
 function sym(t){let code=0;for(let k=1;k<=t.max;k++){code=(code<<1)|read(1);const s=t.map[k].get(code);if(s!==undefined)return s;}throw Error("huffman decode");}
 const fixedLit=tree(Array.from({length:288},(_,i)=>i<144?8:i<256?9:i<280?7:8)),fixedDist=tree(Array(32).fill(5));
 const lenBase=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258];
 const lenExtra=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0];
 const distBase=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577];
 const distExtra=Array.from({length:30},(_,i)=>i<4?0:Math.floor((i-2)/2));
 let end=0;while(!end){end=read(1);const typ=read(2);
  if(typ===0){b=0;n=0;const size=z[p]+256*z[p+1],comp=z[p+2]+256*z[p+3];p+=4;if((size^65535)!==comp)throw Error("stored block length");for(let i=0;i<size;i++)o.push(z[p++]);continue;}
  if(typ===3)throw Error("invalid DEFLATE block type");
  let lit,dist;
  if(typ===1){lit=fixedLit;dist=fixedDist;}
  else{const nl=read(5)+257,nd=read(5)+1,nc=read(4)+4,order=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15],codes=Array(19).fill(0);for(let i=0;i<nc;i++)codes[order[i]]=read(3);const cltree=tree(codes),ll=[];while(ll.length<nl+nd){const s=sym(cltree);if(s<16){ll.push(s);continue;}const ct=s===16?read(2)+3:s===17?read(3)+3:read(7)+11,fill=s===16?ll.at(-1):0;for(let k=0;k<ct;k++)ll.push(fill);}lit=tree(ll.slice(0,nl));dist=tree(ll.slice(nl,nl+nd));}
  while(true){const s=sym(lit);if(s<256){o.push(s);continue;}if(s===256)break;const k=s-257;if(k<0||k>28)throw Error("bad length");const count=lenBase[k]+read(lenExtra[k]),ds=sym(dist);if(ds>29)throw Error("bad distance");const back=distBase[ds]+read(distExtra[ds]);if(back>o.length)throw Error("back beyond output");for(let i=0;i<count;i++)o.push(o[o.length-back]);}
 }
 return new Uint8Array(o);
}
function pngDecode(raw){
 if(String.fromCharCode(...raw.slice(1,4))!=="PNG")throw Error("invalid png");
 const w=u32(raw,16),h=u32(raw,20),depth=raw[24],mode=raw[25],ch=({2:3,3:1,6:4})[mode];
 if(depth!==8||!ch)throw Error("unsupported PNG color type "+mode+" depth "+depth);
 let chunks=[],pal=[],transparent=[],p=8;while(p<raw.length){const n=u32(raw,p),tag=String.fromCharCode(...raw.slice(p+4,p+8)),val=raw.slice(p+8,p+8+n);if(tag==="IDAT")chunks.push(val);if(tag==="PLTE")for(let i=0;i<n;i+=3)pal.push(Array.from(val.slice(i,i+3)));if(tag==="tRNS")transparent=Array.from(val);p+=12+n;if(tag==="IEND")break;}
 const z=new Uint8Array(chunks.reduce((a,v)=>a+v.length,0));let o=0;for(const c of chunks){z.set(c,o);o+=c.length;}
 const data=inflate(z),stride=w*ch;if(data.length!==h*(stride+1))throw Error("incorrect uncompressed size");
 const pixels=new Uint8Array(w*h*4);let prev=new Uint8Array(stride),pos=0,visible=0,invisible=0,partial=0;
 for(let y=0;y<h;y++){const filter=data[pos++],row=new Uint8Array(stride);
  for(let i=0;i<stride;i++){const a=i>=ch?row[i-ch]:0,b=prev[i],c=i>=ch?prev[i-ch]:0;let pr=0;if(filter===1)pr=a;else if(filter===2)pr=b;else if(filter===3)pr=Math.floor((a+b)/2);else if(filter===4){const p=a+b-c,da=Math.abs(p-a),db=Math.abs(p-b),dc=Math.abs(p-c);pr=da<=db&&da<=dc?a:db<=dc?b:c;}else if(filter!==0)throw Error("bad filter "+filter);row[i]=(data[pos++]+pr)&255;}
  for(let x=0;x<w;x++){const i=x*ch,at=(y*w+x)*4;if(mode===6)pixels.set(row.slice(i,i+4),at);else if(mode===2){pixels.set(row.slice(i,i+3),at);pixels[at+3]=255;}else {const k=row[i];pixels.set(pal[k],at);pixels[at+3]=transparent[k]??255;}const alpha=pixels[at+3];if(alpha===0)invisible++;else{visible++;if(alpha<255)partial++;}}
  prev=row;
 }
 if(pos!==data.length)throw Error("extra PNG uncompressed bytes");
 return {w,h,pixels,visible,invisible,partial};
}
function sample(img,face){
 const x0=+face.pixel_x0,y0=+face.pixel_y0,x1=+face.pixel_x1,y1=+face.pixel_y1;
 if(x0<0||y0<0||x1>img.w||y1>img.h||x1<x0||y1<y0)throw Error("rectangle out of PNG");
 const area=(x1-x0)*(y1-y0);let visible=0,invisible=0,partial=0,rs=0,gs=0,bs=0;const colors=new Set();
 for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const at=(y*img.w+x)*4,r=img.pixels[at],g=img.pixels[at+1],b=img.pixels[at+2],a=img.pixels[at+3];if(a===0)invisible++;else{visible++;rs+=r;gs+=g;bs+=b;colors.add([r,g,b,a].join(":"));if(a<255)partial++;}}
 if(area!==visible+invisible||area!==+face.pixel_rect_area)throw Error("face pixel rectangle count mismatch");
 const status=area===0?"zero_uv_area":visible===0?"sampled_fully_transparent":invisible===0&&partial===0?"sampled_all_opaque":partial?"sampled_partial_alpha":"sampled_mixed_opaque_transparent";
 return {leaf:face.leaf,parent:face.parent,element_index:face.element_index,face:face.face,png_name:face.png_name,png_sha:face.png_sha,png_checkpoint:face.png_checkpoint,pixel_x0:x0,pixel_y0:y0,pixel_x1:x1,pixel_y1:y1,uv_reversed:face.uv_reversed,uv_zero_area:face.zero_area,face_uv_rotation:face.source_face_uv_rotation,rect_texels:area,visible_texels:visible,transparent_texels:invisible,partial_alpha_texels:partial,visible_rgba_colors:colors.size,mean_visible_r:visible?+(rs/visible).toFixed(2):"",mean_visible_g:visible?+(gs/visible).toFixed(2):"",mean_visible_b:visible?+(bs/visible).toFixed(2):"",status};
}
return {csvRead,csvWrite,base64Decode,pngDecode,sample};
})()