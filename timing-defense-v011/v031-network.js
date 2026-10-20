// Timing Defense v0.31 — real shared TEAM room transport (room/join/ready/start gate).
// Adds authoritative lobby networking only. Combat synchronization is deliberately not enabled yet.
(function(){
  const API='https://timing-defense-mp.onrender.com';
  const root=document.getElementById('v022Lobby');
  const waiting=document.getElementById('v027Waiting');
  const track=document.getElementById('v022Track');
  if(!root||!waiting||!track)return;

  const CLASSES=['knight','rogue','tank','archer','mage'];
  const META={
    knight:{name:'KNIGHT',ko:'기사',color:'#ffd76a'},
    rogue:{name:'ROGUE',ko:'도적',color:'#d9e0e5'},
    tank:{name:'TANK',ko:'탱커',color:'#69b6ff'},
    archer:{name:'ARCHER',ko:'궁수',color:'#98e493'},
    mage:{name:'MAGE',ko:'마법사',color:'#d0aaff'}
  };

  let session=null, state=null, stream=null, heartbeat=null, busy=false, randomTicket=null, randomPoll=null;
  let entered=false;

  const style=document.createElement('style');
  style.textContent=`
    #v027Waiting.v031Net{background:linear-gradient(145deg,#172621 0%,#263b31 46%,#18251f 100%)}
    .v031Code{font:1000 19px ui-monospace,SFMono-Regular,monospace;letter-spacing:.16em;color:#f3e4b0;margin-top:7px}
    .v031State{margin-top:8px;font:800 8px/1.45 system-ui;color:#a7b6ae}
    .v031Status{display:inline-flex;align-items:center;gap:6px;margin-top:8px;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.10);font:900 8px system-ui}
    .v031Dot{width:7px;height:7px;border-radius:50%;background:#86d9a8;box-shadow:0 0 10px rgba(134,217,168,.5)}
    .v031Join{display:flex;gap:6px;margin-top:10px}.v031Join input{min-width:0;flex:1;border:1px solid rgba(255,255,255,.13);background:rgba(0,0,0,.22);color:#fff;border-radius:8px;padding:7px 9px;font:900 10px ui-monospace;text-transform:uppercase;letter-spacing:.12em;outline:none}
    .v031Msg{margin-top:8px;min-height:18px;font:760 8px/1.45 system-ui;color:#a8b7af}.v031Msg.err{color:#ffaaaa}.v031Msg.ok{color:#a8efbf}
    .v031Ready{color:#91e7b1}.v031NotReady{color:#889991}.v031Host{color:#f0d98c}
    .v031Copy{user-select:all}
    .v031StartReady{background:#efe0ac!important;color:#17201b!important;border-color:#efe0ac!important;opacity:1!important}
    .v031WaitStarting{font:1000 18px system-ui;color:#f3e4b0;margin-top:14px}
  `;
  document.head.appendChild(style);

  function idx(){
    const m=(track.style.transform||'').match(/translateX\((-?[\d.]+)%\)/);
    return m?Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length:0;
  }
  function currentClass(){ return CLASSES[idx()]||'knight'; }
  function nick(){ return (document.getElementById('v022Nick')?.value.trim()||S.v022Nickname||'PLAYER').slice(0,12); }
  function method(){ return root.querySelector('[data-method].on')?.dataset.method||'friend'; }
  function aiFill(){
    const out=[];
    root.querySelectorAll('#v022AiRows .aiRow').forEach(row=>{
      const p=row.querySelector('[data-pos].on')?.dataset.pos;
      const c=row.querySelector('[data-aicls].on')?.dataset.aicls;
      if(!p||!c)return;
      const pos=Number(p.split(':')[1]),cls=c.split(':')[1];
      if(pos>=2&&pos<=4&&META[cls])out.push({pos,cls});
    });
    return out.slice(0,2);
  }
  function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
  function roomFromUrl(){return (new URL(location.href)).searchParams.get('room')?.toUpperCase()||''}
  function shareUrl(code){const u=new URL(location.href);u.search='';u.searchParams.set('room',code);return u.toString()}
  async function api(path,opts={}){
    const r=await fetch(API+path,{cache:'no-store',...opts,headers:{'Content-Type':'application/json',...(opts.headers||{})}});
    let data={};try{data=await r.json()}catch(_){}
    if(!r.ok)throw new Error(data.error||`HTTP ${r.status}`);
    return data;
  }
  function stopLive(){
    try{stream?.close()}catch(_){}
    stream=null;
    clearInterval(heartbeat);heartbeat=null;
    clearInterval(randomPoll);randomPoll=null;
  }
  function attachLive(){
    stopLive();
    if(!state?.code||!session)return;
    stream=new EventSource(`${API}/api/room/${state.code}/stream?session=${encodeURIComponent(session)}`);
    stream.addEventListener('state',e=>{
      try{state=JSON.parse(e.data);render()}catch(_){}
    });
    stream.onerror=()=>setMsg('연결을 다시 시도하고 있습니다.',false);
    heartbeat=setInterval(()=>api(`/api/room/${state.code}/heartbeat`,{method:'POST',body:JSON.stringify({session})}).catch(()=>{}),20000);
  }
  function localParticipant(){
    return state?.participants?.find(p=>p.slot===window.__v031Slot)||null;
  }
  function setMsg(msg,ok){
    const el=waiting.querySelector('#v031Msg');if(!el)return;
    el.textContent=msg||'';el.className='v031Msg '+(ok===true?'ok':ok===false?'err':'');
  }
  function slotHtml(slot){
    const p=state?.participants?.find(x=>x.slot===slot);
    const a=state?.aiFill?.find(x=>x.pos===slot);
    if(p){
      const m=META[p.classId]||META.knight;
      return `<div class="v027Slot ${slot===window.__v031Slot?'local':''}">
        <div class="v027SlotHead"><span>P${slot}</span><span>${p.host?'<b class="v031Host">HOST</b>':'PLAYER'}</span></div>
        <div class="v027SlotName">${esc(p.nickname)}</div>
        <div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div>
        <div class="${p.ready?'v031Ready':'v031NotReady'}">${p.ready?'READY ✓':'NOT READY'}</div>
      </div>`;
    }
    if(a){
      const m=META[a.cls]||META.knight;
      return `<div class="v027Slot ai"><div class="v027SlotHead"><span>P${slot}</span><span>AI FILL</span></div><div class="v027SlotName">CPU ${slot}</div><div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div></div>`;
    }
    return `<div class="v027Slot open"><div class="v027SlotHead"><span>P${slot}</span><span>HUMAN SLOT</span></div><div class="v027SlotName">WAITING</div><div class="v027SlotSub">원격 참가자 대기</div></div>`;
  }
  function render(){
    if(!waiting.classList.contains('show'))return;
    waiting.classList.add('v031Net');
    const m=method();
    const lp=localParticipant();
    const host=!!lp?.host;
    const starting=state?.status==='starting';
    const invite=state?.code?shareUrl(state.code):'';
    waiting.innerHTML=`<div class="v027WaitTop"><div class="v027WaitBrand">TIMING DEFENSE</div><div class="v027WaitMode">TEAM · ${(state?.method||m).toUpperCase()}</div></div>
      <div class="v027WaitBody">
        <section class="v027WaitPanel">
          <div class="v027WaitTitle">${starting?'RUN STARTING':'ONLINE WAITING ROOM'}</div>
          <div class="v027WaitSub">${state?'서버가 참가자 슬롯과 READY 상태를 공유하고 있습니다.':'방 서버에 연결 중입니다.'}</div>
          ${state?.code?`<div class="v031Code">${state.code}</div><div class="v031State">ROOM CODE · ${state.participants.length} HUMAN · ${state.aiFill.length} AI</div>`:''}
          <div class="v031Status"><span class="v031Dot"></span>${state?'SERVER CONNECTED':'CONNECTING'}</div>
          ${state?`<div class="v027LocalCard"><div class="v027LocalTop"><span class="v027Nick">${esc(lp?.nickname||nick())}</span><span class="v027Class" style="color:${META[lp?.classId||currentClass()].color}">${META[lp?.classId||currentClass()].ko} · ${META[lp?.classId||currentClass()].name}</span></div>
            <div class="v027Truth">${host?'내가 방장입니다. 모든 사람 참가자가 READY이면 START를 누를 수 있습니다.':'방장이 시작할 때까지 READY 상태로 기다립니다.'}</div></div>`:''}
          <div class="v027WaitActions">
            ${state?`<button class="v027WaitBtn primary" id="v031Ready">${lp?.ready?'READY ✓':'READY'}</button>`:''}
            ${state?.code?`<button class="v027WaitBtn" id="v031Share">${m==='friend'?'INVITE':'COPY LINK'}</button>`:''}
          </div>
          <div id="v031Msg" class="v031Msg">${starting?`동기 시작 시각: ${new Date(state.startAt).toLocaleTimeString()}`:''}</div>
          ${state?.code?`<div class="v027Truth v031Copy">${esc(invite)}</div>`:''}
        </section>
        <section class="v027WaitPanel"><div class="v027SlotTitle">PARTICIPANT SLOTS</div><div class="v027Slots">${[1,2,3,4].map(slotHtml).join('')}</div></section>
      </div>
      <div class="v027WaitFoot">
        <button class="v027WaitBtn" id="v031Back">← PLAY SETTING</button>
        <div class="v027WaitNote">${starting?'서버 시작 게이트 확인됨 · 전투 상태 동기화는 다음 단계':'실제 원격 참가자 상태를 서버에서 수신 중'}</div>
        <button class="v027WaitBtn ${host&&state?.canStart?'v031StartReady':''}" id="v031Start" ${host&&state?.canStart&&!starting?'':'disabled'}>START</button>
      </div>`;
    waiting.querySelector('#v031Ready')?.addEventListener('click',toggleReady);
    waiting.querySelector('#v031Share')?.addEventListener('click',share);
    waiting.querySelector('#v031Back')?.addEventListener('click',leave);
    waiting.querySelector('#v031Start')?.addEventListener('click',start);
  }
  async function createOrJoin(){
    if(busy||state)return;
    busy=true;render();
    try{
      const code=roomFromUrl();
      if(code){
        const d=await api('/api/room/join',{method:'POST',body:JSON.stringify({code,nickname:nick(),classId:currentClass()})});
        session=d.session;state=d.state;
        window.__v031Slot=state.participants.find(p=>p.nickname===nick()&&p.classId===currentClass()&&!p.host)?.slot||state.participants.at(-1)?.slot;
      }else{
        const d=await api('/api/room/create',{method:'POST',body:JSON.stringify({nickname:nick(),classId:currentClass(),aiFill:aiFill(),method:method()})});
        session=d.session;state=d.state;window.__v031Slot=1;
        history.replaceState(null,'',shareUrl(state.code));
      }
      attachLive();render();
    }catch(e){render();setMsg(`연결 실패: ${e.message}`,false)}
    finally{busy=false}
  }
  async function toggleReady(){
    const lp=localParticipant();if(!lp||busy)return;busy=true;
    try{
      const d=await api(`/api/room/${state.code}/update`,{method:'POST',body:JSON.stringify({session,ready:!lp.ready})});
      state=d.state;render();
    }catch(e){setMsg(e.message,false)}finally{busy=false}
  }
  async function share(){
    const url=shareUrl(state.code);
    try{
      if(navigator.share){await navigator.share({title:'Timing Defense',text:`Timing Defense 방 ${state.code}`,url});setMsg('초대 링크를 열었습니다.',true)}
      else if(navigator.clipboard){await navigator.clipboard.writeText(url);setMsg('방 링크를 복사했습니다.',true)}
      else setMsg(url,true);
    }catch(_){}
  }
  async function leave(){
    stopLive();
    try{if(state?.code&&session)await api(`/api/room/${state.code}/leave`,{method:'POST',body:JSON.stringify({session})})}catch(_){}
    state=null;session=null;window.__v031Slot=null;
    const u=new URL(location.href);u.searchParams.delete('room');history.replaceState(null,'',u);
    waiting.classList.remove('show','v031Net');
  }
  async function start(){
    if(!state?.canStart||!localParticipant()?.host||busy)return;busy=true;
    try{const d=await api(`/api/room/${state.code}/start`,{method:'POST',body:JSON.stringify({session})});state=d.state;render()}
    catch(e){setMsg(e.message,false)}finally{busy=false}
  }

  async function beginRandom(){
    if(busy||randomTicket||state)return;busy=true;render();
    try{
      const d=await api('/api/random/search',{method:'POST',body:JSON.stringify({nickname:nick(),classId:currentClass()})});
      randomTicket=d.ticket;setMsg('랜덤 상대를 찾는 중입니다.',true);
      randomPoll=setInterval(async()=>{
        try{
          const r=await api(`/api/random/status?ticket=${encodeURIComponent(randomTicket)}`);
          if(r.status.status==='matched'){
            clearInterval(randomPoll);randomPoll=null;
            session=r.status.session;window.__v031Slot=r.status.slot;
            const s=await api(`/api/room/${r.status.code}/state`);
            state=s.state;history.replaceState(null,'',shareUrl(state.code));attachLive();render();
          }
        }catch(e){setMsg(e.message,false)}
      },1000);
    }catch(e){setMsg(`매칭 실패: ${e.message}`,false)}finally{busy=false}
  }

  function onShown(){
    if(!waiting.classList.contains('show')||entered)return;
    entered=true;
    if(method()==='random')beginRandom();else createOrJoin();
  }
  new MutationObserver(()=>{if(waiting.classList.contains('show')){onShown()}else{entered=false}}).observe(waiting,{attributes:true,attributeFilter:['class']});

  const inviteCode=roomFromUrl();
  if(inviteCode){
    const team=root.querySelector('[data-mode="team"]');if(team&&!team.classList.contains('on'))team.click();
    const link=root.querySelector('[data-method="link"]');if(link&&!link.classList.contains('on'))link.click();
  }
})();
