(() => {
  'use strict';
  const TD = window.TwinDock;
  const state = TD.createState();
  const ui = TD.UI.collect();
  const renderer = TD.Renderer(state, ui);
  const feedback = TD.FeedbackRenderer(state, ui);
  const effects = TD.Effects(state);
  const transitions = TD.Transitions(ui);

  const CRAFT_PROBES = Object.freeze({
    REFERENCE: Object.freeze({ id:'REFERENCE', label:'기준', x:TD.Config.VISUAL_PROBE_X, y:0, angle:0 }),
    SIDE: Object.freeze({ id:'SIDE', label:'측면', x:2, y:-31, angle:-Math.PI/2 })
  });

  if(new URLSearchParams(location.search).get('debug')==='1') document.body.classList.add('debug');

  function clearControls(){ TD.Input.clearAll(state); }
  function resetShip(){ TD.Physics.resetShip(state, clearControls); }
  function updateChecks(){ const m=TD.Docking.metrics(state); TD.UI.updateDockChecks(ui,m); }
  function progressText(){ const p=TD.Mission.progress(state); return `${Math.min(state.score,p.total)} / ${p.total}`; }
  function targetText(profile){ return `TARGET ${state.mission.index+1} · ${profile.label}`; }
  function currentCraft(){ return CRAFT_PROBES[state.ship.geometryId] || CRAFT_PROBES.REFERENCE; }
  function syncCraftButton(){ const c=currentCraft();ui.craft.textContent=`기체 · ${c.label}`;ui.craft.setAttribute('aria-pressed',String(c.id==='SIDE')); }
  function applyCraft(id){
    const c=CRAFT_PROBES[id] || CRAFT_PROBES.REFERENCE;
    state.ship.geometryId=c.id;state.ship.dockAnchor.x=c.x;state.ship.dockAnchor.y=c.y;state.ship.dockAnchor.angle=c.angle;
  }

  function resetAll(){
    state.running=false;state.startedOnce=false;state.score=0;effects.silence();transitions.reset();resetShip();
    const profile=TD.Mission.reset(state);
    ui.score.textContent=progressText();ui.rel.textContent='0.0';ui.mode.textContent='대기';
    ui.msgT.textContent=targetText(profile);ui.msgS.textContent=state.ship.geometryId==='SIDE'?'상단 측면 포트를 도킹 링에 맞추세요. 기체 자세가 기준형과 달라집니다.':'도킹 링과 상대 운동을 읽고 접근하세요.';ui.start.textContent='시작';syncCraftButton();
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));renderer.draw();feedback.draw();
  }

  function dockSuccess(m){
    state.docked=true;state.dockHold=TD.Config.DOCK_HOLD_SECONDS;state.score++;ui.score.textContent=progressText();clearControls();transitions.progress();
    const ship=state.ship,pose=TD.Geometry.bodyPoseForWorldAnchor(m.captureX,m.captureY,m.stationAnchor.angle,ship.dockAnchor);ship.x=pose.x;ship.y=pose.y;ship.angle=pose.angle;ship.angVel=state.station.omega;ship.vx=m.captureVx;ship.vy=m.captureVy;
    ui.mode.textContent='DOCK';ui.msgT.textContent=`DOCK ${state.mission.index+1} COMPLETE`;ui.msgS.textContent='SOFT CAPTURE · 다음 목표로 이어집니다.';ui.pulse.classList.remove('on');void ui.pulse.offsetWidth;ui.pulse.classList.add('on');effects.softCapture();
  }

  function collision(){
    const ship=state.ship,station=state.station,dx=ship.x-station.cx,dy=ship.y-station.cy,l=Math.hypot(dx,dy)||1;ship.vx+=dx/l*34;ship.vy+=dy/l*34;ship.angVel*=.6;clearControls();ui.mode.textContent='복구';ui.msgT.textContent='접촉 불량';ui.msgS.textContent='튕겨나왔습니다. 자세를 다시 잡고 재접근하세요.';state.flashTimer=.16;ui.flash.classList.add('on');effects.badContact();
  }

  function dockHoldEnd(){
    const next=TD.Mission.advance(state);
    if(!next){
      state.running=false;state.dockHold=1e9;clearControls();ui.mode.textContent='완료';ui.msgT.textContent='MISSION 01 COMPLETE';ui.msgS.textContent='5 DOCKS COMPLETE · 다시 시작할 수 있습니다.';ui.start.textContent='다시';effects.missionComplete();transitions.missionComplete(TD.Mission.profiles.length);return;
    }
    state.docked=false;state.dockHold=0;state.angularDrive=0;clearControls();effects.latch();effects.nextTarget();
    ui.mode.textContent='접근';ui.msgT.textContent=targetText(next);ui.msgS.textContent='새 목표의 움직임을 먼저 읽으세요.';
    transitions.nextTarget(next,state.mission.index+1,TD.Mission.profiles.length);
    [ui.ckPos,ui.ckVel,ui.ckDir,ui.ckSpin].forEach(x=>TD.UI.setCheck(x,false));
  }

  function startStop(){
    effects.unlock();
    if(state.mission.finished){ resetAll(); }
    state.startedOnce=true;
    if(state.running){state.running=false;clearControls();effects.silence();ui.start.textContent='계속';ui.mode.textContent='일시정지';return;}
    state.running=true;ui.start.textContent='정지';ui.mode.textContent='접근';
    const profile=TD.Mission.current(state);ui.msgT.textContent=targetText(profile);ui.msgS.textContent=state.ship.geometryId==='SIDE'?'측면 포트와 목표 포트의 방향·상대운동을 함께 맞추세요.':'가이드 링과 포트의 움직임을 보고 동기화하세요.';state.last=performance.now();
  }

  function toggleCraft(){
    applyCraft(state.ship.geometryId==='SIDE'?'REFERENCE':'SIDE');
    resetAll();
  }

  ui.start.addEventListener('click',startStop);
  ui.reset.addEventListener('click',resetAll);
  ui.craft.addEventListener('click',toggleCraft);
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
  renderer.resize();feedback.resize();applyCraft('REFERENCE');resetAll();renderer.makeStars();state.last=performance.now();requestAnimationFrame(loop);
  TD.App={state,ui,renderer,feedback,effects,transitions,resetAll,startStop,toggleCraft,applyCraft};
})();
