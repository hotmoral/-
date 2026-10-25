(() => {
  'use strict';
  const TD = window.TwinDock;
  TD.MathUtil = {
    clamp(v, a, b) { return Math.max(a, Math.min(b, v)); },
    normAngle(a) { while (a > Math.PI) a -= Math.PI * 2; while (a < -Math.PI) a += Math.PI * 2; return a; },
    seeded01(i) {
      let x = (i + 1) * 0x9e3779b1;
      x ^= x >>> 16; x = Math.imul(x, 0x85ebca6b); x ^= x >>> 13; x = Math.imul(x, 0xc2b2ae35); x ^= x >>> 16;
      return (x >>> 0) / 4294967296;
    },
    inputCurve(raw) {
      const C = TD.Config;
      if (raw < C.INPUT_DEADZONE) return 0;
      const n = (raw - C.INPUT_DEADZONE) / (1 - C.INPUT_DEADZONE);
      return Math.pow(Math.min(1, n), C.INPUT_EXPONENT);
    }
  };
})();
