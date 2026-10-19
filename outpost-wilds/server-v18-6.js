const fs=require('fs');
const Module=require('module');
const {patchSource:patchV185}=require('./server-v18-5.js');
function patchSource(input){
  return patchV185(input)
    .replace(/version:18\.5/g,'version:18.6')
    .replace(/\[V18\.5 persistence\]/g,'[V18.6 persistence]')
    .replace(/Outpost Wilds V18\.5/g,'Outpost Wilds V18.6')
    .replace(/V18\.5 bootstrap failed/g,'V18.6 bootstrap failed');
}
module.exports={patchSource};
if(require.main===module){
  const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
