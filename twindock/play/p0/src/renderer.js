(() => {
  'use strict';
  const TD = window.TwinDock;
  const { clamp } = TD.MathUtil;

  TD.Renderer = function Renderer(state, ui) {
    const canvas = ui.canvas;
    const ctx = canvas.getContext('2d', { alpha: false });
    const C = TD.Config;
    const Cam = TD.Camera;

    function roundedRect(x,y,w,h,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.stroke()}}

    function drawStars(){
      const { W, H } = state.viewport, ship = state.ship;
      ctx.fillStyle='#020610';ctx.fillRect(0,0,W,H);
      const g=ctx.createRadialGradient(W*.53,H*.34,20,W*.53,H*.34,Math.max(W,H)*.72);g.addColorStop(0,'#0b1932');g.addColorStop(.45,'#071022');g.addColorStop(1,'#02050c');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
      for(const st of state.stars){
        const rotFactor=.20+st.d*.50, transFactor=.010+st.d*.028;
        const a=ship.angle*rotFactor,c=Math.cos(a),s=Math.sin(a);
        const px=(ship.x-W*.14)*transFactor,py=(ship.y-H*.46)*transFactor;
        const baseX=st.nx*W,baseY=st.ny*H,dx=baseX-W*.5-px,dy=baseY-H*.5-py;
        let x=W*.5+c*dx+s*dy,y=H*.5-s*dx+c*dy;x=((x%W)+W)%W;y=((y%H)+H)%H;
        ctx.globalAlpha=st.a;ctx.fillStyle=st.d>.72?'#eef8ff':'#bfd6ea';ctx.beginPath();ctx.arc(x,y,st.r,0,Math.PI*2);ctx.fill();
      }
      ctx.globalAlpha=1;
    }

    function drawEarth(){
      const { W, H } = state.viewport, ship = state.ship;
      const earthWorldX=W*.10,earthWorldY=H*1.18,R=Math.max(W,H)*.62;
      const p=Cam.worldToScreenLayer(state,earthWorldX,earthWorldY,.68,.48);
      const grd=ctx.createRadialGradient(p.x,p.y-R*.82,R*.05,p.x,p.y,R);grd.addColorStop(0,'#1f6ba8');grd.addColorStop(.68,'#0a3156');grd.addColorStop(.92,'#07172b');grd.addColorStop(1,'#02050c');
      ctx.fillStyle=grd;ctx.beginPath();ctx.arc(p.x,p.y,R,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(90,180,255,.45)';ctx.lineWidth=3;ctx.beginPath();ctx.arc(p.x,p.y,R,Math.PI*1.11-ship.angle*.68,Math.PI*1.86-ship.angle*.68);ctx.stroke();
    }

    function drawStation(){
      const station=state.station,m=TD.Docking.metrics(state),p=m.p;
      ctx.save();ctx.translate(station.cx,station.cy);
      const metal=ctx.createRadialGradient(-24,-28,8,0,0,station.ringR*1.45);metal.addColorStop(0,'#31485b');metal.addColorStop(.38,'#1b3144');metal.addColorStop(.72,'#0b1724');metal.addColorStop(1,'#040910');
      ctx.strokeStyle='#24394c';ctx.lineWidth=station.ringR*.34;ctx.beginPath();ctx.arc(0,0,station.ringR,0,Math.PI*2);ctx.stroke();ctx.strokeStyle='rgba(180,215,240,.18)';ctx.lineWidth=2;
      for(let i=0;i<24;i++){const a=i*Math.PI*2/24;ctx.beginPath();ctx.arc(0,0,station.ringR+(i%2?4:-4),a,a+.12);ctx.stroke();}
      ctx.fillStyle=metal;ctx.beginPath();ctx.arc(0,0,station.ringR*.56,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(160,205,235,.24)';ctx.lineWidth=2;ctx.stroke();
      ctx.rotate(station.angle);
      for(let i=0;i<8;i++){ctx.save();ctx.rotate(i*Math.PI/4);roundedRect(station.ringR*.42,-8,station.ringR*.82,16,5,'#1c3143','rgba(130,185,220,.20)');ctx.fillStyle=i%2?'#ffb44f':'#69c6ff';ctx.globalAlpha=.65;ctx.fillRect(station.ringR*.78,-2,13,4);ctx.globalAlpha=1;ctx.restore();}
      ctx.restore();

      const axisX=-p.ux,axisY=-p.uy,a=Math.atan2(axisY,axisX);
      ctx.save();ctx.translate(p.px,p.py);ctx.rotate(a);
      roundedRect(-22,-31,28,62,8,'#23384a','rgba(150,205,235,.28)');ctx.fillStyle='#101b27';ctx.fillRect(-18,-23,16,46);
      ctx.shadowColor=state.docked?'rgba(116,226,164,.55)':'rgba(255,180,79,.38)';ctx.shadowBlur=state.docked?18:12;ctx.strokeStyle=state.docked?'#74e2a4':'#ffc56f';ctx.lineWidth=6;ctx.beginPath();ctx.arc(16,0,29,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;
      ctx.strokeStyle='rgba(200,225,245,.65)';ctx.lineWidth=3;ctx.beginPath();ctx.arc(16,0,21,0,Math.PI*2);ctx.stroke();
      const tunnel=ctx.createRadialGradient(16,-5,2,16,0,20);tunnel.addColorStop(0,'#071019');tunnel.addColorStop(.72,'#0a1823');tunnel.addColorStop(1,'#02070c');ctx.fillStyle=tunnel;ctx.beginPath();ctx.arc(16,0,17,0,Math.PI*2);ctx.fill();
      for(let i=0;i<4;i++){ctx.save();ctx.translate(16,0);ctx.rotate(i*Math.PI/2);const latch=state.docked?11:15;roundedRect(19,-3,latch,6,2,state.docked?'#74e2a4':'#8da2b3','rgba(225,245,255,.35)');ctx.restore();}
      const checks=TD.Docking.checks(m),goodCount=Number(checks.pos)+Number(checks.vel)+Number(checks.dir)+Number(checks.spin);
      for(let i=0;i<8;i++){const la=i*Math.PI/4,lx=16+Math.cos(la)*35,ly=Math.sin(la)*35;ctx.fillStyle=(state.docked||goodCount>=3)?'#74e2a4':(i%2?'#69c6ff':'#ffb44f');ctx.globalAlpha=.45+.45*(.5+.5*Math.sin(performance.now()/220+i));ctx.beginPath();ctx.arc(lx,ly,2.2,0,Math.PI*2);ctx.fill();}
      ctx.globalAlpha=1;ctx.restore();
      ctx.strokeStyle='rgba(105,198,255,.30)';ctx.lineWidth=2;ctx.setLineDash([8,9]);ctx.beginPath();ctx.moveTo(p.px+p.ux*190,p.py+p.uy*190);ctx.lineTo(p.px,p.py);ctx.stroke();ctx.setLineDash([]);
      const gateAlpha=m.dist<110?.42:.20;ctx.globalAlpha=gateAlpha;ctx.strokeStyle=state.docked?'#74e2a4':'#ffb44f';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(m.captureX,m.captureY,20,0,Math.PI*2);ctx.stroke();ctx.globalAlpha=1;
    }

    function drawShip(){
      const ship=state.ship,left=state.input.left,right=state.input.right;
      ctx.save();ctx.translate(Cam.camX(state),Cam.camY(state));
      const VL=84,VW=46,l={x:left.x,y:left.y},r={x:right.x,y:right.y},net={x:l.x+r.x,y:l.y+r.y};
      const torqueVisual=clamp((r.y-l.y)*.72+(l.x-r.x)*.18,-1,1);
      function plume(x,y,dirX,dirY,power,size=1){if(power<.025)return;const len=10+30*power*size,w=2.7+2.5*power*size;ctx.save();ctx.translate(x,y);ctx.rotate(Math.atan2(dirY,dirX));const g=ctx.createLinearGradient(0,0,len,0);g.addColorStop(0,'rgba(242,252,255,.98)');g.addColorStop(.18,'rgba(124,215,255,.96)');g.addColorStop(.52,'rgba(52,147,255,.72)');g.addColorStop(1,'rgba(21,72,180,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(0,-w);ctx.lineTo(len,0);ctx.lineTo(0,w);ctx.closePath();ctx.fill();ctx.restore();}
      const fwd=Math.max(0,net.x),back=Math.max(0,-net.x),down=Math.max(0,net.y),up=Math.max(0,-net.y),cw=Math.max(0,torqueVisual),ccw=Math.max(0,-torqueVisual);
      plume(-VL*.43,-VW*.22,-1,0,clamp(fwd*.55+cw*.20,0,1),1.08);plume(-VL*.43,VW*.22,-1,0,clamp(fwd*.55+ccw*.20,0,1),1.08);
      plume(VL*.43,-VW*.22,1,0,clamp(back*.55+ccw*.20,0,1),.9);plume(VL*.43,VW*.22,1,0,clamp(back*.55+cw*.20,0,1),.9);
      plume(-VL*.25,-VW*.47,0,-1,clamp(down*.50+ccw*.50,0,1),.78);plume(VL*.25,-VW*.47,0,-1,clamp(down*.50+cw*.50,0,1),.78);
      plume(-VL*.25,VW*.47,0,1,clamp(up*.50+cw*.50,0,1),.78);plume(VL*.25,VW*.47,0,1,clamp(up*.50+ccw*.50,0,1),.78);
      const podFill='#536779',podStroke='rgba(218,239,252,.62)';roundedRect(-18,-VW*.58,36,10,4,podFill,podStroke);roundedRect(-18,VW*.58-10,36,10,4,podFill,podStroke);
      ctx.fillStyle='#06111b';for(const [x,y] of [[-VL*.28,-VW*.50],[VL*.28,-VW*.50],[-VL*.28,VW*.50],[VL*.28,VW*.50],[-VL*.43,-VW*.22],[-VL*.43,VW*.22],[VL*.43,-VW*.22],[VL*.43,VW*.22]]){ctx.beginPath();ctx.arc(x,y,2.4,0,Math.PI*2);ctx.fill();}
      const hull=ctx.createLinearGradient(-VL*.45,-VW*.2,VL*.45,VW*.15);hull.addColorStop(0,'#707f8e');hull.addColorStop(.28,'#b7c4ce');hull.addColorStop(.55,'#e2e8ec');hull.addColorStop(.78,'#9caab6');hull.addColorStop(1,'#dce5ea');ctx.fillStyle=hull;ctx.strokeStyle='rgba(235,248,255,.82)';ctx.lineWidth=1.35;
      ctx.beginPath();ctx.moveTo(VL*.42,0);ctx.lineTo(VL*.30,-VW*.34);ctx.lineTo(VL*.05,-VW*.43);ctx.lineTo(-VL*.31,-VW*.36);ctx.lineTo(-VL*.44,-VW*.18);ctx.lineTo(-VL*.44,VW*.18);ctx.lineTo(-VL*.31,VW*.36);ctx.lineTo(VL*.05,VW*.43);ctx.lineTo(VL*.30,VW*.34);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.strokeStyle='rgba(41,65,83,.55)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-VL*.23,-VW*.32);ctx.lineTo(-VL*.12,VW*.32);ctx.moveTo(VL*.13,-VW*.36);ctx.lineTo(VL*.04,VW*.36);ctx.stroke();roundedRect(-14,-10,28,20,5,'#142838','rgba(101,202,255,.68)');ctx.fillStyle='rgba(105,198,255,.16)';ctx.fillRect(-10,-6,20,12);
      ctx.fillStyle='#69c6ff';ctx.globalAlpha=.9;ctx.fillRect(-17,-VW*.40,28,3.5);ctx.fillStyle='#ffb44f';ctx.fillRect(-17,VW*.40-3.5,28,3.5);ctx.globalAlpha=1;
      ctx.save();ctx.translate(VL*.42,0);ctx.fillStyle='#263846';ctx.strokeStyle=state.docked?'#74e2a4':'#d9edf8';ctx.lineWidth=2.2;ctx.beginPath();ctx.arc(5,0,8.5,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle='#071119';ctx.beginPath();ctx.arc(5,0,4.3,0,Math.PI*2);ctx.fill();ctx.fillStyle=state.docked?'#74e2a4':'#bdeaff';ctx.globalAlpha=state.docked?1:.72;ctx.beginPath();ctx.arc(5,-10.5,1.8,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(5,10.5,1.8,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;ctx.restore();
      roundedRect(-VL*.48,-10,9,8,2,'#1b2b37','rgba(190,220,235,.42)');roundedRect(-VL*.48,2,9,8,2,'#1b2b37','rgba(190,220,235,.42)');ctx.restore();
    }

    function drawGuidance(){
      const m=TD.Docking.metrics(state),ship=state.ship;
      Cam.withShipCamera(state,ctx,()=>{if(m.dist<145){ctx.strokeStyle='rgba(255,180,79,.22)';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(m.captureX,m.captureY,28,0,Math.PI*2);ctx.stroke();}const rvx=ship.vx-m.captureVx,rvy=ship.vy-m.captureVy,rel=Math.hypot(rvx,rvy);if(rel>2){ctx.strokeStyle='rgba(105,198,255,.28)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(ship.x+rvx*.35,ship.y+rvy*.35);ctx.stroke();}});
    }

    function drawTargetIndicator(){
      const { W,H }=state.viewport,m=TD.Docking.metrics(state),sp=Cam.worldToScreen(state,m.captureX,m.captureY),margin=64;
      if(sp.x>margin&&sp.x<W-margin&&sp.y>margin&&sp.y<H-margin)return;
      const dx=sp.x-Cam.camX(state),dy=sp.y-Cam.camY(state),a=Math.atan2(dy,dx),ex=clamp(Cam.camX(state)+Math.cos(a)*Math.min(W,H)*.40,margin,W-margin),ey=clamp(Cam.camY(state)+Math.sin(a)*Math.min(W,H)*.40,margin,H-margin);
      ctx.save();ctx.translate(ex,ey);ctx.rotate(a);ctx.fillStyle='rgba(255,180,79,.82)';ctx.beginPath();ctx.moveTo(12,0);ctx.lineTo(-8,-7);ctx.lineTo(-8,7);ctx.closePath();ctx.fill();ctx.restore();
    }

    function drawComfortFrame(){
      const {W,H}=state.viewport,cx=Cam.camX(state),cy=Cam.camY(state);ctx.save();ctx.strokeStyle='rgba(165,210,238,.16)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(cx-82,cy);ctx.lineTo(cx-54,cy);ctx.moveTo(cx+54,cy);ctx.lineTo(cx+82,cy);ctx.moveTo(cx,cy-58);ctx.lineTo(cx,cy-38);ctx.moveTo(cx,cy+38);ctx.lineTo(cx,cy+58);ctx.stroke();ctx.strokeStyle='rgba(105,198,255,.12)';ctx.beginPath();ctx.arc(cx,cy,72,-.78,.78);ctx.stroke();ctx.beginPath();ctx.arc(cx,cy,72,Math.PI-.78,Math.PI+.78);ctx.stroke();
      const inset=14,arm=Math.min(70,W*.055);ctx.strokeStyle='rgba(145,184,212,.13)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(inset,H*.30);ctx.lineTo(inset,H*.70);ctx.moveTo(W-inset,H*.30);ctx.lineTo(W-inset,H*.70);ctx.stroke();ctx.strokeStyle='rgba(105,198,255,.11)';ctx.beginPath();ctx.moveTo(inset,H-inset-8);ctx.lineTo(inset+arm,H-inset-8);ctx.moveTo(W-inset-arm,H-inset-8);ctx.lineTo(W-inset,H-inset-8);ctx.stroke();ctx.fillStyle='rgba(185,216,236,.34)';ctx.font='9px system-ui, sans-serif';ctx.textAlign='center';ctx.fillText('BODY FRAME',cx,cy+86);ctx.restore();
    }

    return {
      resize(){
        const r=ui.app.getBoundingClientRect(),v=state.viewport;v.W=Math.max(320,r.width);v.H=Math.max(240,r.height);v.DPR=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(v.W*v.DPR);canvas.height=Math.round(v.H*v.DPR);canvas.style.width=v.W+'px';canvas.style.height=v.H+'px';ctx.setTransform(v.DPR,0,0,v.DPR,0,0);state.station.cx=v.W*.79;state.station.cy=v.H*.45;state.station.radius=Math.min(v.W,v.H)*.12;state.station.ringR=state.station.radius*1.42;
      },
      makeStars(){
        if(state.starFieldReady)return;state.stars=[];for(let i=0;i<C.STAR_COUNT;i++){const d=TD.MathUtil.seeded01(i*4),nx=TD.MathUtil.seeded01(i*4+1),ny=TD.MathUtil.seeded01(i*4+2),z=TD.MathUtil.seeded01(i*4+3);state.stars.push({nx,ny,r:.28+d*1.1,a:.22+d*.5,d,tw:z});}state.starFieldReady=true;
      },
      draw(){drawStars();drawEarth();Cam.withShipCamera(state,ctx,()=>drawStation());drawGuidance();drawTargetIndicator();drawShip();drawComfortFrame();}
    };
  };
})();
