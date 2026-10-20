// Timing Defense v0.28 — landscape-only orientation guard + stale viewport repair.
// Presentation/runtime guard only. No combat, combo, or balance changes.
(function(){
  const style=document.createElement('style');
  style.textContent=`
    html,body{width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;overflow:hidden!important;background:#0b0f14!important}
    #v028OrientationGate{position:fixed;inset:0;z-index:2147483647;display:none;align-items:center;justify-content:center;padding:28px;background:#0b0f14;color:#eef4ef;text-align:center;font-family:Inter,system-ui,sans-serif;pointer-events:auto}
    #v028OrientationGate.show{display:flex!important}
    .v028OrientCard{width:min(420px,86vw);padding:24px 22px;border:1px solid rgba(255,255,255,.14);border-radius:18px;background:rgba(25,38,33,.96);box-shadow:0 18px 60px rgba(0,0,0,.40)}
    .v028OrientIcon{width:54px;height:36px;margin:0 auto 14px;border:3px solid #f0d98c;border-radius:8px;position:relative;box-shadow:0 0 22px rgba(240,217,140,.16)}
    .v028OrientIcon:after{content:'';position:absolute;right:-14px;top:50%;width:8px;height:3px;border-radius:3px;background:#f0d98c;transform:translateY(-50%)}
    .v028OrientTitle{font:1000 18px system-ui;letter-spacing:.03em}.v028OrientText{margin-top:8px;font:750 11px/1.55 system-ui;color:#a9b7af}
    .v028OrientBtn{margin-top:14px;border:1px solid rgba(255,255,255,.15);border-radius:10px;background:#efe0ac;color:#17201b;padding:9px 14px;font:950 10px system-ui;display:none}
    #v028OrientationGate.stale .v028OrientBtn{display:inline-block}
    body.v028Blocked>#v022Lobby,body.v028Blocked>#game,body.v028Blocked>#ui,body.v028Blocked>#v022EndBtns{visibility:hidden!important;pointer-events:none!important}
    @media (orientation:portrait){#v028OrientationGate{display:flex!important}}
  `;
  document.head.appendChild(style);

  let gate=document.getElementById('v028OrientationGate');
  if(!gate){
    gate=document.createElement('div');gate.id='v028OrientationGate';
    gate.innerHTML=`<div class="v028OrientCard"><div class="v028OrientIcon"></div><div id="v028OrientTitle" class="v028OrientTitle">가로 화면 전용</div><div id="v028OrientText" class="v028OrientText">휴대폰을 가로로 돌려주세요.<br>세로 화면에서는 게임 UI를 표시하지 않습니다.</div><button id="v028OrientReload" class="v028OrientBtn">가로 상태에서 새로고침</button></div>`;
    document.body.appendChild(gate)
  }
  const title=gate.querySelector('#v028OrientTitle'),text=gate.querySelector('#v028OrientText'),reload=gate.querySelector('#v028OrientReload');
  reload?.addEventListener('click',()=>location.reload());

  const viewportMeta=()=>document.querySelector('meta[name="viewport"]');
  function physicalLandscape(){
    const type=screen.orientation?.type||'';
    if(type)return type.includes('landscape');
    return Math.max(screen.width,screen.height)===screen.width
  }
  function viewportSize(){
    const vv=window.visualViewport;
    return {w:vv?.width||window.innerWidth||document.documentElement.clientWidth,h:vv?.height||window.innerHeight||document.documentElement.clientHeight}
  }
  let repairTimer=0;
  function attemptLandscapeViewportRepair(){
    const meta=viewportMeta();if(!meta)return;
    const target=Math.max(Number(screen.width)||0,Number(screen.height)||0);
    if(!target)return;
    meta.setAttribute('content',`width=${target},initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover`);
    document.documentElement.style.width='100%';document.body.style.width='100%';
    void document.documentElement.offsetWidth;
  }
  function syncOrientation(){
    clearTimeout(repairTimer);
    const {w,h}=viewportSize();
    const screenLand=physicalLandscape();
    const viewportPortrait=h>w;
    const actualPortrait=!screenLand;
    const staleLandscape=screenLand&&viewportPortrait;

    if(staleLandscape){
      attemptLandscapeViewportRepair();
      repairTimer=setTimeout(()=>{
        const v=viewportSize();
        const stillBad=v.h>v.w;
        document.body.classList.toggle('v028Blocked',stillBad);
        gate.classList.toggle('show',stillBad);
        gate.classList.toggle('stale',stillBad);
        if(stillBad){
          title.textContent='가로 화면 인식 재설정 필요';
          text.innerHTML='기기는 가로인데 브라우저가 세로 폭을 유지하고 있습니다.<br>깨진 화면 대신 차단했습니다. 가로 상태에서 새로고침해 주세요.';
        }
      },180);
      return
    }

    const blocked=actualPortrait||viewportPortrait;
    document.body.classList.toggle('v028Blocked',blocked);
    gate.classList.toggle('show',blocked);
    gate.classList.remove('stale');
    if(blocked){
      title.textContent='가로 화면 전용';
      text.innerHTML='휴대폰을 가로로 돌려주세요.<br>세로 화면에서는 게임 UI를 표시하지 않습니다.';
    }else{
      const meta=viewportMeta();
      if(meta)meta.setAttribute('content','width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover');
      for(const el of [document.getElementById('v022Lobby'),document.getElementById('game'),document.getElementById('ui')]){
        if(!el)continue;el.style.maxWidth='none';el.style.width='100vw';
      }
    }
  }

  window.addEventListener('orientationchange',()=>setTimeout(syncOrientation,120));
  window.addEventListener('resize',syncOrientation,{passive:true});
  window.visualViewport?.addEventListener('resize',syncOrientation,{passive:true});
  screen.orientation?.addEventListener?.('change',()=>setTimeout(syncOrientation,100));
  syncOrientation();
})();
