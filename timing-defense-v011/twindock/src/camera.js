(() => {
  'use strict';
  const TD = window.TwinDock;
  TD.Camera = {
    camX(state) { return state.viewport.W * 0.34; },
    camY(state) { return state.viewport.H * 0.50; },
    withShipCamera(state, ctx, fn) {
      ctx.save(); ctx.translate(this.camX(state), this.camY(state)); ctx.rotate(-state.ship.angle); ctx.translate(-state.ship.x, -state.ship.y); fn(); ctx.restore();
    },
    worldToScreen(state, x, y) {
      const ship = state.ship, dx = x - ship.x, dy = y - ship.y, c = Math.cos(ship.angle), s = Math.sin(ship.angle);
      return { x: this.camX(state) + c * dx + s * dy, y: this.camY(state) - s * dx + c * dy };
    },
    worldToScreenLayer(state, x, y, rotFactor = 1, transFactor = 1) {
      const { W, H } = state.viewport, ship = state.ship;
      const baseX = W * 0.14, baseY = H * 0.46;
      const dx = (x - baseX) - (ship.x - baseX) * transFactor;
      const dy = (y - baseY) - (ship.y - baseY) * transFactor;
      const a = ship.angle * rotFactor, c = Math.cos(a), s = Math.sin(a);
      return { x: this.camX(state) + c * dx + s * dy, y: this.camY(state) - s * dx + c * dy };
    }
  };
})();
