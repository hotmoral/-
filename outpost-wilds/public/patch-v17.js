/* Outpost Wilds V17: square segmented fortification, commercial HUD, image-asset world objects, single-step local prediction. */
const V17_ASSETS={
  player:'/assets/player-v17.svg',backpack:'/assets/backpack-v17.svg',base:'/assets/base-v17.svg',stockpile:'/assets/stockpile-v17.svg',
  workshop:'/assets/workshop-v17.svg',storage:'/assets/storage-v17.svg',farm:'/assets/farm-v17.svg',watchtower:'/assets/watchtower-v17.svg',forge:'/assets/forge-v17.svg',infirmary:'/assets/infirmary-v17.svg',turret:'/assets/turret-v17.svg',turret2:'/assets/turret2-v17.svg',
  wall1:'/assets/wall-lv1-v17.svg',wall2:'/assets/wall-lv2-v17.svg',wall3:'/assets/wall-lv3-v17.svg'
};
for(const [k,p] of Object.entries(V17_ASSETS))v15LoadAsset(`v17_${k}`,p);

const v17RawAdvance=v4Advance;let v17AdvanceStamp=-1;
v4Advance=function(){const stamp=Math.floor(performance.now()/7);if(stamp===v17AdvanceStamp)return;v17AdvanceStamp=stamp;v17RawAdvance();};

function v17DrawImage(key,x,y,w,h,flip=false,rot=0,alpha=1){const im=assets[`v17_${key}`];if(!im?.complete||!im.naturalWidth)return false;ctx.save();ctx.globalAlpha=alpha;ctx.translate(x,y);ctx.rotate(rot);ctx.scale(flip?-1:1,1);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();return true;}

drawPlayer=function(p,isMe,t){
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py),phase=movePhase.get(p.id)||0,moving=isMe?Math.hypot(input.x,input.y)>.04:true,bob=moving?Math.sin(phase)*1.2:Math.sin(phase)*.25,flip=(p.facing??(Math.cos(p.dir||0)>=0?1:-1))<0;
  shadow(s.x,s.y+22,19,7,.28);
  if((p.carry||0)>0)v17DrawImage('backpack',s.x+(flip?14:-14),s.y+1,34,40,flip,0,.98);
  v17DrawImage('player',s.x,s.y-7+bob,60,78,flip);
  ctx.save();ctx.translate(s.x+(flip?-10:10),s.y-7+bob);ctx.scale(flip?-1:1,1);const swing=attackFx.get(p.id);let sw=0;if(swing&&!swing.ranged){sw=(.34-swing.t)/.34;sw=Math.sin(sw*Math.PI)*1.05;}drawWeapon(p,sw);ctx.restore();
  if(isMe){circle(s.x,s.y+3,26,null,'rgba(226,211,171,.7)',1.25);circle(s.x,s.y+3,31,null,'rgba(118,194,159,.22)',1);}
  ctx.save();ctx.textAlign='center';ctx.shadowColor='#000';ctx.shadowBlur=4;ctx.font='800 9px system-ui,sans-serif';ctx.fillStyle='#f6efe1';ctx.fillText(p.name,s.x,s.y-49);ctx.shadowBlur=0;drawHealth(s.x,s.y-41,p.hp/p.maxHp,40);ctx.restore();
};
drawCargo=function(){};

function v17FacilityAsset(fid,lv){const pos=V14_POS[fid];if(!pos||!lv)return;const s=worldToScreen(pos.x,pos.y),sizes={workshop:[94,78],storage:[88,76],farm:[106,82],watchtower:[88,116],forge:[92,84],infirmary:[92,86],turret:[88,82],turret2:[94,86]},sz=sizes[fid]||[88,78];shadow(s.x,s.y+30,sz[0]*.34,9,.28);v17DrawImage(fid,s.x,s.y-8,sz[0]*(1+.035*(lv-1)),sz[1]*(1+.035*(lv-1)));ctx.save();ctx.font='800 8px system-ui,sans-serif';ctx.textAlign='center';ctx.fillStyle='#ead7aa';ctx.fillText(`LV.${lv}`,s.x,s.y+sz[1]*.42);ctx.restore();}

function v17WallAsset(lv){return lv===1?'wall1':lv===2?'wall2':'wall3'}
function v17DrawSide(side,f,base){
  const half=f.half||f.radius||0,seg=f.segments?.[side]||{hp:f.hp,maxHp:f.maxHp},ratio=seg.maxHp?Math.max(0,Math.min(1,seg.hp/seg.maxHp)):0,asset=v17WallAsset(f.level),step=f.level===1?50:54;
  const horizontal=side==='north'||side==='south',length=half*2,count=Math.max(4,Math.ceil(length/step)),broken=ratio<=.001;
  for(let i=0;i<count;i++){
    const u=(i+.5)/count*2-1;let wx,wy,rot=0;
    if(horizontal){wx=base.x+u*half;wy=base.y+(side==='north'?-half:half);rot=0;}else{wx=base.x+(side==='west'?-half:half);wy=base.y+u*half;rot=Math.PI/2;}
    const centerGap=Math.abs(u)<.105,damageGap=broken&&centerGap;if(damageGap)continue;
    const s=worldToScreen(wx,wy);if(s.x<-80||s.x>W+80||s.y<-80||s.y>H+80)continue;
    const dim=ratio<.35&&((i*7)%5===0);v17DrawImage(asset,s.x,s.y,58,39,false,rot,dim?.48:.98);
  }
  if(ratio<.999){let wx=base.x,wy=base.y;if(side==='north')wy-=half;if(side==='south')wy+=half;if(side==='west')wx-=half;if(side==='east')wx+=half;const s=worldToScreen(wx,wy);ctx.save();ctx.fillStyle='rgba(7,12,10,.88)';v4Rounded(s.x-38,s.y-10,76,20,10);ctx.fill();ctx.fillStyle=broken?'#ee7968':'#d9c596';ctx.font='800 8px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText(broken?'돌파됨':`${Math.round(ratio*100)}%`,s.x,s.y+2);ctx.restore();}
}
function v17DrawFortification(){const f=snap?.fortification;if(!f?.level||!f.half)return;for(const side of ['north','east','south','west'])v17DrawSide(side,f,snap.base);}

v6DrawBuiltFacilities=function(){const f=snap?.facilities||{};v17DrawFortification();for(const fid of ['workshop','storage','farm','watchtower','forge','infirmary','turret','turret2'])if(f[fid])v17FacilityAsset(fid,f[fid]);};

const v17BaseOld=drawBase;
drawBase=function(b){const s=worldToScreen(b.x,b.y);shadow(s.x,s.y+33,58,13,.34);v17DrawImage('base',s.x,s.y-8,126+Math.max(0,b.level-1)*4,104+Math.max(0,b.level-1)*3);v6DrawBuiltFacilities();v13DrawStockpile();};
v13DrawStockpile=function(){const st=v13Stock();if(!st)return;const s=worldToScreen(st.x,st.y),q=Math.min(1,(st.total||0)/Math.max(1,st.capacity||1));shadow(s.x,s.y+22,36,10,.26);v17DrawImage('stockpile',s.x,s.y-3,82,67);ctx.save();ctx.fillStyle='rgba(6,12,9,.86)';v4Rounded(s.x-35,s.y+34,70,14,7);ctx.fill();ctx.fillStyle='#263328';ctx.fillRect(s.x-28,s.y+39,56,4);ctx.fillStyle='#9ec67d';ctx.fillRect(s.x-28,s.y+39,56*q,4);ctx.font='800 7px system-ui,sans-serif';ctx.fillStyle='#e9dec5';ctx.textAlign='center';ctx.fillText(`${st.total||0}/${st.capacity||0}`,s.x,s.y+32);ctx.restore();};

function v17MissionPolish(){const root=v16EnsureMissionPanel();if(!root)return;root.classList.add('v17Mission');if(!root.dataset.v17){root.dataset.v17='1';const head=root.querySelector('.v16MissionHead');head.innerHTML='<span>성장</span><i class="v17MissionBadge">0</i><b>›</b>';const pref=localStorage.getItem('ow-v17-mission-open');root.classList.toggle('collapsed',pref!=='1');head.onclick=()=>{root.classList.toggle('collapsed');localStorage.setItem('ow-v17-mission-open',root.classList.contains('collapsed')?'0':'1');};}}
function v17RenderMission(){v17MissionPolish();const root=document.getElementById('v16Mission'),story=snap?.story;if(!root||!story)return;const list=root.querySelector('.v16MissionList'),storyEl=root.querySelector('.v16Story'),objs=(story.objectives||[]).filter(o=>o.state!=='done');root.querySelector('.v17MissionBadge').textContent=Math.min(9,objs.length);storyEl.textContent=story.stage||'거점 성장';list.innerHTML='';for(const o of objs.slice(0,5)){const row=document.createElement('div');row.className=`v16MissionItem ${o.state||''}`;const tag=o.state==='hidden'?'잠금':o.state==='repair'?'보수':o.state==='locked'?'선행':o.state==='upgrade'?'승급':'건설';row.innerHTML=`<header><b>${o.label}</b><em>${tag}</em></header>${o.reason?`<small>${o.reason}</small>`:''}${o.cost?`<div class="v16MissionCost">${v16CostHtml(o.cost,o.progress)}</div>`:''}`;list.appendChild(row);}if(objs.length>5){const more=document.createElement('div');more.className='v17More';more.textContent=`+ ${objs.length-5}개 목표`;list.appendChild(more);}if(!objs.length)list.innerHTML='<div class="v16MissionDone">현재 목표 완료</div>';}

function v17LayoutHud(){let dock=document.getElementById('v17TopDock');if(!dock){dock=document.createElement('div');dock.id='v17TopDock';dock.innerHTML='<div class="v17HudLeft"></div><div class="v17HudCenter"></div><div class="v17HudRight"></div>';document.body.appendChild(dock);const L=dock.querySelector('.v17HudLeft'),C=dock.querySelector('.v17HudCenter'),R=dock.querySelector('.v17HudRight');const brand=document.querySelector('.brand'),zone=document.getElementById('zoneBadge'),res=document.querySelector('.resources'),tops=document.querySelector('.topcards'),personal=document.querySelector('.personal.card');if(brand)L.appendChild(brand);if(zone)C.appendChild(zone);if(res)C.appendChild(res);if(tops)R.appendChild(tops);if(personal)R.appendChild(personal);}const stock=document.getElementById('v13StockHud');if(stock&&stock.parentElement!==dock.querySelector('.v17HudCenter'))dock.querySelector('.v17HudCenter').appendChild(stock);return dock;}

const v17OldHud=updateHud;
updateHud=function(){v17OldHud();v17LayoutHud();v17RenderMission();const f=snap?.fortification,base=document.querySelector('.baseCard');if(base&&f?.level){let w=base.querySelector('.v17WallMini');if(!w){w=document.createElement('small');w.className='v17WallMini';base.appendChild(w);}w.textContent=`성벽 LV.${f.level} · ${Math.round(100*(f.hp||0)/Math.max(1,f.maxHp||1))}%`;}};
setTimeout(()=>{v17LayoutHud();v17MissionPolish();},0);

const v17OldEvent=eventFx;
eventFx=function(m){v17OldEvent(m);if(m.kind==='wallSideBreach'){const names={north:'북벽',south:'남벽',east:'동벽',west:'서벽'};toast(`${names[m.side]||'성벽'} 돌파! 적이 틈으로 진입합니다`,'phaseDanger');nightFlash=.75;shake=8;}};
