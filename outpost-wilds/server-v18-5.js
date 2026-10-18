const fs=require('fs');
const Module=require('module');
const {patchSource:patchV184}=require('./server-v18-4.js');

function replaceFunction(src,name,code){
  const sig=`function ${name}(`,start=src.indexOf(sig);
  if(start<0)throw new Error(`[V18.5 patch] function ${name} not found`);
  const brace=src.indexOf('{',start);if(brace<0)throw new Error(`[V18.5 patch] ${name} brace not found`);
  let depth=0,quote=null,esc=false,line=false,block=false;
  for(let i=brace;i<src.length;i++){
    const c=src[i],n=src[i+1];
    if(line){if(c==='\n')line=false;continue}
    if(block){if(c==='*'&&n==='/'){block=false;i++;}continue}
    if(quote){if(esc){esc=false;continue}if(c==='\\'){esc=true;continue}if(c===quote)quote=null;continue}
    if(c==='/'&&n==='/'){line=true;i++;continue}
    if(c==='/'&&n==='*'){block=true;i++;continue}
    if(c==='"'||c==="'"||c==='`'){quote=c;continue}
    if(c==='{')depth++;else if(c==='}'){depth--;if(depth===0)return src.slice(0,start)+code+src.slice(i+1)}
  }
  throw new Error(`[V18.5 patch] unterminated function ${name}`);
}
function insertBefore(src,needle,chunk,label){const i=src.indexOf(needle);if(i<0)throw new Error(`[V18.5 patch] ${label} anchor missing`);return src.slice(0,i)+chunk+src.slice(i)}

function patchSource(input){
  let src=patchV184(input);
  src=src.replace(/version:18\.4/g,'version:18.5')
    .replace(/\[V18\.4 persistence\]/g,'[V18.5 persistence]')
    .replace(/Outpost Wilds V18\.4/g,'Outpost Wilds V18.5')
    .replace(/V18\.4 bootstrap failed/g,'V18.5 bootstrap failed');

  const rangeDefs=`\nconst V185_WEAPON_RANGES=[null,\n {attack:96,gather:88},\n {attack:104,gather:94},\n {attack:112,gather:100},\n {attack:118,gather:120},\n {attack:126,gather:108},\n {attack:138,gather:114},\n {attack:140,gather:132},\n {attack:154,gather:124},\n {attack:170,gather:130},\n {attack:188,gather:138},\n {attack:210,gather:146},\n {attack:360,gather:190},\n {attack:400,gather:210},\n {attack:440,gather:230},\n {attack:480,gather:250},\n {attack:525,gather:275}\n];\n`;
  src=insertBefore(src,'function weaponInfo()',rangeDefs,'range definitions');

  src=replaceFunction(src,'weaponInfo',`function weaponInfo(){const idx=clamp(Number(SHARED_WEAPON.tier)||1,1,V18_WEAPONS.length-1),d=V18_WEAPONS[idx],r=V185_WEAPON_RANGES[idx]||V185_WEAPON_RANGES[1],w={...d};w.damage=d.damage+facilityLevels.forge*2;w.attackRange=r.attack;w.autoRange=r.attack;w.range=r.attack;w.gatherRange=r.gather;w.level=1;w.tier=idx;w.display=d.name;return w}`);
  src=replaceFunction(src,'publicPlayer',`function publicPlayer(p){const w=weaponInfo();return{id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,dir:p.facing>0?0:Math.PI,facing:p.facing,score:p.score,merit:p.merit,gearLevel:w.tier,weaponIndex:w.tier,weaponLevel:1,weapon:w.display,weaponKind:w.kind,attackRange:w.attackRange,autoRange:w.attackRange,gatherRange:w.gatherRange,carry:carryOf(p),carryCap:carryCap(),zone:zoneAt(p.x,p.y),autoTarget:p.autoTarget||null}}`);
  src=replaceFunction(src,'nearestNode',`function nearestNode(p,max){if(carryOf(p)>=carryCap())return null;const limit=Math.max(40,Number(max)||weaponInfo().gatherRange||88);let b=null,d=limit;for(const n of nodes){if(n.respawnAt)continue;const q=Math.hypot(n.x-p.x,n.y-p.y);if(q<d){b=n;d=q}}return b}`);
  src=replaceFunction(src,'autoAction',`function autoAction(p,now,dt){p.autoTarget=null;const w=weaponInfo(),enemy=nearestEnemy(p,w.attackRange);if(enemy){attackEnemy(p,enemy);return'enemy'}if(processFinalActivation(p,dt))return'final';const node=nearestNode(p,w.gatherRange);if(node){gatherNode(p,node);return'resource'}if(processPads(p,now))return'pad';if(processFarm(p,now))return'farm';return null}`);
  return src;
}
module.exports={patchSource};
if(require.main===module){
  const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
