// Timing Defense v0.29 — Samsung landscape viewport hard-repair.
// Removes v0.28 numeric viewport rewrites; forces real landscape canvas/lobby width when browser keeps a half-width layout viewport.
(function(){
  const meta=document.querySelector('meta[name="viewport"]');
  if(meta) meta.setAttribute('content','width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover');

  const style=document.createElement('style');
  style.textContent=`
    html,body{margin:0!important;overflow:hidden!important;background:#0b0f14!important}
    body.v029Portrait>#v022Lobby,
    body.v029Portrait>#game,
    body.v029Portrait>#ui,
    body.v029Portrait>#v022EndBtns,
    body.v029Broken>#v022Lobby,
    body.v029Broken>#game,
    body.v029Broken>#ui,
    body.v029Broken>#v022EndBtns{visibility:hidden!important;pointer-events:none!important}

    #v029Gate{position:fixed;inset:0;z-index:2147483647;display:none;align-items:center;justify-content:center;
      padding:24px;background:#0b0f14;color:#edf4ef;text-align:center;font-family:Inter,system-ui,sans-serif}
    #v029Gate.show{display:flex!important}
    .v029Card{width:min(460px,86vw);padding:22px;border:1px solid rgba(255,255,255,.14);border-radius:18px;
      background:rgba(24,38,32,.97);box-shadow:0 18px 60px rgba(0,0,0,.42)}
    .v029Title{font:1000 18px system-ui}.v029Text{margin-top:8px;font:750 11px/1.55 system-ui;color:#a8b7af}
    .v029Diag{margin-top:10px;padding:8px 10px;border-radius:9px;background:rgba(0,0,0,.25);
      font:700 8px/1.45 ui-monospace,SFMono-Regular,monospace;color:#8fa198;word-break:break-all;display:none}
    .v029Btn{margin-top:14px;border:1px solid rgba(255,255,255,.16);border-radius:10px;background:#efe0ac;color:#17201b;
      padding:9px 14px;font:950 10px system-ui}
  `;
  document.head.appendChild(style);

  let gate=document.getElementById('v029Gate');
  if(!gate){
    gate=document.createElement('div');gate.id='v029Gate';
    gate.innerHTML=`<div class="v029Card"><div id="v029Title" class="v029Title">가로 화면 전용</div>
      <div id="v029Text" class="v029Text">휴대폰을 가로로 돌려주세요.</div>
      <div id="v029Diag" class="v029Diag"></div>
      <button id="v029Reload" class="v029Btn">새로고침</button></div>`;
    document.body.appendChild(gate);
  }
  const title=gate.querySelector('#v029Title'),text=gate.querySelector('#v029Text'),
        diag=gate.querySelector('#v029Diag'),reload=gate.querySelector('#v029Reload');
  reload.onclick=()=>location.reload();

  function metrics(){
    const vv=window.visualViewport;
    const sw=Number(screen.width)||0, sh=Number(screen.height)||0;
    const ow=Number(window.outerWidth)||0, oh=Number(window.outerHeight)||0;
    const iw=Number(window.innerWidth)||0, ih=Number(window.innerHeight)||0;
    const vw=Number(vv?.width)||0, vh=Number(vv?.height)||0;
    const cw=Number(document.documentElement.clientWidth)||0, ch=Number(document.documentElement.clientHeight)||0;
    const root=document.getElementById('v022Lobby');
    const rw=root?.getBoundingClientRect().width||0, rh=root?.getBoundingClientRect().height||0;
    return {sw,sh,ow,oh,iw,ih,vw,vh,cw,ch,rw,rh,dpr:window.devicePixelRatio||1};
  }

  function isLandscape(m){
    const t=screen.orientation?.type||'';
    if(t) return t.includes('landscape');
    return Math.max(m.ow,m.iw,m.vw,m.sw,m.sh) > Math.max(m.oh,m.ih,m.vh,Math.min(m.sw,m.sh));
  }

  function targetWidth(m){
    const vals=[m.ow,m.sw,m.sh,m.iw,m.vw,m.cw].filter(v=>Number.isFinite(v)&&v>0);
    const max=Math.max(...vals), min=Math.min(...vals);
    if(max/min>3.2) return Math.max(m.iw,m.vw,m.cw);
    return max;
  }

  function forceLandscapeWidth(w){
    const px=`${Math.round(w)}px`;
    document.documentElement.style.setProperty('width',px,'important');
    document.documentElement.style.setProperty('min-width',px,'important');
    document.body.style.setProperty('width',px,'important');
    document.body.style.setProperty('min-width',px,'important');

    for(const id of ['v022Lobby','game','ui','v027Waiting']){
      const el=document.getElementById(id); if(!el) continue;
      el.style.setProperty('left','0px','important');
      el.style.setProperty('right','auto','important');
      el.style.setProperty('width',px,'important');
      el.style.setProperty('max-width','none','important');
    }
    const end=document.getElementById('v022EndBtns');
    if(end) end.style.setProperty('max-width',px,'important');

    void document.documentElement.offsetWidth;
    window.dispatchEvent(new Event('resize'));
  }

  let syncing=false, retryTimer=0;
  function sync(){
    if(syncing) return;
    syncing=true;
    clearTimeout(retryTimer);
    const m=metrics();
    const landscape=isLandscape(m);

    if(!landscape){
      document.body.classList.add('v029Portrait');
      document.body.classList.remove('v029Broken');
      gate.classList.add('show');
      title.textContent='가로 화면 전용';
      text.innerHTML='휴대폰을 가로로 돌려주세요.<br>세로 화면에서는 게임 UI를 표시하지 않습니다.';
      diag.style.display='none';
      syncing=false;
      return;
    }

    document.body.classList.remove('v029Portrait');
    gate.classList.remove('show');

    const target=targetWidth(m);
    const current=Math.max(m.rw,m.iw,m.vw,m.cw);
    if(target>0 && current<target*.82){
      forceLandscapeWidth(target);
    }else{
      document.documentElement.style.removeProperty('width');
      document.documentElement.style.removeProperty('min-width');
      document.body.style.removeProperty('width');
      document.body.style.removeProperty('min-width');
      for(const id of ['v022Lobby','game','ui','v027Waiting']){
        const el=document.getElementById(id); if(!el) continue;
        el.style.setProperty('left','0','important');
        el.style.setProperty('right','0','important');
        el.style.setProperty('width','auto','important');
        el.style.setProperty('max-width','none','important');
      }
    }

    syncing=false;
    retryTimer=setTimeout(()=>{
      const n=metrics(), t=targetWidth(n);
      const rootW=n.rw||n.iw||n.vw||n.cw;
      const stillHalf=t>0 && rootW<t*.82;
      document.body.classList.toggle('v029Broken',stillHalf);
      gate.classList.toggle('show',stillHalf);
      if(stillHalf){
        title.textContent='가로 화면 폭 복구 필요';
        text.innerHTML='브라우저가 게임 영역을 실제 화면보다 좁게 유지하고 있습니다.<br>깨진 화면은 차단했습니다. 아래 값을 기준으로 다음 복구를 적용합니다.';
        diag.style.display='block';
        diag.textContent=`screen ${n.sw}×${n.sh} | outer ${n.ow}×${n.oh} | inner ${n.iw}×${n.ih} | visual ${n.vw}×${n.vh} | client ${n.cw}×${n.ch} | lobby ${Math.round(n.rw)}×${Math.round(n.rh)} | dpr ${n.dpr}`;
      }else{
        document.body.classList.remove('v029Broken');
        gate.classList.remove('show');
        diag.style.display='none';
      }
    },260);
  }

  window.addEventListener('resize',()=>setTimeout(sync,30),{passive:true});
  window.addEventListener('orientationchange',()=>setTimeout(sync,160));
  window.visualViewport?.addEventListener('resize',()=>setTimeout(sync,30),{passive:true});
  screen.orientation?.addEventListener?.('change',()=>setTimeout(sync,120));

  sync();
  setTimeout(sync,120);
  setTimeout(sync,420);
  setTimeout(sync,900);
})();
