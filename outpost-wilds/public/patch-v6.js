/* Outpost Wilds V6: physical build pads, prerequisite facilities, resource-fed gear upgrades. */
const v6OldHud=updateHud;
function v6IconImg(kind){const src=kind==='wood'?'/assets/res-wood.svg':kind==='stone'?'/assets/res-stone.svg':'/assets/res-meat.svg';return `<img src="${src}" alt="">`;}
function v6NeedHtml(cost,progress){if(!cost)return'';return ['wood','stone','meat'].filter(k=>(cost[k]||0)>0).map(k=>{const left=Math.max(0,(cost[k]||0)-(progress?.[k]||0));return `<i class="${left===0?'done':''}">${v6IconImg(k)}<b>${left}</b></i>`}).join('');}
function v6AllPads(){return[...(snap?.pads||[]),...(snap?.personalPads||[])];}
function v6NearestPad(p){let best=null,d=150;for(const pad of v6AllPads()){const q=Math.hypot(p.x-pad.x,p.y-pad.y);if(q<d){d=q;best=pad}}return best;}
updateHud=function(){v6OldHud();const p=myPlayer();if(!p||!snap)return;
  $('meritLabel').textContent=`장비 · ${p.weapon}`;
  const gear=(snap.personalPads||[])[0];$('craftLabel').textContent=gear?.complete?'최고 장비 완성':gear?.locked?gear.reason:'장비 강화 칸에서 자원 투입';
  const pad=v6NearestPad(p),hint=$('contextHint');
  if(pad){if(pad.complete){hint.textContent=pad.kind==='gear'?'현재 최고 장비입니다':`${pad.label} 완성`;hint.className='show';}
    else if(pad.locked){hint.textContent=`🔒 ${pad.label} · ${pad.reason}`;hint.className='show';}
    else{hint.textContent=`${pad.label} · 칸 위에 서 있으면 필요한 자원이 자동 투입됩니다`;hint.className='show';}
  }
  const target=pad&&!pad.complete?pad:(snap.pads||[]).find(x=>!x.complete&&!x.locked);
  if(target){$('missionTitle').textContent=target.locked?`${target.label} 잠김`:target.label;$('missionCost').innerHTML=v6NeedHtml(target.cost,target.progress);const ks=['wood','stone','meat'].filter(k=>(target.cost?.[k]||0)>0);const ratio=ks.length?ks.reduce((a,k)=>a+Math.min(1,(target.progress?.[k]||0)/(target.cost[k]||1)),0)/ks.length:1;$('missionFill').style.width=`${ratio*100}%`;}
  else{$('missionTitle').textContent='현재 가능한 건설 완료';$('missionCost').innerHTML='';$('missionFill').style.width='100%';}
};

function v6DrawIcon(kind,x,y,size=20){const im=v5Assets[kind];if(im?.complete)ctx.drawImage(im,x-size/2,y-size/2,size,size);}
function v6RoundRect(x,y,w,h,r){ctx.beginPath();ctx.roundRect?ctx.roundRect(x,y,w,h,r):v4Rounded(x,y,w,h,r);}
function v6PadProgress(pad){if(!pad.cost)return 1;let total=0,got=0;for(const k of['wood','stone','meat']){const c=pad.cost[k]||0;if(c){total+=c;got+=Math.min(c,pad.progress?.[k]||0)}}return total?got/total:1;}
function v6DrawPad(pad){if(pad.complete&&pad.kind!=='base')return;const s=worldToScreen(pad.x,pad.y),w=pad.size||104,h=82,q=v6PadProgress(pad);ctx.save();
  shadow(s.x,s.y+27,w*.46,14,.24);
  ctx.translate(s.x,s.y);ctx.fillStyle=pad.locked?'rgba(39,42,40,.78)':pad.kind==='gear'?'rgba(64,76,61,.82)':'rgba(82,68,48,.82)';v6RoundRect(-w/2,-h/2,w,h,13);ctx.fill();
  ctx.strokeStyle=pad.locked?'#777b7888':pad.kind==='gear'?'#9bc393aa':'#dfba72aa';ctx.lineWidth=2;ctx.stroke();
  if(!pad.locked&&!pad.complete){ctx.fillStyle=pad.kind==='gear'?'#8bb98a28':'#e4bd6e24';ctx.fillRect(-w/2,-h/2,w*q,h);}
  ctx.font='800 10px sans-serif';ctx.textAlign='center';ctx.fillStyle=pad.locked?'#aeb1ae':'#f5e5c4';ctx.fillText(pad.label,0,-23);
  if(pad.locked){ctx.font='700 18px sans-serif';ctx.fillText('🔒',0,2);ctx.font='600 7px sans-serif';ctx.fillStyle='#c5c4bf';const text=(pad.reason||'선행조건 필요').slice(0,23);ctx.fillText(text,0,25);ctx.restore();return;}
  if(pad.complete){ctx.font='800 10px sans-serif';ctx.fillStyle='#a9d89b';ctx.fillText('완료',0,8);ctx.restore();return;}
  let items=[];for(const k of['wood','stone','meat']){const c=pad.cost?.[k]||0;if(!c)continue;items.push({k,left:Math.max(0,c-(pad.progress?.[k]||0))});}
  const step=items.length===3?31:38,start=-(items.length-1)*step/2;items.forEach((it,i)=>{const x=start+i*step;v6DrawIcon(it.k,x,-2,21);ctx.font='800 9px sans-serif';ctx.fillStyle=it.left===0?'#9fd091':'#fff1d2';ctx.fillText(it.left,x,21);});
  ctx.restore();}
function v6DrawWorkshop(x,y){ctx.save();ctx.translate(x,y);shadow(0,18,42,13,.27);ctx.fillStyle='#684b32';v6RoundRect(-36,-2,72,15,5);ctx.fill();ctx.fillStyle='#b28550';v6RoundRect(-31,-10,62,11,4);ctx.fill();ctx.fillStyle='#454a47';ctx.beginPath();ctx.moveTo(-13,-22);ctx.lineTo(15,-22);ctx.lineTo(24,-11);ctx.lineTo(13,-3);ctx.lineTo(-18,-5);ctx.closePath();ctx.fill();ctx.fillStyle='#735238';ctx.fillRect(-25,12,7,22);ctx.fillRect(18,12,7,22);ctx.restore();}
function v6DrawForge(x,y){ctx.save();ctx.translate(x,y);shadow(0,21,43,15,.3);ctx.fillStyle='#514d47';v6RoundRect(-35,-12,70,38,9);ctx.fill();ctx.fillStyle='#2b2926';v6RoundRect(-22,-4,35,23,5);ctx.fill();const g=ctx.createRadialGradient(-5,7,2,-5,7,22);g.addColorStop(0,'#ffd76f');g.addColorStop(.4,'#d86d39');g.addColorStop(1,'rgba(120,47,31,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(-5,7,22,0,Math.PI*2);ctx.fill();ctx.fillStyle='#7e7468';ctx.fillRect(20,-30,12,55);ctx.restore();}
function v6DrawTurret(x,y){ctx.save();ctx.translate(x,y);shadow(0,18,39,13,.3);ctx.fillStyle='#555d58';ctx.beginPath();ctx.arc(0,8,30,0,Math.PI*2);ctx.fill();ctx.fillStyle='#727c75';v6RoundRect(-22,-16,44,29,10);ctx.fill();ctx.fillStyle='#303735';v6RoundRect(5,-10,43,9,4);ctx.fill();circle(-7,-3,6,'#d89e51');ctx.restore();}
function v6DrawBuiltFacilities(){if(!snap?.facilities)return;const f=snap.facilities;if(f.workshop){const s=worldToScreen(1575,1900);v6DrawWorkshop(s.x,s.y)}if(f.watchtower){const s=worldToScreen(2040,1670);drawTower(s.x,s.y)}if(f.forge){const s=worldToScreen(1580,1645);v6DrawForge(s.x,s.y)}if(f.turret){const s=worldToScreen(2050,1910);v6DrawTurret(s.x,s.y)}}
const v6OldBase=drawBase;
drawBase=function(b){for(const pad of v6AllPads())v6DrawPad(pad);const s=worldToScreen(b.x,b.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,52,145,45,.34);ctx.fillStyle=b.level>=4?'#696a65':'#78583d';v6RoundRect(-72,-35,144,90,12);ctx.fill();ctx.fillStyle='#3e3025';ctx.beginPath();ctx.moveTo(-94,-31);ctx.lineTo(0,-110);ctx.lineTo(94,-31);ctx.closePath();ctx.fill();ctx.strokeStyle='#9c774d';ctx.lineWidth=4;ctx.stroke();ctx.fillStyle='#35261e';v6RoundRect(-15,12,30,43,5);ctx.fill();circle(0,0,23,'#d88745');circle(0,0,10,'#ffd574');if(b.level>=2){drawTent(-112,55,.78);drawTent(108,62,.72)}if(b.level>=4){ctx.strokeStyle='#858985';ctx.lineWidth=5;ctx.beginPath();ctx.arc(0,0,178,.25,Math.PI*1.75);ctx.stroke()}if(b.level>=5){ctx.strokeStyle='#d8b862';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,120,0,Math.PI*2);ctx.stroke();circle(0,-132,9,'#f2c96d')}ctx.restore();v6DrawBuiltFacilities();};

const v6OldEvent=eventFx;
eventFx=function(m){v6OldEvent(m);if(m.kind==='padDeposit'){if(m.playerId===meId){const pad=v6AllPads().find(p=>p.id===m.project);toast(`${pad?.label||'건설'}에 자원 투입 +${m.amount}`);addFloater(`+${m.amount}`,m.x,m.y-30,'#f2d18a',13);}burst(m.x,m.y,'#d6b06a',5,90);}
  if(m.kind==='constructionComplete'){toast(`${m.label} 건설 완료!`,'phaseAlert');constructionFx=1.6;burst(m.x,m.y,'#e7bd68',22,210);shake=6;}
  if(m.kind==='gearUpgrade'&&m.playerId===meId){toast(`${m.weapon} 업그레이드 완료!`,'phaseAlert');burst(m.x,m.y,'#b9d9ad',18,170);shake=4;}
};
