const parts=["./app.part.000.txt","./app.part.001.txt","./app.part.002.txt","./app.part.003.txt","./app.part.004.txt","./app.part.005.txt","./app.part.006.txt","./app.part.007.txt","./app.part.008.txt","./app.part.009.txt","./app.part.010.txt"];
const chunks=await Promise.all(parts.map(async p=>{const r=await fetch(new URL(p,import.meta.url),{cache:"no-store"});if(!r.ok)throw new Error(`PREVIEW_PART_${r.status}_${p}`);return r.text();}));
const url=URL.createObjectURL(new Blob(chunks,{type:"text/javascript"}));
try{await import(url);}finally{URL.revokeObjectURL(url);}
