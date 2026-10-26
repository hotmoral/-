(() => {
  'use strict';
  const TD = window.TwinDock;
  const OriginalRenderer = TD.Renderer;

  TD.Renderer = function CraftProbeRenderer(state, ui) {
    const renderer = OriginalRenderer(state, ui);
    const ctx = ui.canvas.getContext('2d');
    const Cam = TD.Camera;

    function roundedRect(x,y,w,h,r,fill,stroke){
      ctx.beginPath();ctx.roundRect(x,y,w,h,r);
      if(fill){ctx.fillStyle=fill;ctx.fill();}
      if(stroke){ctx.strokeStyle=stroke;ctx.stroke();}
    }

    function drawActiveAnchorOverlay(){
      const ship=state.ship;
      if(ship.geometryId==='REFERENCE') return;
      const cx=Cam.camX(state),cy=Cam.camY(state),a=ship.dockAnchor;

      ctx.save();
      ctx.translate(cx+TD.Config.VISUAL_PROBE_X,cy);
      ctx.fillStyle='#344653';ctx.strokeStyle='rgba(210,232,244,.44)';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.arc(0,0,11.5,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle='#111e28';ctx.beginPath();ctx.arc(0,0,5.2,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(165,190,207,.65)';ctx.fillRect(-3.5,-1,7,2);
      ctx.restore();

      ctx.save();
      ctx.translate(cx+a.x,cy+a.y);
      ctx.rotate(a.angle);
      ctx.lineWidth=1.4;
      roundedRect(-15,-10,16,20,5,'#455b6b','rgba(218,239,252,.58)');
      roundedRect(-21,-7,9,14,3,'#263846','rgba(176,213,234,.42)');
      ctx.fillStyle='#263846';ctx.strokeStyle=state.docked?'#74e2a4':'#ffc56f';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.arc(0,0,9.2,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle='#071119';ctx.beginPath();ctx.arc(0,0,4.5,0,Math.PI*2);ctx.fill();
      ctx.fillStyle=state.docked?'#74e2a4':'#bdeaff';ctx.globalAlpha=state.docked?1:.86;
      ctx.beginPath();ctx.arc(0,-11.8,2,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(0,11.8,2,0,Math.PI*2);ctx.fill();
      ctx.globalAlpha=1;
      ctx.strokeStyle='rgba(255,197,111,.34)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(0,0,14.5,-.72,.72);ctx.stroke();
      ctx.restore();
    }

    return Object.freeze({
      resize: renderer.resize,
      makeStars: renderer.makeStars,
      draw(){ renderer.draw(); drawActiveAnchorOverlay(); }
    });
  };
})();
