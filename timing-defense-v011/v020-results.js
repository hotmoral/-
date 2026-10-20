// Timing Defense v0.20 — cleaner end-run contribution board.
(function(){
  function fresh(){return{kills:0,damage:0,coin:0,perfects:0,combo:0,maxCombo:0}}
  function rows(){
    const out=[{slot:0,label:'YOU',cls:S.playerClass,kills:S.v019Stats?.[0]?.kills||0,damage:S.v019Stats?.[0]?.damage||0,coin:S.v019Stats?.[0]?.coin||0,level:S.level||1,levelScore:(S.level||1)*100000+(S.xp||0),maxCombo:S.v018ComboPeak||0,perfects:S.stats?.perfect||0}];
    for(const ai of S.ai){
      const st=S.v019Stats?.[ai.slot]||fresh();
      out.push({slot:ai.slot,label:`CPU ${ai.slot}`,cls:ai.cls,kills:st.kills||0,damage:st.damage||0,coin:st.coin||0,level:ai.level||1,levelScore:(ai.level||1)*100000+(ai.xp||0),maxCombo:st.maxCombo||0,perfects:st.perfects||0})
    }
    return out.sort((a,b)=>a.slot-b.slot)
  }
  const metrics=[
    {key:'kills',label:'KILLS',fmt:v=>String(v),tie:r=>r.damage},
    {key:'damage',label:'DMG',fmt:v=>v>=10000?`${(v/1000).toFixed(1)}K`:String(Math.round(v)),tie:r=>r.kills},
    {key:'coin',label:'COIN',fmt:v=>String(v),tie:r=>r.kills},
    {key:'level',score:'levelScore',label:'LV',fmt:v=>String(v),tie:r=>r.perfects},
    {key:'maxCombo',label:'MAX COMBO',fmt:v=>String(v),tie:r=>r.perfects}
  ];
  function ranks(rs,m){
    const k=m.score||m.key,sorted=[...rs].sort((a,b)=>((b[k]||0)-(a[k]||0))||((m.tie?m.tie(b):0)-(m.tie?m.tie(a):0))||(a.slot-b.slot));
    const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map
  }
  const rankColor={1:'#ffd65a',2:'#d9e2ea',3:'#c98b5d',4:'#7f93a6'};

  function drawBoard(){
    if(!(S.gameOver||S.runComplete))return;
    const rs=rows(),n=rs.length;
    const px=W*.185,py=H*.175,pw=W*.76,ph=H*.68;
    const pad=28,leftW=Math.min(205,pw*.245),tableX=px+pad,tableW=pw-pad*2;
    const metricW=(tableW-leftW)/metrics.length;
    const headerY=py+96,rowStart=py+119;
    const rowGap=6,rowH=Math.min(48,(ph-154-(n-1)*rowGap)/Math.max(1,n));
    const rankBy={};for(const m of metrics)rankBy[m.key]=ranks(rs,m);

    ctx.save();
    // Completely cover the v0.19 board underneath.
    ctx.fillStyle='rgba(3,6,10,.94)';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(8,13,20,.97)';rr(px,py,pw,ph,20);ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.14)';ctx.lineWidth=1.3;rr(px,py,pw,ph,20);ctx.stroke();

    ctx.textAlign='left';ctx.textBaseline='alphabetic';
    ctx.fillStyle='#f7fbff';ctx.font='1000 30px system-ui';ctx.fillText(S.runComplete?'STAGE 10 CLEAR':`GAME OVER · STAGE ${S.stage}`,px+pad,py+43);
    ctx.fillStyle='rgba(255,255,255,.54)';ctx.font='760 11px system-ui';ctx.fillText(`TEAM CONTRIBUTION  ·  WALL ${S.baseHp}/${S.baseHpMax}  ·  KILL COIN`,px+pad,py+66);

    ctx.fillStyle='rgba(255,255,255,.40)';ctx.font='850 10px system-ui';ctx.fillText('PLAYER / CLASS',tableX+8,headerY);
    ctx.textAlign='center';metrics.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),headerY));
    ctx.strokeStyle='rgba(255,255,255,.08)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(tableX,headerY+10);ctx.lineTo(tableX+tableW,headerY+10);ctx.stroke();

    rs.forEach((r,ri)=>{
      const y=rowStart+ri*(rowH+rowGap),rgb=classColor(r.cls);
      ctx.fillStyle=ri%2===0?'rgba(255,255,255,.035)':'rgba(255,255,255,.020)';rr(tableX,y,tableW,rowH,9);ctx.fill();
      ctx.fillStyle=`rgba(${rgb},.95)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH*.5,5,0,Math.PI*2);ctx.fill();
      ctx.textAlign='left';ctx.fillStyle='#f4f8fc';ctx.font='950 12px system-ui';ctx.fillText(`${ri+1}. ${r.label}`,tableX+26,y+rowH*.43);
      ctx.fillStyle=`rgba(${rgb},.84)`;ctx.font='820 9px system-ui';ctx.fillText(className(r.cls),tableX+26,y+rowH*.72);

      metrics.forEach((m,mi)=>{
        const rank=rankBy[m.key][r.slot],cx=tableX+leftW+metricW*(mi+.5),col=rankColor[rank]||rankColor[4];
        ctx.textAlign='center';ctx.textBaseline='middle';
        // Small rank medallion aligned consistently to the left of the value, without a box around every cell.
        ctx.fillStyle=col;ctx.beginPath();ctx.arc(cx-metricW*.24,y+rowH*.50,7.5,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='rgba(8,11,16,.94)';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),cx-metricW*.24,y+rowH*.50+.3);
        ctx.fillStyle=rank===1?'#ffe49a':rank===2?'#eef4f8':rank===3?'#e1ad85':'rgba(221,231,240,.72)';
        ctx.font=`${rank===1?1000:880} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]||0),cx+metricW*.06,y+rowH*.50+.2);
        if(rank===1){ctx.strokeStyle='rgba(255,214,90,.50)';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(cx-metricW*.02,y+rowH*.72);ctx.lineTo(cx+metricW*.28,y+rowH*.72);ctx.stroke()}
      })
    });

    ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='720 10px system-ui';ctx.fillStyle='rgba(255,255,255,.40)';
    ctx.fillText('항목별 순위  ·  1위 금색 강조  ·  RESET으로 새 런 시작',px+pw*.5,py+ph-18);
    ctx.restore()
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawBoard()};
})();
