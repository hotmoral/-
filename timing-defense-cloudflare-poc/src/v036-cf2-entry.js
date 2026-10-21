import worker, { TimingDefenseRoom } from "./v036-entry.js";

// v0.36 cf.2: Slice A client-authority hardening marker.
// Server combat formulas remain the approved cf.1 Slice A formulas.
const cf2Worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return new Response(JSON.stringify({
        ok:true,
        service:"timing-defense-cloudflare-v036-slice-a",
        version:"0.36-cf.2",
        transport:"websocket-hibernation",
        authority:"durable-object-stage1-stage2-lv6",
        presentation:"authoritative-secondary-vfx-reconnect-floor-hardened",
        locationHint:"apac-ne",
        scope:"stage1-stage2-n1-n2-lv6-authority",
        n1:"legacy-heavy-xp-restored",
        n2:"legacy-ai-stage-damage-scaling-restored",
        n3:"deferred-explicit-discussion-required",
        fix:"rogue-local-secondary-mutation-blocked-secondary-vfx-event-floor"
      }),{status:200,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
    }
    return worker.fetch(request,env,ctx);
  }
};

export default cf2Worker;
export { TimingDefenseRoom };
