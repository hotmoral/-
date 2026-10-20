// Timing Defense v0.24 — character profile radar, lobby layout, lineup readability, projectile visibility.
// No combat-balance coefficients changed. Projectile travel times remain unchanged.
(function(){
  const CLASSES=['knight','rogue','tank','archer','mage'];
  const LEVELS=[6,11,16,21,26,31];
  const AXES=['공격력','치명타','민첩성','넉백','관통','광역'];
  const PROFILE={
    knight:[4,2,3,3,4,2],
    rogue:[2,5,5,1,1,1],
    tank:[2,1,1,5,1,3],
    archer:[3,2,4,1,5,2],
    mage:[4,2,2,1,1,5]
  };
  const META={
    knight:{name:'KNIGHT',ko:'기사',role:'안정적인 전열 · 관통 검기 · 강한 4타',color:'#ffd76a',fill:'rgba(255,215,106,.25)'},
    rogue:{name:'ROGUE',ko:'도적',role:'빠른 다단히트 · 높은 치명타 · 급소 처형',color:'#cbd2d8',fill:'rgba(28,32,36,.72)'},
    tank:{name:'TANK',ko:'탱커',role:'강한 넉백 · 성벽 보호 · 전장 제어',color:'#69b6ff',fill:'rgba(105,182,255,.23)'},
    archer:{name:'ARCHER',ko:'궁수',role:'빠른 전개 · 직선 관통 · 후열 제거',color:'#98e493',fill:'rgba(152,228,147,.22)'},
    mage:{name:'MAGE',ko:'마법사',role:'고화력 · 밀집 광역 · 연쇄 폭발',color:'#d0aaff',fill:'rgba(208,170,255,.24)'}
  };
  const SKILLS={
    knight:[['강화 검기','검기 피해 +12% · 검기 크기 확대'],['돌파 참격','일반 검기 1회 추가 관통 · 4타는 더 깊게 관통'],['예리한 검극','PERFECT 공격 피해와 넉백 강화'],['대검기','4타가 거대한 검기로 변하며 넓은 전열을 절단'],['전열 붕괴','관통할수록 다음 적에 대한 밀어내기 강화'],['천단참','P×P CRITICAL에서 전 경로를 가르는 이중 참격']],
    rogue:[['쌍단검','두 번째 단검이 같은 적도 연속 타격'],['급소 포착','직업 고유 치명타 확률 상승'],['살수의 리듬','PERFECT 후 다음 공격 준비가 빨라짐'],['칼날 난무','4타에 단검 5개를 연속 투척'],['연쇄 투척','PERFECT 시 다른 적에게 추적 단검 생성'],['칼날 폭우','P×P CRITICAL에서 다수 단검이 쏟아짐']],
    tank:[['강화 충격파','충격파 폭과 넉백이 크게 증가'],['철벽','팀 성벽이 받는 피해 감소'],['완벽 방어','PERFECT 시 성벽 보호막 생성'],['대지 충격','4타가 넓은 전방 대지 충격으로 변함'],['여진 지대','4타 후 적을 둔화시키는 여진 지대 생성'],['절대 방벽','P×P CRITICAL에서 전장 충격파 + 강력 보호막']],
    archer:[['관통 화살','한 궤도 위의 적을 연속 관통'],['강궁','화살 속도와 기본 피해 상승'],['정밀 관통','PERFECT 관통이 방어를 무시하고 위력을 보존'],['삼연사','4타에 직선 화살 3발 연속 발사'],['꿰뚫는 사격','PERFECT 관통 수와 후열 보존력이 증가'],['천공의 화살','P×P CRITICAL에서 화면을 가르는 거대 관통 화살']],
    mage:[['마력 폭발','명중 지점 주변 적에게 광역 피해'],['확장 마법진','폭발 범위와 주변 피해 강화'],['마력 공명','PERFECT 후 중심을 제외한 2차 폭발'],['대마력탄','4타가 더 크고 강한 마력탄으로 변함'],['연쇄 폭발','다수 적 명중 시 폭발이 주변으로 연쇄'],['마력 붕괴','P×P CRITICAL에서 3단계 마력 붕괴 발생']]
  };

  const style=document.createElement('style');
  style.textContent=`
    #v022Lobby .lobTop{height:52px!important;padding-top:10px!important}
    #v022Lobby .lobBody{height:calc(100% - 52px)!important;padding:0 16px 10px!important}
    #v022Lobby .nickRow{height:38px!important;margin-bottom:1px!important}
    #v022Lobby .lobFoot{height:40px!important}
    #v022Lobby .carouselShell{border-radius:18px!important}
    #v022Lobby .classCard .heroPane{left:29.4%!important;width:31.6%!important;top:1%!important;bottom:1%!important}
    #v022Lobby .classCard .heroCanvas{width:min(29vw,300px)!important;height:min(63vh,340px)!important;max-height:340px!important;aspect-ratio:1/1!important}
    #v022Lobby .classCard .heroName{font-size:23px!important;margin-top:-12px!important;text-shadow:0 2px 12px rgba(0,0,0,.38)}
    #v022Lobby .navArrow{width:36px!important;height:50px!important;border-radius:12px!important;background:rgba(5,9,8,.66)!important;box-shadow:0 6px 20px rgba(0,0,0,.25)!important}
    #v022Lobby .navArrow.prev{left:29.2%!important}
    #v022Lobby .navArrow.next{right:39.2%!important}
    #v022Lobby .carouselDots{bottom:5px!important}
    #v022Lobby .v023InfoWing{top:2.8%!important;bottom:3.8%!important;padding:10px 11px!important;border-radius:15px!important}
    #v022Lobby .v023Left{left:1.3%!important;width:27.1%!important;justify-content:flex-start!important}
    #v022Lobby .v023Right{right:1.3%!important;width:37.2%!important;justify-content:flex-start!important}
    .v024ProfileHead{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:2px}
    .v024ProfileLabel{font:1000 8px system-ui;letter-spacing:.12em;color:#9eaaa4}.v024ProfileClass{font:1000 13px system-ui;letter-spacing:.055em}
    .v024RadarWrap{position:relative;flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin-top:1px}
    .v024Radar{width:100%;height:100%;min-height:175px;max-height:245px;display:block}
    .v024Role{font:800 8px/1.35 system-ui;color:#b8c4be;text-align:center;margin-top:-2px;min-height:20px}
    .v024SkillHead{height:18px;display:flex;align-items:center;justify-content:space-between;gap:8px}
    .v024SkillTitle{font:1000 8px system-ui;letter-spacing:.11em;color:#aebbb4}.v024SkillHint{font:800 7px system-ui;color:#7f9188}
    .v024SkillGrid{height:calc(100% - 20px);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));gap:6px;margin-top:2px}
    .v024SkillCard{min-width:0;min-height:0;border:1px solid rgba(255,255,255,.095);border-radius:10px;background:rgba(4,9,7,.44);padding:6px;display:grid;grid-template-columns:34px minmax(0,1fr);grid-template-rows:auto 1fr;column-gap:6px;overflow:hidden}
    .v024SkillCard canvas{width:32px;height:32px;grid-row:1/3;align-self:start}.v024SkillName{font:1000 8.5px system-ui;white-space:normal;line-height:1.15}.v024SkillLv{font:1000 6.5px system-ui;margin-left:4px}.v024SkillDesc{font:730 7.2px/1.28 system-ui;color:#aebbb4;margin-top:3px;white-space:normal;overflow:visible}
    #v022Lobby .settingsWrap{grid-template-columns:34% 66%!important;gap:9px!important}
    #v022Lobby .settingPanel{padding:10px 12px!important}
    #v022Lobby .settingPanel:nth-child(2){overflow:hidden!important}
    #v022Lobby .aiRows{gap:6px!important}
    #v022Lobby .aiRow{grid-template-columns:43px 105px minmax(0,1fr)!important;min-height:58px!important;padding:6px 7px!important;gap:6px!important}
    #v022Lobby .classMini{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:4px!important;align-content:center!important}
    #v022Lobby .classMini .mini{min-width:0!important;width:100%!important;height:22px!important;padding:3px 4px!important;font-size:7.5px!important}
    #v022Lobby #v022Summary{display:none!important}
    #v022Lobby #v022Summary + *{display:none!important}
    #v022Lobby .v024SummaryTitle{display:none!important}
    @media(max-height:590px){
      #v022Lobby .lobTop{height:44px!important;padding-top:7px!important}#v022Lobby .lobBody{height:calc(100% - 44px)!important;padding-bottom:6px!important}
      #v022Lobby .nickRow{height:32px!important}#v022Lobby .lobFoot{height:34px!important}
      #v022Lobby .classCard .heroCanvas{height:min(61vh,250px)!important;max-height:250px!important}
      #v022Lobby .classCard .heroName{font-size:19px!important;margin-top:-15px!important}
      #v022Lobby .v023InfoWing{top:1.5%!important;bottom:2.5%!important;padding:7px 8px!important}
      .v024Radar{min-height:145px;max-height:205px}.v024Role{font-size:7px}.v024SkillGrid{gap:4px}.v024SkillCard{padding:4px;grid-template-columns:28px minmax(0,1fr);column-gap:4px}.v024SkillCard canvas{width:27px;height:27px}.v024SkillName{font-size:7.4px}.v024SkillLv{font-size:6px}.v024SkillDesc{font-size:6.5px;line-height:1.2}
      #v022Lobby .aiRow{min-height:51px!important;padding:4px 5px!important}.classMini .mini{height:20px!important}
    }
  `;
  document.head.appendChild(style);

  const root=document.getElementById('v022Lobby');
  const track=document.getElementById('v022Track');
  let currentClass=0;
  let radarToken=0;

  function classIndex(){
    const s=track?.style.transform||'',m=s.match(/translateX\((-?[\d.]+)%\)/);
    if(!m)return 0;
    return Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length
  }
  function copySkillIcon(dst,cls,idx){
    const src=root?.querySelector(`[data-skill="${cls}:${idx}"]`),c=dst.getContext('2d');
    c.clearRect(0,0,dst.width,dst.height);if(src)c.drawImage(src,0,0,dst.width,dst.height)
  }
  function hexPoint(cx,cy,r,i){const a=-Math.PI/2+i*Math.PI/3;return[cx+Math.cos(a)*r,cy+Math.sin(a)*r]}
  function polygon(c,pts){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath()}
  function easeOutBack01(t){t=Math.max(0,Math.min(1,t));const c1=1.28,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)}
  function drawRadar(canvas,cls,start){
    const token=++radarToken,c=canvas.getContext('2d'),m=META[cls],vals=PROFILE[cls],W=canvas.width,H=canvas.height,cx=W/2,cy=H*.51,R=Math.min(W*.28,H*.31),labelR=R*1.28;
    function frame(now){
      if(token!==radarToken||!canvas.isConnected)return;
      const elapsed=now-start;c.clearRect(0,0,W,H);c.save();
      const bg=c.createRadialGradient(cx,cy,2,cx,cy,R*1.5);bg.addColorStop(0,'rgba(255,255,255,.035)');bg.addColorStop(1,'rgba(255,255,255,0)');c.fillStyle=bg;c.fillRect(0,0,W,H);
      for(let ring=1;ring<=5;ring++){
        const rr=R*ring/5,pts=AXES.map((_,i)=>hexPoint(cx,cy,rr,i));
        c.strokeStyle=`rgba(220,232,225,${ring===5?.22:.095})`;c.lineWidth=ring===5?1.35:.8;polygon(c,pts);c.stroke();
      }
      for(let i=0;i<6;i++){
        const p=hexPoint(cx,cy,R,i);c.strokeStyle='rgba(220,232,225,.09)';c.lineWidth=.8;c.beginPath();c.moveTo(cx,cy);c.lineTo(p[0],p[1]);c.stroke();
      }
      const scan=Math.max(0,Math.min(1,elapsed/520));
      if(scan<1){const rr=R*(.15+.85*scan);const pts=AXES.map((_,i)=>hexPoint(cx,cy,rr,i));c.strokeStyle=m.color;c.globalAlpha=.55*(1-scan);c.lineWidth=2.2;polygon(c,pts);c.stroke();c.globalAlpha=1}
      const pts=[];
      for(let i=0;i<6;i++){
        const delay=i*58,pt=Math.max(0,Math.min(1,(elapsed-delay)/520)),e=easeOutBack01(pt),rr=R*(vals[i]/5)*e;pts.push(hexPoint(cx,cy,rr,i));
      }
      c.save();c.shadowBlur=18;c.shadowColor=m.color;c.fillStyle=m.fill;c.strokeStyle=m.color;c.lineWidth=2.2;polygon(c,pts);c.fill();c.stroke();c.restore();
      for(let i=0;i<6;i++){
        const delay=i*58,pt=Math.max(0,Math.min(1,(elapsed-delay)/520)),p=pts[i];
        c.save();c.globalAlpha=pt;c.shadowBlur=9;c.shadowColor=m.color;c.fillStyle=m.color;c.beginPath();c.arc(p[0],p[1],3.2+1.3*Math.sin(Math.min(1,pt)*Math.PI),0,Math.PI*2);c.fill();c.restore();
      }
      c.textAlign='center';c.textBaseline='middle';c.font='900 12px system-ui';
      for(let i=0;i<6;i++){
        const p=hexPoint(cx,cy,labelR,i);c.lineWidth=3;c.strokeStyle='rgba(4,9,7,.72)';c.strokeText(AXES[i],p[0],p[1]);c.fillStyle=i===0?m.color:'rgba(228,235,231,.88)';c.fillText(AXES[i],p[0],p[1]);
      }
      const settle=Math.max(0,Math.min(1,(elapsed-430)/420));
      if(settle>0){c.globalAlpha=.16*(1-settle);c.fillStyle=m.color;c.beginPath();c.arc(cx,cy,R*(.28+.9*settle),0,Math.PI*2);c.fill();c.globalAlpha=1}
      c.restore();
      if(elapsed<980)requestAnimationFrame(frame)
    }
    requestAnimationFrame(frame)
  }
  function renderPanels(){
    if(!root)return;currentClass=classIndex();const cls=CLASSES[currentClass],m=META[cls],left=document.getElementById('v023ClassInfo'),right=document.getElementById('v023SkillInfo');if(!left||!right)return;
    left.innerHTML=`<div class="v024ProfileHead"><span class="v024ProfileLabel">COMBAT PROFILE</span><span class="v024ProfileClass" style="color:${m.color}">${m.ko}</span></div><div class="v024RadarWrap"><canvas class="v024Radar" width="360" height="300"></canvas></div><div class="v024Role">${m.role}</div>`;
    right.innerHTML=`<div class="v024SkillHead"><span class="v024SkillTitle">SKILL ROADMAP</span><span class="v024SkillHint">Lv6 · 11 · 16 · 21 · 26 · 31</span></div><div class="v024SkillGrid">${SKILLS[cls].map((s,i)=>`<div class="v024SkillCard"><canvas width="64" height="64" data-v024icon="${i}"></canvas><div class="v024SkillName" style="color:${m.color}">${s[0]}<span class="v024SkillLv">LV ${LEVELS[i]}</span></div><div class="v024SkillDesc">${s[1]}</div></div>`).join('')}</div>`;
    right.querySelectorAll('[data-v024icon]').forEach((cv,i)=>copySkillIcon(cv,cls,i));
    const canvas=left.querySelector('.v024Radar');if(canvas)drawRadar(canvas,cls,performance.now());
  }
  if(track){new MutationObserver(()=>setTimeout(()=>renderPanels(),0)).observe(track,{attributes:true,attributeFilter:['style']})}
  setTimeout(()=>renderPanels(),0);

  const summary=document.getElementById('v022Summary');
  if(summary){const title=summary.previousElementSibling;if(title?.classList.contains('groupTitle'))title.classList.add('v024SummaryTitle');summary.style.display='none'}

  const previousTimingSquare=drawTimingSquare;
  drawTimingSquare=function(now){
    if(S.playerClass!=='rogue')return previousTimingSquare(now);
    const saved=S.playerClass;S.playerClass='knight';previousTimingSquare(now);S.playerClass=saved;
    if(S.phase!=='x'&&S.phase!=='y'&&now>S.lockedCrossUntil)return;
    const g=squareGeom(),x=g.x,y=g.y,s=g.size,cy=y-22,gap=22,start=x+s/2-gap;
    ctx.save();ctx.shadowBlur=12;ctx.shadowColor='rgba(0,0,0,.58)';ctx.strokeStyle='rgba(15,18,21,.96)';ctx.lineWidth=4.4;rr(x-1,y-1,s+2,s+2,13);ctx.stroke();ctx.shadowBlur=0;ctx.strokeStyle='rgba(226,233,238,.64)';ctx.lineWidth=1.15;rr(x,y,s,s,12);ctx.stroke();
    for(let i=0;i<3;i++){const on=i<S.charge;ctx.fillStyle=on?'#111417':'rgba(25,29,32,.34)';ctx.strokeStyle=on?'rgba(238,243,246,.92)':'rgba(238,243,246,.42)';ctx.lineWidth=1.4;ctx.beginPath();ctx.arc(start+i*gap,cy,7.3,0,Math.PI*2);ctx.fill();ctx.stroke()}
    ctx.font='1000 10px system-ui';ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.lineWidth=3;ctx.strokeStyle='rgba(236,242,245,.88)';const txt=isHeavy()?'HEAVY READY':`CHARGE ${S.charge}/3`;ctx.strokeText(txt,x+s/2,cy-11);ctx.fillStyle='#101316';ctx.fillText(txt,x+s/2,cy-11);ctx.restore()
  };

  const previousProgress=drawProgressHUD;
  drawProgressHUD=function(now){
    if(S.playerClass!=='rogue')return previousProgress(now);
    const savedCls=S.playerClass,savedXpUntil=S.v023XpUntil,savedFlash=S.levelFlashUntil;
    S.playerClass='knight';S.v023XpUntil=0;S.levelFlashUntil=0;previousProgress(now);S.playerClass=savedCls;S.v023XpUntil=savedXpUntil;S.levelFlashUntil=savedFlash;
    const g=squareGeom(),barX=g.x+g.size+12,barY=g.y+5,barW=14,barH=g.size-10,ratio=clamp(S.xp/S.xpNeed,0,1),flash=now<savedFlash,fillH=Math.max(2,barH*ratio);
    ctx.save();if(flash){ctx.shadowBlur=16;ctx.shadowColor='rgba(225,232,237,.72)'}ctx.fillStyle='rgba(232,237,240,.56)';rr(barX,barY,barW,barH,7);ctx.fill();ctx.fillStyle='#111417';rr(barX,barY+barH-fillH,barW,fillH,7);ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle='rgba(22,26,30,.92)';ctx.lineWidth=1.2;rr(barX,barY,barW,barH,7);ctx.stroke();ctx.textAlign='center';ctx.font=`1000 ${flash?13:11}px system-ui`;ctx.lineWidth=3;ctx.strokeStyle='rgba(240,244,246,.92)';ctx.strokeText(`LV ${S.level}`,barX+barW/2,barY-9);ctx.fillStyle='#101316';ctx.fillText(`LV ${S.level}`,barX+barW/2,barY-9);ctx.font='900 8px system-ui';ctx.strokeText('EXP',barX+barW/2,barY+barH+12);ctx.fillText('EXP',barX+barW/2,barY+barH+12);
    if(savedXpUntil&&now<savedXpUntil){const t=clamp((now-S.v023XpStart)/720,0,1),fade=t<.66?1:1-clamp((t-.66)/.34,0,1),rise=8*easeOutCubic(t),tx=barX+barW+7,ty=barY+barH*.53-rise;ctx.globalAlpha=fade;ctx.textAlign='left';ctx.textBaseline='middle';ctx.font='1000 10px system-ui';ctx.lineWidth=3.5;ctx.strokeStyle='rgba(241,245,247,.95)';ctx.strokeText(`+EXP ${S.v023XpAmount}`,tx,ty);ctx.fillStyle='#101316';ctx.fillText(`+EXP ${S.v023XpAmount}`,tx,ty)}ctx.restore()
  };

  const previousProjectiles=drawProjectiles;
  drawProjectiles=function(){
    previousProjectiles();
    for(const p of S.projectiles){
      if(p.age<0||typeof p.x!=='number'||typeof p.y!=='number')continue;
      const ang=Math.atan2(p.ty-p.sy,p.tx-p.sx),local=p.owner==='local',alpha=local?1:.72;
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);ctx.globalAlpha=alpha;ctx.lineCap='round';ctx.lineJoin='round';
      if(p.cls==='knight'){
        ctx.shadowBlur=12;ctx.shadowColor='rgba(112,70,0,.48)';ctx.strokeStyle='rgba(104,64,0,.88)';ctx.lineWidth=p.heavy?10:7;ctx.beginPath();ctx.arc(0,0,p.heavy?32:27,-.92,.92);ctx.stroke();ctx.strokeStyle='rgba(255,221,108,.98)';ctx.lineWidth=p.heavy?4.5:3;ctx.beginPath();ctx.arc(0,0,p.heavy?32:27,-.92,.92);ctx.stroke();
      }else if(p.cls==='rogue'){
        ctx.shadowBlur=9;ctx.shadowColor='rgba(0,0,0,.60)';ctx.fillStyle='rgba(18,21,24,.98)';ctx.strokeStyle='rgba(232,238,242,.96)';ctx.lineWidth=1.6;ctx.beginPath();ctx.moveTo(19,0);ctx.lineTo(-7,-5.3);ctx.lineTo(-14,0);ctx.lineTo(-7,5.3);ctx.closePath();ctx.fill();ctx.stroke();ctx.strokeStyle='rgba(25,29,32,.72)';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-34,0);ctx.lineTo(-15,0);ctx.stroke();
      }else if(p.cls==='tank'){
        const t=clamp(p.age/p.life,0,1),w=34+61*t,h=32+15*t;ctx.shadowBlur=11;ctx.shadowColor='rgba(14,58,94,.55)';ctx.strokeStyle='rgba(18,69,108,.92)';ctx.lineWidth=p.heavy?9:7;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.75,.75);ctx.stroke();ctx.strokeStyle='rgba(121,211,255,.95)';ctx.lineWidth=p.heavy?3.5:2.4;ctx.beginPath();ctx.ellipse(0,0,w,h,0,-.75,.75);ctx.stroke();
      }else if(p.cls==='archer'){
        ctx.shadowBlur=9;ctx.shadowColor='rgba(25,84,39,.48)';ctx.strokeStyle='rgba(26,91,43,.98)';ctx.lineWidth=p.heavy?7:5;ctx.beginPath();ctx.moveTo(-24,0);ctx.lineTo(20,0);ctx.stroke();ctx.strokeStyle='rgba(207,255,207,.96)';ctx.lineWidth=p.heavy?2.6:1.5;ctx.beginPath();ctx.moveTo(-22,0);ctx.lineTo(20,0);ctx.stroke();ctx.fillStyle='rgba(25,91,42,.98)';ctx.beginPath();ctx.moveTo(24,0);ctx.lineTo(11,-6);ctx.lineTo(11,6);ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(207,255,207,.88)';ctx.lineWidth=1.1;ctx.stroke();ctx.strokeStyle='rgba(29,95,44,.54)';ctx.lineWidth=3.5;ctx.beginPath();ctx.moveTo(-46,0);ctx.lineTo(-26,0);ctx.stroke();
      }else{
        const r=(p.heavy?14:10)+(p.skillPower?3:0);ctx.rotate(-ang);ctx.shadowBlur=14;ctx.shadowColor='rgba(75,31,122,.62)';ctx.fillStyle='rgba(88,42,137,.97)';ctx.beginPath();ctx.arc(0,0,r+2,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(235,214,255,.96)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+3,0,Math.PI*2);ctx.stroke();ctx.strokeStyle='rgba(92,43,142,.55)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-r-24,0);ctx.lineTo(-r-6,0);ctx.stroke();
      }
      ctx.restore()
    }
  };
})();
