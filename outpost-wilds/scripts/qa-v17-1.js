const assert=require('assert'),fs=require('fs'),path=require('path');
const {patchSource}=require('../server-v17-1.js');
const base=fs.readFileSync(path.join(__dirname,'..','server-v13.js'),'utf8'),src=patchSource(base);
assert(src.includes('(ws.bufferedAmount||0)>262144'),'snapshot backpressure guard missing');
assert(src.includes('(c.bufferedAmount||0)<=262144'),'broadcast backpressure guard missing');
assert(!src.includes("setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)"),'duplicate delayed ambient respawn still present');
assert(src.includes("shape:'square'"),'V17 square wall must remain intact');
new Function(src);
console.log('[QA V17.1] PASS · websocket backpressure · single ambient respawn authority · V17 fortification preserved');
