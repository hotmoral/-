'use strict';

const http = require('http');
const crypto = require('crypto');
const { URL } = require('url');

const PORT = Number(process.env.PORT || 10000);
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || 'https://timing-defense-v011.onrender.com';
const ROOM_TTL_MS = 2 * 60 * 60 * 1000;
const PARTICIPANT_STALE_MS = 45 * 1000;
const RANDOM_TTL_MS = 90 * 1000;
const CLASSES = new Set(['knight','rogue','tank','archer','mage']);
const METHODS = new Set(['friend','link','random']);

const rooms = new Map();
const streams = new Map();
const randomTickets = new Map();
const randomQueue = [];

function now(){ return Date.now(); }
function id(bytes=16){ return crypto.randomBytes(bytes).toString('hex'); }
function roomCode(){
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  for(let tries=0; tries<100; tries++){
    let code='';
    for(let i=0;i<6;i++) code += alphabet[crypto.randomInt(alphabet.length)];
    if(!rooms.has(code)) return code;
  }
  throw new Error('room-code-exhausted');
}
function cleanNick(v){
  const s = String(v || '').trim().slice(0,12);
  return s || 'PLAYER';
}
function cleanClass(v){ return CLASSES.has(v) ? v : 'knight'; }
function cleanMethod(v){ return METHODS.has(v) ? v : 'friend'; }
function cleanAiFill(value){
  if(!Array.isArray(value)) return [];
  const used = new Set();
  const out=[];
  for(const item of value){
    const pos = Number(item?.pos);
    const cls = cleanClass(item?.cls);
    if(pos < 2 || pos > 4 || used.has(pos)) continue;
    used.add(pos); out.push({pos, cls});
    if(out.length >= 2) break;
  }
  return out.sort((a,b)=>a.pos-b.pos);
}

function cors(req,res){
  const origin = req.headers.origin;
  if(origin && (origin === ALLOWED_ORIGIN || process.env.ALLOW_ANY_ORIGIN === '1')){
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary','Origin');
  } else if(!origin) {
    res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGIN);
  }
  res.setHeader('Access-Control-Allow-Methods','GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers','Content-Type');
  res.setHeader('Cache-Control','no-store');
}
function json(res,status,data){
  res.statusCode=status;
  res.setHeader('Content-Type','application/json; charset=utf-8');
  res.end(JSON.stringify(data));
}
function text(res,status,data){
  res.statusCode=status;
  res.setHeader('Content-Type','text/plain; charset=utf-8');
  res.end(data);
}
function readJson(req){
  return new Promise((resolve,reject)=>{
    let body='';
    req.on('data',c=>{ body += c; if(body.length > 64*1024){ reject(new Error('body-too-large')); req.destroy(); } });
    req.on('end',()=>{
      if(!body) return resolve({});
      try{ resolve(JSON.parse(body)); }catch(e){ reject(new Error('invalid-json')); }
    });
    req.on('error',reject);
  });
}

function humanParticipants(room){
  return [...room.participants.values()].sort((a,b)=>a.slot-b.slot);
}
function publicState(room){
  const humans = humanParticipants(room).map(p=>({
    slot:p.slot,nickname:p.nickname,classId:p.classId,ready:!!p.ready,
    host:p.session === room.hostSession,connected:now()-p.lastSeen <= PARTICIPANT_STALE_MS
  }));
  const openHumanSlots=[];
  const occupied = new Set(humans.map(p=>p.slot));
  for(const a of room.aiFill) occupied.add(a.pos);
  for(let slot=1;slot<=4;slot++) if(!occupied.has(slot)) openHumanSlots.push(slot);
  const allReady = humans.length >= 2 && humans.every(p=>p.ready);
  return {
    code:room.code,method:room.method,status:room.status,createdAt:room.createdAt,
    hostSlot:humans.find(p=>p.host)?.slot || null,
    participants:humans,aiFill:room.aiFill,openHumanSlots,
    canStart:allReady && room.status==='waiting',startAt:room.startAt || null,
    revision:room.revision
  };
}
function broadcast(room){
  room.revision++;
  const set = streams.get(room.code);
  if(!set || !set.size) return;
  const payload = `event: state\ndata: ${JSON.stringify(publicState(room))}\n\n`;
  for(const res of [...set]){
    try{ res.write(payload); }catch(_){ set.delete(res); }
  }
}
function ensureRoom(code){ return rooms.get(String(code||'').toUpperCase()); }
function getParticipant(room,session){ return room?.participants.get(String(session||'')); }
function nextHumanSlot(room){
  const blocked = new Set(room.aiFill.map(a=>a.pos));
  for(const p of room.participants.values()) blocked.add(p.slot);
  for(let i=1;i<=4;i++) if(!blocked.has(i)) return i;
  return null;
}
function createRoom({nickname,classId,aiFill,method}){
  const code=roomCode(), session=id();
  const room={
    code,method:cleanMethod(method),createdAt:now(),updatedAt:now(),status:'waiting',startAt:null,
    hostSession:session,aiFill:cleanAiFill(aiFill),participants:new Map(),revision:0
  };
  room.participants.set(session,{session,slot:1,nickname:cleanNick(nickname),classId:cleanClass(classId),ready:false,lastSeen:now()});
  rooms.set(code,room);
  return {room,session};
}
function joinRoom(room,{nickname,classId}){
  if(room.status!=='waiting') throw new Error('room-not-joinable');
  const slot=nextHumanSlot(room);
  if(!slot) throw new Error('room-full');
  const session=id();
  room.participants.set(session,{session,slot,nickname:cleanNick(nickname),classId:cleanClass(classId),ready:false,lastSeen:now()});
  room.updatedAt=now();
  broadcast(room);
  return {session,slot};
}
function leaveRoom(room,session){
  const p=getParticipant(room,session); if(!p) return false;
  room.participants.delete(session); room.updatedAt=now();
  if(room.hostSession===session){
    const next=humanParticipants(room)[0]; room.hostSession=next?.session || null;
  }
  if(room.participants.size===0){ rooms.delete(room.code); closeStreams(room.code); }
  else broadcast(room);
  return true;
}
function closeStreams(code){
  const set=streams.get(code); if(!set) return;
  for(const res of set){ try{res.end();}catch(_){} }
  streams.delete(code);
}

function matchRandom(){
  while(randomQueue.length>=2){
    const a=randomQueue.shift(), b=randomQueue.shift();
    const ta=randomTickets.get(a), tb=randomTickets.get(b);
    if(!ta || !tb || ta.status!=='searching' || tb.status!=='searching') continue;
    const {room,session:sa}=createRoom({nickname:ta.nickname,classId:ta.classId,aiFill:[],method:'random'});
    const jb=joinRoom(room,{nickname:tb.nickname,classId:tb.classId});
    ta.status='matched'; ta.code=room.code; ta.session=sa; ta.slot=1; ta.host=true;
    tb.status='matched'; tb.code=room.code; tb.session=jb.session; tb.slot=jb.slot; tb.host=false;
    ta.updatedAt=tb.updatedAt=now();
    broadcast(room);
  }
}

async function handler(req,res){
  cors(req,res);
  if(req.method==='OPTIONS'){ res.statusCode=204; return res.end(); }
  const u=new URL(req.url,`http://${req.headers.host||'localhost'}`);
  const path=u.pathname;

  if(req.method==='GET' && path==='/health'){
    return json(res,200,{ok:true,service:'timing-defense-mp',version:'0.1.0',rooms:rooms.size,randomSearching:randomQueue.length,time:now()});
  }

  if(req.method==='POST' && path==='/api/room/create'){
    try{
      const body=await readJson(req); const {room,session}=createRoom(body); broadcast(room);
      return json(res,201,{ok:true,session,state:publicState(room)});
    }catch(e){ return json(res,400,{ok:false,error:e.message}); }
  }

  if(req.method==='POST' && path==='/api/room/join'){
    try{
      const body=await readJson(req), room=ensureRoom(body.code);
      if(!room) return json(res,404,{ok:false,error:'room-not-found'});
      const joined=joinRoom(room,body);
      return json(res,200,{ok:true,session:joined.session,state:publicState(room)});
    }catch(e){ return json(res,409,{ok:false,error:e.message}); }
  }

  const roomMatch=path.match(/^\/api\/room\/([A-Z0-9]{6})(?:\/(state|update|leave|start|stream|heartbeat))?$/i);
  if(roomMatch){
    const code=roomMatch[1].toUpperCase(), action=roomMatch[2]||'state', room=ensureRoom(code);
    if(!room) return json(res,404,{ok:false,error:'room-not-found'});

    if(req.method==='GET' && action==='state') return json(res,200,{ok:true,state:publicState(room)});

    if(req.method==='GET' && action==='stream'){
      const session=u.searchParams.get('session'); const p=getParticipant(room,session);
      if(!p) return json(res,401,{ok:false,error:'invalid-session'});
      p.lastSeen=now();
      res.statusCode=200;
      res.setHeader('Content-Type','text/event-stream; charset=utf-8');
      res.setHeader('Connection','keep-alive');
      res.setHeader('X-Accel-Buffering','no');
      res.write(`event: state\ndata: ${JSON.stringify(publicState(room))}\n\n`);
      if(!streams.has(code)) streams.set(code,new Set());
      streams.get(code).add(res);
      req.on('close',()=>streams.get(code)?.delete(res));
      return;
    }

    if(req.method==='POST' && action==='heartbeat'){
      const body=await readJson(req), p=getParticipant(room,body.session);
      if(!p) return json(res,401,{ok:false,error:'invalid-session'});
      p.lastSeen=now(); room.updatedAt=now(); return json(res,200,{ok:true});
    }

    if(req.method==='POST' && action==='update'){
      const body=await readJson(req), p=getParticipant(room,body.session);
      if(!p) return json(res,401,{ok:false,error:'invalid-session'});
      if(room.status!=='waiting') return json(res,409,{ok:false,error:'room-locked'});
      if(typeof body.ready==='boolean') p.ready=body.ready;
      if(body.nickname!==undefined) p.nickname=cleanNick(body.nickname);
      if(body.classId!==undefined) p.classId=cleanClass(body.classId);
      p.lastSeen=now(); room.updatedAt=now(); broadcast(room);
      return json(res,200,{ok:true,state:publicState(room)});
    }

    if(req.method==='POST' && action==='leave'){
      const body=await readJson(req); leaveRoom(room,body.session); return json(res,200,{ok:true});
    }

    if(req.method==='POST' && action==='start'){
      const body=await readJson(req), p=getParticipant(room,body.session);
      if(!p) return json(res,401,{ok:false,error:'invalid-session'});
      if(room.hostSession!==body.session) return json(res,403,{ok:false,error:'host-only'});
      const state=publicState(room);
      if(!state.canStart) return json(res,409,{ok:false,error:'not-ready',state});
      room.status='starting'; room.startAt=now()+2500; room.updatedAt=now(); broadcast(room);
      return json(res,200,{ok:true,state:publicState(room)});
    }
  }

  if(req.method==='POST' && path==='/api/random/search'){
    try{
      const body=await readJson(req), ticket=id(10);
      randomTickets.set(ticket,{ticket,status:'searching',nickname:cleanNick(body.nickname),classId:cleanClass(body.classId),createdAt:now(),updatedAt:now()});
      randomQueue.push(ticket); matchRandom();
      return json(res,202,{ok:true,ticket,status:randomTickets.get(ticket)});
    }catch(e){ return json(res,400,{ok:false,error:e.message}); }
  }
  if(req.method==='GET' && path==='/api/random/status'){
    const ticket=u.searchParams.get('ticket'), t=randomTickets.get(ticket);
    if(!t) return json(res,404,{ok:false,error:'ticket-not-found'});
    return json(res,200,{ok:true,status:t});
  }
  if(req.method==='POST' && path==='/api/random/cancel'){
    const body=await readJson(req), t=randomTickets.get(body.ticket);
    if(t && t.status==='searching'){ t.status='cancelled'; t.updatedAt=now(); }
    return json(res,200,{ok:true});
  }

  text(res,404,'not found');
}

const server=http.createServer((req,res)=>handler(req,res).catch(err=>{
  console.error(err); if(!res.headersSent) cors(req,res); if(!res.writableEnded) json(res,500,{ok:false,error:'internal'});
}));

setInterval(()=>{
  const t=now();
  for(const room of [...rooms.values()]){
    let changed=false;
    for(const [session,p] of [...room.participants.entries()]){
      if(t-p.lastSeen > PARTICIPANT_STALE_MS*2){ room.participants.delete(session); changed=true; }
    }
    if(changed){
      if(!room.participants.has(room.hostSession)) room.hostSession=humanParticipants(room)[0]?.session||null;
      if(room.participants.size===0){ rooms.delete(room.code); closeStreams(room.code); continue; }
      broadcast(room);
    }
    if(t-room.updatedAt>ROOM_TTL_MS){ rooms.delete(room.code); closeStreams(room.code); }
  }
  for(const [ticket,r] of randomTickets){
    if(t-r.updatedAt>RANDOM_TTL_MS){ randomTickets.delete(ticket); }
  }
  for(const [code,set] of streams){
    for(const res of [...set]){ try{res.write(`: ping ${t}\n\n`);}catch(_){set.delete(res);} }
    if(!set.size) streams.delete(code);
  }
},15000).unref();

server.listen(PORT,'0.0.0.0',()=>console.log(`timing-defense-mp listening on ${PORT}`));
