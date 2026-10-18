(()=>{
'use strict';
const game=document.getElementById('game'),nameEl=document.getElementById('name'),setName=document.getElementById('setName'),respawn=document.getElementById('respawn'),offline=document.getElementById('offline');
const G=window.G={id:null,world:{w:8400,h:8400},snap:{t:0,players:[],mobs:[],items:[],predators:[]},swipe:{on:false,sx:0,sy:0,x:0,y:0},connected:false,lastAlive:true,lastInput:{x:999,y:999,t:0}};
function postJson(url,body,wantJson=false){
  return fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),cache:'no-store'})
    .then(r=>wantJson?r.json():null);
}
async function join(){
  try{
    const resumeId=localStorage.getItem('microevo_id')||undefined;
    const r=await postJson('/api/join',{resumeId},true);
    if(!r||!r.id)throw new Error('join');
    G.id=r.id;G.world=r.world;localStorage.setItem('microevo_id',G.id);
    connectEvents();offline.style.display='none';
  }catch(e){offline.style.display='block';setTimeout(join,1200)}
}
function connectEvents(){
  if(!G.id)return;
  const es=new EventSource('/events?id='+encodeURIComponent(G.id));
  G.es=es;
  es.onopen=()=>{G.connected=true;offline.style.display='none'};
  es.onmessage=e=>{
    try{
      const s=JSON.parse(e.data);
      if(s&&Array.isArray(s.players)){G.snap=s;G.connected=true;offline.style.display='none'}
    }catch{}
  };
  es.onerror=()=>{G.connected=false;offline.style.display='block'};
}
function desiredInput(){
  let x=0,y=0;
  if(G.swipe.on){
    const dx=G.swipe.x-G.swipe.sx,dy=G.swipe.y-G.swipe.sy,l=Math.hypot(dx,dy);
    if(l>8){x=dx/l;y=dy/l}
  }
  return{x,y};
}
function maybeSendInput(force=false){
  if(!G.id)return;
  const v=desiredInput(),now=performance.now(),last=G.lastInput;
  const changed=Math.abs(v.x-last.x)+Math.abs(v.y-last.y)>.045;
  if(!force&&now-last.t<70)return;
  if(!force&&!changed&&now-last.t<240)return;
  G.lastInput={x:v.x,y:v.y,t:now};
  postJson('/api/input',{id:G.id,x:v.x,y:v.y}).catch(()=>{});
}
setInterval(()=>maybeSendInput(false),80);

game.addEventListener('pointerdown',e=>{
  G.swipe.on=true;G.swipe.sx=G.swipe.x=e.clientX;G.swipe.sy=G.swipe.y=e.clientY;
  try{game.setPointerCapture(e.pointerId)}catch{}
  maybeSendInput(true);
});
game.addEventListener('pointermove',e=>{if(G.swipe.on){G.swipe.x=e.clientX;G.swipe.y=e.clientY;maybeSendInput(false)}});
function end(){G.swipe.on=false;maybeSendInput(true)}
game.addEventListener('pointerup',end);game.addEventListener('pointercancel',end);

setName.onclick=()=>{
  const n=nameEl.value.trim();
  if(G.id&&n)postJson('/api/name',{id:G.id,name:n}).catch(()=>{});
};
nameEl.addEventListener('keydown',e=>{if(e.key==='Enter')setName.click()});
respawn.onclick=()=>{if(G.id)postJson('/api/respawn',{id:G.id}).catch(()=>{})};

G.me=()=>G.snap.players.find(p=>p.id===G.id)||null;
G.inputVector=desiredInput;
join();
})();