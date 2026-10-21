import worker, { TimingDefenseRoom } from "./v038-entry.js";
import { runV036SelfTest } from "./v036-selftest.js";
import { runV037SelfTest } from "./v037-selftest.js";
import { runV037WallSelfTest } from "./v037-wall-selftest.js";
import { runV038SelfTest } from "./v038-selftest.js";

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}
function failedBlock(name,error){
  return{ok:false,passed:0,total:0,failed:[`${name}_EXCEPTION`],error:String(error?.stack||error)};
}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v038-party-event-kernel",
        version:"0.38-cf.3",
        transport:"websocket-hibernation-per-socket-event-cursor",
        authority:"durable-object-stage1-stage3-lv6",
        validation:"v036-v037-regression-plus-event-kernel-and-larger-party-live-sim",
        eventDelivery:{history:512,mode:"per-socket-monotonic-batch",gap:"explicit"},
        n3:"option-b-frozen-not-yet-enabled",
        stage4:"blocked",
        scope:"slice-c-event-kernel-larger-party-validation",
        fix:"validation-result-init-plus-diagnostics-isolation"
      });
    }
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v038-slice-c"){
      let v036,v037,wall,stream;
      try{v036=runV036SelfTest(TimingDefenseRoom)}catch(e){v036=failedBlock('V036',e)}
      try{v037=await runV037SelfTest(TimingDefenseRoom)}catch(e){v037=failedBlock('V037',e)}
      try{wall=runV037WallSelfTest(TimingDefenseRoom)}catch(e){wall=failedBlock('WALL',e)}
      try{stream=runV038SelfTest(TimingDefenseRoom)}catch(e){stream=failedBlock('EVENT_KERNEL',e)}
      const result={
        ok:!!(v036.ok&&v037.ok&&wall.ok&&stream.ok),version:"0.38-cf.3-diagnostics",
        v036Regression:{ok:v036.ok,passed:v036.passed,total:v036.total,failed:v036.failed,error:v036.error||null},
        v037Regression:{ok:v037.ok,passed:v037.passed,total:v037.total,failed:v037.failed,error:v037.error||null},
        wall:{ok:wall.ok,passed:wall.passed,total:wall.total,failed:wall.failed,error:wall.error||null},
        eventKernel:{ok:stream.ok,passed:stream.passed,total:stream.total,failed:stream.failed,error:stream.error||null,checks:stream.checks||[]}
      };
      return json(result,result.ok?200:500);
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };