(() => {
  'use strict';
  const TD = window.TwinDock;
  const C = TD.Config;

  const profiles = Object.freeze({
    REFERENCE: Object.freeze({ id:'REFERENCE', label:'전방', x:C.VISUAL_PROBE_X, y:0, angle:0 }),
    SIDE_TOP: Object.freeze({ id:'SIDE_TOP', label:'상단 측면', x:2, y:-31, angle:-Math.PI/2 }),
    SIDE_BOTTOM: Object.freeze({ id:'SIDE_BOTTOM', label:'하단 측면', x:2, y:31, angle:Math.PI/2 })
  });

  function get(id){ return profiles[id] || profiles.REFERENCE; }

  function apply(ship,id){
    const profile=get(id);
    ship.geometryId=profile.id;
    ship.dockAnchor.x=profile.x;
    ship.dockAnchor.y=profile.y;
    ship.dockAnchor.angle=profile.angle;
    return profile;
  }

  TD.CraftGeometry = Object.freeze({ profiles, get, apply });
})();
