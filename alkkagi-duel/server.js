'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;
const PUBLIC = path.join(__dirname, 'public');
const rooms = new Map();
const BOARD = 1000;
const RADIUS = 31;
const ROOM_TTL = 1000 * 60 * 60 * 4;

function id(len = 7) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let out = '';
  for (let i = 0; i < len; i++) out += alphabet[crypto.randomInt(alphabet.length)];
  return out;
}
function token() { return crypto.randomBytes(18).toString('base64url'); }

function makeStones() {
  const stones = [];
  const top = [[380,170],[500,170],[620,170],[320,245],[440,245],[560,245],[680,245]];
  const bot = top.map(([x,y]) => [x, BOARD-y]);
  top.forEach(([x,y], i) => stones.push({ id:`W${i+1}`, owner:'white', x, y, alive:true }));
  bot.forEach(([x,y], i) => stones.push({ id:`B${i+1}`, owner:'black', x, y, alive:true }));
  return stones;
}

function newRoom() {
  const roomId = id();
  const blackToken = token();
  const room = {
    id: roomId,
    createdAt: Date.now(), lastActive: Date.now(),
    players: { black: blackToken, white: null },
    stones: makeStones(),
    turn: 'black', starter: 'black', phase: 'waiting', winner: null,
    shotSeq: 0, lastAnimation: null, locked: false, gameNo: 1,
    rematch: { black:false, white:false }
  };
  rooms.set(roomId, room);
  return { room, blackToken };
}

function roleFor(room, t) {
  if (!t) return 'spectator';
  if (t === room.players.black) return 'black';
  if (t === room.players.white) return 'white';
  return 'spectator';
}

function sanitize(room, after = -1) {
  return {
    id: room.id, phase: room.phase, turn: room.turn, winner: room.winner,
    shotSeq: room.shotSeq, gameNo: room.gameNo,
    players: { black: !!room.players.black, white: !!room.players.white },
    remaining: {
      black: room.stones.filter(s => s.alive && s.owner === 'black').length,
      white: room.stones.filter(s => s.alive && s.owner === 'white').length
    },
    stones: room.stones.map(s => ({id:s.id, owner:s.owner, x:Math.round(s.x*10)/10, y:Math.round(s.y*10)/10, alive:s.alive})),
    rematch: room.rematch,
    animation: room.shotSeq > after ? room.lastAnimation : null
  };
}

function json(res, status, body) {
  const data = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type':'application/json; charset=utf-8',
    'Cache-Control':'no-store',
    'Content-Length': Buffer.byteLength(data)
  });
  res.end(data);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', c => { raw += c; if (raw.length > 20000) reject(new Error('too large')); });
    req.on('end', () => {
      if (!raw) return resolve({});
      try { resolve(JSON.parse(raw)); } catch { reject(new Error('bad json')); }
    });
    req.on('error', reject);
  });
}

function collide(a, b, va, vb) {
  let dx = b.x - a.x, dy = b.y - a.y;
  let d2 = dx*dx + dy*dy;
  const min = RADIUS * 2;
  if (d2 >= min*min) return;
  let d = Math.sqrt(d2);
  if (d < 0.001) { dx = 0.01; dy = 0; d = 0.01; }
  const nx = dx/d, ny = dy/d;
  const overlap = min - d;
  a.x -= nx * overlap * 0.5; a.y -= ny * overlap * 0.5;
  b.x += nx * overlap * 0.5; b.y += ny * overlap * 0.5;
  const rel = (vb.vx - va.vx)*nx + (vb.vy - va.vy)*ny;
  if (rel >= 0) return;
  const e = 0.92;
  const impulse = -(1 + e) * rel / 2;
  va.vx -= impulse*nx; va.vy -= impulse*ny;
  vb.vx += impulse*nx; vb.vy += impulse*ny;
}

function simulate(room, stoneId, vx, vy) {
  const stones = room.stones;
  const moving = new Map();
  stones.forEach(s => moving.set(s.id, {vx:0, vy:0}));
  const shot = stones.find(s => s.id === stoneId && s.alive);
  moving.get(shot.id).vx = vx;
  moving.get(shot.id).vy = vy;
  const frames = [];
  const dt = 1/60;
  let settledTicks = 0;
  const startCounts = {
    black: stones.filter(s=>s.alive&&s.owner==='black').length,
    white: stones.filter(s=>s.alive&&s.owner==='white').length
  };

  for (let step=0; step<480; step++) {
    const live = stones.filter(s => s.alive);
    for (const s of live) {
      const v = moving.get(s.id);
      s.x += v.vx * dt; s.y += v.vy * dt;
    }
    for (let i=0; i<live.length; i++) for (let j=i+1; j<live.length; j++) {
      if (!live[i].alive || !live[j].alive) continue;
      collide(live[i], live[j], moving.get(live[i].id), moving.get(live[j].id));
    }
    for (const s of stones) {
      if (!s.alive) continue;
      if (s.x < 0 || s.x > BOARD || s.y < 0 || s.y > BOARD) {
        s.alive = false;
        const v = moving.get(s.id); v.vx = 0; v.vy = 0;
      }
    }
    let maxSpeed = 0;
    for (const s of stones) {
      if (!s.alive) continue;
      const v = moving.get(s.id);
      v.vx *= 0.986; v.vy *= 0.986;
      const sp = Math.hypot(v.vx, v.vy);
      if (sp < 7) { v.vx = 0; v.vy = 0; }
      maxSpeed = Math.max(maxSpeed, sp);
    }
    if (step % 3 === 0) {
      frames.push(stones.map(s => [s.id, Math.round(s.x*10)/10, Math.round(s.y*10)/10, s.alive?1:0]));
    }
    if (maxSpeed < 8) settledTicks++; else settledTicks = 0;
    if (settledTicks > 18) break;
  }

  for (const s of stones) {
    s.x = Math.max(-50, Math.min(1050, s.x));
    s.y = Math.max(-50, Math.min(1050, s.y));
  }
  const endCounts = {
    black: stones.filter(s=>s.alive&&s.owner==='black').length,
    white: stones.filter(s=>s.alive&&s.owner==='white').length
  };
  return {
    frames,
    durationMs: Math.max(220, frames.length * 50),
    fallen: { black: startCounts.black-endCounts.black, white: startCounts.white-endCounts.white }
  };
}

function evaluate(room) {
  const b = room.stones.filter(s => s.alive && s.owner==='black').length;
  const w = room.stones.filter(s => s.alive && s.owner==='white').length;
  if (b === 0 && w === 0) { room.winner = 'draw'; room.phase='finished'; }
  else if (b === 0) { room.winner='white'; room.phase='finished'; }
  else if (w === 0) { room.winner='black'; room.phase='finished'; }
}

function resetRoom(room) {
  room.stones = makeStones();
  room.starter = room.starter === 'black' ? 'white' : 'black';
  room.turn = room.starter;
  room.phase = room.players.white ? 'playing' : 'waiting';
  room.winner = null;
  room.shotSeq += 1;
  room.lastAnimation = null;
  room.rematch = {black:false, white:false};
  room.gameNo += 1;
}

function serveStatic(req, res, pathname) {
  let file = pathname === '/' || pathname.startsWith('/r/') ? 'index.html' : pathname.slice(1);
  const safe = path.normalize(file).replace(/^([.][.][/\\])+/, '');
  const full = path.join(PUBLIC, safe);
  if (!full.startsWith(PUBLIC)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(full, (err, data) => {
    if (err) {
      if (pathname.startsWith('/r/')) return fs.readFile(path.join(PUBLIC,'index.html'), (e,d)=>{ if(e){res.writeHead(404);res.end('Not found');} else {res.writeHead(200, {'Content-Type':'text/html; charset=utf-8'});res.end(d);} });
      res.writeHead(404); return res.end('Not found');
    }
    const ext = path.extname(full);
    const type = ext==='.html'?'text/html; charset=utf-8':ext==='.js'?'text/javascript; charset=utf-8':ext==='.css'?'text/css; charset=utf-8':ext==='.svg'?'image/svg+xml':'application/octet-stream';
    res.writeHead(200, {'Content-Type':type, 'Cache-Control': ext==='.html'?'no-cache':'public, max-age=300'});
    res.end(data);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const p = url.pathname;
  try {
    if (p === '/api/health') return json(res, 200, {ok:true, rooms:rooms.size});
    if (req.method === 'POST' && p === '/api/rooms') {
      const {room, blackToken} = newRoom();
      return json(res, 201, {roomId:room.id, token:blackToken, role:'black'});
    }
    const match = p.match(/^\/api\/room\/([A-Z0-9]+)(?:\/(join|shot|rematch|resign))?$/);
    if (match) {
      const room = rooms.get(match[1]);
      if (!room) return json(res, 404, {error:'ROOM_NOT_FOUND'});
      room.lastActive = Date.now();
      const action = match[2];
      if (req.method === 'GET' && !action) {
        const after = Number(url.searchParams.get('after') ?? -1);
        const t = url.searchParams.get('token') || '';
        return json(res, 200, {...sanitize(room, after), role:roleFor(room,t)});
      }
      const body = await readBody(req);
      if (req.method === 'POST' && action === 'join') {
        let r = roleFor(room, body.token);
        let t = body.token;
        if (r === 'spectator' && !room.players.white) {
          t = token(); room.players.white = t; r='white';
          if (room.phase === 'waiting') room.phase='playing';
        } else if (r === 'spectator' && !room.players.black) {
          t = token(); room.players.black=t; r='black';
        }
        return json(res, 200, {token:t, role:r, state:sanitize(room,-1)});
      }
      const r = roleFor(room, body.token);
      if (r !== 'black' && r !== 'white') return json(res, 403, {error:'NOT_PLAYER'});
      if (req.method === 'POST' && action === 'shot') {
        if (room.locked) return json(res, 409, {error:'BUSY'});
        if (room.phase !== 'playing') return json(res, 409, {error:'NOT_PLAYING'});
        if (room.turn !== r) return json(res, 409, {error:'NOT_YOUR_TURN'});
        const s = room.stones.find(x => x.id === body.stoneId);
        if (!s || !s.alive || s.owner !== r) return json(res, 400, {error:'INVALID_STONE'});
        let vx = Number(body.vx), vy = Number(body.vy);
        if (!Number.isFinite(vx) || !Number.isFinite(vy)) return json(res,400,{error:'INVALID_VECTOR'});
        const mag = Math.hypot(vx,vy);
        if (mag < 80) return json(res,400,{error:'SHOT_TOO_WEAK'});
        const max = 1450;
        if (mag > max) { vx = vx/mag*max; vy = vy/mag*max; }
        room.locked = true;
        const anim = simulate(room, s.id, vx, vy);
        room.shotSeq += 1;
        room.lastAnimation = { seq:room.shotSeq, shooter:r, stoneId:s.id, ...anim };
        evaluate(room);
        if (room.phase === 'playing') room.turn = r === 'black' ? 'white' : 'black';
        room.locked = false;
        return json(res, 200, sanitize(room, room.shotSeq-1));
      }
      if (req.method === 'POST' && action === 'rematch') {
        if (room.phase !== 'finished') return json(res,409,{error:'GAME_NOT_FINISHED'});
        room.rematch[r] = true;
        if (room.rematch.black && room.rematch.white) resetRoom(room);
        return json(res,200,sanitize(room,-1));
      }
      if (req.method === 'POST' && action === 'resign') {
        if (room.phase !== 'playing') return json(res,409,{error:'NOT_PLAYING'});
        room.winner = r === 'black' ? 'white' : 'black'; room.phase='finished';
        room.shotSeq += 1; room.lastAnimation = null;
        return json(res,200,sanitize(room,-1));
      }
    }
    if (req.method === 'GET') return serveStatic(req,res,p);
    json(res,404,{error:'NOT_FOUND'});
  } catch (e) {
    console.error(e);
    json(res,500,{error:'SERVER_ERROR'});
  }
});

setInterval(() => {
  const cutoff = Date.now() - ROOM_TTL;
  for (const [k,r] of rooms) if (r.lastActive < cutoff) rooms.delete(k);
}, 1000*60*20).unref();

server.listen(PORT, () => console.log(`Alkkagi Duel listening on :${PORT}`));
