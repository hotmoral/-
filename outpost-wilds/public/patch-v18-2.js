/* Outpost Wilds V18.2: player carry meter + authoritative growth mission fallback. */

/* Character overhead: name -> HP -> carry. Keep this independent from world-object renderers. */
const v182BaseDrawPlayer=drawPlayer;
drawPlayer=function(p,isMe,t){
  v182BaseDrawPlayer(p,isMe,t);
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py);
  const cap=Math.max(1,Number(p.carryCap)||1),ratio=Math.max(0,Math.min(1,(Number(p.carry)||0)/cap));
  const color=ratio>=.8?'#e25549':ratio>=.4?'#e9a33d':'#62b86f';
  const w=40,h=4,x=s.x-w/2,y=s.y-30;
  ctx.save();
  ctx.fillStyle='rgba(5,10,8,.82)';v4Rounded(x-1,y-1,w+2,h+2,3);ctx.fill();
  if(ratio>0){ctx.fillStyle=color;v4Rounded(x,y,Math.max(1,w*ratio),h,2);ctx.fill();}
  ctx.restore();
};

/* Never interpret missing mission payload as "campaign complete". */
const V182_BASE_GOALS={
  1:{label:'거점 LV.2',cost:{wood:70,stone:35,meat:18},mission:['gather',50,'누적 채집']},
  2:{label:'거점 LV.3',cost:{wood:150,stone:100,meat:40},mission:['gather',140,'누적 채집'],req:[['workshop',1,'작업대'],['storage',1,'보급 창고']]},
  3:{label:'거점 LV.4',cost:{wood:240,stone:200,meat:80},mission:['kills',15,'적 처치'],extraMission:['raids',1,'습격 방어'],req:[['workshop',2,'작업대'],['watchtower',1,'망루'],['forge',1,'대장간'],['infirmary',1,'회복소']]},
  4:{label:'거점 LV.5',cost:{wood:390,stone:350,meat:140},mission:['kills',30,'적 처치'],extraMission:['raids',2,'습격 방어'],req:[['storage',2,'보급 창고'],['farm',2,'농장'],['wall',2,'방벽'],['turret',1,'자동 터렛']]},
  5:{label:'거점 LV.6',cost:{wood:600,stone:560,meat:220},mission:['gather',700,'누적 채집'],extraMission:['raids',3,'습격 방어'],req:[['workshop',3,'작업대'],['watchtower',3,'망루'],['forge',2,'대장간'],['infirmary',2,'회복소'],['turret',2,'자동 터렛'],['turret2',1,'외곽 터렛']]}
};
function v182BaseObjective(){
  const lv=Number(snap?.base?.level)||1,def=V182_BASE_GOALS[lv];if(!def)return null;
  const pad=v6AllPads().find(p=>p?.id==='base');
  if(pad&&!pad.complete)return{id:'base',label:pad.label||def.label,state:pad.locked?'locked':'build',level:lv,cost:pad.cost||def.cost,progress:pad.progress||{},reason:pad.reason||''};
  const f=snap?.facilities||{},m=snap?.missions||{};let reason='';
  for(const r of def.req||[]){if((Number(f[r[0]])||0)<r[1]){reason=`해금 조건 · ${r[2]} LV.${r[1]}`;break;}}
  if(!reason&&def.mission){const[k,n,label]=def.mission,cur=Number(m[k])||0;if(cur<n)reason=`해금 조건 · ${label} ${cur}/${n}`;}
  if(!reason&&def.extraMission){const[k,n,label]=def.extraMission,cur=Number(m[k])||0;if(cur<n)reason=`해금 조건 · ${label} ${cur}/${n}`;}
  return{id:'base',label:def.label,state:reason?'locked':'build',level:lv,cost:def.cost,progress:{wood:0,stone:0,meat:0},reason};
}
function v182PadObjectives(){
  return v6AllPads().filter(p=>p&&!p.complete).map(p=>({id:p.id,label:p.label,state:p.locked?'locked':p.kind==='repair'?'repair':(p.level?'upgrade':'build'),level:p.level||0,cost:p.cost||null,progress:p.progress||{},reason:p.reason||''}));
}
v18MissionObjectives=function(){
  const story=(snap?.story?.objectives||[]).filter(o=>o&&o.state!=='done');
  const pads=v182PadObjectives();
  const merged=[];const seen=new Set();
  const base=(story.find(o=>o.id==='base')||pads.find(o=>o.id==='base')||v182BaseObjective());
  if(base){merged.push(base);seen.add('base');}
  for(const o of [...story,...pads]){if(!o||o.state==='done'||seen.has(o.id))continue;seen.add(o.id);merged.push(o);}
  if(merged.length)return merged;
  const fallback=v182BaseObjective();
  if(fallback)return[fallback];
  if((Number(snap?.base?.level)||1)>=6&&snap?.endgame?.mode!=='cleared')return[{id:'final',label:'최종 작전 준비',state:'locked',cost:null,progress:{},reason:'신호탑 해금 조건을 확인하세요'}];
  return[];
};

window.__OW_V182__={carryMeter:{green:[0,.4],orange:[.4,.8],red:[.8,1]},missionFallback:'story>pads>base'};
