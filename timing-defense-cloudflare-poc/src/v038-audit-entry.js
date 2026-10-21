import worker, { TimingDefenseRoom } from "./v038-entry.js";
import { runV036SelfTest } from "./v036-selftest.js";
import { runV037SelfTest } from "./v037-selftest.js";
import { runV037WallSelfTest } from "./v037-wall-selftest.js";
import { runV038SelfTest } from "./v038-selftest.js";

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v038-party-event-kernel",
        version:"0.38-cf.2",
        transport:"websocket-hibernation-per-socket-event-cursor",
        authority:"durable-object-stage1-stage3-lv6",
        validation:"v036-v037-regression-plus-event-kernel-and-larger-party-live-sim",
        eventDelivery:{history:512,mode:"per-socket-monotonic-batch",gap:"explicit"},
        n3:"option-b-frozen-not-yet-enabled",
        stage4:"blocked",
        scope:"slice-c-event-kernel-larger-party-validation",
        fix:"event-initialization-normalization"
      });
    }
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v038-slice-c"){
      const v036=runV036SelfTest(TimingDefenseRoom);
      const v037=await runV037SelfTest(TimingDefenseRoom);
      const wall=runV037WallSelfTest(TimingDefenseRoom);
      const stream=runV038SelfTest(TimingDefenseRoom);
      const result={
        ok:!!(v036.ok&&v037.ok&&wall.ok&&stream.ok),version:"0.38-cf.2-diagnostics",
        v036Regression:{ok:v036.ok,passed:v036.passed,total:v036.total,failed:v036.failed},
        v037Regression:{ok:v037.ok,passed:v037.passed,total:v037.total,failed:v037.failed},
        wall:{ok:wall.ok,passed:wall.passed,total:wall.total,failed:wall.failed},
        eventKernel:{ok:stream.ok,passed:stream.passed,total:stream.total,failed:stream.failed,checks:stream.checks}
      };
      return json(result,result.ok?200:500);
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
