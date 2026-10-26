(() => {
  'use strict';
  const TD = window.TwinDock;
  const C = TD.Config;

  const crafts = Object.freeze({
    SHUTTLE: Object.freeze({ id:'SHUTTLE', label:'SHUTTLE', visualKind:'SHUTTLE', visualLength:84, visualWidth:46 }),
    CARGO: Object.freeze({ id:'CARGO', label:'LONG CARGO', visualKind:'CARGO', visualLength:190, visualWidth:116 }),
    TUG: Object.freeze({ id:'TUG', label:'WIDE TUG', visualKind:'TUG', visualLength:134, visualWidth:118 })
  });

  const ports = Object.freeze({
    CIRCLE: Object.freeze({ id:'CIRCLE', label:'원형' }),
    RECT: Object.freeze({ id:'RECT', label:'직사각형' }),
    TRAPEZOID: Object.freeze({ id:'TRAPEZOID', label:'사다리꼴' })
  });

  const setups = Object.freeze({
    REFERENCE: Object.freeze({ id:'REFERENCE', label:'SHUTTLE · 원형 전방', craftId:'SHUTTLE', portShape:'CIRCLE', anchorClass:'FRONT', anchorLabel:'전방', x:C.VISUAL_PROBE_X, y:0, angle:0 }),
    SIDE_TOP: Object.freeze({ id:'SIDE_TOP', label:'SHUTTLE · 상단 측면', craftId:'SHUTTLE', portShape:'CIRCLE', anchorClass:'SIDE', anchorLabel:'상단 측면', x:2, y:-31, angle:-Math.PI/2 }),
    SIDE_BOTTOM: Object.freeze({ id:'SIDE_BOTTOM', label:'SHUTTLE · 하단 측면', craftId:'SHUTTLE', portShape:'CIRCLE', anchorClass:'SIDE', anchorLabel:'하단 측면', x:2, y:31, angle:Math.PI/2 }),
    CARGO_RECT_SIDE: Object.freeze({ id:'CARGO_RECT_SIDE', label:'LONG CARGO · 직사각 측면', craftId:'CARGO', portShape:'RECT', anchorClass:'SIDE', anchorLabel:'상단 측면', x:0, y:-61, angle:-Math.PI/2 }),
    SHUTTLE_TRAPEZOID_FRONT: Object.freeze({ id:'SHUTTLE_TRAPEZOID_FRONT', label:'SHUTTLE · 사다리꼴 전방', craftId:'SHUTTLE', portShape:'TRAPEZOID', anchorClass:'FRONT', anchorLabel:'전방', x:C.VISUAL_PROBE_X, y:0, angle:0 }),
    TUG_TRAPEZOID_CORNER: Object.freeze({ id:'TUG_TRAPEZOID_CORNER', label:'WIDE TUG · 사다리꼴 모서리', craftId:'TUG', portShape:'TRAPEZOID', anchorClass:'CORNER', anchorLabel:'우하단 모서리', x:58, y:50, angle:Math.PI/4 }),
    CARGO_RECT_FRONT: Object.freeze({ id:'CARGO_RECT_FRONT', label:'LONG CARGO · 직사각 전방', craftId:'CARGO', portShape:'RECT', anchorClass:'FRONT', anchorLabel:'전방', x:98, y:0, angle:0 })
  });

  function get(id){ return setups[id] || setups.REFERENCE; }
  function craft(id){ return crafts[id] || crafts.SHUTTLE; }
  function port(id){ return ports[id] || ports.CIRCLE; }

  function apply(ship,id){
    const setup=get(id), hull=craft(setup.craftId);
    ship.geometryId=setup.id;
    ship.craftId=hull.id;
    ship.visualKind=hull.visualKind;
    ship.visualLength=hull.visualLength;
    ship.visualWidth=hull.visualWidth;
    ship.portShape=setup.portShape;
    ship.anchorClass=setup.anchorClass;
    ship.dockAnchor.x=setup.x;
    ship.dockAnchor.y=setup.y;
    ship.dockAnchor.angle=setup.angle;
    return setup;
  }

  TD.CraftGeometry = Object.freeze({ crafts, ports, setups, profiles:setups, get, craft, port, apply });
})();
