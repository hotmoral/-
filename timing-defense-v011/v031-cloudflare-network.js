// Timing Defense Cloudflare v0.31 parity — FRIEND/LINK waiting-room transport.
// Replaces the legacy HTTP+SSE lobby channel with Durable Object WebSocket state.
(function(){
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

  let session=null,state=null,socket=null,busy=false,entered=false,slot=null,reconnectTimer=null,socketEpoch=0;

  const style=document.createElement('style');
  style.textContent=`
    #v027Waiting.v031Net{background:linear-gradient(145deg,#172621 0%,#263b31 46%,#18251f 100%)}
    .v031Code{font:1000 19px ui-monospace,SFMono-Regular,monospace;letter-spacing:.16em;color:#f3e4b0;margin-top:7px}
    .v031State{margin-top:8px;font:800 8px/1.45 system-ui;color:#a7b6ae}
    .v031Status{display:inline-flex;align-items:center;gap:6px;margin-top:8px;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.10);font:900 8px system-ui}
    .v031Dot{width:7px;height:7px;border-radius:50%;background:#86d9a8;box-shadow:0 0 10px rgba(134,217,168,.5)}
    .v031Msg{margin-top:8px;min-height:18px;font:760 8px/1.45 system-ui;color:#a8b7af}.v031Msg.err{color:#ffaaaa}.v031Msg.ok{color:#a8efbf}
    .v031Ready{color:#91e7b1}.v031NotReady{color:#889991}.v031Host{color:#f0d98c}
    .v031Copy{user-select:all}.v031StartReady{background:#efe0ac!important;color:#17201b!important;border-color:#efe0ac!important;opacity:1!important}
  `;
  document.head.appendChild(style);

  function idx(){
    const m=(track.style.transform||'').match(/translateX\((-?[\d.]+)%\)/);
    return m?Math.round(Math.abs(parseFloat(m[1]))/100)%CLASSES.length:0;
  }
  function currentClass(){return CLASSES[idx()]||'knight'}
  function nick(){return (document.getElementById('v022Nick')?.value.trim()||window.S?.v022Nickname||'PLAYER').slice(0,12)}
  function method(){return root.querySelector('[data-method].on')?.dataset.method||'friend'}
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
  function sessionKey(code){return `td-cf031-session-${code}`}
  function identityKey(code){return `td-cf031-identity-${code}`}
  function readIdentity(code){try{return JSON.parse(localStorage.getItem(identityKey(code))||'null')}catch(_){return null}}
  function rememberIdentity(code,identity){try{localStorage.setItem(identityKey(code),JSON.stringify(identity))}catch(_){}}
  function rememberSession(code,value){try{localStorage.setItem(sessionKey(code),value)}catch(_){}}
  function forgetIdentity(code){try{localStorage.removeItem(sessionKey(code));localStorage.removeItem(identityKey(code))}catch(_){}}
  function localParticipant(){return state?.participants?.find(p=>p.slot===slot)||null}
  function socketOpen(){return socket?.readyState===WebSocket.OPEN}

  async function api(path,opts={}){
    const r=await fetch(path,{cache:'no-store',...opts,headers:{'Content-Type':'application/json',...(opts.headers||{})}});
    let data={};try{data=await r.json()}catch(_){}
    if(!r.ok)throw new Error(data.error||`HTTP ${r.status}`);
    return data;
  }

  function setMsg(msg,ok){
    const el=waiting.querySelector('#v031Msg');if(!el)return;
    el.textContent=msg||'';el.className='v031Msg '+(ok===true?'ok':ok===false?'err':'');
  }

  function slotHtml(n){
    const p=state?.participants?.find(x=>x.slot===n);
    const a=state?.aiFill?.find(x=>x.pos===n);
    if(p){
      const m=META[p.classId]||META.knight;
      return `<div class="v027Slot ${n===slot?'local':''}">
        <div class="v027SlotHead"><span>P${n}</span><span>${p.host?'<b class="v031Host">HOST</b>':'PLAYER'}</span></div>
        <div class="v027SlotName">${esc(p.nickname)}</div>
        <div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div>
        <div class="${p.ready?'v031Ready':'v031NotReady'}">${p.ready?'READY ✓':'NOT READY'} · ${p.connected?'ONLINE':'OFFLINE'}</div>
      </div>`;
    }
    if(a){
      const m=META[a.cls]||META.knight;
      return `<div class="v027Slot ai"><div class="v027SlotHead"><span>P${n}</span><span>AI FILL</span></div><div class="v027SlotName">CPU ${n}</div><div class="v027SlotSub" style="color:${m.color}">${m.ko} · ${m.name}</div></div>`;
    }
    return `<div class="v027Slot open"><div class="v027SlotHead"><span>P${n}</span><span>HUMAN SLOT</span></div><div class="v027SlotName">WAITING</div><div class="v027SlotSub">원격 참가자 대기</div></div>`;
  }

  function renderRandomUnsupported(){
    waiting.classList.add('v031Net');
    waiting.innerHTML=`<div class="v027WaitTop"><div class="v027WaitBrand">TIMING DEFENSE</div><div class="v027WaitMode">TEAM · RANDOM</div></div>
      <div class="v027WaitBody"><section class="v027WaitPanel"><div class="v027WaitTitle">RANDOM MIGRATION PENDING</div><div class="v027WaitSub">이번 Cloudflare parity slice는 FRIEND/LINK만 검증합니다.</div><div class="v027Truth">RANDOM은 v0.31/v0.32 FRIEND/LINK parity PASS 뒤 별도 이식합니다.</div></section></div>
      <div class="v027WaitFoot"><button class="v027WaitBtn" id="v031Back">← PLAY SETTING</button><div class="v027WaitNote">범위 보호: 전투 및 랜덤 매칭 미이식</div><button class="v027WaitBtn" disabled>START</button></div>`;
    waiting.querySelector('#v031Back')?.addEventListener('click',leave);
  }

  function render(){
    if(!waiting.classList.contains('show'))return;
    if(method()==='random'&&!state){renderRandomUnsupported();return}
    waiting.classList.add('v031Net');
    const m=state?.method||method();
    const lp=localParticipant();
    const host=!!lp?.host;
    const starting=state?.status==='starting';
    const running=state?.status==='running';
    const invite=state?.code?shareUrl(state.code):'';
    const title=starting?'RUN STARTING':running?'RUN GATE OPEN':'ONLINE WAITING ROOM';
    const note=running?'동기 시작 게이트 통과 · Stage 1 전투는 다음 이식 단계':starting?'동일 startAt 대기 중':'실제 원격 참가자 상태를 Durable Object에서 수신 중';
    waiting.innerHTML=`<div class="v027WaitTop"><div class="v027WaitBrand">TIMING DEFENSE</div><div class="v027WaitMode">TEAM · ${String(m).toUpperCase()}</div></div>
      <div class="v027WaitBody">
        <section class="v027WaitPanel">
          <div class="v027WaitTitle">${title}</div>
          <div class="v027WaitSub">${state?'Cloudflare 방 권한이 참가자 슬롯과 READY 상태를 공유하고 있습니다.':'Cloudflare 방에 연결 중입니다.'}</div>
          ${state?.code?`<div class="v031Code">${state.code}</div><div class="v031State">ROOM CODE · ${state.participants.length} HUMAN · ${state.aiFill.length} AI · REV ${state.revision}</div>`:''}
          <div class="v031Status"><span class="v031Dot"></span>${socketOpen()?'SERVER CONNECTED':'CONNECTING'}</div>
          ${state?`<div class="v027LocalCard"><div class="v027LocalTop"><span class="v027Nick">${esc(lp?.nickname||nick())}</span><span class="v027Class" style="color:${META[lp?.classId||currentClass()].color}">${META[lp?.classId||currentClass()].ko} · ${META[lp?.classId||currentClass()].name}</span></div><div class="v027Truth">${host?'내가 방장입니다. 모든 사람 참가자가 READY이면 START를 누를 수 있습니다.':'방장이 시작할 때까지 READY 상태로 기다립니다.'}</div></div>`:''}
          <div class="v027WaitActions">
            ${state?`<button class="v027WaitBtn primary" id="v031Ready" ${state.status==='waiting'?'':'disabled'}>${lp?.ready?'READY ✓':'READY'}</button>`:''}
            ${state?.code?`<button class="v027WaitBtn" id="v031Share">${m==='friend'?'INVITE':'COPY LINK'}</button>`:''}
          </div>
          <div id="v031Msg" class="v031Msg">${starting&&state.startAt?`동기 시작 시각: ${new Date(state.startAt).toLocaleTimeString()}`:running?'동기 시작 게이트를 통과했습니다.':''}</div>
          ${state?.code?`<div class="v027Truth v031Copy">${esc(invite)}</div>`:''}
        </section>
        <section class="v027WaitPanel"><div class="v027SlotTitle">PARTICIPANT SLOTS</div><div class="v027Slots">${[1,2,3,4].map(slotHtml).join('')}</div></section>
      </div>
      <div class="v027WaitFoot">
        <button class="v027WaitBtn" id="v031Back">← PLAY SETTING</button>
        <div class="v027WaitNote">${note}</div>
        <button class="v027WaitBtn ${host&&state?.canStart?'v031StartReady':''}" id="v031Start" ${host&&state?.canStart&&state.status==='waiting'?'':'disabled'}>START</button>
      </div>`;
    waiting.querySelector('#v031Ready')?.addEventListener('click',toggleReady);
    waiting.querySelector('#v031Share')?.addEventListener('click',share);
    waiting.querySelector('#v031Back')?.addEventListener('click',leave);
    waiting.querySelector('#v031Start')?.addEventListener('click',start);
  }

  function closeSocket(){
    socketEpoch++;
    clearTimeout(reconnectTimer);reconnectTimer=null;
    try{socket?.close()}catch(_){}
    socket=null;
  }

  function openSocket(code,identity){
    closeSocket();
    const epoch=socketEpoch;
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    if(session)u.searchParams.set('session',session);
    u.searchParams.set('nickname',identity.nickname);
    u.searchParams.set('classId',identity.classId);
    const current=new WebSocket(u);socket=current;

    current.onopen=()=>{if(epoch!==socketEpoch)return;render();setMsg('WebSocket 연결됨',true)};
    current.onmessage=e=>{
      if(epoch!==socketEpoch)return;
      let d;try{d=JSON.parse(e.data)}catch(_){return}
      if(d.type==='welcome'){
        session=d.session;slot=d.slot;state=d.state;
        rememberSession(code,session);rememberIdentity(code,{nickname:localParticipant()?.nickname||identity.nickname,classId:localParticipant()?.classId||identity.classId});
        render();setMsg(`P${slot} 세션 연결`,true);return;
      }
      if(d.type==='state'){state=d.state;render();return}
      if(d.type==='error')setMsg(`SERVER ERROR: ${d.error}`,false);
    };
    current.onerror=()=>{if(epoch===socketEpoch)setMsg('WebSocket 오류',false)};
    current.onclose=e=>{
      if(epoch!==socketEpoch)return;
      render();setMsg(`연결 종료 ${e.code} · 재연결 시도`,false);
      if(waiting.classList.contains('show')&&state?.code&&session){
        reconnectTimer=setTimeout(()=>{
          const remembered=readIdentity(code)||identity;
          openSocket(code,remembered);
        },700);
      }
    };
  }

  async function createOrJoin(){
    if(busy||state)return;
    busy=true;render();
    try{
      const code=roomFromUrl();
      if(code){
        await api(`/api/room/${code}/state`);
        session=localStorage.getItem(sessionKey(code))||null;
        const identity=session?(readIdentity(code)||{nickname:nick(),classId:currentClass()}):{nickname:nick(),classId:currentClass()};
        openSocket(code,identity);
      }else{
        const identity={nickname:nick(),classId:currentClass()};
        const d=await api('/api/room/create',{method:'POST',body:JSON.stringify({nickname:identity.nickname,classId:identity.classId,aiFill:aiFill(),method:method()})});
        session=d.session;slot=d.slot;state=d.state;
        rememberSession(d.code,session);rememberIdentity(d.code,identity);
        history.replaceState(null,'',shareUrl(d.code));
        openSocket(d.code,identity);
      }
    }catch(e){render();setMsg(`연결 실패: ${e.message}`,false)}
    finally{busy=false}
  }

  function send(payload){if(socketOpen())socket.send(JSON.stringify(payload))}
  function toggleReady(){const lp=localParticipant();if(!lp||state?.status!=='waiting')return;send({type:'ready',ready:!lp.ready})}
  function start(){if(!state?.canStart||!localParticipant()?.host||state.status!=='waiting')return;send({type:'start'})}

  async function share(){
    if(!state?.code)return;
    const url=shareUrl(state.code);
    try{
      if(navigator.share){await navigator.share({title:'Timing Defense',text:`Timing Defense 방 ${state.code}`,url});setMsg('초대 링크를 열었습니다.',true)}
      else if(navigator.clipboard){await navigator.clipboard.writeText(url);setMsg('방 링크를 복사했습니다.',true)}
      else setMsg(url,true);
    }catch(_){}
  }

  async function leave(){
    const code=state?.code||roomFromUrl();
    const leavingSession=session;
    closeSocket();
    try{if(code&&leavingSession)await api(`/api/room/${code}/leave`,{method:'POST',body:JSON.stringify({session:leavingSession})})}catch(_){}
    if(code)forgetIdentity(code);
    state=null;session=null;slot=null;
    const u=new URL(location.href);u.searchParams.delete('room');history.replaceState(null,'',u);
    waiting.classList.remove('show','v031Net');
  }

  function onShown(){
    if(!waiting.classList.contains('show')||entered)return;
    entered=true;
    if(method()==='random')renderRandomUnsupported();else createOrJoin();
  }

  new MutationObserver(()=>{
    if(waiting.classList.contains('show'))onShown();
    else entered=false;
  }).observe(waiting,{attributes:true,attributeFilter:['class']});

  const inviteCode=roomFromUrl();
  if(inviteCode){
    const team=root.querySelector('[data-mode="team"]');if(team&&!team.classList.contains('on'))team.click();
    const link=root.querySelector('[data-method="link"]');if(link&&!link.classList.contains('on'))link.click();
    if(localStorage.getItem(sessionKey(inviteCode))){
      setTimeout(()=>document.getElementById('v022Start')?.click(),0);
    }
  }
})();
