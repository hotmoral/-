import worker, { TimingDefenseRoom } from "./index.js";

const baseWebSocketMessage = TimingDefenseRoom.prototype.webSocketMessage;
TimingDefenseRoom.prototype.webSocketMessage = async function(ws, message) {
  if (this.room?.run) {
    const now = Date.now();
    const advanced = this.advanceTo(now);
    if (advanced) {
      await this.persist();
      this.broadcastState(now);
      await this.scheduleNext();
    }
  }
  return baseWebSocketMessage.call(this, ws, message);
};

export default worker;
export { TimingDefenseRoom };
