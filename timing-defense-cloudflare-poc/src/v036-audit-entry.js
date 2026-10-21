import worker, { TimingDefenseRoom } from "./v036-cf2-entry.js";
import { runV036SelfTest } from "./v036-selftest.js";

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v036-slice-a",
        version:"0.36-cf.3",
        transport:"websocket-hibernation",
        authority:"durable-object-stage1-stage2-lv6",
        presentation:"authoritative-secondary-vfx-reconnect-floor-hardened",
        validation:"deterministic-server-client-multiclient-harness",
        locationHint:"apac-ne",
        scope:"stage1-stage2-n1-n2-lv6-authority",
        n1:"legacy-heavy-xp-restored",
        n2:"legacy-ai-stage-damage-scaling-restored",
        n3:"deferred-explicit-discussion-required",
        fix:"rogue-local-secondary-mutation-blocked-secondary-vfx-event-floor"
      });
    }
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v036-slice-a"){
      const result=runV036SelfTest(TimingDefenseRoom);
      return json(result,result.ok?200:500);
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
