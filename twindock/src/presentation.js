(() => {
  'use strict';
  const TD = window.TwinDock;
  const OriginalRenderer = TD.Renderer;
  const normAngle = TD.MathUtil.normAngle;

  TD.Presentation = Object.freeze({
    unwrapAngle(visual, previousWrapped, currentWrapped) {
      return visual + normAngle(currentWrapped - previousWrapped);
    }
  });

  TD.Renderer = function PresentationSafeRenderer(state, ui) {
    let previousWrapped = state.ship.angle;
    let visualAngle = previousWrapped;

    const shipView = new Proxy(state.ship, {
      get(target, prop, receiver) {
        if (prop === 'angle') return visualAngle;
        return Reflect.get(target, prop, receiver);
      },
      set(target, prop, value, receiver) {
        return Reflect.set(target, prop, value, receiver);
      }
    });

    const stateView = new Proxy(state, {
      get(target, prop, receiver) {
        if (prop === 'ship') return shipView;
        return Reflect.get(target, prop, receiver);
      },
      set(target, prop, value, receiver) {
        return Reflect.set(target, prop, value, receiver);
      }
    });

    const renderer = OriginalRenderer(stateView, ui);

    function syncAngle() {
      const currentWrapped = state.ship.angle;
      if (!state.startedOnce) {
        visualAngle = currentWrapped;
        previousWrapped = currentWrapped;
        return;
      }
      visualAngle = TD.Presentation.unwrapAngle(visualAngle, previousWrapped, currentWrapped);
      previousWrapped = currentWrapped;
    }

    return Object.freeze({
      resize: renderer.resize,
      makeStars: renderer.makeStars,
      draw() {
        syncAngle();
        renderer.draw();
      }
    });
  };
})();
