/* Outpost Wilds V8: exact auto-action range boundaries and active build-pad feedback. */
const V8_ATTACK_RANGES={1:120,2:132,3:350,4:410,5:455};
const V8_GATHER_RANGE=112;
let v8PulseT=0;

function v8MyRenderPos(){
  const p=myPlayer();if(!p)return null;
  const r=v4Players.get(p.id);return {p,x:r?.x??p.x,y:r?.y??p.y};
}
function v8NearEnemy(p,range){for(const e of snap?.enemies||[]){const r=v4Enemies.get(e.id);const x=r?.x??e.x,y=r?.y??e.y;if(Math.hypot(x-p.x,y-p.y)<=range+34)return true;}return false;}
function v8NearNode(p,range){if(p.carry>=p.carryCap)return false;for(const n of snap?.nodes||[])if(Math.hypot(n.x-p.x,n.y-p.y)<=range+36)return true;return false;}
function v8RangeRing(s,r,color,alpha,dashed=false,width=1.5){
  ctx.save();ctx.globalAlpha=alpha;ctx.strokeStyle=color;ctx.lineWidth=width;if(dashed)ctx.setLineDash([8,8]);
  ctx.beginPath();ctx.arc(s.x,s.y+3,r,0,Math.PI*2);ctx.stroke();
  ctx.globalAlpha=alpha*.12;ctx.fillStyle=color;ctx.beginPath();ctx.arc(s.x,s.y+3,r,0,Math.PI*2);ctx.fill();ctx.restore();
}
function v8DrawActionRanges(p,s){
  if(p.id!==meId)return;
  const ar=V8_ATTACK_RANGES[p.gearLevel]||120,enemyHot=v8NearEnemy(p,ar),nodeHot=v8NearNode(p,V8_GATHER_RANGE);
  const pulse=.82+.18*Math.sin(v8PulseT*5.2);
  /* Gather first, attack second so the combat boundary stays readable when melee radii are close. */
  v8RangeRing(s,V8_GATHER_RANGE,'#9fcf78',nodeHot?.68:.24,true,nodeHot?2.2:1.3);
  v8RangeRing(s,ar,'#e88967',enemyHot?.78*pulse:.28,false,enemyHot?2.5:1.4);
  /* Small non-text badges: resource icon at gather radius, weapon notch at attack radius. */
  const wi=v5Assets.wood;if(wi?.complete){ctx.save();ctx.globalAlpha=nodeHot?.9:.48;ctx.drawImage(wi,s.x-11,s.y+3-V8_GATHER_RANGE-11,22,22);ctx.restore();}
  ctx.save();ctx.translate(s.x,s.y+3-ar);ctx.globalAlpha=enemyHot?.95:.52;ctx.fillStyle='#e9a07f';ctx.beginPath();ctx.moveTo(-3,-10);ctx.lineTo(3,-10);ctx.lineTo(2,5);ctx.lineTo(7,10);ctx.lineTo(-7,10);ctx.lineTo(-2,5);ctx.closePath();ctx.fill();ctx.restore();
}

/* Put the boundaries on the ground immediately before the local survivor. */
const v8OldDrawPlayer=drawPlayer;
drawPlayer=function(p,isMe,t){
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py);
  if(isMe)v8DrawActionRanges({...p,x:px,y:py},s);
  v8OldDrawPlayer(p,isMe,t);
};

function v8InsidePad(p,pad){const half=(pad.size||104)*.52;return Math.abs(p.x-pad.x)<=half&&Math.abs(p.y-pad.y)<=half;}
function v8NearPad(p,pad){const half=(pad.size||104)*.52+34;return Math.abs(p.x-pad.x)<=half&&Math.abs(p.y-pad.y)<=half;}
const v8OldPad=v6DrawPad;
v6DrawPad=function(pad){
  v8OldPad(pad);
  if(pad.complete)return;
  const me=v8MyRenderPos();if(!me)return;
  const local={...me.p,x:me.x,y:me.y},inside=v8InsidePad(local,pad),near=v8NearPad(local,pad),s=worldToScreen(pad.x,pad.y),w=pad.size||104,h=82;
  if(!inside&&!near)return;
  ctx.save();ctx.translate(s.x,s.y);const pulse=.72+.28*Math.sin(v8PulseT*5.5);
  ctx.strokeStyle=pad.locked?'rgba(150,154,151,.55)':inside?`rgba(245,201,112,${.76+.2*pulse})`:'rgba(226,187,105,.46)';
  ctx.lineWidth=inside?3:1.8;ctx.setLineDash(inside?[]:[7,6]);v4Rounded(-w/2-5,-h/2-5,w+10,h+10,15);ctx.stroke();
  if(inside&&!pad.locked){ctx.globalAlpha=.12+.06*pulse;ctx.fillStyle='#f2ca76';v4Rounded(-w/2-5,-h/2-5,w+10,h+10,15);ctx.fill();}
  ctx.restore();
};

/* Reinforce selected auto target without adding text clutter. */
const v8OldEnemy=drawEnemy;
drawEnemy=function(e,t){v8OldEnemy(e,t);const p=myPlayer();if(p?.autoTarget?.kind==='enemy'&&p.autoTarget.id===e.id){const rr=v4Enemies.get(e.id),s=worldToScreen(rr?.x??e.x,rr?.y??e.y);ctx.save();ctx.globalAlpha=.55+.35*Math.sin(v8PulseT*7)**2;circle(s.x,s.y+2,e.r+17,null,'#ff9b74',3);ctx.restore();}};
const v8OldNode=drawNode;
drawNode=function(n){v8OldNode(n);const p=myPlayer();if(p?.autoTarget?.kind==='resource'&&p.autoTarget.id===n.id){const s=worldToScreen(n.x,n.y);ctx.save();ctx.globalAlpha=.5+.3*Math.sin(v8PulseT*7)**2;circle(s.x,s.y,n.r+15,null,'#b8df8e',2.5);ctx.restore();}};

/* One RAF only updates the visual pulse clock; main game render remains unchanged. */
(function v8Clock(t){v8PulseT=t/1000;requestAnimationFrame(v8Clock)})(performance.now());
