/* Outpost Wilds V16: staged unlocks, perimeter wall/repair UX, compact HUD, input/camera stabilization. */
const V16_WALL_POS={x:2040,y:2020};
v15LoadAsset('wallSegV16','/assets/wall-segment-v16.svg');

/* Smaller props/hostiles leave more readable world space without changing gameplay distances. */
for(const st of Object.values(V10_ENEMY_STYLE)){st.w=Math.round(st.w*.9);st.h=Math.round(st.h*.9);}
drawNode=function(n){
  const s=worldToScreen(n.x,n.y);
  if(n.type==='tree')drawAsset('tree',s.x,s.y-30,96,116);
  else if(n.type==='rock')drawAsset('rock',s.x,s.y-4,74,62);
  else if(n.type==='ore')drawAsset('ore',s.x,s.y-5,77,67);
  else drawAsset('berry',s.x,s.y,68,56);
  if(n.hp<n.maxHp)drawHealth(s.x,s.y-(n.type==='tree'?80:49),n.hp/n.maxHp,34);
};

function v16WallSegment(x,y,w,h,rot,lv,damaged){
  const im=assets.wallSegV16;if(!im?.complete||!im.naturalWidth)return;
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha=damaged?.48:.98;
  if(lv===1)ctx.filter='sepia(.22) saturate(.92) brightness(.93)';
  else if(lv===2)ctx.filter='grayscale(.12) contrast(1.04) brightness(.96)';
  else ctx.filter='contrast(1.13) saturate(.88) brightness(.9)';
  ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();
}
function v16DrawPerimeter(){
  const f=snap?.fortification;if(!f?.level||!f.radius)return;
  const base=snap.base,ratio=f.maxHp?Math.max(0,Math.min(1,f.hp/f.maxHp)):0,n=f.level===1?28:f.level===2?34:40;
  for(let i=0;i<n;i++){
    const a=i/n*Math.PI*2,r=f.radius,worldX=base.x+Math.cos(a)*r,worldY=base.y+Math.sin(a)*r,s=worldToScreen(worldX,worldY);
    if(s.x<-90||s.x>W+90||s.y<-90||s.y>H+90)continue;
    const damageRank=((i*17)%n)/n,broken=damageRank>(ratio*.82+.13);
    if(f.breached&&i%4===0)continue;
    v16WallSegment(s.x,s.y,f.level===1?62:68,f.level===1?34:38,a+Math.PI/2,f.level,broken);
  }
  const top=worldToScreen(base.x,base.y-f.radius-26);
  if(top.x>-160&&top.x<W+160&&top.y>-40&&top.y<H+50){
    ctx.save();const bw=128;ctx.fillStyle='rgba(7,13,10,.88)';v4Rounded(top.x-bw/2,top.y-12,bw,24,12);ctx.fill();ctx.strokeStyle=f.breached?'rgba(229,92,76,.72)':'rgba(220,194,135,.34)';ctx.stroke();
    ctx.fillStyle='#171d18';v4Rounded(top.x-49,top.y+2,98,5,3);ctx.fill();ctx.fillStyle=f.breached?'#d45f4e':'#9fc776';ctx.fillRect(top.x-49,top.y+2,98*ratio,5);ctx.font='800 9px system-ui,sans-serif';ctx.textAlign='center';ctx.fillStyle='#f0dfbd';ctx.fillText(f.breached?`방벽 LV.${f.level} · 돌파됨`:`방벽 LV.${f.level} · ${Math.round(f.hp)}/${f.maxHp}`,top.x,top.y-2);ctx.restore();
  }
}

/* Replace V14 facility pass: perimeter is the wall; the obsolete single wall prop disappears. */
v6DrawBuiltFacilities=function(){
  const f=snap?.facilities||{};v16DrawPerimeter();
  if(f.workshop)v14DrawWorkshop(V14_POS.workshop,f.workshop);
  if(f.storage)v14DrawStorage(V14_POS.storage,f.storage);
  if(f.farm)v14DrawFarm(V14_POS.farm,f.farm);
  if(f.watchtower)v14DrawWatchtower(V14_POS.watchtower,f.watchtower);
  if(f.forge)v14DrawForge(V14_POS.forge,f.forge);
  if(f.infirmary)v14DrawInfirmary(V14_POS.infirmary,f.infirmary);
  if(f.turret)v14DrawTurret(V14_POS.turret,f.turret,'turret',false);
  if(f.turret2)v14DrawTurret(V14_POS.turret2,f.turret2,'turret2',true);
};

function v16CostHtml(cost,progress){
  if(!cost)return'';const p=progress||{};return ['wood','stone','meat'].filter(k=>(cost[k]||0)>0).map(k=>{const names={wood:'목',stone:'돌',meat:'식'},left=Math.max(0,(cost[k]||0)-(p[k]||0));return `<i class="${left===0?'done':''}"><b>${names[k]}</b> ${left}</i>`}).join('');
}
function v16EnsureMissionPanel(){
  let root=document.getElementById('v16Mission');if(root)return root;
  root=document.createElement('aside');root.id='v16Mission';root.className='v16Mission';
  root.innerHTML='<button class="v16MissionHead" type="button"><span>성장 미션</span><b>▾</b></button><div class="v16MissionBody"><strong class="v16Story"></strong><div class="v16MissionList"></div></div>';
  document.body.appendChild(root);
  const saved=localStorage.getItem('ow-v16-mission-collapsed');if(saved==='1')root.classList.add('collapsed');
  root.querySelector('.v16MissionHead').onclick=()=>{root.classList.toggle('collapsed');localStorage.setItem('ow-v16-mission-collapsed',root.classList.contains('collapsed')?'1':'0');};
  return root;
}
function v16RenderMission(){
  const root=v16EnsureMissionPanel(),story=snap?.story;if(!story)return;
  root.querySelector('.v16Story').textContent=story.stage||'거점 성장';const list=root.querySelector('.v16MissionList');list.innerHTML='';
  const items=(story.objectives||[]).filter(o=>o.state!=='done').slice(0,8);
  for(const o of items){const row=document.createElement('div');row.className=`v16MissionItem ${o.state||''}`;const tag=o.state==='hidden'?'해금':o.state==='repair'?'보수':o.state==='locked'?'선행':o.state==='upgrade'?'승급':'건설';row.innerHTML=`<header><b>${o.label}</b><em>${tag}</em></header>${o.reason?`<small>${o.reason}</small>`:''}${o.cost?`<div class="v16MissionCost">${v16CostHtml(o.cost,o.progress)}</div>`:''}`;list.appendChild(row);}
  if(!items.length)list.innerHTML='<div class="v16MissionDone">현재 성장 미션 완료</div>';
}
v16EnsureMissionPanel();

function v16FixEatButton(){const b=document.getElementById('eatMeat');if(!b)return null;if(b.parentElement!==document.body)document.body.appendChild(b);b.classList.add('v16Eat');return b;}
v16FixEatButton();

const v16OldHud=updateHud;
updateHud=function(){
  v16OldHud();if(!snap)return;v16FixEatButton();v16RenderMission();
  const st=snap.stockpile,el=document.getElementById('v13StockHud');if(st&&el)el.innerHTML=`<b>📦 목 ${st.wood||0} · 돌 ${st.stone||0} · 식 ${st.meat||0}</b><small>${st.total||0}/${st.capacity||0}</small>`;
};

/* Resource hits previously shook the whole camera, which felt like collision/pushing. */
const v16OldEvent=eventFx;let v16RepairFxAt=0;
eventFx=function(m){
  v16OldEvent(m);
  if(m.kind==='impact')shake=Math.min(shake,.45);
  if(m.kind==='wallHit')shake=Math.max(shake,m.damage>40?1.5:.55);
  if(m.kind==='wallBreach'){toast('방벽이 무너졌습니다 · 적이 거점 안으로 진입합니다','phaseDanger');nightFlash=.6;shake=9;}
  if(m.kind==='wallExpanded'){toast(`방벽 LV.${m.level} 완성 · 방어 영역 확장`,'phaseAlert');constructionFx=1.6;}
  if((m.kind==='wallRepair'||m.kind==='baseRepair')&&m.playerId===meId&&performance.now()-v16RepairFxAt>650){v16RepairFxAt=performance.now();toast(`${m.kind==='wallRepair'?'방벽':'거점'} 보수 · +${m.healed} HP`);addFloater(`+${m.healed}`,m.x,m.y-18,'#a7d89b',12);}
};

/* Match local prediction to authority but stop correcting tiny moving errors every frame. */
v4Advance=function(){
  const now=performance.now(),dt=Math.min(.05,(now-v4RenderT)/1000);v4RenderT=now;if(!snap)return;
  for(const p of snap.players||[]){const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;if(p.id===meId){const moving=Math.hypot(input.x,input.y)>.035;if(moving){const q=Math.max(0,Math.min(1,(p.carry||0)/Math.max(1,p.carryCap||1))),speed=212*Math.max(.86,1-.14*Math.pow(q,1.35));r.x=Math.max(35,Math.min(3565,r.x+input.x*speed*dt));r.y=Math.max(35,Math.min(3565,r.y+input.y*speed*dt));}const ex=r.tx-r.x,ey=r.ty-r.y,err=Math.hypot(ex,ey);if(err>190){r.x=r.tx;r.y=r.ty;}else if(!moving){const k=Math.min(1,dt*13);r.x+=ex*k;r.y+=ey*k;}else if(err>78){const k=Math.min(1,dt*2.4);r.x+=ex*k;r.y+=ey*k;}else if(err>38){const k=Math.min(1,dt*.55);r.x+=ex*k;r.y+=ey*k;}}else{const k=Math.min(1,dt*12.5);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;}}
  for(const e of snap.enemies||[]){const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;const k=Math.min(1,dt*11);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;}
};

/* Camera follows predicted local position instead of raw 15 Hz snapshots. */
const v16QueuedFrame=frame;
frame=function(t){
  const dt=Math.min(.04,(t-prevT)/1000);prevT=t;constructionFx=Math.max(0,constructionFx-dt);for(const p of snap?.players||[]){const old=movePhase.get(p.id)||0;movePhase.set(p.id,old+dt*9)}for(const [id,a]of attackFx){a.t-=dt;if(a.t<=0)attackFx.delete(id)}
  v4Advance();const cp=myPlayer();if(cp){const ck=Math.min(1,dt*10.5);cam.x+=(cp.x-cam.x)*ck;cam.y+=(cp.y-cam.y)*ck;}
  ctx.save();if(shake>0){ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);shake*=.84}drawGround();if(snap){const drawables=[];drawables.push({y:snap.base.y,kind:'base',v:snap.base});for(const n of snap.nodes)if(Math.abs(n.x-cam.x)<W/2+140&&Math.abs(n.y-cam.y)<H/2+160)drawables.push({y:n.y,kind:'node',v:n});for(const e of snap.enemies)if(Math.abs(e.x-cam.x)<W/2+190&&Math.abs(e.y-cam.y)<H/2+190)drawables.push({y:e.y,kind:'enemy',v:e});for(const p2 of snap.players)drawables.push({y:p2.y,kind:'player',v:p2});drawables.sort((a,b)=>a.y-b.y);for(const d of drawables){if(d.kind==='base')drawBase(d.v);else if(d.kind==='node')drawNode(d.v);else if(d.kind==='enemy')drawEnemy(d.v,t);else drawPlayer(d.v,d.v.id===meId,t)}drawParticles(dt);drawCompass();drawMinimap();lighting()}ctx.restore();requestAnimationFrame(frame);
};

/* Joystick dead-zone + hard release on browser/UI interruptions prevents phantom movement. */
const v16Joy=document.getElementById('joystick'),v16Stick=v16Joy?.querySelector('.stick');
function v16FilterJoy(e){if(!v16Joy||!joyActive||e.pointerId!==joyId)return;const r=v16Joy.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,dx=e.clientX-cx,dy=e.clientY-cy,l=Math.hypot(dx,dy),max=43,raw=Math.min(1,l/max),dead=.14,v=raw<=dead?0:(raw-dead)/(1-dead),nx=l?dx/l:0,ny=l?dy/l:0;input.x=nx*v;input.y=ny*v;}
function v16StopInput(){if(!joyActive&&Math.hypot(input.x,input.y)<.001)return;joyId=null;joyActive=false;input.x=0;input.y=0;if(v16Stick)v16Stick.style.transform='';send({type:'input',x:0,y:0});}
if(v16Joy){v16Joy.addEventListener('pointerdown',v16FilterJoy);v16Joy.addEventListener('pointermove',v16FilterJoy);v16Joy.addEventListener('lostpointercapture',v16StopInput);}
window.addEventListener('pointercancel',()=>joyActive&&v16StopInput());window.addEventListener('blur',v16StopInput);document.addEventListener('visibilitychange',()=>{if(document.hidden)v16StopInput()});
