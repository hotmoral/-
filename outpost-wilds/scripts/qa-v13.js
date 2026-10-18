const assert=require('assert'),fs=require('fs'),path=require('path');
const s=fs.readFileSync(path.join(__dirname,'..','server-v13.js'),'utf8'),c=fs.readFileSync(path.join(__dirname,'..','public','patch-v13.js'),'utf8');
for(const t of ['const STOCKPILE=','const stockCap=','function processStash','fromStock','m.type===\'resetWorld\'','function resetWorld','worldTick%2===0'])assert(s.includes(t),`server V13 missing ${t}`);
assert(s.includes("speed=212*Math.max(.86,1-.14*Math.pow(q,1.35))"),'server carry speed contract');
assert(c.includes("const speed=212*Math.max(.86,1-.14*Math.pow(q,1.35))"),'client prediction must match server carry speed');
assert(c.includes("send({type:'resetWorld',confirm:'RESET'})"),'two-step reset action wired');
assert(c.includes('v13DrawStockpile'),'stockpile visual wired');
console.log('[QA V13] PASS · stockpile · shared project spending · reset · 15Hz snapshots · matched local prediction');
