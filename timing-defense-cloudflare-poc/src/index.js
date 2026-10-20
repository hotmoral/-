import { DurableObject } from "cloudflare:workers";

const CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const CLASSES = new Set(["knight", "rogue", "tank", "archer", "mage"]);
const MAX_PLAYERS = 4;
const POC_MONSTER_HP = 300;
const POC_ATTACK_DAMAGE = 100;

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
  for (const b of bytes) out += CODE_ALPHABET[b % CODE_ALPHABET.length];
  return out;
}

function roomStub(env, code) {
  const id = env.ROOMS.idFromName(code);
  return env.ROOMS.get(id, { locationHint: "apac-ne" });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/api/health") {
      return json({
        ok: true,
        service: "timing-defense-do-poc",
        version: "0.1.0",
        transport: "websocket-hibernation",
        authority: "durable-object-event-driven",
        locationHint: "apac-ne"
      });
    }

    if (request.method === "POST" && url.pathname === "/api/room/create") {
      for (let i = 0; i < 12; i++) {
        const code = randomCode();
        const stub = roomStub(env, code);
        const response = await stub.fetch(new Request("https://room.internal/init", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ code })
        }));
        if (response.status === 201) return json({ ok: true, code }, 201);
        if (response.status !== 409) return response;
      }
      return json({ ok: false, error: "room-code-exhausted" }, 503);
    }

    const stateMatch = url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/state$/i);
    if (request.method === "GET" && stateMatch) {
      const code = cleanCode(stateMatch[1]);
      return roomStub(env, code).fetch(new Request("https://room.internal/state"));
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
      const body = await request.json().catch(() => ({}));
      const code = cleanCode(body.code);
      if (code.length !== 6) return json({ ok: false, error: "invalid-room-code" }, 400);
      this.room = {
        code,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        revision: 0,
        status: "waiting",
        hostSession: null,
        participants: [],
        monster: null,
        eventSeq: 0
      };
      await this.persist();
      return json({ ok: true, state: this.publicState() }, 201);
    }

    if (!this.room) return json({ ok: false, error: "room-not-found" }, 404);

    if (request.method === "GET" && url.pathname === "/state") {
      return json({ ok: true, state: this.publicState() });
    }

    if (request.headers.get("Upgrade")?.toLowerCase() === "websocket") {
      return this.acceptSocket(url);
    }

    return json({ ok: false, error: "not-found" }, 404);
  }

  async acceptSocket(url) {
    const nickname = String(url.searchParams.get("nickname") || "PLAYER").trim().slice(0, 12) || "PLAYER";
    const requestedClass = String(url.searchParams.get("classId") || "knight");
    const classId = CLASSES.has(requestedClass) ? requestedClass : "knight";
    const requestedSession = String(url.searchParams.get("session") || "").trim();

    let player = requestedSession
      ? this.room.participants.find((p) => p.session === requestedSession)
      : null;

    if (!player && this.room.status !== "waiting") {
      return json({ ok: false, error: "run-already-started" }, 409);
    }

    if (!player) {
      if (this.room.participants.length >= MAX_PLAYERS) {
        return json({ ok: false, error: "room-full" }, 409);
      }
      const used = new Set(this.room.participants.map((p) => p.slot));
      let slot = 1;
      while (used.has(slot) && slot <= MAX_PLAYERS) slot++;
      player = {
        session: crypto.randomUUID(),
        slot,
        nickname,
        classId,
        ready: false,
        connected: true,
        lastSeq: 0,
        joinedAt: Date.now()
      };
      this.room.participants.push(player);
      if (!this.room.hostSession) this.room.hostSession = player.session;
    } else {
      player.nickname = nickname;
      player.classId = classId;
      player.connected = true;
    }

    for (const existing of this.ctx.getWebSockets()) {
      const attachment = existing.deserializeAttachment?.();
      if (attachment?.session === player.session) {
        try { existing.close(4000, "replaced-by-reconnect"); } catch (_) {}
      }
    }

    const pair = new WebSocketPair();
    const client = pair[0];
    const server = pair[1];
    server.serializeAttachment({ session: player.session, slot: player.slot });
    this.ctx.acceptWebSocket(server);

    await this.persist();
    server.send(JSON.stringify({
      type: "welcome",
      session: player.session,
      slot: player.slot,
      state: this.publicState()
    }));
    this.broadcastState();

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws, message) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (!this.room || !player) {
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

      this.room.status = "combat";
      this.room.monster = { id: 1, hp: POC_MONSTER_HP, maxHp: POC_MONSTER_HP };
      this.room.eventSeq++;
      await this.persist();
      this.broadcast({ type: "event", event: { id: this.room.eventSeq, kind: "start", at: Date.now() } });
      this.broadcastState();
      return;
    }

    if (data.type === "attack") {
      if (this.room.status !== "combat" || !this.room.monster) {
        return this.send(ws, { type: "error", error: "run-not-combat" });
      }
      const seq = Number(data.seq);
      if (!Number.isFinite(seq) || seq <= player.lastSeq) {
        return this.send(ws, { type: "error", error: "stale-seq" });
      }
      player.lastSeq = seq;

      const before = this.room.monster.hp;
      const damage = Math.min(POC_ATTACK_DAMAGE, before);
      this.room.monster.hp = Math.max(0, before - damage);
      this.room.eventSeq++;
      const event = {
        id: this.room.eventSeq,
        kind: "attack",
        slot: player.slot,
        damage,
        hp: this.room.monster.hp,
        at: Date.now()
      };
      if (this.room.monster.hp === 0) this.room.status = "clear";

      await this.persist();
      this.broadcast({ type: "event", event });
      this.broadcastState();
      return;
    }

    this.send(ws, { type: "error", error: "unknown-message" });
  }

  async webSocketClose(ws, code, reason) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (player) {
      player.connected = false;
      if (this.room.status === "waiting" && this.room.hostSession === player.session) {
        const nextHost = this.room.participants.find((p) => p.connected && p.session !== player.session);
        if (nextHost) this.room.hostSession = nextHost.session;
      }
      await this.persist();
      this.broadcastState();
    }
    try { ws.close(code, reason); } catch (_) {}
  }

  async webSocketError(ws) {
    const attachment = ws.deserializeAttachment?.() || {};
    const player = this.room?.participants.find((p) => p.session === attachment.session);
    if (player) {
      player.connected = false;
      await this.persist();
      this.broadcastState();
    }
  }

  canStart() {
    const humans = this.room?.participants || [];
    return humans.length >= 2 && humans.every((p) => p.connected && p.ready);
  }

  publicState() {
    if (!this.room) return null;
    return {
      code: this.room.code,
      status: this.room.status,
      revision: this.room.revision,
      serverTime: Date.now(),
      hostSlot: this.room.participants.find((p) => p.session === this.room.hostSession)?.slot || null,
      canStart: this.canStart(),
      participants: this.room.participants.map((p) => ({
        slot: p.slot,
        nickname: p.nickname,
        classId: p.classId,
        ready: p.ready,
        connected: p.connected,
        host: p.session === this.room.hostSession
      })),
      monster: this.room.monster ? { ...this.room.monster } : null
    };
  }

  async persist() {
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
    this.broadcast({ type: "state", state: this.publicState() });
  }
}
