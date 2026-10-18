/* Outpost Wilds V15: visible chat feed, foreground build HUD, reliable ration control, image-asset visual pass. */

function v15LoadAsset(key,path){const im=new Image();im.src=path;assets[key]=im;return im;}
v15LoadAsset('tree','/assets/tree-v15.svg');
v15LoadAsset('rock','/assets/rock-v15.svg');
v15LoadAsset('ore','/assets/ore-v15.svg');
v15LoadAsset('wolf','/assets/wolf-v15.svg');
v15LoadAsset('boar','/assets/boar-v15.svg');
v15LoadAsset('brute','/assets/beast-v15.svg');
v15LoadAsset('alpha','/assets/beast-v15.svg');
v15LoadAsset('spearV15','/assets/spear-v15.svg');
v15LoadAsset('spear2V15','/assets/spear2-v15.svg');
v15LoadAsset('bowV15','/assets/bow-v15.svg');
v15LoadAsset('crossbowV15','/assets/crossbow-v15.svg');
v15LoadAsset('repeaterV15','/assets/repeater-v15.svg');

Object.assign(V10_ENEMY_STYLE,{
  wolf:{asset:'wolf',w:104,h:82,label:'늑대',filter:'none'},
  boar:{asset:'boar',w:108,h:78,label:'멧돼지',filter:'none'},
  brute:{asset:'brute',w:116,h:102,label:'야수',filter:'brightness(.92) saturate(.86)'},
  direwolf:{asset:'wolf',w:126,h:98,label:'광포 늑대',filter:'saturate(.72) brightness(.8) hue-rotate(155deg)'},
  tusker:{asset:'boar',w:132,h:96,label:'철갑 멧돼지',filter:'sepia(.25) saturate(.82) contrast(1.1)'},
  mauler:{asset:'brute',w:142,h:125,label:'파괴자',filter:'saturate(1.15) brightness(.78) hue-rotate(335deg)'},
  siegebeast:{asset:'brute',w:170,h:150,label:'공성 야수',filter:'grayscale(.2) contrast(1.2) brightness(.76)'},
  alpha:{asset:'alpha',w:174,h:152,label:'잿빛 포식자',filter:'brightness(.9)',boss:true},
  broodmother:{asset:'alpha',w:198,h:170,label:'가시등 어미',filter:'hue-rotate(255deg) saturate(1.1) brightness(.82)',boss:true},
  colossus:{asset:'brute',w:238,h:204,label:'황폐의 거수',filter:'sepia(.28) saturate(.78) contrast(1.28) brightness(.68)',boss:true},
  overlord:{asset:'brute',w:266,h:224,label:'황폐의 군주',filter:'sepia(.25) saturate(1.2) contrast(1.35) brightness(.65) hue-rotate(325deg)',boss:true}
});

function v15WeaponAsset(p){
  if((p.gearLevel||1)<=1)return assets.spearV15;
  if(p.gearLevel===2)return assets.spear2V15;
  if(p.gearLevel===3)return assets.bowV15;
  if(p.gearLevel===4)return assets.crossbowV15;
  return assets.repeaterV15;
}
drawWeapon=function(p,sw=0){
  const im=v15WeaponAsset(p);if(!im?.complete||!im.naturalWidth)return;
  ctx.save();ctx.translate(13,-3);ctx.filter='drop-shadow(0 2px 2px rgba(0,0,0,.55))';
  if((p.gearLevel||1)<=2){ctx.rotate(-.12-sw*.82);ctx.drawImage(im,-7,-16,72,27);}
  else if(p.gearLevel===3){ctx.rotate(-.02);ctx.drawImage(im,-2,-23,58,46);}
  else{ctx.rotate(-.02);ctx.drawImage(im,-1,-22,p.gearLevel>=5?74:67,p.gearLevel>=5?45:42);}
  ctx.restore();
};

v6DrawPad=function(pad){
  if(pad.complete&&pad.kind!=='base')return;
  const s=worldToScreen(pad.x,pad.y),w=pad.size||104,h=78,q=v6PadProgress(pad);
  ctx.save();shadow(s.x,s.y+25,w*.44,13,.19);ctx.translate(s.x,s.y);ctx.globalAlpha=pad.locked?.48:.68;
  ctx.fillStyle=pad.locked?'rgba(35,40,37,.63)':pad.kind==='gear'?'rgba(54,74,62,.66)':'rgba(87,69,42,.62)';
  v6RoundRect(-w/2,-h/2,w,h,14);ctx.fill();
  ctx.strokeStyle=pad.locked?'rgba(135,142,137,.45)':pad.kind==='gear'?'rgba(143,202,164,.68)':'rgba(224,184,105,.68)';ctx.lineWidth=2;ctx.stroke();
  if(!pad.locked&&!pad.complete){ctx.save();ctx.beginPath();v6RoundRect(-w/2,-h/2,w,h,14);ctx.clip();ctx.fillStyle=pad.kind==='gear'?'rgba(134,191,151,.2)':'rgba(239,190,92,.18)';ctx.fillRect(-w/2,-h/2,w*q,h);ctx.restore();}
  ctx.restore();
};

function v15PadForeground(){
  if(!snap)return;
  for(const pad of v6AllPads()){
    if(pad.complete&&pad.kind!=='base')continue;
    const s=worldToScreen(pad.x,pad.y);if(s.x<-100||s.x>W+100||s.y<-120||s.y>H+100)continue;
    const y=s.y-(pad.kind==='base'?92:64),locked=!!pad.locked;let items=[];
    if(!pad.complete&&pad.cost)for(const k of ['wood','stone','meat']){const c=pad.cost[k]||0;if(!c)continue;items.push({k,left:Math.max(0,c-(pad.progress?.[k]||0))});}
    const label=(pad.label||'').replace('공용 무기 · ','무기 '),boxW=Math.max(88,Math.min(176,52+items.length*39)),boxH=items.length?44:28;
    ctx.save();ctx.translate(s.x,y);ctx.globalAlpha=.97;ctx.fillStyle='rgba(7,13,10,.92)';v4Rounded(-boxW/2,-boxH/2,boxW,boxH,11);ctx.fill();
    ctx.strokeStyle=locked?'rgba(180,184,178,.38)':pad.kind==='gear'?'rgba(131,202,164,.68)':'rgba(235,194,104,.62)';ctx.lineWidth=1.4;ctx.stroke();
    ctx.font='800 9px system-ui,sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=locked?'#b9bdb9':'#f2dfb7';ctx.fillText((locked?'🔒 ':'')+label,0,items.length?-11:0);
    if(items.length){const step=items.length===3?43:50,start=-(items.length-1)*step/2;items.forEach((it,i)=>{const x=start+i*step;v6DrawIcon(it.k,x,9,16);ctx.font='800 9px system-ui,sans-serif';ctx.fillStyle=it.left===0?'#9fd291':'#fff1ce';ctx.fillText(String(it.left),x+13,10);});}
    ctx.restore();
  }
}
const v15OldLighting=lighting;lighting=function(){v15OldLighting();v15PadForeground();};

function v15EnsureFeed(){let feed=document.getElementById('v15ChatFeed');if(feed)return feed;feed=document.createElement('div');feed.id='v15ChatFeed';feed.className='v15ChatFeed';document.body.appendChild(feed);return feed;}
function v15PushChat(m){const feed=v15EnsureFeed(),row=document.createElement('div');row.className='v15ChatBubble'+(m.playerId===meId?' me':'');const n=document.createElement('b'),t=document.createElement('span');n.textContent=m.name||'생존자';t.textContent=m.text||'';row.append(n,t);feed.appendChild(row);while(feed.children.length>3)feed.firstChild.remove();clearTimeout(feed._fadeTimer);feed.classList.add('show');feed._fadeTimer=setTimeout(()=>feed.classList.remove('show'),12000);}
v15EnsureFeed();

(function v15BindEat(){const old=v14EnsureEat();if(!old)return;const b=old.cloneNode(true);old.replaceWith(b);b.onclick=null;b.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();if(!b.disabled)send({type:'eat'});},{passive:false});})();

const v15OldHud=updateHud;updateHud=function(){v15OldHud();const p=myPlayer(),b=document.getElementById('eatMeat');if(p&&b){b.disabled=(p.meat||0)<=0;b.textContent=`고기 먹기 · ${p.meat||0}`;b.setAttribute('aria-label',`고기 먹기. 보유 ${p.meat||0}`);}};

const v15OldEvent=eventFx;eventFx=function(m){
  if(m.kind==='kill'&&m.lootTo==='none'){
    if(m.playerId===meId){toast(`${m.enemyName||'습격 몬스터'} 처치 · 공헌 +${m.meritGain}`,'phaseAlert');addFloater(`공헌 +${m.meritGain}`,m.x,m.y-22,'#ffd89a',13);}burst(m.x,m.y,'#c98565',6,125);
  }else v15OldEvent(m);
  if(m.kind==='chat')v15PushChat(m);
  if(m.kind==='meal'&&m.playerId===meId&&m.healed===0)toast(`고기 ${m.used} 소비 · 가방 공간 확보`,'phaseAlert');
};
