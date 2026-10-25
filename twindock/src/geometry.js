(() => {
  'use strict';
  const TD = window.TwinDock;
  const { normAngle } = TD.MathUtil;

  function worldAnchor(bodyX, bodyY, bodyAngle, bodyVx, bodyVy, bodyOmega, anchor) {
    const c = Math.cos(bodyAngle), s = Math.sin(bodyAngle);
    const rx = c * anchor.x - s * anchor.y;
    const ry = s * anchor.x + c * anchor.y;
    return {
      x: bodyX + rx,
      y: bodyY + ry,
      angle: normAngle(bodyAngle + anchor.angle),
      vx: bodyVx - bodyOmega * ry,
      vy: bodyVy + bodyOmega * rx,
      rx,
      ry
    };
  }

  function resolvedStationAnchor(state) {
    const station = state.station, anchor = station.dockAnchor;
    if (!anchor.tracksRadius) return anchor;
    return { x: station.radius - TD.Config.PORT_CAPTURE_INSET, y: 0, angle: Math.PI };
  }

  TD.Geometry = Object.freeze({
    worldAnchor,
    shipDockAnchor(state) {
      const ship = state.ship;
      return worldAnchor(ship.x, ship.y, ship.angle, ship.vx, ship.vy, ship.angVel, ship.dockAnchor);
    },
    stationDockAnchor(state) {
      const station = state.station;
      return worldAnchor(station.cx, station.cy, station.angle, station.vx, station.vy, station.omega, resolvedStationAnchor(state));
    },
    bodyPoseForWorldAnchor(worldX, worldY, worldAngle, localAnchor) {
      const angle = normAngle(worldAngle - localAnchor.angle);
      const c = Math.cos(angle), s = Math.sin(angle);
      const rx = c * localAnchor.x - s * localAnchor.y;
      const ry = s * localAnchor.x + c * localAnchor.y;
      return { x: worldX - rx, y: worldY - ry, angle };
    }
  });
})();
