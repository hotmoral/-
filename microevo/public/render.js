(()=>{
'use strict';
const c=document.getElementById('game'),ctx=c.getContext('2d',{alpha:false}),mini=document.getElementById('mini'),mx=mini.getContext('2d');
const tier=document.getElementById('tier'),stat=document.getElementById('statBody'),dead=document.getElementById('dead'),toast=document.getElementById('toast');
let W=innerWidth,H=innerHeight,DPR=Math.min(devicePixelRatio||1,1.5),last=performance.now(),start=last;
let cam={x:4200,y:4200,z:.9};
const VP=new Map(),VM=new Map();
let toastTimer=0;

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const vr=m=>13+Math.log2(1+Math.max(1,m)/8)*7.2;
const tierOf=m=>Math.max(0,Math.floor(Math.log2(Math.max(1,m)/12)));
const stageName=t=>["미세 연못","수초 생태권","암초 수로","심해 분지","고대 해구","거대 생물권"][t]||`초진화 생태권 ${Math.max(1,t-4)}`;
function resize(){
  W=innerWidth;H=innerHeight;DPR=Math.min(devicePixelRatio||1,1.5);
  c.width=Math.round(W*DPR);c.height=Math.round(H*DPR);c.style.width=W+"px";c.style.height=H+"px";
  ctx.setTransform(DPR,0,0,DPR,0,0);
}
addEventListener('resize',resize,{passive:true});resize();

function ws(x,y){return{x:(x-cam.x)*cam.z+W/2,y:(y-cam.y)*cam.z+H/2}}
function flash(s){clearTimeout(toastTimer);toast.textContent=s;toast.classList.add('show');toastTimer=setTimeout(()=>toast.classList.remove('show'),800)}
function sync(targets,map,dt){
  const now=Date.now(),seen=new Set(),age=clamp((now-(G.snap.t||now))/1000,0,.22);
  for(const o of targets){
    seen.add(o.id);
    let v=map.get(o.id);
    let tx=o.x+(o.vx||0)*age,ty=o.y+(o.vy||0)*age;
    if(o.id===G.id&&G.inputVector){
      const iv=G.inputVector();tx+=iv.x*42*age;ty+=iv.y*42*age;
    }
    if(!v){v={...o,x:tx,y:ty,lastSeen:now};map.set(o.id,v)}
    const fast=o.id===G.id?24:13,k=1-Math.exp(-fast*dt);
    v.x+=(tx-v.x)*k;v.y+=(ty-v.y)*k;
    for(const key in o)if(key!=='x'&&key!=='y')v[key]=o[key];
    v.lastSeen=now;
  }
  for(const [id,v] of map)if(!seen.has(id)&&now-v.lastSeen>900)map.delete(id);
}
function bg(me){
  const t=me?tierOf(me.mass):0;
  const P=[
    ["#061b23","#123f4b","#73decf"],["#09251f","#244c3c","#9be571"],
    ["#0b2440","#28556d","#79c4ff"],["#101632","#342b58","#a28dff"],
    ["#170f29","#442249","#e282ff"],["#101c2b","#25444c","#ffd77c"]
  ][t%6];
  const g=ctx.createLinearGradient(0,0,W,H);g.addColorStop(0,P[0]);g.addColorStop(1,P[1]);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  const step=Math.max(120,280*cam.z),ox=((0-cam.x)*cam.z+W/2)%step,oy=((0-cam.y)*cam.z+H/2)%step;
  ctx.globalAlpha=.055;ctx.strokeStyle=P[2];ctx.lineWidth=1;
  for(let x=ox;x<W;x+=step){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}
  for(let y=oy;y<H;y+=step){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
  ctx.globalAlpha=1;
}
function palette(kind){
  if(kind==='attack')return['#ff6c6c','#ffd0c6'];
  if(kind==='speed')return['#62baff','#d5efff'];
  return['#6bdd89','#d9ffe2'];
}
function visible(p,r=50){return p.x>-r&&p.x<W+r&&p.y>-r&&p.y<H+r}
function item(it){
  const p=ws(it.x,it.y),r=11*cam.z;if(!visible(p,28))return;
  const t=(performance.now()-start)/1000,s=1+Math.sin(t*4+it.x*.01)*.06;
  ctx.save();ctx.translate(p.x,p.y);ctx.scale(s,s);
  const color=it.kind==='attack'?'#ff6c6c':it.kind==='speed'?'#62baff':it.kind==='armor'?'#6bdd89':it.kind==='heal'?'#ffd86d':'#d58cff';
  ctx.globalAlpha=.18;ctx.fillStyle=color;ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;ctx.fillStyle=color;
  if(it.kind==='attack'){
    ctx.beginPath();for(let k=0;k<12;k++){const a=k*Math.PI/6,rr=k%2?r*.5:r,x=Math.cos(a)*rr,y=Math.sin(a)*rr;k?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();
  }else if(it.kind==='speed'){
    ctx.beginPath();ctx.moveTo(-r,-r*.1);ctx.quadraticCurveTo(-r*.05,-r,r,-r*.42);ctx.quadraticCurveTo(r*.2,0,r,r*.42);ctx.quadraticCurveTo(-r*.05,r,-r,r*.1);ctx.closePath();ctx.fill();
  }else if(it.kind==='armor'){
    ctx.beginPath();ctx.moveTo(0,-r);ctx.lineTo(r*.8,-r*.5);ctx.lineTo(r*.6,r*.55);ctx.lineTo(0,r);ctx.lineTo(-r*.6,r*.55);ctx.lineTo(-r*.8,-r*.5);ctx.closePath();ctx.fill();
  }else if(it.kind==='heal'){
    ctx.beginPath();ctx.arc(0,0,r*.8,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.fillRect(-r*.13,-r*.52,r*.26,r*1.04);ctx.fillRect(-r*.52,-r*.13,r*1.04,r*.26);
  }else{
    ctx.beginPath();for(let k=0;k<8;k++){const a=k*Math.PI/4,rr=k%2?r*.4:r,x=Math.cos(a)*rr,y=Math.sin(a)*rr;k?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();
  }
  ctx.restore();
}
function mob(m){
  const p=ws(m.x,m.y),r=vr(m.mass)*.88*cam.z;if(!visible(p,r*2+20))return;
  const a=Math.atan2(m.vy||0,m.vx||1),t=(performance.now()-start)/1000,[c1,c2]=palette(m.kind);
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a);
  if(m.role==='apex'||m.role==='predator'){
    ctx.strokeStyle=m.role==='apex'?'rgba(255,216,109,.7)':'rgba(255,130,120,.55)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+6,0,Math.PI*2);ctx.stroke();
  }
  if(m.flee){
    ctx.strokeStyle='rgba(255,255,255,.30)';ctx.lineWidth=2;
    for(let k=0;k<2;k++){ctx.beginPath();ctx.moveTo(-r*(1.2+k*.35),-r*.25);ctx.lineTo(-r*(1.55+k*.35),-r*.25);ctx.stroke()}
  }
  const wag=Math.sin(t*8+m.x*.01)*r*.25;ctx.fillStyle=c2;
  ctx.beginPath();ctx.moveTo(-r*.72,0);ctx.quadraticCurveTo(-r*1.15,wag,-r*1.55,-r*.45);ctx.lineTo(-r*1.42,0);ctx.lineTo(-r*1.55,r*.45);ctx.quadraticCurveTo(-r*1.15,wag,-r*.72,0);ctx.fill();
  ctx.fillStyle=c1;
  if((m.species||0)%3===1){ctx.beginPath();ctx.moveTo(r,0);ctx.quadraticCurveTo(r*.25,-r*.82,-r*.86,-r*.5);ctx.quadraticCurveTo(-r,0,-r*.86,r*.5);ctx.quadraticCurveTo(r*.25,r*.82,r,0);ctx.fill()}
  else{ctx.beginPath();ctx.ellipse(0,0,r,r*((m.species||0)%3===2?.78:.64),0,0,Math.PI*2);ctx.fill()}
  if(m.kind==='attack'){ctx.fillStyle=c2;for(let k=-2;k<=2;k++){const yy=k*r*.2;ctx.beginPath();ctx.moveTo(r*.12,yy);ctx.lineTo(r*.72,yy-r*.11);ctx.lineTo(r*.5,yy+r*.1);ctx.fill()}}
  if(m.kind==='speed'){ctx.fillStyle=c2;ctx.beginPath();ctx.moveTo(-r*.15,-r*.5);ctx.lineTo(-r*.7,-r*.95);ctx.lineTo(r*.1,-r*.6);ctx.fill();ctx.beginPath();ctx.moveTo(-r*.15,r*.5);ctx.lineTo(-r*.7,r*.95);ctx.lineTo(r*.1,r*.6);ctx.fill()}
  ctx.fillStyle='#05232a';ctx.beginPath();ctx.arc(r*.42,-r*.16,Math.max(1.5,r*.07),0,Math.PI*2);ctx.fill();
  ctx.restore();
}
function player(p,self){
  if(!p.alive)return;
  const q=ws(p.x,p.y),r=vr(p.mass)*cam.z;if(!visible(q,r*2+30))return;
  const a=Math.atan2(p.vy||0,p.vx||1),t=(performance.now()-start)/1000;
  ctx.save();ctx.translate(q.x,q.y);ctx.rotate(a);
  const wag=Math.sin(t*8+p.x*.01)*r*.16;ctx.fillStyle=`hsl(${p.hue},72%,72%)`;
  ctx.beginPath();ctx.moveTo(-r*.75,0);ctx.quadraticCurveTo(-r*1.17,wag,-r*1.55,-r*.44);ctx.lineTo(-r*1.42,0);ctx.lineTo(-r*1.55,r*.44);ctx.quadraticCurveTo(-r*1.17,wag,-r*.75,0);ctx.fill();
  if(p.speed>0){ctx.fillStyle='#78cfff';ctx.beginPath();ctx.moveTo(-r*.1,-r*.55);ctx.lineTo(-r*.68,-r*1.05);ctx.lineTo(r*.2,-r*.65);ctx.fill();ctx.beginPath();ctx.moveTo(-r*.1,r*.55);ctx.lineTo(-r*.68,r*1.05);ctx.lineTo(r*.2,r*.65);ctx.fill()}
  if(p.attack>0){ctx.fillStyle='#ffc0a8';const n=Math.min(16,5+Math.floor(Math.log2(1+p.attack)*3));for(let k=0;k<n;k++){ctx.save();ctx.rotate(k/n*Math.PI*2);ctx.beginPath();ctx.moveTo(r*.7,-r*.09);ctx.lineTo(r*1.13,0);ctx.lineTo(r*.7,r*.09);ctx.fill();ctx.restore()}}
  ctx.fillStyle=self?'#61dcb7':`hsl(${p.hue},68%,54%)`;ctx.beginPath();ctx.ellipse(0,0,r*1.04,r*.82,0,0,Math.PI*2);ctx.fill();
  if(p.armor>0){ctx.strokeStyle='rgba(240,255,240,.7)';ctx.lineWidth=Math.max(1.2,r*.045);const bands=Math.min(5,1+Math.floor(Math.log2(1+p.armor)));for(let k=0;k<bands;k++){ctx.beginPath();ctx.arc(-r*.05,0,r*(.35+k*.1),-1.02,1.02);ctx.stroke()}}
  ctx.fillStyle='#05232a';ctx.beginPath();ctx.arc(r*.43,-r*.19,Math.max(2,r*.07),0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(r*.43,r*.19,Math.max(2,r*.07),0,Math.PI*2);ctx.fill();
  ctx.restore();
  if(self){ctx.strokeStyle='rgba(255,255,255,.85)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(q.x,q.y,r+5,0,Math.PI*2);ctx.stroke()}
  ctx.textAlign='center';ctx.font='10px system-ui';ctx.fillStyle='#f4fcff';ctx.fillText(p.name,q.x,q.y-r-11);
  const bw=Math.max(36,r*1.5);ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(q.x-bw/2,q.y-r-7,bw,4);ctx.fillStyle=p.hp/p.maxHp>.35?'#9effb9':'#ff8989';ctx.fillRect(q.x-bw/2,q.y-r-7,bw*clamp(p.hp/p.maxHp,0,1),4);
}
function swipe(){
  const s=G.swipe;if(!s.on)return;const dx=s.x-s.sx,dy=s.y-s.sy,l=Math.hypot(dx,dy);
  ctx.strokeStyle='rgba(235,255,250,.28)';ctx.lineWidth=7;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(s.sx,s.sy);ctx.lineTo(s.x,s.y);ctx.stroke();
  if(l>8){const a=Math.atan2(dy,dx);ctx.save();ctx.translate(s.x,s.y);ctx.rotate(a);ctx.fillStyle='#effffb';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-14,-7);ctx.lineTo(-14,7);ctx.fill();ctx.restore()}
}
function minimap(me){
  const cw=mini.width,ch=mini.height;mx.clearRect(0,0,cw,ch);mx.fillStyle='#0c2933';mx.fillRect(0,0,cw,ch);
  for(const p of G.snap.players){if(!p.alive)continue;const px=p.x/G.world.w*cw,py=p.y/G.world.h*ch;if(p.id===G.id){mx.fillStyle='#fff';mx.beginPath();mx.arc(px,py,6,0,Math.PI*2);mx.fill();mx.strokeStyle='#6fffd3';mx.lineWidth=3;mx.beginPath();mx.arc(px,py,9,0,Math.PI*2);mx.stroke()}else{mx.fillStyle=`hsl(${p.hue},75%,62%)`;mx.beginPath();mx.arc(px,py,4,0,Math.PI*2);mx.fill()}}
  if(me)for(const m of (G.snap.predators||[])){const px=m.x/G.world.w*cw,py=m.y/G.world.h*ch;mx.fillStyle=m.role==='apex'?'#ffd86d':'#ff8c83';mx.beginPath();mx.moveTo(px,py-5);mx.lineTo(px+5,py);mx.lineTo(px,py+5);mx.lineTo(px-5,py);mx.closePath();mx.fill()}
  if(me){const vw=(W/cam.z)/G.world.w*cw,vh=(H/cam.z)/G.world.h*ch,px=me.x/G.world.w*cw-vw/2,py=me.y/G.world.h*ch-vh/2;mx.strokeStyle='rgba(255,255,255,.42)';mx.lineWidth=2;mx.strokeRect(px,py,vw,vh)}
}
function hud(me){
  if(!me){tier.textContent='공용 월드 연결 중';stat.textContent='서버 연결 중…';return}
  const t=tierOf(me.mass),online=G.snap.players.filter(p=>p.alive).length;
  tier.textContent=`${stageName(t)} · 진화 ${t}`;
  stat.innerHTML=`온라인 <b>${online}</b>명 · 질량 <b>${Math.floor(me.mass)}</b><br>가시 <b>${me.attack}</b> · 속도 <b>${me.speed}</b> · 방어 <b>${me.armor}</b><br>포식 <b>${me.eaten}</b> · PvP <b>${me.kills}</b>`;
  if(me.alive!==G.lastAlive){if(!me.alive)dead.classList.add('show');else{dead.classList.remove('show');flash('같은 공용 월드에 복귀했습니다')}G.lastAlive=me.alive}
}
function frame(now){
  const dt=Math.min(.05,(now-last)/1000||.016);last=now;
  sync(G.snap.players,VP,dt);sync(G.snap.mobs,VM,dt);
  const me=VP.get(G.id)||G.me();
  if(me){
    cam.x+=(me.x-cam.x)*(1-Math.exp(-9*dt));cam.y+=(me.y-cam.y)*(1-Math.exp(-9*dt));
    const targetZ=clamp(.98-Math.log2(1+me.mass/20)*.065,.42,.92);cam.z+=(targetZ-cam.z)*(1-Math.exp(-4*dt));
  }
  bg(me);
  for(const i of G.snap.items)item(i);
  for(const m of VM.values())mob(m);
  for(const p of VP.values())if(p.id!==G.id)player(p,false);
  if(me)player(me,true);
  swipe();minimap(me);hud(me);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();