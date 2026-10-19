// Timing Defense v0.14 patch
function nowShim(){return performance.now()*.001}

function drawProjectiles(){
  for(const p of S.projectiles){
    if(p.age<0)continue;
    const t=clamp(p.age/p.life,0,1),e=easeOutCubic(t);
    p.x=p.sx+(p.tx-p.sx)*e;p.y=p.sy+(p.ty-p.sy)*e;
    const ang=Math.atan2(p.ty-p.sy,p.tx-p.sx),alpha=p.owner==='local'?1:.64,rgb=classColor(p.cls);
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);ctx.globalAlpha=alpha;
    ctx.shadowColor=`rgba(${rgb},.75)`;ctx.shadowBlur=p.heavy?20:11;
    if(p.cls==='knight'){
      const sc=(p.heavy?1.45:1)*(p.skillPower?1.20:1);ctx.scale(sc,sc);
      ctx.strokeStyle='rgba(255,211,106,.20)';ctx.lineWidth=p.heavy?12:8;ctx.beginPath();ctx.arc(-11,0,31,-.88,.88);ctx.stroke();
      ctx.strokeStyle='rgba(255,226,142,.96)';ctx.lineWidth=p.heavy?6.5:4.2;ctx.beginPath();ctx.arc(0,0,27,-.90,.90);ctx.stroke();
      ctx.strokeStyle='rgba(255,255,255,.75)';ctx.lineWidth=1.4;ctx.beginPath();ctx.arc(2,0,23,-.82,.82);ctx.stroke();
    }else if(p.cls==='rogue'){
      p.rot+=.28;ctx.rotate(p.rot);
      ctx.strokeStyle='rgba(170,225,255,.28)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-30,0);ctx.lineTo(-8,0);ctx.stroke();
      ctx.fillStyle='rgba(225,246,255,.98)';ctx.beginPath();ctx.moveTo(18,0);ctx.lineTo(-3,-5);ctx.lineTo(-12,0);ctx.lineTo(-3,5);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(110,190,225,.95)';ctx.fillRect(-11,-2,8,4);
      ctx.strokeStyle='rgba(255,255,255,.8)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(14,0);ctx.lineTo(-2,-3);ctx.stroke();
    }else if(p.cls==='tank'){
      const skillScale=p.skillPower?1.25:1,w=(31+58*t)*skillScale,h=(28+14*t)*skillScale;
      ctx.rotate(-ang);
      ctx.strokeStyle='rgba(130,210,255,.18)';ctx.lineWidth=p.heavy?14:9;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.72,.72);ctx.stroke();
      ctx.strokeStyle='rgba(185,238,255,.96)';ctx.lineWidth=p.heavy?5.5:3.8;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.72,.72);ctx.stroke();
      ctx.strokeStyle='rgba(255,255,255,.55)';ctx.lineWidth=1.2;ctx.beginPath();ctx.ellipse(2,0,w*.76,h*.76,0,-.72,.72);ctx.stroke();
    }else if(p.cls==='archer'){
      ctx.strokeStyle='rgba(170,235,170,.20)';ctx.lineWidth=p.heavy?7:4;ctx.beginPath();ctx.moveTo(-38,0);ctx.lineTo(-11,0);ctx.stroke();
      ctx.strokeStyle='rgba(220,255,223,.98)';ctx.lineWidth=p.heavy?3.6:2.3;ctx.beginPath();ctx.moveTo(-18,0);ctx.lineTo(17,0);ctx.stroke();
      ctx.fillStyle='rgba(225,255,228,.98)';ctx.beginPath();ctx.moveTo(22,0);ctx.lineTo(10,-6);ctx.lineTo(12,0);ctx.lineTo(10,6);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(140,220,150,.95)';ctx.beginPath();ctx.moveTo(-16,0);ctx.lineTo(-24,-5);ctx.lineTo(-21,0);ctx.lineTo(-24,5);ctx.closePath();ctx.fill();
      if(p.heavy){ctx.globalAlpha*=.7;ctx.strokeStyle='rgba(210,255,215,.7)';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-15,-7);ctx.lineTo(17,-7);ctx.moveTo(-15,7);ctx.lineTo(17,7);ctx.stroke()}
    }else{
      const r=(p.heavy?13:9)+(p.skillPower?3:0);
      ctx.rotate(-ang);
      const grd=ctx.createRadialGradient(0,0,1,0,0,r+8);
      grd.addColorStop(0,'rgba(255,255,255,.98)');grd.addColorStop(.28,'rgba(230,210,255,.96)');grd.addColorStop(1,'rgba(170,120,255,0)');
      ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r+8,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle='rgba(235,218,255,.72)';ctx.lineWidth=1.5;
      for(let i=0;i<3;i++){const rr0=r+5+i*4+2*Math.sin(t*Math.PI+i);ctx.beginPath();ctx.arc(0,0,rr0,(i+nowShim())*.8,(i+nowShim())*.8+Math.PI*1.25);ctx.stroke()}
      ctx.fillStyle='rgba(236,218,255,.28)';ctx.beginPath();ctx.arc(-18,0,r*.45,0,Math.PI*2);ctx.fill()
    }
    ctx.restore()
  }
}

function visualImpact(p,m,now,local){
  if(!m)return false;
  const critical=p.tier==='CRITICAL',perfect=critical||p.tier==='PERFECT'||p.tier==='SUPER',good=perfect||p.tier==='GOOD'||p.tier==='GREAT';
  const d=MONSTER_TYPES[m.type];
  const actual=Math.max(1,Math.round(p.damage*d.armor));
  m.hp-=actual;m.hitFlash=1;
  const knockBase=local?(critical?W*.047:perfect?W*.024:good?W*.013:W*.006):(critical?W*.011:perfect?W*.007:good?W*.004:W*.002);
  const kMul=local?knockMultiplier(p):1;
  m.x=Math.min(W*.985,m.x+knockBase*d.knockResist*kMul);
  if(local&&(critical||perfect)){S.shakeUntil=now+(critical?145:95);S.shakeMag=critical?4.8:2.8}
  if(local)S.flash=critical?.9:perfect?.45:.12;
  const a=monsterAimPoint(m);const impactRgb=classColor(p.cls);
  addParticles(a.x,a.y,critical?22:perfect?15:good?9:6,critical?1.28:perfect?1.08:1,impactRgb,true);
  addParticles(a.x,a.y,critical?10:perfect?7:good?4:2,critical?1.18:1,impactRgb,false);
  S.pulses.push({x:a.x,y:a.y,age:0,life:critical?.36:perfect?.27:.20,maxR:critical?112:perfect?78:55,rgb:impactRgb});
  addFloat(String(actual),a.x,a.y-H*.035,local?(critical||p.procCrit?42:perfect?32:good?27:22):17,local&&(critical||p.procCrit)?'critical':'damage');
  if(p.procCrit)addFloat('PROC CRIT',a.x,a.y-H*.085,14,'gain');
  if(m.hp<=0){m.dead=true;S.kills++;S.stageKills++;if(local){S.gold+=d.reward;addFloat(`COIN +${d.reward}`,a.x,a.y-H*.08,12,'gain')}}
  return true;
}
