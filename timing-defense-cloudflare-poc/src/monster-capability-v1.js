// Timing Defense — Monster Capability Sandbox V1
// PROVISIONAL — NOT BALANCE FROZEN.
// Pure, stage-number-independent capability helpers. No live gameplay wiring here.

export const PROVISIONAL_MONSTER_TYPES=Object.freeze({
  grunt:Object.freeze({role:'baseline',hp:320,speed:.070,wallDamage:90,knockResist:.85,armor:1.00,reward:6}),
  runner:Object.freeze({role:'sustained-tempo',hp:165,speed:.135,wallDamage:60,knockResist:1.00,armor:1.00,reward:5}),
  brute:Object.freeze({role:'raw-durability',hp:900,speed:.040,wallDamage:180,knockResist:.38,armor:1.00,reward:14}),
  shield:Object.freeze({role:'mitigation',hp:540,speed:.057,wallDamage:120,knockResist:.62,armor:.72,reward:10}),
  flyer:Object.freeze({role:'vertical-geometry',hp:225,speed:.100,wallDamage:70,knockResist:.90,armor:1.00,reward:7,oscAmp:.020,oscOmega:5.0}),
  charger:Object.freeze({role:'burst-tempo',hp:380,speed:.060,wallDamage:110,knockResist:.80,armor:1.00,reward:8,windupMs:650,chargeSpeed:.210,rearmMs:900}),
  splitter:Object.freeze({role:'population-transform',hp:420,speed:.065,wallDamage:100,knockResist:.82,armor:1.00,rewardBudget:8,childHp:120,childSpeed:.115,childWallDamage:40}),
  supporter:Object.freeze({role:'formation-support',hp:280,speed:.055,wallDamage:70,knockResist:.90,armor:1.00,reward:8,auraRadius:.18,auraSpeedMul:1.18}),
  sieger:Object.freeze({role:'objective-pressure',hp:520,speed:.045,wallDamage:0,knockResist:.55,armor:1.00,reward:11,standoffX:.38,windupMs:800,shotDamage:75,repeatMs:2200})
});

export function meta(type){
  return PROVISIONAL_MONSTER_TYPES[type]||PROVISIONAL_MONSTER_TYPES.grunt;
}

export function armorDamage(type,incoming){
  const raw=Math.max(0,Number(incoming)||0),armor=meta(type).armor??1;
  return Math.max(1,Math.round(raw*armor));
}

export function flyerY(baseY,ageMs,type='flyer'){
  const d=meta(type),amp=d.oscAmp||0,omega=d.oscOmega||0;
  return Number(baseY||0)+Math.sin(Math.max(0,Number(ageMs)||0)/1000*omega)*amp;
}

export function chargerSpeed(phase){
  const d=meta('charger');
  return phase==='charge'?d.chargeSpeed:d.speed;
}

export function chargerNext(state,event){
  const d=meta('charger');
  const s={phase:'advance',phaseAt:0,rearmUntil:0,...state};
  const e={at:0,atTrigger:false,knockback:0,wallHit:false,...event};
  if(e.wallHit)return{...s,phase:'resolved',phaseAt:e.at};
  if(s.phase==='windup'&&Number(e.knockback)>0){
    return{...s,phase:'advance',phaseAt:e.at,rearmUntil:e.at+d.rearmMs,interrupted:true};
  }
  if(s.phase==='advance'&&e.atTrigger&&e.at>=Number(s.rearmUntil||0)){
    return{...s,phase:'windup',phaseAt:e.at,interrupted:false};
  }
  if(s.phase==='windup'&&e.at-s.phaseAt>=d.windupMs){
    return{...s,phase:'charge',phaseAt:e.at,interrupted:false};
  }
  return s;
}

export function splitterChildren(parent,nextId=1){
  const d=meta('splitter'),p=parent||{};
  const x=Number(p.x||0),y=Number(p.y||0),refAt=Number(p.refAt||0);
  return[
    {id:nextId,type:'splitter-child',parentId:p.id??null,x,y:y-.018,refAt,hp:d.childHp,maxHp:d.childHp,speed:d.childSpeed,wallDamage:d.childWallDamage,canSplit:false},
    {id:nextId+1,type:'splitter-child',parentId:p.id??null,x,y:y+.018,refAt,hp:d.childHp,maxHp:d.childHp,speed:d.childSpeed,wallDamage:d.childWallDamage,canSplit:false}
  ];
}

export function supporterSpeedMultiplier(distances){
  const d=meta('supporter'),list=Array.isArray(distances)?distances:[];
  return list.some(x=>Number.isFinite(Number(x))&&Number(x)<=d.auraRadius)?d.auraSpeedMul:1;
}

export function effectiveMoveSpeed(type,{phase='advance',supporterDistances=[]}={}){
  const base=type==='charger'?chargerSpeed(phase):(meta(type).speed||0);
  if(type==='supporter')return base;
  return base*supporterSpeedMultiplier(supporterDistances);
}

export function siegerNext(state,event){
  const d=meta('sieger');
  const s={phase:'advance',phaseAt:0,nextShotAt:null,...state};
  const e={at:0,x:1,knockback:0,...event};
  const inRange=Number(e.x)<=d.standoffX;

  if((s.phase==='windup'||s.phase==='cooldown'||s.phase==='siege')&&Number(e.knockback)>0&&!inRange){
    return{...s,phase:'advance',phaseAt:e.at,nextShotAt:null,repositioned:true};
  }
  if(s.phase==='advance'&&inRange){
    return{...s,phase:'windup',phaseAt:e.at,nextShotAt:e.at+d.windupMs,repositioned:false};
  }
  if(s.phase==='windup'&&inRange&&e.at>=Number(s.nextShotAt)){
    return{...s,phase:'siege',phaseAt:e.at,nextShotAt:e.at,fire:true,repositioned:false};
  }
  if(s.phase==='siege'){
    return{...s,phase:'cooldown',phaseAt:e.at,nextShotAt:e.at+d.repeatMs,fire:false};
  }
  if(s.phase==='cooldown'&&inRange&&e.at>=Number(s.nextShotAt)){
    return{...s,phase:'windup',phaseAt:e.at,nextShotAt:e.at+d.windupMs,repositioned:false};
  }
  return{...s,fire:false};
}

export function rosterRoles(){
  return Object.fromEntries(Object.entries(PROVISIONAL_MONSTER_TYPES).map(([k,v])=>[k,v.role]));
}
