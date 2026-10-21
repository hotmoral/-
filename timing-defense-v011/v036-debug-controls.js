// Timing Defense v0.36 Slice A candidate-only debug controls.
// Visible only with ?v036debug=1. Host can force a human run player to Lv5/Lv6.
(function(){
  const url=new URL(location.href);
  if(url.searchParams.get('v036debug')!=='1')return;
  const mp=window.__TDMP34CF,bridge=window.__TDCFBridge;
  if(!mp||!bridge)return;

  const style=document.createElement('style');
  style.textContent=`#v036Debug{position:fixed;right:calc(env(safe-area-inset-right) + 8px);bottom:calc(env(safe-area-inset-bottom) + 8px);z-index:150;display:flex;align-items:center;gap:5px;padding:5px 7px;border:1px solid rgba(255,255,255,.18);border-radius:9px;background:rgba(7,12,15,.90);font:800 8px system-ui;color:#dfe8e3;pointer-events:auto}#v036Debug button{padding:5px 7px;border-radius:6px;border:1px solid rgba(255,255,255,.15);background:#172621;color:#dce6e0;font:900 8px system-ui}#v036Debug button.on{background:#efe0ac;color:#17201b;border-color:#efe0ac}#v036Debug button:disabled{opacity:.35}#v036Debug .st{min-width:74px;color:#9fb0a7}`;
  document.head.appendChild(style);
  const root=document.createElement('div');root.id='v036Debug';
  root.innerHTML='<span class="st">LV TEST · WAIT</span><button data-lv="5">LV5</button><button data-lv="6">LV6</button>';
  document.body.appendChild(root);
  root.addEventListener('pointerdown',e=>e.stopPropagation());
  root.addEventListener('click',e=>e.stopPropagation());

  const status=root.querySelector('.st');
  const buttons=[...root.querySelectorAll('[data-lv]')];
  function localParticipant(st=mp.state){return st?.participants?.find(p=>p.slot===(bridge.slot||mp.slot))||null}
  function localRunPlayer(st=mp.state){return st?.run?.players?.find(p=>p.slot===(bridge.slot||mp.slot))||null}
  function render(st=mp.state,msg=''){
    const p=localParticipant(st),rp=localRunPlayer(st),host=!!p?.host,lv=rp?.level||null;
    status.textContent=msg||`${host?'HOST':'GUEST'} · ${p?.classId?.toUpperCase?.()||'WAIT'} · ${lv?`LV${lv}`:'WAIT'}`;
    for(const b of buttons){b.disabled=!host||!st?.run;b.classList.toggle('on',Number(b.dataset.lv)===lv)}
  }
  async function setLevel(level){
    const st=mp.state,session=bridge.session||mp.session;
    if(!st?.code||!session)return render(st,'WAIT · NO RUN');
    render(st,`SETTING LV${level}…`);
    try{
      const r=await fetch(`/api/room/${st.code}/debug-level`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session,level}),cache:'no-store'});
      const d=await r.json().catch(()=>null);
      if(!r.ok)throw new Error(d?.error||`HTTP ${r.status}`);
      if(d?.state)window.dispatchEvent(new CustomEvent('tdcf:state',{detail:{state:d.state,source:'v036-debug-level'}}));
      render(d?.state||mp.state,`SET · LV${level}`);
    }catch(e){render(mp.state,`ERR · ${String(e.message||e).slice(0,22)}`)}
  }
  for(const b of buttons)b.addEventListener('click',()=>setLevel(Number(b.dataset.lv)));
  window.addEventListener('tdcf:state',e=>render(e.detail?.state));
  render();
})();
