// Timing Defense v0.26 — lobby card reflow + combat HUD/base polish.
// Presentation/input reliability only. Combo behavior and combat balance are unchanged.
(function(){
  const root=document.getElementById('v022Lobby');
  const right=document.getElementById('v023SkillInfo');

  const style=document.createElement('style');
  style.textContent=`
    /* Combat: remove the legacy prototype title/stats strip. Lobby brand is separate. */
    #topbar{display:none!important}

    /* Character-select skill cards: icon + name/level header, full-width description below. */
    #v022Lobby .v024SkillGrid{gap:7px!important}
    #v022Lobby .v024SkillCard{
      padding:7px 8px!important;
      display:grid!important;
      grid-template-columns:40px minmax(0,1fr)!important;
      grid-template-rows:auto minmax(0,1fr)!important;
      column-gap:8px!important;
      row-gap:5px!important;
      align-items:start!important;
    }
    #v022Lobby .v024SkillCard canvas{
      grid-column:1!important;grid-row:1!important;
      width:38px!important;height:38px!important;
      align-self:start!important
    }
    #v022Lobby .v024SkillName{
      grid-column:2!important;grid-row:1!important;
      display:flex!important;flex-direction:column!important;align-items:flex-start!important;
      gap:3px!important;font-size:10px!important;line-height:1.12!important;
      white-space:normal!important;overflow:visible!important
    }
    #v022Lobby .v024SkillLv{
      display:block!important;margin:0!important;
      font-size:7.8px!important;line-height:1!important;
      color:#aebbb4!important;letter-spacing:.03em!important
    }
    #v022Lobby .v024SkillDesc{
      grid-column:1 / -1!important;grid-row:2!important;
      margin:0!important;padding-top:1px!important;
      font-size:8.7px!important;line-height:1.34!important;
      color:#b9c5bf!important;white-space:normal!important;overflow:visible!important
    }

    /* Left profile: move radar upward and guarantee room for both role + full description. */
    #v022Lobby .v025RadarWrap{
      flex:0 0 min(34vh,210px)!important;
      min-height:0!important;
      margin:-7px -4px -3px!important;
      align-items:flex-start!important
    }
    #v022Lobby .v025Radar{height:100%!important;min-height:0!important;max-height:none!important}
    #v022Lobby .v025Role{font-size:9.5px!important;line-height:1.34!important;margin-top:0!important}
    #v022Lobby .v025Detail{font-size:8.6px!important;line-height:1.42!important;margin:5px 2px 0!important;color:#aab8b1!important}

    /* Hero class name belongs above the head, not under the feet. */
    #v022Lobby .classCard .heroPane{position:absolute!important}
    #v022Lobby .classCard .heroName{
      position:absolute!important;top:2.2%!important;left:50%!important;
      transform:translateX(-50%)!important;margin:0!important;
      z-index:7!important;font-size:24px!important;line-height:1!important;
      white-space:nowrap!important;pointer-events:none!important
    }
    #v022Lobby .classCard .heroCanvas{transform:translateY(9px)!important}

    /* Fixed navigation coordinates + no active-state jump. */
    #v022Lobby .navArrow{
      width:44px!important;height:60px!important;z-index:12!important;
      touch-action:manipulation!important;user-select:none!important;-webkit-user-select:none!important;
      pointer-events:auto!important
    }
    #v022Lobby .navArrow.prev{left:29.1%!important;right:auto!important}
    #v022Lobby .navArrow.next{left:58.3%!important;right:auto!important}
    #v022Lobby .navArrow:active{transform:translateY(-50%)!important}

    /* Formal combat HUD. */
    #v026CombatHud{position:absolute;inset:0;display:none;pointer-events:none;color:#f5f8f6;font-family:Inter,system-ui,sans-serif}
    #v026CombatHud.show{display:block}
    .v026BaseHud{
      position:absolute;top:8px;left:50%;transform:translateX(-50%);
      width:min(38vw,440px);min-width:280px;
      padding:6px 10px 8px;border:1px solid rgba(255,255,255,.18);border-radius:11px;
      background:rgba(15,23,23,.70);box-shadow:0 5px 18px rgba(0,0,0,.22);backdrop-filter:blur(4px)
    }
    .v026BaseLine{display:flex;align-items:center;justify-content:center;gap:7px;font-size:9px;font-weight:950;letter-spacing:.06em;margin-bottom:5px}
    .v026BaseIcon{width:13px;height:13px;display:inline-flex;color:#dbe7df}
    .v026BaseIcon svg,.v026HudIcon svg{width:100%;height:100%;display:block}
    .v026BaseValue{color:#eef5f0;font-weight:1000}
    .v026BaseTrack{height:7px;border-radius:99px;background:rgba(0,0,0,.40);overflow:hidden;border:1px solid rgba(255,255,255,.08)}
    .v026BaseFill{height:100%;width:100%;border-radius:99px;background:#9fe0ba;box-shadow:0 0 10px rgba(159,224,186,.30);transition:width .16s linear,background .18s ease}
    .v026RunHud{position:absolute;top:8px;right:14px;display:flex;gap:5px;align-items:center}
    .v026HudChip{height:29px;min-width:70px;padding:0 9px;display:flex;align-items:center;justify-content:center;gap:6px;border:1px solid rgba(255,255,255,.15);border-radius:9px;background:rgba(15,23,23,.68);box-shadow:0 4px 15px rgba(0,0,0,.18);backdrop-filter:blur(4px);font-size:9px;font-weight:950;letter-spacing:.025em;white-space:nowrap}
    .v026HudIcon{width:13px;height:13px;display:inline-flex;color:#e5eee8}
    .v026HudChip.stage .v026HudIcon{color:#f0d98c}.v026HudChip.level .v026HudIcon{color:#a9d8ff}.v026HudChip.kills .v026HudIcon{color:#f0b39a}

    @media(max-height:590px){
      #v022Lobby .v025RadarWrap{flex-basis:min(31vh,178px)!important;margin-top:-9px!important}
      #v022Lobby .v025Role{font-size:8.5px!important}
      #v022Lobby .v025Detail{font-size:7.6px!important;line-height:1.35!important;margin-top:3px!important}
      #v022Lobby .v024SkillCard{padding:5px 6px!important;grid-template-columns:34px minmax(0,1fr)!important;gap:3px 6px!important}
      #v022Lobby .v024SkillCard canvas{width:32px!important;height:32px!important}
      #v022Lobby .v024SkillName{font-size:8.5px!important;gap:2px!important}
      #v022Lobby .v024SkillLv{font-size:6.8px!important}
      #v022Lobby .v024SkillDesc{font-size:7.5px!important;line-height:1.28!important}
      #v022Lobby .classCard .heroName{font-size:21px!important;top:1.8%!important}
      #v022Lobby .navArrow{width:42px!important;height:56px!important}
      .v026BaseHud{top:6px;width:min(36vw,370px);min-width:245px;padding:5px 8px 6px}.v026BaseLine{font-size:8px;margin-bottom:4px}.v026BaseTrack{height:6px}
      .v026RunHud{top:6px;right:10px}.v026HudChip{height:26px;min-width:62px;padding:0 7px;font-size:8px;gap:4px}.v026HudIcon{width:11px;height:11px}
    }
  `;
  document.head.appendChild(style);

  function normalizeSkillCards(){
    if(!right)return;
    right.querySelectorAll('.v024SkillLv').forEach(el=>{
      const raw=(el.textContent||'').trim().replace(/^습득\s*/,'');
      const next=`습득 ${raw}`;
      if(el.textContent!==next)el.textContent=next;
    });
  }
  if(right){
    new MutationObserver(()=>normalizeSkillCards()).observe(right,{childList:true,subtree:true});
    normalizeSkillCards();
  }

  /* Prevent carousel swipe tracking from stealing arrow taps. Keep the existing moveClass closure. */
  for(const id of ['v022Prev','v022Next']){
    const b=document.getElementById(id);if(!b)continue;
    b.addEventListener('pointerdown',e=>{e.stopPropagation();try{b.setPointerCapture(e.pointerId)}catch(_){}});
    b.addEventListener('pointerup',e=>{e.stopPropagation();try{b.releasePointerCapture(e.pointerId)}catch(_){}});
    b.addEventListener('pointercancel',e=>e.stopPropagation());
    b.addEventListener('touchstart',e=>e.stopPropagation(),{passive:true});
  }

  /* Hide legacy canvas footer stats and old small wall-HP label; their information now has dedicated HUD. */
  const nativeFillText=ctx.fillText.bind(ctx);
  ctx.fillText=function(text,...args){
    const s=String(text??'');
    if(/^WALL HP\s/.test(s))return;
    if(/^TEAM \d+\/4 · STAGE /.test(s))return;
    if(/^COIN .* · WALL .* · ENEMIES /.test(s))return;
    return nativeFillText(text,...args)
  };

  /* Improved fortified home-base body. Drawn after the natural background and before characters. */
  const previousBackground=drawBackground;
  drawBackground=function(){
    previousBackground();
    const x=W*.030,w=W*.121,top=H*.145,bottom=H*.845,capH=H*.073;
    ctx.save();
    const body=ctx.createLinearGradient(x,0,x+w,0);
    body.addColorStop(0,'rgba(28,39,40,.98)');body.addColorStop(.48,'rgba(49,63,61,.98)');body.addColorStop(1,'rgba(25,36,37,.98)');
    ctx.fillStyle=body;rr(x,top+capH*.55,w,bottom-(top+capH*.55),4);ctx.fill();
    ctx.strokeStyle='rgba(219,230,224,.20)';ctx.lineWidth=1.4;rr(x,top+capH*.55,w,bottom-(top+capH*.55),4);ctx.stroke();

    /* top armored cap intentionally covers the obsolete tiny HP gauge */
    const cap=ctx.createLinearGradient(0,top,0,top+capH);
    cap.addColorStop(0,'rgba(57,72,70,.99)');cap.addColorStop(1,'rgba(29,41,42,.99)');
    ctx.fillStyle=cap;rr(x-W*.004,top,w+W*.008,capH,7);ctx.fill();
    ctx.strokeStyle='rgba(230,238,233,.24)';ctx.lineWidth=1.4;rr(x-W*.004,top,w+W*.008,capH,7);ctx.stroke();

    /* crenellated silhouette */
    const crenelY=top-H*.020,crenelW=w/7;
    ctx.fillStyle='rgba(38,51,51,.99)';
    for(let i=0;i<7;i+=2){rr(x+i*crenelW,crenelY,crenelW*.82,H*.031,3);ctx.fill()}

    /* reinforced side columns */
    for(const px of [x+W*.004,x+w-W*.014]){
      const pg=ctx.createLinearGradient(px,0,px+W*.012,0);pg.addColorStop(0,'rgba(80,94,90,.42)');pg.addColorStop(1,'rgba(18,28,30,.58)');
      ctx.fillStyle=pg;rr(px,top+capH*.67,W*.011,bottom-top-capH*.72,3);ctx.fill();
      ctx.strokeStyle='rgba(225,233,228,.14)';ctx.stroke();
    }

    /* four inset bays and character platforms */
    for(let i=0;i<4;i++){
      const y=charBase(i).y,cy=y+H*.016,bayH=H*.122;
      ctx.fillStyle='rgba(4,10,11,.20)';rr(x+W*.016,cy-bayH*.50,w-W*.032,bayH,7);ctx.fill();
      ctx.strokeStyle='rgba(222,232,226,.10)';ctx.lineWidth=1;rr(x+W*.016,cy-bayH*.50,w-W*.032,bayH,7);ctx.stroke();
      const ledgeY=y+H*.033;
      ctx.fillStyle='rgba(101,115,108,.60)';rr(x+W*.009,ledgeY,w+W*.012,H*.010,3);ctx.fill();
      ctx.fillStyle='rgba(225,232,226,.18)';ctx.fillRect(x+W*.013,ledgeY,w+W*.003,1.2);
    }

    /* small central crest — visual identity only */
    const cx=x+w*.5,cy=top+capH*.52;
    ctx.strokeStyle='rgba(222,232,226,.34)';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(cx,cy-H*.020);ctx.lineTo(cx+W*.010,cy-H*.005);ctx.lineTo(cx+W*.007,cy+H*.018);ctx.lineTo(cx,cy+H*.026);ctx.lineTo(cx-W*.007,cy+H*.018);ctx.lineTo(cx-W*.010,cy-H*.005);ctx.closePath();ctx.stroke();
    ctx.restore();
  };

  /* Use the exact class-selection skill artwork in the combat six-slot strip. */
  drawSkillIcon=function(now){
    const g=squareGeom(),count=typeof v016SkillCount==='function'?v016SkillCount():0;
    const gap=4,slot=Math.max(16,Math.min(20,g.size*.18)),total=slot*6+gap*5,start=g.x+g.size*.5-total*.5,y=g.y+g.size+10;
    ctx.save();
    for(let i=0;i<6;i++){
      const x=start+i*(slot+gap),active=i<count;
      const just=active&&typeof V016_UNLOCKS!=='undefined'&&V016_UNLOCKS[i]===S.v016SkillNoticeLevel&&now<S.skillNoticeUntil;
      if(just){ctx.shadowBlur=11;ctx.shadowColor='rgba(255,240,190,.72)'}
      ctx.fillStyle='rgba(6,10,11,.68)';rr(x,y,slot,slot,Math.max(3,slot*.20));ctx.fill();ctx.shadowBlur=0;
      const src=document.querySelector(`[data-skill="${S.playerClass}:${i}"]`);
      if(src){
        ctx.save();ctx.globalAlpha=active?1:.24;if(!active)ctx.filter='grayscale(1) brightness(.72)';
        ctx.drawImage(src,x+1,y+1,slot-2,slot-2);ctx.restore();
      }else if(typeof v016DrawSkillGlyph==='function'){
        v016DrawSkillGlyph(x+slot/2,y+slot/2,slot*.40,i,classColor(),active)
      }
      ctx.strokeStyle=active?'rgba(238,244,240,.46)':'rgba(255,255,255,.10)';ctx.lineWidth=just?2:1;rr(x,y,slot,slot,Math.max(3,slot*.20));ctx.stroke();
    }
    ctx.restore();
  };

  /* Formal top HUD. */
  const ui=document.getElementById('ui');
  if(ui){
    const hud=document.createElement('div');hud.id='v026CombatHud';
    hud.innerHTML=`
      <div class="v026BaseHud">
        <div class="v026BaseLine"><span class="v026BaseIcon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9l8-5 8 5v9H4z"/><path d="M8 18v-5h8v5"/></svg></span><span>BASE HP</span><span id="v026BaseValue" class="v026BaseValue">0 / 0</span></div>
        <div class="v026BaseTrack"><div id="v026BaseFill" class="v026BaseFill"></div></div>
      </div>
      <div class="v026RunHud">
        <div class="v026HudChip stage"><span class="v026HudIcon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 21V4"/><path d="M6 5h11l-2.5 3L17 11H6"/></svg></span><span id="v026Stage">STAGE 1</span></div>
        <div class="v026HudChip level"><span class="v026HudIcon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l3 6 6 .8-4.5 4.3 1.1 6.1L12 17l-5.6 3.2 1.1-6.1L3 9.8 9 9z"/></svg></span><span id="v026Level">LV 1</span></div>
        <div class="v026HudChip kills"><span class="v026HudIcon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="10" r="7"/><path d="M8 17v3m4-3v3m4-3v3M9 9h.01M15 9h.01M10 13h4"/></svg></span><span id="v026Kills">KILLS 0</span></div>
      </div>`;
    ui.appendChild(hud);

    const stageEl=document.getElementById('v026Stage'),levelEl=document.getElementById('v026Level'),killsEl=document.getElementById('v026Kills'),baseValue=document.getElementById('v026BaseValue'),baseFill=document.getElementById('v026BaseFill');
    function updateHud(){
      const visible=!S.v022LobbyOpen&&!S.gameOver&&!S.runComplete&&(S.stageMode==='combat'||S.stageMode==='intro');
      hud.classList.toggle('show',visible);if(!visible)return;
      stageEl.textContent=`STAGE ${S.stage}`;levelEl.textContent=`LV ${S.level}`;killsEl.textContent=`KILLS ${S.kills}`;
      const max=Math.max(1,Number(S.baseHpMax)||1),hp=Math.max(0,Number(S.baseHp)||0),ratio=Math.max(0,Math.min(1,hp/max));
      baseValue.textContent=`${Math.ceil(hp)} / ${Math.ceil(max)}`;baseFill.style.width=`${ratio*100}%`;
      baseFill.style.background=ratio>.5?'#9fe0ba':ratio>.25?'#f0d98c':'#ef7d72';
    }
    const previousDraw=draw;
    draw=function(now){previousDraw(now);updateHud()};
    updateHud();
  }
})();
