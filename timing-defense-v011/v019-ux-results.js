// Timing Defense v0.19 — visible-target integrity, wider party, and end-run contribution board.
(function(){
  const V019_SLOT_Y=[.255,.405,.555,.705];
  charBase=function(slot){return{x:W*.105,y:H*(V019_SLOT_Y[slot]??V019_SLOT_Y[0]),scale:.41}};

  // Only enemies whose aim point has actually entered the viewport may be damaged/targeted.
  function v019VisibleTarget(m){
    if(!m||m.dead)return false;
    const a=monsterAimPoint(m);
    return a.x<=W-10;
  }
  nearestMonster=function(){
    let best=null;
    for(const m of S.monsters){
      if(!v019VisibleTarget(m))continue;
      if(!best||m.x<best.x)best=m;
    }
    return best;
  };

  function freshSlot(){return{kills:0,damage:0,coin:0,perfects:0,combo:0,maxCombo:0}}
  function initContribution(){
    S.v019Stats=[freshSlot(),freshSlot(),freshSlot(),freshSlot()];
  }
  initContribution();

  function actorSlot(p,local){
    if(p&&Number.isInteger(p.slot))return clamp(p.slot,0,3);
    return local?0:null;
  }

  // Reject any damage to not-yet-visible enemies, including AoE/pierce spill.
  const baseVisualImpact=visualImpact;
  visualImpact=function(p,m,now,local){
    if(!v019VisibleTarget(m))return false;
    const slot=actorSlot(p,local),before=m&&!m.dead?Math.max(0,m.hp):0,wasAlive=!!m&&!m.dead;
    const ok=baseVisualImpact(p,m,now,local);
    if(ok&&slot!==null&&wasAlive){
      const s=S.v019Stats?.[slot];
      if(s){
        const after=Math.max(0,m.hp);
        s.damage+=Math.max(0,Math.min(before,before-after));
        if(m.dead){
          s.kills++;
          s.coin+=(MONSTER_TYPES[m.type]?.reward||0);
        }
      }
    }
    return ok
  };

  // Capture the current v0.17 AI timing rolls to build PERFECT/max-streak statistics
  // without drawing extra AI Timing Squares.
  function aiJudgeFromRoll(r){return r<.28?'NORMAL':r<.82?'GOOD':'PERFECT'}
  function recordAiJudge(slot,judge){
    const s=S.v019Stats?.[slot];if(!s)return;
    if(judge==='PERFECT'){
      s.perfects++;s.combo++;s.maxCombo=Math.max(s.maxCombo,s.combo);
    }else s.combo=0;
  }
  const baseAiAttack=aiAttack;
  aiAttack=function(ai,now){
    const heavy=(ai.charge||0)>=3,rolls=[],realRandom=Math.random;
    Math.random=function(){const v=realRandom();rolls.push(v);return v};
    try{baseAiAttack(ai,now)}finally{Math.random=realRandom}
    if(heavy){
      recordAiJudge(ai.slot,aiJudgeFromRoll(rolls[0]??0));
      recordAiJudge(ai.slot,aiJudgeFromRoll(rolls[1]??0));
    }else{
      recordAiJudge(ai.slot,aiJudgeFromRoll(rolls[0]??0));
    }
  };

  // v0.19 owns combo presentation; remove old milestone combo floats.
  const baseAddFloat=addFloat;
  addFloat=function(text,x,y,size=25,kind='damage'){
    if(typeof text==='string'&&text.includes('COMBO'))return;
    return baseAddFloat(text,x,y,size,kind)
  };

  const baseReset=reset;
  reset=function(){baseReset();initContribution()};

  function teamRows(){
    const rows=[];
    rows.push({
      slot:0,label:'YOU',cls:S.playerClass,
      kills:S.v019Stats?.[0]?.kills||0,
      damage:S.v019Stats?.[0]?.damage||0,
      coin:S.v019Stats?.[0]?.coin||0,
      level:S.level||1,
      levelScore:(S.level||1)*100000+(S.xp||0),
      maxCombo:S.v018ComboPeak||0,
      perfects:S.stats?.perfect||0
    });
    for(const ai of S.ai){
      const st=S.v019Stats?.[ai.slot]||freshSlot();
      rows.push({
        slot:ai.slot,label:`CPU ${ai.slot}`,cls:ai.cls,
        kills:st.kills,damage:st.damage,coin:st.coin,
        level:ai.level||1,levelScore:(ai.level||1)*100000+(ai.xp||0),
        maxCombo:st.maxCombo,perfects:st.perfects
      });
    }
    return rows.sort((a,b)=>a.slot-b.slot);
  }

  const METRICS=[
    {key:'kills',label:'KILLS',fmt:v=>String(v),tie:r=>r.damage},
    {key:'damage',label:'DMG',fmt:v=>v>=10000?`${(v/1000).toFixed(1)}K`:String(Math.round(v)),tie:r=>r.kills},
    {key:'coin',label:'COIN',fmt:v=>String(v),tie:r=>r.kills},
    {key:'level',score:'levelScore',label:'LV',fmt:v=>String(v),tie:r=>r.perfects},
    {key:'maxCombo',label:'MAX COMBO',fmt:v=>String(v),tie:r=>r.perfects}
  ];
  function rankMap(rows,metric){
    const scoreKey=metric.score||metric.key;
    const sorted=[...rows].sort((a,b)=>{
      const d=(b[scoreKey]||0)-(a[scoreKey]||0);
      if(d)return d;
      const t=(metric.tie?metric.tie(b):0)-(metric.tie?metric.tie(a):0);
      if(t)return t;
      return a.slot-b.slot;
    });
    const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map
  }
  const RANK_STYLE={
    1:{fill:'rgba(255,205,86,.16)',stroke:'rgba(255,220,112,.88)',text:'#ffe49a',badge:'#ffd65a'},
    2:{fill:'rgba(213,224,235,.10)',stroke:'rgba(221,232,242,.52)',text:'#e9f0f6',badge:'#d9e2ea'},
    3:{fill:'rgba(199,134,82,.10)',stroke:'rgba(211,148,96,.44)',text:'#e3ad83',badge:'#c98b5d'},
    4:{fill:'rgba(113,134,154,.065)',stroke:'rgba(151,171,190,.22)',text:'rgba(220,230,240,.66)',badge:'#7f93a6'}
  };

  function drawResultBoard(){
    if(!(S.gameOver||S.runComplete))return;
    const rows=teamRows(),n=rows.length;
    const px=W*.205,py=H*.155,pw=W*.735,ph=H*.675;
    ctx.save();
    ctx.fillStyle='rgba(3,6,10,.90)';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(8,13,20,.96)';rr(px,py,pw,ph,18);ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.13)';ctx.lineWidth=1.4;rr(px,py,pw,ph,18);ctx.stroke();

    ctx.textAlign='left';ctx.fillStyle='#f7fbff';ctx.font='1000 28px system-ui';
    ctx.fillText(S.runComplete?'STAGE 10 CLEAR':`GAME OVER · STAGE ${S.stage}`,px+24,py+38);
    ctx.font='750 11px system-ui';ctx.fillStyle='rgba(255,255,255,.55)';
    ctx.fillText(`TEAM CONTRIBUTION · WALL ${S.baseHp}/${S.baseHpMax} · KILL COIN 기준`,px+25,py+59);

    const leftW=Math.min(190,pw*.22),tableX=px+18,tableY=py+82,tableW=pw-36;
    const metricW=(tableW-leftW)/METRICS.length;
    ctx.font='850 10px system-ui';ctx.fillStyle='rgba(255,255,255,.48)';
    ctx.fillText('PLAYER / CLASS',tableX+9,tableY);
    ctx.textAlign='center';
    METRICS.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),tableY));
    const rowGap=6,rowH=Math.min(58,(ph-126-(n-1)*rowGap)/Math.max(1,n));
    const ranks={};for(const m of METRICS)ranks[m.key]=rankMap(rows,m);

    rows.forEach((r,ri)=>{
      const y=tableY+14+ri*(rowH+rowGap);
      const rgb=classColor(r.cls);
      ctx.fillStyle='rgba(255,255,255,.035)';rr(tableX,y,tableW,rowH,10);ctx.fill();

      ctx.textAlign='left';
      ctx.fillStyle=`rgba(${rgb},.95)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH/2,4.5,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#f5f8fb';ctx.font='950 12px system-ui';ctx.fillText(`${ri+1}  ${r.label}`,tableX+23,y+rowH*.42);
      ctx.fillStyle=`rgba(${rgb},.82)`;ctx.font='800 9px system-ui';ctx.fillText(className(r.cls),tableX+23,y+rowH*.70);

      METRICS.forEach((m,mi)=>{
        const rank=ranks[m.key][r.slot],st=RANK_STYLE[rank]||RANK_STYLE[4];
        const x=tableX+leftW+metricW*mi+4,w=metricW-8;
        ctx.save();
        if(rank===1){ctx.shadowBlur=10;ctx.shadowColor='rgba(255,211,90,.22)'}
        ctx.fillStyle=st.fill;rr(x,y+5,w,rowH-10,8);ctx.fill();
        ctx.shadowBlur=0;ctx.strokeStyle=st.stroke;ctx.lineWidth=rank===1?1.5:1;rr(x,y+5,w,rowH-10,8);ctx.stroke();
        ctx.fillStyle=st.badge;ctx.beginPath();ctx.arc(x+12,y+14,8,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='rgba(10,13,18,.92)';ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),x+12,y+14);
        ctx.fillStyle=st.text;ctx.font=`${rank===1?1000:850} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]||0),x+w*.56,y+rowH*.54);
        ctx.restore();
      });
    });

    ctx.textAlign='center';ctx.font='700 10px system-ui';ctx.fillStyle='rgba(255,255,255,.42)';
    ctx.fillText('각 항목 1위는 금색 강조 · RESET으로 새 런 시작',px+pw/2,py+ph-15);
    ctx.restore()
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawResultBoard()};

  if(window.__gameDebug){
    const baseState=window.__gameDebug.state;
    window.__gameDebug.state=()=>({...baseState(),v019Contribution:teamRows()});
  }
})();
