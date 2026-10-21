import {
  PROVISIONAL_MONSTER_TYPES,armorDamage,flyerY,chargerNext,chargerSpeed,
  splitterChildren,supporterSpeedMultiplier,effectiveMoveSpeed,siegerNext,rosterRoles
} from './monster-capability-v1.js';

function check(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runMonsterCapabilityV1SelfTest(){
  const checks=[];

  const roles=rosterRoles(),roleValues=Object.values(roles);
  checks.push(check('ROSTER_HAS_9_ARCHETYPES',Object.keys(PROVISIONAL_MONSTER_TYPES).length===9,Object.keys(PROVISIONAL_MONSTER_TYPES),9));
  checks.push(check('ROSTER_PRIMARY_ROLES_UNIQUE',new Set(roleValues).size===9,roles,'9 unique roles'));

  checks.push(check('SHIELD_ARMOR_100_TO_72',armorDamage('shield',100)===72,armorDamage('shield',100),72));
  checks.push(check('SHIELD_ARMOR_MIN_ONE',armorDamage('shield',1)===1,armorDamage('shield',1),1));
  checks.push(check('BRUTE_HAS_NO_ARMOR_REDUCTION',armorDamage('brute',100)===100,armorDamage('brute',100),100));

  const y0=flyerY(.4,0),yQuarter=flyerY(.4,Math.PI/(2*5)*1000);
  checks.push(check('FLYER_Y_AUTH_FUNCTION_BASE',Math.abs(y0-.4)<1e-12,y0,.4));
  checks.push(check('FLYER_Y_AUTH_FUNCTION_AMPLITUDE',Math.abs(yQuarter-.42)<1e-9,yQuarter,.42));

  let c={phase:'advance',phaseAt:0,rearmUntil:0};
  c=chargerNext(c,{at:1000,atTrigger:true});
  checks.push(check('CHARGER_ADVANCE_TO_WINDUP',c.phase==='windup',c.phase,'windup'));
  const ci=chargerNext(c,{at:1200,knockback:.001});
  checks.push(check('CHARGER_WINDUP_INTERRUPT',ci.phase==='advance'&&ci.interrupted===true,{phase:ci.phase,interrupted:ci.interrupted},{phase:'advance',interrupted:true}));
  const blocked=chargerNext(ci,{at:1500,atTrigger:true});
  checks.push(check('CHARGER_REARM_BLOCK',blocked.phase==='advance',blocked.phase,'advance'));
  let c2=chargerNext({phase:'advance',phaseAt:0,rearmUntil:0},{at:1000,atTrigger:true});
  c2=chargerNext(c2,{at:1650});
  checks.push(check('CHARGER_WINDUP_TO_CHARGE',c2.phase==='charge'&&chargerSpeed('charge')===.210,{phase:c2.phase,speed:chargerSpeed('charge')},{phase:'charge',speed:.210}));

  const children=splitterChildren({id:7,x:.5,y:.4,refAt:2000},20);
  checks.push(check('SPLITTER_EXACTLY_TWO_CHILDREN',children.length===2,children.length,2));
  checks.push(check('SPLITTER_CHILDREN_NON_RECURSIVE',children.every(x=>x.canSplit===false),children.map(x=>x.canSplit),[false,false]));
  checks.push(check('SPLITTER_CHILDREN_DETERMINISTIC_OFFSETS',Math.abs(children[0].y-.382)<1e-12&&Math.abs(children[1].y-.418)<1e-12,children.map(x=>x.y),[.382,.418]));

  checks.push(check('SUPPORTER_AURA_OFF',supporterSpeedMultiplier([.19,.3])===1,supporterSpeedMultiplier([.19,.3]),1));
  checks.push(check('SUPPORTER_AURA_ON',supporterSpeedMultiplier([.10])===1.18,supporterSpeedMultiplier([.10]),1.18));
  checks.push(check('SUPPORTER_NON_STACKING',supporterSpeedMultiplier([.10,.12])===1.18,supporterSpeedMultiplier([.10,.12]),1.18));
  checks.push(check('SUPPORTER_DOES_NOT_SELF_BUFF',effectiveMoveSpeed('supporter',{supporterDistances:[0]})===.055,effectiveMoveSpeed('supporter',{supporterDistances:[0]}),.055));

  let s={phase:'advance',phaseAt:0,nextShotAt:null};
  s=siegerNext(s,{at:1000,x:.38});
  checks.push(check('SIEGER_ADVANCE_TO_WINDUP',s.phase==='windup'&&s.nextShotAt===1800,{phase:s.phase,next:s.nextShotAt},{phase:'windup',next:1800}));
  s=siegerNext(s,{at:1800,x:.38});
  checks.push(check('SIEGER_WINDUP_TO_FIRE',s.phase==='siege'&&s.fire===true,{phase:s.phase,fire:s.fire},{phase:'siege',fire:true}));
  s=siegerNext(s,{at:1800,x:.38});
  checks.push(check('SIEGER_FIRE_TO_COOLDOWN',s.phase==='cooldown'&&s.nextShotAt===4000,{phase:s.phase,next:s.nextShotAt},{phase:'cooldown',next:4000}));
  const sr=siegerNext({phase:'windup',phaseAt:1000,nextShotAt:1800},{at:1300,x:.45,knockback:.01});
  checks.push(check('SIEGER_KNOCKBACK_REPOSITION',sr.phase==='advance'&&sr.repositioned===true,{phase:sr.phase,repositioned:sr.repositioned},{phase:'advance',repositioned:true}));

  const passed=checks.filter(x=>x.pass).length;
  return{ok:passed===checks.length,version:'monster-capability-v1-provisional',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
