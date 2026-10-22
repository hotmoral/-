// Timing Defense v0.41 — network FLYER presentation follows authoritative server Y phase.
// Server owns gameplay Y. Client only extrapolates the same deterministic phase between snapshots.
(function(){
  const mp=window.__TDMP34CF;if(!mp||typeof MONSTER_TYPES==='undefined'||!MONSTER_TYPES.flyer)return;
  const flyerMeta={...MONSTER_TYPES.flyer};
  if(!MONSTER_TYPES.flyer_net)MONSTER_TYPES.flyer_net={...flyerMeta};

  function yNormalized(meta,serverAt){
    const base=Number(meta?.baseY)||0,epoch=Number(meta?.yEpochAt)||0,amp=Number(meta?.yAmp)||0,omega=Number(meta?.yOmega)||0;
    return base+Math.sin(Math.max(0,Number(serverAt||0)-epoch)/1000*omega)*amp;
  }
  function attachState(st){
    const run=st?.run;if(!run)return;
    const perfAt=performance.now(),serverTime=Number(run.serverTime??st.serverTime??Date.now());
    for(const sm of run.monsters||[]){
      if(sm.type!=='flyer')continue;
      const m=mp.monsterById?.get?.(sm.id);if(!m)continue;
      m.v041Flyer={
        baseY:Number(sm.baseY??sm.y),yEpochAt:Number(sm.yEpochAt??serverTime),
        yAmp:Number(sm.yAmp??.020),yOmega:Number(sm.yOmega??5),serverTime,perfAt
      };
      const y=yNormalized(m.v041Flyer,serverTime)*H;
      m.v034TargetY=y;m.baseY=y;
    }
  }

  window.addEventListener('tdcf:state',e=>queueMicrotask(()=>attachState(e.detail?.state)));
  attachState(mp.state);

  const priorUpdate=update;
  update=function(now,dt){
    if(!mp.active)return priorUpdate(now,dt);
    const swapped=[];
    for(const m of S.monsters||[]){
      if(m.type!=='flyer')continue;
      const f=m.v041Flyer;
      if(f){
        const serverAt=f.serverTime+(now-f.perfAt),y=yNormalized(f,serverAt)*H;
        m.v034TargetY=y;m.baseY=y;
      }
      // baseUpdate contains legacy local FLYER oscillation. Use an equivalent render/meta
      // alias so v0.34 still extrapolates X but the old independent Y oscillator does not run.
      m.type='flyer_net';swapped.push(m);
    }
    try{return priorUpdate(now,dt)}finally{for(const m of swapped)m.type='flyer'}
  };

  window.__TDFlyerYV041={yNormalized,attachState,netType:'flyer_net'};
})();
