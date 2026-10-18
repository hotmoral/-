(()=>{
'use strict';

const NativeEventSource=window.EventSource;
let lastAlive=null;
let respawning=false;

function deadLayer(){return document.getElementById('dead')}
function respawnButton(){return document.getElementById('respawn')}
function setButtonBusy(busy){
  const b=respawnButton();
  if(!b)return;
  b.disabled=busy;
  b.textContent=busy?'복귀 중…':'다시 태어나기';
}
function applyAliveState(alive){
  const d=deadLayer();
  if(!d)return;
  d.classList.toggle('show',!alive);
  if(alive){
    respawning=false;
    setButtonBusy(false);
  }
  lastAlive=alive;
}

function HookedEventSource(url,options){
  const es=new NativeEventSource(url,options);
  es.addEventListener('message',ev=>{
    try{
      const s=JSON.parse(ev.data);
      const id=localStorage.getItem('microevo_id');
      if(!id||!Array.isArray(s.players))return;
      const me=s.players.find(p=>p.id===id);
      if(!me)return;
      applyAliveState(!!me.alive);
    }catch{}
  });
  return es;
}
HookedEventSource.prototype=NativeEventSource.prototype;
for(const k of ['CONNECTING','OPEN','CLOSED']){
  try{Object.defineProperty(HookedEventSource,k,{value:NativeEventSource[k]})}catch{}
}
window.EventSource=HookedEventSource;

window.addEventListener('load',()=>{
  const b=respawnButton();
  if(!b)return;
  b.addEventListener('click',async ev=>{
    ev.preventDefault();
    ev.stopImmediatePropagation();
    if(respawning)return;
    const id=localStorage.getItem('microevo_id');
    if(!id){location.replace('/?v=12&new=1');return}
    respawning=true;
    setButtonBusy(true);
    try{
      const r=await fetch('/api/respawn',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({id}),
        cache:'no-store'
      });
      if(r.status===404){
        localStorage.removeItem('microevo_id');
        location.replace('/?v=12&new=1');
        return;
      }
      if(!r.ok)throw new Error('respawn failed');
      applyAliveState(true);
      setTimeout(()=>location.replace('/?v=12&r='+Date.now()),120);
    }catch{
      respawning=false;
      setButtonBusy(false);
    }
  },true);
});
})();
