const fs=require('fs');
const Module=require('module');
const {patchSource:patchV181}=require('./server-v18-1.js');

function patchSource(input){
  let src=patchV181(input);
  src=src.replace(/version:18\.1/g,'version:18.2')
    .replace(/\[V18\.1 persistence\]/g,'[V18.2 persistence]')
    .replace(/Outpost Wilds V18\.1/g,'Outpost Wilds V18.2')
    .replace(/V18\.1 bootstrap failed/g,'V18.2 bootstrap failed');
  return src;
}
module.exports={patchSource};
if(require.main===module){
  const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
