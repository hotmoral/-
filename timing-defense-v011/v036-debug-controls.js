// Timing Defense v0.36 Slice A candidate-only debug controls.
// Visible only with ?v036debug=1. Always targets the real local human captured from the primary welcome.
(function(){
  const url=new URL(location.href);
  if(url.searchParams.get('v036debug')!=='1')return;
  const mp=window.__TDMP34CF,bridge=window.__TDCFBridge;
  if(!mp||!bridge)return;

  const local={session:bridge.session||'',slot:Number(bridge.slot)||0};
  const style=document.createElement('style');
  style.textContent=`#v036Debug{position:fixed;right:calc(env(safe-area-inset-right) + 6px);top:50%;transform:translateY(-50%);z-index:150;display:none;flex-direction:column;align-items:center;gap:4px;padding:5px;border:1px solid rgba(255,255,255,.16);border-radius:9px;background:rgba(7,12,15,.86);font:800 7px system-ui;color:#dfe8e3;pointer-events:auto}#v036Debug button{min-width:38px;padding:5px 4px;border-radius:6px;border:1px solid rgba(255,255,255,.15);background:#172621;color:#dce6e0;font:900 8px system-ui}#v036Debug button.on{background:#efe0ac;color:#17201b;border-color:#efe0ac}#v036Debug button:disabled{opacity:.35}#v036Debug .st{max-width:46px;text-align:center;line-height:1.15;color:#9fb0a7}`;
  document.head.appendChild(style);
  const root=document.createElement('div');root.id='v036Debug';
  root.innerHTML='<span class="st">LV TEST</span><button data-lv="5">LV5</button><button data-lv="6">LV6</button>';
  document.body.appendChild(root);
  root.addEventListener('pointerdown',e=>e.stopPropagation());
  root.addEventListener('click',e=>e.stopPropagation());

  const status=root.querySelector('.st');
  const buttons=[...root.querySelectorAll('[data-lv]')];
  function capturePrimary(detail){
    if(detail?.socket&&bridge.socket&&detail.socket!==bridge.socket)return;
    if(detail?.session)local.session=detail.session;
    if(Number.isInteger(detail?.slot))local.slot=detail.slot;
  }
  function localParticipant(st=mp.state){return st?.participants?.find(p=>p.slot===local.slot)||null}
  function localRunPlayer(st=mp.state){return st?.run?.players?.find(p=>p.slot===local.slot)||null}
  function visibleFor(st){return ['starting','intro','stage-starting','combat'].includes(st?.run?.status||'')}
  function render(st=mp.state,msg=''){
    root.style.display=visibleFor(st)?'flex':'none';
    const p=localParticipant(st),rp=localRunPlayer(st),host=!!p?.host,lv=rp?.level||null;
    status.textContent=msg||`${p?.classId?.toUpperCase?.()||'LOCAL'}${lv?`\nLV${lv}`:''}`;
    for(const b of buttons){b.disabled=!host||!st?.run||!local.session||!local.slot;b.classList.toggle('on',Number(b.dataset.lv)===lv)}
  }
  async function setLevel(level){
    const st=mp.state;
    if(!st?.code||!local.session||!local.slot)return render(st,'WAIT');
    render(st,`SET LV${level}`);
    try{
      const r=await fetch(`/api/room/${st.code}/debug-level`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:local.session,slot:local.slot,level}),cache:'no-store'});
      const d=await r.json().catch(()=>null);
      if(!r.ok)throw new Error(d?.error||`HTTP ${r.status}`);
      if(d?.state)window.dispatchEvent(new CustomEvent('tdcf:state',{detail:{state:d.state,source:'v036-debug-level'}}));
      render(d?.state||mp.state,`LOCAL\nLV${level}`);
    }catch(e){render(mp.state,'ERR')}
  }
  for(const b of buttons)b.addEventListener('click',()=>setLevel(Number(b.dataset.lv)));
  window.addEventListener('tdcf:welcome',e=>{capturePrimary(e.detail);render(e.detail?.state)});
  window.addEventListener('tdcf:state',e=>render(e.detail?.state));
  render();
})();
