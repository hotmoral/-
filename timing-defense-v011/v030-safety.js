// Timing Defense v0.30 — v0.27 observer-loop guard + simple portrait block.
// No viewport width/meta rewrites. No combat/combo/balance changes.
(function(){
  const NativeMO=window.MutationObserver;
  if(NativeMO&&!window.__v030ObserverGuard){
    window.__v030ObserverGuard=true;
    function GuardedMutationObserver(callback){
      if(callback&&callback.name==='normalizeSkillLevels'){
        window.__v030ObserverGuardIntercepted=(window.__v030ObserverGuardIntercepted||0)+1;
        return new NativeMO(function(){});
      }
      return new NativeMO(callback);
    }
    GuardedMutationObserver.prototype=NativeMO.prototype;
    window.MutationObserver=GuardedMutationObserver;
  }

  const style=document.createElement('style');
  style.textContent=`
    #orientation{display:none!important}
    #v030OrientationGate{position:fixed;inset:0;z-index:2147483647;display:none;align-items:center;justify-content:center;
      padding:28px;background:#0b0f14;color:#eef4ef;text-align:center;font-family:Inter,system-ui,sans-serif;pointer-events:auto}
    .v030OrientCard{width:min(420px,86vw);padding:24px 22px;border:1px solid rgba(255,255,255,.14);border-radius:18px;
      background:rgba(25,38,33,.97);box-shadow:0 18px 60px rgba(0,0,0,.42)}
    .v030OrientIcon{width:54px;height:36px;margin:0 auto 14px;border:3px solid #f0d98c;border-radius:8px;position:relative}
    .v030OrientIcon:after{content:'';position:absolute;right:-14px;top:50%;width:8px;height:3px;border-radius:3px;background:#f0d98c;transform:translateY(-50%)}
    .v030OrientTitle{font:1000 18px system-ui;letter-spacing:.03em}.v030OrientText{margin-top:8px;font:750 11px/1.55 system-ui;color:#a9b7af}
    @media (orientation:portrait){#v030OrientationGate{display:flex!important}}
  `;
  document.head.appendChild(style);
  if(!document.getElementById('v030OrientationGate')){
    const gate=document.createElement('div');
    gate.id='v030OrientationGate';
    gate.innerHTML='<div class="v030OrientCard"><div class="v030OrientIcon"></div><div class="v030OrientTitle">가로 화면 전용</div><div class="v030OrientText">휴대폰을 가로로 돌려주세요.<br>세로 화면에서는 게임 UI를 표시하지 않습니다.</div></div>';
    document.body.appendChild(gate);
  }
})();
