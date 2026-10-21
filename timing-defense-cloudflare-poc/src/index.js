import { DurableObject } from "cloudflare:workers";

const CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const CLASSES = new Set(["knight", "rogue", "tank", "archer", "mage"]);
const METHODS = new Set(["friend", "link"]);
const JUDGES = new Set(["NORMAL", "GOOD", "PERFECT"]);
const MAX_SLOTS = 4;
const START_DELAY_MS = 2500;
const INTRO_MS = 1050;
const STAGE_TARGET = 8;
const SPAWN_GAP_MS = 1120;
const BASE_HP = 2000;
const WALL_X = 0.155;
const GRUNT = { hp: 320, speed: 0.070, baseDamage: 90, armor: 1, reward: 6, knockResist: 0.85 };

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
  });
}
function cleanCode(value) { return String(value || "").trim().toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6); }
function randomCode() {
  const bytes = new Uint8Array(6); crypto.getRandomValues(bytes); let out = "";
  for (const byte of bytes) out += CODE_ALPHABET[byte % CODE_ALPHABET.length];
  return out;
}
function cleanNickname(value) { const out = String(value || "").trim().slice(0, 12); return out || "PLAYER"; }
function cleanClass(value) { const out = String(value || "knight"); return CLASSES.has(out) ? out : "knight"; }
function cleanMethod(value) { const out = String(value || "friend"); return METHODS.has(out) ? out : "friend"; }
function cleanAiFill(value) {
  if (!Array.isArray(value)) return [];
  const used = new Set(), out = [];
  for (const raw of value) {
    const pos = Number(raw?.pos), cls = cleanClass(raw?.cls);
    if (pos < 2 || pos > 4 || used.has(pos)) continue;
    used.add(pos); out.push({ pos, cls }); if (out.length >= 2) break;
  }
  return out.sort((a, b) => a.pos - b.pos);
}
function roomStub(env, code) { const id = env.ROOMS.idFromName(code); return env.ROOMS.get(id, { locationHint: "apac-ne" }); }
async function parseJson(request) { return request.json().catch(() => ({})); }
function newSeed() { const a = new Uint32Array(1); crypto.getRandomValues(a); return (a[0] & 0x7fffffff) || 1; }
function need(level) { return 60 + 12 * (level - 1); }
function comboBonus(combo) { return combo >= 30 ? 0.15 : combo >= 20 ? 0.12 : combo >= 10 ? 0.08 : combo >= 5 ? 0.05 : 0; }
function baseDamage(tier) {
  return tier === "PERFECT" ? 200 : tier === "GOOD" ? 140 : tier === "CRITICAL" ? 600 : tier === "SUPER" ? 400 : tier === "GREAT" ? 300 : tier === "HEAVY+" ? 230 : tier === "HEAVY" ? 180 : 100;
}
function strongTier(x, y) {
  if (x === "PERFECT" && y === "PERFECT") return "CRITICAL";
  const weight = (x === "PERFECT" ? 2 : x === "GOOD" ? 1 : 0) + (y === "PERFECT" ? 2 : y === "GOOD" ? 1 : 0);
  return weight >= 3 ? "SUPER" : weight === 2 ? "GREAT" : weight === 1 ? "HEAVY+" : "HEAVY";
}
function xpFor(tier) {
  const critical = tier === "CRITICAL", perfect = critical || tier === "PERFECT" || tier === "SUPER", good = perfect || tier === "GOOD" || tier === "GREAT";
  return critical ? 28 : perfect ? 18 : good ? 12 : 8;
}
function aiInterval(cls) { return cls === "rogue" ? 1150 : cls === "tank" ? 1650 : 1400; }

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/api/health") {
      return json({ ok: true, service: "timing-defense-cloudflare-v033-stage1", version: "0.33-cf.1", transport: "websocket-hibernation", authority: "durable-object-event-driven-stage1", locationHint: "apac-ne", scope: "room-ready-start-stage1" });
    }
    if (request.method === "GET" && url.pathname === "/") {
      const assetUrl = new URL(request.url); assetUrl.pathname = "/v033-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl, request));
    }
    if (request.method === "POST" && url.pathname === "/api/room/create") {
      const body = await parseJson(request);
      for (let i = 0; i < 12; i++) {
        const code = randomCode(), session = crypto.randomUUID();
        const response = await roomStub(env, code).fetch(new Request("https://room.internal/init", {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ code, method: cleanMethod(body.method), aiFill: cleanAiFill(body.aiFill), host: { session, nickname: cleanNickname(body.nickname), classId: cleanClass(body.classId) } })
        }));
        if (response.status === 201) {
          const data = await response.json();
          return json({ ok: true, code, session, slot: 1, state: data.state }, 201);
        }
        if (response.status !== 409) return response;
      }
      return json({ ok: false, error: "room-code-exhausted" }, 503);
    }
    const stateMatch = url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/state$/i);
    if (request.method === "GET" && stateMatch) return roomStub(env, cleanCode(stateMatch[1])).fetch(new Request("https://room.internal/state"));
    const leaveMatch = url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/leave$/i);
    if (request.method === "POST" && leaveMatch) {
      const body = await parseJson(request);
      return roomStub(env, cleanCode(leaveMatch[1])).fetch(new Request("https://room.internal/leave", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ session: String(body.session || "") }) }));
    }
    const wsMatch = url.pathname.match(/^\/ws\/([A-Z0-9]{6})$/i);
    if (request.method === "GET" && wsMatch) return roomStub(env, cleanCode(wsMatch[1])).fetch(request);
    return env.ASSETS.fetch(request);
  }
};

export class TimingDefenseRoom extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.ctx = ctx; this.env = env; this.room = null;
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair("ping", "pong"));
    this.ctx.blockConcurrencyWhile(async () => { this.room = (await this.ctx.storage.get("room")) || null; });
  }

  async fetch(request) {
    const url = new URL(request.url);
    if (request.method === "POST" && url.pathname === "/init") {
      if (this.room) return json({ ok: false, error: "room-already-exists" }, 409);
      const body = await parseJson(request), code = cleanCode(body.code), host = body.host || {}, session = String(host.session || "");
      if (code.length !== 6 || !session) return json({ ok: false, error: "invalid-room-init" }, 400);
      this.room = {
        version: "0.33-cf.1", code, method: cleanMethod(body.method), createdAt: Date.now(), updatedAt: Date.now(), revision: 0,
        status: "waiting", startAt: null, hostSession: session, aiFill: cleanAiFill(body.aiFill),
        participants: [{ session, slot: 1, nickname: cleanNickname(host.nickname), classId: cleanClass(host.classId), ready: false, connected: false, activeConnectionId: null, joinedAt: Date.now() }],
        run: null
      };
      await this.persist();
      return json({ ok: true, state: this.publicState(Date.now()) }, 201);
    }
    if (!this.room) return json({ ok: false, error: "room-not-found" }, 404);
    if (request.method === "GET" && url.pathname === "/state") {
      const now = Date.now(), changed = this.advanceTo(now);
      if (changed) { await this.persist(); this.broadcastState(now); }
      await this.scheduleNext();
      return json({ ok: true, state: this.publicState(now) });
    }
    if (request.method === "POST" && url.pathname === "/leave") {
      const body = await parseJson(request), session = String(body.session || ""), removed = await this.explicitLeave(session);
      return json({ ok: true, removed, state: this.room ? this.publicState(Date.now()) : null });
    }
    if (request.headers.get("Upgrade")?.toLowerCase() === "websocket") return this.acceptSocket(url);
    return json({ ok: false, error: "not-found" }, 404);
  }

  async acceptSocket(url) {
    const now = Date.now(), advanced = this.advanceTo(now), requestedSession = String(url.searchParams.get("session") || "").trim();
    const nickname = cleanNickname(url.searchParams.get("nickname")), classId = cleanClass(url.searchParams.get("classId"));
    let player = requestedSession ? this.room.participants.find(p => p.session === requestedSession) : null;
    if (!player) {
      if (this.room.status !== "waiting") return json({ ok: false, error: "room-not-joinable" }, 409);
      const slot = this.nextHumanSlot(); if (!slot) return json({ ok: false, error: "room-full" }, 409);
      player = { session: crypto.randomUUID(), slot, nickname, classId, ready: false, connected: false, activeConnectionId: null, joinedAt: now };
      this.room.participants.push(player);
    } else if (this.room.status === "waiting") { player.nickname = nickname; player.classId = classId; }
    const connectionId = crypto.randomUUID(); player.connected = true; player.activeConnectionId = connectionId;
    for (const existing of this.ctx.getWebSockets()) {
      const attachment = existing.deserializeAttachment?.();
      if (attachment?.session === player.session) { try { existing.close(4000, "replaced-by-reconnect"); } catch (_) {} }
    }
    const pair = new WebSocketPair(), client = pair[0], server = pair[1];
    server.serializeAttachment({ session: player.session, slot: player.slot, connectionId }); this.ctx.acceptWebSocket(server);
    await this.persist();
    const runPlayer = this.room.run?.players?.find(p => p.slot === player.slot);
    this.send(server, { type: "welcome", session: player.session, slot: player.slot, lastSeq: runPlayer?.lastSeq || 0, state: this.publicState(now) });
    this.broadcastState(now); await this.scheduleNext(); if (advanced) this.broadcastState(now);
    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws, message) {
    const attachment = ws.deserializeAttachment?.() || {}, player = this.room?.participants.find(p => p.session === attachment.session);
    if (!this.room || !player || player.activeConnectionId !== attachment.connectionId) { this.send(ws, { type: "error", error: "invalid-session" }); return; }
    let data; try { const text = typeof message === "string" ? message : new TextDecoder().decode(message); data = JSON.parse(text); }
    catch (_) { this.send(ws, { type: "error", error: "invalid-json" }); return; }
    const now = Date.now(); let changed = this.advanceTo(now);
    if (data.type === "ready") {
      if (this.room.status !== "waiting") return this.send(ws, { type: "error", error: "room-locked" });
      player.ready = !!data.ready; changed = true;
    } else if (data.type === "start") {
      if (this.room.status !== "waiting") return this.send(ws, { type: "error", error: "room-locked" });
      if (this.room.hostSession !== player.session) return this.send(ws, { type: "error", error: "host-only" });
      if (!this.canStart()) return this.send(ws, { type: "error", error: "not-ready" });
      this.room.status = "starting"; this.room.startAt = now + START_DELAY_MS; this.room.run = this.makeRun(this.room.startAt); changed = true;
    } else if (data.type === "action") {
      try { const result = this.playerAction(player, data, now); changed = true; this.send(ws, { type: "action-result", result }); }
      catch (error) { this.send(ws, { type: "error", error: error.message || "action-failed" }); await this.scheduleNext(); return; }
    } else if (data.type === "leave") {
      await this.explicitLeave(player.session); try { ws.close(1000, "left-room"); } catch (_) {} return;
    } else { this.send(ws, { type: "error", error: "unknown-message" }); await this.scheduleNext(); return; }
    if (changed) { await this.persist(); this.broadcastState(now); }
    await this.scheduleNext();
  }

  async webSocketClose(ws, code, reason) {
    const attachment = ws.deserializeAttachment?.() || {}, player = this.room?.participants.find(p => p.session === attachment.session);
    if (player && player.activeConnectionId === attachment.connectionId) { player.connected = false; player.activeConnectionId = null; await this.persist(); this.broadcastState(Date.now()); }
    try { ws.close(code, reason); } catch (_) {}
  }
  async webSocketError(ws) {
    const attachment = ws.deserializeAttachment?.() || {}, player = this.room?.participants.find(p => p.session === attachment.session);
    if (player && player.activeConnectionId === attachment.connectionId) { player.connected = false; player.activeConnectionId = null; await this.persist(); this.broadcastState(Date.now()); }
  }
  async alarm() {
    if (!this.room?.run) return;
    const now = Date.now(), changed = this.advanceTo(now);
    if (changed) { await this.persist(); this.broadcastState(now); }
    await this.scheduleNext();
  }

  makeRun(startAt) {
    const seed = newSeed(), combatAt = startAt + INTRO_MS;
    return {
      id: crypto.randomUUID().replace(/-/g, "").slice(0, 16), seed, rngState: seed >>> 0, status: "starting", startAt, combatAt,
      stage: 1, stageTarget: STAGE_TARGET, spawned: 0, nextSpawnAt: combatAt, baseHp: BASE_HP, baseHpMax: BASE_HP, kills: 0, nextMonsterId: 1,
      monsters: [],
      players: this.room.participants.map(p => ({ slot: p.slot, level: 1, xp: 0, xpNeed: 60, charge: 0, combo: 0, comboPeak: 0, kills: 0, coin: 0, damage: 0, lastSeq: 0, nextPassiveAt: combatAt + 2000 })),
      ai: this.room.aiFill.map(a => ({ slot: a.pos, cls: a.cls, charge: 0, nextAt: combatAt + 450 + a.pos * 220 })),
      events: [], nextEventId: 1, revision: 0
    };
  }
  rng() { const run = this.room.run; let x = (run.rngState >>> 0) || 1; x ^= (x << 13) >>> 0; x ^= x >>> 17; x ^= (x << 5) >>> 0; run.rngState = x >>> 0; return run.rngState / 4294967296; }
  event(data, at) { const run = this.room.run; run.events.push({ id: run.nextEventId++, ...data, at }); if (run.events.length > 48) run.events.splice(0, run.events.length - 48); }
  recordCombo(player, judge) { player.combo = judge === "PERFECT" ? player.combo + 1 : 0; player.comboPeak = Math.max(player.comboPeak, player.combo); }
  grantXp(player, amount) { player.xp += amount; while (player.xp >= player.xpNeed) { player.xp -= player.xpNeed; player.level++; player.xpNeed = need(player.level); } }
  xAt(monster, at) { return monster.x - GRUNT.speed * Math.max(0, at - monster.refAt) / 1000; }
  materialize(monster, at) { monster.x = this.xAt(monster, at); monster.refAt = at; }
  wallAt(monster) { if (monster.x <= WALL_X) return monster.refAt; return monster.refAt + ((monster.x - WALL_X) / GRUNT.speed) * 1000; }
  nearest(at) {
    let best = null, bestX = Infinity;
    for (const monster of this.room.run?.monsters || []) { const x = this.xAt(monster, at); if (x < bestX) { bestX = x; best = monster; } }
    return best;
  }
  spawn(at) {
    const run = this.room.run, id = run.nextMonsterId++, hp = Math.round(GRUNT.hp * 1.10);
    run.monsters.push({ id, type: "grunt", x: 1.055 + this.rng() * 0.04, y: 0.30 + this.rng() * 0.32, refAt: at, hp, maxHp: hp }); run.spawned++;
    this.event({ type: "spawn", targetId: id, monsterType: "grunt", stage: 1 }, at);
  }
  applyDamage(monster, damage, slot, tier, at, knock = true, source = "hit") {
    const run = this.room.run; if (!monster) return { actual: 0, killed: false };
    this.materialize(monster, at); const actual = Math.max(1, Math.round(damage * GRUNT.armor)); monster.hp -= actual;
    if (knock) {
      const critical = tier === "CRITICAL", perfect = critical || tier === "PERFECT" || tier === "SUPER", good = perfect || tier === "GOOD" || tier === "GREAT";
      const base = critical ? 0.047 : perfect ? 0.024 : good ? 0.013 : 0.006; monster.x = Math.min(0.985, monster.x + base * GRUNT.knockResist);
    }
    const player = run.players.find(p => p.slot === slot); let killed = false;
    if (monster.hp <= 0) { killed = true; run.kills++; if (player) { player.kills++; player.coin += GRUNT.reward; } run.monsters = run.monsters.filter(m => m.id !== monster.id); }
    if (player) player.damage += actual;
    this.event({ type: source, slot, targetId: monster.id, tier, damage: actual, killed, stage: 1 }, at); return { actual, killed };
  }
  playerAction(participant, body, at) {
    const run = this.room.run; if (!run || run.status !== "combat") throw new Error("run-not-combat");
    const player = run.players.find(p => p.slot === participant.slot); if (!player) throw new Error("player-not-in-run");
    const seq = Number(body.seq); if (!Number.isFinite(seq) || seq <= player.lastSeq) throw new Error("stale-seq"); player.lastSeq = seq;
    const x = JUDGES.has(body.xJudge) ? body.xJudge : "NORMAL", heavy = player.charge >= 3, y = heavy && JUDGES.has(body.yJudge) ? body.yJudge : null;
    let tier, predictedCombo;
    if (heavy) { this.recordCombo(player, x); predictedCombo = y === "PERFECT" ? player.combo + 1 : 0; tier = strongTier(x, y || "NORMAL"); this.recordCombo(player, y || "NORMAL"); }
    else { predictedCombo = x === "PERFECT" ? player.combo + 1 : 0; tier = x; this.recordCombo(player, x); }
    const damage = Math.round(baseDamage(tier) * (1 + comboBonus(predictedCombo))), monster = this.nearest(at);
    const result = this.applyDamage(monster, damage, player.slot, tier, at, true, "hit"), xpGain = xpFor(tier);
    this.grantXp(player, xpGain); player.charge = heavy ? 0 : Math.min(3, player.charge + 1);
    const event = run.events[run.events.length - 1];
    if (event?.type === "hit" && event.slot === player.slot) Object.assign(event, { xpGain, level: player.level, charge: player.charge, combo: player.combo, xJudge: x, yJudge: y });
    run.revision++; this.checkEnd(at);
    return { tier, ...result, xpGain, player: this.playerPublic(player) };
  }
  aiTier(ai) {
    const r = this.rng(), heavy = ai.charge >= 3;
    if (heavy) { ai.charge = 0; return r < 0.15 ? "SUPER" : r < 0.65 ? "GREAT" : "HEAVY+"; }
    ai.charge++; return r < 0.18 ? "PERFECT" : r < 0.72 ? "GOOD" : "NORMAL";
  }
  processAt(at) {
    const run = this.room.run; if (!run) return false; let changed = false;
    if (run.status === "starting" && at >= run.startAt) { run.status = at < run.combatAt ? "intro" : "combat"; this.room.status = "running"; changed = true; }
    if (run.status === "intro" && at >= run.combatAt) { run.status = "combat"; changed = true; }
    if (run.status !== "combat") { if (changed) run.revision++; return changed; }
    while (run.spawned < run.stageTarget && run.nextSpawnAt <= at) { this.spawn(run.nextSpawnAt); run.nextSpawnAt += SPAWN_GAP_MS; changed = true; }
    const wallHits = [...run.monsters].filter(m => this.wallAt(m) <= at + 0.5).sort((a, b) => this.wallAt(a) - this.wallAt(b) || a.id - b.id);
    for (const monster of wallHits) {
      if (!run.monsters.find(m => m.id === monster.id)) continue;
      const hitAt = Math.min(at, this.wallAt(monster)); this.materialize(monster, hitAt); run.monsters = run.monsters.filter(m => m.id !== monster.id);
      run.baseHp = Math.max(0, run.baseHp - GRUNT.baseDamage); this.event({ type: "wall", targetId: monster.id, damage: GRUNT.baseDamage, baseHp: run.baseHp }, hitAt); changed = true;
      if (this.checkEnd(hitAt)) break;
    }
    if (run.status !== "combat") { if (changed) run.revision++; return changed; }
    for (const player of [...run.players].sort((a, b) => a.slot - b.slot)) {
      if (player.nextPassiveAt > at) continue;
      const eventAt = player.nextPassiveAt, monster = this.nearest(eventAt);
      if (monster) { this.applyDamage(monster, 40, player.slot, "AUTO", eventAt, false, "passive"); player.nextPassiveAt = eventAt + 2000; changed = true; if (this.checkEnd(eventAt)) break; }
      else { player.nextPassiveAt = eventAt + 250; changed = true; }
    }
    if (run.status !== "combat") { if (changed) run.revision++; return changed; }
    for (const ai of [...run.ai].sort((a, b) => a.slot - b.slot)) {
      if (ai.nextAt > at) continue;
      const eventAt = ai.nextAt, monster = this.nearest(eventAt);
      if (monster) { const tier = this.aiTier(ai); this.applyDamage(monster, baseDamage(tier), ai.slot, tier, eventAt, true, "ai"); ai.nextAt = eventAt + aiInterval(ai.cls) + Math.round(-140 + this.rng() * 310); changed = true; if (this.checkEnd(eventAt)) break; }
      else { ai.nextAt = eventAt + 120; changed = true; }
    }
    if (changed) run.revision++; return changed;
  }
  nextDueAt() {
    const run = this.room?.run; if (!run || ["stage1-clear", "gameover"].includes(run.status)) return null;
    if (run.status === "starting") return run.startAt; if (run.status === "intro") return run.combatAt; if (run.status !== "combat") return null;
    let due = Infinity; if (run.spawned < run.stageTarget) due = Math.min(due, run.nextSpawnAt);
    for (const player of run.players) due = Math.min(due, player.nextPassiveAt); for (const ai of run.ai) due = Math.min(due, ai.nextAt); for (const monster of run.monsters) due = Math.min(due, this.wallAt(monster));
    return Number.isFinite(due) ? due : null;
  }
  advanceTo(target) {
    const run = this.room?.run; if (!run) return false; let changed = false, guard = 0;
    while (guard++ < 512) { const due = this.nextDueAt(); if (due == null || due > target) break; changed = this.processAt(due) || changed; if (["stage1-clear", "gameover"].includes(run.status)) break; }
    return changed;
  }
  checkEnd(at) {
    const run = this.room.run;
    if (run.baseHp <= 0 && run.status !== "gameover") { run.status = "gameover"; this.room.status = "run-ended"; this.event({ type: "gameover" }, at); return true; }
    if (run.spawned >= run.stageTarget && run.monsters.length === 0 && run.status === "combat") { run.status = "stage1-clear"; this.room.status = "stage1-clear"; this.event({ type: "stage-clear", stage: 1 }, at); return true; }
    return false;
  }
  nextHumanSlot() {
    const occupied = new Set(this.room.aiFill.map(x => x.pos)); for (const participant of this.room.participants) occupied.add(participant.slot);
    for (let slot = 1; slot <= MAX_SLOTS; slot++) if (!occupied.has(slot)) return slot; return null;
  }
  canStart() { const humans = this.room?.participants || []; return this.room?.status === "waiting" && humans.length >= 2 && humans.every(p => p.ready); }
  async explicitLeave(session) {
    if (!this.room) return false; const index = this.room.participants.findIndex(p => p.session === session); if (index < 0) return false;
    const [removed] = this.room.participants.splice(index, 1); if (this.room.run) this.room.run.players = this.room.run.players.filter(p => p.slot !== removed.slot);
    if (this.room.hostSession === removed.session) { const next = [...this.room.participants].sort((a, b) => a.slot - b.slot)[0] || null; this.room.hostSession = next?.session || null; }
    if (!this.room.participants.length) {
      for (const socket of this.ctx.getWebSockets()) { try { socket.close(1000, "room-empty"); } catch (_) {} }
      await this.ctx.storage.deleteAll(); this.room = null; try { await this.ctx.storage.deleteAlarm(); } catch (_) {} return true;
    }
    await this.persist(); this.broadcastState(Date.now());
    for (const socket of this.ctx.getWebSockets()) { const attachment = socket.deserializeAttachment?.(); if (attachment?.session === session) { try { socket.close(1000, "left-room"); } catch (_) {} } }
    await this.scheduleNext(); return true;
  }
  playerPublic(player) { return { slot: player.slot, level: player.level, xp: player.xp, xpNeed: player.xpNeed, charge: player.charge, combo: player.combo, comboPeak: player.comboPeak, kills: player.kills, coin: player.coin, damage: player.damage }; }
  runPublic(at) {
    const run = this.room?.run; if (!run) return null;
    return { id: run.id, seed: run.seed, status: run.status, startAt: run.startAt, combatAt: run.combatAt, stage: 1, stageTarget: run.stageTarget, spawned: run.spawned, baseHp: run.baseHp, baseHpMax: run.baseHpMax, kills: run.kills, revision: run.revision, serverTime: at,
      monsters: run.monsters.map(m => ({ id: m.id, type: m.type, x: Math.max(WALL_X, this.xAt(m, at)), y: m.y, hp: m.hp, maxHp: m.maxHp, boss: false })),
      players: run.players.map(p => this.playerPublic(p)), events: run.events.slice(-24) };
  }
  publicState(at = Date.now()) {
    if (!this.room) return null;
    const participants = [...this.room.participants].sort((a, b) => a.slot - b.slot).map(p => ({ slot: p.slot, nickname: p.nickname, classId: p.classId, ready: !!p.ready, connected: !!p.connected, host: p.session === this.room.hostSession }));
    const occupied = new Set(participants.map(p => p.slot)); for (const ai of this.room.aiFill) occupied.add(ai.pos); const openHumanSlots = [];
    for (let slot = 1; slot <= MAX_SLOTS; slot++) if (!occupied.has(slot)) openHumanSlots.push(slot);
    return { version: this.room.version, code: this.room.code, method: this.room.method, status: this.room.status, createdAt: this.room.createdAt, revision: this.room.revision, serverTime: at,
      hostSlot: participants.find(p => p.host)?.slot || null, participants, aiFill: this.room.aiFill.map(x => ({ ...x })), openHumanSlots, canStart: this.canStart(), startAt: this.room.startAt || null, run: this.runPublic(at) };
  }
  async persist() { if (!this.room) return; this.room.updatedAt = Date.now(); this.room.revision = (this.room.revision || 0) + 1; await this.ctx.storage.put("room", this.room); }
  async scheduleNext() {
    if (!this.room?.run) { try { await this.ctx.storage.deleteAlarm(); } catch (_) {} return; }
    const due = this.nextDueAt(); if (due == null) { try { await this.ctx.storage.deleteAlarm(); } catch (_) {} return; }
    await this.ctx.storage.setAlarm(Math.max(Date.now() + 1, Math.ceil(due)));
  }
  send(ws, payload) { try { ws.send(JSON.stringify(payload)); } catch (_) {} }
  broadcast(payload) { const text = JSON.stringify(payload); for (const ws of this.ctx.getWebSockets()) { try { ws.send(text); } catch (_) {} } }
  broadcastState(at = Date.now()) { this.broadcast({ type: "state", state: this.publicState(at) }); }
}
