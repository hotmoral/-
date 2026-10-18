(()=>{
"use strict";

const game=document.getElementById("game"),ctx=game.getContext("2d",{alpha:false});
const mini=document.getElementById("mini"),mx=mini.getContext("2d");
const tierEl=document.getElementById("tier"),statEl=document.getElementById("statBody"),deadEl=document.getElementById("dead"),toastEl=document.getElementById("toast"),offlineEl=document.getElementById("offline"),nameEl=document.getElementById("name"),setNameBtn=document.getElementById("setName"),respawnBtn=document.getElementById("respawn");

let W=innerWidth,H=innerHeight,last=performance.now(),start=last,lastHud=0,lastMini=0,fps=60,fpsFrames=0,fpsMark=last;
let id=null,world={w:8400,h:8400},snap={t:0,players:[],mobs:[],items:[],predators:[],snapHz:12};
let swipe={on:false,sx:0,sy:0,x:0,y:0},lastInput={x:999,y:999,t:0},cam={x:4200,y:4200,z:.9},toastTimer=0,bitePulse=0;
const SELF={init:false,x:0,y:0,vx:0,vy:0,alive:true};
const REMOTE_PLAYERS=new Map(),REMOTE_MOBS=new Map(),PENDING_EATS=new Map();
const EAT_FX=[],PARTICLES=[];
const plankton=Array.from({length:52},(_,i)=>({x:(i*997)%8400,y:(i*619+311)%8400,r:1+(i%3)*.55,a:.08+(i%5)*.018}));

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const vr=m=>13+Math.log2(1+Math.max(1,m)/8)*7.2;
const tierOf=m=>Math.max(0,Math.floor(Math.log2(Math.max(1,m)/12)));
const speedBonus=s=>Math.log2(1+Math.max(0,s))*18;
const eatRatio=a=>Math.min(.90,.70+Math.log2(1+Math.max(0,a))*.035);
const stageName=t=>["미세 연못","수초 생태권","암초 수로","심해 분지","고대 해구","거대 생물권"][t]||`초진화 생태권 ${Math.max(1,t-4)}`;

function resize(){W=innerWidth;H=innerHeight;game.width=W;game.height=H;game.style.width=W+"px";game.style.height=H+"px";ctx.setTransform(1,0,0,1,0,0)}
addEventListener("resize",resize,{passive:true});resize();
function ws(x,y){return{x:(x-cam.x)*cam.z+W/2,y:(y-cam.y)*cam.z+H/2}}
function visible(p,r=50){return p.x>-r&&p.x<W+r&&p.y>-r&&p.y<H+r}
function flash(s){clearTimeout(toastTimer);toastEl.textContent=s;toastEl.classList.add("show");toastTimer=setTimeout(()=>toastEl.classList.remove("show"),750)}
function post(url,body,wantJson=false){return fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body),cache:"no-store"}).then(r=>wantJson?r.json():null)}

async function join(){try{const resumeId=localStorage.getItem("microevo_id")||undefined,r=await post("/api/join",{resumeId},true);if(!r||!r.id)throw 0;id=r.id;world=r.world;localStorage.setItem("microevo_id",id);connectEvents()}catch{offlineEl.style.display="block";setTimeout(join,1000)}}
function connectEvents(){const es=new EventSource("/events?id="+encodeURIComponent(id));es.onopen=()=>offlineEl.style.display="none";es.onmessage=e=>{try{const s=JSON.parse(e.data);if(s&&Array.isArray(s.players)){snap=s;offlineEl.style.display="none";ingest(s)}}catch{}};es.onerror=()=>offlineEl.style.display="block"}

function desiredInput(){if(!swipe.on)return{x:0,y:0};const dx=swipe.x-swipe.sx,dy=swipe.y-swipe.sy,l=Math.hypot(dx,dy);return l>8?{x:dx/l,y:dy/l}:{x:0,y:0}}
function sendInput(force=false){if(!id)return;const v=desiredInput(),now=performance.now(),changed=Math.abs(v.x-lastInput.x)+Math.abs(v.y-lastInput.y)>.035;if(!force&&now-lastInput.t<68)return;if(!force&&!changed&&now-lastInput.t<220)return;lastInput={x:v.x,y:v.y,t:now};post("/api/input",{id,x:v.x,y:v.y}).catch(()=>{})}
setInterval(()=>sendInput(false),72);
game.addEventListener("pointerdown",e=>{swipe.on=true;swipe.sx=swipe.x=e.clientX;swipe.sy=swipe.y=e.clientY;try{game.setPointerCapture(e.pointerId)}catch{}sendInput(true)});
game.addEventListener("pointermove",e=>{if(swipe.on){swipe.x=e.clientX;swipe.y=e.clientY;sendInput(false)}});
function endSwipe(){swipe.on=false;sendInput(true)}
game.addEventListener("pointerup",endSwipe);game.addEventListener("pointercancel",endSwipe);
setNameBtn.onclick=()=>{const n=nameEl.value.trim();if(id&&n)post("/api/name",{id,name:n}).catch(()=>{})};
nameEl.addEventListener("keydown",e=>{if(e.key==="Enter")setNameBtn.click()});
respawnBtn.onclick=()=>{if(id)post("/api/respawn",{id}).catch(()=>{})};
function serverMe(){return snap.players.find(p=>p.id===id)||null}

function ingest(s){
  const now=performance.now();
  const ingestMap=(arr,map,skipSelf=false)=>{const seen=new Set();for(const o of arr||[]){if(skipSelf&&o.id===id)continue;if(PENDING_EATS.has(o.id))continue;seen.add(o.id);let v=map.get(o.id);if(!v){v={...o,x:o.x,y:o.y,vx:o.vx||0,vy:o.vy||0,tx:o.x,ty:o.y,tvx:o.vx||0,tvy:o.vy||0,lastSeen:now};map.set(o.id,v)}else{v.tx=o.x;v.ty=o.y;v.tvx=o.vx||0;v.tvy=o.vy||0;v.lastSeen=now;for(const k in o)if(!["x","y","vx","vy"].includes(k))v[k]=o[k]}}for(const [k,v] of map)if(!seen.has(k)&&now-v.lastSeen>450)map.delete(k)};
  ingestMap(s.players,REMOTE_PLAYERS,true);ingestMap(s.mobs,REMOTE_MOBS,false);
}
function stepRemotes(map,dt){for(const v of map.values()){v.x+=v.vx*dt;v.y+=v.vy*dt;const dx=v.tx-v.x,dy=v.ty-v.y,err=Math.hypot(dx,dy);if(err>260){v.x=v.tx;v.y=v.ty}else{const k=1-Math.exp(-4.8*dt);v.x+=dx*k;v.y+=dy*k}const kv=1-Math.exp(-5.2*dt);v.vx+=(v.tvx-v.vx)*kv;v.vy+=(v.tvy-v.vy)*kv}}
function stepSelf(server,dt){
  if(!server)return null;if(!SELF.init||SELF.alive!==server.alive){SELF.init=true;SELF.x=server.x;SELF.y=server.y;SELF.vx=server.vx||0;SELF.vy=server.vy||0;SELF.alive=server.alive}if(!server.alive)return{...server,x:SELF.x,y:SELF.y,vx:0,vy:0};
  const iv=desiredInput(),maxSpeed=Math.max(82,166-tierOf(server.mass)*5)+speedBonus(server.speed),tvx=iv.x*maxSpeed,tvy=iv.y*maxSpeed;SELF.vx+=(tvx-SELF.vx)*Math.min(1,dt*8.5);SELF.vy+=(tvy-SELF.vy)*Math.min(1,dt*8.5);if(Math.abs(iv.x)+Math.abs(iv.y)<.05){SELF.vx*=Math.pow(.12,dt);SELF.vy*=Math.pow(.12,dt)}const r=vr(server.mass);SELF.x=clamp(SELF.x+SELF.vx*dt,r,world.w-r);SELF.y=clamp(SELF.y+SELF.vy*dt,r,world.h-r);
  const dx=server.x-SELF.x,dy=server.y-SELF.y,err=Math.hypot(dx,dy);if(swipe.on){if(err>950){SELF.x+=dx*.035;SELF.y+=dy*.035}}else if(err>520){SELF.x=server.x;SELF.y=server.y;SELF.vx=server.vx||0;SELF.vy=server.vy||0}else if(err>8){const k=1-Math.exp(-.7*dt);SELF.x+=dx*k;SELF.y+=dy*k}
  return{...server,x:SELF.x,y:SELF.y,vx:SELF.vx,vy:SELF.vy};
}

function optimisticEat(me,m){
  if(!id||PENDING_EATS.has(m.id))return;const now=performance.now();PENDING_EATS.set(m.id,now);REMOTE_MOBS.delete(m.id);bitePulse=1;EAT_FX.push({...m,fxStart:now,fxDur:235,fromX:m.x,fromY:m.y});
  const hue=m.kind==="attack"?8:m.kind==="speed"?202:m.kind==="armor"?132:280;for(let i=0;i<7;i++)PARTICLES.push({x:m.x,y:m.y,vx:(Math.random()-.5)*105,vy:(Math.random()-.5)*105,life:.32+Math.random()*.18,max:.5,hue});
  post("/api/eat",{id,mobId:m.id,x:SELF.x,y:SELF.y},true).then(r=>{if(!r||!r.ok){PENDING_EATS.delete(m.id)}else setTimeout(()=>PENDING_EATS.delete(m.id),900)}).catch(()=>PENDING_EATS.delete(m.id));
}
function tryOptimisticEats(me){if(!me||!me.alive)return;const pr=vr(me.mass),ratio=eatRatio(me.attack);for(const m of [...REMOTE_MOBS.values()]){if(m.mass>=me.mass*ratio)continue;const rr=pr+vr(m.mass)*.88+15;if((SELF.x-m.x)**2+(SELF.y-m.y)**2<=rr*rr)optimisticEat(me,m)}}

function bg(me){
  const t=me?tierOf(me.mass):0,P=[["#061a21","#123e47","#76e5d2"],["#08251e","#28503e","#a5ef78"],["#0b223c","#26546c","#79c7ff"],["#11152e","#352a56","#a48fff"],["#180f28","#462148","#ef8dff"],["#0f1c2a","#25434b","#ffdc82"]][t%6],g=ctx.createLinearGradient(0,0,W,H);g.addColorStop(0,P[0]);g.addColorStop(1,P[1]);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  for(const q of plankton){const p=ws(q.x,q.y);if(!visible(p,10))continue;ctx.globalAlpha=q.a;ctx.fillStyle=P[2];ctx.beginPath();ctx.arc(p.x,p.y,q.r,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1;
  const step=Math.max(160,330*cam.z),ox=((0-cam.x)*cam.z+W/2)%step,oy=((0-cam.y)*cam.z+H/2)%step;ctx.globalAlpha=.026;ctx.strokeStyle=P[2];for(let x=ox;x<W;x+=step){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}for(let y=oy;y<H;y+=step){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}ctx.globalAlpha=1;
}

function bodyGradient(x1,y1,x2,y2,c1,c2){const g=ctx.createLinearGradient(x1,y1,x2,y2);g.addColorStop(0,c1);g.addColorStop(.58,c2);g.addColorStop(1,"rgba(2,21,28,.55)");return g}
function drawGrazer(m,p,r,a){
  const palettes=[["#a8ffe0","#41bfa6"],["#ffd69a","#ef8c6b"],["#b9d8ff","#5d86df"],["#ddaaff","#9361cb"],["#b7f58e","#5fae62"]],pal=palettes[(m.species||0)%palettes.length];ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a);ctx.lineJoin="round";
  ctx.globalAlpha=.42;ctx.fillStyle=pal[0];ctx.beginPath();ctx.moveTo(-r*.25,-r*.42);ctx.quadraticCurveTo(-r*.75,-r*1.05,-r*1.12,-r*.62);ctx.quadraticCurveTo(-r*.62,-r*.18,-r*.12,-r*.08);ctx.fill();ctx.beginPath();ctx.moveTo(-r*.25,r*.42);ctx.quadraticCurveTo(-r*.75,r*1.05,-r*1.12,r*.62);ctx.quadraticCurveTo(-r*.62,r*.18,-r*.12,r*.08);ctx.fill();ctx.globalAlpha=1;
  ctx.fillStyle=bodyGradient(-r,-r,r,r,pal[0],pal[1]);ctx.strokeStyle="rgba(228,255,250,.22)";ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(r*.98,0);ctx.bezierCurveTo(r*.48,-r*.70,-r*.65,-r*.74,-r*.98,-r*.18);ctx.lineTo(-r*1.45,-r*.48);ctx.lineTo(-r*1.25,0);ctx.lineTo(-r*1.45,r*.48);ctx.lineTo(-r*.98,r*.18);ctx.bezierCurveTo(-r*.65,r*.74,r*.48,r*.70,r*.98,0);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.globalAlpha=.30;ctx.fillStyle="#fff";ctx.beginPath();ctx.ellipse(r*.15,-r*.22,r*.5,r*.16,-.16,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;ctx.fillStyle="#071f27";ctx.beginPath();ctx.arc(r*.45,-r*.14,Math.max(1.8,r*.075),0,Math.PI*2);ctx.fill();ctx.fillStyle="rgba(255,255,255,.8)";ctx.beginPath();ctx.arc(r*.47,-r*.17,Math.max(.8,r*.027),0,Math.PI*2);ctx.fill();ctx.restore();
}
function drawHunter(m,p,r,a){
  const apex=m.archetype==="apex",danger=m.role==="predator"||m.role==="apex";ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a);ctx.lineJoin="round";
  if(danger){ctx.strokeStyle=apex?"rgba(255,214,92,.58)":"rgba(255,106,98,.46)";ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+7,0,Math.PI*2);ctx.stroke()}
  const c1=apex?"#ffd66c":"#ff8b84",c2=apex?"#946b31":"#8b3e52";ctx.fillStyle=bodyGradient(-r,-r,r,r,c1,c2);ctx.strokeStyle="rgba(255,238,223,.26)";ctx.lineWidth=1.3;
  ctx.beginPath();ctx.moveTo(r*1.06,0);ctx.lineTo(r*.56,-r*.34);ctx.lineTo(r*.18,-r*.82);ctx.lineTo(-r*.05,-r*.46);ctx.lineTo(-r*.72,-r*.62);ctx.lineTo(-r*.55,-r*.22);ctx.lineTo(-r*1.32,-r*.06);ctx.lineTo(-r*.72,r*.20);ctx.lineTo(-r*.20,r*.65);ctx.lineTo(r*.10,r*.42);ctx.lineTo(r*.58,r*.34);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle="rgba(255,244,229,.55)";for(let k=-1;k<=1;k++){ctx.beginPath();ctx.moveTo(r*.54,k*r*.16);ctx.lineTo(r*.92,k*r*.16-r*.08);ctx.lineTo(r*.79,k*r*.16+r*.08);ctx.closePath();ctx.fill()}
  ctx.fillStyle="#101015";ctx.beginPath();ctx.ellipse(r*.76,0,r*.24,r*.19,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#f8fffd";ctx.beginPath();ctx.arc(r*.42,-r*.28,Math.max(2,r*.08),0,Math.PI*2);ctx.fill();ctx.fillStyle=apex?"#ffcf4f":"#ff574f";ctx.beginPath();ctx.arc(r*.44,-r*.28,Math.max(1,r*.038),0,Math.PI*2);ctx.fill();ctx.restore();
}
function drawMob(m){const p=ws(m.x,m.y),r=vr(m.mass)*.88*cam.z;if(!visible(p,r*2+24))return;const a=Math.atan2(m.vy||0,m.vx||1);if(m.archetype==="hunter"||m.archetype==="apex")drawHunter(m,p,r,a);else drawGrazer(m,p,r,a)}

function drawPlayer(p,self){
  if(!p||!p.alive)return;const q=ws(p.x,p.y),r=vr(p.mass)*cam.z;if(!visible(q,r*2+34))return;const a=Math.atan2(p.vy||0,p.vx||1),open=self?Math.sin(Math.min(1,bitePulse)*Math.PI)*.62:0;ctx.save();ctx.translate(q.x,q.y);ctx.rotate(a);ctx.lineJoin="round";
  const hue=p.hue||165,c1=`hsl(${hue},78%,78%)`,c2=`hsl(${hue},58%,47%)`;
  ctx.globalAlpha=.46;ctx.fillStyle=`hsla(${(hue+25)%360},85%,78%,.72)`;ctx.beginPath();ctx.moveTo(-r*.12,-r*.45);ctx.quadraticCurveTo(-r*.60,-r*1.12,-r*.98,-r*.58);ctx.quadraticCurveTo(-r*.58,-r*.18,-r*.04,-r*.06);ctx.fill();ctx.beginPath();ctx.moveTo(-r*.12,r*.45);ctx.quadraticCurveTo(-r*.60,r*1.12,-r*.98,r*.58);ctx.quadraticCurveTo(-r*.58,r*.18,-r*.04,r*.06);ctx.fill();ctx.globalAlpha=1;
  ctx.fillStyle=bodyGradient(-r,-r,r,r,c1,c2);ctx.strokeStyle="rgba(237,255,251,.34)";ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(r*(.98-open*.12),0);ctx.bezierCurveTo(r*.55,-r*.70,-r*.58,-r*.78,-r*.96,-r*.24);ctx.lineTo(-r*1.48,-r*.48);ctx.lineTo(-r*1.28,0);ctx.lineTo(-r*1.48,r*.48);ctx.lineTo(-r*.96,r*.24);ctx.bezierCurveTo(-r*.58,r*.78,r*.55,r*.70,r*(.98-open*.12),0);ctx.closePath();ctx.fill();ctx.stroke();
  if(p.armor>0){ctx.strokeStyle="rgba(224,255,234,.58)";ctx.lineWidth=Math.max(1.1,r*.045);const bands=Math.min(5,1+Math.floor(Math.log2(1+p.armor)));for(let k=0;k<bands;k++){ctx.beginPath();ctx.arc(-r*.16,0,r*(.36+k*.105),-1.02,1.02);ctx.stroke()}}
  if(p.speed>0){ctx.fillStyle="rgba(111,213,255,.72)";ctx.beginPath();ctx.moveTo(-r*.05,-r*.45);ctx.lineTo(-r*.74,-r*.98);ctx.lineTo(r*.15,-r*.61);ctx.closePath();ctx.fill();ctx.beginPath();ctx.moveTo(-r*.05,r*.45);ctx.lineTo(-r*.74,r*.98);ctx.lineTo(r*.15,r*.61);ctx.closePath();ctx.fill()}
  if(p.attack>0){ctx.fillStyle="#ffe1c7";const n=Math.min(12,3+Math.floor(Math.log2(1+p.attack)*2));for(let k=0;k<n;k++){const yy=(k-(n-1)/2)*r*.12;ctx.beginPath();ctx.moveTo(r*.28,yy);ctx.lineTo(r*.78,yy-r*.07);ctx.lineTo(r*.61,yy+r*.07);ctx.closePath();ctx.fill()}}
  if(open>0){ctx.fillStyle="#071018";ctx.beginPath();ctx.moveTo(r*.50,-r*(.10+.25*open));ctx.quadraticCurveTo(r*1.03,0,r*.50,r*(.10+.25*open));ctx.quadraticCurveTo(r*.69,0,r*.50,-r*(.10+.25*open));ctx.fill();ctx.fillStyle="#fff2df";ctx.beginPath();ctx.moveTo(r*.62,-r*.14);ctx.lineTo(r*.82,-r*.02);ctx.lineTo(r*.58,-r*.01);ctx.fill();ctx.beginPath();ctx.moveTo(r*.62,r*.14);ctx.lineTo(r*.82,r*.02);ctx.lineTo(r*.58,r*.01);ctx.fill()}
  ctx.globalAlpha=.28;ctx.fillStyle="#fff";ctx.beginPath();ctx.ellipse(r*.08,-r*.26,r*.48,r*.15,-.12,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;ctx.fillStyle="#061a21";ctx.beginPath();ctx.arc(r*.40,-r*.20,Math.max(2.1,r*.078),0,Math.PI*2);ctx.fill();ctx.fillStyle="#fff";ctx.beginPath();ctx.arc(r*.43,-r*.23,Math.max(.8,r*.028),0,Math.PI*2);ctx.fill();ctx.restore();
  if(self){ctx.strokeStyle="rgba(255,255,255,.58)";ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(q.x,q.y,r+5,0,Math.PI*2);ctx.stroke()}
  ctx.textAlign="center";ctx.font="600 10px system-ui";ctx.fillStyle="#f4fcff";ctx.fillText(p.name,q.x,q.y-r-11);const bw=Math.max(36,r*1.5);ctx.fillStyle="rgba(0,0,0,.28)";ctx.fillRect(q.x-bw/2,q.y-r-7,bw,3.5);ctx.fillStyle=p.hp/p.maxHp>.35?"#9effb9":"#ff8989";ctx.fillRect(q.x-bw/2,q.y-r-7,bw*clamp(p.hp/p.maxHp,0,1),3.5);
}

function drawItem(it){const p=ws(it.x,it.y),r=10*cam.z;if(!visible(p,28))return;const tt=(performance.now()-start)/1000,pulse=1+Math.sin(tt*4+it.x*.01)*.07,color=it.kind==="attack"?"#ff756e":it.kind==="speed"?"#72c8ff":it.kind==="armor"?"#78e59a":it.kind==="heal"?"#ffd96d":"#dca0ff";ctx.save();ctx.translate(p.x,p.y);ctx.scale(pulse,pulse);ctx.globalAlpha=.18;ctx.fillStyle=color;ctx.beginPath();ctx.arc(0,0,r*1.7,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;ctx.fillStyle=color;ctx.beginPath();for(let k=0;k<8;k++){const a=k*Math.PI/4,rr=k%2?r*.48:r,x=Math.cos(a)*rr,y=Math.sin(a)*rr;k?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();ctx.restore()}

function drawEatFx(now){for(let i=EAT_FX.length-1;i>=0;i--){const f=EAT_FX[i],t=clamp((now-f.fxStart)/f.fxDur,0,1),ease=1-Math.pow(1-t,3),x=f.fromX+(SELF.x-f.fromX)*ease,y=f.fromY+(SELF.y-f.fromY)*ease,p=ws(x,y),r=vr(f.mass)*.88*cam.z*(1-t*.82);ctx.save();ctx.globalAlpha=1-t*.55;ctx.translate(p.x,p.y);ctx.rotate(t*4);ctx.fillStyle=f.kind==="attack"?"#ff8d80":f.kind==="speed"?"#88d5ff":"#93e6a2";ctx.beginPath();ctx.ellipse(0,0,r,r*.65,0,0,Math.PI*2);ctx.fill();ctx.restore();if(t>=1)EAT_FX.splice(i,1)}}
function stepParticles(dt){for(let i=PARTICLES.length-1;i>=0;i--){const p=PARTICLES[i];p.life-=dt;if(p.life<=0){PARTICLES.splice(i,1);continue}p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=Math.pow(.16,dt);p.vy*=Math.pow(.16,dt);const q=ws(p.x,p.y);ctx.globalAlpha=clamp(p.life/p.max,0,1);ctx.fillStyle=`hsl(${p.hue},85%,72%)`;ctx.beginPath();ctx.arc(q.x,q.y,2.2,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}

function drawSwipe(){if(!swipe.on)return;const dx=swipe.x-swipe.sx,dy=swipe.y-swipe.sy,l=Math.hypot(dx,dy);ctx.strokeStyle="rgba(235,255,250,.20)";ctx.lineWidth=6;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(swipe.sx,swipe.sy);ctx.lineTo(swipe.x,swipe.y);ctx.stroke();if(l>8){const a=Math.atan2(dy,dx);ctx.save();ctx.translate(swipe.x,swipe.y);ctx.rotate(a);ctx.fillStyle="#effffb";ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-13,-6);ctx.lineTo(-13,6);ctx.fill();ctx.restore()}}
function drawMini(me){const cw=mini.width,ch=mini.height;mx.clearRect(0,0,cw,ch);const g=mx.createLinearGradient(0,0,cw,ch);g.addColorStop(0,"#09252f");g.addColorStop(1,"#0c3540");mx.fillStyle=g;mx.fillRect(0,0,cw,ch);for(const p of snap.players||[]){if(!p.alive)continue;const x=p.x/world.w*cw,y=p.y/world.h*ch;if(p.id===id){mx.fillStyle="#fff";mx.beginPath();mx.arc(x,y,5,0,Math.PI*2);mx.fill();mx.strokeStyle="#6fffd3";mx.lineWidth=2;mx.beginPath();mx.arc(x,y,8,0,Math.PI*2);mx.stroke()}else{mx.fillStyle=`hsl(${p.hue},75%,62%)`;mx.beginPath();mx.arc(x,y,3.5,0,Math.PI*2);mx.fill()}}for(const m of snap.predators||[]){const x=m.x/world.w*cw,y=m.y/world.h*ch;mx.fillStyle=m.role==="apex"?"#ffd86d":"#ff746c";mx.beginPath();mx.moveTo(x,y-5);mx.lineTo(x+5,y);mx.lineTo(x,y+5);mx.lineTo(x-5,y);mx.closePath();mx.fill()}if(me){const vw=(W/cam.z)/world.w*cw,vh=(H/cam.z)/world.h*ch,x=me.x/world.w*cw-vw/2,y=me.y/world.h*ch-vh/2;mx.strokeStyle="rgba(255,255,255,.34)";mx.strokeRect(x,y,vw,vh)}}
function updateHud(server,me){const p=server||me;if(!p){tierEl.textContent="공용 월드 연결 중";statEl.textContent="서버 연결 중…";return}const t=tierOf(p.mass),online=(snap.players||[]).filter(x=>x.alive).length,nearThreats=[...REMOTE_MOBS.values()].filter(m=>m.role==="predator"||m.role==="apex").length;tierEl.textContent=`${stageName(t)} · 진화 ${t}`;statEl.innerHTML=`온라인 <b>${online}</b>명 · 질량 <b>${Math.floor(p.mass)}</b><br>공격 <b>${p.attack}</b> · 속도 <b>${p.speed}</b> · 방어 <b>${p.armor}</b> · 위협 <b>${nearThreats}</b><br>FPS <b>${fps}</b> · 동기화 <b>${snap.snapHz||12}Hz</b>`;if(p.alive!==SELF.alive){SELF.alive=p.alive;if(!p.alive)deadEl.classList.add("show");else{deadEl.classList.remove("show");flash("같은 공용 월드에 복귀했습니다")}}}

function frame(now){
  const dt=Math.min(.033,(now-last)/1000||.016);last=now;stepRemotes(REMOTE_PLAYERS,dt);stepRemotes(REMOTE_MOBS,dt);const sm=serverMe(),me=stepSelf(sm,dt);if(me){cam.x=me.x;cam.y=me.y;const z=clamp(.98-Math.log2(1+me.mass/20)*.065,.42,.92);cam.z+=(z-cam.z)*(1-Math.exp(-4*dt));tryOptimisticEats(me)}bitePulse=Math.max(0,bitePulse-dt*4.2);
  bg(me);for(const it of snap.items||[])drawItem(it);for(const m of REMOTE_MOBS.values())drawMob(m);for(const p of REMOTE_PLAYERS.values())drawPlayer(p,false);drawEatFx(now);if(me)drawPlayer(me,true);stepParticles(dt);drawSwipe();if(now-lastMini>125){drawMini(me);lastMini=now}if(now-lastHud>250){updateHud(sm,me);lastHud=now}
  for(const [mid,t] of PENDING_EATS)if(now-t>1600)PENDING_EATS.delete(mid);fpsFrames++;if(now-fpsMark>=1000){fps=Math.round(fpsFrames*1000/(now-fpsMark));fpsFrames=0;fpsMark=now}requestAnimationFrame(frame)
}

join();requestAnimationFrame(frame);
})();
