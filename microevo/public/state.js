(()=>{
'use strict';
const game=document.getElementById('game'),nameEl=document.getElementById('name'),setName=document.getElementById('setName'),respawn=document.getElementById('respawn'),offline=document.getElementById('offline');
const G=window.G={id:null,world:{w:8400,h:8400},snap:{players:[],mobs:[],items:[]},swipe:{on:false,sx:0,sy:0,x:0,y:0},connected:false,lastAlive:true};
function post(url,body){return fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(r=>r.json())}
async function join(){
  try{
    const resumeId=localStorage.getItem('microevo_id')||undefined;
    const r=await post('/api/join',{resumeId});
    G.id=r.id;G.world=r.world;localStorage.setItem('microevo_id',G.id);
    connectEvents();offline.style.display='none';
  }catch(e){offline.style.display='block';setTimeout(join,1500)}
}
function connectEvents(){
  if(!G.id)return;
  const es=new EventSource('/events?id='+encodeURIComponent(G.id));
  es.onopen=()=>{G.connected=true;offline.style.display='none'};
  es.onmessage=e=>{try{G.snap=JSON.parse(e.data);G.connected=true;offline.style.display='none'}catch{}};
  es.onerror=()=>{G.connected=false;offline.style.display='block'};
}
function sendInput(){
  if(!G.id)return;
  let x=0,y=0;
  if(G.swipe.on){const dx=G.swipe.x-G.swipe.sx,dy=G.swipe.y-G.swipe.sy,l=Math.hypot(dx,dy);if(l>8){x=dx/l;y=dy/l}}
  post('/api/input',{id:G.id,x,y}).catch(()=>{});
}
setInterval(sendInput,55);

game.addEventListener('pointerdown',e=>{G.swipe.on=true;G.swipe.sx=G.swipe.x=e.clientX;G.swipe.sy=G.swipe.y=e.clientY;try{game.setPointerCapture(e.pointerId)}catch{}});
game.addEventListener('pointermove',e=>{if(G.swipe.on){G.swipe.x=e.clientX;G.swipe.y=e.clientY}});
function end(){G.swipe.on=false;sendInput()}
game.addEventListener('pointerup',end);game.addEventListener('pointercancel',end);
setName.onclick=()=>{const n=nameEl.value.trim();if(G.id&&n)post('/api/name',{id:G.id,name:n}).catch(()=>{})};
nameEl.addEventListener('keydown',e=>{if(e.key==='Enter')setName.click()});
respawn.onclick=()=>{if(G.id)post('/api/respawn',{id:G.id}).catch(()=>{})};
G.me=()=>G.snap.players.find(p=>p.id===G.id)||null;
join();
})();