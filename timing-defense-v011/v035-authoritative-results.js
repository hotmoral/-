// Timing Defense Cloudflare v0.35 cf.4 — authoritative synchronized result board.
// Presentation only. Reads final contribution values from the Durable Object snapshot.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  let finalState=null;
  function capture(st){
    const run=st?.run;
    if(!run)return;
    if(run.status==='stage2-clear'||run.status==='gameover')finalState=st;
  }
  window.addEventListener('tdcf:state',e=>capture(e.detail?.state));
  capture(mp.state);

  const metrics=[
    {key:'kills',label:'KILLS',fmt:v=>String(Math.round(v||0)),tie:r=>r.damage||0},
    {key:'damage',label:'DMG',fmt:v=>(v||0)>=10000?`${((v||0)/1000).toFixed(1)}K`:String(Math.round(v||0)),tie:r=>r.kills||0},
    {key:'coin',label:'COIN',fmt:v=>String(Math.round(v||0)),tie:r=>r.kills||0},
    {key:'level',label:'LV',fmt:v=>String(Math.round(v||1)),tie:r=>r.xp||0},
    {key:'maxCombo',label:'MAX COMBO',fmt:v=>String(Math.round(v||0)),tie:r=>r.damage||0}
  ];
  const rankColor={1:'#ffd65a',2:'#d9e2ea',3:'#c98b5d',4:'#7f93a6'};

  function rows(st){
    const run=st?.run;if(!run)return[];
    const out=[];
    for(const p of [...(st.participants||[])].sort((a,b)=>a.slot-b.slot)){
      const rp=run.players?.find(x=>x.slot===p.slot)||{};
      out.push({slot:p.slot,label:p.nickname||`P${p.slot}`,cls:p.classId||'knight',kills:rp.kills||0,damage:rp.damage||0,coin:rp.coin||0,level:rp.level||1,xp:rp.xp||0,maxCombo:rp.comboPeak||0,human:true});
    }
    const aiBySlot=new Map((run.ai||[]).map(a=>[a.slot,a]));
    for(const a of [...(st.aiFill||[])].sort((x,y)=>x.pos-y.pos)){
      const ra=aiBySlot.get(a.pos)||{};
      out.push({slot:a.pos,label:`CPU ${a.pos}`,cls:a.cls||ra.cls||'knight',kills:ra.kills||0,damage:ra.damage||0,coin:ra.coin||0,level:ra.level||1,xp:0,maxCombo:ra.comboPeak||0,human:false});
    }
    return out.sort((a,b)=>a.slot-b.slot);
  }
  function ranks(rs,m){
    const sorted=[...rs].sort((a,b)=>((b[m.key]||0)-(a[m.key]||0))||((m.tie?m.tie(b):0)-(m.tie?m.tie(a):0))||(a.slot-b.slot));
    const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map;
  }

  function drawBoard(st){
    const run=st?.run;if(!run)return;
    const rs=rows(st),n=Math.max(1,rs.length);
    const pw=Math.min(W*.80,1060),ph=Math.min(H*.76,535),px=(W-pw)/2,py=(H-ph)/2-4,pad=30;
    const leftW=Math.min(230,pw*.25),tableX=px+pad,tableW=pw-pad*2,metricW=(tableW-leftW)/metrics.length;
    const titleY=py+45,subY=py+70,headerY=py+108,rowStart=py+127,rowGap=7,footerSpace=34;
    const rowH=Math.min(50,(py+ph-footerSpace-rowStart-(n-1)*rowGap)/n);
    const rankBy={};for(const m of metrics)rankBy[m.key]=ranks(rs,m);

    ctx.save();
    ctx.fillStyle='rgba(7,12,15,.94)';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(11,18,21,.988)';rr(px,py,pw,ph,21);ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.16)';ctx.lineWidth=1.3;rr(px,py,pw,ph,21);ctx.stroke();
    ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle='#f7fbff';ctx.font='1000 30px system-ui';
    ctx.fillText(run.status==='gameover'?`GAME OVER · STAGE ${run.stage||S.stage||1}`:`STAGE ${run.stage||2} CLEAR`,px+pad,titleY);
    ctx.fillStyle='rgba(255,255,255,.58)';ctx.font='760 11px system-ui';
    ctx.fillText(`TEAM CONTRIBUTION  ·  WALL ${run.baseHp}/${run.baseHpMax}  ·  SERVER SYNC`,px+pad,subY);
    ctx.fillStyle='rgba(255,255,255,.44)';ctx.font='850 10px system-ui';ctx.fillText('PLAYER / CLASS',tableX+10,headerY);
    ctx.textAlign='center';metrics.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),headerY));
    ctx.strokeStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.moveTo(tableX,headerY+11);ctx.lineTo(tableX+tableW,headerY+11);ctx.stroke();

    rs.forEach((r,ri)=>{
      const y=rowStart+ri*(rowH+rowGap),rgb=classColor(r.cls);
      ctx.fillStyle=ri%2===0?'rgba(255,255,255,.043)':'rgba(255,255,255,.024)';rr(tableX,y,tableW,rowH,10);ctx.fill();
      ctx.fillStyle=`rgba(${rgb},.96)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH*.50,5.4,0,Math.PI*2);ctx.fill();
      ctx.textAlign='left';ctx.fillStyle='#f3f8fb';ctx.font='950 11px system-ui';ctx.fillText(`${r.slot}. ${r.label}`,tableX+28,y+rowH*.42);
      ctx.fillStyle=`rgba(${rgb},.88)`;ctx.font='850 8px system-ui';ctx.fillText(className(r.cls),tableX+28,y+rowH*.70);
      metrics.forEach((m,mi)=>{
        const rank=rankBy[m.key][r.slot],cx=tableX+leftW+metricW*(mi+.5),col=rankColor[rank]||rankColor[4];
        ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=col;ctx.beginPath();ctx.arc(cx-metricW*.23,y+rowH*.50,7.4,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='rgba(8,12,15,.95)';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),cx-metricW*.23,y+rowH*.50+.3);
        ctx.fillStyle=rank===1?'#ffe49a':rank===2?'#eef4f8':rank===3?'#e1ad85':'rgba(221,231,240,.75)';ctx.font=`${rank===1?1000:880} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]),cx+metricW*.06,y+rowH*.50);
        if(rank===1){ctx.strokeStyle='rgba(255,214,90,.48)';ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(cx-metricW*.04,y+rowH*.73);ctx.lineTo(cx+metricW*.27,y+rowH*.73);ctx.stroke()}
      });
    });
    ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='720 9px system-ui';ctx.fillStyle='rgba(255,255,255,.42)';ctx.fillText('서버 확정 기여도 · 모든 클라이언트 동일',px+pw*.5,py+ph-14);
    ctx.restore();
  }

  const baseDraw=draw;
  draw=function(now){
    const st=finalState||mp.state,run=st?.run;
    const final=run&&(run.status==='stage2-clear'||run.status==='gameover');
    if(!final)return baseDraw(now);
    // Suppress inherited single/local result boards while preserving the rest of the scene and DOM buttons.
    const savedComplete=S.runComplete,savedGameOver=S.gameOver;
    S.runComplete=false;S.gameOver=false;
    baseDraw(now);
    S.runComplete=savedComplete;S.gameOver=savedGameOver;
    drawBoard(st);
  };
})();
