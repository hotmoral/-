(() => {
  'use strict';
  const TD = window.TwinDock;
  const OriginalRenderer = TD.Renderer;
  const { clamp, normAngle } = TD.MathUtil;

  TD.Renderer = function CraftFamilyProbeRenderer(state, ui) {
    const renderer = OriginalRenderer(state, ui);
    const ctx = ui.canvas.getContext('2d');
    const Cam = TD.Camera;
    const C = TD.Config;

    function roundedRect(x,y,w,h,r,fill,stroke){
      ctx.beginPath();ctx.roundRect(x,y,w,h,r);
      if(fill){ctx.fillStyle=fill;ctx.fill();}
      if(stroke){ctx.strokeStyle=stroke;ctx.stroke();}
    }

    function plume(x,y,dirX,dirY,power,size=1){
      if(power<.025)return;
      const len=10+30*power*size,w=2.7+2.5*power*size;
      ctx.save();ctx.translate(x,y);ctx.rotate(Math.atan2(dirY,dirX));
      const g=ctx.createLinearGradient(0,0,len,0);
      g.addColorStop(0,'rgba(242,252,255,.98)');g.addColorStop(.18,'rgba(124,215,255,.96)');g.addColorStop(.52,'rgba(52,147,255,.72)');g.addColorStop(1,'rgba(21,72,180,0)');
      ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(0,-w);ctx.lineTo(len,0);ctx.lineTo(0,w);ctx.closePath();ctx.fill();ctx.restore();
    }

    function drawProbePlumes(L,W){
      const left=state.input.left,right=state.input.right;
      const netX=left.x+right.x,netY=left.y+right.y;
      const torque=clamp((right.y-left.y)*.72+(left.x-right.x)*.18,-1,1);
      const fwd=Math.max(0,netX),back=Math.max(0,-netX),down=Math.max(0,netY),up=Math.max(0,-netY),cw=Math.max(0,torque),ccw=Math.max(0,-torque);
      plume(-L*.45,-W*.28,-1,0,clamp(fwd*.55+cw*.20,0,1),1.08);plume(-L*.45,W*.28,-1,0,clamp(fwd*.55+ccw*.20,0,1),1.08);
      plume(L*.45,-W*.28,1,0,clamp(back*.55+ccw*.20,0,1),.9);plume(L*.45,W*.28,1,0,clamp(back*.55+cw*.20,0,1),.9);
      plume(-L*.24,-W*.50,0,-1,clamp(down*.50+ccw*.50,0,1),.84);plume(L*.24,-W*.50,0,-1,clamp(down*.50+cw*.50,0,1),.84);
      plume(-L*.24,W*.50,0,1,clamp(up*.50+cw*.50,0,1),.84);plume(L*.24,W*.50,0,1,clamp(up*.50+ccw*.50,0,1),.84);
    }

    function drawPortGlyph(shape,docked,target=false,scale=1){
      const active=docked?'#74e2a4':(target?'#ffc56f':'#d9edf8');
      const fill=target?'rgba(7,17,25,.58)':'#263846';
      ctx.save();ctx.scale(scale,scale);ctx.lineWidth=target?1.8:2.3;ctx.strokeStyle=active;ctx.fillStyle=fill;
      if(shape==='RECT'){
        ctx.beginPath();ctx.roundRect(-11,-7.5,22,15,2.2);ctx.fill();ctx.stroke();
        ctx.fillStyle='#071119';ctx.fillRect(-6,-3.4,12,6.8);
        ctx.fillStyle=active;ctx.globalAlpha=.9;ctx.fillRect(11.5,-3.3,2.5,6.6);ctx.globalAlpha=1;
        ctx.strokeStyle='rgba(189,234,255,.52)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-8,-10);ctx.lineTo(-8,-6.5);ctx.moveTo(-8,10);ctx.lineTo(-8,6.5);ctx.stroke();
      }else if(shape==='TRAPEZOID'){
        ctx.beginPath();ctx.moveTo(-11,-9);ctx.lineTo(10,-5.5);ctx.lineTo(10,5.5);ctx.lineTo(-11,9);ctx.closePath();ctx.fill();ctx.stroke();
        ctx.fillStyle='#071119';ctx.beginPath();ctx.moveTo(-5,-4.5);ctx.lineTo(5,-2.7);ctx.lineTo(5,2.7);ctx.lineTo(-5,4.5);ctx.closePath();ctx.fill();
        ctx.fillStyle=active;ctx.globalAlpha=.9;ctx.fillRect(10.8,-3.4,2.6,6.8);ctx.globalAlpha=1;
      }else{
        ctx.beginPath();ctx.arc(0,0,9.2,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.fillStyle='#071119';ctx.beginPath();ctx.arc(0,0,4.5,0,Math.PI*2);ctx.fill();
        ctx.fillStyle=active;ctx.globalAlpha=.8;ctx.beginPath();ctx.arc(0,-11.8,2,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(0,11.8,2,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
      }
      ctx.restore();
    }

    function coverReferenceNose(){
      const cx=Cam.camX(state),cy=Cam.camY(state);
      ctx.save();ctx.translate(cx+C.VISUAL_PROBE_X,cy);
      roundedRect(-15,-15,30,30,9,'#4a5d6c','rgba(220,239,250,.42)');
      ctx.fillStyle='#1a2a36';ctx.beginPath();ctx.arc(-2,0,7,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }

    function drawShuttleVariant(){
      const ship=state.ship,a=ship.dockAnchor;
      if(ship.geometryId==='REFERENCE' && ship.portShape==='CIRCLE') return;
      coverReferenceNose();
      const cx=Cam.camX(state),cy=Cam.camY(state);
      ctx.save();ctx.translate(cx+a.x,cy+a.y);ctx.rotate(a.angle);drawPortGlyph(ship.portShape,state.docked,false,1);ctx.restore();
    }

    function drawCargo(){
      const ship=state.ship,L=ship.visualLength,W=ship.visualWidth,cx=Cam.camX(state),cy=Cam.camY(state);
      ctx.save();ctx.translate(cx,cy);drawProbePlumes(L,W);
      const hull=ctx.createLinearGradient(-L*.48,-W*.2,L*.48,W*.18);hull.addColorStop(0,'#556b78');hull.addColorStop(.22,'#8fa0aa');hull.addColorStop(.55,'#c8d0d4');hull.addColorStop(.78,'#7f909c');hull.addColorStop(1,'#b7c3ca');
      roundedRect(-L*.50,-36,L,72,10,hull,'rgba(230,245,252,.70)');
      roundedRect(-L*.28,-W*.50,L*.56,18,5,'#384f5e','rgba(188,220,238,.48)');
      roundedRect(-L*.28,W*.50-18,L*.56,18,5,'#384f5e','rgba(188,220,238,.48)');
      for(let i=-2;i<=2;i++){
        const x=i*31;
        roundedRect(x-13,-28,26,56,4,i%2?'#758793':'#657985','rgba(228,242,249,.22)');
        ctx.strokeStyle='rgba(22,46,61,.45)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x,-25);ctx.lineTo(x,25);ctx.stroke();
      }
      roundedRect(-L*.49,-13,18,26,5,'#243947','rgba(199,229,244,.45)');
      roundedRect(L*.40,-18,17,36,5,'#223948','rgba(185,222,241,.52)');
      ctx.fillStyle='rgba(105,198,255,.35)';ctx.fillRect(L*.42,-11,10,22);
      ctx.fillStyle='#ffb44f';ctx.globalAlpha=.72;ctx.fillRect(-52,-W*.36,104,3);ctx.fillStyle='#69c6ff';ctx.fillRect(-52,W*.36-3,104,3);ctx.globalAlpha=1;
      ctx.fillStyle='rgba(5,14,23,.72)';ctx.font='700 8px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText('LONG CARGO',0,3);
      const a=ship.dockAnchor;ctx.save();ctx.translate(a.x,a.y);ctx.rotate(a.angle);drawPortGlyph(ship.portShape,state.docked,false,1.08);ctx.restore();
      ctx.restore();
    }

    function drawTug(){
      const ship=state.ship,L=ship.visualLength,W=ship.visualWidth,cx=Cam.camX(state),cy=Cam.camY(state);
      ctx.save();ctx.translate(cx,cy);drawProbePlumes(L,W);
      const hull=ctx.createLinearGradient(-60,-50,58,52);hull.addColorStop(0,'#4e6676');hull.addColorStop(.45,'#a9b7c0');hull.addColorStop(1,'#738895');
      ctx.fillStyle=hull;ctx.strokeStyle='rgba(231,246,253,.72)';ctx.lineWidth=1.4;
      ctx.beginPath();ctx.moveTo(59,-29);ctx.lineTo(43,-51);ctx.lineTo(5,-58);ctx.lineTo(-35,-51);ctx.lineTo(-65,-27);ctx.lineTo(-62,18);ctx.lineTo(-44,43);ctx.lineTo(-7,55);ctx.lineTo(39,51);ctx.lineTo(66,24);ctx.closePath();ctx.fill();ctx.stroke();
      roundedRect(-58,-31,26,61,7,'#2b4352','rgba(190,222,239,.45)');
      roundedRect(-29,-48,34,18,5,'#405967','rgba(203,231,245,.42)');
      roundedRect(-17,31,45,17,5,'#3b5362','rgba(203,231,245,.42)');
      ctx.fillStyle='#102534';ctx.strokeStyle='rgba(105,198,255,.68)';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(20,-27);ctx.lineTo(46,-20);ctx.lineTo(51,4);ctx.lineTo(23,10);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.fillStyle='rgba(105,198,255,.18)';ctx.fill();
      ctx.strokeStyle='rgba(38,63,78,.50)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-27,-28);ctx.lineTo(28,29);ctx.moveTo(-23,24);ctx.lineTo(25,-30);ctx.stroke();
      ctx.fillStyle='#ffb44f';ctx.globalAlpha=.78;ctx.fillRect(-49,-39,30,3);ctx.fillStyle='#69c6ff';ctx.fillRect(-6,39,28,3);ctx.globalAlpha=1;
      ctx.fillStyle='rgba(7,17,25,.72)';ctx.font='700 8px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText('WIDE TUG',-9,2);
      const a=ship.dockAnchor;ctx.save();ctx.translate(a.x,a.y);ctx.rotate(a.angle);drawPortGlyph(ship.portShape,state.docked,false,1.1);ctx.restore();
      ctx.restore();
    }

    function drawActiveCraft(){
      const kind=state.ship.visualKind;
      if(kind==='CARGO') drawCargo();
      else if(kind==='TUG') drawTug();
      else drawShuttleVariant();
    }

    function drawTargetShape(){
      const ship=state.ship;
      if(ship.portShape==='CIRCLE') return;
      const m=TD.Docking.metrics(state),p=Cam.worldToScreen(state,m.captureX,m.captureY);
      const screenAngle=normAngle(m.stationAnchor.angle-ship.angle);
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(screenAngle);ctx.globalAlpha=m.dist<130?.92:.58;drawPortGlyph(ship.portShape,state.docked,true,1.32);ctx.globalAlpha=1;ctx.restore();
    }

    return Object.freeze({
      resize: renderer.resize,
      makeStars: renderer.makeStars,
      draw(){ renderer.draw(); drawActiveCraft(); drawTargetShape(); }
    });
  };
})();
