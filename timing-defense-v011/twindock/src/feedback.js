(() => {
  'use strict';
  const TD = window.TwinDock;
  const { clamp } = TD.MathUtil;

  TD.FeedbackRenderer = function FeedbackRenderer(state, ui) {
    const canvas = document.getElementById('feedback');
    const ctx = canvas.getContext('2d');

    function resize(){
      const r=ui.app.getBoundingClientRect(),v=state.viewport,dpr=Math.min(window.devicePixelRatio||1,2);
      canvas.width=Math.round(Math.max(320,r.width)*dpr);canvas.height=Math.round(Math.max(240,r.height)*dpr);
      canvas.style.width=Math.max(320,r.width)+'px';canvas.style.height=Math.max(240,r.height)+'px';ctx.setTransform(dpr,0,0,dpr,0,0);
    }

    function drawBracket(gap,arm,color,width){
      ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();
      for(const sx of [-1,1])for(const sy of [-1,1]){ctx.moveTo(sx*gap,sy*(gap-arm));ctx.lineTo(sx*gap,sy*gap);ctx.lineTo(sx*(gap-arm),sy*gap);}ctx.stroke();
    }

    function draw(){
      const {W,H}=state.viewport;ctx.clearRect(0,0,W,H);
      const m=TD.Docking.metrics(state),checks=TD.Docking.checks(m);
      if(m.dist>210)return;
      const sp=TD.Camera.worldToScreen(state,m.captureX,m.captureY);
      if(sp.x<-80||sp.x>W+80||sp.y<-80||sp.y>H+80)return;
      const ship=state.ship,alpha=clamp(1-(m.dist-45)/190,.20,1);
      const relAngle=Math.atan2(Math.sin(m.p.targetAngle-ship.angle),Math.cos(m.p.targetAngle-ship.angle));
      ctx.save();ctx.translate(sp.x,sp.y);ctx.globalAlpha=alpha;

      if(state.docked){
        ctx.strokeStyle='rgba(116,226,164,.95)';ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(0,0,34,0,Math.PI*2);ctx.stroke();ctx.restore();return;
      }

      const gap=22+clamp(m.dist*.18,0,34);
      drawBracket(gap,9,checks.pos?'rgba(116,226,164,.95)':'rgba(255,180,79,.64)',checks.pos?2.2:1.5);

      ctx.lineWidth=2;ctx.strokeStyle=checks.dir?'rgba(116,226,164,.86)':'rgba(105,198,255,.42)';ctx.beginPath();ctx.moveTo(-34,-5);ctx.lineTo(-34,5);ctx.moveTo(34,-5);ctx.lineTo(34,5);ctx.stroke();
      ctx.save();ctx.rotate(relAngle);ctx.strokeStyle=checks.dir?'rgba(116,226,164,.98)':'rgba(255,180,79,.86)';ctx.lineWidth=2.6;ctx.beginPath();ctx.moveTo(-34,-7);ctx.lineTo(-34,7);ctx.moveTo(34,-7);ctx.lineTo(34,7);ctx.stroke();ctx.restore();

      const signedSpin=state.station.omega-ship.angVel,trail=clamp(Math.abs(signedSpin)*.85,.035,.72),spinDir=signedSpin===0?1:Math.sign(signedSpin);
      ctx.strokeStyle=checks.spin?'rgba(116,226,164,.90)':'rgba(255,180,79,.56)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,43,relAngle-spinDir*trail,relAngle);ctx.stroke();ctx.fillStyle=checks.spin?'#74e2a4':'#ffb44f';ctx.beginPath();ctx.arc(Math.cos(relAngle)*43,Math.sin(relAngle)*43,checks.spin?2.8:2.2,0,Math.PI*2);ctx.fill();

      const rvx=ship.vx-m.captureVx,rvy=ship.vy-m.captureVy,c=Math.cos(ship.angle),s=Math.sin(ship.angle),bx=c*rvx+s*rvy,by=-s*rvx+c*rvy,mag=Math.hypot(bx,by);
      if(mag<1.2){ctx.fillStyle='rgba(116,226,164,.90)';ctx.beginPath();ctx.arc(0,51,2.5,0,Math.PI*2);ctx.fill();}
      else{
        const ux=bx/mag,uy=by/mag,len=clamp(mag*.55,7,42),start=49,end=start+len,color=checks.vel?'rgba(116,226,164,.90)':'rgba(255,180,79,.66)';
        ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(ux*start,uy*start);ctx.lineTo(ux*end,uy*end);ctx.stroke();
        ctx.save();ctx.translate(ux*end,uy*end);ctx.rotate(Math.atan2(uy,ux));ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-7,-4);ctx.lineTo(-7,4);ctx.closePath();ctx.fill();ctx.restore();
      }
      ctx.restore();
    }

    return {resize,draw};
  };
})();
