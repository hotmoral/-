(() => {
  'use strict';
  const TD = window.TwinDock;
  TD.UI = {
    collect() {
      const byId = id => document.getElementById(id);
      return {
        app: byId('app'), canvas: byId('game'), score: byId('score'), rel: byId('relSpeed'), mode: byId('mode'),
        msgT: byId('msgTitle'), msgS: byId('msgSub'), ckPos: byId('ckPos'), ckVel: byId('ckVel'), ckDir: byId('ckDir'), ckSpin: byId('ckSpin'),
        start: byId('startBtn'), reset: byId('resetBtn'), full: byId('fullBtn'), craft: byId('craftBtn'), flash: byId('flash'), pulse: byId('pulse'),
        left: { pad: byId('lPad'), origin: byId('lOrigin'), thumb: byId('lThumb'), pct: byId('lPct') },
        right: { pad: byId('rPad'), origin: byId('rOrigin'), thumb: byId('rThumb'), pct: byId('rPct') }
      };
    },
    setCheck(el, ok) { el.classList.toggle('ok', ok); },
    updateDockChecks(ui, metrics) {
      const c = TD.Docking.checks(metrics);
      this.setCheck(ui.ckPos, c.pos); this.setCheck(ui.ckVel, c.vel); this.setCheck(ui.ckDir, c.dir); this.setCheck(ui.ckSpin, c.spin);
      ui.rel.textContent = (metrics.rel / 10).toFixed(1); ui.mode.textContent = metrics.dist < 95 ? '정밀 동기화' : '접근';
    },
    vibrate(pattern) { if (navigator.vibrate) navigator.vibrate(pattern); }
  };
})();
