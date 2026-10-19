const express = require('express');
const http = require('http');
const path = require('path');
const { WebSocketServer } = require('ws');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));
app.get('/healthz', (_req, res) => res.json({ ok: true }));

const server = http.createServer(app);
const wss = new WebSocketServer({ server });
const PORT = process.env.PORT || 3000;

const WORLD = { width: 1200, height: 800, base: { x: 600, y: 400, r: 105 } };
const DAY_MS = 90_000;
const NIGHT_MS = 45_000;
const READY_COUNTDOWN_MS = 5_000;
const DISCONNECT_GRACE_MS = 30_000;
const TICK_MS = 50;
const SNAPSHOT_MS = 100;

const resourceTemplates = [
  { id: 'food-a', type: 'food', label: '편의점', x: 225, y: 195, r: 48, stock: 20 },
  { id: 'food-b', type: 'food', label: '마트', x: 1020, y: 615, r: 55, stock: 28 },
  { id: 'scrap-a', type: 'scrap', label: '정비소', x: 980, y: 180, r: 52, stock: 24 },
  { id: 'scrap-b', type: 'scrap', label: '공사장', x: 180, y: 635, r: 56, stock: 30 },
  { id: 'meds-a', type: 'meds', label: '약국', x: 395, y: 115, r: 44, stock: 14 },
  { id: 'ammo-a', type: 'ammo', label: '경비실', x: 820, y: 680, r: 44, stock: 18 }
];

const state = {
  day: 1,
  phase: 'maintenance',
  phaseEndsAt: null,
  countdownEndsAt: null,
  hasEverStarted: false,
  baseHp: 300,
  baseMaxHp: 300,
  stash: { food: 8, scrap: 10, meds: 2 },
  players: new Map(),
  zombies: new Map(),
  resources: [],
  events: []
};

let zombieSeq = 1;
let eventSeq = 1;
let lastSnapshotAt = 0;
let lastAmbientSpawnAt = 0;

function now() { return Date.now(); }
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
function token() { return Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2); }
function pushEvent(text, tone = 'info') {
  state.events.push({ id: eventSeq++, text, tone, at: now() });
  if (state.events.length > 12) state.events.splice(0, state.events.length - 12);
}

function resetResources() {
  state.resources = resourceTemplates.map(r => ({ ...r, stock: r.stock }));
}
resetResources();

function makePlayer(resumeToken, name = '생존자') {
  return {
    id: 'p-' + token().slice(0, 8),
    token: resumeToken || token(),
    name: String(name || '생존자').slice(0, 16),
    x: WORLD.base.x + (Math.random() - 0.5) * 70,
    y: WORLD.base.y + (Math.random() - 0.5) * 70,
    tx: WORLD.base.x,
    ty: WORLD.base.y,
    hp: 100,
    maxHp: 100,
    ammo: 18,
    carry: { food: 0, scrap: 0, meds: 0, ammo: 0 },
    carryCap: 12,
    ready: false,
    connected: true,
    disconnectedAt: null,
    pending: state.hasEverStarted,
    downUntil: 0,
    lastAttackAt: 0,
    lastGatherAt: 0,
    kills: 0,
    ws: null
  };
}

function eligiblePlayers() {
  const t = now();
  return [...state.players.values()].filter(p => !p.pending && (p.connected || (p.disconnectedAt && t - p.disconnectedAt <= DISCONNECT_GRACE_MS)));
}

function readyStatus() {
  const eligible = eligiblePlayers();
  const ready = eligible.filter(p => p.ready).length;
  const required = eligible.length ? Math.floor(eligible.length / 2) + 1 : 1;
  return { ready, total: eligible.length, required };
}

function setPhase(phase) {
  state.phase = phase;
  state.countdownEndsAt = null;
  for (const p of state.players.values()) p.ready = false;

  if (phase === 'day') {
    state.hasEverStarted = true;
    state.phaseEndsAt = now() + DAY_MS;
    state.zombies.clear();
    resetResources();
    for (const p of state.players.values()) {
      if (p.connected) {
        p.pending = false;
        p.hp = Math.max(p.hp, 70);
        p.x = WORLD.base.x + (Math.random() - 0.5) * 75;
        p.y = WORLD.base.y + (Math.random() - 0.5) * 75;
        p.tx = p.x; p.ty = p.y;
      }
    }
    spawnZombies(8 + Math.min(8, state.day * 2), false);
    pushEvent(`DAY ${state.day} 아침. 외부 탐색을 시작합니다.`, 'good');
  } else if (phase === 'night') {
    state.phaseEndsAt = now() + NIGHT_MS;
    spawnZombies(14 + Math.min(22, state.day * 3), true);
    pushEvent('해가 졌습니다. 좀비가 거점으로 몰려옵니다.', 'danger');
  } else {
    state.phaseEndsAt = null;
    state.zombies.clear();
    for (const p of state.players.values()) {
      p.tx = WORLD.base.x; p.ty = WORLD.base.y;
      if (p.connected) {
        p.x = WORLD.base.x + (Math.random() - 0.5) * 70;
        p.y = WORLD.base.y + (Math.random() - 0.5) * 70;
      }
    }
    pushEvent(`DAY ${state.day} 종료. 정비 후 준비 완료를 눌러주세요.`, 'info');
  }
}

function startNextDay() {
  if (state.hasEverStarted) state.day += 1;
  setPhase('day');
}

function spawnZombie(strong = false) {
  const side = Math.floor(Math.random() * 4);
  let x, y;
  if (side === 0) { x = Math.random() * WORLD.width; y = -20; }
  if (side === 1) { x = WORLD.width + 20; y = Math.random() * WORLD.height; }
  if (side === 2) { x = Math.random() * WORLD.width; y = WORLD.height + 20; }
  if (side === 3) { x = -20; y = Math.random() * WORLD.height; }
  const elite = strong && Math.random() < Math.min(0.28, 0.08 + state.day * 0.02);
  const id = 'z-' + zombieSeq++;
  state.zombies.set(id, {
    id, x, y,
    hp: elite ? 90 : 48,
    maxHp: elite ? 90 : 48,
    speed: elite ? 39 : (state.phase === 'night' ? 34 : 27),
    damage: elite ? 16 : 8,
    elite,
    lastAttackAt: 0
  });
}

function spawnZombies(count, strong) {
  for (let i = 0; i < count; i++) spawnZombie(strong);
}

function carryTotal(p) {
  return p.carry.food + p.carry.scrap + p.carry.meds + p.carry.ammo;
}

function depositAtBase(p) {
  if (dist(p, WORLD.base) > WORLD.base.r) return;
  const total = carryTotal(p);
  if (!total) return;
  state.stash.food += p.carry.food;
  state.stash.scrap += p.carry.scrap;
  state.stash.meds += p.carry.meds;
  p.ammo += p.carry.ammo * 3;
  p.carry = { food: 0, scrap: 0, meds: 0, ammo: 0 };
  pushEvent(`${p.name}이(가) 물자를 거점에 반납했습니다.`, 'good');
}

function gather(p, t) {
  if (state.phase !== 'day' || p.pending || p.downUntil > t) return;
  if (carryTotal(p) >= p.carryCap || t - p.lastGatherAt < 850) return;
  let target = null;
  for (const r of state.resources) {
    if (r.stock > 0 && dist(p, r) <= r.r) { target = r; break; }
  }
  if (!target) return;
  target.stock -= 1;
  p.carry[target.type] += 1;
  p.lastGatherAt = t;
}

function movePlayer(p, dt, t) {
  if (!p.connected || p.pending) return;
  if (p.downUntil > t) return;
  if (state.phase === 'maintenance') {
    p.tx = clamp(p.tx, WORLD.base.x - WORLD.base.r + 12, WORLD.base.x + WORLD.base.r - 12);
    p.ty = clamp(p.ty, WORLD.base.y - WORLD.base.r + 12, WORLD.base.y + WORLD.base.r - 12);
  }
  const dx = p.tx - p.x, dy = p.ty - p.y;
  const d = Math.hypot(dx, dy);
  if (d > 2) {
    const speed = 125;
    const step = Math.min(d, speed * dt);
    p.x += dx / d * step;
    p.y += dy / d * step;
    p.x = clamp(p.x, 8, WORLD.width - 8);
    p.y = clamp(p.y, 8, WORLD.height - 8);
  }
  depositAtBase(p);
  gather(p, t);
}

function nearestLivingPlayer(z) {
  let best = null, bestD = Infinity;
  for (const p of state.players.values()) {
    if (!p.connected || p.pending || p.downUntil > now()) continue;
    const d = dist(z, p);
    if (d < bestD) { best = p; bestD = d; }
  }
  return { p: best, d: bestD };
}

function updateZombie(z, dt, t) {
  const near = nearestLivingPlayer(z);
  let target = WORLD.base;
  if (near.p && near.d < (state.phase === 'night' ? 340 : 220)) target = near.p;
  const dx = target.x - z.x, dy = target.y - z.y;
  const d = Math.hypot(dx, dy) || 1;
  if (d > 22) {
    z.x += dx / d * z.speed * dt;
    z.y += dy / d * z.speed * dt;
  }

  if (target !== WORLD.base && d < 24 && t - z.lastAttackAt > 850) {
    target.hp -= z.damage;
    z.lastAttackAt = t;
    if (target.hp <= 0) {
      target.hp = 0;
      target.downUntil = t + 8000;
      target.carry = { food: 0, scrap: 0, meds: 0, ammo: 0 };
      pushEvent(`${target.name}이(가) 쓰러졌습니다.`, 'danger');
    }
  } else if (target === WORLD.base && d < WORLD.base.r + 10 && t - z.lastAttackAt > 900) {
    state.baseHp = Math.max(0, state.baseHp - z.damage);
    z.lastAttackAt = t;
  }
}

function autoAttack(p, t) {
  if (!p.connected || p.pending || p.downUntil > t || state.phase === 'maintenance') return;
  let target = null, bestD = Infinity;
  for (const z of state.zombies.values()) {
    const d = dist(p, z);
    if (d < bestD) { target = z; bestD = d; }
  }
  if (!target) return;
  const usingGun = p.ammo > 0 && bestD <= 155;
  const usingMelee = bestD <= 29;
  if (!usingGun && !usingMelee) return;
  const delay = usingGun ? 520 : 760;
  if (t - p.lastAttackAt < delay) return;
  p.lastAttackAt = t;
  if (usingGun) {
    p.ammo -= 1;
    target.hp -= 20;
  } else {
    target.hp -= 12;
  }
  if (target.hp <= 0) {
    state.zombies.delete(target.id);
    p.kills += 1;
  }
}

function revivePlayers(t) {
  for (const p of state.players.values()) {
    if (p.downUntil && p.downUntil <= t && p.hp <= 0) {
      p.hp = 60;
      p.downUntil = 0;
      p.x = WORLD.base.x + (Math.random() - 0.5) * 55;
      p.y = WORLD.base.y + (Math.random() - 0.5) * 55;
      p.tx = p.x; p.ty = p.y;
    }
  }
}

function updateReadyCountdown(t) {
  if (state.phase !== 'maintenance') { state.countdownEndsAt = null; return; }
  const s = readyStatus();
  const hasMajority = s.total > 0 && s.ready >= s.required;
  if (!hasMajority) {
    state.countdownEndsAt = null;
    return;
  }
  if (!state.countdownEndsAt) {
    state.countdownEndsAt = t + READY_COUNTDOWN_MS;
    pushEvent(`준비 과반수 달성. ${READY_COUNTDOWN_MS / 1000}초 후 출발합니다.`, 'good');
  } else if (t >= state.countdownEndsAt) {
    startNextDay();
  }
}

function cleanupDisconnected(t) {
  for (const [id, p] of state.players.entries()) {
    if (!p.connected && p.disconnectedAt && t - p.disconnectedAt > DISCONNECT_GRACE_MS) {
      state.players.delete(id);
    }
  }
}

function maintenanceAction(p, action) {
  if (state.phase !== 'maintenance' || p.pending) return;
  if (action === 'repair' && state.stash.scrap >= 5 && state.baseHp < state.baseMaxHp) {
    state.stash.scrap -= 5;
    state.baseHp = Math.min(state.baseMaxHp, state.baseHp + 75);
    pushEvent(`${p.name}: 방벽을 수리했습니다.`, 'good');
  }
  if (action === 'ammo' && state.stash.scrap >= 4) {
    state.stash.scrap -= 4;
    p.ammo += 18;
    pushEvent(`${p.name}: 탄약을 보급했습니다.`, 'good');
  }
  if (action === 'heal' && state.stash.meds >= 1 && p.hp < p.maxHp) {
    state.stash.meds -= 1;
    p.hp = Math.min(p.maxHp, p.hp + 45);
    pushEvent(`${p.name}: 치료를 완료했습니다.`, 'good');
  }
}

function publicState() {
  const t = now();
  const rdy = readyStatus();
  return {
    type: 'state',
    serverNow: t,
    world: WORLD,
    day: state.day,
    phase: state.phase,
    phaseEndsAt: state.phaseEndsAt,
    countdownEndsAt: state.countdownEndsAt,
    baseHp: state.baseHp,
    baseMaxHp: state.baseMaxHp,
    stash: state.stash,
    ready: rdy,
    players: [...state.players.values()].map(p => ({
      id: p.id, name: p.name, x: p.x, y: p.y, hp: p.hp, maxHp: p.maxHp,
      ammo: p.ammo, carry: p.carry, carryCap: p.carryCap, ready: p.ready,
      connected: p.connected, pending: p.pending, downUntil: p.downUntil,
      kills: p.kills
    })),
    zombies: [...state.zombies.values()],
    resources: state.resources,
    events: state.events.slice(-7)
  };
}

function send(ws, payload) {
  if (ws.readyState === ws.OPEN) ws.send(JSON.stringify(payload));
}

function broadcast() {
  const payload = JSON.stringify(publicState());
  for (const client of wss.clients) {
    if (client.readyState === client.OPEN) client.send(payload);
  }
}

wss.on('connection', ws => {
  ws.playerId = null;
  send(ws, { type: 'hello-required' });

  ws.on('message', raw => {
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch { return; }

    if (msg.type === 'hello') {
      const resumeToken = String(msg.token || '');
      let p = [...state.players.values()].find(x => resumeToken && x.token === resumeToken);
      if (p) {
        p.connected = true;
        p.disconnectedAt = null;
        p.ws = ws;
        if (msg.name) p.name = String(msg.name).slice(0, 16);
      } else {
        p = makePlayer(resumeToken || null, msg.name);
        p.ws = ws;
        state.players.set(p.id, p);
        if (p.pending) pushEvent(`${p.name}이(가) 참가했습니다. 다음 DAY부터 합류합니다.`);
        else pushEvent(`${p.name}이(가) 거점에 합류했습니다.`, 'good');
      }
      ws.playerId = p.id;
      send(ws, { type: 'welcome', id: p.id, token: p.token });
      return;
    }

    const p = state.players.get(ws.playerId);
    if (!p) return;

    if (msg.type === 'move' && !p.pending) {
      p.tx = clamp(Number(msg.x) || p.x, 0, WORLD.width);
      p.ty = clamp(Number(msg.y) || p.y, 0, WORLD.height);
    }
    if (msg.type === 'ready' && state.phase === 'maintenance' && !p.pending) {
      p.ready = Boolean(msg.value);
      updateReadyCountdown(now());
    }
    if (msg.type === 'maintenance-action') maintenanceAction(p, msg.action);
    if (msg.type === 'name') p.name = String(msg.name || p.name).slice(0, 16);
  });

  ws.on('close', () => {
    const p = state.players.get(ws.playerId);
    if (p) {
      p.connected = false;
      p.disconnectedAt = now();
      p.ready = false;
      updateReadyCountdown(now());
    }
  });
});

let lastTick = now();
setInterval(() => {
  const t = now();
  const dt = Math.min(0.1, (t - lastTick) / 1000);
  lastTick = t;

  cleanupDisconnected(t);
  revivePlayers(t);
  updateReadyCountdown(t);

  if (state.phase === 'day' || state.phase === 'night') {
    if (state.phaseEndsAt && t >= state.phaseEndsAt) {
      if (state.phase === 'day') setPhase('night');
      else setPhase('maintenance');
    }

    for (const p of state.players.values()) {
      movePlayer(p, dt, t);
      autoAttack(p, t);
    }
    for (const z of [...state.zombies.values()]) updateZombie(z, dt, t);

    if (state.phase === 'day' && t - lastAmbientSpawnAt > 7000 && state.zombies.size < 18 + state.day * 2) {
      spawnZombie(false);
      lastAmbientSpawnAt = t;
    }
    if (state.phase === 'night' && t - lastAmbientSpawnAt > 3200 && state.zombies.size < 45) {
      spawnZombie(true);
      lastAmbientSpawnAt = t;
    }
  } else {
    for (const p of state.players.values()) movePlayer(p, dt, t);
  }

  if (t - lastSnapshotAt >= SNAPSHOT_MS) {
    broadcast();
    lastSnapshotAt = t;
  }
}, TICK_MS);

server.listen(PORT, () => {
  console.log(`Zombie co-op prototype listening on ${PORT}`);
});
