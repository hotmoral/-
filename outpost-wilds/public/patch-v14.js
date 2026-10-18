/* Outpost Wilds V14: realtime chat, field rations, readable/polished base defenses. */
const V14_POS={workshop:{x:1575,y:1900},storage:{x:1510,y:1770},farm:{x:1540,y:2070},watchtower:{x:2040,y:1670},forge:{x:1580,y:1645},infirmary:{x:2090,y:1780},wall:{x:2200,y:2020},turret:{x:2050,y:1910},turret2:{x:2070,y:2150}};
const v14DefenseFx=new Map();

function v14Panel(x,y,w,h,r,top,bottom){
  const g=ctx.createLinearGradient(x,y,x,y+h);g.addColorStop(0,top);g.addColorStop(1,bottom);ctx.fillStyle=g;v4Rounded(x,y,w,h,r);ctx.fill();
}
function v14Label(text,x,y,accent='#e9d5a7'){
  ctx.save();ctx.font='800 9px system-ui,sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';const w=Math.max(46,ctx.measureText(text).width+14);ctx.fillStyle='rgba(8,13,11,.82)';v4Rounded(x-w/2,y-8,w,16,8);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.08)';ctx.stroke();ctx.fillStyle=accent;ctx.fillText(text,x,y);ctx.restore();
}
function v14RangeRing(pos,range){if(!snap?.wave?.active)return;const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.strokeStyle='rgba(229,190,105,.11)';ctx.lineWidth=2;ctx.setLineDash([10,15]);ctx.beginPath();ctx.arc(s.x,s.y,range,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);ctx.restore();}
function v14Fx(source){const fx=v14DefenseFx.get(source);if(!fx)return null;const age=(performance.now()-fx.at)/1000;if(age>1.4){v14DefenseFx.delete(source);return null}return{...fx,age};}

function v14DrawWorkshop(pos,lv){const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,24,46,13,.3);v14Panel(-43,-22,86,46,9,'#795735','#3c3128');ctx.fillStyle='#b7864d';for(let i=-30;i<=30;i+=20)ctx.fillRect(i,-16,12,6);ctx.fillStyle='#303532';v4Rounded(-28,-9,56,18,5);ctx.fill();ctx.fillStyle='#d8be83';ctx.fillRect(-18,-5,22,4);ctx.fillStyle='#8f9a94';ctx.beginPath();ctx.moveTo(10,-6);ctx.lineTo(26,-13);ctx.lineTo(30,-6);ctx.lineTo(15,3);ctx.closePath();ctx.fill();if(lv>=2){ctx.fillStyle='#5d4933';ctx.fillRect(-39,-34,6,20);ctx.fillRect(33,-34,6,20);ctx.fillStyle='#8d6b45';ctx.fillRect(-43,-38,86,7)}if(lv>=3){ctx.fillStyle='#d49b48';circle(0,-31,5,'#d49b48');}ctx.restore();v14Label(`작업대 LV.${lv}`,s.x,s.y+39);}
function v14DrawStorage(pos,lv){const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,26,48,15,.32);v14Panel(-42,-29,84,58,10,'#6e5438','#3e352b');ctx.fillStyle='#252b27';v4Rounded(-34,-19,68,38,6);ctx.fill();ctx.strokeStyle='#b38a55';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#8a6037';for(let y=-12;y<=10;y+=18){ctx.fillRect(-26,y,23,13);ctx.fillRect(5,y,22,13)}ctx.fillStyle='#d7b36f';ctx.fillRect(-4,-19,8,38);if(lv>=2){ctx.fillStyle='#6c7770';ctx.fillRect(-46,-36,92,8)}if(lv>=3){ctx.strokeStyle='#c7d5c5';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-24,-42);ctx.lineTo(24,-42);ctx.stroke();circle(0,-42,5,'#d7c276')}ctx.restore();v14Label(`보급 창고 LV.${lv}`,s.x,s.y+43,'#d9c08c');}
function v14DrawFarm(pos,lv){const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,22,52,15,.2);ctx.fillStyle='#4a3b29';v4Rounded(-49,-23,98,49,10);ctx.fill();for(let y=-15;y<=15;y+=15){ctx.strokeStyle='#806441';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(-39,y);ctx.lineTo(39,y);ctx.stroke();for(let x=-32;x<=32;x+=16){ctx.fillStyle=lv>=3?'#9ac66e':'#789955';ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-5,y-8);ctx.lineTo(x,y-5);ctx.lineTo(x+5,y-8);ctx.closePath();ctx.fill()}}ctx.strokeStyle='#b18a56';ctx.lineWidth=3;ctx.strokeRect(-49,-23,98,49);ctx.restore();v14Label(`농장 LV.${lv}`,s.x,s.y+39,'#b9dda0');}
function v14DrawForge(pos,lv){const s=worldToScreen(pos.x,pos.y),t=performance.now()*.006;ctx.save();ctx.translate(s.x,s.y);shadow(0,26,47,15,.34);v14Panel(-42,-28,84,56,10,'#555651','#272b29');ctx.fillStyle='#151916';v4Rounded(-28,-12,47,33,6);ctx.fill();const g=ctx.createRadialGradient(-6,7,2,-6,7,23);g.addColorStop(0,'#fff3a0');g.addColorStop(.38,'#e98542');g.addColorStop(1,'rgba(154,53,30,0)');ctx.fillStyle=g;circle(-6,7,20,g);ctx.fillStyle='#73766f';ctx.fillRect(24,-48,14,72);ctx.fillStyle='rgba(100,105,100,.24)';circle(31,-54+Math.sin(t)*3,10,'rgba(120,125,120,.18)');if(lv>=2){ctx.fillStyle='#929a91';ctx.fillRect(-39,-35,25,8)}if(lv>=3){ctx.strokeStyle='#e6c376';ctx.lineWidth=2;ctx.strokeRect(-42,-28,84,56)}ctx.restore();v14Label(`대장간 LV.${lv}`,s.x,s.y+42,'#f0bd71');}
function v14DrawInfirmary(pos,lv){const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,25,47,14,.28);ctx.fillStyle='#d4cfb7';ctx.beginPath();ctx.moveTo(-46,22);ctx.lineTo(-30,-30);ctx.lineTo(30,-30);ctx.lineTo(46,22);ctx.closePath();ctx.fill();ctx.fillStyle='#556b5c';ctx.fillRect(-4,-12,8,31);ctx.fillRect(-15,-2,30,8);ctx.fillStyle='#37453c';v4Rounded(-12,5,24,19,4);ctx.fill();if(lv>=2){ctx.strokeStyle='#8da398';ctx.lineWidth=3;ctx.stroke()}if(lv>=3){ctx.fillStyle='#d9b965';circle(0,-36,5,'#d9b965')}ctx.restore();v14Label(`회복소 LV.${lv}`,s.x,s.y+39,'#d8eadc');}
function v14DrawWall(pos,lv){const s=worldToScreen(pos.x,pos.y);ctx.save();ctx.translate(s.x,s.y);shadow(0,23,60,13,.32);ctx.fillStyle=lv>=2?'#696c67':'#70563c';for(let i=-54;i<=42;i+=24){v4Rounded(i,-22,20,45,4);ctx.fill();ctx.fillStyle='#393f3c';ctx.fillRect(i+6,-28,8,10);ctx.fillStyle=lv>=2?'#696c67':'#70563c'}ctx.strokeStyle=lv>=3?'#c0b279':'#987750';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-58,5);ctx.lineTo(58,5);ctx.stroke();ctx.restore();v14Label(`방벽 LV.${lv}`,s.x,s.y+38,'#d9cfac');}
function v14DrawWatchtower(pos,lv){const s=worldToScreen(pos.x,pos.y),fx=v14Fx('watchtower'),ang=fx?.angle??-.35,flash=fx&&fx.age<.2;v14RangeRing(pos,430+lv*35);ctx.save();ctx.translate(s.x,s.y);shadow(0,34,42,13,.34);ctx.strokeStyle='#6b5035';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-25,30);ctx.lineTo(-15,-42);ctx.moveTo(25,30);ctx.lineTo(15,-42);ctx.stroke();ctx.strokeStyle='#a27748';ctx.lineWidth=5;for(let y=15;y>-35;y-=18){ctx.beginPath();ctx.moveTo(-20,y);ctx.lineTo(20,y-12);ctx.stroke()}v14Panel(-34,-59,68,28,7,'#7a5a3a','#493826');ctx.fillStyle='#32291f';ctx.beginPath();ctx.moveTo(-44,-58);ctx.lineTo(0,-83);ctx.lineTo(44,-58);ctx.closePath();ctx.fill();ctx.translate(0,-47);ctx.rotate(ang);ctx.strokeStyle='#d0ab68';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(26,0);ctx.stroke();ctx.strokeStyle='#e7d7aa';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-7,-13);ctx.quadraticCurveTo(16,0,-7,13);ctx.stroke();if(flash){const g=ctx.createRadialGradient(29,0,1,29,0,17);g.addColorStop(0,'rgba(255,243,167,.95)');g.addColorStop(1,'rgba(255,184,72,0)');ctx.fillStyle=g;circle(29,0,17,g)}ctx.restore();v14Label(`망루 LV.${lv}${flash?' · 사격':''}`,s.x,s.y+48,flash?'#ffe09a':'#ebd0a0');}
function v14DrawTurret(pos,lv,id,outer=false){const s=worldToScreen(pos.x,pos.y),fx=v14Fx(id),ang=fx?.angle??(outer?-.7:.2),flash=fx&&fx.age<.16,range=(outer?580:520)+lv*35;v14RangeRing(pos,range);ctx.save();ctx.translate(s.x,s.y);shadow(0,23,43,13,.34);ctx.fillStyle=outer?'#444d4a':'#4d5853';ctx.beginPath();ctx.arc(0,10,outer?34:30,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#78877f';ctx.lineWidth=3;ctx.stroke();ctx.save();ctx.rotate(ang);v14Panel(-23,-15,46,30,11,outer?'#6d7774':'#727e78','#353d39');ctx.fillStyle='#222925';v4Rounded(7,-7,outer?53:45,14,5);ctx.fill();ctx.fillStyle='#9aa49e';ctx.fillRect(14,-3,outer?46:38,6);if(outer){ctx.fillStyle='#59635f';ctx.fillRect(-31,-9,12,18)}if(flash){const mx=outer?63:55,g=ctx.createRadialGradient(mx,0,1,mx,0,18);g.addColorStop(0,'rgba(255,239,155,.95)');g.addColorStop(1,'rgba(255,164,60,0)');ctx.fillStyle=g;circle(mx,0,18,g)}ctx.restore();ctx.fillStyle='#d6ad5e';circle(-7,4,5,'#d6ad5e');ctx.restore();v14Label(`${outer?'외곽 터렛':'자동 터렛'} LV.${lv}${flash?' · 사격':''}`,s.x,s.y+43,flash?'#ffe092':'#d7d8c4');}

v6DrawBuiltFacilities=function(){
  const f=snap?.facilities||{};
  if(f.workshop)v14DrawWorkshop(V14_POS.workshop,f.workshop);
  if(f.storage)v14DrawStorage(V14_POS.storage,f.storage);
  if(f.farm)v14DrawFarm(V14_POS.farm,f.farm);
  if(f.watchtower)v14DrawWatchtower(V14_POS.watchtower,f.watchtower);
  if(f.forge)v14DrawForge(V14_POS.forge,f.forge);
  if(f.infirmary)v14DrawInfirmary(V14_POS.infirmary,f.infirmary);
  if(f.wall)v14DrawWall(V14_POS.wall,f.wall);
  if(f.turret)v14DrawTurret(V14_POS.turret,f.turret,'turret',false);
  if(f.turret2)v14DrawTurret(V14_POS.turret2,f.turret2,'turret2',true);
};

function v14EnsureChat(){
  let root=document.getElementById('v14Chat');if(root)return root;
  root=document.createElement('div');root.id='v14Chat';root.className='v14Chat';root.innerHTML='<button class="v14ChatToggle" type="button">채팅 <i></i></button><section><header><b>생존자 채팅</b><button class="v14ChatClose" type="button">×</button></header><div class="v14ChatLog"></div><form><input maxlength="80" autocomplete="off" placeholder="메시지 입력…"><button type="submit">전송</button></form></section>';
  document.body.appendChild(root);
  const toggle=root.querySelector('.v14ChatToggle'),close=root.querySelector('.v14ChatClose'),form=root.querySelector('form'),inputEl=root.querySelector('input');
  toggle.onclick=()=>{root.classList.toggle('open');if(root.classList.contains('open')){toggle.querySelector('i').textContent='';setTimeout(()=>inputEl.focus(),60)}};
  close.onclick=()=>root.classList.remove('open');
  for(const ev of['keydown','keyup','pointerdown','pointermove','pointerup'])inputEl.addEventListener(ev,e=>e.stopPropagation());
  form.onsubmit=e=>{e.preventDefault();const text=inputEl.value.trim();if(!text)return;send({type:'chat',text});inputEl.value='';inputEl.focus();};
  return root;
}
function v14ChatMessage(m){
  const root=v14EnsureChat(),log=root.querySelector('.v14ChatLog'),row=document.createElement('div');row.className='v14ChatRow'+(m.playerId===meId?' me':'');const name=document.createElement('b'),text=document.createElement('span');name.textContent=m.name||'생존자';text.textContent=m.text||'';row.append(name,text);log.appendChild(row);while(log.children.length>28)log.firstChild.remove();log.scrollTop=log.scrollHeight;if(!root.classList.contains('open')){const badge=root.querySelector('.v14ChatToggle i'),n=Math.min(99,(Number(badge.textContent)||0)+1);badge.textContent=String(n)}}
v14EnsureChat();

function v14EnsureEat(){let b=document.getElementById('eatMeat');if(b)return b;b=document.createElement('button');b.id='eatMeat';b.type='button';b.className='v14Eat';b.textContent='고기 먹기';b.onclick=()=>send({type:'eat'});document.querySelector('.carry.card')?.appendChild(b);return b;}
v14EnsureEat();

const v14OldHud=updateHud;
updateHud=function(){v14OldHud();const p=myPlayer(),b=v14EnsureEat();if(p&&b){b.disabled=(p.meat||0)<=0;b.textContent=`고기 먹기 · ${Math.min(3,p.meat||0)}`;b.title='고기 최대 3개를 소비해 체력을 회복합니다';}};

const v14OldEvent=eventFx;
eventFx=function(m){
  if(m.kind==='kill'&&m.lootTo==='stockpile'){
    if(m.playerId===meId){const name=m.enemyName||m.enemyType||'적';toast(`${name} 처치 · 고기 ${m.amount} → 공용 비축고 · 공헌 +${m.meritGain}`,'phaseAlert');addFloater(`비축고 +${m.amount}`,m.x,m.y-22,'#c6e2a5',13);}burst(m.x,m.y,'#e3be82',6,120);
  }else v14OldEvent(m);
  if(m.kind==='chat')v14ChatMessage(m);
  if(m.kind==='meal'&&m.playerId===meId)toast(`고기 ${m.used} 소비 · 체력 +${m.healed}`,'phaseAlert');
  if(m.kind==='raidLoot'&&m.playerId===meId&&m.overflow>0)toast(`비축고가 가득 차 고기 ${m.overflow}개를 보관하지 못했습니다`,'phaseAlert');
  if(m.kind==='towerShot'){
    v14DefenseFx.set(m.source,{at:performance.now(),angle:Math.atan2(m.y2-m.y1,m.x2-m.x1),damage:m.damage,targetId:m.targetId});
    burst(m.x2,m.y2,m.source==='watchtower'?'#e6ce91':'#ffd06d',m.source==='watchtower'?7:10,m.source==='watchtower'?105:150);
    if(m.damage)addFloater(`-${m.damage}`,m.x2,m.y2-16,m.source==='watchtower'?'#efdca8':'#ffd58a',11);
  }
};
