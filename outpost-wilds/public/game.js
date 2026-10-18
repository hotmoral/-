const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
let DPR=Math.min(2,devicePixelRatio||1),W=innerWidth,H=innerHeight;
function resize(){W=innerWidth;H=innerHeight;canvas.width=W*DPR;canvas.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0)}
resize();addEventListener('resize',resize);

const $=id=>document.getElementById(id);
const assets={};
for(const name of ['tree','rock','berry','wolf','boar','brute']){const im=new Image();im.src=`/assets/${name}.svg`;assets[name]=im}
let meId=null,snap=null,cam={x:1800,y:1800},input={x:0,y:0};
let particles=[],floaters=[],tracers=[],shake=0,nightFlash=0,hurtFlash=0;
const attackFx=new Map(),movePhase=new Map();
const toastEl=$('toast');let toastTimer,fullToastAt=0;
function toast(s,cls=''){toastEl.textContent=s;toastEl.className='show '+cls;clearTimeout(toastTimer);toastTimer=setTimeout(()=>toastEl.className='',1800)}
const protocol=location.protocol==='https:'?'wss':'ws';const ws=new WebSocket(`${protocol}://${location.host}`);
ws.onopen=()=>{$('online').textContent='공동 월드 연결됨'};
ws.onclose=()=>{$('online').textContent='연결 끊김 · 새로고침 필요'};
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.type==='welcome')meId=m.id;if(m.type==='snapshot'){snap=m;updateHud()}if(m.type==='event')eventFx(m)};
function send(m){if(ws.readyState===1)ws.send(JSON.stringify(m))}
function myPlayer(){return snap?.players.find(p=>p.id===meId)}
function updateHud(){
  const p=myPlayer();if(!p)return;
  $('wood').textContent=p.wood;$('stone').textContent=p.stone;$('meat').textContent=p.meat;
  $('baseLv').textContent=`LV.${snap.base.level}`;$('weapon').textContent=p.weapon;
  $('baseHp').style.width=`${100*snap.base.hp/snap.base.maxHp}%`;
  $('online').textContent=`공동 월드 · ${snap.players.length}명 접속`;
  const labels={day:['낮','☀ 탐험 · 채집'],dusk:['해질녘','거점으로 복귀'],night:['밤','⚠ 습격 방어'],dawn:['새벽','곧 안전해짐']};
  const l=labels[snap.day.phase];$('phaseLabel').textContent=l[0];$('clockLabel').textContent=l[1];
  $('carryLabel').textContent=`${p.carry} / ${p.carryCap}`;$('carryFill').style.width=`${100*p.carry/p.carryCap}%`;
  const up=snap.base.upgrade;
  if(up?.complete){$('missionTitle').textContent='최종 거점 완성 · 밤을 버티세요';$('missionCost').innerHTML='최종 단계';$('missionFill').style.width='100%'}
  else if(up?.cost){
    $('missionTitle').textContent=`거점 LV.${snap.base.level+1} 건설`;
    const c=up.cost,b=snap.base;
    $('missionCost').innerHTML=`<i class="${b.wood>=c.wood?'done':''}">목재 ${b.wood}/${c.wood}</i><i class="${b.stone>=c.stone?'done':''}">돌 ${b.stone}/${c.stone}</i><i class="${b.meat>=c.meat?'done':''}">식량 ${b.meat}/${c.meat}</i>`;
    $('missionFill').style.width=`${up.ratio*100}%`;
  }
  const hint=$('contextHint');
  const nearBase=Math.hypot(p.x-snap.base.x,p.y-snap.base.y)<snap.base.r+130;
  if(nearBase&&p.carry>0){hint.textContent='거점에 접근하면 자원이 자동 반납됩니다';hint.className='show'}
  else if(p.carry>=p.carryCap*.9){hint.textContent='짐이 가득 찼습니다 · 거점으로 돌아가세요';hint.className='show'}else hint.className='';
}
function addFloater(text,x,y,color='#f3e6c9',size=13){floaters.push({text,x,y,life:1.05,color,size})}
function burst(x,y,color,count=8,speed=145){for(let i=0;i<count;i++){const a=Math.random()*Math.PI*2,v=Math.random()*speed;particles.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-20,life:.45+Math.random()*.2,size:2+Math.random()*3,color})}}
function eventFx(m){
  if(m.kind==='swing'){attackFx.set(m.playerId,{t:.34,dir:m.dir,tier:m.tier})}
  if(m.kind==='impact'){burst(m.x,m.y,m.target==='tree'?'#b9d58b':m.target==='rock'?'#d8d8cb':'#ba6b63',7);shake=Math.max(shake,2.5)}
  if(m.kind==='slash'){burst(m.x,m.y,'#f3c79c',8,190);addFloater(`-${m.damage}`,m.x,m.y-18,'#ffd0a7',12);shake=Math.max(shake,4)}
  if(m.kind==='gather'&&m.playerId===meId){const label=m.resource==='wood'?'목재':m.resource==='stone'?'돌':'식량';if(m.amount>0){toast(`+${m.amount} ${label} 획득`);addFloater(`+${m.amount} ${label}`,m.x,m.y-20,'#f4d494',13)}}
  if(m.kind==='kill'&&m.playerId===meId){const n=m.enemyType==='boar'?'멧돼지':m.enemyType==='brute'?'야수':'늑대';toast(`${n} 사냥 성공 · 식량 +${m.amount}`);addFloater(`사냥 성공 +${m.amount}`,m.x,m.y-22,'#ffca8b',14)}
  if(m.kind==='raid'){toast(`밤 습격! ${m.count}마리가 거점으로 몰려옵니다`,'phaseDanger');nightFlash=1;shake=8}
  if(m.kind==='upgrade'){toast(`공동 거점 LV.${m.level} 완성 · ${m.weapon} 해금`,'phaseAlert');nightFlash=.7;shake=7}
  if(m.kind==='down'&&m.playerId===meId){toast('쓰러졌습니다 · 거점에서 재정비','phaseDanger');hurtFlash=1}
  if(m.kind==='hurt'&&m.playerId===meId){hurtFlash=Math.min(1,hurtFlash+.35);shake=Math.max(shake,4)}
  if(m.kind==='baseHit'){shake=Math.max(shake,5);burst(m.x||snap.base.x,m.y||snap.base.y,'#d86151',5,100)}
  if(m.kind==='baseBreach'){toast('방벽이 돌파됐습니다! 거점을 지키세요','phaseDanger');nightFlash=1;shake=12}
  if(m.kind==='deposit'&&m.playerId===meId){toast(`공동 창고 반납 · 목재 ${m.wood} / 돌 ${m.stone} / 식량 ${m.meat}`);burst(snap.base.x,snap.base.y,'#efc96f',15,200)}
  if(m.kind==='carryFull'&&m.playerId===meId&&performance.now()-fullToastAt>1500){fullToastAt=performance.now();toast('짐이 가득 찼습니다 · 거점으로 복귀하세요','phaseAlert')}
  if(m.kind==='towerShot')tracers.push({x1:m.x1,y1:m.y1,x2:m.x2,y2:m.y2,life:.17});
}
function worldToScreen(x,y){return{x:x-cam.x+W/2,y:y-cam.y+H/2}}
function circle(x,y,r,fill,stroke,lw=1){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.lineWidth=lw;ctx.strokeStyle=stroke;ctx.stroke()}}
function shadow(x,y,rx,ry,a=.25){ctx.save();ctx.globalAlpha=a;ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill();ctx.restore()}
function hash2(x,y){const s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)}
function groundColorAt(x,y){const d=Math.hypot(x-1800,y-1800);if(d>1250)return '#1a241d';if(x<800||y>2850)return '#202a20';if(x>2700)return '#242b24';return '#1d3022'}
function drawGround(){
  ctx.fillStyle=groundColorAt(cam.x,cam.y);ctx.fillRect(0,0,W,H);
  const tile=90,x0=Math.floor((cam.x-W/2)/tile)*tile,y0=Math.floor((cam.y-H/2)/tile)*tile;
  for(let x=x0;x<cam.x+W/2+tile;x+=tile)for(let y=y0;y<cam.y+H/2+tile;y+=tile){
    const s=worldToScreen(x,y),h=hash2(x/tile,y/tile);ctx.globalAlpha=.14;
    ctx.fillStyle=h>.68?'#75805c':h>.35?'#416b46':'#284b34';
    ctx.save();ctx.translate(s.x+(h-.5)*45,s.y+(hash2(y/tile,x/tile)-.5)*45);ctx.rotate(h*6);ctx.fillRect(-1,-4,2,8);ctx.fillRect(-4,-1,8,2);ctx.restore();ctx.globalAlpha=1;
  }
  if(snap){const s=worldToScreen(snap.base.x,snap.base.y);const g=ctx.createRadialGradient(s.x,s.y,15,s.x,s.y,360);g.addColorStop(0,'rgba(174,132,71,.10)');g.addColorStop(1,'rgba(174,132,71,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(s.x,s.y,360,0,Math.PI*2);ctx.fill()}
}
function drawAsset(name,x,y,w,h,flip=false,rot=0){const im=assets[name];if(!im?.complete)return;ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(flip?-1:1,1);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore()}
function drawNode(n){const s=worldToScreen(n.x,n.y);if(n.type==='tree')drawAsset('tree',s.x,s.y-35,112,136);else if(n.type==='rock')drawAsset('rock',s.x,s.y-5,88,74);else drawAsset('berry',s.x,s.y,82,67);if(n.hp<n.maxHp)drawHealth(s.x,s.y-(n.type==='tree'?93:55),n.hp/n.maxHp,38)}
function drawBase(b){
  const s=worldToScreen(b.x,b.y),r=b.r;
  ctx.save();ctx.translate(s.x,s.y);
  const aura=ctx.createRadialGradient(0,0,25,0,0,r);aura.addColorStop(0,'rgba(235,190,103,.10)');aura.addColorStop(1,'rgba(235,190,103,.015)');circle(0,0,r,aura,'#d8ba7a2a',2);
  ctx.setLineDash([8,10]);circle(0,0,r,null,'#e1c58a35',1.5);ctx.setLineDash([]);
  shadow(0,50,142,44,.34);
  const posts=20+(b.level>=3?4:0),wallR=164+(b.level>=4?12:0);
  for(let i=0;i<posts;i++){
    const a=i/posts*Math.PI*2;if(Math.abs(Math.atan2(Math.sin(a),Math.cos(a)))<.23)continue;
    const x=Math.cos(a)*wallR,y=Math.sin(a)*wallR*.72;
    ctx.save();ctx.translate(x,y);ctx.rotate(a+Math.PI/2);ctx.fillStyle=b.level>=4?'#73756f':b.level>=2?'#80684c':'#6a4b34';ctx.fillRect(-6,-19,12,38);ctx.fillStyle='#b49767';ctx.beginPath();ctx.moveTo(-6,-19);ctx.lineTo(0,-28);ctx.lineTo(6,-19);ctx.fill();ctx.restore();
  }
  ctx.fillStyle=b.level>=4?'#676963':'#77583e';ctx.fillRect(-70,-35,140,88);ctx.fillStyle='#423226';ctx.beginPath();ctx.moveTo(-91,-31);ctx.lineTo(0,-108);ctx.lineTo(91,-31);ctx.closePath();ctx.fill();ctx.strokeStyle='#9a764e';ctx.lineWidth=4;ctx.stroke();
  ctx.fillStyle='#35261e';ctx.fillRect(-14,12,28,41);circle(0,0,22,'#d98645');circle(0,0,10,'#ffd374');
  if(b.level>=2){drawTent(-112,55,.78);drawTent(105,62,.72);ctx.fillStyle='#5c4937';ctx.fillRect(-124,-72,46,32);ctx.fillStyle='#c0a170';ctx.fillRect(-117,-65,31,6)}
  if(b.level>=3){for(const [x,y] of [[-124,-105],[126,-99],[-132,104],[133,105]])drawTower(x,y)}
  if(b.level>=4){ctx.fillStyle='#666d69';ctx.fillRect(79,-18,44,64);ctx.fillStyle='#9f8d72';ctx.fillRect(86,-10,30,8);ctx.fillRect(86,8,30,8)}
  if(b.level>=5){ctx.strokeStyle='#d8b862';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,120,0,Math.PI*2);ctx.stroke();circle(0,-131,9,'#f2c96d')}
  ctx.restore();
}
function drawTent(x,y,k){ctx.save();ctx.translate(x,y);ctx.scale(k,k);ctx.fillStyle='#8a6d46';ctx.beginPath();ctx.moveTo(-34,20);ctx.lineTo(0,-25);ctx.lineTo(34,20);ctx.closePath();ctx.fill();ctx.strokeStyle='#4a3829';ctx.lineWidth=3;ctx.stroke();ctx.restore()}
function drawTower(x,y){ctx.save();ctx.translate(x,y);ctx.fillStyle='#695039';ctx.fillRect(-12,-19,24,48);ctx.fillStyle='#3c3025';ctx.fillRect(-24,-29,48,17);ctx.strokeStyle='#ad895a';ctx.lineWidth=3;ctx.strokeRect(-24,-29,48,17);ctx.restore()}
function drawHealth(x,y,q,w){ctx.fillStyle='#0009';ctx.fillRect(x-w/2,y,w,5);ctx.fillStyle=q>.55?'#7bc57a':q>.27?'#ddb35e':'#d46759';ctx.fillRect(x-w/2,y,w*Math.max(0,q),5)}
function drawCargo(p,s){
  if(!p.carry)return;const q=Math.min(1,p.carry/p.carryCap),n=Math.ceil(q*5);ctx.save();ctx.translate(s.x-11,s.y+4);for(let i=0;i<n;i++){const yy=10-i*5;ctx.fillStyle=i%3===0?'#ba814d':i%3===1?'#8f9692':'#a94e45';ctx.fillRect(-13,yy,22,5)}ctx.restore()
}
function drawPlayer(p,isMe,t){
  const s=worldToScreen(p.x,p.y),phase=movePhase.get(p.id)||0;let bob=Math.sin(phase)*2;
  const moving=p.id===meId?Math.hypot(input.x,input.y)>.05:true;
  if(!moving)bob*=.25;
  shadow(s.x,s.y+22,19,7,.32);drawCargo(p,s);
  ctx.save();ctx.translate(s.x,s.y+bob);ctx.rotate(p.dir||0);
  const swing=attackFx.get(p.id);let sw=0;if(swing){sw=(.34-swing.t)/.34;sw=Math.sin(sw*Math.PI)*1.15}
  const leg=Math.sin(phase)*7;
  ctx.strokeStyle='#332b27';ctx.lineWidth=6;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-3,8);ctx.lineTo(-9,18+leg*.35);ctx.moveTo(4,8);ctx.lineTo(10,18-leg*.35);ctx.stroke();
  ctx.fillStyle=isMe?'#426f62':`hsl(${(p.id.charCodeAt(0)*47)%360} 35% 48%)`;ctx.beginPath();ctx.ellipse(0,0,13,17,0,0,Math.PI*2);ctx.fill();
  circle(5,-15,9,'#d8af84');ctx.fillStyle='#4d3829';ctx.beginPath();ctx.arc(4,-18,9,Math.PI,Math.PI*2);ctx.fill();
  ctx.save();ctx.rotate(-.18-sw);ctx.strokeStyle='#d2ad80';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(6,-2);ctx.lineTo(21,-4);ctx.stroke();ctx.strokeStyle=p.tier>=3?'#b0a98f':'#9b764b';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(17,-5);ctx.lineTo(40,-7);ctx.stroke();ctx.fillStyle=p.tier>=3?'#d6d9d2':'#c7b486';ctx.beginPath();ctx.moveTo(38,-12);ctx.lineTo(53,-7);ctx.lineTo(38,-2);ctx.closePath();ctx.fill();ctx.restore();
  ctx.restore();
  if(isMe){circle(s.x,s.y+1,25,null,'#fff8',1.5);circle(s.x,s.y+1,30,null,'#9bd8c033',1)}
  ctx.font='600 10px sans-serif';ctx.textAlign='center';ctx.fillStyle='#fff';ctx.shadowColor='#000';ctx.shadowBlur=4;ctx.fillText(p.name,s.x,s.y-35);ctx.shadowBlur=0;drawHealth(s.x,s.y-29,p.hp/p.maxHp,38)
}
function drawEnemy(e,t){
  const s=worldToScreen(e.x,e.y),movingBob=Math.sin(t*.006+e.id)*1.3;shadow(s.x,s.y+18,e.r*1.25,7,.32);
  const name=e.type==='boar'?'boar':e.type==='brute'?'brute':'wolf';const flip=Math.cos(e.dir||0)<0;
  drawAsset(name,s.x,s.y-3+movingBob,e.type==='brute'?100:e.type==='boar'?96:92,e.type==='brute'?76:e.type==='boar'?64:61,flip,0);
  drawHealth(s.x,s.y-e.r-20,e.hp/e.maxHp,42);
  if(e.raid){ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#f38b78';ctx.fillText('습격',s.x,s.y-e.r-28)}
}
function drawParticles(dt){
  for(let i=particles.length-1;i>=0;i--){const p=particles[i];p.life-=dt;if(p.life<=0){particles.splice(i,1);continue}p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=.92;p.vy=p.vy*.94+70*dt;const s=worldToScreen(p.x,p.y);ctx.globalAlpha=Math.min(1,p.life/.25);circle(s.x,s.y,p.size,p.color);ctx.globalAlpha=1}
  for(let i=floaters.length-1;i>=0;i--){const f=floaters[i];f.life-=dt;if(f.life<=0){floaters.splice(i,1);continue}f.y-=22*dt;const s=worldToScreen(f.x,f.y);ctx.globalAlpha=Math.min(1,f.life/.35);ctx.font=`700 ${f.size}px sans-serif`;ctx.textAlign='center';ctx.fillStyle=f.color;ctx.shadowColor='#000';ctx.shadowBlur=5;ctx.fillText(f.text,s.x,s.y);ctx.shadowBlur=0;ctx.globalAlpha=1}
  for(let i=tracers.length-1;i>=0;i--){const tr=tracers[i];tr.life-=dt;if(tr.life<=0){tracers.splice(i,1);continue}const a=worldToScreen(tr.x1,tr.y1),b=worldToScreen(tr.x2,tr.y2);ctx.strokeStyle=`rgba(255,207,105,${tr.life/.17})`;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();circle(b.x,b.y,5,'#ffd36b')}
}
function drawMinimap(){
  const mw=126,mh=126,x=W-mw-15,y=H<600?130:108;ctx.save();ctx.globalAlpha=.94;ctx.fillStyle='#09100ccc';ctx.fillRect(x,y,mw,mh);ctx.strokeStyle='#ffffff20';ctx.strokeRect(x,y,mw,mh);const sc=mw/3600;circle(x+snap.base.x*sc,y+snap.base.y*sc,5,'#e3ad59');for(const e of snap.enemies)if(e.raid)circle(x+e.x*sc,y+e.y*sc,1.5,'#e66a5d');for(const p of snap.players)circle(x+p.x*sc,y+p.y*sc,p.id===meId?3.5:2.5,p.id===meId?'#fff':'#7ecad6');ctx.restore()
}
function drawCompass(){const p=myPlayer();if(!p)return;const dx=snap.base.x-p.x,dy=snap.base.y-p.y,d=Math.hypot(dx,dy);if(d<430)return;const a=Math.atan2(dy,dx),cx=W/2+Math.cos(a)*Math.min(W,H)*.32,cy=H/2+Math.sin(a)*Math.min(W,H)*.26;ctx.save();ctx.translate(cx,cy);ctx.rotate(a);ctx.fillStyle='#e7c27c';ctx.beginPath();ctx.moveTo(12,0);ctx.lineTo(-7,-6);ctx.lineTo(-7,6);ctx.closePath();ctx.fill();ctx.restore();ctx.font='9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#e8d6b5bb';ctx.fillText(`거점 ${Math.round(d/10)}m`,cx,cy+18)}
function lighting(){
  if(!snap)return;const phase=snap.day.phase;let a=phase==='night'?.54:phase==='dusk'?.22:phase==='dawn'?.13:0;
  if(a){ctx.fillStyle=`rgba(8,14,25,${a})`;ctx.fillRect(0,0,W,H);const p=myPlayer();if(p&&phase==='night'){const s=worldToScreen(p.x,p.y),g=ctx.createRadialGradient(s.x,s.y,35,s.x,s.y,175);g.addColorStop(0,'rgba(255,205,113,.14)');g.addColorStop(1,'rgba(255,205,113,0)');ctx.globalCompositeOperation='screen';ctx.fillStyle=g;ctx.beginPath();ctx.arc(s.x,s.y,175,0,Math.PI*2);ctx.fill();ctx.globalCompositeOperation='source-over'}}
  if(nightFlash>0){ctx.fillStyle=`rgba(188,57,42,${nightFlash*.12})`;ctx.fillRect(0,0,W,H);nightFlash*=.91}
  if(hurtFlash>0){ctx.fillStyle=`rgba(205,43,36,${hurtFlash*.16})`;ctx.fillRect(0,0,W,H);hurtFlash*=.88}
}
let prevT=performance.now();
function frame(t){
  const dt=Math.min(.04,(t-prevT)/1000);prevT=t;
  for(const p of snap?.players||[]){const old=movePhase.get(p.id)||0;movePhase.set(p.id,old+dt*9)}
  for(const [id,a] of attackFx){a.t-=dt;if(a.t<=0)attackFx.delete(id)}
  ctx.save();if(shake>0){ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);shake*=.84}
  drawGround();
  if(snap){
    const p=myPlayer();if(p){cam.x+=(p.x-cam.x)*Math.min(1,dt*8);cam.y+=(p.y-cam.y)*Math.min(1,dt*8)}
    const drawables=[];
    drawables.push({y:snap.base.y,kind:'base',v:snap.base});
    for(const n of snap.nodes)if(Math.abs(n.x-cam.x)<W/2+120&&Math.abs(n.y-cam.y)<H/2+140)drawables.push({y:n.y,kind:'node',v:n});
    for(const e of snap.enemies)if(Math.abs(e.x-cam.x)<W/2+150&&Math.abs(e.y-cam.y)<H/2+150)drawables.push({y:e.y,kind:'enemy',v:e});
    for(const p2 of snap.players)drawables.push({y:p2.y,kind:'player',v:p2});
    drawables.sort((a,b)=>a.y-b.y);
    for(const d of drawables){if(d.kind==='base')drawBase(d.v);else if(d.kind==='node')drawNode(d.v);else if(d.kind==='enemy')drawEnemy(d.v,t);else drawPlayer(d.v,d.v.id===meId,t)}
    drawParticles(dt);drawCompass();drawMinimap();lighting();
  }
  ctx.restore();requestAnimationFrame(frame)
}
requestAnimationFrame(frame);

const keys={};
addEventListener('keydown',e=>{keys[e.code]=true;if(e.code==='Space'){e.preventDefault();send({type:'attack'})}if(e.code==='KeyE')send({type:'deposit'})});
addEventListener('keyup',e=>keys[e.code]=false);
setInterval(()=>{let x=(keys.KeyD?1:0)-(keys.KeyA?1:0),y=(keys.KeyS?1:0)-(keys.KeyW?1:0);if(Math.hypot(x,y)){const l=Math.hypot(x,y);x/=l;y/=l;if(!joyActive){input.x=x;input.y=y}}else if(!joyActive){input.x=0;input.y=0}send({type:'input',x:input.x,y:input.y})},50);
const joy=$('joystick'),stick=joy.querySelector('.stick');let joyId=null,joyActive=false;
function joyMove(e){const r=joy.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,dx=e.clientX-cx,dy=e.clientY-cy,l=Math.hypot(dx,dy),m=Math.min(43,l),nx=l?dx/l:0,ny=l?dy/l:0;stick.style.transform=`translate(${nx*m}px,${ny*m}px)`;input.x=nx*(m/43);input.y=ny*(m/43)}
joy.addEventListener('pointerdown',e=>{joyId=e.pointerId;joyActive=true;joy.setPointerCapture(e.pointerId);joyMove(e)});
joy.addEventListener('pointermove',e=>{if(e.pointerId===joyId)joyMove(e)});
function joyEnd(e){if(e.pointerId!==joyId)return;joyId=null;joyActive=false;input.x=input.y=0;stick.style.transform=''}
joy.addEventListener('pointerup',joyEnd);joy.addEventListener('pointercancel',joyEnd);
$('attack').addEventListener('pointerdown',e=>{e.preventDefault();send({type:'attack'})});
$('deposit').addEventListener('pointerdown',e=>{e.preventDefault();send({type:'deposit'})});
