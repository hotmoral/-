(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;

  const CONTROL = Object.freeze({ ahead:0.49, lateral:-0.10, bodyVx:4, bodyVy:-5, omega:-0.14 });
  const profiles = Object.freeze([
    Object.freeze({ id:'SIDE_TOP', label:'LONG CARGO · 상단 측면 · r61', setupId:'CARGO_CTRL_SIDE_TOP', ...CONTROL }),
    Object.freeze({ id:'FRONT', label:'LONG CARGO · 전방 · r98', setupId:'CARGO_CTRL_FRONT', ...CONTROL }),
    Object.freeze({ id:'SIDE_BOTTOM', label:'LONG CARGO · 하단 측면 · r61', setupId:'CARGO_CTRL_SIDE_BOTTOM', ...CONTROL }),
    Object.freeze({ id:'REAR', label:'LONG CARGO · 후방 · r98', setupId:'CARGO_CTRL_REAR', ...CONTROL }),
    Object.freeze({ id:'CORNER', label:'LONG CARGO · 우하단 모서리 · r98', setupId:'CARGO_CTRL_CORNER', ...CONTROL })
  ]);

  function current(state){ return profiles[state.mission.index] || profiles[profiles.length-1]; }

  function placeCurrent(state){
    const profile=current(state), ship=state.ship, station=state.station;
    TD.CraftGeometry.apply(ship,profile.setupId);
    const W=state.viewport.W, H=state.viewport.H;
    const c=Math.cos(ship.angle), s=Math.sin(ship.angle);
    const forwardX=c, forwardY=s, rightX=-s, rightY=c;
    const ahead=Math.max(320, Math.min(540, W*profile.ahead));
    const lateral=H*profile.lateral;
    station.cx=ship.x + forwardX*ahead + rightX*lateral;
    station.cy=ship.y + forwardY*ahead + rightY*lateral;
    station.angle=normAngle(ship.angle + ship.dockAnchor.angle + Math.PI);
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
    control: CONTROL,
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
