'use strict';
const $ = s => document.querySelector(s);
const app = document.getElementById('app');
let roomId = location.pathname.match(/^\/r\/([A-Z0-9]+)/)?.[1] || null;
let role = 'spectator', token = null, state = null, seenSeq = -1;
let polling = null, canvas, ctx, dpr = 1, displayStones = [], animating = false;
let drag = null, toastTimer = null;
const keys = id => `alkkagi:${id}:token`;

function toast(msg){
  let el=$('.toast'); if(!el){el=document.createElement('div');el.className='toast';document.body.appendChild(el)}
  el.textContent=msg; el.classList.add('show'); clearTimeout(toastTimer); toastTimer=setTimeout(()=>el.classList.remove('show'),1500);
}
async function api(path, opts={}){
  const r=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});
  const j=await r.json().catch(()=>({})); if(!r.ok) throw Object.assign(new Error(j.error||'REQUEST_FAILED'),{code:j.error,status:r.status}); return j;
}
function landing(){
  app.innerHTML=`<main class="shell"><section class="card landing">
    <div class="emblem"><i class="stone"></i><i class="stone"></i></div>
    <h1>알까기 <span>DUEL</span></h1>
    <p>친구에게 초대 링크를 보내세요. 두 사람이 같은 판에서 번갈아 돌을 튕겨 마지막까지 살아남으면 승리합니다.</p>
    <button class="primary" id="create">대전방 만들기</button>
    <p class="tiny">설치 없이 모바일 브라우저에서 바로 플레이</p>
  </section></main>`;
  $('#create').onclick=async()=>{ const b=$('#create'); b.disabled=true; b.textContent='방 만드는 중…'; try{const x=await api('/api/rooms',{method:'POST'});localStorage.setItem(keys(x.roomId),x.token);location.href=`/r/${x.roomId}`;}catch{b.disabled=false;b.textContent='대전방 만들기';toast('방을 만들지 못했습니다');} };
}
function gameUI(){
  app.innerHTML=`<main class="shell">
    <header class="brand"><div class="logo">알까기 <b>DUEL</b></div><div class="top-actions"><button class="icon-btn" id="copy">초대 링크</button><span class="room-code">ROOM ${roomId}</span></div></header>
    <section class="scorebar">
      <div class="player" id="pBlack"><i class="mini-stone black"></i><div><div class="who">BLACK</div><div class="count" id="cBlack">7</div></div></div>
      <div class="versus">VS</div>
      <div class="player right" id="pWhite"><div><div class="who">WHITE</div><div class="count" id="cWhite">7</div></div><i class="mini-stone white"></i></div>
    </section>
    <div class="status" id="status">접속 중…</div>
    <section class="board-wrap"><canvas id="board"></canvas><div class="wait-overlay hidden" id="wait"><div class="wait-card"><h2>상대를 기다리는 중</h2><p>아래 링크를 친구에게 보내면 바로 백돌로 참가합니다.</p><div class="invite"><code id="link"></code><button class="icon-btn" id="copy2">복사</button></div></div></div></section>
    <div class="power"><i id="powerBar"></i></div>
    <div class="hint" id="hint">내 돌을 누르고 원하는 방향의 반대로 당겼다가 놓으세요.</div>
    <div class="controls"><button class="secondary hidden" id="rematch">재대결</button><button class="danger" id="resign">기권</button></div>
  </main>`;
  canvas=$('#board'); ctx=canvas.getContext('2d');
  resize(); addEventListener('resize',resize);
  canvas.addEventListener('pointerdown',pointerDown); canvas.addEventListener('pointermove',pointerMove); canvas.addEventListener('pointerup',pointerUp); canvas.addEventListener('pointercancel',cancelDrag);
  $('#copy').onclick=copyInvite; $('#copy2').onclick=copyInvite; $('#link').textContent=location.href;
  $('#resign').onclick=resign; $('#rematch').onclick=rematch;
  requestAnimationFrame(drawLoop);
}
function resize(){ if(!canvas)return; const r=canvas.getBoundingClientRect(); dpr=Math.min(devicePixelRatio||1,2); canvas.width=Math.round(r.width*dpr);canvas.height=Math.round(r.height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0); }
function copyInvite(){navigator.clipboard?.writeText(location.href).then(()=>toast('초대 링크를 복사했습니다')).catch(()=>toast('주소창의 링크를 복사해주세요'));}
function boardPos(e){const r=canvas.getBoundingClientRect();return{x:(e.clientX-r.left)/r.width*1000,y:(e.clientY-r.top)/r.height*1000};}
function pointerDown(e){
  if(!state||animating||state.phase!=='playing'||role!==state.turn)return;
  const p=boardPos(e); let best=null,dist=1e9;
  for(const s of displayStones){if(!s.alive||s.owner!==role)continue;const d=Math.hypot(s.x-p.x,s.y-p.y);if(d<dist){dist=d;best=s}}
  if(best&&dist<60){drag={stoneId:best.id,start:{x:best.x,y:best.y},cur:p};canvas.setPointerCapture?.(e.pointerId);navigator.vibrate?.(10);}
}
function pointerMove(e){if(!drag)return;drag.cur=boardPos(e);const m=Math.min(1,Math.hypot(drag.start.x-drag.cur.x,drag.start.y-drag.cur.y)/230);$('#powerBar').style.width=`${Math.round(m*100)}%`;}
function cancelDrag(){drag=null;if($('#powerBar'))$('#powerBar').style.width='0%';}
async function pointerUp(e){
  if(!drag)return; const d=drag; drag=null; $('#powerBar').style.width='0%';
  const p=boardPos(e), dx=d.start.x-p.x,dy=d.start.y-p.y,mag=Math.hypot(dx,dy);
  if(mag<20){toast('조금 더 당겨주세요');return}
  const speed=Math.min(1450,mag*5.4);const vx=dx/mag*speed,vy=dy/mag*speed;
  animating=true;navigator.vibrate?.(18);
  try{const next=await api(`/api/room/${roomId}/shot`,{method:'POST',body:JSON.stringify({token,stoneId:d.stoneId,vx,vy})});await applyState(next,true);}catch(err){animating=false;toast(err.code==='NOT_YOUR_TURN'?'상대 차례입니다':'샷을 처리하지 못했습니다');await poll();}
}
async function resign(){if(!state||state.phase!=='playing'||(role!=='black'&&role!=='white'))return; if(!confirm('이번 판을 기권할까요?'))return;try{const x=await api(`/api/room/${roomId}/resign`,{method:'POST',body:JSON.stringify({token})});applyState(x,false)}catch{toast('기권 처리에 실패했습니다')}}
async function rematch(){try{const x=await api(`/api/room/${roomId}/rematch`,{method:'POST',body:JSON.stringify({token})});applyState(x,false);toast(x.phase==='playing'?'재대결 시작!':'상대의 재대결 선택을 기다립니다')}catch{toast('재대결 요청에 실패했습니다')}}
function stoneMapFrame(frame){const owners=Object.fromEntries((state?.stones||[]).map(s=>[s.id,s.owner]));return frame.map(v=>({id:v[0],x:v[1],y:v[2],alive:!!v[3],owner:owners[v[0]] || (v[0][0]==='B'?'black':'white')}));}
async function animate(anim){
  if(!anim||!anim.frames?.length){animating=false;return}
  animating=true; const start=performance.now(),dur=anim.durationMs||anim.frames.length*50;
  await new Promise(resolve=>{function step(now){const t=Math.min(1,(now-start)/dur);const idx=Math.min(anim.frames.length-1,Math.floor(t*(anim.frames.length-1)));displayStones=stoneMapFrame(anim.frames[idx]);if(t<1)requestAnimationFrame(step);else resolve()}requestAnimationFrame(step)});
  animating=false; displayStones=state.stones.map(s=>({...s})); navigator.vibrate?.(anim.fallen?.black||anim.fallen?.white?[25,35,45]:12);
}
async function applyState(next, forceAnim=false){
  const oldSeq=seenSeq; state=next; role=next.role||role; seenSeq=Math.max(seenSeq,next.shotSeq??seenSeq);
  if(!animating)displayStones=next.stones.map(s=>({...s}));
  updateUI();
  if(next.animation && (forceAnim || next.animation.seq>oldSeq)){await animate(next.animation);displayStones=next.stones.map(s=>({...s}));updateUI();}
}
function updateUI(){if(!state)return;
  $('#cBlack').textContent=state.remaining.black;$('#cWhite').textContent=state.remaining.white;
  $('#pBlack').classList.toggle('active',state.turn==='black'&&state.phase==='playing');$('#pWhite').classList.toggle('active',state.turn==='white'&&state.phase==='playing');
  $('#wait').classList.toggle('hidden',state.phase!=='waiting'||role!=='black');
  const st=$('#status'),hint=$('#hint'),rm=$('#rematch'),rs=$('#resign');st.className='status';
  if(state.phase==='waiting'){st.textContent=role==='black'?'초대 링크를 보내 상대를 불러오세요':'대전 상대를 기다리는 방입니다';hint.textContent='두 번째 플레이어가 들어오면 자동으로 시작합니다.'}
  else if(state.phase==='finished'){
    const win=state.winner===role, draw=state.winner==='draw'; st.textContent=draw?'무승부':win?'승리! 마지막 돌까지 살아남았습니다':role==='spectator'?`${state.winner==='black'?'흑돌':'백돌'} 승리`:'패배';st.classList.add(draw?'':win?'win':'lose');
    hint.textContent=role==='spectator'?'관전이 종료되었습니다.':'재대결은 두 명 모두 선택하면 시작됩니다.';rm.classList.toggle('hidden',role==='spectator');rs.classList.add('hidden');
    if((role==='black'||role==='white')&&!draw&&win)navigator.vibrate?.([50,40,70]);
  } else {
    const mine=state.turn===role;st.textContent=role==='spectator'?(state.turn==='black'?'흑돌 차례':'백돌 차례'):(mine?'내 차례 · 돌을 튕기세요':'상대 차례');if(mine)st.classList.add('mine');
    hint.textContent=role==='spectator'?'관전 중입니다.':mine?'내 돌을 누르고 원하는 방향의 반대로 당겼다가 놓으세요.':'상대가 수를 두고 있습니다.';rm.classList.add('hidden');rs.classList.toggle('hidden',role==='spectator');
  }
}
function drawBoard(){
  if(!ctx||!canvas)return;const w=canvas.getBoundingClientRect().width,h=w,s=w/1000;ctx.clearRect(0,0,w,h);
  const g=ctx.createLinearGradient(0,0,w,h);g.addColorStop(0,'#e1b56f');g.addColorStop(.52,'#c68d45');g.addColorStop(1,'#a86f33');ctx.fillStyle=g;ctx.fillRect(0,0,w,h);
  ctx.save();ctx.globalAlpha=.09;ctx.strokeStyle='#6f3e1d';for(let i=0;i<34;i++){const y=(i*73%1000)*s;ctx.beginPath();ctx.moveTo(0,y);for(let x=0;x<=1000;x+=90)ctx.lineTo(x*s,y+Math.sin((x+i*29)/115)*4*s);ctx.stroke()}ctx.restore();
  const pad=75*s, step=(850/14)*s;ctx.strokeStyle='#3b2517bb';ctx.lineWidth=Math.max(1,s*.9);for(let i=0;i<15;i++){const v=pad+i*step;ctx.beginPath();ctx.moveTo(pad,v);ctx.lineTo(w-pad,v);ctx.stroke();ctx.beginPath();ctx.moveTo(v,pad);ctx.lineTo(v,h-pad);ctx.stroke()}
  ctx.fillStyle='#332115';for(const [a,b] of [[3,3],[3,11],[7,7],[11,3],[11,11]]){ctx.beginPath();ctx.arc(pad+a*step,pad+b*step,4*s,0,Math.PI*2);ctx.fill()}
}
function drawStone(s){if(!s.alive)return;const w=canvas.getBoundingClientRect().width,k=w/1000,x=s.x*k,y=s.y*k,r=31*k;ctx.save();ctx.shadowColor='rgba(0,0,0,.42)';ctx.shadowBlur=14*k;ctx.shadowOffsetY=7*k;const gr=ctx.createRadialGradient(x-r*.35,y-r*.45,r*.08,x,y,r);if(s.owner==='black'){gr.addColorStop(0,'#77736d');gr.addColorStop(.22,'#393734');gr.addColorStop(.7,'#161513');gr.addColorStop(1,'#050505')}else{gr.addColorStop(0,'#ffffff');gr.addColorStop(.35,'#f2efe8');gr.addColorStop(.76,'#d2cdc3');gr.addColorStop(1,'#9f998e')}ctx.fillStyle=gr;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.shadowColor='transparent';ctx.strokeStyle=s.owner==='black'?'#ffffff18':'#ffffff88';ctx.lineWidth=Math.max(1,k);ctx.stroke();ctx.restore()}
function drawAim(){if(!drag)return;const w=canvas.getBoundingClientRect().width,k=w/1000;const s=displayStones.find(x=>x.id===drag.stoneId);if(!s)return;const dx=drag.start.x-drag.cur.x,dy=drag.start.y-drag.cur.y,mag=Math.hypot(dx,dy);if(mag<3)return;const ux=dx/mag,uy=dy/mag,len=Math.min(260,mag*1.25);const x=s.x*k,y=s.y*k,ex=(s.x+ux*len)*k,ey=(s.y+uy*len)*k;ctx.save();ctx.strokeStyle='rgba(255,245,214,.92)';ctx.fillStyle='rgba(255,245,214,.92)';ctx.lineWidth=3*k;ctx.setLineDash([10*k,8*k]);ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(ex,ey);ctx.stroke();ctx.setLineDash([]);const a=Math.atan2(ey-y,ex-x);ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-Math.cos(a-.55)*15*k,ey-Math.sin(a-.55)*15*k);ctx.lineTo(ex-Math.cos(a+.55)*15*k,ey-Math.sin(a+.55)*15*k);ctx.closePath();ctx.fill();ctx.beginPath();ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=2*k;ctx.arc(x,y,42*k,0,Math.PI*2);ctx.stroke();ctx.restore()}
function drawLoop(){drawBoard();for(const s of displayStones)drawStone(s);drawAim();requestAnimationFrame(drawLoop)}
async function poll(){if(!roomId)return;try{const q=new URLSearchParams({after:String(seenSeq),token:token||''});const x=await api(`/api/room/${roomId}?${q}`);await applyState(x,false)}catch(e){if(e.status===404){clearInterval(polling);toast('방이 만료되었습니다')}}}
async function join(){
  gameUI(); token=localStorage.getItem(keys(roomId));
  try{const x=await api(`/api/room/${roomId}/join`,{method:'POST',body:JSON.stringify({token})});token=x.token;if(x.role!=='spectator'&&token)localStorage.setItem(keys(roomId),token);role=x.role;await applyState({...x.state,role},false);seenSeq=x.state.shotSeq;polling=setInterval(poll,550);}catch(e){$('#status').textContent=e.status===404?'존재하지 않거나 만료된 방입니다':'방에 접속하지 못했습니다';$('#hint').textContent='새 대전방을 만들어 다시 시작해주세요.';}
}
if(roomId)join();else landing();
