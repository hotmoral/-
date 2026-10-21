import { DurableObject } from "cloudflare:workers";

const CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const CLASSES = new Set(["knight", "rogue", "tank", "archer", "mage"]);
const METHODS = new Set(["friend", "link"]);
const MAX_SLOTS = 4;
const START_DELAY_MS = 2500;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
  });
}

function cleanCode(value) {
  return String(value || "").trim().toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6);
}

function randomCode() {
  const bytes = new Uint8Array(6);
  crypto.getRandomValues(bytes);
  let out = "";
  for (const byte of bytes) out += CODE_ALPHABET[byte % CODE_ALPHABET.length];
  return out;
}

function cleanNickname(value) {
  const out = String(value || "").trim().slice(0, 12);
  return out || "PLAYER";
}

function cleanClass(value) {
  const out = String(value || "knight");
  return CLASSES.has(out) ? out : "knight";
}

function cleanMethod(value) {
  const out = String(value || "friend");
  return METHODS.has(out) ? out : "friend";
}

function cleanAiFill(value) {
  if (!Array.isArray(value)) return [];
  const used = new Set();
  const out = [];
  for (const raw of value) {
    const pos = Number(raw?.pos);
    const cls = cleanClass(raw?.cls);
    if (pos < 2 || pos > 4 || used.has(pos)) continue;
    used.add(pos);
    out.push({ pos, cls });
    if (out.length >= 2) break;
  }
  return out.sort((a, b) => a.pos - b.pos);
}

function roomStub(env, code) {
  const id = env.ROOMS.idFromName(code);
  return env.ROOMS.get(id, { locationHint: "apac-ne" });
}

async function parseJson(request) {
  return request.json().catch(() => ({}));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/api/health") {
      return json({
        ok: true,
        service: "timing-defense-cloudflare-v031-parity",
        version: "0.31-cf.1",
        transport: "websocket-hibernation",
        authority: "durable-object-event-driven",
        locationHint: "apac-ne",
        scope: "room-ready-start-only"
      });
    }

    if (request.method === "GET" && url.pathname === "/") {
      const assetUrl = new URL(request.url);
      assetUrl.pathname = "/v032-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl, request));
    }

    if (request.method === "POST" && url.pathname === "/api/room/create") {
      const body = await parseJson(request);
      for (let i = 0; i < 12; i++) {
        const code = randomCode();
        const session = crypto.randomUUID();
        const response = await roomStub(env, code).fetch(new Request("https://room.internal/init", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            code,
            method: cleanMethod(body.method),
            aiFill: cleanAiFill(body.aiFill),
            host: {
              session,
              nickname: cleanNickname(body.nickname),
              classId: cleanClass(body.classId)
            }
          })
        }));
        if (response.status === 201) {
          const data = await response.json();
          return json({
            ok: true,
            code,
            session,
            slot: 1,
            state: data.state
          }, 201);
        }
        if (response.status !== 409) return response;
      }
      return json({ ok: false, error: "room-code-exhausted" }, 503);
    }

    const stateMatch = url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/state$/i);
    if (request.method === "GET" && stateMatch) {
      const code = cleanCode(stateMatch[1]);
      return roomStub(env, code).fetch(new Request("https://room.internal/state"));
    }

    const leaveMatch = url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/leave$/i);
    if (request.method === "POST" && leaveMatch) {
      const code = cleanCode(leaveMatch[1]);
      const body = await parseJson(request);
      return roomStub(env, code).fetch(new Request("https://room.internal/leave", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ session: String(body.session || "") })
      }));
    }

    const wsMatch = url.pathname.match(/^\/ws\/([A-Z0-9]{6})$/i);
    if (request.method === "GET" && wsMatch) {
      const code = cleanCode(wsMatch[1]);
      return roomStub(env, code).fetch(request);
    }

    return env.ASSETS.fetch(request);
  }
};

export class TimingDefenseRoom extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.ctx = ctx;
    this.env = env;
    this.room = null;
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair("ping", "pong"));
    this.ctx.blockConcurrencyWhile(async () => {
      this.room = (await this.ctx.storage.get("room")) || null;
    });
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "POST" && url.pathname === "/init") {
      if (this.room) return json({ ok: false, error: "room-already-exists" }, 409);
      const body = await parseJson(request);
      const code = cleanCode(body.code);
      const host = body.host || {};
      const session = String(host.session || "");
      if (code.length !== 6 || !session) return json({ ok: false, error: "invalid-room-init" }, 400);

      this.room = {
        version: "0.31-cf.1",
        code,
        method: cleanMethod(body.method),
        createdAt: Date.now(),
        updatedAt: Date.now(),
        revision: 0,
        status: "waiting",
        startAt: null,
        hostSession: session,
        aiFill: cleanAiFill(body.aiFill),
        participants: [{
          session,
          slot: 1,
          nickname: cleanNickname(host.nickname),
          classId: cleanClass(host.classId),
          ready: false,
          connected: false,
          activeConnectionId: null,
          joinedAt: Date.now()
        }]
      };
      await this.persist();
      return json({ ok: true, state: this.publicState() }, 201);
    }

    if (!this.room) return json({ ok: false, error: "room-not-found" }, 404);

    if (request.method === "GET" && url.pathname === "/state") {
      return json({ ok: true, state: this.publicState() });
    }

    if (request.method === "POST" && url.pathname === "/leave") {
      const body = await parseJson(request);
      const session = String(body.session || "");
      const removed = await this.explicitLeave(session);
      return json({ ok: true, removed, state: this.publicState() });
    }

    if (request.headers.get("Upgrade")?.toLowerCase() === "websocket") {
      return this.acceptSocket(url);
    }

    return json({ ok: false, error: "not-found" }, 404);
  }

  async acceptSocket(url) {
    const requestedSession = String(url.searchParams.get("session") || "").trim();
    const nickname = cleanNickname(url.searchParams.get("nickname"));
    const classId = cleanClass(url.searchParams.get("classId"));

    let player = requestedSession
      ? this.room.participants.find((p) => p.session === requestedSession)
      : null;

    if (!player) {
      if (this.room.status !== "waiting") return json({ ok: false, error: "room-not-joinable" }, 409);
      const slot = this.nextHumanSlot();
      if (!slot) return json({ ok: false, error: "room-full" }, 409);
      player = {
        session: crypto.randomUUID(),
        slot,
        nickname,
        classId,
        ready: false,
        connected: false,
        activeConnectionId: null,
        joinedAt: Date.now()
      };
      this.room.participants.push(player);
    }

    const connectionId = crypto.randomUUID();
    player.connected = true;
    player.activeConnectionId = connectionId;

    for (const existing of this.ctx.getWebSockets()) {
      const attachment = existing.deserializeAttachment?.();
      if (attachment?.session === player.session) {
        try { existing.close(4000, "replaced-by-reconnect"); } catch (_) {}
      }
    }

    const [client, server] = Object.values(new WebSocketPair());
    server.serializeAttachment({ session: player.session, slot: player.slot, connectionId });
    this.ctx.acceptWebSocket(server);

    await this.persist();
    this.send(server, {
      type: "welcome",
      session: player.session,
      slot: player.slot,
      state: this.publicState()
    });
    this.broadcastState();

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws, message) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (!this.room || !player || player.activeConnectionId !== attachment.connectionId) {
      this.send(ws, { type: "error", error: "invalid-session" });
      return;
    }

    let data;
    try {
      const text = typeof message === "string" ? message : new TextDecoder().decode(message);
      data = JSON.parse(text);
    } catch (_) {
      this.send(ws, { type: "error", error: "invalid-json" });
      return;
    }

    if (data.type === "ready") {
      if (this.room.status !== "waiting") return this.send(ws, { type: "error", error: "room-locked" });
      player.ready = !!data.ready;
      await this.persist();
      this.broadcastState();
      return;
    }

    if (data.type === "start") {
      if (this.room.status !== "waiting") return this.send(ws, { type: "error", error: "room-locked" });
      if (this.room.hostSession !== player.session) return this.send(ws, { type: "error", error: "host-only" });
      if (!this.canStart()) return this.send(ws, { type: "error", error: "not-ready" });

      this.room.status = "starting";
      this.room.startAt = Date.now() + START_DELAY_MS;
      await this.persist();
      await this.ctx.storage.setAlarm(this.room.startAt);
      this.broadcastState();
      return;
    }

    if (data.type === "leave") {
      await this.explicitLeave(player.session);
      try { ws.close(1000, "left-room"); } catch (_) {}
      return;
    }

    this.send(ws, { type: "error", error: "unknown-message" });
  }

  async webSocketClose(ws, code, reason) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (player && player.activeConnectionId === attachment.connectionId) {
      player.connected = false;
      player.activeConnectionId = null;
      await this.persist();
      this.broadcastState();
    }
    try { ws.close(code, reason); } catch (_) {}
  }

  async webSocketError(ws) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (player && player.activeConnectionId === attachment.connectionId) {
      player.connected = false;
      player.activeConnectionId = null;
      await this.persist();
      this.broadcastState();
    }
  }

  async alarm() {
    if (!this.room || this.room.status !== "starting" || !this.room.startAt) return;
    const now = Date.now();
    if (now < this.room.startAt) {
      await this.ctx.storage.setAlarm(this.room.startAt);
      return;
    }
    this.room.status = "running";
    await this.persist();
    this.broadcastState();
  }

  nextHumanSlot() {
    const occupied = new Set(this.room.aiFill.map((x) => x.pos));
    for (const participant of this.room.participants) occupied.add(participant.slot);
    for (let slot = 1; slot <= MAX_SLOTS; slot++) if (!occupied.has(slot)) return slot;
    return null;
  }

  canStart() {
    const humans = this.room?.participants || [];
    return this.room?.status === "waiting" && humans.length >= 2 && humans.every((p) => p.ready);
  }

  async explicitLeave(session) {
    if (!this.room) return false;
    const index = this.room.participants.findIndex((p) => p.session === session);
    if (index < 0) return false;
    const [removed] = this.room.participants.splice(index, 1);

    if (this.room.hostSession === removed.session) {
      const next = [...this.room.participants].sort((a, b) => a.slot - b.slot)[0] || null;
      this.room.hostSession = next?.session || null;
    }

    if (!this.room.participants.length) {
      for (const socket of this.ctx.getWebSockets()) {
        try { socket.close(1000, "room-empty"); } catch (_) {}
      }
      await this.ctx.storage.deleteAll();
      this.room = null;
      return true;
    }

    await this.persist();
    this.broadcastState();
    for (const socket of this.ctx.getWebSockets()) {
      const attachment = socket.deserializeAttachment?.();
      if (attachment?.session === session) {
        try { socket.close(1000, "left-room"); } catch (_) {}
      }
    }
    return true;
  }

  publicState() {
    if (!this.room) return null;
    const participants = [...this.room.participants]
      .sort((a, b) => a.slot - b.slot)
      .map((p) => ({
        slot: p.slot,
        nickname: p.nickname,
        classId: p.classId,
        ready: !!p.ready,
        connected: !!p.connected,
        host: p.session === this.room.hostSession
      }));
    const occupied = new Set(participants.map((p) => p.slot));
    for (const ai of this.room.aiFill) occupied.add(ai.pos);
    const openHumanSlots = [];
    for (let slot = 1; slot <= MAX_SLOTS; slot++) if (!occupied.has(slot)) openHumanSlots.push(slot);

    return {
      version: this.room.version,
      code: this.room.code,
      method: this.room.method,
      status: this.room.status,
      createdAt: this.room.createdAt,
      revision: this.room.revision,
      serverTime: Date.now(),
      hostSlot: participants.find((p) => p.host)?.slot || null,
      participants,
      aiFill: this.room.aiFill.map((x) => ({ ...x })),
      openHumanSlots,
      canStart: this.canStart(),
      startAt: this.room.startAt || null
    };
  }

  async persist() {
    if (!this.room) return;
    this.room.updatedAt = Date.now();
    this.room.revision = (this.room.revision || 0) + 1;
    await this.ctx.storage.put("room", this.room);
  }

  send(ws, payload) {
    try { ws.send(JSON.stringify(payload)); } catch (_) {}
  }

  broadcast(payload) {
    const text = JSON.stringify(payload);
    for (const ws of this.ctx.getWebSockets()) {
      try { ws.send(text); } catch (_) {}
    }
  }

  broadcastState() {
    if (!this.room) return;
    this.broadcast({ type: "state", state: this.publicState() });
  }
}
