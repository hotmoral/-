// Timing Defense v0.27 — device-fix pass + truthful TEAM waiting-room UX.
// Presentation / input UX only. Combo behavior and combat balance are unchanged.
(function(){
  const root=document.getElementById('v022Lobby');
  const shell=root?.querySelector('.carouselShell');
  const track=document.getElementById('v022Track');
  const prev=document.getElementById('v022Prev');
  const next=document.getElementById('v022Next');
  const startBtn=document.getElementById('v022Start');
  const CLASSES=['knight','rogue','tank','archer','mage'];
  const CLASS_META={
    knight:{name:'KNIGHT',ko:'기사',color:'#ffd76a'},
    rogue:{name:'ROGUE',ko:'도적',color:'#d9e0e5'},
    tank:{name:'TANK',ko:'탱커',color:'#69b6ff'},
    archer:{name:'ARCHER',ko:'궁수',color:'#98e493'},
    mage:{name:'MAGE',ko:'마법사',color:'#d0aaff'}
  };

  const style=document.createElement('style');
  style.textContent=`
    #v022Lobby .v024SkillCard{grid-template-columns:38px minmax(0,1fr)!important;column-gap:6px!important;row-gap:4px!important;padding:6px 7px!important}
    #v022Lobby .v024SkillCard canvas{width:36px!important;height:36px!important}
    #v022Lobby .v024SkillName{display:flex!important;flex-direction:column!important;align-items:flex-start!important;gap:2px!important;font-size:8.3px!important;line-height:1.05!important;letter-spacing:-.045em!important;white-space:nowrap!important;word-break:keep-all!important;overflow:visible!important}
    #v022Lobby .v024SkillLv{display:block!important;font-size:6.8px!important;line-height:1!important;letter-spacing:-.02em!important;white-space:nowrap!important;word-break:keep-all!important}
    #v022Lobby .v024SkillDesc{font-size:8.1px!important;line-height:1.30!important;word-break:keep-all!important}
    #v022Lobby .v025RadarWrap{flex:0 0 205px!important;min-height:0!important;margin:-10px -3px -6px!important;align-items:center!important;justify-content:center!important;overflow:visible!important}
    #v022Lobby .v025Radar{height:100%!important;width:auto!important;max-width:100%!important;min-height:0!important;max-height:100%!important;aspect-ratio:330/280!important;object-fit:contain!important}
    #v022Lobby .v025Role{margin-top:0!important}
    #v022Lobby .v025Detail{margin-top:4px!important}
    #v022Lobby .carouselShell{touch-action:pan-y!important;overscroll-behavior:contain!important}
    #v027Waiting{position:absolute;inset:0;z-index:40;display:none;background:linear-gradient(145deg,#172621 0%,#263b31 46%,#18251f 100%);color:#f5faf7;font-family:Inter,system-ui,sans-serif;padding:18px 24px 16px}
    #v027Waiting.show{display:flex;flex-direction:column}
    .v027WaitTop{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:34px}
    .v027WaitBrand{font:1000 14px system-ui;letter-spacing:.11em}.v027WaitMode{font:900 8px system-ui;letter-spacing:.12em;color:#9fb0a7;padding:5px 9px;border:1px solid rgba(255,255,255,.12);border-radius:999px;background:rgba(255,255,255,.035)}
    .v027WaitBody{flex:1;min-height:0;display:grid;grid-template-columns:38% 62%;gap:10px;margin-top:8px}
    .v027WaitPanel{min-height:0;border:1px solid rgba(255,255,255,.10);border-radius:18px;background:rgba(7,12,10,.36);padding:14px 16px;overflow:hidden}
    .v027WaitTitle{font:1000 18px system-ui;letter-spacing:.035em}.v027WaitSub{font:730 9px/1.5 system-ui;color:#98a89f;margin-top:6px}.v027Method{display:inline-flex;margin-top:12px;padding:5px 9px;border-radius:999px;background:#eadcaf;color:#17201b;font:1000 8px system-ui;letter-spacing:.08em}
    .v027LocalCard{margin-top:14px;padding:11px 12px;border:1px solid rgba(255,255,255,.10);border-radius:13px;background:rgba(255,255,255,.035)}
    .v027LocalTop{display:flex;align-items:center;justify-content:space-between;gap:8px}.v027Nick{font:1000 13px system-ui}.v027Class{font:1000 10px system-ui;letter-spacing:.055em}.v027Truth{margin-top:12px;padding:9px 10px;border-radius:10px;background:rgba(0,0,0,.20);font:750 8px/1.45 system-ui;color:#9fb0a7}
    .v027WaitActions{display:flex;gap:7px;margin-top:10px;flex-wrap:wrap}.v027WaitBtn{border:1px solid rgba(255,255,255,.13);border-radius:9px;background:rgba(8,13,11,.62);color:#dce6df;padding:7px 11px;font:950 9px system-ui}.v027WaitBtn.primary{background:#efe0ac;color:#17201b;border-color:#efe0ac}.v027WaitBtn:disabled{opacity:.35}
    .v027SlotTitle{font:1000 10px system-ui;letter-spacing:.10em;color:#a9b7af;margin-bottom:8px}.v027Slots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.v027Slot{height:86px;border:1px solid rgba(255,255,255,.09);border-radius:12px;background:rgba(255,255,255,.025);padding:10px;display:flex;flex-direction:column;justify-content:space-between}.v027SlotHead{display:flex;justify-content:space-between;align-items:center;font:1000 8px system-ui;color:#86988e}.v027SlotName{font:1000 12px system-ui}.v027SlotSub{font:800 8px system-ui;color:#9fb0a7}.v027Slot.local{border-color:rgba(239,224,172,.42);background:rgba(239,224,172,.055)}.v027Slot.ai{border-color:rgba(143,186,221,.22)}.v027Slot.open{border-style:dashed}
    .v027SearchBox{margin-top:10px;padding:10px;border:1px dashed rgba(255,255,255,.16);border-radius:11px;font:800 8px/1.45 system-ui;color:#a6b5ad;display:none}.v027SearchBox.show{display:block}.v027Pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:#efe0ac;margin-right:6px;animation:v027Pulse 1s ease-in-out infinite}@keyframes v027Pulse{0%,100%{opacity:.3;transform:scale(.75)}50%{opacity:1;transform:scale(1.15)}}
    .v027WaitFoot{height:42px;display:flex;align-items:flex-end;justify-content:space-between;gap:8px}.v027WaitNote{font:760 8px system-ui;color:#83958b}
    @media(max-height:590px){
      #v022Lobby .v024SkillCard{padding:4px 5px!important;grid-template-columns:31px minmax(0,1fr)!important;column-gap:5px!important;row-gap:2px!important}
      #v022Lobby .v024SkillCard canvas{width:30px!important;height:30px!important}
      #v022Lobby .v024SkillName{font-size:7.2px!important}.v024SkillLv{font-size:6.2px!important}.v024SkillDesc{font-size:7.0px!important;line-height:1.24!important}
      #v022Lobby .v025RadarWrap{flex-basis:178px!important;margin-top:-11px!important;margin-bottom:-8px!important}
      #v027Waiting{padding:10px 16px 9px}.v027WaitBody{margin-top:5px}.v027WaitPanel{padding:9px 11px}.v027WaitTitle{font-size:15px}.v027WaitSub{font-size:8px;margin-top:3px}.v027LocalCard{margin-top:8px;padding:8px 9px}.v027Truth{margin-top:7px;padding:6px 8px}.v027WaitActions{margin-top:6px}.v027Slot{height:68px;padding:7px}.v027SlotName{font-size:10px}.v027WaitFoot{height:32px}
    }
  `;
  document.head.appendChild(style);
  function normalizeSkillLevels(){root?.querySelectorAll('.v024SkillLv').forEach(el=>{const n=(el.textContent||'').match(/\d+/)?.[0]||'';if(n)el.textContent=`습득 LV ${n}`})}
  if(root){new MutationObserver(normalizeSkillLevels).observe(root,{childList:true,subtree:true});normalizeSkillLevels()}
  if(shell&&prev&&next){
    let pid=null,startX=0,startY=0,lastX=0,lastY=0,dragging=false;
    const down=e=>{if(e.target.closest('.navArrow,button,input'))return;pid=e.pointerId;startX=lastX=e.clientX;startY=lastY=e.clientY;dragging=false;try{shell.setPointerCapture(pid)}catch(_){ }e.stopImmediatePropagation()};
    const move=e=>{if(pid!==e.pointerId)return;lastX=e.clientX;lastY=e.clientY;const dx=lastX-startX,dy=lastY-startY;if(Math.abs(dx)>10&&Math.abs(dx)>Math.abs(dy)*1.15){dragging=true;e.preventDefault()}e.stopImmediatePropagation()};
    const end=e=>{if(pid!==e.pointerId)return;const dx=(e.clientX??lastX)-startX,dy=(e.clientY??lastY)-startY;try{shell.releasePointerCapture(pid)}catch(_){ }pid=null;e.stopImmediatePropagation();if(dragging&&Math.abs(dx)>38&&Math.abs(dx)>Math.abs(dy)*1.15){(dx<0?next:prev).click()}dragging=false};
    shell.addEventListener('pointerdown',down,true);shell.addEventListener('pointermove',move,{capture:true,passive:false});shell.addEventListener('pointerup',end,true);shell.addEventListener('pointercancel',end,true)
  }
  let waiting=null,ready=false,searching=false;
  function currentClass(){const s=track?.style.transform||'',m=s.match(/translateX\((-?[\d.]+)%\)/);const idx=m?Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length:0;return CLASSES[idx]||'knight'}
  function selectedMethod(){return root?.querySelector('[data-method].on')?.dataset.method||'friend'}
  function selectedMode(){return root?.querySelector('[data-mode].on')?.dataset.mode||'solo'}
  function selectedAI(){const out=[];root?.querySelectorAll('#v022AiRows .aiRow').forEach(row=>{const pb=row.querySelector('[data-pos].on'),cb=row.querySelector('[data-aicls].on');if(!pb||!cb)return;const p=Number(pb.dataset.pos.split(':')[1]),cls=cb.dataset.aicls.split(':')[1];if(p>=2&&p<=4&&CLASS_META[cls])out.push({pos:p,cls})});return out.slice(0,2)}
  function escapeHtml(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
  function methodLabel(m){return m==='friend'?'FRIEND':m==='link'?'LINK':'RANDOM'}
  function methodCopy(m){if(m==='friend')return '친구 초대형 대기실입니다. 실제 초대 전송은 네트워크 백엔드 연결 이후 활성화됩니다.';if(m==='link')return '링크 참가형 대기실입니다. 아직 실제 방 URL은 발급하지 않으며 가짜 링크를 표시하지 않습니다.';return '랜덤 매칭 대기 UI입니다. 현재 매칭 서버가 없으므로 실제 상대를 찾았다고 표시하지 않습니다.'}
  function slotHtml(pos,local,ai){
    if(local){const cls=currentClass(),m=CLASS_META[cls],nick=(document.getElementById('v022Nick')?.value.trim()||S.v022Nickname||'PLAYER');return `<div class="v027Slot local"><div class="v027SlotHead"><span>P${pos}</span><span>YOU</span></div><div class="v027SlotName">${escapeHtml(nick)}</div><div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div></div>`}
    if(ai){const m=CLASS_META[ai.cls];return `<div class="v027Slot ai"><div class="v027SlotHead"><span>P${pos}</span><span>AI FILL</span></div><div class="v027SlotName">CPU ${pos}</div><div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div></div>`}
    return `<div class="v027Slot open"><div class="v027SlotHead"><span>P${pos}</span><span>HUMAN SLOT</span></div><div class="v027SlotName">WAITING</div><div class="v027SlotSub">원격 참가자 연결 전</div></div>`
  }
  function renderWaiting(){
    if(!waiting)return;const method=selectedMethod(),cls=currentClass(),m=CLASS_META[cls],nick=(document.getElementById('v022Nick')?.value.trim()||S.v022Nickname||'PLAYER'),ais=selectedAI(),byPos=new Map(ais.map(a=>[a.pos,a]));
    waiting.innerHTML=`<div class="v027WaitTop"><div class="v027WaitBrand">TIMING DEFENSE</div><div class="v027WaitMode">TEAM · ${methodLabel(method)}</div></div><div class="v027WaitBody"><section class="v027WaitPanel"><div class="v027WaitTitle">TEAM WAITING ROOM</div><div class="v027WaitSub">선택한 캐릭터와 AI FILL을 유지한 채 사람 참가 슬롯을 기다립니다.</div><div class="v027Method">${methodLabel(method)}</div><div class="v027LocalCard"><div class="v027LocalTop"><span class="v027Nick">${escapeHtml(nick)}</span><span class="v027Class" style="color:${m.color}">${m.ko} · ${m.name}</span></div><div class="v027Truth">${methodCopy(method)}</div></div><div class="v027WaitActions"><button class="v027WaitBtn primary" id="v027Ready">${ready?'READY ✓':'READY'}</button>${method==='friend'?'<button class="v027WaitBtn" id="v027Invite">INVITE</button>':''}${method==='link'?'<button class="v027WaitBtn" id="v027Link">ROOM LINK</button>':''}${method==='random'?`<button class="v027WaitBtn" id="v027Search">${searching?'CANCEL SEARCH':'SEARCH'}</button>`:''}</div><div id="v027SearchBox" class="v027SearchBox ${searching?'show':''}">${searching?'<span class="v027Pulse"></span>SEARCHING UI · NETWORK NOT CONNECTED':'실제 네트워크 기능은 다음 구현 단계에서 연결됩니다.'}</div></section><section class="v027WaitPanel"><div class="v027SlotTitle">PARTICIPANT SLOTS</div><div class="v027Slots">${slotHtml(1,true,null)}${[2,3,4].map(p=>slotHtml(p,false,byPos.get(p))).join('')}</div></section></div><div class="v027WaitFoot"><button class="v027WaitBtn" id="v027WaitBack">← PLAY SETTING</button><div class="v027WaitNote">START는 실제 참가자 동기화/방 권한 구현 후 활성화됩니다.</div><button class="v027WaitBtn" disabled>START</button></div>`;
    waiting.querySelector('#v027WaitBack').onclick=()=>{searching=false;waiting.classList.remove('show')};waiting.querySelector('#v027Ready').onclick=()=>{ready=!ready;renderWaiting()};const invite=waiting.querySelector('#v027Invite');if(invite)invite.onclick=()=>{const box=waiting.querySelector('#v027SearchBox');box.classList.add('show');box.textContent='초대 전송은 아직 비활성화되어 있습니다. 네트워크 백엔드 연결 후 활성화됩니다.'};const link=waiting.querySelector('#v027Link');if(link)link.onclick=()=>{const box=waiting.querySelector('#v027SearchBox');box.classList.add('show');box.textContent='실제 방 링크는 아직 발급되지 않습니다. 가짜 링크는 생성하지 않습니다.'};const search=waiting.querySelector('#v027Search');if(search)search.onclick=()=>{searching=!searching;renderWaiting()}
  }
  if(root&&startBtn){waiting=document.createElement('div');waiting.id='v027Waiting';root.appendChild(waiting);startBtn.addEventListener('click',e=>{if(selectedMode()!=='team')return;e.preventDefault();e.stopImmediatePropagation();ready=false;searching=false;renderWaiting();waiting.classList.add('show')},true)}
  function fresh(){return{kills:0,damage:0,coin:0,perfects:0,maxCombo:0}}
  function resultRows(){const localName=(S.v022Nickname||'YOU').trim()||'YOU';const out=[{slot:0,label:localName,cls:S.playerClass,kills:S.v019Stats?.[0]?.kills||0,damage:S.v019Stats?.[0]?.damage||0,coin:S.v019Stats?.[0]?.coin||0,level:S.level||1,levelScore:(S.level||1)*100000+(S.xp||0),maxCombo:S.v018ComboPeak||0,perfects:S.stats?.perfect||0}];for(const ai of S.ai){const st=S.v019Stats?.[ai.slot]||fresh();out.push({slot:ai.slot,label:`CPU ${ai.slot}`,cls:ai.cls,kills:st.kills||0,damage:st.damage||0,coin:st.coin||0,level:ai.level||1,levelScore:(ai.level||1)*100000+(ai.xp||0),maxCombo:st.maxCombo||0,perfects:st.perfects||0})}return out.sort((a,b)=>a.slot-b.slot)}
  const metrics=[{key:'kills',label:'KILLS',fmt:v=>String(v),tie:r=>r.damage},{key:'damage',label:'DMG',fmt:v=>v>=10000?`${(v/1000).toFixed(1)}K`:String(Math.round(v)),tie:r=>r.kills},{key:'coin',label:'COIN',fmt:v=>String(v),tie:r=>r.kills},{key:'level',score:'levelScore',label:'LV',fmt:v=>String(v),tie:r=>r.perfects},{key:'maxCombo',label:'MAX COMBO',fmt:v=>String(v),tie:r=>r.perfects}];
  function ranks(rs,m){const k=m.score||m.key,sorted=[...rs].sort((a,b)=>((b[k]||0)-(a[k]||0))||((m.tie?m.tie(b):0)-(m.tie?m.tie(a):0))||(a.slot-b.slot));const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map}
  const rankColor={1:'#ffd65a',2:'#d9e2ea',3:'#c98b5d',4:'#7f93a6'};
  function fitText(text,maxW,font){ctx.save();ctx.font=font;if(ctx.measureText(text).width<=maxW){ctx.restore();return text}let s=text;while(s.length>1&&ctx.measureText(s+'…').width>maxW)s=s.slice(0,-1);ctx.restore();return s+'…'}
  function drawResultV027(){
    if(S.v022LobbyOpen||!(S.gameOver||S.runComplete))return;const rs=resultRows(),n=rs.length,pw=Math.min(W*.80,1060),ph=Math.min(H*.68,485),px=(W-pw)/2,py=(H-ph)/2-10,pad=30;const leftW=Math.min(245,pw*.27),tableX=px+pad,tableW=pw-pad*2,metricW=(tableW-leftW)/metrics.length;const titleY=py+43,subY=py+67,headerY=py+105,rowStart=py+122,rowGap=6,footerSpace=30;const rowH=Math.max(27,Math.min(43,(py+ph-footerSpace-rowStart-(n-1)*rowGap)/Math.max(1,n)));const rankBy={};for(const m of metrics)rankBy[m.key]=ranks(rs,m);
    ctx.save();ctx.fillStyle='rgba(7,12,15,.94)';ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(11,18,21,.988)';rr(px,py,pw,ph,21);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.16)';ctx.lineWidth=1.3;rr(px,py,pw,ph,21);ctx.stroke();ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle='#f7fbff';ctx.font='1000 30px system-ui';ctx.fillText(S.runComplete?'STAGE 10 CLEAR':`GAME OVER · STAGE ${S.stage}`,px+pad,titleY);ctx.fillStyle='rgba(255,255,255,.58)';ctx.font='760 11px system-ui';ctx.fillText(`TEAM CONTRIBUTION  ·  WALL ${S.baseHp}/${S.baseHpMax}  ·  KILL COIN`,px+pad,subY);ctx.fillStyle='rgba(255,255,255,.44)';ctx.font='850 10px system-ui';ctx.fillText('PLAYER / CLASS',tableX+10,headerY);ctx.textAlign='center';metrics.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),headerY));ctx.strokeStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.moveTo(tableX,headerY+10);ctx.lineTo(tableX+tableW,headerY+10);ctx.stroke();
    rs.forEach((r,ri)=>{const y=rowStart+ri*(rowH+rowGap),rgb=classColor(r.cls);ctx.fillStyle=ri%2===0?'rgba(255,255,255,.043)':'rgba(255,255,255,.024)';rr(tableX,y,tableW,rowH,9);ctx.fill();ctx.fillStyle=`rgba(${rgb},.96)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH*.5,5.2,0,Math.PI*2);ctx.fill();const nameFont='950 11px system-ui',nameX=tableX+28,classW=55,classX=tableX+leftW-classW-8,maxNameW=Math.max(45,classX-nameX-8);ctx.textAlign='left';ctx.textBaseline='middle';ctx.font=nameFont;ctx.fillStyle='#f3f8fb';ctx.fillText(fitText(`${ri+1}. ${r.label}`,maxNameW,nameFont),nameX,y+rowH*.5);ctx.fillStyle=`rgba(${rgb},.16)`;rr(classX,y+rowH*.5-9,classW,18,8);ctx.fill();ctx.strokeStyle=`rgba(${rgb},.38)`;ctx.lineWidth=1;rr(classX,y+rowH*.5-9,classW,18,8);ctx.stroke();ctx.textAlign='center';ctx.font='900 7.5px system-ui';ctx.fillStyle=`rgba(${rgb},.96)`;ctx.fillText(className(r.cls),classX+classW/2,y+rowH*.5+.3);metrics.forEach((m,mi)=>{const rank=rankBy[m.key][r.slot],cx=tableX+leftW+metricW*(mi+.5),col=rankColor[rank]||rankColor[4];ctx.fillStyle=col;ctx.beginPath();ctx.arc(cx-metricW*.23,y+rowH*.5,7.2,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(8,12,15,.95)';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),cx-metricW*.23,y+rowH*.5+.3);ctx.fillStyle=rank===1?'#ffe49a':rank===2?'#eef4f8':rank===3?'#e1ad85':'rgba(221,231,240,.75)';ctx.font=`${rank===1?1000:880} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]||0),cx+metricW*.06,y+rowH*.5)})});ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='720 9px system-ui';ctx.fillStyle='rgba(255,255,255,.42)';ctx.fillText('항목별 순위 · 1위 금색 강조',px+pw*.5,py+ph-12);ctx.restore()
  }
  const priorDraw=draw;draw=function(now){priorDraw(now);drawResultV027()};
})();
