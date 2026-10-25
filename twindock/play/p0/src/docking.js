(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;
  TD.Docking = {
    portState(state) {
      const s = state.station;
      const ux = Math.cos(s.angle), uy = Math.sin(s.angle);
      const px = s.cx + ux * s.radius, py = s.cy + uy * s.radius;
      return { ux, uy, px, py, pvx: -s.omega * uy * s.radius, pvy: s.omega * ux * s.radius, targetAngle: normAngle(s.angle + Math.PI) };
    },
    metrics(state) {
      const C = TD.Config, ship = state.ship, station = state.station;
      const p = this.portState(state);
      const fx = Math.cos(ship.angle), fy = Math.sin(ship.angle);
      const probeX = ship.x + fx * C.VISUAL_PROBE_X, probeY = ship.y + fy * C.VISUAL_PROBE_X;
      const tx = Math.cos(p.targetAngle), ty = Math.sin(p.targetAngle);
      const captureX = p.px + tx * C.PORT_CAPTURE_INSET, captureY = p.py + ty * C.PORT_CAPTURE_INSET;
      const rx = captureX - station.cx, ry = captureY - station.cy;
      const captureVx = -station.omega * ry, captureVy = station.omega * rx;
      const rvx = ship.vx - captureVx, rvy = ship.vy - captureVy;
      return {
        p, probeX, probeY, captureX, captureY, captureVx, captureVy,
        dist: Math.hypot(probeX - captureX, probeY - captureY),
        rel: Math.hypot(rvx, rvy),
        dir: Math.abs(normAngle(ship.angle - p.targetAngle)),
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
