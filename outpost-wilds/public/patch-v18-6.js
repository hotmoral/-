/* Outpost Wilds V18.6: authored atlas integration with SVG fallback and aspect-safe rendering. */
(function(){
  const V186_ATLAS='/assets/v186/atlas.webp?v=186';
  const V186_RECTS={"player":{"x":13,"y":8,"w":102,"h":112},"tree":{"x":143,"y":8,"w":97,"h":112},"rock":{"x":264,"y":10,"w":112,"h":107},"ore":{"x":393,"y":8,"w":109,"h":112},"berry":{"x":523,"y":8,"w":105,"h":112},"wolf":{"x":648,"y":10,"w":112,"h":108},"boar":{"x":776,"y":8,"w":111,"h":112},"brute":{"x":904,"y":14,"w":112,"h":99},"direwolf":{"x":1032,"y":14,"w":112,"h":99},"tusker":{"x":8,"y":138,"w":112,"h":107},"mauler":{"x":136,"y":136,"w":112,"h":112},"siegebeast":{"x":264,"y":136,"w":112,"h":111},"alpha":{"x":392,"y":138,"w":112,"h":107},"broodmother":{"x":520,"y":136,"w":112,"h":111},"colossus":{"x":648,"y":137,"w":112,"h":110},"overlord":{"x":776,"y":136,"w":112,"h":111},"base1":{"x":904,"y":136,"w":111,"h":112},"base2":{"x":1032,"y":143,"w":112,"h":97},"base3":{"x":8,"y":266,"w":112,"h":107},"base4":{"x":136,"y":264,"w":112,"h":111},"base5":{"x":264,"y":265,"w":112,"h":109},"base6":{"x":392,"y":264,"w":111,"h":112},"stockpile":{"x":520,"y":268,"w":112,"h":103},"signal":{"x":657,"y":264,"w":93,"h":112},"workshop1":{"x":778,"y":264,"w":108,"h":112},"workshop2":{"x":904,"y":268,"w":112,"h":104},"workshop3":{"x":1032,"y":268,"w":112,"h":103},"storage1":{"x":8,"y":392,"w":112,"h":111},"storage2":{"x":136,"y":394,"w":112,"h":107},"storage3":{"x":264,"y":393,"w":112,"h":110},"farm1":{"x":392,"y":394,"w":112,"h":108},"farm2":{"x":520,"y":393,"w":112,"h":109},"farm3":{"x":648,"y":393,"w":112,"h":110},"watchtower1":{"x":789,"y":392,"w":85,"h":112},"watchtower2":{"x":910,"y":392,"w":100,"h":112},"watchtower3":{"x":1048,"y":392,"w":79,"h":112},"forge1":{"x":8,"y":522,"w":112,"h":108},"forge2":{"x":138,"y":520,"w":108,"h":112},"forge3":{"x":264,"y":520,"w":112,"h":111},"infirmary1":{"x":392,"y":520,"w":112,"h":111},"infirmary2":{"x":520,"y":521,"w":112,"h":110},"infirmary3":{"x":648,"y":521,"w":112,"h":110},"turret1":{"x":776,"y":521,"w":112,"h":110},"turret2":{"x":904,"y":522,"w":112,"h":108},"turret3":{"x":1032,"y":520,"w":112,"h":111},"turret21":{"x":8,"y":653,"w":112,"h":102},"turret22":{"x":136,"y":648,"w":112,"h":112},"turret23":{"x":267,"y":648,"w":105,"h":112},"wall1":{"x":392,"y":653,"w":112,"h":102},"wall2":{"x":520,"y":657,"w":112,"h":93},"wall3":{"x":648,"y":653,"w":112,"h":102},"weapon1":{"x":776,"y":652,"w":112,"h":103},"weapon2":{"x":909,"y":648,"w":102,"h":112},"weapon3":{"x":1034,"y":648,"w":108,"h":112},"weapon4":{"x":8,"y":778,"w":112,"h":107},"weapon5":{"x":139,"y":776,"w":105,"h":112},"weapon6":{"x":265,"y":776,"w":110,"h":112},"weapon7":{"x":393,"y":776,"w":110,"h":112},"weapon8":{"x":523,"y":776,"w":105,"h":112},"weapon9":{"x":649,"y":776,"w":109,"h":112},"weapon10":{"x":778,"y":776,"w":108,"h":112},"weapon11":{"x":908,"y":776,"w":104,"h":112},"weapon12":{"x":1040,"y":776,"w":96,"h":112},"weapon13":{"x":8,"y":904,"w":111,"h":112},"weapon14":{"x":136,"y":908,"w":112,"h":103},"weapon15":{"x":264,"y":907,"w":112,"h":106},"weapon16":{"x":392,"y":905,"w":112,"h":109}};
  const atlas=new Image();atlas.decoding='async';atlas.src=V186_ATLAS;
  let atlasReady=false;atlas.onload=()=>{atlasReady=true;};atlas.onerror=()=>{atlasReady=false;};
  const fallbackImg=v18Img;

  function drawAtlas(key,x,y,w,h,flip=false,rot=0,alpha=1){
    const r=V186_RECTS[key];if(!r||!atlasReady||!atlas.naturalWidth)return false;
    const scale=Math.min(w/r.w,h/r.h),dw=r.w*scale,dh=r.h*scale;
    ctx.save();ctx.globalAlpha=alpha;ctx.translate(x,y);ctx.rotate(rot);ctx.scale(flip?-1:1,1);
    ctx.drawImage(atlas,r.x,r.y,r.w,r.h,-dw/2,-dh/2,dw,dh);ctx.restore();return true;
  }
  v18Img=function(key,x,y,w,h,flip=false,rot=0,alpha=1){
    return drawAtlas(key,x,y,w,h,flip,rot,alpha)||fallbackImg(key,x,y,w,h,flip,rot,alpha);
  };

  /* Authored weapon art already carries its silhouette/orientation, so do not stretch it into old narrow boxes. */
  drawWeapon=function(p,swing=0){
    const idx=Math.max(1,Math.min(16,p.weaponIndex||p.gearLevel||1)),kind=p.weaponKind||V18_WEAPON_KIND[idx],key=`weapon${idx}`;
    ctx.save();
    if(kind==='ranged'){ctx.translate(8,-3);ctx.rotate(-.08+swing*.12);v18Img(key,18,0,60,60,false,0,1);}
    else{ctx.translate(8,-4);ctx.rotate(-.12+swing*.72);v18Img(key,20,0,58,58,false,0,1);}
    ctx.restore();
  };

  /* Square-ish authored buildings should keep their native proportions instead of being horizontally squashed. */
  v18FacilityAsset=function(fid,lv){
    const pos=V14_POS[fid];if(!pos||!lv)return;const s=worldToScreen(pos.x,pos.y);
    const sizes={workshop:[88,88],storage:[88,88],farm:[98,94],watchtower:[80,110],forge:[88,86],infirmary:[90,90],turret:[84,84],turret2:[90,86]},sz=sizes[fid]||[88,88];
    shadow(s.x,s.y+28,sz[0]*.31,8,.25);if(!v18Img(`${fid}${lv}`,s.x,s.y-8,sz[0],sz[1]))v17DrawImage(fid,s.x,s.y-8,sz[0],sz[1]);
  };
  v17FacilityAsset=v18FacilityAsset;
  v6DrawBuiltFacilities=function(){const f=snap?.facilities||{};v17DrawFortification();for(const fid of['workshop','storage','farm','watchtower','forge','infirmary','turret','turret2'])if(f[fid])v18FacilityAsset(fid,f[fid]);};

  const previousBase=drawBase;
  drawBase=function(b){
    const s=worldToScreen(b.x,b.y);shadow(s.x,s.y+34,56,13,.31);
    if(!v18Img(`base${Math.max(1,Math.min(6,b.level||1))}`,s.x,s.y-8,114,114))return previousBase(b);
    v6DrawBuiltFacilities();v13DrawStockpile();
    const sp=(typeof v12SignalPad==='function')?v12SignalPad():null;
    if(sp&&snap?.endgame?.signalBuilt){
      const q=worldToScreen(sp.x,sp.y);shadow(q.x,q.y+25,32,9,.26);
      if(v18Img('signal',q.x,q.y-22,72,92)){ctx.save();ctx.font='800 8px system-ui,sans-serif';ctx.textAlign='center';ctx.fillStyle='#dcebd2';ctx.fillText(sp.label||'신호탑',q.x,q.y+38);ctx.restore();}
    }
  };

  v13DrawStockpile=function(){
    const st=v13Stock();if(!st)return;const s=worldToScreen(st.x,st.y),q=Math.min(1,(st.total||0)/Math.max(1,st.capacity||1));
    shadow(s.x,s.y+21,32,9,.25);v18Img('stockpile',s.x,s.y-4,78,72);
    ctx.save();ctx.fillStyle='rgba(5,10,8,.86)';v4Rounded(s.x-31,s.y+31,62,13,7);ctx.fill();ctx.fillStyle='#253329';ctx.fillRect(s.x-25,s.y+36,50,3);ctx.fillStyle='#a7cb82';ctx.fillRect(s.x-25,s.y+36,50*q,3);ctx.font='800 7px system-ui,sans-serif';ctx.textAlign='center';ctx.fillStyle='#eee3ca';ctx.fillText(`${st.total||0}/${st.capacity||0}`,s.x,s.y+30);ctx.restore();
  };

  window.__OW_V186__={authoredAtlas:true,assetCount:Object.keys(V186_RECTS).length,atlas:V186_ATLAS,svgFallback:true,aspectSafe:true};
})();
