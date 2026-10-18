(()=>{
"use strict";
const game=document.getElementById("game");if(!game)return;
const layer=document.createElement("canvas");layer.id="motionBackdrop";Object.assign(layer.style,{position:"fixed",inset:"0",width:"100%",height:"100%",pointerEvents:"none",zIndex:"1",opacity:"1"});game.style.zIndex="0";document.body.appendChild(layer);for(const id of ["ui","toast","offline","dead"]){const el=document.getElementById(id);if(el)el.style.zIndex="5"}
const c=layer.getContext("2d");let W=innerWidth,H=innerHeight,last=performance.now(),ox=0,oy=0,vx=0,vy=0,drag=false,sx=0,sy=0,px=0,py=0;
function resize(){W=innerWidth;H=innerHeight;layer.width=W;layer.height=H}addEventListener("resize",resize,{passive:true});resize();
function parsePush(){const s=document.getElementById("statBody")?.textContent||"";const m=s.match(/추진\s*(\d+)/);return m?Number(m[1]):0}
function desired(){if(!drag)return{x:0,y:0};const dx=px-sx,dy=py-sy,l=Math.hypot(dx,dy);if(l<8)return{x:0,y:0};const trait=parsePush(),speed=Math.max(82,166)+Math.log2(1+trait)*18;return{x:dx/l*speed,y:dy/l*speed}}
function down(e){drag=true;sx=px=e.clientX;sy=py=e.clientY}function move(e){if(drag){px=e.clientX;py=e.clientY}}function up(){drag=false}
game.addEventListener("pointerdown",down,{passive:true});game.addEventListener("pointermove",move,{passive:true});game.addEventListener("pointerup",up,{passive:true});game.addEventListener("pointercancel",up,{passive:true});
function hash(x,y){let n=(x*374761393+y*668265263)>>>0;n=(n^(n>>>13))*1274126177>>>0;return((n^(n>>>16))>>>0)/4294967295}
function drawLandmarks(){
  const cell=260,ix0=Math.floor((-ox)/cell)-2,ix1=Math.floor((W-ox)/cell)+2,iy0=Math.floor((-oy)/cell)-2,iy1=Math.floor((H-oy)/cell)+2;
  for(let gy=iy0;gy<=iy1;gy++)for(let gx=ix0;gx<=ix1;gx++){
    const h=hash(gx,gy);if(h<.25)continue;const x=gx*cell+hash(gx+11,gy+7)*cell+ox,y=gy*cell+hash(gx+3,gy+19)*cell+oy,r=18+hash(gx+29,gy+5)*48,rot=hash(gx+17,gy+31)*Math.PI*2;c.save();c.translate(x,y);c.rotate(rot);
    if(h<.52){c.globalAlpha=.12;c.fillStyle="#a9f4db";c.strokeStyle="rgba(214,255,241,.18)";c.lineWidth=1;c.beginPath();c.ellipse(0,0,r*1.7,r*.48,0,0,Math.PI*2);c.fill();c.stroke();c.globalAlpha=.08;for(let k=0;k<5;k++){const a=k*Math.PI*2/5;c.beginPath();c.arc(Math.cos(a)*r*.55,Math.sin(a)*r*.2,r*.16,0,Math.PI*2);c.fill()}}
    else if(h<.76){c.globalAlpha=.14;c.strokeStyle="#7ed2c9";c.lineWidth=Math.max(1,r*.06);for(let k=-2;k<=2;k++){c.beginPath();c.moveTo(-r*1.5,k*r*.14);c.bezierCurveTo(-r*.5,k*r*.42,r*.45,-k*r*.38,r*1.45,k*r*.1);c.stroke()}}
    else{c.globalAlpha=.10;c.fillStyle="#cebdf6";for(let k=0;k<6;k++){const a=k*Math.PI/3;c.beginPath();c.arc(Math.cos(a)*r*.58,Math.sin(a)*r*.46,r*(.18+(k%2)*.07),0,Math.PI*2);c.fill()}}
    c.restore();c.globalAlpha=1;
  }
}
function drawFineParticles(){c.fillStyle="rgba(222,255,246,.18)";for(let i=0;i<70;i++){const x=((i*137+ox*.46)%W+W)%W,y=((i*83+oy*.46)%H+H)%H,r=.7+(i%4)*.35;c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fill()}}
function drawStreaks(speed){const n=Math.min(1,Math.max(0,(speed-45)/180));if(n<=.02)return;const a=Math.atan2(vy,vx),dx=Math.cos(a),dy=Math.sin(a),len=14+n*52;c.save();c.strokeStyle=`rgba(220,255,248,${.04+n*.11})`;c.lineWidth=1;c.lineCap="round";for(let i=0;i<18;i++){const x=(i*149)%W,y=(i*97+31)%H,par=.55+(i%4)*.13;c.beginPath();c.moveTo(x-dx*len*par,y-dy*len*par);c.lineTo(x+dx*3,y+dy*3);c.stroke()}c.restore()}
function frame(now){const dt=Math.min(.035,(now-last)/1000||.016);last=now;const d=desired(),k=1-Math.exp(-7.5*dt);vx+=(d.x-vx)*k;vy+=(d.y-vy)*k;if(!drag){const f=Math.pow(.12,dt);vx*=f;vy*=f}ox-=vx*dt;oy-=vy*dt;const wrap=260*24;if(ox>wrap||ox<-wrap)ox%=260;if(oy>wrap||oy<-wrap)oy%=260;c.clearRect(0,0,W,H);drawLandmarks();drawFineParticles();drawStreaks(Math.hypot(vx,vy));requestAnimationFrame(frame)}
requestAnimationFrame(frame);
})();
