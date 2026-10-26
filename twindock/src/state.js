(() => {
  'use strict';
  const TD = window.TwinDock;
  TD.createState = function createState() {
    const C = TD.Config;
    return {
      viewport: { W: 1280, H: 720, DPR: 1 },
      running: false,
      startedOnce: false,
      score: 0,
      docked: false,
      dockHold: 0,
      flashTimer: 0,
      angularDrive: 0,
      last: performance.now(),
      stars: [],
      starFieldReady: false,
      station: {
        cx: 0, cy: 0, vx: 0, vy: 0, angle: Math.PI, omega: C.STATION_OMEGA, radius: 98, ringR: 138,
        dockAnchor: { x: 98 - C.PORT_CAPTURE_INSET, y: 0, angle: Math.PI, tracksRadius: true }
      },
      mission: { index: 0, finished: false },
      ship: {
        x: 0, y: 0, vx: 0, vy: 0, angle: 0, angVel: 0, length: C.SHIP_LENGTH, width: C.SHIP_WIDTH,
        geometryId: 'REFERENCE', craftId:'SHUTTLE', visualKind:'SHUTTLE', visualLength:84, visualWidth:46, portShape:'CIRCLE', anchorClass:'FRONT',
        dockAnchor: { x: C.VISUAL_PROBE_X, y: 0, angle: 0 }
      },
      input: {
        left: { x: 0, y: 0, held: false, pid: null, sx: 0, sy: 0 },
        right: { x: 0, y: 0, held: false, pid: null, sx: 0, sy: 0 }
      }
    };
  };
})();
