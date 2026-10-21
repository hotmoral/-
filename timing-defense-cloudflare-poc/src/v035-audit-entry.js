import worker, { TimingDefenseRoom } from "./v035-entry.js";

// Exact legacy-v0.35 contract guards applied after the bounded v0.35 extension.
// 1) Legacy AI interval: rogue=1150, tank=1650, all other classes=1400.
// 2) shop-next publishes room.status=starting + room.startAt.
// 3) Stage 2 closes with room.status=stage2-clear and the existing stage-clear event grammar.

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

export default worker;
export { TimingDefenseRoom };
