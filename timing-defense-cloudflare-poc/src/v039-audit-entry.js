import worker, { TimingDefenseRoom } from "./v039-hardening-entry.js";
import { runV039SelfTest } from "./v039-selftest.js";

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-cloudflare-v039-n3-authority",version:"0.39-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",authority:"durable-object-stage1-stage3-lv6-n3",
      n3:{status:"option-b-enabled",milestones:[5,10,20,30,"every+10"],budgets:[60,90,150,210],knockback:"normal-equivalent",recursive:false},
      validation:"v038-regression-plus-n3-contract-plus-four-human-milestone-stress",stage4:"blocked",scope:"n3-authority-validation"
    });
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v039-n3"){
      try{
        const n3=runV039SelfTest(TimingDefenseRoom);
        return json({ok:n3.ok,version:"0.39-cf.1-diagnostics",n3},n3.ok?200:500);
      }catch(error){return json({ok:false,version:"0.39-cf.1-diagnostics",error:String(error?.stack||error)},500)}
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
