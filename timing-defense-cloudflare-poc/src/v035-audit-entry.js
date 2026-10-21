import worker, { TimingDefenseRoom } from "./v035-entry.js";

// Exact legacy-v0.35 contract guards applied after the bounded v0.35 extension.
// 1) Legacy AI interval: rogue=1150, tank=1650, all other classes=1400.
// 2) shop-next publishes room.status=starting + room.startAt.
// 3) Stage 2 closes with room.status=stage2-clear and the existing stage-clear event grammar.
// 4) Public run state must expose the authoritative run.stage (v0.33 hardcoded stage: 1).
// 5) Result-board contribution data must come from the authoritative room/run state.
// 6) KILL COIN is cumulative monster-kill reward, independent of wallet spending / stage-clear rewards.

const KILL_REWARD = { grunt: 6, runner: 5 };

const baseProcessAt = TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt = function(at) {
  const rewrites = [];
  for (const ai of this.room?.run?.ai || []) {
    if (ai.cls === "archer" || ai.cls === "mage") {
      rewrites.push([ai, ai.cls]);
      ai.cls = "__legacy_default__";
    }
  }
  try {
    return baseProcessAt.call(this, at);
  } finally {
    for (const [ai, cls] of rewrites) ai.cls = cls;
  }
};

const baseBeginStage = TimingDefenseRoom.prototype.beginStage;
TimingDefenseRoom.prototype.beginStage = function(stage, at) {
  const out = baseBeginStage.call(this, stage, at);
  if (stage === 2 && this.room?.run) {
    this.room.status = "starting";
    this.room.startAt = this.room.run.startAt;
    const e = this.room.run.events?.[this.room.run.events.length - 1];
    if (e?.type === "stage-starting") e.combatAt = this.room.run.combatAt;
  }
  return out;
};

const baseApplyDamage = TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage = function(monster, damage, slot, tier, at, knock = true, source = "hit", proc = false) {
  const run = this.room?.run;
  const monsterType = monster?.type || "grunt";
  const reward = KILL_REWARD[monsterType] || 0;
  const ai = source === "ai" ? run?.ai?.find(a => a.slot === slot) : null;
  const human = run?.players?.find(p => p.slot === slot) || null;
  const result = baseApplyDamage.call(this, monster, damage, slot, tier, at, knock, source, proc);

  if (human && result?.killed) {
    human.killCoinEarned = (human.killCoinEarned || 0) + reward;
  }
  if (ai && result) {
    ai.damage = (ai.damage || 0) + (result.actual || 0);
    if (result.killed) {
      ai.kills = (ai.kills || 0) + 1;
      ai.killCoinEarned = (ai.killCoinEarned || 0) + reward;
    }
  }
  return result;
};

const basePlayerPublic = TimingDefenseRoom.prototype.playerPublic;
TimingDefenseRoom.prototype.playerPublic = function(player) {
  const out = basePlayerPublic.call(this, player);
  out.killCoin = player.killCoinEarned || 0;
  return out;
};

const baseRunPublic = TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic = function(at) {
  const out = baseRunPublic.call(this, at);
  const run = this.room?.run;
  if (out && run) {
    out.stage = run.stage || 1;
    out.status = run.status;
    out.startAt = run.startAt;
    out.combatAt = run.combatAt;
    out.ai = (run.ai || []).map(a => ({
      slot: a.slot,
      cls: a.cls,
      kills: a.kills || 0,
      damage: a.damage || 0,
      killCoin: a.killCoinEarned || 0,
      level: 1,
      comboPeak: 0
    }));
  }
  return out;
};

const baseCheckEnd = TimingDefenseRoom.prototype.checkEnd;
TimingDefenseRoom.prototype.checkEnd = function(at) {
  const out = baseCheckEnd.call(this, at);
  const run = this.room?.run;
  if (run?.status === "stage2-clear") {
    this.room.status = "stage2-clear";
    const e = run.events?.[run.events.length - 1];
    if (e?.type === "stage2-clear") e.type = "stage-clear";
  }
  return out;
};

const auditedWorker = {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/api/health") {
      return new Response(JSON.stringify({
        ok: true,
        service: "timing-defense-cloudflare-v035-parity",
        version: "0.35-cf.5",
        transport: "websocket-hibernation",
        authority: "durable-object-event-driven-stage2-shop",
        presentation: "v034-render-parity-retained-authoritative-human-results",
        locationHint: "apac-ne",
        scope: "room-stage1-shop-stage2-reconnect",
        fix: "authoritative-participants-contribution-killcoin"
      }), {
        status: 200,
        headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
      });
    }
    return worker.fetch(request, env, ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
