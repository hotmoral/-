/* Outpost Wilds V4 play-feel patch: smoothing, hold attack, lighter rendering, clearer survivor/cargo. */
const v4Coarse=matchMedia('(pointer:coarse)').matches;
DPR=Math.min(v4Coarse?1.25:1.7,devicePixelRatio||1);
resize();
ctx.imageSmoothingEnabled=true;
ctx.imageSmoothingQuality='high';

const v4Players=new Map();
const v4Enemies=new Map();
let v4RenderT=performance.now();
let v4HudNext=0;

function v4State(map,id,x,y){
  let r=map.get(id);
  if(!r){r={x,y,tx:x,ty:y};map.set(id,r);}
  return r;
}
function v4SyncSnapshot(s){
  if(!s)return;
  const liveP=new Set(),liveE=new Set();
  for(const p of s.players||[]){
    liveP.add(p.id);const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;
    if(Math.hypot(r.x-p.x,r.y-p.y)>260){r.x=p.x;r.y=p.y;}
  }
  for(const e of s.enemies||[]){
    liveE.add(e.id);const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;
    if(Math.hypot(r.x-e.x,r.y-e.y)>320){r.x=e.x;r.y=e.y;}
  }
  for(const id of v4Players.keys())if(!liveP.has(id))v4Players.delete(id);
  for(const id of v4Enemies.keys())if(!liveE.has(id))v4Enemies.delete(id);
}
const v4OldMessage=ws.onmessage;
ws.onmessage=function(e){
  try{const m=JSON.parse(e.data);if(m.type==='snapshot')v4SyncSnapshot(m);}catch{}
  v4OldMessage.call(this,e);
};

const v4RawHud=updateHud;
updateHud=function(){
  const now=performance.now();
  if(now<v4HudNext)return;
  v4HudNext=now+150;
  v4RawHud();
};

function v4Advance(){
  const now=performance.now(),dt=Math.min(.05,(now-v4RenderT)/1000);v4RenderT=now;
  if(!snap)return;
  for(const p of snap.players||[]){
    const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;
    if(p.id===meId){
      const moving=Math.hypot(input.x,input.y)>.025;
      if(moving){
        const z=zoneAtPos(r.x,r.y),speed=z==='quarry'?212:z==='danger'?218:224;
        r.x+=input.x*speed*dt;r.y+=input.y*speed*dt;
        r.x=Math.max(35,Math.min(3565,r.x));r.y=Math.max(35,Math.min(3565,r.y));
      }
      const err=Math.hypot(r.tx-r.x,r.ty-r.y);
      if(err>150){r.x=r.tx;r.y=r.ty;}
      else{
        const k=Math.min(1,dt*(moving?1.7:8.5));r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
      }
    }else{
      const k=Math.min(1,dt*11.5);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
    }
  }
  for(const e of snap.enemies||[]){
    const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;
    const k=Math.min(1,dt*10.5);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
  }
}

myPlayer=function(){
  const p=snap?.players.find(p=>p.id===meId);if(!p)return p;
  const r=v4Players.get(p.id);return r?{...p,x:r.x,y:r.y}:p;
};

function v4Rounded(x,y,w,h,r){
  const rr=Math.min(r,w/2,h/2);ctx.beginPath();ctx.moveTo(x+rr,y);ctx.arcTo(x+w,y,x+w,y+h,rr);ctx.arcTo(x+w,y+h,x,y+h,rr);ctx.arcTo(x,y+h,x,y,rr);ctx.arcTo(x,y,x+w,y,rr);ctx.closePath();
}

const v4OldGround=drawGround;
drawGround=function(){
  v4Advance();
  ctx.fillStyle=zoneColors.danger;ctx.fillRect(0,0,W,H);
  const c=worldToScreen(1800,1800);
  ctx.save();ctx.beginPath();ctx.arc(c.x,c.y,1320,0,Math.PI*2);ctx.clip();
  ctx.fillStyle=zoneColors.meadow;ctx.fillRect(0,0,W,H);
  const forestX=1420-cam.x+W/2,quarryX=2260-cam.x+W/2;
  ctx.fillStyle=zoneColors.forest;ctx.fillRect(-1e4,-1e4,forestX+1e4,2e4);
  ctx.fillStyle=zoneColors.quarry;ctx.fillRect(quarryX,-1e4,1e4,2e4);
  ctx.restore();
  ctx.fillStyle=zoneColors.camp;ctx.beginPath();ctx.arc(c.x,c.y,470,0,Math.PI*2);ctx.fill();

  const tile=v4Coarse?156:132;
  const x0=Math.floor((cam.x-W/2)/tile)*tile,y0=Math.floor((cam.y-H/2)/tile)*tile;
  for(let x=x0;x<cam.x+W/2+tile;x+=tile)for(let y=y0;y<cam.y+H/2+tile;y+=tile){
    const sx=x-cam.x+W/2,sy=y-cam.y+H/2,h=hash2(x/tile,y/tile),z=zoneAtPos(x,y);
    ctx.save();ctx.translate(sx+(h-.5)*44,sy+(hash2(y/tile,x/tile)-.5)*44);ctx.rotate(h*6);ctx.globalAlpha=.15;
    if(z==='forest'){ctx.fillStyle='#77a16b';ctx.fillRect(-1,-8,2,16);ctx.fillRect(-6,-1,12,2);}
    else if(z==='quarry'){ctx.strokeStyle='#b0a287';ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(-10,2);ctx.lineTo(-3,-5);ctx.lineTo(6,-1);ctx.stroke();}
    else if(z==='danger'){ctx.strokeStyle='#a17768';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-7,0);ctx.lineTo(7,0);ctx.moveTo(-2,-4);ctx.lineTo(2,4);ctx.stroke();}
    else{ctx.fillStyle='#90aa72';ctx.fillRect(-1,-5,2,10);ctx.fillRect(-5,-1,10,2);}
    ctx.restore();ctx.globalAlpha=1;
  }
  if(snap){
    const s=worldToScreen(snap.base.x,snap.base.y),g=ctx.createRadialGradient(s.x,s.y,20,s.x,s.y,370);g.addColorStop(0,'rgba(214,171,92,.12)');g.addColorStop(1,'rgba(214,171,92,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(s.x,s.y,370,0,Math.PI*2);ctx.fill();
  }
  ctx.save();ctx.strokeStyle='#9a75602b';ctx.lineWidth=2;ctx.setLineDash([18,22]);ctx.beginPath();ctx.arc(c.x,c.y,1320,0,Math.PI*2);ctx.stroke();ctx.restore();
};

function v4CargoVisual(p,s){
  if(!p.carry)return;
  const dir=p.dir||0,bx=s.x-Math.cos(dir)*23,by=s.y-Math.sin(dir)*23+4;
  ctx.save();ctx.translate(bx,by);ctx.rotate(dir);
  ctx.fillStyle='#252820cc';v4Rounded(-16,-16,30,34,8);ctx.fill();ctx.strokeStyle='#8c7958';ctx.lineWidth=2;ctx.stroke();
  const woodN=Math.min(4,Math.ceil((p.wood||0)/8));
  for(let i=0;i<woodN;i++){const yy=10-i*6;ctx.fillStyle='#9c643b';v4Rounded(-19,yy-4,30,6,3);ctx.fill();ctx.fillStyle='#d39a62';ctx.beginPath();ctx.arc(10,yy-1,3,0,Math.PI*2);ctx.fill();}
  const stoneN=Math.min(3,Math.ceil((p.stone||0)/9));
  for(let i=0;i<stoneN;i++){const xx=-13+i*8,yy=-13-(i%2)*4;ctx.fillStyle='#9ba2a0';ctx.beginPath();ctx.moveTo(xx-5,yy+4);ctx.lineTo(xx-2,yy-5);ctx.lineTo(xx+5,yy-3);ctx.lineTo(xx+6,yy+4);ctx.closePath();ctx.fill();}
  const meatN=Math.min(2,Math.ceil((p.meat||0)/10));
  for(let i=0;i<meatN;i++){ctx.fillStyle='#b85b50';v4Rounded(3+i*5,-17-i*4,10,13,4);ctx.fill();ctx.strokeStyle='#e6c3aa';ctx.lineWidth=1;ctx.stroke();}
  ctx.restore();
  if(p.id===meId){
    const label=`목 ${p.wood||0}  돌 ${p.stone||0}  식 ${p.meat||0}`;
    ctx.save();ctx.font='700 9px sans-serif';const tw=ctx.measureText(label).width+14;ctx.fillStyle='#08100bd9';v4Rounded(s.x-tw/2,s.y-69,tw,18,9);ctx.fill();ctx.strokeStyle='#ffffff16';ctx.stroke();ctx.fillStyle='#f3e5c9';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(label,s.x,s.y-60);ctx.restore();
  }
}

drawCargo=function(p,s){v4CargoVisual(p,s);};

drawPlayer=function(p,isMe,t){
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py);
  const phase=movePhase.get(p.id)||0,moving=isMe?Math.hypot(input.x,input.y)>.04:true,bob=moving?Math.sin(phase)*1.9:Math.sin(phase)*.35;
  shadow(s.x,s.y+25,22,8,.32);v4CargoVisual(p,s);
  ctx.save();ctx.translate(s.x,s.y+bob);ctx.rotate(p.dir||0);ctx.scale(1.08,1.08);
  const stride=moving?Math.sin(phase)*6:0;
  ctx.strokeStyle='#282a29';ctx.lineWidth=7;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-5,8);ctx.lineTo(-8,19+stride*.35);ctx.moveTo(5,8);ctx.lineTo(9,19-stride*.35);ctx.stroke();
  ctx.strokeStyle='#181b1b';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-8,18+stride*.35);ctx.lineTo(-13,20+stride*.35);ctx.moveTo(9,18-stride*.35);ctx.lineTo(14,20-stride*.35);ctx.stroke();
  ctx.fillStyle=isMe?'#4f7868':`hsl(${(p.id.charCodeAt(0)*47)%360} 32% 48%)`;v4Rounded(-13,-9,27,29,8);ctx.fill();
  ctx.fillStyle='#2d342f';ctx.fillRect(-13,5,27,5);ctx.fillStyle='#c6a36f';ctx.fillRect(1,5,4,5);
  ctx.fillStyle='#718b79';ctx.beginPath();ctx.moveTo(-11,-8);ctx.lineTo(-4,-14);ctx.lineTo(3,-8);ctx.closePath();ctx.fill();
  circle(7,-18,9.5,'#dcb58c');ctx.fillStyle='#4b382d';ctx.beginPath();ctx.arc(6,-20,10,Math.PI,Math.PI*2);ctx.fill();ctx.fillRect(-1,-22,15,4);
  ctx.fillStyle='#e0b994';ctx.beginPath();ctx.moveTo(15,-18);ctx.lineTo(20,-16);ctx.lineTo(15,-14);ctx.closePath();ctx.fill();
  circle(12,-19,1.15,'#312923');
  ctx.strokeStyle='#d8b28b';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(5,-2);ctx.lineTo(19,-4);ctx.stroke();
  const swing=attackFx.get(p.id);let sw=0;if(swing&&!swing.ranged){sw=(.34-swing.t)/.34;sw=Math.sin(sw*Math.PI)*1.12;}drawWeapon(p,sw);
  ctx.restore();
  if(isMe){circle(s.x,s.y+2,28,null,'#ffffffa0',1.5);circle(s.x,s.y+2,34,null,'#9bd8c02d',1);}
  ctx.save();ctx.textAlign='center';ctx.shadowColor='#000';ctx.shadowBlur=5;ctx.font='700 10px sans-serif';ctx.fillStyle='#fff';ctx.fillText(p.name,s.x,s.y-42);ctx.shadowBlur=0;drawHealth(s.x,s.y-35,p.hp/p.maxHp,42);ctx.restore();
};

drawEnemy=function(e,t){
  const rr=v4Enemies.get(e.id),ex=rr?.x??e.x,ey=rr?.y??e.y,s=worldToScreen(ex,ey),movingBob=Math.sin(t*.006+e.id)*1.1;
  shadow(s.x,s.y+18,e.r*1.25,7,.32);const name=e.type==='alpha'?'alpha':e.type==='boar'?'boar':e.type==='brute'?'brute':'wolf',flip=Math.cos(e.dir||0)<0,w=e.type==='alpha'?148:e.type==='brute'?100:e.type==='boar'?96:92,h=e.type==='alpha'?108:e.type==='brute'?76:e.type==='boar'?64:61;
  if(e.type==='alpha'){const g=ctx.createRadialGradient(s.x,s.y,15,s.x,s.y,75);g.addColorStop(0,'rgba(160,56,45,.18)');g.addColorStop(1,'rgba(160,56,45,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(s.x,s.y,75,0,Math.PI*2);ctx.fill();}
  drawAsset(name,s.x,s.y-3+movingBob,w,h,flip,0);drawHealth(s.x,s.y-e.r-22,e.hp/e.maxHp,e.type==='alpha'?72:42);if(e.raid){ctx.font='bold 9px sans-serif';ctx.textAlign='center';ctx.fillStyle='#f38b78';ctx.fillText(e.type==='alpha'?'우두머리':'습격',s.x,s.y-e.r-30);}
};

const v4OldBurst=burst;
burst=function(x,y,color,count=8,speed=145){if(particles.length>90)return;v4OldBurst(x,y,color,Math.min(count,12),speed);};

const v4OldAttack=document.getElementById('attack');
const v4Attack=v4OldAttack.cloneNode(true);v4OldAttack.replaceWith(v4Attack);
let v4AttackTimer=null;
function v4AttackStart(e){e.preventDefault();if(v4AttackTimer)return;v4Attack.classList.add('holding');send({type:'attack'});v4AttackTimer=setInterval(()=>send({type:'attack'}),255);}
function v4AttackStop(e){if(e)e.preventDefault();if(v4AttackTimer){clearInterval(v4AttackTimer);v4AttackTimer=null;}v4Attack.classList.remove('holding');}
v4Attack.addEventListener('pointerdown',v4AttackStart);v4Attack.addEventListener('pointerup',v4AttackStop);v4Attack.addEventListener('pointercancel',v4AttackStop);v4Attack.addEventListener('pointerleave',e=>{if(e.buttons===0)v4AttackStop(e)});
window.addEventListener('blur',()=>v4AttackStop());
