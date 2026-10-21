import worker, { TimingDefenseRoom } from "./v037-entry.js";
import { runV036SelfTest } from "./v036-selftest.js";
import { runV037SelfTest } from "./v037-selftest.js";

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v037-stage3",
        version:"0.37-cf.1",
        transport:"websocket-hibernation",
        authority:"durable-object-stage1-stage3-lv6",
        presentation:"generic-stage-flow-stage3-brute",
        validation:"v036-regression-plus-stage3-deterministic-and-live-multiclient",
        locationHint:"apac-ne",
        scope:"stage1-stage3-brute-team-shop",
        stage3:{count:12,gap:980,composition:{grunt:.44,runner:.34,brute:.22}},
        stage4:"blocked",
        n1:"legacy-heavy-xp-restored",
        n2:"legacy-ai-stage-damage-scaling-restored",
        n3:"deferred-explicit-discussion-required"
      });
    }
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v037-slice-b"){
      const v036=runV036SelfTest(TimingDefenseRoom);
      const v037=await runV037SelfTest(TimingDefenseRoom);
      const result={
        ok:!!(v036.ok&&v037.ok),version:"0.37-cf.1-diagnostics",
        v036Regression:{ok:v036.ok,passed:v036.passed,total:v036.total,failed:v036.failed,checks:v036.checks},
        stage3:{ok:v037.ok,passed:v037.passed,total:v037.total,failed:v037.failed,checks:v037.checks}
      };
      return json(result,result.ok?200:500);
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };