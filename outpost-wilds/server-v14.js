const fs=require('fs');
const path=require('path');
const Module=require('module');

function replaceOnce(src,from,to,label){
  if(!src.includes(from))throw new Error(`[V14 patch] missing ${label}`);
  return src.replace(from,to);
}

function patchSource(input){
  let src=input;
  src=src.replace(/version:13/g,'version:14').replace(/\[V13 persistence\]/g,'[V14 persistence]').replace(/Outpost Wilds V13/g,'Outpost Wilds V14').replace(/V13 bootstrap failed/g,'V14 bootstrap failed');

  src=replaceOnce(src,
    "function recordKill(e){MISSION.kills++;if(e.boss)MISSION.boss++;markDirty()}\nfunction finishEnemy(p,e){enemies.delete(e.id);const amount=addCarry(p,'meat',e.reward||6),mg=e.merit||4;p.merit+=mg;p.score+=18+amount*2+mg;MISSION.meat+=amount;MISSION.gather+=amount;recordKill(e);broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,enemyName:e.bossName||e.type,amount,meritGain:mg,x:e.x,y:e.y,boss:e.boss});if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:p.id,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}\nfunction finishDefenseEnemy(e){enemies.delete(e.id);recordKill(e);if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:null,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}",
    "function recordKill(e){MISSION.kills++;if(e.boss)MISSION.boss++;markDirty()}\nfunction storeRaidMeat(e,playerId){const reward=Math.max(0,e.reward||0),free=Math.max(0,stockCap()-stockOf()),stored=Math.min(reward,free),overflow=reward-stored;if(stored>0){STOCKPILE.meat+=stored;MISSION.meat+=stored;MISSION.gather+=stored;markDirty()}broadcast({type:'event',kind:'raidLoot',playerId,amount:stored,overflow,stockpile:{...STOCKPILE},capacity:stockCap(),x:e.x,y:e.y});return stored}\nfunction finishEnemy(p,e){enemies.delete(e.id);const reward=e.reward||6,amount=e.raid?storeRaidMeat(e,p.id):addCarry(p,'meat',reward),mg=e.merit||4;p.merit+=mg;p.score+=18+reward*2+mg;if(!e.raid){MISSION.meat+=amount;MISSION.gather+=amount}recordKill(e);broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,enemyName:e.bossName||e.type,amount,meritGain:mg,x:e.x,y:e.y,boss:e.boss,lootTo:e.raid?'stockpile':'carry'});if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:p.id,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}\nfunction finishDefenseEnemy(e){enemies.delete(e.id);if(e.raid)storeRaidMeat(e,null);recordKill(e);if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:null,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>{if(ENDGAME.mode!=='final')spawnPressureEnemy(false)},14000)}",
    'raid meat routing');

  src=replaceOnce(src,
    "target.hp-=damage+lv*8;broadcast({type:'event',kind:'towerShot',source:fid,x1:PAD_POS[fid].x,y1:PAD_POS[fid].y,x2:target.x,y2:target.y});if(target.hp<=0)finishDefenseEnemy(target)",
    "const hit=damage+lv*8;target.hp-=hit;broadcast({type:'event',kind:'towerShot',source:fid,level:lv,damage:hit,targetId:target.id,targetType:target.type,x1:PAD_POS[fid].x,y1:PAD_POS[fid].y,x2:target.x,y2:target.y});if(target.hp<=0)finishDefenseEnemy(target)",
    'tower shot payload');
  src=replaceOnce(src,"fire('watchtower',430,18,false,1.03)","fire('watchtower',430,18,true,1.03)",'watchtower hostile targeting');

  src=replaceOnce(src,'lastStash:0,input:{x:0,y:0}',"lastStash:0,lastChat:0,input:{x:0,y:0}",'chat cooldown state');
  src=replaceOnce(src,
    "else if(m.type==='name'&&typeof m.name==='string')p.name=m.name.trim().slice(0,14)||p.name;else if(m.type==='endless'&&ENDGAME.mode==='cleared')",
    "else if(m.type==='name'&&typeof m.name==='string')p.name=m.name.trim().slice(0,14)||p.name;else if(m.type==='chat'&&typeof m.text==='string'){const now=Date.now();if(now-(p.lastChat||0)>=700){const text=m.text.replace(/[\\u0000-\\u001F\\u007F]/g,' ').replace(/\\s+/g,' ').trim().slice(0,80);if(text){p.lastChat=now;broadcast({type:'event',kind:'chat',playerId:p.id,name:p.name,text,ts:now})}}}else if(m.type==='eat'&&p.meat>0){const used=Math.min(3,p.meat);p.meat-=used;const before=p.hp;p.hp=Math.min(p.maxHp,p.hp+used*12);broadcast({type:'event',kind:'meal',playerId:p.id,used,healed:Math.round(p.hp-before),hp:p.hp})}else if(m.type==='endless'&&ENDGAME.mode==='cleared')",
    'chat and meat consumption messages');

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
