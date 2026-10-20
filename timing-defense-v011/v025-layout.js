// Timing Defense v0.25 — character-select vertical expansion + richer combat profile.
// Presentation-only patch. No combat balance values changed.
(function(){
  const CLASSES=['knight','rogue','tank','archer','mage'];
  const AXES=['공격력','치명타','민첩성','넉백','관통','광역'];
  const PROFILE={
    knight:[4,2,3,3,4,2],
    rogue:[2,5,5,1,1,1],
    tank:[2,1,1,5,1,3],
    archer:[3,2,4,1,5,2],
    mage:[4,2,2,1,1,5]
  };
  const META={
    knight:{name:'KNIGHT',ko:'기사',tag:'ALL-ROUNDER',color:'#ffd76a',fill:'rgba(255,215,106,.26)',role:'안정적인 전열 · 관통 검기 · 강한 4타',detail:'높은 공격력과 관통력을 바탕으로 어떤 전황에서도 꾸준히 활약하는 균형형 전사.'},
    rogue:{name:'ROGUE',ko:'도적',tag:'EXECUTION',color:'#d9e0e5',fill:'rgba(30,34,38,.78)',role:'빠른 다단히트 · 높은 치명타 · 급소 처형',detail:'치명타와 민첩성이 가장 높다. 빠르게 공격을 겹쳐 단단한 일반 적을 집중적으로 제거한다.'},
    tank:{name:'TANK',ko:'탱커',tag:'TEAM DEFENSE',color:'#69b6ff',fill:'rgba(105,182,255,.25)',role:'강한 넉백 · 성벽 보호 · 전장 제어',detail:'압도적인 넉백과 광역 충격으로 적의 진격을 늦추고 팀이 대응할 시간을 만들어낸다.'},
    archer:{name:'ARCHER',ko:'궁수',tag:'LINE CONTROL',color:'#98e493',fill:'rgba(152,228,147,.24)',role:'높은 민첩성 · 직선 관통 · 후열 제거',detail:'긴 직선 궤도를 빠르게 관통해 전열 뒤의 적까지 압박하는 원거리 관통 전문가.'},
    mage:{name:'MAGE',ko:'마법사',tag:'AREA BURST',color:'#d0aaff',fill:'rgba(208,170,255,.26)',role:'고화력 · 밀집 광역 · 연쇄 폭발',detail:'높은 공격력과 최고 수준의 광역 능력으로 적이 밀집할수록 폭발적인 효율을 낸다.'}
  };

  const style=document.createElement('style');
  style.textContent=`
    #v022Lobby .lobTop{height:34px!important;padding:7px 18px 0!important;align-items:flex-start!important}
    #v022Lobby .brand{font-size:14px!important;line-height:20px!important}
    #v022Lobby .stepDots{margin-top:4px!important}
    #v022Lobby .lobBody{height:calc(100% - 34px)!important;padding:0 14px 7px!important}
    #v022Lobby .nickRow{height:29px!important;max-width:500px!important;margin:-1px auto 2px!important;gap:10px!important}
    #v022Lobby .nickLabel{font-size:9.5px!important}
    #v022Lobby .nickInput{padding:5px 10px!important;border-radius:9px!important;font-size:11px!important}
    #v022Lobby .lobFoot{height:34px!important;align-items:flex-end!important}
    #v022Lobby .primaryBtn,#v022Lobby .ghostBtn{padding:7px 16px!important}

    #v022Lobby .carouselShell{border-radius:19px!important}
    #v022Lobby .v023InfoWing{top:1.1%!important;bottom:1.6%!important;padding:11px 13px!important}
    #v022Lobby .v023Left{left:1.15%!important;width:28.6%!important}
    #v022Lobby .v023Right{right:1.15%!important;width:37.7%!important}
    #v022Lobby .classCard .heroPane{left:30.1%!important;width:31.2%!important;top:-1%!important;bottom:-1%!important}
    #v022Lobby .classCard .heroCanvas{width:min(30vw,320px)!important;height:min(70vh,385px)!important;max-height:385px!important}
    #v022Lobby .classCard .heroName{font-size:25px!important;margin-top:-16px!important}
    #v022Lobby .navArrow.prev{left:29.8%!important}
    #v022Lobby .navArrow.next{right:38.5%!important}
    #v022Lobby .carouselDots{bottom:4px!important}

    .v025Profile{height:100%;display:flex;flex-direction:column;min-height:0}
    .v025Head{flex:0 0 auto;display:grid;grid-template-columns:1fr auto;grid-template-areas:'label ko' 'name name' 'tag tag';align-items:end;column-gap:8px}
    .v025Label{grid-area:label;font:1000 8.5px system-ui;letter-spacing:.13em;color:#9eaaa4}
    .v025Ko{grid-area:ko;font:900 10px system-ui;color:#b9c5bf;text-align:right}
    .v025Name{grid-area:name;font:1000 19px system-ui;letter-spacing:.075em;line-height:1.06;margin-top:2px;text-shadow:0 3px 14px rgba(0,0,0,.32)}
    .v025Tag{grid-area:tag;justify-self:start;margin-top:5px;padding:3px 7px;border-radius:999px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.045);font:1000 7.5px system-ui;letter-spacing:.12em;color:#d6dfda}
    .v025RadarWrap{flex:1 1 auto;min-height:150px;display:flex;align-items:center;justify-content:center;margin:1px -4px 0}
    .v025Radar{display:block;width:100%;height:100%;min-height:185px;max-height:275px}
    .v025Role{flex:0 0 auto;font:900 9.2px/1.35 system-ui;color:#e1e8e4;text-align:center;margin-top:-2px}
    .v025Detail{flex:0 0 auto;font:720 8.2px/1.42 system-ui;color:#98a8a0;text-align:center;margin:4px 2px 0}

    #v022Lobby .v024SkillHead{height:20px!important}
    #v022Lobby .v024SkillTitle{font-size:8.6px!important}
    #v022Lobby .v024SkillHint{font-size:7.3px!important}
    #v022Lobby .v024SkillGrid{height:calc(100% - 22px)!important;gap:7px!important}
    #v022Lobby .v024SkillCard{padding:7px!important;grid-template-columns:36px minmax(0,1fr)!important;column-gap:7px!important}
    #v022Lobby .v024SkillCard canvas{width:34px!important;height:34px!important}
    #v022Lobby .v024SkillName{font-size:8.8px!important}
    #v022Lobby .v024SkillDesc{font-size:7.5px!important;line-height:1.30!important}

    @media(max-height:590px){
      #v022Lobby .lobTop{height:30px!important;padding-top:5px!important}
      #v022Lobby .lobBody{height:calc(100% - 30px)!important;padding-bottom:5px!important}
      #v022Lobby .nickRow{height:25px!important;margin-top:-1px!important}
      #v022Lobby .lobFoot{height:30px!important}
      #v022Lobby .v023InfoWing{top:.8%!important;bottom:1.2%!important;padding:7px 9px!important}
      #v022Lobby .classCard .heroCanvas{height:min(68vh,285px)!important;max-height:285px!important}
      #v022Lobby .classCard .heroName{font-size:21px!important;margin-top:-18px!important}
      .v025Name{font-size:16px}.v025Ko{font-size:8.5px}.v025Tag{font-size:6.6px;padding:2px 6px}
      .v025Radar{min-height:150px;max-height:215px}.v025Role{font-size:8px}.v025Detail{font-size:7px;line-height:1.32;margin-top:2px}
      #v022Lobby .v024SkillGrid{gap:4px!important}#v022Lobby .v024SkillCard{padding:4px!important;grid-template-columns:29px minmax(0,1fr)!important;column-gap:4px!important}
      #v022Lobby .v024SkillCard canvas{width:28px!important;height:28px!important}#v022Lobby .v024SkillName{font-size:7.4px!important}#v022Lobby .v024SkillDesc{font-size:6.5px!important}
    }
  `;
  document.head.appendChild(style);

  const root=document.getElementById('v022Lobby');
  const track=document.getElementById('v022Track');
  const left=document.getElementById('v023ClassInfo');
  if(!root||!track||!left)return;

  let radarToken=0;
  let enhanceQueued=false;

  function currentIndex(){
    const s=track.style.transform||'',m=s.match(/translateX\((-?[\d.]+)%\)/);
    return m?Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length:0
  }
  function point(cx,cy,r,i){const a=-Math.PI/2+i*Math.PI/3;return[cx+Math.cos(a)*r,cy+Math.sin(a)*r]}
  function poly(c,pts){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath()}
  function easeBack(t){t=Math.max(0,Math.min(1,t));const c1=1.18,c3=c1+1;return 1+c3*(t-1)**3+c1*(t-1)**2}
  function hexToRgb(hex){const h=hex.replace('#','');return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]}

  function drawRadar(canvas,cls,start){
    const token=++radarToken,c=canvas.getContext('2d'),m=META[cls],vals=PROFILE[cls],rgb=hexToRgb(m.color);
    const W=canvas.width,H=canvas.height,cx=W/2,cy=H*.51,R=Math.min(W*.285,H*.32),labelR=R*1.30;
    function frame(now){
      if(token!==radarToken||!canvas.isConnected)return;
      const elapsed=now-start;c.clearRect(0,0,W,H);c.save();
      const bg=c.createRadialGradient(cx,cy,2,cx,cy,R*1.55);bg.addColorStop(0,`rgba(${rgb.join(',')},.10)`);bg.addColorStop(1,'rgba(255,255,255,0)');c.fillStyle=bg;c.fillRect(0,0,W,H);
      for(let ring=1;ring<=5;ring++){
        const rr=R*ring/5,pts=AXES.map((_,i)=>point(cx,cy,rr,i));
        c.strokeStyle=`rgba(224,234,228,${ring===5?.25:.11})`;c.lineWidth=ring===5?1.45:.9;poly(c,pts);c.stroke();
      }
      for(let i=0;i<6;i++){const p=point(cx,cy,R,i);c.strokeStyle='rgba(224,234,228,.105)';c.lineWidth=.9;c.beginPath();c.moveTo(cx,cy);c.lineTo(p[0],p[1]);c.stroke()}
      const scan=Math.max(0,Math.min(1,elapsed/430));
      if(scan<1){const rr=R*(.08+.98*scan),pts=AXES.map((_,i)=>point(cx,cy,rr,i));c.save();c.globalAlpha=.75*(1-scan);c.strokeStyle=m.color;c.shadowBlur=15;c.shadowColor=m.color;c.lineWidth=2.4;poly(c,pts);c.stroke();c.restore()}
      const pts=[];
      for(let i=0;i<6;i++){
        const delay=70+i*62,t=Math.max(0,Math.min(1,(elapsed-delay)/460)),rr=R*(vals[i]/5)*easeBack(t);pts.push(point(cx,cy,rr,i));
      }
      const fillT=Math.max(0,Math.min(1,(elapsed-150)/510));
      if(fillT>0){
        c.save();c.globalAlpha=.18+.82*fillT;c.fillStyle=m.fill;c.strokeStyle=m.color;c.lineWidth=2.4;c.shadowBlur=20*fillT;c.shadowColor=m.color;poly(c,pts);c.fill();c.stroke();c.restore();
      }
      for(let i=0;i<6;i++){
        const delay=70+i*62,t=Math.max(0,Math.min(1,(elapsed-delay)/460)),p=pts[i];
        if(t<=0)continue;
        const pulse=1+1.8*Math.sin(Math.min(1,t)*Math.PI);c.save();c.globalAlpha=t;c.shadowBlur=11;c.shadowColor=m.color;c.fillStyle=m.color;c.beginPath();c.arc(p[0],p[1],3.1+pulse,0,Math.PI*2);c.fill();c.restore();
      }
      c.textAlign='center';c.textBaseline='middle';c.font='1000 16px system-ui';
      for(let i=0;i<6;i++){
        const p=point(cx,cy,labelR,i);c.lineWidth=4.2;c.strokeStyle='rgba(4,9,7,.82)';c.strokeText(AXES[i],p[0],p[1]);c.fillStyle=i===0?m.color:'rgba(238,243,240,.95)';c.fillText(AXES[i],p[0],p[1]);
      }
      const settle=Math.max(0,Math.min(1,(elapsed-610)/430));
      if(settle>0&&settle<1){c.save();c.globalAlpha=.22*(1-settle);c.strokeStyle=m.color;c.lineWidth=2;c.shadowBlur=12;c.shadowColor=m.color;c.beginPath();c.arc(cx,cy,R*(.18+1.08*settle),0,Math.PI*2);c.stroke();c.restore()}
      c.restore();
      if(elapsed<1080)requestAnimationFrame(frame)
    }
    requestAnimationFrame(frame)
  }

  function enhance(){
    enhanceQueued=false;
    const idx=currentIndex(),cls=CLASSES[idx],m=META[cls];
    if(left.dataset.v025Class===cls&&left.querySelector('.v025Profile'))return;
    left.dataset.v025Class=cls;
    left.innerHTML=`<div class="v025Profile">
      <div class="v025Head"><span class="v025Label">COMBAT PROFILE</span><span class="v025Ko">${m.ko}</span><div class="v025Name" style="color:${m.color}">${m.name}</div><div class="v025Tag">${m.tag}</div></div>
      <div class="v025RadarWrap"><canvas class="v025Radar" width="330" height="280"></canvas></div>
      <div class="v025Role">${m.role}</div><div class="v025Detail">${m.detail}</div>
    </div>`;
    const canvas=left.querySelector('.v025Radar');if(canvas)drawRadar(canvas,cls,performance.now())
  }
  function queueEnhance(){if(enhanceQueued)return;enhanceQueued=true;requestAnimationFrame(()=>requestAnimationFrame(enhance))}

  new MutationObserver(()=>{if(!left.querySelector('.v025Profile'))queueEnhance()}).observe(left,{childList:true});
  new MutationObserver(()=>queueEnhance()).observe(track,{attributes:true,attributeFilter:['style']});
  queueEnhance();
})();
