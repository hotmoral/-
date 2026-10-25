(() => {
  'use strict';
  const TD = window.TwinDock;
  const state = TD.createState();
  const ui = TD.UI.collect();
  const renderer = TD.Renderer(state, ui);

  function clearControls(){ TD.Input.clearAll(state); }
  function resetShip(){ TD.Physics.resetShip(state, clearControls); }
  function updateChecks(){ const m=TD.Docking.metrics(state); TD.UI.updateDockChecks(ui,m); }

  function resetAll(){
    state.running=false;state.startedOnce=false;state.score=0;state.station.angle=Math.PI;resetShip();
    ui.score.textContent='0';ui.rel.textContent='0.0';ui.mode.textContent='대기';ui.msgT.textContent='우주선 기준 시점 · 자유회전';ui.msgS.textContent='배경은 고정된 하나의 우주 공간을 유지하고, 도킹 판정은 정밀 모드입니다.';ui.start.textContent='시작';
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));renderer.draw();
  }

  function dockSuccess(m){
    state.docked=true;state.dockHold=TD.Config.DOCK_HOLD_SECONDS;state.score++;ui.score.textContent=state.score;clearControls();
    const ship=state.ship;ship.angle=m.p.targetAngle;ship.angVel=state.station.omega;const fx=Math.cos(ship.angle),fy=Math.sin(ship.angle);ship.x=m.captureX-fx*TD.Config.VISUAL_PROBE_X;ship.y=m.captureY-fy*TD.Config.VISUAL_PROBE_X;ship.vx=m.captureVx;ship.vy=m.captureVy;
    ui.mode.textContent='DOCK';ui.msgT.textContent='도킹 완료';ui.msgS.textContent='SOFT CAPTURE · 래치 결합 · RCS 정지';ui.pulse.classList.remove('on');void ui.pulse.offsetWidth;ui.pulse.classList.add('on');TD.UI.vibrate([18,35,35]);
  }

  function collision(){
    const ship=state.ship,station=state.station,dx=ship.x-station.cx,dy=ship.y-station.cy,l=Math.hypot(dx,dy)||1;ship.vx+=dx/l*34;ship.vy+=dy/l*34;ship.angVel*=.6;clearControls();ui.mode.textContent='복구';ui.msgT.textContent='접촉 불량';ui.msgS.textContent='운동 상태를 다시 맞추세요.';state.flashTimer=.16;ui.flash.classList.add('on');TD.UI.vibrate(25);
  }

  function respawn(){ resetShip(); ui.mode.textContent='접근';ui.msgT.textContent='다음 도킹 포트';ui.msgS.textContent='배경과 정거장 운동은 끊기지 않고 그대로 이어집니다.'; }

  function startStop(){
    state.startedOnce=true;
    if(state.running){state.running=false;clearControls();ui.start.textContent='계속';ui.mode.textContent='일시정지';return;}
    state.running=true;ui.start.textContent='정지';ui.mode.textContent='접근';ui.msgT.textContent='주변의 상대운동을 읽으세요';ui.msgS.textContent='같은 배경 안에서 정거장 상대운동을 읽고 정밀하게 맞추세요.';state.last=performance.now();
  }

  ui.start.addEventListener('click',startStop);
  ui.reset.addEventListener('click',resetAll);
  ui.full.addEventListener('click',async()=>{try{if(!document.fullscreenElement)await ui.app.requestFullscreen({navigationUI:'hide'});else await document.exitFullscreen();}catch(_){ui.msgT.textContent='브라우저에서 전체화면을 허용해주세요';}});
  TD.Input.bind(state,ui);

  function resize(){ renderer.resize(); if(!state.startedOnce) resetShip(); renderer.makeStars(); renderer.draw(); }
  function loop(now){
    const dt=Math.min(.033,Math.max(.001,(now-state.last)/1000));state.last=now;
    TD.Physics.update(state,dt,{onDock:dockSuccess,onCollision:collision,onDockHoldEnd:respawn});
    if(!state.docked && state.running) updateChecks();
    if(state.flashTimer>0){state.flashTimer-=dt;if(state.flashTimer<=0)ui.flash.classList.remove('on');}
    renderer.draw();requestAnimationFrame(loop);
  }

  window.addEventListener('resize',resize);window.addEventListener('orientationchange',()=>setTimeout(resize,120));
  resize();resetAll();state.last=performance.now();requestAnimationFrame(loop);
  TD.App={state,ui,renderer,resetAll,startStop};
})();
