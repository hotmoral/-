(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;
  TD.Docking = {
    portState(state, stationAnchor = TD.Geometry.stationDockAnchor(state)) {
      const C = TD.Config, s = state.station;
      const tx = Math.cos(stationAnchor.angle), ty = Math.sin(stationAnchor.angle);
      const px = stationAnchor.x - tx * C.PORT_CAPTURE_INSET;
      const py = stationAnchor.y - ty * C.PORT_CAPTURE_INSET;
      const rx = px - s.cx, ry = py - s.cy;
      return {
        ux: -tx,
        uy: -ty,
        px,
        py,
        pvx: s.vx - s.omega * ry,
        pvy: s.vy + s.omega * rx,
        targetAngle: stationAnchor.angle
      };
    },
    metrics(state) {
      const ship = state.ship, station = state.station;
      const shipAnchor = TD.Geometry.shipDockAnchor(state);
      const stationAnchor = TD.Geometry.stationDockAnchor(state);
      const p = this.portState(state, stationAnchor);
      const rvx = ship.vx - stationAnchor.vx, rvy = ship.vy - stationAnchor.vy;
      return {
        p,
        shipAnchor,
        stationAnchor,
        probeX: shipAnchor.x,
        probeY: shipAnchor.y,
        captureX: stationAnchor.x,
        captureY: stationAnchor.y,
        captureVx: stationAnchor.vx,
        captureVy: stationAnchor.vy,
        rvx,
        rvy,
        dist: Math.hypot(shipAnchor.x - stationAnchor.x, shipAnchor.y - stationAnchor.y),
        rel: Math.hypot(rvx, rvy),
        dir: Math.abs(normAngle(shipAnchor.angle - stationAnchor.angle)),
        spin: Math.abs(ship.angVel - station.omega)
      };
    },
    checks(metrics) {
      const L = TD.Config.DOCK_LIMIT;
      return { pos: metrics.dist < L.dist, vel: metrics.rel < L.rel, dir: metrics.dir < L.dir, spin: metrics.spin < L.spin };
    },
    canDock(metrics) {
      const c = this.checks(metrics);
      return c.pos && c.vel && c.dir && c.spin;
    }
  };
})();
