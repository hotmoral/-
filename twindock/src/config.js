(() => {
  'use strict';
  const TD = window.TwinDock = window.TwinDock || {};
  TD.Config = Object.freeze({
    VISUAL_PROBE_X: 40,
    PORT_CAPTURE_INSET: 16,
    DOCK_LIMIT: Object.freeze({ dist: 11, rel: 10, dir: 0.095, spin: 0.10 }),
    FORCE_SCALE: 58,
    INPUT_DEADZONE: 0.10,
    INPUT_EXPONENT: 2.05,
    MAX_SPEED: 78,
    MAX_ANGULAR_SPEED: 0.90,
    ANGULAR_TORQUE_SCALE: 0.00155,
    ANGULAR_BLEND_RATE: 7.2,
    LINEAR_DAMPING_PER_60HZ: 0.9992,
    ANGULAR_DAMPING_PER_60HZ: 0.972,
    STATION_OMEGA: 0.18,
    SHIP_LENGTH: 66,
    SHIP_WIDTH: 28,
    DOCK_HOLD_SECONDS: 2.0,
    STAR_COUNT: 150
  });
})();
