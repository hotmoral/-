// Timing Defense v0.15 — class palette identity pass
(function(){
  const PALETTE={
    knight:{rgb:'255,196,74',body:'#b9943d',body2:'#e2c56f',metal:'#eef4f8',dark:'#66562b',accent:'#fff0b5'},
    rogue:{rgb:'166,170,176',body:'#34383e',body2:'#4b5057',metal:'#e5e8eb',dark:'#1d2025',accent:'#d85c5c'},
    tank:{rgb:'72,158,255',body:'#2f6fae',body2:'#478bd0',metal:'#dcecff',dark:'#24415f',accent:'#a9d8ff'},
    archer:{rgb:'144,219,139',body:'#718d78',body2:'#8bb18f',metal:'#e8fff0',dark:'#415f46',accent:'#dffff0'},
    mage:{rgb:'204,170,255',body:'#7f7094',body2:'#a48cc2',metal:'#eee2ff',dark:'#514461',accent:'#dec9ff'}
  };
  window.CLASS_PALETTE=PALETTE;
  classColor=function(c=S.playerClass){return (PALETTE[c]||PALETTE.knight).rgb};

  const css=document.createElement('style');
  css.textContent=`
    #classControls button[data-class="knight"].active{box-shadow:0 0 0 1px rgba(255,196,74,.75) inset,0 0 14px rgba(255,196,74,.18)}
    #classControls button[data-class="rogue"].active{box-shadow:0 0 0 1px rgba(166,170,176,.80) inset,0 0 14px rgba(166,170,176,.14)}
    #classControls button[data-class="tank"].active{box-shadow:0 0 0 1px rgba(72,158,255,.82) inset,0 0 14px rgba(72,158,255,.20)}
    #classControls button[data-class="archer"].active{box-shadow:0 0 0 1px rgba(144,219,139,.78) inset,0 0 14px rgba(144,219,139,.17)}
    #classControls button[data-class="mage"].active{box-shadow:0 0 0 1px rgba(204,170,255,.80) inset,0 0 14px rgba(204,170,255,.20)}
  `;
  document.head.appendChild(css);
})();

drawCharacter=function(slot,cls,local=false){
  const b=charBase(slot),pal=(window.CLASS_PALETTE||{})[cls]||window.CLASS_PALETTE.knight,rgb=pal.rgb,charged=local&&isHeavy();
  ctx.save();ctx.translate(b.x+(local?S.playerKick:0),b.y);ctx.scale(b.scale,b.scale);
  ctx.strokeStyle=local?(charged?`rgba(${rgb},.98)`:'rgba(255,255,255,.52)'):'rgba(255,255,255,.16)';
  ctx.lineWidth=local?3:2;ctx.beginPath();ctx.ellipse(0,22,local?36:29,local?11:8,0,0,Math.PI*2);ctx.stroke();

  if(cls==='knight'){
    ctx.fillStyle=pal.metal;ctx.beginPath();ctx.arc(0,-48,16,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=local?pal.body2:'#766b4a';rr(-15,-34,30,48,7);ctx.fill();
    ctx.fillStyle=pal.body;rr(-12,-31,7,40,4);ctx.fill();
    ctx.strokeStyle=pal.dark;ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(8,-20);ctx.lineTo(48,-30);ctx.stroke();
    ctx.strokeStyle=charged?'#fff0a8':pal.metal;ctx.lineWidth=3.5;ctx.beginPath();ctx.moveTo(11,-22);ctx.lineTo(50,-31);ctx.stroke();
    ctx.strokeStyle=pal.body;ctx.lineWidth=4.5;ctx.beginPath();ctx.moveTo(13,-14);ctx.lineTo(9,-29);ctx.stroke();
    ctx.strokeStyle=pal.accent;ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(-10,-30);ctx.lineTo(10,-30);ctx.stroke();
  }else if(cls==='rogue'){
    ctx.fillStyle='#25292e';ctx.beginPath();ctx.arc(-2,-43,14,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#3a3f45';ctx.beginPath();ctx.arc(-2,-44,11,Math.PI,Math.PI*2);ctx.fill();
    ctx.fillStyle=local?pal.body:pal.dark;rr(-12,-31,24,40,6);ctx.fill();
    ctx.fillStyle=pal.body2;rr(-9,-28,6,34,3);ctx.fill();
    ctx.strokeStyle='rgba(216,92,92,.72)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-8,3);ctx.lineTo(8,3);ctx.stroke();
    for(const [ox,oy,rot] of [[6,-21,-.15],[5,-11,.2]]){
      ctx.save();ctx.translate(ox,oy);ctx.rotate(rot);
      ctx.shadowBlur=charged?10:3;ctx.shadowColor='rgba(230,235,240,.65)';
      ctx.fillStyle=pal.metal;ctx.beginPath();ctx.moveTo(0,-2.6);ctx.lineTo(31,0);ctx.lineTo(0,3.3);ctx.closePath();ctx.fill();
      ctx.fillStyle='#8f959d';ctx.fillRect(-3,-3,8,6);
      ctx.strokeStyle='rgba(216,92,92,.88)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(3,2);ctx.lineTo(24,.7);ctx.stroke();ctx.restore()
    }
  }else if(cls==='tank'){
    ctx.fillStyle='#dcecff';ctx.beginPath();ctx.arc(-5,-48,15,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=local?pal.body:pal.dark;rr(-23,-35,39,51,5);ctx.fill();
    ctx.fillStyle=pal.body2;rr(-18,-31,12,43,4);ctx.fill();
    ctx.fillStyle='#2a5d8d';rr(12,-40,26,56,10);ctx.fill();
    ctx.strokeStyle=pal.metal;ctx.lineWidth=3.2;rr(12,-40,26,56,10);ctx.stroke();
    ctx.strokeStyle=`rgba(${rgb},.92)`;ctx.lineWidth=3;ctx.beginPath();ctx.arc(25,-12,10,-1.25,1.25);ctx.stroke();
    ctx.fillStyle=pal.accent;ctx.beginPath();ctx.arc(26,-12,3,0,Math.PI*2);ctx.fill();
  }else if(cls==='archer'){
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-45,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?pal.body:'#5d7463';ctx.beginPath();ctx.moveTo(-13,-31);ctx.lineTo(11,-31);ctx.lineTo(7,13);ctx.lineTo(-9,13);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#7baa80';ctx.lineWidth=5;ctx.beginPath();ctx.arc(24,-17,21,-1.35,1.30);ctx.stroke();ctx.strokeStyle='#dbffe0';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(28,-37);ctx.lineTo(28,3);ctx.stroke();ctx.strokeStyle=pal.metal;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(8,-17);ctx.lineTo(49,-17);ctx.stroke();ctx.fillStyle=pal.accent;ctx.beginPath();ctx.moveTo(52,-17);ctx.lineTo(43,-22);ctx.lineTo(43,-12);ctx.closePath();ctx.fill();
  }else{
    ctx.fillStyle='#dce5ef';ctx.beginPath();ctx.arc(-4,-47,13,0,Math.PI*2);ctx.fill();ctx.fillStyle=local?pal.body:'#665a77';ctx.beginPath();ctx.moveTo(-15,-32);ctx.lineTo(11,-32);ctx.lineTo(16,15);ctx.lineTo(-18,15);ctx.closePath();ctx.fill();
    ctx.strokeStyle='#7f6b9b';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(8,-19);ctx.lineTo(39,-37);ctx.stroke();ctx.strokeStyle=pal.accent;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(9,-20);ctx.lineTo(39,-37);ctx.stroke();ctx.fillStyle=pal.metal;ctx.shadowBlur=10;ctx.shadowColor='rgba(204,170,255,.8)';ctx.beginPath();ctx.arc(42,-39,7,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle='rgba(220,195,255,.8)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(42,-39,11,0,Math.PI*2);ctx.stroke();
  }

  if(local){
    const wp=cls==='knight'?{x:53,y:-20}:cls==='rogue'?{x:47,y:-18}:cls==='tank'?{x:46,y:-10}:cls==='archer'?{x:51,y:-20}:{x:45,y:-28},r=4+S.charge*3+(charged?4:0),pulse=.72+.28*Math.sin(performance.now()*.018);
    ctx.shadowBlur=charged?20:8+S.charge*4;ctx.shadowColor=`rgba(${rgb},.88)`;
    if(cls==='tank'||cls==='mage'){ctx.strokeStyle=`rgba(${rgb},${.30+S.charge*.20})`;ctx.lineWidth=charged?4:2.6;ctx.beginPath();ctx.arc(wp.x,wp.y,r*pulse,0,Math.PI*2);ctx.stroke()}
    else if(cls==='archer'){ctx.strokeStyle=`rgba(${rgb},${.30+S.charge*.18})`;ctx.lineWidth=charged?3.5:2.2;ctx.beginPath();ctx.moveTo(wp.x-r,wp.y+r*.45);ctx.lineTo(wp.x+r,wp.y-r*.45);ctx.stroke()}
    else if(cls==='rogue'){
      ctx.strokeStyle=`rgba(${rgb},${.32+S.charge*.18})`;ctx.lineWidth=charged?3.2:2.1;ctx.beginPath();ctx.arc(wp.x,wp.y,r*pulse,0,Math.PI*2);ctx.stroke();
      ctx.strokeStyle='rgba(216,92,92,.62)';ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(wp.x-r*.8,wp.y+r*.5);ctx.lineTo(wp.x+r*.9,wp.y-r*.6);ctx.stroke()
    }else{ctx.fillStyle=`rgba(${rgb},${.24+S.charge*.20})`;ctx.beginPath();ctx.arc(wp.x,wp.y,r*pulse,0,Math.PI*2);ctx.fill()}
    ctx.shadowBlur=0
  }
  ctx.fillStyle=local?'#fff':'rgba(255,255,255,.65)';ctx.beginPath();ctx.moveTo(0,-78);ctx.lineTo(-6,-68);ctx.lineTo(6,-68);ctx.closePath();ctx.fill();ctx.restore();
  ctx.fillStyle=local?'rgba(255,255,255,.76)':'rgba(255,255,255,.34)';ctx.font=`${local?'800':'700'} 9px system-ui`;ctx.textAlign='center';ctx.fillText(local?'YOU':`CPU ${slot}`,b.x,b.y+H*.045)
};

drawProjectiles=function(){
  for(const p of S.projectiles){
    if(p.age<0)continue;
    const t=clamp(p.age/p.life,0,1),e=easeOutCubic(t);p.x=p.sx+(p.tx-p.sx)*e;p.y=p.sy+(p.ty-p.sy)*e;
    const ang=Math.atan2(p.ty-p.sy,p.tx-p.sx),alpha=p.owner==='local'?1:.64,rgb=classColor(p.cls);
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);ctx.globalAlpha=alpha;ctx.shadowColor=`rgba(${rgb},.78)`;ctx.shadowBlur=p.heavy?20:11;
    if(p.cls==='knight'){
      const sc=(p.heavy?1.45:1)*(p.skillPower?1.20:1);ctx.scale(sc,sc);ctx.strokeStyle='rgba(255,196,74,.20)';ctx.lineWidth=p.heavy?12:8;ctx.beginPath();ctx.arc(-11,0,31,-.88,.88);ctx.stroke();ctx.strokeStyle='rgba(255,218,112,.98)';ctx.lineWidth=p.heavy?6.5:4.2;ctx.beginPath();ctx.arc(0,0,27,-.90,.90);ctx.stroke();ctx.strokeStyle='rgba(255,255,255,.78)';ctx.lineWidth=1.4;ctx.beginPath();ctx.arc(2,0,23,-.82,.82);ctx.stroke();
    }else if(p.cls==='rogue'){
      p.rot+=.28;ctx.rotate(p.rot);ctx.strokeStyle='rgba(166,170,176,.22)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-30,0);ctx.lineTo(-8,0);ctx.stroke();ctx.strokeStyle='rgba(216,92,92,.24)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-25,3);ctx.lineTo(-9,1);ctx.stroke();ctx.fillStyle='rgba(235,238,241,.99)';ctx.beginPath();ctx.moveTo(18,0);ctx.lineTo(-3,-5);ctx.lineTo(-12,0);ctx.lineTo(-3,5);ctx.closePath();ctx.fill();ctx.fillStyle='#777d84';ctx.fillRect(-11,-2,8,4);ctx.strokeStyle='rgba(216,92,92,.80)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(13,1);ctx.lineTo(-2,3);ctx.stroke();
    }else if(p.cls==='tank'){
      const skillScale=p.skillPower?1.25:1,w=(31+58*t)*skillScale,h=(28+14*t)*skillScale;ctx.rotate(-ang);ctx.strokeStyle='rgba(72,158,255,.20)';ctx.lineWidth=p.heavy?15:10;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.72,.72);ctx.stroke();ctx.strokeStyle='rgba(132,202,255,.98)';ctx.lineWidth=p.heavy?6:4.2;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.72,.72);ctx.stroke();ctx.strokeStyle='rgba(235,247,255,.72)';ctx.lineWidth=1.3;ctx.beginPath();ctx.ellipse(2,0,w*.76,h*.76,0,-.72,.72);ctx.stroke();
    }else if(p.cls==='archer'){
      ctx.strokeStyle='rgba(144,219,139,.20)';ctx.lineWidth=p.heavy?7:4;ctx.beginPath();ctx.moveTo(-38,0);ctx.lineTo(-11,0);ctx.stroke();ctx.strokeStyle='rgba(220,255,223,.98)';ctx.lineWidth=p.heavy?3.6:2.3;ctx.beginPath();ctx.moveTo(-18,0);ctx.lineTo(17,0);ctx.stroke();ctx.fillStyle='rgba(225,255,228,.98)';ctx.beginPath();ctx.moveTo(22,0);ctx.lineTo(10,-6);ctx.lineTo(12,0);ctx.lineTo(10,6);ctx.closePath();ctx.fill();ctx.fillStyle='rgba(140,220,150,.95)';ctx.beginPath();ctx.moveTo(-16,0);ctx.lineTo(-24,-5);ctx.lineTo(-21,0);ctx.lineTo(-24,5);ctx.closePath();ctx.fill();if(p.heavy){ctx.globalAlpha*=.7;ctx.strokeStyle='rgba(210,255,215,.7)';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-15,-7);ctx.lineTo(17,-7);ctx.moveTo(-15,7);ctx.lineTo(17,7);ctx.stroke()}
    }else{
      const r=(p.heavy?13:9)+(p.skillPower?3:0);ctx.rotate(-ang);const grd=ctx.createRadialGradient(0,0,1,0,0,r+8);grd.addColorStop(0,'rgba(255,255,255,.98)');grd.addColorStop(.28,'rgba(230,210,255,.96)');grd.addColorStop(1,'rgba(170,120,255,0)');ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r+8,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(235,218,255,.72)';ctx.lineWidth=1.5;for(let i=0;i<3;i++){const rr0=r+5+i*4+2*Math.sin(t*Math.PI+i);ctx.beginPath();ctx.arc(0,0,rr0,(i+performance.now()*.001)*.8,(i+performance.now()*.001)*.8+Math.PI*1.25);ctx.stroke()}ctx.fillStyle='rgba(236,218,255,.28)';ctx.beginPath();ctx.arc(-18,0,r*.45,0,Math.PI*2);ctx.fill()
    }
    ctx.restore()
  }
};
