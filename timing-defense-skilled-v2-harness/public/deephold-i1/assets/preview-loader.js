const parts=Array.from({length:28},(_,i)=>`./app.gz.b64.part.${String(i).padStart(3,"0")}.txt`);
const encoded=(await Promise.all(parts.map(async p=>{const r=await fetch(new URL(p,import.meta.url),{cache:"no-store"});if(!r.ok)throw new Error(`PREVIEW_PART_${r.status}_${p}`);return r.text();}))).join("");
const bytes=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));
const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
const source=await new Response(stream).text();
const url=URL.createObjectURL(new Blob([source],{type:"text/javascript"}));
try{await import(url);}finally{URL.revokeObjectURL(url);}
