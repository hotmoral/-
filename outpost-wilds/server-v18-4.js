const fs=require('fs');
const Module=require('module');
const {patchSource:patchV182}=require('./server-v18-2.js');

function replaceFunction(src,name,code){
  const sig=`function ${name}(`,start=src.indexOf(sig);
  if(start<0)throw new Error(`[V18.4 patch] function ${name} not found`);
  const brace=src.indexOf('{',start);if(brace<0)throw new Error(`[V18.4 patch] ${name} brace not found`);
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
  throw new Error(`[V18.4 patch] unterminated function ${name}`);
}

function patchSource(input){
  let src=patchV182(input);
  src=src.replace(/version:18\.2/g,'version:18.4')
    .replace(/\[V18\.2 persistence\]/g,'[V18.4 persistence]')
    .replace(/Outpost Wilds V18\.2/g,'Outpost Wilds V18.4')
    .replace(/V18\.2 bootstrap failed/g,'V18.4 bootstrap failed');

  src=replaceFunction(src,'startWave',`function startWave(){if(WAVE.active||ENDGAME.mode==='cleared'||ENDGAME.mode==='final')return;raidSeq++;raidStartedThisNight=true;Object.assign(WAVE,{active:true,raid:raidSeq,phase:'warning',stage:0,totalStages:3,timer:10,bossName:null,breached:false,final:false});markDirty();broadcast({type:'event',kind:'waveWarning',raid:raidSeq,seconds:10,baseLevel:BASE.level})}`);
  src=replaceFunction(src,'startFinalNight',`function startFinalNight(playerId){if(WAVE.active||ENDGAME.mode!=='ready')return;ENDGAME.mode='final';ENDGAME.finalAttempts++;dayClock=150;for(const[eid,e]of enemies)if(!e.raid)enemies.delete(eid);Object.assign(WAVE,{active:true,raid:\`FINAL-\${ENDGAME.finalAttempts}\`,phase:'warning',stage:0,totalStages:5,timer:12,bossName:null,breached:false,final:true});markDirty();saveWorld(false);broadcast({type:'event',kind:'finalNightStart',attempt:ENDGAME.finalAttempts,playerId,seconds:12})}`);
  src=replaceFunction(src,'updateWave',`function updateWave(dt){if(!WAVE.active)return;if(WAVE.phase==='warning'||WAVE.phase==='intermission'){WAVE.timer=Math.max(0,WAVE.timer-dt);if(WAVE.timer<=0)spawnWaveStage(WAVE.stage+1);return}if(WAVE.phase==='combat'&&raidEnemyCount()===0){if(WAVE.stage<WAVE.totalStages){WAVE.phase='intermission';WAVE.timer=WAVE.final?6:5;broadcast({type:'event',kind:WAVE.final?'finalIntermission':'waveIntermission',raid:WAVE.raid,nextStage:WAVE.stage+1,seconds:WAVE.timer})}else if(WAVE.final){if(WAVE.breached)failFinal();else completeCampaign()}else clearRegularWave()}}`);
  return src;
}
module.exports={patchSource};
if(require.main===module){
  const target=require.resolve('./server-v13.js'),original=Module._extensions['.js'];
  Module._extensions['.js']=function(mod,filename){if(filename===target)return mod._compile(patchSource(fs.readFileSync(filename,'utf8')),filename);return original(mod,filename)};
  try{require('./server-v13.js')}finally{Module._extensions['.js']=original}
}
