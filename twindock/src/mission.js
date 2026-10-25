(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;

  const profiles = Object.freeze([
    Object.freeze({ id:'STATIC', label:'정지 포트', ahead:0.45, lateral:0.00, bodyVx:0, bodyVy:0, omega:0.00 }),
    Object.freeze({ id:'TRANSLATE', label:'이동 포트', ahead:0.47, lateral:-0.11, bodyVx:5, bodyVy:6, omega:0.00 }),
    Object.freeze({ id:'ROTATE', label:'회전 포트', ahead:0.46, lateral:0.12, bodyVx:0, bodyVy:0, omega:0.12 }),
    Object.freeze({ id:'COMBINED', label:'이동 + 회전', ahead:0.49, lateral:-0.13, bodyVx:4, bodyVy:-5, omega:-0.14 }),
    Object.freeze({ id:'FINAL', label:'최종 정밀 도킹', ahead:0.52, lateral:0.10, bodyVx:5, bodyVy:6, omega:0.18 })
  ]);

  function current(state){ return profiles[state.mission.index] || profiles[profiles.length-1]; }

  function placeCurrent(state){
    const profile=current(state), ship=state.ship, station=state.station;
    const W=state.viewport.W, H=state.viewport.H;
    const c=Math.cos(ship.angle), s=Math.sin(ship.angle);
    const forwardX=c, forwardY=s, rightX=-s, rightY=c;
    const ahead=Math.max(320, Math.min(540, W*profile.ahead));
    const lateral=H*profile.lateral;
    station.cx=ship.x + forwardX*ahead + rightX*lateral;
    station.cy=ship.y + forwardY*ahead + rightY*lateral;
    station.angle=normAngle(ship.angle + Math.PI);
    station.omega=profile.omega;
    station.vx=c*profile.bodyVx - s*profile.bodyVy;
    station.vy=s*profile.bodyVx + c*profile.bodyVy;
    station.radius=Math.min(W,H)*0.12;
    station.ringR=station.radius*1.42;
    station.dockAnchor.x=station.radius-TD.Config.PORT_CAPTURE_INSET;
    station.dockAnchor.y=0;
    station.dockAnchor.angle=Math.PI;
    station.dockAnchor.tracksRadius=true;
    return profile;
  }

  TD.Mission = Object.freeze({
    profiles,
    current,
    reset(state){ state.mission.index=0; state.mission.finished=false; return placeCurrent(state); },
    placeCurrent,
    advance(state){
      if(state.mission.index >= profiles.length-1){ state.mission.finished=true; return null; }
      state.mission.index += 1;
      return placeCurrent(state);
    },
    progress(state){ return { current: state.mission.index+1, total: profiles.length, finished: state.mission.finished }; }
  });
})();
