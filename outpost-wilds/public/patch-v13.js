/* Outpost Wilds V13: shared stockpile, safe world reset, local movement reconciliation. */

v4Advance=function(){
  const now=performance.now(),dt=Math.min(.05,(now-v4RenderT)/1000);v4RenderT=now;
  if(!snap)return;
  for(const p of snap.players||[]){
    const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;
    if(p.id===meId){
      const moving=Math.hypot(input.x,input.y)>.025;
      if(moving){
        const q=Math.max(0,Math.min(1,(p.carry||0)/Math.max(1,p.carryCap||1)));
        const speed=212*Math.max(.86,1-.14*Math.pow(q,1.35));
        r.x=Math.max(35,Math.min(3565,r.x+input.x*speed*dt));
        r.y=Math.max(35,Math.min(3565,r.y+input.y*speed*dt));
      }
      const ex=r.tx-r.x,ey=r.ty-r.y,err=Math.hypot(ex,ey);
      if(err>120){r.x=r.tx;r.y=r.ty;}
      else if(!moving){const k=Math.min(1,dt*11);r.x+=ex*k;r.y+=ey*k;}
      else if(err>42){const k=Math.min(1,dt*4.2);r.x+=ex*k;r.y+=ey*k;}
      else if(err>18){const k=Math.min(1,dt*1.25);r.x+=ex*k;r.y+=ey*k;}
    }else{
      const k=Math.min(1,dt*13.5);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
    }
  }
  for(const e of snap.enemies||[]){const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;const k=Math.min(1,dt*11);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;}
};

function v13Stock(){return snap?.stockpile||null;}
function v13NearStock(){const p=myPlayer(),s=v13Stock();return !!(p&&s&&Math.hypot(p.x-s.x,p.y-s.y)<145);}
function v13EnsureStockHud(){
  let el=document.getElementById('v13StockHud');if(el)return el;
  el=document.createElement('div');el.id='v13StockHud';el.className='v13StockHud';
  const carry=document.querySelector('.carry.card');if(carry)carry.insertAdjacentElement('afterend',el);else document.getElementById('hud').appendChild(el);
  return el;
}
function v13DrawStockpile(){
  const st=v13Stock();if(!st)return;const s=worldToScreen(st.x,st.y),q=Math.min(1,(st.total||0)/Math.max(1,st.capacity||1));
  ctx.save();shadow(s.x,s.y+24,45,13,.3);ctx.fillStyle='#40382b';v4Rounded(s.x-43,s.y-27,86,55,9);ctx.fill();ctx.strokeStyle='#ae8955';ctx.lineWidth=3;ctx.stroke();
  ctx.fillStyle='#765638';ctx.fillRect(s.x-36,s.y-17,72,9);ctx.fillRect(s.x-36,s.y+4,72,9);ctx.fillStyle='#caa56a';ctx.fillRect(s.x-4,s.y-27,8,55);
  ctx.fillStyle='#172019';v4Rounded(s.x-42,s.y+36,84,16,8);ctx.fill();ctx.fillStyle='#a6d39b';ctx.fillRect(s.x-39,s.y+39,78*q,10);
  ctx.font='800 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#f4e3c1';ctx.fillText(`공용 비축고 ${st.total||0}/${st.capacity||0}`,s.x,s.y+64);ctx.restore();
}
const v13OldBase=drawBase;
drawBase=function(b){v13OldBase(b);v13DrawStockpile();};

const v13OldHud=updateHud;
updateHud=function(){
  v13OldHud();if(!snap)return;const st=v13Stock(),el=v13EnsureStockHud();
  if(st)el.innerHTML=`<span>공용 비축고</span><b>목 ${st.wood||0} · 돌 ${st.stone||0} · 식 ${st.meat||0}</b><small>${st.total||0}/${st.capacity||0}</small>`;
  if(v13NearStock()){$('contextHint').textContent=st.total>=st.capacity?'공용 비축고가 가득 찼습니다':'공용 비축고 · 이 위치에 서 있으면 들고 있는 자원을 자동 보관합니다';$('contextHint').className='show';}
};

function v13EnsureReset(){
  let b=document.getElementById('restartWorld');if(b)return b;
  b=document.createElement('button');b.id='restartWorld';b.type='button';b.textContent='처음부터';b.className='restartWorld';
  const brand=document.querySelector('.brand');brand?.appendChild(b);
  let armedUntil=0;
  b.onclick=()=>{const now=Date.now();if(now<armedUntil){armedUntil=0;b.classList.remove('armed');b.textContent='처음부터';send({type:'resetWorld',confirm:'RESET'});return;}armedUntil=now+4000;b.classList.add('armed');b.textContent='정말 초기화?';toast((snap?.players?.length||0)>1?'공동 월드 전체가 초기화됩니다 · 한 번 더 누르세요':'현재 진행을 처음부터 시작합니다 · 한 번 더 누르세요','phaseDanger');setTimeout(()=>{if(Date.now()>=armedUntil){armedUntil=0;b.classList.remove('armed');b.textContent='처음부터';}},4100);};
  return b;
}
v13EnsureReset();

const v13OldEvent=eventFx;
eventFx=function(m){
  v13OldEvent(m);
  if(m.kind==='stashDeposit'&&m.playerId===meId){toast(`비축고 보관 +${m.amount} · ${m.stockpile.wood}/${m.stockpile.stone}/${m.stockpile.meat}`);addFloater(`보관 +${m.amount}`,m.x,m.y-28,'#b7dda8',13);}
  if(m.kind==='worldReset'){toast(`${m.by}님이 공동 월드를 처음부터 시작했습니다`,'phaseAlert');nightFlash=.4;shake=5;const el=document.getElementById('v12Clear');el?.classList.remove('show');}
};
