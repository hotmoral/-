(()=>{
"use strict";

const game=document.getElementById("game");
const ctx=game.getContext("2d",{alpha:false});
const mini=document.getElementById("mini");
const mx=mini.getContext("2d");
const tierEl=document.getElementById("tier");
const statEl=document.getElementById("statBody");
const deadEl=document.getElementById("dead");
const toastEl=document.getElementById("toast");
const offlineEl=document.getElementById("offline");
const nameEl=document.getElementById("name");
const setNameBtn=document.getElementById("setName");
const respawnBtn=document.getElementById("respawn");

let W=innerWidth,H=innerHeight,DPR=1;
let id=null,world={w:8400,h:8400},snap={t:0,players:[],mobs:[],items:[],predators:[],snapHz:8};
let connected=false;
let last=performance.now(),start=last,lastHud=0,lastMini=0,lastSnapAt=0;
let fps=60,fpsFrames=0,fpsMark=last;
let lastInput={x:999,y:999,t:0};
let swipe={on:false,sx:0,sy:0,x:0,y:0};
let cam={x:4200,y:4200,z:.9};
let toastTimer=0;

const SELF={init:false,x:0,y:0,vx:0,vy:0,alive:true};
const REMOTE_PLAYERS=new Map();
const REMOTE_MOBS=new Map();

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const vr=m=>13+Math.log2(1+Math.max(1,m)/8)*7.2;
const tierOf=m=>Math.max(0,Math.floor(Math.log2(Math.max(1,m)/12)));
const speedBonus=s=>Math.log2(1+Math.max(0,s))*18;
const stageName=t=>["미세 연못","수초 생태권","암초 수로","심해 분지","고대 해구","거대 생물권"][t]||`초진화 생태권 ${Math.max(1,t-4)}`;

function resize(){
  W=innerWidth;H=innerHeight;DPR=1;
  game.width=Math.round(W*DPR);game.height=Math.round(H*DPR);
  game.style.width=W+"px";game.style.height=H+"px";
  ctx.setTransform(DPR,0,0,DPR,0,0);
}
addEventListener("resize",resize,{passive:true});resize();

function post(url,body,wantJson=false){
  return fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body),cache:"no-store"})
    .then(r=>wantJson?r.json():null);
}
async function join(){
  try{
    const resumeId=localStorage.getItem("microevo_id")||undefined;
    const r=await post("/api/join",{resumeId},true);
    if(!r||!r.id)throw new Error("join");
    id=r.id;world=r.world;localStorage.setItem("microevo_id",id);
    connectEvents();
  }catch{
    offlineEl.style.display="block";
    setTimeout(join,1200);
  }
}
function connectEvents(){
  if(!id)return;
  const es=new EventSource("/events?id="+encodeURIComponent(id));
  es.onopen=()=>{connected=true;offlineEl.style.display="none"};
  es.onmessage=e=>{
    try{
      const s=JSON.parse(e.data);
      if(s&&Array.isArray(s.players)){
        snap=s;lastSnapAt=performance.now();connected=true;offlineEl.style.display="none";
        ingest(s);
      }
    }catch{}
  };
  es.onerror=()=>{connected=false;offlineEl.style.display="block"};
}

function desiredInput(){
  if(!swipe.on)return{x:0,y:0};
  const dx=swipe.x-swipe.sx,dy=swipe.y-swipe.sy,l=Math.hypot(dx,dy);
  return l>8?{x:dx/l,y:dy/l}:{x:0,y:0};
}
function sendInput(force=false){
  if(!id)return;
  const v=desiredInput(),now=performance.now();
  const changed=Math.abs(v.x-lastInput.x)+Math.abs(v.y-lastInput.y)>.04;
  if(!force&&now-lastInput.t<85)return;
  if(!force&&!changed&&now-lastInput.t<300)return;
  lastInput={x:v.x,y:v.y,t:now};
  post("/api/input",{id,x:v.x,y:v.y}).catch(()=>{});
}
setInterval(()=>sendInput(false),90);

game.addEventListener("pointerdown",e=>{
  swipe.on=true;swipe.sx=swipe.x=e.clientX;swipe.sy=swipe.y=e.clientY;
  try{game.setPointerCapture(e.pointerId)}catch{}
  sendInput(true);
});
game.addEventListener("pointermove",e=>{
  if(!swipe.on)return;
  swipe.x=e.clientX;swipe.y=e.clientY;
  sendInput(false);
});
function endSwipe(){swipe.on=false;sendInput(true)}
game.addEventListener("pointerup",endSwipe);
game.addEventListener("pointercancel",endSwipe);

setNameBtn.onclick=()=>{const n=nameEl.value.trim();if(id&&n)post("/api/name",{id,name:n}).catch(()=>{})};
nameEl.addEventListener("keydown",e=>{if(e.key==="Enter")setNameBtn.click()});
respawnBtn.onclick=()=>{if(id)post("/api/respawn",{id}).catch(()=>{})};

function serverMe(){return snap.players.find(p=>p.id===id)||null}

function ingest(s){
  const now=performance.now();
  const ingestMap=(arr,map,skipSelf)=>{
    const seen=new Set();
    for(const o of arr||[]){
      if(skipSelf&&o.id===id)continue;
      seen.add(o.id);
      let v=map.get(o.id);
      if(!v){
        v={...o,x:o.x,y:o.y,vx:o.vx||0,vy:o.vy||0,tx:o.x,ty:o.y,tvx:o.vx||0,tvy:o.vy||0,lastSeen:now};
        map.set(o.id,v);
      }else{
        v.tx=o.x;v.ty=o.y;v.tvx=o.vx||0;v.tvy=o.vy||0;v.lastSeen=now;
        for(const k in o)if(!["x","y","vx","vy"].includes(k))v[k]=o[k];
      }
    }
    for(const [k,v] of map)if(!seen.has(k)&&now-v.lastSeen>500)map.delete(k);
  };
  ingestMap(s.players,REMOTE_PLAYERS,true);
  ingestMap(s.mobs,REMOTE_MOBS,false);
}

function stepRemotes(map,dt){
  for(const v of map.values()){
    v.x+=v.vx*dt;v.y+=v.vy*dt;
    const dx=v.tx-v.x,dy=v.ty-v.y,err=Math.hypot(dx,dy);
    if(err>300){v.x=v.tx;v.y=v.ty}
    else{
      const k=1-Math.exp(-4.0*dt);
      v.x+=dx*k;v.y+=dy*k;
    }
    const kv=1-Math.exp(-4.5*dt);
    v.vx+=(v.tvx-v.vx)*kv;v.vy+=(v.tvy-v.vy)*kv;
  }
}

function stepSelf(server,dt){
  if(!server)return null;
  if(!SELF.init||SELF.alive!==server.alive){
    SELF.init=true;SELF.x=server.x;SELF.y=server.y;SELF.vx=server.vx||0;SELF.vy=server.vy||0;SELF.alive=server.alive;
  }
  if(!server.alive)return{...server,x:SELF.x,y:SELF.y,vx:0,vy:0};

  const iv=desiredInput();
  const maxSpeed=Math.max(82,166-tierOf(server.mass)*5)+speedBonus(server.speed);
  const tvx=iv.x*maxSpeed,tvy=iv.y*maxSpeed;
  SELF.vx+=(tvx-SELF.vx)*Math.min(1,dt*8.5);
  SELF.vy+=(tvy-SELF.vy)*Math.min(1,dt*8.5);
  if(Math.abs(iv.x)+Math.abs(iv.y)<.05){
    SELF.vx*=Math.pow(.12,dt);SELF.vy*=Math.pow(.12,dt);
  }
  const r=vr(server.mass);
  SELF.x=clamp(SELF.x+SELF.vx*dt,r,world.w-r);
  SELF.y=clamp(SELF.y+SELF.vy*dt,r,world.h-r);

  const dx=server.x-SELF.x,dy=server.y-SELF.y,err=Math.hypot(dx,dy);
  if(swipe.on){
    if(err>900){SELF.x+=dx*.04;SELF.y+=dy*.04}
  }else{
    if(err>500){
      SELF.x=server.x;SELF.y=server.y;SELF.vx=server.vx||0;SELF.vy=server.vy||0;
    }else if(err>8){
      const k=1-Math.exp(-.75*dt);
      SELF.x+=dx*k;SELF.y+=dy*k;
    }
  }
  return{...server,x:SELF.x,y:SELF.y,vx:SELF.vx,vy:SELF.vy};
}

function ws(x,y){return{x:(x-cam.x)*cam.z+W/2,y:(y-cam.y)*cam.z+H/2}}
function visible(p,r=50){return p.x>-r&&p.x<W+r&&p.y>-r&&p.y<H+r}
function palette(kind){return kind==="attack"?["#ff6c6c","#ffd0c6"]:kind==="speed"?["#62baff","#d5efff"]:["#6bdd89","#d9ffe2"]}
function flash(s){clearTimeout(toastTimer);toastEl.textContent=s;toastEl.classList.add("show");toastTimer=setTimeout(()=>toastEl.classList.remove("show"),800)}

function bg(me){
  const t=me?tierOf(me.mass):0;
  const P=[["#071c23","#123e48","#73decf"],["#09251f","#244c3c","#9be571"],["#0b2440","#28556d","#79c4ff"],["#101632","#342b58","#a28dff"],["#170f29","#442249","#e282ff"],["#101c2b","#25444c","#ffd77c"]][t%6];
  const g=ctx.createLinearGradient(0,0,W,H);g.addColorStop(0,P[0]);g.addColorStop(1,P[1]);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  const step=Math.max(140,300*cam.z),ox=((0-cam.x)*cam.z+W/2)%step,oy=((0-cam.y)*cam.z+H/2)%step;
  ctx.globalAlpha=.04;ctx.strokeStyle=P[2];ctx.lineWidth=1;
  for(let x=ox;x<W;x+=step){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}
  for(let y=oy;y<H;y+=step){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
  ctx.globalAlpha=1;
}

function drawItem(it){
  const p=ws(it.x,it.y),r=11*cam.z;if(!visible(p,30))return;
  const tt=(performance.now()-start)/1000,s=1+Math.sin(tt*4+it.x*.01)*.05;
  ctx.save();ctx.translate(p.x,p.y);ctx.scale(s,s);
  const color=it.kind==="attack"?"#ff6c6c":it.kind==="speed"?"#62baff":it.kind==="armor"?"#6bdd89":it.kind==="heal"?"#ffd86d":"#d58cff";
  ctx.fillStyle=color;
  if(it.kind==="attack"){
    ctx.beginPath();for(let k=0;k<12;k++){const a=k*Math.PI/6,rr=k%2?r*.5:r,x=Math.cos(a)*rr,y=Math.sin(a)*rr;k?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();
  }else if(it.kind==="speed"){
    ctx.beginPath();ctx.moveTo(-r,-r*.1);ctx.quadraticCurveTo(-r*.05,-r,r,-r*.42);ctx.quadraticCurveTo(r*.2,0,r,r*.42);ctx.quadraticCurveTo(-r*.05,r,-r,r*.1);ctx.closePath();ctx.fill();
  }else if(it.kind==="armor"){
    ctx.beginPath();ctx.moveTo(0,-r);ctx.lineTo(r*.8,-r*.5);ctx.lineTo(r*.6,r*.55);ctx.lineTo(0,r);ctx.lineTo(-r*.6,r*.55);ctx.lineTo(-r*.8,-r*.5);ctx.closePath();ctx.fill();
  }else if(it.kind==="heal"){
    ctx.beginPath();ctx.arc(0,0,r*.8,0,Math.PI*2);ctx.fill();ctx.fillStyle="#fff";ctx.fillRect(-r*.13,-r*.52,r*.26,r*1.04);ctx.fillRect(-r*.52,-r*.13,r*1.04,r*.26);
  }else{
    ctx.beginPath();for(let k=0;k<8;k++){const a=k*Math.PI/4,rr=k%2?r*.4:r,x=Math.cos(a)*rr,y=Math.sin(a)*rr;k?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();
  }
  ctx.restore();
}

function drawMob(m){
  const p=ws(m.x,m.y),r=vr(m.mass)*.88*cam.z;if(!visible(p,r*2+20))return;
  const a=Math.atan2(m.vy||0,m.vx||1),tt=(performance.now()-start)/1000,[c1,c2]=palette(m.kind);
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a);
  if(m.role==="predator"||m.role==="apex"){
    ctx.strokeStyle=m.role==="apex"?"rgba(255,216,109,.8)":"rgba(255,130,120,.55)";
    ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+6,0,Math.PI*2);ctx.stroke();
  }
  const wag=Math.sin(tt*7+m.id.length)*r*.25;
  ctx.fillStyle=c2;ctx.beginPath();ctx.moveTo(-r*.72,0);ctx.quadraticCurveTo(-r*1.15,wag,-r*1.5,-r*.44);ctx.lineTo(-r*1.38,0);ctx.lineTo(-r*1.5,r*.44);ctx.quadraticCurveTo(-r*1.15,wag,-r*.72,0);ctx.fill();
  ctx.fillStyle=c1;
  if((m.species||0)%3===1){
    ctx.beginPath();ctx.moveTo(r,0);ctx.quadraticCurveTo(r*.25,-r*.82,-r*.86,-r*.5);ctx.quadraticCurveTo(-r,0,-r*.86,r*.5);ctx.quadraticCurveTo(r*.25,r*.82,r,0);ctx.fill();
  }else{
    ctx.beginPath();ctx.ellipse(0,0,r,r*((m.species||0)%3===2?.78:.64),0,0,Math.PI*2);ctx.fill();
  }
  if(m.kind==="attack"){
    ctx.fillStyle=c2;for(let k=-2;k<=2;k++){const y=k*r*.2;ctx.beginPath();ctx.moveTo(r*.12,y);ctx.lineTo(r*.72,y-r*.11);ctx.lineTo(r*.5,y+r*.1);ctx.fill()}
  }else if(m.kind==="speed"){
    ctx.fillStyle=c2;ctx.beginPath();ctx.moveTo(-r*.15,-r*.5);ctx.lineTo(-r*.7,-r*.95);ctx.lineTo(r*.1,-r*.6);ctx.fill();
    ctx.beginPath();ctx.moveTo(-r*.15,r*.5);ctx.lineTo(-r*.7,r*.95);ctx.lineTo(r*.1,r*.6);ctx.fill();
  }
  ctx.fillStyle="#05232a";ctx.beginPath();ctx.arc(r*.42,-r*.16,Math.max(1.5,r*.07),0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawPlayer(p,self){
  if(!p||!p.alive)return;
  const q=ws(p.x,p.y),r=vr(p.mass)*cam.z;if(!visible(q,r*2+30))return;
  const a=Math.atan2(p.vy||0,p.vx||1),tt=(performance.now()-start)/1000;
  ctx.save();ctx.translate(q.x,q.y);ctx.rotate(a);
  const wag=Math.sin(tt*7+(p.hue||0))*r*.16;
  ctx.fillStyle=`hsl(${p.hue},72%,72%)`;ctx.beginPath();ctx.moveTo(-r*.75,0);ctx.quadraticCurveTo(-r*1.17,wag,-r*1.52,-r*.44);ctx.lineTo(-r*1.4,0);ctx.lineTo(-r*1.52,r*.44);ctx.quadraticCurveTo(-r*1.17,wag,-r*.75,0);ctx.fill();
  if(p.speed>0){
    ctx.fillStyle="#78cfff";ctx.beginPath();ctx.moveTo(-r*.1,-r*.55);ctx.lineTo(-r*.68,-r*1.05);ctx.lineTo(r*.2,-r*.65);ctx.fill();
    ctx.beginPath();ctx.moveTo(-r*.1,r*.55);ctx.lineTo(-r*.68,r*1.05);ctx.lineTo(r*.2,r*.65);ctx.fill();
  }
  if(p.attack>0){
    ctx.fillStyle="#ffc0a8";const n=Math.min(14,5+Math.floor(Math.log2(1+p.attack)*3));
    for(let k=0;k<n;k++){ctx.save();ctx.rotate(k/n*Math.PI*2);ctx.beginPath();ctx.moveTo(r*.7,-r*.09);ctx.lineTo(r*1.13,0);ctx.lineTo(r*.7,r*.09);ctx.fill();ctx.restore()}
  }
  ctx.fillStyle=self?"#61dcb7":`hsl(${p.hue},68%,54%)`;ctx.beginPath();ctx.ellipse(0,0,r*1.04,r*.82,0,0,Math.PI*2);ctx.fill();
  if(p.armor>0){
    ctx.strokeStyle="rgba(240,255,240,.7)";ctx.lineWidth=Math.max(1.2,r*.045);
    const bands=Math.min(5,1+Math.floor(Math.log2(1+p.armor)));
    for(let k=0;k<bands;k++){ctx.beginPath();ctx.arc(-r*.05,0,r*(.35+k*.1),-1.02,1.02);ctx.stroke()}
  }
  ctx.fillStyle="#05232a";ctx.beginPath();ctx.arc(r*.43,-r*.19,Math.max(2,r*.07),0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(r*.43,r*.19,Math.max(2,r*.07),0,Math.PI*2);ctx.fill();
  ctx.restore();
  if(self){ctx.strokeStyle="rgba(255,255,255,.85)";ctx.lineWidth=2;ctx.beginPath();ctx.arc(q.x,q.y,r+5,0,Math.PI*2);ctx.stroke()}
  ctx.textAlign="center";ctx.font="10px system-ui";ctx.fillStyle="#f4fcff";ctx.fillText(p.name,q.x,q.y-r-11);
  const bw=Math.max(36,r*1.5);ctx.fillStyle="rgba(0,0,0,.35)";ctx.fillRect(q.x-bw/2,q.y-r-7,bw,4);
  ctx.fillStyle=p.hp/p.maxHp>.35?"#9effb9":"#ff8989";ctx.fillRect(q.x-bw/2,q.y-r-7,bw*clamp(p.hp/p.maxHp,0,1),4);
}

function drawSwipe(){
  if(!swipe.on)return;
  const dx=swipe.x-swipe.sx,dy=swipe.y-swipe.sy,l=Math.hypot(dx,dy);
  ctx.strokeStyle="rgba(235,255,250,.24)";ctx.lineWidth=7;ctx.lineCap="round";
  ctx.beginPath();ctx.moveTo(swipe.sx,swipe.sy);ctx.lineTo(swipe.x,swipe.y);ctx.stroke();
  if(l>8){
    const a=Math.atan2(dy,dx);ctx.save();ctx.translate(swipe.x,swipe.y);ctx.rotate(a);ctx.fillStyle="#effffb";
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-14,-7);ctx.lineTo(-14,7);ctx.fill();ctx.restore();
  }
}

function drawMini(me){
  const cw=mini.width,ch=mini.height;
  mx.clearRect(0,0,cw,ch);mx.fillStyle="#0c2933";mx.fillRect(0,0,cw,ch);
  for(const p of snap.players||[]){
    if(!p.alive)continue;
    const x=p.x/world.w*cw,y=p.y/world.h*ch;
    if(p.id===id){
      mx.fillStyle="#fff";mx.beginPath();mx.arc(x,y,6,0,Math.PI*2);mx.fill();
      mx.strokeStyle="#6fffd3";mx.lineWidth=3;mx.beginPath();mx.arc(x,y,9,0,Math.PI*2);mx.stroke();
    }else{
      mx.fillStyle=`hsl(${p.hue},75%,62%)`;mx.beginPath();mx.arc(x,y,4,0,Math.PI*2);mx.fill();
    }
  }
  for(const m of snap.predators||[]){
    const x=m.x/world.w*cw,y=m.y/world.h*ch;
    mx.fillStyle=m.role==="apex"?"#ffd86d":"#ff8c83";
    mx.beginPath();mx.moveTo(x,y-5);mx.lineTo(x+5,y);mx.lineTo(x,y+5);mx.lineTo(x-5,y);mx.closePath();mx.fill();
  }
  if(me){
    const vw=(W/cam.z)/world.w*cw,vh=(H/cam.z)/world.h*ch,x=me.x/world.w*cw-vw/2,y=me.y/world.h*ch-vh/2;
    mx.strokeStyle="rgba(255,255,255,.42)";mx.lineWidth=2;mx.strokeRect(x,y,vw,vh);
  }
}

function updateHud(server,me){
  const p=server||me;
  if(!p){tierEl.textContent="공용 월드 연결 중";statEl.textContent="서버 연결 중…";return}
  const t=tierOf(p.mass),online=(snap.players||[]).filter(x=>x.alive).length;
  tierEl.textContent=`${stageName(t)} · 진화 ${t}`;
  statEl.innerHTML=`온라인 <b>${online}</b>명 · 질량 <b>${Math.floor(p.mass)}</b><br>가시 <b>${p.attack}</b> · 속도 <b>${p.speed}</b> · 방어 <b>${p.armor}</b><br>FPS <b>${fps}</b> · 동기화 <b>${snap.snapHz||8}Hz</b>`;
  if(p.alive!==SELF.alive){
    SELF.alive=p.alive;
    if(!p.alive)deadEl.classList.add("show");
    else{deadEl.classList.remove("show");flash("같은 공용 월드에 복귀했습니다")}
  }
}

function frame(now){
  const dt=Math.min(.033,(now-last)/1000||.016);last=now;
  stepRemotes(REMOTE_PLAYERS,dt);stepRemotes(REMOTE_MOBS,dt);
  const sm=serverMe(),me=stepSelf(sm,dt);

  if(me){
    cam.x=me.x;cam.y=me.y;
    const z=clamp(.98-Math.log2(1+me.mass/20)*.065,.42,.92);
    cam.z+=(z-cam.z)*(1-Math.exp(-4*dt));
  }

  bg(me);
  for(const it of snap.items||[])drawItem(it);
  for(const m of REMOTE_MOBS.values())drawMob(m);
  for(const p of REMOTE_PLAYERS.values())drawPlayer(p,false);
  if(me)drawPlayer(me,true);
  drawSwipe();

  if(now-lastMini>125){drawMini(me);lastMini=now}
  if(now-lastHud>250){updateHud(sm,me);lastHud=now}

  fpsFrames++;
  if(now-fpsMark>=1000){fps=Math.round(fpsFrames*1000/(now-fpsMark));fpsFrames=0;fpsMark=now}

  requestAnimationFrame(frame);
}

join();
requestAnimationFrame(frame);
})();