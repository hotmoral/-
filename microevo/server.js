"use strict";

const http=require("http");
const fs=require("fs");
const path=require("path");
const crypto=require("crypto");

const PORT=process.env.PORT||3000;
const PUBLIC_DIR=path.join(__dirname,"public");
const WORLD={w:8400,h:8400};
const TICK_HZ=30;
const SNAP_HZ=12;
const MAX_PLAYERS=100;
const LOCAL_RADIUS=1700;
const ITEM_RADIUS=1450;
const PREDATOR_TARGET=2;

const players=new Map();
const streams=new Map();
const mobs=[];
const items=[];
const TRAITS=["attack","speed","armor"];

const rand=(a,b)=>a+Math.random()*(b-a);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const sqr=v=>v*v;
const d2=(a,b)=>sqr(a.x-b.x)+sqr(a.y-b.y);
const mag=(x,y)=>Math.hypot(x,y)||1;
const nowMs=()=>Date.now();

function visualRadius(mass){return 13+Math.log2(1+Math.max(1,mass)/8)*7.2}
function evolutionTier(mass){return Math.max(0,Math.floor(Math.log2(Math.max(1,mass)/12)))}
function armorReduction(armor){return Math.min(.62,1-Math.exp(-Math.max(0,armor)/18))}
function speedBonus(speed){return Math.log2(1+Math.max(0,speed))*18}
function attackEatRatio(attack){return Math.min(.90,.70+Math.log2(1+Math.max(0,attack))*.035)}
function randomPoint(m=250){return{x:rand(m,WORLD.w-m),y:rand(m,WORLD.h-m)}}
function pointAround(base,minD,maxD){const a=rand(0,Math.PI*2),d=rand(minD,maxD);return{x:clamp(base.x+Math.cos(a)*d,80,WORLD.w-80),y:clamp(base.y+Math.sin(a)*d,80,WORLD.h-80)}}
function sanitizeName(v){return String(v||"").replace(/[^\p{L}\p{N}_\- ]/gu,"").trim().slice(0,14)}
function distPointSegmentSq(px,py,ax,ay,bx,by){const vx=bx-ax,vy=by-ay,wx=px-ax,wy=py-ay,c1=wx*vx+wy*vy;if(c1<=0)return sqr(px-ax)+sqr(py-ay);const c2=vx*vx+vy*vy;if(c2<=c1)return sqr(px-bx)+sqr(py-by);const t=c1/c2,qx=ax+t*vx,qy=ay+t*vy;return sqr(px-qx)+sqr(py-qy)}

function makePlayer(id){const p=randomPoint(500);return{id,name:`세포-${id.slice(0,4)}`,x:p.x,y:p.y,prevX:p.x,prevY:p.y,vx:0,vy:0,ix:0,iy:0,mass:12,hp:100,maxHp:100,attack:0,speed:0,armor:0,eaten:0,kills:0,hue:Math.floor(rand(0,360)),alive:true,connected:false,lastSeen:nowMs(),nextPredatorAt:0}}

let mobSeq=1,itemSeq=1;
const GRAZER_TYPES=["amoeba","ciliate","spore","colony","tendril","glider"];
const PREDATOR_TYPES=["hunter","stinger","leech"];
function randomGrazerType(){return GRAZER_TYPES[(Math.random()*GRAZER_TYPES.length)|0]}
function randomPredatorType(){return PREDATOR_TYPES[(Math.random()*PREDATOR_TYPES.length)|0]}
function makeMobAt(x,y,mass,role="wild",targetId=null,archetype=null){return{id:`m${mobSeq++}`,x,y,prevX:x,prevY:y,vx:rand(-18,18),vy:rand(-18,18),mass:Math.max(2,mass),role,targetId,archetype:archetype||role,kind:TRAITS[(Math.random()*TRAITS.length)|0],species:(rand(0,9)|0),phase:rand(0,Math.PI*2),flee:0,bornAt:nowMs()}}
function spawnWild(){const p=randomPoint(),mass=rand(3,58)*rand(.68,1.26);mobs.push(makeMobAt(p.x,p.y,mass,"wild",null,randomGrazerType()))}
function spawnPrey(p){const q=pointAround(p,220,980),tier=evolutionTier(p.mass),arch=(tier>=6&&Math.random()<.28)?"colony":(tier>=3&&Math.random()<.38)?"tendril":randomGrazerType();mobs.push(makeMobAt(q.x,q.y,Math.max(2,p.mass*rand(.14,.68)),"prey",p.id,arch))}
function spawnPredator(p){const q=pointAround(p,760,1200),tier=evolutionTier(p.mass),mult=tier>=7?rand(1.18,1.42):rand(1.30,1.58);mobs.push(makeMobAt(q.x,q.y,p.mass*mult,"predator",p.id,randomPredatorType()))}
function spawnApex(p){const q=pointAround(p,1450,2100);mobs.push(makeMobAt(q.x,q.y,p.mass*rand(1.85,2.30),"apex",p.id,"apex"))}
function makeItemNear(base=null){const p=base?pointAround(base,220,900):randomPoint();const r=Math.random(),kind=r<.28?"attack":r<.56?"speed":r<.84?"armor":r<.94?"heal":"mutation";return{id:`i${itemSeq++}`,x:p.x,y:p.y,kind}}
for(let i=0;i<72;i++)spawnWild();
for(let i=0;i<34;i++)items.push(makeItemNear());

function json(res,status,obj){res.writeHead(status,{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"});res.end(JSON.stringify(obj))}
function noContent(res){res.writeHead(204,{"Cache-Control":"no-store"});res.end()}
function readJson(req){return new Promise((resolve,reject)=>{let raw="";req.on("data",c=>{raw+=c;if(raw.length>32768){reject(new Error("too large"));req.destroy()}});req.on("end",()=>{try{resolve(raw?JSON.parse(raw):{})}catch(e){reject(e)}});req.on("error",reject)})}
function mime(file){return({".html":"text/html; charset=utf-8",".js":"application/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".svg":"image/svg+xml",".webmanifest":"application/manifest+json; charset=utf-8"}[path.extname(file).toLowerCase()]||"application/octet-stream")}
function serveStatic(req,res){let pn;try{pn=decodeURIComponent(new URL(req.url,"http://localhost").pathname)}catch{return json(res,400,{error:"bad url"})}if(pn==="/")pn="/index.html";const file=path.resolve(PUBLIC_DIR,"."+pn);if(!file.startsWith(PUBLIC_DIR+path.sep))return json(res,403,{error:"forbidden"});fs.stat(file,(err,st)=>{if(err||!st.isFile())return json(res,404,{error:"not found"});res.writeHead(200,{"Content-Type":mime(file),"Cache-Control":"no-store, max-age=0","Pragma":"no-cache"});fs.createReadStream(file).pipe(res)})}

function mobEdibleBy(p,m){return m.mass<p.mass*attackEatRatio(p.attack)}
function applyConsume(p,m,index){p.mass+=Math.max(1.2,m.mass*.105);p.eaten++;p[m.kind]=(p[m.kind]||0)+1;p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+5+Math.log2(1+m.mass));if(index>=0)mobs.splice(index,1);return{mass:p.mass,eaten:p.eaten,kind:m.kind,mobId:m.id}}
function killPlayer(victim,killer=null){if(!victim.alive)return;victim.alive=false;victim.hp=0;victim.vx=victim.vy=victim.ix=victim.iy=0;if(killer){killer.kills++;killer.mass+=Math.max(2,victim.mass*.12)}}

const server=http.createServer(async(req,res)=>{
  const u=new URL(req.url,"http://localhost");
  try{
    if(req.method==="GET"&&u.pathname==="/health"){const now=nowMs(),active=[...players.values()].filter(p=>p.alive&&now-p.lastSeen<60000);return json(res,200,{ok:true,version:9,players:players.size,connected:streams.size,mobs:mobs.length,items:items.length,predators:mobs.filter(m=>m.role==="predator").length,apex:mobs.filter(m=>m.role==="apex").length,active:active.length,world:WORLD})}
    if(req.method==="GET"&&u.pathname==="/events"){const id=u.searchParams.get("id"),p=players.get(id);if(!p)return json(res,404,{error:"unknown player"});const old=streams.get(id);if(old){try{old.end()}catch{}}res.writeHead(200,{"Content-Type":"text/event-stream","Cache-Control":"no-cache, no-transform","Connection":"keep-alive","X-Accel-Buffering":"no","Content-Encoding":"identity"});res.write("retry: 1000\n\n");streams.set(id,res);p.connected=true;p.lastSeen=nowMs();req.on("close",()=>{if(streams.get(id)===res)streams.delete(id);const q=players.get(id);if(q){q.connected=false;q.lastSeen=nowMs()}});return}
    if(req.method==="POST"&&u.pathname==="/api/join"){const b=await readJson(req);let p=null;if(b.resumeId&&players.has(b.resumeId))p=players.get(b.resumeId);if(!p){if(players.size>=MAX_PLAYERS)return json(res,503,{error:"full"});const id=crypto.randomUUID();p=makePlayer(id);players.set(id,p)}const nm=sanitizeName(b.name);if(nm)p.name=nm;p.lastSeen=nowMs();return json(res,200,{id:p.id,world:WORLD,snapHz:SNAP_HZ})}
    if(req.method==="POST"&&u.pathname==="/api/input"){const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});let x=Number(b.x)||0,y=Number(b.y)||0,l=Math.hypot(x,y);if(l>1){x/=l;y/=l}p.ix=clamp(x,-1,1);p.iy=clamp(y,-1,1);p.lastSeen=nowMs();return noContent(res)}
    if(req.method==="POST"&&u.pathname==="/api/eat"){const b=await readJson(req),p=players.get(b.id);if(!p||!p.alive)return json(res,404,{ok:false});const idx=mobs.findIndex(m=>m.id===b.mobId);if(idx<0)return json(res,200,{ok:true,already:true});const m=mobs[idx];if(!mobEdibleBy(p,m))return json(res,200,{ok:false,reason:"too_big"});const cx=Number(b.x),cy=Number(b.y);if(!Number.isFinite(cx)||!Number.isFinite(cy))return json(res,200,{ok:false,reason:"bad_pos"});const drift=Math.hypot(cx-p.x,cy-p.y);if(drift>180)return json(res,200,{ok:false,reason:"drift"});const rr=visualRadius(p.mass)+visualRadius(m.mass)*.88+22+Math.min(28,Math.hypot(p.vx-m.vx,p.vy-m.vy)*.12);const ok=d2({x:cx,y:cy},m)<=rr*rr||distPointSegmentSq(m.x,m.y,p.prevX,p.prevY,p.x,p.y)<=rr*rr;if(!ok)return json(res,200,{ok:false,reason:"miss"});return json(res,200,{ok:true,...applyConsume(p,m,idx)})}
    if(req.method==="POST"&&u.pathname==="/api/name"){const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});const s=sanitizeName(b.name);if(s)p.name=s;p.lastSeen=nowMs();return noContent(res)}
    if(req.method==="POST"&&u.pathname==="/api/respawn"){const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});if(!p.alive){const q=randomPoint(500);Object.assign(p,{x:q.x,y:q.y,prevX:q.x,prevY:q.y,vx:0,vy:0,ix:0,iy:0,mass:12,hp:100,maxHp:100,attack:0,speed:0,armor:0,eaten:0,alive:true,nextPredatorAt:0})}p.lastSeen=nowMs();return noContent(res)}
  }catch{return json(res,400,{error:"bad request"})}
  if(req.method==="GET")return serveStatic(req,res);return json(res,404,{error:"not found"})
});

function updatePlayer(p,dt){
  if(!p.alive)return;p.prevX=p.x;p.prevY=p.y;
  const r=visualRadius(p.mass),tier=evolutionTier(p.mass),maxSpeed=Math.max(82,166-tier*5)+speedBonus(p.speed),tvx=p.ix*maxSpeed,tvy=p.iy*maxSpeed;
  p.vx+=(tvx-p.vx)*Math.min(1,dt*8.5);p.vy+=(tvy-p.vy)*Math.min(1,dt*8.5);if(Math.abs(p.ix)+Math.abs(p.iy)<.05){p.vx*=Math.pow(.12,dt);p.vy*=Math.pow(.12,dt)}p.x=clamp(p.x+p.vx*dt,r,WORLD.w-r);p.y=clamp(p.y+p.vy*dt,r,WORLD.h-r);
  for(let i=mobs.length-1;i>=0;i--){const m=mobs[i],base=r+visualRadius(m.mass)*.88,assist=mobEdibleBy(p,m)?Math.min(24,8+Math.hypot(p.vx-m.vx,p.vy-m.vy)*.10):0,rr=base+assist;const hit=d2(p,m)<=rr*rr||distPointSegmentSq(m.x,m.y,p.prevX,p.prevY,p.x,p.y)<=rr*rr;if(!hit)continue;if(mobEdibleBy(p,m)){applyConsume(p,m,i);continue}if((m.role==="predator"||m.role==="apex")&&m.mass>p.mass*1.10){const danger=Math.min(3,m.mass/p.mass),damage=(7+danger*4)*(1-armorReduction(p.armor));p.hp-=damage*dt*1.75;if(p.hp<=0){killPlayer(p);return}}}
  for(let i=items.length-1;i>=0;i--){const it=items[i],rr=r+20;if(d2(p,it)>rr*rr)continue;if(it.kind==="heal")p.hp=Math.min(p.maxHp,p.hp+p.maxHp*.32);else if(it.kind==="mutation"){p.attack++;p.speed++;p.armor++;p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+14)}else{p[it.kind]++;if(it.kind==="armor"){p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+9)}}items.splice(i,1)}
  for(const other of players.values()){if(other.id===p.id||!other.alive)continue;const rr=r+visualRadius(other.mass);if(d2(p,other)>rr*rr)continue;if(other.mass<p.mass*attackEatRatio(p.attack)*.90)killPlayer(other,p)}
}

function nearestAlivePlayer(m){if(m.targetId){const t=players.get(m.targetId);if(t&&t.alive&&nowMs()-t.lastSeen<60000)return[t,d2(m,t)]}let best=null,bestD=Infinity;for(const p of players.values()){if(!p.alive||nowMs()-p.lastSeen>=60000)continue;const dd=d2(m,p);if(dd<bestD){best=p;bestD=dd}}return[best,bestD]}
function updateMobs(dt){
  for(const m of mobs){m.prevX=m.x;m.prevY=m.y;const mr=visualRadius(m.mass)*.88,[p,dd]=nearestAlivePlayer(m);let ax=0,ay=0;if(p){const dx=p.x-m.x,dy=p.y-m.y,d=Math.sqrt(dd)||1;if((m.role==="wild"||m.role==="prey")&&d<560&&p.mass>m.mass*1.03){ax-=dx/d*150;ay-=dy/d*150;m.flee=.70}else if(m.role==="predator"&&d<1100&&m.mass>p.mass*1.05){ax+=dx/d*132;ay+=dy/d*132}else if(m.role==="apex"&&d<1350&&m.mass>p.mass*1.05){ax+=dx/d*160;ay+=dy/d*160}}
    if(m.flee>0)m.flee-=dt;else{m.phase+=dt*(.55+(m.species+1)*.06);ax+=Math.cos(m.phase*1.7)*14;ay+=Math.sin(m.phase*1.31)*14}m.vx+=ax*dt;m.vy+=ay*dt;const boost=m.role==="apex"?48:m.role==="predator"?38:0,maxSpeed=46+Math.min(92,Math.log2(1+m.mass)*10)+boost+(m.flee>0?42:0),l=mag(m.vx,m.vy);if(l>maxSpeed){m.vx=m.vx/l*maxSpeed;m.vy=m.vy/l*maxSpeed}m.vx*=Math.pow(.82,dt);m.vy*=Math.pow(.82,dt);m.x+=m.vx*dt;m.y+=m.vy*dt;if(m.x<mr||m.x>WORLD.w-mr){m.vx*=-1;m.x=clamp(m.x,mr,WORLD.w-mr)}if(m.y<mr||m.y>WORLD.h-mr){m.vy*=-1;m.y=clamp(m.y,mr,WORLD.h-mr)}}
}

function removeMobById(id){const i=mobs.findIndex(m=>m.id===id);if(i>=0)mobs.splice(i,1)}
function retireIfOutgrown(m,p){if(!p||!(m.role==="predator"||m.role==="apex"))return false;const edible=mobEdibleBy(p,m);if(edible){m.role="prey";m.targetId=p.id;m.flee=.8;return true}return false}

setInterval(()=>{
  const now=nowMs(),alive=[...players.values()].filter(p=>p.alive&&now-p.lastSeen<60000),activeIds=new Set(alive.map(p=>p.id));
  for(const m of mobs){if((m.role==="predator"||m.role==="apex")&&m.targetId){const t=players.get(m.targetId);if(!t||!activeIds.has(m.targetId)){m.role="wild";m.targetId=null}else retireIfOutgrown(m,t)}}
  for(const p of alive){
    const threats=mobs.filter(m=>m.role==="predator"&&m.targetId===p.id&&!mobEdibleBy(p,m));
    if(threats.length<PREDATOR_TARGET&&now>=p.nextPredatorAt){spawnPredator(p);p.nextPredatorAt=now+2800+rand(0,1800)}
    if(threats.length>PREDATOR_TARGET){for(let i=PREDATOR_TARGET;i<threats.length;i++){threats[i].role="wild";threats[i].targetId=null}}
    let prey=0,pickups=0;for(const m of mobs)if((m.role==="prey"||m.role==="wild")&&mobEdibleBy(p,m)&&d2(m,p)<sqr(1150))prey++;for(const it of items)if(d2(it,p)<sqr(1050))pickups++;for(let i=0;i<Math.min(5,Math.max(0,11-prey));i++)spawnPrey(p);while(pickups<3){items.push(makeItemNear(p));pickups++}
  }
  const activeApex=mobs.filter(m=>m.role==="apex");
  if(alive.length){const largest=alive.reduce((a,b)=>a.mass>b.mass?a:b);let apex=activeApex[0];if(apex&&mobEdibleBy(largest,apex)){apex.role="prey";apex.targetId=largest.id;apex=null}if(!apex)spawnApex(largest);for(let i=1;i<activeApex.length;i++){activeApex[i].role="wild";activeApex[i].targetId=null}}
  else for(const a of activeApex){a.role="wild";a.targetId=null}
  if(alive.length){for(let i=mobs.length-1;i>=0;i--){const m=mobs[i];if(m.role!=="prey"||PREDATOR_TYPES.includes(m.archetype)||m.archetype==="apex")continue;let near=false;for(const p of alive){if(d2(m,p)<sqr(2200)){near=true;break}}if(!near)mobs.splice(i,1)}}
  const wildCount=mobs.filter(m=>m.role==="wild"&&!PREDATOR_TYPES.includes(m.archetype)&&m.archetype!=="apex").length;for(let i=wildCount;i<72;i++)spawnWild();const itemTarget=34+Math.min(80,alive.length*5);while(items.length<itemTarget)items.push(makeItemNear());if(items.length>itemTarget+20)items.splice(0,items.length-(itemTarget+20));
},900);

let last=nowMs();setInterval(()=>{const now=nowMs(),dt=Math.min(.05,(now-last)/1000);last=now;for(const p of players.values())updatePlayer(p,dt);updateMobs(dt)},1000/TICK_HZ);
function playerDto(p){return{id:p.id,name:p.name,x:p.x,y:p.y,vx:p.vx,vy:p.vy,mass:p.mass,hp:p.hp,maxHp:p.maxHp,attack:p.attack,speed:p.speed,armor:p.armor,eaten:p.eaten,kills:p.kills,hue:p.hue,alive:p.alive,tier:evolutionTier(p.mass)}}
function mobDto(m){return{id:m.id,x:m.x,y:m.y,vx:m.vx,vy:m.vy,mass:m.mass,role:m.role,archetype:m.archetype,kind:m.kind,species:m.species,flee:m.flee>0,targetId:m.targetId}}
setInterval(()=>{const now=nowMs(),activePlayers=[...players.values()].filter(p=>now-p.lastSeen<60000),playersLite=activePlayers.map(playerDto);for(const [id,res] of streams){const p=players.get(id);if(!p)continue;const localMobs=[],radarPredators=[];for(const m of mobs){const dd=d2(p,m);if(dd<sqr(LOCAL_RADIUS))localMobs.push(mobDto(m));if((m.role==="predator"||m.role==="apex")&&radarPredators.length<16)radarPredators.push({id:m.id,x:m.x,y:m.y,mass:m.mass,role:m.role,targetId:m.targetId})}const localItems=[];for(const it of items)if(d2(p,it)<sqr(ITEM_RADIUS))localItems.push(it);const payload=JSON.stringify({t:now,players:playersLite,mobs:localMobs,items:localItems,predators:radarPredators,snapHz:SNAP_HZ,version:9});try{res.write(`data: ${payload}\n\n`)}catch{streams.delete(id)}}},1000/SNAP_HZ);
setInterval(()=>{const now=nowMs();for(const [id,p] of players)if(!p.connected&&now-p.lastSeen>60000){players.delete(id);const s=streams.get(id);if(s){try{s.end()}catch{}streams.delete(id)}}for(const res of streams.values())try{res.write(`: ping ${now}\n\n`)}catch{}},15000);
server.listen(PORT,"0.0.0.0",()=>console.log(`MicroEvo v9 microbe server on 0.0.0.0:${PORT}`));