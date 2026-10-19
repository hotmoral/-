function drawCharacter(slot,cls,local=false){const b=charBase(slot),rgb=classColor(cls),charged=local&&isHeavy();ctx.save();ctx.translate(b.x+(local?S.playerKick:0),b.y);ctx.scale(b.scale,b.scale);ctx.strokeStyle=local?(charged?`rgba(${rgb},.95)`:'rgba(255,255,255,.55)'):'rgba(255,255,255,.16)';ctx.lineWidth=local?3:2;ctx.beginPath();ctx.ellipse(0,22,local?36:29,local?11:8,0,0,Math.PI*2);ctx.stroke();
if(cls==='knight'){ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(0,-48,16,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#8799ad':'#657586';rr(-14,-33,28,47,7);ctx.fill();ctx.strokeStyle=charged?'#ffd36a':'#e7eef5';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(9,-22);ctx.lineTo(34,-31);ctx.lineTo(48,-22);ctx.stroke()}
else if(cls==='rogue'){ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-2,-43,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#708398':'#5b6a79';rr(-11,-30,22,39,6);ctx.fill();ctx.strokeStyle='#c9ecff';ctx.lineWidth=3.5;ctx.beginPath();ctx.moveTo(6,-22);ctx.lineTo(31,-16);ctx.moveTo(4,-13);ctx.lineTo(28,-3);ctx.stroke()}
else if(cls==='tank'){ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-5,-48,15,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#71879a':'#5d6e7c';rr(-22,-34,38,50,5);ctx.fill();ctx.fillStyle='#92a9ba';rr(13,-35,21,49,8);ctx.fill();ctx.strokeStyle='#d9f3ff';ctx.lineWidth=3;ctx.beginPath();ctx.arc(23,-10,13,-1.2,1.2);ctx.stroke()}
else if(cls==='archer'){ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-45,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#718d78':'#5d7463';ctx.beginPath();ctx.moveTo(-13,-31);ctx.lineTo(11,-31);ctx.lineTo(7,13);ctx.lineTo(-9,13);ctx.closePath();ctx.fill();ctx.strokeStyle='#bceec1';ctx.lineWidth=3;ctx.beginPath();ctx.arc(24,-17,20,-1.3,1.25);ctx.stroke();ctx.strokeStyle='#d8f7dc';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(29,-36);ctx.lineTo(29,2);ctx.moveTo(8,-17);ctx.lineTo(48,-17);ctx.stroke()}
else{ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-47,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#7f7094':'#665a77';ctx.beginPath();ctx.moveTo(-15,-32);ctx.lineTo(11,-32);ctx.lineTo(16,15);ctx.lineTo(-18,15);ctx.closePath();ctx.fill();ctx.strokeStyle='#d8c2ff';ctx.lineWidth=3.5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(8,-20);ctx.lineTo(38,-35);ctx.stroke();ctx.fillStyle='#e9dcff';ctx.beginPath();ctx.arc(41,-37,6,0,Math.PI*2);ctx.fill()}
if(local){const wp=cls==='knight'?{x:53,y:-20}:cls==='rogue'?{x:47,y:-18}:cls==='tank'?{x:46,y:-10}:cls==='archer'?{x:51,y:-20}:{x:45,y:-28},r=4+S.charge*3+(charged?4:0);if(cls==='tank'||cls==='mage'){ctx.strokeStyle=`rgba(${rgb},${.25+S.charge*.22})`;ctx.lineWidth=3;ctx.beginPath();ctx.arc(wp.x,wp.y,r,0,Math.PI*2);ctx.stroke()}else if(cls==='archer'){ctx.strokeStyle=`rgba(${rgb},${.28+S.charge*.2})`;ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(wp.x-r,wp.y+r*.45);ctx.lineTo(wp.x+r,wp.y-r*.45);ctx.stroke()}else{ctx.fillStyle=`rgba(${rgb},${.22+S.charge*.23})`;ctx.shadowBlur=8+S.charge*5;ctx.shadowColor=`rgba(${rgb},.72)`;ctx.beginPath();ctx.arc(wp.x,wp.y,r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0}}
ctx.fillStyle=local?'#fff':'rgba(255,255,255,.65)';ctx.beginPath();ctx.moveTo(0,-78);ctx.lineTo(-6,-68);ctx.lineTo(6,-68);ctx.closePath();ctx.fill();ctx.restore();ctx.fillStyle=local?'rgba(255,255,255,.76)':'rgba(255,255,255,.34)';ctx.font=`${local?'800':'700'} 9px system-ui`;ctx.textAlign='center';ctx.fillText(local?'YOU':`CPU ${slot}`,b.x,b.y+H*.045)}
function drawMonsterShape(m){
  const d=MONSTER_TYPES[m.type],s=d.size*(m.scaleMul||1);
  ctx.save();ctx.translate(m.x,m.y);ctx.scale(s,s);

  if(m.hitFlash>.08){ctx.shadowBlur=18;ctx.shadowColor='rgba(255,255,255,.75)'}
  if(m.boss){ctx.strokeStyle='rgba(255,211,106,.38)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,-22,48,0,Math.PI*2);ctx.stroke()}

  if(m.type==='grunt'){
    ctx.fillStyle=m.hitFlash>.15?'#9ba9b6':'#586673';
    ctx.beginPath();ctx.ellipse(0,-18,30,34,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#758392';
    ctx.beginPath();ctx.moveTo(-18,-42);ctx.lineTo(-10,-56);ctx.lineTo(-4,-40);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(18,-42);ctx.lineTo(10,-56);ctx.lineTo(4,-40);ctx.closePath();ctx.fill();
    ctx.fillStyle='#0b0f14';ctx.beginPath();ctx.arc(-9,-23,4,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(9,-23,4,0,Math.PI*2);ctx.fill();
  }else if(m.type==='runner'){
    ctx.fillStyle=m.hitFlash>.15?'#a8b6c3':'#657482';
    ctx.beginPath();ctx.ellipse(0,-12,23,20,-.15,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#8795a2';
    ctx.beginPath();ctx.moveTo(17,-14);ctx.lineTo(34,-5);ctx.lineTo(18,0);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#9eacb8';ctx.lineWidth=5;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(-11,2);ctx.lineTo(-20,20);ctx.moveTo(6,4);ctx.lineTo(17,21);ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.17)';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(31,-5);ctx.lineTo(50,-5);ctx.moveTo(27,4);ctx.lineTo(45,8);ctx.stroke();
  }else if(m.type==='brute'){
    ctx.fillStyle=m.hitFlash>.15?'#929eaa':'#4e5a65';
    rr(-38,-64,76,76,10);ctx.fill();
    ctx.fillStyle='#687681';rr(-29,-54,58,25,8);ctx.fill();
    ctx.fillStyle='#0b0f14';ctx.beginPath();ctx.arc(-14,-42,5,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(14,-42,5,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='#73808b';ctx.lineWidth=9;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-30,3);ctx.lineTo(-38,23);ctx.moveTo(30,3);ctx.lineTo(38,23);ctx.stroke();
  }else if(m.type==='shield'){
    ctx.fillStyle=m.hitFlash>.15?'#a3b0bd':'#5e6d7a';
    ctx.beginPath();ctx.ellipse(-5,-20,29,34,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#8a99a7';
    rr(-37,-52,18,62,8);ctx.fill();
    ctx.strokeStyle='#c1ccd6';ctx.lineWidth=3;rr(-37,-52,18,62,8);ctx.stroke();
    ctx.fillStyle='#0b0f14';ctx.beginPath();ctx.arc(3,-26,4,0,Math.PI*2);ctx.fill();
  }else{
    ctx.fillStyle=m.hitFlash>.15?'#b2bec9':'#697987';
    ctx.beginPath();ctx.moveTo(0,-45);ctx.lineTo(25,-18);ctx.lineTo(0,8);ctx.lineTo(-25,-18);ctx.closePath();ctx.fill();
    ctx.fillStyle='#8796a3';
    ctx.beginPath();ctx.moveTo(-18,-20);ctx.lineTo(-42,-32);ctx.lineTo(-28,-7);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(18,-20);ctx.lineTo(42,-32);ctx.lineTo(28,-7);ctx.closePath();ctx.fill();
    ctx.fillStyle='#0b0f14';ctx.beginPath();ctx.arc(0,-22,5,0,Math.PI*2);ctx.fill();
  }

  // HP bar, only emphasized after damage.
  const ratio=clamp(m.hp/m.maxHp,0,1);
  const bw=52,bh=5;
  ctx.fillStyle='rgba(0,0,0,.45)';rr(-bw/2,-76,bw,bh,3);ctx.fill();
  ctx.fillStyle=ratio>.5?'rgba(214,231,238,.72)':ratio>.25?'rgba(255,211,106,.82)':'rgba(255,120,120,.86)';
  rr(-bw/2,-76,bw*ratio,bh,3);ctx.fill();

  ctx.restore();
}
function drawMonsters(){
  const ordered=[...S.monsters].filter(m=>!m.dead).sort((a,b)=>a.y-b.y);
  for(const m of ordered)drawMonsterShape(m)
}
function drawChargeMotes(){for(const m of S.chargeMotes){if(m.age<0)continue;ctx.save();ctx.globalAlpha=.85;ctx.fillStyle=`rgba(${m.rgb},.95)`;ctx.shadowBlur=9;ctx.shadowColor=`rgba(${m.rgb},.7)`;if(m.cls==='rogue'){ctx.translate(m.x,m.y);ctx.rotate(-.6);ctx.fillRect(-m.size*1.5,-m.size*.4,m.size*3,m.size*.8)}else if(m.cls==='tank'||m.cls==='mage'){ctx.strokeStyle=`rgba(${m.rgb},.86)`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(m.x,m.y,m.cls==='mage'?m.size*1.35:m.size,0,Math.PI*2);ctx.stroke()}else if(m.cls==='archer'){ctx.strokeStyle=`rgba(${m.rgb},.9)`;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(m.x-m.size*2,m.y+m.size*.6);ctx.lineTo(m.x+m.size*2,m.y-m.size*.6);ctx.stroke()}else{ctx.beginPath();ctx.arc(m.x,m.y,m.size,0,Math.PI*2);ctx.fill()}ctx.restore()}}