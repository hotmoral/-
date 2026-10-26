(() => {
  'use strict';
  const TD = window.TwinDock;
  const state = TD.createState();
  const ui = TD.UI.collect();
  const renderer = TD.Renderer(state, ui);
  const feedback = TD.FeedbackRenderer(state, ui);
  const effects = TD.Effects(state);
  const transitions = TD.Transitions(ui);

  if(new URLSearchParams(location.search).get('debug')==='1') document.body.classList.add('debug');

  function clearControls(){ TD.Input.clearAll(state); }
  function resetShip(){ TD.Physics.resetShip(state, clearControls); }
  function updateChecks(){ const m=TD.Docking.metrics(state); TD.UI.updateDockChecks(ui,m); }
  function progressText(){ const p=TD.Mission.progress(state); return `${Math.min(state.score,p.total)} / ${p.total}`; }
  function targetText(profile){ return `TRIAL ${state.mission.index+1} · ${profile.label}`; }
  function setupText(profile){
    const setup=TD.CraftGeometry.get(profile.setupId),craft=TD.CraftGeometry.craft(setup.craftId),port=TD.CraftGeometry.port(setup.portShape);
    return `${craft.label} · ${port.label} 포트 · ${setup.anchorLabel}`;
  }

  function resetAll(){
    state.running=false;state.startedOnce=false;state.score=0;effects.silence();transitions.reset();resetShip();
    const profile=TD.Mission.reset(state);
    ui.score.textContent=progressText();ui.rel.textContent='0.0';ui.mode.textContent='대기';
    ui.msgT.textContent=targetText(profile);ui.msgS.textContent='각 trial은 동일한 초기 위치·속도에서 시작합니다.';ui.start.textContent='시작';
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));renderer.draw();feedback.draw();
  }

  function dockSuccess(m){
    state.docked=true;state.dockHold=TD.Config.DOCK_HOLD_SECONDS;state.score++;ui.score.textContent=progressText();clearControls();transitions.progress();
    const ship=state.ship,pose=TD.Geometry.bodyPoseForWorldAnchor(m.captureX,m.captureY,m.stationAnchor.angle,ship.dockAnchor);ship.x=pose.x;ship.y=pose.y;ship.angle=pose.angle;ship.angVel=state.station.omega;ship.vx=m.captureVx;ship.vy=m.captureVy;
    ui.mode.textContent='DOCK';ui.msgT.textContent=`TRIAL ${state.mission.index+1} COMPLETE`;ui.msgS.textContent='다음 trial은 운동 상태를 이어받지 않고 동일 조건으로 재시작합니다.';ui.pulse.classList.remove('on');void ui.pulse.offsetWidth;ui.pulse.classList.add('on');effects.softCapture();
  }

  function collision(){
    const ship=state.ship,station=state.station,dx=ship.x-station.cx,dy=ship.y-station.cy,l=Math.hypot(dx,dy)||1;ship.vx+=dx/l*34;ship.vy+=dy/l*34;ship.angVel*=.6;clearControls();ui.mode.textContent='복구';ui.msgT.textContent='접촉 불량';ui.msgS.textContent='튕겨나왔습니다. 자세를 다시 잡고 재접근하세요.';state.flashTimer=.16;ui.flash.classList.add('on');effects.badContact();
  }

  function dockHoldEnd(){
    const next=TD.Mission.advance(state);
    if(!next){
      state.running=false;state.dockHold=1e9;clearControls();ui.mode.textContent='완료';ui.msgT.textContent='ANCHOR CONTROL V2 COMPLETE';ui.msgS.textContent='5개 독립 trial 완료 · 난도 순서를 비교해주세요.';ui.start.textContent='다시';effects.missionComplete();transitions.missionComplete(TD.Mission.profiles.length);return;
    }
    state.docked=false;state.dockHold=0;state.angularDrive=0;clearControls();effects.latch();effects.nextTarget();
    ui.mode.textContent='접근';ui.msgT.textContent=targetText(next);ui.msgS.textContent='동일 초기 운동 상태 · anchor 위치만 변경';
    transitions.nextTarget(next,state.mission.index+1,TD.Mission.profiles.length);
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));
  }

  function startStop(){
    effects.unlock();
    if(state.mission.finished){ resetAll(); }
    state.startedOnce=true;
    if(state.running){state.running=false;clearControls();effects.silence();ui.start.textContent='계속';ui.mode.textContent='일시정지';return;}
    state.running=true;ui.start.textContent='정지';ui.mode.textContent='접근';
    const profile=TD.Mission.current(state);ui.msgT.textContent=targetText(profile);ui.msgS.textContent=setupText(profile);state.last=performance.now();
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
  TD.App={state,ui,renderer,feedback,effects,transitions,resetAll,startStop};
})();
