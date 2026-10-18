const fs=require('fs');
const Module=require('module');
const {patchSource:patchV17}=require('./server-v17.js');

function patchSource(input){
  let src=patchV17(input);
  const sendOld="const send=(ws,p)=>ws.readyState===1&&ws.send(JSON.stringify(p));";
  const sendNew="const send=(ws,p)=>{if(ws.readyState!==1)return false;if((ws.bufferedAmount||0)>262144)return false;ws.send(JSON.stringify(p));return true};";
  if(!src.includes(sendOld))throw new Error('[V17.1 patch] send anchor missing');
  src=src.replace(sendOld,sendNew);
  const broadcastOld="const broadcast=p=>{const s=JSON.stringify(p);for(const c of wss.clients)if(c.readyState===1)c.send(s)};";
  const broadcastNew="const broadcast=p=>{const s=JSON.stringify(p);for(const c of wss.clients)if(c.readyState===1&&(c.bufferedAmount||0)<=262144)c.send(s)};";
  if(!src.includes(broadcastOld))throw new Error('[V17.1 patch] broadcast anchor missing');
  src=src.replace(broadcastOld,broadcastNew);
  const delayed="else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)";
  const n=src.split(delayed).length-1;if(n<2)throw new Error(`[V17.1 patch] expected delayed ambient respawns, found ${n}`);
  src=src.split(delayed).join('');
  src=src.replace(/\[V17 persistence\]/g,'[V17.1 persistence]').replace(/Outpost Wilds V17/g,'Outpost Wilds V17.1').replace(/V17 bootstrap failed/g,'V17.1 bootstrap failed');
  return src;
}
module.exports={patchSource};
if(require.main===module){const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};try{require('./server-v13.js')}finally{Module._extensions['.js']=original}}
