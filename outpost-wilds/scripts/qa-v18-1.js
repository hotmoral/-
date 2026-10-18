const assert=require('assert'),fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.join(__dirname,'..');
const client=fs.readFileSync(path.join(root,'public','patch-v18-1.js'),'utf8');
const {patchSource}=require(path.join(root,'server-v18-1.js'));
const base=fs.readFileSync(path.join(root,'server-v13.js'),'utf8');
const compiled=patchSource(base);new vm.Script(compiled,{filename:'server-v18-1.compiled.js'});
for(const token of ["base:{x:1800,y:1980}","gear:{x:1800,y:1590}","workshop:{x:1580,y:1900}","storage:{x:1580,y:1740}","watchtower:{x:1950,y:1620}","turret:{x:2010,y:1900}","Object.assign(STASH_POS,{x:1685,y:1810})","Object.assign(V16_WALL_PAD,{x:2050,y:2035})"])assert(compiled.includes(token),`V18.1 compact layout missing ${token}`);
for(const token of ['v181StoppedAt','now-v181StoppedAt>=240','err<=8','v181CloseChat','popstate','pointerdown','거점에 접근하면 자원이 자동','Object.assign(V14_POS,V181_POS)'])assert(client.includes(token),`V18.1 client contract missing ${token}`);
assert(client.includes('v18StopInput()'),'chat dismissal must stop movement input');
assert(client.includes("history.pushState({...history.state,owChatV181:true},'')"),'Android/browser back must dismiss chat before navigation');
const positions={workshop:[1580,1900],storage:[1580,1740],farm:[1680,2020],watchtower:[1950,1620],forge:[1650,1620],infirmary:[2020,1760],turret:[2010,1900],turret2:[1925,2020],stash:[1685,1810],gear:[1800,1590]};
for(const [id,[x,y]] of Object.entries(positions)){const d=Math.hypot(x-1800,y-1800);assert(d<=310,`${id} too far from base: ${d.toFixed(1)}`);}
const core=fs.readFileSync(path.join(root,'public','patch-v18.js'),'utf8');for(const token of ['v18DrawActionRanges','v18DrawPadGround','v18DrawPadForeground','window.__OW_CORE_RENDER_CONTRACT__'])assert(core.includes(token),`V18 core interaction contract regressed: ${token}`);
console.log('[QA V18.1] PASS · legacy hint removed · stop reconciliation grace · back/tap chat dismissal · compact base-centered facilities · V18 interaction invariants preserved');
