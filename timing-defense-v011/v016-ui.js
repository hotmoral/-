// Timing Defense v0.16 — six-slot learned-skill strip below Timing Square.
function v016DrawSkillGlyph(cx,cy,r,idx,rgb,active){
  ctx.save();ctx.translate(cx,cy);ctx.strokeStyle=active?`rgba(${rgb},.96)`:'rgba(255,255,255,.18)';ctx.fillStyle=ctx.strokeStyle;ctx.lineWidth=Math.max(1.1,r*.18);ctx.lineCap='round';ctx.lineJoin='round';
  if(idx===0){ctx.beginPath();ctx.arc(0,0,r*.42,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(-r*.62,r*.35);ctx.lineTo(r*.62,-r*.35);ctx.stroke()}
  else if(idx===1){ctx.beginPath();ctx.moveTo(-r*.55,r*.45);ctx.lineTo(r*.55,-r*.45);ctx.moveTo(-r*.25,-r*.55);ctx.lineTo(r*.55,r*.25);ctx.stroke()}
  else if(idx===2){ctx.beginPath();ctx.moveTo(0,-r*.62);ctx.lineTo(r*.58,0);ctx.lineTo(0,r*.62);ctx.lineTo(-r*.58,0);ctx.closePath();ctx.stroke()}
  else if(idx===3){ctx.beginPath();ctx.arc(-r*.22,0,r*.42,-1.15,1.15);ctx.stroke();ctx.beginPath();ctx.arc(r*.22,0,r*.42,Math.PI-1.15,Math.PI+1.15);ctx.stroke()}
  else if(idx===4){for(let a=0;a<4;a++){const q=a*Math.PI/2;ctx.beginPath();ctx.moveTo(Math.cos(q)*r*.22,Math.sin(q)*r*.22);ctx.lineTo(Math.cos(q)*r*.68,Math.sin(q)*r*.68);ctx.stroke()}ctx.beginPath();ctx.arc(0,0,r*.18,0,Math.PI*2);ctx.fill()}
  else{for(let a=0;a<5;a++){const q=-Math.PI/2+a*Math.PI*2/5,q2=q+Math.PI/5;const p1=[Math.cos(q)*r*.68,Math.sin(q)*r*.68],p2=[Math.cos(q2)*r*.28,Math.sin(q2)*r*.28];if(a===0){ctx.beginPath();ctx.moveTo(...p1)}else ctx.lineTo(...p1);ctx.lineTo(...p2)}ctx.closePath();ctx.stroke()}
  ctx.restore()
}

drawSkillIcon=function(now){
  const g=squareGeom(),rgb=classColor(),gap=3,total=g.size,slot=Math.max(11,(total-gap*5)/6),used=slot*6+gap*5,start=g.x+(g.size-used)/2,y=g.y+g.size+12;
  const count=v016SkillCount();ctx.save();
  for(let i=0;i<6;i++){
    const x=start+i*(slot+gap),active=i<count,just=active&&V016_UNLOCKS[i]===S.v016SkillNoticeLevel&&now<S.skillNoticeUntil,pulse=just?(.55+.45*Math.sin(now*.018)):0;
    if(just){ctx.shadowBlur=10+7*pulse;ctx.shadowColor=`rgba(${rgb},.92)`}
    ctx.fillStyle=active?`rgba(${rgb},.10)`:'rgba(0,0,0,.48)';rr(x,y,slot,slot,Math.max(3,slot*.22));ctx.fill();
    ctx.strokeStyle=active?`rgba(${rgb},${just?.98:.58})`:'rgba(255,255,255,.10)';ctx.lineWidth=just?2:1;rr(x,y,slot,slot,Math.max(3,slot*.22));ctx.stroke();ctx.shadowBlur=0;
    v016DrawSkillGlyph(x+slot/2,y+slot/2,slot*.42,i,rgb,active)
  }
  ctx.restore()
};
