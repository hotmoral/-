(() => {
  'use strict';
  const TD = window.TwinDock;
  const { clamp, normAngle } = TD.MathUtil;
  TD.Physics = {
    resetShip(state, clearControls) {
      const { W, H } = state.viewport, ship = state.ship;
      ship.x = W * 0.14; ship.y = H * 0.46; ship.vx = ship.vy = 0; ship.angle = ship.angVel = 0;
      state.angularDrive = 0; state.docked = false; state.dockHold = 0;
      if (clearControls) clearControls();
    },
    update(state, dt, hooks = {}) {
      const C = TD.Config, ship = state.ship, station = state.station;
      station.cx += station.vx * dt; station.cy += station.vy * dt;
      station.angle = normAngle(station.angle + station.omega * dt);
      if (state.docked) {
        state.dockHold -= dt;
        const m = TD.Docking.metrics(state);
        ship.angle = m.p.targetAngle; ship.angVel = station.omega;
        const fx = Math.cos(ship.angle), fy = Math.sin(ship.angle);
        ship.x = m.captureX - fx * C.VISUAL_PROBE_X; ship.y = m.captureY - fy * C.VISUAL_PROBE_X;
        ship.vx = m.captureVx; ship.vy = m.captureVy;
        if (state.dockHold <= 0 && hooks.onDockHoldEnd) hooks.onDockHoldEnd();
        return;
      }
      if (!state.running) return;

      const left = state.input.left, right = state.input.right;
      const c = Math.cos(ship.angle), s = Math.sin(ship.angle);
      const lLocalX = left.x * C.FORCE_SCALE, lLocalY = left.y * C.FORCE_SCALE;
      const rLocalX = right.x * C.FORCE_SCALE, rLocalY = right.y * C.FORCE_SCALE;
      const fLx = c * lLocalX - s * lLocalY, fLy = s * lLocalX + c * lLocalY;
      const fRx = c * rLocalX - s * rLocalY, fRy = s * rLocalX + c * rLocalY;
      ship.vx += (fLx + fRx) * dt; ship.vy += (fLy + fRy) * dt;
      const half = ship.length * 0.27;
      const torque = (-c * half * fLy - (-s * half) * fLx) + (c * half * fRy - (s * half) * fRx);
      const targetAngularDrive = torque * C.ANGULAR_TORQUE_SCALE;
      const angularBlend = 1 - Math.exp(-dt * C.ANGULAR_BLEND_RATE);
      state.angularDrive += (targetAngularDrive - state.angularDrive) * angularBlend;
      ship.angVel += state.angularDrive * dt;
      ship.vx *= Math.pow(C.LINEAR_DAMPING_PER_60HZ, dt * 60); ship.vy *= Math.pow(C.LINEAR_DAMPING_PER_60HZ, dt * 60);
      ship.angVel *= Math.pow(C.ANGULAR_DAMPING_PER_60HZ, dt * 60);
      const sp = Math.hypot(ship.vx, ship.vy);
      if (sp > C.MAX_SPEED) { ship.vx = ship.vx / sp * C.MAX_SPEED; ship.vy = ship.vy / sp * C.MAX_SPEED; }
      ship.angVel = clamp(ship.angVel, -C.MAX_ANGULAR_SPEED, C.MAX_ANGULAR_SPEED);
      ship.x += ship.vx * dt; ship.y += ship.vy * dt; ship.angle = normAngle(ship.angle + ship.angVel * dt);
      const worldLimit = Math.max(state.viewport.W, state.viewport.H) * 8;
      ship.x = clamp(ship.x, -worldLimit, worldLimit); ship.y = clamp(ship.y, -worldLimit, worldLimit);

      const m = TD.Docking.metrics(state);
      if (TD.Docking.canDock(m) && hooks.onDock) hooks.onDock(m);
      else if (m.dist < 10 && (m.rel > 28 || m.dir > 0.32 || m.spin > 0.42) && hooks.onCollision) hooks.onCollision(m);
    }
  };
})();
