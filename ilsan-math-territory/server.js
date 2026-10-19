const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });
app.use(express.static('public'));
app.get('/health', (_req, res) => res.json({ ok: true, version: '0.1.0' }));

const PORT = process.env.PORT || 3000;
const TICK_MS = 1000;
const GAME_SECONDS_PER_TICK = 60; // accelerated pilot clock
const SUPPORT_MAX = 0.060;
const HQ_SUPPORT = 0.180;
const CAPTURE_REQ = 25;
const ACTIVATION_REQ = 5;
const PREP_DEFENSE_RATE = 0.70;
const MIN_READY = 0.59;
const EMERGENCY_FRAC = 0.40;
const LEVELS = [
  { cap: 50, prod: 0.030, maintain: 8, grow: 20 },
  { cap: 55, prod: 0.040, maintain: 11, grow: 50 },
  { cap: 60, prod: 0.050, maintain: 15, grow: 120 },
  { cap: 70, prod: 0.060, maintain: 20, grow: 260 },
  { cap: 80, prod: 0.075, maintain: 26, grow: null }
];

const coords = [
[37.680977,126.753891],[37.678474,126.750636],[37.675970,126.747380],[37.673466,126.744124],[37.670963,126.740869],
[37.674679,126.761619],[37.672176,126.758364],[37.669672,126.755108],[37.667168,126.751852],[37.664665,126.748597],
[37.668381,126.769347],[37.665878,126.766092],[37.663374,126.762836],[37.660870,126.759580],[37.658367,126.756325],
[37.662083,126.777075],[37.659580,126.773820],[37.657076,126.770564],[37.654572,126.767308],[37.652069,126.764053],
[37.655785,126.784803],[37.653282,126.781548],[37.650778,126.778292],[37.648274,126.775036],[37.645771,126.771781],
[37.649487,126.792531],[37.646984,126.789276],[37.644480,126.786020],[37.641976,126.782764],[37.639473,126.779509]
];
const COLS=6, ROWS=5;
const nodeId=(c,r)=>c*ROWS+r;
const edges=[];
for(let c=0;c<COLS;c++) for(let r=0;r<ROWS;r++){
  if(c+1<COLS) edges.push([nodeId(c,r),nodeId(c+1,r)]);
  if(r+1<ROWS) edges.push([nodeId(c,r),nodeId(c,r+1)]);
}
const diag=[[[1,0],[2,1]],[[4,0],[3,1]],[[1,4],[2,3]],[[4,4],[3,3]],[[1,1],[2,2]],[[4,1],[3,2]],[[1,3],[2,2]],[[4,3],[3,2]]];
for(const [a,b] of diag) edges.push([nodeId(...a),nodeId(...b)]);
const adj=Array.from({length:30},()=>[]);
for(const [a,b] of edges){ adj[a].push(b); adj[b].push(a); }

const names = [
 '대화 북부','대화 중앙','대화 거점','대화 남부','킨텍스 서부',
 '주엽 북부','주엽 중앙','주엽 서부','주엽 남부','킨텍스 동부',
 '호수 북서','호수 서부','호수 중서','호수 남서','호수 서남',
 '정발산 북부','정발산 중앙','문화 중앙','호수 중동','호수 남동',
 '마두 북부','마두 중앙','마두 서부','마두 남부','장항 남부',
 '백석 북부','백석 중앙','백석 거점','백석 남부','백석 서남'
];
const typeByRow=['CALC','HOLE','COMP','RULE','MIX'];
const typeLabel={CALC:'계산',HOLE:'빈칸',COMP:'비교',RULE:'규칙',MIX:'혼합'};

function initialBase(id){
  const col=Math.floor(id/ROWS), row=id%ROWS;
  const team=col<3?'blue':'red';
  return {
    id, name:names[id], lat:coords[id][0], lng:coords[id][1], row, col,
    problemType:typeByRow[row], problemLabel:typeLabel[typeByRow[row]],
    control:team, territory:team, state:'ACTIVE', level:1,
    garrison:50, maintenance:0, growth:0, activation:0,
    contestTeam:null, contest:0, leveledToday:false
  };
}
let bases=Array.from({length:30},(_,i)=>initialBase(i));
let commitments=new Map();
let lastFlows=[];
let gameRevision=1;

function growthFrac(b){ if(b.level>=5) return 0; const req=LEVELS[b.level-1].grow; return Math.min(1,b.growth/req); }
function maintainFrac(b){ const req=LEVELS[b.level-1].maintain; return Math.min(1,b.maintenance/req); }
function readiness(b){ return MIN_READY+(1-MIN_READY)*maintainFrac(b); }
function capOf(b){
  if(b.state==='PREPARING') return 50;
  if(b.level>=5) return 80;
  const f=growthFrac(b), a=LEVELS[b.level-1].cap, n=LEVELS[b.level].cap;
  return a+f*(n-a);
}
function prodOf(b){
  if(b.state==='PREPARING') return LEVELS[0].prod*PREP_DEFENSE_RATE;
  let p;
  if(b.level>=5) p=LEVELS[4].prod;
  else { const f=growthFrac(b); p=LEVELS[b.level-1].prod+f*(LEVELS[b.level].prod-LEVELS[b.level-1].prod); }
  return p*readiness(b);
}
function supportCapOf(b){ return SUPPORT_MAX*(b.state==='PREPARING'?PREP_DEFENSE_RATE:readiness(b)); }
function frontier(id,team){ return adj[id].some(j=>bases[j].control!==team); }
function rowRank(r){ return [3,1,0,2,4][r]; }
function validCommit(a,t){
  const A=bases[a], T=bases[t];
  if(A.state!=='ACTIVE' || !adj[a].includes(t)) return false;
  if(T.control!==A.control) return true;
  return T.garrison < capOf(T)-0.01;
}
function assignTargets(){
  for(const [a,t] of [...commitments]) if(!validCommit(a,t)) commitments.delete(a);
  const occupied=new Set([...commitments.values()]);
  const candidates=[];
  for(const A of bases){
    if(A.state!=='ACTIVE' || commitments.has(A.id) || A.garrison < EMERGENCY_FRAC*capOf(A)) continue;
    for(const t of adj[A.id]){
      const T=bases[t]; if(T.control===A.control || occupied.has(t)) continue;
      const preparing=T.state==='PREPARING'?0:1;
      const weakness=T.garrison/Math.max(1,capOf(T));
      candidates.push({a:A.id,t,score:[preparing,weakness,rowRank(T.row),Math.abs(T.col-2.5)]});
    }
  }
  candidates.sort((x,y)=>{
    for(let i=0;i<x.score.length;i++){ if(x.score[i]!==y.score[i]) return x.score[i]-y.score[i]; }
    return 0;
  });
  const usedA=new Set(commitments.keys());
  for(const c of candidates){ if(usedA.has(c.a)||occupied.has(c.t)) continue; commitments.set(c.a,c.t); usedA.add(c.a); occupied.add(c.t); }
}

function militaryTick(){
  const caps=bases.map(capOf), prods=bases.map(prodOf), full=bases.map((b,i)=>b.garrison>=caps[i]-0.01);
  assignTargets();
  const threatened=new Set();
  for(const [a,t] of commitments) if(bases[a].control!==bases[t].control) threatened.add(t);
  const pools={blue:HQ_SUPPORT,red:HQ_SUPPORT};
  for(const b of bases) if(b.state==='ACTIVE' && full[b.id] && !commitments.has(b.id)) pools[b.control]+=prods[b.id];
  const defSupport=new Map(), atkSupport=new Map();
  for(const team of ['blue','red']){
    const em=bases.filter(b=>b.control===team&&threatened.has(b.id)&&b.garrison<=EMERGENCY_FRAC*caps[b.id])
      .sort((a,b)=>(a.garrison/caps[a.id])-(b.garrison/caps[b.id]) || rowRank(a.row)-rowRank(b.row));
    for(const b of em){ const u=Math.min(supportCapOf(b),pools[team]); defSupport.set(b.id,u); pools[team]-=u; }
    const ats=[...commitments.keys()].filter(a=>bases[a].control===team).sort((a,b)=>rowRank(bases[commitments.get(a)].row)-rowRank(bases[commitments.get(b)].row));
    for(const a of ats){ const u=Math.min(supportCapOf(bases[a]),pools[team]); atkSupport.set(a,u); pools[team]-=u; }
  }
  // refill nodes that were not full at tick start
  for(const b of bases){
    if(!full[b.id]){
      const rate=prods[b.id]+(defSupport.get(b.id)||0)+(atkSupport.get(b.id)||0);
      b.garrison=Math.min(caps[b.id],b.garrison+rate*GAME_SECONDS_PER_TICK);
    }
  }
  const directed=new Map();
  for(const [a,t] of commitments){
    const A=bases[a],T=bases[t]; if(!full[a]||A.garrison<EMERGENCY_FRAC*caps[a]) continue;
    const rate=prods[a]+(atkSupport.get(a)||0);
    if(T.control===A.control){ if(T.garrison<caps[t]-0.01) directed.set(`${a}:${t}`,rate); }
    else directed.set(`${a}:${t}`,rate);
  }
  const net=[]; const seen=new Set();
  for(const [key,rate] of directed){
    const [a,t]=key.split(':').map(Number), edgeKey=a<t?`${a}-${t}`:`${t}-${a}`; if(seen.has(edgeKey)) continue; seen.add(edgeKey);
    const r1=directed.get(`${a}:${t}`)||0, r2=directed.get(`${t}:${a}`)||0;
    if(r1>r2+1e-6) net.push({from:a,to:t,rate:r1-r2,team:bases[a].control});
    else if(r2>r1+1e-6) net.push({from:t,to:a,rate:r2-r1,team:bases[t].control});
  }
  const staged=[];
  for(const f of net){
    const A=bases[f.from],T=bases[f.to];
    if(T.control===A.control){ T.garrison=Math.min(capOf(T),T.garrison+f.rate*GAME_SECONDS_PER_TICK); continue; }
    let damage=f.rate*GAME_SECONDS_PER_TICK;
    if(T.garrison>0){
      const used=Math.min(T.garrison,damage); T.garrison-=used; damage-=used;
    }
    if(damage>0){
      if(!T.contestTeam){ T.contestTeam=A.control; T.contest=damage; }
      else if(T.contestTeam===A.control) T.contest+=damage;
      else if(damage>=T.contest){ T.contestTeam=A.control; T.contest=damage-T.contest; }
      else T.contest-=damage;
      if(T.contest>=CAPTURE_REQ) staged.push({id:T.id,team:T.contestTeam});
    }
  }
  // commit captures together
  for(const c of staged){
    const b=bases[c.id];
    b.control=c.team; b.territory=null; b.state='PREPARING'; b.level=1; b.garrison=CAPTURE_REQ;
    b.maintenance=0;b.growth=0;b.activation=0;b.contest=0;b.contestTeam=null;b.leveledToday=false;
    commitments.delete(c.id);
  }
  lastFlows=net.map(f=>({from:f.from,to:f.to,rate:+f.rate.toFixed(3),team:f.team}));
  gameRevision++;
}

function applyContribution(baseId,team,count){
  const b=bases[baseId]; let rem=count, applied=0;
  if(!b || b.control!==team) return {applied:0,reason:'BASE_NOT_CONTROLLED'};
  if(b.state==='PREPARING'){
    const use=Math.min(rem,ACTIVATION_REQ-b.activation); b.activation+=use; applied+=use;
    if(b.activation>=ACTIVATION_REQ){ b.state='ACTIVE'; b.territory=team; b.maintenance=LEVELS[0].maintain; }
    return {applied,reason:applied<count?'ACTIVATION_COMPLETED':'APPLIED'};
  }
  if(b.territory!==team) return {applied:0,reason:'BASE_NOT_OWNED'};
  const mReq=LEVELS[b.level-1].maintain;
  if(b.maintenance<mReq){ const u=Math.min(rem,mReq-b.maintenance); b.maintenance+=u; rem-=u; applied+=u; }
  if(rem>0 && b.level<5 && !b.leveledToday){
    const gReq=LEVELS[b.level-1].grow, u=Math.min(rem,gReq-b.growth); b.growth+=u; rem-=u; applied+=u;
    if(b.growth>=gReq-1e-9){
      const oldCap=LEVELS[b.level-1].cap, empty=Math.max(0,oldCap-b.garrison);
      b.level++; b.growth=0; b.leveledToday=true; b.garrison=Math.max(0,LEVELS[b.level-1].cap-empty);
    }
  }
  return {applied,reason:applied<count?'PARTIAL':'APPLIED'};
}

function publicState(){
  const score={blue:0,red:0,preparing:0};
  for(const b of bases){ if(b.state==='ACTIVE'&&b.territory) score[b.territory]++; else score.preparing++; }
  return {
    revision:gameRevision, accelerated:true, speed:60, score,
    bases:bases.map(b=>({
      ...b, cap:+capOf(b).toFixed(1), prod:+prodOf(b).toFixed(4),
      maintReq:LEVELS[b.level-1].maintain, growReq:LEVELS[b.level-1].grow
    })), edges, flows:lastFlows
  };
}

function resetGame(){ bases=Array.from({length:30},(_,i)=>initialBase(i)); commitments=new Map(); lastFlows=[]; gameRevision++; io.emit('state',publicState()); }

// --- Math generator ---
function randInt(a,b){ return Math.floor(Math.random()*(b-a+1))+a; }
function problem(type,band){
  band=Math.max(1,Math.min(6,band||2));
  let text='',answer='',choices=null;
  if(type==='CALC'){
    if(band<=1){ const a=randInt(2,12),b=randInt(1,Math.min(a,9)); text=`${a} + ${b} = ?`; answer=String(a+b); }
    else if(band<=3){ const op=Math.random()<.55?'×':'+'; if(op==='×'){const a=randInt(2,12),b=randInt(2,9);text=`${a} × ${b} = ?`;answer=String(a*b);}else{const a=randInt(20,199),b=randInt(10,99);text=`${a} + ${b} = ?`;answer=String(a+b);} }
    else { const a=randInt(12,48),b=randInt(2,9); text=`${a} × ${b} = ?`; answer=String(a*b); }
  } else if(type==='HOLE'){
    const x=randInt(2,12),a=band<4?randInt(2,9):randInt(3,15); const c=a*x; text=`${a} × □ = ${c}`; answer=String(x);
  } else if(type==='COMP'){
    let a=randInt(3,30),b=randInt(3,30); if(Math.random()<.2)b=a; text=`${a}  □  ${b}`; answer=a<b?'<':a>b?'>':'='; choices=['<','=','>'];
  } else if(type==='RULE'){
    const k=randInt(2,5),plus=randInt(0,5),x=randInt(3,9); text=`규칙: ×${k}${plus?` + ${plus}`:''}   |   ${x} → ?`; answer=String(x*k+plus);
  } else {
    const a=randInt(8,30),b=randInt(2,6),c=randInt(2,8); text=band<3?`${a} + ${b} × ${c} = ?`:`(${a} - ${b}) + ${c} × 2 = ?`; answer=String(band<3?a+b*c:(a-b)+c*2);
  }
  return {id:Math.random().toString(36).slice(2),type,band,text,answer,choices};
}

const players=new Map();
io.on('connection', socket=>{
  players.set(socket.id,{team:'spectator',bands:{CALC:2,HOLE:2,COMP:2,RULE:2,MIX:2},pending:null,session:null});
  socket.emit('state',publicState());
  socket.on('joinTeam',team=>{ if(['blue','red','spectator'].includes(team)) players.get(socket.id).team=team; socket.emit('joined',{team}); });
  socket.on('startSession',baseId=>{
    const p=players.get(socket.id), b=bases[baseId];
    if(!p||!b||!['blue','red'].includes(p.team)) return;
    p.session={baseId,correct:0,total:0,targetControl:b.control};
    const pr=problem(b.problemType,p.bands[b.problemType]); p.pending=pr; socket.emit('problem',{...pr,answer:undefined,baseId});
  });
  socket.on('answer',raw=>{
    const p=players.get(socket.id); if(!p||!p.pending||!p.session) return;
    const ok=String(raw).trim()===String(p.pending.answer).trim();
    p.session.total++; if(ok)p.session.correct++;
    const b=bases[p.session.baseId], type=b?b.problemType:p.pending.type;
    socket.emit('answerResult',{ok,correct:p.session.correct,total:p.session.total});
    if(p.session.total>=5){
      const result=applyContribution(p.session.baseId,p.team,p.session.correct);
      if(p.session.correct>=4) p.bands[type]=Math.min(6,p.bands[type]+1); else if(p.session.correct<=2) p.bands[type]=Math.max(1,p.bands[type]-1);
      socket.emit('sessionComplete',{correct:p.session.correct,total:5,...result,band:p.bands[type]});
      p.pending=null;p.session=null; io.emit('state',publicState());
    } else {
      const pr=problem(type,p.bands[type]); p.pending=pr; socket.emit('problem',{...pr,answer:undefined,baseId:p.session.baseId});
    }
  });
  socket.on('requestState',()=>socket.emit('state',publicState()));
  socket.on('resetDemo',()=>resetGame());
  socket.on('disconnect',()=>players.delete(socket.id));
});

setInterval(()=>{ militaryTick(); io.emit('state',publicState()); },TICK_MS);
server.listen(PORT,()=>console.log(`Ilsan Math Territory listening on ${PORT}`));
