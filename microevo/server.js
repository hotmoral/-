"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, "public");
const WORLD = { w: 8400, h: 8400 };
const TICK_HZ = 30;
const SNAP_HZ = 10;
const MAX_PLAYERS = 100;

const players = new Map();
const streams = new Map();
const mobs = [];
const items = [];
const TRAITS = ["attack", "speed", "armor"];

const rand=(a,b)=>a+Math.random()*(b-a);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const sqr=v=>v*v;
const d2=(a,b)=>sqr(a.x-b.x)+sqr(a.y-b.y);
const mag=(x,y)=>Math.hypot(x,y)||1;

function visualRadius(mass){ return 13 + Math.log2(1 + Math.max(1,mass)/8) * 7.2; }
function evolutionTier(mass){ return Math.max(0,Math.floor(Math.log2(Math.max(1,mass)/12))); }
function armorReduction(armor){ return Math.min(.62,1-Math.exp(-Math.max(0,armor)/18)); }
function speedBonus(speed){ return Math.log2(1+Math.max(0,speed))*18; }
function attackEatRatio(attack){ return Math.min(.90,.70+Math.log2(1+Math.max(0,attack))*.035); }
function randomPoint(margin=250){ return{x:rand(margin,WORLD.w-margin),y:rand(margin,WORLD.h-margin)}; }
function pointAround(base,minD,maxD){ const a=rand(0,Math.PI*2),d=rand(minD,maxD); return{x:clamp(base.x+Math.cos(a)*d,80,WORLD.w-80),y:clamp(base.y+Math.sin(a)*d,80,WORLD.h-80)}; }
function sanitizeName(v){ return String(v||"").replace(/[^\p{L}\p{N}_\- ]/gu,"").trim().slice(0,14); }

function makePlayer(id){
  const p=randomPoint(500);
  return{id,name:`세포-${id.slice(0,4)}`,x:p.x,y:p.y,vx:0,vy:0,ix:0,iy:0,mass:12,hp:100,maxHp:100,attack:0,speed:0,armor:0,eaten:0,kills:0,hue:Math.floor(rand(0,360)),alive:true,connected:false,lastSeen:Date.now(),bornAt:Date.now()};
}

let mobSeq=1;
function makeMobAt(x,y,mass,role="wild"){
  return{id:`m${mobSeq++}`,x,y,vx:rand(-18,18),vy:rand(-18,18),mass:Math.max(2,mass),role,kind:TRAITS[Math.floor(Math.random()*TRAITS.length)],species:Math.floor(rand(0,6)),phase:rand(0,Math.PI*2),flee:0,targetId:null};
}
function spawnWild(){ const p=randomPoint(),expo=rand(0,7),mass=6*Math.pow(2,expo)*rand(.65,1.45); mobs.push(makeMobAt(p.x,p.y,mass,"wild")); }
function spawnAdaptivePrey(player){ const p=pointAround(player,420,1100); mobs.push(makeMobAt(p.x,p.y,Math.max(2,player.mass*rand(.12,.72)),"prey")); }
function spawnAdaptivePredator(player,apex=false){ const p=pointAround(player,700,1250),mass=player.mass*rand(apex?2.2:1.35,apex?3.4:2.15),m=makeMobAt(p.x,p.y,mass,apex?"apex":"predator"); m.targetId=player.id; mobs.push(m); }
let itemSeq=1;
function makeItemNear(base=null){ const p=base?pointAround(base,260,1000):randomPoint(),r=Math.random(),kind=r<.28?"attack":r<.56?"speed":r<.84?"armor":r<.94?"heal":"mutation"; return{id:`i${itemSeq++}`,x:p.x,y:p.y,kind}; }
for(let i=0;i<150;i++)spawnWild();
for(let i=0;i<70;i++)items.push(makeItemNear());

function json(res,status,obj){ const data=JSON.stringify(obj); res.writeHead(status,{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"}); res.end(data); }
function readJson(req){
  return new Promise((resolve,reject)=>{ let raw=""; req.on("data",c=>{raw+=c;if(raw.length>32768){reject(new Error("too large"));req.destroy();}}); req.on("end",()=>{try{resolve(raw?JSON.parse(raw):{});}catch(e){reject(e);}}); req.on("error",reject); });
}
function mime(file){ const ext=path.extname(file).toLowerCase(); return({".html":"text/html; charset=utf-8",".js":"application/javascript; charset=utf-8",".webmanifest":"application/manifest+json; charset=utf-8",".png":"image/png",".css":"text/css; charset=utf-8",".svg":"image/svg+xml"})[ext]||"application/octet-stream"; }
function serveStatic(req,res){
  let pathname;
  try{pathname=decodeURIComponent(new URL(req.url,"http://localhost").pathname);}catch{return json(res,400,{error:"bad url"});}
  if(pathname==="/")pathname="/index.html";
  const file=path.resolve(PUBLIC_DIR,"."+pathname);
  if(!file.startsWith(PUBLIC_DIR+path.sep))return json(res,403,{error:"forbidden"});
  fs.stat(file,(err,st)=>{
    if(err||!st.isFile())return json(res,404,{error:"not found"});
    res.writeHead(200,{"Content-Type":mime(file),"Cache-Control":process.env.NODE_ENV==="production"?"public, max-age=3600":"no-store"});
    fs.createReadStream(file).pipe(res);
  });
}

const server=http.createServer(async(req,res)=>{
  const u=new URL(req.url,"http://localhost");
  try{
    if(req.method==="GET"&&u.pathname==="/health")return json(res,200,{ok:true,players:players.size,connected:streams.size,mobs:mobs.length,items:items.length,world:WORLD});
    if(req.method==="GET"&&u.pathname==="/events"){
      const id=u.searchParams.get("id"),p=players.get(id);
      if(!p)return json(res,404,{error:"unknown player"});
      const old=streams.get(id); if(old){try{old.end();}catch{}}
      res.writeHead(200,{"Content-Type":"text/event-stream","Cache-Control":"no-cache, no-transform","Connection":"keep-alive","X-Accel-Buffering":"no"});
      res.write("retry: 1500\n\n");
      streams.set(id,res);p.connected=true;p.lastSeen=Date.now();
      req.on("close",()=>{if(streams.get(id)===res)streams.delete(id);const q=players.get(id);if(q){q.connected=false;q.lastSeen=Date.now();}});
      return;
    }
    if(req.method==="POST"&&u.pathname==="/api/join"){
      const body=await readJson(req); let p=null;
      if(body.resumeId&&players.has(body.resumeId))p=players.get(body.resumeId);
      if(!p){
        if(players.size>=MAX_PLAYERS)return json(res,503,{error:"full"});
        const id=crypto.randomUUID();p=makePlayer(id);players.set(id,p);
      }
      const nm=sanitizeName(body.name);if(nm)p.name=nm;p.lastSeen=Date.now();
      return json(res,200,{id:p.id,world:WORLD});
    }
    if(req.method==="POST"&&u.pathname==="/api/input"){
      const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});
      let x=Number(b.x)||0,y=Number(b.y)||0,l=Math.hypot(x,y);if(l>1){x/=l;y/=l;}p.ix=clamp(x,-1,1);p.iy=clamp(y,-1,1);p.lastSeen=Date.now();return json(res,200,{ok:true});
    }
    if(req.method==="POST"&&u.pathname==="/api/name"){
      const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});const s=sanitizeName(b.name);if(s)p.name=s;p.lastSeen=Date.now();return json(res,200,{ok:true});
    }
    if(req.method==="POST"&&u.pathname==="/api/respawn"){
      const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});
      if(!p.alive){const q=randomPoint(500);Object.assign(p,{x:q.x,y:q.y,vx:0,vy:0,ix:0,iy:0,mass:12,hp:100,maxHp:100,attack:0,speed:0,armor:0,eaten:0,alive:true,bornAt:Date.now()});}p.lastSeen=Date.now();return json(res,200,{ok:true});
    }
    if(process.env.MICROEVO_TEST==="1"&&req.method==="POST"&&u.pathname==="/api/test/setMass"){
      const b=await readJson(req),p=players.get(b.id);if(!p)return json(res,404,{error:"unknown"});
      p.mass=Math.max(1,Number(b.mass)||1);p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=p.maxHp;p.lastSeen=Date.now();return json(res,200,{ok:true,mass:p.mass});
    }
  }catch(e){return json(res,400,{error:"bad request"});}
  if(req.method==="GET")return serveStatic(req,res);
  return json(res,404,{error:"not found"});
});

function killPlayer(victim,killer=null){ if(!victim.alive)return;victim.alive=false;victim.hp=0;victim.vx=victim.vy=victim.ix=victim.iy=0;if(killer){killer.kills++;killer.mass+=Math.max(2,victim.mass*.12);} }
function updatePlayer(p,dt){
  if(!p.alive)return;
  const r=visualRadius(p.mass),tier=evolutionTier(p.mass),baseSpeed=Math.max(82,166-tier*5),maxSpeed=baseSpeed+speedBonus(p.speed),tvx=p.ix*maxSpeed,tvy=p.iy*maxSpeed;
  p.vx+=(tvx-p.vx)*Math.min(1,dt*8.5);p.vy+=(tvy-p.vy)*Math.min(1,dt*8.5);if(Math.abs(p.ix)+Math.abs(p.iy)<.05){p.vx*=Math.pow(.12,dt);p.vy*=Math.pow(.12,dt);}p.x=clamp(p.x+p.vx*dt,r,WORLD.w-r);p.y=clamp(p.y+p.vy*dt,r,WORLD.h-r);
  for(let i=mobs.length-1;i>=0;i--){const m=mobs[i],rr=r+visualRadius(m.mass)*.88;if(d2(p,m)>rr*rr)continue;const ratio=attackEatRatio(p.attack);if(m.mass<p.mass*ratio){p.mass+=Math.max(1.2,m.mass*.105);p.eaten++;p[m.kind]+=1;p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+5+Math.log2(1+m.mass));mobs.splice(i,1);continue;}if(m.mass>p.mass*1.12){const danger=Math.min(3.5,m.mass/p.mass),damage=(9+danger*5)*(1-armorReduction(p.armor));p.hp-=damage*dt*2.2;if(p.hp<=0){killPlayer(p);return;}}}
  for(let i=items.length-1;i>=0;i--){const it=items[i],rr=r+20;if(d2(p,it)>rr*rr)continue;if(it.kind==="heal")p.hp=Math.min(p.maxHp,p.hp+p.maxHp*.32);else if(it.kind==="mutation"){p.attack++;p.speed++;p.armor++;p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+14);}else{p[it.kind]++;if(it.kind==="armor"){p.maxHp=100+p.armor*8+Math.log2(1+p.mass)*7;p.hp=Math.min(p.maxHp,p.hp+9);}}items.splice(i,1);}
  for(const other of players.values()){if(other.id===p.id||!other.alive)continue;const rr=r+visualRadius(other.mass);if(d2(p,other)>rr*rr)continue;if(other.mass<p.mass*attackEatRatio(p.attack)*.90)killPlayer(other,p);}
}
function nearestAlivePlayer(m){if(m.targetId){const t=players.get(m.targetId);if(t&&t.alive)return[t,d2(m,t)];}let best=null,bestD=Infinity;for(const p of players.values()){if(!p.alive)continue;const dd=d2(m,p);if(dd<bestD){best=p;bestD=dd;}}return[best,bestD];}
function updateMobs(dt){for(const m of mobs){const mr=visualRadius(m.mass)*.88,[p,dd]=nearestAlivePlayer(m);let ax=0,ay=0;if(p){const dx=p.x-m.x,dy=p.y-m.y,d=Math.sqrt(dd)||1,detect=250+Math.min(620,visualRadius(m.mass)*12);if(d<detect){if(p.mass>m.mass*1.10){ax-=dx/d*150;ay-=dy/d*150;m.flee=.7;}else if(m.mass>p.mass*1.14){ax+=dx/d*(m.role==="apex"?105:76);ay+=dy/d*(m.role==="apex"?105:76);}}}if(m.flee>0)m.flee-=dt;else{m.phase+=dt*(.55+(m.species+1)*.06);ax+=Math.cos(m.phase*1.7)*17;ay+=Math.sin(m.phase*1.31)*17;}m.vx+=ax*dt;m.vy+=ay*dt;const boost=m.role==="apex"?36:m.role==="predator"?22:0,maxSpeed=48+Math.min(105,Math.log2(1+m.mass)*12)+boost+(m.flee>0?62:0),l=mag(m.vx,m.vy);if(l>maxSpeed){m.vx=m.vx/l*maxSpeed;m.vy=m.vy/l*maxSpeed;}m.vx*=Math.pow(.78,dt);m.vy*=Math.pow(.78,dt);m.x+=m.vx*dt;m.y+=m.vy*dt;if(m.x<mr||m.x>WORLD.w-mr){m.vx*=-1;m.x=clamp(m.x,mr,WORLD.w-mr);}if(m.y<mr||m.y>WORLD.h-mr){m.vy*=-1;m.y=clamp(m.y,mr,WORLD.h-mr);}}}

setInterval(()=>{
  const alive=[...players.values()].filter(p=>p.alive&&Date.now()-p.lastSeen<60000);
  for(const p of alive){let predators=0,prey=0,pickups=0;for(const m of mobs){const dd=d2(p,m);if(dd<sqr(1450)&&m.mass>p.mass*1.22)predators++;if(dd<sqr(1150)&&m.mass<p.mass*.78)prey++;}for(const it of items)if(d2(p,it)<sqr(1100))pickups++;if(predators<1)spawnAdaptivePredator(p,false);if(prey<5)for(let i=0;i<Math.min(3,5-prey);i++)spawnAdaptivePrey(p);if(pickups<2)items.push(makeItemNear(p));}
  if(alive.length){const largest=alive.reduce((a,b)=>a.mass>b.mass?a:b),apexNearby=mobs.some(m=>m.role==="apex"&&m.mass>largest.mass*1.8&&d2(m,largest)<sqr(2500));if(!apexNearby)spawnAdaptivePredator(largest,true);}
  const softMax=190+Math.min(360,alive.length*8);while(mobs.length<Math.min(170,softMax))spawnWild();if(mobs.length>softMax){for(let i=mobs.length-1;i>=0&&mobs.length>softMax;i--)if(mobs[i].role==="wild"||mobs[i].role==="prey")mobs.splice(i,1);}
  const itemTarget=70+Math.min(120,alive.length*2);while(items.length<itemTarget)items.push(makeItemNear());if(items.length>itemTarget+35)items.splice(0,items.length-(itemTarget+35));
},1500);

let last=Date.now();setInterval(()=>{const now=Date.now(),dt=Math.min(.05,(now-last)/1000);last=now;for(const p of players.values())updatePlayer(p,dt);updateMobs(dt);},1000/TICK_HZ);

setInterval(()=>{
  const payload=JSON.stringify({t:Date.now(),players:[...players.values()].filter(p=>Date.now()-p.lastSeen<60000).map(p=>({id:p.id,name:p.name,x:p.x,y:p.y,vx:p.vx,vy:p.vy,mass:p.mass,hp:p.hp,maxHp:p.maxHp,attack:p.attack,speed:p.speed,armor:p.armor,eaten:p.eaten,kills:p.kills,hue:p.hue,alive:p.alive,tier:evolutionTier(p.mass)})),mobs:mobs.map(m=>({id:m.id,x:m.x,y:m.y,vx:m.vx,vy:m.vy,mass:m.mass,role:m.role,kind:m.kind,species:m.species,flee:m.flee>0})),items:items.map(i=>({id:i.id,x:i.x,y:i.y,kind:i.kind}))});
  for(const [id,res] of streams){try{res.write(`data: ${payload}\n\n`);}catch{streams.delete(id);}}
},1000/SNAP_HZ);

setInterval(()=>{const now=Date.now();for(const [id,p] of players){if(!p.connected&&now-p.lastSeen>60000){players.delete(id);const s=streams.get(id);if(s){try{s.end();}catch{}streams.delete(id);}}}for(const res of streams.values()){try{res.write(`: ping ${now}\n\n`);}catch{}}},15000);

server.listen(PORT,"0.0.0.0",()=>console.log(`MicroEvo Online v3.1 on http://0.0.0.0:${PORT}`));
