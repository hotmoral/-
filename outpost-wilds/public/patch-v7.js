/* Outpost Wilds V7: movement-only controls, auto action priority, horizontal-facing survivor, staged construction. */

/* V5 compensated inputs for an older zone-speed server. V7 server owns one stable speed curve, so send raw movement. */
send=function(m){return v5RawSend(m);};

function v7Facing(p){return p?.facing===-1?-1:1;}
function v7CargoVisual(p,s){
  if(!p.carry)return;
  const face=v7Facing(p),bx=s.x-face*21,by=s.y+7;
  ctx.save();ctx.translate(bx,by);
  ctx.fillStyle='#252820dd';v4Rounded(-15,-16,29,33,8);ctx.fill();ctx.strokeStyle='#8c7958';ctx.lineWidth=2;ctx.stroke();
  const woodN=Math.min(4,Math.ceil((p.wood||0)/8));
  for(let i=0;i<woodN;i++){const yy=10-i*6;const im=v5Assets.wood;if(im?.complete)ctx.drawImage(im,-17,yy-8,28,16);}
  const stoneN=Math.min(3,Math.ceil((p.stone||0)/9));
  for(let i=0;i<stoneN;i++){const im=v5Assets.stone;if(im?.complete)ctx.drawImage(im,-15+i*7,-20-(i%2)*4,18,18);}
  const meatN=Math.min(2,Math.ceil((p.meat||0)/10));
  for(let i=0;i<meatN;i++){const im=v5Assets.meat;if(im?.complete)ctx.drawImage(im,2+i*5,-18-i*5,18,18);}
  ctx.restore();
}
drawCargo=function(p,s){v7CargoVisual(p,s);};

drawPlayer=function(p,isMe,t){
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py),phase=movePhase.get(p.id)||0;
  const moving=isMe?Math.hypot(input.x,input.y)>.04:true,bob=moving?Math.sin(phase)*1.25:0,face=v7Facing(p);
  shadow(s.x,s.y+27,23,8,.30);v7CargoVisual(p,s);
  ctx.save();ctx.translate(s.x,s.y+bob);ctx.scale(face,1);
  const frame=moving&&Math.sin(phase)>0?v5Assets.survivorB:v5Assets.survivorA;
  if(frame?.complete)ctx.drawImage(frame,-35,-49,70,88);
  const swing=attackFx.get(p.id);let sw=0;if(swing&&!swing.ranged){sw=(.34-swing.t)/.34;sw=Math.sin(sw*Math.PI)*1.12;}
  ctx.translate(0,-3);drawWeapon(p,sw);ctx.restore();
  if(isMe){circle(s.x,s.y+3,29,null,'#fff9',1.5);circle(s.x,s.y+3,35,null,'#9bd8c028',1);}
  ctx.save();ctx.textAlign='center';ctx.shadowColor='#000';ctx.shadowBlur=5;ctx.font='700 10px sans-serif';ctx.fillStyle='#fff';ctx.fillText(p.name,s.x,s.y-45);ctx.shadowBlur=0;drawHealth(s.x,s.y-38,p.hp/p.maxHp,43);ctx.restore();
};

/* Target cue: one selected action at a time. Enemy > resource > pad/facility. */
const v7OldEnemy=drawEnemy;
drawEnemy=function(e,t){v7OldEnemy(e,t);const p=myPlayer();if(p?.autoTarget?.kind==='enemy'&&p.autoTarget.id===e.id){const rr=v4Enemies.get(e.id),s=worldToScreen(rr?.x??e.x,rr?.y??e.y);ctx.save();ctx.setLineDash([5,5]);circle(s.x,s.y+2,e.r+12,null,'#ffb071bb',2);ctx.setLineDash([]);ctx.restore();}};
const v7OldNode=drawNode;
drawNode=function(n){v7OldNode(n);const p=myPlayer();if(p?.autoTarget?.kind==='resource'&&p.autoTarget.id===n.id){const s=worldToScreen(n.x,n.y);ctx.save();ctx.setLineDash([4,5]);circle(s.x,s.y,n.r+10,null,'#e9d79eaa',1.5);ctx.setLineDash([]);ctx.restore();}};

function v7Scaffold(pad,q){
  if(pad.complete||pad.locked||q<=0)return;
  const s=worldToScreen(pad.x,pad.y),w=(pad.size||104)*.72,h=54;
  ctx.save();ctx.translate(s.x,s.y-3);ctx.globalAlpha=.88;
  ctx.strokeStyle='#b78955';ctx.lineWidth=4;ctx.lineCap='round';
  const posts=q<.28?2:q<.58?3:4;
  for(let i=0;i<posts;i++){const x=-w/2+i*(w/(posts-1||1));ctx.beginPath();ctx.moveTo(x,h*.34);ctx.lineTo(x,-h*.35);ctx.stroke();}
  if(q>.22){ctx.strokeStyle='#93683f';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-w/2,-h*.12);ctx.lineTo(w/2,-h*.12);ctx.stroke();}
  if(q>.48){ctx.fillStyle='#75543acb';v4Rounded(-w*.38,-h*.18,w*.76,h*.38,5);ctx.fill();ctx.strokeStyle='#b58b59';ctx.lineWidth=2;ctx.stroke();}
  if(q>.72){ctx.fillStyle='#3d3329e8';ctx.beginPath();ctx.moveTo(-w*.48,-h*.18);ctx.lineTo(0,-h*.58);ctx.lineTo(w*.48,-h*.18);ctx.closePath();ctx.fill();}
  if(q>.9){ctx.fillStyle='#e6bd68';circle(0,-h*.62,4,'#e6bd68');}
  ctx.restore();
}
const v7OldPad=v6DrawPad;
v6DrawPad=function(pad){v7OldPad(pad);v7Scaffold(pad,v6PadProgress(pad));};

function v7DrawStorage(x,y){ctx.save();ctx.translate(x,y);shadow(0,18,42,13,.28);ctx.fillStyle='#694a31';v4Rounded(-38,-19,76,45,8);ctx.fill();ctx.strokeStyle='#ad8456';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#3d3127';ctx.beginPath();ctx.moveTo(-43,-18);ctx.lineTo(0,-42);ctx.lineTo(43,-18);ctx.closePath();ctx.fill();ctx.fillStyle='#b89059';ctx.fillRect(-5,-3,10,29);ctx.restore();}
function v7DrawFarm(x,y){ctx.save();ctx.translate(x,y);shadow(0,18,48,12,.22);ctx.fillStyle='#6d5338';ctx.beginPath();ctx.ellipse(0,8,49,22,0,0,Math.PI*2);ctx.fill();for(let i=-3;i<=3;i++){ctx.strokeStyle='#6f9a55';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(i*12,17);ctx.quadraticCurveTo(i*12-5,-3,i*12-2,-15);ctx.stroke();ctx.beginPath();ctx.moveTo(i*12,10);ctx.quadraticCurveTo(i*12+6,-2,i*12+5,-10);ctx.stroke();}ctx.restore();}
function v7DrawInfirmary(x,y){ctx.save();ctx.translate(x,y);shadow(0,19,40,12,.26);ctx.fillStyle='#74684e';ctx.beginPath();ctx.moveTo(-38,22);ctx.lineTo(0,-31);ctx.lineTo(38,22);ctx.closePath();ctx.fill();ctx.strokeStyle='#b9a77b';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#e5d9bc';ctx.fillRect(-5,-17,10,28);ctx.fillRect(-14,-8,28,10);ctx.restore();}
function v7DrawWall(x,y){ctx.save();ctx.translate(x,y);shadow(0,18,54,13,.26);for(let i=-4;i<=4;i++){ctx.fillStyle=i%2?'#6c5a43':'#7b684d';ctx.fillRect(i*11-5,-27+(Math.abs(i)%2)*4,10,49);ctx.fillStyle='#a88a5c';ctx.beginPath();ctx.moveTo(i*11-5,-27+(Math.abs(i)%2)*4);ctx.lineTo(i*11,-37+(Math.abs(i)%2)*4);ctx.lineTo(i*11+5,-27+(Math.abs(i)%2)*4);ctx.fill();}ctx.restore();}
function v7DrawTurret(x,y,outer=false){ctx.save();ctx.translate(x,y);shadow(0,18,39,13,.3);ctx.fillStyle=outer?'#4d5955':'#555d58';ctx.beginPath();ctx.arc(0,8,31,0,Math.PI*2);ctx.fill();ctx.fillStyle=outer?'#7b8a82':'#727c75';v4Rounded(-22,-16,44,29,10);ctx.fill();ctx.fillStyle='#303735';v4Rounded(4,-10,46,9,4);ctx.fill();circle(-7,-3,6,outer?'#8dd0b0':'#d89e51');ctx.restore();}

v6DrawBuiltFacilities=function(){if(!snap?.facilities)return;const f=snap.facilities;
 if(f.workshop){const s=worldToScreen(1575,1900);v6DrawWorkshop(s.x,s.y)}
 if(f.storage){const s=worldToScreen(1510,1770);v7DrawStorage(s.x,s.y)}
 if(f.farm){const s=worldToScreen(1540,2070);v7DrawFarm(s.x,s.y)}
 if(f.watchtower){const s=worldToScreen(2040,1670);drawTower(s.x,s.y)}
 if(f.forge){const s=worldToScreen(1580,1645);v6DrawForge(s.x,s.y)}
 if(f.infirmary){const s=worldToScreen(2090,1780);v7DrawInfirmary(s.x,s.y)}
 if(f.wall){const s=worldToScreen(2200,2020);v7DrawWall(s.x,s.y)}
 if(f.turret){const s=worldToScreen(2050,1910);v7DrawTurret(s.x,s.y,false)}
 if(f.turret2){const s=worldToScreen(2070,2150);v7DrawTurret(s.x,s.y,true)}
};

const v7OldHud=updateHud;
updateHud=function(){v7OldHud();const p=myPlayer();if(!p)return;const hint=$('contextHint');if(p.autoTarget?.kind==='enemy'){hint.textContent='⚔ 가까운 위협 자동 공격';hint.className='show autoAction';}else if(p.autoTarget?.kind==='resource'){hint.textContent='✦ 가까운 자원 자동 채집';hint.className='show autoAction';}};
