(() => {
  'use strict';
  const TD = window.TwinDock;
  const state = TD.createState();
  const ui = TD.UI.collect();
  const renderer = TD.Renderer(state, ui);
  const feedback = TD.FeedbackRenderer(state, ui);
  const effects = TD.Effects(state);

  if(new URLSearchParams(location.search).get('debug')==='1') document.body.classList.add('debug');

  function clearControls(){ TD.Input.clearAll(state); }
  function resetShip(){ TD.Physics.resetShip(state, clearControls); }
  function updateChecks(){ const m=TD.Docking.metrics(state); TD.UI.updateDockChecks(ui,m); }
  function progressText(){ const p=TD.Mission.progress(state); return `${Math.min(state.score,p.total)} / ${p.total}`; }
  function targetText(profile){ return `TARGET ${state.mission.index+1} · ${profile.label}`; }

  function resetAll(){
    state.running=false;state.startedOnce=false;state.score=0;effects.silence();resetShip();
    const profile=TD.Mission.reset(state);
    ui.score.textContent=progressText();ui.rel.textContent='0.0';ui.mode.textContent='대기';
    ui.msgT.textContent=targetText(profile);ui.msgS.textContent='도킹 링과 상대 운동을 읽고 접근하세요.';ui.start.textContent='시작';
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));renderer.draw();
  }

  function dockSuccess(m){
    state.docked=true;state.dockHold=TD.Config.DOCK_HOLD_SECONDS;state.score++;ui.score.textContent=progressText();clearControls();
    const ship=state.ship;ship.angle=m.p.targetAngle;ship.angVel=state.station.omega;const fx=Math.cos(ship.angle),fy=Math.sin(ship.angle);ship.x=m.captureX-fx*TD.Config.VISUAL_PROBE_X;ship.y=m.captureY-fy*TD.Config.VISUAL_PROBE_X;ship.vx=m.captureVx;ship.vy=m.captureVy;
    ui.mode.textContent='DOCK';ui.msgT.textContent=`DOCK ${state.mission.index+1} COMPLETE`;ui.msgS.textContent='SOFT CAPTURE · 다음 목표로 이어집니다.';ui.pulse.classList.remove('on');void ui.pulse.offsetWidth;ui.pulse.classList.add('on');effects.softCapture();
  }

  function collision(){
    const ship=state.ship,station=state.station,dx=ship.x-station.cx,dy=ship.y-station.cy,l=Math.hypot(dx,dy)||1;ship.vx+=dx/l*34;ship.vy+=dy/l*34;ship.angVel*=.6;clearControls();ui.mode.textContent='복구';ui.msgT.textContent='접촉 불량';ui.msgS.textContent='튕겨나왔습니다. 자세를 다시 잡고 재접근하세요.';state.flashTimer=.16;ui.flash.classList.add('on');effects.badContact();
  }

  function dockHoldEnd(){
    const next=TD.Mission.advance(state);effects.latch();
    if(!next){
      state.running=false;state.dockHold=1e9;clearControls();ui.mode.textContent='완료';ui.msgT.textContent='MISSION 01 COMPLETE';ui.msgS.textContent='5 DOCKS COMPLETE · 다시 시작할 수 있습니다.';ui.start.textContent='다시';effects.missionComplete();return;
    }
    state.docked=false;state.dockHold=0;state.angularDrive=0;clearControls();effects.nextTarget();
    ui.mode.textContent='접근';ui.msgT.textContent=targetText(next);ui.msgS.textContent='새 목표의 움직임을 먼저 읽으세요.';
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));
  }

  function startStop(){
    effects.unlock();
    if(state.mission.finished){ resetAll(); }
    state.startedOnce=true;
    if(state.running){state.running=false;clearControls();effects.silence();ui.start.textContent='계속';ui.mode.textContent='일시정지';return;}
    state.running=true;ui.start.textContent='정지';ui.mode.textContent='접근';
    const profile=TD.Mission.current(state);ui.msgT.textContent=targetText(profile);ui.msgS.textContent='가이드 링과 포트의 움직임을 보고 동기화하세요.';state.last=performance.now();
  }

  ui.start.addEventListener('click',startStop);
  ui.reset.addEventListener('click',resetAll);
  ui.full.addEventListener('click',async()=>{try{if(!document.fullscreenElement)await ui.app.requestFullscreen({navigationUI:'hide'});else await document.exitFullscreen();}catch(_){ui.msgT.textContent='브라우저에서 전체화면을 허용해주세요';}});
  TD.Input.bind(state,ui);

  function resize(){ renderer.resize(); feedback.resize(); if(!state.startedOnce){ resetShip(); TD.Mission.placeCurrent(state); } renderer.makeStars(); renderer.draw(); feedback.draw(); }
  function loop(now){
    const dt=Math.min(.033,Math.max(.001,(now-state.last)/1000));state.last=now;
    TD.Physics.update(state,dt,{onDock:dockSuccess,onCollision:collision,onDockHoldEnd:dockHoldEnd});effects.update();
    if(!state.docked && state.running) updateChecks();
    if(state.flashTimer>0){state.flashTimer-=dt;if(state.flashTimer<=0)ui.flash.classList.remove('on');}
    renderer.draw();feedback.draw();requestAnimationFrame(loop);
  }

  window.addEventListener('resize',resize);window.addEventListener('orientationchange',()=>setTimeout(resize,120));
  renderer.resize();feedback.resize();resetAll();renderer.makeStars();state.last=performance.now();requestAnimationFrame(loop);
  TD.App={state,ui,renderer,feedback,effects,resetAll,startStop};
})();
