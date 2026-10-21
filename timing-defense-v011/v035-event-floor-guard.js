// Timing Defense Cloudflare v0.35 — reconnect event-floor guard.
// v0.34 beginRun resets lastEvent for a fresh run; during reload recovery this guard
// prevents that reset from dropping below the last event already seen in this room.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  let activeRoom='',floor=0,current=Number(mp.lastEvent)||0;
  const room=()=>((new URL(location.href)).searchParams.get('room')||'').toUpperCase();
  const key=r=>`td-cf035-event-floor-${r}`;
  function load(){
    const r=room();
    if(!r)return;
    if(r!==activeRoom){
      activeRoom=r;
      const saved=Number(localStorage.getItem(key(r)))||0;
      floor=Math.max(0,saved);
      current=Math.max(current,floor);
    }
  }
  function save(){
    load();
    if(!activeRoom||!mp.state?.run)return;
    floor=Math.max(floor,current);
    try{localStorage.setItem(key(activeRoom),String(floor))}catch(_){}
  }

  load();
  try{
    Object.defineProperty(mp,'lastEvent',{
      configurable:true,
      enumerable:true,
      get(){return current},
      set(v){load();current=Math.max(Number(v)||0,floor)}
    });
  }catch(_){return}

  window.addEventListener('tdcf:welcome',save);
  window.addEventListener('tdcf:state',save);
})();
