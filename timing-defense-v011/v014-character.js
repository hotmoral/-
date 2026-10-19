// Timing Defense v0.14 patch
function drawCharacter(slot,cls,local=false){
  const b=charBase(slot),rgb=classColor(cls),charged=local&&isHeavy();
  ctx.save();ctx.translate(b.x+(local?S.playerKick:0),b.y);ctx.scale(b.scale,b.scale);
  ctx.strokeStyle=local?(charged?`rgba(${rgb},.98)`:'rgba(255,255,255,.52)'):'rgba(255,255,255,.16)';
  ctx.lineWidth=local?3:2;ctx.beginPath();ctx.ellipse(0,22,local?36:29,local?11:8,0,0,Math.PI*2);ctx.stroke();
  if(cls==='knight'){
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(0,-48,16,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=local?'#8799ad':'#657586';rr(-14,-33,28,47,7);ctx.fill();
    ctx.strokeStyle='#51606f';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(8,-20);ctx.lineTo(48,-30);ctx.stroke();
    ctx.strokeStyle=charged?'#ffe18a':'#eef5fb';ctx.lineWidth=3.2;ctx.beginPath();ctx.moveTo(11,-22);ctx.lineTo(49,-31);ctx.stroke();
    ctx.strokeStyle='#c8a95d';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(13,-14);ctx.lineTo(9,-29);ctx.stroke();
  }else if(cls==='rogue'){
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-2,-43,13,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=local?'#708398':'#5b6a79';rr(-11,-30,22,39,6);ctx.fill();
    for(const [ox,oy,rot] of [[6,-21,-.15],[5,-11,.2]]){
      ctx.save();ctx.translate(ox,oy);ctx.rotate(rot);ctx.fillStyle='#e5f7ff';ctx.beginPath();ctx.moveTo(0,-2);ctx.lineTo(29,0);ctx.lineTo(0,3);ctx.closePath();ctx.fill();ctx.fillStyle='#6fa9c5';ctx.fillRect(-2,-3,7,6);ctx.restore()
    }
  }else if(cls==='tank'){
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-5,-48,15,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#71879a':'#5d6e7c';rr(-22,-34,38,50,5);ctx.fill();
    ctx.fillStyle='#61798b';rr(12,-39,25,54,10);ctx.fill();ctx.strokeStyle='#d9f3ff';ctx.lineWidth=3;rr(12,-39,25,54,10);ctx.stroke();ctx.strokeStyle='rgba(160,225,255,.72)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(24,-12,10,-1.25,1.25);ctx.stroke();
  }else if(cls==='archer'){
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-45,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#718d78':'#5d7463';ctx.beginPath();ctx.moveTo(-13,-31);ctx.lineTo(11,-31);ctx.lineTo(7,13);ctx.lineTo(-9,13);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#7baa80';ctx.lineWidth=5;ctx.beginPath();ctx.arc(24,-17,21,-1.35,1.30);ctx.stroke();ctx.strokeStyle='#dbffe0';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(28,-37);ctx.lineTo(28,3);ctx.stroke();ctx.strokeStyle='#e8fff0';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(8,-17);ctx.lineTo(49,-17);ctx.stroke();ctx.fillStyle='#dffff0';ctx.beginPath();ctx.moveTo(52,-17);ctx.lineTo(43,-22);ctx.lineTo(43,-12);ctx.closePath();ctx.fill();
  }else{
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-47,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?'#7f7094':'#665a77';ctx.beginPath();ctx.moveTo(-15,-32);ctx.lineTo(11,-32);ctx.lineTo(16,15);ctx.lineTo(-18,15);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#7f6b9b';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(8,-19);ctx.lineTo(39,-37);ctx.stroke();ctx.strokeStyle='#dec9ff';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(9,-20);ctx.lineTo(39,-37);ctx.stroke();ctx.fillStyle='#eee2ff';ctx.shadowBlur=10;ctx.shadowColor='rgba(204,170,255,.8)';ctx.beginPath();ctx.arc(42,-39,7,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle='rgba(220,195,255,.8)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(42,-39,11,0,Math.PI*2);ctx.stroke();
  }
  if(local){
    const wp=cls==='knight'?{x:53,y:-20}:cls==='rogue'?{x:47,y:-18}:cls==='tank'?{x:46,y:-10}:cls==='archer'?{x:51,y:-20}:{x:45,y:-28},r=4+S.charge*3+(charged?4:0),pulse=.72+.28*Math.sin(performance.now()*.018);
    ctx.shadowBlur=charged?18:8+S.charge*4;ctx.shadowColor=`rgba(${rgb},.82)`;
    if(cls==='tank'||cls==='mage'){ctx.strokeStyle=`rgba(${rgb},${.28+S.charge*.20})`;ctx.lineWidth=charged?4:2.6;ctx.beginPath();ctx.arc(wp.x,wp.y,r*pulse,0,Math.PI*2);ctx.stroke()}
    else if(cls==='archer'){ctx.strokeStyle=`rgba(${rgb},${.30+S.charge*.18})`;ctx.lineWidth=charged?3.5:2.2;ctx.beginPath();ctx.moveTo(wp.x-r,wp.y+r*.45);ctx.lineTo(wp.x+r,wp.y-r*.45);ctx.stroke()}
    else{ctx.fillStyle=`rgba(${rgb},${.24+S.charge*.20})`;ctx.beginPath();ctx.arc(wp.x,wp.y,r*pulse,0,Math.PI*2);ctx.fill()}
    ctx.shadowBlur=0
  }
  ctx.fillStyle=local?'#fff':'rgba(255,255,255,.65)';ctx.beginPath();ctx.moveTo(0,-78);ctx.lineTo(-6,-68);ctx.lineTo(6,-68);ctx.closePath();ctx.fill();ctx.restore();
  ctx.fillStyle=local?'rgba(255,255,255,.76)':'rgba(255,255,255,.34)';ctx.font=`${local?'800':'700'} 9px system-ui`;ctx.textAlign='center';ctx.fillText(local?'YOU':`CPU ${slot}`,b.x,b.y+H*.045)
}
