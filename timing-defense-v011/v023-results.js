// Timing Defense v0.23 — spacious centered team result board.
(function(){
  function fresh(){return{kills:0,damage:0,coin:0,perfects:0,combo:0,maxCombo:0}}
  function rows(){
    const localName=(S.v022Nickname||'YOU').trim()||'YOU';
    const out=[{slot:0,label:localName,cls:S.playerClass,kills:S.v019Stats?.[0]?.kills||0,damage:S.v019Stats?.[0]?.damage||0,coin:S.v019Stats?.[0]?.coin||0,level:S.level||1,levelScore:(S.level||1)*100000+(S.xp||0),maxCombo:S.v018ComboPeak||0,perfects:S.stats?.perfect||0}];
    for(const ai of S.ai){const st=S.v019Stats?.[ai.slot]||fresh();out.push({slot:ai.slot,label:`CPU ${ai.slot}`,cls:ai.cls,kills:st.kills||0,damage:st.damage||0,coin:st.coin||0,level:ai.level||1,levelScore:(ai.level||1)*100000+(ai.xp||0),maxCombo:st.maxCombo||0,perfects:st.perfects||0})}
    return out.sort((a,b)=>a.slot-b.slot)
  }
  const metrics=[{key:'kills',label:'KILLS',fmt:v=>String(v),tie:r=>r.damage},{key:'damage',label:'DMG',fmt:v=>v>=10000?`${(v/1000).toFixed(1)}K`:String(Math.round(v)),tie:r=>r.kills},{key:'coin',label:'COIN',fmt:v=>String(v),tie:r=>r.kills},{key:'level',score:'levelScore',label:'LV',fmt:v=>String(v),tie:r=>r.perfects},{key:'maxCombo',label:'MAX COMBO',fmt:v=>String(v),tie:r=>r.perfects}];
  function ranks(rs,m){const k=m.score||m.key,sorted=[...rs].sort((a,b)=>((b[k]||0)-(a[k]||0))||((m.tie?m.tie(b):0)-(m.tie?m.tie(a):0))||(a.slot-b.slot));const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map}
  const rankColor={1:'#ffd65a',2:'#d9e2ea',3:'#c98b5d',4:'#7f93a6'};
  function board(){
    if(S.v022LobbyOpen||!(S.gameOver||S.runComplete))return;
    const rs=rows(),n=rs.length,pw=Math.min(W*.80,1060),ph=Math.min(H*.76,535),px=(W-pw)/2,py=(H-ph)/2-4,pad=30;
    const leftW=Math.min(230,pw*.25),tableX=px+pad,tableW=pw-pad*2,metricW=(tableW-leftW)/metrics.length;
    const titleY=py+45,subY=py+70,headerY=py+108,rowStart=py+127,rowGap=7;
    const footerSpace=34,rowH=Math.min(50,(py+ph-footerSpace-rowStart-(n-1)*rowGap)/Math.max(1,n));
    const rankBy={};for(const m of metrics)rankBy[m.key]=ranks(rs,m);
    ctx.save();ctx.fillStyle='rgba(7,12,15,.92)';ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(11,18,21,.985)';rr(px,py,pw,ph,21);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.16)';ctx.lineWidth=1.3;rr(px,py,pw,ph,21);ctx.stroke();
    ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle='#f7fbff';ctx.font='1000 30px system-ui';ctx.fillText(S.runComplete?'STAGE 10 CLEAR':`GAME OVER · STAGE ${S.stage}`,px+pad,titleY);ctx.fillStyle='rgba(255,255,255,.58)';ctx.font='760 11px system-ui';ctx.fillText(`TEAM CONTRIBUTION  ·  WALL ${S.baseHp}/${S.baseHpMax}  ·  KILL COIN`,px+pad,subY);
    ctx.fillStyle='rgba(255,255,255,.44)';ctx.font='850 10px system-ui';ctx.fillText('PLAYER / CLASS',tableX+10,headerY);ctx.textAlign='center';metrics.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),headerY));ctx.strokeStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.moveTo(tableX,headerY+11);ctx.lineTo(tableX+tableW,headerY+11);ctx.stroke();
    rs.forEach((r,ri)=>{const y=rowStart+ri*(rowH+rowGap),rgb=classColor(r.cls);ctx.fillStyle=ri%2===0?'rgba(255,255,255,.043)':'rgba(255,255,255,.024)';rr(tableX,y,tableW,rowH,10);ctx.fill();ctx.fillStyle=`rgba(${rgb},.96)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH*.50,5.4,0,Math.PI*2);ctx.fill();ctx.textAlign='left';ctx.fillStyle='#f3f8fb';ctx.font='950 11px system-ui';ctx.fillText(`${ri+1}. ${r.label}`,tableX+28,y+rowH*.42);ctx.fillStyle=`rgba(${rgb},.88)`;ctx.font='850 8px system-ui';ctx.fillText(className(r.cls),tableX+28,y+rowH*.70);
      metrics.forEach((m,mi)=>{const rank=rankBy[m.key][r.slot],cx=tableX+leftW+metricW*(mi+.5),col=rankColor[rank]||rankColor[4];ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=col;ctx.beginPath();ctx.arc(cx-metricW*.23,y+rowH*.50,7.4,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(8,12,15,.95)';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),cx-metricW*.23,y+rowH*.50+.3);ctx.fillStyle=rank===1?'#ffe49a':rank===2?'#eef4f8':rank===3?'#e1ad85':'rgba(221,231,240,.75)';ctx.font=`${rank===1?1000:880} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]||0),cx+metricW*.06,y+rowH*.50);if(rank===1){ctx.strokeStyle='rgba(255,214,90,.48)';ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(cx-metricW*.04,y+rowH*.73);ctx.lineTo(cx+metricW*.27,y+rowH*.73);ctx.stroke()}})
    });
    ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='720 9px system-ui';ctx.fillStyle='rgba(255,255,255,.42)';ctx.fillText('항목별 순위 · 1위 금색 강조',px+pw*.5,py+ph-14);ctx.restore()
  }
  const baseDraw=draw;draw=function(now){baseDraw(now);board()}
})();
