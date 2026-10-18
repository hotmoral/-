/* Outpost Wilds V10: shared weapon ladder, escalating enemy silhouettes, boss invasion feedback. */
const V10_ENEMY_STYLE={
 wolf:{asset:'wolf',w:92,h:61,label:'늑대',filter:'none'},
 boar:{asset:'boar',w:96,h:64,label:'멧돼지',filter:'none'},
 brute:{asset:'brute',w:100,h:76,label:'야수',filter:'none'},
 direwolf:{asset:'wolf',w:112,h:74,label:'광포 늑대',filter:'saturate(.55) brightness(.88) hue-rotate(155deg)'},
 tusker:{asset:'boar',w:118,h:80,label:'철갑 멧돼지',filter:'sepia(.35) saturate(.8) contrast(1.12)'},
 mauler:{asset:'brute',w:126,h:94,label:'파괴자',filter:'saturate(1.35) brightness(.82) hue-rotate(335deg)'},
 siegebeast:{asset:'brute',w:154,h:112,label:'공성 야수',filter:'grayscale(.45) contrast(1.25) brightness(.82)'},
 alpha:{asset:'alpha',w:148,h:108,label:'잿빛 포식자',filter:'none',boss:true},
 broodmother:{asset:'alpha',w:178,h:132,label:'가시등 어미',filter:'hue-rotate(255deg) saturate(1.2) brightness(.9)',boss:true},
 colossus:{asset:'brute',w:218,h:158,label:'황폐의 거수',filter:'sepia(.35) saturate(.7) contrast(1.35) brightness(.72)',boss:true}
};

/* V8 action boundary now follows the exact shared weapon auto range sent by V10. */
v8DrawActionRanges=function(p,s){
  if(p.id!==meId)return;
  const ar=p.autoRange||120,enemyHot=v8NearEnemy(p,ar),nodeHot=v8NearNode(p,V8_GATHER_RANGE),pulse=.82+.18*Math.sin(v8PulseT*5.2);
  v8RangeRing(s,V8_GATHER_RANGE,'#9fcf78',nodeHot?.68:.24,true,nodeHot?2.2:1.3);
  v8RangeRing(s,ar,'#e88967',enemyHot?.78*pulse:.28,false,enemyHot?2.5:1.4);
  const wi=v5Assets.wood;if(wi?.complete){ctx.save();ctx.globalAlpha=nodeHot?.9:.48;ctx.drawImage(wi,s.x-11,s.y+3-V8_GATHER_RANGE-11,22,22);ctx.restore();}
  ctx.save();ctx.translate(s.x,s.y+3-ar);ctx.globalAlpha=enemyHot?.95:.52;ctx.fillStyle='#e9a07f';ctx.beginPath();ctx.moveTo(-3,-10);ctx.lineTo(3,-10);ctx.lineTo(2,5);ctx.lineTo(7,10);ctx.lineTo(-7,10);ctx.lineTo(-2,5);ctx.closePath();ctx.fill();ctx.restore();
};

/* Replace enemy drawing so each base-level enemy family reads differently without adding screen clutter. */
drawEnemy=function(e,t){
  const rr=v4Enemies.get(e.id),ex=rr?.x??e.x,ey=rr?.y??e.y,s=worldToScreen(ex,ey),st=V10_ENEMY_STYLE[e.type]||V10_ENEMY_STYLE.wolf,movingBob=Math.sin(t*.006+e.id)*1.3;
  shadow(s.x,s.y+18,e.r*1.25,7,.32);
  if(e.boss){const g=ctx.createRadialGradient(s.x,s.y,18,s.x,s.y,Math.max(80,e.r*2));g.addColorStop(0,e.type==='colossus'?'rgba(214,139,67,.24)':'rgba(174,70,63,.22)');g.addColorStop(1,'rgba(150,60,45,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(s.x,s.y,Math.max(80,e.r*2),0,Math.PI*2);ctx.fill();}
  ctx.save();ctx.filter=st.filter;drawAsset(st.asset,s.x,s.y-3+movingBob,st.w,st.h,Math.cos(e.dir||0)<0,0);ctx.restore();
  if(e.type==='tusker'||e.type==='siegebeast'||e.type==='colossus'){ctx.save();ctx.globalAlpha=.68;ctx.strokeStyle='#bbb29c';ctx.lineWidth=e.boss?4:3;ctx.beginPath();ctx.arc(s.x,s.y+2,e.r*.78,Math.PI*1.08,Math.PI*1.88);ctx.stroke();ctx.restore();}
  drawHealth(s.x,s.y-e.r-22,e.hp/e.maxHp,e.boss?86:e.type==='siegebeast'?56:44);
  if(e.raid||e.boss||!['wolf','boar','brute'].includes(e.type)){ctx.font=`800 ${e.boss?11:9}px sans-serif`;ctx.textAlign='center';ctx.fillStyle=e.boss?'#ffd09c':'#efb18e';ctx.shadowColor='#000';ctx.shadowBlur=4;ctx.fillText(e.boss?(e.bossName||st.label):st.label,s.x,s.y-e.r-31);ctx.shadowBlur=0;}
  const p=myPlayer();if(p?.autoTarget?.kind==='enemy'&&p.autoTarget.id===e.id){ctx.save();ctx.globalAlpha=.58+.32*Math.sin(v8PulseT*7)**2;circle(s.x,s.y+2,e.r+17,null,'#ff9b74',3);ctx.restore();}
};

const v10OldHud=updateHud;
updateHud=function(){
  v10OldHud();const p=myPlayer();if(!p||!snap)return;
  if($('weapon'))$('weapon').textContent=p.weapon;
  const title=document.querySelector('.personal > span');if(title)title.textContent='공용 무기';
  if($('meritLabel'))$('meritLabel').textContent=`공용 · ${p.weapon}`;
  const gear=(snap.personalPads||[])[0];
  if($('craftLabel'))$('craftLabel').textContent=gear?.complete?'공용 무기 최종 단계':gear?.locked?gear.reason:`다음 · ${gear.label}`;
  const boss=$('bossHud');if(boss&&snap.boss?.active){const n=boss.querySelector('b');if(n)n.textContent=snap.boss.name||'우두머리';}
};

const v10OldEvent=eventFx;
eventFx=function(m){
  v10OldEvent(m);
  if(m.kind==='weaponUpgrade'){toast(`공용 무기 강화 · ${m.from} → ${m.to} · 전원 적용`,'phaseAlert');constructionFx=1.9;burst(m.x,m.y,'#d8d59f',24,210);shake=5;}
  if(m.kind==='enemyTier'){toast(`거점 LV.${m.level} · 더 강한 적들이 진격하기 시작했습니다`,'phaseDanger');nightFlash=.35;}
  if(m.kind==='bossRaid'){toast(`우두머리 습격 · ${m.name}이 거점을 향해 진격합니다!`,'phaseDanger');nightFlash=1;shake=10;}
  if(m.kind==='bossDown'&&m.name){toast(`${m.name} 격파!`,'phaseAlert');nightFlash=.35;shake=9;}
  if(m.kind==='kill'&&m.playerId===meId&&V10_ENEMY_STYLE[m.enemyType]){const st=V10_ENEMY_STYLE[m.enemyType];if(!['wolf','boar','brute','alpha'].includes(m.enemyType))toast(`${st.label} 격파 · 식량 +${m.amount} · 공헌 +${m.meritGain}`);}
};
