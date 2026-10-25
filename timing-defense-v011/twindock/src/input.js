(() => {
  'use strict';
  const TD = window.TwinDock;
  const { inputCurve } = TD.MathUtil;

  TD.Input = {
    bind(state, ui) {
      const attach = (side, refs) => {
        side.pad = refs.pad; side.origin = refs.origin; side.thumb = refs.thumb; side.pct = refs.pct;
        refs.pad.addEventListener('pointerdown', e => this.begin(state, side, e), { passive: false });
        refs.pad.addEventListener('contextmenu', e => e.preventDefault());
        refs.pad.addEventListener('dragstart', e => e.preventDefault());
      };
      attach(state.input.left, ui.left);
      attach(state.input.right, ui.right);
      window.addEventListener('pointermove', e => { this.move(state.input.left, e); this.move(state.input.right, e); }, { passive: false });
      window.addEventListener('pointerup', e => { this.end(state.input.left, e); this.end(state.input.right, e); }, { passive: false });
      window.addEventListener('pointercancel', e => { this.end(state.input.left, e); this.end(state.input.right, e); }, { passive: false });
      ui.app.addEventListener('touchmove', e => { if (state.running) e.preventDefault(); }, { passive: false });
      document.addEventListener('visibilitychange', () => { if (document.hidden) this.clearAll(state); });
    },
    clear(side) {
      side.x = side.y = 0; side.held = false; side.pid = null;
      if (side.origin) side.origin.style.display = 'none';
      if (side.thumb) side.thumb.style.display = 'none';
      if (side.pct) side.pct.textContent = '0%';
    },
    clearAll(state) { this.clear(state.input.left); this.clear(state.input.right); },
    begin(state, side, e) {
      if (!state.running || state.docked || side.held) return;
      e.preventDefault();
      side.held = true; side.pid = e.pointerId; side.sx = e.clientX; side.sy = e.clientY; side.x = side.y = 0;
      const r = side.pad.getBoundingClientRect(), lx = e.clientX - r.left, ly = e.clientY - r.top;
      side.origin.style.left = lx + 'px'; side.origin.style.top = ly + 'px'; side.origin.style.display = 'block';
      side.thumb.style.left = lx + 'px'; side.thumb.style.top = ly + 'px'; side.thumb.style.display = 'block';
      try { side.pad.setPointerCapture(e.pointerId); } catch (_) {}
    },
    move(side, e) {
      if (!side.held || side.pid !== e.pointerId) return;
      e.preventDefault();
      const dx = e.clientX - side.sx, dy = e.clientY - side.sy;
      const max = Math.min(112, Math.max(76, side.pad.getBoundingClientRect().height * 0.58));
      const len = Math.hypot(dx, dy) || 1, used = Math.min(max, len), out = inputCurve(used / max);
      side.x = dx / len * out; side.y = dy / len * out;
      const r = side.pad.getBoundingClientRect(), ox = side.sx - r.left, oy = side.sy - r.top;
      side.thumb.style.left = (ox + dx / len * used) + 'px'; side.thumb.style.top = (oy + dy / len * used) + 'px';
      side.pct.textContent = Math.round(out * 100) + '%';
    },
    end(side, e) {
      if (!side.held || side.pid !== e.pointerId) return;
      e.preventDefault();
      try { side.pad.releasePointerCapture(side.pid); } catch (_) {}
      this.clear(side);
    }
  };
})();
