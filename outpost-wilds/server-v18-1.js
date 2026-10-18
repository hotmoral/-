const fs=require('fs');
const Module=require('module');
const {patchSource:patchV18}=require('./server-v18.js');

function patchSource(input){
  let src=patchV18(input);
  src=src.replace(/version:18/g,'version:18.1').replace(/\[V18 persistence\]/g,'[V18.1 persistence]').replace(/Outpost Wilds V18/g,'Outpost Wilds V18.1').replace(/V18 bootstrap failed/g,'V18.1 bootstrap failed');
  const anchor='function zoneAt(x,y)';
  if(!src.includes(anchor))throw new Error('[V18.1 patch] compact-layout anchor missing');
  const layout=`\n/* V18.1 compact base-centered layout. Shared by construction, defense fire and snapshots. */\nObject.assign(PAD_POS,{\n base:{x:1800,y:1980},gear:{x:1800,y:1590},\n workshop:{x:1580,y:1900},storage:{x:1580,y:1740},farm:{x:1680,y:2020},\n watchtower:{x:1950,y:1620},forge:{x:1650,y:1620},infirmary:{x:2020,y:1760},\n wall:{x:2050,y:2035},turret:{x:2010,y:1900},turret2:{x:1925,y:2020}\n});\nObject.assign(STASH_POS,{x:1685,y:1810});\nObject.assign(SIGNAL_POS,{x:1800,y:2160});\nObject.assign(V16_WALL_PAD,{x:2050,y:2035});\nObject.assign(V16_BASE_REPAIR,{x:1885,y:1875});\n`;
  src=src.replace(anchor,layout+'\n'+anchor);
  return src;
}
module.exports={patchSource};
if(require.main===module){
  const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
