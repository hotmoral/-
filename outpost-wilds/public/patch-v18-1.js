/* Outpost Wilds V18.1: stop reconciliation, dismissible chat, compact base layout, legacy hint cleanup. */
const V181_POS={
  workshop:{x:1580,y:1900},storage:{x:1580,y:1740},farm:{x:1680,y:2020},watchtower:{x:1950,y:1620},
  forge:{x:1650,y:1620},infirmary:{x:2020,y:1760},wall:{x:2050,y:2035},turret:{x:2010,y:1900},turret2:{x:1925,y:2020}
};
Object.assign(V14_POS,V181_POS);

/* Do not expose the obsolete pre-stockpile guidance. */
const v181OldHud=updateHud;
updateHud=function(){
  v181OldHud();
  const hint=document.getElementById('contextHint');
  if(hint&&/거점에 접근하면 자원이 자동 (?:반납|보관)/.test(hint.textContent||'')){hint.textContent='';hint.className='';}
};

/* Local-player reconciliation: hold the predicted stop briefly so an older server sample cannot pull the avatar backward, then converge once. */
let v181WasMoving=false,v181StoppedAt=-1;
v4Advance=function(){
  if(v18AdvancedSerial===v18FrameSerial)return;
  v18AdvancedSerial=v18FrameSerial;
  const now=performance.now(),dt=Math.min(.05,(now-v4RenderT)/1000);v4RenderT=now;
  if(!snap)return;
  const localMoving=Math.hypot(input.x,input.y)>.035;
  if(v181WasMoving&&!localMoving)v181StoppedAt=now;
  v181WasMoving=localMoving;
  for(const p of snap.players||[]){
    const r=v4State(v4Players,p.id,p.x,p.y);r.tx=p.x;r.ty=p.y;
    if(p.id===meId){
      if(localMoving){const speed=212;r.x=Math.max(35,Math.min(3565,r.x+input.x*speed*dt));r.y=Math.max(35,Math.min(3565,r.y+input.y*speed*dt));}
      const ex=r.tx-r.x,ey=r.ty-r.y,err=Math.hypot(ex,ey);
      if(err>260){r.x=r.tx;r.y=r.ty;}
      else if(localMoving){if(err>120){const k=Math.min(1,dt*.7);r.x+=ex*k;r.y+=ey*k;}}
      else if(now-v181StoppedAt>=240){
        if(err<=8){r.x=r.tx;r.y=r.ty;}
        else{const k=Math.min(1,dt*(err>80?7:4));r.x+=ex*k;r.y+=ey*k;}
      }
    }else{
      const k=Math.min(1,dt*12);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;
    }
  }
  for(const e of snap.enemies||[]){const r=v4State(v4Enemies,e.id,e.x,e.y);r.tx=e.x;r.ty=e.y;const k=Math.min(1,dt*11);r.x+=(r.tx-r.x)*k;r.y+=(r.ty-r.y)*k;}
};

/* Chat behaves like a mobile overlay: X, Escape/Android back, or tapping the game closes it. */
const v181Chat=v14EnsureChat();
let v181HistoryArmed=false,v181Popping=false;
function v181CloseChat(popHistory=true){
  if(!v181Chat.classList.contains('open'))return;
  v181Chat.classList.remove('open');
  v181Chat.querySelector('input')?.blur();
  v18StopInput();
  if(popHistory&&v181HistoryArmed&&history.state?.owChatV181){v181Popping=true;history.back();setTimeout(()=>{v181Popping=false;v181HistoryArmed=false;},0);}
}
new MutationObserver(()=>{
  const open=v181Chat.classList.contains('open');
  if(open&&!v181HistoryArmed){history.pushState({...history.state,owChatV181:true},'');v181HistoryArmed=true;}
  if(!open&&v181HistoryArmed&&!v181Popping&&history.state?.owChatV181){v181Popping=true;history.back();setTimeout(()=>{v181Popping=false;v181HistoryArmed=false;},0);}
}).observe(v181Chat,{attributes:true,attributeFilter:['class']});
addEventListener('popstate',()=>{if(v181Chat.classList.contains('open')){v181Popping=true;v181Chat.classList.remove('open');v181Chat.querySelector('input')?.blur();v18StopInput();v181HistoryArmed=false;setTimeout(()=>v181Popping=false,0);}else{v181HistoryArmed=false;}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&v181Chat.classList.contains('open')){e.preventDefault();v181CloseChat();}},true);
document.addEventListener('pointerdown',e=>{if(v181Chat.classList.contains('open')&&!v181Chat.contains(e.target)){v181CloseChat();}},true);

window.__OW_V181_LAYOUT__={center:{x:1800,y:1800},positions:V181_POS,stopGraceMs:240,chatDismiss:['close','back','game-tap']};
