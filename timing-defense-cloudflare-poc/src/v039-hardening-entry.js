import worker, { TimingDefenseRoom, allocateBudget, milestonesCrossed, budgetFor } from "./v039-entry.js";

// N3 queues are combat-only. Clear any delayed Rogue milestone daggers whenever
// the authoritative run leaves combat so a past due queue item can never keep
// the Durable Object alarm scheduler alive in Shop/Game Over.
const baseEnterShop=TimingDefenseRoom.prototype.enterShop;
TimingDefenseRoom.prototype.enterShop=function(at){
  const out=baseEnterShop.call(this,at);
  if(this.room?.run)this.room.run.n3Queue=[];
  return out;
};

const baseCheckEnd=TimingDefenseRoom.prototype.checkEnd;
TimingDefenseRoom.prototype.checkEnd=function(at){
  const ended=baseCheckEnd.call(this,at);
  const run=this.room?.run;
  if(run&&run.status!=="combat"&&Array.isArray(run.n3Queue))run.n3Queue=[];
  return ended;
};

export default worker;
export { TimingDefenseRoom, allocateBudget, milestonesCrossed, budgetFor };
