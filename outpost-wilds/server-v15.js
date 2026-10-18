const fs=require('fs');
const Module=require('module');
const {patchSource:patchV14}=require('./server-v14.js');

function patchSource(input){
  let src=patchV14(input);
  const a=src.indexOf('function storeRaidMeat');
  const b=src.indexOf('function nearestEnemy',a);
  if(a<0||b<0)throw new Error('[V15 patch] raid loot block not found');
  const combat=`function recordKill(e){MISSION.kills++;if(e.boss)MISSION.boss++;markDirty()}\nfunction finishEnemy(p,e){enemies.delete(e.id);const reward=e.reward||6,amount=e.raid?0:addCarry(p,'meat',reward),mg=e.merit||4;p.merit+=mg;p.score+=18+reward*2+mg;if(!e.raid){MISSION.meat+=amount;MISSION.gather+=amount}recordKill(e);broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,enemyName:e.bossName||e.type,amount,meritGain:mg,x:e.x,y:e.y,boss:e.boss,lootTo:e.raid?'none':'carry'});if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:p.id,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}\nfunction finishDefenseEnemy(e){enemies.delete(e.id);recordKill(e);if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:null,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}\n`;
  src=src.slice(0,a)+combat+src.slice(b);
  if(!src.includes("const used=Math.min(3,p.meat);"))throw new Error('[V15 patch] eat amount not found');
  src=src.replace("const used=Math.min(3,p.meat);p.meat-=used;const before=p.hp;p.hp=Math.min(p.maxHp,p.hp+used*12);","const used=Math.min(5,p.meat);p.meat-=used;const before=p.hp;p.hp=Math.min(p.maxHp,p.hp+used*10);");
  src=src.replace(/version:14/g,'version:15').replace(/\[V14 persistence\]/g,'[V15 persistence]').replace(/Outpost Wilds V14/g,'Outpost Wilds V15').replace(/V14 bootstrap failed/g,'V15 bootstrap failed');
  return src;
}

module.exports={patchSource};

if(require.main===module){
  const target=require.resolve('./server-v13.js');
  const original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){
    if(filename===target){
      const patched=patchSource(fs.readFileSync(filename,'utf8'));
      return mod._compile(patched,filename);
    }
    return original(mod,filename);
  };
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
