const $=s=>document.querySelector(s);
const home=$('#home'), game=$('#game'), canvas=$('#arena'), ctx=canvas.getContext('2d');
const qs=new URLSearchParams(location.search); let room=(qs.get('room')||'').toUpperCase();
let socket=null, role='spectator', me=null, state=null, queuedState=null, selectedWeapon='knife', anim=null, toastTimer=null;
const angle=$('#angle'), power=$('#power');

function code(){const c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';return Array.from({length:6},()=>c[Math.floor(Math.random()*c.length)]).join('')}
if(!room){home.classList.remove('hidden')}else{game.classList.remove('hidden');connect()}
$('#createBtn').onclick=()=>{location.href='/?room='+code()};
$('#shareBtn').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);toast('초대 링크를 복사했습니다.')}catch{toast('주소창의 링크를 상대에게 보내세요.')}};
$('#roomCode').textContent=room||'-----';
angle.oninput=()=>$('#angleVal').textContent=angle.value+'°'; power.oninput=()=>$('#powerVal').textContent=power.value;
$('#weapons').onclick=e=>{const b=e.target.closest('button[data-w]');if(!b)return;selectedWeapon=b.dataset.w;document.querySelectorAll('#weapons button').forEach(x=>x.classList.toggle('selected',x===b));};
$('#leftBtn').onclick=()=>send({type:'move',delta:-18}); $('#rightBtn').onclick=()=>send({type:'move',delta:18});
$('#fireBtn').onclick=()=>send({type:'fire',weapon:selectedWeapon,angle:+angle.value,power:+power.value});
$('#rematchBtn').onclick=()=>send({type:'rematch'});
function send(o){if(socket&&socket.readyState===1)socket.send(JSON.stringify(o))}
function toast(t,ms=1800){const el=$('#statusToast');el.textContent=t;el.classList.remove('hide');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.add('hide'),ms)}
function connect(){
 const proto=location.protocol==='https:'?'wss':'ws'; socket=new WebSocket(`${proto}://${location.host}/?room=${room}`);
 socket.onopen=()=>toast('서버 연결 완료'); socket.onclose=()=>{toast('연결이 끊겼습니다. 재접속 중...',5000);setTimeout(connect,1800)};
 socket.onmessage=e=>{const m=JSON.parse(e.data);if(m.type==='hello'){role=m.role;me=m.index;applyState(m.state);toast(role==='player'?(me===0?'BLACK으로 참가했습니다.':'WHITE로 참가했습니다.'):'관전자로 참가했습니다.',2500)}if(m.type==='state'){if(anim)queuedState=m.state;else applyState(m.state)}if(m.type==='shot')startShot(m.shot,m.state);if(m.type==='notice')toast(m.message,3000);};
}
function applyState(s){state=s;$('#round').textContent=s.round;$('#moveLeft').textContent=Math.round(s.moveLeft);for(let i=0;i<2;i++){const hp=Math.max(0,s.players[i].hp);$('#hp'+i).style.width=hp+'%';$('#hpText'+i).textContent=hp+' HP'}
 const both=s.connected[0]&&s.connected[1];const myTurn=role==='player'&&me===s.turn&&both&&!s.resolving&&s.winner===null;
 $('#turnText').textContent=!both?'상대 접속 대기':s.winner!==null?'라운드 종료':s.resolving?'탄도 계산 중':(s.turn===0?'BLACK TURN':'WHITE TURN');
 const arrows=s.wind>0?'▶':'◀';$('#wind').textContent=`WIND ${arrows} ${Math.abs(s.wind*100).toFixed(1)}`;
 $('#roleText').textContent=role==='player'?(me===0?'YOU ARE BLACK · 왼쪽 진영':'YOU ARE WHITE · 오른쪽 진영'):'SPECTATOR MODE';
 ['#leftBtn','#rightBtn','#fireBtn'].forEach(q=>$(q).disabled=!myTurn);document.querySelectorAll('#weapons button').forEach(b=>b.disabled=!myTurn);
 if(s.winner!==null){const r=$('#result');r.classList.remove('hidden');let title='DRAW',sub='두 캐릭터가 동시에 쓰러졌습니다.';if(s.winner!=='draw'){title=(role==='player'&&s.winner===me)?'VICTORY':'DEFEAT';sub=s.winner===0?'BLACK이 승리했습니다.':'WHITE가 승리했습니다.'}$('#resultTitle').textContent=title;$('#resultSub').textContent=sub;$('#rematchBtn').style.display=role==='player'?'inline-block':'none'}else $('#result').classList.add('hidden');
}
function startShot(shot,finalState){anim={shot,start:performance.now(),finalState,impactAt:null};toast(weaponName(shot.weapon)+' 발사!',1000)}
function weaponName(w){return({knife:'투척칼',grenade:'수류탄',pistol:'권총',rifle:'소총'})[w]||w}
function resize(){const r=canvas.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);canvas.width=Math.max(1,Math.round(r.width*d));canvas.height=Math.max(1,Math.round(r.height*d));ctx.setTransform(canvas.width/1000,0,0,canvas.height/600,0,0)}
new ResizeObserver(resize).observe(canvas);
function drawBackground(t){
 const g=ctx.createLinearGradient(0,0,0,600);g.addColorStop(0,'#9dc4df');g.addColorStop(.62,'#d8e1df');g.addColorStop(1,'#ece4d2');ctx.fillStyle=g;ctx.fillRect(0,0,1000,600);
 ctx.globalAlpha=.35;ctx.fillStyle='#fff';for(const [x,y,s] of [[130,95,1],[690,125,.8]]){ctx.beginPath();ctx.ellipse(x,y,64*s,18*s,0,0,Math.PI*2);ctx.ellipse(x+45*s,y-7*s,42*s,22*s,0,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1;
 ctx.fillStyle='#8aa1a9';ctx.beginPath();ctx.moveTo(0,390);for(let x=0;x<=1000;x+=40)ctx.lineTo(x,330+Math.sin(x/90)*35+Math.sin(x/37)*12);ctx.lineTo(1000,600);ctx.lineTo(0,600);ctx.fill();
}
function drawTerrain(s){ctx.beginPath();ctx.moveTo(0,600);s.terrain.forEach((y,i)=>ctx.lineTo(i*s.terrainStep,y));ctx.lineTo(1000,600);ctx.closePath();ctx.fillStyle='#373b35';ctx.fill();ctx.strokeStyle='#111827';ctx.lineWidth=3;ctx.stroke();ctx.save();ctx.clip();ctx.globalAlpha=.12;ctx.strokeStyle='#fff';ctx.lineWidth=1;for(let x=-200;x<1200;x+=28){ctx.beginPath();ctx.moveTo(x,360);ctx.lineTo(x+220,620);ctx.stroke()}ctx.restore();ctx.globalAlpha=1}
function drawStick(p,idx,t,isTurn){
 const x=p.x,y=p.y,bob=Math.sin(t/500+idx)*1.2,face=idx===0?1:-1;ctx.save();ctx.translate(x,y+bob);ctx.strokeStyle=idx===0?'#101216':'#f5f3ec';ctx.fillStyle=ctx.strokeStyle;ctx.lineWidth=5;ctx.lineCap='round';ctx.lineJoin='round';
 if(idx===1){ctx.shadowColor='#111';ctx.shadowBlur=3} if(isTurn){ctx.shadowColor='#ff5a36';ctx.shadowBlur=13}
 ctx.beginPath();ctx.arc(0,-42,11,0,Math.PI*2);ctx.stroke();
 const joints=[[-1,-27],[-10,-8],[8,-8],[-13,14],[13,14],[-16,34],[17,34]];ctx.beginPath();ctx.moveTo(0,-30);ctx.lineTo(-2,3);ctx.moveTo(-2,-21);ctx.lineTo(15*face,-8);ctx.lineTo(25*face,3);ctx.moveTo(-2,-19);ctx.lineTo(-16*face,-4);ctx.lineTo(-22*face,7);ctx.moveTo(-2,3);ctx.lineTo(-14,18);ctx.lineTo(-18,35);ctx.moveTo(-2,3);ctx.lineTo(13,18);ctx.lineTo(18,35);ctx.stroke();
 ctx.shadowBlur=0;joints.forEach(([jx,jy])=>{ctx.beginPath();ctx.arc(jx,jy,3.6,0,Math.PI*2);ctx.fill()});
 ctx.strokeStyle='#ff5a36';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(16*face,-9);const a=(+angle.value)*Math.PI/180;ctx.lineTo(16*face+Math.cos(a)*face*38,-9-Math.sin(a)*38);if(isTurn)ctx.stroke();ctx.restore();
}
function drawHudMarks(s){for(let i=0;i<2;i++){const p=s.players[i];ctx.fillStyle='rgba(17,24,39,.8)';ctx.font='800 11px system-ui';ctx.textAlign='center';ctx.fillText(`${p.hp} HP`,p.x,p.y-68)}}
function render(ts){requestAnimationFrame(render);if(!state)return;drawBackground(ts);drawTerrain(state);drawStick(state.players[0],0,ts,state.turn===0&&!state.resolving);drawStick(state.players[1],1,ts,state.turn===1&&!state.resolving);drawHudMarks(state);
 if(anim){const pts=anim.shot.path,dur=Math.max(450,pts.length*15),elapsed=ts-anim.start,idx=Math.min(pts.length-1,Math.floor(elapsed/dur*pts.length));ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=2;ctx.beginPath();for(let i=0;i<=idx;i++){const p=pts[i];i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])}ctx.stroke();const p=pts[idx];if(p){ctx.fillStyle=anim.shot.weapon==='grenade'?'#ff5a36':'#111827';ctx.beginPath();ctx.arc(p[0],p[1],anim.shot.weapon==='grenade'?7:4,0,Math.PI*2);ctx.fill()}
   if(elapsed>=dur){if(anim.impactAt===null)anim.impactAt=ts;const imp=anim.shot.impact;if(imp.kind!=='out'){const q=Math.min(1,(ts-anim.impactAt)/350);ctx.globalAlpha=1-q;ctx.fillStyle='#ff5a36';ctx.beginPath();ctx.arc(imp.x,imp.y,12+q*(anim.shot.weapon==='grenade'?75:24),0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}if(ts-anim.impactAt>420){const f=anim.finalState;anim=null;applyState(queuedState||f);queuedState=null;}}
 }
}
requestAnimationFrame(render);
