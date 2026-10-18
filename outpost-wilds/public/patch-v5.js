/* Outpost Wilds V5: icon-first resources, stable weighted movement, illustrated survivor. */
const v5AssetPaths={wood:'/assets/res-wood.svg',stone:'/assets/res-stone.svg',meat:'/assets/res-meat.svg',survivorA:'/assets/survivor-walk-a.svg',survivorB:'/assets/survivor-walk-b.svg'};
const v5Assets={};
for(const [k,src] of Object.entries(v5AssetPaths)){const im=new Image();im.src=src;v5Assets[k]=im;}

function v5CarryFactor(p){
  if(!p||!p.carryCap)return 1;
  const q=Math.max(0,Math.min(1,p.carry/p.carryCap));
  return Math.max(.86,1-.14*Math.pow(q,1.35));
}
function v5ServerZoneSpeed(x,y){const z=zoneAtPos(x,y);return z==='quarry'?212:z==='danger'?218:224;}
function v5PredictedPlayer(){
  const base=snap?.players?.find(p=>p.id===meId);if(!base)return base;
  const r=v4Players.get(meId);return r?{...base,x:r.x,y:r.y}:base;
}

/* Send movement at a compensating magnitude so all zones resolve to one world speed.
   Cargo weight is continuous, avoiding abrupt threshold changes. */
const v5RawSend=send;
send=function(m){
  if(m?.type==='input'){
    const p=v5PredictedPlayer();
    if(p){
      const zoneBase=v5ServerZoneSpeed(p.x,p.y),weight=v5CarryFactor(p),scale=(212/zoneBase)*weight;
      return v5RawSend({...m,x:(Number(m.x)||0)*scale,y:(Number(m.y)||0)*scale});
    }
  }
  return v5RawSend(m);
};

/* Replace V4 prediction with the exact same effective 212px/s * cargo factor used above. */
v4Advance=function(){
  const now=performance.now(),dt=Math.min(.04,(now-v4RenderT)/1000);v4RenderT=now;
  if(!snap)return;
  for(const p of snap.players||[]){
    const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;
    if(p.id===meId){
      const moving=Math.hypot(input.x,input.y)>.025;
      if(moving){
        const speed=212*v5CarryFactor(p);
        r.x+=input.x*speed*dt;r.y+=input.y*speed*dt;
        r.x=Math.max(35,Math.min(3565,r.x));r.y=Math.max(35,Math.min(3565,r.y));
      }
      const err=Math.hypot(r.tx-r.x,r.ty-r.y);
      if(err>180){r.x=r.tx;r.y=r.ty;}
      else{
        const rate=err<8?(moving?.75:7.5):err<36?(moving?2.1:8.5):5.2;
        const k=1-Math.exp(-rate*dt);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
      }
    }else{
      const k=1-Math.exp(-10.5*dt);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
    }
  }
  for(const e of snap.enemies||[]){
    const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;
    const k=1-Math.exp(-9.5*dt);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
  }
};

/* Icon-first HUD. */
const v5OldHud=updateHud;
updateHud=function(){
  v5OldHud();
  const p=v5PredictedPlayer();if(!p||!snap)return;
  const q=Math.max(0,Math.min(1,p.carry/p.carryCap));
  const carryLabel=document.getElementById('carryLabel');if(carryLabel)carryLabel.textContent=`${Math.round(q*100)}%`;
  const carryCard=carryLabel?.closest('.carry');if(carryCard)carryCard.style.setProperty('--load',q.toFixed(3));
  const up=snap.base.upgrade,costEl=document.getElementById('missionCost');
  if(costEl&&up?.cost){
    const c=up.cost,b=snap.base;
    costEl.innerHTML=`<i class="${b.wood>=c.wood?'done':''}"><img src="${v5AssetPaths.wood}" alt="목재"><b>${b.wood}/${c.wood}</b></i><i class="${b.stone>=c.stone?'done':''}"><img src="${v5AssetPaths.stone}" alt="돌"><b>${b.stone}/${c.stone}</b></i><i class="${b.meat>=c.meat?'done':''}"><img src="${v5AssetPaths.meat}" alt="식량"><b>${b.meat}/${c.meat}</b></i>`;
  }
};

const v5IconFloaters=[];
function v5PushResource(resource,amount,x,y,scale=1){
  if(amount<=0)return;v5IconFloaters.push({resource,amount,x,y,life:1.05,max:1.05,scale});
  const chip=document.getElementById(resource)?.closest('.resourceChip');if(chip){chip.classList.remove('gain');void chip.offsetWidth;chip.classList.add('gain');}
}
function v5ResourceToast(m){
  const bits=[];for(const r of ['wood','stone','meat'])if((m[r]||0)>0)bits.push(`<span><img src="${v5AssetPaths[r]}" alt=""><b>${m[r]}</b></span>`);
  if(!bits.length)return;
  toastEl.innerHTML=`<div class="resourceToast">${bits.join('')}</div>`;toastEl.className='show iconToast';
  clearTimeout(window.__v5ToastTimer);window.__v5ToastTimer=setTimeout(()=>{toastEl.className='';},1350);
}
const v5OldEventFx=eventFx;
eventFx=function(m){
  if(m.kind==='gather'&&m.playerId===meId){v5PushResource(m.resource,m.amount,m.x,m.y,m.nodeType==='ore'?1.12:1);return;}
  if(m.kind==='kill'&&m.playerId===meId){v5PushResource('meat',m.amount,m.x,m.y,1.08);return;}
  if(m.kind==='deposit'&&m.playerId===meId){v5ResourceToast(m);burst(snap.base.x,snap.base.y,'#efc96f',10,170);return;}
  v5OldEventFx(m);
};

const v5OldDrawParticles=drawParticles;
drawParticles=function(dt){
  v5OldDrawParticles(dt);
  for(let i=v5IconFloaters.length-1;i>=0;i--){
    const f=v5IconFloaters[i];f.life-=dt;if(f.life<=0){v5IconFloaters.splice(i,1);continue;}
    f.y-=27*dt;const s=worldToScreen(f.x,f.y),im=v5Assets[f.resource],fade=Math.min(1,f.life/.22),size=27*f.scale;
    ctx.save();ctx.globalAlpha=fade;ctx.translate(s.x,s.y);ctx.fillStyle='rgba(7,13,9,.82)';v4Rounded(-27,-17,54,34,16);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.10)';ctx.stroke();
    if(im?.complete)ctx.drawImage(im,-23,-13,size,size);ctx.font='800 14px sans-serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillStyle='#fff2da';ctx.shadowColor='#000';ctx.shadowBlur=4;ctx.fillText(`+${f.amount}`,7,0);ctx.restore();
  }
};

function v5DrawMiniResource(resource,count,x,y,size=19){
  if(!count)return;const im=v5Assets[resource];ctx.save();ctx.translate(x,y);ctx.fillStyle='rgba(7,13,9,.82)';v4Rounded(-size*.62,-size*.55,size*1.55,size*1.1,size*.45);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.10)';ctx.stroke();if(im?.complete)ctx.drawImage(im,-size*.55,-size*.5,size,size);ctx.font=`800 ${Math.round(size*.55)}px sans-serif`;ctx.fillStyle='#fff0d7';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(String(count),size*.30,0);ctx.restore();
}
function v5CargoVisual(p,s){
  if(!p.carry)return;
  const dir=p.dir||0,bx=s.x-Math.cos(dir)*27,by=s.y-Math.sin(dir)*27+7;
  ctx.save();ctx.translate(bx,by);ctx.rotate(dir);ctx.fillStyle='#2b2922';ctx.beginPath();ctx.ellipse(-2,1,18,23,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#9a7650';ctx.lineWidth=2.5;ctx.stroke();
  const slots=[];if(p.wood)slots.push(['wood',Math.min(1,p.wood/18)]);if(p.stone)slots.push(['stone',Math.min(1,p.stone/18)]);if(p.meat)slots.push(['meat',Math.min(1,p.meat/18)]);
  const pos=[[-13,7],[2,-9],[10,8]];slots.forEach(([r,q],i)=>{const im=v5Assets[r],sz=21+q*8;if(im?.complete)ctx.drawImage(im,pos[i][0]-sz/2,pos[i][1]-sz/2,sz,sz);});ctx.restore();
  if(p.id===meId){const y=s.y-72;let x=s.x-48;for(const r of ['wood','stone','meat']){const n=p[r]||0;if(n){v5DrawMiniResource(r,n,x,y,19);x+=37;}}}
}
drawCargo=function(p,s){v5CargoVisual(p,s);};

/* Illustrated two-frame survivor instead of geometric body primitives. */
drawPlayer=function(p,isMe,t){
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py),phase=movePhase.get(p.id)||0;
  const moving=isMe?Math.hypot(input.x,input.y)>.04:true,bob=moving?Math.sin(phase)*1.6:Math.sin(phase)*.25;
  shadow(s.x,s.y+27,23,8,.30);v5CargoVisual(p,s);
  ctx.save();ctx.translate(s.x,s.y+bob);ctx.rotate(p.dir||0);
  const frame=moving&&Math.sin(phase)>0?v5Assets.survivorB:v5Assets.survivorA;if(frame?.complete)ctx.drawImage(frame,-35,-49,70,88);
  const swing=attackFx.get(p.id);let sw=0;if(swing&&!swing.ranged){sw=(.34-swing.t)/.34;sw=Math.sin(sw*Math.PI)*1.12;}ctx.translate(0,-3);drawWeapon(p,sw);ctx.restore();
  if(isMe){circle(s.x,s.y+3,29,null,'#fff9',1.5);circle(s.x,s.y+3,35,null,'#9bd8c028',1);}
  ctx.save();ctx.textAlign='center';ctx.shadowColor='#000';ctx.shadowBlur=5;ctx.font='700 10px sans-serif';ctx.fillStyle='#fff';ctx.fillText(p.name,s.x,s.y-45);ctx.shadowBlur=0;drawHealth(s.x,s.y-38,p.hp/p.maxHp,43);ctx.restore();
};

/* Keep SPACE held for continuous desktop attack as well. */
let v5SpaceTimer=null;
addEventListener('keydown',e=>{if(e.code==='Space'&&!v5SpaceTimer){e.preventDefault();v5SpaceTimer=setInterval(()=>send({type:'attack'}),255);}},true);
addEventListener('keyup',e=>{if(e.code==='Space'&&v5SpaceTimer){clearInterval(v5SpaceTimer);v5SpaceTimer=null;}},true);
window.addEventListener('blur',()=>{if(v5SpaceTimer){clearInterval(v5SpaceTimer);v5SpaceTimer=null;}});
