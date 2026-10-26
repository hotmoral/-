(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;

  const CONTROL = Object.freeze({
    targetAhead: 0.42,
    targetLateral: -0.10,
    captureBodyVx: 4,
    captureBodyVy: -5,
    omega: -0.14
  });

  const profiles = Object.freeze([
    Object.freeze({ id:'SIDE_TOP', label:'LONG CARGO · 상단 측면 · r61', setupId:'CARGO_CTRL_SIDE_TOP', ...CONTROL }),
    Object.freeze({ id:'FRONT', label:'LONG CARGO · 전방 · r98', setupId:'CARGO_CTRL_FRONT', ...CONTROL }),
    Object.freeze({ id:'SIDE_BOTTOM', label:'LONG CARGO · 하단 측면 · r61', setupId:'CARGO_CTRL_SIDE_BOTTOM', ...CONTROL }),
    Object.freeze({ id:'REAR', label:'LONG CARGO · 후방 · r98', setupId:'CARGO_CTRL_REAR', ...CONTROL }),
    Object.freeze({ id:'CORNER', label:'LONG CARGO · 우하단 모서리 · r98', setupId:'CARGO_CTRL_CORNER', ...CONTROL })
  ]);

  function current(state){ return profiles[state.mission.index] || profiles[profiles.length-1]; }

  function resetTrialShip(state){
    const { W, H } = state.viewport, ship = state.ship;
    ship.x = W * 0.14;
    ship.y = H * 0.46;
    ship.vx = 0;
    ship.vy = 0;
    ship.angle = 0;
    ship.angVel = 0;
    state.angularDrive = 0;
  }

  function placeCurrent(state){
    const profile=current(state), ship=state.ship, station=state.station;
    resetTrialShip(state);
    TD.CraftGeometry.apply(ship,profile.setupId);

    const W=state.viewport.W, H=state.viewport.H;
    station.radius=Math.min(W,H)*0.12;
    station.ringR=station.radius*1.42;
    station.dockAnchor.x=station.radius-TD.Config.PORT_CAPTURE_INSET;
    station.dockAnchor.y=0;
    station.dockAnchor.angle=Math.PI;
    station.dockAnchor.tracksRadius=true;

    const c=Math.cos(ship.angle), s=Math.sin(ship.angle);
    const forwardX=c, forwardY=s, rightX=-s, rightY=c;
    const ahead=Math.max(300,Math.min(470,W*profile.targetAhead));
    const lateral=H*profile.targetLateral;
    const playerAnchor=TD.Geometry.shipDockAnchor(state);

    const captureX=playerAnchor.x + forwardX*ahead + rightX*lateral;
    const captureY=playerAnchor.y + forwardY*ahead + rightY*lateral;
    const captureAngle=normAngle(ship.angle + ship.dockAnchor.angle);

    station.angle=normAngle(captureAngle - Math.PI);
    station.omega=profile.omega;

    const localX=station.radius-TD.Config.PORT_CAPTURE_INSET;
    const cs=Math.cos(station.angle), ss=Math.sin(station.angle);
    const rx=cs*localX, ry=ss*localX;
    station.cx=captureX-rx;
    station.cy=captureY-ry;

    const captureVx=c*profile.captureBodyVx - s*profile.captureBodyVy;
    const captureVy=s*profile.captureBodyVx + c*profile.captureBodyVy;
    station.vx=captureVx + station.omega*ry;
    station.vy=captureVy - station.omega*rx;

    return profile;
  }

  TD.Mission = Object.freeze({
    profiles,
    control: CONTROL,
    current,
    resetTrialShip,
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
