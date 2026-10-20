// Timing Defense v0.23 — lobby/readability polish.
// No combat-balance coefficients changed.
(function(){
  const CLASSES=['knight','rogue','tank','archer','mage'];
  const LEVELS=[6,11,16,21,26,31];
  const META={
    knight:{name:'KNIGHT',ko:'기사',tag:'ALL-ROUNDER',role:'안정적인 전열 · 관통 검기 · 강한 4타',style:'전황에 관계없이 꾸준히 기여하는 안정형 전사',color:'#ffd76a',skills:[['강화 검기','검기 피해 +12% · 검기 크기 확대'],['돌파 참격','일반 검기 1회 추가 관통 · 4타는 더 깊게 관통'],['예리한 검극','PERFECT 공격 피해와 넉백 강화'],['대검기','4타가 거대한 검기로 변하며 넓은 전열을 절단'],['전열 붕괴','관통할수록 다음 적에 대한 밀어내기 강화'],['천단참','P×P CRITICAL에서 전 경로를 가르는 이중 참격']]},
    rogue:{name:'ROGUE',ko:'도적',tag:'EXECUTION',role:'빠른 다단히트 · 고체력 일반몹 처형',style:'짧은 간격의 연속타와 급소 공격에 특화',color:'#ef6b6b',skills:[['쌍단검','두 번째 단검이 같은 적도 연속 타격'],['급소 포착','직업 고유 치명타 확률 상승'],['살수의 리듬','PERFECT 후 다음 공격 준비가 빨라짐'],['칼날 난무','4타에 단검 5개를 연속 투척'],['연쇄 투척','PERFECT 시 다른 적에게 추적 단검 생성'],['칼날 폭우','P×P CRITICAL에서 다수 단검이 쏟아짐']]},
    tank:{name:'TANK',ko:'탱커',tag:'TEAM DEFENSE',role:'넉백 · 성벽 보호 · 전장 제어',style:'팀의 시간을 벌고 위기 상황을 되돌리는 수비형',color:'#69b6ff',skills:[['강화 충격파','충격파 폭과 넉백이 크게 증가'],['철벽','팀 성벽이 받는 피해 감소'],['완벽 방어','PERFECT 시 성벽 보호막 생성'],['대지 충격','4타가 넓은 전방 대지 충격으로 변함'],['여진 지대','4타 후 적을 둔화시키는 여진 지대 생성'],['절대 방벽','P×P CRITICAL에서 전장 충격파 + 강력 보호막']]},
    archer:{name:'ARCHER',ko:'궁수',tag:'LINE CONTROL',role:'직선 관통 · 후열 제거 · 장거리 압박',style:'한 궤도에 정렬된 적을 빠르게 꿰뚫는 사수',color:'#98e493',skills:[['관통 화살','한 궤도 위의 적을 연속 관통'],['강궁','화살 속도와 기본 피해 상승'],['정밀 관통','PERFECT 관통이 방어를 무시하고 위력을 보존'],['삼연사','4타에 직선 화살 3발 연속 발사'],['꿰뚫는 사격','PERFECT 관통 수와 후열 보존력이 증가'],['천공의 화살','P×P CRITICAL에서 화면을 가르는 거대 관통 화살']]},
    mage:{name:'MAGE',ko:'마법사',tag:'AREA BURST',role:'밀집 광역 · 폭발 · 연쇄 피해',style:'적이 뭉칠수록 강해지는 밀집 전투 전문가',color:'#d0aaff',skills:[['마력 폭발','명중 지점 주변 적에게 광역 피해'],['확장 마법진','폭발 범위와 주변 피해 강화'],['마력 공명','PERFECT 후 중심을 제외한 2차 폭발'],['대마력탄','4타가 더 크고 강한 마력탄으로 변함'],['연쇄 폭발','다수 적 명중 시 폭발이 주변으로 연쇄'],['마력 붕괴','P×P CRITICAL에서 3단계 마력 붕괴 발생']]}
  };

  const style=document.createElement('style');
  style.textContent=`
    #attackLabel{display:none!important}
    #v022Lobby .carouselShell{overflow:hidden!important}
    #v022Lobby .classCard{display:block!important;position:relative!important;padding:0!important}
    #v022Lobby .classCard .heroPane{position:absolute!important;left:31%!important;top:0!important;bottom:0!important;width:38%!important;display:flex!important;align-items:center!important;justify-content:center!important}
    #v022Lobby .classCard .heroCanvas{width:min(29vw,300px)!important;height:min(48vh,285px)!important;max-height:285px!important}
    #v022Lobby .classCard .heroName{display:block!important;font-size:21px!important;margin-top:-8px!important}
    #v022Lobby .classCard .heroRole,#v022Lobby .classCard .heroTag,#v022Lobby .classCard .skillPane{display:none!important}
    #v022Lobby .navArrow.prev{left:28.5%!important}.navArrow.next{right:29.5%!important}
    #v022Lobby .carouselDots{left:50%!important;bottom:10px!important}
    .v023InfoWing{position:absolute;top:8%;bottom:8%;z-index:2;border:1px solid rgba(255,255,255,.085);border-radius:16px;background:rgba(5,11,9,.30);backdrop-filter:blur(4px);padding:14px 15px;pointer-events:auto}
    .v023Left{left:2.2%;width:25.2%;display:flex;flex-direction:column;justify-content:center}
    .v023Right{right:2.2%;width:38.2%;display:flex;flex-direction:column;justify-content:center}
    .v023Ko{font-size:10px;font-weight:900;letter-spacing:.10em;color:#9faea6}.v023Class{font-size:24px;font-weight:1000;letter-spacing:.065em;margin-top:3px}.v023Tag{display:inline-flex;align-self:flex-start;margin-top:8px;padding:4px 8px;border-radius:99px;border:1px solid rgba(255,255,255,.13);font-size:8px;font-weight:1000;letter-spacing:.10em;background:rgba(255,255,255,.045)}
    .v023Role{font-size:10px;line-height:1.5;color:#d9e2dc;margin-top:13px}.v023Style{font-size:8px;line-height:1.5;color:#91a198;margin-top:8px}.v023SkillTitle{font-size:9px;font-weight:1000;letter-spacing:.10em;color:#aab7b0;margin-bottom:7px}.v023SkillStrip{display:grid;grid-template-columns:repeat(6,1fr);gap:5px}.v023SkillPick{min-width:0;padding:4px 2px 3px;border:1px solid rgba(255,255,255,.10);border-radius:9px;background:rgba(4,9,7,.48);color:#b8c4bd}.v023SkillPick.on{border-color:var(--skill-color,#f1d889);background:rgba(255,255,255,.065)}.v023SkillPick canvas{display:block;width:34px;height:34px;margin:0 auto}.v023SkillLv{font-size:7px;font-weight:950;margin-top:2px;color:#a7b4ac}.v023SkillDetail{margin-top:9px;min-height:76px;border-top:1px solid rgba(255,255,255,.08);padding-top:9px}.v023SkillName{font-size:13px;font-weight:1000}.v023SkillLevel{font-size:8px;font-weight:950;margin-left:6px}.v023SkillDesc{font-size:9px;line-height:1.55;color:#bac6c0;margin-top:6px;white-space:normal;overflow:visible}
    #v022Lobby .settingsWrap{grid-template-columns:40% 60%!important;gap:9px!important}
    #v022Lobby .settingPanel{overflow:hidden!important;padding:10px 13px!important}
    #v022Lobby .setTitle{margin-bottom:7px!important}.groupTitle{margin:7px 0 4px!important}.segBtn{padding:6px 10px!important}.tierCard{padding:7px 10px!important}.netNote{display:none!important}
    #v022Lobby .aiRows{gap:5px!important}.aiRow{grid-template-columns:47px 105px 1fr!important;padding:5px 6px!important;gap:5px!important}.mini{padding:4px 6px!important}.classMini{gap:4px!important;flex-wrap:nowrap!important}.classMini .mini{min-width:49px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:4px!important}.v023RoleGlyph{display:inline-flex;width:12px;height:12px;align-items:center;justify-content:center;font:1000 10px system-ui;line-height:1}.v023RoleGlyph.knight{color:#ffd76a}.v023RoleGlyph.rogue{color:#ef6b6b}.v023RoleGlyph.tank{color:#69b6ff}.v023RoleGlyph.archer{color:#98e493}.v023RoleGlyph.mage{color:#d0aaff}.summary{font-size:8px!important;line-height:1.35!important}.v023TeamRule{font-size:8px;color:#9dac9f;margin-top:5px}
    @media(max-height:590px){.v023InfoWing{top:4%;bottom:5%;padding:10px 12px}.v023Class{font-size:20px}.v023Role{margin-top:8px}.v023SkillPick canvas{width:28px;height:28px}.v023SkillDetail{min-height:60px;margin-top:6px;padding-top:6px}.v023SkillDesc{font-size:8px;line-height:1.4}.v023Right{width:39%}.v023Left{width:25.5%}#v022Lobby .classCard .heroCanvas{height:205px!important}.aiRow{padding:4px 5px!important}.groupTitle{margin:4px 0 3px!important}.segBtn{padding:5px 9px!important}}
  `;
  document.head.appendChild(style);

  const baseAwardXP=awardXP;
  awardXP=function(amount){
    const valid=S.stageMode==='combat'&&!S.gameOver&&!S.runComplete&&Number(amount)>0;
    const out=baseAwardXP(amount);
    if(valid){const now=performance.now();S.v023XpAmount=Number(amount);S.v023XpStart=now;S.v023XpUntil=now+720}
    return out
  };
  const baseProgress=drawProgressHUD;
  drawProgressHUD=function(now){
    const oldUntil=S.xpGainUntil;S.xpGainUntil=0;baseProgress(now);S.xpGainUntil=oldUntil;
    if(!S.v023XpUntil||now>=S.v023XpUntil)return;
    const g=squareGeom(),barX=g.x+g.size+12,barY=g.y+5,barW=14,barH=g.size-10;
    const t=clamp((now-S.v023XpStart)/720,0,1),fade=t<.66?1:1-clamp((t-.66)/.34,0,1),rise=8*easeOutCubic(t);
    const rgb=S.playerClass==='rogue'?'240,105,105':classColor();
    ctx.save();ctx.globalAlpha=fade;ctx.textAlign='left';ctx.textBaseline='middle';ctx.font='1000 10px system-ui';ctx.fillStyle=`rgba(${rgb},.98)`;ctx.shadowBlur=8;ctx.shadowColor=`rgba(${rgb},.52)`;ctx.fillText(`+EXP ${S.v023XpAmount}`,barX+barW+7,barY+barH*.53-rise);ctx.restore()
  };

  const baseTimingSquare=drawTimingSquare;
  drawTimingSquare=function(now){
    baseTimingSquare(now);
    if(S.playerClass!=='rogue')return;
    if(S.phase!=='x'&&S.phase!=='y'&&now>S.lockedCrossUntil)return;
    const g=squareGeom(),x=g.x,y=g.y,s=g.size,cy=y-22,gap=22,start=x+s/2-gap;
    ctx.save();ctx.shadowBlur=9;ctx.shadowColor='rgba(239,92,92,.42)';ctx.strokeStyle='rgba(239,101,101,.76)';ctx.lineWidth=1.8;rr(x-1,y-1,s+2,s+2,13);ctx.stroke();ctx.shadowBlur=0;
    for(let i=0;i<3;i++){const on=i<S.charge;ctx.fillStyle=on?'rgba(255,105,105,.98)':'rgba(246,250,252,.32)';ctx.strokeStyle=on?'rgba(255,220,220,.82)':'rgba(35,42,47,.45)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(start+i*gap,cy,7,0,Math.PI*2);ctx.fill();ctx.stroke()}
    ctx.restore()
  };

  const root=document.getElementById('v022Lobby');
  const shell=root?.querySelector('.carouselShell');
  const track=document.getElementById('v022Track');
  let currentClass=0,selectedSkill=0;

  function refineHeroes(){
    root?.querySelectorAll('[data-hero]').forEach(cv=>{
      if(cv.dataset.v023Refined)return;cv.dataset.v023Refined='1';
      const cls=cv.dataset.hero,c=cv.getContext('2d'),w=cv.width,h=cv.height;
      c.save();c.globalAlpha=.82;c.lineCap='round';
      const accents={knight:'#fff0b5',rogue:'#d85c5c',tank:'#a9d8ff',archer:'#b8f2b2',mage:'#ead9ff'};
      c.strokeStyle=accents[cls]||'#fff';c.fillStyle=accents[cls]||'#fff';
      if(cls==='knight'){c.lineWidth=4;c.beginPath();c.moveTo(w*.37,h*.52);c.lineTo(w*.30,h*.61);c.moveTo(w*.59,h*.52);c.lineTo(w*.65,h*.61);c.stroke();c.lineWidth=2;c.strokeRect(w*.40,h*.57,w*.18,h*.08)}
      if(cls==='rogue'){c.lineWidth=3;c.beginPath();c.moveTo(w*.38,h*.55);c.lineTo(w*.29,h*.63);c.moveTo(w*.58,h*.56);c.lineTo(w*.67,h*.64);c.stroke();c.fillRect(w*.43,h*.67,w*.14,4)}
      if(cls==='tank'){c.lineWidth=5;c.beginPath();c.moveTo(w*.33,h*.52);c.lineTo(w*.24,h*.61);c.stroke();c.strokeStyle='rgba(220,238,255,.7)';c.lineWidth=2;c.strokeRect(w*.34,h*.55,w*.16,h*.09)}
      if(cls==='archer'){c.strokeStyle='rgba(216,255,220,.72)';c.lineWidth=2;c.beginPath();c.moveTo(w*.36,h*.52);c.lineTo(w*.29,h*.63);c.stroke();c.strokeStyle='rgba(152,228,147,.65)';for(let i=0;i<4;i++){c.beginPath();c.moveTo(w*.36+i*3,h*.42);c.lineTo(w*.39+i*3,h*.34);c.stroke()}}
      if(cls==='mage'){c.strokeStyle='rgba(238,220,255,.65)';c.lineWidth=2;c.beginPath();c.moveTo(w*.35,h*.56);c.lineTo(w*.28,h*.66);c.stroke();c.beginPath();c.moveTo(w*.43,h*.61);c.lineTo(w*.56,h*.61);c.stroke()}
      c.restore()
    })
  }

  function makeInfoWings(){
    if(!shell||shell.querySelector('.v023InfoWing'))return;
    const left=document.createElement('div');left.className='v023InfoWing v023Left';left.id='v023ClassInfo';
    const right=document.createElement('div');right.className='v023InfoWing v023Right';right.id='v023SkillInfo';
    shell.append(left,right);renderInfo()
  }

  function copySkillIcon(dst,cls,idx){
    const src=root.querySelector(`[data-skill="${cls}:${idx}"]`),c=dst.getContext('2d');c.clearRect(0,0,dst.width,dst.height);if(src)c.drawImage(src,0,0,dst.width,dst.height)
  }
  function renderInfo(){
    if(!root)return;const cls=CLASSES[currentClass],m=META[cls],left=document.getElementById('v023ClassInfo'),right=document.getElementById('v023SkillInfo');if(!left||!right)return;
    left.innerHTML=`<div class="v023Ko">${m.ko}</div><div class="v023Class" style="color:${m.color}">${m.name}</div><div class="v023Tag">${m.tag}</div><div class="v023Role">${m.role}</div><div class="v023Style">${m.style}</div>`;
    right.innerHTML=`<div class="v023SkillTitle">SKILL ROADMAP · Lv6 / 11 / 16 / 21 / 26 / 31</div><div class="v023SkillStrip">${m.skills.map((s,i)=>`<button class="v023SkillPick ${i===selectedSkill?'on':''}" data-v023skill="${i}" style="--skill-color:${m.color}"><canvas width="64" height="64"></canvas><div class="v023SkillLv">LV ${LEVELS[i]}</div></button>`).join('')}</div><div class="v023SkillDetail"><span class="v023SkillName" style="color:${m.color}">${m.skills[selectedSkill][0]}</span><span class="v023SkillLevel" style="color:${m.color}">LV ${LEVELS[selectedSkill]}</span><div class="v023SkillDesc">${m.skills[selectedSkill][1]}</div></div>`;
    right.querySelectorAll('[data-v023skill]').forEach((b,i)=>{copySkillIcon(b.querySelector('canvas'),cls,i);b.onclick=e=>{e.stopPropagation();selectedSkill=+b.dataset.v023skill;renderInfo()}})
  }
  function indexFromTransform(){
    const s=track?.style.transform||'',m=s.match(/translateX\((-?[\d.]+)%\)/);if(!m)return 0;return Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length
  }
  if(track){new MutationObserver(()=>{const idx=indexFromTransform();if(idx!==currentClass){currentClass=idx;selectedSkill=0;renderInfo()}}).observe(track,{attributes:true,attributeFilter:['style']})}
  refineHeroes();makeInfoWings();

  const short={knight:'KNI',rogue:'ROG',tank:'TNK',archer:'ARC',mage:'MAG'},glyph={knight:'╱',rogue:'×',tank:'▱',archer:'➝',mage:'✦'};
  function decorateAiButtons(){
    const box=document.getElementById('v022AiRows');if(!box)return;
    box.querySelectorAll('[data-aicls]').forEach(b=>{const cls=(b.dataset.aicls.split(':')[1]||'');if(!short[cls]||b.dataset.v023Decorated)return;b.dataset.v023Decorated='1';b.innerHTML=`<span class="v023RoleGlyph ${cls}">${glyph[cls]}</span><span>${short[cls]}</span>`})
  }
  const aiBox=document.getElementById('v022AiRows');if(aiBox){new MutationObserver(()=>decorateAiButtons()).observe(aiBox,{childList:true,subtree:true});decorateAiButtons()}

  const teamBtn=root?.querySelector('[data-mode="team"]'),soloBtn=root?.querySelector('[data-mode="solo"]'),ai3=root?.querySelector('[data-ai="3"]'),ai2=root?.querySelector('[data-ai="2"]'),aiLabel=document.getElementById('v022AiCount')?.previousElementSibling;
  function syncModePolish(){
    const isTeam=!!root?.querySelector('[data-mode="team"].on');
    if(ai3){ai3.style.display=isTeam?'none':'';ai3.disabled=isTeam}
    if(aiLabel)aiLabel.textContent=isTeam?'AI FILL':'AI COUNT';
    let note=document.getElementById('v023TeamRule');
    if(isTeam){if(root?.querySelector('[data-ai="3"].on')&&ai2)ai2.click();if(!note){note=document.createElement('div');note.id='v023TeamRule';note.className='v023TeamRule';document.getElementById('v022AiCount')?.insertAdjacentElement('afterend',note)}note.textContent='TEAM은 사람 참가 슬롯을 최소 1자리 남깁니다. AI는 최대 2명까지 빈 자리를 채웁니다.'}
    else if(note)note.remove();
    decorateAiButtons()
  }
  teamBtn?.addEventListener('click',()=>setTimeout(syncModePolish,0));soloBtn?.addEventListener('click',()=>setTimeout(syncModePolish,0));root?.querySelectorAll('[data-ai]').forEach(b=>b.addEventListener('click',()=>setTimeout(()=>{syncModePolish();decorateAiButtons()},0)));syncModePolish();
})();
